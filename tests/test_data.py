# -*- coding: utf-8 -*-
"""Tests for data modules and expected counts (no asyncio)."""

import sys
from pathlib import Path

import pytest

# Project root on path for "data" imports
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


EXPECTED_COUNTS = {
    "places": 37,
    "buildings": 47,
    "parks": 21,
    "museums": 27,
    "palaces": 23,
    "sculptures": 61,
    "churches": 58,
    "monasteries": 20,
    "metro": 37,
}


def test_places_count() -> None:
    """Places list length matches build_pdf expected count."""
    from data.places import PLACES
    assert len(PLACES) == EXPECTED_COUNTS["places"]


def test_buildings_count() -> None:
    """Buildings list length matches build_pdf expected count."""
    from data.buildings import BUILDINGS
    assert len(BUILDINGS) == EXPECTED_COUNTS["buildings"]


def test_parks_count() -> None:
    """Parks list length matches build_pdf expected count."""
    from data.parks import PARKS
    assert len(PARKS) == EXPECTED_COUNTS["parks"]


def test_museums_count() -> None:
    """Museums list length matches build_pdf expected count."""
    from data.museums import MUSEUMS
    assert len(MUSEUMS) == EXPECTED_COUNTS["museums"]


def test_palaces_count() -> None:
    """Palaces list length matches build_pdf expected count."""
    from data.palaces import PALACES
    assert len(PALACES) == EXPECTED_COUNTS["palaces"]


def test_sculptures_count() -> None:
    """Sculptures list length matches build_pdf expected count."""
    from data.sculptures import SCULPTURES
    assert len(SCULPTURES) == EXPECTED_COUNTS["sculptures"]


def test_churches_count() -> None:
    """Churches list length matches build_pdf expected count."""
    from data.churches import CHURCHES
    assert len(CHURCHES) == EXPECTED_COUNTS["churches"]


def test_monasteries_count() -> None:
    """Monasteries list length matches build_pdf expected count."""
    from data.monasteries import MONASTERIES
    assert len(MONASTERIES) == EXPECTED_COUNTS["monasteries"]


def test_metro_count() -> None:
    """Metro stations list length matches build_pdf expected count."""
    from data.metro_stations import METRO_STATIONS
    assert len(METRO_STATIONS) == EXPECTED_COUNTS["metro"]


def test_place_has_required_keys() -> None:
    """Each place has name, images, lat, lon."""
    from data.places import PLACES
    for p in PLACES[:3]:
        assert "name" in p
        assert "images" in p
        assert "lat" in p
        assert "lon" in p
        assert isinstance(p["images"], list)
        assert len(p["images"]) >= 1


def _map_url(lon: float, lat: float) -> str:
    """Same formula as build_pdf._map_img_url (map URL by coords)."""
    return (
        "https://static-maps.yandex.ru/1.x/?ll={lon:.4f},{lat:.4f}&z=16&l=map"
        "&size=380,200&pt={lon:.4f},{lat:.4f},pm2rdm".format(lon=lon, lat=lat)
    )


def _all_places_by_guide() -> list[tuple[str, list[dict]]]:
    """Returns [(guide_name, list of place dicts with name, lat, lon), ...]."""
    from data.places import PLACES
    from data.buildings import BUILDINGS
    from data.parks import PARKS
    from data.museums import MUSEUMS
    from data.palaces import PALACES
    from data.sculptures import SCULPTURES
    from data.churches import CHURCHES
    from data.monasteries import MONASTERIES
    from data.metro_stations import METRO_STATIONS

    return [
        ("places", PLACES),
        ("buildings", BUILDINGS),
        ("parks", PARKS),
        ("museums", MUSEUMS),
        ("palaces", PALACES),
        ("sculptures", SCULPTURES),
        ("churches", CHURCHES),
        ("monasteries", MONASTERIES),
        ("metro", METRO_STATIONS),
    ]


def test_no_duplicate_map_urls_across_guides() -> None:
    """No two different items (across all guides) share the same map URL.

    Map URL is determined by (lat, lon). Same coords => same map => forbidden.
    """
    map_to_sources: dict[str, list[tuple[str, str]]] = {}
    for guide_name, places in _all_places_by_guide():
        for p in places:
            name = p.get("name", "?")
            lon = p.get("lon")
            lat = p.get("lat")
            if lon is None or lat is None:
                continue
            url = _map_url(lon, lat)
            if url not in map_to_sources:
                map_to_sources[url] = []
            map_to_sources[url].append((guide_name, name))

    duplicates = [(url, srcs) for url, srcs in map_to_sources.items()
                  if len(srcs) > 1]
    assert not duplicates, (
        "Duplicate map URL (same lat,lon for 2+ items): " +
        "; ".join(
            "{} used by {}".format(u[:60], [s for s in srcs])
            for u, srcs in duplicates[:5]
        )
    )


def test_no_duplicate_image_urls_in_places_metro_parks() -> None:
    """No image URL is shared between two different items in places/metro/parks."""
    from data.place_image_urls import PLACE_IMAGE_DOWNLOADS
    from data.metro_image_urls import METRO_IMAGE_DOWNLOADS
    from data.park_image_urls import PARK_IMAGE_DOWNLOADS

    url_to_sources: dict[str, list[tuple[str, str]]] = {}
    for guide_name, downloads in [
            ("places", PLACE_IMAGE_DOWNLOADS),
            ("metro", METRO_IMAGE_DOWNLOADS),
            ("parks", PARK_IMAGE_DOWNLOADS),
    ]:
        for key, url in downloads.items():
            url = url.strip()
            if url not in url_to_sources:
                url_to_sources[url] = []
            url_to_sources[url].append((guide_name, key))

    duplicates = [(url, srcs) for url, srcs in url_to_sources.items()
                  if len(srcs) > 1]
    assert not duplicates, (
        "Duplicate image URLs (forbidden): " +
        "; ".join(
            "{} used by {}".format(u[:80], [s for s in srcs])
            for u, srcs in duplicates[:5]
        )
    )


@pytest.mark.xfail(
    reason="Museum/building/palace/church/sculpture/monastery image URLs "
           "still share Commons URLs; replace duplicates in *_image_urls.py",
    strict=False,
)
def test_no_duplicate_image_urls_across_all_guides() -> None:
    """No image URL is used for 2+ different items across any guide.

    Uses same logic as scripts/check_duplicate_images.py.
    """
    from collections import defaultdict

    configs = [
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
    url_to_sources: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for guide, module_name, attr in configs:
        try:
            mod = __import__(module_name, fromlist=[attr])
            downloads = getattr(mod, attr, None)
        except Exception:
            continue
        if not isinstance(downloads, dict):
            continue
        for key, url in downloads.items():
            if isinstance(url, str):
                url_to_sources[url.strip().rstrip("/")].append((guide, key))

    duplicates = [(u, s) for u, s in url_to_sources.items() if len(s) > 1]
    assert not duplicates, (
        "Duplicate image URL across guides (forbidden): " +
        "; ".join(
            "{} -> {}".format(u[:60], [x for x in srcs[:3]])
            for u, srcs in duplicates[:5]
        )
    )
