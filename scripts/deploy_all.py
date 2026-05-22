# -*- coding: utf-8 -*-
"""Rebuild stale guides (all editions), then copy them to final_guides/."""

from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if (_HERE / "scripts" / "deploy_final_guides.py").is_file():
    _PROJECT_ROOT = _HERE
else:
    _PROJECT_ROOT = _HERE.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.deploy_final_guides import main


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
