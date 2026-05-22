# -*- coding: utf-8 -*-
"""Download missing primary images for registry cities (post-grow batch)."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_jerusalem_style_images import (
    add_download_image_args,
    download_jerusalem_style_images,
)
from scripts.city_guide_naming import is_pdf_filler_slug
from scripts.city_guide_title_heraldry_assets import (
    title_page_assets_for_download_arg,
)
from scripts.verify_city_guide_place_images import _REGISTRY


def _missing_count(city_slug: str, places: list[dict]) -> int:
    root = _PROJECT_ROOT / city_slug
    n = 0
    for p in places:
        if p.get("suppress_images_for_pdf"):
            continue
        if is_pdf_filler_slug(str(p.get("slug") or "")):
            continue
        rel = str(p.get("image_rel_path") or "").replace("\\", "/")
        if rel and not (root / rel).is_file():
            n += 1
    return n


def _download_city(city_slug: str, args: argparse.Namespace) -> int:
    mod_name = "{}.data.places_registry".format(city_slug)
    wl_mod_name = "{}.whitelist".format(city_slug)
    try:
        reg = importlib.import_module(mod_name)
        wl = importlib.import_module(wl_mod_name)
    except ModuleNotFoundError as exc:
        print(city_slug, "skip:", exc, file=sys.stderr)
        return 0
    attr = None
    for key in dir(reg):
        if key.endswith("_PLACES") and key.isupper():
            attr = key
            break
    if not attr:
        print(city_slug, "skip: no *_PLACES", file=sys.stderr)
        return 0
    places = list(getattr(reg, attr))
    miss = _missing_count(city_slug, places)
    if miss == 0:
        print(city_slug, "skip (all images on disk)")
        return 0
    print(city_slug, "downloading", miss, "missing …", flush=True)
    title_assets = ()
    if args.with_title_assets:
        title_assets = title_page_assets_for_download_arg(city_slug)
    return download_jerusalem_style_images(
        city_root=_PROJECT_ROOT / city_slug,
        places=places,
        whitelist_path=wl.default_whitelist_path(),
        title_page_assets=title_assets,
        args=args,
        url_is_whitelisted_fn=wl.url_is_whitelisted,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cities",
        nargs="*",
        default=None,
        metavar="SLUG",
    )
    parser.add_argument(
        "--with-title-assets",
        action="store_true",
        help="Also download guide coat/flag SVGs (Commons API; 429-prone).",
    )
    add_download_image_args(parser)
    parser.set_defaults(delay=5.0, thumb_width=330, retries_429=3, pause_429=30.0)
    args = parser.parse_args()
    if not args.full_size and not args.allow_original:
        print(
            "Using Commons standard thumbs only (330px default). "
            "Pass --allow-original to fall back to full-size URLs.",
            file=sys.stderr,
        )
    want = frozenset(args.cities) if args.cities else None
    rc = 0
    for slug, _mod, _attr in _REGISTRY:
        if want and slug not in want:
            continue
        if slug in ("smolensk", "spb"):
            continue
        code = _download_city(slug, args)
        if code:
            rc = code
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
