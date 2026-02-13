# -*- coding: utf-8 -*-
"""Сборка всех гидов: по очереди запускает build_pdf.py для каждого гида.

Запуск: python scripts/build_all_guides.py
Создаёт HTML (и при наличии playwright — PDF) в output/ для каждого гида.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent
GUIDES = [
    "monasteries",
    "places_of_worship",
    "parks",
    "museums",
    "palaces",
    "buildings",
    "sculptures",
    "places",
    "squares",
    "metro",
    "theaters",
    "viewpoints",
    "bridges",
    "markets",
    "libraries",
    "railway_stations",
    "cemeteries",
    "landmarks",
    "cafes",
]


def main() -> int:
    """Запускает build_pdf.py --guide <name> для каждого гида."""
    python = sys.executable
    build_script = _SCRIPT_DIR / "build_pdf.py"
    if not build_script.is_file():
        print("Error: build_pdf.py not found.", file=sys.stderr)
        return 1

    use_available = "--build-with-available" in sys.argv
    failed: list[str] = []
    for guide in GUIDES:
        print("\n--- Building guide: {} ---".format(guide))
        cmd = [python, str(build_script), "--guide", guide]
        if use_available:
            cmd.append("--build-with-available")
        ret = subprocess.call(cmd, cwd=str(_PROJECT_ROOT))
        if ret != 0:
            failed.append(guide)

    if failed:
        print(
            "\nFailed guides: {}.".format(", ".join(failed)),
            file=sys.stderr,
        )
        return 1
    print("\nAll guides built successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
