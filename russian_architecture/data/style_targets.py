# -*- coding: utf-8 -*-
"""Per-style example counts for the Russian Architecture guide."""

from __future__ import annotations

from russian_architecture.data.style_catalog import STYLE_ORDER

_TEN_EXAMPLES = frozenset({"empire", "art_nouveau", "art_deco"})
_FIVE_UNTIL = "naryshkin_baroque"


def style_example_target(style_key: str) -> int:
    """Return how many examples a style chapter should list."""
    if style_key == "ancient_rus":
        return 6
    if style_key in _TEN_EXAMPLES:
        return 10
    if STYLE_ORDER.index(style_key) <= STYLE_ORDER.index(_FIVE_UNTIL):
        return 5
    return 7
