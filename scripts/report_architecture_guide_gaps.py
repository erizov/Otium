# -*- coding: utf-8 -*-
"""Report missing text/images for architecture guide modules."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.architecture_guide_modules import MODULES  # noqa: E402
from scripts.architecture_guide_modules import module_config  # noqa: E402

MIN_IMAGE_BYTES = 500


def _audit(module: str, project_root: Path) -> dict[str, list[str]]:
    cfg = module_config(module)
    path = project_root / cfg.slug / "data" / cfg.places_json
    rows: list[dict] = json.loads(path.read_text(encoding="utf-8"))
    guide_root = project_root / cfg.slug
    missing_text: list[str] = []
    missing_image: list[str] = []
    for row in rows:
        slug = str(row.get("slug") or "")
        text = str(
            row.get("description_ru") or row.get("description") or "",
        ).strip()
        if not text:
            missing_text.append(slug)
        rel = str(row.get("image_rel_path") or "")
        img = guide_root / rel if rel else None
        if not img or not img.is_file() or img.stat().st_size < MIN_IMAGE_BYTES:
            missing_image.append(slug)
    return {"missing_text": missing_text, "missing_image": missing_image}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Report architecture guide gaps.",
    )
    parser.add_argument(
        "--module",
        choices=sorted(MODULES),
        action="append",
        dest="modules",
        help="Module slug (repeatable; default: all)",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=_PROJECT_ROOT,
    )
    args = parser.parse_args()
    modules = args.modules or sorted(MODULES)
    exit_code = 0
    for module in modules:
        gaps = _audit(module, args.project_root)
        print("=== {} ===".format(module))
        print("  missing text: {}".format(len(gaps["missing_text"])))
        print("  missing image: {}".format(len(gaps["missing_image"])))
        for slug in gaps["missing_image"][:20]:
            print("    img: {}".format(slug))
        if len(gaps["missing_image"]) > 20:
            print("    ... and {} more".format(
                len(gaps["missing_image"]) - 20,
            ))
        if gaps["missing_text"] or gaps["missing_image"]:
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
