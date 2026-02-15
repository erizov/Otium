# -*- coding: utf-8 -*-
"""
Fill *_image_urls.py DOWNLOADS by place name using multiple image services.

Uses Commons, Pixabay, Pexels, Openverse, Flickr, Unsplash, Yandex (round-robin)
to find image URLs by place name, then writes only real URLs into the
corresponding data/<guide>_image_urls.py. No placeholders (example.com) are
written.

Usage:
  python scripts/fill_image_urls.py [--guide GUIDE] [--dry-run]

  --guide: only fill this guide (default: all).
  --dry-run: print what would be written, do not modify files.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.guide_loader import GUIDES, load_guide_with_downloads, load_places
from scripts.slug_item_map import basename_to_slug

# Guide -> (data filename, DOWNLOADS var name, FALLBACKS var name)
_GUIDE_TO_CONFIG: dict[str, tuple[str, str, str]] = {
    "monasteries": ("image_urls.py", "IMAGE_DOWNLOADS", "IMAGE_FALLBACKS"),
    "places_of_worship": (
        "places_of_worship_image_urls.py",
        "PLACES_OF_WORSHIP_IMAGE_DOWNLOADS",
        "PLACES_OF_WORSHIP_IMAGE_FALLBACKS",
    ),
    "parks": ("park_image_urls.py", "PARK_IMAGE_DOWNLOADS", "PARK_IMAGE_FALLBACKS"),
    "museums": (
        "museum_image_urls.py",
        "MUSEUM_IMAGE_DOWNLOADS",
        "MUSEUM_IMAGE_FALLBACKS",
    ),
    "palaces": (
        "palace_image_urls.py",
        "PALACE_IMAGE_DOWNLOADS",
        "PALACE_IMAGE_FALLBACKS",
    ),
    "buildings": (
        "building_image_urls.py",
        "BUILDING_IMAGE_DOWNLOADS",
        "BUILDING_IMAGE_FALLBACKS",
    ),
    "sculptures": (
        "sculpture_image_urls.py",
        "SCULPTURE_IMAGE_DOWNLOADS",
        "SCULPTURE_IMAGE_FALLBACKS",
    ),
    "places": (
        "place_image_urls.py",
        "PLACE_IMAGE_DOWNLOADS",
        "PLACE_IMAGE_FALLBACKS",
    ),
    "squares": (
        "squares_image_urls.py",
        "SQUARES_IMAGE_DOWNLOADS",
        "SQUARES_IMAGE_FALLBACKS",
    ),
    "metro": (
        "metro_image_urls.py",
        "METRO_IMAGE_DOWNLOADS",
        "METRO_IMAGE_FALLBACKS",
    ),
    "theaters": (
        "theater_image_urls.py",
        "THEATER_IMAGE_DOWNLOADS",
        "THEATER_IMAGE_FALLBACKS",
    ),
    "viewpoints": (
        "viewpoint_image_urls.py",
        "VIEWPOINT_IMAGE_DOWNLOADS",
        "VIEWPOINT_IMAGE_FALLBACKS",
    ),
    "bridges": (
        "bridge_image_urls.py",
        "BRIDGE_IMAGE_DOWNLOADS",
        "BRIDGE_IMAGE_FALLBACKS",
    ),
    "markets": (
        "market_image_urls.py",
        "MARKET_IMAGE_DOWNLOADS",
        "MARKET_IMAGE_FALLBACKS",
    ),
    "libraries": (
        "library_image_urls.py",
        "LIBRARY_IMAGE_DOWNLOADS",
        "LIBRARY_IMAGE_FALLBACKS",
    ),
    "railway_stations": (
        "railway_station_image_urls.py",
        "RAILWAY_STATION_IMAGE_DOWNLOADS",
        "RAILWAY_STATION_IMAGE_FALLBACKS",
    ),
    "cemeteries": (
        "cemetery_image_urls.py",
        "CEMETERY_IMAGE_DOWNLOADS",
        "CEMETERY_IMAGE_FALLBACKS",
    ),
    "landmarks": (
        "landmarks_image_urls.py",
        "LANDMARK_IMAGE_DOWNLOADS",
        "LANDMARK_IMAGE_FALLBACKS",
    ),
    "cafes": ("cafe_image_urls.py", "CAFE_IMAGE_DOWNLOADS", "CAFE_IMAGE_FALLBACKS"),
}

_SKIP_PREFIXES = ("https://example.com/", "http://example.com/")
_DELAY_BETWEEN_PLACES_SEC = 2.5


def _basename(img_path: str) -> str:
    """From 'images/moscow_cafes/foo_1.jpg' -> 'foo_1.jpg'."""
    return img_path.split("/")[-1] if "/" in img_path else img_path


def _is_placeholder(url: str) -> bool:
    """True if URL should not be written (placeholder or invalid)."""
    if not url or not url.strip():
        return True
    u = url.strip()
    if any(u.startswith(p) for p in _SKIP_PREFIXES):
        return True
    if "placeholder" in u.lower():
        return True
    return False


def _get_search_names(place: dict) -> list[str]:
    """Return list of names to try (RU, EN, aliases) for image search."""
    names: list[str] = []
    primary = (place.get("name") or "").strip()
    if primary:
        names.append(primary)
    name_en = (place.get("name_en") or "").strip()
    if name_en and name_en != primary:
        names.append(name_en)
    if len(names) < 2:
        try:
            from scripts.translate_place_name import get_search_names as gsn
            ru, en = gsn(primary)
            if ru and ru not in names:
                names.append(ru)
            if en and en not in names:
                names.append(en)
        except Exception:
            pass
    for a in place.get("aliases") or []:
        if isinstance(a, str) and a.strip() and a.strip() not in names:
            names.append(a.strip())
        if len(names) >= 4:
            break
    return names[:4]


def _fetch_urls_for_place(
    place_name: str,
    place: dict,
    excluded_sources: set[str],
    failure_counts: dict[str, int],
    project_root: Path,
) -> list[str]:
    """Fetch image URLs from multiple services by place name. No placeholders."""
    from scripts.download_with_dedup import (
        _fetch_urls_round_robin,
        _normalize_image_url,
    )
    names = _get_search_names(place)
    if not names:
        names = [place_name]
    urls, _ = _fetch_urls_round_robin(
        names,
        city="Moscow",
        city_ru="Москва",
        max_per_source=5,
        excluded_sources=excluded_sources,
        failure_counts=failure_counts,
        project_root=project_root,
    )
    out: list[str] = []
    seen: set[str] = set()
    for u in urls:
        norm = _normalize_image_url(u)
        if not norm or _is_placeholder(norm) or norm in seen:
            continue
        out.append(norm)
        seen.add(norm)
        if len(out) >= 4:
            break
    return out


def _required_slots(images: list[str]) -> list[str]:
    """Return [slug_1.jpg, slug_2.jpg, slug_3.jpg, slug_4.jpg] from first slot."""
    basenames = [_basename(p) for p in (images or [])]
    standard = [
        b for b in basenames
        if b.endswith("_1.jpg") or b.endswith("_2.jpg")
        or b.endswith("_3.jpg") or b.endswith("_4.jpg")
    ]
    if not standard:
        return []
    slug = basename_to_slug(standard[0])
    return [
        "{}_1.jpg".format(slug),
        "{}_2.jpg".format(slug),
        "{}_3.jpg".format(slug),
        "{}_4.jpg".format(slug),
    ]


def fill_guide(
    guide: str,
    dry_run: bool,
    excluded_sources: set[str],
    failure_counts: dict[str, int],
) -> int:
    """Fill DOWNLOADS for one guide. Returns number of URLs written."""
    if guide not in _GUIDE_TO_CONFIG:
        print("Unknown guide: {}.".format(guide), file=sys.stderr)
        return 0
    data_file, downloads_var, fallbacks_var = _GUIDE_TO_CONFIG[guide]
    places, existing_downloads = load_guide_with_downloads(guide)
    # Start from existing; replace only placeholders or missing
    downloads: dict[str, str] = {}
    for bn, url in (existing_downloads or {}).items():
        if url and not _is_placeholder(url):
            downloads[bn] = url
    added = 0
    for place in places:
        name = place.get("name") or "?"
        images = place.get("images") or []
        slots = _required_slots(images)
        if not slots:
            continue
        # Fetch only if at least one slot is missing or placeholder
        need = [bn for bn in slots if bn not in downloads]
        if not need:
            continue
        urls = _fetch_urls_for_place(
            name,
            place,
            excluded_sources,
            failure_counts,
            _PROJECT_ROOT,
        )
        for i, bn in enumerate(slots):
            if bn not in downloads and i < len(urls) and not _is_placeholder(urls[i]):
                downloads[bn] = urls[i]
                added += 1
        time.sleep(_DELAY_BETWEEN_PLACES_SEC)
    if dry_run:
        print(
            "[dry-run] {}: {} total ({} added).".format(
                guide, len(downloads), added,
            ),
        )
        for k, v in sorted(downloads.items()):
            print("  {} -> {}".format(k, v[:60] + "..." if len(v) > 60 else v))
        return len(downloads)
    data_path = _PROJECT_ROOT / "data" / data_file
    lines = [
        "# -*- coding: utf-8 -*-",
        '"""Image URLs filled by place name (Commons, Pixabay, Pexels, '
        'Openverse, etc.). No placeholders."""',
        "",
        "{}: dict[str, str] = {{".format(downloads_var),
    ]
    for k in sorted(downloads.keys()):
        url = downloads[k]
        # Escape backslash and quote in URL for Python string
        url_esc = url.replace("\\", "\\\\").replace('"', '\\"')
        lines.append('    "{}": "{}",'.format(k, url_esc))
    lines.append("}")
    if fallbacks_var:
        lines.append("")
        lines.append("{}: dict[str, list[str]] = {{}}".format(fallbacks_var))
    lines.append("")
    data_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Wrote {} ({} entries, {} new).".format(data_path, len(downloads), added))
    return len(downloads)


def main() -> int:
    """Entry point."""
    parser = argparse.ArgumentParser(
        description="Fill image URL index by place name (multi-source).",
    )
    parser.add_argument(
        "--guide",
        type=str,
        default="",
        help="Only fill this guide (default: all).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not write files.",
    )
    args = parser.parse_args()
    guides = [args.guide] if args.guide else GUIDES
    if args.guide and args.guide not in GUIDES:
        print("Unknown guide: {}.".format(args.guide), file=sys.stderr)
        return 1
    # Persist exclusion across places/guides so "temporarily excluded (1h)"
    # is honoured for the rest of this run (and saved to file for next run).
    from scripts.download_with_dedup import _load_excluded_sources
    excluded_sources: set[str] = _load_excluded_sources(_PROJECT_ROOT)
    if excluded_sources:
        print(
            "Excluded sources (1h): {}.".format(
                ", ".join(sorted(excluded_sources)),
            ),
        )
    failure_counts: dict[str, int] = {}
    total = 0
    for g in guides:
        total += fill_guide(g, args.dry_run, excluded_sources, failure_counts)
    print("Total: {} URL(s) written.".format(total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
