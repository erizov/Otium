# -*- coding: utf-8 -*-
"""
Pre-geocode guide places for proximity route planning.

Writes ``<city>/data/<city>_route_coords.json`` (slug → lat/lon).
Subsequent PDF builds reuse the cache and skip Wikipedia lookups.

Usage::

  python scripts/warm_route_coords_cache.py --cities yaroslavl dubai
  python scripts/warm_route_coords_cache.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_core import place_has_pdf_image, places_for_pdf
from scripts.city_guide_naming import is_pdf_filler_slug
from scripts.city_guide_proximity_routes import (
    load_route_coords_cache,
    resolve_place_coordinates,
    save_route_coords_cache,
)
from scripts.rebuild_stale_city_guide_pdfs import _discover_slugs


def _load_places(path: Path) -> list[dict]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        return []
    return [p for p in raw if isinstance(p, dict)]


def warm_city(project_root: Path, city_slug: str) -> tuple[int, int]:
    """Return (resolved, missing) counts."""
    city_root = project_root / city_slug
    places_path = city_root / "data" / "{}_places.json".format(city_slug)
    if not places_path.is_file():
        return 0, 0
    places = _load_places(places_path)
    pdf_places = places_for_pdf(city_root, places, city_slug=city_slug)
    cache = load_route_coords_cache(project_root, city_slug)
    resolved = 0
    missing = 0
    for place in pdf_places:
        slug = str(place.get("slug") or "")
        if not slug or is_pdf_filler_slug(slug):
            continue
        coords = resolve_place_coordinates(
            place,
            city_slug,
            cache,
            write_cache=False,
            project_root=None,
            allow_geocode=True,
        )
        if coords:
            resolved += 1
        else:
            missing += 1
    save_route_coords_cache(project_root, city_slug, cache)
    return resolved, missing


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (AttributeError, OSError, ValueError):
            pass
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=_PROJECT_ROOT,
    )
    parser.add_argument(
        "--cities",
        nargs="*",
        metavar="SLUG",
        help="City slugs (default: all build_*_pdf cities)",
    )
    args = parser.parse_args()
    root = args.project_root.resolve()
    cities = sorted(set(args.cities)) if args.cities else _discover_slugs(root)
    total_ok = total_miss = 0
    for city in cities:
        ok, miss = warm_city(root, city)
        total_ok += ok
        total_miss += miss
        print("{}: {} geocoded, {} missing".format(city, ok, miss))
    print(
        "--- done --- geocoded:",
        total_ok,
        "missing:",
        total_miss,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
