# -*- coding: utf-8 -*-
"""Validate Boston image_source_url entries against the whitelist."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from boston.data.places_registry import BOSTON_PLACES
from boston.whitelist import default_whitelist_path, url_is_whitelisted


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate boston place image_source_url against "
            "SOURCES_WHITELIST.md."
        ),
    )
    parser.add_argument(
        "--whitelist",
        type=Path,
        default=None,
        help="Override path to SOURCES_WHITELIST.md",
    )
    args = parser.parse_args()
    wpath = args.whitelist or default_whitelist_path()
    if not wpath.is_file():
        print("Whitelist file missing: {}".format(wpath), file=sys.stderr)
        return 2

    errors: list[str] = []
    for place in BOSTON_PLACES:
        slug = place.get("slug", "<no slug>")
        url = place.get("image_source_url")
        if not url:
            errors.append("{}: missing image_source_url".format(slug))
            continue
        if not url_is_whitelisted(url, whitelist_path=wpath):
            errors.append("{}: not whitelisted: {}".format(slug, url))
        for j, extra in enumerate(place.get("additional_images") or [], start=1):
            eu = extra.get("image_source_url")
            if not eu:
                errors.append(
                    "{}: additional image #{} missing URL".format(slug, j),
                )
                continue
            if not url_is_whitelisted(eu, whitelist_path=wpath):
                errors.append(
                    "{}: additional #{} not whitelisted: {}".format(
                        slug, j, eu,
                    ),
                )

    if errors:
        print("Boston source URL validation failed:", file=sys.stderr)
        for line in errors:
            print("  {}".format(line), file=sys.stderr)
        return 1
    print("OK: {} place(s), all image_source_url whitelisted.".format(
        len(BOSTON_PLACES),
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
