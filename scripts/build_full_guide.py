# -*- coding: utf-8 -*-
"""
Single script to build the full Moscow guide PDF from parts.

By default does not download images (uses existing guide HTML/PDFs).
Use --download-images to run image download for all guides first, then build.

- Backs up existing full guide (PDF + HTML) before overwriting; keeps up to 3.
- Ensures Playwright/Chromium and pypdf are available (installs if needed).
- Preface includes 6 famous Moscow places and OTIUM contact details.
- References are a separate chapter at the end.

- Moscow_Complete_Guide.html is editable in the browser: edit text, delete images,
  add images (up to 4 per place), then "Export HTML" and save over the file.
  Run with --use-existing-html to regenerate the PDF from the edited HTML.

Usage:
  python scripts/build_full_guide.py              # build from existing parts
  python scripts/build_full_guide.py --download-images  # download missing, then build
  python scripts/build_full_guide.py --use-existing-html  # PDF from edited HTML only
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.guide_loader import GUIDES, load_places

OUTPUT_BASENAME = "Moscow_Complete_Guide"
OUTPUT_DIR = _PROJECT_ROOT / "output"
BACKUP_DIR = OUTPUT_DIR / "backup"
MAX_BACKUPS = 3

# Same chapter config as build_combined_guide
CHAPTER_CONFIG: list[tuple[str, str, str]] = [
    ("monasteries", "Монастыри Москвы",
     "Московские монастыри — древние обители и духовные центры города. "
     "В этой главе: действующие монастыри с историей и архитектурой."),
    ("places_of_worship", "Храмы и места поклонения Москвы",
     "От кремлёвских соборов до районных церквей и храмов других конфессий."),
    ("parks", "Парки Москвы",
     "Зелёные пространства: исторические усадебные парки и современные "
     "общественные пространства Москвы."),
    ("museums", "Музеи Москвы",
     "От национальных музеев до мемориальных и тематических пространств."),
    ("palaces", "Дворцы и усадьбы Москвы",
     "Дворцовые и усадебные ансамбли Москвы и окрестностей."),
    ("buildings", "Знаменитые здания Москвы",
     "От сталинских высоток до конструктивизма и современной архитектуры."),
    ("sculptures", "Скульптуры и памятники Москвы",
     "Монументы и скульптурные ансамбли на улицах и площадях города."),
    ("places", "Места и районы Москвы",
     "Улицы, районы и знаковые места Москвы."),
    ("squares", "Площади Москвы",
     "Исторические и современные площади — узлы городской жизни."),
    ("metro", "Станции Московского метро",
     "Архитектура и оформление станций — «подземные дворцы» Москвы."),
    ("theaters", "Театры Москвы",
     "Исторические сцены и современные театральные площадки."),
    ("viewpoints", "Смотровые площадки Москвы",
     "Точки обзора панорам Москвы."),
    ("bridges", "Мосты Москвы",
     "Мосты через Москву-реку и Яузу."),
    ("markets", "Рынки и гастрономические центры Москвы",
     "Исторические и современные рынки и фуд-холлы."),
    ("libraries", "Библиотеки Москвы",
     "Крупнейшие и знаменитые библиотеки Москвы."),
    ("railway_stations", "Вокзалы Москвы",
     "Главные железнодорожные вокзалы — ворота города."),
    ("cemeteries", "Некрополи и кладбища Москвы",
     "Исторические некрополи и мемориальные кладбища."),
    ("landmarks", "Символы Москвы",
     "Iconic места: от Красной площади до Москва-Сити."),
    ("cafes", "Исторические кафе Москвы",
     "Легендарные кафе и рестораны Москвы."),
]

# 6 famous Moscow places for preface
SIX_FAMOUS_PLACES = [
    ("Красная площадь", "Главная площадь России, объект ЮНЕСКО."),
    ("Московский Кремль", "Резиденция президента, соборы и музеи."),
    ("Большой театр", "Символ русского балета и оперы."),
    ("Третьяковская галерея", "Крупнейшее собрание русской живописи."),
    ("ВДНХ", "Выставка достижений народного хозяйства, парк и павильоны."),
    ("Воробьёвы горы", "Смотровая площадка, МГУ, вид на город."),
]

# Fictitious OTIUM contact details (realistic format)
OTIUM_CONTACT = {
    "address": "Москва, ул. Воздвиженка, 4/7, стр. 1",
    "email": "info@otium-guide.ru",
    "phone": "+7 (495) 123-45-67",
    "phone_alt": "+7 (495) 123-45-68",
    "website": "www.otium-guide.ru",
    "edition": "Редакция путеводителей OTIUM",
}

_COMBINED_CSS = """
  @page { size: A4; margin: 1.25cm; margin-bottom: 1.5cm; }
  *, html, body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .page-footer { display: none; }
  @media print {
    .page-footer { display: block; position: fixed; bottom: 0; left: 0; right: 0;
      text-align: center; font-size: 8pt; color: #6b635b;
      font-family: Inter, sans-serif; padding: 0.25em 0; }
    .page-footer::after { content: " · " counter(page) " / " counter(pages); }
  }
  html { background-color: #faf8f5; }
  html, body { margin: 0; padding: 0; font-family: "Source Serif 4",
    Georgia, "Times New Roman", serif; font-size: 10pt; line-height: 1.45;
    color: #1c1b19; background-color: #faf8f5; }
  body { color: #1c1b19 !important; background-color: #faf8f5 !important; }
  h1 { font-family: "Source Serif 4", Georgia, serif; font-size: 18pt;
       text-align: center; margin: 0 0 0.5em; color: #1c1b19 !important; }
  h2 { font-family: "Source Serif 4", Georgia, serif; color: #1c1b19 !important; }
  h2.monastery-title { font-family: Pochaevsk, Georgia, serif; font-size: 14pt;
    margin: 0.5em 0 0.2em 0.2em; border-bottom: 1px solid #8b7355;
    padding-bottom: 0.15em; color: #2c2a28 !important; }
  h2.chapter-title { font-family: Pochaevsk, Georgia, serif; font-size: 16pt;
    margin: 1.5em 0 0.4em 0; color: #2c2a28 !important;
    page-break-after: avoid; }
  .meta, .block-label { font-family: Inter, sans-serif; font-size: 8pt; }
  .meta { margin: 0.1em 0 0.35em 0.2em; color: #6b635b !important; }
  .block-label { margin: 0.6em 0 0.15em 0.3em; text-transform: uppercase;
    font-weight: 600; color: #6b7b8a !important; }
  .body-text { margin: 0 0 0.25em 0.2em; font-size: 9pt; line-height: 1.4;
    text-align: left; max-width: 42em; color: #1c1b19;
    font-family: "Source Serif 4", Georgia, serif; }
  .story-text { font-style: italic; color: #4a5568; font-size: 9pt;
    margin: 0 0 0.25em 0.2em; line-height: 1.4; }
  ul, li, p { color: #1c1b19; font-family: "Source Serif 4", Georgia, serif; }
  .front-page { min-height: 100vh; display: flex; flex-direction: column;
    justify-content: center; align-items: center; text-align: center;
    padding: 3em 2em; font-family: "Source Serif 4", Georgia, serif;
    background: linear-gradient(165deg, #f8f6f2 0%, #ebe8e2 35%, #e8e4dc 70%,
      #f5f2ec 100%);
    page-break-after: always; box-sizing: border-box; }
  .front-page .fp-inner { max-width: 42em; padding: 3em 2.5em;
    border: 1px solid #d4cfc4; border-radius: 4px;
    box-shadow: 0 4px 24px rgba(44, 42, 40, 0.08),
      0 1px 0 rgba(255, 255, 255, 0.6) inset;
    background: rgba(255, 255, 255, 0.75); }
  .front-page .fp-emblem { width: 4.5em; height: 4.5em; margin: 0 auto 0.6em;
    display: block; }
  .front-page .fp-logo { font-size: 36pt; font-weight: 600; letter-spacing: 0.32em;
    color: #1c1b19 !important; margin: 0 0 0.2em; }
  .front-page .fp-rule { width: 5em; height: 2px; background: linear-gradient(
      90deg, transparent, #8b7355 20%, #8b7355 80%, transparent);
    margin: 0 auto 1em; opacity: 0.85; border: none; }
  .front-page .fp-subtitle { font-size: 10pt; letter-spacing: 0.12em;
    color: #5c5549; margin-bottom: 0.9em; text-transform: uppercase;
    font-weight: 500; }
  .front-page .fp-tagline { font-size: 12.5pt; font-style: italic; color: #6b635b;
    margin-bottom: 0.4em; }
  .front-page .fp-tagline + .fp-rule { margin: 0.4em auto 1.2em; width: 3em; }
  .front-page .fp-desc { font-size: 10pt; color: #2c2a28; max-width: 32em;
    margin: 0 auto 1.6em; line-height: 1.6; }
  .front-page .fp-board { font-size: 9pt; text-align: left; max-width: 38em;
    margin: 0 auto; padding: 1.2em 1.4em;
    background: linear-gradient(180deg, rgba(255,255,255,0.9), rgba(248,246,242,0.8));
    border: 1px solid #e0ddd8; border-radius: 3px;
    color: #2c2a28; font-family: "Source Serif 4", Georgia, serif;
    box-shadow: 0 1px 3px rgba(44, 42, 40, 0.04); }
  .front-page .fp-board h3 { font-size: 9pt; font-weight: 600; margin: 0 0 0.6em;
    text-align: center; letter-spacing: 0.04em; color: #4a5568;
    padding-bottom: 0.4em; border-bottom: 1px solid #e0ddd8; }
  .front-page .fp-board ul { list-style: none; padding: 0; margin: 0; }
  .front-page .fp-board li { margin: 0.25em 0; padding-left: 0;
    white-space: nowrap; }
  .preface-block, .chapter-intro { padding: 2em 1em 1em 1.2em;
    background-color: #faf8f5; page-break-after: always; }
  .preface-block h1 { margin-bottom: 0.5em; }
  .preface-block .subtitle { font-size: 11pt; text-align: center;
    color: #6b635b; font-style: italic; margin-bottom: 1em; }
  .preface-block p, .chapter-intro p { margin: 0.4em 0; font-size: 9.5pt;
    line-height: 1.5; text-align: justify; max-width: 38em;
    margin-left: auto; margin-right: auto; }
  .preface-block .contact-block { margin-top: 1.5em; font-size: 9pt;
    padding: 0.8em 1em; background: #f0ede8; border-radius: 4px;
    max-width: 28em; margin-left: auto; margin-right: auto; }
  .preface-block .contact-block p { margin: 0.25em 0; text-align: left; }
  .preface-block .famous-places { margin: 0.6em 0 0 1.2em; }
  .preface-block .famous-places li { margin: 0.2em 0; }
  .chapter-intro { page-break-after: avoid; padding-bottom: 0.5em;
    border-left: 3px solid #c9c4b8; padding-left: 1.35em; }
  .chapter-intro .place-list { margin: 0.4em 0 0 1.2em; font-size: 9pt;
    columns: 2; column-gap: 2em; list-style: disc; }
  .toc-block { padding: 2em 1.5em; background-color: #faf8f5;
    page-break-after: always; }
  .toc-block h2 { font-family: "Source Serif 4", Georgia, serif; font-size: 14pt;
    margin: 0 0 1em; color: #1c1b19 !important; }
  .toc-block ul { list-style: none; padding: 0; margin: 0; }
  .toc-block li { margin: 0.35em 0; font-size: 10pt; }
  .toc-block a { color: #2c2a28; text-decoration: none; }
  .toc-block a:hover { text-decoration: underline; color: #8b7355; }
  .references-chapter { page-break-before: always; padding: 2.2em 1.8em 2em;
    background-color: #faf8f5; font-family: "Source Serif 4", Georgia, serif;
    font-size: 10pt; line-height: 1.5; color: #1c1b19; }
  .references-chapter h2 { font-family: "Source Serif 4", Georgia, serif;
    font-size: 12pt; font-weight: 600; margin: 0 0 1.25em;
    color: #1c1b19 !important; letter-spacing: 0.02em;
    padding-bottom: 0.4em; border-bottom: 1px solid #c9c4b8; }
  .references-chapter .ref-body { max-width: 38em; }
  .references-chapter .ref-body p { margin: 0 0 0.75em; font-size: 10pt;
    line-height: 1.5; text-align: justify; color: #1c1b19; }
  .references-chapter .ref-body p strong { font-weight: 600; color: #2c2a28; }
  .references-chapter .ref-colophon { margin-top: 3em; padding-top: 1.35em;
    border-top: 1px solid #c9c4b8; font-size: 8.5pt; line-height: 1.5;
    color: #5c5549; text-align: center; max-width: 28em; margin-left: auto;
    margin-right: auto; }
  .references-chapter .ref-colophon-emblem { margin-bottom: 0.6em; }
  .references-chapter .ref-emblem { width: 2.8em; height: 2.8em;
    display: block; margin: 0 auto; }
  .references-chapter .ref-colophon p { margin: 0.35em 0; font-size: inherit;
    line-height: inherit; text-align: center; }
  .references-chapter .ref-colophon .ref-year { font-weight: 500; color: #2c2a28; }
  .monastery { display: block; page-break-before: always; padding: 0.5em 0 0; }
  .monastery:first-of-type { page-break-before: auto; }
  .visual-block { margin: 0.45em 0 0; page-break-after: always; }
  .images-row { display: grid; grid-template-columns: 1fr 1fr; gap: 0.6em;
    margin: 0.5em; max-width: 100%; }
  .monastery-img { width: 100%; height: auto; max-height: 155px;
    object-fit: contain; display: block; margin: 0 auto;
    box-sizing: border-box; }
  .images-caption { font-size: 8pt; color: #6b635b; margin: 0.25em 0.5em 0;
    font-family: Inter, sans-serif; }
  .map-block { margin: 0.5em; }
  .map-caption { font-size: 8pt; color: #6b635b; margin: 0.25em 0 0;
    font-family: Inter, sans-serif; }
  .map-img { max-width: 100%; height: auto; max-height: 115px; }
  @media print {
    html, body { color: #1c1b19 !important; background: #faf8f5 !important; }
    .monastery { page-break-before: always; }
    .monastery:first-of-type { page-break-before: auto; }
  }
  .edit-toolbar { position: fixed; top: 8px; right: 8px; z-index: 9999; }
  .edit-toolbar button { font-family: Inter, sans-serif; font-size: 11px;
    padding: 6px 10px; background: #2c2a28; color: #faf8f5; border: none;
    border-radius: 4px; cursor: pointer; }
  .edit-toolbar button:hover { background: #4a5568; }
  .img-wrap { position: relative; display: block; width: 100%; }
  .img-wrap.img-dragging { opacity: 0.6; }
  .img-wrap.img-drop-target { outline: 2px dashed #8b7355; outline-offset: 2px; }
  .img-del { position: absolute; top: 4px; right: 4px; width: 22px; height: 22px;
    font-size: 16px; line-height: 20px; text-align: center; background: rgba(0,0,0,.6);
    color: #fff; border: none; border-radius: 3px; cursor: pointer; }
  .img-del:hover { background: #c53030; }
  .add-img-btn { grid-column: 1 / -1; font-family: Inter, sans-serif; font-size: 10px;
    padding: 4px 8px; margin: 4px 0 0 4px; background: #e0ddd8; color: #2c2a28;
    border: 1px solid #8b7355; border-radius: 3px; cursor: pointer; }
  .add-img-btn:hover { background: #d0cdc8; }
  .add-img-btn.hidden { display: none; }
  .img-count { font-size: 9pt; color: #6b635b; margin-left: 0.25em;
    font-family: Inter, sans-serif; }
  @media print { .edit-toolbar, .img-del, .add-img-btn, .img-count { display: none !important; } }
"""

# Front page: title, subtitle, tagline, short description
FRONT_PAGE_LOGO = "OTIUM"
FRONT_PAGE_SUBTITLE = "Institute of Narrative Geography"
FRONT_PAGE_TAGLINE = "Otium cum dignitate"
FRONT_PAGE_DESC = (
    "Leisure with dignity — intellectual engagement with place"
)
# Emblem variants (A–E). Set EMBLEM_CHOICE to the key you want.
# Each SVG uses {{class}} for fp-emblem (front) or ref-emblem (last page).
EMBLEM_VARIANTS = {
    "A": (
        '<svg class="{{class}}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"'
        ' role="img"><title>OTIUM — laurel wreath and Kremlin tower</title>'
        '<circle cx="32" cy="32" r="29" fill="none" stroke="#8b7355" stroke-width="1.2"/>'
        '<circle cx="32" cy="32" r="25" fill="none" stroke="#c9c4b8" stroke-width="0.6"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.8" '
        'd="M20 36 Q20 22 32 18 Q44 22 44 36"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.8" d="M20 36 Q32 42 44 36"/>'
        '<path fill="#2c2a28" d="M29 24 h6 v20 h-6 z"/>'
        '<path fill="#2c2a28" d="M27 24 L32 18 L37 24 L37 26 L27 26 z"/>'
        '<circle fill="#8b7355" cx="32" cy="16" r="1.8"/>'
        "</svg>"
    ),
    "B": (
        '<svg class="{{class}}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"'
        ' role="img"><title>OTIUM — Kremlin tower seal</title>'
        '<circle cx="32" cy="32" r="28" fill="none" stroke="#8b7355" stroke-width="1.5"/>'
        '<path fill="#2c2a28" d="M28 20 h8 v24 h-8 z"/>'
        '<path fill="#2c2a28" d="M26 20 L32 14 L38 20 L38 22 L26 22 z"/>'
        '<circle fill="#8b7355" cx="32" cy="12" r="2.5"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.7" '
        'd="M32 8 L32 6 M28 10 L26 8 M36 10 L38 8"/>'
        "</svg>"
    ),
    "C": (
        '<svg class="{{class}}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"'
        ' role="img"><title>OTIUM — laurel wreath (dignity)</title>'
        '<circle cx="32" cy="32" r="28" fill="none" stroke="#8b7355" stroke-width="1.2"/>'
        '<circle cx="32" cy="32" r="24" fill="none" stroke="#c9c4b8" stroke-width="0.5"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.9" '
        'd="M16 32 Q16 20 32 14 Q48 20 48 32 Q32 44 16 32"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.9" d="M16 32 Q32 42 48 32"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.6" '
        'd="M24 28 Q32 24 40 28 M24 36 Q32 40 40 36"/>'
        "</svg>"
    ),
    "D": (
        '<svg class="{{class}}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"'
        ' role="img"><title>OTIUM — letter O and tower</title>'
        '<circle cx="32" cy="32" r="26" fill="none" stroke="#8b7355" stroke-width="1.2"/>'
        '<text x="32" y="38" font-family="Georgia,serif" font-size="22" font-weight="600" '
        'fill="#2c2a28" text-anchor="middle">O</text>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.6" '
        'd="M32 44 L32 48 M28 46 L32 50 L36 46"/>'
        "</svg>"
    ),
    "E": (
        '<svg class="{{class}}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"'
        ' role="img"><title>OTIUM — shield, tower and laurel</title>'
        '<path fill="none" stroke="#8b7355" stroke-width="1.2" '
        'd="M32 6 L52 18 L52 46 Q52 54 32 58 Q12 54 12 46 L12 18 Z"/>'
        '<path fill="#2c2a28" d="M28 24 h8 v18 h-8 z"/>'
        '<path fill="#2c2a28" d="M26 24 L32 18 L38 24 L38 26 L26 26 z"/>'
        '<circle fill="#8b7355" cx="32" cy="16" r="1.5"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.6" '
        'd="M20 38 Q32 34 44 38 M20 42 Q32 46 44 42"/>'
        "</svg>"
    ),
}
EMBLEM_CHOICE = "A"


def _emblem_svg(css_class: str) -> str:
    """Return the chosen emblem SVG with the given CSS class."""
    svg = EMBLEM_VARIANTS.get(EMBLEM_CHOICE, EMBLEM_VARIANTS["A"])
    return svg.replace("{{class}}", css_class)


def _write_emblem_preview(output_dir: Path) -> None:
    """Write output/emblem_variants.html to compare emblem variants A–E."""
    parts = []
    for key in ("A", "B", "C", "D", "E"):
        svg = EMBLEM_VARIANTS[key].replace("{{class}}", "emblem-preview")
        parts.append(
            (
                '<div class="variant">'
                '<span class="label">Variant {}</span>'
                "{}"
                "</div>"
            ).format(key, svg)
        )
    body = "\n".join(parts)
    css = (
        "body { font-family: Georgia, serif; background: #f5f2eb; "
        "color: #2c2a28; padding: 2em; }\n"
        "h1 { font-size: 1.4em; margin-bottom: 1em; }\n"
        ".grid { display: flex; flex-wrap: wrap; gap: 2em; }\n"
        ".variant { text-align: center; }\n"
        ".label { display: block; margin-bottom: 0.5em; font-weight: 600; }\n"
        ".emblem-preview { width: 120px; height: 120px; display: block; "
        "margin: 0 auto; }\n"
    )
    html = (
        "<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'>"
        "<title>OTIUM emblem variants</title><style>{}</style></head>"
        "<body><h1>OTIUM emblem variants — choose one, set EMBLEM_CHOICE "
        "in scripts/build_full_guide.py</h1>"
        "<div class='grid'>{}</div></body></html>"
    ).format(css, body)
    path = output_dir / "emblem_variants.html"
    path.write_text(html, encoding="utf-8")


# Editorial board: literature-inspired names (Russian & English), plausible
EDITORIAL_BOARD = [
    ("Е. В. Облонская", "главный редактор"),
    ("А. П. Чебоевский", "заместитель главного редактора"),
    ("Ф. К. Карамазов", ""),
    ("Д. В. Шапира", ""),
    ("М. И. Мышкина", ""),
    ("Ч. Д. Пиквик", ""),
    ("Дж. О. Марч", ""),
    ("И. А. Бездомнова", ""),
    ("Т. Д. Ларина", ""),
    ("Э. Бовари", ""),
    ("Н. Киевна", ""),
    ("М. Шифман", ""),
    ("Ж. Вальжан", ""),
    ("Э. Дантес", ""),
    ("М. Мерсо", ""),
    ("Р. Шухарт", ""),
    ("Д. Румата", ""),
]

PREFACE_TITLE = "Полный путеводитель по Москве"
PREFACE_SUBTITLE = "OTIUM — маршруты без спешки"

REFERENCES_CHAPTER_TITLE = "Примечания и источники"

REFERENCES_BODY = """
<div class="ref-body">
<p><strong>Структура издания.</strong> Главы соответствуют тематическим
гидам OTIUM. Описания мест основаны на открытых источниках; даты и факты
рекомендуется уточнять перед посещением.</p>
<p><strong>Карты.</strong> Статические карты предоставлены Яндекс.Картами.
Для навигации в городе используйте актуальные картографические сервисы.</p>
<p><strong>Изображения.</strong> Фотографии подобраны из открытых источников
(Wikimedia Commons и др.). Права на изображения принадлежат правообладателям.</p>
<p><strong>Контакты и режим работы.</strong> Адреса и координаты приведены
по состоянию на момент подготовки издания; режим работы учреждений и условия
посещения уточняйте на официальных сайтах.</p>
</div>
<div class="ref-colophon">
<div class="ref-colophon-emblem">{colophon_emblem}</div>
<p>© <span class="ref-year">2025</span> OTIUM — Institute of Narrative Geography</p>
<p>Москва</p>
<p>Вёрстка: OTIUM. Печать: Москва, 2025.</p>
<p>Издание для личного использования. Тираж не для продажи.</p>
</div>
"""

# Chapters per PDF chunk to avoid Chromium string size limit (~536M).
# Use 2; if still failing, set to 1 (one chapter per chunk).
CHUNK_CHAPTERS = 2

# Footer for chunk PDFs: Playwright replaces pageNumber and totalPages.
PDF_FOOTER_TEMPLATE = (
    '<div style="font-size:9px;color:#6b635b;width:100%;text-align:center;'
    'font-family:Inter,sans-serif">'
    '<span class="pageNumber"></span> / <span class="totalPages"></span>'
    '</div>'
)


def _strip_moscow_from_title(chapter_title: str) -> str:
    """Remove Moscow-related words so header does not repeat 'Москва'."""
    s = chapter_title
    for word in ("Москвы", "Москве", "Московского", "Москва", "Moscow"):
        s = re.sub(re.escape(word), "", s, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", s).strip().strip(" ,—–")


def _pdf_header_html(header_text: str) -> str:
    """Build Playwright header template HTML (no date/time)."""
    return (
        '<div style="font-size:9px;color:#6b635b;width:100%;text-align:center;'
        'font-family:Inter,sans-serif">'
        "{}"
        "</div>"
    ).format(_escape(header_text))

# Script for editable HTML: contenteditable, image delete/upload (max 4 per item), export
_EDITABLE_SCRIPT = """
(function(){
  var MAX_IMAGES_PER_ROW = 4;
  function initEditable() {
    var sel = '.preface-block p,.preface-block h1,.preface-block li,.chapter-intro p,' +
      '.chapter-intro h2,.chapter-intro li,.monastery .monastery-title,.monastery .meta,' +
      '.monastery .body-text,.monastery .story-text,.references-chapter p,' +
      '.references-chapter h2,.front-page p,.front-page li,.front-page h3';
    document.querySelectorAll(sel).forEach(function(el){ el.contentEditable = 'true'; });
  }
  function setupImages() {
    document.querySelectorAll('.images-row').forEach(function(row){
      var imgs = row.querySelectorAll('.monastery-img');
      imgs.forEach(function(img){
        if (img.closest('.img-wrap')) return;
        var wrap = document.createElement('span');
        wrap.className = 'img-wrap';
        wrap.draggable = true;
        wrap.title = 'Drag to reorder';
        img.parentNode.insertBefore(wrap, img);
        wrap.appendChild(img);
        var delBtn = document.createElement('button');
        delBtn.className = 'img-del';
        delBtn.type = 'button';
        delBtn.textContent = '×';
        delBtn.title = 'Delete image';
        delBtn.onclick = function(){ wrap.remove(); updateAddBtn(row); };
        wrap.appendChild(delBtn);
        wrap.ondragstart = function(e){ e.dataTransfer.setData('text/plain',''); e.dataTransfer.effectAllowed = 'move'; window._dragSrc = wrap; wrap.classList.add('img-dragging'); };
        wrap.ondragend = function(){ wrap.classList.remove('img-dragging'); };
        wrap.ondragover = function(e){ e.preventDefault(); e.dataTransfer.dropEffect = 'move'; if (e.currentTarget !== window._dragSrc) e.currentTarget.classList.add('img-drop-target'); };
        wrap.ondragleave = function(e){ e.currentTarget.classList.remove('img-drop-target'); };
        wrap.ondrop = function(e){ e.preventDefault(); e.currentTarget.classList.remove('img-drop-target'); var src = window._dragSrc; if (src && src !== e.currentTarget) { row.insertBefore(src, e.currentTarget); updateAddBtn(row); } };
      });
      var addBtn = row.querySelector('.add-img-btn');
      if (!addBtn) {
        addBtn = document.createElement('button');
        addBtn.className = 'add-img-btn';
        addBtn.type = 'button';
        addBtn.appendChild(document.createTextNode('+ Add image '));
        var countSpan = document.createElement('span');
        countSpan.className = 'img-count';
        addBtn.appendChild(countSpan);
        addBtn.onclick = function(){ var inp = document.createElement('input'); inp.type = 'file'; inp.accept = 'image/*'; inp.multiple = true; inp.onchange = function(){ [].slice.call(inp.files).forEach(function(file){ if (row.querySelectorAll('.monastery-img').length >= MAX_IMAGES_PER_ROW) return; var r = new FileReader(); r.onload = function(){ var i = document.createElement('img'); i.className = 'monastery-img'; i.src = r.result; i.alt = ''; var w = document.createElement('span'); w.className = 'img-wrap'; w.draggable = true; w.title = 'Drag to reorder'; var dB = document.createElement('button'); dB.className = 'img-del'; dB.type = 'button'; dB.textContent = '×'; dB.onclick = function(){ w.remove(); updateAddBtn(row); }; w.appendChild(i); w.appendChild(dB); w.ondragstart = function(e){ e.dataTransfer.setData('text/plain',''); e.dataTransfer.effectAllowed = 'move'; window._dragSrc = w; w.classList.add('img-dragging'); }; w.ondragend = function(){ w.classList.remove('img-dragging'); }; w.ondragover = function(e){ e.preventDefault(); e.dataTransfer.dropEffect = 'move'; if (e.currentTarget !== window._dragSrc) e.currentTarget.classList.add('img-drop-target'); }; w.ondragleave = function(e){ e.currentTarget.classList.remove('img-drop-target'); }; w.ondrop = function(e){ e.preventDefault(); e.currentTarget.classList.remove('img-drop-target'); var src = window._dragSrc; if (src && src !== e.currentTarget) { row.insertBefore(src, e.currentTarget); updateAddBtn(row); } }; row.insertBefore(w, addBtn); updateAddBtn(row); }; r.readAsDataURL(file); }); }; inp.click(); };
        row.appendChild(addBtn);
      }
      updateAddBtn(row);
    });
  }
  function updateAddBtn(row) {
    var n = row.querySelectorAll('.monastery-img').length;
    var addBtn = row.querySelector('.add-img-btn');
    var countSpan = addBtn ? addBtn.querySelector('.img-count') : null;
    if (countSpan) { countSpan.textContent = n + ' \u0438\u0437 4'; }
    if (addBtn) { addBtn.classList.toggle('hidden', n >= MAX_IMAGES_PER_ROW); }
  }
  function addExportButton() {
    var bar = document.createElement('div');
    bar.className = 'edit-toolbar';
    var btn = document.createElement('button');
    btn.textContent = 'Export HTML';
    btn.onclick = function() {
      var root = document.documentElement.cloneNode(true);
      root.querySelectorAll('.edit-toolbar').forEach(function(el){ el.remove(); });
      root.querySelectorAll('.img-del, .add-img-btn').forEach(function(el){ el.remove(); });
      root.querySelectorAll('.img-wrap').forEach(function(wrap){
        var img = wrap.querySelector('.monastery-img');
        if (img) { wrap.parentNode.insertBefore(img, wrap); }
        wrap.remove();
      });
      var html = '<!DOCTYPE html>\\n' + root.outerHTML;
      var blob = new Blob([html], { type: 'text/html;charset=utf-8' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'Moscow_Complete_Guide.html';
      a.click();
      URL.revokeObjectURL(a.href);
    };
    bar.appendChild(btn);
    document.body.appendChild(bar);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run);
  else run();
  function run() {
    initEditable();
    setupImages();
    addExportButton();
  }
})();
"""


def _build_front_page_html() -> str:
    """Build front page block: logo, subtitle, tagline, description, editorial board."""
    board_items = []
    for name, role in EDITORIAL_BOARD:
        if role:
            board_items.append(
                "<li>{}, {}</li>".format(_escape(name), _escape(role))
            )
        else:
            board_items.append("<li>{}</li>".format(_escape(name)))
    board_list = "\n    ".join(board_items)
    return (
        '<div class="front-page">'
        '<div class="fp-inner">'
        + _emblem_svg("fp-emblem")
        + '<p class="fp-logo">{}</p>'
        '<div class="fp-rule"></div>'
        '<p class="fp-subtitle">{}</p>'
        '<p class="fp-tagline">{}</p>'
        '<div class="fp-rule"></div>'
        '<p class="fp-desc">{}</p>'
        '<div class="fp-board">'
        "<h3>Редакционная коллегия / Editorial Board</h3>"
        "<ul>\n    {}\n  </ul>"
        "</div></div></div>"
    ).format(
        _escape(FRONT_PAGE_LOGO),
        _escape(FRONT_PAGE_SUBTITLE),
        _escape(FRONT_PAGE_TAGLINE),
        _escape(FRONT_PAGE_DESC),
        board_list,
    )


def _extract_place_sections(html: str) -> list[str]:
    """Extract <section class="monastery">...</section> from guide HTML."""
    pattern = re.compile(
        r'<section\s+class="monastery"[^>]*>.*?</section>',
        re.DOTALL,
    )
    return pattern.findall(html)


def _escape(s: str) -> str:
    """Escape HTML entities."""
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def ensure_deps() -> bool:
    """Ensure playwright and chromium are available; install if needed."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            p.chromium.launch()
        return True
    except Exception:
        pass
    # Try pip install playwright if import failed
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "playwright"],
            cwd=str(_PROJECT_ROOT),
            check=True,
            timeout=60000,
        )
    except (subprocess.CalledProcessError, FileNotFoundError, Exception):
        pass
    print("Installing Chromium for Playwright...")
    try:
        subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            cwd=str(_PROJECT_ROOT),
            check=True,
            timeout=120000,
        )
    except (subprocess.CalledProcessError, FileNotFoundError, Exception) as e:
        print(
            "Playwright/Chromium install failed: {}.".format(e),
            file=sys.stderr,
        )
        return False
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            p.chromium.launch()
        return True
    except Exception as e:
        print("Chromium still unavailable: {}.".format(e), file=sys.stderr)
        return False


def _parse_html_to_blocks(html_path: Path) -> list[str] | None:
    """
    Parse existing Moscow_Complete_Guide.html into body blocks for chunked PDF.
    Returns list of block HTML strings (direct children of body: div/section)
    or None if parsing fails.
    """
    try:
        text = html_path.read_text(encoding="utf-8")
    except Exception:
        return None
    body_start = text.find("<body>")
    body_end = text.find("</body>")
    if body_start == -1 or body_end == -1 or body_end <= body_start:
        return None
    content = text[body_start + len("<body>") : body_end]
    blocks = []
    i = 0
    while i < len(content):
        while i < len(content) and content[i] in " \t\n\r":
            i += 1
        if i >= len(content):
            break
        if content[i] != "<":
            return None
        tag_end = content.find(">", i)
        if tag_end == -1:
            return None
        tag = content[i + 1 : tag_end].split()[0].lower()
        if tag not in ("div", "section"):
            if tag == "script":
                j = content.find("</script>", tag_end + 1)
                if j == -1:
                    return None
                i = j + len("</script>")
                continue
            return None
        open_tag = content[i : tag_end + 1]
        depth = 1
        j = tag_end + 1
        while j < len(content) and depth > 0:
            next_close = content.find("</" + tag + ">", j)
            if next_close == -1:
                return None
            next_open = content.find("<" + tag, j)
            if next_open != -1 and next_open < next_close:
                depth += 1
                j = next_open + 1
            else:
                depth -= 1
                j = next_close + len("</" + tag + ">")
        block = content[i:j]
        blocks.append(block)
        i = j
    return blocks if blocks else None


def rotate_backup_full_guide(output_dir: Path, backup_dir: Path) -> None:
    """Back up Moscow_Complete_Guide.pdf and .html; keep up to MAX_BACKUPS."""
    base = OUTPUT_BASENAME
    for ext in (".pdf", ".html"):
        src = output_dir / (base + ext)
        if not src.is_file():
            continue
        backup_dir.mkdir(parents=True, exist_ok=True)
        oldest = backup_dir / (base + "_{}".format(MAX_BACKUPS) + ext)
        if oldest.exists():
            oldest.unlink()
        for i in range(MAX_BACKUPS - 1, 0, -1):
            prev = backup_dir / (base + "_{}".format(i) + ext)
            next_p = backup_dir / (base + "_{}".format(i + 1) + ext)
            if prev.exists():
                shutil.copy2(prev, next_p)
        dest1 = backup_dir / (base + "_1" + ext)
        shutil.copy2(src, dest1)
        print("Backed up {} -> {}".format(src.name, dest1.name))


def _wrap_html(body_blocks: list[str], editable: bool = True) -> str:
    """Wrap body blocks in full HTML document. If editable=True, add edit script."""
    body = "\n".join(body_blocks)
    if editable:
        body = body + "\n<script>\n" + _EDITABLE_SCRIPT.strip() + "\n</script>"
    font_url = (
        "https://fonts.googleapis.com/css2?family=Cormorant:ital,wght@0,400;0,600"
        "&family=Source+Serif+4:ital,wght@0,400;0,600"
        "&family=Inter:wght@400;500;600&display=swap&subset=latin,cyrillic"
    )
    return """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <title>{title}</title>
  <link href="{font_url}" rel="stylesheet" />
  <style>{css}</style>
</head>
<body>
{body}
<div class="page-footer" aria-hidden="true">— Moscow Complete Guide · OTIUM</div>
</body>
</html>
""".format(
        title=_escape(PREFACE_TITLE),
        font_url=font_url,
        css=_COMBINED_CSS,
        body=body,
    )


def build_combined_parts(output_dir: Path) -> list[str]:
    """
    Build list of body blocks: [preface, ch1_block, ch2_block, ..., refs].
    Each block is one or more divs; used for full HTML and chunked PDF.
    """
    blocks: list[str] = []

    # Preface
    famous_li = "".join(
        "<li><strong>{}</strong> — {}.</li>".format(
            _escape(name), _escape(desc),
        )
        for name, desc in SIX_FAMOUS_PLACES
    )
    contact = OTIUM_CONTACT
    contact_html = (
        '<div class="contact-block">'
        "<p><strong>{}</strong></p>"
        "<p>Адрес: {}</p>"
        "<p>Эл. почта: {}</p>"
        "<p>Тел.: {} (многоканальный), {}</p>"
        "<p>Сайт: {}</p>"
        "</div>"
    ).format(
        _escape(contact["edition"]),
        _escape(contact["address"]),
        _escape(contact["email"]),
        _escape(contact["phone"]),
        _escape(contact["phone_alt"]),
        _escape(contact["website"]),
    )
    preface_body = """
<p>Этот том объединяет тематические путеводители OTIUM по Москве в один
сводный гид. Каждая глава посвящена одной теме: монастыри, храмы, парки,
музеи, дворцы, здания, скульптуры, площади, метро, театры, смотровые
площадки, мосты, рынки, библиотеки, вокзалы, некрополи, символы города
и исторические кафе.</p>
<p>В начале каждой главы — краткое введение и список объектов; далее —
описания с адресами, историей, фотографиями и картами.</p>
<p><strong>Шесть знаковых мест Москвы</strong>, с которых удобно начать
знакомство с городом:</p>
<ul class="famous-places">{}</ul>
<p>OTIUM — практика осмысленного досуга: не «посетить всё», а выбрать
немногое и задержаться. Издание подготовлено для печати в формате A4.</p>
{}
""".format(famous_li, contact_html)
    preface = (
        '<div class="preface-block">'
        "<h1>{}</h1>"
        '<p class="subtitle">{}</p>'
        "{}"
        "</div>"
    ).format(
        _escape(PREFACE_TITLE),
        _escape(PREFACE_SUBTITLE),
        preface_body.strip(),
    )
    blocks.append(_build_front_page_html())
    blocks.append(preface)

    toc_entries: list[tuple[int, str]] = []
    chapter_num = 0
    for guide_key, chapter_title, chapter_desc in CHAPTER_CONFIG:
        if guide_key not in GUIDES:
            continue
        chapter_num += 1
        toc_entries.append((chapter_num, chapter_title))
        try:
            places = load_places(guide_key)
        except Exception:
            places = []
        place_names = [p.get("name") or "?" for p in places]
        html_path = output_dir / "{}_guide.html".format(guide_key)
        if not html_path.is_file():
            blocks.append(
                '<div class="chapter-intro" id="ch-{}">'
                "<h2 class=\"chapter-title\">{}. {}</h2>"
                "<p>{}</p>"
                "<p class=\"block-label\">Места в главе (файл гида отсутствует)"
                "</p></div>".format(
                    chapter_num, chapter_num, _escape(chapter_title),
                    _escape(chapter_desc),
                )
            )
            continue
        html = html_path.read_text(encoding="utf-8")
        sections = _extract_place_sections(html)
        # Unique id per place for anchors (ch-1-p1, ch-1-p2, ...)
        out_sections = []
        for idx, s in enumerate(sections):
            place_id = ' id="ch-{}-p{}"'.format(chapter_num, idx + 1)
            if re.search(r'\sid="monastery-', s):
                s = re.sub(r'\s+id="monastery-\d+"', place_id, s, count=1)
            else:
                s = re.sub(
                    r'<section\s+class="monastery"',
                    '<section class="monastery"' + place_id,
                    s, count=1,
                )
            out_sections.append(s)
        sections = out_sections
        list_items = "".join(
            "<li>{}</li>".format(_escape(n)) for n in place_names
        )
        intro = (
            '<div class="chapter-intro" id="ch-{}">'
            "<h2 class=\"chapter-title\">{}. {}</h2>"
            "<p>{}</p>"
            "<p class=\"block-label\">Объекты в этой главе</p>"
            "<ul class=\"place-list\">{}</ul>"
            "</div>"
        ).format(
            chapter_num,
            chapter_num, _escape(chapter_title), _escape(chapter_desc),
            list_items,
        )
        chapter_block = "\n".join([intro] + sections)
        blocks.append(chapter_block)

    toc_html = (
        '<div class="toc-block">'
        "<h2>Содержание</h2><ul>"
        + "".join(
            '<li><a href="#ch-{}">{}. {}</a></li>'.format(
                n, n, _escape(title),
            )
            for n, title in toc_entries
        )
        + "</ul></div>"
    )
    blocks.insert(2, toc_html)

    refs = (
        '<div class="references-chapter">'
        "<h2>{}</h2>"
        "{}"
        "</div>"
    ).format(
        _escape(REFERENCES_CHAPTER_TITLE),
        REFERENCES_BODY.strip().format(
            colophon_emblem=_emblem_svg("ref-emblem"),
        ),
    )
    blocks.append(refs)
    return blocks


def build_combined_html(output_dir: Path) -> str:
    """Build one HTML: preface (6 places + OTIUM) + chapters + references."""
    return _wrap_html(build_combined_parts(output_dir))


def _build_combined_pdf_chunked(
    output_dir: Path,
    blocks: list[str],
    pdf_path: Path,
    image_wait_timeout_ms: int = 60000,
) -> bool:
    """
    Generate combined PDF by rendering chunks (to avoid Chromium string limit)
    and merging with pypdf.
    """
    from scripts.build_pdf import _pdf_via_playwright
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        print("pypdf required for merging chunk PDFs.", file=sys.stderr)
        return False

    # Chunk: [preface], [ch1..ch4], [ch5..ch8], ..., [refs]
    n = len(blocks)
    if n < 2:
        return False
    preface = [blocks[0]]
    refs = [blocks[-1]]
    middle = blocks[1:-1]
    chunk_list: list[list[str]] = [preface]
    for i in range(0, len(middle), CHUNK_CHAPTERS):
        chunk_list.append(middle[i : i + CHUNK_CHAPTERS])
    chunk_list.append(refs)

    chunk_pdfs: list[Path] = []
    try:
        for idx, chunk_blocks in enumerate(chunk_list):
            print("  PDF chunk {}/{}...".format(idx + 1, len(chunk_list)))
            # No header (and no date) on title page or last page (references).
            if idx == 0 or idx == len(chunk_list) - 1:
                header_template = '<div></div>'
            else:
                if idx >= 2:
                    first_chapter_idx = (idx - 2) * CHUNK_CHAPTERS
                    if first_chapter_idx < len(CHAPTER_CONFIG):
                        short = _strip_moscow_from_title(
                            CHAPTER_CONFIG[first_chapter_idx][1],
                        )
                        header_text = "{} : {}".format(PREFACE_TITLE, short)
                    else:
                        header_text = PREFACE_TITLE
                else:
                    header_text = PREFACE_TITLE
                header_template = _pdf_header_html(header_text)
            chunk_html = _wrap_html(chunk_blocks, editable=False)
            chunk_html_path = output_dir / "{}_chunk_{}.html".format(
                OUTPUT_BASENAME, idx,
            )
            chunk_html_path.write_text(chunk_html, encoding="utf-8")
            chunk_pdf_path = output_dir / "{}_chunk_{}.pdf".format(
                OUTPUT_BASENAME, idx,
            )
            if not _pdf_via_playwright(
                chunk_html_path,
                chunk_pdf_path,
                image_wait_timeout_ms=image_wait_timeout_ms,
                display_header_footer=True,
                footer_template=PDF_FOOTER_TEMPLATE,
                header_template=header_template,
            ):
                return False
            chunk_pdfs.append(chunk_pdf_path)
        writer = PdfWriter()
        for p in chunk_pdfs:
            reader = PdfReader(str(p))
            for page in reader.pages:
                writer.add_page(page)
        writer.add_metadata({
            "/Title": "Полный путеводитель по Москве / Moscow Complete Guide",
            "/Author": "OTIUM — Institute of Narrative Geography",
            "/Subject": "Moscow guide, places, monasteries, museums, parks",
            "/Creator": "build_full_guide.py",
        })
        writer.write(str(pdf_path))
        return True
    finally:
        for p in chunk_pdfs:
            if p.is_file():
                try:
                    p.unlink()
                except OSError:
                    pass
        for idx in range(len(chunk_list)):
            html_p = output_dir / "{}_chunk_{}.html".format(
                OUTPUT_BASENAME, idx,
            )
            if html_p.is_file():
                try:
                    html_p.unlink()
                except OSError:
                    pass


def main() -> int:
    """Build full guide: optional download, backup, parts build, combined PDF."""
    parser = argparse.ArgumentParser(
        description="Build full Moscow guide PDF from parts.",
    )
    parser.add_argument(
        "--download-images",
        action="store_true",
        help="Download missing images for all guides before building.",
    )
    parser.add_argument(
        "--use-existing-html",
        action="store_true",
        help="Do not overwrite HTML; generate PDF from existing "
        "Moscow_Complete_Guide.html. After editing in browser, use "
        "'Export HTML' and save over the file, then run with this flag.",
    )
    args = parser.parse_args()

    output_dir = OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_emblem_preview(output_dir)
    html_path = output_dir / "{}.html".format(OUTPUT_BASENAME)
    pdf_path = output_dir / "{}.pdf".format(OUTPUT_BASENAME)

    if not ensure_deps():
        print(
            "Run: pip install playwright && playwright install chromium",
            file=sys.stderr,
        )
        return 1

    if args.use_existing_html:
        if not html_path.is_file():
            print(
                "Moscow_Complete_Guide.html not found. Run without "
                "--use-existing-html first.",
                file=sys.stderr,
            )
            return 1
        blocks = _parse_html_to_blocks(html_path)
        if not blocks:
            print(
                "Could not parse existing HTML into blocks.",
                file=sys.stderr,
            )
            return 1
        if pdf_path.is_file():
            rotate_backup_full_guide(output_dir, BACKUP_DIR)
        print("--- Generating PDF from existing HTML ---")
        try:
            if _build_combined_pdf_chunked(
                output_dir,
                blocks,
                pdf_path,
                image_wait_timeout_ms=60000,
            ):
                print("Written: {}".format(pdf_path))
            else:
                print("PDF generation failed.", file=sys.stderr)
                return 1
        except Exception as e:
            print("PDF generation failed: {}.".format(e), file=sys.stderr)
            return 1
        return 0

    build_script = _PROJECT_ROOT / "scripts" / "build_pdf.py"
    # Step 1: build all single-guide HTML/PDF (with or without download)
    if args.download_images:
        print("--- Downloading images and building all guides ---")
        cmd = [
            sys.executable,
            str(build_script),
            "--all-guides",
            "--build-with-available",
        ]
    else:
        print("--- Building all guides (no image download) ---")
        cmd = [
            sys.executable,
            str(build_script),
            "--all-guides",
            "--build-only",
            "--build-with-available",
        ]
    ret = subprocess.call(cmd, cwd=str(_PROJECT_ROOT))
    if ret != 0:
        return ret

    # Step 2: backup existing full guide if present
    if pdf_path.is_file():
        rotate_backup_full_guide(output_dir, BACKUP_DIR)

    # Step 3: build combined HTML and PDF (chunked to avoid Chromium size limit)
    print("--- Building combined Moscow guide ---")
    blocks = build_combined_parts(output_dir)
    html_path.write_text(_wrap_html(blocks), encoding="utf-8")
    print("Written: {}".format(html_path))

    try:
        if _build_combined_pdf_chunked(
            output_dir,
            blocks,
            pdf_path,
            image_wait_timeout_ms=60000,
        ):
            print("Written: {}".format(pdf_path))
        else:
            print("PDF generation failed.", file=sys.stderr)
            return 1
    except Exception as e:
        print("PDF generation failed: {}.".format(e), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
