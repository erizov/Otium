# -*- coding: utf-8 -*-
"""Tests for city guide primer and trip-plan front matter."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.city_guide_front_matter import (
    CITIES_WITHOUT_TRIP_ROUTES,
    ITINERARY_KEYS,
    front_matter_html_blocks,
    front_matter_json_path,
    place_prominence_score,
    primer_section_html,
    save_front_matter,
    top_places_for_prompt,
    trip_plans_section_html,
)

_SAMPLE_FRONT = {
    "city_slug": "sample",
    "primer": {
        "en": {
            "climate": "Mild winters and warm summers.",
            "transport": "Metro and trams cover the centre.",
            "etiquette": "Dress modestly in religious sites.",
            "overview_paragraphs": ["A compact city for walking."],
        },
        "ru": {
            "climate": "Мягкая зима и тёплое лето.",
            "transport": "Метро и трамваи покрывают центр.",
            "etiquette": "Скромная одежда в храмах.",
        },
    },
    "itineraries": {
        "en": {
            "1d": {
                "title": "One day downtown",
                "intro": "A short loop near the river.",
                "stops": [
                    {
                        "slug": "sample_tower",
                        "minutes": 60,
                        "note": "Panorama",
                    },
                    {
                        "slug": "sample_market",
                        "minutes": 45,
                        "note": "Lunch stop",
                    },
                ],
            },
        },
        "ru": {
            "1d": {
                "title": "Один день",
                "intro": "Короткий маршрут.",
                "stops": [
                    {"slug": "sample_tower", "minutes": 60, "note": "Вид"},
                ],
            },
        },
    },
}

_PLACES = [
    {
        "slug": "sample_tower",
        "name_en": "Old Tower",
        "description_en": "A landmark tower with city views.",
        "image_rel_path": "images/sample_tower.jpg",
    },
    {
        "slug": "sample_market",
        "name_en": "Central Market",
        "description_en": "Food stalls and local produce.",
        "image_rel_path": "images/sample_market.jpg",
    },
]


def test_primer_section_en() -> None:
    html = primer_section_html(_SAMPLE_FRONT, "en")
    assert "City primer" in html
    assert "Climate" in html
    assert "Mild winters" in html
    assert "guide-primer" in html


def test_trip_plans_anchors_and_durations() -> None:
    html = trip_plans_section_html(_SAMPLE_FRONT, "en", _PLACES)
    assert "Trip ideas" in html
    assert 'href="#sample_tower"' in html
    assert "Old Tower" in html
    assert "One day downtown" in html
    assert 'id="trip-1d"' in html


def test_front_matter_html_blocks_roundtrip(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CITY_GUIDE_NO_GEOCODE", "1")
    save_front_matter(tmp_path, "sample", _SAMPLE_FRONT)
    assert front_matter_json_path(tmp_path, "sample").is_file()
    blocks = front_matter_html_blocks(
        tmp_path,
        "sample",
        "en",
        _PLACES,
    )
    assert len(blocks) >= 1
    assert "guide-primer" in blocks[0]


def test_top_places_ranking() -> None:
    rows = top_places_for_prompt(_PLACES, "en", limit=2)
    assert len(rows) == 2
    slugs = {r["slug"] for r in rows}
    assert slugs == {"sample_tower", "sample_market"}
    assert place_prominence_score(_PLACES[0], "en") >= 0


def test_front_matter_html_blocks_includes_proximity_routes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CITY_GUIDE_NO_GEOCODE", "1")
    save_front_matter(tmp_path, "sample", _SAMPLE_FRONT)
    blocks = front_matter_html_blocks(
        tmp_path,
        "sample",
        "en",
        _PLACES,
    )
    assert len(blocks) >= 1
    assert any("guide-trip-plans" in b for b in blocks)


def test_front_matter_skips_trip_routes_for_moscow_spb(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CITY_GUIDE_NO_GEOCODE", "1")
    save_front_matter(tmp_path, "moscow", _SAMPLE_FRONT)
    for slug in CITIES_WITHOUT_TRIP_ROUTES:
        blocks = front_matter_html_blocks(
            tmp_path,
            slug,
            "en",
            _PLACES,
        )
        assert not any("guide-trip-plans" in b for b in blocks)
