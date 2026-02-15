# -*- coding: utf-8 -*-
"""
Build a single combined PDF guide for Moscow from existing guide HTML/PDFs.

Output: Moscow_Complete_Guide.pdf (and .html) — preface, chapter-by-chapter
content with unique intros (Moscow + topic description + place list), then
references. No duplicate intros; each chapter intro is specific to that theme.

Usage:
  python scripts/build_combined_guide.py

Requires: existing output/<guide>_guide.html for each guide (build guides first).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.guide_loader import GUIDES, load_places

OUTPUT_BASENAME = "Moscow_Complete_Guide"
OUTPUT_DIR = _PROJECT_ROOT / "output"

# Chapter order and unique Moscow-themed intro (title, description).
# Description is specific to Moscow and the chapter topic; not repeated.
CHAPTER_CONFIG: list[tuple[str, str, str]] = [
    ("monasteries", "Монастыри Москвы",
     "Московские монастыри — древние обители и духовные центры города. "
     "В этой главе: действующие монастыри с историей, архитектурой и ролью "
     "в жизни столицы."),
    ("places_of_worship", "Храмы и места поклонения Москвы",
     "От кремлёвских соборов до районных церквей и храмов других конфессий. "
     "Архитектура, история и современная жизнь московских мест поклонения."),
    ("parks", "Парки Москвы",
     "Зелёные пространства города: исторические усадебные парки, "
     "ландшафтные ансамбли и современные общественные пространства Москвы."),
    ("museums", "Музеи Москвы",
     "Коллекции и здания: от главных национальных музеев до мемориальных "
     "и тематических пространств Москвы."),
    ("palaces", "Дворцы и усадьбы Москвы",
     "Дворцовые и усадебные ансамбли Москвы и окрестностей — архитектура "
     "и история."),
    ("buildings", "Знаменитые здания Москвы",
     "Узнаваемые дома и комплексы: от сталинских высоток до конструктивизма "
     "и современной архитектуры Москвы."),
    ("sculptures", "Скульптуры и памятники Москвы",
     "Монументы, памятники и скульптурные ансамбли на улицах и площадях "
     "города."),
    ("places", "Места и районы Москвы",
     "Улицы, районы и знаковые места Москвы — от центра до окраин."),
    ("squares", "Площади Москвы",
     "Исторические и современные площади Москвы — узлы городской жизни "
     "и архитектурные ансамбли."),
    ("metro", "Станции Московского метро",
     "Архитектура и оформление станций метрополитена — «подземные дворцы» "
     "Москвы."),
    ("theaters", "Театры Москвы",
     "Исторические сцены и современные театральные площадки Москвы."),
    ("viewpoints", "Смотровые площадки Москвы",
     "Точки обзора панорам Москвы — высотки, холмы и набережные."),
    ("bridges", "Мосты Москвы",
     "Мосты через Москву-реку и Яузу — инженерия и виды города."),
    ("markets", "Рынки и гастрономические центры Москвы",
     "Исторические и современные рынки, фуд-холлы и гастрономические "
     "пространства Москвы."),
    ("libraries", "Библиотеки Москвы",
     "Крупнейшие и знаменитые библиотеки Москвы — здания и собрания."),
    ("railway_stations", "Вокзалы Москвы",
     "Главные железнодорожные вокзалы Москвы — архитектура и ворота города."),
    ("cemeteries", "Некрополи и кладбища Москвы",
     "Исторические некрополи и мемориальные кладбища Москвы."),
    ("landmarks", "Символы Москвы",
     "Iconic места и символы города: от Красной площади до Москва-Сити."),
    ("cafes", "Исторические кафе Москвы",
     "Легендарные кафе и рестораны Москвы — история и атмосфера."),
]

# Shared print CSS (aligned with build_pdf.py)
_COMBINED_CSS = """
  @page { size: A4; margin: 2cm 1.5cm 1.5cm 1.8cm; }
  *, html, body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  html { background-color: #faf8f5; }
  html, body { margin: 0; padding: 0; font-family: "Source Serif 4",
    Georgia, "Times New Roman", serif; font-size: 10pt; line-height: 1.45;
    color: #1c1b19; background-color: #faf8f5; }
  body { color: #1c1b19 !important; background-color: #faf8f5 !important; }
  h1 { font-family: "Source Serif 4", Georgia, serif; font-size: 18pt;
       text-align: center; margin: 0 0 0.5em; color: #1c1b19 !important; }
  h2 { font-family: "Source Serif 4", Georgia, serif; color: #1c1b19 !important; }
  h2.monastery-title { font-family: Pochaevsk, Georgia, serif; font-size: 17pt;
    margin: 1.2em 0 0.4em 0.3em; border-bottom: 1px solid #8b7355;
    padding-bottom: 0.25em; color: #2c2a28 !important; }
  h2.chapter-title { font-family: Pochaevsk, Georgia, serif; font-size: 16pt;
    margin: 1.5em 0 0.4em 0; color: #2c2a28 !important;
    page-break-after: avoid; }
  .meta, .block-label { font-family: Inter, sans-serif; font-size: 8.5pt;
    letter-spacing: 0.02em; }
  .meta { margin: 0.2em 0 0.6em 0.3em; color: #6b635b !important; }
  .block-label { margin: 0.6em 0 0.15em 0.3em; text-transform: uppercase;
    font-weight: 600; color: #6b7b8a !important; }
  .body-text { margin: 0 0 0.4em 0.3em; text-align: left; max-width: 42em;
    color: #1c1b19; font-family: "Source Serif 4", Georgia, serif; }
  .story-text { font-style: italic; color: #4a5568; }
  ul, li, p { color: #1c1b19; font-family: "Source Serif 4", Georgia, serif; }
  .preface-block, .chapter-intro, .references-block {
    padding: 2em 1em 1em 1.2em; background-color: #faf8f5;
    page-break-after: always; }
  .preface-block h1 { margin-bottom: 0.5em; }
  .preface-block .subtitle { font-size: 11pt; text-align: center;
    color: #6b635b; font-style: italic; margin-bottom: 1.2em; }
  .preface-block p, .chapter-intro p, .references-block p {
    margin: 0.4em 0; font-size: 9.5pt; line-height: 1.5; text-align: justify;
    max-width: 38em; margin-left: auto; margin-right: auto; }
  .chapter-intro { page-break-after: avoid; padding-bottom: 0.5em; }
  .chapter-intro .place-list { margin: 0.4em 0 0 1.2em; font-size: 9pt;
    columns: 2; column-gap: 2em; list-style: disc; }
  .monastery { display: block; page-break-before: always; padding: 1.5em 0 0; }
  .monastery:first-of-type { page-break-before: auto; }
  .visual-block { margin: 0.8em 0 0; page-break-after: always; }
  .images-row { display: flex; gap: 10px; margin: 1em; flex-wrap: wrap; }
  .monastery-img { flex: 1 1 200px; max-width: 100%; height: 150px;
    object-fit: cover; }
  .map-block { margin: 1em; }
  .map-img { max-width: 100%; height: auto; max-height: 160px;
    border: 1px solid #e0ddd8; }
  .references-block h2 { margin-bottom: 0.6em; }
  .references-block ul { margin-left: 1.2em; }
  @media print {
    html, body { color: #1c1b19 !important; background: #faf8f5 !important; }
    .monastery { page-break-before: always; }
    .monastery:first-of-type { page-break-before: auto; }
  }
"""

PREFACE_TITLE = "Полный путеводитель по Москве"
PREFACE_SUBTITLE = "OTIUM — маршруты без спешки"

PREFACE_BODY = """
<p>Этот том объединяет тематические путеводители OTIUM по Москве в один
сводный гид. Каждая глава посвящена одной теме: монастыри, храмы, парки,
музеи, дворцы, здания, скульптуры, площади, метро, театры, смотровые
площадки, мосты, рынки, библиотеки, вокзалы, некрополи, символы города
и исторические кафе.</p>
<p>В начале каждой главы — краткое введение о месте темы в жизни Москвы
и список объектов. Далее следуют описания мест с адресами, историей,
фотографиями и картами.</p>
<p>OTIUM — практика осмысленного досуга: не «посетить всё», а выбрать
немногое и задержаться. Путеводитель можно использовать по главам или
как единый справочник по городу.</p>
<p>Издание подготовлено для печати в формате A4. Карты и изображения
включены по возможности; для актуальных маршрутов используйте карты
и транспортные приложения.</p>
"""

REFERENCES_BODY = """
<p><strong>Структура издания.</strong> Главы соответствуют тематическим
гидам OTIUM. Описания мест основаны на открытых источниках; даты и факты
рекомендуется уточнять перед посещением.</p>
<p><strong>Карты.</strong> Статические карты в путеводителе предоставлены
Яндекс.Картами. Для навигации в городе используйте актуальные картографические
сервисы.</p>
<p><strong>Изображения.</strong> Фотографии подобраны из открытых и
свободных источников (Wikimedia Commons, открытые API и др.) по названию
места и городу. Права на изображения принадлежат их авторам.</p>
<p><strong>Контакты и режим работы.</strong> Адреса и координаты приведены
по состоянию на момент подготовки издания; режим работы учреждений и
входные билеты уточняйте на официальных сайтах.</p>
"""


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


def build_combined_html(output_dir: Path) -> str:
    """Build one HTML document: preface + chapters (intro + places) + refs."""
    parts: list[str] = []

    preface = (
        '<div class="preface-block">'
        "<h1>{}</h1>"
        '<p class="subtitle">{}</p>'
        "{}</div>"
    ).format(
        _escape(PREFACE_TITLE),
        _escape(PREFACE_SUBTITLE),
        PREFACE_BODY.strip(),
    )
    parts.append(preface)

    chapter_num = 0
    for guide_key, chapter_title, chapter_desc in CHAPTER_CONFIG:
        if guide_key not in GUIDES:
            continue
        chapter_num += 1
        try:
            places = load_places(guide_key)
        except Exception:
            places = []
        place_names = [p.get("name") or "?" for p in places]

        html_path = output_dir / "{}_guide.html".format(guide_key)
        if not html_path.is_file():
            parts.append(
                '<div class="chapter-intro">'
                "<h2 class=\"chapter-title\">{}. {}</h2>"
                "<p>{}</p>"
                "<p class=\"block-label\">Места в главе (файл гида отсутствует)"
                "</p></div>".format(
                    chapter_num,
                    _escape(chapter_title),
                    _escape(chapter_desc),
                )
            )
            continue

        html = html_path.read_text(encoding="utf-8")
        sections = _extract_place_sections(html)

        list_items = "".join(
            "<li>{}</li>".format(_escape(n)) for n in place_names
        )
        intro = (
            '<div class="chapter-intro">'
            "<h2 class=\"chapter-title\">{}. {}</h2>"
            "<p>{}</p>"
            "<p class=\"block-label\">Объекты в этой главе</p>"
            "<ul class=\"place-list\">{}</ul>"
            "</div>"
        ).format(
            chapter_num,
            _escape(chapter_title),
            _escape(chapter_desc),
            list_items,
        )
        parts.append(intro)
        parts.extend(sections)

    refs = (
        '<div class="references-block">'
        "<h2>Примечания и источники</h2>"
        "{}"
        "</div>"
    ).format(REFERENCES_BODY.strip())
    parts.append(refs)

    body = "\n".join(parts)
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
</body>
</html>
""".format(
        title=_escape(PREFACE_TITLE),
        font_url=font_url,
        css=_COMBINED_CSS,
        body=body,
    )


def main() -> int:
    """Build combined HTML and PDF."""
    output_dir = OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    html_path = output_dir / "{}.html".format(OUTPUT_BASENAME)
    pdf_path = output_dir / "{}.pdf".format(OUTPUT_BASENAME)

    print("Building combined Moscow guide...")
    html_content = build_combined_html(output_dir)
    html_path.write_text(html_content, encoding="utf-8")
    print("Written: {}".format(html_path))

    try:
        from scripts.build_pdf import _pdf_via_playwright
        # Combined guide has many images; use longer timeout.
        if _pdf_via_playwright(
            html_path,
            pdf_path,
            image_wait_timeout_ms=90000,
        ):
            print("Written: {}".format(pdf_path))
        else:
            print(
                "PDF: install playwright and run 'playwright install chromium'.",
                file=sys.stderr,
            )
            return 1
    except Exception as e:
        print("PDF generation failed: {}.".format(e), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
