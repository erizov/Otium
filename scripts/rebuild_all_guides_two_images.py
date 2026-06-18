# -*- coding: utf-8 -*-
"""Download missing images (max 2/place) and rebuild all city guide PDFs."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    py = sys.executable
    root = str(_PROJECT_ROOT)
    steps = [
        (
            "download_missing_registry_images.py",
            [py, str(_PROJECT_ROOT / "scripts" / "download_missing_registry_images.py")],
        ),
        (
            "rebuild_stale_city_guide_pdfs.py --force-all",
            [
                py,
                str(_PROJECT_ROOT / "scripts" / "rebuild_stale_city_guide_pdfs.py"),
                "--force-all",
            ],
        ),
    ]
    for label, cmd in steps:
        print("=== {} ===".format(label))
        rc = subprocess.run(cmd, cwd=root, check=False).returncode
        if rc:
            print("Failed:", label, "(exit {})".format(rc), file=sys.stderr)
            return rc
    print("All city guides rebuilt with 2-image PDF rule.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
