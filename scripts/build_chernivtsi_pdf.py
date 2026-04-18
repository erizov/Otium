# -*- coding: utf-8 -*-
"""HTML + PDF for Chernivtsi."""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from chernivtsi.data.places_registry import CHERNIVTSI_PLACES

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
        city_slug="chernivtsi",
        city_root=_PROJECT_ROOT / "chernivtsi",
        display_title="Chernivtsi",
        title_symbols_class="chernivtsi-title-symbols",
        title_symbols=_TITLE_SYMBOLS,
        places=list(CHERNIVTSI_PLACES),
        html_name="chernivtsi_guide.html",
        pdf_name="chernivtsi_guide.pdf",
        argv=sys.argv[1:],
    )


if __name__ == "__main__":
    raise SystemExit(main())
