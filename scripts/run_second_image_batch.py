# -*- coding: utf-8 -*-
"""Batch: second-image download per city, PDF rebuild, stats every 30 min.

Image sources per place (in order): registry/sidecar URL, Commons, trusted
hosts (Openverse whitelist + Wikipedia), then Yandex Images, Openverse,
Flickr, Pixabay/Pexels (opt-in via PIXABAY_ENABLE / PEXELS_ENABLE), Unsplash, Pastvu. Optional ``--yandex-maps``.
Subject filter (people/animals) and perceptual dedup are on by default.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.download_city_second_images import cities_needing_second
from scripts.download_city_second_images import download_city_second_images
from scripts.city_guide_copy import install_guide_copy_patch

install_guide_copy_patch()


def _print_stats(label: str) -> None:
    print("\n=== SECOND_IMAGE_STATS {} ===".format(label), flush=True)
    subprocess.run(
        [sys.executable, str(_PROJECT_ROOT / "scripts" / "stats_city_guide_images_per_place.py")],
        cwd=str(_PROJECT_ROOT),
        check=False,
    )
    need = cities_needing_second()
    print(
        "Cities still needing 2nd image: {} ({} places)".format(
            len(need),
            sum(n for _, n in need),
        ),
        flush=True,
    )
    if need[:8]:
        print(
            "  top: " + ", ".join("{}({})".format(s, n) for s, n in need[:8]),
            flush=True,
        )


def _stats_loop(stop: threading.Event, interval_sec: int) -> None:
    tick = 0
    while not stop.wait(interval_sec):
        tick += 1
        _print_stats("tick #{}".format(tick))


def _rebuild_city(slug: str, *, image_wait_ms: int) -> int:
    script = _PROJECT_ROOT / "scripts" / "build_{}_pdf.py".format(slug)
    if not script.is_file():
        print("No builder for", slug, file=sys.stderr)
        return 2
    env = dict(os.environ)
    env["CITY_GUIDE_NO_TRANSLATE"] = "1"
    bootstrap = (
        "import runpy, sys\n"
        "from pathlib import Path\n"
        "root = Path({root!r})\n"
        "if str(root) not in sys.path:\n"
        "    sys.path.insert(0, str(root))\n"
        "from scripts.city_guide_copy import install_guide_copy_patch\n"
        "install_guide_copy_patch()\n"
        "sys.argv = [{script!r}, '--image-wait-ms', {wait!r}]\n"
        "code = runpy.run_path({script!r}, run_name='__main__')\n"
        "raise SystemExit(code if code is not None else 0)\n"
    ).format(
        root=str(_PROJECT_ROOT),
        script=str(script),
        wait=str(image_wait_ms),
    )
    proc = subprocess.run(
        [sys.executable, "-c", bootstrap],
        cwd=str(_PROJECT_ROOT),
        check=False,
        env=env,
    )
    return int(proc.returncode)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cities",
        nargs="*",
        default=None,
        metavar="SLUG",
        help="Default: all registry cities needing a 2nd image.",
    )
    parser.add_argument(
        "--stats-interval",
        type=int,
        default=1800,
        metavar="SEC",
        help="Print stats every N seconds (default 1800 = 30 min). 0 = off.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=6.0,
        metavar="SEC",
        help="Pause after each 1-image place (search + download).",
    )
    parser.add_argument(
        "--yandex-maps",
        action="store_true",
        help="Also search Yandex Maps per place (Playwright; slow).",
    )
    parser.add_argument(
        "--max-per-source",
        type=int,
        default=4,
        metavar="N",
        help="Max URLs per extended source (Yandex, Flickr, Openverse, …).",
    )
    parser.add_argument(
        "--city-pause",
        type=float,
        default=30.0,
        metavar="SEC",
        help="Pause between cities (Commons API cooldown).",
    )
    parser.add_argument(
        "--image-wait-ms",
        type=int,
        default=120000,
        metavar="MS",
        help="Playwright image wait for PDF rebuild.",
    )
    parser.add_argument(
        "--skip-rebuild",
        action="store_true",
        help="Download only; do not rebuild PDF after each city.",
    )
    parser.add_argument(
        "--no-subject-filter",
        action="store_true",
        help="Disable person/animal main-subject rejection (on by default).",
    )
    args = parser.parse_args()

    if args.no_subject_filter:
        os.environ["SUBJECT_FILTER"] = "0"

    if args.cities:
        slugs = [s.strip().lower() for s in args.cities]
    else:
        slugs = [s for s, _ in cities_needing_second()]

    if not slugs:
        print("No cities need second images.")
        return 0

    print(
        "Second-image batch: {} cities at {}".format(
            len(slugs),
            datetime.now().strftime("%Y-%m-%d %H:%M"),
        ),
        flush=True,
    )
    _print_stats("start")

    stop = threading.Event()
    stats_thread = None
    if args.stats_interval > 0:
        stats_thread = threading.Thread(
            target=_stats_loop,
            args=(stop, args.stats_interval),
            daemon=True,
        )
        stats_thread.start()

    failed_rebuild: list[str] = []
    for i, slug in enumerate(slugs, 1):
        print(
            "\n[{}/{}] === {} ===".format(i, len(slugs), slug),
            flush=True,
        )
        download_city_second_images(
            slug,
            delay_sec=args.delay,
            include_yandex_maps=args.yandex_maps,
            max_per_source=max(1, args.max_per_source),
        )
        if args.city_pause > 0 and i < len(slugs):
            time.sleep(args.city_pause)
        if not args.skip_rebuild:
            print("Rebuilding PDF for {} …".format(slug), flush=True)
            code = _rebuild_city(slug, image_wait_ms=args.image_wait_ms)
            if code != 0:
                failed_rebuild.append(slug)
                print("PDF rebuild failed for {} (exit {})".format(slug, code))

    stop.set()
    if stats_thread is not None:
        stats_thread.join(timeout=2.0)
    _print_stats("final")

    if failed_rebuild:
        print("Rebuild failures:", ", ".join(failed_rebuild), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
