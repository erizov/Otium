# -*- coding: utf-8 -*-
"""21 architectural styles — chronological chapters."""

from __future__ import annotations

from typing import Any

# category key -> (title_ru, title_en, style_intro_ru, style_intro_en)
STYLE_META: dict[str, tuple[str, str, str, str]] = {
    "gallo_roman": (
        "Галло-римское зодчество (I–V вв.)",
        "Gallo-Roman architecture (1st–5th c.)",
        "Театры, термы и мосты римской Галлии.",
        "Theatres, baths and bridges of Roman Gaul.",
    ),
    "romanesque": (
        "Романский стиль (XI–XII вв.)",
        "Romanesque (11th–12th c.)",
        "Паломнические аббатства и массивные апсиды.",
        "Pilgrimage abbeys and massive apses.",
    ),
    "early_gothic": (
        "Раннеготика (XII–XIII вв.)",
        "Early Gothic (12th–13th c.)",
        "Сен-Дени и соборы Иль-де-Франс: стрельчатые арки и витражи.",
        "Saint-Denis and Île-de-France cathedrals: pointed arches and glass.",
    ),
    "rayonnant_flamboyant": (
        "Радиантная и пламенеющая готика (XIV–XV вв.)",
        "Rayonnant and Flamboyant Gothic (14th–15th c.)",
        "Световые стены и пламенеющие линии декора.",
        "Luminous walls and flamboyant tracery.",
    ),
    "french_renaissance": (
        "Французское Возрождение (XVI в.)",
        "French Renaissance (16th c.)",
        "Замки Луары и дворцы Валуа с итальянскими мотивами.",
        "Loire châteaux and Valois palaces with Italian motifs.",
    ),
    "classical_louis_xiii": (
        "Классицизм эпохи Людовика XIII (XVII в., первая половина)",
        "Classical architecture under Louis XIII (early 17th c.)",
        "Сдержанный классицизм и кирпично-каменные фасады.",
        "Restrained classicism and brick-and-stone façades.",
    ),
    "louis_xiv_classicism": (
        "Классицизм Людовика XIV (вторая половина XVII в.)",
        "Louis XIV classicism (late 17th c.)",
        "Версаль и осевые ансамбли абсолютной монархии.",
        "Versailles and axial ensembles of absolute monarchy.",
    ),
    "regency_rococo": (
        "Регентство и рококо (начало XVIII в.)",
        "Régence and Rococo (early 18th c.)",
        "Изящные интерьеры и асимметричный декор.",
        "Elegant interiors and asymmetrical ornament.",
    ),
    "louis_xv_rococo": (
        "Рококо Людовика XV (середина XVIII в.)",
        "Louis XV Rococo (mid-18th c.)",
        "Парижские особняки и павильоны с рокайльным орнаментом.",
        "Parisian hôtels particuliers with rocaille ornament.",
    ),
    "louis_xvi_neoclassical": (
        "Неоклассицизм Людовика XVI (конец XVIII в.)",
        "Louis XVI Neoclassicism (late 18th c.)",
        "Античные мотивы и строгая симметрия перед революцией.",
        "Antique motifs and strict symmetry before the Revolution.",
    ),
    "revolution_empire": (
        "Революция и ампир (конец XVIII — начало XIX вв.)",
        "Revolution and Empire (late 18th — early 19th c.)",
        "Триумфальные арки и монументальность Наполеоновской эпохи.",
        "Triumphal arches and Napoleonic monumentality.",
    ),
    "restoration_july_monarchy": (
        "Реставрация и Июльская монархия (1815–1848)",
        "Restoration and July Monarchy (1815–1848)",
        "Эклектика и новые институциональные здания.",
        "Eclecticism and new institutional buildings.",
    ),
    "second_empire": (
        "Второе имперское зодчество (1852–1870)",
        "Second Empire (1852–1870)",
        "Мансарды, ордер и парадные фасады Наполеона III.",
        "Mansard roofs, orders and ceremonial façades of Napoleon III.",
    ),
    "haussmann": (
        "Османизация Парижа (1853–1870)",
        "Haussmann Paris (1853–1870)",
        "Единые фасады бульваров, парки и инженерная инфраструктура.",
        "Uniform boulevard façades, parks and engineering infrastructure.",
    ),
    "belle_epoque": (
        "Прекрасная эпоха (конец XIX — начало XX вв.)",
        "Belle Époque (late 19th — early 20th c.)",
        "Грандиозные выставки и парадная архитектура Третьей республики.",
        "Grand exhibitions and ceremonial architecture of the Third Republic.",
    ),
    "art_nouveau": (
        "Ар-нуво (1890‑е — 1914)",
        "Art Nouveau (1890s–1914)",
        "Гимар и метро Парижа; растительные линии и железо.",
        "Guimard and the Paris Métro; organic lines and ironwork.",
    ),
    "art_deco_interwar": (
        "Ар-деко и межвоенный период (1920–1930‑е)",
        "Art Deco and interwar (1920s–1930s)",
        "Геометрический декор и роскошь межвоенных выставок.",
        "Geometric décor and interwar exhibition luxury.",
    ),
    "modernism_lecorbusier": (
        "Модернизм и Ле Корбюсье (1920–1960‑е)",
        "Modernism and Le Corbusier (1920s–1960s)",
        "Пилонная архитектура, жилая ячейка и брутальный бетон.",
        "Pilotis, the dwelling unit and béton brut.",
    ),
    "brutalism": (
        "Брутализм (1960–1970‑е)",
        "Brutalism (1960s–1970s)",
        "Массивные общественные здания и жилые комплексы.",
        "Massive public buildings and housing estates.",
    ),
    "grands_projets": (
        "Великие проекты и постмодерн (1980–1990‑е)",
        "Grands Projets and postmodern (1980s–1990s)",
        "Национальные институции и постмодернистские вмешательства.",
        "National institutions and postmodern interventions.",
    ),
    "contemporary": (
        "Современная архитектура (2000‑е — н. в.)",
        "Contemporary architecture (2000s–present)",
        "Стекло, экология и культурные центры XXI века.",
        "Glass, sustainability and 21st-century cultural centres.",
    ),
}

from french_architecture.data.style_examples_seeds import STYLE_EXAMPLES

STYLE_ORDER: tuple[str, ...] = (
    "gallo_roman",
    "romanesque",
    "early_gothic",
    "rayonnant_flamboyant",
    "french_renaissance",
    "classical_louis_xiii",
    "louis_xiv_classicism",
    "regency_rococo",
    "louis_xv_rococo",
    "louis_xvi_neoclassical",
    "revolution_empire",
    "restoration_july_monarchy",
    "second_empire",
    "haussmann",
    "belle_epoque",
    "art_nouveau",
    "art_deco_interwar",
    "modernism_lecorbusier",
    "brutalism",
    "grands_projets",
    "contemporary",
)

if set(STYLE_ORDER) != set(STYLE_META):
    _missing = sorted(set(STYLE_META) - set(STYLE_ORDER))
    _extra = sorted(set(STYLE_ORDER) - set(STYLE_META))
    raise RuntimeError(
        "STYLE_ORDER / STYLE_META mismatch: "
        "missing={!r}, extra={!r}".format(_missing, _extra),
    )
