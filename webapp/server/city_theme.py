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
    if city_slug in {"smolensk", "spb", "moscow"}:
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
    # Vatican City
    if city_slug == "vatican":
        return _theme_for_flag("#fecd00", "#ffffff", "#fecd00", accent="#c9a000")
    # United Kingdom
    if city_slug == "london":
        return _theme_for_flag("#012169", "#ffffff", "#c8102e", accent="#7cc7ff")
    # Netherlands
    if city_slug == "amsterdam":
        return _theme_for_flag("#ae1c28", "#ffffff", "#21468b", accent="#7cc7ff")
    # Türkiye
    if city_slug == "istanbul":
        return _theme_for_flag("#e30a17", "#ffffff", None, accent="#ff9aa2")
    # Japan
    if city_slug == "tokyo":
        return _theme_for_flag("#ffffff", "#bc002d", None, accent="#ff9aa2")
    # UAE
    if city_slug == "dubai":
        return _theme_for_flag("#00732f", "#ffffff", "#000000", accent="#f4c200")
    # Greece
    if city_slug == "athens":
        return _theme_for_flag("#0d5eaf", "#ffffff", None, accent="#7cc7ff")
    # Portugal
    if city_slug == "lisbon":
        return _theme_for_flag("#006600", "#ff0000", None, accent="#7ee6b3")
    # Singapore
    if city_slug == "singapore":
        return _theme_for_flag("#ef3340", "#ffffff", None, accent="#ff9aa2")
    # Thailand
    if city_slug == "bangkok":
        return _theme_for_flag("#ed1c24", "#ffffff", "#241d4f", accent="#7cc7ff")
    # Ireland
    if city_slug == "dublin":
        return _theme_for_flag("#169b62", "#ffffff", "#ff883e", accent="#7ee6b3")
    # Denmark
    if city_slug == "copenhagen":
        return _theme_for_flag("#c8102e", "#ffffff", None, accent="#7cc7ff")
    # USA (extra cities)
    if city_slug in {"los_angeles", "san_francisco"}:
        return _theme_for_flag("#1c4fb8", "#ffffff", "#d12b2b", accent="#7cc7ff")

    return _theme_for_flag("#7cc7ff", "#b9ffb7", None, accent="#7cc7ff")

