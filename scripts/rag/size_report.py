# -*- coding: utf-8 -*-
"""Print corpus size estimates for the local city-guide RAG cache."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.rag.chunk_and_embed import _size_report
from scripts.rag.config import rag_paths


def _per_city_doc_bytes(paths) -> dict[str, int]:
    out: dict[str, int] = {}
    if not paths.docs_dir.is_dir():
        return out
    for city_dir in sorted(p for p in paths.docs_dir.iterdir() if p.is_dir()):
        total = 0
        for p in city_dir.rglob("*.json"):
            if p.is_file():
                total += p.stat().st_size
        out[city_dir.name] = total
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help="Repo root (default: auto).",
    )
    parser.add_argument(
        "--per-city",
        action="store_true",
        help="Also report bytes per city.",
    )
    args = parser.parse_args()
    root = (
        args.project_root.resolve()
        if args.project_root
        else Path(__file__).resolve().parent.parent.parent
    )
    paths = rag_paths(root)
    report = _size_report(root)
    if args.per_city:
        report["per_city_docs_bytes"] = _per_city_doc_bytes(paths)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

