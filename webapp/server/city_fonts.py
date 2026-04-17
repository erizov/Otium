# -*- coding: utf-8 -*-
"""City title/body font selection for the web editor UI."""

from __future__ import annotations

from dataclasses import dataclass

from scripts.city_guide_typography import typography_triple


@dataclass(frozen=True)
class CityFonts:
    google_fonts_href: str
    title_font_family: str
    body_font_family: str


def fonts_for_city(city_slug: str) -> CityFonts:
    """
    Pick the same title/body fonts as the city guide generators.

    Most Latin-script cities are configured in `scripts/city_guide_typography.py`.
    Smolensk and SPB have dedicated styles, so we mirror their known stacks.
    """
    if city_slug == "smolensk":
        return CityFonts(
            google_fonts_href=(
                "https://fonts.googleapis.com/css2?"
                "family=Cormorant+Garamond:wght@600&family=Ponomar&family=Triodion&"
                "family=Source+Sans+3:wght@400;600&display=swap"
            ),
            title_font_family=(
                "'Triodion', 'Ponomar', 'Cormorant Garamond', serif"
            ),
            body_font_family="'Source Sans 3', sans-serif",
        )
    if city_slug == "spb":
        return CityFonts(
            google_fonts_href=(
                "https://fonts.googleapis.com/css2?"
                "family=Cormorant+Garamond:wght@600&family=Source+Sans+3:wght@400;600"
                "&display=swap"
            ),
            title_font_family="'Cormorant Garamond', serif",
            body_font_family="'Source Sans 3', sans-serif",
        )
    href, title, body = typography_triple(city_slug)
    return CityFonts(
        google_fonts_href=href,
        title_font_family=title,
        body_font_family=body,
    )

