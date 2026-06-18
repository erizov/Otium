# -*- coding: utf-8 -*-
"""Download osobnjaki images, export places JSON, optional PDF build."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from moscow.data.osobnjaki import OSOBNJAKI


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Skip image download; only export JSON.",
    )
    parser.add_argument(
        "--build-pdf",
        action="store_true",
        help="Build osobnjaki PDF after export.",
    )
    parser.add_argument(
        "--force-download",
        action="store_true",
        help="Pass --force-overwrite to build_pdf download step.",
    )
    args = parser.parse_args()

    print("Moscow osobnjaki: {} places".format(len(OSOBNJAKI)))
    if not args.skip_download:
        cmd = [
            sys.executable,
            "-m",
            "scripts.build_pdf",
            "--guide",
            "osobnjaki",
            "--download-only",
            "--build-with-available",
            "--no-ai-identify",
        ]
        if args.force_download:
            cmd.append("--force-overwrite")
        print("Downloading images …")
        subprocess.run(cmd, check=True, cwd=str(_PROJECT_ROOT))

    print("Exporting moscow_places.json …")
    subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.export_moscow_webapp_places",
        ],
        check=True,
        cwd=str(_PROJECT_ROOT),
    )

    if args.build_pdf:
        print("Building osobnjaki PDF …")
        subprocess.run(
            [
                sys.executable,
                "-m",
                "scripts.build_pdf",
                "--guide",
                "osobnjaki",
                "--build-with-available",
                "--build-only",
            ],
            check=True,
            cwd=str(_PROJECT_ROOT),
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
