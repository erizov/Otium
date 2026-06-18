# -*- coding: utf-8 -*-
"""Wait for Moscow/SPB osobnjaki, then rebuild all city guide PDFs."""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from moscow.data.osobnjaki import OSOBNJAKI
from scripts.city_guide_core import DOWNLOAD_MAX_IMAGES_PER_PLACE
from scripts.city_guide_core import MIN_IMAGE_BYTES


def _moscow_complete() -> bool:
    img_dir = _PROJECT_ROOT / "moscow" / "images" / "moscow_osobnjaki"
    if not img_dir.is_dir():
        return False
    ok = 0
    for item in OSOBNJAKI:
        prefix = Path(item["images"][0]).name.rsplit("_", 1)[0]
        count = sum(
            1
            for p in img_dir.glob("{}_*.jpg".format(prefix))
            if p.stat().st_size >= MIN_IMAGE_BYTES
        )
        if count >= DOWNLOAD_MAX_IMAGES_PER_PLACE:
            ok += 1
    return ok >= len(OSOBNJAKI)


def _spb_complete() -> bool:
    from spb.data.osobnjaki import OSOBNJAKI as SPB_OS
    img_dir = _PROJECT_ROOT / "spb" / "images" / "spb_osobnjaki"
    if not img_dir.is_dir():
        return False
    ok = 0
    for item in SPB_OS:
        prefix = Path(item["images"][0]).name.rsplit("_", 1)[0]
        count = sum(
            1
            for p in img_dir.glob("{}_*.jpg".format(prefix))
            if p.stat().st_size >= MIN_IMAGE_BYTES
        )
        if count >= DOWNLOAD_MAX_IMAGES_PER_PLACE:
            ok += 1
    return ok >= len(SPB_OS)


def main() -> int:
    poll = 300
    print("Waiting for Moscow osobnjaki 50/50 at {}/{} images …".format(
        DOWNLOAD_MAX_IMAGES_PER_PLACE, DOWNLOAD_MAX_IMAGES_PER_PLACE,
    ))
    while not _moscow_complete():
        subprocess.run(
            [sys.executable, str(_PROJECT_ROOT / "scripts" / "osobnjaki_status.py")],
            cwd=str(_PROJECT_ROOT),
        )
        time.sleep(poll)
    print("Moscow complete. Rebuilding osobnjaki PDF …")
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
        [sys.executable, "-m", "scripts.export_moscow_webapp_places"],
        check=True,
        cwd=str(_PROJECT_ROOT),
    )
    print("Starting SPB osobnjaki bootstrap …")
    subprocess.run(
        [sys.executable, str(_PROJECT_ROOT / "scripts" / "bootstrap_spb_osobnjaki.py"),
         "--build-pdf"],
        check=True,
        cwd=str(_PROJECT_ROOT),
    )
    print(
        "Waiting for SPB osobnjaki 50/50 at {}/{} images …".format(
            DOWNLOAD_MAX_IMAGES_PER_PLACE, DOWNLOAD_MAX_IMAGES_PER_PLACE,
        ),
    )
    while not _spb_complete():
        subprocess.run(
            [
                sys.executable,
                str(_PROJECT_ROOT / "scripts" / "spb_osobnjaki_status.py"),
            ],
            cwd=str(_PROJECT_ROOT),
        )
        time.sleep(poll)
    print("SPB osobnjaki ready. Downloading missing images for other cities …")
    subprocess.run(
        [
            sys.executable,
            str(_PROJECT_ROOT / "scripts" / "download_missing_registry_images.py"),
        ],
        check=True,
        cwd=str(_PROJECT_ROOT),
    )
    print("Rebuilding all city guide PDFs (2-image rule) …")
    subprocess.run(
        [
            sys.executable,
            str(_PROJECT_ROOT / "scripts" / "rebuild_stale_city_guide_pdfs.py"),
            "--force-all",
        ],
        check=True,
        cwd=str(_PROJECT_ROOT),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
