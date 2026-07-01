# -*- coding: utf-8 -*-
"""Collect architecture guide image / PDF stats."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.architecture_guide_modules import import_places_list  # noqa: E402
from scripts.architecture_guide_runtime import load_parts  # noqa: E402
from scripts.build_architecture_guide_pdf import (  # noqa: E402
    _BuildContext,
    _load_build_context,
    _places_with_local_images,
)
from scripts.city_guide_registry_common import load_pdf_expand_rows  # noqa: E402


def collect_module_stats(project_root: Path, module: str) -> dict[str, Any]:
    parts = load_parts(module)
    guide_root = project_root / module
    data_dir = guide_root / "data"
    places_path = data_dir / parts.cfg.places_json
    base_rows: list[dict[str, Any]] = json.loads(
        places_path.read_text(encoding="utf-8"),
    )
    expand_rows = load_pdf_expand_rows(data_dir, module)

    def _with_img(rows: list[dict]) -> list[str]:
        out: list[str] = []
        for row in rows:
            rel = str(row.get("image_rel_path") or "")
            if rel and parts.has_local_image(guide_root, rel):
                out.append(str(row.get("slug") or ""))
        return out

    base_ok = _with_img(base_rows)
    expand_ok = _with_img(expand_rows)
    all_rows = import_places_list(module)
    ctx = _load_build_context(module)
    pdf_places = _places_with_local_images(ctx, guide_root)
    missing_path = data_dir / "missing_but_wanted.json"
    missing_n = 0
    if missing_path.is_file():
        missing_n = len(json.loads(missing_path.read_text(encoding="utf-8")))

    return {
        "module": module,
        "base_places": len(base_rows),
        "base_with_images": len(base_ok),
        "expand_rows": len(expand_rows),
        "expand_with_images": len(expand_ok),
        "registry_total": len(all_rows),
        "pdf_places": len(pdf_places),
        "missing_but_wanted": missing_n,
        "expand_missing_slugs": [
            str(r.get("slug") or "")
            for r in expand_rows
            if str(r.get("slug") or "") not in expand_ok
        ],
    }


def collect_all(
    project_root: Path,
    modules: tuple[str, ...],
) -> dict[str, Any]:
    return {
        mod: collect_module_stats(project_root, mod)
        for mod in modules
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--modules",
        nargs="*",
        default=[
            "german_architecture",
            "english_architecture",
            "american_architecture",
        ],
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
    )
    args = parser.parse_args()
    stats = collect_all(_PROJECT_ROOT, tuple(args.modules))
    text = json.dumps(stats, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
        print("Wrote", args.out)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
