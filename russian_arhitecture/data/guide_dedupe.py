# -*- coding: utf-8 -*-
"""Cross-chapter deduplication for architecture guide places."""

from __future__ import annotations

import re
from typing import Any


def normalize_ru_title(name: str) -> str:
    """Lowercase title with collapsed whitespace for dedup keys."""
    return re.sub(r"\s+", " ", name.strip().lower())


def dedupe_places_by_ru_title(
    places: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Keep the first place for each ``name_ru`` (guide chapter order)."""
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for place in places:
        key = normalize_ru_title(str(place.get("name_ru") or ""))
        if key and key in seen:
            continue
        if key:
            seen.add(key)
        out.append(place)
    return out
