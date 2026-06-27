# -*- coding: utf-8 -*-
"""Download Russian Architecture guide images."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from russian_arhitecture.data.places_registry import RUSSIAN_ARHITECTURE_PLACES
from russian_arhitecture.whitelist import default_whitelist_path
from russian_arhitecture.whitelist import url_is_whitelisted

from scripts.city_guide_jerusalem_style_images import (
    add_download_image_args,
    download_jerusalem_style_images,
)
from scripts.city_guide_title_heraldry_assets import (
    title_page_assets_for_download_arg,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download Russian Architecture guide images.",
    )
    parser.add_argument(
        "--russian_arhitecture-root",
        type=Path,
        default=_PROJECT_ROOT / "russian_arhitecture",
        dest="city_root",
        help="russian_arhitecture tree root",
    )
    add_download_image_args(parser)
    args = parser.parse_args()
    return download_jerusalem_style_images(
        city_root=args.city_root,
        places=RUSSIAN_ARHITECTURE_PLACES,
        whitelist_path=default_whitelist_path(),
        title_page_assets=title_page_assets_for_download_arg("russian_arhitecture"),
        args=args,
        url_is_whitelisted_fn=url_is_whitelisted,
    )


if __name__ == "__main__":
    raise SystemExit(main())
