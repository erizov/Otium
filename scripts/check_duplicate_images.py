    # -*- coding: utf-8 -*-
"""Проверка: один и тот же URL изображения не используется для двух разных объектов.

Запуск: python scripts/check_duplicate_images.py
Правило: один URL — только для одного объекта во всех гидах (и один ключ в одном гиде).
"""

from __future__ import annotations

import os
import sys
from collections import defaultdict

# Корень проекта для импорта data.*
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_SCRIPT_DIR)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


def _normalize_url(url: str) -> str:
    """Нормализация URL для сравнения (один и тот же файл)."""
    return url.strip().rstrip("/")


def _load_all_downloads() -> dict[str, list[tuple[str, str]]]:
    """Загружает все DOWNLOADS из *image_urls.py; возвращает url -> [(guide, key), ...]."""
    url_to_sources: dict[str, list[tuple[str, str]]] = defaultdict(list)

    configs = [
        ("place", "data.place_image_urls", "PLACE_IMAGE_DOWNLOADS"),
        ("park", "data.park_image_urls", "PARK_IMAGE_DOWNLOADS"),
        ("metro", "data.metro_image_urls", "METRO_IMAGE_DOWNLOADS"),
        ("places_of_worship", "data.places_of_worship_image_urls", "PLACES_OF_WORSHIP_IMAGE_DOWNLOADS"),
        ("building", "data.building_image_urls", "BUILDING_IMAGE_DOWNLOADS"),
        ("palace", "data.palace_image_urls", "PALACE_IMAGE_DOWNLOADS"),
        ("museum", "data.museum_image_urls", "MUSEUM_IMAGE_DOWNLOADS"),
        ("sculpture", "data.sculpture_image_urls", "SCULPTURE_IMAGE_DOWNLOADS"),
        ("monastery", "data.image_urls", "IMAGE_DOWNLOADS"),
    ]

    for guide, module_name, attr in configs:
        try:
            mod = __import__(module_name, fromlist=[attr])
            downloads = getattr(mod, attr, None)
        except Exception as e:
            print("Warning: could not load {}: {}".format(module_name, e), file=sys.stderr)
            continue
        if not isinstance(downloads, dict):
            continue
        for key, url in downloads.items():
            if isinstance(url, str):
                norm = _normalize_url(url)
                url_to_sources[norm].append((guide, key))

    return dict(url_to_sources)


def main() -> int:
    """Проверяет дубликаты URL по всем гидам; возвращает 0 при отсутствии дубликатов."""
    url_to_sources = _load_all_downloads()
    duplicates: list[tuple[str, list[tuple[str, str]]]] = []
    for url, sources in url_to_sources.items():
        if len(sources) > 1:
            # Один и тот же URL для нескольких (guide, key) — запрещено
            duplicates.append((url, sources))

    if not duplicates:
        print("OK: no duplicate image URLs across guides.")
        return 0

    print("ERROR: the same image URL must not be used for 2+ different items.", file=sys.stderr)
    for url, sources in duplicates:
        short_url = url[:80] + "..." if len(url) > 80 else url
        print("  URL: {}".format(short_url), file=sys.stderr)
        for guide, key in sources:
            print("    -> {} / {}".format(guide, key), file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
