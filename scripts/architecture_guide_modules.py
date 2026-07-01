# -*- coding: utf-8 -*-
"""Configuration for national architecture guide modules."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class ArchitectureGuideModule:
    slug: str
    places_json: str
    places_registry_attr: str
    title_ru: str
    title_en: str
    city_roots: tuple[str, ...]
    has_heraldry: bool = False
    single_image_only: bool = False
    image_prefer_width: int = 1280


MODULES: dict[str, ArchitectureGuideModule] = {
    "russian_architecture": ArchitectureGuideModule(
        slug="russian_architecture",
        places_json="russian_architecture_places.json",
        places_registry_attr="RUSSIAN_ARCHITECTURE_PLACES",
        title_ru="Русская архитектура",
        title_en="Russian Architecture",
        city_roots=(
            "moscow",
            "spb",
            "kyiv",
            "novosibirsk",
            "vladimir",
            "pskov",
            "novgorod",
        ),
        has_heraldry=True,
    ),
    "italian_architecture": ArchitectureGuideModule(
        slug="italian_architecture",
        places_json="italian_architecture_places.json",
        places_registry_attr="ITALIAN_ARCHITECTURE_PLACES",
        title_ru="Итальянская архитектура",
        title_en="Italian Architecture",
        city_roots=("rome", "florence", "venice"),
        single_image_only=True,
        image_prefer_width=1920,
    ),
    "french_architecture": ArchitectureGuideModule(
        slug="french_architecture",
        places_json="french_architecture_places.json",
        places_registry_attr="FRENCH_ARCHITECTURE_PLACES",
        title_ru="Французская архитектура",
        title_en="French Architecture",
        city_roots=("paris",),
        single_image_only=True,
    ),
    "spanish_architecture": ArchitectureGuideModule(
        slug="spanish_architecture",
        places_json="spanish_architecture_places.json",
        places_registry_attr="SPANISH_ARCHITECTURE_PLACES",
        title_ru="Иберийская архитектура (Испания и Португалия)",
        title_en="Iberian architecture (Spain and Portugal)",
        city_roots=("madrid", "barcelona", "lisbon"),
        single_image_only=True,
    ),
    "german_architecture": ArchitectureGuideModule(
        slug="german_architecture",
        places_json="german_architecture_places.json",
        places_registry_attr="GERMAN_ARCHITECTURE_PLACES",
        title_ru="Немецкая архитектура",
        title_en="German Architecture",
        city_roots=("berlin", "vienna"),
        single_image_only=True,
    ),
    "english_architecture": ArchitectureGuideModule(
        slug="english_architecture",
        places_json="english_architecture_places.json",
        places_registry_attr="ENGLISH_ARCHITECTURE_PLACES",
        title_ru="Английская архитектура",
        title_en="English Architecture",
        city_roots=("london", "boston", "philadelphia"),
        single_image_only=True,
    ),
    "american_architecture": ArchitectureGuideModule(
        slug="american_architecture",
        places_json="american_architecture_places.json",
        places_registry_attr="AMERICAN_ARCHITECTURE_PLACES",
        title_ru="Американская архитектура (обе Америки)",
        title_en="American Architecture (Both Continents)",
        city_roots=(
            "new_york",
            "boston",
            "philadelphia",
            "los_angeles",
            "san_francisco",
            "montreal",
        ),
        single_image_only=True,
    ),
}


def module_config(slug: str) -> ArchitectureGuideModule:
    if slug not in MODULES:
        known = ", ".join(sorted(MODULES))
        raise KeyError("Unknown architecture module {!r}; known: {}".format(
            slug,
            known,
        ))
    return MODULES[slug]


def import_places_list(slug: str) -> list:
    """Load places registry constant for a module."""
    import importlib

    cfg = module_config(slug)
    reg = importlib.import_module("{}.data.places_registry".format(slug))
    return list(getattr(reg, cfg.places_registry_attr))
