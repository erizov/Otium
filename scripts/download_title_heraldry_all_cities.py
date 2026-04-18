# -*- coding: utf-8 -*-
"""Download title-strip heraldry (coat + flag) for all known slugs."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_jerusalem_style_images import (
    add_download_image_args,
    download_jerusalem_style_images,
)
from scripts.city_guide_standard_whitelist import (
    url_is_whitelisted,
    whitelist_path_for_city,
)
from scripts.city_guide_title_heraldry_assets import (
    heraldry_slugs,
    title_page_assets_for_download_arg,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Download guide_coat / guide_flag from Commons for "
            "Jerusalem-style cities."
        ),
    )
    parser.add_argument(
        "--city",
        metavar="SLUG",
        default="",
        help="Process a single city slug (default: all).",
    )
    add_download_image_args(parser)
    args = parser.parse_args()
    failed = 0
    slugs = heraldry_slugs()
    if args.city.strip():
        want = args.city.strip()
        if want not in slugs:
            print("Unknown slug: {}".format(want), file=sys.stderr)
            return 2
        slugs = (want,)
    for slug in slugs:
        city_root = _PROJECT_ROOT / slug
        if not city_root.is_dir():
            print("skip (no tree): {}".format(slug), file=sys.stderr)
            continue
        wpath = whitelist_path_for_city(_PROJECT_ROOT, slug)
        assets = title_page_assets_for_download_arg(slug)
        if not assets:
            continue
        print("--- {} ---".format(slug))
        rc = download_jerusalem_style_images(
            city_root=city_root,
            places=(),
            whitelist_path=wpath,
            title_page_assets=assets,
            args=args,
            url_is_whitelisted_fn=url_is_whitelisted,
        )
        if rc != 0:
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
