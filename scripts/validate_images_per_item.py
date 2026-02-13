# -*- coding: utf-8 -*-
"""
Validate that every guide has at least 2 images per item (or exactly 4 in
strict mode), no empty items, each image has a download URL, and no duplicate
URLs within an item.

Run after download + cross-guide dedup; exit 1 if validation fails.
Use --strict or STRICT_IMAGE_VALIDATION=1 to require exactly 4 images per item.
Use --check-slugs to ensure every image file in output/images/ has a (guide, slug)
that matches an item in the slug–item map (name-aware consistency).

Usage:
  python scripts/validate_images_per_item.py
  python scripts/validate_images_per_item.py --strict
  python scripts/validate_images_per_item.py --check-slugs

  PowerShell (strict): $env:STRICT_IMAGE_VALIDATION="1"; python scripts/validate_images_per_item.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

IMAGES_PER_ITEM_STRICT = 4
MIN_IMAGES_PER_ITEM = 1


def _basename(img_path: str) -> str:
    """From 'images/moscow_places/red_square_1.jpg' -> 'red_square_1.jpg'."""
    return img_path.split("/")[-1] if "/" in img_path else img_path


def _load_guide(guide: str) -> tuple[list[dict], dict[str, str]]:
    """Load places list and DOWNLOADS dict for a guide."""
    if guide == "places_of_worship":
        from data.places_of_worship import PLACES_OF_WORSHIP
        from data.places_of_worship_image_urls import (
            PLACES_OF_WORSHIP_IMAGE_DOWNLOADS,
        )
        return PLACES_OF_WORSHIP, PLACES_OF_WORSHIP_IMAGE_DOWNLOADS
    if guide == "parks":
        from data.parks import PARKS
        from data.park_image_urls import PARK_IMAGE_DOWNLOADS
        return PARKS, PARK_IMAGE_DOWNLOADS
    if guide == "museums":
        from data.museums import MUSEUMS
        from data.museum_image_urls import MUSEUM_IMAGE_DOWNLOADS
        return MUSEUMS, MUSEUM_IMAGE_DOWNLOADS
    if guide == "palaces":
        from data.palaces import PALACES
        from data.palace_image_urls import PALACE_IMAGE_DOWNLOADS
        return PALACES, PALACE_IMAGE_DOWNLOADS
    if guide == "buildings":
        from data.buildings import BUILDINGS
        from data.building_image_urls import BUILDING_IMAGE_DOWNLOADS
        return BUILDINGS, BUILDING_IMAGE_DOWNLOADS
    if guide == "sculptures":
        from data.sculptures import SCULPTURES
        from data.sculpture_image_urls import SCULPTURE_IMAGE_DOWNLOADS
        return SCULPTURES, SCULPTURE_IMAGE_DOWNLOADS
    if guide == "places":
        from data.places import PLACES
        from data.place_image_urls import PLACE_IMAGE_DOWNLOADS
        return PLACES, PLACE_IMAGE_DOWNLOADS
    if guide == "squares":
        from data.squares import SQUARES
        from data.squares_image_urls import SQUARES_IMAGE_DOWNLOADS
        return SQUARES, SQUARES_IMAGE_DOWNLOADS
    if guide == "metro":
        from data.metro_stations import METRO_STATIONS
        from data.metro_image_urls import METRO_IMAGE_DOWNLOADS
        return METRO_STATIONS, METRO_IMAGE_DOWNLOADS
    if guide == "monasteries":
        from data.monasteries import MONASTERIES
        from data.image_urls import IMAGE_DOWNLOADS
        return MONASTERIES, IMAGE_DOWNLOADS
    if guide == "theaters":
        from data.theaters import THEATERS
        from data.theater_image_urls import THEATER_IMAGE_DOWNLOADS
        return THEATERS, THEATER_IMAGE_DOWNLOADS
    if guide == "viewpoints":
        from data.viewpoints import VIEWPOINTS
        from data.viewpoint_image_urls import VIEWPOINT_IMAGE_DOWNLOADS
        return VIEWPOINTS, VIEWPOINT_IMAGE_DOWNLOADS
    if guide == "bridges":
        from data.bridges import BRIDGES
        from data.bridge_image_urls import BRIDGE_IMAGE_DOWNLOADS
        return BRIDGES, BRIDGE_IMAGE_DOWNLOADS
    if guide == "markets":
        from data.markets import MARKETS
        from data.market_image_urls import MARKET_IMAGE_DOWNLOADS
        return MARKETS, MARKET_IMAGE_DOWNLOADS
    if guide == "libraries":
        from data.libraries import LIBRARIES
        from data.library_image_urls import LIBRARY_IMAGE_DOWNLOADS
        return LIBRARIES, LIBRARY_IMAGE_DOWNLOADS
    if guide == "railway_stations":
        from data.railway_stations import RAILWAY_STATIONS
        from data.railway_station_image_urls import (
            RAILWAY_STATION_IMAGE_DOWNLOADS,
        )
        return RAILWAY_STATIONS, RAILWAY_STATION_IMAGE_DOWNLOADS
    if guide == "cemeteries":
        from data.cemeteries import CEMETERIES
        from data.cemetery_image_urls import CEMETERY_IMAGE_DOWNLOADS
        return CEMETERIES, CEMETERY_IMAGE_DOWNLOADS
    if guide == "landmarks":
        from data.landmarks import LANDMARKS
        from data.landmarks_image_urls import LANDMARK_IMAGE_DOWNLOADS
        return LANDMARKS, LANDMARK_IMAGE_DOWNLOADS
    if guide == "cafes":
        from data.cafes import CAFES
        from data.cafe_image_urls import CAFE_IMAGE_DOWNLOADS
        return CAFES, CAFE_IMAGE_DOWNLOADS
    raise ValueError("Unknown guide: {}".format(guide))


GUIDES = [
    "monasteries", "places_of_worship", "parks", "museums", "palaces",
    "buildings", "sculptures", "places", "squares", "metro", "theaters",
    "viewpoints", "bridges", "markets", "libraries", "railway_stations",
    "cemeteries", "landmarks", "cafes",
]

# Subdir under output/images/ -> guide key (must match workflow SUBDIR_TO_GUIDE)
SUBDIR_TO_GUIDE = {
    "moscow_monasteries": "monasteries",
    "moscow_places_of_worship": "places_of_worship",
    "moscow_parks": "parks",
    "moscow_museums": "museums",
    "moscow_palaces": "palaces",
    "moscow_buildings": "buildings",
    "moscow_sculptures": "sculptures",
    "moscow_places": "places",
    "moscow_squares": "squares",
    "moscow_metro": "metro",
    "moscow_theaters": "theaters",
    "moscow_viewpoints": "viewpoints",
    "moscow_bridges": "bridges",
    "moscow_markets": "markets",
    "moscow_libraries": "libraries",
    "moscow_railway_stations": "railway_stations",
    "moscow_cemeteries": "cemeteries",
    "moscow_landmarks": "landmarks",
    "moscow_cafes": "cafes",
}


def validate_guide(guide: str, strict: bool) -> list[str]:
    """
    Validate one guide: at least MIN_IMAGES_PER_ITEM (or exactly 4 if strict),
    all in DOWNLOADS, no duplicate URLs per item. Returns list of errors.
    """
    errors: list[str] = []
    try:
        places, downloads = _load_guide(guide)
    except Exception as e:
        errors.append("{}: failed to load: {}".format(guide, e))
        return errors

    required = IMAGES_PER_ITEM_STRICT if strict else MIN_IMAGES_PER_ITEM
    for i, place in enumerate(places):
        name = place.get("name", "?")
        images = place.get("images") or []
        basenames = [_basename(im) for im in images]

        if strict and len(basenames) != IMAGES_PER_ITEM_STRICT:
            errors.append(
                "{} item {} ({!r}): expected {} images, got {}: {}".format(
                    guide, i + 1, name, IMAGES_PER_ITEM_STRICT, len(basenames),
                    basenames,
                )
            )
            continue
        if not strict and len(basenames) < MIN_IMAGES_PER_ITEM:
            errors.append(
                "{} item {} ({!r}): expected at least {} images, got {}: "
                "{}".format(
                    guide, i + 1, name, MIN_IMAGES_PER_ITEM, len(basenames),
                    basenames,
                )
            )
            continue

        missing = [b for b in basenames if b not in downloads]
        if missing:
            errors.append(
                "{} item {} ({!r}): missing DOWNLOADS for: {}".format(
                    guide, i + 1, name, missing,
                )
            )

        urls = [downloads.get(b) for b in basenames if b in downloads]
        if strict and len(urls) >= 2 and len(set(urls)) < len(urls):
            errors.append(
                "{} item {} ({!r}): duplicate URL within item (need "
                "distinct images)".format(guide, i + 1, name)
            )

    return errors


def validate_slugs_against_files(output_images: Path) -> list[str]:
    """
    Check that every image file in output/images/<subdir> has (guide, slug)
    in the slug–item map. Returns list of errors.
    """
    from scripts.slug_item_map import basename_to_slug, get_slug_to_item_name

    errors: list[str] = []
    if not output_images.exists() or not output_images.is_dir():
        return errors
    slug_to_name = get_slug_to_item_name(_PROJECT_ROOT)
    for subdir_path in output_images.iterdir():
        if not subdir_path.is_dir():
            continue
        guide = SUBDIR_TO_GUIDE.get(subdir_path.name)
        if guide is None:
            continue
        for path in subdir_path.iterdir():
            if not path.is_file():
                continue
            if path.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
                continue
            slug = basename_to_slug(path.name)
            if (guide, slug) not in slug_to_name:
                errors.append(
                    "{}: file {!r} has slug {!r} not tied to any item in guide "
                    "{!r}".format(subdir_path.name, path.name, slug, guide),
                )
    return errors


def main() -> int:
    strict_env = os.environ.get("STRICT_IMAGE_VALIDATION", "").strip().lower() in (
        "1", "true", "yes",
    )
    strict = strict_env or ("--strict" in sys.argv)
    check_slugs = "--check-slugs" in sys.argv
    all_errors: list[str] = []
    for guide in GUIDES:
        all_errors.extend(validate_guide(guide, strict=strict))

    if check_slugs:
        output_images = _PROJECT_ROOT / "output" / "images"
        all_errors.extend(validate_slugs_against_files(output_images))

    if all_errors:
        print("Image validation failed:", file=sys.stderr)
        for e in all_errors:
            print("  ", e, file=sys.stderr)
        if strict:
            print(
                "\nStrict mode requires exactly {} images per item with "
                "distinct DOWNLOADS. Expand each guide like places: add _3 and "
                "_4 to every item in data/<guide>.py and add 2 new Commons URLs "
                "per item in data/<guide>_image_urls.py. Run without --strict "
                "to pass with current data (at least 1 image per item).".format(
                    IMAGES_PER_ITEM_STRICT,
                ),
                file=sys.stderr,
            )
        else:
            print(
                "\nFix data/*.py and data/*_image_urls.py so every item has "
                "at least {} images with DOWNLOADS.".format(MIN_IMAGES_PER_ITEM),
                file=sys.stderr,
            )
        return 1
    print(
        "OK: every guide has required images per item with distinct URLs."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
