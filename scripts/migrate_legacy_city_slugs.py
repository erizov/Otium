# -*- coding: utf-8 -*-
"""Rename unprefixed place slugs to {city}_{id} across guide JSON and images."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_naming import curated_place_slug
from scripts.city_guide_naming import is_pdf_filler_slug
from scripts.verify_city_guide_place_images import _REGISTRY

_RASTER = frozenset({".jpg", ".jpeg", ".png", ".webp", ".gif"})


def _rename_slug(city_slug: str, old_slug: str) -> str:
    if old_slug.startswith(city_slug + "_"):
        return old_slug
    if is_pdf_filler_slug(old_slug):
        return old_slug
    return curated_place_slug(city_slug, old_slug)


def _update_rel_path(rel: str, old: str, new: str) -> str:
    rel_norm = rel.replace("\\", "/")
    p = Path(rel_norm)
    parts = rel_norm.split("/")
    new_parts = [new if part == old else part for part in parts]
    out = "/".join(new_parts)
    p2 = Path(out)
    if p.stem == old:
        out = str(p2.with_name(new + p2.suffix)).replace("\\", "/")
    return out


def _collect_mapping(city_slug: str, rows: list[dict]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for row in rows:
        old = str(row.get("slug") or "").strip()
        if not old:
            continue
        new = _rename_slug(city_slug, old)
        if new != old:
            mapping[old] = new
    return mapping


def _patch_place_dict(row: dict[str, Any], mapping: dict[str, str]) -> bool:
    changed = False
    old_slug = str(row.get("slug") or "")
    if old_slug in mapping:
        row["slug"] = mapping[old_slug]
        changed = True
    rel = str(row.get("image_rel_path") or "")
    if rel:
        for o, n in mapping.items():
            new_rel = _update_rel_path(rel, o, n)
            if new_rel != rel:
                row["image_rel_path"] = new_rel
                changed = True
                break
    for extra in row.get("additional_images") or []:
        if not isinstance(extra, dict):
            continue
        erel = str(extra.get("image_rel_path") or "")
        if erel:
            for o, n in mapping.items():
                new_rel = _update_rel_path(erel, o, n)
                if new_rel != erel:
                    extra["image_rel_path"] = new_rel
                    changed = True
                    break
    return changed


def _walk_json(path: Path, mapping: dict[str, str]) -> bool:
    try:
        blob = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False
    changed = False
    if isinstance(blob, list):
        for row in blob:
            if isinstance(row, dict) and _patch_place_dict(row, mapping):
                changed = True
    elif isinstance(blob, dict):
        new_blob: dict[str, Any] = {}
        for key, val in blob.items():
            nk = mapping.get(key, key)
            if nk != key:
                changed = True
            if isinstance(val, dict):
                _patch_place_dict(val, mapping)
            new_blob[nk] = val
        if changed:
            blob = new_blob
    if changed:
        bak = path.with_suffix(path.suffix + ".slugbak")
        if not bak.is_file():
            shutil.copy2(path, bak)
        path.write_text(
            json.dumps(blob, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return changed


def _rename_images(img_dir: Path, mapping: dict[str, str]) -> int:
    n = 0
    if not img_dir.is_dir():
        return 0
    for path in list(img_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in _RASTER:
            continue
        stem = path.stem
        if stem not in mapping:
            continue
        dest = path.with_name(mapping[stem] + path.suffix)
        if dest.is_file():
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        path.rename(dest)
        n += 1
    return n


def migrate_city(
    project_root: Path,
    city_slug: str,
    module_name: str,
    attr: str,
    *,
    dry_run: bool,
) -> int:
    try:
        mod = __import__(module_name, fromlist=[attr])
        places = [dict(p) for p in getattr(mod, attr)]
    except Exception as exc:
        print("{}: skip ({})".format(city_slug, exc), file=sys.stderr)
        return 0
    mapping = _collect_mapping(city_slug, places)
    if not mapping:
        return 0
    print("{}: {} slug renames".format(city_slug, len(mapping)))
    if dry_run:
        return len(mapping)
    data_dir = project_root / city_slug / "data"
    for path in sorted(data_dir.glob("*.json")):
        _walk_json(path, mapping)
    img_n = _rename_images(project_root / city_slug / "images", mapping)
    if img_n:
        print("  renamed {} image file(s)".format(img_n))
    return len(mapping)


def cities_needing_prefix() -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    for slug, mod, attr in _REGISTRY:
        try:
            mod_o = __import__(mod, fromlist=[attr])
            places = getattr(mod_o, attr)
        except Exception:
            continue
        for p in places:
            s = str(p.get("slug") or "")
            if not s or is_pdf_filler_slug(s):
                continue
            if not s.startswith(slug + "_"):
                out.append((slug, mod, attr))
                break
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cities",
        nargs="*",
        default=None,
        metavar="SLUG",
    )
    parser.add_argument(
        "--all-unprefixed",
        action="store_true",
        help="Migrate every registry city with unprefixed slugs.",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.all_unprefixed:
        targets = cities_needing_prefix()
    elif args.cities:
        want = frozenset(args.cities)
        targets = [t for t in _REGISTRY if t[0] in want]
    else:
        targets = []
    total = 0
    seen: set[str] = set()
    for slug, mod, attr in targets:
        if slug in seen:
            continue
        seen.add(slug)
        total += migrate_city(
            _PROJECT_ROOT,
            slug,
            mod,
            attr,
            dry_run=args.dry_run,
        )
    print("Renamed {} slug(s) total.".format(total))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
