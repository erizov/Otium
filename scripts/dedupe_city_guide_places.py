# -*- coding: utf-8 -*-
"""
Remove duplicate place rows within each city guide (JSON source).

Keeps the first curated row per heading (city-aware) or image URL.
Also trims pdf_expand sidecar rows that duplicate curated places.

Usage::

  python scripts/dedupe_city_guide_places.py --dry-run
  python scripts/dedupe_city_guide_places.py --write
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_core import dedupe_curated_places, dedupe_pdf_sidecar_places
from scripts.city_guide_naming import is_pdf_filler_slug
from scripts.city_guide_registry_common import pdf_expand_sidecar_paths


def _load(path: Path) -> list[dict]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        return []
    return [p for p in raw if isinstance(p, dict)]


def _write(path: Path, rows: list[dict]) -> None:
    path.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def dedupe_city(
    city_slug: str,
    *,
    write: bool,
) -> tuple[int, int, list[str]]:
    """Return (removed_main, removed_expand, log lines)."""
    data_dir = _PROJECT_ROOT / city_slug / "data"
    main_path = data_dir / "{}_places.json".format(city_slug)
    if not main_path.is_file():
        return 0, 0, []

    main = _load(main_path)
    deduped_main = dedupe_curated_places(main, city_slug)
    removed_main = len(main) - len(deduped_main)

    expand_paths = pdf_expand_sidecar_paths(data_dir, city_slug)
    removed_expand = 0
    logs: list[str] = []
    kept_main_slugs = {str(p.get("slug") or "") for p in deduped_main}
    dropped_main = [
        p for p in main
        if str(p.get("slug") or "") not in kept_main_slugs
    ]
    for p in dropped_main:
        logs.append(
            "  drop main {} ({})".format(
                p.get("slug"),
                p.get("name_en") or p.get("name_ru") or "?",
            ),
        )

    new_expand_by_path: dict[Path, list[dict]] = {}
    for expand_path in expand_paths:
        if not expand_path.is_file():
            continue
        expand = _load(expand_path)
        merged = dedupe_pdf_sidecar_places(
            deduped_main + expand,
            city_slug=city_slug,
        )
        kept_expand_slugs = {
            str(p.get("slug") or "")
            for p in merged
            if is_pdf_filler_slug(str(p.get("slug") or ""))
        }
        deduped_expand = [
            p for p in expand
            if str(p.get("slug") or "") in kept_expand_slugs
        ]
        n = len(expand) - len(deduped_expand)
        removed_expand += n
        for p in expand:
            slug = str(p.get("slug") or "")
            if slug and slug not in kept_expand_slugs:
                logs.append("  drop expand {} ({})".format(
                    slug,
                    p.get("name_en") or p.get("subtitle_en") or "?",
                ))
        new_expand_by_path[expand_path] = deduped_expand

    if write:
        if removed_main:
            _write(main_path, deduped_main)
        for path, rows in new_expand_by_path.items():
            if _load(path) != rows:
                _write(path, rows)

    return removed_main, removed_expand, logs


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (AttributeError, OSError, ValueError):
            pass
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cities",
        nargs="*",
        default=None,
        metavar="SLUG",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write deduplicated JSON (default: dry-run report only).",
    )
    args = parser.parse_args()

    if args.cities:
        cities = sorted(args.cities)
    else:
        cities = sorted(
            p.parent.parent.name
            for p in _PROJECT_ROOT.glob("*/data/*_places.json")
        )

    total_main = 0
    total_expand = 0
    affected = 0
    for city in cities:
        rm, re, logs = dedupe_city(city, write=bool(args.write))
        if rm or re:
            affected += 1
            print("{}: -{} main, -{} expand".format(city, rm, re))
            for line in logs:
                print(line)
        total_main += rm
        total_expand += re

    mode = "write" if args.write else "dry-run"
    print(
        "--- {} ---".format(mode),
        "cities affected:",
        affected,
        "main rows removed:",
        total_main,
        "expand rows removed:",
        total_expand,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
