# -*- coding: utf-8 -*-
"""Resolve Commons file titles for ``grow_city_guides_to_25`` static fallback.

Run from repo root with a generous pause to avoid Commons HTTP 429::

    python scripts/build_grow_existing_static_commons.py --pause 2.5

Writes ``scripts/grow_existing_static_commons.json`` (slug -> place_slug ->
filename). Merge into the grow script or load at runtime.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.grow_city_guides_to_25 import _EXISTING_12
from scripts.grow_city_guides_to_25 import _SEEDS
from scripts.grow_city_guides_to_25 import _commons_search_title

_OUT = Path(__file__).resolve().parent / "grow_existing_static_commons.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pause",
        type=float,
        default=2.2,
        help="pause between Commons searches (default 2.2)",
    )
    parser.add_argument(
        "--cities",
        nargs="*",
        metavar="SLUG",
        help="only these slugs (default: all 14)",
    )
    args = parser.parse_args()
    want = frozenset(args.cities) if args.cities else None
    out: dict[str, dict[str, str]] = {}
    if _OUT.is_file():
        prev = json.loads(_OUT.read_text(encoding="utf-8"))
        if isinstance(prev, dict):
            for k, v in prev.items():
                if isinstance(v, dict):
                    out[str(k)] = {str(a): str(b) for a, b in v.items()}
    for slug in _EXISTING_12:
        if want is not None and slug not in want:
            continue
        inner: dict[str, str] = {}
        for place_slug, _name, _cat, query in _SEEDS[slug]:
            title = _commons_search_title(query, pause=args.pause)
            if not title:
                print(
                    "MISSING",
                    slug,
                    place_slug,
                    repr(query),
                    file=sys.stderr,
                )
                raise SystemExit(1)
            inner[place_slug] = title
            print(slug, place_slug, "->", title)
        out[slug] = inner
    _OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Wrote", _OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
