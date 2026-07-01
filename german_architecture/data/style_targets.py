# -*- coding: utf-8 -*-
"""Per-style example counts for the architecture guide."""

from __future__ import annotations

from german_architecture.data.style_catalog import STYLE_ORDER


def style_example_target(style_key: str) -> int:
    """Return how many examples a style chapter should list."""
    # Commons-only guides: aim for 4, accept fewer after filtering.
    return 4
