# -*- coding: utf-8 -*-
"""City primer and trip-plan front matter for guide PDFs."""

from __future__ import annotations

import json
from html import escape
from pathlib import Path
from typing import Any, Mapping, Sequence

from scripts.city_guide_core import is_substantive_text
from scripts.city_guide_naming import is_pdf_filler_slug
from scripts.city_guide_narrative import place_heading_plain

ITINERARY_KEYS: tuple[str, ...] = ("1d", "3d1", "3d2", "3d3")

# Large chapter-based guides: no proximity trip section in PDF/HTML.
CITIES_WITHOUT_TRIP_ROUTES: frozenset[str] = frozenset({"moscow", "spb"})

_PRIMER_HEADINGS_EN: dict[str, str] = {
    "section": "City primer",
    "climate": "Climate",
    "transport": "Getting around",
    "etiquette": "Etiquette",
}
_PRIMER_HEADINGS_RU: dict[str, str] = {
    "section": "Практическая справка",
    "climate": "Климат",
    "transport": "Транспорт",
    "etiquette": "Этикет",
}
_TRIP_HEADINGS_EN: dict[str, str] = {
    "section": "Trip ideas",
    "1d": "One day",
    "3d1": "Three days — day 1",
    "3d2": "Three days — day 2",
    "3d3": "Three days — day 3",
}
_TRIP_HEADINGS_RU: dict[str, str] = {
    "section": "Маршруты",
    "1d": "Один день",
    "3d1": "Три дня — день 1",
    "3d2": "Три дня — день 2",
    "3d3": "Три дня — день 3",
}


def front_matter_json_path(project_root: Path, city_slug: str) -> Path:
    """``<city>/data/<city>_guide_front.json``."""
    slug = city_slug.strip().lower()
    return project_root / slug / "data" / "{}_guide_front.json".format(slug)


def load_front_matter(
    project_root: Path,
    city_slug: str,
) -> dict[str, Any] | None:
    path = front_matter_json_path(project_root, city_slug)
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else None


def save_front_matter(
    project_root: Path,
    city_slug: str,
    data: Mapping[str, Any],
) -> Path:
    path = front_matter_json_path(project_root, city_slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(dict(data), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def _edition_block(
    root: Mapping[str, Any],
    edition: str,
) -> dict[str, Any] | None:
    block = root.get(edition)
    if isinstance(block, dict):
        return block
    return None


def _primer_headings(edition: str) -> dict[str, str]:
    return _PRIMER_HEADINGS_RU if edition == "ru" else _PRIMER_HEADINGS_EN


def _trip_headings(edition: str) -> dict[str, str]:
    return _TRIP_HEADINGS_RU if edition == "ru" else _TRIP_HEADINGS_EN


def _prose_paragraphs(text: str) -> str:
    chunks = [t.strip() for t in str(text).split("\n\n") if t.strip()]
    if not chunks and str(text).strip():
        chunks = [str(text).strip()]
    return "\n".join(
        '<p class="prose">{}</p>'.format(escape(c)) for c in chunks
    )


def _primer_subsection(title: str, body: str) -> str:
    text = str(body).strip()
    if not text:
        return ""
    return (
        "<h3>{}</h3>\n{}".format(escape(title), _prose_paragraphs(text))
    )


def primer_section_html(
    data: Mapping[str, Any],
    edition: str,
) -> str:
    """Primer block (climate, transport, etiquette) for one edition."""
    block = _edition_block(data.get("primer") or {}, edition)
    if not block:
        return ""
    h = _primer_headings(edition)
    parts: list[str] = []
    for key in ("climate", "transport", "etiquette"):
        chunk = _primer_subsection(h[key], str(block.get(key) or ""))
        if chunk:
            parts.append(chunk)
    for para in block.get("overview_paragraphs") or []:
        text = str(para).strip()
        if text:
            parts.append('<p class="prose">{}</p>'.format(escape(text)))
    if not parts:
        return ""
    from scripts.city_guide_toc import guide_toc_back_link_html

    return (
        '<section class="guide-primer" id="{id}" aria-label="{title}">'
        "<h2>{title}</h2>\n"
        "{back}\n"
        "{body}"
        "</section>"
    ).format(
        id="guide-primer",
        title=escape(h["section"]),
        back=guide_toc_back_link_html(edition),
        body="\n".join(parts),
    )


def _stop_display_name(
    stop: Mapping[str, Any],
    places_by_slug: Mapping[str, Mapping[str, Any]],
    edition: str,
) -> str:
    slug = str(stop.get("slug") or "").strip()
    if slug and slug in places_by_slug:
        return place_heading_plain(places_by_slug[slug], edition)
    name = str(stop.get("name") or "").strip()
    if name:
        return name
    return slug or "—"


def _itinerary_article(
    key: str,
    plan: Mapping[str, Any],
    *,
    edition: str,
    places_by_slug: Mapping[str, Mapping[str, Any]],
    trip_h: Mapping[str, str],
) -> str:
    title = str(plan.get("title") or "").strip() or trip_h.get(key, key)
    intro = str(plan.get("intro") or "").strip()
    stops = plan.get("stops")
    if not isinstance(stops, list) or not stops:
        return ""
    items: list[str] = []
    for stop in stops:
        if not isinstance(stop, dict):
            continue
        slug = str(stop.get("slug") or "").strip()
        note = str(stop.get("note") or "").strip()
        minutes = stop.get("minutes")
        label = _stop_display_name(stop, places_by_slug, edition)
        time_bit = ""
        if isinstance(minutes, (int, float)) and minutes > 0:
            unit = "мин" if edition == "ru" else "min"
            time_bit = " (~{}{})".format(int(minutes), unit)
        anchor = (
            '<a href="#{}">{}</a>'.format(escape(slug), escape(label))
            if slug
            else escape(label)
        )
        line = "<li>{}".format(anchor + escape(time_bit))
        if note:
            line += " — {}".format(escape(note))
        line += "</li>"
        items.append(line)
    if not items:
        return ""
    intro_html = _prose_paragraphs(intro) if intro else ""
    return (
        '<article class="trip-plan" id="trip-{}">'
        "<h3>{}</h3>\n"
        "{}\n"
        '<ol class="trip-stops">{}</ol>'
        "</article>"
    ).format(
        escape(key),
        escape(title),
        intro_html,
        "\n".join(items),
    )


def trip_plans_section_html(
    data: Mapping[str, Any],
    edition: str,
    places: Sequence[Mapping[str, Any]],
) -> str:
    """Trip planning block (1d / 3d1–3d3) for one edition."""
    root = data.get("itineraries")
    if not isinstance(root, dict):
        return ""
    block = _edition_block(root, edition)
    if not block:
        return ""
    places_by_slug = {
        str(p.get("slug") or ""): p
        for p in places
        if str(p.get("slug") or "")
    }
    trip_h = _trip_headings(edition)
    articles: list[str] = []
    for key in ITINERARY_KEYS:
        plan = block.get(key)
        if not isinstance(plan, dict):
            continue
        art = _itinerary_article(
            key,
            plan,
            edition=edition,
            places_by_slug=places_by_slug,
            trip_h=trip_h,
        )
        if art:
            articles.append(art)
    if not articles:
        return ""
    from scripts.city_guide_toc import guide_toc_back_link_html

    return (
        '<section class="guide-trip-plans" id="guide-trips" aria-label="{title}">'
        "<h2>{title}</h2>\n"
        "{back}\n"
        "{body}"
        "</section>"
    ).format(
        title=escape(trip_h["section"]),
        back=guide_toc_back_link_html(edition),
        body="\n".join(articles),
    )


def proximity_trip_plans_section_html(
    city_slug: str,
    edition: str,
    places: Sequence[Mapping[str, Any]],
    *,
    project_root: Path | None,
) -> str:
    """Proximity-optimised 1-day and 3-day routes from guide places."""
    from scripts.city_guide_proximity_routes import (
        proximity_itineraries_for_edition,
    )

    if not places:
        return ""
    block = proximity_itineraries_for_edition(
        places,
        city_slug,
        edition,
        project_root=project_root,
    )
    if not block:
        return ""
    wrapper = {"itineraries": {edition: block}}
    return trip_plans_section_html(wrapper, edition, places)


def front_matter_html_blocks(
    project_root: Path | None,
    city_slug: str,
    edition: str,
    places: Sequence[Mapping[str, Any]],
) -> list[str]:
    """Primer (optional JSON) + proximity trip routes for one edition."""
    if project_root is None:
        return []
    blocks: list[str] = []
    data = load_front_matter(project_root, city_slug)
    if data:
        primer = primer_section_html(data, edition)
        if primer:
            blocks.append(primer)
    slug = city_slug.strip().lower()
    if slug not in CITIES_WITHOUT_TRIP_ROUTES:
        trips = proximity_trip_plans_section_html(
            city_slug,
            edition,
            places,
            project_root=project_root,
        )
        if not trips and data:
            trips = trip_plans_section_html(data, edition, places)
        if trips:
            blocks.append(trips)
    return blocks


def _text_len(place: Mapping[str, Any], edition: str, base: str) -> int:
    if edition == "ru":
        keys = (f"{base}_ru", base)
    else:
        keys = (f"{base}_en", base)
    total = 0
    for key in keys:
        raw = place.get(key)
        if raw is None:
            continue
        total += len(str(raw).strip())
    return total


def place_prominence_score(
    place: Mapping[str, Any],
    edition: str,
) -> int:
    """Rank places for LLM context (higher = more narrative)."""
    slug = str(place.get("slug") or "")
    if is_pdf_filler_slug(slug):
        return -1
    score = 0
    if place.get("image_rel_path"):
        score += 2
    for base in ("description", "history", "significance"):
        if _text_len(place, edition, base) > 80:
            score += 4
        elif _text_len(place, edition, base) > 20:
            score += 2
    facts_key = "facts_ru" if edition == "ru" else "facts"
    facts = place.get(facts_key) or place.get("facts")
    if isinstance(facts, list) and facts:
        score += min(3, len(facts))
    name = (
        str(place.get("name_en") or "")
        or str(place.get("name_ru") or "")
        or str(place.get("name") or "")
    ).strip()
    if is_substantive_text(name):
        score += 1
    return score


def top_places_for_prompt(
    places: Sequence[Mapping[str, Any]],
    edition: str,
    *,
    limit: int = 12,
) -> list[dict[str, Any]]:
    """Curated rows for front-matter generation prompts."""
    ranked = sorted(
        (p for p in places if place_prominence_score(p, edition) >= 0),
        key=lambda p: (
            -place_prominence_score(p, edition),
            str(p.get("slug") or ""),
        ),
    )
    out: list[dict[str, Any]] = []
    for p in ranked[: max(1, limit)]:
        slug = str(p.get("slug") or "")
        title = place_heading_plain(p, edition)
        blurb = ""
        if edition == "ru":
            for key in ("description_ru", "description", "subtitle_ru"):
                raw = str(p.get(key) or "").strip()
                if is_substantive_text(raw):
                    blurb = raw[:220]
                    break
        else:
            for key in ("description_en", "description", "subtitle_en"):
                raw = str(p.get(key) or "").strip()
                if is_substantive_text(raw):
                    blurb = raw[:220]
                    break
        out.append({"slug": slug, "title": title, "blurb": blurb})
    return out
