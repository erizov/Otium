# -*- coding: utf-8 -*-
"""Resolve Russian Architecture images (wrapper)."""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.resolve_architecture_guide_images import main as _main

_DEFAULT_MODULE = "russian_architecture"


def main() -> int:
    if "--module" not in sys.argv:
        sys.argv[1:1] = ["--module", _DEFAULT_MODULE]
    return _main()


if __name__ == "__main__":
    raise SystemExit(main())
