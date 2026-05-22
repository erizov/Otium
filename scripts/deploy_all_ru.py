# -*- coding: utf-8 -*-
"""Rebuild stale Russian PDFs when needed, then copy *_guide_ru.pdf."""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.deploy_final_guides import main


if __name__ == "__main__":
    raise SystemExit(main(["--lang", "ru"] + sys.argv[1:]))
