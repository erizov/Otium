# -*- coding: utf-8 -*-
"""Which place categories carry street addresses vs location labels vs hours."""

from __future__ import annotations

from typing import Any

# Fixed building / venue — show postal or street address when known.
ADDRESS_EXPECTED: frozenset[str] = frozenset({
    "buildings",
    "cafes",
    "cemeteries",
    "landmarks",
    "libraries",
    "markets",
    "monasteries",
    "museums",
    "osobnjaki",
    "palaces",
    "places",
    "places_of_worship",
    "railway_stations",
    "theaters",
})

# Open feature or monument — show ``location`` (square, bridge, park gate).
ADDRESS_OPTIONAL: frozenset[str] = frozenset({
    "bridges",
    "metro",
    "parks",
    "sculptures",
    "squares",
    "viewpoints",
})

# Ticketed or timed public access — ``visit_hours`` when sourced officially.
SCHEDULE_EXPECTED: frozenset[str] = frozenset({
    "cafes",
    "libraries",
    "markets",
    "museums",
    "theaters",
})

# No fixed daily hours in the guide (may note service times in prose only).
SCHEDULE_OPTIONAL: frozenset[str] = frozenset({
    "bridges",
    "buildings",
    "cemeteries",
    "landmarks",
    "metro",
    "monasteries",
    "osobnjaki",
    "palaces",
    "parks",
    "places",
    "places_of_worship",
    "railway_stations",
    "sculptures",
    "squares",
    "viewpoints",
})

VISIT_HOURS_KEYS = (
    "visit_hours",
    "visit_hours_ru",
    "visit_hours_en",
    "hours",
    "hours_ru",
    "hours_en",
    "opening_hours",
    "schedule",
    "schedule_ru",
    "schedule_en",
)

_LINE_HINTS = ("линия", "line", "кольцевая", "радиальная")


def place_category(place: dict[str, Any]) -> str:
    return str(place.get("category") or "").strip().lower()


def expects_street_address(category: str) -> bool:
    return category in ADDRESS_EXPECTED


def expects_location_label(category: str) -> bool:
    return category in ADDRESS_OPTIONAL


def expects_visit_hours(category: str) -> bool:
    return category in SCHEDULE_EXPECTED


def _looks_like_metro_line(text: str) -> bool:
    low = str(text or "").strip().lower()
    return bool(low) and any(h in low for h in _LINE_HINTS)


def pick_visit_hours(place: dict[str, Any], edition: str) -> str:
    """Return visit hours for *edition* when a dedicated field is set."""
    if edition == "ru":
        keys = ("visit_hours_ru", "visit_hours", "hours_ru", "hours", "schedule_ru")
    else:
        keys = ("visit_hours_en", "visit_hours", "hours_en", "hours", "schedule_en")
    for key in keys:
        raw = str(place.get(key) or "").strip()
        if raw:
            return raw
    for key in ("opening_hours", "schedule"):
        raw = str(place.get(key) or "").strip()
        if raw:
            return raw
    return ""


def pick_street_address(
    place: dict[str, Any],
    edition: str = "ru",
) -> str:
    """Street or postal address (not a metro line or monument square label)."""
    cat = place_category(place)
    if edition == "en":
        addr = str(
            place.get("address_en") or place.get("address") or "",
        ).strip()
    else:
        addr = str(
            place.get("address") or place.get("address_en") or "",
        ).strip()
    if not addr:
        return ""
    if cat == "metro" and _looks_like_metro_line(addr):
        return ""
    if cat in ADDRESS_OPTIONAL:
        return ""
    return addr


def pick_location_label(place: dict[str, Any]) -> str:
    """
    Human placement: square, park gate, bridge span, metro plaza.

    Uses ``location`` when set; for optional categories falls back to
    legacy ``address`` when it is a place label rather than a street.
    """
    loc = str(place.get("location") or "").strip()
    if loc:
        return loc
    cat = place_category(place)
    addr = str(place.get("address") or "").strip()
    if not addr:
        return ""
    if cat in ADDRESS_OPTIONAL:
        return addr
    if cat == "metro" and _looks_like_metro_line(addr):
        return ""
    return ""


def pick_metro_line(place: dict[str, Any]) -> str:
    line = str(place.get("metro_line") or "").strip()
    if line:
        return line
    addr = str(place.get("address") or "").strip()
    if place_category(place) == "metro" and _looks_like_metro_line(addr):
        return addr
    return str(place.get("subtitle_en") or "").strip()


def meta_labels(edition: str) -> dict[str, str]:
    if edition == "ru":
        return {
            "address": "Адрес:",
            "location": "Место:",
            "metro_line": "Линия:",
            "visit_hours": "Часы работы:",
        }
    return {
        "address": "Address:",
        "location": "Location:",
        "metro_line": "Line:",
        "visit_hours": "Hours:",
    }
