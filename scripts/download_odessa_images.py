# -*- coding: utf-8 -*-
"""Download Odessa guide images."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from odessa.data.places_registry import ODESSA_PLACES
from odessa.whitelist import default_whitelist_path
from odessa.whitelist import url_is_whitelisted

from scripts.city_guide_jerusalem_style_images import (
    add_download_image_args,
    download_jerusalem_style_images,
)
from scripts.city_guide_title_heraldry_assets import (
    title_page_assets_for_download_arg,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download Odessa guide images.",
    )
    parser.add_argument(
        "--odessa-root",
        type=Path,
        default=_PROJECT_ROOT / "odessa",
        dest="city_root",
        help="odessa tree root",
    )
    add_download_image_args(parser)
    args = parser.parse_args()
    return download_jerusalem_style_images(
        city_root=args.city_root,
        places=ODESSA_PLACES,
        whitelist_path=default_whitelist_path(),
        title_page_assets=title_page_assets_for_download_arg("odessa"),
        args=args,
        url_is_whitelisted_fn=url_is_whitelisted,
    )


if __name__ == "__main__":
    raise SystemExit(main())
