# -*- coding: utf-8 -*-
"""Lint built guide HTML for merged narrative and edition language."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

_CYRILLIC_RE = re.compile(r"[\u0400-\u04FF]")
_BANNED_HEADINGS = (
    "Facts and details",
    "History",
    "Significance",
    "Факты и детали",
    "История",
    "Значение",
)


def _cyrillic_ratio(text: str) -> float:
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0
    cyr = sum(1 for c in letters if "\u0400" <= c <= "\u04FF")
    return cyr / len(letters)


def lint_html(path: Path, edition: str) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for label in _BANNED_HEADINGS:
        if "<h4>{}</h4>".format(label) in text:
            errors.append("{}: section heading {!r} still present".format(
                path.name,
                label,
            ))
    prose_chunks = re.findall(
        r'<p class="prose">(.*?)</p>',
        text,
        flags=re.DOTALL,
    )
    for chunk in prose_chunks:
        plain = re.sub(r"<[^>]+>", "", chunk).strip()
        if len(plain) < 20:
            continue
        if edition == "en":
            if _CYRILLIC_RE.search(plain):
                errors.append("{}: Cyrillic in EN prose: {!r}...".format(
                    path.name,
                    plain[:60],
                ))
        else:
            ratio = _cyrillic_ratio(plain)
            if ratio < 0.35:
                errors.append("{}: non-Russian prose block: {!r}...".format(
                    path.name,
                    plain[:60],
                ))
    for section in re.findall(
        r'<section class="place"[^>]*>(.*?)</section>',
        text,
        flags=re.DOTALL,
    ):
        prose_count = section.count('<p class="prose">')
        if prose_count > 2:
            slug_m = re.search(r'id="([^"]+)"', section)
            slug = slug_m.group(1) if slug_m else "?"
            errors.append("{}: place {} has {} prose paragraphs".format(
                path.name,
                slug,
                prose_count,
            ))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="Guide HTML files to lint.",
    )
    parser.add_argument(
        "--edition",
        choices=("en", "ru"),
        required=True,
    )
    args = parser.parse_args()
    all_errors: list[str] = []
    for raw in args.paths:
        path = raw.resolve()
        if not path.is_file():
            all_errors.append("missing: {}".format(path))
            continue
        all_errors.extend(lint_html(path, args.edition))
    if all_errors:
        for err in all_errors:
            print(err, file=sys.stderr)
        return 1
    print("OK: {} file(s)".format(len(args.paths)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
