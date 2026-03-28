# -*- coding: utf-8 -*-
"""Реестр объектов СПб: единая схема для всех категорий."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict, cast


class SpbPlace(TypedDict, total=False):
    """Один объект гида."""

    slug: str
    category: str
    name_ru: str
    subtitle_en: str
    image_rel_path: str
    image_source_url: str
    license_note: str
    attribution: str
    address: str
    year_built: str
    architecture_style: str
    description: str
    history: str
    significance: str
    facts: list[str]
    stories: list[str]


def _load_detail_slugs() -> dict[str, dict]:
    """Объединяет spb_place_details*.json (по алфавиту: база, затем _more)."""
    base = Path(__file__).parent
    merged: dict[str, dict] = {}
    for path in sorted(base.glob("spb_place_details*.json")):
        blob = json.loads(path.read_text(encoding="utf-8"))
        merged.update(blob)
    return merged


def _merge_details(rows: list[dict]) -> list[dict]:
    extra = _load_detail_slugs()
    if not extra:
        return rows
    for row in rows:
        block = extra.get(row.get("slug"))
        if not block:
            continue
        for key, val in block.items():
            if val in (None, "", [], {}):
                continue
            row[key] = val
    return rows


def _load_places() -> list[SpbPlace]:
    path = Path(__file__).with_name("spb_places.json")
    raw: list[dict] = json.loads(path.read_text(encoding="utf-8"))
    raw = _merge_details(raw)
    return cast(list[SpbPlace], raw)


SPB_PLACES: list[SpbPlace] = _load_places()
