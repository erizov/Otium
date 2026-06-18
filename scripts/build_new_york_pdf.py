# -*- coding: utf-8 -*-
"""HTML + PDF for New York from files under new_york/images/."""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from new_york.data.places_registry import NEW_YORK_PLACES

from scripts.city_guide_copy import install_guide_copy_patch
from scripts.city_guide_jerusalem_style_pdf import run_build_pdf_main
from scripts.city_guide_title_heraldry_assets import title_symbols_for_slug

_TITLE_SYMBOLS = title_symbols_for_slug("new_york")


def main() -> int:
    install_guide_copy_patch()
    return run_build_pdf_main(
        project_root=_PROJECT_ROOT,
        city_slug="new_york",
        city_root=_PROJECT_ROOT / "new_york",
        display_title="New York",
        title_symbols_class="new_york-title-symbols",
        title_symbols=_TITLE_SYMBOLS,
        places=list(NEW_YORK_PLACES),
        html_name="new_york_guide.html",
        pdf_name="new_york_guide.pdf",
        argv=sys.argv[1:],
    )


if __name__ == "__main__":
    raise SystemExit(main())
