# -*- coding: utf-8 -*-
"""
Shared constants for guide build scripts: guide list, expected counts, paths.
"""

from __future__ import annotations

from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = _SCRIPT_DIR.parent
MOSCOW_ROOT = PROJECT_ROOT / "moscow"

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


def get_moscow_root() -> Path:
    """Moscow city package root (``moscow/``)."""
    return MOSCOW_ROOT


def get_output_dir() -> Path:
    """Moscow category guide HTML/PDF output (``moscow/output/``)."""
    return MOSCOW_ROOT / "output"


def get_images_root() -> Path:
    """Moscow place images root (``moscow/images/``)."""
    return MOSCOW_ROOT / "images"


def get_moscow_data_dir() -> Path:
    """Moscow registry Python modules (``moscow/data/``)."""
    return MOSCOW_ROOT / "data"


def moscow_city_root_from_html_dir(html_output_dir: Path) -> Path:
    """
    Resolve city root when HTML lives in ``moscow/output/``.

    Legacy callers passed ``output/`` as both HTML and image parent; images
    now live under ``moscow/images/`` with ``html_output_dir`` at
    ``moscow/output/``.
    """
    if html_output_dir.name == "output":
        parent = html_output_dir.parent
        if parent.name == "moscow":
            return parent
    return html_output_dir
