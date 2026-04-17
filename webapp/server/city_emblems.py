# -*- coding: utf-8 -*-
"""Detect per-city emblem assets for the web editor UI."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from webapp.server.country_emblem_download import (
    ensure_country_emblem_svg,
    is_placeholder_emblem,
)


@dataclass(frozen=True)
class CityEmblems:
    city_emblem_url: str | None
    city_flag_url: str | None
    country_flag_url: str | None
    country_emblem_url: str | None


def _first_existing(root: Path, rel_candidates: list[str]) -> str | None:
    for rel in rel_candidates:
        rel_clean = rel.replace("\\", "/").lstrip("/")
        if (root / rel_clean).is_file():
            return rel_clean
    return None


def emblems_for_city(project_root: Path, city_slug: str) -> CityEmblems:
    """
    Return URLs for the city emblem, city flag, and country flag.

    Convention used by the per-city guide builders: `images/guide_coat_of_arms.*`
    and `images/guide_flag.*` inside each `<city>/images/` directory.

    Note: `images/guide_flag.*` is often a city flag in this repo; the country
    flag is provided by this webapp from `webapp/server/static/flags/`.
    """
    city_root = project_root / city_slug
    city_rel = _first_existing(
        city_root,
        [
            "images/guide_coat_of_arms.svg",
            "images/guide_coat_of_arms.png",
            "images/guide_coat_of_arms.jpg",
            "images/guide_coat_of_arms.webp",
        ],
    )
    city_flag_rel = _first_existing(
        city_root,
        [
            "images/guide_flag.svg",
            "images/guide_flag.png",
            "images/guide_flag.jpg",
            "images/guide_flag.webp",
        ],
    )
    country_code = _country_code_for_city(city_slug)
    static_root = Path(__file__).resolve().parent / "static"
    country_flag_url = None
    country_emblem_url = None
    if country_code:
        flag_path = static_root / "flags" / f"{country_code}.svg"
        if flag_path.is_file():
            country_flag_url = f"/static/flags/{country_code}.svg"
        emblem_path = static_root / "emblems" / f"{country_code}.svg"
        ok = ensure_country_emblem_svg(static_root, country_code)
        if emblem_path.is_file() and not is_placeholder_emblem(emblem_path):
            country_emblem_url = f"/static/emblems/{country_code}.svg"
        elif emblem_path.is_file() and is_placeholder_emblem(emblem_path) and ok is False:
            try:
                emblem_path.unlink()
            except OSError:
                pass
    city_url = None
    if city_rel and (city_root / city_rel).is_file():
        city_url = f"/city/{city_slug}/{city_rel}"
    city_flag_url = None
    if city_flag_rel and (city_root / city_flag_rel).is_file():
        city_flag_url = f"/city/{city_slug}/{city_flag_rel}"
    return CityEmblems(
        city_emblem_url=city_url,
        city_flag_url=city_flag_url,
        country_flag_url=country_flag_url,
        country_emblem_url=country_emblem_url,
    )


def _country_code_for_city(city_slug: str) -> str | None:
    city_to_country: dict[str, str] = {
        "smolensk": "ru",
        "spb": "ru",
        "berlin": "de",
        "paris": "fr",
        "rome": "it",
        "venice": "it",
        "florence": "it",
        "barcelona": "es",
        "madrid": "es",
        "prague": "cz",
        "budapest": "hu",
        "vienna": "at",
        "boston": "us",
        "philadelphia": "us",
        "new_york": "us",
        "montreal": "ca",
        "jerusalem": "il",
    }
    return city_to_country.get(city_slug)

