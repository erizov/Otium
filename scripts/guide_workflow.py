# -*- coding: utf-8 -*-
"""
Shared workflow helpers: build all guides, dedup, compress large images.
Used by build_all_guides.py, build_all_guides_opt.py, build_all_guides_opt_dedup.py,
run_all.py, workflow_build_guides.py.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_image_optimize import CITY_GUIDE_IMAGE_MAX_BYTES
from scripts.city_guide_image_optimize import optimize_raster_image_if_large
from scripts.guide_constants import PROJECT_ROOT, get_images_root

BUILD_PDF_SCRIPT = _SCRIPT_DIR / "build_pdf.py"
DEDUP_SCRIPT = _SCRIPT_DIR / "dedup_all_folders.py"
DEFAULT_SIZE_LIMIT_BYTES = CITY_GUIDE_IMAGE_MAX_BYTES
SKIP_SUBDIRS = frozenset({"forbidden", "large_orig", "duplicates"})


def run_build_all_guides(
    optimized: bool = False,
    build_only: bool = True,
    build_with_available: bool = True,
    download_images: bool = False,
    download_retries: int | None = None,
) -> int:
    """
    Run build_pdf.py --all-guides. Returns exit code.
    """
    if not BUILD_PDF_SCRIPT.is_file():
        print("Error: build_pdf.py not found.", file=sys.stderr)
        return 1
    cmd = [sys.executable, str(BUILD_PDF_SCRIPT), "--all-guides"]
    if download_images:
        cmd.append("--build-with-available")
        if download_retries is not None:
            cmd.extend(["--download-retries", str(download_retries)])
    else:
        if build_only:
            cmd.append("--build-only")
        if build_with_available:
            cmd.append("--build-with-available")
    if optimized:
        cmd.append("--optimized")
    return subprocess.call(cmd, cwd=str(PROJECT_ROOT))


def run_dedup(images_root: Path | None = None) -> int:
    """
    Run dedup_all_folders.py. Uses EXCURSION_IMAGES_ROOT if images_root given.
    Returns exit code.
    """
    if not DEDUP_SCRIPT.is_file():
        print("Error: dedup_all_folders.py not found.", file=sys.stderr)
        return 1
    env = os.environ.copy()
    root = images_root or get_images_root()
    env["EXCURSION_IMAGES_ROOT"] = str(root)
    return subprocess.call(
        [sys.executable, str(DEDUP_SCRIPT)],
        cwd=str(PROJECT_ROOT),
        env=env,
    )


def run_compress_large(
    images_root: Path | None = None,
    size_limit_bytes: int = DEFAULT_SIZE_LIMIT_BYTES,
) -> int:
    """
    Optimize rasters larger than size_limit via city_guide_image_optimize.

    Copies originals to large_orig/ before rewrite. Returns files optimized.
    """
    root = images_root or get_images_root()
    if not root.is_dir():
        return 0
    count = 0
    for subdir in root.iterdir():
        if not subdir.is_dir() or subdir.name in SKIP_SUBDIRS:
            continue
        large_orig = subdir / "large_orig"
        for path in subdir.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
                continue
            try:
                if path.stat().st_size <= size_limit_bytes:
                    continue
            except OSError:
                continue
            try:
                large_orig.mkdir(parents=True, exist_ok=True)
                backup = large_orig / path.name
                if not backup.exists():
                    shutil.copy2(path, backup)
                if optimize_raster_image_if_large(
                    path,
                    max_bytes=size_limit_bytes,
                    verbose=True,
                ):
                    count += 1
                    print(
                        "  Compressed: {}".format(
                            path.relative_to(PROJECT_ROOT),
                        ),
                    )
            except Exception as e:
                print("  Skip {}: {}".format(path.name, e), file=sys.stderr)
    return count
