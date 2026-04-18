# -*- coding: utf-8 -*-
"""Download singapore guide images."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from singapore.data.places_registry import SINGAPORE_PLACES
from singapore.whitelist import default_whitelist_path
from singapore.whitelist import url_is_whitelisted

from scripts.city_guide_jerusalem_style_images import (
    add_download_image_args,
)
from scripts.city_guide_jerusalem_style_images import (
    download_jerusalem_style_images,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download singapore guide images.",
    )
    parser.add_argument(
        "--singapore-root",
        type=Path,
        default=_PROJECT_ROOT / "singapore",
        dest="city_root",
        help="singapore tree root",
    )
    add_download_image_args(parser)
    args = parser.parse_args()
    return download_jerusalem_style_images(
        city_root=args.city_root,
        places=SINGAPORE_PLACES,
        whitelist_path=default_whitelist_path(),
        title_page_assets=(),
        args=args,
        url_is_whitelisted_fn=url_is_whitelisted,
    )


if __name__ == "__main__":
    raise SystemExit(main())
