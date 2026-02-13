# -*- coding: utf-8 -*-
"""
Populate *_IMAGE_FALLBACKS in data/*_image_urls.py with extra URLs from
Wikimedia Commons for items that are still missing images.

Workflow:

1. Run the downloader to generate download_todo.txt for each guide, e.g.:

   python scripts/build_pdf.py --all-guides --download-retries 7 --download-only

2. Run this script to fetch extra image URLs from Commons and update the
   corresponding data/*_image_urls.py files:

   python scripts/fill_commons_fallbacks.py

3. Run the downloader again to try filling remaining slots using the new
   fallbacks.
"""

from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_IMAGES_DIR = PROJECT_ROOT / "output" / "images"

# Mapping from guide name -> module / variable names / images subdir
GUIDE_CONFIG: Dict[str, Dict[str, str]] = {
    "monasteries": {
        "module": "image_urls",
        "downloads": "IMAGE_DOWNLOADS",
        "fallbacks": "IMAGE_FALLBACKS",
        "subdir": "moscow_monasteries",
    },
    "places_of_worship": {
        "module": "places_of_worship_image_urls",
        "downloads": "PLACES_OF_WORSHIP_IMAGE_DOWNLOADS",
        "fallbacks": "PLACES_OF_WORSHIP_IMAGE_FALLBACKS",
        "subdir": "moscow_places_of_worship",
    },
    "parks": {
        "module": "park_image_urls",
        "downloads": "PARK_IMAGE_DOWNLOADS",
        "fallbacks": "PARK_IMAGE_FALLBACKS",
        "subdir": "moscow_parks",
    },
    "museums": {
        "module": "museum_image_urls",
        "downloads": "MUSEUM_IMAGE_DOWNLOADS",
        "fallbacks": "MUSEUM_IMAGE_FALLBACKS",
        "subdir": "moscow_museums",
    },
    "palaces": {
        "module": "palace_image_urls",
        "downloads": "PALACE_IMAGE_DOWNLOADS",
        "fallbacks": "PALACE_IMAGE_FALLBACKS",
        "subdir": "moscow_palaces",
    },
    "buildings": {
        "module": "building_image_urls",
        "downloads": "BUILDING_IMAGE_DOWNLOADS",
        "fallbacks": "BUILDING_IMAGE_FALLBACKS",
        "subdir": "moscow_buildings",
    },
    "sculptures": {
        "module": "sculpture_image_urls",
        "downloads": "SCULPTURE_IMAGE_DOWNLOADS",
        "fallbacks": "SCULPTURE_IMAGE_FALLBACKS",
        "subdir": "moscow_sculptures",
    },
    "places": {
        "module": "place_image_urls",
        "downloads": "PLACE_IMAGE_DOWNLOADS",
        "fallbacks": "PLACE_IMAGE_FALLBACKS",
        "subdir": "moscow_places",
    },
    "metro": {
        "module": "metro_image_urls",
        "downloads": "METRO_IMAGE_DOWNLOADS",
        "fallbacks": "METRO_IMAGE_FALLBACKS",
        "subdir": "moscow_metro",
    },
    "theaters": {
        "module": "theater_image_urls",
        "downloads": "THEATER_IMAGE_DOWNLOADS",
        "fallbacks": "THEATER_IMAGE_FALLBACKS",
        "subdir": "moscow_theaters",
    },
    "viewpoints": {
        "module": "viewpoint_image_urls",
        "downloads": "VIEWPOINT_IMAGE_DOWNLOADS",
        "fallbacks": "VIEWPOINT_IMAGE_FALLBACKS",
        "subdir": "moscow_viewpoints",
    },
    "cemeteries": {
        "module": "cemetery_image_urls",
        "downloads": "CEMETERY_IMAGE_DOWNLOADS",
        "fallbacks": "CEMETERY_IMAGE_FALLBACKS",
        "subdir": "moscow_cemeteries",
    },
}


def commons_search_urls(
    place_name: str,
    city: str = "Moscow",
    max_images: int = 5,
    min_width: int = 600,
    min_height: int = 400,
) -> List[str]:
    """
    Query Wikimedia Commons for images related to the place name.

    Returns a list of direct image URLs (jpg/jpeg/png/webp) with at least the
    requested width/height. This uses only existing photos (no generation).
    """
    query = f"{place_name} {city}".strip()
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": query,
        "gsrlimit": str(max_images * 4),
        "prop": "imageinfo",
        "iiprop": "url|size",
        "format": "json",
    }
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "ExcursionGuide/Commons/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
    except Exception as exc:
        print(f"[Commons] request failed for {place_name!r}: {exc}", file=sys.stderr)
        return []

    try:
        payload = json.loads(data.decode("utf-8", errors="ignore"))
    except Exception as exc:
        print(f"[Commons] JSON decode failed for {place_name!r}: {exc}", file=sys.stderr)
        return []

    pages = (payload.get("query") or {}).get("pages") or {}
    urls: List[str] = []
    seen: set[str] = set()

    for page in pages.values():
        infos = page.get("imageinfo") or []
        for info in infos:
            src = info.get("url") or ""
            if not src:
                continue
            # Only accept real raster images
            if not any(
                src.lower().endswith(ext)
                for ext in (".jpg", ".jpeg", ".png", ".webp")
            ):
                continue
            width = int(info.get("width", 0))
            height = int(info.get("height", 0))
            if width < min_width or height < min_height:
                continue
            if src in seen:
                continue
            seen.add(src)
            urls.append(src)
            if len(urls) >= max_images:
                break
        if len(urls) >= max_images:
            break

    return urls


def load_image_url_module(guide: str) -> Tuple[Path, Dict[str, str], Dict[str, List[str]], str]:
    cfg = GUIDE_CONFIG[guide]
    module_name = cfg["module"]
    downloads_name = cfg["downloads"]
    fallbacks_name = cfg["fallbacks"]
    path = DATA_DIR / f"{module_name}.py"

    sys.path.insert(0, str(PROJECT_ROOT))
    try:
        mod = __import__(f"data.{module_name}", fromlist=[downloads_name, fallbacks_name])
    finally:
        if str(PROJECT_ROOT) in sys.path:
            sys.path.remove(str(PROJECT_ROOT))
    downloads = getattr(mod, downloads_name)
    fallbacks = getattr(mod, fallbacks_name)
    return path, downloads, fallbacks, fallbacks_name


def update_fallbacks_file(
    path: Path,
    fallbacks_name: str,
    fallbacks: Dict[str, List[str]],
) -> None:
    """
    Replace the definition of *_IMAGE_FALLBACKS in the given file with the
    updated dictionary. Assumes the file contains a line:

        FALLBACK_NAME: dict[str, list[str]] = {...}
    """
    text = path.read_text(encoding="utf-8")
    marker = f"{fallbacks_name}: dict[str, list[str]] = "
    idx = text.find(marker)
    if idx == -1:
        raise RuntimeError(f"Could not find {fallbacks_name} in {path}")
    prefix = text[: idx + len(marker)]

    lines: List[str] = ["{"]
    for key in sorted(fallbacks.keys()):
        urls = fallbacks[key]
        if not urls:
            continue
        joined = ", ".join(repr(u) for u in urls)
        lines.append(f"    {key!r}: [{joined}],")
    lines.append("}")

    new_body = "\n".join(lines) + "\n"
    new_text = prefix + new_body
    path.write_text(new_text, encoding="utf-8")


def process_guide(guide: str) -> None:
    cfg = GUIDE_CONFIG[guide]
    images_dir = OUTPUT_IMAGES_DIR / cfg["subdir"]
    todo_path = images_dir / "download_todo.txt"

    if not todo_path.exists():
        print(f"[{guide}] No {todo_path}, nothing to do.")
        return

    lines = [
        ln.strip()
        for ln in todo_path.read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]
    if not lines:
        print(f"[{guide}] {todo_path} is empty, nothing to do.")
        return

    path, downloads, fallbacks, fallbacks_name = load_image_url_module(guide)
    updated = dict(fallbacks)

    print(f"[{guide}] Filling Commons fallbacks from {todo_path} ...")
    for line in lines:
        parts = line.split("\t", 3)
        if len(parts) < 3:
            continue
        # Format: guide \t basename \t item_name \t reason
        _, basename, item_name, *rest = parts + [""]
        key = basename.strip()
        name = item_name.strip()

        current = updated.get(key, [])
        # If we already have 4+ fallbacks for this basename, skip
        if len(current) >= 4:
            continue

        reason = rest[0] if rest else ""
        print(f"  {basename}: reason={reason!r} — search Commons for {name!r}")
        urls = commons_search_urls(name, city="Moscow", max_images=5)
        if not urls:
            continue

        merged = list(current)
        for u in urls:
            if u not in merged:
                merged.append(u)
        updated[key] = merged

    update_fallbacks_file(path, fallbacks_name, updated)
    print(f"[{guide}] Updated fallbacks in {path}")


def main() -> None:
    for guide in GUIDE_CONFIG.keys():
        process_guide(guide)


if __name__ == "__main__":
    main()

