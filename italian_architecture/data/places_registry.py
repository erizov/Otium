# -*- coding: utf-8 -*-
"""Architecture guide place registry."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict, cast

from scripts.city_guide_registry_common import load_pdf_expand_rows


class CityPlace(TypedDict, total=False):
    slug: str
    category: str
    name_ru: str
    subtitle_en: str
    image_rel_path: str
    image_source_url: str
    additional_images: list[dict[str, str]]
    description: str
    history: str
    significance: str
    facts: list[str]


def _load_places() -> list[CityPlace]:
    path = Path(__file__).with_name("italian_architecture_places.json")
    data_dir = Path(__file__).parent
    raw: list[dict] = json.loads(path.read_text(encoding="utf-8"))
    raw.extend(load_pdf_expand_rows(data_dir, "italian_architecture"))
    return cast(list[CityPlace], raw)


ITALIAN_ARCHITECTURE_PLACES: list[CityPlace] = _load_places()
