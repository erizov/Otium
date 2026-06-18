# -*- coding: utf-8 -*-
"""Wait for batch-1 images, then bootstrap batch-2 and export (50 mansions)."""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from moscow.data.osobnjaki import OSOBNJAKI_CORE
from scripts.city_guide_core import MIN_IMAGE_BYTES


def _batch1_complete() -> bool:
    img_dir = _PROJECT_ROOT / "moscow" / "images" / "moscow_osobnjaki"
    if not img_dir.is_dir():
        return False
    prefixes = set()
    for item in OSOBNJAKI_CORE:
        for img in item["images"]:
            prefixes.add(Path(img).name.rsplit("_", 1)[0])
            break
    ok = 0
    for prefix in prefixes:
        count = sum(
            1
            for path in img_dir.glob("{}_*.jpg".format(prefix))
            if path.stat().st_size >= MIN_IMAGE_BYTES
        )
        if count >= 4:
            ok += 1
    return ok >= len(OSOBNJAKI_CORE)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--poll-sec",
        type=int,
        default=300,
        help="Seconds between batch-1 completion checks (default 300).",
    )
    parser.add_argument(
        "--skip-wait",
        action="store_true",
        help="Do not wait for batch 1; download all missing now.",
    )
    parser.add_argument(
        "--build-pdf",
        action="store_true",
        help="Build osobnjaki PDF after export.",
    )
    args = parser.parse_args()

    if not args.skip_wait:
        print("Waiting for batch 1 (20 mansions) image download to finish…")
        while not _batch1_complete():
            subprocess.run(
                [sys.executable, str(_PROJECT_ROOT / "scripts" / "osobnjaki_status.py")],
                cwd=str(_PROJECT_ROOT),
            )
            time.sleep(max(60, args.poll_sec))
        print("Batch 1 complete. Starting batch 2 pipeline…")

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
    print("Downloading images for all 50 osobnjaki…")
    subprocess.run(cmd, check=True, cwd=str(_PROJECT_ROOT))

    print("Exporting moscow_places.json…")
    subprocess.run(
        [sys.executable, "-m", "scripts.export_moscow_webapp_places"],
        check=True,
        cwd=str(_PROJECT_ROOT),
    )

    if args.build_pdf:
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

    subprocess.run(
        [sys.executable, str(_PROJECT_ROOT / "scripts" / "osobnjaki_status.py")],
        cwd=str(_PROJECT_ROOT),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
