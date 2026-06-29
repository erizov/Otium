# -*- coding: utf-8 -*-
"""Extended style chapter intros (optional)."""

from __future__ import annotations

STYLE_INTRO_PARAS: dict[str, tuple[list[str], list[str]]] = {}


def style_intro_paragraphs(cat: str, edition: str) -> list[str]:
    """Return intro paragraphs for a style chapter, or empty list."""
    block = STYLE_INTRO_PARAS.get(cat)
    if not block:
        return []
    paras = block[0] if edition == "ru" else block[1]
    return list(paras)
