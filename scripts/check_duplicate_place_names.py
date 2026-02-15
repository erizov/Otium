# -*- coding: utf-8 -*-
"""
Check for duplicate place names across guide subfolders.

Reports any place name that appears in more than one guide (e.g. Red Square
in squares, landmarks, places).

Usage: python scripts/check_duplicate_place_names.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.core import ensure_utf8_console
from scripts.guide_loader import GUIDES, load_places, GUIDE_TO_SUBDIR

ensure_utf8_console()


def main() -> int:
    """Collect place names per guide, report duplicates."""
    # name -> list of subfolder names (e.g. moscow_squares)
    name_to_subdirs: dict[str, list[str]] = {}

    for guide in GUIDES:
        try:
            places = load_places(guide)
        except Exception as e:
            print(
                "Error loading {}: {}.".format(guide, e),
                file=sys.stderr,
            )
            continue
        subdir = GUIDE_TO_SUBDIR.get(guide, guide)
        for place in places:
            name = (place.get("name") or "").strip()
            if not name:
                continue
            if name not in name_to_subdirs:
                name_to_subdirs[name] = []
            if subdir not in name_to_subdirs[name]:
                name_to_subdirs[name].append(subdir)

    duplicates = [
        (name, subdirs)
        for name, subdirs in sorted(name_to_subdirs.items())
        if len(subdirs) > 1
    ]

    if not duplicates:
        print("No duplicate place names across subfolders.")
        return 0

    print("Duplicate place names (name -> subfolders):")
    for name, subdirs in duplicates:
        print("  {} found in {}".format(name, ", ".join(sorted(subdirs))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
