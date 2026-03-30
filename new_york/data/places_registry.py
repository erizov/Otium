# -*- coding: utf-8 -*-
"""New York City guide registry: flat images/<slug> paths."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict, cast


class NewYorkExtraImage(TypedDict, total=False):
    """Extra photo in flat images/ catalog."""

    image_rel_path: str
    image_source_url: str


class NewYorkPlace(TypedDict, total=False):
    """One guide place card."""

    slug: str
    category: str
    suppress_images_for_pdf: bool
    name_en: str
    subtitle_en: str
    image_rel_path: str
    image_source_url: str
    additional_images: list[NewYorkExtraImage]
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
    base = Path(__file__).parent
    merged: dict[str, dict] = {}
    for path in sorted(base.glob("new_york_place_details*.json")):
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


def _load_places() -> list[NewYorkPlace]:
    path = Path(__file__).with_name("new_york_places.json")
    raw: list[dict] = json.loads(path.read_text(encoding="utf-8"))
    raw = _merge_details(raw)
    return cast(list[NewYorkPlace], raw)


NEW_YORK_PLACES: list[NewYorkPlace] = _load_places()
