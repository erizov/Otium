# -*- coding: utf-8 -*-
"""Format RAG retrieval snippets for LLM draft prompts."""

from __future__ import annotations

from pathlib import Path

_MIN_SCORE = 0.12


def rag_context_for_place(
    project_root: Path,
    *,
    city_slug: str,
    place: dict,
    lang: str = "en",
    k: int = 5,
) -> str:
    """
    Return a plain-text block of retrieved chunks for the web editor draft.

    Empty string when the index is missing or nothing scores above threshold.
    """
    try:
        from scripts.rag.export_place_fields import _filter_hits_for_title
        from scripts.rag.export_place_fields import _place_title
        from scripts.rag.export_place_fields import _should_skip_chunk
        from scripts.rag.query import retrieve
        from scripts.rag.city_map import names_for_slug
    except Exception:
        return ""

    title = _place_title(place, lang)
    if not title:
        return ""
    names = names_for_slug(city_slug)
    city_hint = names.name_ru if lang == "ru" else names.name_en
    q = "{} {}".format(title, city_hint)
    hits = retrieve(
        project_root,
        query=q,
        city_slug=city_slug,
        language=lang,
        place=title,
        k=k,
    )
    hits = _filter_hits_for_title(hits, title=title)
    parts: list[str] = []
    for h in hits:
        if h.score < _MIN_SCORE:
            continue
        if _should_skip_chunk(h.chunk, title=title):
            continue
        text = str(h.chunk.get("text") or "").strip()
        if not text:
            continue
        parts.append(text[:600])
        if len(parts) >= 3:
            break
    if not parts:
        return ""
    return "Retrieved reference excerpts (verify before use):\n\n" + "\n\n---\n\n".join(
        parts,
    )
