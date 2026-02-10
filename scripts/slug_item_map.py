# -*- coding: utf-8 -*-
"""
Slug–item map for name-aware image deduplication and validation.

Builds (guide, slug) -> item_name from all guides. Slug is derived from
image basename: e.g. red_square_1.jpg -> red_square (strip extension and
trailing _N).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

GUIDES = [
    "monasteries", "places_of_worship", "parks", "museums", "palaces",
    "buildings", "sculptures", "places", "metro",
]


def basename_to_slug(basename: str) -> str:
    """
    From image basename to slug (item identifier).

    Examples: red_square_1.jpg -> red_square, danilov_2.png -> danilov.
    """
    stem = Path(basename).stem
    return re.sub(r"_\d+$", "", stem) or stem


def _basename(img_path: str) -> str:
    """From 'images/moscow_places/red_square_1.jpg' -> 'red_square_1.jpg'."""
    return img_path.split("/")[-1] if "/" in img_path else img_path


def _load_places(guide: str) -> list[dict]:
    """Load list of items (dict with 'name' and 'images') for a guide."""
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
    if guide == "metro":
        from data.metro_stations import METRO_STATIONS
        return METRO_STATIONS
    if guide == "monasteries":
        from data.monasteries import MONASTERIES
        return MONASTERIES
    raise ValueError("Unknown guide: {}".format(guide))


def get_slug_to_item_name(project_root: Path | str) -> dict[tuple[str, str], str]:
    """
    Build (guide, slug) -> item_name from all guides.

    Caller must ensure project_root is on sys.path so data.* imports work.
    """
    root = Path(project_root)
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    result: dict[tuple[str, str], str] = {}
    for guide in GUIDES:
        try:
            places = _load_places(guide)
        except Exception:
            continue
        for item in places:
            name = item.get("name", "?")
            images = item.get("images") or []
            for img in images:
                bn = _basename(img)
                slug = basename_to_slug(bn)
                result[(guide, slug)] = name
    return result


def get_slugs_per_guide(project_root: Path | str) -> dict[str, set[str]]:
    """
    Build guide -> set of slugs that appear in that guide's items.

    Useful for name-aware dedup to check (guide, slug) validity.
    """
    slug_to_name = get_slug_to_item_name(project_root)
    per_guide: dict[str, set[str]] = {}
    for (guide, slug), _ in slug_to_name.items():
        per_guide.setdefault(guide, set()).add(slug)
    return per_guide
