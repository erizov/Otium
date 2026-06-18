# -*- coding: utf-8 -*-
"""Rename legacy ``{city}_pdfband_*`` slugs and images to descriptive names."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_naming import descriptive_place_slug
from scripts.city_guide_naming import is_pdf_filler_slug
from scripts.city_guide_naming import title_for_descriptive_slug
from scripts.city_guide_registry_common import pdf_expand_sidecar_paths
from scripts.migrate_legacy_city_slugs import _rename_images
from scripts.migrate_legacy_city_slugs import _update_rel_path
from scripts.migrate_legacy_city_slugs import _walk_json
from scripts.rebuild_stale_city_guide_pdfs import _discover_slugs


def _load_rows(data_dir: Path, city_slug: str) -> list[dict]:
    rows: list[dict] = []
    main = data_dir / "{}_places.json".format(city_slug)
    if main.is_file():
        blob = json.loads(main.read_text(encoding="utf-8"))
        if isinstance(blob, list):
            rows.extend(blob)
    for path in pdf_expand_sidecar_paths(data_dir, city_slug):
        if path.is_file():
            blob = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(blob, list):
                rows.extend(blob)
    return rows


def _collect_pdfband_mapping(
    city_slug: str,
    rows: list[dict],
) -> dict[str, str]:
    used = {
        str(r.get("slug") or "").strip()
        for r in rows
        if str(r.get("slug") or "").strip()
    }
    mapping: dict[str, str] = {}
    for row in rows:
        old = str(row.get("slug") or "").strip()
        if not old or not is_pdf_filler_slug(old):
            continue
        title = title_for_descriptive_slug(row)
        new = descriptive_place_slug(city_slug, title, used)
        if new == old:
            continue
        mapping[old] = new
        used.add(new)
    return mapping


def _patch_second_images(path: Path, mapping: dict[str, str]) -> bool:
    if not path.is_file():
        return False
    blob = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(blob, dict):
        return False
    changed = False
    new_blob: dict[str, Any] = {}
    for key, val in blob.items():
        nk = mapping.get(key, key)
        if nk != key:
            changed = True
        if isinstance(val, list):
            for item in val:
                if not isinstance(item, dict):
                    continue
                rel = str(item.get("image_rel_path") or "")
                if rel:
                    for o, n in mapping.items():
                        new_rel = _update_rel_path(rel, o, n)
                        if new_rel != rel:
                            item["image_rel_path"] = new_rel
                            changed = True
                            break
        new_blob[nk] = val
    if changed:
        bak = path.with_suffix(path.suffix + ".pdfbandbak")
        if not bak.is_file():
            shutil.copy2(path, bak)
        path.write_text(
            json.dumps(new_blob, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return changed


def _mapping_from_sidecar_slugbak(
    data_dir: Path,
    city_slug: str,
) -> dict[str, str]:
    """Old pdfband slug -> new slug from sidecar ``.slugbak``."""
    path = data_dir / "{}_places_pdf_expand.json".format(city_slug)
    bak = path.with_suffix(path.suffix + ".slugbak")
    if not bak.is_file() or not path.is_file():
        return {}
    old_rows = json.loads(bak.read_text(encoding="utf-8"))
    new_rows = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(old_rows, list) or not isinstance(new_rows, list):
        return {}
    url_to_new: dict[str, str] = {}
    for row in new_rows:
        if not isinstance(row, dict):
            continue
        url = str(row.get("image_source_url") or "")
        slug = str(row.get("slug") or "")
        if url and slug:
            url_to_new[url] = slug
    mapping: dict[str, str] = {}
    for row in old_rows:
        if not isinstance(row, dict):
            continue
        old = str(row.get("slug") or "")
        if not is_pdf_filler_slug(old):
            continue
        new = url_to_new.get(str(row.get("image_source_url") or ""))
        if new and new != old:
            mapping[old] = new
    return mapping


def _fix_second_image_paths(data_dir: Path, city_slug: str) -> int:
    path = data_dir / "{}_second_images.json".format(city_slug)
    if not path.is_file():
        return 0
    blob = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(blob, dict):
        return 0
    changed = False
    for key, val in blob.items():
        if not isinstance(val, list):
            continue
        for item in val:
            if not isinstance(item, dict):
                continue
            rel = str(item.get("image_rel_path") or "")
            if "pdfband" in rel:
                item["image_rel_path"] = "images/{}_b.jpg".format(key)
                changed = True
    if changed:
        path.write_text(
            json.dumps(blob, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return int(changed)


def _rename_orphan_pdfband_images(
    img_dir: Path,
    mapping: dict[str, str],
) -> int:
    if not img_dir.is_dir() or not mapping:
        return 0
    n = 0
    for path in list(img_dir.iterdir()):
        if not path.is_file():
            continue
        stem = path.stem
        old_slug = stem
        if stem.endswith("_b"):
            old_slug = stem[:-2]
        if old_slug not in mapping:
            continue
        new_stem = mapping[old_slug]
        if stem.endswith("_b"):
            new_stem = "{}_b".format(new_stem)
        dest = path.with_name(new_stem + path.suffix)
        if dest.is_file():
            continue
        path.rename(dest)
        n += 1
    return n


def fix_city_pdfband_leftovers(
    project_root: Path,
    city_slug: str,
) -> int:
    data_dir = project_root / city_slug / "data"
    mapping = _mapping_from_sidecar_slugbak(data_dir, city_slug)
    n = _fix_second_image_paths(data_dir, city_slug)
    img_n = _rename_orphan_pdfband_images(
        project_root / city_slug / "images",
        mapping,
    )
    if img_n:
        print("  fixed {} orphan pdfband image file(s)".format(img_n))
    return n + img_n


def rename_city(
    project_root: Path,
    city_slug: str,
    *,
    dry_run: bool,
) -> int:
    data_dir = project_root / city_slug / "data"
    rows = _load_rows(data_dir, city_slug)
    mapping = _collect_pdfband_mapping(city_slug, rows)
    if not mapping:
        return 0
    print("{}: {} pdfband rename(s)".format(city_slug, len(mapping)))
    for old, new in sorted(mapping.items()):
        print("  {} -> {}".format(old, new))
    if dry_run:
        return len(mapping)

    for path in sorted(data_dir.glob("*.json")):
        _walk_json(path, mapping)
    second = data_dir / "{}_second_images.json".format(city_slug)
    _patch_second_images(second, mapping)

    img_dir = project_root / city_slug / "images"
    img_n = _rename_images(img_dir, mapping)
    # Second-image stems: ``{old}_b`` -> ``{new}_b``.
    extra: dict[str, str] = {}
    for old, new in mapping.items():
        extra["{}_b".format(old)] = "{}_b".format(new)
    img_n += _rename_images(img_dir, extra)
    if img_n:
        print("  renamed {} image file(s)".format(img_n))
    fix_city_pdfband_leftovers(project_root, city_slug)
    return len(mapping)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cities", nargs="*", default=None, metavar="SLUG")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--fix-leftovers",
        action="store_true",
        help="Only fix second_images paths and orphan pdfband files.",
    )
    args = parser.parse_args()
    cities = _discover_slugs(_PROJECT_ROOT)
    if args.cities:
        cities = [c for c in cities if c in set(args.cities)]
    total = 0
    if args.fix_leftovers:
        for slug in cities:
            total += fix_city_pdfband_leftovers(_PROJECT_ROOT, slug)
        print("Fixed {} leftover pdfband reference(s).".format(total))
        return 0
    for slug in cities:
        total += rename_city(_PROJECT_ROOT, slug, dry_run=args.dry_run)
    print("Renamed {} pdfband slug(s) total.".format(total))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
