# -*- coding: utf-8 -*-
"""City title/body font selection for the web editor UI."""

from __future__ import annotations

from dataclasses import dataclass

from scripts.city_guide_typography import typography_triple
from scripts.guide_editor_presets import SMOLENSK_BODY_FONT_FAMILY
from scripts.guide_editor_presets import SMOLENSK_GOOGLE_FONTS_HREF
from scripts.guide_editor_presets import SMOLENSK_TITLE_FONT_FAMILY


@dataclass(frozen=True)
class CityFonts:
    google_fonts_href: str
    title_font_family: str
    body_font_family: str


def fonts_for_city(city_slug: str) -> CityFonts:
    """
    Pick the same title/body fonts as the city guide generators.

    Most Latin-script cities are configured in `scripts/city_guide_typography.py`.
    Smolensk, Moscow, and SPB have dedicated stacks; Moscow matches Smolensk
    Cyrillic-friendly fonts. Other cities use ``city_guide_typography``.
    """
    if city_slug in {"smolensk", "moscow"}:
        return CityFonts(
            google_fonts_href=SMOLENSK_GOOGLE_FONTS_HREF,
            title_font_family=SMOLENSK_TITLE_FONT_FAMILY,
            body_font_family=SMOLENSK_BODY_FONT_FAMILY,
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

