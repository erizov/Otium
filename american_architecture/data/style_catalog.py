# -*- coding: utf-8 -*-
"""Architectural styles — chronological chapters."""

from __future__ import annotations

from typing import Any

STYLE_META: dict[str, tuple[str, str, str, str]] = {
    "colonial_americas": (
        "Колониальная архитектура (XVII–XVIII вв.)",
        "Colonial architecture (17th–18th c.)",
        "Испанские, британские и французские колониальные формы.",
        "Spanish, British and French colonial forms.",
    ),
    "federal": (
        "Федеральный стиль (1780–1830)",
        "Federal style (1780–1830)",
        "Ранний американский неоклассицизм.",
        "Early American Neoclassicism.",
    ),
    "greek_revival": (
        "Греческое возрождение (1820–1860)",
        "Greek Revival (1820–1860)",
        "Храмы демократии с дорическими портиками.",
        "Democracy temples with Doric porticos.",
    ),
    "gothic_revival": (
        "Готическое возрождение (1830–1900)",
        "Gothic Revival (1830–1900)",
        "Соборы и кампусные часовни неоготики.",
        "Neo-Gothic cathedrals and campus chapels.",
    ),
    "victorian_americas": (
        "Викторианская Америка (1860–1900)",
        "Victorian America (1860–1900)",
        "Рядовые дома, вторую империю и лесные особняки.",
        "Row houses, Second Empire and shingle style.",
    ),
    "chicago_school": (
        "Чикагская школа (1880–1910)",
        "Chicago School (1880–1910)",
        "Стальной каркас и коммерческий небоскрёб.",
        "Steel frame and commercial skyscraper.",
    ),
    "beaux_arts": (
        "Бо-ар (1890–1930)",
        "Beaux-Arts (1890–1930)",
        "Парадная классика американских институтов.",
        "Ceremonial classicism of American institutions.",
    ),
    "prairie_style": (
        "Прерийный стиль (1900–1920)",
        "Prairie Style (1900–1920)",
        "Горизонтальные линии и открытые планировки Райта.",
        "Wright's horizontal lines and open plans.",
    ),
    "art_deco_americas": (
        "Ар-деко в Америке (1920–1940)",
        "Art Deco in the Americas (1920–1940)",
        "Небоскрёбы и декоративная геометрия.",
        "Skyscrapers and decorative geometry.",
    ),
    "international_style": (
        "Интернациональный стиль (1920–1960)",
        "International Style (1920–1960)",
        "Стекло, сталь и функциональная сетка.",
        "Glass, steel and functional grid.",
    ),
    "midcentury_modern": (
        "Мидсенчури-модерн (1945–1970)",
        "Mid-century Modern (1945–1970)",
        "Послевоенные дома и корпоративные кампусы.",
        "Post-war houses and corporate campuses.",
    ),
    "brutalism_americas": (
        "Брутализм в Америке (1960–1980)",
        "Brutalism in the Americas (1960–80)",
        "Бетонные университеты и гражданские центры.",
        "Concrete universities and civic centres.",
    ),
    "postmodern": (
        "Постмодерн (1970–2000)",
        "Postmodern (1970–2000)",
        "Ирония, цитаты и декоративный небоскрёб.",
        "Irony, quotation and decorative skyscraper.",
    ),
    "latin_colonial_baroque": (
        "Латиноамериканский колониальный барокко",
        "Latin American colonial Baroque",
        "Церкви и монастыри испанской и португальской Америки.",
        "Churches and monasteries of Spanish and Portuguese America.",
    ),
    "latin_modernism": (
        "Латиноамериканский модернизм",
        "Latin American Modernism",
        "Бетон, пейзаж и тропический модерн XX века.",
        "Concrete, landscape and tropical 20th-century modern.",
    ),
    "contemporary_americas": (
        "Современная архитектура Америк (1990-е — наст.)",
        "Contemporary Americas (1990s–present)",
        "Музеи, башни и устойчивые кварталы обоих континентов.",
        "Museums, towers and sustainable districts on both continents.",
    ),
}

from american_architecture.data.style_examples_seeds import STYLE_EXAMPLES

STYLE_ORDER: tuple[str, ...] = (
    "colonial_americas",
    "federal",
    "greek_revival",
    "gothic_revival",
    "victorian_americas",
    "chicago_school",
    "beaux_arts",
    "prairie_style",
    "art_deco_americas",
    "international_style",
    "midcentury_modern",
    "brutalism_americas",
    "postmodern",
    "latin_colonial_baroque",
    "latin_modernism",
    "contemporary_americas",
)

if set(STYLE_ORDER) != set(STYLE_META):
    raise RuntimeError('STYLE_ORDER / STYLE_META mismatch')
