# -*- coding: utf-8 -*-
"""Stock image API toggles (off by default)."""

from __future__ import annotations

import os


def _stock_api_enabled(enable_var: str, skip_var: str) -> bool:
    skip = os.environ.get(skip_var, "").strip().lower()
    if skip in ("1", "true", "yes"):
        return False
    if skip in ("0", "false", "no"):
        return True
    enable = os.environ.get(enable_var, "").strip().lower()
    return enable in ("1", "true", "yes")


def pixabay_image_search_enabled() -> bool:
    """Pixabay: opt in with ``PIXABAY_ENABLE=1``."""
    return _stock_api_enabled("PIXABAY_ENABLE", "PIXABAY_SKIP")


def pexels_image_search_enabled() -> bool:
    """Pexels: opt in with ``PEXELS_ENABLE=1``."""
    return _stock_api_enabled("PEXELS_ENABLE", "PEXELS_SKIP")
