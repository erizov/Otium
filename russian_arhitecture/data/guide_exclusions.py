# -*- coding: utf-8 -*-
"""Places and pool entries excluded from the architecture guide."""

from __future__ import annotations

# Catalog seed suffixes skipped in generate (style_catalog STYLE_EXAMPLES).
EXCLUDED_CATALOG_SUFFIXES: frozenset[str] = frozenset({
    "rodina_cinema",
    "kyiv_sophia",
    "zaryadye_park",
    "vdnh_pavilion_revival",
})

# Generated slug suffixes skipped after row assembly.
EXCLUDED_SLUG_SUFFIXES: frozenset[str] = frozenset({
    "kyiv_saint_sophia_2",
    "rodina_cinema",
    "moscow_osobnjaki_22_2",
    "contemporary_zaryadye_park",
    "soviet_neoclassicism_revival_vdnh_pavilion_revival",
})

# (style_key, city, place_slug) tuples removed from CITY_STYLE_POOL fill.
EXCLUDED_POOL_ENTRIES: frozenset[tuple[str, str, str]] = frozenset({
    ("ancient_rus", "kyiv", "kyiv_saint_sophia"),
    ("constructivism", "moscow", "moscow_osobnjaki_22"),
    ("constructivism", "moscow", "moscow_buildings_32"),
    ("avant_garde", "moscow", "moscow_buildings_32"),
    ("post_constructivism", "moscow", "moscow_buildings_32"),
    ("stalinist_neoclassicism", "moscow", "moscow_buildings_30"),
    ("art_deco", "moscow", "moscow_buildings_30"),
    ("post_constructivism", "moscow", "moscow_buildings_30"),
    ("soviet_neoclassicism_revival", "moscow", "moscow_buildings_30"),
    ("empire", "moscow", "moscow_metro_1"),
    ("stalinist_neoclassicism", "moscow", "moscow_metro_1"),
    ("art_deco", "moscow", "moscow_metro_1"),
    ("soviet_neoclassicism_revival", "moscow", "moscow_metro_1"),
    ("stalinist_neoclassicism", "moscow", "moscow_buildings_17"),
    ("art_deco", "moscow", "moscow_buildings_17"),
    ("panel_housing", "moscow", "moscow_buildings_9"),
    ("brutalism", "moscow", "moscow_buildings_9"),
    ("brutalism", "moscow", "moscow_buildings_22"),
    ("postmodernism", "moscow", "moscow_buildings_22"),
    ("moscow_fifteenth_sixteenth", "moscow", "moscow_places_of_worship_1"),
    ("tent_roof", "moscow", "moscow_places_of_worship_1"),
    ("soviet_modernism", "moscow", "moscow_landmarks_4"),
    ("contemporary", "moscow", "moscow_landmarks_4"),
    ("regional_soviet", "novosibirsk", "novosibirsk_business_centre"),
})


def is_catalog_suffix_excluded(suffix: str) -> bool:
    return suffix.strip() in EXCLUDED_CATALOG_SUFFIXES


def is_slug_excluded(slug: str) -> bool:
    low = slug.strip().lower()
    return any(low.endswith(suf) for suf in EXCLUDED_SLUG_SUFFIXES)


def is_pool_entry_excluded(
    style_key: str,
    city: str,
    place_slug: str,
) -> bool:
    return (style_key, city, place_slug) in EXCLUDED_POOL_ENTRIES


def pool_for_style(style_key: str) -> list[tuple[str, str]]:
    """Return CITY_STYLE_POOL entries for *style_key* minus exclusions."""
    from russian_arhitecture.data.city_style_pool import CITY_STYLE_POOL

    out: list[tuple[str, str]] = []
    for city, place_slug in CITY_STYLE_POOL.get(style_key, []):
        if is_pool_entry_excluded(style_key, city, place_slug):
            continue
        out.append((city, place_slug))
    return out
