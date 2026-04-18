# -*- coding: utf-8 -*-
"""HTML + PDF for Copenhagen."""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from copenhagen.data.places_registry import COPENHAGEN_PLACES

from scripts.city_guide_jerusalem_style_pdf import run_build_pdf_main
from scripts.city_guide_title_heraldry_assets import (
    title_symbols_for_slug,
)

_TITLE_SYMBOLS = title_symbols_for_slug("copenhagen")


def main() -> int:
    return run_build_pdf_main(
        project_root=_PROJECT_ROOT,
        city_slug="copenhagen",
        city_root=_PROJECT_ROOT / "copenhagen",
        display_title="Copenhagen",
        title_symbols_class="copenhagen-title-symbols",
        title_symbols=_TITLE_SYMBOLS,
        places=list(COPENHAGEN_PLACES),
        html_name="copenhagen_guide.html",
        pdf_name="copenhagen_guide.pdf",
        argv=sys.argv[1:],
    )


if __name__ == "__main__":
    raise SystemExit(main())
