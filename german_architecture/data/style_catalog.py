# -*- coding: utf-8 -*-
"""Architectural styles — chronological chapters."""

from __future__ import annotations

from typing import Any

STYLE_META: dict[str, tuple[str, str, str, str]] = {
    "roman_germania": (
        "Римская Германия (I–IV вв.)",
        "Roman Germania (1st–4th c.)",
        "Амфитеатры, ворота и термы римских провинций Рейна и Дуная.",
        "Amphitheatres, gates and baths of Rhine and Danube provinces.",
    ),
    "romanesque": (
        "Романский стиль (XI–XII вв.)",
        "Romanesque (11th–12th c.)",
        "Массивные западные фасады и круглые арки Рейнской земли.",
        "Massive westworks and round arches of the Rhineland.",
    ),
    "gothic": (
        "Немецкая готика (XIII–XVI вв.)",
        "German Gothic (13th–16th c.)",
        "Зальные церкви, кирпичная северогерманская готика.",
        "Hallenkirchen and brick Baltic Gothic.",
    ),
    "renaissance": (
        "Возрождение и маньеризм (XVI в.)",
        "Renaissance and Mannerism (16th c.)",
        "Дворцы князей-архиепископов и ренессансные замки.",
        "Prince-archbishop palaces and Renaissance castles.",
    ),
    "baroque": (
        "Барокко (XVII–XVIII вв.)",
        "Baroque (17th–18th c.)",
        "Дворцы абсолютизма и церковная динамика Юга и Австрии.",
        "Absolutist palaces and southern/Austrian church drama.",
    ),
    "rococo": (
        "Рококо (XVIII в.)",
        "Rococo (18th c.)",
        "Лёгкие павильоны, пастель и парадные интерьеры.",
        "Light pavilions, pastel and ceremonial interiors.",
    ),
    "neoclassicism": (
        "Неоклассицизм (конец XVIII — начало XIX вв.)",
        "Neoclassicism (late 18th – early 19th c.)",
        "Античные формы эпохи Просвещения и наполеоновской Германии.",
        "Classical forms of Enlightenment and Napoleonic Germany.",
    ),
    "historicism": (
        "Историзм (XIX в.)",
        "Historicism (19th c.)",
        "Эклектика стилей империи и объединённой Германии.",
        "Eclectic styles of empire and unified Germany.",
    ),
    "art_nouveau": (
        "Югендстиль (конец XIX — начало XX вв.)",
        "Jugendstil (late 19th – early 20th c.)",
        "Органические линии и декоративный модерн.",
        "Organic lines and decorative modernity.",
    ),
    "modernism": (
        "Ранний модернизм (1900–1930-е)",
        "Early Modernism (1900s–1930s)",
        "Функционализм и экспрессия Веймарской республики.",
        "Functionalism and Weimar Republic expression.",
    ),
    "bauhaus": (
        "Баухаус (1919–1933)",
        "Bauhaus (1919–1933)",
        "Школа, объединившая искусство, ремесло и индустрию.",
        "School uniting art, craft and industry.",
    ),
    "expressionism": (
        "Экспрессионизм (1910–1930-е)",
        "Expressionism (1910s–1930s)",
        "Кирпичные и бетонные формы эмоциональной геометрии.",
        "Brick and concrete emotional geometry.",
    ),
    "nazi_monumental": (
        "Монументальный стиль 1930–1940-х",
        "Nazi-era monumentalism (1930s–40s)",
        "Парадная классика и техника массовых митингов.",
        "Ceremonial classicism and mass-rally spaces.",
    ),
    "postwar_modern": (
        "Послевоенный модерн (1945–1970-е)",
        "Post-war Modern (1945–1970s)",
        "Восстановление и интернациональный стиль ФРГ и ГДР.",
        "Reconstruction and International Style in FRG and GDR.",
    ),
    "brutalism": (
        "Брутализм (1960–1980-е)",
        "Brutalism (1960s–80s)",
        "Бетонные монолиты послевоенных университетов и культуры.",
        "Concrete monoliths of post-war universities and culture.",
    ),
    "contemporary": (
        "Современная архитектура (1990-е — наст.)",
        "Contemporary (1990s–present)",
        "Музеи, вокзалы и устойчивое городское развитие.",
        "Museums, stations and sustainable urban development.",
    ),
}

from german_architecture.data.style_examples_seeds import STYLE_EXAMPLES

STYLE_ORDER: tuple[str, ...] = (
    "roman_germania",
    "romanesque",
    "gothic",
    "renaissance",
    "baroque",
    "rococo",
    "neoclassicism",
    "historicism",
    "art_nouveau",
    "modernism",
    "bauhaus",
    "expressionism",
    "nazi_monumental",
    "postwar_modern",
    "brutalism",
    "contemporary",
)

if set(STYLE_ORDER) != set(STYLE_META):
    raise RuntimeError('STYLE_ORDER / STYLE_META mismatch')
