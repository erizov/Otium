# -*- coding: utf-8 -*-
"""Per-place image rules for the architecture guide."""

from __future__ import annotations

from typing import Any

SINGLE_IMAGE_SLUGS: frozenset[str] = frozenset({
    "midcentury_modern_saint_joseph_oratory",
})

LARGE_SOLO_IMAGE_SLUGS: frozenset[str] = frozenset({
    "midcentury_modern_saint_joseph_oratory",
})


def large_solo_image_css() -> str:
    """Extra CSS for places that should show one oversized solo photo."""
    rules: list[str] = []
    for slug in sorted(LARGE_SOLO_IMAGE_SLUGS):
        rules.append(
            "#{0} .place-fig--solo img {{ width: 88%; min-width: 88%; "
            "max-height: 58vh; }}".format(slug)
        )
        rules.append(
            "#{0} .place-fig--solo.place-fig--hi-res img {{ "
            "max-height: 58vh; }}".format(slug)
        )
    return "\n".join(rules) + ("\n" if rules else "")


def strip_extra_images(place: dict[str, Any]) -> dict[str, Any]:
    slug = str(place.get("slug") or "")
    if slug not in SINGLE_IMAGE_SLUGS:
        return place
    if not place.get("additional_images"):
        return place
    out = dict(place)
    out.pop("additional_images", None)
    return out
