# -*- coding: utf-8 -*-
"""
Historical coats of arms for the guide title strip.

Source article (Ruwiki mirrors ru.wikipedia):
https://ru.ruwiki.ru/wiki/История_герба_России
https://ru.wikipedia.org/wiki/История_герба_России
"""

from __future__ import annotations

from typing import Any

# image rel under russian_architecture/, captions, Commons URLs
HISTORY_HERALDRY: tuple[dict[str, Any], ...] = (
    {
        "image": "images/history_coat_ivan3.png",
        "caption_ru": "Печать Ивана III (Московское княжество)",
        "caption_en": "Seal of Ivan III (Grand Duchy of Moscow)",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/c/c3/"
            "Seal_of_Ivan_3.png",
        ],
    },
    {
        "image": "images/history_coat_ivan4.svg",
        "caption_ru": "Печать Ивана IV, 1539 (Московское княжество)",
        "caption_en": "Seal of Ivan IV, 1539 (Grand Duchy of Moscow)",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/a/a3/"
            "Seal_of_Ivan_4_1539.svg",
        ],
    },
    {
        "image": "images/history_coat_tsardom.jpg",
        "caption_ru": "Герб Русского царства (Титулярник)",
        "caption_en": "Coat of arms of the Tsardom of Russia (Titulary)",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/1/11/"
            "01_Tsarskiy_titulyarnik.jpg",
        ],
    },
    {
        "image": "images/history_coat_empire_1796.jpg",
        "caption_ru": "Герб Российской империи, 1796",
        "caption_en": "Coat of arms of the Russian Empire, 1796",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/5/55/"
            "Russian_COA_1796_a.jpg",
        ],
    },
    {
        "image": "images/history_coat_empire_greater.jpg",
        "caption_ru": "Большой герб Российской империи",
        "caption_en": "Greater coat of arms of the Russian Empire",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/b/b4/"
            "Greater_Coat_of_Arms_of_the_Russian_Empire_1700x1767_pix_"
            "Igor_Barbe_2006.jpg",
        ],
    },
    {
        "image": "images/history_coat_1917.svg",
        "caption_ru": "Эмблема России, 1917",
        "caption_en": "Emblem of Russia, 1917",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/e/ea/"
            "Russian_coa_1917.svg",
        ],
    },
    {
        "image": "images/history_coat_1918_kolchak.jpg",
        "caption_ru": "Герб Российского государства, 1918–1920 (проект)",
        "caption_en": (
            "Coat of arms of the Russian State, 1918–1920 (project)"
        ),
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/2/25/"
            "5_rub_Kolchak_project.jpg",
        ],
    },
    {
        "image": "images/history_coat_rsfsr.svg",
        "caption_ru": "Герб РСФСР (1978–1991)",
        "caption_en": "Coat of arms of the RSFSR (1978–1991)",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/d/dc/"
            "Emblem_of_the_Russian_Soviet_Federative_Socialist_Republic_%28"
            "1978%E2%80%931991%29%2C_Emblem_of_the_Russian_Federation_%28"
            "1991%E2%80%931992%29.svg",
        ],
    },
    {
        "image": "images/history_coat_rf.svg",
        "caption_ru": "Герб Российской Федерации",
        "caption_en": "Coat of arms of the Russian Federation",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/f/f2/"
            "Coat_of_Arms_of_the_Russian_Federation.svg",
        ],
    },
)


def history_coats_for_pdf() -> tuple[tuple[str, str, str], ...]:
    """(image rel, alt_en, alt_ru) for ``_HISTORY_COATS`` in the PDF builder."""
    rows: list[tuple[str, str, str]] = []
    for item in HISTORY_HERALDRY:
        image = str(item.get("image") or "").strip()
        cap_ru = str(item.get("caption_ru") or "").strip()
        cap_en = str(item.get("caption_en") or cap_ru).strip()
        if image and cap_ru:
            rows.append((image, cap_en, cap_ru))
    return tuple(rows)


def history_heraldry_download_pairs() -> tuple[tuple[str, list[str]], ...]:
    """(dest rel, source URLs) for ``download_russian_architecture_heraldry``."""
    pairs: list[tuple[str, list[str]]] = []
    for item in HISTORY_HERALDRY:
        image = str(item.get("image") or "").strip()
        urls = item.get("urls")
        if not image or not isinstance(urls, list):
            continue
        clean = [u.strip() for u in urls if isinstance(u, str) and u.strip()]
        if clean:
            pairs.append((image, clean))
    return tuple(pairs)
