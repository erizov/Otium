# -*- coding: utf-8 -*-
"""
Единый скрипт: создание подкаталога для изображений, загрузка фото,
проверка дубликатов, генерация PDF-путеводителя по московским монастырям.
"""

import io
import json
import re
import shutil
import socket
import sys
import threading
import urllib.request
from pathlib import Path
from typing import Optional

# Добавляем корень проекта в путь для импорт data
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

# Fix Windows console encoding for Cyrillic (run before any prints)
if sys.platform == "win32":
    for _name, _s in [("stdout", sys.stdout), ("stderr", sys.stderr)]:
        if hasattr(_s, "buffer"):
            try:
                _w = io.TextIOWrapper(_s.buffer, encoding="utf-8", errors="replace")
                setattr(sys, _name, _w)
            except (AttributeError, OSError):
                pass

from scripts.image_utils import image_content_hash

MIN_IMAGE_BYTES = 500
IMAGES_PER_PLACE = 4
# Optimized guide: 3 photos + 1 map = 2x2 grid per place
OPT_IMAGES_PER_PLACE = 3
MAPS_PER_PLACE = 1
# Include item in guide if it has at least this many distinct images
MIN_IMAGES_TO_BUILD = 2
# Optimized: include place if it has at least 1 image
MIN_IMAGES_OPT = 1

# Файлы, которые не использовать в гиде монастырей
BANNED_IMAGE_BASENAMES = frozenset([
    "andreevsky_3.jpg", "andreevsky_4.jpg", "andronikov_3.jpg",
    "danilov_4.jpg", "donskoy_cathedral.jpg", "krutitsy_1.jpg",
    "novo_alekseevsky_4.jpg", "simonov_3.jpg", "zachatievsky_1.jpg",
    "zachatievsky_4.jpg", "vysoko_petrovsky_3.jpg", "vysoko_petrovsky_4.jpg",
])


GUIDE_EXPECTED_COUNTS: dict[str, int] = {
    "test_e2e": 5,
    "monasteries": 20,
    "places_of_worship": 66,
    "parks": 28,
    "museums": 32,
    "palaces": 24,
    "buildings": 42,
    "sculptures": 61,
    "places": 30,
    "metro": 37,
    "theaters": 14,
    "viewpoints": 14,
    "bridges": 12,
    "squares": 12,
    "markets": 8,
    "libraries": 7,
    "railway_stations": 9,
    "cemeteries": 9,
    "landmarks": 14,
    "cafes": 11,
}


def _load_guide_config(guide: str) -> None:
    """Загружает конфиг для гида (глобальные переменные)."""
    global IMAGES_SUBFOLDER, PLACES, IMAGE_DOWNLOADS, IMAGE_FALLBACKS
    global QA, BANNED, HTML_NAME, PDF_NAME, INTRO_TITLE, INTRO_SUBTITLE
    if guide == "places_of_worship":
        from data.places_of_worship import (
            PLACES_OF_WORSHIP,
            IMAGES_SUBFOLDER as _SUB,
        )
        from data.places_of_worship_image_urls import (
            PLACES_OF_WORSHIP_IMAGE_DOWNLOADS,
            PLACES_OF_WORSHIP_IMAGE_FALLBACKS,
        )
        from data.qa_places_of_worship import QA as _QA
        IMAGES_SUBFOLDER = _SUB
        PLACES = PLACES_OF_WORSHIP
        IMAGE_DOWNLOADS = PLACES_OF_WORSHIP_IMAGE_DOWNLOADS
        IMAGE_FALLBACKS = PLACES_OF_WORSHIP_IMAGE_FALLBACKS
        QA = _QA
        BANNED = frozenset()
        HTML_NAME = "places_of_worship_guide.html"
        PDF_NAME = "places_of_worship_guide.pdf"
        INTRO_TITLE = "Места поклонения Москвы"
        INTRO_SUBTITLE = "66 мест поклонения (православные храмы, мечети, синагоги, буддийские храмы, неортодоксальные христианские церкви)"
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
        INTRO_SUBTITLE = "28 парков"
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
        INTRO_SUBTITLE = "32 музея"
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
        INTRO_TITLE = "Дворцы и усадьбы Москвы"
        INTRO_SUBTITLE = "24 дворца и усадьбы"
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
        INTRO_TITLE = "Дома Москвы"
        INTRO_SUBTITLE = "50 знаменитых домов"
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
        INTRO_SUBTITLE = "61 скульптура и памятник"
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
        INTRO_SUBTITLE = "46 лучших мест (улицы, площади, районы)"
    elif guide == "metro":
        from data.metro_stations import METRO_STATIONS, IMAGES_SUBFOLDER as _SUB
        from data.metro_image_urls import (
            METRO_IMAGE_DOWNLOADS,
            METRO_IMAGE_FALLBACKS,
        )
        from data.qa_metro import QA as _QA
        IMAGES_SUBFOLDER = _SUB
        PLACES = METRO_STATIONS
        IMAGE_DOWNLOADS = METRO_IMAGE_DOWNLOADS
        IMAGE_FALLBACKS = METRO_IMAGE_FALLBACKS
        QA = _QA
        BANNED = frozenset()
        HTML_NAME = "metro_guide.html"
        PDF_NAME = "metro_guide.pdf"
        INTRO_TITLE = "Станции Московского метро"
        INTRO_SUBTITLE = "37 лучших станций"
    elif guide == "theaters":
        from data.theaters import THEATERS, IMAGES_SUBFOLDER as _SUB
        from data.theater_image_urls import (
            THEATER_IMAGE_DOWNLOADS,
            THEATER_IMAGE_FALLBACKS,
        )
        from data.qa_theaters import QA as _QA
        IMAGES_SUBFOLDER = _SUB
        PLACES = THEATERS
        IMAGE_DOWNLOADS = THEATER_IMAGE_DOWNLOADS
        IMAGE_FALLBACKS = THEATER_IMAGE_FALLBACKS
        QA = _QA
        BANNED = frozenset()
        HTML_NAME = "theaters_guide.html"
        PDF_NAME = "theaters_guide.pdf"
        INTRO_TITLE = "Театры Москвы"
        INTRO_SUBTITLE = "12 театров"
    elif guide == "viewpoints":
        from data.viewpoints import VIEWPOINTS, IMAGES_SUBFOLDER as _SUB
        from data.viewpoint_image_urls import (
            VIEWPOINT_IMAGE_DOWNLOADS,
            VIEWPOINT_IMAGE_FALLBACKS,
        )
        from data.qa_viewpoints import QA as _QA
        IMAGES_SUBFOLDER = _SUB
        PLACES = VIEWPOINTS
        IMAGE_DOWNLOADS = VIEWPOINT_IMAGE_DOWNLOADS
        IMAGE_FALLBACKS = VIEWPOINT_IMAGE_FALLBACKS
        QA = _QA
        BANNED = frozenset()
        HTML_NAME = "viewpoints_guide.html"
        PDF_NAME = "viewpoints_guide.pdf"
        INTRO_TITLE = "Смотровые площадки Москвы"
        INTRO_SUBTITLE = "13 смотровых площадок"
    elif guide == "bridges":
        from data.bridges import BRIDGES, IMAGES_SUBFOLDER as _SUB
        from data.bridge_image_urls import (
            BRIDGE_IMAGE_DOWNLOADS,
            BRIDGE_IMAGE_FALLBACKS,
        )
        from data.qa_bridges import QA as _QA
        IMAGES_SUBFOLDER = _SUB
        PLACES = BRIDGES
        IMAGE_DOWNLOADS = BRIDGE_IMAGE_DOWNLOADS
        IMAGE_FALLBACKS = BRIDGE_IMAGE_FALLBACKS
        QA = _QA
        BANNED = frozenset()
        HTML_NAME = "bridges_guide.html"
        PDF_NAME = "bridges_guide.pdf"
        INTRO_TITLE = "Мосты Москвы"
        INTRO_SUBTITLE = "10 знаменитых мостов"
    elif guide == "squares":
        from data.squares import SQUARES, IMAGES_SUBFOLDER as _SUB
        from data.squares_image_urls import (
            SQUARES_IMAGE_DOWNLOADS,
            SQUARES_IMAGE_FALLBACKS,
        )
        from data.qa_squares import QA as _QA
        IMAGES_SUBFOLDER = _SUB
        PLACES = SQUARES
        IMAGE_DOWNLOADS = SQUARES_IMAGE_DOWNLOADS
        IMAGE_FALLBACKS = SQUARES_IMAGE_FALLBACKS
        QA = _QA
        BANNED = frozenset()
        HTML_NAME = "squares_guide.html"
        PDF_NAME = "squares_guide.pdf"
        INTRO_TITLE = "Площади Москвы"
        INTRO_SUBTITLE = "12 площадей"
    elif guide == "markets":
        from data.markets import MARKETS, IMAGES_SUBFOLDER as _SUB
        from data.market_image_urls import (
            MARKET_IMAGE_DOWNLOADS,
            MARKET_IMAGE_FALLBACKS,
        )
        from data.qa_markets import QA as _QA
        IMAGES_SUBFOLDER = _SUB
        PLACES = MARKETS
        IMAGE_DOWNLOADS = MARKET_IMAGE_DOWNLOADS
        IMAGE_FALLBACKS = MARKET_IMAGE_FALLBACKS
        QA = _QA
        BANNED = frozenset()
        HTML_NAME = "markets_guide.html"
        PDF_NAME = "markets_guide.pdf"
        INTRO_TITLE = "Рынки и гастрономические центры Москвы"
        INTRO_SUBTITLE = "7 рынков и гастрономических центров"
    elif guide == "libraries":
        from data.libraries import LIBRARIES, IMAGES_SUBFOLDER as _SUB
        from data.library_image_urls import (
            LIBRARY_IMAGE_DOWNLOADS,
            LIBRARY_IMAGE_FALLBACKS,
        )
        from data.qa_libraries import QA as _QA
        IMAGES_SUBFOLDER = _SUB
        PLACES = LIBRARIES
        IMAGE_DOWNLOADS = LIBRARY_IMAGE_DOWNLOADS
        IMAGE_FALLBACKS = LIBRARY_IMAGE_FALLBACKS
        QA = _QA
        BANNED = frozenset()
        HTML_NAME = "libraries_guide.html"
        PDF_NAME = "libraries_guide.pdf"
        INTRO_TITLE = "Библиотеки Москвы"
        INTRO_SUBTITLE = "5 знаменитых библиотек"
    elif guide == "railway_stations":
        from data.railway_stations import (
            RAILWAY_STATIONS,
            IMAGES_SUBFOLDER as _SUB,
        )
        from data.railway_station_image_urls import (
            RAILWAY_STATION_IMAGE_DOWNLOADS,
            RAILWAY_STATION_IMAGE_FALLBACKS,
        )
        from data.qa_railway_stations import QA as _QA
        IMAGES_SUBFOLDER = _SUB
        PLACES = RAILWAY_STATIONS
        IMAGE_DOWNLOADS = RAILWAY_STATION_IMAGE_DOWNLOADS
        IMAGE_FALLBACKS = RAILWAY_STATION_IMAGE_FALLBACKS
        QA = _QA
        BANNED = frozenset()
        HTML_NAME = "railway_stations_guide.html"
        PDF_NAME = "railway_stations_guide.pdf"
        INTRO_TITLE = "Вокзалы Москвы"
        INTRO_SUBTITLE = "9 главных вокзалов"
    elif guide == "cemeteries":
        from data.cemeteries import CEMETERIES, IMAGES_SUBFOLDER as _SUB
        from data.cemetery_image_urls import (
            CEMETERY_IMAGE_DOWNLOADS,
            CEMETERY_IMAGE_FALLBACKS,
        )
        from data.qa_cemeteries import QA as _QA
        IMAGES_SUBFOLDER = _SUB
        PLACES = CEMETERIES
        IMAGE_DOWNLOADS = CEMETERY_IMAGE_DOWNLOADS
        IMAGE_FALLBACKS = CEMETERY_IMAGE_FALLBACKS
        QA = _QA
        BANNED = frozenset()
        HTML_NAME = "cemeteries_guide.html"
        PDF_NAME = "cemeteries_guide.pdf"
        INTRO_TITLE = "Некрополи Москвы"
        INTRO_SUBTITLE = "7 знаменитых некрополей и кладбищ"
    elif guide == "landmarks":
        from data.landmarks import LANDMARKS, IMAGES_SUBFOLDER as _SUB
        from data.landmarks_image_urls import (
            LANDMARK_IMAGE_DOWNLOADS,
            LANDMARK_IMAGE_FALLBACKS,
        )
        from data.qa_landmarks import QA as _QA
        IMAGES_SUBFOLDER = _SUB
        PLACES = LANDMARKS
        IMAGE_DOWNLOADS = LANDMARK_IMAGE_DOWNLOADS
        IMAGE_FALLBACKS = LANDMARK_IMAGE_FALLBACKS
        QA = _QA
        BANNED = frozenset()
        HTML_NAME = "landmarks_guide.html"
        PDF_NAME = "landmarks_guide.pdf"
        INTRO_TITLE = "Iconic landmarks Москвы"
        INTRO_SUBTITLE = "10 символов города: Москва-Сити, Лужники, Василий Блаженный"
    elif guide == "cafes":
        from data.cafes import CAFES, IMAGES_SUBFOLDER as _SUB
        from data.cafe_image_urls import (
            CAFE_IMAGE_DOWNLOADS,
            CAFE_IMAGE_FALLBACKS,
        )
        from data.qa_cafes import QA as _QA
        IMAGES_SUBFOLDER = _SUB
        PLACES = CAFES
        IMAGE_DOWNLOADS = CAFE_IMAGE_DOWNLOADS
        IMAGE_FALLBACKS = CAFE_IMAGE_FALLBACKS
        QA = _QA
        BANNED = frozenset()
        HTML_NAME = "cafes_guide.html"
        PDF_NAME = "cafes_guide.pdf"
        INTRO_TITLE = "Исторические кафе Москвы"
        INTRO_SUBTITLE = "6 легендарных кафе и ресторанов"
    elif guide == "test_e2e":
        from data.test_e2e_guide import TEST_E2E_PLACES, IMAGES_SUBFOLDER as _SUB
        from data.test_e2e_image_urls import (
            TEST_E2E_IMAGE_DOWNLOADS,
            TEST_E2E_IMAGE_FALLBACKS,
        )
        from data.qa_test_e2e import QA as _QA
        IMAGES_SUBFOLDER = _SUB
        PLACES = TEST_E2E_PLACES
        IMAGE_DOWNLOADS = TEST_E2E_IMAGE_DOWNLOADS
        IMAGE_FALLBACKS = TEST_E2E_IMAGE_FALLBACKS
        QA = _QA
        BANNED = frozenset()
        HTML_NAME = "test_e2e_guide.html"
        PDF_NAME = "test_e2e_guide.pdf"
        INTRO_TITLE = "E2E Test Guide"
        INTRO_SUBTITLE = "5 test places"
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
    """URL статической карты (Яндекс) по координатам объекта с маркером в этой точке."""
    return (
        "https://static-maps.yandex.ru/1.x/?ll={lon:.4f},{lat:.4f}&z=16&l=map"
        "&size={w},{h}&pt={lon:.4f},{lat:.4f},pm2rdm".format(
            lon=lon, lat=lat, w=width, h=height
        )
    )


def _escape(s: str) -> str:
    """Экранирование HTML."""
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _wrap_ya_old_russian(s: str) -> str:
    """
    Оборачивает буквы «я» и «Я» в span (Source Serif 4); остальной заголовок — Pochaevsk.
    Ожидает уже экранированную для HTML строку.
    """
    return s.replace(
        "Я", '<span class="old-russian-ya">Я</span>'
    ).replace("я", '<span class="old-russian-ya">я</span>')


def _title_html(raw_title: str) -> str:
    """Заголовок с буквами я/Я в старорусском шрифте."""
    return _wrap_ya_old_russian(_escape(raw_title))


def _file_hash(path: Path) -> str:
    """
    Content-based hash for deduplication (perceptual hash if available,
    else SHA256). Same image at different resolution = same hash when
    using perceptual hash.
    """
    return image_content_hash(path, min_bytes=MIN_IMAGE_BYTES)


def download_images(
    output_dir: Path,
    guide_name: str = "guide",
    build_with_available: bool = False,
    use_ai_identify: bool = False,
    force_overwrite: bool = False,
    stats_out: Optional[dict] = None,
) -> None:
    """
    Скачивает фотографии в output/images/<IMAGES_SUBFOLDER>/ с проверкой
    дубликатов. Если build_with_available=False, требует 4 различных
    изображения на объект.
    """
    from scripts.download_with_dedup import (
        download_images_with_dedup,
        validate_item_images_format,
    )

    images_dir = output_dir / "images" / IMAGES_SUBFOLDER
    images_dir.mkdir(parents=True, exist_ok=True)

    print("Downloading images with duplicate checking...")
    images_root = output_dir / "images"
    results, stats = download_images_with_dedup(
        images_dir=images_dir,
        image_downloads=IMAGE_DOWNLOADS,
        image_fallbacks=IMAGE_FALLBACKS,
        banned=BANNED,
        items=PLACES,
        max_attempts_per_item=20,
        images_root=images_root,
        use_ai_identify=use_ai_identify,
        guide_name=guide_name,
        force_overwrite=force_overwrite,
    )
    if stats_out is not None:
        for k, v in stats.items():
            stats_out[k] = stats_out.get(k, 0) + v

    print("\nValidating image format (4 distinct per item)...")
    is_valid, errors = validate_item_images_format(
        PLACES, images_dir, guide_name=guide_name,
    )
    if not is_valid:
        for e in errors:
            print("  ", e, file=sys.stderr)
        if build_with_available:
            print(
                "\nBuilding with available images (some items have < 4 images).",
                file=sys.stderr,
            )
            return
        print(
            "\nEach item must have exactly 4 distinct images in format: "
            "name_1.jpg, name_2.jpg, name_3.jpg, name_4.jpg",
            file=sys.stderr,
        )
        raise ValueError("Image validation failed: not all items have 4 distinct images")

    print("OK: All items have 4 distinct images in correct format.")


def ensure_images_subdir(output_dir: Path) -> Path:
    """Создаёт output/images и output/images/<IMAGES_SUBFOLDER> при отсутствии."""
    images_dir = output_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    subdir = images_dir / IMAGES_SUBFOLDER
    subdir.mkdir(parents=True, exist_ok=True)
    return subdir


def check_duplicate_images(images_dir: Path) -> list[tuple[str, list[str]]]:
    """
    Проверяет дубликаты по содержимому (perceptual hash или SHA256).
    Одинаковое изображение в разном разрешении считается дубликатом.
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
    image_rels: list[str],
    output_dir: Path,
    max_images: int | None = None,
) -> list[str]:
    """Return up to max_images (default IMAGES_PER_PLACE) unique image paths.
    Skip by hash: if file hash matches forbidden/ folder, exclude."""
    from scripts.download_with_dedup import _load_forbidden_hashes
    limit = max_images if max_images is not None else IMAGES_PER_PLACE
    forbidden_hashes = _load_forbidden_hashes(
        output_dir / "images" / IMAGES_SUBFOLDER,
    )
    seen_hashes: set[str] = set()
    result: list[str] = []
    for img_rel in image_rels:
        if len(result) >= limit:
            break
        path = output_dir / img_rel
        if not path.exists() or not path.is_file():
            continue
        if path.stat().st_size < MIN_IMAGE_BYTES:
            continue
        h = _file_hash(path)
        if not h or h in seen_hashes:
            continue
        if h in forbidden_hashes:
            continue
        seen_hashes.add(h)
        result.append(img_rel)
    return result


def get_used_image_basenames(output_dir: Path) -> set[str]:
    """Имена файлов изображений, реально используемых в путеводителе."""
    used: set[str] = set()
    for place in PLACES:
        rels = _unique_images_for_place(place["images"], output_dir)
        if len(rels) < MIN_IMAGES_TO_BUILD:
            continue
        for r in rels:
            basename = r.split("/")[-1] if "/" in r else r
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


# Script for editable HTML: contenteditable, image delete/upload (max 4 per item), export
# Deleted image paths (relative, e.g. images/moscow_monasteries/foo.jpg) are stored
# and embedded on export so next build can move them to forbidden/
_EDITABLE_SCRIPT = """
(function(){
  var MAX_IMAGES_PER_ROW = 4;
  window._deletedImagePaths = window._deletedImagePaths || [];
  function recordDeleted(src) {
    if (typeof src !== 'string') return;
    var s = src.split('?')[0].replace(/\\\\/g, '/');
    var idx = s.indexOf('images/');
    if (idx === 0) window._deletedImagePaths.push(s);
    else if (idx > 0) window._deletedImagePaths.push(s.substring(idx));
  }
  function initEditable() {
    var sel = '.intro-block p,.intro-block h1,.monastery .monastery-title,.monastery .meta,' +
      '.monastery .body-text,.monastery .story-text,.qa-section p,.qa-section h2,' +
      '.monastery ul li';
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
        delBtn.onclick = function(){ recordDeleted(img.src); wrap.remove(); updateAddBtn(row); };
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
    if (countSpan) { countSpan.textContent = n + ' из 4'; }
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
      var deleted = window._deletedImagePaths || [];
      if (deleted.length) {
        var script = root.ownerDocument.createElement('script');
        script.type = 'application/json';
        script.id = 'otium-deleted-images';
        script.textContent = JSON.stringify(deleted);
        root.querySelector('body').appendChild(script);
      }
      var html = '<!DOCTYPE html>\\n' + root.outerHTML;
      var blob = new Blob([html], { type: 'text/html;charset=utf-8' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = document.title.replace(/[^a-z0-9]/gi, '_') + '.html';
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


def _section_place(
    number: int,
    m: dict,
    output_dir: Path,
    story: str | None = None,
    images_max: int | None = None,
) -> str:
    """HTML block for one place: photos + map. If images_max=3, use 2x2 grid."""
    name = _title_html(m["name"])
    name_alt = _escape(m["name"])
    address = _escape(m["address"])
    style = _escape(m["style"])
    history = _escape(m["history"])
    significance = _escape(m["significance"])
    map_url = _map_img_url(m["lon"], m["lat"])

    highlights_html = "".join(
        "<li>{}</li>".format(_escape(h)) for h in m["highlights"]
    )
    facts_html = "".join("<li>{}</li>".format(_escape(f)) for f in m["facts"])

    limit = images_max if images_max is not None else IMAGES_PER_PLACE
    unique_rels = _unique_images_for_place(
        m["images"], output_dir, max_images=limit
    )
    if not unique_rels:
        images_block = ""
    elif images_max == OPT_IMAGES_PER_PLACE:
        # 2x2 grid: row1 = img1, img2; row2 = img3, map
        cells = []
        for i, img_rel in enumerate(unique_rels):
            cells.append(
                '    <img src="{}" alt="{} — фото {}" class="monastery-img" />'
                .format(
                    img_rel.replace("\\", "/"), name_alt, i + 1,
                )
            )
        cells.append(
            '    <div class="map-cell">'
            '<img src="{}" alt="Карта: {}" class="map-img" />'
            '<p class="map-caption">Схема · Яндекс.Карты</p></div>'
            .format(map_url, name_alt)
        )
        images_block = (
            '  <div class="visual-grid-2x2">\n{}\n  </div>\n'
            '  <p class="images-caption">Фото: {}</p>'
        ).format("\n".join(cells), name_alt)
    else:
        imgs_html_parts = [
            '<img src="{}" alt="{} — фото {}" class="monastery-img" />'.format(
                img_rel.replace("\\", "/"), name_alt, i + 1,
            )
            for i, img_rel in enumerate(unique_rels)
        ]
        imgs_html = "\n".join(imgs_html_parts)
        images_block = (
            "  <div class=\"images-row\">\n    {}\n  </div>\n"
            "  <p class=\"images-caption\">Фото: {}</p>"
        ).format(imgs_html, name_alt)
    title_class = "monastery-title"

    story_block = ""
    if story and story.strip():
        story_block = (
            '  <p class="block-label">Заметка</p>\n'
            '  <p class="body-text story-text">{}</p>\n'
        ).format(_escape(story.strip()))

    if images_max == OPT_IMAGES_PER_PLACE:
        visual_inner = images_block
    else:
        visual_inner = (
            "{images_block}\n"
            "  <div class=\"map-block\">\n"
            "    <img src=\"{map_url}\" alt=\"Карта: {name_alt}\" "
            "class=\"map-img\" />\n"
            "    <p class=\"map-caption\">Схема расположения · "
            "Яндекс.Карты</p>\n  </div>"
        ).format(
            images_block=images_block,
            map_url=map_url, name_alt=name_alt,
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
{story_block}
  <div class="visual-block">
{visual_inner}
  </div>
</section>
""".format(
        num=number,
        name=name,
        name_alt=name_alt,
        title_class=title_class,
        address=address,
        style=style,
        visual_inner=visual_inner,
        history=history,
        significance=significance,
        highlights_html=highlights_html,
        facts_html=facts_html,
        story_block=story_block,
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


def build_html(
    output_dir: Path,
    guide_name: str | None = None,
    editable: bool = False,
    optimized: bool = False,
) -> str:
    """Build full HTML (~1 page per place). guide_name for stories.
    editable=True adds edit script. optimized=True: only places with >=1 image,
    3 images + map in 2x2 grid, smaller output."""
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
      .old-russian-ya { font-family: "Source Serif 4", Georgia, serif; }
      .meta, .block-label { font-family: Inter, "IBM Plex Sans", sans-serif;
          font-size: 8.5pt; letter-spacing: 0.02em; }
      .meta { margin: 0.2em 0 0.6em 0.3em; color: #6b635b !important; }
      .block-label { margin: 0.6em 0 0.15em 0.3em; text-transform: uppercase;
                     font-weight: 600; color: #6b7b8a !important; }
      .body-text { margin: 0 0 0.4em 0.3em; text-align: left; max-width: 42em;
                   color: #1c1b19; font-family: "Source Serif 4", Georgia, serif; }
      .story-text { font-style: italic; color: #4a5568; }
      ul, li, p { color: #1c1b19; font-family: "Source Serif 4", Georgia, serif; }
      .intro-block { page-break-after: always; padding: 2.5em 1em 0 1.2em;
                     background-color: #faf8f5; }
      .intro-block .otium-brand { font-family: Inter, sans-serif;
        font-size: 8pt; letter-spacing: 0.2em; color: #6b635b !important;
        margin-bottom: 0.3em; }
      .intro-block .otium-title { font-family: Pochaevsk, Georgia, serif;
        font-size: 20pt; font-weight: 600; text-align: center;
        margin: 0.2em 0 0.1em; color: #1a1a1a !important; }
      .intro-block .otium-subtitle { font-family: Pochaevsk, Georgia, serif;
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
      .visual-grid-2x2 { display: grid; grid-template-columns: 1fr 1fr;
        grid-template-rows: auto auto; gap: 10px; margin: 1em; }
      .visual-grid-2x2 .monastery-img,
      .visual-grid-2x2 .map-cell .map-img { width: 100%; height: 150px;
        object-fit: cover; }
      .visual-grid-2x2 .map-cell { display: flex; flex-direction: column; }
      .visual-grid-2x2 .map-cell .map-img { max-height: 160px; height: auto; }
      .visual-grid-2x2 .map-caption { font-size: 8pt; color: #6b635b;
        margin: 0.25em 0 0; font-family: Inter, sans-serif; }
      .images-caption { font-size: 8pt; color: #6b635b; margin: 0.25em 1em 0;
        font-family: Inter, sans-serif; }
      .map-block { margin: 1em; }
      .map-caption { font-size: 8pt; color: #6b635b; margin: 0.25em 0 0;
        font-family: Inter, sans-serif; }
      .map-img { max-width: 100%; height: auto; max-height: 160px; }
      .qa-section { margin-top: 2em; page-break-before: always;
                     break-before: page; padding-top: 1.5em; }
      .qa-item { margin-bottom: 0.6em; font-size: 9pt; color: #1c1b19; }
      .question { margin-bottom: 0.1em; color: #1c1b19; }
      .answer { margin-left: 0.5em; color: #2c2a28;
        font-family: "Source Serif 4", Georgia, serif; }
      ul { margin: 0.2em 0 0.4em 0.3em; padding-left: 1.2em; color: #1c1b19; }
      p { margin: 0.2em 0; color: #1c1b19; }
      .map-block { background: transparent; }
      .edit-toolbar { position: fixed; top: 8px; right: 8px; z-index: 9999; }
      .edit-toolbar button { font-family: Inter, sans-serif; font-size: 11px;
        padding: 6px 10px; background: #2c2a28; color: #faf8f5; border: none;
        border-radius: 4px; cursor: pointer; }
      .edit-toolbar button:hover { background: #4a5568; }
      .img-wrap { position: relative; display: inline-block; }
      .img-wrap.img-dragging { opacity: 0.6; }
      .img-wrap.img-drop-target { outline: 2px dashed #8b7355; outline-offset: 2px; }
      .img-del { position: absolute; top: 4px; right: 4px; width: 22px; height: 22px;
        font-size: 16px; line-height: 20px; text-align: center; background: rgba(0,0,0,.6);
        color: #fff; border: none; border-radius: 3px; cursor: pointer; }
      .img-del:hover { background: #c53030; }
      .add-img-btn { font-family: Inter, sans-serif; font-size: 10px;
        padding: 4px 8px; margin: 4px 0 0 4px; background: #e0ddd8; color: #2c2a28;
        border: 1px solid #8b7355; border-radius: 3px; cursor: pointer; }
      .add-img-btn:hover { background: #d0cdc8; }
      .add-img-btn.hidden { display: none; }
      .img-count { font-size: 9pt; color: #6b635b; margin-left: 0.25em;
        font-family: Inter, sans-serif; }
      @media print {
        html, body { color: #1c1b19 !important; background: #faf8f5 !important; }
        .block-label { color: #6b7b8a !important; }
        .meta { color: #6b635b !important; }
        .monastery { page-break-before: always; break-before: page; }
        .monastery:first-of-type { page-break-before: auto; break-before: auto; }
        .edit-toolbar, .img-del, .add-img-btn, .img-count { display: none !important; }
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
        intro_title=_title_html(INTRO_TITLE),
        intro_subtitle=_title_html(INTRO_SUBTITLE),
    )
    stories: dict[str, str] = {}
    if guide_name:
        try:
            from scripts.guide_loader import load_stories
            stories = load_stories(guide_name)
        except Exception:
            pass
    sections = [intro]
    if optimized:
        placed = [
            m for m in PLACES
            if len(_unique_images_for_place(
                m["images"], output_dir,
                max_images=OPT_IMAGES_PER_PLACE,
            )) >= MIN_IMAGES_OPT
        ]
        images_max = OPT_IMAGES_PER_PLACE
    else:
        placed = list(PLACES)
        images_max = None
    for num, m in enumerate(placed, 1):
        story = stories.get(m.get("name") or "")
        sections.append(
            _section_place(
                num, m, output_dir,
                story=story,
                images_max=images_max,
            )
        )
    sections.append(_section_qa())

    body_content = "\n".join(sections)
    if editable:
        body_content = (
            body_content + "\n<script>\n" + _EDITABLE_SCRIPT.strip() + "\n</script>"
        )

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
        body=body_content,
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


# Patterns that indicate placeholder Q&A; validation must fail if present.
_QA_PLACEHOLDER_QUESTION = "Дополнительный вопрос"
_QA_PLACEHOLDER_ANSWER = "См. описание объектов в гиде."


def validate_output(html_path: Path, output_dir: Path) -> list[str]:
    """Проверяет HTML на битые ссылки и плейсхолдеры. Возвращает список ошибок."""
    errors: list[str] = []
    html = html_path.read_text(encoding="utf-8")

    if _QA_PLACEHOLDER_QUESTION in html:
        errors.append(
            "QA placeholder found (question): '{}'".format(
                _QA_PLACEHOLDER_QUESTION
            )
        )
    if _QA_PLACEHOLDER_ANSWER in html:
        errors.append(
            "QA placeholder found (answer): '{}'".format(
                _QA_PLACEHOLDER_ANSWER
            )
        )

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


def _pdf_via_playwright(
    html_path: Path,
    pdf_path: Path,
    image_wait_timeout_ms: int = 15000,
    display_header_footer: bool = False,
    footer_template: Optional[str] = None,
    header_template: Optional[str] = None,
) -> bool:
    """
    Генерирует PDF из HTML через Playwright.
    Отдаёт страницу по HTTP, чтобы Google Fonts загружались; ждёт шрифты.
    image_wait_timeout_ms: таймаут ожидания загрузки всех изображений (для
    больших документов увеличьте, например 60000).
    display_header_footer: если True и задан footer_template, добавляет футер
    с номерами страниц (Playwright подставляет pageNumber и totalPages).
    header_template: если задан, подставляет шапку (убирает дату/время по умол.).
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
            # Wait for images to load; on timeout still generate PDF (best-effort)
            try:
                page.wait_for_function(
                    "() => { const imgs = document.querySelectorAll('img'); "
                    "return imgs.length === 0 || Array.from(imgs).every("
                    "i => i.complete && i.naturalWidth > 0); }",
                    timeout=image_wait_timeout_ms,
                )
            except Exception:
                print(
                    "  Note: some images may still be loading; generating PDF.",
                    file=sys.stderr,
                )
            page.wait_for_timeout(500)
            # Use screen media so background colors and images are not stripped
            page.emulate_media(media="screen")
            margin = {
                "top": "1.2cm", "right": "1.2cm",
                "bottom": "1.5cm" if display_header_footer else "1.2cm",
                "left": "1.2cm",
            }
            pdf_options = {
                "path": str(pdf_path),
                "format": "A4",
                "margin": margin,
                "print_background": True,
            }
            if display_header_footer and footer_template:
                pdf_options["display_header_footer"] = True
                pdf_options["footer_template"] = footer_template
                if header_template is not None:
                    pdf_options["header_template"] = header_template
            page.pdf(**pdf_options)
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


def _print_download_stats(stats: dict) -> None:
    """Print running total: downloaded, banned, dups, no URLs, etc."""
    parts = [str(stats.get("downloaded", 0)) + " downloaded"]
    for k, label in [
        ("banned", "banned"), ("moved", "moved"), ("dups", "dups"),
        ("no_urls", "no URLs"), ("network", "network"), ("timeout", "timeout"),
        ("forbidden", "forbidden"), ("ai_reject", "AI reject"),
        ("too_small", "too small"), ("non_image", "non-image"),
        ("other", "other"),
    ]:
        n = stats.get(k, 0)
        if n > 0:
            parts.append("{} {}".format(n, label))
    if len(parts) > 1:
        print("\n--- Running total ({}): ---".format(
            __import__("time").strftime("%H:%M:%S"),
        ))
        print("  {}".format(", ".join(parts)))


def _all_images_complete(images_subdir: Path, guide_name: str) -> bool:
    """Check if all items have all 4 images downloaded."""
    from scripts.download_with_dedup import validate_item_images_format
    is_valid, errors = validate_item_images_format(
        PLACES, images_subdir, guide_name=guide_name,
    )
    return is_valid and len(errors) == 0


# Script id embedded by editable export; images listed here are moved to forbidden/
OTIUM_DELETED_IMAGES_ID = "otium-deleted-images"


def _inject_editable_script_before_body_close(html: str) -> str:
    """Insert editable script before </body>. Idempotent (single insertion)."""
    marker = "</body>"
    if "_EDITABLE_SCRIPT" in html or "initEditable" in html:
        return html
    script_tag = "\n<script>\n" + _EDITABLE_SCRIPT.strip() + "\n</script>\n"
    if marker in html:
        return html.replace(marker, script_tag + marker, 1)
    return html


def _process_deleted_images_and_strip_script(
    html_content: str,
    output_dir: Path,
) -> tuple[str, int]:
    """
    If HTML contains otium-deleted-images script, move those image files to
    forbidden/ so they won't be re-downloaded. Return (cleaned_html, moved_count).
    """
    pattern = re.compile(
        r'<script[^>]*\s+id="' + re.escape(OTIUM_DELETED_IMAGES_ID) + r'"[^>]*>'
        r'([^<]*)</script>',
        re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(html_content)
    if not match:
        return html_content, 0
    try:
        paths = json.loads(match.group(1).strip())
    except (json.JSONDecodeError, ValueError):
        return html_content, 0
    if not isinstance(paths, list):
        return html_content, 0
    moved = 0
    for rel_path in paths:
        if not isinstance(rel_path, str) or ".." in rel_path:
            continue
        if not rel_path.replace("\\", "/").startswith("images/"):
            continue
        src = output_dir / rel_path.replace("\\", "/")
        if not src.is_file():
            continue
        # Move to same directory's forbidden/ subdir
        forbidden_dir = src.parent / "forbidden"
        forbidden_dir.mkdir(parents=True, exist_ok=True)
        dest = forbidden_dir / src.name
        try:
            shutil.copy2(str(src), str(dest))
            src.unlink()
            moved += 1
        except OSError:
            pass
    cleaned = pattern.sub("", html_content)
    return cleaned, moved


def _run_one_guide(args, stats_out: Optional[dict] = None) -> None:
    """Run download, verify, and build for one guide (args.guide)."""
    global HTML_NAME, PDF_NAME
    _load_guide_config(args.guide)
    if getattr(args, "optimized", False):
        HTML_NAME = HTML_NAME.replace("_guide.html", "_guide_opt.html")
        PDF_NAME = PDF_NAME.replace("_guide.pdf", "_guide_opt.pdf")
    output_dir = (
        Path(args.output_dir)
        if getattr(args, "output_dir", None)
        else _project_root / "output"
    )
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

    verify_only = getattr(args, "verify_images", False) and not getattr(
        args, "download_only", False,
    )
    if verify_only:
        from scripts.download_with_dedup import (
            validate_item_images_format,
        )
        print("Verifying images (forbidden folder checked)...")
        is_valid, errors = validate_item_images_format(
            PLACES, images_subdir, guide_name=args.guide,
        )
        if not is_valid:
            for e in errors:
                print("  ", e, file=sys.stderr)
        else:
            print("  Format OK: 4 distinct images per item.")
        print("Checking for duplicate images...")
        duplicates = check_duplicate_images(images_subdir)
        if duplicates:
            for h, files in duplicates:
                print("  Duplicate ({}): {}".format(h[:12], ", ".join(files)))
        else:
            print("  No duplicate images by content.")
        return

    if not getattr(args, "build_only", False):
        if not getattr(args, "verify_images", False):
            print("Downloading images with duplicate checking...")
        else:
            print("Downloading/verifying images (existing slots verified only)...")
        try:
            download_images(
                output_dir,
                guide_name=args.guide,
                build_with_available=getattr(args, "build_with_available", False),
                use_ai_identify=getattr(args, "ai_identify", True),
                force_overwrite=getattr(args, "force_overwrite", False),
                stats_out=stats_out,
            )
        except ValueError as e:
            print("Error: {}".format(e), file=sys.stderr)
            if not getattr(args, "build_with_available", False):
                print(
                    "Cannot proceed to PDF generation: not all items have 4 distinct "
                    "images. Use --build-with-available to build with current images.",
                    file=sys.stderr,
                )
            if getattr(args, "all_guides", False):
                raise  # Caller catches and continues to next guide
            if getattr(args, "download_only", False):
                return  # With download-only, no PDF to build; exit normally
            sys.exit(1)

        print("Checking for any remaining duplicate images...")
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

    if getattr(args, "download_only", False):
        return

    # HTML_NAME/PDF_NAME already set to *_opt.* when --optimized
    html_path = output_dir / HTML_NAME
    pdf_path = output_dir / PDF_NAME
    edit_name = Path(HTML_NAME).stem + "_edit.html"
    edit_path = output_dir / edit_name

    # If user saved exported HTML as *_edit.html, process it: move deleted images
    # to forbidden/ and use edited content for guide/PDF. Keep edit file editable.
    if edit_path.exists():
        edit_content = edit_path.read_text(encoding="utf-8")
        cleaned, moved = _process_deleted_images_and_strip_script(
            edit_content, output_dir,
        )
        if moved > 0:
            print("Moved {} deleted image(s) to forbidden/.".format(moved))
        if cleaned != edit_content or moved > 0:
            html_path.write_text(cleaned, encoding="utf-8")
            edit_path.write_text(
                _inject_editable_script_before_body_close(cleaned),
                encoding="utf-8",
            )
            print("Using edited content from {} for PDF.".format(edit_path.name))
    else:
        opt = getattr(args, "optimized", False)
        html_content = build_html(
            output_dir,
            guide_name=args.guide,
            editable=False,
            optimized=opt,
        )
        html_path.write_text(html_content, encoding="utf-8")
        edit_content = build_html(
            output_dir,
            guide_name=args.guide,
            editable=True,
            optimized=opt,
        )
        edit_path.write_text(edit_content, encoding="utf-8")
        print("Written:", edit_path)

    # If guide HTML (not edit) was overwritten with exported HTML, process it too
    current = html_path.read_text(encoding="utf-8")
    cleaned, moved = _process_deleted_images_and_strip_script(current, output_dir)
    if moved > 0:
        print("Moved {} deleted image(s) to forbidden/.".format(moved))
        html_path.write_text(cleaned, encoding="utf-8")
    elif cleaned != current:
        html_path.write_text(cleaned, encoding="utf-8")

    if _pdf_via_playwright(html_path, pdf_path):
        _strip_pdf_metadata(pdf_path)
        print("Written:", pdf_path)
    else:
        print(
            "PDF: install playwright and run 'playwright install chromium'.",
            file=sys.stderr,
        )
    print("Written:", html_path)
    # Do not delete any existing images automatically. We still compute which
    # images are used for validation, but keep extra files in place so that
    # the user can move bad ones into the forbidden/ folder manually.
    # deleted = delete_unused_images(output_dir)
    # if deleted:
    #     print("Removed {} unused image(s).".format(deleted))
    errors = validate_output(html_path, output_dir)
    if errors:
        print("Validation:", file=sys.stderr)
        for e in errors:
            print("  -", e, file=sys.stderr)
    else:
        print("Validation: no broken links or placeholders found.")


def _ensure_utf8_console() -> None:
    """Use UTF-8 for stdout/stderr so Cyrillic prints correctly on Windows."""
    if sys.platform != "win32":
        return
    for name, stream in [("stdout", sys.stdout), ("stderr", sys.stderr)]:
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8")
                continue
            except (AttributeError, OSError):
                pass
        if hasattr(stream, "buffer"):
            try:
                wrapper = io.TextIOWrapper(
                    stream.buffer, encoding="utf-8", errors="replace",
                )
                setattr(sys, name, wrapper)
            except (AttributeError, OSError):
                pass


def main() -> None:
    """Создаёт подкаталог, скачивает фото, проверяет дубликаты, генерирует PDF."""
    _ensure_utf8_console()
    try:
        from dotenv import load_dotenv
        load_dotenv(_project_root / ".env")
    except ImportError:
        pass
    import argparse
    parser = argparse.ArgumentParser(description="Build PDF guide (monasteries or churches)")
    parser.add_argument(
        "--guide",
        choices=[
            "monasteries", "places_of_worship", "parks", "museums", "palaces",
            "buildings", "sculptures", "places", "squares", "metro",
            "theaters", "viewpoints", "bridges", "markets",
            "libraries", "railway_stations", "cemeteries", "landmarks", "cafes",
            "test_e2e",
        ],
        default="monasteries",
        help="Guide name (test_e2e for E2E tests).",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        metavar="DIR",
        help="Output directory (default: output/).",
    )
    parser.add_argument(
        "--download-only",
        action="store_true",
        help="Only download images and validate maps; do not write HTML/PDF.",
    )
    parser.add_argument(
        "--build-only",
        action="store_true",
        help="Skip image download; only generate HTML/PDF from existing images.",
    )
    parser.add_argument(
        "--build-with-available",
        action="store_true",
        help="Generate PDF/HTML from currently available images (allow < 4 per item).",
    )
    parser.add_argument(
        "--no-ai-identify",
        action="store_true",
        help="Disable AI image identification (enabled by default).",
    )
    parser.add_argument(
        "--verify-images",
        action="store_true",
        help="Verify all images (duplicate check + format). With --download-only: "
             "download then verify. Alone: verify only, no download/build.",
    )
    parser.add_argument(
        "--all-guides",
        action="store_true",
        help="Run for all guides (use with --build-with-available to build all).",
    )
    parser.add_argument(
        "--force-overwrite",
        action="store_true",
        help="Overwrite existing images (default: do not overwrite).",
    )
    parser.add_argument(
        "--optimized",
        action="store_true",
        help="Build optimized guide: only places with >=1 image, 3 photos + map "
             "(2x2 grid), output *_guide_opt.html / *_guide_opt.pdf.",
    )
    parser.add_argument(
        "--download-retries",
        type=int,
        default=1,
        metavar="N",
        help="With --all-guides: try downloading missing images N times before "
             "building (default 2).",
    )
    args = parser.parse_args()
    args.ai_identify = not getattr(args, "no_ai_identify", False)

    BUILD_GUIDES = [
        "monasteries", "places_of_worship", "parks", "museums", "palaces",
        "buildings", "sculptures", "places", "squares", "metro", "theaters",
        "viewpoints", "bridges", "markets", "libraries", "railway_stations",
        "cemeteries", "landmarks", "cafes",
    ]

    if getattr(args, "all_guides", False):
        args.build_with_available = True
        user_build_only = getattr(args, "build_only", False)

        if user_build_only:
            # Build only: one pass per guide, no download rounds.
            for g in BUILD_GUIDES:
                args.guide = g
                print("\n" + "=" * 60)
                print("Guide: {} (build only)".format(g))
                print("=" * 60)
                try:
                    _run_one_guide(args)
                except ValueError as e:
                    print("  Skipped: {}".format(e), file=sys.stderr)
            print("\nAll guides built.")
            return

        # For --all-guides with download: default to 2 rounds.
        argv = sys.argv[1:]
        user_set_retries = any(
            a == "--download-retries" or a.startswith("--download-retries=")
            for a in argv
        )
        if not user_set_retries:
            args.download_retries = 2
        retries = max(1, getattr(args, "download_retries", 1))
        user_download_only = getattr(args, "download_only", False)

        cumulative_stats = {
            "downloaded": 0, "banned": 0, "moved": 0, "dups": 0,
            "no_urls": 0, "network": 0, "timeout": 0, "forbidden": 0,
            "ai_reject": 0, "too_small": 0, "non_image": 0, "other": 0,
        }
        stats_done = threading.Event()

        def _stats_timer() -> None:
            while not stats_done.wait(timeout=300):
                _print_download_stats(cumulative_stats)

        timer = threading.Thread(target=_stats_timer, daemon=True)
        timer.start()

        for g in BUILD_GUIDES:
            args.guide = g
            _load_guide_config(g)
            output_dir = (
                Path(args.output_dir)
                if getattr(args, "output_dir", None)
                else _project_root / "output"
            )
            images_subdir = ensure_images_subdir(output_dir)
            
            # Check if all images already downloaded - skip rounds if complete
            if _all_images_complete(images_subdir, g):
                print("\n=== Guide: {} (all images complete, skipping download rounds) ===".format(g))
                args.download_only = user_download_only
                print("\n" + "=" * 60)
                print("Guide: {} — build only (all images present)".format(g))
                print("=" * 60)
                try:
                    _run_one_guide(args, stats_out=cumulative_stats)
                except ValueError as e:
                    print("  Skipped: {}".format(e), file=sys.stderr)
                continue
            
            if retries > 1:
                print("\n=== Guide: {} (download rounds: {}) ===".format(g, retries))

            for round_one in range(1, retries):
                args.download_only = True
                print("\n" + "=" * 60)
                print("Guide: {} — download round {}/{}".format(g, round_one, retries))
                print("=" * 60)
                try:
                    _run_one_guide(args, stats_out=cumulative_stats)
                except ValueError as e:
                    print("  Skipped: {}".format(e), file=sys.stderr)
                # Check after round completes - if all images complete, skip remaining rounds
                if _all_images_complete(images_subdir, g):
                    print("\n  All images complete after round {}, skipping remaining rounds".format(round_one))
                    break

            # Final round: check again before building
            if not _all_images_complete(images_subdir, g):
                args.download_only = user_download_only
                print("\n" + "=" * 60)
                print("Guide: {} — final round".format(g))
                print("=" * 60)
                try:
                    _run_one_guide(args, stats_out=cumulative_stats)
                except ValueError as e:
                    print("  Skipped: {}".format(e), file=sys.stderr)
            else:
                # All complete, just build
                args.download_only = user_download_only
                print("\n" + "=" * 60)
                print("Guide: {} — build only (all images complete)".format(g))
                print("=" * 60)
                try:
                    _run_one_guide(args, stats_out=cumulative_stats)
                except ValueError as e:
                    print("  Skipped: {}".format(e), file=sys.stderr)

        stats_done.set()
        print("\n" + "=" * 60)
        print("Process finished. Final stats:")
        _print_download_stats(cumulative_stats)
        print("=" * 60)
        return

    _run_one_guide(args)


if __name__ == "__main__":
    main()
