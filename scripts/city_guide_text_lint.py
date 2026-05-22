# -*- coding: utf-8 -*-
"""Lint place text for banned templates and missing substantive fields."""

from __future__ import annotations

import argparse
import importlib
import re
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_core import is_substantive_text
from scripts.city_guide_naming import is_pdf_filler_slug
from scripts.verify_city_guide_place_images import _REGISTRY

# Substrings that indicate auto-generated / low-quality prose.
BANNED_TEXT_FRAGMENTS: tuple[str, ...] = (
    "notable city landmark",
    "see commons file page",
    "see official visitor information",
    "wikimedia commons contributors",
    "see wikimedia commons",
)

_BANNED_RE = re.compile(
    "|".join(re.escape(s) for s in BANNED_TEXT_FRAGMENTS),
    re.IGNORECASE,
)

_TEXT_KEYS = (
    "description",
    "history",
    "significance",
    "address",
)


def _load_places(module_name: str, attr: str) -> list[dict]:
    mod = importlib.import_module(module_name)
    raw = getattr(mod, attr)
    return [dict(p) for p in raw]


def lint_place_row(
    city_slug: str,
    place: dict,
    *,
    require_description: bool = False,
) -> list[str]:
    errs: list[str] = []
    slug = str(place.get("slug") or "").strip()
    if is_pdf_filler_slug(slug):
        return errs
    name = place.get("name_en", place.get("name_ru", slug))
    for key in _TEXT_KEYS:
        val = place.get(key)
        if not isinstance(val, str):
            continue
        if _BANNED_RE.search(val):
            errs.append(
                "{} {!r}: banned template in {}".format(
                    city_slug, name, key,
                ),
            )
    facts = place.get("facts") or []
    if isinstance(facts, list):
        for i, f in enumerate(facts):
            if isinstance(f, str) and _BANNED_RE.search(f):
                errs.append(
                    "{} {!r}: banned template in facts[{}]".format(
                        city_slug, name, i,
                    ),
                )
    if require_description:
        if not is_substantive_text(str(place.get("description") or "")):
            errs.append(
                "{} {!r}: missing substantive description".format(
                    city_slug, name,
                ),
            )
    return errs


def lint_city(
    city_slug: str,
    module_name: str,
    attr: str,
    *,
    require_description: bool = False,
) -> list[str]:
    try:
        places = _load_places(module_name, attr)
    except Exception as exc:
        return ["{}: load failed: {}".format(city_slug, exc)]
    errs: list[str] = []
    for p in places:
        errs.extend(
            lint_place_row(
                city_slug,
                p,
                require_description=require_description,
            ),
        )
    return errs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cities",
        nargs="*",
        default=None,
        metavar="SLUG",
    )
    parser.add_argument(
        "--require-description",
        action="store_true",
        help="Fail when curated places lack description.",
    )
    args = parser.parse_args()
    targets = _REGISTRY
    if args.cities:
        want = frozenset(args.cities)
        targets = tuple(t for t in _REGISTRY if t[0] in want)
    all_errs: list[str] = []
    for slug, mod, attr in targets:
        all_errs.extend(
            lint_city(
                slug,
                mod,
                attr,
                require_description=args.require_description,
            ),
        )
    for line in all_errs:
        print(line, file=sys.stderr)
    if all_errs:
        print(
            "lint_place_text: {} issue(s)".format(len(all_errs)),
            file=sys.stderr,
        )
        return 1
    print("lint_place_text: ok ({} cities)".format(len(targets)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
