# -*- coding: utf-8 -*-
"""Image source URL checks against vatican/docs/SOURCES_WHITELIST.md."""

from __future__ import annotations

from pathlib import Path

from scripts.city_guide_standard_whitelist import clear_whitelist_cache
from scripts.city_guide_standard_whitelist import url_is_whitelisted

__all__ = [
    "clear_whitelist_cache",
    "default_whitelist_path",
    "url_is_whitelisted",
]


def default_whitelist_path() -> Path:
    return Path(__file__).resolve().parent / "docs" / "SOURCES_WHITELIST.md"
