# -*- coding: utf-8 -*-
"""Rotate primary image and refresh downloads for named Moscow places."""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from moscow.whitelist import default_whitelist_path
from moscow.whitelist import url_is_whitelisted

from scripts.city_guide_core import MIN_IMAGE_BYTES
from scripts.city_guide_jerusalem_style_images import _candidate_urls
from scripts.city_guide_jerusalem_style_images import _download_place_image

_PLACES_PATH = _PROJECT_ROOT / "moscow" / "data" / "moscow_places.json"
_MOSCOW = _PROJECT_ROOT / "moscow"

# slug -> new primary image_rel_path
_NEW_PRIMARY: dict[str, str] = {
    "moscow_buildings_8": "images/moscow_markets/tsum_3.jpg",
    "moscow_cafes_7": "images/moscow_cafes/elitny_vdnkh_3.jpg",
    "moscow_cafes_6": "images/moscow_cafes/yar_3.jpg",
    "moscow_places_of_worship_26": (
        "images/moscow_places_of_worship/rozhdestva_izmaylovo_2.jpg"
    ),
    "moscow_landmarks_4": "images/moscow_buildings/mid_3.jpg",
    "moscow_markets_2": "images/moscow_markets/dorogomilovsky_3.jpg",
    "moscow_buildings_13": "images/moscow_buildings/dom_soyuzov_1.jpg",
    "moscow_parks_1": "images/moscow_parks/vdnh_1.jpg",
    "moscow_places_of_worship_62": (
        "images/moscow_places_of_worship/buddhist_temple_1.jpg"
    ),
    "moscow_parks_4": "images/moscow_parks/sokolniki_3.jpg",
    "moscow_buildings_25": "images/moscow_buildings/tsra_3.jpg",
    "moscow_buildings_14": "images/moscow_buildings/leningradskaya_3.jpg",
    "moscow_buildings_11": "images/moscow_buildings/duma_3.jpg",
    "moscow_buildings_16": "images/moscow_buildings/mid_3.jpg",
    "moscow_places_of_worship_9": (
        "images/moscow_places_of_worship/georgy_pskovskaya_2.jpg"
    ),
    "moscow_places_of_worship_39": (
        "images/moscow_places_of_worship/nikita_shvivaya_2.jpg"
    ),
    "moscow_places_of_worship_38": (
        "images/moscow_places_of_worship/spas_bolvanovka_3.jpg"
    ),
    "moscow_buildings_3": "images/moscow_buildings/city_3.jpg",
}

# Identical placeholder downloads (re-fetch from registry URLs).
_CORRUPTED_SIZES = frozenset({859466})


def _load_url_map() -> dict[str, str]:
    from moscow.data.building_image_urls import BUILDING_IMAGE_DOWNLOADS
    from moscow.data.cafe_image_urls import CAFE_IMAGE_DOWNLOADS
    from moscow.data.landmarks_image_urls import LANDMARK_IMAGE_DOWNLOADS
    from moscow.data.park_image_urls import PARK_IMAGE_DOWNLOADS
    from moscow.data.places_of_worship_image_urls import (
        PLACES_OF_WORSHIP_IMAGE_DOWNLOADS,
    )

    merged: dict[str, str] = {}
    for block in (
        BUILDING_IMAGE_DOWNLOADS,
        CAFE_IMAGE_DOWNLOADS,
        PARK_IMAGE_DOWNLOADS,
        PLACES_OF_WORSHIP_IMAGE_DOWNLOADS,
        LANDMARK_IMAGE_DOWNLOADS,
    ):
        merged.update(block)
    return merged


def _resolve(rel: str) -> Path:
    rel = rel.lstrip("/").replace("\\", "/")
    if rel.startswith("images/"):
        return _MOSCOW / rel
    return _MOSCOW / "images" / rel


def _image_prefix(basename: str) -> str:
    match = re.match(r"^(.*)_\d+\.(jpg|jpeg|png)$", basename, re.I)
    if match:
        return match.group(1)
    stem = Path(basename).stem
    return stem


def _sync_four_images(
    place: dict[str, Any],
    primary_rel: str,
    url_map: dict[str, str],
) -> None:
    rel = primary_rel.replace("\\", "/")
    parts = rel.split("/")
    folder = parts[1] if len(parts) >= 3 else "images"
    prefix = _image_prefix(parts[-1])
    slots: list[dict[str, str]] = []
    for idx in range(1, 5):
        filename = f"{prefix}_{idx}.jpg"
        slots.append(
            {
                "image_rel_path": f"images/{folder}/{filename}",
                "image_source_url": url_map.get(filename, ""),
            },
        )
    primary = primary_rel.replace("\\", "/")
    extras = [item for item in slots if item["image_rel_path"] != primary]
    place["image_rel_path"] = primary
    for item in slots:
        if item["image_rel_path"] == primary:
            place["image_source_url"] = item["image_source_url"]
            break
    place["additional_images"] = extras[:3]


def _reorder_images(
    place: dict[str, Any],
    new_primary: str,
    url_map: dict[str, str],
) -> bool:
    new_primary = new_primary.replace("\\", "/")
    old_primary = str(place.get("image_rel_path") or "").replace("\\", "/")
    old_extras = json.dumps(
        place.get("additional_images") or [],
        ensure_ascii=False,
        sort_keys=True,
    )
    _sync_four_images(place, new_primary, url_map)
    new_extras = json.dumps(
        place.get("additional_images") or [],
        ensure_ascii=False,
        sort_keys=True,
    )
    return old_primary != new_primary or old_extras != new_extras


def _needs_download(path: Path, *, force: bool) -> bool:
    if force:
        return True
    if not path.is_file():
        return True
    if path.stat().st_size < MIN_IMAGE_BYTES:
        return True
    if path.stat().st_size in _CORRUPTED_SIZES:
        return True
    return False


def _download_place_images(
    place: dict[str, Any],
    *,
    force: bool,
    delay: float,
    no_whitelist_check: bool,
) -> list[str]:
    results: list[str] = []
    todo: list[tuple[str, str]] = []
    rel = str(place.get("image_rel_path") or "")
    url = str(place.get("image_source_url") or "")
    if rel and url:
        todo.append((rel, url))
    for extra in place.get("additional_images") or []:
        er = str(extra.get("image_rel_path") or "")
        eu = str(extra.get("image_source_url") or "")
        if er and eu:
            todo.append((er, eu))
    wpath = default_whitelist_path()
    for rel_path, source_url in todo:
        dest = _resolve(rel_path)
        if not _needs_download(dest, force=force):
            continue
        if not no_whitelist_check and not url_is_whitelisted(
            source_url,
            whitelist_path=wpath,
        ):
            results.append(f"skip not whitelisted: {rel_path}")
            continue
        urls = _candidate_urls(source_url, None)
        ok, msg = _download_place_image(
            urls,
            dest,
            timeout_sec=60,
            retries_429=4,
            pause_429_sec=20.0,
        )
        if ok:
            results.append(f"OK {rel_path}")
        else:
            results.append(f"FAIL {rel_path}: {msg}")
        if delay > 0:
            time.sleep(delay)
    return results


def swap_moscow_place_images(
    *,
    dry_run: bool = False,
    download: bool = False,
    force_download: bool = False,
    download_delay: float = 2.0,
    no_whitelist_check: bool = False,
) -> list[dict[str, str]]:
    url_map = _load_url_map()
    rows: list[dict[str, Any]] = json.loads(
        _PLACES_PATH.read_text(encoding="utf-8"),
    )
    by_slug = {str(p.get("slug")): p for p in rows}
    changes: list[dict[str, str]] = []
    for slug, new_rel in _NEW_PRIMARY.items():
        place = by_slug.get(slug)
        if place is None:
            changes.append({"slug": slug, "status": "missing slug"})
            continue
        old = str(place.get("image_rel_path") or "")
        updated = _reorder_images(place, new_rel, url_map)
        new = str(place.get("image_rel_path") or "")
        if download and not dry_run:
            dl = _download_place_images(
                place,
                force=force_download,
                delay=download_delay,
                no_whitelist_check=no_whitelist_check,
            )
            changes.append(
                {
                    "slug": slug,
                    "status": "updated" if updated or old != new else "synced",
                    "old": old,
                    "new": new,
                    "downloads": "; ".join(dl),
                },
            )
        elif old != new:
            changes.append(
                {"slug": slug, "status": "updated", "old": old, "new": new},
            )
        else:
            changes.append({"slug": slug, "status": "unchanged", "old": old})
    if not dry_run:
        _PLACES_PATH.write_text(
            json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return changes


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--download",
        action="store_true",
        help="Download missing or corrupted images after swap.",
    )
    parser.add_argument(
        "--force-download",
        action="store_true",
        help="Re-download all images for swapped places.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        help="Pause between downloads (default 2.0).",
    )
    parser.add_argument(
        "--no-whitelist-check",
        action="store_true",
        help="Download even if URL is outside SOURCES_WHITELIST.md.",
    )
    args = parser.parse_args()
    changes = swap_moscow_place_images(
        dry_run=args.dry_run,
        download=args.download,
        force_download=args.force_download,
        download_delay=args.delay,
        no_whitelist_check=args.no_whitelist_check,
    )
    print(json.dumps(changes, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
