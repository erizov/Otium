# -*- coding: utf-8 -*-
"""Create minimal per-city guide package (folders, registry, scripts)."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

_INIT = "# -*- coding: utf-8 -*-\n"
_WHITELIST = '''# -*- coding: utf-8 -*-
"""Image source URL checks for {slug}."""

from __future__ import annotations

from pathlib import Path

from scripts.city_guide_standard_whitelist import clear_whitelist_cache
from scripts.city_guide_standard_whitelist import url_is_whitelisted

__all__ = [
    "clear_whitelist_cache",
    "default_whitelist_path",
    "url_is_whitelisted",
]


def default_whitelist_path() -> Path:
    return Path(__file__).resolve().parent / "docs" / "SOURCES_WHITELIST.md"
'''

_SOURCES_MD = """# Allowed image source prefixes

Wikimedia Commons and Wikipedia are allowed by the shared validator.

Add HTTPS prefixes below as you expand sources:

https://www.example.org/
"""

_README_TEMPLATE = """# {display} guide

```bash
python scripts/download_{slug}_images.py
python scripts/validate_{slug}_sources.py
python scripts/build_{slug}_pdf.py --html-only
```
"""


def _registry_body(slug: str, display: str) -> str:
    attr = slug.upper() + "_PLACES"
    return '''# -*- coding: utf-8 -*-
"""{display} guide registry."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict, cast


class CityPlace(TypedDict, total=False):
    slug: str
    category: str
    suppress_images_for_pdf: bool
    name_en: str
    subtitle_en: str
    image_rel_path: str
    image_source_url: str
    license_note: str
    attribution: str
    address: str
    year_built: str
    architecture_style: str
    description: str
    history: str
    significance: str
    facts: list[str]
    stories: list[str]


def _load_detail_slugs() -> dict[str, dict]:
    base = Path(__file__).parent
    merged: dict[str, dict] = {{}}
    for path in sorted(base.glob("{slug}_place_details*.json")):
        blob = json.loads(path.read_text(encoding="utf-8"))
        merged.update(blob)
    return merged


def _merge_details(rows: list[dict]) -> list[dict]:
    extra = _load_detail_slugs()
    if not extra:
        return rows
    skip_merge = frozenset({{"additional_images"}})
    for row in rows:
        block = extra.get(row.get("slug"))
        if not block:
            continue
        for key, val in block.items():
            if key in skip_merge:
                continue
            if val in (None, "", [], {{}}):
                continue
            row[key] = val
    return rows


def _load_places() -> list[CityPlace]:
    path = Path(__file__).with_name("{slug}_places.json")
    raw: list[dict] = json.loads(path.read_text(encoding="utf-8"))
    raw = _merge_details(raw)
    return cast(list[CityPlace], raw)


{attr}: list[CityPlace] = _load_places()
'''.format(display=display, slug=slug, attr=attr)


def _download_body(slug: str, display: str) -> str:
    attr = slug.upper() + "_PLACES"
    return '''# -*- coding: utf-8 -*-
"""Download {display} guide images."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from {slug}.data.places_registry import {attr}
from {slug}.whitelist import default_whitelist_path
from {slug}.whitelist import url_is_whitelisted

from scripts.city_guide_jerusalem_style_images import (
    add_download_image_args,
)
from scripts.city_guide_jerusalem_style_images import (
    download_jerusalem_style_images,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download {display} guide images.",
    )
    parser.add_argument(
        "--{slug}-root",
        type=Path,
        default=_PROJECT_ROOT / "{slug}",
        dest="city_root",
        help="{slug} tree root",
    )
    add_download_image_args(parser)
    args = parser.parse_args()
    return download_jerusalem_style_images(
        city_root=args.city_root,
        places={attr},
        whitelist_path=default_whitelist_path(),
        title_page_assets=(),
        args=args,
        url_is_whitelisted_fn=url_is_whitelisted,
    )


if __name__ == "__main__":
    raise SystemExit(main())
'''.format(display=display, slug=slug, attr=attr)


def _validate_body(slug: str, display: str) -> str:
    attr = slug.upper() + "_PLACES"
    return '''# -*- coding: utf-8 -*-
"""Validate {display} image_source_url entries."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from {slug}.data.places_registry import {attr}
from {slug}.whitelist import default_whitelist_path
from {slug}.whitelist import url_is_whitelisted

from scripts.city_guide_jerusalem_style_images import (
    validate_jerusalem_style_urls,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--whitelist", type=Path, default=None)
    args = parser.parse_args()
    wpath = args.whitelist or default_whitelist_path()
    return validate_jerusalem_style_urls(
        {attr},
        whitelist_path=wpath,
        url_is_whitelisted_fn=url_is_whitelisted,
        city_label="{display}",
    )


if __name__ == "__main__":
    raise SystemExit(main())
'''.format(display=display, slug=slug, attr=attr)


def _build_body(slug: str, display: str) -> str:
    attr = slug.upper() + "_PLACES"
    return '''# -*- coding: utf-8 -*-
"""HTML + PDF for {display}."""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from {slug}.data.places_registry import {attr}

from scripts.city_guide_jerusalem_style_pdf import run_build_pdf_main

_TITLE_SYMBOLS: tuple[tuple[str, str], ...] = (
    (
        "images/guide_coat_of_arms.svg",
        "City emblem (local seed SVG)",
    ),
    (
        "images/guide_flag.svg",
        "Flag (local seed SVG)",
    ),
)


def main() -> int:
    return run_build_pdf_main(
        project_root=_PROJECT_ROOT,
        city_slug="{slug}",
        city_root=_PROJECT_ROOT / "{slug}",
        display_title="{display}",
        title_symbols_class="{slug}-title-symbols",
        title_symbols=_TITLE_SYMBOLS,
        places=list({attr}),
        html_name="{slug}_guide.html",
        pdf_name="{slug}_guide.pdf",
        argv=sys.argv[1:],
    )


if __name__ == "__main__":
    raise SystemExit(main())
'''.format(display=display, slug=slug, attr=attr)


def scaffold(slug: str, display: str) -> None:
    root = _PROJECT_ROOT / slug
    marker = root / "data" / "places_registry.py"
    if marker.is_file():
        print("skip (already scaffolded):", slug)
        return
    (root / "data").mkdir(parents=True, exist_ok=True)
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "images").mkdir(parents=True, exist_ok=True)
    (root / "output").mkdir(parents=True, exist_ok=True)
    (root / "__init__.py").write_text(_INIT, encoding="utf-8")
    (root / "whitelist.py").write_text(
        _WHITELIST.format(slug=slug),
        encoding="utf-8",
    )
    (root / "docs" / "SOURCES_WHITELIST.md").write_text(
        _SOURCES_MD,
        encoding="utf-8",
    )
    (root / "data" / "places_registry.py").write_text(
        _registry_body(slug, display),
        encoding="utf-8",
    )
    (root / "README.md").write_text(
        _README_TEMPLATE.format(slug=slug, display=display),
        encoding="utf-8",
    )
    (root / "output" / ".gitkeep").write_text("", encoding="utf-8")
    src_svg = _PROJECT_ROOT / "dublin" / "images"
    for name in ("guide_coat_of_arms.svg", "guide_flag.svg"):
        shutil.copy2(src_svg / name, root / "images" / name)
    scripts = _PROJECT_ROOT / "scripts"
    (scripts / "download_{}_images.py".format(slug)).write_text(
        _download_body(slug, display),
        encoding="utf-8",
    )
    (scripts / "validate_{}_sources.py".format(slug)).write_text(
        _validate_body(slug, display),
        encoding="utf-8",
    )
    (scripts / "build_{}_pdf.py".format(slug)).write_text(
        _build_body(slug, display),
        encoding="utf-8",
    )
    print("scaffolded", slug)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug")
    parser.add_argument("display")
    args = parser.parse_args()
    scaffold(args.slug, args.display)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
