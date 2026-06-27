# -*- coding: utf-8 -*-
"""21 architectural styles — chronological chapters."""

from __future__ import annotations

from typing import Any

# category key -> (title_ru, title_en, style_intro_ru, style_intro_en)
STYLE_META: dict[str, tuple[str, str, str, str]] = {
    "etruscan_roman": (
        "Этрусское и древнеримское зодчество (VIII в. до н.э. — V в. н.э.)",
        "Etruscan and Roman architecture (8th c. BCE — 5th c. CE)",
        "Храмы, форумы и арки Италии античности; римский бетон и ордер.",
        "Temples, forums and arches of ancient Italy; Roman concrete and orders.",
    ),
    "early_christian": (
        "Раннехристианское и византийское (IV–VIII вв.)",
        "Early Christian and Byzantine (4th–8th c.)",
        "Базилики и мозаики Равенны; переход от античности к средневековью.",
        "Ravenna basilicas and mosaics; transition from antiquity to Middle Ages.",
    ),
    "romanesque": (
        "Романский стиль (XI–XII вв.)",
        "Romanesque (11th–12th c.)",
        "Массивные стены, арочные проёмы и каменные церкви Севера и Тосканы.",
        "Thick walls, round arches and stone churches of the North and Tuscany.",
    ),
    "norman_sicilian": (
        "Норманно-арабское Сицилии (XII в.)",
        "Norman-Arab architecture of Sicily (12th c.)",
        "Синтез норманнских, арабских и византийских мотивов на Сицилии.",
        "Synthesis of Norman, Arab and Byzantine motifs in Sicily.",
    ),
    "gothic": (
        "Итальянская готика (XIII–XIV вв.)",
        "Italian Gothic (13th–14th c.)",
        "Кирпичные фасады, полихромная мраморная отделка, сдержанные шпили.",
        "Brick façades, polychrome marble and restrained spires.",
    ),
    "early_renaissance": (
        "Раннее Возрождение (XV в.)",
        "Early Renaissance (15th c.)",
        "Флоренция: пропорции, перспектива, античные мотивы в частной архитектуре.",
        "Florence: proportion, perspective and classical motifs in private palaces.",
    ),
    "high_renaissance": (
        "Высокое Возрождение (начало XVI в.)",
        "High Renaissance (early 16th c.)",
        "Рим и Ватикан: гармония объёма, купола и центрические композиции.",
        "Rome and the Vatican: harmonious volumes, domes and central plans.",
    ),
    "mannerism": (
        "Маньеризм (XVI в.)",
        "Mannerism (16th c.)",
        "Игра с пропорцией и пространством после классической нормы Возрождения.",
        "Play with proportion and space after High Renaissance norms.",
    ),
    "palladian_venetian": (
        "Палладианство и венецианское Возрождение (XVI в.)",
        "Palladian and Venetian Renaissance (16th c.)",
        "Виллы Палладио и дворцы каналов Венеции.",
        "Palladio's villas and the palazzi of the Venetian canals.",
    ),
    "baroque": (
        "Итальянское барокко (XVII в.)",
        "Italian Baroque (17th c.)",
        "Рим: динамика фасадов, кривые линии, театральность интерьеров.",
        "Rome: dynamic façades, curves and theatrical interiors.",
    ),
    "sicilian_baroque": (
        "Сицилийское барокко (XVII–XVIII вв.)",
        "Sicilian Baroque (17th–18th c.)",
        "Пышные фасады Ното, Катании и Палермо после землетрясения 1693 года.",
        "Ornate façades of Noto, Catania and Palermo after the 1693 earthquake.",
    ),
    "rococo_late_baroque": (
        "Позднее барокко и рококо (XVIII в.)",
        "Late Baroque and Rococo (18th c.)",
        "Лёгкий декор, позолота и парадные интерьеры Севера Италии.",
        "Light ornament, gilding and ceremonial interiors of northern Italy.",
    ),
    "neoclassicism": (
        "Неоклассицизм (конец XVIII — начало XIX вв.)",
        "Neoclassicism (late 18th — early 19th c.)",
        "Возврат к античным формам в эпоху наполеоновских реформ.",
        "Return to antique forms in the Napoleonic era.",
    ),
    "romantic_eclectic": (
        "Романтизм и эклектика (XIX в.)",
        "Romanticism and Eclecticism (19th c.)",
        "Исторические стили в общественных зданиях объединённой Италии.",
        "Historicist styles in public buildings of unified Italy.",
    ),
    "liberty": (
        "Стили «Либерти» (итальянский модерн, конец XIX — начало XX вв.)",
        "Stile Liberty (Italian Art Nouveau, late 19th — early 20th c.)",
        "Растительный орнамент, железо и стекло в галереях и вокзалах.",
        "Floral ornament, iron and glass in galleries and stations.",
    ),
    "rationalism": (
        "Рационализм и итальянский модернизм (1920–1930‑е)",
        "Rationalism and Italian modernism (1920s–1930s)",
        "Строгая геометрия, бетон и функционализм межвоенной Италии.",
        "Strict geometry, concrete and interwar functionalism.",
    ),
    "fascist_rationalism": (
        "Архитектура эпохи фашизма и рационализм (1930–1940‑е)",
        "Fascist-era and Razionalismo architecture (1930s–1940s)",
        "Монументальные оси и кварталы EUR в Риме.",
        "Monumental axes and the EUR district in Rome.",
    ),
    "postwar_modern": (
        "Послевоенный модернизм (1950–1970‑е)",
        "Post-war modernism (1950s–1970s)",
        "Реконструкция городов и итальянское неореализм в архитектуре.",
        "Urban reconstruction and Italian architectural Neorealism.",
    ),
    "brutalism": (
        "Брутализм (1960–1970‑е)",
        "Brutalism (1960s–1970s)",
        "Выразительный бетон в университетах и жилых комплексах.",
        "Expressive concrete in universities and housing estates.",
    ),
    "postmodern_tendenza": (
        "Постмодернизм и Tendenza (1970–1990‑е)",
        "Postmodernism and Tendenza (1970s–1990s)",
        "Исторические цитаты и критика модернистского функционализма.",
        "Historical quotation and critique of modernist functionalism.",
    ),
    "contemporary": (
        "Современная архитектура (2000‑е — н. в.)",
        "Contemporary architecture (2000s–present)",
        "Музеи, выставочные центры и городские вмешательства XXI века.",
        "Museums, cultural centres and urban interventions of the 21st century.",
    ),
}

# Curated seed examples — filled in a later implementation phase.
from italian_architecture.data.style_examples_seeds import STYLE_EXAMPLES

STYLE_ORDER: tuple[str, ...] = (
    "etruscan_roman",
    "early_christian",
    "romanesque",
    "norman_sicilian",
    "gothic",
    "early_renaissance",
    "high_renaissance",
    "mannerism",
    "palladian_venetian",
    "baroque",
    "sicilian_baroque",
    "rococo_late_baroque",
    "neoclassicism",
    "romantic_eclectic",
    "liberty",
    "rationalism",
    "fascist_rationalism",
    "postwar_modern",
    "brutalism",
    "postmodern_tendenza",
    "contemporary",
)

if set(STYLE_ORDER) != set(STYLE_META):
    _missing = sorted(set(STYLE_META) - set(STYLE_ORDER))
    _extra = sorted(set(STYLE_ORDER) - set(STYLE_META))
    raise RuntimeError(
        "STYLE_ORDER / STYLE_META mismatch: "
        "missing={!r}, extra={!r}".format(_missing, _extra),
    )
