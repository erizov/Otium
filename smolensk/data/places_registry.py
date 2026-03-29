# -*- coding: utf-8 -*-
"""Реестр объектов Смоленска: единая схема, плоские пути images/<slug>.jpg."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict, cast


class SmolenskExtraImage(TypedDict, total=False):
    """Дополнительное фото (тот же плоский каталог images/)."""

    image_rel_path: str
    image_source_url: str


class SmolenskPlace(TypedDict, total=False):
    """Один объект гида."""

    slug: str
    category: str
    suppress_images_for_pdf: bool
    name_ru: str
    subtitle_en: str
    image_rel_path: str
    image_source_url: str
    additional_images: list[SmolenskExtraImage]
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
    """Объединяет smolensk_place_details*.json по алфавиту."""
    base = Path(__file__).parent
    merged: dict[str, dict] = {}
    for path in sorted(base.glob("smolensk_place_details*.json")):
        blob = json.loads(path.read_text(encoding="utf-8"))
        merged.update(blob)
    return merged


def _merge_details(rows: list[dict]) -> list[dict]:
    extra = _load_detail_slugs()
    if not extra:
        return rows
    skip_merge = frozenset({"additional_images"})
    for row in rows:
        block = extra.get(row.get("slug"))
        if not block:
            continue
        for key, val in block.items():
            if key in skip_merge:
                continue
            if val in (None, "", [], {}):
                continue
            row[key] = val
    return rows


def _load_places() -> list[SmolenskPlace]:
    path = Path(__file__).with_name("smolensk_places.json")
    raw: list[dict] = json.loads(path.read_text(encoding="utf-8"))
    raw = _merge_details(raw)
    return cast(list[SmolenskPlace], raw)


SMOLENSK_PLACES: list[SmolenskPlace] = _load_places()
