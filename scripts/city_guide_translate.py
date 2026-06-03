# -*- coding: utf-8 -*-
"""On-demand EN↔RU translation for city guide editions (cached)."""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_core import is_substantive_text

_CACHE_VERSION = 1
_CYRILLIC_RE = re.compile(r"[\u0400-\u04FF]")
_singleton: EditionTranslator | None = None
logger = logging.getLogger(__name__)


class OllamaFatalError(RuntimeError):
    """Non-recoverable Ollama error (suspend further attempts)."""



def has_cyrillic(text: str) -> bool:
    return bool(_CYRILLIC_RE.search(text))


def _text_for_edition(text: str, edition: str) -> bool:
    from scripts.city_guide_narrative import text_for_edition

    return text_for_edition(text, edition)


def _load_dotenv() -> None:
    try:
        from dotenv import load_dotenv as _ld
    except ImportError:
        return
    _ld(_PROJECT_ROOT / ".env")
    _ld(_SCRIPT_DIR / ".env")


def _load_dotenv_once() -> None:
    if getattr(_load_dotenv_once, "_done", False):
        return
    _load_dotenv()
    _load_dotenv_once._done = True  # type: ignore[attr-defined]


def _cache_path(project_root: Path | None = None) -> Path:
    root = project_root or _PROJECT_ROOT
    cache_dir = root / ".cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / "city_guide_translate.json"


def _cache_key(text: str, *, src: str, dst: str, kind: str) -> str:
    payload = "{}|{}|{}|{}".format(_CACHE_VERSION, src, dst, kind)
    digest = hashlib.sha256(
        (payload + "\n" + text).encode("utf-8"),
    ).hexdigest()
    return digest


class EditionTranslator:
    """Translate guide strings between en and ru with a JSON disk cache."""

    def __init__(
        self,
        *,
        project_root: Path | None = None,
        enabled: bool = True,
        cache_path: Path | None = None,
    ) -> None:
        self._root = project_root or _PROJECT_ROOT
        self._enabled = enabled
        self._cache_file = cache_path or _cache_path(self._root)
        self._mem: dict[str, str] = {}
        self._load_cache()

    def _load_cache(self) -> None:
        if not self._cache_file.is_file():
            return
        try:
            raw = json.loads(self._cache_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return
        if isinstance(raw, dict):
            for key, val in raw.items():
                if isinstance(key, str) and isinstance(val, str):
                    self._mem[key] = val

    def _persist(self) -> None:
        self._cache_file.write_text(
            json.dumps(self._mem, ensure_ascii=False, indent=0),
            encoding="utf-8",
        )

    def translate(
        self,
        text: str,
        *,
        src: str,
        dst: str,
        kind: str = "prose",
    ) -> str | None:
        """Return translated text or None when translation is unavailable."""
        if not self._enabled:
            return None
        s = str(text).strip()
        if not s or src == dst:
            return s if _text_for_edition(s, dst) else None
        if _text_for_edition(s, dst):
            return s
        key = _cache_key(s, src=src, dst=dst, kind=kind)
        if key in self._mem:
            cached = self._mem[key].strip()
            return cached if cached and _text_for_edition(cached, dst) else None
        translated = self._call_backend(s, src=src, dst=dst, kind=kind)
        if not translated:
            return None
        translated = translated.strip()
        if not _text_for_edition(translated, dst):
            return None
        self._mem[key] = translated
        try:
            self._persist()
        except OSError:
            pass
        return translated

    def _call_backend(
        self,
        text: str,
        *,
        src: str,
        dst: str,
        kind: str,
    ) -> str | None:
        if os.environ.get("OLLAMA_HOST") or os.environ.get("USE_OLLAMA") == "1":
            try:
                return self._ollama(text, src=src, dst=dst, kind=kind)
            except Exception:
                pass
        if os.environ.get("OPENAI_API_KEY", "").strip():
            try:
                return self._openai(text, src=src, dst=dst, kind=kind)
            except Exception:
                pass
        return None

    def _prompt(self, text: str, *, src: str, dst: str, kind: str) -> str:
        lang = {"en": "English", "ru": "Russian"}
        src_name = lang.get(src, src)
        dst_name = lang.get(dst, dst)
        if kind == "name":
            return (
                "Translate this place name from {src} to {dst}.\n"
                "- Use the established name in the destination language.\n"
                "- Return ONLY the translated name.\n\n"
                "{text}"
            ).format(src=src_name, dst=dst_name, text=text)
        return (
            "Translate this city-guide passage from {src} to {dst}.\n"
            "- Keep dates, numbers, and proper names accurate.\n"
            "- Guidebook tone; do not add facts.\n"
            "- Output plain text only.\n\n"
            "{text}"
        ).format(src=src_name, dst=dst_name, text=text)

    def _ollama(
        self,
        text: str,
        *,
        src: str,
        dst: str,
        kind: str,
    ) -> str | None:
        import requests

        host = os.environ.get("OLLAMA_HOST") or "http://127.0.0.1:11434"
        url = host.rstrip("/") + "/api/generate"
        model = os.environ.get("OLLAMA_MODEL") or "llama3.1"
        payload = {
            "model": model,
            "prompt": self._prompt(text, src=src, dst=dst, kind=kind),
            "stream": False,
        }
        timeout = 180 if kind == "prose" else 60

        last_err: Exception | None = None
        for attempt in range(4):
            try:
                resp = requests.post(
                    url,
                    json=payload,
                    timeout=timeout,
                )
                if resp.status_code >= 500:
                    raise OllamaFatalError(
                        "Ollama server error {} for {}".format(
                            resp.status_code,
                            url,
                        ),
                    )
                resp.raise_for_status()
                data = resp.json()
                out = str(data.get("response") or "").strip()
                return out or None
            except (
                OllamaFatalError,
                requests.RequestException,
                OSError,
                TimeoutError,
                json.JSONDecodeError,
                ValueError,
            ) as exc:
                last_err = exc
                if isinstance(exc, OllamaFatalError):
                    logger.warning("%s", exc)
                    raise
                if attempt < 3:
                    time.sleep(2.0 * (attempt + 1))
                    continue
                logger.warning("Ollama translate failed after retries: %s", exc)
                return None

        logger.warning("Ollama translate failed: %s", last_err)
        return None

    def _openai(
        self,
        text: str,
        *,
        src: str,
        dst: str,
        kind: str,
    ) -> str | None:
        import urllib.request

        model = os.environ.get("OPENAI_MODEL") or "gpt-4o-mini"
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": self._prompt(text, src=src, dst=dst, kind=kind),
                },
            ],
            "max_tokens": 900 if kind == "prose" else 80,
        }
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": "Bearer "
                + os.environ.get("OPENAI_API_KEY", "").strip(),
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        choices = result.get("choices") or []
        if not choices:
            return None
        return str(
            (choices[0].get("message") or {}).get("content") or "",
        ).strip() or None


class OllamaOnlyEditionTranslator(EditionTranslator):
    """Translate via local Ollama only (sparse-fill cross-edition fallback)."""

    def _call_backend(
        self,
        text: str,
        *,
        src: str,
        dst: str,
        kind: str,
    ) -> str | None:
        if not (
            os.environ.get("OLLAMA_HOST")
            or os.environ.get("USE_OLLAMA") == "1"
        ):
            return None
        try:
            return self._ollama(text, src=src, dst=dst, kind=kind)
        except OllamaFatalError:
            raise
        except Exception:
            return None


_ollama_only_singleton: OllamaOnlyEditionTranslator | None = None


def get_ollama_only_translator(
    project_root: Path | None = None,
) -> OllamaOnlyEditionTranslator | None:
    """Ollama-only translator; None when Ollama is not configured."""
    global _ollama_only_singleton
    _load_dotenv_once()
    if not (
        os.environ.get("OLLAMA_HOST")
        or os.environ.get("USE_OLLAMA") == "1"
    ):
        return None
    if _ollama_only_singleton is None:
        _ollama_only_singleton = OllamaOnlyEditionTranslator(
            project_root=project_root,
        )
    return _ollama_only_singleton


def opposite_edition(edition: str) -> str:
    return "ru" if edition == "en" else "en"


def edition_of_text(text: str) -> str | None:
    s = str(text).strip()
    if not s:
        return None
    if _text_for_edition(s, "ru") and not _text_for_edition(s, "en"):
        return "ru"
    if _text_for_edition(s, "en") and not _text_for_edition(s, "ru"):
        return "en"
    if has_cyrillic(s):
        return "ru"
    if _CYRILLIC_RE.search(s):
        return "ru"
    return "en"


def get_edition_translator(
    project_root: Path | None = None,
) -> EditionTranslator | None:
    """Shared translator; None when CITY_GUIDE_NO_TRANSLATE=1."""
    global _singleton
    _load_dotenv_once()
    if os.environ.get("CITY_GUIDE_NO_TRANSLATE") == "1":
        return None
    if _singleton is None:
        _singleton = EditionTranslator(project_root=project_root)
    return _singleton


def set_edition_translator(translator: EditionTranslator | None) -> None:
    """Test hook: inject or reset the shared translator."""
    global _singleton
    _singleton = translator


def translate_for_edition(
    text: str,
    edition: str,
    *,
    kind: str = "prose",
    translator: EditionTranslator | None = None,
) -> str | None:
    s = str(text).strip()
    if not s:
        return None
    if _text_for_edition(s, edition):
        return s
    src = edition_of_text(s)
    if not src or src == edition:
        return None
    tr = translator if translator is not None else get_edition_translator()
    if tr is None:
        return None
    return tr.translate(s, src=src, dst=edition, kind=kind)
