# -*- coding: utf-8 -*-
"""
Update download_list.txt for each guide subfolder.

Scans actual files in each directory, builds manifest in both RU and EN.
Default: study directory first, then write list. Use before download to
reflect manual adds/deletes.

Usage:
  python scripts/update_download_lists.py
  python scripts/update_download_lists.py --guide monasteries
"""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.download_with_dedup import download_list_from_directory

BUILD_GUIDES = [
    "monasteries", "places_of_worship", "parks", "museums", "palaces",
    "buildings", "sculptures", "places", "squares", "metro", "theaters",
    "viewpoints", "bridges", "markets", "libraries", "railway_stations",
    "cemeteries", "landmarks", "cafes",
]

GUIDE_TO_SUBDIR = {
    "monasteries": "moscow_monasteries",
    "places_of_worship": "moscow_places_of_worship",
    "parks": "moscow_parks",
    "museums": "moscow_museums",
    "palaces": "moscow_palaces",
    "buildings": "moscow_buildings",
    "sculptures": "moscow_sculptures",
    "places": "moscow_places",
    "squares": "moscow_squares",
    "metro": "moscow_metro",
    "theaters": "moscow_theaters",
    "viewpoints": "moscow_viewpoints",
    "bridges": "moscow_bridges",
    "markets": "moscow_markets",
    "libraries": "moscow_libraries",
    "railway_stations": "moscow_railway_stations",
    "cemeteries": "moscow_cemeteries",
    "landmarks": "moscow_landmarks",
    "cafes": "moscow_cafes",
}


def _load_places(guide: str) -> list[dict]:
    """Load items for a guide."""
    if guide == "monasteries":
        from data.monasteries import MONASTERIES
        return MONASTERIES
    if guide == "places_of_worship":
        from data.places_of_worship import PLACES_OF_WORSHIP
        return PLACES_OF_WORSHIP
    if guide == "parks":
        from data.parks import PARKS
        return PARKS
    if guide == "museums":
        from data.museums import MUSEUMS
        return MUSEUMS
    if guide == "palaces":
        from data.palaces import PALACES
        return PALACES
    if guide == "buildings":
        from data.buildings import BUILDINGS
        return BUILDINGS
    if guide == "sculptures":
        from data.sculptures import SCULPTURES
        return SCULPTURES
    if guide == "places":
        from data.places import PLACES
        return PLACES
    if guide == "squares":
        from data.squares import SQUARES
        return SQUARES
    if guide == "metro":
        from data.metro_stations import METRO_STATIONS
        return METRO_STATIONS
    if guide == "theaters":
        from data.theaters import THEATERS
        return THEATERS
    if guide == "viewpoints":
        from data.viewpoints import VIEWPOINTS
        return VIEWPOINTS
    if guide == "bridges":
        from data.bridges import BRIDGES
        return BRIDGES
    if guide == "markets":
        from data.markets import MARKETS
        return MARKETS
    if guide == "libraries":
        from data.libraries import LIBRARIES
        return LIBRARIES
    if guide == "railway_stations":
        from data.railway_stations import RAILWAY_STATIONS
        return RAILWAY_STATIONS
    if guide == "cemeteries":
        from data.cemeteries import CEMETERIES
        return CEMETERIES
    if guide == "landmarks":
        from data.landmarks import LANDMARKS
        return LANDMARKS
    if guide == "cafes":
        from data.cafes import CAFES
        return CAFES
    raise ValueError("Unknown guide: {}".format(guide))


def main() -> None:
    """Update download_list.txt for each guide subfolder."""
    try:
        from dotenv import load_dotenv
        load_dotenv(_PROJECT_ROOT / ".env")
    except ImportError:
        pass

    import argparse
    parser = argparse.ArgumentParser(
        description="Update download_list.txt from directory scan (RU+EN)",
    )
    parser.add_argument(
        "--guide",
        choices=BUILD_GUIDES,
        default=None,
        help="Update only this guide (default: all).",
    )
    args = parser.parse_args()

    guides = [args.guide] if args.guide else BUILD_GUIDES
    output_dir = _PROJECT_ROOT / "output" / "images"

    for guide in guides:
        subdir = GUIDE_TO_SUBDIR.get(guide)
        if not subdir:
            continue
        images_dir = output_dir / subdir
        if not images_dir.exists():
            print("  Skip {} (dir not found)".format(subdir))
            continue
        try:
            items = _load_places(guide)
        except Exception as e:
            print("  Skip {}: {}".format(guide, e))
            continue
        missing = download_list_from_directory(
            images_dir, items, guide_name=guide,
        )
        print("  {}: {} missing slot(s)".format(subdir, len(missing)))


if __name__ == "__main__":
    main()
