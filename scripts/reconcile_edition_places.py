# -*- coding: utf-8 -*-
"""
Reconcile EN/RU place text and images across JSON sources.

Uses the registry with more image-backed places for images/rows; merges
richer EN or RU narrative from main JSON and ``*_place_details.json``.

Usage::

  python scripts/reconcile_edition_places.py
  python scripts/reconcile_edition_places.py --cities smolensk boston
  python scripts/reconcile_edition_places.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_edition_reconcile import reconcile_city_places
from scripts.city_guide_sparse_narrative import place_edition_needs_fill


def _discover_cities(root: Path) -> list[str]:
    return sorted(
        p.parent.parent.name
        for p in root.glob("*/data/*_places.json")
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=_PROJECT_ROOT,
    )
    parser.add_argument(
        "--cities",
        nargs="*",
        metavar="SLUG",
        default=None,
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = args.project_root.resolve()
    cities = args.cities if args.cities else _discover_cities(root)

    total_changed = 0
    for city in cities:
        stats = reconcile_city_places(root, city, dry_run=args.dry_run)
        if stats["places"] == 0:
            continue
        data_path = root / city / "data" / "{}_places.json".format(city)
        places = json.loads(data_path.read_text(encoding="utf-8"))
        needs_en = sum(
            1 for p in places if place_edition_needs_fill(p, "en")
        )
        needs_ru = sum(
            1 for p in places if place_edition_needs_fill(p, "ru")
        )
        mode = "would update" if args.dry_run else "updated"
        print(
            "{:16} {} {} place(s)  EN chars {:6}  RU chars {:6}  "
            "gaps EN {:3} RU {:3}".format(
                city,
                mode,
                stats["changed"],
                stats["en_chars"],
                stats["ru_chars"],
                needs_en,
                needs_ru,
            ),
        )
        total_changed += stats["changed"]

    print("Total {} place row(s) in {} cities".format(
        total_changed, len(cities),
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
