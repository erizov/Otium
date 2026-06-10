# -*- coding: utf-8 -*-
"""Tests for proximity-optimised guide routes."""

from __future__ import annotations

from scripts.city_guide_proximity_routes import (
    STOPS_ONE_DAY,
    haversine_km,
    nearest_neighbor_route,
    _Point,
    build_proximity_itineraries,
)


def test_haversine_short_distance() -> None:
    # ~1.1 km apart in Moscow centre
    d = haversine_km(55.7558, 37.6173, 55.7650, 37.6200)
    assert 0.5 < d < 2.0


def test_nearest_neighbor_prefers_closest_next() -> None:
    seed = _Point(slug="a", lat=55.75, lon=37.62, prominence=10)
    near = _Point(slug="b", lat=55.751, lon=37.621, prominence=5)
    far = _Point(slug="c", lat=55.80, lon=37.70, prominence=8)
    route = nearest_neighbor_route([seed, near, far], limit=3, start_slug="a")
    assert [p.slug for p in route] == ["a", "b", "c"]


def test_build_itineraries_use_only_listed_slugs() -> None:
    places = [
        {
            "slug": "demo_north",
            "name_en": "North Gate",
            "lat": 55.76,
            "lon": 37.61,
            "description_en": "A historic gate with city views and long narrative.",
            "image_rel_path": "images/demo_north.jpg",
        },
        {
            "slug": "demo_south",
            "name_en": "South Garden",
            "lat": 55.74,
            "lon": 37.62,
            "description_en": "A riverside garden with fountains and paths.",
            "image_rel_path": "images/demo_south.jpg",
        },
        {
            "slug": "demo_east",
            "name_en": "East Museum",
            "lat": 55.755,
            "lon": 37.64,
            "description_en": "Regional museum with permanent collections.",
            "image_rel_path": "images/demo_east.jpg",
        },
    ]
    plans = build_proximity_itineraries(
        places,
        "demo",
        "en",
        project_root=None,
        write_cache=False,
    )
    assert "1d" in plans
    slugs = {s["slug"] for s in plans["1d"]["stops"]}
    assert slugs.issubset({"demo_north", "demo_south", "demo_east"})
    assert len(plans["1d"]["stops"]) <= STOPS_ONE_DAY


def test_three_day_routes_present() -> None:
    places = [
        {
            "slug": "p{}".format(i),
            "name_en": "Place {}".format(i),
            "lat": 55.75 + i * 0.01,
            "lon": 37.60 + (i % 3) * 0.01,
            "description_en": "Description for place {}.".format(i),
            "image_rel_path": "images/p{}.jpg".format(i),
        }
        for i in range(8)
    ]
    plans = build_proximity_itineraries(
        places,
        "demo",
        "en",
        project_root=None,
        write_cache=False,
    )
    assert "3d1" in plans
    assert plans["3d1"]["stops"]
