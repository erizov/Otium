# -*- coding: utf-8 -*-
"""
Build only: all guides using existing images, 3 images + map per item.
With dedup checking and optimizing large (>500KB) images (originals moved to
large_orig).

Steps:
  1. Run dedup_all_folders.py (per-folder duplicate detection, move dupes).
  2. Compress images > 500KB: copy original to large_orig/, then overwrite with
     compressed version.
  3. Run build_pdf.py --all-guides --optimized --build-only --build-with-available

Output: output/<guide>_guide_opt.html and output/<guide>_guide_opt.pdf per guide.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.guide_workflow import (
    run_build_all_guides,
    run_compress_large,
    run_dedup,
)


def main() -> int:
    print("Step 1: Dedup (move duplicates to duplicates/)...")
    ret = run_dedup()
    if ret != 0:
        print("Dedup failed.", file=sys.stderr)
        return ret

    print("\nStep 2: Compress images > 500KB (originals in large_orig/)...")
    n = run_compress_large()
    print("  Compressed {} image(s).".format(n))

    print("\nStep 3: Build all guides (optimized, 3 images + map)...")
    return run_build_all_guides(
        optimized=True,
        build_only=True,
        build_with_available=True,
    )


if __name__ == "__main__":
    sys.exit(main())
