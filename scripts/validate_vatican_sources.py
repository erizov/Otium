# -*- coding: utf-8 -*-
"""Validate Vatican image_source_url entries against the whitelist."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from vatican.data.places_registry import VATICAN_PLACES
from vatican.whitelist import default_whitelist_path
from vatican.whitelist import url_is_whitelisted

from scripts.city_guide_jerusalem_style_images import validate_jerusalem_style_urls


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate Vatican place image_source_url against "
            "SOURCES_WHITELIST.md."
        ),
    )
    parser.add_argument(
        "--whitelist",
        type=Path,
        default=None,
        help="Override path to SOURCES_WHITELIST.md",
    )
    args = parser.parse_args()
    wpath = args.whitelist or default_whitelist_path()
    return validate_jerusalem_style_urls(
        VATICAN_PLACES,
        whitelist_path=wpath,
        url_is_whitelisted_fn=url_is_whitelisted,
        city_label="Vatican",
    )


if __name__ == "__main__":
    raise SystemExit(main())
