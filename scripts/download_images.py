# -*- coding: utf-8 -*-
"""
Загрузка изображений для путеводителя «Московские монастыри».

Скачивает общедоступные изображения (Wikipedia/Commons) в папку
output/images/moscow_monasteries/. Запускается в цикле с паузой
каждые несколько минут, пока не будут успешно загружены все файлы
для каждого объекта (или не истечёт лимит попыток).
"""

import sys
import time
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from data.monasteries import IMAGES_SUBFOLDER, MONASTERIES

MIN_IMAGE_BYTES = 500
PAUSE_MINUTES = 3
MAX_ROUNDS = 480  # 480 * 3 min = 24 h максимум


def _required_filenames() -> set[str]:
    """Имена файлов, которые нужны для всех 20 объектов."""
    out: set[str] = set()
    for m in MONASTERIES:
        for rel in m["images"]:
            # rel = "images/moscow_monasteries/andronikov_1.jpg"
            parts = rel.replace("\\", "/").split("/")
            if len(parts) >= 2 and parts[-2] == IMAGES_SUBFOLDER:
                out.add(parts[-1])
            elif "/" in rel:
                out.add(rel.split("/")[-1])
            else:
                out.add(rel)
    return out


def _target_dir() -> Path:
    return _project_root / "output" / "images" / IMAGES_SUBFOLDER


def _all_downloaded() -> bool:
    target = _target_dir()
    if not target.exists():
        return False
    required = _required_filenames()
    for name in required:
        path = target / name
        if not path.exists() or path.stat().st_size < MIN_IMAGE_BYTES:
            return False
    return True


def _download_round() -> int:
    """Одна попытка загрузки недостающих. Возвращает число загруженных."""
    try:
        import urllib.request
    except ImportError:
        return 0

    from data.image_urls import IMAGE_DOWNLOADS

    target = _target_dir()
    target.mkdir(parents=True, exist_ok=True)
    required = _required_filenames()
    downloaded = 0
    seen_urls: set[str] = set()

    for filename, url in IMAGE_DOWNLOADS.items():
        if filename not in required:
            continue
        if url in seen_urls:
            continue
        path = target / filename
        if path.exists() and path.stat().st_size >= MIN_IMAGE_BYTES:
            seen_urls.add(url)
            continue
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "ExcursionGuide/1.0 (educational)"},
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = resp.read()
            if len(data) < MIN_IMAGE_BYTES:
                continue
            path.write_bytes(data)
            downloaded += 1
            seen_urls.add(url)
            print("Downloaded:", path.name)
        except Exception as e:
            print("Skip {}: {}".format(filename, e), file=sys.stderr)
        time.sleep(0.6)
    return downloaded


def main() -> None:
    """Цикл загрузки каждые PAUSE_MINUTES минут до успеха или MAX_ROUNDS."""
    target = _target_dir()
    target.mkdir(parents=True, exist_ok=True)
    required = _required_filenames()
    print(
        "Target: {}. Required files: {}.".format(
            target, len(required)
        )
    )
    round_num = 0
    while round_num < MAX_ROUNDS:
        round_num += 1
        n = _download_round()
        if _all_downloaded():
            print("All images downloaded successfully.")
            return
        if n > 0:
            print("This round: {} new. Next try in {} min.".format(
                n, PAUSE_MINUTES
            ))
        else:
            print(
                "No new downloads. Next try in {} min (round {}).".format(
                    PAUSE_MINUTES, round_num
                )
            )
        time.sleep(PAUSE_MINUTES * 60)
    print("Stopped after {} rounds. Some images may still be missing.".format(
        MAX_ROUNDS
    ), file=sys.stderr)


if __name__ == "__main__":
    main()
