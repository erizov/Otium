# -*- coding: utf-8 -*-
"""Fill missing name_en for Moscow PDF-eligible places via Wikipedia langlinks."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_core import places_for_pdf
from scripts.city_guide_naming import title_from_place_slug
from scripts.fetch_place_stories import fetch_english_title_via_russian_page
from scripts.reconcile_moscow_guide_editions import (
    _english_wikipedia_name,
    _is_bad_english_place_name,
)

_PLACES_PATH = _PROJECT_ROOT / "moscow" / "data" / "moscow_places.json"
_DELAY_SEC = 0.35


def _scrub_bad_name_en(
    rows: list[dict],
    pdf_slugs: set[str],
) -> int:
    """Replace or drop name_en values that fail validated ru→en lookup."""
    removed = 0
    for row in rows:
        slug = str(row.get("slug") or "")
        if slug not in pdf_slugs:
            continue
        name_en = str(row.get("name_en") or "").strip()
        name_ru = str(row.get("name_ru") or row.get("name") or "").strip()
        if not name_en or not name_ru:
            continue
        if _is_bad_english_place_name(name_en):
            row.pop("name_en", None)
            removed += 1
            continue
        validated = fetch_english_title_via_russian_page(name_ru)
        time.sleep(_DELAY_SEC)
        if validated:
            if validated != name_en:
                row["name_en"] = validated
                removed += 1
            continue
        slug_title = title_from_place_slug(slug)
        if name_en != slug_title:
            row.pop("name_en", None)
            removed += 1
    return removed


def fill_moscow_en_names(
    *,
    dry_run: bool = False,
    scrub: bool = True,
) -> dict[str, int]:
    rows: list[dict] = json.loads(
        _PLACES_PATH.read_text(encoding="utf-8"),
    )
    pdf_slugs = {
        str(p.get("slug") or "")
        for p in places_for_pdf(_PROJECT_ROOT / "moscow", rows, city_slug="moscow")
    }
    stats = {"scrubbed": 0, "attempted": 0, "filled": 0, "still_missing": 0}
    if scrub:
        stats["scrubbed"] = _scrub_bad_name_en(rows, pdf_slugs)
    for row in rows:
        slug = str(row.get("slug") or "")
        if slug not in pdf_slugs:
            continue
        if str(row.get("name_en") or "").strip():
            continue
        stats["attempted"] += 1
        name_en = _english_wikipedia_name(row)
        time.sleep(_DELAY_SEC)
        if name_en:
            row["name_en"] = name_en
            stats["filled"] += 1
        else:
            stats["still_missing"] += 1
    if not dry_run and (stats["filled"] or stats["scrubbed"]):
        _PLACES_PATH.write_text(
            json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return stats


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-scrub", action="store_true")
    args = parser.parse_args()
    stats = fill_moscow_en_names(dry_run=args.dry_run, scrub=not args.no_scrub)
    print(json.dumps(stats, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
