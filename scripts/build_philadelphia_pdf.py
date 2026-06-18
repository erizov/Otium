# -*- coding: utf-8 -*-
"""HTML + PDF for Philadelphia from files under philadelphia/images/."""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from philadelphia.data.places_registry import PHILADELPHIA_PLACES

from scripts.city_guide_copy import install_guide_copy_patch
from scripts.city_guide_jerusalem_style_pdf import run_build_pdf_main
from scripts.city_guide_title_heraldry_assets import title_symbols_for_slug

_TITLE_SYMBOLS = title_symbols_for_slug("philadelphia")


def main() -> int:
    install_guide_copy_patch()
    return run_build_pdf_main(
        project_root=_PROJECT_ROOT,
        city_slug="philadelphia",
        city_root=_PROJECT_ROOT / "philadelphia",
        display_title="Philadelphia",
        title_symbols_class="philadelphia-title-symbols",
        title_symbols=_TITLE_SYMBOLS,
        places=list(PHILADELPHIA_PLACES),
        html_name="philadelphia_guide.html",
        pdf_name="philadelphia_guide.pdf",
        argv=sys.argv[1:],
    )


if __name__ == "__main__":
    raise SystemExit(main())
