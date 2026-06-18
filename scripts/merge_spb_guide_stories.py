# -*- coding: utf-8 -*-
"""
Merge SPB place stories into ``spb/data/spb_places*.json``.

Sources: existing ``stories_ru`` and ``spb_place_details*.json`` ``stories``.
No synthetic fillers; blank when no curated story exists.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_narrative import is_synthetic_tourist_story
from scripts.merge_moscow_guide_stories import (
    classify_story_edition,
    finalize_story_editions,
)

_SPB_DATA = _PROJECT_ROOT / "spb" / "data"
_PLACE_FILES = (
    "spb_places.json",
    "spb_places_more.json",
    "spb_places_expansion_m2026.json",
    "spb_places_pdf_size_expand.json",
)


def _load_detail_stories() -> dict[str, str]:
    """Map place slug -> first curated story from detail overlays."""
    out: dict[str, str] = {}
    for path in sorted(_SPB_DATA.glob("spb_place_details*.json")):
        blob = json.loads(path.read_text(encoding="utf-8"))
        for key, block in blob.items():
            if not isinstance(block, dict):
                continue
            stories = block.get("stories") or []
            if not stories or not str(stories[0]).strip():
                continue
            story = str(stories[0]).strip()
            if is_synthetic_tourist_story(story):
                continue
            slug = key[4:] if str(key).startswith("spb_") else str(key)
            prev = out.get(slug, "")
            if len(story) > len(prev):
                out[slug] = story
    return out


def _best_ru_story(row: dict[str, Any], details: dict[str, str]) -> str:
    slug = str(row.get("slug") or "").strip()
    candidates: list[str] = []
    for key in ("stories_ru", "stories"):
        raw = row.get(key) or []
        if raw and str(raw[0]).strip():
            text = str(raw[0]).strip()
            if not is_synthetic_tourist_story(text):
                candidates.append(text)
    detail = details.get(slug, "")
    if detail and not is_synthetic_tourist_story(detail):
        candidates.append(detail)
    if not candidates:
        return ""
    return max(candidates, key=len)


def _apply_row_stories(row: dict[str, Any], details: dict[str, str]) -> None:
    row.pop("stories", None)
    story = _best_ru_story(row, details)
    row.pop("stories_ru", None)
    row.pop("stories_en", None)
    if not story:
        return
    edition = classify_story_edition(story)
    if edition == "ru":
        row["stories_ru"] = [story]
    else:
        row["stories_en"] = [story]


def merge_file(path: Path, details: dict[str, str]) -> dict[str, int]:
    rows: list[dict[str, Any]] = json.loads(path.read_text(encoding="utf-8"))
    stats = {"rows": len(rows), "with_ru": 0, "with_en": 0}
    for row in rows:
        if not isinstance(row, dict):
            continue
        _apply_row_stories(row, details)
    finalize_story_editions(rows)
    for row in rows:
        if not isinstance(row, dict):
            continue
        if row.get("stories_ru"):
            stats["with_ru"] += 1
        if row.get("stories_en"):
            stats["with_en"] += 1
    path.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return stats


def merge_all(data_dir: Path | None = None) -> dict[str, dict[str, int]]:
    base = data_dir or _SPB_DATA
    details = _load_detail_stories()
    out: dict[str, dict[str, int]] = {}
    for name in _PLACE_FILES:
        path = base / name
        if not path.is_file():
            continue
        out[name] = merge_file(path, details)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Merge SPB place stories into spb/data JSON files.",
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=_SPB_DATA,
    )
    args = parser.parse_args()
    results = merge_all(args.data_dir)
    for name, stats in results.items():
        print(
            "{}: {} rows (ru: {}, en: {})".format(
                name,
                stats["rows"],
                stats["with_ru"],
                stats["with_en"],
            ),
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
