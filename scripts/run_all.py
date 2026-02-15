# -*- coding: utf-8 -*-
"""
Single entry point: fill image URLs (optional), download all images,
then build all guides.

Usage:
  python scripts/run_all.py [--fill-urls]

  --fill-urls: run fill_image_urls.py first to populate data/*_image_urls.py
    by place name (Commons, Pixabay, Pexels, Openverse, Flickr, Unsplash,
    Yandex). Skip if URLs are already filled or you use Yandex-only generation.

Then runs build_pdf.py --all-guides: downloads images for every guide,
then builds HTML/PDF. Places with no images show no placeholder — the image
block is omitted.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent


def main() -> int:
    """Run fill-urls (optional), download all, then build all guides."""
    fill_urls = "--fill-urls" in sys.argv
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

    build_script = _SCRIPT_DIR / "build_pdf.py"
    if not build_script.is_file():
        print("Error: build_pdf.py not found.", file=sys.stderr)
        return 1
    print("\n--- Download images + build all guides ---")
    cmd = [
        sys.executable,
        str(build_script),
        "--all-guides",
    ]
    ret = subprocess.call(cmd, cwd=str(_PROJECT_ROOT))
    return ret


if __name__ == "__main__":
    sys.exit(main())
