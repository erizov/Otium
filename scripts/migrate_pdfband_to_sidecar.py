# -*- coding: utf-8 -*-
"""Move legacy pdfband rows from main places JSON into PDF expand sidecar."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_naming import is_pdf_filler_slug
from scripts.city_guide_naming import pdf_expand_sidecar_filename
from scripts.rebuild_stale_city_guide_pdfs import _discover_slugs


def migrate_city(project_root: Path, city_slug: str, *, dry_run: bool) -> int:
    main_path = project_root / city_slug / "data" / "{}_places.json".format(
        city_slug,
    )
    if not main_path.is_file():
        return 0
    rows = json.loads(main_path.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        return 0
    curated: list[dict] = []
    fillers: list[dict] = []
    for row in rows:
        slug = str(row.get("slug") or "")
        if is_pdf_filler_slug(slug):
            fillers.append(row)
        else:
            curated.append(row)
    if not fillers:
        return 0
    sidecar_name = pdf_expand_sidecar_filename(city_slug)
    sidecar_path = main_path.parent / sidecar_name
    prev: list[dict] = []
    if sidecar_path.is_file():
        prev = json.loads(sidecar_path.read_text(encoding="utf-8"))
    merged = prev + fillers
    print(
        "{}: move {} filler row(s) -> {}".format(
            city_slug,
            len(fillers),
            sidecar_name,
        ),
    )
    if dry_run:
        return len(fillers)
    bak = main_path.with_suffix(main_path.suffix + ".bak")
    if not bak.is_file():
        shutil.copy2(main_path, bak)
    main_path.write_text(
        json.dumps(curated, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    sidecar_path.write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return len(fillers)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cities", nargs="*", default=None, metavar="SLUG")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = _PROJECT_ROOT
    cities = _discover_slugs(root)
    if args.cities:
        cities = [c for c in cities if c in set(args.cities)]
    total = 0
    for slug in cities:
        total += migrate_city(root, slug, dry_run=args.dry_run)
    print("Moved {} filler row(s) total.".format(total))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
