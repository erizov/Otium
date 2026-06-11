# -*- coding: utf-8 -*-
"""Moscow per-city guide (HTML/PDF) or optional legacy combined Moscow book."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_jerusalem_style_pdf import run_build_pdf_main
from scripts.city_guide_title_heraldry_assets import title_symbols_for_slug
from scripts.moscow_title_assets_data import install_moscow_bundled_assets
from webapp.server.city_store import load_city_places


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Moscow city guide under moscow/output/ (default), or legacy "
            "Moscow_Complete_Guide under output/."
        ),
    )
    parser.add_argument(
        "--export-places",
        action="store_true",
        help=(
            "Regenerate moscow/data/moscow_places.json from data/*.py "
            "registries (no guide build)."
        ),
    )
    parser.add_argument(
        "--moscow-complete-guide",
        action="store_true",
        help=(
            "Delegate to scripts/build_full_guide.py (large combined book; "
            "passes through extra args)."
        ),
    )
    args, rest = parser.parse_known_args()
    if args.export_places:
        return subprocess.call(
            [
                sys.executable,
                str(_PROJECT_ROOT / "scripts" / "export_moscow_webapp_places.py"),
            ],
            cwd=str(_PROJECT_ROOT),
        )
    if args.moscow_complete_guide:
        cmd = [sys.executable, str(_PROJECT_ROOT / "scripts" / "build_full_guide.py")]
        if rest:
            cmd.extend(rest)
        return subprocess.call(cmd, cwd=str(_PROJECT_ROOT))

    moscow_root = _PROJECT_ROOT / "moscow"
    install_moscow_bundled_assets(moscow_root)
    places = load_city_places(_PROJECT_ROOT, "moscow")
    return run_build_pdf_main(
        project_root=_PROJECT_ROOT,
        city_slug="moscow",
        city_root=_PROJECT_ROOT / "moscow",
        display_title="Moscow",
        title_symbols_class="moscow-title-symbols",
        title_symbols=title_symbols_for_slug("moscow"),
        places=places,
        html_name="moscow_guide.html",
        pdf_name="moscow_guide.pdf",
        argv=rest,
    )


if __name__ == "__main__":
    raise SystemExit(main())
