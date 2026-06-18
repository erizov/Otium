# -*- coding: utf-8 -*-
"""Rename non-descriptive PDF-expand slugs (numeric IDs, wrong-city titles)."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_naming import descriptive_place_slug
from scripts.city_guide_naming import clean_place_display_title
from scripts.city_guide_naming import title_for_descriptive_slug
from scripts.city_guide_registry_common import pdf_expand_sidecar_paths
from scripts.migrate_legacy_city_slugs import _rename_images
from scripts.migrate_legacy_city_slugs import _update_rel_path
from scripts.rebuild_stale_city_guide_pdfs import _discover_slugs


_BAD_TOKEN_RE = re.compile(r"(?:^|_)\d{7,}(?:_|$)")


def _is_bad(slug: str, city_slug: str = "") -> bool:
    s = str(slug or "").strip().lower()
    city = city_slug.strip().lower()
    if not s:
        return False
    if _BAD_TOKEN_RE.search(s):
        return True
    parts = s.split("_")
    if len(parts) >= 2 and parts[-1].isdigit() and len(parts[-1]) >= 6:
        return True
    if city and s.startswith(city + "_"):
        tail = s[len(city) + 1 :]
        if tail in (city, "place") or re.fullmatch(r"\d+", tail or ""):
            return True
    return False


def _load_rows(paths: tuple[Path, ...]) -> list[dict]:
    rows: list[dict] = []
    for p in paths:
        if not p.is_file():
            continue
        blob = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(blob, list):
            rows.extend([r for r in blob if isinstance(r, dict)])
    return rows


def _mapping_for_city(city_slug: str, data_dir: Path) -> dict[str, str]:
    sidecars = pdf_expand_sidecar_paths(data_dir, city_slug)
    rows = _load_rows(sidecars)
    used = {str(r.get("slug") or "").strip() for r in rows if r.get("slug")}
    mapping: dict[str, str] = {}
    for row in rows:
        old = str(row.get("slug") or "").strip()
        if not _is_bad(old, city_slug):
            continue
        title = title_for_descriptive_slug(row)
        new = descriptive_place_slug(city_slug, title, used)
        if new == old:
            continue
        mapping[old] = new
        used.add(new)
    return mapping


def _clean_row_titles(row: dict) -> bool:
    """Strip asset IDs from expand-row display fields; return True if changed."""
    changed = False
    for key in ("name_en", "name_ru", "subtitle_en", "subtitle_ru", "name"):
        raw = row.get(key)
        if raw is None:
            continue
        cleaned = clean_place_display_title(str(raw))
        if cleaned != str(raw).strip():
            row[key] = cleaned[:120] if key.startswith("name") else cleaned
            changed = True
    desc = row.get("description")
    if desc is not None:
        cleaned_desc = clean_place_display_title(str(desc))
        if cleaned_desc != str(desc).strip():
            row["description"] = cleaned_desc
            changed = True
    return changed


def _patch_sidecar(path: Path, mapping: dict[str, str]) -> int:
    if not path.is_file():
        return 0
    blob = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(blob, list):
        return 0
    changed = 0
    for row in blob:
        if not isinstance(row, dict):
            continue
        if _clean_row_titles(row):
            changed += 1
        old = str(row.get("slug") or "").strip()
        new = mapping.get(old)
        if not new:
            continue
        row["slug"] = new
        rel = str(row.get("image_rel_path") or "")
        if rel:
            row["image_rel_path"] = _update_rel_path(rel, old, new)
        changed += 1
    if changed:
        bak = path.with_suffix(path.suffix + ".slugbak")
        if not bak.is_file():
            shutil.copy2(path, bak)
        path.write_text(
            json.dumps(blob, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return changed


def rename_city(project_root: Path, city_slug: str, *, dry_run: bool) -> int:
    data_dir = project_root / city_slug / "data"
    mapping = _mapping_for_city(city_slug, data_dir)
    if mapping:
        print("{}: {} bad expand slug(s)".format(city_slug, len(mapping)))
        for o, n in sorted(mapping.items()):
            print("  {} -> {}".format(o, n))
    if dry_run:
        return len(mapping)
    total = 0
    for sidecar in pdf_expand_sidecar_paths(data_dir, city_slug):
        total += _patch_sidecar(sidecar, mapping)
    if mapping:
        img_dir = project_root / city_slug / "images"
        _rename_images(img_dir, mapping)
        extra = {o + "_b": n + "_b" for o, n in mapping.items()}
        _rename_images(img_dir, extra)
    return total


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cities", nargs="*", default=None, metavar="SLUG")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    cities = _discover_slugs(_PROJECT_ROOT)
    if args.cities:
        want = set(args.cities)
        cities = [c for c in cities if c in want]
    total = 0
    for slug in cities:
        total += rename_city(_PROJECT_ROOT, slug, dry_run=args.dry_run)
    print("Renamed {} bad expand slug(s) total.".format(total))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

