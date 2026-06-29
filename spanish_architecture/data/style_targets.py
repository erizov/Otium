# -*- coding: utf-8 -*-
"""Per-style example counts for the architecture guide."""

from __future__ import annotations

from spanish_architecture.data.style_catalog import STYLE_ORDER

_TEN_EXAMPLES = frozenset({"catalan_modernisme", "contemporary", "islamic_iberia", "manuelin", "portuguese_baroque"})
_FIVE_UNTIL = "romanesque"


def style_example_target(style_key: str) -> int:
    """Return how many examples a style chapter should list."""
    if style_key in _TEN_EXAMPLES:
        return 10
    if STYLE_ORDER.index(style_key) <= STYLE_ORDER.index(_FIVE_UNTIL):
        return 5
    return 7
