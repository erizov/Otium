# -*- coding: utf-8 -*-
"""HTML + PDF for Jerusalem from files under jerusalem/images/."""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from jerusalem.data.places_registry import JERUSALEM_PLACES

from scripts.city_guide_jerusalem_style_pdf import run_build_pdf_main
from scripts.city_guide_title_heraldry_assets import title_symbols_for_slug

_TITLE_SYMBOLS = title_symbols_for_slug("jerusalem")


def main() -> int:
    return run_build_pdf_main(
        project_root=_PROJECT_ROOT,
        city_slug="jerusalem",
        city_root=_PROJECT_ROOT / "jerusalem",
        display_title="Jerusalem",
        title_symbols_class="jerusalem-title-symbols",
        title_symbols=_TITLE_SYMBOLS,
        places=list(JERUSALEM_PLACES),
        html_name="jerusalem_guide.html",
        pdf_name="jerusalem_guide.pdf",
        argv=sys.argv[1:],
    )


if __name__ == "__main__":
    raise SystemExit(main())
