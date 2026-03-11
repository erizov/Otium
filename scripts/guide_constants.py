# -*- coding: utf-8 -*-
"""
Shared constants for guide build scripts: guide list, expected counts, paths.
"""

from __future__ import annotations

from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = _SCRIPT_DIR.parent

BUILD_GUIDES = [
    "monasteries",
    "places_of_worship",
    "parks",
    "museums",
    "palaces",
    "buildings",
    "sculptures",
    "places",
    "squares",
    "metro",
    "theaters",
    "viewpoints",
    "bridges",
    "markets",
    "libraries",
    "railway_stations",
    "cemeteries",
    "landmarks",
    "cafes",
]

GUIDE_EXPECTED_COUNTS: dict[str, int] = {
    "test_e2e": 5,
    "monasteries": 20,
    "places_of_worship": 66,
    "parks": 28,
    "museums": 32,
    "palaces": 24,
    "buildings": 42,
    "sculptures": 61,
    "places": 30,
    "metro": 37,
    "theaters": 14,
    "viewpoints": 14,
    "bridges": 12,
    "squares": 12,
    "markets": 8,
    "libraries": 7,
    "railway_stations": 9,
    "cemeteries": 9,
    "landmarks": 14,
    "cafes": 11,
}


def get_output_dir() -> Path:
    """Output directory (output/)."""
    return PROJECT_ROOT / "output"


def get_images_root() -> Path:
    """Images root (output/images/)."""
    return PROJECT_ROOT / "output" / "images"
