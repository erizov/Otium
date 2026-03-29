# -*- coding: utf-8 -*-
"""Wikimedia assets for the Moscow combined guide title page (output/images/)."""

from __future__ import annotations

import argparse
import shutil
import sys
import time
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from spb.whitelist import default_whitelist_path, url_is_whitelisted

from scripts.download_spb_images import (
    MIN_IMAGE_BYTES,
    _TITLE_PAGE_ASSETS,
    _download_place_image,
)

_MOSCOW_HERALDRY_URLS: tuple[tuple[str, str], ...] = (
    (
        "images/title_msk_russian_empire_lesser.svg",
        (
            "https://upload.wikimedia.org/wikipedia/commons/b/be/"
            "Lesser_coat_of_arms_of_the_Russian_Empire.svg"
        ),
    ),
    (
        "images/title_msk_bolshoi_basrelief_2025.jpg",
        (
            "https://upload.wikimedia.org/wikipedia/commons/6/60/"
            "Moscow_-_2025_-_The_bas-relief_of_Coat_of_Arms_of_the_Russian_"
            "Empire_on_facade_of_Bolshoi_Theatre1.jpg"
        ),
    ),
    (
        "images/title_msk_moscow_coat_soviet.svg",
        (
            "https://upload.wikimedia.org/wikipedia/commons/9/91/"
            "Coat_of_Arms_of_Moscow_%28Soviet%29.svg"
        ),
    ),
    (
        "images/title_msk_moscow_coat_empire.jpg",
        (
            "https://upload.wikimedia.org/wikipedia/commons/5/5c/"
            "Coat_of_Arms_of_Moscow_%28Russian_Empire%29.jpg"
        ),
    ),
)


def _univ_assets() -> tuple[tuple[str, str], ...]:
    return tuple(
        x for x in _TITLE_PAGE_ASSETS if x[0].startswith("images/title_univ_")
    )


def _copy_univ_from_spb(output_root: Path, rel: str) -> bool:
    """Reuse files from spb/images/ when the user already ran download_spb_images."""
    if not rel.startswith("images/title_univ_"):
        return False
    spb_file = _PROJECT_ROOT / "spb" / rel.replace("\\", "/")
    if not spb_file.is_file() or spb_file.stat().st_size < MIN_IMAGE_BYTES:
        return False
    dest = output_root / rel.replace("\\", "/")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(spb_file, dest)
    return True


def download_moscow_title_assets(
    output_dir: Path,
    *,
    force: bool = False,
    no_whitelist_check: bool = False,
    timeout_sec: int = 90,
    retries_429: int = 4,
    pause_429_sec: float = 45.0,
    delay_sec: float = 3.5,
) -> int:
    """
    Download Moscow heraldry + SPb university logos into output_dir.

    Returns 0 if all attempted downloads succeeded or were skipped (exists).
    """
    wpath = default_whitelist_path()
    root = output_dir.resolve()
    pairs = _MOSCOW_HERALDRY_URLS + _univ_assets()
    failures = 0
    for i, (rel, url) in enumerate(pairs):
        dest = root / rel.replace("\\", "/")
        if dest.is_file() and not force:
            print("exists: {}".format(rel))
            continue
        if not force and _copy_univ_from_spb(root, rel.replace("\\", "/")):
            print("copy spb -> {}".format(rel))
            continue
        if not no_whitelist_check and not url_is_whitelisted(
            url,
            whitelist_path=wpath,
        ):
            print(
                "skip {}: URL not whitelisted".format(rel),
                file=sys.stderr,
            )
            failures += 1
            continue
        ok, msg = _download_place_image(
            [url],
            dest,
            timeout_sec=timeout_sec,
            retries_429=retries_429,
            pause_429_sec=pause_429_sec,
        )
        if ok:
            print("OK -> {}".format(rel))
        else:
            print("FAIL {}: {}".format(rel, msg), file=sys.stderr)
            failures += 1
        if delay_sec > 0 and i + 1 < len(pairs):
            time.sleep(delay_sec)
    return 0 if failures == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download Moscow guide title-page images into output/.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=_PROJECT_ROOT / "output",
        help="Guide output root (default: output/)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-download even if file already exists.",
    )
    parser.add_argument(
        "--no-whitelist-check",
        action="store_true",
        help="Do not reject URLs outside SOURCES_WHITELIST.md.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=3.5,
        metavar="SEC",
        help="Pause between downloads (default 3.5).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=90,
        metavar="SEC",
        help="Request timeout (default 90).",
    )
    parser.add_argument(
        "--retries-429",
        type=int,
        default=4,
        metavar="N",
        help="429 retries per URL (default 4).",
    )
    parser.add_argument(
        "--pause-429",
        type=float,
        default=45.0,
        metavar="SEC",
        help="Base sleep after 429 (default 45).",
    )
    args = parser.parse_args()
    return download_moscow_title_assets(
        args.output_dir.resolve(),
        force=args.force,
        no_whitelist_check=args.no_whitelist_check,
        timeout_sec=args.timeout,
        retries_429=args.retries_429,
        pause_429_sec=args.pause_429,
        delay_sec=args.delay,
    )


if __name__ == "__main__":
    raise SystemExit(main())
