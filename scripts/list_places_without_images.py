# -*- coding: utf-8 -*-
"""
List places with and without image files (excluding map), by guide type.

For each guide, loads places and checks output/images/<subdir>/ for the
place's image basenames. Writes a report: summary, then per-type lists
of places without images and places with images (with count).

Usage:
  python scripts/list_places_without_images.py
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.guide_loader import GUIDES, GUIDE_TO_SUBDIR, load_places

OUTPUT_DIR = _PROJECT_ROOT / "output"


def _basename(rel_path: str) -> str:
    """From 'images/moscow_monasteries/foo_1.jpg' or 'foo_1.jpg' -> 'foo_1.jpg'."""
    return rel_path.replace("\\", "/").split("/")[-1]


def _count_existing(place: dict[str, Any], img_dir: Path) -> int:
    """Number of place image files that exist on disk (map not counted)."""
    images = place.get("images") or []
    return sum(
        1 for p in images
        if (img_dir / _basename(p)).is_file()
    )


def main() -> int:
    """Build report: places with/without images, by type."""
    by_guide: dict[str, tuple[list[str], list[tuple[str, int]]]] = {}
    total_places = 0
    total_with = 0
    total_without = 0

    for guide in GUIDES:
        if guide == "test_e2e":
            continue
        try:
            places = load_places(guide)
        except Exception as e:
            print("Skip {}: {}.".format(guide, e), file=sys.stderr)
            continue
        subdir = GUIDE_TO_SUBDIR.get(guide)
        if not subdir:
            continue
        img_dir = OUTPUT_DIR / "images" / subdir
        without: list[str] = []
        with_imgs: list[tuple[str, int]] = []
        for place in places:
            name = place.get("name") or "?"
            total_places += 1
            n = _count_existing(place, img_dir)
            if n == 0:
                without.append(name)
                total_without += 1
            else:
                with_imgs.append((name, n))
                total_with += 1
        by_guide[guide] = (without, with_imgs)

    out_path = OUTPUT_DIR / "places_without_images.txt"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    lines: list[str] = [
        "Places with / without images (map not counted)",
        "=" * 50,
        "",
        "Summary",
        "-------",
        "Total places: {}".format(total_places),
        "With at least one image: {}".format(total_with),
        "Without any image: {}".format(total_without),
        "",
        "By type (guide)",
        "=" * 50,
        "",
    ]

    for guide in GUIDES:
        if guide not in by_guide:
            continue
        without, with_imgs = by_guide[guide]
        lines.append("--- {} ---".format(guide))
        lines.append("Without images ({}):".format(len(without)))
        if without:
            for name in without:
                lines.append("  - {}".format(name))
        else:
            lines.append("  (none)")
        lines.append("With images ({}):".format(len(with_imgs)))
        if with_imgs:
            for name, count in with_imgs:
                lines.append("  - {} ({} image(s))".format(name, count))
        else:
            lines.append("  (none)")
        lines.append("")

    lines.append("")
    lines.append("Flat list: places WITHOUT any image")
    lines.append("-" * 40)
    for guide in GUIDES:
        if guide not in by_guide:
            continue
        without, _ = by_guide[guide]
        for name in without:
            lines.append("{} | {}".format(guide, name))
    lines.append("")
    lines.append("Flat list: places WITH at least one image")
    lines.append("-" * 40)
    for guide in GUIDES:
        if guide not in by_guide:
            continue
        _, with_imgs = by_guide[guide]
        for name, count in with_imgs:
            lines.append("{} | {} ({} image(s))".format(guide, name, count))

    text = "\n".join(lines)
    out_path.write_text(text, encoding="utf-8")
    print("Written: {} ({} with, {} without images).".format(
        out_path, total_with, total_without,
    ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
