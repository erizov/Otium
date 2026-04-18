# -*- coding: utf-8 -*-
"""Static UI presets for the local guide editor (shared with FastAPI)."""

from __future__ import annotations

from typing import TypedDict

from scripts.city_guide_typography import typography_triple

# Smolensk guide + editor city-default (single source for builders).
SMOLENSK_GOOGLE_FONTS_HREF = (
    "https://fonts.googleapis.com/css2?"
    "family=Cormorant+Garamond:wght@600&family=Ponomar&family=Triodion&"
    "family=Source+Sans+3:wght@400;600&display=swap"
)
SMOLENSK_TITLE_FONT_FAMILY = (
    "'Triodion', 'Ponomar', 'Cormorant Garamond', serif"
)
SMOLENSK_BODY_FONT_FAMILY = "'Source Sans 3', sans-serif"


class ThemeCssVars(TypedDict):
    """CSS custom properties for editor chrome (see city.html :root)."""

    bg_base: str
    flag_a: str
    flag_b: str
    flag_c: str
    accent: str
    accent_2: str


# Dark graphite; flag_* drive soft gradients without country colors.
NEUTRAL_PALETTE: ThemeCssVars = {
    "bg_base": "#0e1218",
    "flag_a": "#3d4d62",
    "flag_b": "#283545",
    "flag_c": "#4a5d78",
    "accent": "#6eb8f0",
    "accent_2": "#8b97a8",
}

# Light surfaces; pair with html[data-palette="paper"] in app.css.
PAPER_PALETTE: ThemeCssVars = {
    "bg_base": "#ece8e0",
    "flag_a": "#d8d0c4",
    "flag_b": "#cbc2b4",
    "flag_c": "#e4dfd6",
    "accent": "#1a4f8c",
    "accent_2": "#5c4a3d",
}


class FontProfileDict(TypedDict, total=False):
    """One selectable font profile (editor only)."""

    id: str
    label: str
    google_fonts_href: str | None
    title_font_family: str
    body_font_family: str


def editorial_font_profile() -> FontProfileDict:
    """Match generic guide typography (_DEFAULT in city_guide_typography)."""
    href, title, body = typography_triple("_unknown_city_slug_")
    return {
        "id": "editorial",
        "label": "Editorial",
        "google_fonts_href": href,
        "title_font_family": title,
        "body_font_family": body,
    }


def system_font_profile() -> FontProfileDict:
    """No extra webfont request."""
    return {
        "id": "system",
        "label": "System",
        "google_fonts_href": None,
        "title_font_family": (
            "ui-serif, Georgia, 'Times New Roman', serif"
        ),
        "body_font_family": (
            "ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, "
            "sans-serif"
        ),
    }


def static_font_profiles() -> list[FontProfileDict]:
    """Font profiles except city_default (filled in the API)."""
    return [editorial_font_profile(), system_font_profile()]
