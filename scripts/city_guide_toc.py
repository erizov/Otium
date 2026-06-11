# -*- coding: utf-8 -*-
"""Table of contents for city guide HTML/PDF (en/ru editions)."""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from scripts.city_guide_core import places_for_pdf
from scripts.city_guide_front_matter import (
    CITIES_WITHOUT_TRIP_ROUTES,
    load_front_matter,
    primer_section_html,
    proximity_trip_plans_section_html,
    trip_plans_section_html,
    _primer_headings,
    _trip_headings,
)
from scripts.city_guide_historical_reference_ru import (
    HISTORICAL_SECTION_TITLE_EN,
    HISTORICAL_SECTION_TITLE_RU,
    reference_text_en_for_any_city,
    reference_text_ru_for_any_city,
)
from scripts.city_guide_narrative import place_heading_plain

GUIDE_HISTORICAL_ID = "guide-historical"
GUIDE_PRIMER_ID = "guide-primer"
GUIDE_TRIPS_ID = "guide-trips"
GUIDE_UNIVERSITIES_ID = "guide-universities"
GUIDE_MODERN_SMOLENSK_ID = "guide-modern-smolensk"
GUIDE_WELCOME_CLOSING_ID = "guide-welcome-closing"


@dataclass(frozen=True)
class GuideTocEntry:
    """One TOC row: in-document anchor and display label."""

    anchor: str
    label: str
    level: int = 1


def guide_toc_title(edition: str) -> str:
    """Localized TOC heading."""
    return "Содержание" if edition == "ru" else "Contents"


def category_chapter_anchor(category: str) -> str:
    """Stable chapter anchor for category-grouped guides."""
    slug = str(category or "misc").strip().lower().replace("_", "-")
    return "cat-{}".format(slug)


def guide_toc_html(entries: Sequence[GuideTocEntry], edition: str) -> str:
    """Render TOC nav block; empty when there are no entries."""
    if not entries:
        return ""
    items: list[str] = []
    for entry in entries:
        li_class = "toc-item"
        if entry.level > 1:
            li_class += " toc-item--sub"
        items.append(
            '<li class="{}"><a href="#{}">{}</a></li>'.format(
                li_class,
                escape(entry.anchor),
                escape(entry.label),
            )
        )
    title = guide_toc_title(edition)
    return (
        '<nav class="guide-toc" aria-label="{}">'
        "<h2>{}</h2>"
        "<ol>{}</ol>"
        "</nav>"
    ).format(escape(title), escape(title), "".join(items))


def _historical_toc_entry(
    city_slug: str,
    edition: str,
    project_root: Path | None,
) -> GuideTocEntry | None:
    if project_root is None:
        return None
    slug = city_slug.strip().lower()
    if edition == "ru":
        body = reference_text_ru_for_any_city(slug, project_root)
        title = HISTORICAL_SECTION_TITLE_RU
    else:
        body = reference_text_en_for_any_city(slug, project_root)
        title = HISTORICAL_SECTION_TITLE_EN
    if not body or not str(body).strip():
        return None
    return GuideTocEntry(GUIDE_HISTORICAL_ID, title)


def _primer_toc_entry(
    project_root: Path | None,
    city_slug: str,
    edition: str,
) -> GuideTocEntry | None:
    if project_root is None:
        return None
    data = load_front_matter(project_root, city_slug)
    if not data or not primer_section_html(data, edition):
        return None
    return GuideTocEntry(
        GUIDE_PRIMER_ID,
        _primer_headings(edition)["section"],
    )


def _trips_toc_entry(
    project_root: Path | None,
    city_slug: str,
    edition: str,
    pdf_places: Sequence[Mapping[str, Any]],
) -> GuideTocEntry | None:
    if project_root is None:
        return None
    slug = city_slug.strip().lower()
    if slug in CITIES_WITHOUT_TRIP_ROUTES:
        return None
    block = proximity_trip_plans_section_html(
        slug,
        edition,
        pdf_places,
        project_root=project_root,
    )
    if not block:
        data = load_front_matter(project_root, city_slug)
        if data:
            block = trip_plans_section_html(data, edition, pdf_places)
    if not block:
        return None
    return GuideTocEntry(
        GUIDE_TRIPS_ID,
        _trip_headings(edition)["section"],
    )


def toc_entries_for_flat_places(
    places: Sequence[Mapping[str, Any]],
    edition: str,
) -> list[GuideTocEntry]:
    """TOC rows for place sections (same order as rendered sections)."""
    rows: list[GuideTocEntry] = []
    for place in places:
        slug = str(place.get("slug") or "").strip()
        if not slug:
            continue
        rows.append(
            GuideTocEntry(
                slug,
                place_heading_plain(place, edition),
            )
        )
    return rows


def toc_entries_for_jerusalem_guide(
    root: Path,
    places: Sequence[Mapping[str, Any]],
    edition: str,
    *,
    city_slug: str,
    project_root: Path | None,
    sort_key: Callable[[Mapping[str, Any]], Any],
    has_section: Callable[[Path, Mapping[str, Any]], bool],
) -> list[GuideTocEntry]:
    """
    Build TOC for Jerusalem-style guides from the same place filter as HTML.
    """
    pdf_places = places_for_pdf(
        root,
        places,
        city_slug=city_slug,
        sort_key=sort_key,
    )
    section_places = [p for p in pdf_places if has_section(root, p)]
    entries: list[GuideTocEntry] = []
    hist = _historical_toc_entry(city_slug, edition, project_root)
    if hist:
        entries.append(hist)
    primer = _primer_toc_entry(project_root, city_slug, edition)
    if primer:
        entries.append(primer)
    trips = _trips_toc_entry(project_root, city_slug, edition, section_places)
    if trips:
        entries.append(trips)
    entries.extend(toc_entries_for_flat_places(section_places, edition))
    return entries


def toc_entries_for_category_guide(
    places: Sequence[Mapping[str, Any]],
    edition: str,
    *,
    chapter_title: Callable[[str, int, str], tuple[str, str]],
    counts_by_category: Mapping[str, int],
    has_section: Callable[[Mapping[str, Any]], bool],
) -> list[GuideTocEntry]:
    """TOC with category chapters and nested place links (SPB-style)."""
    entries: list[GuideTocEntry] = []
    last_cat: str | None = None
    for place in places:
        if not has_section(place):
            continue
        cat = str(place.get("category") or "misc")
        if cat != last_cat:
            h2, _sub = chapter_title(cat, counts_by_category.get(cat, 0), edition)
            entries.append(
                GuideTocEntry(
                    category_chapter_anchor(cat),
                    h2,
                    level=1,
                )
            )
            last_cat = cat
        slug = str(place.get("slug") or "").strip()
        if not slug:
            continue
        entries.append(
            GuideTocEntry(
                slug,
                place_heading_plain(place, edition),
                level=2,
            )
        )
    return entries
