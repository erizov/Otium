# -*- coding: utf-8 -*-
"""Remove OCR/book-reference boilerplate from Moscow place detail overlays."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_narrative import is_reference_boilerplate

_OVERLAY_PATH = _PROJECT_ROOT / "moscow" / "data" / "moscow_place_details_more.json"
_TEXT_FIELDS = (
    "description",
    "history",
    "significance",
    "history_en",
    "significance_en",
    "description_en",
)


def _is_bad_value(value: Any) -> bool:
    if isinstance(value, str):
        return is_reference_boilerplate(value)
    if isinstance(value, list):
        return any(isinstance(x, str) and is_reference_boilerplate(x) for x in value)
    return False


def clean_moscow_reference_boilerplate(
    *,
    dry_run: bool = False,
) -> dict[str, int]:
    blob: dict[str, Any] = json.loads(
        _OVERLAY_PATH.read_text(encoding="utf-8"),
    )
    stats = {"slugs_touched": 0, "fields_removed": 0}
    for slug, block in blob.items():
        if not isinstance(block, dict):
            continue
        removed = 0
        for field in list(block.keys()):
            if field in _TEXT_FIELDS and _is_bad_value(block.get(field)):
                del block[field]
                removed += 1
                continue
            if field in ("facts", "facts_en", "stories_ru", "stories_en"):
                val = block.get(field)
                if not isinstance(val, list):
                    continue
                cleaned = [
                    x for x in val
                    if not (isinstance(x, str) and is_reference_boilerplate(x))
                ]
                if len(cleaned) != len(val):
                    removed += 1
                    if cleaned:
                        block[field] = cleaned
                    else:
                        del block[field]
        if removed:
            stats["slugs_touched"] += 1
            stats["fields_removed"] += removed
            if not block:
                blob[slug] = {}
    if not dry_run:
        _OVERLAY_PATH.write_text(
            json.dumps(blob, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return stats


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    stats = clean_moscow_reference_boilerplate(dry_run=args.dry_run)
    print(json.dumps(stats, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
