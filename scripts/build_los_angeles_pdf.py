# -*- coding: utf-8 -*-
"""HTML + PDF for Los Angeles."""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from los_angeles.data.places_registry import LOS_ANGELES_PLACES

from scripts.city_guide_jerusalem_style_pdf import run_build_pdf_main

_TITLE_SYMBOLS: tuple[tuple[str, str], ...] = (
    (
        "images/guide_coat_of_arms.svg",
        "City emblem (local seed SVG)",
    ),
    (
        "images/guide_flag.svg",
        "Flag (local seed SVG)",
    ),
)


def main() -> int:
    return run_build_pdf_main(
        project_root=_PROJECT_ROOT,
        city_slug="los_angeles",
        city_root=_PROJECT_ROOT / "los_angeles",
        display_title="Los Angeles",
        title_symbols_class="los_angeles-title-symbols",
        title_symbols=_TITLE_SYMBOLS,
        places=list(LOS_ANGELES_PLACES),
        html_name="los_angeles_guide.html",
        pdf_name="los_angeles_guide.pdf",
        argv=sys.argv[1:],
    )


if __name__ == "__main__":
    raise SystemExit(main())
