# -*- coding: utf-8 -*-
"""Per-place image rules for the architecture guide."""

from __future__ import annotations

from typing import Any

SINGLE_IMAGE_SLUGS: frozenset[str] = frozenset()


def strip_extra_images(place: dict[str, Any]) -> dict[str, Any]:
    slug = str(place.get("slug") or "")
    if slug not in SINGLE_IMAGE_SLUGS:
        return place
    if not place.get("additional_images"):
        return place
    out = dict(place)
    out.pop("additional_images", None)
    return out
