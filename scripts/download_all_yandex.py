# -*- coding: utf-8 -*-
"""
Download first 4 Yandex images for all guides (each chapter).

Runs the same logic as individual download_*_yandex.py scripts for every guide.
Use --guide NAME to run only one guide.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.download_yandex_common import download_yandex_for_guide


# (guide_key, label for log, data_module, places_attr, extra_query_word or None)
_GUIDES = [
    ("monasteries", "Monastery", "data.monasteries", "MONASTERIES", None),
    ("places_of_worship", "Place of worship", "data.places_of_worship",
     "PLACES_OF_WORSHIP", None),
    ("parks", "Park", "data.parks", "PARKS", "парк"),
    ("museums", "Museum", "data.museums", "MUSEUMS", None),
    ("palaces", "Palace", "data.palaces", "PALACES", None),
    ("buildings", "Building", "data.buildings", "BUILDINGS", None),
    ("sculptures", "Sculpture", "data.sculptures", "SCULPTURES", None),
    ("places", "Place", "data.places", "PLACES", None),
    ("squares", "Square", "data.squares", "SQUARES", None),
    ("metro", "Metro", "data.metro_stations", "METRO_STATIONS", None),
    ("theaters", "Theater", "data.theaters", "THEATERS", None),
    ("viewpoints", "Viewpoint", "data.viewpoints", "VIEWPOINTS", None),
    ("bridges", "Bridge", "data.bridges", "BRIDGES", None),
    ("markets", "Market", "data.markets", "MARKETS", None),
    ("libraries", "Library", "data.libraries", "LIBRARIES", None),
    ("railway_stations", "Station", "data.railway_stations",
     "RAILWAY_STATIONS", None),
    ("cemeteries", "Cemetery", "data.cemeteries", "CEMETERIES", None),
    ("landmarks", "Landmark", "data.landmarks", "LANDMARKS", None),
    ("cafes", "Cafe", "data.cafes", "CAFES", None),
]


def _load_guide(guide_key: str):
    """Return (places, images_subfolder) for guide_key."""
    for key, _label, mod_name, places_attr, _extra in _GUIDES:
        if key != guide_key:
            continue
        mod = importlib.import_module(mod_name)
        places = getattr(mod, places_attr)
        subfolder = getattr(mod, "IMAGES_SUBFOLDER")
        return places, subfolder
    raise ValueError("Unknown guide: {}".format(guide_key))


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(
        description="Download first 4 Yandex images for all guides (or one)."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=_PROJECT_ROOT / "output",
        help="Output directory (default: output/).",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-headless", action="store_true")
    parser.add_argument(
        "--guide",
        choices=[g[0] for g in _GUIDES],
        default=None,
        help="Run only this guide (default: all).",
    )
    args = parser.parse_args()

    to_run = _GUIDES
    if args.guide:
        to_run = [g for g in _GUIDES if g[0] == args.guide]

    total_updated = 0
    guides_with_updates = 0
    for guide_key, label, _mod, _places_attr, extra_word in to_run:
        print("\n=== {} ===".format(guide_key))
        try:
            places, images_subfolder = _load_guide(guide_key)
        except (ImportError, AttributeError) as e:
            print("  Skip: {}".format(e))
            continue
        n = download_yandex_for_guide(
            label,
            places,
            images_subfolder,
            args.output_dir,
            images_per_place=4,
            dry_run=args.dry_run,
            city="Москва",
            extra_query_word=extra_word,
        )
        total_updated += n
        if n > 0:
            guides_with_updates += 1
        print("  Updated: {}".format(n))

    print("\nTotal items updated: {}".format(total_updated))
    print("Guides with at least one update: {}".format(guides_with_updates))
    return 0


if __name__ == "__main__":
    sys.exit(main())
