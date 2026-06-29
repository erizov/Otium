# -*- coding: utf-8 -*-
"""21 architectural styles — chronological chapters."""

from __future__ import annotations

from typing import Any

# category key -> (title_ru, title_en, style_intro_ru, style_intro_en)
STYLE_META: dict[str, tuple[str, str, str, str]] = {
    "roman_hispania": (
        "Римская Испания (I–V вв.)",
        "Roman Hispania (1st–5th c.)",
        "Акведуки, театры и мосты римской Иберии.",
        "Aqueducts, theatres and bridges of Roman Iberia.",
    ),
    "visigothic": (
        "Вестготское зодчество (VI–VIII вв.)",
        "Visigothic architecture (6th–8th c.)",
        "Раннесредневековые церкви на Пиренейском полуострове.",
        "Early medieval churches of the Iberian Peninsula.",
    ),
    "islamic_iberia": (
        "Исламская архитектура Аль-Андалуса (VIII–XV вв.)",
        "Islamic architecture of Al-Andalus (8th–15th c.)",
        "Мечети, дворцы и сады Кордовы и Гранады.",
        "Mosques, palaces and gardens of Córdoba and Granada.",
    ),
    "mudejar": (
        "Мудéjar (XII–XVI вв.)",
        "Mudéjar (12th–16th c.)",
        "Исламские мотивы в христианских зданиях кирпичной кладки.",
        "Islamic motifs in Christian brick buildings.",
    ),
    "romanesque": (
        "Романский стиль (XI–XIII вв.)",
        "Romanesque (11th–13th c.)",
        "Паломнический путь в Сантьяго и каменные церкви.",
        "Camino de Santiago and stone Romanesque churches.",
    ),
    "catalan_gothic": (
        "Каталонская готика (XIII–XV вв.)",
        "Catalan Gothic (13th–15th c.)",
        "Зальные церкви и морской готический Каталонии.",
        "Hall churches and maritime Gothic of Catalonia.",
    ),
    "isabelline_gothic": (
        "Изабеллинская готика (конец XV в.)",
        "Isabelline Gothic (late 15th c.)",
        "Позднеготический декор при дворе Католических королей.",
        "Late Gothic ornament at the court of the Catholic Monarchs.",
    ),
    "manuelin": (
        "Мануэлино (португальская готика, конец XV — начало XVI вв.)",
        "Manueline (Portuguese late Gothic, late 15th — early 16th c.)",
        "Морские мотивы эпохи великих географических открытий.",
        "Maritime motifs of the Age of Discovery.",
    ),
    "plateresque": (
        "Платереско (первая половина XVI в.)",
        "Plateresque (first half of 16th c.)",
        "Фасады, напоминающие чеканку по серебру.",
        "Façades resembling silver-plate ornament.",
    ),
    "herrerian": (
        "Стиль Эрреры и эскориальское зодчество (XVI в.)",
        "Herrerian and El Escorial style (16th c.)",
        "Суровая геометрия монастыря Эскориал.",
        "Severe geometry of the Escorial monastery.",
    ),
    "spanish_baroque": (
        "Испанское барокко (XVII в.)",
        "Spanish Baroque (17th c.)",
        "Соломонические колонны и пышные алтари.",
        "Solomonic columns and lavish altarpieces.",
    ),
    "churrigueresque": (
        "Чурригереско (конец XVII — XVIII вв.)",
        "Churrigueresque (late 17th — 18th c.)",
        "Экстремальный декор испанского позднего барокко.",
        "Extreme ornament of Spanish late Baroque.",
    ),
    "portuguese_baroque": (
        "Португальское барокко (XVII–XVIII вв.)",
        "Portuguese Baroque (17th–18th c.)",
        "Резной мрамор и храмы эпохи золота Бразилии.",
        "Carved marble and churches of the Brazilian gold age.",
    ),
    "neoclassicism": (
        "Неоклассицизм (конец XVIII — начало XIX вв.)",
        "Neoclassicism (late 18th — early 19th c.)",
        "Античные формы в королевских академиях и площадях.",
        "Antique forms in royal academies and squares.",
    ),
    "eclectic_historicism": (
        "Эклектика и историзм (XIX в.)",
        "Eclecticism and historicism (19th c.)",
        "Исторические стили в буржуазных кварталах Мадрида и Лиссабона.",
        "Historicist styles in bourgeois quarters of Madrid and Lisbon.",
    ),
    "catalan_modernisme": (
        "Каталонский модернизм / модернизм (1880‑е — 1910‑е)",
        "Catalan Modernisme (1880s–1910s)",
        "Гауди, кованое железо и керамика Барселоны.",
        "Gaudí, wrought iron and ceramics of Barcelona.",
    ),
    "portuguese_art_nouveau": (
        "Португальский ар-нуво / Arte Nova (начало XX в.)",
        "Portuguese Art Nouveau / Arte Nova (early 20th c.)",
        "Фасады Лиссабона и Порту с растительным орнаментом.",
        "Floral façades of Lisbon and Porto.",
    ),
    "rationalist_interwar": (
        "Рационализм и межвоенный авангард (1920–1930‑е)",
        "Rationalism and interwar avant-garde (1920s–1930s)",
        "Гражданские центры и функционализм Республики.",
        "Civic centres and functionalism of the Republic era.",
    ),
    "franco_estado_novo": (
        "Франко и Estado Novo: монументальное зодчество (1930–1950‑е)",
        "Franco and Estado Novo monumentalism (1930s–1950s)",
        "Диктаторские мемориалы и государственные ансамбли.",
        "Dictatorship memorials and state ensembles.",
    ),
    "postwar_modern": (
        "Послевоенная модернизация (1950–1970‑е)",
        "Post-war modernization (1950s–1970s)",
        "Массовое жилищное строительство и туризм побережья.",
        "Mass housing and coastal tourism development.",
    ),
    "contemporary": (
        "Современная архитектура (1990‑е — н. в.)",
        "Contemporary architecture (1990s–present)",
        "Музеи, инфраструктура и городские регенерации.",
        "Museums, infrastructure and urban regeneration.",
    ),
}

from spanish_architecture.data.style_examples_seeds import STYLE_EXAMPLES

STYLE_ORDER: tuple[str, ...] = (
    "roman_hispania",
    "visigothic",
    "islamic_iberia",
    "mudejar",
    "romanesque",
    "catalan_gothic",
    "isabelline_gothic",
    "manuelin",
    "plateresque",
    "herrerian",
    "spanish_baroque",
    "churrigueresque",
    "portuguese_baroque",
    "neoclassicism",
    "eclectic_historicism",
    "catalan_modernisme",
    "portuguese_art_nouveau",
    "rationalist_interwar",
    "franco_estado_novo",
    "postwar_modern",
    "contemporary",
)

if set(STYLE_ORDER) != set(STYLE_META):
    _missing = sorted(set(STYLE_META) - set(STYLE_ORDER))
    _extra = sorted(set(STYLE_ORDER) - set(STYLE_META))
    raise RuntimeError(
        "STYLE_ORDER / STYLE_META mismatch: "
        "missing={!r}, extra={!r}".format(_missing, _extra),
    )
