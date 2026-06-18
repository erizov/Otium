# -*- coding: utf-8 -*-
"""HTML + PDF for Montreal from files under montreal/images/."""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from montreal.data.places_registry import MONTREAL_PLACES

from scripts.city_guide_copy import install_guide_copy_patch
from scripts.city_guide_jerusalem_style_pdf import run_build_pdf_main
from scripts.city_guide_title_heraldry_assets import title_symbols_for_slug

_TITLE_SYMBOLS = title_symbols_for_slug("montreal")


def main() -> int:
    install_guide_copy_patch()
    return run_build_pdf_main(
        project_root=_PROJECT_ROOT,
        city_slug="montreal",
        city_root=_PROJECT_ROOT / "montreal",
        display_title="Montreal",
        title_symbols_class="montreal-title-symbols",
        title_symbols=_TITLE_SYMBOLS,
        places=list(MONTREAL_PLACES),
        html_name="montreal_guide.html",
        pdf_name="montreal_guide.pdf",
        argv=sys.argv[1:],
    )


if __name__ == "__main__":
    raise SystemExit(main())
