# -*- coding: utf-8
"""Apply address/location/hours policy to moscow_places.json."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from moscow.data.metro_station_locations import METRO_STATION_META
from scripts.city_guide_place_meta import ADDRESS_OPTIONAL, place_category

_OPTIONAL = ADDRESS_OPTIONAL


def _migrate_optional_location(row: dict) -> bool:
    cat = place_category(row)
    if cat not in _OPTIONAL or cat == "metro":
        return False
    addr = str(row.get("address") or "").strip()
    loc = str(row.get("location") or "").strip()
    if not addr:
        return False
    if not loc:
        row["location"] = addr
    row.pop("address", None)
    return True


def _migrate_metro(row: dict) -> bool:
    if place_category(row) != "metro":
        return False
    slug = str(row.get("slug") or "")
    meta = METRO_STATION_META.get(slug)
    if not meta:
        return False
    changed = False
    line = meta.get("metro_line", "")
    loc = meta.get("location", "")
    if line and row.get("metro_line") != line:
        row["metro_line"] = line
        changed = True
    if line and row.get("subtitle_en") != line:
        row["subtitle_en"] = line
        changed = True
    if loc and row.get("location") != loc:
        row["location"] = loc
        changed = True
    if row.get("address"):
        row.pop("address", None)
        changed = True
    return changed


def apply(rows: list[dict]) -> tuple[int, int]:
    loc_n = metro_n = 0
    for row in rows:
        if _migrate_metro(row):
            metro_n += 1
        elif _migrate_optional_location(row):
            loc_n += 1
    return loc_n, metro_n


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    path = _PROJECT_ROOT / "moscow" / "data" / "moscow_places.json"
    rows = json.loads(path.read_text(encoding="utf-8"))
    loc_n, metro_n = apply(rows)
    print(
        "Updated {} metro station(s), {} open-air location label(s).".format(
            metro_n, loc_n,
        ),
    )
    if args.dry_run:
        return 0
    bak = path.with_suffix(".json.metabak")
    if not bak.is_file():
        shutil.copy2(path, bak)
    path.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("Written", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
