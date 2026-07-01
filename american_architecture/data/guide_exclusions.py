# -*- coding: utf-8 -*-
"""Places and pool entries excluded from the architecture guide."""

from __future__ import annotations

EXCLUDED_CATALOG_SUFFIXES: frozenset[str] = frozenset()
EXCLUDED_SLUG_SUFFIXES: frozenset[str] = frozenset()
EXCLUDED_POOL_ENTRIES: frozenset[tuple[str, str, str]] = frozenset()


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
    from american_architecture.data.city_style_pool import CITY_STYLE_POOL

    out: list[tuple[str, str]] = []
    for city, place_slug in CITY_STYLE_POOL.get(style_key, []):
        if is_pool_entry_excluded(style_key, city, place_slug):
            continue
        out.append((city, place_slug))
    return out
