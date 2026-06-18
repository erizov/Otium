# -*- coding: utf-8 -*-
"""Download Moscow guide images (Commons + culture.ru URLs in places JSON)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from moscow.whitelist import default_whitelist_path
from moscow.whitelist import url_is_whitelisted

from scripts.city_guide_jerusalem_style_images import (
    add_download_image_args,
    download_jerusalem_style_images,
)
from scripts.city_guide_title_heraldry_assets import (
    title_page_assets_for_download_arg,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--moscow-root",
        type=Path,
        default=_PROJECT_ROOT / "moscow",
        dest="city_root",
    )
    add_download_image_args(parser)
    args = parser.parse_args()
    places_path = args.city_root / "data" / "moscow_places.json"
    places = json.loads(places_path.read_text(encoding="utf-8"))
    return download_jerusalem_style_images(
        city_root=args.city_root,
        places=places,
        whitelist_path=default_whitelist_path(),
        title_page_assets=title_page_assets_for_download_arg("moscow"),
        args=args,
        url_is_whitelisted_fn=url_is_whitelisted,
        city_slug="moscow",
    )


if __name__ == "__main__":
    raise SystemExit(main())
