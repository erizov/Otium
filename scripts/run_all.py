# -*- coding: utf-8 -*-
"""
Single entry point: fill image URLs (optional), then build all guides
using existing images (or optionally download first).

Usage:
  python scripts/run_all.py [--fill-urls] [--download-images]

  --fill-urls: run fill_image_urls.py first to populate data/*_image_urls.py
    by place name (Commons, Pixabay, Pexels, Openverse, Flickr, Unsplash,
    Yandex). Skip if URLs are already filled or you use Yandex-only generation.

  --download-images: download missing images for every guide before building.
    If omitted, only existing images in output/images/<subdir> are used.

Then runs build_pdf.py --all-guides (with --build-only --build-with-available
unless --download-images). Places with no images omit the image block.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.guide_workflow import run_build_all_guides


def main() -> int:
    """Run fill-urls (optional), then build using existing or downloaded images."""
    fill_urls = "--fill-urls" in sys.argv
    download_images = "--download-images" in sys.argv
    if fill_urls:
        fill_script = _SCRIPT_DIR / "fill_image_urls.py"
        if not fill_script.is_file():
            print("Error: fill_image_urls.py not found.", file=sys.stderr)
            return 1
        print("--- Filling image URLs by place name (all guides) ---")
        ret = subprocess.call(
            [sys.executable, str(fill_script)],
            cwd=str(_PROJECT_ROOT),
        )
        if ret != 0:
            return ret

    if download_images:
        print("\n--- Download images + build all guides ---")
    else:
        print("\n--- Build all guides (using existing images only) ---")
    return run_build_all_guides(download_images=download_images)


if __name__ == "__main__":
    sys.exit(main())
