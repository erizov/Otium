# -*- coding: utf-8 -*-
"""Curated place prose overrides."""

from __future__ import annotations

from typing import Any

from spanish_architecture.data.thin_text_supplements import (
    apply_thin_text_supplements,
)

_OVERRIDES: dict[str, tuple[str, str, str, str, str, str]] = {}


def narrative_override_for_slug(slug: str) -> dict[str, str] | None:
    block = _OVERRIDES.get(slug)
    if not block:
        return None
    return {
        "description_ru": block[0],
        "description_en": block[1],
        "history_ru": block[2],
        "history_en": block[3],
        "significance_ru": block[4],
        "significance_en": block[5],
    }


def apply_narrative_overrides(place: dict[str, Any]) -> dict[str, Any]:
    """Return a shallow copy with curated text fields when defined."""
    slug = str(place.get("slug") or "")
    override = narrative_override_for_slug(slug)
    if not override:
        return apply_thin_text_supplements(place)
    merged = dict(place)
    for key, value in override.items():
        if value:
            merged[key] = value
    if override.get("description_ru"):
        merged["description"] = override["description_ru"]
    if override.get("history_ru"):
        merged["history"] = override["history_ru"]
    if override.get("significance_ru"):
        merged["significance"] = override["significance_ru"]
    return apply_thin_text_supplements(merged)


def max_sentences_for_slug(slug: str) -> int | None:
    """Optional per-slug narrative length cap."""
    return None
