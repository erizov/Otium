# -*- coding: utf-8 -*-
"""Backward-compatible re-export of shared city-guide image optimizer."""

from __future__ import annotations

from scripts.city_guide_image_optimize import CITY_GUIDE_IMAGE_MAX_BYTES
from scripts.city_guide_image_optimize import optimize_raster_image_if_large

SMOLENSK_IMAGE_OPTIMIZE_THRESHOLD_BYTES = CITY_GUIDE_IMAGE_MAX_BYTES

__all__ = [
    "SMOLENSK_IMAGE_OPTIMIZE_THRESHOLD_BYTES",
    "optimize_raster_image_if_large",
]
