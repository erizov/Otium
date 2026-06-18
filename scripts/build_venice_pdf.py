# -*- coding: utf-8 -*-
"""HTML + PDF for Venice from files under venice/images/."""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from venice.data.places_registry import VENICE_PLACES

from scripts.city_guide_copy import install_guide_copy_patch
from scripts.city_guide_jerusalem_style_pdf import run_build_pdf_main
from scripts.city_guide_title_heraldry_assets import title_symbols_for_slug

_TITLE_SYMBOLS = title_symbols_for_slug("venice")


def main() -> int:
    install_guide_copy_patch()
    return run_build_pdf_main(
        project_root=_PROJECT_ROOT,
        city_slug="venice",
        city_root=_PROJECT_ROOT / "venice",
        display_title="Venice",
        title_symbols_class="venice-title-symbols",
        title_symbols=_TITLE_SYMBOLS,
        places=list(VENICE_PLACES),
        html_name="venice_guide.html",
        pdf_name="venice_guide.pdf",
        argv=sys.argv[1:],
    )


if __name__ == "__main__":
    raise SystemExit(main())
