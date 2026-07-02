# -*- coding: utf-8 -*-
"""Architectural styles — chronological chapters."""

from __future__ import annotations

from typing import Any

STYLE_META: dict[str, tuple[str, str, str, str]] = {
    "roman_britain": (
        "Римская Британия (I–V вв.)",
        "Roman Britain (1st–5th c.)",
        "Бани, стены и амфитеатры римской провинции.",
        "Baths, walls and amphitheatres of the Roman province.",
    ),
    "norman": (
        "Норманнская архитектура (XI–XII вв.)",
        "Norman architecture (11th–12th c.)",
        "Массивные башни и романские соборы после 1066 года.",
        "Massive towers and Romanesque cathedrals after 1066.",
    ),
    "english_gothic": (
        "Английская готика (XIII–XVI вв.)",
        "English Gothic (13th–16th c.)",
        "Перпендикуляр, декорированный и раннеанглийский стили.",
        "Perpendicular, Decorated and Early English styles.",
    ),
    "tudor": (
        "Тюдор (XVI в.)",
        "Tudor (16th c.)",
        "Каркасное заполнение, острые арки и кирпичные особняки.",
        "Half-timbering, pointed arches and brick mansions.",
    ),
    "elizabethan_jacobean": (
        "Елизаветинский и яковианский (конец XVI — начало XVII вв.)",
        "Elizabethan and Jacobean (late 16th – early 17th c.)",
        "Симметричные фасады и классические детали.",
        "Symmetrical façades and classical details.",
    ),
    "palladian_wren": (
        "Палладианство и Врен (XVII в.)",
        "Palladianism and Wren (17th c.)",
        "Классические пропорции после Великого пожара.",
        "Classical proportion after the Great Fire.",
    ),
    "georgian": (
        "Георгианский стиль (1714–1830)",
        "Georgian (1714–1830)",
        "Кирпичные террасы, ордер и городские квадраты.",
        "Brick terraces, orders and urban squares.",
    ),
    "regency": (
        "Регентство (1811–1830)",
        "Regency (1811–1830)",
        "Элегантные фасады и бульварная застройка Брайтона.",
        "Elegant façades and Brighton seafront.",
    ),
    "victorian": (
        "Викторианская эпоха (1837–1901)",
        "Victorian (1837–1901)",
        "Готическое возрождение, железо и промышленные города.",
        "Gothic Revival, iron and industrial cities.",
    ),
    "arts_crafts": (
        "Искусства и ремёсла (1880–1910)",
        "Arts and Crafts (1880–1910)",
        "Реакция на индустриализацию и машинное производство.",
        "Reaction against industrial mass production.",
    ),
    "edwardian": (
        "Эдвардианский период (1901–1914)",
        "Edwardian (1901–1914)",
        "Лёгкая классика и барокко возрождения.",
        "Light classicism and Baroque Revival.",
    ),
    "art_nouveau": (
        "Ар-нуво (1890-е — 1914)",
        "Art Nouveau (1890s–1914)",
        "Изогнутые линии, цветная керамика и декоративные фасады.",
        "Curving lines, glazed ceramics and ornamental façades.",
    ),
    "art_deco": (
        "Ар-деко (1920–1939)",
        "Art Deco (1920–1939)",
        "Геометрия и роскошь межвоенной Британии.",
        "Geometry and interwar luxury in Britain.",
    ),
    "modernism": (
        "Британский модернизм (1920–1970-е)",
        "British Modernism (1920s–1970s)",
        "Модернистское движение и послевоенное жильё.",
        "Modern Movement and post-war housing.",
    ),
    "brutalism": (
        "Брутализм (1960–1980-е)",
        "Brutalism (1960s–80s)",
        "Бетонные жилые и культурные комплексы.",
        "Concrete housing and cultural complexes.",
    ),
    "contemporary": (
        "Современная архитектура (1990-е — наст.)",
        "Contemporary (1990s–present)",
        "Музеи, небоскрёбы и устойчивые кварталы.",
        "Museums, skyscrapers and sustainable quarters.",
    ),
}

from english_architecture.data.style_examples_seeds import STYLE_EXAMPLES

STYLE_ORDER: tuple[str, ...] = (
    "roman_britain",
    "norman",
    "english_gothic",
    "tudor",
    "elizabethan_jacobean",
    "palladian_wren",
    "georgian",
    "regency",
    "victorian",
    "arts_crafts",
    "edwardian",
    "art_nouveau",
    "art_deco",
    "modernism",
    "brutalism",
    "contemporary",
)

if set(STYLE_ORDER) != set(STYLE_META):
    raise RuntimeError('STYLE_ORDER / STYLE_META mismatch')
