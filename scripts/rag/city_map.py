# -*- coding: utf-8 -*-
"""City slug -> canonical names used for source lookups."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CityNames:
    slug: str
    name_en: str
    name_ru: str | None = None


_OVERRIDES: dict[str, CityNames] = {
    "spb": CityNames(slug="spb", name_en="Saint Petersburg", name_ru="Санкт-Петербург"),
    "smolensk": CityNames(slug="smolensk", name_en="Smolensk", name_ru="Смоленск"),
    "kyiv": CityNames(slug="kyiv", name_en="Kyiv", name_ru="Киев"),
    "lviv": CityNames(slug="lviv", name_en="Lviv", name_ru="Львов"),
    "istanbul": CityNames(slug="istanbul", name_en="Istanbul", name_ru="Стамбул"),
    "new_york": CityNames(slug="new_york", name_en="New York City", name_ru="Нью-Йорк"),
    "los_angeles": CityNames(slug="los_angeles", name_en="Los Angeles"),
    "san_francisco": CityNames(slug="san_francisco", name_en="San Francisco"),
    "vatican": CityNames(slug="vatican", name_en="Vatican City", name_ru="Ватикан"),
    "chernivtsi": CityNames(slug="chernivtsi", name_en="Chernivtsi", name_ru="Черновцы"),
}


def names_for_slug(slug: str) -> CityNames:
    s = slug.strip().lower()
    if s in _OVERRIDES:
        return _OVERRIDES[s]
    base = s.replace("_", " ")
    return CityNames(slug=s, name_en=base.title(), name_ru=None)

