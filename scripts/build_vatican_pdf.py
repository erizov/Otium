# -*- coding: utf-8 -*-
"""HTML + PDF for Vatican City from files under vatican/images/."""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from vatican.data.places_registry import VATICAN_PLACES

from scripts.city_guide_jerusalem_style_pdf import run_build_pdf_main

_TITLE_SYMBOLS: tuple[tuple[str, str], ...] = (
    (
        "images/guide_coat_of_arms.svg",
        "Coat of arms of Vatican City (Wikimedia Commons)",
    ),
    (
        "images/guide_flag.svg",
        "Flag of Vatican City (Wikimedia Commons)",
    ),
)


def main() -> int:
    return run_build_pdf_main(
        project_root=_PROJECT_ROOT,
        city_slug="vatican",
        city_root=_PROJECT_ROOT / "vatican",
        display_title="Vatican City",
        title_symbols_class="vatican-title-symbols",
        title_symbols=_TITLE_SYMBOLS,
        places=list(VATICAN_PLACES),
        html_name="vatican_guide.html",
        pdf_name="vatican_guide.pdf",
        argv=sys.argv[1:],
    )


if __name__ == "__main__":
    raise SystemExit(main())
