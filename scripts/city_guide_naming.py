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


_IMAGE_FILE_SUFFIX_RE = re.compile(
    r"\.(?:jpe?g|png|gif|webp|svg|tiff?)\s*$",
    re.IGNORECASE,
)
_WIKIMEDIA_DISAMBIG_SUFFIX_RE = re.compile(r"\s*\([I]\)\s*$")
_WIKIMEDIA_DATE_SUFFIX_RE = re.compile(r"\s+\d{4}\s+\d{2}\s*$")
_WIKIMEDIA_TRAILING_INDEX_RE = re.compile(r"\s+\d+\s*$")
_WIKIMEDIA_TRAILING_YEAR_RE = re.compile(r"\s+\d{4}\s*$")
_COMMONS_UPLOAD_META_RE = re.compile(
    r"\s*--\s*\d{4}\s*--\s*\d+\s*$",
)
_COMMONS_LOCATION_PREFIX_RE = re.compile(
    r"^[A-Za-zÀ-ÿ\s\-]+(?:\([A-Z]{2}\))?\s*,\s*",
)
_PHOTOCHROM_SUFFIX_DIGIT_RE = re.compile(
    r"(photochrom)\d+$",
    re.IGNORECASE,
)


def clean_wikimedia_display_title(text: str) -> str:
    """
    Strip Commons filename artifacts from a place title or subtitle.

    Examples:
    - ``Scala Cinema (I).jpg`` → ``Scala Cinema``
    - ``St Louis Church Bangkok 2018 02.jpg`` → ``St Louis Church Bangkok``
    - ``Amsterdam (NL), Koninklijk Paleis -- 2015 -- 7193.jpg``
      → ``Koninklijk Paleis``
    - ``Amsterdam photochrom2.jpg`` → ``Amsterdam photochrom``
    """
    s = str(text).strip()
    if not s:
        return s
    s = _IMAGE_FILE_SUFFIX_RE.sub("", s)
    s = _COMMONS_UPLOAD_META_RE.sub("", s)
    s = _COMMONS_LOCATION_PREFIX_RE.sub("", s)
    s = _WIKIMEDIA_DISAMBIG_SUFFIX_RE.sub("", s)
    s = _WIKIMEDIA_DATE_SUFFIX_RE.sub("", s)
    s = _WIKIMEDIA_TRAILING_YEAR_RE.sub("", s)
    s = _WIKIMEDIA_TRAILING_INDEX_RE.sub("", s)
    s = _PHOTOCHROM_SUFFIX_DIGIT_RE.sub(r"\1", s)
    return s.strip()


def title_from_place_slug(slug: str) -> str:
    """
    Human title from a place slug: ``dubai_gold_souk`` → ``Dubai Gold Souk``.

    PDF-band filler slugs are left unchanged.
    """
    s = str(slug).strip()
    if not s:
        return s
    if is_pdf_filler_slug(s):
        return s
    words = s.replace("_", " ").strip()
    return clean_wikimedia_display_title(words.title())


def looks_like_slug_title(text: str) -> bool:
    """True when *text* is a lowercase slug token (``city_place_name``)."""
    s = str(text).strip()
    return bool(re.fullmatch(r"[a-z0-9_]+", s)) and "_" in s


def place_heading_dedupe_key(text: str) -> str:
    """Normalized heading key for cross-row PDF deduplication."""
    from scripts.city_guide_narrative import normalize_sentence_key

    cleaned = clean_wikimedia_display_title(str(text).strip())
    return normalize_sentence_key(cleaned)


def place_row_heading_dedupe_key(place: dict) -> str:
    """Dedupe key from the best available place title fields."""
    for key in ("name_en", "name_ru", "name", "subtitle_en", "subtitle_ru"):
        raw = str(place.get(key) or "").strip()
        if raw:
            return place_heading_dedupe_key(raw)
    slug = str(place.get("slug") or "").strip()
    if slug and not is_pdf_filler_slug(slug):
        return place_heading_dedupe_key(title_from_place_slug(slug))
    return place_heading_dedupe_key(slug)
