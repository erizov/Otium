# -*- coding: utf-8 -*-
"""Fix Latin/Cyrillic mixups in osobnjaki.py."""

from __future__ import annotations

from pathlib import Path

_PATH = Path(__file__).resolve().parent.parent / "moscow" / "data" / "osobnjaki.py"


def main() -> int:
    text = _PATH.read_text(encoding="utf-8")
    text = text.replace("Малютin", "Малютин")
    text = text.replace("Малютina", "Малютина")
    _PATH.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
