# -*- coding: utf-8 -*-
"""Скачивание фото Смоленска из image_source_url (плоская папка images/)."""

from __future__ import annotations

import argparse
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from smolensk.data.places_registry import SMOLENSK_PLACES
from smolensk.image_optimize import optimize_raster_image_if_large
from smolensk.whitelist import default_whitelist_path, url_is_whitelisted
from scripts.city_guide_core import min_bytes_for_filename
# Титул гида (не в smolensk_places.json); только upload.wikimedia.org.
_TITLE_PAGE_ASSETS: tuple[tuple[str, str], ...] = (
    (
        "images/title_coat_governorate_1856.svg",
        "https://upload.wikimedia.org/wikipedia/commons/b/b0/"
        "Coat_of_arms_of_Smolensk_governorate_1856.svg",
    ),
    (
        "images/title_coat_city_2000_il76m.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/7/72/"
        "Coat_of_arms_of_Smolensk_%282000%2C_Il-76M%29.jpg",
    ),
    (
        "images/title_coat_oblast.svg",
        "https://upload.wikimedia.org/wikipedia/commons/9/9e/"
        "Coat_of_arms_of_Smolensk_oblast.svg",
    ),
    (
        "images/title_coat_vinkler.gif",
        "https://upload.wikimedia.org/wikipedia/commons/e/e2/"
        "Coat_of_Arms_of_Smolensk_%28Vinkler%29.gif",
    ),
    (
        "images/title_coat_soviet.png",
        "https://upload.wikimedia.org/wikipedia/commons/2/28/"
        "Coat_of_Arms_of_Smolensk_soviet.png",
    ),
)
# Логотипы «Региональные вузы»: scripts/download_smolensk_vuzopedia_logos.py
_USER_AGENT = (
    "ExcursionGuide-Smolensk/1.0 (batch download for local guide; "
    "Python urllib; respectful throttling)"
)


def _commons_thumb_url(original: str, width_px: int) -> str | None:
    """Commons -> /thumb/.../Wpx-name."""
    parsed = urllib.parse.urlparse(original)
    if parsed.netloc.lower() != "upload.wikimedia.org":
        return None
    path = parsed.path
    if "/wikipedia/commons/thumb/" in path:
        return None
    marker = "/wikipedia/commons/"
    pos = path.find(marker)
    if pos < 0:
        return None
    rest = path[pos + len(marker) :].lstrip("/")
    if not rest or "/" not in rest:
        return None
    fname = rest.rsplit("/", 1)[-1]
    if not fname:
        return None
    thumb_path = "/wikipedia/commons/thumb/{}/{}px-{}".format(
        rest, width_px, fname,
    )
    return urllib.parse.urlunparse(parsed._replace(path=thumb_path))


def _candidate_urls(source_url: str, thumb_width: int | None) -> list[str]:
    out: list[str] = []
    if thumb_width and thumb_width > 0:
        t = _commons_thumb_url(source_url, thumb_width)
        if t and t != source_url:
            out.append(t)
    if source_url not in out:
        out.append(source_url)
    return out


def _fetch_bytes(
    url: str,
    timeout_sec: int,
    *,
    min_len: int,
) -> tuple[str, bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            data = resp.read()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "404", b""
        if e.code == 429:
            return "429", b""
        return "err", str(e).encode()
    except (urllib.error.URLError, OSError) as e:
        low = str(e).lower()
        if "429" in low or "too many requests" in low:
            return "429", b""
        return "err", str(e).encode()
    if len(data) < min_len:
        return "err", b"response too small"
    return "ok", data


def _download_place_image(
    urls: list[str],
    dest: Path,
    *,
    timeout_sec: int,
    retries_429: int,
    pause_429_sec: float,
) -> tuple[bool, str]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    min_len = min_bytes_for_filename(dest.name)
    last_err = "no URL"
    for u in urls:
        attempt = 0
        while attempt < max(1, retries_429):
            status, data = _fetch_bytes(u, timeout_sec, min_len=min_len)
            if status == "ok":
                dest.write_bytes(data)
                return True, "ok"
            if status == "404":
                last_err = "HTTP 404 (try next URL)"
                break
            if status == "429":
                wait = pause_429_sec + attempt * 15.0
                print(
                    "  429: sleep {:.0f}s, retry {}/{} ...".format(
                        wait, attempt + 1, retries_429,
                    ),
                    file=sys.stderr,
                )
                time.sleep(wait)
                attempt += 1
                last_err = "HTTP 429 (exhausted retries)"
                continue
            last_err = data.decode("utf-8", errors="replace") if data else status
            break
    return False, last_err


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download Smolensk guide images into smolensk/images/.",
    )
    parser.add_argument(
        "--smolensk-root",
        type=Path,
        default=_PROJECT_ROOT / "smolensk",
        help="Smolensk tree root (default: smolensk/)",
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
        help="Pause between finished downloads (default 3.5).",
    )
    parser.add_argument(
        "--thumb-width",
        type=int,
        default=1280,
        metavar="PX",
        help="Commons /thumb/ width (default 1280). 0 = originals only.",
    )
    parser.add_argument(
        "--full-size",
        action="store_true",
        help="Download originals only (higher 429 risk).",
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
    parser.add_argument(
        "--timeout",
        type=int,
        default=90,
        metavar="SEC",
        help="Request timeout (default 90).",
    )
    parser.add_argument(
        "--no-optimize",
        action="store_true",
        help="Do not recompress local files over ~350 KiB after download.",
    )
    args = parser.parse_args()
    root = args.smolensk_root.resolve()
    wpath = default_whitelist_path()

    if args.full_size:
        thumb_w: int | None = None
    else:
        thumb_w = args.thumb_width if args.thumb_width > 0 else None

    todo: list[tuple[str, str, Path]] = []
    n_incomplete = 0
    n_not_whitelisted = 0
    n_already_on_disk = 0

    def _queue(url: str, rel: str, label: str) -> None:
        nonlocal n_not_whitelisted, n_already_on_disk
        if not args.no_whitelist_check and not url_is_whitelisted(
            url, whitelist_path=wpath,
        ):
            n_not_whitelisted += 1
            print(
                "skip {}: URL not whitelisted: {}".format(label, url),
                file=sys.stderr,
            )
            return
        dest = root / rel
        if dest.is_file() and not args.force:
            n_already_on_disk += 1
            print("exists: {}".format(rel))
            return
        todo.append((label, url, dest))

    for place in SMOLENSK_PLACES:
        slug = place.get("slug", "?")
        url = place.get("image_source_url")
        rel = place.get("image_rel_path")
        if not url or not rel:
            n_incomplete += 1
            print(
                "skip {}: need image_source_url and image_rel_path".format(slug),
                file=sys.stderr,
            )
            continue
        _queue(url, rel, slug)
        for j, extra in enumerate(place.get("additional_images") or [], start=1):
            eu = extra.get("image_source_url")
            er = extra.get("image_rel_path")
            if not eu or not er:
                print(
                    "skip {} additional #{}: need URL and path".format(slug, j),
                    file=sys.stderr,
                )
                continue
            _queue(eu, er, "{}:extra{}".format(slug, j))

    for rel, url in _TITLE_PAGE_ASSETS:
        short = rel.replace("images/", "").replace("/", "_")[:24]
        _queue(url, rel, "title:{}".format(short))

    if not todo:
        n = len(SMOLENSK_PLACES)
        if n == 0:
            print(
                "No entries in SMOLENSK_PLACES — add smolensk_places.json.",
                file=sys.stderr,
            )
        elif n_already_on_disk == n and n_incomplete == 0 and n_not_whitelisted == 0:
            print(
                "All {} place(s) already have images; use --force to "
                "re-download.".format(n),
            )
        else:
            print(
                "Nothing to download. Summary: {} place(s); incomplete: {}; "
                "not whitelisted: {}; on disk: {}.".format(
                    n, n_incomplete, n_not_whitelisted, n_already_on_disk,
                ),
                file=sys.stderr,
            )
        return 0

    if thumb_w:
        print(
            "Commons thumbnails ~{}px + {:.1f}s between files; "
            "429 -> up to {} retries.".format(
                thumb_w, args.delay, args.retries_429,
            ),
        )
    else:
        print(
            "Full-size URLs + {:.1f}s delay.".format(args.delay),
        )

    ok_n = err_n = 0
    for i, (slug, url, dest) in enumerate(todo):
        if slug.startswith("title:"):
            cands = [url]
        else:
            cands = _candidate_urls(url, thumb_w)
        ok, msg = _download_place_image(
            cands,
            dest,
            timeout_sec=args.timeout,
            retries_429=args.retries_429,
            pause_429_sec=args.pause_429,
        )
        if ok:
            print("OK {} -> {}".format(slug, dest.relative_to(root)))
            if not args.no_optimize and optimize_raster_image_if_large(dest):
                print(
                    "  (optimized >350 KiB) {}".format(
                        dest.relative_to(root),
                    ),
                )
            ok_n += 1
        else:
            print("FAIL {}: {}".format(slug, msg), file=sys.stderr)
            err_n += 1
        if i + 1 < len(todo) and args.delay > 0:
            time.sleep(args.delay)
    print("Done: {} downloaded, {} failed.".format(ok_n, err_n))
    return 0 if err_n == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
