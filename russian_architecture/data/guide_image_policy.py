# -*- coding: utf-8 -*-
"""Per-place image rules for the architecture guide."""

from __future__ import annotations

from typing import Any

# Places that must show only the primary photo in HTML/PDF.
SINGLE_IMAGE_SLUGS: frozenset[str] = frozenset({
    "postmodernism_moscow_theaters_4_2",
    "tent_roof_st_basil",
    "constructivism_narkomfin",
    "post_constructivism_moscow_osobnjaki_24_2",
    "post_constructivism_moscow_osobnjaki_20_2",
    "post_constructivism_moscow_buildings_2_2",
    "neoclassicism_early20_moscow_buildings_11_2",
    "art_deco_moscow_railway_stations_6_2",
    "constructivism_moscow_osobnjaki_25_2",
    "avant_garde_moscow_buildings_2_2",
    "constructivism_moscow_buildings_2_2",
    "avant_garde_moscow_buildings_29_2",
    "constructivism_moscow_buildings_29_2",
    "neoclassicism_early20_moscow_osobnjaki_48_2",
    "neoclassicism_early20_moscow_osobnjaki_38_2",
    "stalinist_moscow_buildings_30_2",
    "stalinist_neoclassicism_moscow_buildings_30_2",
    "art_deco_moscow_buildings_30_2",
    "post_constructivism_moscow_buildings_30_2",
    "soviet_neoclassicism_revival_moscow_buildings_30_2",
    "avant_garde_moscow_libraries_0_2",
    "stalinist_neoclassicism_moscow_libraries_0_2",
    "soviet_neoclassicism_revival_moscow_libraries_0_2",
    "soviet_modernism_moscow_buildings_22_2",
    "naryshkin_baroque_trinity_lykovo",
    "eclecticism_moscow_osobnjaki_5_2",
    "eclecticism_moscow_osobnjaki_4_2",
    "eclecticism_moscow_osobnjaki_7_2",
    "eclecticism_moscow_buildings_37_2",
    "russo_byzantine_christ_savior",
    "neo_russian_yaroslavsky_station",
    "art_nouveau_vitebsky_station",
    "neo_russian_moscow_osobnjaki_2_2",
    "post_constructivism_zil_palace",
})


def strip_extra_images(place: dict[str, Any]) -> dict[str, Any]:
    """Drop ``additional_images`` for single-image slugs."""
    slug = str(place.get("slug") or "")
    if slug not in SINGLE_IMAGE_SLUGS:
        return place
    if not place.get("additional_images"):
        return place
    out = dict(place)
    out.pop("additional_images", None)
    return out
