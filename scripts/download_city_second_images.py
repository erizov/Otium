# -*- coding: utf-8 -*-
"""Download one missing second image per place (trusted sources, single pass)."""

from __future__ import annotations

import argparse
import importlib
import json
import sys
import time
from collections.abc import Callable
from collections.abc import Sequence
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_commons_fetch import commons_file_upload_url
from scripts.city_guide_commons_fetch import commons_search_raster_title_for_city
from scripts.city_guide_core import DOWNLOAD_FROZEN_CITY_SLUGS
from scripts.city_guide_core import DOWNLOAD_MAX_IMAGES_PER_PLACE
from scripts.city_guide_core import MIN_IMAGE_BYTES
from scripts.city_guide_core import smallest_same_stem_image_rel
from scripts.city_guide_jerusalem_style_images import _fetch_bytes
from scripts.city_guide_jerusalem_style_images import snap_commons_thumb_width
from scripts.city_guide_jerusalem_style_images import _candidate_urls
from scripts.city_guide_core import min_bytes_for_filename
from scripts.image_subject_filter import check_image_bytes
from scripts.image_subject_filter import rejection_message
from scripts.image_subject_filter import subject_filter_enabled
from scripts.image_utils import image_content_hash
from scripts.image_utils import image_content_hash_from_bytes
from scripts.city_guide_registry_common import derive_second_image_rel
from scripts.city_guide_registry_common import load_second_image_sidecar
from scripts.city_guide_registry_common import merge_second_image_sidecar
from scripts.city_guide_registry_common import save_second_image_sidecar
from scripts.city_guide_second_image_sources import discover_extended_second_image_urls
from scripts.city_guide_trusted_image_sources import discover_trusted_image_urls
from scripts.rag.city_map import names_for_slug
from scripts.verify_city_guide_place_images import _REGISTRY


def _load_city_second_image_bundle(
    city_slug: str,
) -> tuple[
    list[dict],
    Path,
    Path,
    Path,
    Callable[..., bool],
] | None:
    """Load places, paths, and whitelist helpers for second-image download."""
    root = _PROJECT_ROOT / city_slug
    data_dir = root / "data"

    if city_slug == "moscow":
        path = data_dir / "moscow_places.json"
        if not path.is_file():
            print(city_slug, "skip: no moscow_places.json", file=sys.stderr)
            return None
        wl = importlib.import_module("moscow.whitelist")
        places = merge_second_image_sidecar(
            [dict(p) for p in json.loads(path.read_text(encoding="utf-8"))],
            data_dir,
            city_slug,
        )
        return (
            places,
            root,
            data_dir,
            wl.default_whitelist_path(),
            wl.url_is_whitelisted,
        )

    mod_name = "{}.data.places_registry".format(city_slug)
    wl_mod_name = "{}.whitelist".format(city_slug)
    try:
        reg = importlib.import_module(mod_name)
        wl = importlib.import_module(wl_mod_name)
    except ModuleNotFoundError as exc:
        print(city_slug, "skip:", exc, file=sys.stderr)
        return None

    attr = None
    for key in dir(reg):
        if key.endswith("_PLACES") and key.isupper():
            attr = key
            break
    if not attr:
        print(city_slug, "skip: no *_PLACES", file=sys.stderr)
        return None

    places = merge_second_image_sidecar(
        [dict(p) for p in getattr(reg, attr)],
        data_dir,
        city_slug,
    )
    return (
        places,
        root,
        data_dir,
        wl.default_whitelist_path(),
        wl.url_is_whitelisted,
    )


def _place_image_count(root: Path, place: dict) -> int:
    if place.get("suppress_images_for_pdf"):
        return -1
    n = 0
    rel = place.get("image_rel_path")
    if rel and smallest_same_stem_image_rel(root, rel):
        n += 1
    for item in place.get("additional_images") or []:
        er = item.get("image_rel_path")
        if er and smallest_same_stem_image_rel(root, er):
            n += 1
    return min(n, DOWNLOAD_MAX_IMAGES_PER_PLACE)


def _city_reject_hashes(root: Path) -> frozenset[str]:
    """Perceptual / SHA hashes of existing place images + forbidden/."""
    from scripts.download_with_dedup import _load_forbidden_hashes

    images_dir = root / "images"
    hashes: set[str] = set(_load_forbidden_hashes(images_dir))
    if not images_dir.is_dir():
        return frozenset(hashes)
    for path in images_dir.iterdir():
        if not path.is_file():
            continue
        if path.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
            continue
        if path.name.startswith("."):
            continue
        h = image_content_hash(path, min_bytes=MIN_IMAGE_BYTES)
        if h:
            hashes.add(h)
    return frozenset(hashes)


def _download_second_place_image(
    urls: list[str],
    dest: Path,
    *,
    timeout_sec: int,
    reject_hashes: frozenset[str],
) -> tuple[bool, str]:
    """Download with subject filter + dedup against existing guide images."""
    if not urls:
        return False, "no URL"
    dest.parent.mkdir(parents=True, exist_ok=True)
    min_len = min_bytes_for_filename(dest.name)
    last_err = "no URL"
    for u in urls:
        if not str(u).startswith(("http://", "https://")):
            continue
        status, data = _fetch_bytes(u, timeout_sec, min_len=min_len)
        if status != "ok":
            last_err = data.decode("utf-8", errors="replace") if data else status
            continue
        if subject_filter_enabled():
            verdict = check_image_bytes(data)
            if not verdict.accept:
                last_err = rejection_message(verdict)
                print(
                    "  subject reject {}: {}".format(dest.name, last_err),
                    file=sys.stderr,
                    flush=True,
                )
                continue
        h = image_content_hash_from_bytes(data, min_bytes=min_len)
        if h and h in reject_hashes:
            last_err = "duplicate of existing guide image"
            print(
                "  dedup reject {}: {}".format(dest.name, last_err),
                file=sys.stderr,
                flush=True,
            )
            continue
        dest.write_bytes(data)
        return True, "ok"
    return False, last_err


def _search_query(place: dict, city_slug: str) -> str:
    names = names_for_slug(city_slug)
    city_en = names.name_en or city_slug.replace("_", " ")
    for key in ("name_en", "name_ru", "name"):
        val = str(place.get(key) or "").strip()
        if val:
            return "{} {}".format(val, city_en).strip()
    return city_en


def _resolve_second_candidates(
    place: dict,
    city_slug: str,
    sidecar: dict[str, list[dict]],
    *,
    whitelist_path: Path,
    whitelist_fn: Callable[..., bool],
    include_yandex_maps: bool = False,
    max_per_source: int = 4,
    skip_pixabay: bool | None = None,
) -> tuple[str, list[str]]:
    """Return (rel_path, ordered unique image URLs to try)."""
    slug = str(place.get("slug") or "")
    primary_rel = str(place.get("image_rel_path") or "")
    primary_url = str(place.get("image_source_url") or "")
    if not primary_rel:
        return "", []

    rel = derive_second_image_rel(primary_rel)
    urls: list[str] = []
    seen: set[str] = set()

    def _add(url: str) -> None:
        u = url.strip()
        if not u or u == primary_url or u in seen:
            return
        if not whitelist_fn(u, whitelist_path=whitelist_path):
            return
        seen.add(u)
        urls.append(u)

    extras = list(place.get("additional_images") or [])
    if not extras:
        side = sidecar.get(slug) or []
        if side:
            extras = side

    for item in extras:
        eu = str(item.get("image_source_url") or "")
        if eu:
            _add(eu)

    query = _search_query(place, city_slug)
    title = commons_search_raster_title_for_city(query, city_slug, srlimit=12)
    if title:
        commons_url = commons_file_upload_url("File:{}".format(title))
        if commons_url:
            _add(commons_url)

    for trusted in discover_trusted_image_urls(
        query,
        whitelist_path=whitelist_path,
        url_is_whitelisted=whitelist_fn,
        exclude_url=primary_url,
    ):
        _add(trusted)

    for ext in discover_extended_second_image_urls(
        place,
        city_slug,
        query,
        whitelist_path=whitelist_path,
        url_is_whitelisted=whitelist_fn,
        exclude_url=primary_url,
        max_per_source=max_per_source,
        include_yandex_maps=include_yandex_maps,
        skip_pixabay=skip_pixabay,
    ):
        _add(ext)

    return rel, urls


def download_city_second_images(
    city_slug: str,
    *,
    delay_sec: float = 2.5,
    thumb_width: int = 330,
    timeout_sec: int = 90,
    include_yandex_maps: bool = False,
    max_per_source: int = 4,
    skip_pixabay: bool | None = None,
    allow_frozen: bool = False,
) -> tuple[int, int, int]:
    """
    Single-pass second-image download for one city.

    Returns (attempted, ok, skipped_already_two).
    """
    if city_slug in DOWNLOAD_FROZEN_CITY_SLUGS and not allow_frozen:
        print(city_slug, "skip (frozen city)")
        return 0, 0, 0

    bundle = _load_city_second_image_bundle(city_slug)
    if bundle is None:
        return 0, 0, 0
    places, root, data_dir, wpath, whitelist_fn = bundle
    sidecar = load_second_image_sidecar(data_dir, city_slug)
    thumb_w = snap_commons_thumb_width(thumb_width)
    reject_hashes = _city_reject_hashes(root)

    attempted = ok = already_two = 0
    for place in places:
        slug = str(place.get("slug") or "?")
        count = _place_image_count(root, place)
        if count < 0:
            continue
        if count >= DOWNLOAD_MAX_IMAGES_PER_PLACE:
            already_two += 1
            continue

        rel, url_candidates = _resolve_second_candidates(
            place,
            city_slug,
            sidecar,
            whitelist_path=wpath,
            whitelist_fn=whitelist_fn,
            include_yandex_maps=include_yandex_maps,
            max_per_source=max_per_source,
            skip_pixabay=skip_pixabay,
        )
        if not rel:
            continue
        if smallest_same_stem_image_rel(root, rel):
            already_two += 1
            if delay_sec > 0:
                time.sleep(delay_sec)
            continue

        if not url_candidates:
            print("  {}: no image URL".format(slug), flush=True)
            if delay_sec > 0:
                time.sleep(delay_sec)
            continue

        if not (place.get("additional_images") or sidecar.get(slug)):
            sidecar[slug] = [
                {
                    "image_rel_path": rel,
                    "image_source_url": url_candidates[0],
                },
            ]
            save_second_image_sidecar(data_dir, city_slug, sidecar)

        dest = root / rel
        success = False
        last_msg = "no URL"
        for url in url_candidates:
            cands = _candidate_urls(url, thumb_w, thumbs_only=True)
            if not cands and url.startswith("https://"):
                cands = [url]
            attempted += 1
            success, last_msg = _download_second_place_image(
                cands,
                dest,
                timeout_sec=timeout_sec,
                reject_hashes=reject_hashes,
            )
            if success:
                ok += 1
                h = image_content_hash(dest, min_bytes=MIN_IMAGE_BYTES)
                if h:
                    reject_hashes = frozenset(set(reject_hashes) | {h})
                print("  OK {} -> {}".format(slug, rel), flush=True)
                break

        if not success:
            print(
                "  FAIL {}: {}".format(slug, last_msg),
                file=sys.stderr,
                flush=True,
            )
        if delay_sec > 0:
            time.sleep(delay_sec)

    print(
        "{}: second-image pass — {} ok / {} tried; {} already at 2".format(
            city_slug, ok, attempted, already_two,
        ),
        flush=True,
    )
    return attempted, ok, already_two


def cities_needing_second(
    *,
    skip_frozen: bool = True,
    only_slugs: Sequence[str] | None = None,
) -> list[tuple[str, int]]:
    allowed = (
        {s.strip().lower() for s in only_slugs}
        if only_slugs is not None
        else None
    )
    out: list[tuple[str, int]] = []
    if allowed is None or "moscow" in allowed:
        if not skip_frozen or "moscow" not in DOWNLOAD_FROZEN_CITY_SLUGS:
            bundle = _load_city_second_image_bundle("moscow")
            if bundle is not None:
                places, root, *_rest = bundle
                need = sum(
                    1
                    for p in places
                    if _place_image_count(root, p) == 1
                )
                if need:
                    out.append(("moscow", need))
    for slug, mod, attr in _REGISTRY:
        if allowed is not None and slug not in allowed:
            continue
        if skip_frozen and slug in DOWNLOAD_FROZEN_CITY_SLUGS:
            continue
        places = list(getattr(importlib.import_module(mod), attr))
        root = _PROJECT_ROOT / slug
        need = sum(
            1
            for p in places
            if _place_image_count(root, p) == 1
        )
        if need:
            out.append((slug, need))
    out.sort(key=lambda t: (-t[1], t[0]))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--city", required=True, metavar="SLUG")
    parser.add_argument("--delay", type=float, default=6.0, metavar="SEC")
    parser.add_argument("--thumb-width", type=int, default=330, metavar="PX")
    parser.add_argument(
        "--yandex-maps",
        action="store_true",
        help="Also search Yandex Maps (Playwright; slow).",
    )
    parser.add_argument(
        "--max-per-source",
        type=int,
        default=4,
        metavar="N",
        help="Max URLs per extended source (Yandex, Flickr, …).",
    )
    parser.add_argument(
        "--no-subject-filter",
        action="store_true",
        help="Disable person/animal main-subject rejection.",
    )
    parser.add_argument(
        "--allow-frozen",
        action="store_true",
        help="Allow frozen cities (moscow, spb).",
    )
    args = parser.parse_args()
    if args.no_subject_filter:
        import os

        os.environ["SUBJECT_FILTER"] = "0"
    _, ok, _ = download_city_second_images(
        args.city.strip().lower(),
        delay_sec=args.delay,
        thumb_width=args.thumb_width,
        include_yandex_maps=args.yandex_maps,
        max_per_source=max(1, args.max_per_source),
        allow_frozen=args.allow_frozen,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
