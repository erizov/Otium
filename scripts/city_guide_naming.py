# -*- coding: utf-8 -*-
"""Canonical slug and image path helpers for per-city guides."""

from __future__ import annotations

import re
import urllib.parse

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
    raw = clean_place_display_title(title.strip())
    raw = re.sub(r"^\d{6,8}\s+", "", raw)
    # Drop camera/asset IDs like "(8392011668)" that often leak into filenames.
    raw = re.sub(r"\(\d{7,}\)\s*$", "", raw).strip()
    raw = raw.lower()
    raw = re.sub(r"[^a-z0-9]+", "_", raw)
    raw = re.sub(r"_+", "_", raw).strip("_")
    # Remove long numeric tokens anywhere (usually an asset ID, not a place).
    parts = [p for p in raw.split("_") if not re.fullmatch(r"\d{7,}", p)]
    raw = "_".join(parts).strip("_")
    city_key = city_slug.replace("_", " ")
    if raw in (city_slug, city_key.replace(" ", "_"), city_key):
        raw = "landmark"
    # Avoid returning numeric-only or near-empty IDs.
    if not raw or re.fullmatch(r"\d+", raw):
        raw = "landmark"
    if raw.startswith(city_slug + "_"):
        return raw[len(city_slug) + 1 :]
    return raw[:48] or "place"


def descriptive_place_slug(
    city_slug: str,
    title: str,
    used_slugs: set[str],
) -> str:
    """
    Build ``{city}_{short_id}`` from a human title; suffix on collision.

    Never uses ``pdfband`` / ``filler`` tokens — for PDF size-band rows.
    """
    short = short_id_from_title(city_slug, title)
    base = curated_place_slug(city_slug, short)
    if base not in used_slugs:
        return base
    for nn in range(2, 100):
        cand = "{}_{}".format(base, nn)
        if cand not in used_slugs:
            return cand
    return "{}_{}".format(base, len(used_slugs) + 1)


def title_for_descriptive_slug(place: dict) -> str:
    """Best display title for slug derivation from a place row."""
    filler = filler_display_title(place)
    if filler:
        return filler
    for key in ("name_en", "name_ru", "name", "subtitle_en", "subtitle_ru"):
        raw = str(place.get(key) or "").strip()
        if raw:
            cleaned = clean_place_display_title(raw)
            if cleaned:
                return cleaned
    url = str(place.get("image_source_url") or "")
    if url:
        name = url.rsplit("/", 1)[-1]
        cleaned = clean_place_display_title(
            urllib.parse.unquote(name.replace("_", " ")),
        )
        if cleaned:
            return cleaned
    return "landmark"


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
_ASSET_ID_PAREN_RE = re.compile(r"\s*\(\d{5,}\)\s*")
_LEADING_FILE_ID_RE = re.compile(r"^\d{6,8}\s+")
_TRAILING_ASSET_ID_RE = re.compile(r"\s+\d{7,}\s*$")


def clean_place_display_title(text: str) -> str:
    """
    Human place title: strip Commons filename noise and camera/asset IDs.

    Examples:
    - ``Dubai (19225459).jpeg`` → ``Dubai``
    - ``Downtown Montreal (8392011668)`` → ``Downtown Montreal``
    - ``141227 Berliner Dom`` → ``Berliner Dom``
    """
    s = clean_wikimedia_display_title(str(text).strip())
    if not s:
        return s
    s = _ASSET_ID_PAREN_RE.sub("", s).strip()
    s = _LEADING_FILE_ID_RE.sub("", s).strip()
    s = _TRAILING_ASSET_ID_RE.sub("", s).strip()
    return s.strip()


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


def filler_display_title(place: dict) -> str | None:
    """Display title for PDF-band rows from name/subtitle (any language)."""
    from scripts.city_guide_core import is_substantive_text

    for key in ("name_ru", "name_en", "subtitle_ru", "subtitle_en", "name"):
        raw = place.get(key)
        if raw is None:
            continue
        cleaned = clean_place_display_title(str(raw).strip())
        if not cleaned or not is_substantive_text(cleaned):
            continue
        if looks_like_slug_title(cleaned) or is_pdf_filler_slug(cleaned):
            continue
        return cleaned
    return None


def title_from_pdf_filler_slug(slug: str) -> str:
    """
    Last-resort title for PDF-band slugs without usable name fields.

    Never returns the raw slug (no ``pdfband``, hash suffix, or underscores).
    """
    s = str(slug).strip().lower()
    match = re.match(r"^([a-z0-9_]+)_(?:pdfband|filler)_(\d+)", s)
    if match:
        city = match.group(1).replace("_", " ").title()
        return city
    return "Landmark"


def title_from_place_slug(slug: str) -> str:
    """
    Human title from a place slug: ``dubai_gold_souk`` → ``Dubai Gold Souk``.

    PDF-band filler slugs fall back to ``title_from_pdf_filler_slug``.
    City registry slugs ``city_category_12`` drop the city and index tokens.
    """
    s = str(slug).strip()
    if not s:
        return s
    if is_pdf_filler_slug(s):
        return title_from_pdf_filler_slug(s)
    parts = s.lower().split("_")
    if len(parts) >= 3 and parts[-1].isdigit():
        tail = parts[1:-1]
        index = parts[-1]
        if tail:
            words = " ".join(tail).replace("-", " ")
            title = clean_wikimedia_display_title(words.title())
            if title:
                return "{} {}".format(title, index)
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
    if is_pdf_filler_slug(str(place.get("slug") or "")):
        filler = filler_display_title(place)
        if filler:
            return place_heading_dedupe_key(filler)
    for key in ("name_en", "name_ru", "name", "subtitle_en", "subtitle_ru"):
        raw = str(place.get(key) or "").strip()
        if raw:
            return place_heading_dedupe_key(raw)
    slug = str(place.get("slug") or "").strip()
    if slug and not is_pdf_filler_slug(slug):
        return place_heading_dedupe_key(title_from_place_slug(slug))
    return place_heading_dedupe_key(slug)


def _strip_city_suffix(key: str, city_slug: str) -> str:
    from scripts.city_guide_narrative import normalize_sentence_key
    from scripts.rag.city_map import names_for_slug

    base = normalize_sentence_key(key)
    names = names_for_slug(city_slug)
    suffixes: set[str] = set()
    for raw in (names.name_en, names.name_ru, city_slug.replace("_", " ")):
        if raw:
            suffixes.add(normalize_sentence_key(raw))
    for suffix in sorted(suffixes, key=len, reverse=True):
        if not suffix or base == suffix:
            continue
        tail = " {}".format(suffix)
        if base.endswith(tail):
            return base[: -len(tail)].strip()
    return base


def guide_heading_dedupe_key(place: dict, city_slug: str) -> str:
    """
    Primary heading key for deduplication within one city guide.

    Strips trailing city name tokens so
    ``Assumption Cathedral Yaroslavl`` matches ``Assumption Cathedral``.
    """
    return _strip_city_suffix(place_row_heading_dedupe_key(place), city_slug)


def guide_heading_dedupe_keys(place: dict, city_slug: str) -> set[str]:
    """All normalized heading keys for a row (EN, RU, subtitles, slug)."""
    keys: set[str] = {guide_heading_dedupe_key(place, city_slug)}
    for key in ("name_en", "name_ru", "name", "subtitle_en", "subtitle_ru"):
        raw = clean_wikimedia_display_title(str(place.get(key) or ""))
        if raw and not is_pdf_filler_slug(raw):
            keys.add(_strip_city_suffix(place_heading_dedupe_key(raw), city_slug))
    return {k for k in keys if k}


def image_identity_key(place: dict) -> str:
    """Normalized image URL or rel path for duplicate detection."""
    url = str(place.get("image_source_url") or "").strip().lower()
    if url:
        return url
    return str(place.get("image_rel_path") or "").strip().lower()
