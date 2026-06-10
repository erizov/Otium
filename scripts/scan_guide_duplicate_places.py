# -*- coding: utf-8 -*-
"""Report duplicate place headings in city guide HTML."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

_PLACE_H3_RE = re.compile(
    r'<section class="place"[^>]*>\s*<h3>([^<]+)</h3>',
)


def place_headings(path: Path) -> list[str]:
    return _PLACE_H3_RE.findall(path.read_text(encoding="utf-8"))


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (AttributeError, OSError, ValueError):
            pass
    root = Path(__file__).resolve().parent.parent
    issues: list[tuple[str, str, list[tuple[str, int]]]] = []
    for city_dir in sorted(root.glob("*/output")):
        city = city_dir.parent.name
        for lang in ("", "_en", "_ru"):
            name = "{}{}.html".format(
                city + "_guide",
                lang,
            )
            path = city_dir / name
            if not path.is_file():
                continue
            headings = place_headings(path)
            dups = [(h, n) for h, n in Counter(headings).items() if n > 1]
            if dups:
                issues.append((city, name, dups))
    if not issues:
        print("No duplicate place headings found.")
        return 0
    print("Duplicate place headings ({} files):".format(len(issues)))
    for city, name, dups in issues:
        print("{} {}:".format(city, name))
        for heading, count in sorted(dups, key=lambda x: -x[1]):
            print("  {} x {}".format(count, heading))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
