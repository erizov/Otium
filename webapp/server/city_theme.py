# -*- coding: utf-8 -*-
"""City theme colors for the web editor UI."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CityTheme:
    bg_base: str
    flag_a: str
    flag_b: str
    flag_c: str | None
    accent: str
    accent_2: str


def _theme_for_flag(
    a: str,
    b: str,
    c: str | None = None,
    *,
    bg_base: str = "#0b0f17",
    accent: str | None = None,
    accent_2: str | None = None,
) -> CityTheme:
    if accent is None:
        accent = a
    if accent_2 is None:
        accent_2 = b
    return CityTheme(
        bg_base=bg_base,
        flag_a=a,
        flag_b=b,
        flag_c=c,
        accent=accent,
        accent_2=accent_2,
    )


def theme_for_city(city_slug: str) -> CityTheme:
    """
    Background accents come from the country flag colors.

    This is intentionally approximate and UI-focused (not a vexillology tool).
    """
    # Russia (Smolensk, Saint Petersburg)
    if city_slug in {"smolensk", "spb"}:
        return _theme_for_flag("#ffffff", "#1c57c8", "#d11f2d", accent="#7cc7ff")
    # Germany
    if city_slug == "berlin":
        return _theme_for_flag("#d42020", "#f2c400", "#111111", accent="#f2c400")
    # France
    if city_slug == "paris":
        return _theme_for_flag("#1c4fb8", "#ffffff", "#d12b2b", accent="#7cc7ff")
    # Italy
    if city_slug in {"rome", "venice", "florence"}:
        return _theme_for_flag("#1f9e55", "#ffffff", "#d12b2b", accent="#7ee6b3")
    # Spain
    if city_slug in {"madrid", "barcelona"}:
        return _theme_for_flag("#c81e2b", "#f4c200", None, accent="#f4c200")
    # Czech Republic
    if city_slug == "prague":
        return _theme_for_flag("#1c4fb8", "#ffffff", "#d12b2b", accent="#7cc7ff")
    # Hungary
    if city_slug == "budapest":
        return _theme_for_flag("#c81e2b", "#ffffff", "#1f9e55", accent="#7ee6b3")
    # Austria
    if city_slug == "vienna":
        return _theme_for_flag("#d12b2b", "#ffffff", None, accent="#ff9aa2")
    # USA
    if city_slug in {"boston", "philadelphia", "new_york"}:
        return _theme_for_flag("#1c4fb8", "#ffffff", "#d12b2b", accent="#7cc7ff")
    # Canada
    if city_slug == "montreal":
        return _theme_for_flag("#d12b2b", "#ffffff", None, accent="#ff9aa2")
    # Israel
    if city_slug == "jerusalem":
        return _theme_for_flag("#1c4fb8", "#ffffff", None, accent="#7cc7ff")

    return _theme_for_flag("#7cc7ff", "#b9ffb7", None, accent="#7cc7ff")

