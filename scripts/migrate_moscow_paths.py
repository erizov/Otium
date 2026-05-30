# -*- coding: utf-8 -*-
"""One-off: retarget Moscow paths after move to moscow/."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {
    "data/__init__.py",
    "moscow/data/__init__.py",
    "scripts/migrate_moscow_paths.py",
}


def main() -> int:
    patterns = [
        (re.compile(r"from data\."), "from moscow.data."),
        (re.compile(r"import data\."), "import moscow.data."),
        (re.compile(r'"data\.'), '"moscow.data.'),
        (re.compile(r"'data\."), "'moscow.data."),
    ]
    replacements = [
        ('default=_PROJECT_ROOT / "output"', 'default=_PROJECT_ROOT / "moscow"'),
        ('PROJECT_ROOT / "output"', 'PROJECT_ROOT / "moscow" / "output"'),
        ('_PROJECT_ROOT / "output"', '_PROJECT_ROOT / "moscow" / "output"'),
    ]
    changed: list[str] = []
    paths = list((ROOT / "scripts").rglob("*.py"))
    paths += list((ROOT / "tests").rglob("*.py"))
    for path in paths:
        rel = path.relative_to(ROOT).as_posix()
        if rel in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        orig = text
        for pat, repl in patterns:
            text = pat.sub(repl, text)
        for old, new in replacements:
            text = text.replace(old, new)
        if text != orig:
            path.write_text(text, encoding="utf-8")
            changed.append(rel)
    print("updated {} files".format(len(changed)))
    for rel in changed:
        print(" ", rel)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
