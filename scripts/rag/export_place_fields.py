# -*- coding: utf-8 -*-
"""Export RAG-backed draft fields into per-city overlay JSON (optional apply).

This script is intentionally conservative:
- It **never** writes source URLs or licenses into PDF-facing fields.
- By default it writes drafts to `rag_outputs/<city>/...` only.
- With `--apply`, it uses the same overlay mechanism as the web editor:
  `<city>/data/<city>_place_details_more.json`.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.rag.config import rag_paths
from scripts.rag.city_map import names_for_slug
from scripts.rag.query import retrieve
from scripts.city_guide_core import is_curated_place_row
from webapp.server.city_store import apply_place_patch
from webapp.server.city_store import load_city_places

_MIN_RAG_SCORE = 0.12

_SENT_RE = re.compile(r"[^.!?\\n]{20,300}[.!?]")
_NORM_RE = re.compile(r"[^A-Za-zА-Яа-яЁё0-9]+")


def _place_title(place: dict[str, Any], lang: str) -> str:
    if lang == "ru":
        return str(place.get("name_ru") or place.get("name_en") or "").strip()
    return str(place.get("name_en") or place.get("subtitle_en") or place.get("name_ru") or "").strip()


def _clean_text(text: str) -> str:
    s = " ".join(text.split())
    # Hard filter: keep PDF clean of obvious source boilerplate.
    for bad in ("wikipedia", "wikimedia", "commons", "источник", "source:"):
        s = s.replace(bad, "")
        s = s.replace(bad.title(), "")
    return s.strip()


def _norm_key(text: str) -> str:
    s = _NORM_RE.sub(" ", text.lower()).strip()
    return " ".join(s.split())


def _looks_like_bad_ocr(text: str) -> bool:
    s = text.strip()
    if len(s) < 80:
        return True
    # If most "words" are 1-2 chars, OCR likely failed.
    words = re.findall(r"[A-Za-zА-Яа-яЁё0-9]{1,}", s)
    if len(words) < 8:
        return True
    short = sum(1 for w in words if len(w) <= 2)
    if short / max(1, len(words)) > 0.55:
        return True
    # Too many non-alnum characters is another strong signal.
    non = sum(1 for ch in s if not (ch.isalnum() or ch.isspace() or ch in ".,;:!?()[]-—\"'«»/"))
    if non / max(1, len(s)) > 0.04:
        return True
    return False


def _should_skip_chunk(chunk: dict[str, Any], *, title: str) -> bool:
    source_name = str(chunk.get("source_name") or "").strip().lower()
    if source_name not in {"wikipedia", "wikidata", "local_file"}:
        return True
    text = str(chunk.get("text") or "")
    if _looks_like_bad_ocr(text):
        return True
    low = text.lower()
    if "как добраться" in low or "how to get" in low:
        return True
    # Enforce that the chunk actually mentions the place name.
    t = _norm_key(title)
    doc_title = str(chunk.get("doc_title") or "")
    doc_key = _norm_key(doc_title)
    blob_key = _norm_key(text)
    if t and (t not in doc_key and t not in blob_key):
        return True
    # For Wikipedia/Wikidata, be much stricter: prefer dedicated pages, not
    # city-wide lists that just mention the place once.
    if source_name in {"wikipedia", "wikidata"} and t and t not in doc_key:
        return True
    return False


def _filter_hits_for_title(
    hits: list[Any],
    *,
    title: str,
) -> list[Any]:
    t = _norm_key(title)
    if not t:
        return hits
    out: list[Any] = []
    for h in hits:
        ch = getattr(h, "chunk", None) or {}
        blob = "{}\n{}".format(str(ch.get("doc_title") or ""), str(ch.get("text") or ""))
        if t and t in _norm_key(blob):
            out.append(h)
    return out or hits


def _draft_from_chunks(chunks: list[dict[str, Any]]) -> dict[str, Any]:
    if not chunks:
        return {}
    merged = "\n\n".join(_clean_text(str(c.get("text") or "")) for c in chunks)
    paras = [p.strip() for p in merged.split("\n\n") if p.strip()]
    if not paras:
        return {}
    description = paras[0]
    history = ""
    significance = ""
    facts: list[str] = []

    # Heuristics: pick paragraphs with time markers for history and superlatives for significance.
    for p in paras[1:6]:
        low = p.lower()
        if not history and any(x in low for x in ("founded", "built", "century", "век", "основан", "построен")):
            history = p
            continue
        if not significance and any(x in low for x in ("symbol", "major", "important", "значим", "символ", "главн")):
            significance = p
            continue
    if history and history.strip() == description.strip():
        history = ""
    if significance and significance.strip() == description.strip():
        significance = ""
    if history and significance and history.strip() == significance.strip():
        significance = ""

    # Facts: sentence snippets from top paragraphs.
    used_blobs: set[str] = set()
    used_blobs.add(description.strip())
    if history:
        used_blobs.add(history.strip())
    if significance:
        used_blobs.add(significance.strip())
    for p in paras[:4]:
        for m in _SENT_RE.findall(p):
            s = _clean_text(m).strip()
            if not s:
                continue
            if any(s in u for u in used_blobs):
                continue
            if s not in facts:
                facts.append(s)
            if len(facts) >= 5:
                break
        if len(facts) >= 5:
            break

    patch: dict[str, Any] = {"description": description}
    if history:
        patch["history"] = history
    if significance:
        patch["significance"] = significance
    if facts:
        patch["facts"] = facts[:5]
    return patch


def export_city(
    project_root: Path,
    *,
    city_slug: str,
    lang: str,
    k: int,
    apply: bool,
) -> int:
    paths = rag_paths(project_root)
    out_dir = paths.outputs_dir / city_slug
    out_dir.mkdir(parents=True, exist_ok=True)

    places = load_city_places(project_root, city_slug)
    patches: dict[str, dict[str, Any]] = {}
    city_names = names_for_slug(city_slug)
    city_hint = city_names.name_ru if lang == "ru" else city_names.name_en
    for place in places:
        slug = str(place.get("slug") or "").strip()
        if not slug or not is_curated_place_row(place):
            continue
        title = _place_title(place, lang)
        if not title:
            continue
        q = "{} {}".format(title, city_hint)
        hits = retrieve(
            project_root,
            query=q,
            city_slug=city_slug,
            language=lang,
            place=title,
            k=k,
        )
        hits = _filter_hits_for_title(hits, title=title)
        chunk_dicts = [
            h.chunk
            for h in hits
            if h.score >= _MIN_RAG_SCORE
            and not _should_skip_chunk(h.chunk, title=title)
        ]
        patch = _draft_from_chunks(chunk_dicts)
        if patch:
            # Conservative apply: only fill missing fields.
            filtered: dict[str, Any] = {}
            for key, val in patch.items():
                if key == "facts":
                    existing = place.get("facts")
                    if not existing:
                        filtered[key] = val
                    continue
                if place.get(key) in (None, "", [], {}):
                    filtered[key] = val
            patch = filtered
        if patch:
            patches[slug] = patch

    draft_path = out_dir / "place_patches_{}.json".format(lang)
    draft_path.write_text(
        json.dumps(patches, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("Written:", draft_path.as_posix())

    if apply and patches:
        for slug, patch in patches.items():
            apply_place_patch(project_root, city_slug, slug, patch)
        print("Applied patches into overlay details.")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=None)
    parser.add_argument("--city", required=True, help="City slug.")
    parser.add_argument(
        "--lang",
        choices=("en", "ru"),
        default="en",
        help="Draft language (default: en).",
    )
    parser.add_argument(
        "--k",
        type=int,
        default=6,
        help="How many chunks to retrieve per place (default: 6).",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply patches into <city>_place_details_more.json.",
    )
    args = parser.parse_args()
    root = (
        args.project_root.resolve()
        if args.project_root
        else Path(__file__).resolve().parent.parent.parent
    )
    return export_city(
        root,
        city_slug=str(args.city).strip(),
        lang=str(args.lang),
        k=int(args.k),
        apply=bool(args.apply),
    )


if __name__ == "__main__":
    raise SystemExit(main())

