# -*- coding: utf-8 -*-
"""Image URLs and local paths that must not be used in the guide."""

from __future__ import annotations

# Moscow Kremlin Archangel Cathedral — wrong or overused file; never reuse.
BANNED_IMAGE_URL_FRAGMENTS: tuple[str, ...] = (
    "Moscow_Arkangelsky_Cathedral.jpg",
    "arkhangelsky_1.jpg",
    "Pskov_Vasily_on_Gorka.jpg",
    "Rusakov_Workers%27_Club.jpg",
    "Rusakov_Workers'_Club.jpg",
)

BANNED_LOCAL_IMAGE_RELS: tuple[str, ...] = (
    "images/moscow_places_of_worship/arkhangelsky_1.jpg",
    "images/styles/moscow_fifteenth_sixteenth_kremlin_archangel.jpg",
)


def url_is_banned(url: str) -> bool:
    low = str(url or "").strip().lower()
    if not low:
        return False
    return any(frag.lower() in low for frag in BANNED_IMAGE_URL_FRAGMENTS)


def local_rel_is_banned(rel: str) -> bool:
    norm = str(rel or "").replace("\\", "/").strip().lower()
    if not norm:
        return False
    return any(b.lower() in norm for b in BANNED_LOCAL_IMAGE_RELS)
