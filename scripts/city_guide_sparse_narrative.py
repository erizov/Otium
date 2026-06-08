# -*- coding: utf-8 -*-
"""Detect and fill sparse EN/RU place narratives before guide builds."""

from __future__ import annotations

import json
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_core import is_substantive_text
from scripts.city_guide_naming import clean_wikimedia_display_title
from scripts.city_guide_narrative import (
    is_usable_narrative_text,
    polish_display_title,
    text_for_edition,
)
from scripts.city_guide_registry_common import pdf_expand_sidecar_paths
from scripts.city_guide_translate import (
    EditionTranslator,
    get_ollama_only_translator,
    OllamaFatalError,
    opposite_edition,
    translate_for_edition,
)
from scripts.enrich_en_places_gigachat import (
    _apply_enrichment as apply_en_fields,
    _build_prompt as build_en_openai_prompt,
)
from scripts.enrich_places_gigachat_common import extract_json, load_dotenv
from scripts.enrich_ru_places_gigachat import (
    _apply_enrichment as apply_ru_fields,
    _build_prompt as build_ru_gigachat_prompt,
    _load_place_details,
)
from scripts.gigachat_client import ask_gigachat
from scripts.enrich_places_gigachat_common import (
    gigachat_failed,
    gigachat_refusal,
)

_HTML_TAG_RE = re.compile(r"<[^>]+>")


def _progress(message: str) -> None:
    print(message, flush=True)


@dataclass
class _ProviderState:
    consecutive_failures: int = 0
    suspended_places_left: int = 0


class ProviderCircuitBreaker:
    """
    Suspend flaky providers after repeated failures.

    Rule: if a provider fails 3 times in a row (on different places),
    suspend it for the next 100 places.
    """

    def __init__(
        self,
        *,
        fail_threshold: int = 3,
        suspend_places: int = 1000,
    ) -> None:
        self._fail_threshold = int(fail_threshold)
        self._suspend_places = int(suspend_places)
        self._states: dict[str, _ProviderState] = {}

    def on_new_place(self) -> None:
        for state in self._states.values():
            if state.suspended_places_left > 0:
                state.suspended_places_left -= 1

    def allowed(self, provider: str) -> bool:
        state = self._states.get(provider)
        if state is None:
            return True
        return state.suspended_places_left <= 0

    def record_success(self, provider: str) -> None:
        state = self._states.setdefault(provider, _ProviderState())
        state.consecutive_failures = 0

    def record_failure(self, provider: str) -> None:
        state = self._states.setdefault(provider, _ProviderState())
        state.consecutive_failures += 1
        if state.consecutive_failures < self._fail_threshold:
            return
        state.consecutive_failures = 0
        state.suspended_places_left = self._suspend_places

    def suspend_forever(self, provider: str) -> None:
        state = self._states.setdefault(provider, _ProviderState())
        state.consecutive_failures = 0
        state.suspended_places_left = 10**9

    def suspension_left(self, provider: str) -> int:
        state = self._states.get(provider)
        if state is None:
            return 0
        return max(0, int(state.suspended_places_left))


def _json_has_usable_narrative_for_edition(
    place: Mapping[str, Any],
    edition: str,
) -> bool:
    """Fast JSON check — no live translation (avoids slow Ollama during scan)."""
    for base in ("description", "history", "significance"):
        for key in _field_keys_for_edition(edition, base):
            text = _read_field(place, key)
            if (
                text
                and is_usable_narrative_text(text)
                and text_for_edition(text, edition)
            ):
                return True
    for key in _field_keys_for_edition(edition, "facts"):
        raw = place.get(key)
        if not isinstance(raw, list):
            continue
        for item in raw:
            text = str(item).strip()
            if (
                is_usable_narrative_text(text)
                and text_for_edition(text, edition)
            ):
                return True
    return False


def _opposite_has_usable_narrative(
    place: Mapping[str, Any],
    edition: str,
) -> bool:
    alt = opposite_edition(edition)
    return _json_has_usable_narrative_for_edition(place, alt)


def place_edition_needs_fill(
    place: Mapping[str, Any],
    edition: str,
) -> bool:
    """True when this edition lacks substantive narrative fields in JSON."""
    return not _json_has_usable_narrative_for_edition(place, edition)


def _english_place_name(place: Mapping[str, Any]) -> str:
    for key in ("name_en", "name", "subtitle_en"):
        value = polish_display_title(str(place.get(key) or ""))
        if value and not re.search(r"[\u0400-\u04FF]", value):
            return value
    return ""


def _russian_place_name(place: Mapping[str, Any]) -> str:
    for key in ("name_ru", "name", "name_en"):
        value = str(place.get(key) or "").strip()
        if value:
            return polish_display_title(value)
    return ""


def _field_keys_for_edition(edition: str, base: str) -> tuple[str, ...]:
    if edition == "ru":
        return (f"{base}_ru", base)
    return (f"{base}_en", base)


def _opposite_field_keys(edition: str, base: str) -> tuple[str, ...]:
    alt = opposite_edition(edition)
    return _field_keys_for_edition(alt, base)


def _read_field(place: Mapping[str, Any], key: str) -> str | None:
    raw = place.get(key)
    if raw is None:
        return None
    text = str(raw).strip()
    return text if is_substantive_text(text) else None


def _edition_has_usable_field(
    place: Mapping[str, Any],
    edition: str,
    base: str,
) -> bool:
    from scripts.city_guide_narrative import text_for_edition

    for key in _field_keys_for_edition(edition, base):
        text = _read_field(place, key)
        if text and is_usable_narrative_text(text):
            if text_for_edition(text, edition):
                return True
    return False


def _best_opposite_source(
    place: Mapping[str, Any],
    edition: str,
    base: str,
) -> str | None:
    from scripts.city_guide_narrative import text_for_edition

    alt = opposite_edition(edition)
    for key in _opposite_field_keys(edition, base):
        text = _read_field(place, key)
        if not text:
            continue
        if is_usable_narrative_text(text) and text_for_edition(text, alt):
            return text
    return None


def _write_text_field(
    place: dict[str, Any],
    edition: str,
    base: str,
    value: str,
) -> None:
    if not is_usable_narrative_text(value):
        return
    if edition == "ru":
        if _read_field(place, f"{base}_ru") is None:
            place[f"{base}_ru"] = value
        elif not is_usable_narrative_text(str(place.get(base) or "")):
            place[base] = value
    else:
        if _read_field(place, f"{base}_en") is None:
            place[f"{base}_en"] = value
        elif not is_usable_narrative_text(str(place.get(base) or "")):
            place[base] = value


def fill_edition_from_opposite(
    place: dict[str, Any],
    edition: str,
    *,
    translator: EditionTranslator | None = None,
    breaker: ProviderCircuitBreaker | None = None,
    delay: float = 0.0,
) -> bool:
    """Copy narrative fields from the other edition via Ollama translator."""
    tr = translator if translator is not None else get_ollama_only_translator()
    if tr is None:
        return False
    changed = False
    for base in ("description", "history", "significance"):
        if _edition_has_usable_field(place, edition, base):
            continue
        src = _best_opposite_source(place, edition, base)
        if not src:
            continue
        try:
            translated = translate_for_edition(
                src,
                edition,
                kind="prose",
                translator=tr,
            )
        except OllamaFatalError as exc:
            _progress("    Ollama fatal: {}".format(exc))
            if breaker is not None:
                breaker.suspend_forever("ollama_translate")
            return changed
        if not translated or not is_usable_narrative_text(translated):
            if breaker is not None:
                breaker.record_failure("ollama_translate")
            continue
        _write_text_field(place, edition, base, translated)
        changed = True
        if breaker is not None:
            breaker.record_success("ollama_translate")
        if delay > 0:
            time.sleep(delay)

    if not _edition_has_usable_field(place, edition, "facts"):
        src_items: list[str] = []
        for key in _opposite_field_keys(edition, "facts"):
            raw = place.get(key)
            if not isinstance(raw, list):
                continue
            for item in raw:
                text = str(item).strip()
                if is_usable_narrative_text(text):
                    src_items.append(text)
            if src_items:
                break
        out: list[str] = []
        for text in src_items[:6]:
            try:
                translated = translate_for_edition(
                    text,
                    edition,
                    kind="prose",
                    translator=tr,
                )
            except OllamaFatalError as exc:
                _progress("    Ollama fatal: {}".format(exc))
                if breaker is not None:
                    breaker.suspend_forever("ollama_translate")
                return changed
            if translated and is_usable_narrative_text(translated):
                out.append(translated)
                if breaker is not None:
                    breaker.record_success("ollama_translate")
            elif breaker is not None:
                breaker.record_failure("ollama_translate")
            if delay > 0:
                time.sleep(delay)
        if out:
            if edition == "ru":
                place["facts_ru"] = out
            else:
                place["facts"] = out
            changed = True
    return changed


def build_sparse_narrative_prompt(
    place: dict[str, Any],
    city_slug: str,
    edition: str,
) -> str:
    """Prompt for OpenAI or GigaChat; output language matches *edition*."""
    if edition == "ru":
        details = _load_place_details(city_slug).get(
            str(place.get("slug") or ""),
        )
        detail_dict = details if isinstance(details, dict) else None
        base = build_ru_gigachat_prompt(place, city_slug, detail_dict)
        return (
            base
            + "\n\nЯзык ответа: русский. Все строковые поля JSON — "
            "только на русском языке."
        )
    base = build_en_openai_prompt(place, city_slug)
    return (
        base
        + "\n\nOutput language: English. All JSON text fields must be "
        "in English only."
    )


def _apply_edition_enrichment(
    place: dict[str, Any],
    edition: str,
    data: dict[str, Any],
) -> bool:
    if edition == "ru":
        return apply_ru_fields(place, data)
    return apply_en_fields(place, data)


def _place_row_label(place: Mapping[str, Any]) -> str:
    slug = str(place.get("slug") or "").strip()
    if slug:
        return slug
    for key in ("name_en", "name_ru", "name", "subtitle_en"):
        val = str(place.get(key) or "").strip()
        if val:
            return val[:60]
    return "row-without-slug"


def ask_gigachat_place_json(
    prompt: str,
    *,
    model: str = "GigaChat",
) -> dict[str, Any] | None:
    try:
        raw = ask_gigachat(prompt, model=model, max_tokens=1200)
    except RuntimeError as exc:
        _progress("    GigaChat error: {}".format(exc))
        return None
    if gigachat_failed(raw) or gigachat_refusal(raw):
        return None
    return extract_json(raw)


def ask_openai_place_json(
    prompt: str,
    *,
    model: str | None = None,
) -> dict[str, Any] | None:
    """Call OpenAI chat completions; return parsed JSON or None."""
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        return None
    model_name = model or os.environ.get("OPENAI_MODEL") or "gpt-4o-mini"
    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.35,
        "response_format": {"type": "json_object"},
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.HTTPError, urllib.error.URLError, OSError, json.JSONDecodeError):
        return None
    choices = result.get("choices") or []
    if not choices:
        return None
    raw = str((choices[0].get("message") or {}).get("content") or "").strip()
    return extract_json(raw)


def openai_configured() -> bool:
    return bool(os.environ.get("OPENAI_API_KEY", "").strip())


def gigachat_configured() -> bool:
    return bool(os.environ.get("GIGA_AUTH_KEY", "").strip())


def pixabay_configured() -> bool:
    return bool(os.environ.get("PIXABAY_API_KEY", "").strip())


def ollama_configured() -> bool:
    return bool(os.environ.get("OLLAMA_HOST", "").strip()) or (
        os.environ.get("USE_OLLAMA") == "1"
    )


def fill_edition_place(
    place: dict[str, Any],
    city_slug: str,
    edition: str,
    *,
    breaker: ProviderCircuitBreaker | None = None,
    openai_model: str | None = None,
    gigachat_model: str = "GigaChat",
    delay: float = 0.0,
) -> str | None:
    """
    Fill sparse narrative for *edition* (``en`` or ``ru``).

    Order: OpenAI → GigaChat → Pixabay (EN only) → Ollama translate
    from the opposite edition when it has usable text.
    """
    if not place_edition_needs_fill(place, edition):
        return None

    tag = edition.upper()
    prompt = build_sparse_narrative_prompt(place, city_slug, edition)

    if openai_configured():
        if breaker is not None and not breaker.allowed("openai"):
            _progress(
                "    {}: OpenAI suspended for {} places".format(
                    tag, breaker.suspension_left("openai"),
                ),
            )
        else:
            _progress("    {}: OpenAI…".format(tag))
            parsed = ask_openai_place_json(prompt, model=openai_model)
            if (
                parsed
                and not parsed.get("skip")
                and _apply_edition_enrichment(place, edition, parsed)
                and not place_edition_needs_fill(place, edition)
            ):
                if breaker is not None:
                    breaker.record_success("openai")
                return "openai"
            if breaker is not None:
                breaker.record_failure("openai")
            if delay > 0:
                time.sleep(delay)

    if gigachat_configured():
        if breaker is not None and not breaker.allowed("gigachat"):
            _progress(
                "    {}: GigaChat suspended for {} places".format(
                    tag, breaker.suspension_left("gigachat"),
                ),
            )
        else:
            _progress("    {}: GigaChat…".format(tag))
            parsed = ask_gigachat_place_json(prompt, model=gigachat_model)
            if (
                parsed
                and not parsed.get("skip")
                and _apply_edition_enrichment(place, edition, parsed)
                and not place_edition_needs_fill(place, edition)
            ):
                if breaker is not None:
                    breaker.record_success("gigachat")
                return "gigachat"
            if breaker is not None:
                breaker.record_failure("gigachat")
            if delay > 0:
                time.sleep(delay)

    if (
        edition == "en"
        and place_edition_needs_fill(place, "en")
        and pixabay_configured()
    ):
        name = _english_place_name(place)
        city_title = city_slug.replace("_", " ").title()
        if breaker is not None and not breaker.allowed("pixabay"):
            _progress(
                "    EN: Pixabay suspended for {} places".format(
                    breaker.suspension_left("pixabay"),
                ),
            )
        else:
            _progress("    EN: Pixabay hints…")
            hints = fetch_pixabay_hints(name, city_title) if name else None
            if hints:
                _progress(
                    "    EN: Pixabay hints skipped (Colab EN fill)",
                )
            if breaker is not None:
                breaker.record_failure("pixabay")
            if delay > 0:
                time.sleep(delay)

    if (
        place_edition_needs_fill(place, edition)
        and _opposite_has_usable_narrative(place, edition)
        and ollama_configured()
    ):
        opp = opposite_edition(edition).upper()
        if breaker is not None and not breaker.allowed("ollama_translate"):
            _progress(
                "    {}: Ollama translate suspended for {} places".format(
                    tag, breaker.suspension_left("ollama_translate"),
                ),
            )
        else:
            _progress(
                "    {}: Ollama translate from {}…".format(tag, opp),
            )
            if fill_edition_from_opposite(
                place,
                edition,
                translator=get_ollama_only_translator(),
                breaker=breaker,
                delay=delay,
            ) and not place_edition_needs_fill(place, edition):
                if breaker is not None:
                    breaker.record_success("ollama_translate")
                return "translate_{}".format(opposite_edition(edition))

    return None


def fetch_pixabay_hints(
    place_name: str,
    city_title: str,
) -> dict[str, str] | None:
    """
    Pixabay image search — use tags from the top hit as factual hints.

    Requires ``PIXABAY_API_KEY``. Not an LLM; composes minimal EN copy.
    """
    key = os.environ.get("PIXABAY_API_KEY", "").strip()
    if not key or not place_name.strip():
        return None
    query = "{} {}".format(place_name, city_title).strip()[:100]
    params = {
        "key": key,
        "q": query,
        "image_type": "photo",
        "lang": "en",
        "per_page": "5",
        "safesearch": "true",
    }
    url = "https://pixabay.com/api/?" + urllib.parse.urlencode(
        params,
        encoding="utf-8",
    )
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "ExcursionGuide/Pixabay/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            payload = json.loads(resp.read().decode("utf-8", errors="ignore"))
    except (
        urllib.error.HTTPError,
        urllib.error.URLError,
        socket.timeout,
        TimeoutError,
        OSError,
        json.JSONDecodeError,
    ):
        return None
    hits = payload.get("hits") or []
    if not hits:
        return None
    hit = hits[0]
    tags = str(hit.get("tags") or "").strip()
    if not tags:
        return None
    return {
        "tags": tags,
        "page_url": str(hit.get("pageURL") or "").strip(),
    }


def compose_en_from_pixabay_hints(
    place: Mapping[str, Any],
    city_slug: str,
    hints: Mapping[str, str],
) -> dict[str, Any]:
    """Build minimal English narrative JSON from Pixabay tag hints."""
    name = _english_place_name(place) or clean_wikimedia_display_title(
        str(place.get("slug") or "place"),
    )
    city_title = city_slug.replace("_", " ").title()
    category = str(place.get("category") or "landmark").replace("_", " ")
    tag_list = [
        t.strip()
        for t in str(hints.get("tags") or "").split(",")
        if t.strip()
    ][:6]
    tag_phrase = ", ".join(tag_list[:4]) if tag_list else city_title
    description = (
        "{} is a {} in {}.".format(name, category, city_title)
    )
    history = (
        "Public photo archives associate this site with: {}.".format(
            tag_phrase,
        )
    )
    significance = "Worth a stop when exploring {}.".format(city_title)
    facts = [
        "Photo tags: {}.".format(tag_phrase),
    ]
    return {
        "description": description,
        "history": history,
        "significance": significance,
        "facts": facts[:4],
    }


def _city_place_files(project_root: Path, city_slug: str) -> list[Path]:
    data_dir = project_root / city_slug / "data"
    paths: list[Path] = []
    main = data_dir / "{}_places.json".format(city_slug)
    if main.is_file():
        paths.append(main)
    paths.extend(pdf_expand_sidecar_paths(data_dir, city_slug))
    return paths


def process_city_file(
    path: Path,
    city_slug: str,
    *,
    breaker: ProviderCircuitBreaker,
    dry_run: bool,
    limit: int | None,
    openai_model: str | None,
    gigachat_model: str,
    delay: float,
) -> dict[str, int]:
    stats = {
        "en_openai": 0,
        "en_gigachat": 0,
        "en_pixabay": 0,
        "en_translate": 0,
        "ru_openai": 0,
        "ru_gigachat": 0,
        "ru_translate": 0,
        "still_sparse_en": 0,
        "still_sparse_ru": 0,
        "skipped_ok": 0,
    }
    places: list[dict[str, Any]] = json.loads(
        path.read_text(encoding="utf-8"),
    )
    targets = [
        p for p in places
        if place_edition_needs_fill(p, "en")
        or place_edition_needs_fill(p, "ru")
    ]
    if limit is not None:
        targets = targets[:limit]

    if dry_run:
        for place in targets:
            flags = []
            if place_edition_needs_fill(place, "en"):
                flags.append("EN")
            if place_edition_needs_fill(place, "ru"):
                flags.append("RU")
            print("[dry-run] {} / {} needs {}".format(
                path.name, _place_row_label(place), "+".join(flags),
            ))
        return stats

    changed_file = False
    for place in targets:
        breaker.on_new_place()
        snapshot = json.dumps(place, sort_keys=True, ensure_ascii=False)
        label = _place_row_label(place)
        needs_en = place_edition_needs_fill(place, "en")
        needs_ru = place_edition_needs_fill(place, "ru")
        if not needs_en and not needs_ru:
            stats["skipped_ok"] += 1
            continue

        _progress("{} / {}: filling…".format(path.name, label))

        try:
            # RU first so EN can Ollama-translate from freshly filled RU fields.
            if needs_ru:
                method = fill_edition_place(
                    place,
                    city_slug,
                    "ru",
                    breaker=breaker,
                    openai_model=openai_model,
                    gigachat_model=gigachat_model,
                    delay=delay,
                )
                if method == "openai":
                    stats["ru_openai"] += 1
                    print("{} / {}: RU via OpenAI".format(path.name, label))
                elif method == "gigachat":
                    stats["ru_gigachat"] += 1
                    print("{} / {}: RU via GigaChat".format(path.name, label))
                elif method == "translate_en":
                    stats["ru_translate"] += 1
                    print(
                        "{} / {}: RU via EN translate".format(path.name, label),
                    )
                elif place_edition_needs_fill(place, "ru"):
                    stats["still_sparse_ru"] += 1
                    print("{} / {}: RU still sparse".format(path.name, label))

            if place_edition_needs_fill(place, "en"):
                method = fill_edition_place(
                    place,
                    city_slug,
                    "en",
                    breaker=breaker,
                    openai_model=openai_model,
                    gigachat_model=gigachat_model,
                    delay=delay,
                )
                if method == "openai":
                    stats["en_openai"] += 1
                    print("{} / {}: EN via OpenAI".format(path.name, label))
                elif method == "gigachat":
                    stats["en_gigachat"] += 1
                    print("{} / {}: EN via GigaChat".format(path.name, label))
                elif method == "pixabay":
                    stats["en_pixabay"] += 1
                    print(
                        "{} / {}: EN via Pixabay hints".format(path.name, label),
                    )
                elif method == "translate_ru":
                    stats["en_translate"] += 1
                    print(
                        "{} / {}: EN via RU translate".format(
                            path.name, label,
                        ),
                    )
                elif place_edition_needs_fill(place, "en"):
                    stats["still_sparse_en"] += 1
                    print("{} / {}: EN still sparse".format(path.name, label))
        except Exception as exc:
            print(
                "{} / {}: ERROR — {}".format(path.name, label, exc),
                file=sys.stderr,
            )
            continue

        if json.dumps(place, sort_keys=True, ensure_ascii=False) != snapshot:
            changed_file = True
            if not dry_run:
                path.write_text(
                    json.dumps(places, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
    return stats


def process_city(
    project_root: Path,
    city_slug: str,
    *,
    breaker: ProviderCircuitBreaker | None = None,
    dry_run: bool = False,
    limit: int | None = None,
    openai_model: str | None = None,
    gigachat_model: str = "GigaChat",
    delay: float = 2.0,
) -> dict[str, int]:
    load_dotenv(project_root)
    cb = breaker if breaker is not None else ProviderCircuitBreaker()
    totals = {
        "en_openai": 0,
        "en_gigachat": 0,
        "en_pixabay": 0,
        "en_translate": 0,
        "ru_openai": 0,
        "ru_gigachat": 0,
        "ru_translate": 0,
        "still_sparse_en": 0,
        "still_sparse_ru": 0,
        "skipped_ok": 0,
    }
    for path in _city_place_files(project_root, city_slug):
        part = process_city_file(
            path,
            city_slug,
            breaker=cb,
            dry_run=dry_run,
            limit=limit,
            openai_model=openai_model,
            gigachat_model=gigachat_model,
            delay=delay,
        )
        for key in totals:
            totals[key] += part.get(key, 0)
    return totals
