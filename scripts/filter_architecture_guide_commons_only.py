# -*- coding: utf-8 -*-
"""Drop guide places without local Commons images; track missing wanted."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.architecture_guide_modules import MODULES  # noqa: E402
from scripts.architecture_guide_runtime import load_parts  # noqa: E402


def filter_places(
    project_root: Path,
    module: str,
) -> dict[str, Any]:
    parts = load_parts(module)
    guide_root = project_root / parts.cfg.slug
    data_path = guide_root / "data" / parts.cfg.places_json
    rows: list[dict[str, Any]] = json.loads(
        data_path.read_text(encoding="utf-8"),
    )
    kept: list[dict[str, Any]] = []
    missing: list[dict[str, Any]] = []
    for row in rows:
        rel = str(row.get("image_rel_path") or "")
        if rel and parts.has_local_image(guide_root, rel):
            kept.append(row)
        else:
            missing.append({
                "slug": row.get("slug"),
                "name_ru": row.get("name_ru"),
                "name_en": row.get("subtitle_en"),
                "category": row.get("category"),
                "image_source_url": row.get("image_source_url"),
                "reason": "no_commons_image",
            })
    data_path.write_text(
        json.dumps(kept, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    missing_path = guide_root / "data" / "missing_but_wanted.json"
    missing_path.write_text(
        json.dumps(missing, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    per_style: dict[str, int] = {}
    for row in kept:
        cat = str(row.get("category") or "")
        per_style[cat] = per_style.get(cat, 0) + 1
    return {
        "module": module,
        "success": len(kept),
        "failed": len(missing),
        "attempted": len(rows),
        "per_style": per_style,
        "missing_path": str(missing_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Keep only architecture guide places with local images.",
    )
    parser.add_argument(
        "--module",
        choices=tuple(MODULES.keys()),
        required=True,
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=_PROJECT_ROOT,
    )
    args = parser.parse_args()
    report = filter_places(args.project_root, args.module)
    print(
        "{module}: success={success} failed={failed} "
        "attempted={attempted}".format(**report),
    )
    print("Missing list:", report["missing_path"])
    parts = load_parts(args.module)
    for style_key in parts.STYLE_ORDER:
        count = report["per_style"].get(style_key, 0)
        if count:
            print("  {}: {}".format(style_key, count))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
