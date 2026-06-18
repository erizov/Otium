# -*- coding: utf-8 -*-
"""Audit on-disk place images for person/animal main-subject rejects."""

from __future__ import annotations

import argparse
import importlib
import os
import shutil
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.image_subject_filter import check_image_path
from scripts.image_subject_filter import rejection_message
from scripts.image_subject_filter import subject_filter_enabled
from scripts.rebuild_stale_city_guide_pdfs import _discover_slugs
from scripts.verify_city_guide_place_images import _REGISTRY

_FORBIDDEN = "forbidden"


def _place_image_paths(city_slug: str) -> list[tuple[str, Path]]:
    mod = None
    attr = None
    for slug, mod_name, a in _REGISTRY:
        if slug == city_slug:
            mod = importlib.import_module(mod_name)
            attr = a
            break
    if mod is None or not attr:
        return []
    root = _PROJECT_ROOT / city_slug
    out: list[tuple[str, Path]] = []
    for place in getattr(mod, attr):
        slug = str(place.get("slug") or "")
        rel = str(place.get("image_rel_path") or "").replace("\\", "/")
        if rel:
            out.append((slug, root / rel))
        for item in place.get("additional_images") or []:
            er = str(item.get("image_rel_path") or "").replace("\\", "/")
            if er:
                out.append((slug, root / er))
    return out


def audit_city(
    city_slug: str,
    *,
    move_forbidden: bool,
    dry_run: bool,
) -> tuple[int, int]:
    paths = _place_image_paths(city_slug)
    checked = rejected = 0
    img_root = _PROJECT_ROOT / city_slug / "images"
    forb = img_root / _FORBIDDEN
    for slug, path in paths:
        if not path.is_file():
            continue
        checked += 1
        verdict = check_image_path(path)
        if verdict.accept:
            continue
        rejected += 1
        msg = rejection_message(verdict)
        print("{} / {}: {}".format(city_slug, slug, msg))
        if dry_run or not move_forbidden:
            continue
        forb.mkdir(parents=True, exist_ok=True)
        dest = forb / path.name
        if not dest.is_file():
            shutil.move(str(path), str(dest))
    return checked, rejected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cities", nargs="*", default=None, metavar="SLUG")
    parser.add_argument(
        "--move-forbidden",
        action="store_true",
        help="Move rejected images to images/forbidden/.",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--no-subject-filter",
        action="store_true",
        help="Disable person/animal checks (enabled by default).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Use stricter person/animal area thresholds.",
    )
    args = parser.parse_args()

    if args.no_subject_filter:
        os.environ["SUBJECT_FILTER"] = "0"
    if args.strict:
        os.environ["SUBJECT_FILTER_STRICT"] = "1"
    if not subject_filter_enabled():
        print("Subject filter disabled.", file=sys.stderr)
        return 2

    cities = _discover_slugs(_PROJECT_ROOT)
    if args.cities:
        cities = [c for c in cities if c in set(args.cities)]

    total_c = total_r = 0
    for slug in cities:
        c, r = audit_city(
            slug,
            move_forbidden=args.move_forbidden,
            dry_run=args.dry_run,
        )
        if r:
            print("{}: {}/{} rejected".format(slug, r, c))
        total_c += c
        total_r += r
    print("Checked {} images; rejected {}.".format(total_c, total_r))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
