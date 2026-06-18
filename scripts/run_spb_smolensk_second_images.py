# -*- coding: utf-8 -*-
"""Second-image batch for Saint Petersburg and Smolensk only.

Same pipeline as ``run_second_image_batch.py``: registry/sidecar URL, Commons,
trusted hosts, Yandex Images, Openverse, Flickr, Unsplash, Pastvu (Pixabay/
Pexels opt-in). Subject filter (people/animals) and perceptual dedup on by
default. SPb is normally a frozen download city — this script enables it via
``allow_frozen``.

After each city, rebuilds ``build_spb_pdf.py`` / ``build_smolensk_pdf.py``
unless ``--skip-rebuild``.
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

DEFAULT_CITIES: tuple[str, ...] = ("spb", "smolensk")


def _print_stats(label: str, *, city_slugs: tuple[str, ...]) -> None:
    print("\n=== SPB/SMOLENSK SECOND_IMAGE_STATS {} ===".format(label), flush=True)
    subprocess.run(
        [
            sys.executable,
            str(_PROJECT_ROOT / "scripts" / "stats_city_guide_images_per_place.py"),
        ],
        cwd=str(_PROJECT_ROOT),
        check=False,
    )
    need = cities_needing_second(only_slugs=city_slugs, skip_frozen=False)
    print(
        "Places still needing 2nd image: {} ({} places)".format(
            len(need),
            sum(n for _, n in need),
        ),
        flush=True,
    )
    for slug, n in need:
        print("  {}: {}".format(slug, n), flush=True)


def _stats_loop(
    stop: threading.Event,
    interval_sec: int,
    *,
    city_slugs: tuple[str, ...],
) -> None:
    tick = 0
    while not stop.wait(interval_sec):
        tick += 1
        _print_stats("tick #{}".format(tick), city_slugs=city_slugs)


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
        default=list(DEFAULT_CITIES),
        metavar="SLUG",
        help="Default: spb smolensk.",
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

    slugs = [s.strip().lower() for s in args.cities]
    need_map = dict(
        cities_needing_second(only_slugs=slugs, skip_frozen=False),
    )
    slugs = [s for s in slugs if need_map.get(s, 0) > 0]

    if not slugs:
        print("No places need second images in", ", ".join(args.cities) or "—")
        return 0

    city_tuple = tuple(slugs)
    print(
        "SPB/Smolensk second-image batch: {} at {}".format(
            ", ".join(
                "{}({})".format(s, need_map[s]) for s in slugs
            ),
            datetime.now().strftime("%Y-%m-%d %H:%M"),
        ),
        flush=True,
    )
    _print_stats("start", city_slugs=city_tuple)

    stop = threading.Event()
    stats_thread = None
    if args.stats_interval > 0:
        stats_thread = threading.Thread(
            target=_stats_loop,
            args=(stop, args.stats_interval),
            kwargs={"city_slugs": city_tuple},
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
            allow_frozen=True,
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
    _print_stats("final", city_slugs=city_tuple)

    if failed_rebuild:
        print("Rebuild failures:", ", ".join(failed_rebuild), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
