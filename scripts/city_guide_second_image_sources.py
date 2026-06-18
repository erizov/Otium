# -*- coding: utf-8 -*-
"""Extra image URL sources for second-place downloads (Yandex, stock APIs)."""

from __future__ import annotations

import os
import sys
from collections.abc import Callable
from pathlib import Path
from urllib.parse import urlparse

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.rag.city_map import names_for_slug

# CDNs used by download_with_dedup — allowed without SOURCES_WHITELIST match.
_EXTRA_HOST_MARKERS: tuple[str, ...] = (
    "avatars.mds.yandex.net",
    "yandex.net",
    "staticflickr.com",
    "flickr.com",
    "images.pexels.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "openverse.org",
    "wp.com",
    "pastvu.com",
    "upload.wikimedia.org",
)


def url_allowed_for_second_image(
    url: str,
    *,
    whitelist_path: Path,
    url_is_whitelisted: Callable[..., bool],
) -> bool:
    """Whitelist entry or known image CDN from the main downloader."""
    raw = url.strip()
    if not raw.startswith("https://"):
        return False
    if url_is_whitelisted(raw, whitelist_path=whitelist_path):
        return True
    host = urlparse(raw).netloc.lower()
    return any(marker in host for marker in _EXTRA_HOST_MARKERS)


def _queries_for_place(query: str, place: dict, city_slug: str) -> list[str]:
    """Search phrases: full query, then place name alone."""
    names = names_for_slug(city_slug)
    city_en = names.name_en or city_slug.replace("_", " ")
    city_ru = names.name_ru or city_en
    out: list[str] = []
    seen: set[str] = set()

    def _add(q: str) -> None:
        s = q.strip()
        if s and s not in seen:
            seen.add(s)
            out.append(s)

    _add(query)
    for key in ("name_en", "name_ru", "name"):
        val = str(place.get(key) or "").strip()
        if val:
            _add("{} {}".format(val, city_en))
            if city_ru != city_en:
                _add("{} {}".format(val, city_ru))
            _add(val)
    return out


def discover_extended_second_image_urls(
    place: dict,
    city_slug: str,
    query: str,
    *,
    whitelist_path: Path,
    url_is_whitelisted: Callable[..., bool],
    exclude_url: str = "",
    max_per_source: int = 4,
    include_yandex_maps: bool = False,
    skip_pixabay: bool | None = None,
    skip_pexels: bool | None = None,
) -> list[str]:
    """
    URLs from Yandex, Openverse, Flickr, etc. (same family as download_with_dedup).

    Commons and city-whitelist Openverse are handled elsewhere; this adds the
  rest. URLs are deduped; exclude_url is skipped (usually the primary photo).
    """
    from scripts.download_with_dedup import SourceFetchError
    from scripts.download_with_dedup import _fetch_commons_urls_for_place
    from scripts.download_with_dedup import _fetch_flickr_urls_for_place
    from scripts.download_with_dedup import _fetch_openverse_urls_for_place
    from scripts.download_with_dedup import _fetch_pastvu_urls_for_place
    from scripts.download_with_dedup import _fetch_pexels_urls_for_place
    from scripts.download_with_dedup import _fetch_pixabay_urls_for_place
    from scripts.download_with_dedup import _fetch_unsplash_urls_for_place
    from scripts.download_with_dedup import _fetch_yandex_images_urls
    from scripts.download_with_dedup import _fetch_yandex_urls_for_place

    if skip_pixabay is None:
        from scripts.pixabay_config import pixabay_image_search_enabled

        skip_pixabay = not pixabay_image_search_enabled()
    if skip_pexels is None:
        from scripts.pixabay_config import pexels_image_search_enabled

        skip_pexels = not pexels_image_search_enabled()

    names = names_for_slug(city_slug)
    city_en = names.name_en or city_slug.replace("_", " ")
    city_ru = names.name_ru or city_en
    queries = _queries_for_place(query, place, city_slug)

    sources: list[tuple[str, Callable[..., list[str]]]] = [
        (
            "YandexImages",
            lambda q: _fetch_yandex_images_urls(
                q, city=city_ru, max_images=max_per_source,
            ),
        ),
        (
            "Openverse",
            lambda q: _fetch_openverse_urls_for_place(
                q, city=city_en, max_images=max_per_source,
            ),
        ),
        (
            "Flickr",
            lambda q: _fetch_flickr_urls_for_place(
                q, city=city_en, max_images=max_per_source,
            ),
        ),
        (
            "CommonsApi",
            lambda q: _fetch_commons_urls_for_place(
                q, city=city_en, max_images=max_per_source,
            ),
        ),
    ]
    if not skip_pixabay:
        sources.append(
            (
                "Pixabay",
                lambda q: _fetch_pixabay_urls_for_place(
                    q, city=city_en, max_images=max_per_source,
                ),
            ),
        )
    if not skip_pexels:
        sources.append(
            (
                "Pexels",
                lambda q: _fetch_pexels_urls_for_place(
                    q, city=city_en, max_images=max_per_source,
                ),
            ),
        )
    sources.append(
        (
            "Unsplash",
            lambda q: _fetch_unsplash_urls_for_place(
                q, city=city_en, max_images=max_per_source,
            ),
        ),
    )
    if city_ru:
        sources.append(
            (
                "Pastvu",
                lambda q: _fetch_pastvu_urls_for_place(
                    q, city=city_ru, max_images=max_per_source,
                ),
            ),
        )
        sources.append(
            (
                "OpenverseRu",
                lambda q: _fetch_openverse_urls_for_place(
                    q, city=city_ru, max_images=max_per_source,
                ),
            ),
        )
    if include_yandex_maps:
        sources.insert(
            1,
            (
                "YandexMaps",
                lambda q: _fetch_yandex_urls_for_place(
                    q, city=city_ru, max_images=max_per_source,
                ),
            ),
        )

    seen: set[str] = set()
    out: list[str] = []

    def _add(url: str) -> None:
        u = url.strip()
        if not u or u == exclude_url or u in seen:
            return
        if not url_allowed_for_second_image(
            u,
            whitelist_path=whitelist_path,
            url_is_whitelisted=url_is_whitelisted,
        ):
            return
        seen.add(u)
        out.append(u)

    for src_name, fetch in sources:
        for q in queries:
            try:
                for u in fetch(q):
                    _add(u)
            except SourceFetchError:
                continue
            except Exception:
                continue
    return out
