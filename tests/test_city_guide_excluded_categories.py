# -*- coding: utf-8 -*-
"""Cafe/restaurant rows must not appear in city guides."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.city_guide_core import (
    drop_excluded_category_places,
    is_excluded_place_category,
)

_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_is_excluded_place_category() -> None:
    assert is_excluded_place_category("cafes")
    assert is_excluded_place_category("Restaurants")
    assert not is_excluded_place_category("museums")


def test_no_cafe_category_in_places_json() -> None:
    for path in _PROJECT_ROOT.glob("*/data/*_places.json"):
        rows = json.loads(path.read_text(encoding="utf-8"))
        assert isinstance(rows, list)
        for row in rows:
            if not isinstance(row, dict):
                continue
            cat = str(row.get("category") or "")
            assert not is_excluded_place_category(cat), (
                "{} has excluded category {}".format(path.name, row.get("slug"))
            )


def test_drop_excluded_category_places() -> None:
    rows = [
        {"slug": "a", "category": "museums"},
        {"slug": "b", "category": "cafes"},
    ]
    out = drop_excluded_category_places(rows)
    assert [r["slug"] for r in out] == ["a"]
