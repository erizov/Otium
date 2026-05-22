# -*- coding: utf-8 -*-
"""HTML + PDF for Florence from files under florence/images/."""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from florence.data.places_registry import FLORENCE_PLACES

from scripts.city_guide_jerusalem_style_pdf import run_build_pdf_main
from scripts.city_guide_title_heraldry_assets import title_symbols_for_slug

_TITLE_SYMBOLS = title_symbols_for_slug("florence")


def main() -> int:
    return run_build_pdf_main(
        project_root=_PROJECT_ROOT,
        city_slug="florence",
        city_root=_PROJECT_ROOT / "florence",
        display_title="Florence",
        title_symbols_class="florence-title-symbols",
        title_symbols=_TITLE_SYMBOLS,
        places=list(FLORENCE_PLACES),
        html_name="florence_guide.html",
        pdf_name="florence_guide.pdf",
        argv=sys.argv[1:],
    )


if __name__ == "__main__":
    raise SystemExit(main())
