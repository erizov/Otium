# -*- coding: utf-8 -*-
"""
Cross-guide image URL deduplication by priority.

Loads all *_image_urls DOWNLOADS, groups by URL, and reports which (guide, key)
to keep (highest priority) vs replace (lower priority).
Priority: Monastery > Church > Palace > Building > Parks > Metro > Place >
Sculpture.

Usage: python scripts/dedup_by_priority.py
Exit 0 if no duplicates; 1 if duplicates (list kept vs replace).
"""

from __future__ import annotations

import os
import sys
from collections import defaultdict

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_SCRIPT_DIR)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

# Highest (0) to lowest (8)
GUIDE_PRIORITY = {
    "monastery": 0,
    "church": 1,
    "palace": 2,
    "building": 3,
    "park": 4,
    "museum": 5,
    "metro": 6,
    "place": 7,
    "sculpture": 8,
}

CONFIGS = [
    ("place", "data.place_image_urls", "PLACE_IMAGE_DOWNLOADS"),
    ("park", "data.park_image_urls", "PARK_IMAGE_DOWNLOADS"),
    ("metro", "data.metro_image_urls", "METRO_IMAGE_DOWNLOADS"),
    ("church", "data.church_image_urls", "CHURCH_IMAGE_DOWNLOADS"),
    ("building", "data.building_image_urls", "BUILDING_IMAGE_DOWNLOADS"),
    ("palace", "data.palace_image_urls", "PALACE_IMAGE_DOWNLOADS"),
    ("museum", "data.museum_image_urls", "MUSEUM_IMAGE_DOWNLOADS"),
    ("sculpture", "data.sculpture_image_urls", "SCULPTURE_IMAGE_DOWNLOADS"),
    ("monastery", "data.image_urls", "IMAGE_DOWNLOADS"),
]


def _normalize_url(url: str) -> str:
    return url.strip().rstrip("/")


def _load_all_downloads() -> dict[str, list[tuple[str, str]]]:
    url_to_sources: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for guide, module_name, attr in CONFIGS:
        try:
            mod = __import__(module_name, fromlist=[attr])
            downloads = getattr(mod, attr, None)
        except Exception:
            continue
        if not isinstance(downloads, dict):
            continue
        for key, url in downloads.items():
            if isinstance(url, str):
                url_to_sources[_normalize_url(url)].append((guide, key))
    return dict(url_to_sources)


def main() -> int:
    url_to_sources = _load_all_downloads()
    duplicates: list[tuple[str, list[tuple[str, str]]]] = []
    for url, sources in url_to_sources.items():
        if len(sources) > 1:
            duplicates.append((url, sources))

    if not duplicates:
        print("OK: no duplicate image URLs across guides.")
        return 0

    print(
        "Duplicate URLs (keep highest priority, replace others):",
        file=sys.stderr,
    )
    exit_code = 1
    for url, sources in duplicates:
        # Sort by priority (lower number = higher priority)
        ordered = sorted(
            sources,
            key=lambda x: (GUIDE_PRIORITY.get(x[0], 99), x[1]),
        )
        keep = ordered[0]
        replace = ordered[1:]
        short = url[:70] + "..." if len(url) > 70 else url
        print("  URL: {}".format(short), file=sys.stderr)
        print("    KEEP: {} / {}".format(keep[0], keep[1]), file=sys.stderr)
        for g, k in replace:
            print("    REPLACE: {} / {}".format(g, k), file=sys.stderr)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
