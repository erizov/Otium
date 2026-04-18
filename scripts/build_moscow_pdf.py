# -*- coding: utf-8 -*-
"""Moscow combined guide: delegate to build_full_guide or sync webapp JSON."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Moscow combined guide (full build) or webapp JSON sync.",
    )
    parser.add_argument(
        "--html-only",
        action="store_true",
        help="Regenerate moscow/data/moscow_places.json from data/*.py registries.",
    )
    args, rest = parser.parse_known_args()
    if args.html_only:
        return subprocess.call(
            [
                sys.executable,
                str(_PROJECT_ROOT / "scripts" / "export_moscow_webapp_places.py"),
            ],
            cwd=str(_PROJECT_ROOT),
        )
    cmd = [sys.executable, str(_PROJECT_ROOT / "scripts" / "build_full_guide.py")]
    if rest:
        cmd.extend(rest)
    return subprocess.call(cmd, cwd=str(_PROJECT_ROOT))


if __name__ == "__main__":
    raise SystemExit(main())
