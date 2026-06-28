# -*- coding: utf-8 -*-
"""Download historical heraldry for the Russian Architecture guide title strip."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from russian_architecture.data.history_heraldry import history_heraldry_download_pairs
from russian_architecture.whitelist import default_whitelist_path
from russian_architecture.whitelist import url_is_whitelisted

from scripts.download_spb_images import MIN_IMAGE_BYTES, _download_place_image


def download_history_heraldry(
    guide_root: Path,
    *,
    force: bool = False,
    no_whitelist_check: bool = False,
    timeout_sec: int = 90,
    retries_429: int = 4,
    pause_429_sec: float = 45.0,
    delay_sec: float = 2.0,
) -> int:
    """Download coats from Commons (see history_heraldry.HISTORY_HERALDRY)."""
    wpath = default_whitelist_path()
    pairs = history_heraldry_download_pairs()
    failures = 0
    for i, (rel, urls) in enumerate(pairs):
        dest = guide_root / rel.replace("\\", "/")
        if dest.is_file() and dest.stat().st_size >= MIN_IMAGE_BYTES and not force:
            print("exists: {}".format(rel))
            continue
        allowed = urls
        if not no_whitelist_check:
            allowed = [
                u for u in urls if url_is_whitelisted(u, whitelist_path=wpath)
            ]
            if not allowed:
                print("skip {}: URL not whitelisted".format(rel), file=sys.stderr)
                failures += 1
                continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        ok, msg = _download_place_image(
            allowed,
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
        description=(
            "Download historical Russian coats of arms for the architecture "
            "guide (from ru.wikipedia «История герба России»)."
        ),
    )
    parser.add_argument(
        "--guide-root",
        type=Path,
        default=_PROJECT_ROOT / "russian_architecture",
    )
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--no-whitelist-check", action="store_true")
    args = parser.parse_args()
    return download_history_heraldry(
        args.guide_root,
        force=args.force,
        no_whitelist_check=args.no_whitelist_check,
    )


if __name__ == "__main__":
    raise SystemExit(main())
