# -*- coding: utf-8 -*-
"""Canonical slug and image path helpers for per-city guides."""

from __future__ import annotations

import re

# Legacy PDF size-band rows (pre-unification).
_LEGACY_PDFBAND_RE = re.compile(r"^([a-z0-9_]+)_(?:pdfband|filler)_")
_FILLER_RE = re.compile(r"^([a-z0-9_]+)_filler_([a-z0-9_]+)_(\d+)$")

# Cities that may omit the city prefix on curated slugs (legacy guides).
LEGACY_UNPREFIXED_CITIES: frozenset[str] = frozenset({"smolensk", "spb"})


def curated_place_slug(city_slug: str, short_id: str) -> str:
    """Build ``{city}_{short_id}`` slug (ASCII, lowercase, underscores)."""
    city = city_slug.strip().lower()
    sid = short_id.strip().lower().replace("-", "_")
    sid = re.sub(r"[^a-z0-9_]+", "_", sid)
    sid = re.sub(r"_+", "_", sid).strip("_")
    if sid.startswith(city + "_"):
        return sid
    return "{}_{}".format(city, sid)


def image_rel_path_for_slug(place_slug: str) -> str:
    return "images/{}.jpg".format(place_slug)


def filler_place_slug(city_slug: str, category: str, nn: int) -> str:
    """Stable filler slug: ``{city}_filler_{category}_{nn:02d}``."""
    cat = category.strip().lower().replace("-", "_")
    cat = re.sub(r"[^a-z0-9_]+", "_", cat)
    cat = re.sub(r"_+", "_", cat).strip("_") or "landmark"
    return "{}_filler_{}_{:02d}".format(city_slug.strip().lower(), cat, nn)


def pdf_expand_sidecar_filename(city_slug: str) -> str:
    return "{}_places_pdf_expand.json".format(city_slug.strip().lower())


def is_pdf_filler_slug(slug: str) -> bool:
    s = str(slug or "").strip().lower()
    return "_pdfband_" in s or "_filler_" in s


def is_curated_place_slug(slug: str, city_slug: str) -> bool:
    """True when slug is not a PDF filler and matches naming rules."""
    s = str(slug or "").strip().lower()
    if not s or is_pdf_filler_slug(s):
        return False
    if city_slug in LEGACY_UNPREFIXED_CITIES:
        return True
    return s.startswith(city_slug.strip().lower() + "_")


def short_id_from_title(city_slug: str, title: str) -> str:
    """Derive a short_id from a display title (for migrations)."""
    raw = title.strip().lower()
    raw = re.sub(r"[^a-z0-9]+", "_", raw)
    raw = re.sub(r"_+", "_", raw).strip("_")
    if raw.startswith(city_slug + "_"):
        return raw[len(city_slug) + 1 :]
    return raw[:48] or "place"
