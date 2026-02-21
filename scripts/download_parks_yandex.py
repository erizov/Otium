# -*- coding: utf-8 -*-
"""
Download first 4 Yandex images for parks missing images.

Saves as JPG in output/images/moscow_parks/ with naming: <slug>_1.jpg .. _4.jpg.
"""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from data.parks import PARKS, IMAGES_SUBFOLDER
from scripts.download_yandex_common import download_yandex_for_guide


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(
        description="Download first 4 Yandex images for parks missing images."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=_PROJECT_ROOT / "output",
        help="Output directory (default: output/).",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-headless", action="store_true")
    args = parser.parse_args()
    n = download_yandex_for_guide(
        "Park",
        PARKS,
        IMAGES_SUBFOLDER,
        args.output_dir,
        images_per_place=4,
        dry_run=args.dry_run,
        city="Москва",
        extra_query_word="парк",
    )
    print("Parks updated: {}".format(n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
