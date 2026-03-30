# -*- coding: utf-8 -*-
"""Скачивание логотипов для блока «Региональные вузы» с vuzopedia.ru."""

from __future__ import annotations

import argparse
import html as html_module
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from smolensk.image_optimize import optimize_raster_image_if_large
from smolensk.whitelist import default_whitelist_path, url_is_whitelisted
from scripts.city_guide_core import min_bytes_for_filename

_LIST_URL = "https://vuzopedia.ru/region/city/90?page=1"
_USER_AGENT = (
    "ExcursionGuide-Smolensk/1.0 (Vuzopedia logos; Python urllib; throttled)"
)
_ROW_RE = re.compile(
    r'<div class="col-md-12 itemCityLeftVuz">'
    r'<a href="(/vuz/\d+)">([^<]+)</a>\s*'
    r'<div><a href="/vuz/\d+"[^>]*>([^<]+)</a></div>\s*'
    r"</div>",
    re.DOTALL,
)


def _page_html() -> str:
    req = urllib.request.Request(
        _LIST_URL,
        headers={"User-Agent": _USER_AGENT},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read()
    return raw.decode("utf-8", errors="replace")


def _large_logo_urls(html: str) -> list[str]:
    imgs = re.findall(r'<img[^>]+src="([^"]+)"', html, re.I)
    return [
        u for u in imgs
        if "0_400" in u and "vuzopedia.ru" in u
    ]


def _parse_entries(html: str) -> list[tuple[str, str, str, str]]:
    """Кортежи: path /vuz/ID, короткое имя, полное имя, числовой id."""
    logos = _large_logo_urls(html)
    rows = _ROW_RE.findall(html)
    out: list[tuple[str, str, str, str]] = []
    for i, row in enumerate(rows):
        if i >= len(logos):
            break
        vpath, short, long_html = row
        vid = vpath.rsplit("/", 1)[-1]
        long_name = html_module.unescape(long_html.strip())
        out.append((vpath, short.strip(), long_name, vid))
    return out


def _fetch_file(url: str, dest: Path, *, timeout: int) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    min_len = min_bytes_for_filename(dest.name)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
    if len(data) < min_len:
        raise ValueError("response too small: {}".format(len(data)))
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Download first N university logos from Vuzopedia Smolensk page 1."
        ),
    )
    parser.add_argument(
        "--smolensk-root",
        type=Path,
        default=_PROJECT_ROOT / "smolensk",
        help="Smolensk tree root (default: smolensk/)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        metavar="N",
        help="How many institutes from the top of the list (default 10).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-download even if file exists.",
    )
    parser.add_argument(
        "--no-whitelist-check",
        action="store_true",
        help="Skip whitelist validation (not recommended).",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        metavar="SEC",
        help="Pause between downloads (default 2).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=90,
        metavar="SEC",
        help="HTTP timeout (default 90).",
    )
    parser.add_argument(
        "--no-optimize",
        action="store_true",
        help="Do not recompress large rasters after download.",
    )
    args = parser.parse_args()
    root = args.smolensk_root.resolve()
    images = root / "images"
    wpath = default_whitelist_path()

    html = _page_html()
    entries = _parse_entries(html)
    logos = _large_logo_urls(html)
    if len(entries) < args.limit:
        print(
            "Expected at least {} entries, got {}.".format(
                args.limit, len(entries),
            ),
            file=sys.stderr,
        )
        return 2
    if len(logos) < args.limit:
        print(
            "Expected at least {} logo URLs, got {}.".format(
                args.limit, len(logos),
            ),
            file=sys.stderr,
        )
        return 2

    for i in range(args.limit):
        _vpath, _short, _long, vid = entries[i]
        url = logos[i]
        if not args.no_whitelist_check and not url_is_whitelisted(
            url, whitelist_path=wpath,
        ):
            print("Not whitelisted: {}".format(url), file=sys.stderr)
            return 1
        dest = images / "title_univ_regional_{}.jpg".format(vid)
        if dest.is_file() and not args.force:
            print("skip exists", dest.name)
            continue
        try:
            _fetch_file(url, dest, timeout=args.timeout)
        except (urllib.error.HTTPError, urllib.error.URLError, OSError) as e:
            print("{}: {}".format(url, e), file=sys.stderr)
            return 1
        except ValueError as e:
            print("{}".format(e), file=sys.stderr)
            return 1
        print("ok", dest.name)
        if not args.no_optimize:
            optimize_raster_image_if_large(dest)
        time.sleep(max(0.0, args.delay))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
