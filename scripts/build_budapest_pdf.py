# -*- coding: utf-8 -*-
"""HTML + PDF for Budapest from files under budapest/images/."""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from budapest.data.places_registry import BUDAPEST_PLACES

from scripts.city_guide_copy import install_guide_copy_patch
from scripts.city_guide_jerusalem_style_pdf import run_build_pdf_main
from scripts.city_guide_title_heraldry_assets import title_symbols_for_slug

_TITLE_SYMBOLS = title_symbols_for_slug("budapest")


def main() -> int:
    install_guide_copy_patch()
    return run_build_pdf_main(
        project_root=_PROJECT_ROOT,
        city_slug="budapest",
        city_root=_PROJECT_ROOT / "budapest",
        display_title="Budapest",
        title_symbols_class="budapest-title-symbols",
        title_symbols=_TITLE_SYMBOLS,
        places=list(BUDAPEST_PLACES),
        html_name="budapest_guide.html",
        pdf_name="budapest_guide.pdf",
        argv=sys.argv[1:],
    )


if __name__ == "__main__":
    raise SystemExit(main())
