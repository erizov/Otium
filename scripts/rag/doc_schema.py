# -*- coding: utf-8 -*-
"""Normalized document schema for RAG caches."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RagDocument:
    """One normalized source document."""

    doc_id: str
    city_slug: str
    language: str  # 'en' or 'ru'
    source_name: str  # wikipedia / wikidata / wikivoyage / ...
    source_url: str
    license: str
    retrieved_at_utc: str
    title: str
    text: str
    extra: dict[str, Any]


def doc_to_dict(d: RagDocument) -> dict[str, Any]:
    return {
        "doc_id": d.doc_id,
        "city_slug": d.city_slug,
        "language": d.language,
        "source_name": d.source_name,
        "source_url": d.source_url,
        "license": d.license,
        "retrieved_at_utc": d.retrieved_at_utc,
        "title": d.title,
        "text": d.text,
        "extra": d.extra,
    }

