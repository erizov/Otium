# -*- coding: utf-8 -*-
"""
Единый скрипт: создание подкаталога для изображений, загрузка фото,
проверка дубликатов, генерация PDF-путеводителя по московским монастырям.
"""

import hashlib
import re
import socket
import sys
import threading
import urllib.request
from pathlib import Path

# Добавляем корень проекта в путь для импорт data
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

MIN_IMAGE_BYTES = 500
IMAGES_PER_PLACE = 4
MAPS_PER_PLACE = 1

# Файлы, которые не использовать в гиде монастырей
BANNED_IMAGE_BASENAMES = frozenset([
    "andreevsky_3.jpg", "andreevsky_4.jpg", "andronikov_3.jpg",
    "danilov_4.jpg", "donskoy_cathedral.jpg", "krutitsy_1.jpg",
    "novo_alekseevsky_4.jpg", "simonov_3.jpg", "zachatievsky_1.jpg",
    "zachatievsky_4.jpg", "vysoko_petrovsky_3.jpg", "vysoko_petrovsky_4.jpg",
])


GUIDE_EXPECTED_COUNTS: dict[str, int] = {
    "monasteries": 20,
    "churches": 60,
    "parks": 22,
    "museums": 32,
    "palaces": 22,
    "buildings": 52,
    "sculptures": 62,
    "places": 52,
}


def _load_guide_config(guide: str) -> None:
    """Загружает конфиг для гида (глобальные переменные)."""
    global IMAGES_SUBFOLDER, PLACES, IMAGE_DOWNLOADS, IMAGE_FALLBACKS
    global QA, BANNED, HTML_NAME, PDF_NAME, INTRO_TITLE, INTRO_SUBTITLE
    if guide == "churches":
        from data.churches import CHURCHES, IMAGES_SUBFOLDER as _SUB
        from data.church_image_urls import (
            CHURCH_IMAGE_DOWNLOADS,
            CHURCH_IMAGE_FALLBACKS,
        )
        from data.qa_churches import QA as _QA
        IMAGES_SUBFOLDER = _SUB
        PLACES = CHURCHES
        IMAGE_DOWNLOADS = CHURCH_IMAGE_DOWNLOADS
        IMAGE_FALLBACKS = CHURCH_IMAGE_FALLBACKS
        QA = _QA
        BANNED = frozenset()
        HTML_NAME = "churches_guide.html"
        PDF_NAME = "churches_guide.pdf"
        INTRO_TITLE = "Храмы Москвы"
        INTRO_SUBTITLE = "60 значимых храмов"
    elif guide == "parks":
        from data.parks import PARKS, IMAGES_SUBFOLDER as _SUB
        from data.park_image_urls import (
            PARK_IMAGE_DOWNLOADS,
            PARK_IMAGE_FALLBACKS,
        )
        from data.qa_parks import QA as _QA
        IMAGES_SUBFOLDER = _SUB
        PLACES = PARKS
        IMAGE_DOWNLOADS = PARK_IMAGE_DOWNLOADS
        IMAGE_FALLBACKS = PARK_IMAGE_FALLBACKS
        QA = _QA
        BANNED = frozenset()
        HTML_NAME = "parks_guide.html"
        PDF_NAME = "parks_guide.pdf"
        INTRO_TITLE = "Парки Москвы"
        INTRO_SUBTITLE = "22 лучших парка"
    elif guide == "museums":
        from data.museums import MUSEUMS, IMAGES_SUBFOLDER as _SUB
        from data.museum_image_urls import (
            MUSEUM_IMAGE_DOWNLOADS,
            MUSEUM_IMAGE_FALLBACKS,
        )
        from data.qa_museums import QA as _QA
        IMAGES_SUBFOLDER = _SUB
        PLACES = MUSEUMS
        IMAGE_DOWNLOADS = MUSEUM_IMAGE_DOWNLOADS
        IMAGE_FALLBACKS = MUSEUM_IMAGE_FALLBACKS
        QA = _QA
        BANNED = frozenset()
        HTML_NAME = "museums_guide.html"
        PDF_NAME = "museums_guide.pdf"
        INTRO_TITLE = "Музеи Москвы"
        INTRO_SUBTITLE = "32 лучших музея"
    elif guide == "palaces":
        from data.palaces import PALACES, IMAGES_SUBFOLDER as _SUB
        from data.palace_image_urls import (
            PALACE_IMAGE_DOWNLOADS,
            PALACE_IMAGE_FALLBACKS,
        )
        from data.qa_palaces import QA as _QA
        IMAGES_SUBFOLDER = _SUB
        PLACES = PALACES
        IMAGE_DOWNLOADS = PALACE_IMAGE_DOWNLOADS
        IMAGE_FALLBACKS = PALACE_IMAGE_FALLBACKS
        QA = _QA
        BANNED = frozenset()
        HTML_NAME = "palaces_guide.html"
        PDF_NAME = "palaces_guide.pdf"
        INTRO_TITLE = "Усадьбы и дворцы Москвы"
        INTRO_SUBTITLE = "22 лучших усадьбы и дворца"
    elif guide == "buildings":
        from data.buildings import BUILDINGS, IMAGES_SUBFOLDER as _SUB
        from data.building_image_urls import (
            BUILDING_IMAGE_DOWNLOADS,
            BUILDING_IMAGE_FALLBACKS,
        )
        from data.qa_buildings import QA as _QA
        IMAGES_SUBFOLDER = _SUB
        PLACES = BUILDINGS
        IMAGE_DOWNLOADS = BUILDING_IMAGE_DOWNLOADS
        IMAGE_FALLBACKS = BUILDING_IMAGE_FALLBACKS
        QA = _QA
        BANNED = frozenset()
        HTML_NAME = "buildings_guide.html"
        PDF_NAME = "buildings_guide.pdf"
        INTRO_TITLE = "Знаменитые здания Москвы"
        INTRO_SUBTITLE = "52 знаменитых здания"
    elif guide == "sculptures":
        from data.sculptures import SCULPTURES, IMAGES_SUBFOLDER as _SUB
        from data.sculpture_image_urls import (
            SCULPTURE_IMAGE_DOWNLOADS,
            SCULPTURE_IMAGE_FALLBACKS,
        )
        from data.qa_sculptures import QA as _QA
        IMAGES_SUBFOLDER = _SUB
        PLACES = SCULPTURES
        IMAGE_DOWNLOADS = SCULPTURE_IMAGE_DOWNLOADS
        IMAGE_FALLBACKS = SCULPTURE_IMAGE_FALLBACKS
        QA = _QA
        BANNED = frozenset()
        HTML_NAME = "sculptures_guide.html"
        PDF_NAME = "sculptures_guide.pdf"
        INTRO_TITLE = "Скульптуры и памятники Москвы"
        INTRO_SUBTITLE = "62 скульптуры и памятника"
    elif guide == "places":
        from data.places import PLACES as _PLACES, IMAGES_SUBFOLDER as _SUB
        from data.place_image_urls import (
            PLACE_IMAGE_DOWNLOADS,
            PLACE_IMAGE_FALLBACKS,
        )
        from data.qa_places import QA as _QA
        IMAGES_SUBFOLDER = _SUB
        PLACES = _PLACES
        IMAGE_DOWNLOADS = PLACE_IMAGE_DOWNLOADS
        IMAGE_FALLBACKS = PLACE_IMAGE_FALLBACKS
        QA = _QA
        BANNED = frozenset()
        HTML_NAME = "places_guide.html"
        PDF_NAME = "places_guide.pdf"
        INTRO_TITLE = "Места Москвы"
        INTRO_SUBTITLE = "52 лучших места (улицы, площади, районы)"
    else:
        from data.monasteries import MONASTERIES, IMAGES_SUBFOLDER as _SUB
        from data.image_urls import IMAGE_DOWNLOADS as _DL, IMAGE_FALLBACKS as _FB
        from data.qa import QA as _QA
        IMAGES_SUBFOLDER = _SUB
        PLACES = MONASTERIES
        IMAGE_DOWNLOADS = _DL
        IMAGE_FALLBACKS = _FB
        QA = _QA
        BANNED = BANNED_IMAGE_BASENAMES
        HTML_NAME = "monasteries_guide.html"
        PDF_NAME = "monasteries_guide.pdf"
        INTRO_TITLE = "Монастыри Москвы"
        INTRO_SUBTITLE = "маршруты созерцания и памяти"


def _map_img_url(lon: float, lat: float, width: int = 380, height: int = 200) -> str:
    """URL статической карты (Яндекс) по координатам."""
    return (
        "https://static-maps.yandex.ru/1.x/?ll={lon:.4f},{lat:.4f}&z=16&l=map"
        "&size={w},{h}".format(lon=lon, lat=lat, w=width, h=height)
    )


def _escape(s: str) -> str:
    """Экранирование HTML."""
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _file_hash(path: Path) -> str:
    """SHA256 hash of file contents (for deduplication)."""
    if not path.exists() or not path.is_file():
        return ""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def download_images(output_dir: Path) -> None:
    """
    Скачивает фотографии в output/images/moscow_monasteries/.
    URL берутся из data.image_urls (Wikimedia Commons).
    Для каждого файла пробует основной URL и fallback-источники;
    несколько проходов, пока есть загрузки.
    """
    try:
        import time
        import urllib.request
    except ImportError:
        return

    images_dir = output_dir / "images" / IMAGES_SUBFOLDER
    images_dir.mkdir(parents=True, exist_ok=True)
    max_rounds = 8

    for _round in range(max_rounds):
        downloaded = 0
        for filename, main_url in IMAGE_DOWNLOADS.items():
            if filename in BANNED:
                continue
            path = images_dir / filename
            if path.exists() and path.stat().st_size >= MIN_IMAGE_BYTES:
                continue
            if path.exists():
                path.unlink()
            urls_to_try = [main_url] + list(IMAGE_FALLBACKS.get(filename, []))
            for url in urls_to_try:
                try:
                    req = urllib.request.Request(
                        url,
                        headers={
                            "User-Agent": "ExcursionGuide/1.0 (https://github.com/)"
                        },
                    )
                    with urllib.request.urlopen(req, timeout=15) as resp:
                        data = resp.read()
                    if len(data) < MIN_IMAGE_BYTES:
                        continue
                    path.write_bytes(data)
                    print("Downloaded:", filename)
                    downloaded += 1
                    break
                except Exception as e:
                    continue
                finally:
                    time.sleep(0.3)
        if downloaded == 0:
            break


def ensure_images_subdir(output_dir: Path) -> Path:
    """Создаёт output/images и output/images/<IMAGES_SUBFOLDER> при отсутствии."""
    images_dir = output_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    subdir = images_dir / IMAGES_SUBFOLDER
    subdir.mkdir(parents=True, exist_ok=True)
    return subdir


def check_duplicate_images(images_dir: Path) -> list[tuple[str, list[str]]]:
    """
    Проверяет дубликаты по содержимому (SHA256).
    Возвращает список (hash, [имена файлов с этим хешем]) для групп из 2+ файлов.
    """
    hash_to_files: dict[str, list[str]] = {}
    for path in images_dir.iterdir():
        if not path.is_file():
            continue
        if path.stat().st_size < MIN_IMAGE_BYTES:
            continue
        h = _file_hash(path)
        if not h:
            continue
        if h not in hash_to_files:
            hash_to_files[h] = []
        hash_to_files[h].append(path.name)
    duplicates = [
        (h, sorted(files))
        for h, files in hash_to_files.items()
        if len(files) > 1
    ]
    return duplicates


def _unique_images_for_place(
    image_rels: list[str], output_dir: Path,
) -> list[str]:
    """Возвращает до IMAGES_PER_PLACE уникальных путей (разный контент)."""
    seen_hashes: set[str] = set()
    result: list[str] = []
    for img_rel in image_rels:
        if len(result) >= IMAGES_PER_PLACE:
            break
        basename = img_rel.split("/")[-1] if "/" in img_rel else img_rel
        if basename in BANNED:
            continue
        path = output_dir / img_rel
        if not path.exists() or not path.is_file():
            continue
        if path.stat().st_size < MIN_IMAGE_BYTES:
            continue
        h = _file_hash(path)
        if not h or h in seen_hashes:
            continue
        seen_hashes.add(h)
        result.append(img_rel)
    return result


def get_used_image_basenames(output_dir: Path) -> set[str]:
    """Имена файлов изображений, реально используемых в путеводителе."""
    used: set[str] = set()
    for place in PLACES:
        rels = _unique_images_for_place(place["images"], output_dir)
        for r in rels:
            basename = r.split("/")[-1] if "/" in r else r
            if basename not in BANNED:
                used.add(basename)
    return used


def delete_unused_images(output_dir: Path) -> int:
    """
    Удаляет из output/images/moscow_monasteries файлы, не используемые в гиде.
    Возвращает количество удалённых файлов.
    """
    used = get_used_image_basenames(output_dir)
    images_dir = output_dir / "images" / IMAGES_SUBFOLDER
    if not images_dir.exists():
        return 0
    deleted = 0
    for path in images_dir.iterdir():
        if not path.is_file():
            continue
        if path.name not in used:
            path.unlink()
            deleted += 1
    return deleted


def _section_place(
    number: int, m: dict, output_dir: Path
) -> str:
    """HTML-блок для одного места (монастырь или храм): фото + карта."""
    name = _escape(m["name"])
    address = _escape(m["address"])
    style = _escape(m["style"])
    history = _escape(m["history"])
    significance = _escape(m["significance"])
    map_url = _map_img_url(m["lon"], m["lat"])

    highlights_html = "".join(
        "<li>{}</li>".format(_escape(h)) for h in m["highlights"]
    )
    facts_html = "".join("<li>{}</li>".format(_escape(f)) for f in m["facts"])

    unique_rels = _unique_images_for_place(m["images"], output_dir)
    imgs_html_parts = [
        '<img src="{}" alt="" class="monastery-img" />'.format(
            img_rel.replace("\\", "/")
        )
        for img_rel in unique_rels
    ]
    imgs_html = "\n".join(imgs_html_parts) if imgs_html_parts else ""
    images_block = (
        "  <div class=\"images-row\">\n    {}\n  </div>".format(imgs_html)
        if imgs_html else ""
    )
    name_str = m.get("name", "")
    title_class = (
        "monastery-title source-serif-title"
        if "я" in name_str.lower() else "monastery-title"
    )

    return """
<section class="monastery" id="monastery-{num}" tabindex="-1">
  <h2 class="{title_class}">{num}. {name}</h2>
  <p class="meta"><strong>Адрес:</strong> {address} &nbsp;|&nbsp; <strong>Стиль:</strong> {style}</p>
  <p class="block-label">История</p>
  <p class="body-text">{history}</p>
  <p class="block-label">Значение</p>
  <p class="body-text">{significance}</p>
  <p class="block-label">Объекты</p>
  <ul>{highlights_html}</ul>
  <p class="block-label">Факты</p>
  <ul>{facts_html}</ul>
  <div class="visual-block">
{images_block}
  <div class="map-block">
    <img src="{map_url}" alt="" class="map-img" />
  </div>
  </div>
</section>
""".format(
        num=number,
        name=name,
        title_class=title_class,
        address=address,
        style=style,
        images_block=images_block,
        map_url=map_url,
        history=history,
        significance=significance,
        highlights_html=highlights_html,
        facts_html=facts_html,
    )


def _section_qa() -> str:
    """HTML-блок вопросов и ответов."""
    items = []
    for i, qa in enumerate(QA, 1):
        q = _escape(qa["question"])
        a = _escape(qa["answer"])
        items.append(
            '<div class="qa-item">'
            '<p class="question"><strong>Вопрос {n}. {q}</strong></p>'
            '<p class="answer">Ответ: {a}</p>'
            "</div>".format(n=i, q=q, a=a)
        )
    return """
<section class="qa-section" id="qa" tabindex="-1">
  <h2>Вопросы и ответы по фактам</h2>
  {items}
</section>
""".format(
        items="\n".join(items)
    )


def build_html(output_dir: Path) -> str:
    """Собирает полный HTML (~1 страница на монастырь)."""
    # Single braces: CSS is inserted as-is into HTML (no .format on this string)
    css = """
      @page { size: A4; margin: 2cm 1.5cm 1.5cm 1.8cm; }
      *, html, body { -webkit-print-color-adjust: exact;
                      print-color-adjust: exact; }
      html { background-color: #faf8f5; }
      html, body { margin: 0; padding: 0; font-family: "Source Serif 4",
        Georgia, "Times New Roman", serif;
        font-size: 10pt; line-height: 1.45; color: #1c1b19;
        background-color: #faf8f5; }
      body { color: #1c1b19 !important; background-color: #faf8f5 !important; }
      h1 { font-family: "Source Serif 4", Georgia, serif;
           font-size: 18pt; text-align: center; margin: 0 0 0.5em;
           color: #1c1b19 !important; }
      h2 { font-family: "Source Serif 4", Georgia, serif;
           color: #1c1b19 !important; }
      h2.monastery-title { font-family: Pochaevsk, Georgia, serif;
           font-size: 17pt; margin: 1.2em 0 0.4em 0.3em;
           border-bottom: 1px solid #8b7355; padding-bottom: 0.25em;
           color: #2c2a28 !important; }
      h2.monastery-title.source-serif-title { font-family: "Source Serif 4",
           Georgia, serif; }
      .meta, .block-label { font-family: Inter, "IBM Plex Sans", sans-serif;
          font-size: 8.5pt; letter-spacing: 0.02em; }
      .meta { margin: 0.2em 0 0.6em 0.3em; color: #6b635b !important; }
      .block-label { margin: 0.6em 0 0.15em 0.3em; text-transform: uppercase;
                     font-weight: 600; color: #6b7b8a !important; }
      .body-text { margin: 0 0 0.4em 0.3em; text-align: left; max-width: 42em;
                   color: #1c1b19; font-family: "Source Serif 4", Georgia, serif; }
      ul, li, p { color: #1c1b19; font-family: "Source Serif 4", Georgia, serif; }
      .intro-block { page-break-after: always; padding: 2.5em 1em 0 1.2em;
                     background-color: #faf8f5; }
      .intro-block .otium-brand { font-family: Inter, sans-serif;
        font-size: 8pt; letter-spacing: 0.2em; color: #6b635b !important;
        margin-bottom: 0.3em; }
      .intro-block .otium-title { font-family: "Source Serif 4", Georgia, serif;
        font-size: 20pt; font-weight: 600; text-align: center;
        margin: 0.2em 0 0.1em; color: #1a1a1a !important; }
      .intro-block .otium-subtitle { font-family: "Source Serif 4", Georgia, serif;
        font-size: 11pt; text-align: center; color: #6b635b !important;
        font-style: italic; margin-bottom: 1em; }
      .intro-block p { margin: 0.4em 0; font-size: 9.5pt; line-height: 1.5;
        text-align: justify; max-width: 38em; margin-left: auto;
        margin-right: auto; color: #1c1b19;
        font-family: "Source Serif 4", Georgia, serif; }
      .monastery { display: block; page-break-before: always;
                    break-before: page; padding: 1.5em 0 0; }
      .monastery:first-of-type { page-break-before: auto; break-before: auto; }
      .monastery:last-of-type { padding-bottom: 0.5em; }
      .visual-block { margin: 0.8em 0 0; page-break-after: always; }
      .monastery:last-of-type .visual-block { page-break-after: auto; }
      .images-row { display: flex; gap: 10px; margin: 1em; flex-wrap: wrap; }
      .monastery-img { flex: 1 1 200px; max-width: 100%; height: 150px;
                        object-fit: cover; }
      .map-block { margin: 1em; }
      .map-img { max-width: 100%; height: auto; max-height: 160px;
                  border: 1px solid #e0ddd8; }
      .qa-section { margin-top: 2em; page-break-before: always;
                     break-before: page; padding-top: 1.5em; }
      .qa-item { margin-bottom: 0.6em; font-size: 9pt; color: #1c1b19; }
      .question { margin-bottom: 0.1em; color: #1c1b19; }
      .answer { margin-left: 0.5em; color: #2c2a28;
        font-family: "Source Serif 4", Georgia, serif; }
      ul { margin: 0.2em 0 0.4em 0.3em; padding-left: 1.2em; color: #1c1b19; }
      p { margin: 0.2em 0; color: #1c1b19; }
      .map-block { background: transparent; }
      @media print {
        html, body { color: #1c1b19 !important; background: #faf8f5 !important; }
        .block-label { color: #6b7b8a !important; }
        .meta { color: #6b635b !important; }
        .monastery { page-break-before: always; break-before: page; }
        .monastery:first-of-type { page-break-before: auto; break-before: auto; }
      }
    """
    intro = """
    <div class="intro-block">
    <p class="otium-brand">OTIUM / Sacred</p>
    <h1 class="otium-title">{intro_title}</h1>
    <p class="otium-subtitle">{intro_subtitle}</p>
    <p>OTIUM — это практика осмысленного досуга.
    В античной традиции otium означало не отдых от труда, а время, в котором
    человек возвращается к взгляду, памяти и мышлению. Это время без
    утилитарной цели, без спешки, без требования результата.</p>
    <p>Мы создаём маршруты не для «посещения», а для пребывания.
    Не для потребления культуры, а для внимательного присутствия в ней.</p>
    <p>OTIUM работает с пространствами, где время уплотняется:
    архитектурой, сакральными местами, кино, памятью, ландшафтом.
    Мы не стремимся охватить всё и не обещаем «лучшее».
    Мы отбираем немногое — то, что выдерживает тишину и повторный взгляд.</p>
    <p>OTIUM — это не гид и не сервис.
    Это приглашение к прогулке без обязательств.
    К маршруту, который можно прервать.
    К месту, где можно задержаться.</p>
    <p>OTIUM существует для тех, кто хочет смотреть медленно.</p>
    </div>
    """.format(
        intro_title=INTRO_TITLE,
        intro_subtitle=INTRO_SUBTITLE,
    )
    sections = [intro]
    for i, m in enumerate(PLACES, 1):
        sections.append(_section_place(i, m, output_dir))
    sections.append(_section_qa())

    return """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <title>{page_title}</title>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant:ital,wght@0,400;0,600&amp;family=EB+Garamond:ital,wght@0,400;0,600&amp;family=Pochaevsk&amp;family=Source+Serif+4:ital,wght@0,400;0,600&amp;family=Inter:wght@400;500;600&amp;display=swap&amp;subset=latin,cyrillic"
        rel="stylesheet" />
  <style>{css}</style>
</head>
<body>
{body}
</body>
</html>
""".format(
        css=css,
        body="\n".join(sections),
        page_title=INTRO_TITLE,
    )


def validate_yandex_maps() -> list[str]:
    """
    Проверяет, что статические карты Яндекса для каждого места
    доступны (URL возвращает 200). Возвращает список сообщений об ошибках.
    """
    errors: list[str] = []
    for m in PLACES:
        name = m.get("name", "?")
        lon = m.get("lon")
        lat = m.get("lat")
        if lon is None or lat is None:
            errors.append("{}: нет координат (lat/lon).".format(name))
            continue
        url = _map_img_url(lon, lat)
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "ExcursionGuide/1.0"},
                method="GET",
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status != 200:
                    errors.append(
                        "{}: карта вернула {}.".format(name, resp.status)
                    )
        except Exception as e:
            errors.append("{}: карта недоступна — {}.".format(name, e))
    return errors


def validate_output(html_path: Path, output_dir: Path) -> list[str]:
    """Проверяет HTML на битые ссылки и плейсхолдеры. Возвращает список ошибок."""
    errors: list[str] = []
    html = html_path.read_text(encoding="utf-8")

    for m in re.finditer(r'<img[^>]+src="([^"]+)"', html):
        src = m.group(1)
        if src.startswith("http"):
            continue
        if src.startswith("images/") and "/" in src:
            local = output_dir / src
            if not local.exists():
                errors.append("Missing image: {}".format(src))
            elif local.stat().st_size < MIN_IMAGE_BYTES:
                errors.append("Too small (placeholder?): {}".format(src))

    map_srcs = re.findall(
        r'<img[^>]+class="map-img"[^>]+src="([^"]+)"', html
    )
    for url in map_srcs:
        if not url.startswith("http") or "yandex" not in url:
            errors.append("Map URL unexpected: {}...".format(url[:50]))

    return errors


def _free_port() -> int:
    """Возвращает свободный порт для локального сервера."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _pdf_via_playwright(html_path: Path, pdf_path: Path) -> bool:
    """
    Генерирует PDF из HTML через Playwright.
    Отдаёт страницу по HTTP, чтобы Google Fonts загружались; ждёт шрифты.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return False

    output_dir = html_path.parent
    port = _free_port()
    thread = server = None
    try:
        from http.server import HTTPServer
        from http.server import SimpleHTTPRequestHandler
        from functools import partial
        handler = partial(
            SimpleHTTPRequestHandler,
            directory=str(output_dir.resolve()),
        )
        server = HTTPServer(("127.0.0.1", port), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
    except Exception as e:
        print("HTTP server failed:", e, file=sys.stderr)
        server = None

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            if server is not None:
                url = "http://127.0.0.1:{}/{}".format(port, html_path.name)
                page.goto(url, wait_until="networkidle")
            else:
                page.goto(
                    "file://{}".format(html_path.resolve().as_posix()),
                    wait_until="networkidle",
                )
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(800)
            # Wait for all images (including maps) to load so they appear in PDF
            page.wait_for_function(
                "() => { const imgs = document.querySelectorAll('img'); "
                "return imgs.length === 0 || Array.from(imgs).every("
                "i => i.complete && i.naturalWidth > 0); }",
                timeout=15000,
            )
            page.wait_for_timeout(500)
            # Use screen media so background colors and images are not stripped
            page.emulate_media(media="screen")
            page.pdf(
                path=str(pdf_path),
                format="A4",
                margin={"top": "1.2cm", "right": "1.2cm",
                        "bottom": "1.2cm", "left": "1.2cm"},
                print_background=True,
            )
            browser.close()
        return True
    except Exception as e:
        print("Playwright PDF failed:", e, file=sys.stderr)
        return False
    finally:
        if server is not None:
            server.shutdown()


def _strip_pdf_metadata(pdf_path: Path) -> None:
    """
    Заменяет метаданные PDF на нейтральные (без имени, адреса, компьютера).
    Перезаписывает файл.
    """
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        return
    try:
        reader = PdfReader(str(pdf_path))
        writer = PdfWriter()
        for p in reader.pages:
            writer.add_page(p)
        writer.add_metadata({
            "/Producer": "Excursion",
            "/Creator": "Excursion",
        })
        with open(pdf_path, "wb") as f:
            writer.write(f)
    except Exception as e:
        print("  Strip metadata: {}.".format(e), file=sys.stderr)


def main() -> None:
    """Создаёт подкаталог, скачивает фото, проверяет дубликаты, генерирует PDF."""
    import argparse
    parser = argparse.ArgumentParser(description="Build PDF guide (monasteries or churches)")
    parser.add_argument(
        "--guide",
        choices=[
            "monasteries", "churches", "parks", "museums", "palaces",
            "buildings", "sculptures", "places",
        ],
        default="monasteries",
        help="Guide: monasteries(20), churches(60), parks(22), museums(32), "
             "palaces(22), buildings(52), sculptures(62), places(52)",
    )
    args = parser.parse_args()
    _load_guide_config(args.guide)

    output_dir = _project_root / "output"
    output_dir.mkdir(exist_ok=True)

    images_subdir = ensure_images_subdir(output_dir)
    print("Images subdir: {}".format(images_subdir))
    print("Guide: {} ({} places)".format(args.guide, len(PLACES)))

    expected = GUIDE_EXPECTED_COUNTS.get(args.guide, 20)
    if len(PLACES) != expected:
        print(
            "Warning: expected {} places, got {}.".format(expected, len(PLACES)),
            file=sys.stderr,
        )

    print("Downloading images...")
    download_images(output_dir)

    print("Checking duplicate images...")
    duplicates = check_duplicate_images(images_subdir)
    if duplicates:
        for h, files in duplicates:
            print("  Duplicate ({}): {}".format(h[:12], ", ".join(files)))
    else:
        print("  No duplicate images by content.")

    print("Validating Yandex map URLs...")
    map_errors = validate_yandex_maps()
    if map_errors:
        for e in map_errors:
            print("  -", e, file=sys.stderr)
    else:
        print("  All map URLs OK.")

    html_path = output_dir / HTML_NAME
    pdf_path = output_dir / PDF_NAME

    html_content = build_html(output_dir)
    html_path.write_text(html_content, encoding="utf-8")
    if _pdf_via_playwright(html_path, pdf_path):
        _strip_pdf_metadata(pdf_path)
        print("Written:", pdf_path)
    else:
        print(
            "PDF: install playwright and run 'playwright install chromium'.",
            file=sys.stderr,
        )
    print("Written:", html_path)

    deleted = delete_unused_images(output_dir)
    if deleted:
        print("Removed {} unused image(s).".format(deleted))

    errors = validate_output(html_path, output_dir)
    if errors:
        print("Validation:", file=sys.stderr)
        for e in errors:
            print("  -", e, file=sys.stderr)
    else:
        print("Validation: no broken links or placeholders found.")


if __name__ == "__main__":
    main()
