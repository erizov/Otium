# -*- coding: utf-8 -*-
"""Реестр объектов СПб: единая схема для всех категорий."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict, cast


class SpbAdditionalImage(TypedDict):
    """Доп. фото объекта (тот же whitelist, что у основного)."""

    image_rel_path: str
    image_source_url: str


class SpbPlace(TypedDict, total=False):
    """Один объект гида."""

    slug: str
    category: str
    name_ru: str
    subtitle_en: str
    image_rel_path: str
    image_source_url: str
    additional_images: list[SpbAdditionalImage]
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


def _merge_additional_images(rows: list[dict]) -> list[dict]:
    """Подмешивает spb_place_additional_images.json (доп. фото к карточкам)."""
    path = Path(__file__).with_name("spb_place_additional_images.json")
    if not path.is_file():
        return rows
    blob = json.loads(path.read_text(encoding="utf-8"))
    for row in rows:
        slug = row.get("slug")
        if not slug or slug not in blob:
            continue
        imgs = blob[slug].get("additional_images")
        if imgs:
            row["additional_images"] = imgs
    return rows


def _load_places() -> list[SpbPlace]:
    path = Path(__file__).with_name("spb_places.json")
    raw: list[dict] = json.loads(path.read_text(encoding="utf-8"))
    for more_name in ("spb_places_more.json", "spb_places_expansion_m2026.json"):
        more_path = Path(__file__).with_name(more_name)
        if more_path.is_file():
            raw.extend(json.loads(more_path.read_text(encoding="utf-8")))
    raw = _merge_details(raw)
    raw = _merge_additional_images(raw)
    return cast(list[SpbPlace], raw)


SPB_PLACES: list[SpbPlace] = _load_places()
