# -*- coding: utf-8 -*-
"""Validate dubai image_source_url entries."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from dubai.data.places_registry import DUBAI_PLACES
from dubai.whitelist import default_whitelist_path
from dubai.whitelist import url_is_whitelisted

from scripts.city_guide_jerusalem_style_images import (
    validate_jerusalem_style_urls,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--whitelist", type=Path, default=None)
    args = parser.parse_args()
    wpath = args.whitelist or default_whitelist_path()
    return validate_jerusalem_style_urls(
        DUBAI_PLACES,
        whitelist_path=wpath,
        url_is_whitelisted_fn=url_is_whitelisted,
        city_label="Dubai",
    )


if __name__ == "__main__":
    raise SystemExit(main())
