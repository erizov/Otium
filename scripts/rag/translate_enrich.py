# -*- coding: utf-8 -*-
"""Translate high-value chunks between RU and EN to enrich the corpus."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.rag.config import rag_paths
from scripts.rag.query import retrieve


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _dedupe_key(text: str) -> str:
    return _sha(" ".join(text.lower().split()))


@dataclass(frozen=True)
class Translator:
    kind: str  # 'ollama' or 'openai'
    model: str

    def translate(self, text: str, *, src: str, dst: str) -> str:
        if self.kind == "ollama":
            return _ollama_translate(text, src=src, dst=dst, model=self.model)
        if self.kind == "openai":
            return _openai_translate(text, src=src, dst=dst, model=self.model)
        raise ValueError("Unknown translator kind: {}".format(self.kind))


def _ollama_translate(text: str, *, src: str, dst: str, model: str) -> str:
    host = os.environ.get("OLLAMA_HOST") or "http://127.0.0.1:11434"
    url = host.rstrip("/") + "/api/generate"
    prompt = (
        "Translate from {src} to {dst}.\n"
        "- Keep proper names as commonly used in the destination language.\n"
        "- Keep dates, numbers, and toponyms accurate.\n"
        "- Output plain text only.\n\n"
        "{text}"
    ).format(src=src, dst=dst, text=text)
    resp = requests.post(
        url,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
        },
        timeout=180,
    )
    resp.raise_for_status()
    data = resp.json()
    return str(data.get("response") or "").strip()


def _openai_translate(text: str, *, src: str, dst: str, model: str) -> str:
    # Optional fallback; requires OPENAI_API_KEY (uses existing dependency).
    try:
        from openai import OpenAI  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("OpenAI SDK not available: {}".format(exc)) from exc
    client = OpenAI()
    msg = (
        "Translate from {src} to {dst}. Output plain text only.\n\n{text}"
    ).format(src=src, dst=dst, text=text)
    r = client.responses.create(
        model=model,
        input=msg,
    )
    return str(r.output_text or "").strip()


def _pick_translator() -> Translator:
    if os.environ.get("OLLAMA_HOST") or os.environ.get("USE_OLLAMA") == "1":
        return Translator(kind="ollama", model=os.environ.get("OLLAMA_MODEL") or "llama3.1")
    if os.environ.get("OPENAI_API_KEY"):
        return Translator(kind="openai", model=os.environ.get("OPENAI_MODEL") or "gpt-4.1-mini")
    raise RuntimeError(
        "No translator configured. Set OLLAMA_HOST (local) or OPENAI_API_KEY."
    )


def _derived_doc_path(paths, city_slug: str, language: str) -> Path:
    ddir = paths.docs_dir / city_slug
    ddir.mkdir(parents=True, exist_ok=True)
    return ddir / "derived_translate_{}.jsonl".format(language)


def _load_existing_derived_keys(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    out: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            blob = json.loads(line)
        except Exception:
            continue
        key = str(blob.get("dedupe_key") or "").strip()
        if key:
            out.add(key)
    return out


def enrich_city(
    project_root: Path,
    *,
    city_slug: str,
    translator: Translator,
    k: int,
    per_direction: int,
    sleep_sec: float,
) -> int:
    paths = rag_paths(project_root)

    # For each direction, retrieve top-k from the other language and translate.
    pairs = (("ru", "en"), ("en", "ru"))
    for src, dst in pairs:
        out_path = _derived_doc_path(paths, city_slug, dst)
        seen = _load_existing_derived_keys(out_path)
        retrieved = retrieve(
            project_root,
            query="history architecture facts significance famous persons",
            city_slug=city_slug,
            language=src,
            k=k,
        )
        wrote = 0
        lines: list[str] = []
        for rc in retrieved:
            if wrote >= per_direction:
                break
            text = str(rc.chunk.get("text") or "").strip()
            if not text:
                continue
            dk = _dedupe_key(text)
            if dk in seen:
                continue
            translated = translator.translate(text, src=src, dst=dst)
            if not translated.strip():
                continue
            blob = {
                "doc_id": "derived:{}:{}:{}".format(city_slug, src, _sha(text)[:12]),
                "city_slug": city_slug,
                "language": dst,
                "source_name": "derived_translate",
                "source_url": str(rc.chunk.get("source_url") or ""),
                "license": str(rc.chunk.get("license") or ""),
                "retrieved_at_utc": _utc_now(),
                "title": "Derived translation",
                "text": translated.strip(),
                "extra": {
                    "derived_from_chunk_id": rc.chunk.get("chunk_id"),
                    "translator": {"kind": translator.kind, "model": translator.model},
                    "score": rc.score,
                },
                "dedupe_key": dk,
            }
            lines.append(json.dumps(blob, ensure_ascii=False))
            seen.add(dk)
            wrote += 1
            if sleep_sec > 0:
                time.sleep(sleep_sec)
        if lines:
            out_path.write_text(
                (out_path.read_text(encoding="utf-8") if out_path.is_file() else "")
                + "\n".join(lines)
                + "\n",
                encoding="utf-8",
            )
            print("{}: wrote {} derived {} chunk(s)".format(city_slug, wrote, dst))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help="Repo root (default: auto).",
    )
    parser.add_argument("--city", required=True, help="City slug.")
    parser.add_argument("--k", type=int, default=12, help="Retrieve top-k.")
    parser.add_argument(
        "--per-direction",
        type=int,
        default=4,
        help="How many chunks to translate per direction.",
    )
    parser.add_argument(
        "--sleep-sec",
        type=float,
        default=0.0,
        help="Sleep between translations (default: 0).",
    )
    args = parser.parse_args()
    root = (
        args.project_root.resolve()
        if args.project_root
        else Path(__file__).resolve().parent.parent.parent
    )
    try:
        tr = _pick_translator()
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return enrich_city(
        root,
        city_slug=str(args.city).strip(),
        translator=tr,
        k=int(args.k),
        per_direction=int(args.per_direction),
        sleep_sec=max(0.0, float(args.sleep_sec)),
    )


if __name__ == "__main__":
    raise SystemExit(main())

