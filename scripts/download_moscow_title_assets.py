# -*- coding: utf-8 -*-
"""Title-page heraldry and university logos for the Moscow guide."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from spb.whitelist import default_whitelist_path, url_is_whitelisted

from scripts.download_spb_images import MIN_IMAGE_BYTES, _download_place_image
from scripts.moscow_title_assets_data import moscow_download_pairs


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
    Download Moscow heraldry, city symbols, and university logos.

    Returns 0 if all attempted downloads succeeded or were skipped (exists).
    """
    wpath = default_whitelist_path()
    root = output_dir.resolve()
    pairs = moscow_download_pairs()
    failures = 0
    for i, (rel, urls) in enumerate(pairs):
        dest = root / rel.replace("\\", "/")
        if dest.is_file() and not force:
            print("exists: {}".format(rel))
            continue
        allowed_urls = urls
        if not no_whitelist_check:
            allowed_urls = [
                u for u in urls if url_is_whitelisted(u, whitelist_path=wpath)
            ]
            if not allowed_urls:
                print(
                    "skip {}: URL not whitelisted".format(rel),
                    file=sys.stderr,
                )
                failures += 1
                continue
        ok, msg = _download_place_image(
            allowed_urls,
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
        default=_PROJECT_ROOT / "moscow",
        help="Guide output root (default: moscow/)",
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
