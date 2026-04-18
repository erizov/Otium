# -*- coding: utf-8 -*-
"""HTML + PDF for Vladivostok."""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from vladivostok.data.places_registry import VLADIVOSTOK_PLACES

from scripts.city_guide_jerusalem_style_pdf import run_build_pdf_main
from scripts.city_guide_title_heraldry_assets import (
    title_symbols_for_slug,
)

_TITLE_SYMBOLS = title_symbols_for_slug("vladivostok")


def main() -> int:
    return run_build_pdf_main(
        project_root=_PROJECT_ROOT,
        city_slug="vladivostok",
        city_root=_PROJECT_ROOT / "vladivostok",
        display_title="Vladivostok",
        title_symbols_class="vladivostok-title-symbols",
        title_symbols=_TITLE_SYMBOLS,
        places=list(VLADIVOSTOK_PLACES),
        html_name="vladivostok_guide.html",
        pdf_name="vladivostok_guide.pdf",
        argv=sys.argv[1:],
    )


if __name__ == "__main__":
    raise SystemExit(main())
