# -*- coding: utf-8 -*-
"""Print per-city counts of places with 0, 1, or 2 PDF-eligible images."""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_core import PDF_MAX_IMAGES_PER_PLACE
from scripts.city_guide_core import smallest_same_stem_image_rel
from scripts.verify_city_guide_place_images import _REGISTRY


def _count_images(root: Path, place: dict) -> int:
    if place.get("suppress_images_for_pdf"):
        return -1
    n = 0
    rel = place.get("image_rel_path")
    if rel and smallest_same_stem_image_rel(root, rel):
        n += 1
    for item in place.get("additional_images") or []:
        er = item.get("image_rel_path")
        if er and smallest_same_stem_image_rel(root, er):
            n += 1
    return min(n, PDF_MAX_IMAGES_PER_PLACE)


def _load_places(module_name: str, attr: str) -> list[dict]:
    mod = importlib.import_module(module_name)
    return [dict(p) for p in getattr(mod, attr)]


def _row(slug: str, places: list[dict]) -> tuple[str, int, int, int, int, int]:
    root = _PROJECT_ROOT / slug
    c0 = c1 = c2 = cskip = 0
    for p in places:
        n = _count_images(root, p)
        if n < 0:
            cskip += 1
        elif n == 0:
            c0 += 1
        elif n == 1:
            c1 += 1
        else:
            c2 += 1
    return slug, len(places), cskip, c0, c1, c2


def main() -> int:
    rows: list[tuple[str, int, int, int, int, int]] = []
    for slug, mod, attr in _REGISTRY:
        rows.append(_row(slug, _load_places(mod, attr)))

    moscow_path = _PROJECT_ROOT / "moscow" / "data" / "moscow_places.json"
    moscow_places = json.loads(moscow_path.read_text(encoding="utf-8"))
    rows.append(_row("moscow", moscow_places))
    rows.sort(key=lambda r: r[0])

    print(
        "{:<16} {:>6} {:>5} {:>5} {:>5} {:>5}".format(
            "city", "places", "skip", "0img", "1img", "2img",
        ),
    )
    print("-" * 48)
    t0 = t1 = t2 = 0
    for slug, total, skip, c0, c1, c2 in rows:
        print(
            "{:<16} {:>6} {:>5} {:>5} {:>5} {:>5}".format(
                slug, total, skip, c0, c1, c2,
            ),
        )
        t0 += c0
        t1 += c1
        t2 += c2
    print("-" * 48)
    print(
        "{:<16} {:>6} {:>5} {:>5} {:>5} {:>5}".format(
            "TOTAL",
            sum(r[1] for r in rows),
            sum(r[2] for r in rows),
            t0,
            t1,
            t2,
        ),
    )
    eligible = sum(r[1] - r[2] for r in rows)
    if eligible:
        print()
        print("PDF-eligible (excl. skip):", eligible)
        print("1 image: {} ({:.1f}%)".format(t1, 100.0 * t1 / eligible))
        print("2 images: {} ({:.1f}%)".format(t2, 100.0 * t2 / eligible))
        print("0 images: {} ({:.1f}%)".format(t0, 100.0 * t0 / eligible))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
