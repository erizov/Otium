# -*- coding: utf-8 -*-
"""Normalize image_rel_path to canonical images/<slug>.jpg in places JSON."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_registry_common import drop_empty_place_rows
from scripts.verify_city_guide_place_images import _REGISTRY


def _fix_ext(rel: str) -> str:
    rel_clean = rel.replace("\\", "/").lstrip("/")
    p = Path(rel_clean)
    if p.suffix.lower() in (".jpg", ".jpeg") and p.suffix != ".jpg":
        return str(p.with_suffix(".jpg")).replace("\\", "/")
    return rel_clean


def _norm_place(place: dict) -> bool:
    slug = str(place.get("slug") or "").strip()
    if not slug:
        return False
    changed = False
    rel = str(place.get("image_rel_path") or "").strip()
    if rel:
        fixed = _fix_ext(rel)
        if fixed != rel.replace("\\", "/").lstrip("/"):
            place["image_rel_path"] = fixed
            changed = True
    extras = place.get("additional_images")
    if isinstance(extras, list):
        for extra in extras:
            if not isinstance(extra, dict):
                continue
            er = str(extra.get("image_rel_path") or "").strip()
            if not er:
                continue
            fixed = _fix_ext(er)
            if fixed != er.replace("\\", "/").lstrip("/"):
                extra["image_rel_path"] = fixed
                changed = True
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cities",
        nargs="*",
        default=None,
        metavar="SLUG",
    )
    args = parser.parse_args()
    want = frozenset(args.cities) if args.cities else None
    total = 0
    for slug, _mod, _attr in _REGISTRY:
        if want and slug not in want:
            continue
        path = _PROJECT_ROOT / slug / "data" / "{}_places.json".format(slug)
        if not path.is_file():
            continue
        rows = drop_empty_place_rows(
            json.loads(path.read_text(encoding="utf-8")),
        )
        changed = sum(1 for p in rows if _norm_place(p))
        if changed:
            path.write_text(
                json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            print(slug, "normalized", changed, "rows")
            total += changed
    print("normalize_place_image_paths: done ({} rows)".format(total))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
