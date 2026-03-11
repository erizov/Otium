# -*- coding: utf-8 -*-
"""
Build only: all guides using existing images, 3 images + map per item.
No dedup checking, no image optimization.

Runs: build_pdf.py --all-guides --optimized --build-only --build-with-available
Output: output/<guide>_guide_opt.html and output/<guide>_guide_opt.pdf per guide.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.guide_workflow import run_build_all_guides


def main() -> int:
    return run_build_all_guides(
        optimized=True,
        build_only=True,
        build_with_available=True,
    )


if __name__ == "__main__":
    sys.exit(main())
