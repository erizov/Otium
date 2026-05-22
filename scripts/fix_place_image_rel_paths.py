# -*- coding: utf-8 -*-
"""Fix image_rel_path when file exists under another extension or stem."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_core import smallest_same_stem_image_rel
from scripts.verify_city_guide_place_images import _REGISTRY

_RASTER = frozenset({".jpg", ".jpeg", ".png", ".webp", ".gif"})


def _load_places(module_name: str, attr: str) -> list[dict]:
    mod = __import__(module_name, fromlist=[attr])
    return [dict(p) for p in getattr(mod, attr)]


def _prefixed_stem_path(
    root: Path,
    rel_clean: str,
    city_slug: str,
) -> str | None:
    """``images/foo.jpg`` -> ``images/{city}_foo.jpg`` when that file exists."""
    stem = Path(rel_clean).stem
    parent = (root / rel_clean).parent
    if not parent.is_dir():
        parent = root / "images"
    if not parent.is_dir():
        return None
    prefixed = "{}_{}".format(city_slug.strip().lower(), stem)
    for path in sorted(parent.iterdir()):
        if path.is_file() and path.stem == prefixed:
            if path.suffix.lower() in _RASTER:
                return path.relative_to(root).as_posix()
    images_dir = root / "images"
    if images_dir.is_dir():
        for path in sorted(images_dir.rglob(prefixed + ".*")):
            if path.is_file() and path.suffix.lower() in _RASTER:
                return path.relative_to(root).as_posix()
    return None


def _resolve_rel(root: Path, rel: str, *, city_slug: str = "") -> str | None:
    rel_clean = rel.replace("\\", "/").lstrip("/")
    base = root / rel_clean
    if base.is_file():
        return rel_clean
    alt = smallest_same_stem_image_rel(root, rel_clean)
    if alt:
        return alt.replace("\\", "/")
    if city_slug:
        pref = _prefixed_stem_path(root, rel_clean, city_slug)
        if pref:
            return pref
    stem = Path(rel_clean).stem
    parent = (root / rel_clean).parent
    if not parent.is_dir():
        parent = root / "images"
    if not parent.is_dir():
        return None
    for path in sorted(parent.iterdir()):
        if path.is_file() and path.suffix.lower() in _RASTER:
            if path.stem == stem or path.stem.startswith(stem):
                return path.relative_to(root).as_posix()
    # e.g. Smolensk_Readovka1.jpg -> Smolensk_Readovka.jpg
    m = re.match(r"^(.+?)(\d+)$", stem)
    if m:
        base_stem = m.group(1)
        for path in sorted(parent.iterdir()):
            if path.is_file() and path.stem == base_stem:
                return path.relative_to(root).as_posix()
    return None


def fix_city(city_slug: str, module_name: str, attr: str, *, dry_run: bool) -> int:
    root = _PROJECT_ROOT / city_slug
    places = _load_places(module_name, attr)
    fixes: dict[str, str] = {}
    for p in places:
        slug = str(p.get("slug") or "")
        rel = str(p.get("image_rel_path") or "").strip()
        if not rel:
            continue
        resolved = _resolve_rel(root, rel, city_slug=city_slug)
        if resolved and resolved != rel.replace("\\", "/").lstrip("/"):
            fixes[slug] = resolved
    if not fixes:
        return 0
    print("{}: {} image_rel_path fix(es)".format(city_slug, len(fixes)))
    if dry_run:
        return len(fixes)
    data_dir = root / "data"
    for path in sorted(data_dir.glob("*.json")):
        text = path.read_text(encoding="utf-8")
        try:
            blob = json.loads(text)
        except json.JSONDecodeError:
            continue
        changed = False

        def patch_row(row: dict) -> None:
            nonlocal changed
            s = str(row.get("slug") or "")
            if s in fixes:
                row["image_rel_path"] = fixes[s]
                changed = True
            for extra in row.get("additional_images") or []:
                if isinstance(extra, dict) and extra.get("image_rel_path"):
                    old = extra["image_rel_path"]
                    new = _resolve_rel(root, old, city_slug=city_slug)
                    if new and new != old:
                        extra["image_rel_path"] = new
                        changed = True

        if isinstance(blob, list):
            for row in blob:
                if isinstance(row, dict):
                    patch_row(row)
        elif isinstance(blob, dict):
            for key, row in blob.items():
                if isinstance(row, dict):
                    if key in fixes and "image_rel_path" in row:
                        row["image_rel_path"] = fixes[key]
                        changed = True
                    elif "image_rel_path" in row:
                        old = row["image_rel_path"]
                        new = _resolve_rel(root, old, city_slug=city_slug)
                        if new and new != old:
                            row["image_rel_path"] = new
                            changed = True
        if changed:
            path.write_text(
                json.dumps(blob, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
    return len(fixes)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cities", nargs="*", default=None, metavar="SLUG")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    targets = _REGISTRY
    if args.cities:
        want = frozenset(args.cities)
        targets = tuple(t for t in _REGISTRY if t[0] in want)
    total = 0
    for slug, mod, attr in targets:
        total += fix_city(slug, mod, attr, dry_run=args.dry_run)
    print("Fixed {} path(s) total.".format(total))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
