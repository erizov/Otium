# -*- coding: utf-8 -*-
"""
Central loader for guide data — single source of truth for guides and items.

Reduces duplication across slug_item_map, validate_images_per_item,
update_download_lists, generate_yandex_image_urls.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

GUIDES = [
    "monasteries", "places_of_worship", "parks", "museums", "palaces",
    "buildings", "sculptures", "places", "squares", "metro", "theaters",
    "viewpoints", "bridges", "markets", "libraries", "railway_stations",
    "cemeteries", "landmarks", "cafes",
]

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

GUIDE_TO_SUBDIR = {v: k for k, v in SUBDIR_TO_GUIDE.items()}


def load_places(guide: str) -> list[dict[str, Any]]:
    """
    Load items (places) for a guide. Returns list of dicts with name, images, etc.
    """
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


def load_guide_with_downloads(guide: str) -> tuple[list[dict[str, Any]], dict]:
    """
    Load (places, image_downloads) for a guide. Returns (places, downloads dict).
    """
    places = load_places(guide)
    if guide == "places_of_worship":
        from data.places_of_worship_image_urls import (
            PLACES_OF_WORSHIP_IMAGE_DOWNLOADS,
        )
        return places, PLACES_OF_WORSHIP_IMAGE_DOWNLOADS
    if guide == "parks":
        from data.park_image_urls import PARK_IMAGE_DOWNLOADS
        return places, PARK_IMAGE_DOWNLOADS
    if guide == "museums":
        from data.museum_image_urls import MUSEUM_IMAGE_DOWNLOADS
        return places, MUSEUM_IMAGE_DOWNLOADS
    if guide == "palaces":
        from data.palace_image_urls import PALACE_IMAGE_DOWNLOADS
        return places, PALACE_IMAGE_DOWNLOADS
    if guide == "buildings":
        from data.building_image_urls import BUILDING_IMAGE_DOWNLOADS
        return places, BUILDING_IMAGE_DOWNLOADS
    if guide == "sculptures":
        from data.sculpture_image_urls import SCULPTURE_IMAGE_DOWNLOADS
        return places, SCULPTURE_IMAGE_DOWNLOADS
    if guide == "places":
        from data.place_image_urls import PLACE_IMAGE_DOWNLOADS
        return places, PLACE_IMAGE_DOWNLOADS
    if guide == "squares":
        from data.squares_image_urls import SQUARES_IMAGE_DOWNLOADS
        return places, SQUARES_IMAGE_DOWNLOADS
    if guide == "metro":
        from data.metro_image_urls import METRO_IMAGE_DOWNLOADS
        return places, METRO_IMAGE_DOWNLOADS
    if guide == "monasteries":
        from data.image_urls import IMAGE_DOWNLOADS
        return places, IMAGE_DOWNLOADS
    if guide == "theaters":
        from data.theater_image_urls import THEATER_IMAGE_DOWNLOADS
        return places, THEATER_IMAGE_DOWNLOADS
    if guide == "viewpoints":
        from data.viewpoint_image_urls import VIEWPOINT_IMAGE_DOWNLOADS
        return places, VIEWPOINT_IMAGE_DOWNLOADS
    if guide == "bridges":
        from data.bridge_image_urls import BRIDGE_IMAGE_DOWNLOADS
        return places, BRIDGE_IMAGE_DOWNLOADS
    if guide == "markets":
        from data.market_image_urls import MARKET_IMAGE_DOWNLOADS
        return places, MARKET_IMAGE_DOWNLOADS
    if guide == "libraries":
        from data.library_image_urls import LIBRARY_IMAGE_DOWNLOADS
        return places, LIBRARY_IMAGE_DOWNLOADS
    if guide == "railway_stations":
        from data.railway_station_image_urls import (
            RAILWAY_STATION_IMAGE_DOWNLOADS,
        )
        return places, RAILWAY_STATION_IMAGE_DOWNLOADS
    if guide == "cemeteries":
        from data.cemetery_image_urls import CEMETERY_IMAGE_DOWNLOADS
        return places, CEMETERY_IMAGE_DOWNLOADS
    if guide == "landmarks":
        from data.landmarks_image_urls import LANDMARK_IMAGE_DOWNLOADS
        return places, LANDMARK_IMAGE_DOWNLOADS
    if guide == "cafes":
        from data.cafe_image_urls import CAFE_IMAGE_DOWNLOADS
        return places, CAFE_IMAGE_DOWNLOADS
    raise ValueError("Unknown guide: {}".format(guide))
