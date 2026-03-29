# -*- coding: utf-8 -*-
"""Скачивание фото SPB из полей image_source_url в spb/data/places_registry.py."""

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

from spb.data.places_registry import SPB_PLACES
from spb.whitelist import default_whitelist_path, url_is_whitelisted

MIN_IMAGE_BYTES = 500
# Титул гида (не в spb_places.json); upload.wikimedia.org в whitelist.
_HERALD_ASSETS: tuple[tuple[str, str], ...] = (
    (
        "images/guide_coat_of_arms.png",
        "https://upload.wikimedia.org/wikipedia/commons/3/3c/"
        "Coat_of_arms_of_Saint_Petersburg_%282003%29.png",
    ),
    (
        "images/guide_flag.svg",
        "https://upload.wikimedia.org/wikipedia/commons/c/ca/"
        "Flag_of_Saint_Petersburg.svg",
    ),
)
# Титул: исторические гербы + вузы (полный файл, без /thumb/ — как у Смоленска).
_TITLE_PAGE_ASSETS: tuple[tuple[str, str], ...] = (
    (
        "images/title_spb_coat_proposal_xix.svg",
        "https://upload.wikimedia.org/wikipedia/commons/4/43/"
        "Coat_of_Arms_of_St_Petersburg_proposal_large_%28XIX_century%29.svg",
    ),
    (
        "images/title_spb_coat_1730_1856.svg",
        "https://upload.wikimedia.org/wikipedia/commons/8/87/"
        "Petersburg_coat_of_arms_1730_to_1856.svg",
    ),
    (
        "images/title_russian_empire_great_coat_1882_1917.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/b/b5/"
        "Great_State_Coat_of_Arms_of_the_Russian_Empire._1882-1917.jpg",
    ),
    (
        "images/title_univ_spbgu.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/1/18/"
        "5175-2._St._Petersburg._Building_of_the_Twelve_Collegia.jpg",
    ),
    (
        "images/title_univ_itmo.png",
        "https://upload.wikimedia.org/wikipedia/commons/4/43/"
        "ITMO_University_official_logo_horizontal.png",
    ),
    (
        "images/title_univ_spbpu.png",
        "https://upload.wikimedia.org/wikipedia/commons/f/f8/"
        "St_Petersburg_State_Polytechnical_University_emblem.png",
    ),
    (
        "images/title_univ_leti.svg",
        "https://upload.wikimedia.org/wikipedia/commons/e/e5/"
        "ETU_%C2%ABLETI%C2%BB_official_logo.svg",
    ),
    (
        "images/title_univ_herzen.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/b/b4/"
        "Herzen_State_Pedagogical_University_of_Russia%2C_main_building.jpg",
    ),
    (
        "images/title_univ_unecon.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/7/7b/"
        "Unecon_logo_2.jpg",
    ),
    (
        "images/title_univ_pavlov.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/b/b8/"
        "0477Ca._%D0%9F%D0%B5%D1%80%D0%B2%D1%8B%D0%B9_"
        "%D0%9C%D0%B5%D0%B4%D0%B8%D1%86%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%D0%B9_"
        "%D1%83%D0%BD%D0%B8%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D1%82%D0%B5%D1%82_"
        "%D0%B8%D0%BC%D0%B5%D0%BD%D0%B8_%D0%9F%D0%B0%D0%B2%D0%BB%D0%BE%D0%B2%D0%B0.jpg",
    ),
    (
        "images/title_univ_rshu.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/d/d6/RSHU.jpg",
    ),
    (
        "images/title_univ_lesgaft.png",
        "https://upload.wikimedia.org/wikipedia/commons/2/21/"
        "Logo_lesgaft_mini.png",
    ),
    (
        "images/title_univ_pushkin.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/8/85/"
        "8857.1._Pushkin._Oktyabrsky_Boulevard%2C_18.jpg",
    ),
)
_USER_AGENT = (
    "ExcursionGuide-SP/1.0 (batch download for local SPB guide; "
    "Python urllib; respectful throttling)"
)


def _commons_thumb_url(original: str, width_px: int) -> str | None:
    """Прямой URL Commons -> /thumb/.../Wpx-name (рекомендация при массовой загрузке)."""
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


def _fetch_bytes(url: str, timeout_sec: int) -> tuple[str, bytes]:
    """Возвращает ('ok', data) | ('404', b'') | ('429', b'') | ('err', b'')."""
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
    if len(data) < MIN_IMAGE_BYTES:
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
    last_err = "no URL"
    for u in urls:
        attempt = 0
        while attempt < max(1, retries_429):
            status, data = _fetch_bytes(u, timeout_sec)
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
        description="Download SPB guide images from image_source_url into spb/.",
    )
    parser.add_argument(
        "--spb-root",
        type=Path,
        default=_PROJECT_ROOT / "spb",
        help="SPB tree root (default: spb/)",
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
    args = parser.parse_args()
    root = args.spb_root.resolve()
    wpath = default_whitelist_path()

    for rel, url in _HERALD_ASSETS:
        dest = root / rel
        if dest.is_file() and not args.force:
            print("exists: {}".format(rel))
            continue
        if not args.no_whitelist_check and not url_is_whitelisted(
            url, whitelist_path=wpath,
        ):
            print(
                "skip herald {}: URL not whitelisted".format(rel),
                file=sys.stderr,
            )
            continue
        ok, msg = _download_place_image(
            [url],
            dest,
            timeout_sec=args.timeout,
            retries_429=args.retries_429,
            pause_429_sec=args.pause_429,
        )
        if ok:
            print("OK herald -> {}".format(dest.relative_to(root)))
        else:
            print("FAIL herald {}: {}".format(rel, msg), file=sys.stderr)

    for rel, url in _TITLE_PAGE_ASSETS:
        dest = root / rel
        if dest.is_file() and not args.force:
            print("exists: {}".format(rel))
            continue
        if not args.no_whitelist_check and not url_is_whitelisted(
            url, whitelist_path=wpath,
        ):
            print(
                "skip title {}: URL not whitelisted".format(rel),
                file=sys.stderr,
            )
            continue
        ok, msg = _download_place_image(
            [url],
            dest,
            timeout_sec=args.timeout,
            retries_429=args.retries_429,
            pause_429_sec=args.pause_429,
        )
        if ok:
            print("OK title -> {}".format(dest.relative_to(root)))
        else:
            print("FAIL title {}: {}".format(rel, msg), file=sys.stderr)
        if args.delay > 0:
            time.sleep(args.delay)

    if args.full_size:
        thumb_w: int | None = None
    else:
        thumb_w = args.thumb_width if args.thumb_width > 0 else None

    todo: list[tuple[str, str, Path]] = []
    n_incomplete = 0
    n_not_whitelisted = 0
    n_already_on_disk = 0
    for place in SPB_PLACES:
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
        if not args.no_whitelist_check and not url_is_whitelisted(
            url, whitelist_path=wpath,
        ):
            n_not_whitelisted += 1
            print(
                "skip {}: URL not whitelisted: {}".format(slug, url),
                file=sys.stderr,
            )
            continue
        dest = root / rel
        if dest.is_file() and not args.force:
            n_already_on_disk += 1
            print("exists: {}".format(rel))
        else:
            todo.append((slug, url, dest))

        for j, extra in enumerate(place.get("additional_images") or [], start=1):
            eu = extra.get("image_source_url")
            er = extra.get("image_rel_path")
            if not eu or not er:
                print(
                    "skip {} additional #{}: need URL and path".format(slug, j),
                    file=sys.stderr,
                )
                continue
            if not args.no_whitelist_check and not url_is_whitelisted(
                eu, whitelist_path=wpath,
            ):
                print(
                    "skip {} additional #{}: not whitelisted".format(slug, j),
                    file=sys.stderr,
                )
                continue
            edest = root / er
            if edest.is_file() and not args.force:
                print("exists: {}".format(er))
                n_already_on_disk += 1
                continue
            todo.append(("{}:extra{}".format(slug, j), eu, edest))

    if not todo:
        n = len(SPB_PLACES)
        if n == 0:
            print(
                "No entries in SPB_PLACES - nothing to download. "
                "Add objects in spb/data/places_registry.py "
                "(image_source_url + image_rel_path).",
                file=sys.stderr,
            )
        elif n_already_on_disk == n and n_incomplete == 0 and n_not_whitelisted == 0:
            print(
                "All {} place(s) already have image files under spb/; "
                "nothing to download. Use --force to re-download.".format(n),
            )
        else:
            print(
                "Nothing to download. Summary: {} place(s) total; "
                "incomplete fields: {}; not whitelisted: {}; "
                "already on disk: {}.".format(
                    n, n_incomplete, n_not_whitelisted, n_already_on_disk,
                ),
                file=sys.stderr,
            )
        return 0

    if thumb_w:
        print(
            "Commons thumbnails ~{}px + {:.1f}s between files; "
            "429 -> up to {} retries (--full-size for originals).".format(
                thumb_w, args.delay, args.retries_429,
            ),
        )
    else:
        print(
            "Full-size URLs + {:.1f}s delay (expect 429; increase "
            "--delay / --pause-429).".format(args.delay),
        )

    ok_n = err_n = 0
    for i, (slug, url, dest) in enumerate(todo):
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
