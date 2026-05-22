# -*- coding: utf-8 -*-
"""Batch-optimize raster images under per-city ``images/`` trees."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_image_optimize import CITY_GUIDE_IMAGE_MAX_BYTES
from scripts.city_guide_image_optimize import CITY_GUIDE_IMAGE_MAX_SIDE_PX
from scripts.city_guide_image_optimize import optimize_raster_image_if_large
from scripts.rebuild_stale_city_guide_pdfs import _discover_slugs

_RASTER_EXT = frozenset({".jpg", ".jpeg", ".png", ".webp"})


def optimize_city_images(
    project_root: Path,
    city_slug: str,
    *,
    max_bytes: int,
    dry_run: bool,
) -> int:
    img_dir = project_root / city_slug / "images"
    if not img_dir.is_dir():
        return 0
    changed = 0
    for path in sorted(img_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in _RASTER_EXT:
            continue
        if dry_run:
            try:
                sz = path.stat().st_size
            except OSError:
                continue
            print("{}  {} B".format(path.relative_to(project_root), sz))
            continue
        if optimize_raster_image_if_large(
            path,
            max_bytes=max_bytes,
            max_side=CITY_GUIDE_IMAGE_MAX_SIDE_PX,
            verbose=True,
        ):
            changed += 1
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=_PROJECT_ROOT,
    )
    parser.add_argument(
        "--cities",
        nargs="*",
        default=None,
        metavar="SLUG",
        help="City slugs (default: all discovered).",
    )
    parser.add_argument(
        "--max-kib",
        type=int,
        default=CITY_GUIDE_IMAGE_MAX_BYTES // 1024,
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = args.project_root.resolve()
    cap = max(1, args.max_kib) * 1024
    if args.cities:
        cities = sorted(set(args.cities))
    else:
        cities = _discover_slugs(root)
    total = 0
    for slug in cities:
        n = optimize_city_images(root, slug, max_bytes=cap, dry_run=args.dry_run)
        total += n
        if n and not args.dry_run:
            print("{}: optimized {} file(s)".format(slug, n))
    if args.dry_run:
        print("dry-run complete ({} cities)".format(len(cities)))
    else:
        print("Total optimized: {} across {} cities".format(total, len(cities)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
