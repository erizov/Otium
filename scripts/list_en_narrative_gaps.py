# -*- coding: utf-8 -*-
"""Print all EN places missing narrative (tabular list)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.en_narrative_fill_queue import (
    discover_cities,
    iter_en_narrative_fill_jobs,
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
    parser.add_argument(
        "--csv",
        action="store_true",
        help="Comma-separated: city,slug,place_name,action",
    )
    args = parser.parse_args()
    root = args.project_root.resolve()
    cities = args.cities if args.cities else discover_cities(root)

    total = 0
    for city in cities:
        for job in iter_en_narrative_fill_jobs(root, city):
            total += 1
            if args.csv:
                print("{},{},{},{}".format(
                    job["city_slug"],
                    job["slug"],
                    job["place_name_en"].replace(",", " "),
                    job["suggested_action"],
                ))
            else:
                print("{:16}  {:40}  {}  [{}]".format(
                    job["city_slug"],
                    job["slug"][:40],
                    job["place_name_en"][:36],
                    job["suggested_action"],
                ))
    print("Total: {} place(s)".format(total), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
