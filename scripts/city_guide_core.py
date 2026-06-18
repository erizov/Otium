# -*- coding: utf-8 -*-
"""Shared helpers for per-city guide builds (Smolensk-style PDF/HTML)."""

from __future__ import annotations

import shutil
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any, TypeVar

from scripts.city_guide_naming import is_pdf_filler_slug

_P = TypeVar("_P", bound=dict[str, Any])

MIN_IMAGE_BYTES = 500
_MIN_VECTOR_BYTES = 32

# PDF: show 1 image when only one exists on disk; up to 2 when two+ exist.
PDF_MAX_IMAGES_PER_PLACE = 2
# Registry-style downloads: primary + extras, capped at 2 total per place.
DOWNLOAD_MAX_IMAGES_PER_PLACE = 2
# Do not fetch missing place photos for these cities (use on-disk only).
DOWNLOAD_FROZEN_CITY_SLUGS: frozenset[str] = frozenset({"moscow", "spb"})


def should_skip_city_place_downloads(city_slug: str) -> bool:
    """True when registry downloads must not add place images."""
    return city_slug.strip().lower() in DOWNLOAD_FROZEN_CITY_SLUGS


def additional_images_for_download(
    place: dict[str, Any],
    *,
    max_total: int | None = None,
) -> list[Any]:
    """``additional_images`` entries to attempt (excludes primary slot)."""
    cap = max_total if max_total is not None else DOWNLOAD_MAX_IMAGES_PER_PLACE
    extras = place.get("additional_images") or []
    return list(extras[: max(0, cap - 1)])

# Food venues are out of scope for curated sightseeing guides.
EXCLUDED_PLACE_CATEGORIES: frozenset[str] = frozenset({
    "cafes",
    "restaurants",
    "cafe",
    "restaurant",
})


def is_excluded_place_category(category: str | None) -> bool:
    """True when a place row should not appear in city guides."""
    if not category:
        return False
    return str(category).strip().lower() in EXCLUDED_PLACE_CATEGORIES


def drop_excluded_category_places(places: Sequence[_P]) -> list[_P]:
    """Remove cafe/restaurant category rows from a place list."""
    return [
        p for p in places
        if not is_excluded_place_category(str(p.get("category") or ""))
    ]


# Lone filler tokens in JSON/detail merges — omit section if only this.
_PLACEHOLDER_TOKENS: frozenset[str] = frozenset({
    "—",
    "–",
    "-",
    "…",
    "...",
    "n/a",
    "na",
    "n.a.",
    "tbd",
    "tbc",
})


def is_curated_place_row(place: dict) -> bool:
    """Exclude PDF size-band filler rows from editorial stats."""
    return not is_pdf_filler_slug(str(place.get("slug") or ""))


def is_substantive_text(value: str | None) -> bool:
    """
    True when value is non-empty and not a single placeholder token.

    Used so Facts / History / Significance (and meta lines) stay hidden
    when source data only contains an em dash or similar stub.
    """
    if value is None:
        return False
    s = str(value).strip()
    if not s:
        return False
    if s in _PLACEHOLDER_TOKENS:
        return False
    if s.lower() in _PLACEHOLDER_TOKENS:
        return False
    return True


def copy_built_guide_pdf_to_final_guides(
    project_root: Path,
    pdf_path: Path,
) -> None:
    """
    Mirror a finished city-guide PDF under ``<repo>/final_guides/``.

    Called after Playwright PDF + strip steps so ``final_guides/`` stays a
    single folder of latest builds (filenames match ``*_guide.pdf``, etc.).
    """
    src = pdf_path.resolve()
    if not src.is_file():
        return
    dest_dir = project_root.resolve() / "final_guides"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    shutil.copy2(src, dest)
    print("Copied to final_guides:", dest.as_posix())


def min_bytes_for_filename(filename: str) -> int:
    """Raster images need a size floor; tiny SVG/GIF are still valid."""
    suf = Path(filename).suffix.lower()
    if suf in (".svg", ".gif"):
        return _MIN_VECTOR_BYTES
    return MIN_IMAGE_BYTES


def smallest_same_stem_image_rel(root: Path, rel: str) -> str | None:
    """
    Among files sharing the same stem (foo.jpg, foo.webp, …), pick the
    smallest by bytes that is still >= MIN_IMAGE_BYTES.
    """
    root_res = root.resolve()
    rel_clean = rel.replace("\\", "/").lstrip("/")
    base = root_res / rel_clean
    parent = base.parent
    stem = base.stem
    if not parent.is_dir():
        return None
    sized: list[tuple[Path, int]] = []
    try:
        for path in parent.iterdir():
            if not path.is_file() or path.stem != stem:
                continue
            size = path.stat().st_size
            if size >= min_bytes_for_filename(path.name):
                sized.append((path, size))
    except OSError:
        return None
    if not sized:
        return None
    best = min(sized, key=lambda t: t[1])[0]
    try:
        return best.resolve().relative_to(root_res).as_posix()
    except ValueError:
        return None


def place_has_pdf_image(root: Path, place: _P) -> bool:
    """True when a lead or extra image resolves under *root*."""
    rel = place.get("image_rel_path")
    if rel and smallest_same_stem_image_rel(root, rel):
        return True
    for item in place.get("additional_images") or []:
        er = item.get("image_rel_path")
        if er and smallest_same_stem_image_rel(root, er):
            return True
    return False


def _pdfband_duplicates_curated(
    filler: _P,
    curated: Sequence[_P],
) -> bool:
    """True when a PDF sidecar row repeats an existing curated place."""
    from scripts.city_guide_naming import (
        clean_wikimedia_display_title,
        is_pdf_filler_slug,
        place_row_heading_dedupe_key,
    )

    if not is_pdf_filler_slug(str(filler.get("slug") or "")):
        return False
    filler_key = place_row_heading_dedupe_key(filler)
    desc = str(filler.get("description") or "").lower()
    for row in curated:
        if place_row_heading_dedupe_key(row) == filler_key:
            return True
        for key in ("name_en", "name_ru", "name", "subtitle_en"):
            cname = clean_wikimedia_display_title(
                str(row.get(key) or ""),
            ).lower()
            if len(cname) >= 8 and cname in desc:
                return True
        cur_key = place_row_heading_dedupe_key(row)
        ft = {w for w in filler_key.split() if len(w) >= 6}
        ct = {w for w in cur_key.split() if len(w) >= 6}
        if ft & ct:
            return True
    return False


def dedupe_curated_places(
    places: Sequence[_P],
    city_slug: str,
) -> list[_P]:
    """
    Drop curated rows that repeat the same heading or image in one guide.

    Keeps the first row in list order.
    """
    from scripts.city_guide_naming import (
        guide_heading_dedupe_keys,
        image_identity_key,
        is_pdf_filler_slug,
    )

    out: list[_P] = []
    seen_heading: set[str] = set()
    seen_image: set[str] = set()
    for p in places:
        slug = str(p.get("slug") or "")
        if is_pdf_filler_slug(slug):
            out.append(p)
            continue
        headings = guide_heading_dedupe_keys(p, city_slug)
        image = image_identity_key(p)
        if headings & seen_heading:
            continue
        if image and image in seen_image:
            continue
        seen_heading.update(headings)
        if image:
            seen_image.add(image)
        out.append(p)
    return out


def dedupe_pdf_sidecar_places(
    places: Sequence[_P],
    *,
    city_slug: str = "",
) -> list[_P]:
    """
    Drop duplicate curated rows and PDF sidecar rows within one guide.

    Keeps the first row in source order per heading (city-aware) or image URL.
    """
    from scripts.city_guide_naming import (
        guide_heading_dedupe_key,
        guide_heading_dedupe_keys,
        image_identity_key,
        is_pdf_filler_slug,
        place_row_heading_dedupe_key,
    )

    out: list[_P] = []
    seen_heading: set[str] = set()
    seen_image: set[str] = set()
    curated: list[_P] = []
    for p in places:
        slug = str(p.get("slug") or "")
        if not is_pdf_filler_slug(slug):
            headings = (
                guide_heading_dedupe_keys(p, city_slug)
                if city_slug
                else {place_row_heading_dedupe_key(p)}
            )
            image = image_identity_key(p)
            if headings & seen_heading:
                continue
            if image and image in seen_image:
                continue
            seen_heading.update(headings)
            if image:
                seen_image.add(image)
            curated.append(p)
            out.append(p)
            continue
        heading = place_row_heading_dedupe_key(p)
        if city_slug:
            heading = guide_heading_dedupe_key(p, city_slug)
        image = image_identity_key(p)
        if (
            heading in seen_heading
            or (image and image in seen_image)
            or _pdfband_duplicates_curated(p, curated)
        ):
            continue
        seen_heading.add(heading)
        if image:
            seen_image.add(image)
        out.append(p)
    return out


def places_for_pdf(
    root: Path,
    places: Sequence[_P],
    *,
    city_slug: str = "",
    sort_key: Callable[[_P], Any] | None = None,
    dedupe_sidecar: bool = True,
    include_food_venues: bool | None = None,
) -> list[_P]:
    """
    Places eligible for PDF/HTML export: must have a local image on disk.

    ``suppress_images_for_pdf`` rows are omitted (no text-only fallback).
    Moscow includes historical cafes (Complete Guide ch. 19).
    """
    if include_food_venues is None:
        include_food_venues = city_slug.strip().lower() == "moscow"
    if include_food_venues:
        rows = list(places)
    else:
        rows = drop_excluded_category_places(list(places))
    if dedupe_sidecar:
        rows = dedupe_pdf_sidecar_places(rows, city_slug=city_slug)
    out = [p for p in rows if place_has_pdf_image(root, p)]
    if sort_key is not None:
        out.sort(key=sort_key)
    return out
