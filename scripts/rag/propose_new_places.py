# -*- coding: utf-8 -*-
"""Propose new popular/religion places as (category, Commons query) pairs.

This does not download images or modify city JSON. It emits a suggestion file
under `rag_outputs/<city>/new_place_queries.json` which can be fed into your
existing expansion/download tooling.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.rag.city_map import names_for_slug
from scripts.rag.config import rag_paths


def propose(city_slug: str) -> list[dict[str, str]]:
    names = names_for_slug(city_slug)
    display = names.name_en
    ru = names.name_ru
    base = [
        {"category": "places_of_worship", "query": f"{display} cathedral"},
        {"category": "places_of_worship", "query": f"{display} church"},
        {"category": "places_of_worship", "query": f"{display} mosque"},
        {"category": "landmarks", "query": f"{display} historic centre"},
        {"category": "museums", "query": f"{display} museum"},
    ]
    if ru:
        base.extend(
            [
                {"category": "places_of_worship", "query": f"{ru} собор"},
                {"category": "places_of_worship", "query": f"{ru} храм"},
                {"category": "landmarks", "query": f"{ru} памятник"},
                {"category": "museums", "query": f"{ru} музей"},
            ]
        )
    return base


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=None)
    parser.add_argument("--city", required=True)
    args = parser.parse_args()
    root = (
        args.project_root.resolve()
        if args.project_root
        else Path(__file__).resolve().parent.parent.parent
    )
    paths = rag_paths(root)
    out_dir = paths.outputs_dir / str(args.city)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "new_place_queries.json"
    out_path.write_text(
        json.dumps(propose(str(args.city)), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("Written:", out_path.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

