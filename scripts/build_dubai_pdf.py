# -*- coding: utf-8 -*-
"""HTML + PDF for Dubai."""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from dubai.data.places_registry import DUBAI_PLACES

from scripts.city_guide_jerusalem_style_pdf import run_build_pdf_main
from scripts.city_guide_title_heraldry_assets import (
    title_symbols_for_slug,
)

_TITLE_SYMBOLS = title_symbols_for_slug("dubai")


def main() -> int:
    return run_build_pdf_main(
        project_root=_PROJECT_ROOT,
        city_slug="dubai",
        city_root=_PROJECT_ROOT / "dubai",
        display_title="Dubai",
        title_symbols_class="dubai-title-symbols",
        title_symbols=_TITLE_SYMBOLS,
        places=list(DUBAI_PLACES),
        html_name="dubai_guide.html",
        pdf_name="dubai_guide.pdf",
        argv=sys.argv[1:],
    )


if __name__ == "__main__":
    raise SystemExit(main())
