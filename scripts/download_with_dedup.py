# -*- coding: utf-8 -*-
"""
Download images with per-download duplicate checking.

Downloads images one by one, checking after each download if it's a duplicate
of any existing file in the folder. Ensures each item gets exactly 4 distinct
images before proceeding.
"""

from __future__ import annotations

import json
import logging
import re
import os
import shutil
import socket
import sys
import time
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path
from typing import Callable, Optional, Tuple

from scripts.core import ensure_utf8_console, load_env, project_root

ensure_utf8_console()
load_env()

logger = logging.getLogger(__name__)
if not logger.handlers:
    h = logging.StreamHandler(sys.stderr)
    h.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(h)
    logger.setLevel(logging.WARNING)

# Failure reason codes for detailed warnings
FAIL_NO_URLS = "no URLs"
FAIL_NETWORK = "network error"
FAIL_TIMEOUT = "timeout"
FAIL_FORBIDDEN = "forbidden (hash)"
FAIL_DUPLICATE = "duplicate of {}"  # .format(dup_basename)
FAIL_AI_REJECT = "AI: does not match place"
FAIL_TOO_SMALL = "response too small"
FAIL_BANNED = "banned"
FAIL_MOVED = "moved to forbidden"
FAIL_EXISTING_DUP = "existing duplicate of {}"  # .format(dup_basename)

_PROJECT_ROOT = project_root()
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.image_utils import (
    image_content_hash,
    image_content_hash_from_bytes,
)
from scripts.slug_item_map import basename_to_slug

MIN_IMAGE_BYTES = 500

# Pauses to reduce rate-limiting / ban risk (seconds)
DELAY_AFTER_REJECT_SEC = 1.2
DELAY_AFTER_DOWNLOAD_SEC = 2.5
DELAY_BETWEEN_REQUESTS_SEC = 1.8
# Delay scaled by 1/N when using N sources (round-robin)
MAX_SOURCES_FOR_DELAY_SCALE = 20
# Exclude source from round-robin after this many failures (any items)
SOURCE_FAILURE_THRESHOLD = 3
# When one variant fails, exclude all variants of same site (e.g. Pixabay*)
_SITE_PREFIXES = ("Pixabay", "Pexels", "Unsplash", "Flickr", "Commons",
                  "Openverse", "Yandex", "Pastvu")


class SourceFetchError(Exception):
    """Raised when a URL source fails (network, HTTP, etc.)."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


def _normalize_error(exc: Exception) -> str:
    """Return a stable key for grouping same-type errors (for exclusion)."""
    if isinstance(exc, urllib.error.HTTPError):
        return "HTTPError:{}".format(exc.code)
    if isinstance(exc, (socket.timeout, TimeoutError)):
        return "timeout"
    if isinstance(exc, urllib.error.URLError):
        return "URLError"
    if isinstance(exc, SourceFetchError):
        msg = (exc.message or "").lower()
        if "timeout" in msg or "timed out" in msg:
            return "timeout"
        if "403" in msg or "forbidden" in msg:
            return "HTTPError:403"
        if "429" in msg or "rate" in msg:
            return "HTTPError:429"
        if "500" in msg or "502" in msg or "503" in msg:
            return "HTTPError:5xx"
        return "SourceFetchError"
    if isinstance(exc, OSError):
        return "OSError"
    return type(exc).__name__


# Do not retry URL on failure: skip and try next
URL_NETWORK_RETRIES = 1
URL_RETRY_DELAY_SEC = 5.0

# No basename-based skip: forbidden is by content hash only (forbidden/ folder).
FORBIDDEN_BASENAMES: frozenset[str] = frozenset()

# Hashes of forbidden images (skip any download matching these).
# Loaded from forbidden/ subfolder at runtime and merged with this set.
# Add known-bad hashes here for faster skip without scanning forbidden/.
FORBIDDEN_IMAGE_HASHES: frozenset[str] = frozenset()

FORBIDDEN_SUBDIR_NAME = "forbidden"
DOWNLOAD_TODO_FILENAME = "download_todo.txt"
DOWNLOAD_LIST_FILENAME = "download_list.txt"
FAIL_LOG_FILENAME = "download_failures.log"
EXCLUDED_SOURCES_FILENAME = "excluded_sources.json"
EXCLUDED_SOURCES_TTL_SEC = 3600  # 1 hour

# Placeholder or non-image URLs to skip
_SKIP_URL_PREFIXES = (
    "https://example.com/", "http://example.com/", "https://yandex.ru/clck/",
    "data:", "javascript:", "blob:",
)
_SKIP_URL_CONTAINS = (
    "/pixel?", "/track?", "/analytics?", "/ad.", "/ads.",
    "placeholder", "default-avatar", "logo.svg", "1x1.gif",
)
_YANDEX_AVATARS = "avatars.mds.yandex.net"


def _url_to_ascii(url: str) -> str | None:
    """
    Convert URL with non-ASCII to ASCII-safe form for urllib. Returns None if
    conversion fails.
    """
    try:
        if all(ord(c) < 128 for c in url):
            return url
        parsed = urllib.parse.urlparse(url)
        path = urllib.parse.quote(parsed.path, safe="/")
        query = (
            urllib.parse.quote(parsed.query, safe="=&")
            if parsed.query else parsed.query
        )
        netloc = parsed.netloc.encode("idna").decode("ascii")
        return urllib.parse.urlunparse((
            parsed.scheme, netloc, path, parsed.params, query, parsed.fragment,
        ))
    except Exception:
        return None


_ALL_SOURCE_NAMES = frozenset({
    "Commons", "Pixabay", "Pexels", "Unsplash", "Flickr", "FlickrInteresting",
    "FlickrRecent", "CommonsNameOnly", "PexelsNameOnly", "UnsplashNameOnly",
    "PixabayNameOnly", "FlickrNameOnly", "Openverse", "OpenverseNameOnly",
    "CommonsRussia", "PixabayRussia", "PexelsRussia", "UnsplashRussia",
    "YandexMaps", "YandexImages",
    "CommonsCityRu", "OpenverseCityRu", "Pastvu", "PastvuMoscow",
    "FlickrRussia", "FlickrCityRu", "PixabayCityRu", "PexelsCityRu",
    "UnsplashCityRu",
})


def _sources_for_site(src_name: str) -> set[str]:
    """Return all source names that belong to the same site as src_name."""
    for prefix in _SITE_PREFIXES:
        if src_name == prefix or src_name.startswith(prefix):
            return {n for n in _ALL_SOURCE_NAMES
                    if n == prefix or n.startswith(prefix)}
    return {src_name}


def _load_excluded_sources(project_root: Path) -> set[str]:
    """
    Load excluded sources from file. Returns non-empty set only if file exists
    and exclusion timestamp is within EXCLUDED_SOURCES_TTL_SEC (1 hour).
    """
    path = project_root / EXCLUDED_SOURCES_FILENAME
    if not path.exists() or not path.is_file():
        return set()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return set()
    excluded = set(data.get("sources") or [])
    ts = data.get("excluded_at")
    if not excluded or ts is None:
        return set()
    try:
        excluded_at = float(ts)
    except (TypeError, ValueError):
        return set()
    if time.time() - excluded_at > EXCLUDED_SOURCES_TTL_SEC:
        return set()
    return excluded


def _save_excluded_sources(
    project_root: Path,
    excluded_sources: set[str],
) -> None:
    """Persist excluded sources with current timestamp."""
    if not excluded_sources:
        return
    path = project_root / EXCLUDED_SOURCES_FILENAME
    try:
        data = {
            "sources": sorted(excluded_sources),
            "excluded_at": time.time(),
        }
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except OSError:
        pass


def _slot_number(basename: str) -> int:
    """Extract slot from name_1.jpg -> 1, name_2.jpg -> 2. Return 999 if unknown."""
    m = re.search(r"_(\d+)\.(jpg|jpeg|png|webp)$", basename.lower())
    return int(m.group(1)) if m else 999


def _load_failed_urls(images_dir: Path) -> set[str]:
    """
    Load URLs that failed before (forbidden, duplicate, AI reject) from
    download_failures.log. Skip these when building urls_to_try.
    """
    path = images_dir / FAIL_LOG_FILENAME
    if not path.exists() or not path.is_file():
        return set()
    urls: set[str] = set()
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t", 3)
            if len(parts) >= 4:
                url = parts[3].strip()
                if url and url.startswith("http"):
                    urls.add(url)
    except Exception:
        pass
    return urls


def _normalize_image_url(url: str) -> str | None:
    """
    Return a downloadable image URL, or None if not usable.
    Fixes Yandex template URLs (e.g. .../%s or .../%).
    """
    if not url or not url.strip():
        return None
    url = url.strip()
    if any(url.startswith(p) for p in _SKIP_URL_PREFIXES):
        return None
    if any(s in url.lower() for s in _SKIP_URL_CONTAINS):
        return None
    if url.startswith("//"):
        url = "https:" + url
    if _YANDEX_AVATARS in url:
        # Yandex template: replace %s or trailing /% with /orig
        if "%s" in url:
            url = url.replace("%s", "orig")
        if url.rstrip("/").endswith("/%"):
            url = url.rstrip("/").rstrip("%") + "orig"
        if "/%" in url:
            url = url.replace("/%", "/orig")
    if not url.startswith("http"):
        return None
    # Skip non-image resources
    if ".js" in url or "/jclck/" in url:
        return None
    return url


def _yandex_url_variants(url: str) -> list[str]:
    """
    For a Yandex avatars URL, return a list of URLs to try (different sizes).
    """
    if _YANDEX_AVATARS not in url:
        return [url]
    normalized = _normalize_image_url(url)
    if not normalized:
        return []
    # Same URL may support size suffix; try alternates as fallbacks
    variants = [normalized]
    if "/get-altay/" in normalized or "/get-vh/" in normalized:
        base = normalized
        for size in ("XXXL", "L_height", "M_height", "orig"):
            if size in base:
                continue
            if base.endswith("orig"):
                alt = base[:-4] + size
            else:
                alt = base.rstrip("/") + "/" + size
            if alt != base and alt not in variants:
                variants.append(alt)
    return variants[:5]  # Cap so we don't try too many


def _fetch_commons_urls_for_place(
    item_name: str,
    city: str = "Moscow",
    max_images: int = 10,
) -> list[str]:
    """
    Fetch image URLs from Wikimedia Commons by place name (HTTP API, no browser).

    Returns normalized, deduplicated list of direct image URLs.
    """
    query = "{} {}".format(item_name, city).strip()
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": query,
        "gsrlimit": str(max_images * 4),
        "prop": "imageinfo",
        "iiprop": "url|size",
        "format": "json",
    }
    url = (
        "https://commons.wikimedia.org/w/api.php?"
        + urllib.parse.urlencode(params, encoding="utf-8")
    )
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "ExcursionGuide/Commons/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
    except (urllib.error.URLError, urllib.error.HTTPError, socket.timeout,
            TimeoutError, OSError) as e:
        logger.warning("Commons API failed for %r: %s", query[:50], e)
        raise SourceFetchError(str(e))
    except Exception as e:
        logger.warning("Commons API error for %r: %s", query[:50], e)
        raise SourceFetchError(str(e))
    try:
        payload = json.loads(data.decode("utf-8", errors="ignore"))
    except Exception:
        return []
    pages = (payload.get("query") or {}).get("pages") or {}
    urls: list[str] = []
    seen: set[str] = set()
    for page in pages.values():
        infos = page.get("imageinfo") or []
        for info in infos:
            src = info.get("url") or ""
            if not src:
                continue
            if not any(
                src.lower().endswith(ext)
                for ext in (".jpg", ".jpeg", ".png", ".webp")
            ):
                continue
            width = int(info.get("width", 0))
            height = int(info.get("height", 0))
            if width < 400 or height < 300:
                continue
            norm = _normalize_image_url(src)
            if norm and norm not in seen:
                urls.append(norm)
                seen.add(norm)
            if len(urls) >= max_images:
                break
        if len(urls) >= max_images:
            break
    return urls[:20]


def _fetch_pixabay_urls_for_place(
    item_name: str,
    city: str = "Moscow",
    max_images: int = 10,
) -> list[str]:
    """
    Fetch image URLs from Pixabay by place name (requires PIXABAY_API_KEY).
    """
    key = os.environ.get("PIXABAY_API_KEY", "").strip()
    if not key:
        return []
    query = "{} {}".format(item_name, city).strip()
    params = {
        "key": key,
        "q": query[:100],
        "image_type": "photo",
        "lang": "ru",
        "per_page": str(min(max_images * 2, 20)),
        "safesearch": "true",
    }
    url = (
        "https://pixabay.com/api/?"
        + urllib.parse.urlencode(params, encoding="utf-8")
    )
    req = urllib.request.Request(
        url, headers={"User-Agent": "ExcursionGuide/Pixabay/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
    except urllib.error.HTTPError as e:
        logger.warning("Pixabay API HTTP %s: %s", e.code, e.reason)
        raise SourceFetchError(str(e))
    except (urllib.error.URLError, socket.timeout, TimeoutError,
            OSError) as e:
        logger.warning("Pixabay API failed (will try other sources): %s", e)
        raise SourceFetchError(str(e))
    except Exception as e:
        logger.warning("Pixabay API error (will try other sources): %s", e)
        raise SourceFetchError(str(e))
    try:
        payload = json.loads(data.decode("utf-8", errors="ignore"))
    except Exception:
        return []
    hits = payload.get("hits") or []
    urls: list[str] = []
    seen: set[str] = set()
    for hit in hits:
        src = hit.get("largeImageURL") or hit.get("webformatURL") or ""
        if not src:
            continue
        norm = _normalize_image_url(src)
        if norm and norm not in seen:
            urls.append(norm)
            seen.add(norm)
        if len(urls) >= max_images:
            break
    return urls[:20]


def _fetch_pexels_urls_for_place(
    item_name: str,
    city: str = "Moscow",
    max_images: int = 10,
) -> list[str]:
    """
    Fetch image URLs from Pexels by place name (requires PEXELS_API_KEY).
    """
    key = os.environ.get("PEXELS_API_KEY", "").strip()
    if not key:
        return []
    query = "{} {}".format(item_name, city).strip()
    params = {
        "query": query[:100],
        "per_page": str(min(max_images * 2, 20)),
        "locale": "ru-RU",
    }
    url = (
        "https://api.pexels.com/v1/search?"
        + urllib.parse.urlencode(params, encoding="utf-8")
    )
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": key,
            "User-Agent": "ExcursionGuide/Pexels/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
    except urllib.error.HTTPError as e:
        logger.warning("Pexels API HTTP %s: %s", e.code, e.reason)
        raise SourceFetchError(str(e))
    except (urllib.error.URLError, socket.timeout, TimeoutError,
            OSError) as e:
        logger.warning("Pexels API failed (will try other sources): %s", e)
        raise SourceFetchError(str(e))
    except Exception as e:
        logger.warning("Pexels API error (will try other sources): %s", e)
        raise SourceFetchError(str(e))
    try:
        payload = json.loads(data.decode("utf-8", errors="ignore"))
    except Exception:
        return []
    photos = payload.get("photos") or []
    urls: list[str] = []
    seen: set[str] = set()
    for photo in photos:
        src_obj = photo.get("src") or {}
        src = src_obj.get("original") or src_obj.get("large2x") or src_obj.get(
            "large", ""
        )
        if not src:
            continue
        norm = _normalize_image_url(src)
        if norm and norm not in seen:
            urls.append(norm)
            seen.add(norm)
        if len(urls) >= max_images:
            break
    return urls[:20]


def _fetch_unsplash_urls_for_place(
    item_name: str,
    city: str = "Moscow",
    max_images: int = 10,
) -> list[str]:
    """
    Fetch image URLs from Unsplash by place name (UNSPLASH_ACCESS_KEY).
    """
    key = os.environ.get("UNSPLASH_ACCESS_KEY", "").strip()
    if not key:
        return []
    query = "{} {}".format(item_name, city).strip()
    params = {
        "query": query[:100],
        "per_page": str(min(max_images * 2, 20)),
    }
    url = (
        "https://api.unsplash.com/search/photos?"
        + urllib.parse.urlencode(params, encoding="utf-8")
    )
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": "Client-ID {}".format(key),
            "Accept-Version": "v1",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
    except urllib.error.HTTPError as e:
        logger.warning("Unsplash API HTTP %s: %s", e.code, e.reason)
        raise SourceFetchError(str(e))
    except (urllib.error.URLError, socket.timeout, TimeoutError,
            OSError) as e:
        logger.warning("Unsplash API failed (will try other sources): %s", e)
        raise SourceFetchError(str(e))
    except Exception as e:
        logger.warning("Unsplash API error (will try other sources): %s", e)
        raise SourceFetchError(str(e))
    try:
        payload = json.loads(data.decode("utf-8", errors="ignore"))
    except Exception:
        return []
    results = payload.get("results") or []
    urls: list[str] = []
    seen: set[str] = set()
    for photo in results:
        urls_obj = photo.get("urls") or {}
        src = urls_obj.get("regular") or urls_obj.get("full") or urls_obj.get(
            "raw", ""
        )
        if not src:
            continue
        norm = _normalize_image_url(src)
        if norm and norm not in seen:
            urls.append(norm)
            seen.add(norm)
        if len(urls) >= max_images:
            break
    return urls[:20]


def _fetch_flickr_urls_for_place(
    item_name: str,
    city: str = "Moscow",
    max_images: int = 10,
    sort: str = "relevance",
) -> list[str]:
    """
    Fetch image URLs from Flickr by place name (FLICKR_API_KEY).
    """
    key = os.environ.get("FLICKR_API_KEY", "").strip()
    if not key:
        return []
    query = "{} {}".format(item_name, city).strip()
    params = {
        "method": "flickr.photos.search",
        "api_key": key,
        "text": query[:100],
        "format": "json",
        "nojsoncallback": "1",
        "per_page": str(min(max_images * 2, 20)),
        "content_type": "1",  # photos only
        "safe_search": "1",
        "sort": sort,
    }
    url = (
        "https://api.flickr.com/services/rest?"
        + urllib.parse.urlencode(params, encoding="utf-8")
    )
    req = urllib.request.Request(
        url, headers={"User-Agent": "ExcursionGuide/Flickr/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
    except urllib.error.HTTPError as e:
        logger.warning("Flickr API HTTP %s: %s", e.code, e.reason)
        raise SourceFetchError(str(e))
    except (urllib.error.URLError, socket.timeout, TimeoutError,
            OSError) as e:
        logger.warning("Flickr API failed (will try other sources): %s", e)
        raise SourceFetchError(str(e))
    except Exception as e:
        logger.warning("Flickr API error (will try other sources): %s", e)
        raise SourceFetchError(str(e))
    try:
        payload = json.loads(data.decode("utf-8", errors="ignore"))
    except Exception:
        return []
    photos = (payload.get("photos") or {}).get("photo") or []
    urls: list[str] = []
    seen: set[str] = set()
    for p in photos:
        sid = p.get("server") or ""
        pid = p.get("id") or ""
        secret = p.get("secret") or ""
        if not (sid and pid and secret):
            continue
        # Use size 'b' (1024) or 'w' (400) for good resolution
        src = "https://live.staticflickr.com/{}/{}_{}_b.jpg".format(
            sid, pid, secret,
        )
        norm = _normalize_image_url(src)
        if norm and norm not in seen:
            urls.append(norm)
            seen.add(norm)
        if len(urls) >= max_images:
            break
    return urls[:20]


def _fetch_openverse_urls_for_place(
    item_name: str,
    city: str = "Moscow",
    max_images: int = 10,
) -> list[str]:
    """
    Fetch image URLs from Openverse (openly-licensed media, no key required).
    """
    query = "{} {}".format(item_name, city).strip() if city else item_name.strip()
    if not query:
        return []
    params = {
        "q": query[:100],
        "page_size": str(min(max_images * 2, 20)),
        "page": "1",
    }
    url = (
        "https://api.openverse.org/v1/images/?"
        + urllib.parse.urlencode(params, encoding="utf-8")
    )
    req = urllib.request.Request(
        url, headers={"User-Agent": "ExcursionGuide/Openverse/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
    except urllib.error.HTTPError as e:
        logger.warning("Openverse API HTTP %s: %s", e.code, e.reason)
        raise SourceFetchError(str(e))
    except (urllib.error.URLError, socket.timeout, TimeoutError,
            OSError) as e:
        logger.warning("Openverse API failed (will try other sources): %s", e)
        raise SourceFetchError(str(e))
    except Exception as e:
        logger.warning("Openverse API error (will try other sources): %s", e)
        raise SourceFetchError(str(e))
    try:
        payload = json.loads(data.decode("utf-8", errors="ignore"))
    except Exception:
        return []
    results = payload.get("results") or []
    urls_list: list[str] = []
    seen: set[str] = set()
    for r in results:
        src = r.get("url") or ""
        if not src:
            continue
        norm = _normalize_image_url(src)
        if norm and norm not in seen:
            urls_list.append(norm)
            seen.add(norm)
        if len(urls_list) >= max_images:
            break
    return urls_list[:20]


# Moscow center for Pastvu (historical photos)
_PASTVU_MOSCOW_LAT = 55.7558
_PASTVU_MOSCOW_LON = 37.6173


def _fetch_pastvu_urls_for_place(
    item_name: str,
    city: str = "Moscow",
    max_images: int = 10,
) -> list[str]:
    """
    Fetch image URLs from Pastvu (historical photos) for Moscow/Москва.
    Uses photo.giveNearestPhotos near city center; free, Russian-friendly.
    """
    city_lower = (city or "").lower()
    if "москва" not in (city or "") and "moscow" not in city_lower:
        return []
    params = json.dumps({
        "geo": [_PASTVU_MOSCOW_LAT, _PASTVU_MOSCOW_LON],
        "limit": min(max_images, 30),
        "distance": 15000,
    })
    url = (
        "https://api.pastvu.com/api2?"
        + urllib.parse.urlencode({"method": "photo.giveNearestPhotos",
                                  "params": params})
    )
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "ExcursionGuide/Pastvu/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
    except (urllib.error.URLError, urllib.error.HTTPError, socket.timeout,
            TimeoutError, OSError) as e:
        logger.warning("Pastvu API failed: %s", e)
        raise SourceFetchError(str(e))
    try:
        payload = json.loads(data.decode("utf-8", errors="ignore"))
    except Exception:
        return []
    result = payload.get("result") or {}
    photos = result.get("photos") or []
    urls_list: list[str] = []
    seen: set[str] = set()
    for p in photos:
        f = p.get("file")
        if not f or not isinstance(f, str):
            continue
        # Standard size: https://img.pastvu.com/d/{file}
        src = "https://img.pastvu.com/d/{}".format(f.strip())
        if src not in seen:
            urls_list.append(src)
            seen.add(src)
        if len(urls_list) >= max_images:
            break
    return urls_list[:20]


def _source_api_family(name: str) -> str:
    """Return API family: Pixabay* -> Pixabay, Flickr* -> Flickr, etc."""
    for prefix in ("Pixabay", "Flickr", "Commons", "Pexels", "Unsplash",
                   "Openverse", "Yandex", "Pastvu"):
        if name.startswith(prefix):
            return prefix
    return name


def _fetch_urls_round_robin(
    names_to_try: list[str],
    city: str = "Moscow",
    city_ru: str = "Москва",
    max_per_source: int = 5,
    failed_urls: set[str] | None = None,
    excluded_sources: set[str] | None = None,
    failure_counts: dict[str, int] | None = None,
    project_root: Path | None = None,
) -> tuple[list[str], int]:
    """
    Fetch URLs from all sources in round-robin order, interleaving results. If
    one source fails, try the next. Returns (urls, num_sources_used).
    Pass excluded_sources and failure_counts to persist exclusion across calls.
    """
    failed_urls = failed_urls or set()
    if excluded_sources is None:
        excluded_sources = set()
    if failure_counts is None:
        failure_counts = {}
    skip_pixabay = os.environ.get("PIXABAY_SKIP", "").strip().lower() in (
        "1", "true", "yes",
    )
    # Each (source, query) pair is a round-robin bucket; more buckets = less
    # delay per site (each site called every Nth request).
    _all_sources: list[tuple[str, Callable[[str], list[str]]]] = [
        ("Commons", lambda q: _fetch_commons_urls_for_place(
            q, city=city, max_images=max_per_source,
        )),
        ("Pixabay", lambda q: _fetch_pixabay_urls_for_place(
            q, city=city, max_images=max_per_source,
        )),
        ("Pexels", lambda q: _fetch_pexels_urls_for_place(
            q, city=city, max_images=max_per_source,
        )),
        ("Unsplash", lambda q: _fetch_unsplash_urls_for_place(
            q, city=city, max_images=max_per_source,
        )),
        ("Flickr", lambda q: _fetch_flickr_urls_for_place(
            q, city=city, max_images=max_per_source,
        )),
        ("FlickrInteresting", lambda q: _fetch_flickr_urls_for_place(
            q, city=city, max_images=max_per_source,
            sort="interestingness-desc",
        )),
        ("FlickrRecent", lambda q: _fetch_flickr_urls_for_place(
            q, city=city, max_images=max_per_source,
            sort="date-posted-desc",
        )),
        ("CommonsNameOnly", lambda q: _fetch_commons_urls_for_place(
            q, city="", max_images=max_per_source,
        )),
        ("PexelsNameOnly", lambda q: _fetch_pexels_urls_for_place(
            q, city="", max_images=max_per_source,
        )),
        ("UnsplashNameOnly", lambda q: _fetch_unsplash_urls_for_place(
            q, city="", max_images=max_per_source,
        )),
        ("PixabayNameOnly", lambda q: _fetch_pixabay_urls_for_place(
            q, city="", max_images=max_per_source,
        )),
        ("FlickrNameOnly", lambda q: _fetch_flickr_urls_for_place(
            q, city="", max_images=max_per_source,
        )),
        ("Openverse", lambda q: _fetch_openverse_urls_for_place(
            q, city=city, max_images=max_per_source,
        )),
        ("OpenverseNameOnly", lambda q: _fetch_openverse_urls_for_place(
            q, city="", max_images=max_per_source,
        )),
        ("CommonsRussia", lambda q: _fetch_commons_urls_for_place(
            q, city="Russia", max_images=max_per_source,
        )),
        ("PixabayRussia", lambda q: _fetch_pixabay_urls_for_place(
            q, city="Russia", max_images=max_per_source,
        )),
        ("PexelsRussia", lambda q: _fetch_pexels_urls_for_place(
            q, city="Russia", max_images=max_per_source,
        )),
        ("UnsplashRussia", lambda q: _fetch_unsplash_urls_for_place(
            q, city="Russia", max_images=max_per_source,
        )),
        ("FlickrRussia", lambda q: _fetch_flickr_urls_for_place(
            q, city="Russia", max_images=max_per_source,
        )),
        ("FlickrCityRu", lambda q: _fetch_flickr_urls_for_place(
            q, city=city_ru, max_images=max_per_source,
        )),
        ("PixabayCityRu", lambda q: _fetch_pixabay_urls_for_place(
            q, city=city_ru, max_images=max_per_source,
        )),
        ("PexelsCityRu", lambda q: _fetch_pexels_urls_for_place(
            q, city=city_ru, max_images=max_per_source,
        )),
        ("UnsplashCityRu", lambda q: _fetch_unsplash_urls_for_place(
            q, city=city_ru, max_images=max_per_source,
        )),
        ("YandexMaps", lambda q: _fetch_yandex_urls_for_place(
            q, city=city_ru, max_images=max_per_source,
        )),
        ("YandexImages", lambda q: _fetch_yandex_images_urls(
            q, city=city_ru, max_images=max_per_source,
        )),
        # Russian and free-image sources (Moscow/Москва)
        ("CommonsCityRu", lambda q: _fetch_commons_urls_for_place(
            q, city=city_ru, max_images=max_per_source,
        )),
        ("OpenverseCityRu", lambda q: _fetch_openverse_urls_for_place(
            q, city=city_ru, max_images=max_per_source,
        )),
        ("Pastvu", lambda q: _fetch_pastvu_urls_for_place(
            q, city=city_ru, max_images=max_per_source,
        )),
        ("PastvuMoscow", lambda q: _fetch_pastvu_urls_for_place(
            q, city="Moscow", max_images=max_per_source,
        )),
    ]
    sources = [
        (n, f) for n, f in _all_sources
        if not (skip_pixabay and n.startswith("Pixabay"))
    ]
    # Use configured source count for delay scaling (each site called every Nth)
    # Expand: each (source, query) = one bucket for round-robin. More buckets
    # = each site called every Nth request = can reduce delay N times.
    # If a source fails 3+ times (any items), exclude from round-robin till
    # next run (exclusion is per-run, persisted via passed-in dicts).
    by_source: list[list[str]] = []
    for src_name, fetch in sources:
        if src_name in excluded_sources:
            continue
        family = _source_api_family(src_name)
        for qname in names_to_try:
            urls: list[str] = []
            try:
                for u in fetch(qname):
                    if u and u not in failed_urls:
                        urls.append(u)
            except Exception as e:
                failure_counts[family] = failure_counts.get(family, 0) + 1
                if failure_counts[family] >= SOURCE_FAILURE_THRESHOLD:
                    to_exclude = _sources_for_site(src_name)
                    excluded_sources.update(to_exclude)
                    if project_root:
                        _save_excluded_sources(project_root, excluded_sources)
                    logger.warning(
                        "%s temporarily excluded (%d failures, 1h)",
                        family, failure_counts[family],
                    )
                    break
            by_source.append(urls)

    # Interleave: [s0[0], s1[0], ..., sN[0], s0[1], s1[1], ...]
    interleaved: list[str] = []
    seen: set[str] = set()
    max_len = max(len(u) for u in by_source) if by_source else 0
    for i in range(max_len):
        for src_urls in by_source:
            if i < len(src_urls):
                u = src_urls[i]
                if u not in seen:
                    interleaved.append(u)
                    seen.add(u)
    # Scale delay by N: configured sources = each site called every Nth try
    num_configured = len(sources)
    # Allow more URLs when many sources (improve chance of at least one download)
    max_urls = 80 if num_configured > 20 else 60
    return interleaved[:max_urls], max(1, min(num_configured, MAX_SOURCES_FOR_DELAY_SCALE))


def _fetch_yandex_images_urls(
    item_name: str,
    city: str = "Москва",
    max_images: int = 10,
) -> list[str]:
    """
    Fetch image URLs from Yandex Images (yandex.ru/images) by place name.

    Alternative to Yandex Maps; used when Maps returns no URLs.
    """
    try:
        from scripts.yandex_maps_images import search_yandex_images
    except ImportError:
        return []
    try:
        raw = search_yandex_images(
            item_name, city=city, max_images=max_images,
        )
    except Exception as e:
        logger.warning("Yandex Images failed for %r: %s", item_name[:40], e)
        raise SourceFetchError(str(e))
    urls: list[str] = []
    seen: set[str] = set()
    for u in raw:
        if not u:
            continue
        norm = _normalize_image_url(u)
        if norm and norm not in seen:
            urls.append(norm)
            seen.add(norm)
        if _YANDEX_AVATARS in (u or ""):
            for variant in _yandex_url_variants(u):
                v = _normalize_image_url(variant) or variant
                if v and v not in seen:
                    urls.append(v)
                    seen.add(v)
    return urls[:20]


def _fetch_yandex_urls_for_place(
    item_name: str,
    city: str = "Москва",
    max_images: int = 10,
) -> list[str]:
    """
    Fetch image URLs from Yandex Maps by place name (Playwright).
    Use when data has no URL or only placeholders, or when all URLs failed.
    Returns normalized, deduplicated list of URLs.
    """
    try:
        from scripts.yandex_maps_images import get_place_images
    except ImportError:
        return []

    try:
        raw = get_place_images(
            item_name, city=city, max_images=max_images, retry=2,
        )
    except Exception as exc:
        logger.warning("Yandex Maps failed for %r: %s", item_name[:40], exc)
        raise SourceFetchError(str(exc))
    urls: list[str] = []
    seen: set[str] = set()
    for u in raw:
        if not u:
            continue
        norm = _normalize_image_url(u)
        if norm and norm not in seen:
            urls.append(norm)
            seen.add(norm)
        if _YANDEX_AVATARS in (u or ""):
            for variant in _yandex_url_variants(u):
                v = _normalize_image_url(variant) or variant
                if v and v not in seen:
                    urls.append(v)
                    seen.add(v)
    return urls[:20]


def _load_forbidden_hashes(images_dir: Path) -> set[str]:
    """
    Load content hashes of all images in images_dir/forbidden/.
    Used to skip downloads that match known-bad images (fast check).
    """
    forbidden_dir = images_dir / FORBIDDEN_SUBDIR_NAME
    out: set[str] = set()
    if not forbidden_dir.exists() or not forbidden_dir.is_dir():
        return out
    for path in forbidden_dir.iterdir():
        if not path.is_file():
            continue
        if path.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
            continue
        if path.stat().st_size < MIN_IMAGE_BYTES:
            continue
        h = image_content_hash(path, min_bytes=MIN_IMAGE_BYTES)
        if h:
            out.add(h)
    return out


def _write_download_todo(
    images_dir: Path,
    guide_name: str,
    failed_slots: list[tuple[str, str, str]],
) -> None:
    """Write download_todo.txt (guide, basename, item_name, reason) for later runs."""
    path = images_dir / DOWNLOAD_TODO_FILENAME
    lines = []
    for bn, iname, reason in failed_slots:
        line = "\t".join((guide_name, bn, iname.replace("\t", " "), reason))
        lines.append(line)
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def _append_fail_log(images_dir: Path, lines: list[str]) -> None:
    """Append failed URL lines to download_failures.log (for skip on next run)."""
    if not lines:
        return
    path = images_dir / FAIL_LOG_FILENAME
    with path.open("a", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")


def download_list_from_directory(
    images_dir: Path,
    items: list[dict],
    guide_name: str = "",
    forbidden_basenames: Optional[frozenset[str]] = None,
) -> set[str]:
    """
    Scan directory, build download_list.txt (RU + EN names), return missing set.

    Consults actual files in directory (user can add/delete manually). Writes
    place_ru, place_en, basename, slot, status (exists|missing).
    Returns set of basenames that are missing (to download).
    """
    if forbidden_basenames is None:
        forbidden_basenames = FORBIDDEN_BASENAMES
    forbidden_hashes = _load_forbidden_hashes(images_dir) | set(
        FORBIDDEN_IMAGE_HASHES,
    )
    existing_hashes = _get_existing_hashes(images_dir)

    from scripts.validate_images_per_item import _basename

    basename_to_item: dict[str, str] = {}
    for item in items:
        name = item.get("name", "?")
        for img in item.get("images") or []:
            bn = _basename(img)
            basename_to_item[bn] = name

    def _basename_to_slug(bn: str) -> str:
        stem = Path(bn).stem
        import re
        return re.sub(r"_\d+$", "", stem) or stem

    lines: list[str] = []
    lines.append(
        "# place_ru\tplace_en\tbasename\tslot\tstatus",
    )
    missing_basenames: set[str] = set()

    for item in items:
        item_name = item.get("name", "?")
        images = item.get("images") or []
        basenames = [_basename(img) for img in images]
        standard = sorted([
            bn for bn in basenames
            if bn.endswith("_1.jpg") or bn.endswith("_2.jpg") or
            bn.endswith("_3.jpg") or bn.endswith("_4.jpg")
        ])
        if not standard:
            continue
        slug = _basename_to_slug(standard[0])
        required = [
            "{}_1.jpg".format(slug),
            "{}_2.jpg".format(slug),
            "{}_3.jpg".format(slug),
            "{}_4.jpg".format(slug),
        ]
        name_ru = item_name
        name_en: Optional[str] = None
        try:
            from scripts.translate_place_name import get_search_names, _has_cyrillic
            primary, secondary = get_search_names(item_name)
            if _has_cyrillic(item_name):
                name_ru, name_en = primary, secondary
            else:
                name_en, name_ru = primary, secondary
        except Exception:
            pass

        for i, bn in enumerate(required, 1):
            path = images_dir / bn
            status = "missing"
            if path.exists() and path.stat().st_size >= MIN_IMAGE_BYTES:
                h = image_content_hash(path, min_bytes=MIN_IMAGE_BYTES)
                if h and h not in forbidden_hashes:
                    status = "exists"
                else:
                    missing_basenames.add(bn)
            else:
                missing_basenames.add(bn)
            lines.append(
                "{}\t{}\t{}\t{}\t{}".format(
                    name_ru, name_en or "-", bn, i, status,
                ),
            )

    path = images_dir / DOWNLOAD_LIST_FILENAME
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return missing_basenames


def _read_download_list_missing(images_dir: Path) -> set[str]:
    """
    Read download_list.txt, return set of basenames with status=missing.
    """
    p = images_dir / DOWNLOAD_LIST_FILENAME
    if not p.exists() or not p.is_file():
        return set()
    found: set[str] = set()
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) >= 5 and parts[4].lower() in ("missing", "forbidden"):
            found.add(parts[2])
    return found


def _read_download_todo(images_dir: Path) -> list[tuple[str, str, str]]:
    """
    Read download_todo.txt. Returns list of (basename, item_name, reason).
    Consult this list and forbidden/ when running later image downloads.
    """
    path = images_dir / DOWNLOAD_TODO_FILENAME
    if not path.exists() or not path.is_file():
        return []
    out: list[tuple[str, str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t", 3)
        if len(parts) >= 4:
            out.append((parts[1], parts[2], parts[3]))
        elif len(parts) == 3:
            out.append((parts[1], parts[2], ""))
    return out


def _get_existing_hashes(images_dir: Path, images_root: Optional[Path] = None) -> dict[str, str]:
    """
    Get content hash for all existing image files in directory and all subdirs.

    If images_root is provided, scans all subdirectories in images_root.
    Skips the forbidden/ subfolder. Returns: {filename: hash, ...}
    """
    existing: dict[str, str] = {}

    def _scan_dir(directory: Path) -> None:
        if not directory.exists():
            return
        for path in directory.iterdir():
            if path.is_dir():
                if path.name == FORBIDDEN_SUBDIR_NAME:
                    continue
                continue
            if path.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
                continue
            try:
                if path.stat().st_size < MIN_IMAGE_BYTES:
                    continue
                h = image_content_hash(path, min_bytes=MIN_IMAGE_BYTES)
            except (FileNotFoundError, OSError):
                continue
            if h:
                existing[path.name] = h

    # If images_root provided, scan all subdirs (each guide subdir)
    if images_root and images_root.exists():
        for subdir in images_root.iterdir():
            if not subdir.is_dir() or subdir.name == FORBIDDEN_SUBDIR_NAME:
                continue
            _scan_dir(subdir)
    _scan_dir(images_dir)
    return existing


def _is_duplicate(
    new_path: Path,
    existing_hashes: dict[str, str],
    images_dir: Path,
) -> Optional[str]:
    """
    Check if newly downloaded file is duplicate of any existing file.

    Returns: existing filename if duplicate, None otherwise.
    """
    if not new_path.exists() or new_path.stat().st_size < MIN_IMAGE_BYTES:
        return None
    new_hash = image_content_hash(new_path, min_bytes=MIN_IMAGE_BYTES)
    if not new_hash:
        return None
    for existing_name, existing_hash in existing_hashes.items():
        if existing_hash == new_hash:
            return existing_name
    return None


def _validate_uniqueness(
    path: Path,
    existing_hashes: dict[str, str],
    current_basename: str,
) -> tuple[bool, Optional[str]]:
    """
    Validate that the image at path is unique.

    Returns (True, None) if unique, (False, existing_name) if duplicate.
    """
    if not path.exists() or path.stat().st_size < MIN_IMAGE_BYTES:
        return False, None
    h = image_content_hash(path, min_bytes=MIN_IMAGE_BYTES)
    if not h:
        return False, None
    for existing_name, existing_hash in existing_hashes.items():
        if existing_name == current_basename:
            continue
        if existing_hash == h:
            return False, existing_name
    return True, None


def download_images_with_dedup(
    images_dir: Path,
    image_downloads: dict[str, str],
    image_fallbacks: dict[str, list[str]],
    banned: frozenset[str],
    items: list[dict],
    max_attempts_per_item: int = 20,
    images_root: Optional[Path] = None,
    forbidden_basenames: Optional[frozenset[str]] = None,
    use_ai_identify: bool = False,
    guide_name: str = "",
    force_overwrite: bool = False,
) -> Tuple[dict[str, int], dict[str, int]]:
    """
    Download images with per-download duplicate checking.

    Images are never deleted unless: (1) explicitly requested (force_overwrite),
    or (2) the file is a duplicate of another. By default existing image files
    are not overwritten. Use force_overwrite to replace duplicates or
    re-download. For each item, up to 4 distinct images; after each download,
    validates uniqueness.

    Args:
        images_dir: Directory to save images
        image_downloads: {basename: url, ...}
        image_fallbacks: {basename: [url, ...], ...}
        banned: Set of banned basenames
        items: List of item dicts with 'name' and 'images' keys
        max_attempts_per_item: Max URLs to try per item
        images_root: If set, check hashes in all subdirs
        forbidden_basenames: Basenames to skip (e.g. znamensky_4.jpg).
        use_ai_identify: If True, use AI to check image matches item.
        guide_name: Guide name for AI context (e.g. monasteries).
        force_overwrite: If True, replace existing duplicates; default False.

    Returns:
        Tuple of (results, stats): results is {item_name: count}, stats is
        {downloaded, banned, dups, no_urls, network, timeout, ...}.
    """
    images_dir.mkdir(parents=True, exist_ok=True)
    forbidden_dir = images_dir / FORBIDDEN_SUBDIR_NAME
    forbidden_dir.mkdir(parents=True, exist_ok=True)
    if forbidden_basenames is None:
        forbidden_basenames = FORBIDDEN_BASENAMES
    # Load forbidden hashes from forbidden/ subfolder + constant (fast skip)
    forbidden_hashes = _load_forbidden_hashes(images_dir) | set(FORBIDDEN_IMAGE_HASHES)
    existing_hashes = _get_existing_hashes(images_dir, images_root=images_root)

    # Study directory first, update download_list.txt (RU+EN), consult when
    # downloading
    missing_from_list = download_list_from_directory(
        images_dir, items, guide_name=guide_name,
        forbidden_basenames=forbidden_basenames,
    )
    if missing_from_list and guide_name:
        print(
            "  {}: {} slot(s) to download (from {})".format(
                guide_name, len(missing_from_list), DOWNLOAD_LIST_FILENAME,
            ),
        )

    todo_slots = _read_download_todo(images_dir)
    if todo_slots and guide_name:
        print(
            "  Todo: {} slot(s) from {} (forbidden/ checked).".format(
                len(todo_slots), DOWNLOAD_TODO_FILENAME,
            ),
        )
    if use_ai_identify:
        key = os.environ.get("OPENAI_API_KEY", "")
        print(
            "  AI identify: {}.".format(
                "enabled (OPENAI_API_KEY set)" if key else "disabled (no key)",
            ),
        )
    else:
        print("  AI identify: disabled.")
    pixabay_skip = os.environ.get("PIXABAY_SKIP", "").strip().lower() in (
        "1", "true", "yes",
    )
    pixabay = (
        "skipped" if pixabay_skip
        else ("yes" if os.environ.get("PIXABAY_API_KEY", "").strip() else "no")
    )
    pexels = "yes" if os.environ.get("PEXELS_API_KEY", "").strip() else "no"
    unsplash = "yes" if os.environ.get("UNSPLASH_ACCESS_KEY", "").strip() else "no"
    flickr = "yes" if os.environ.get("FLICKR_API_KEY", "").strip() else "no"
    print(
        "  Image sources (round-robin ×20): Commons, Pixabay ({}), Pexels ({}), "
        "Unsplash ({}), Flickr ({}), Openverse, Yandex".format(
            pixabay, pexels, unsplash, flickr,
        ),
    )
    failed_urls = _load_failed_urls(images_dir)
    if failed_urls:
        print("  Skipping {} known-bad URL(s) from {}.".format(
            len(failed_urls), FAIL_LOG_FILENAME,
        ))

    # Build item -> list of image basenames mapping
    from scripts.validate_images_per_item import _basename

    item_to_basenames: dict[str, list[str]] = {}
    basename_to_item: dict[str, str] = {}
    for item in items:
        name = item.get("name", "?")
        images = item.get("images") or []
        basenames = [_basename(img) for img in images]
        item_to_basenames[name] = basenames
        for bn in basenames:
            basename_to_item[bn] = name

    results: dict[str, int] = {}
    downloaded_count = 0
    failed_slots: list[tuple[str, str, str]] = []  # (basename, item_name, reason)
    fail_log_lines: list[str] = []  # basename\titem_name\treason\turl
    stats: dict[str, int] = {
        "downloaded": 0, "banned": 0, "moved": 0, "dups": 0,
        "no_urls": 0, "network": 0, "timeout": 0, "forbidden": 0,
        "ai_reject": 0, "too_small": 0, "non_image": 0, "other": 0,
    }
    # Cache fetched URLs per item: (urls, num_sources) or ([], 0) if tried+empty
    _url_cache: dict[str, tuple[list[str], int]] = {}
    # Persist source exclusion across round-robin calls (3 failures = skip site)
    _excluded_sources: set[str] = _load_excluded_sources(_PROJECT_ROOT)
    if _excluded_sources:
        print(
            "  Excluded sources (1h): {}.".format(
                ", ".join(sorted(_excluded_sources)),
            ),
        )
    _failure_counts: dict[str, int] = {}

    # Process each item to get 4 distinct images
    for item_idx, item in enumerate(items, 1):
        item_name = item.get("name", "?")
        print("\n[{}/{}] Processing: {}".format(item_idx, len(items), item_name), flush=True)
        basenames = item_to_basenames.get(item_name, [])

        # Filter to only _1, _2, _3, _4 images (standard format)
        standard_basenames = sorted([
            bn for bn in basenames
            if bn.endswith("_1.jpg") or bn.endswith("_2.jpg") or
            bn.endswith("_3.jpg") or bn.endswith("_4.jpg")
        ])
        if not standard_basenames:
            # No standard-format slot in data; cannot derive slug — skip.
            print(
                "  Warning: {} has no _1/_2/_3/_4 image slot in data; "
                "skipped.".format(item_name),
            )
            results[item_name] = 0
            continue

        # Derive slug and always target 4 slots per item (download up to 4).
        # Always process all 4 slots to fill gaps (e.g. name_1, name_3, name_4
        # -> fill name_2) and to detect duplicates (after dedup, fill gaps).
        slug = basename_to_slug(standard_basenames[0])
        required_slots = [
            "{}_1.jpg".format(slug),
            "{}_2.jpg".format(slug),
            "{}_3.jpg".format(slug),
            "{}_4.jpg".format(slug),
        ]
        if len(standard_basenames) < 4:
            print(
                "  {} has {} slot(s) in data; filling up to 4.".format(
                    item_name, len(standard_basenames),
                ),
            )

        # Check upfront if all 4 images already exist and are valid
        # (skip entire item immediately if complete, unless force_overwrite)
        # This skips ALL delays (time.sleep calls) by skipping before download loop
        if not force_overwrite:
            all_exist_and_valid = True
            existing_hashes_check = _get_existing_hashes(images_dir, images_root=images_root)
            for basename in required_slots:
                path = images_dir / basename
                if not path.exists() or path.stat().st_size < MIN_IMAGE_BYTES:
                    all_exist_and_valid = False
                    break
                this_hash = image_content_hash(path, min_bytes=MIN_IMAGE_BYTES)
                if not this_hash or this_hash in forbidden_hashes:
                    all_exist_and_valid = False
                    break
                # Check for duplicates against other files
                is_dup = False
                for existing_name, existing_hash in existing_hashes_check.items():
                    if existing_name == basename:
                        continue
                    if existing_hash == this_hash:
                        is_dup = True
                        break
                if is_dup:
                    all_exist_and_valid = False
                    break
            
            if all_exist_and_valid:
                # Skip immediately - no delays, no URL fetching, no downloads
                print("  SKIP {}: all 4 images exist and valid, skipping item (no delays)".format(item_name), flush=True)
                results[item_name] = 4
                continue

        distinct_count = 0

        for basename in required_slots:
            if distinct_count >= 4:
                break
            path = images_dir / basename
            attempts_for_this_basename = 0
            # Refresh hash list to include any files downloaded for previous items
            existing_hashes = _get_existing_hashes(images_dir, images_root=images_root)
            
            # If file already exists and is valid, skip unless force_overwrite
            if path.exists() and path.stat().st_size >= MIN_IMAGE_BYTES:
                this_hash = image_content_hash(path, min_bytes=MIN_IMAGE_BYTES)
                if not force_overwrite:
                    # Skip existing valid files (do not overwrite)
                    if this_hash and this_hash not in forbidden_hashes:
                        # Valid file: count it and skip download
                        distinct_count += 1
                        if basename not in existing_hashes:
                            existing_hashes[basename] = this_hash
                        print("  SKIP {}: exists, valid (dedup: unique)".format(basename), flush=True)
                        continue
                    # Invalid or forbidden: skip (don't try to replace without force_overwrite)
                    if not this_hash:
                        print("  SKIP {}: exists, invalid hash".format(basename), flush=True)
                    elif this_hash in forbidden_hashes:
                        print("  SKIP {}: exists, forbidden hash".format(basename), flush=True)
                    continue
                
                # force_overwrite=True: check and possibly replace
                if not this_hash:
                    # Invalid file: delete and try to replace
                    path.unlink()
                    print("  SKIP {}: exists, invalid hash (force_overwrite: will replace)".format(basename), flush=True)
                elif this_hash in forbidden_hashes:
                    # Content matches forbidden image: delete and try to replace
                    dest = forbidden_dir / "rejected_{}_{}.jpg".format(
                        path.stem, this_hash[:8],
                    )
                    try:
                        shutil.copy2(str(path), str(dest))
                    except OSError:
                        pass
                    path.unlink()
                    print(
                        "  SKIP {}: exists, forbidden hash (force_overwrite: will replace)".format(
                            basename,
                        ),
                        flush=True,
                    )
                    if basename in existing_hashes:
                        del existing_hashes[basename]
                    # Fall through to download attempt
                else:
                    # Check against ALL existing files (no duplicates allowed)
                    is_dup = False
                    dup_of_name: Optional[str] = None
                    for existing_name, existing_hash in existing_hashes.items():
                        if existing_name == basename:
                            continue
                        if existing_hash == this_hash:
                            is_dup = True
                            dup_of_name = existing_name
                            break

                    if is_dup and dup_of_name:
                        # Same hash = identical. Remove higher suffix (keep _1 over _2).
                        to_remove = (
                            basename
                            if _slot_number(basename) > _slot_number(dup_of_name)
                            else dup_of_name
                        )
                        path_to_remove = images_dir / to_remove
                        if path_to_remove.exists():
                            path_to_remove.unlink()
                            print(
                                "  SKIP {}: exists, duplicate of {} (force_overwrite: will replace)".format(
                                    to_remove,
                                    dup_of_name if to_remove == basename else basename,
                                ),
                                flush=True,
                            )
                        if to_remove in existing_hashes:
                            del existing_hashes[to_remove]
                        if to_remove == basename:
                            # Fall through to download attempt
                            pass
                        else:
                            # Kept current; other removed
                            distinct_count += 1
                            if basename not in existing_hashes:
                                existing_hashes[basename] = this_hash
                            print("  SKIP {}: exists, valid (dedup: kept, duplicate {} removed)".format(
                                basename, to_remove), flush=True)
                            continue

                    if not is_dup:
                        # File is distinct, count it
                        distinct_count += 1
                        if basename not in existing_hashes:
                            existing_hashes[basename] = this_hash
                        print("  SKIP {}: exists, valid (dedup: unique)".format(basename), flush=True)
                        continue

            # Try to download (either missing file or duplicate that was deleted)
            # Refresh existing_hashes to include all files currently in folder
            existing_hashes = _get_existing_hashes(images_dir, images_root=images_root)
            existing_hash_values = set(existing_hashes.values())

            raw_urls = [image_downloads.get(basename)] + list(
                image_fallbacks.get(basename, []),
            )
            urls_to_try = []
            seen: set[str] = set()
            for u in raw_urls:
                if not u:
                    continue
                norm = _normalize_image_url(u)
                if not norm or norm in seen:
                    continue
                if _YANDEX_AVATARS in norm:
                    for variant in _yandex_url_variants(u):
                        v = _normalize_image_url(variant) or variant
                        if v not in seen:
                            urls_to_try.append(v)
                            seen.add(v)
                else:
                    urls_to_try.append(norm)
                    seen.add(norm)
            urls_to_try = [u for u in urls_to_try if u not in failed_urls][:20]

            # When data has no valid URL, fetch from all sources (cached per item).
            urls_from_yandex = False
            url_sources = 1  # Default when from image_downloads
            if not urls_to_try:
                if item_name in _url_cache:
                    urls_to_try, url_sources = _url_cache[item_name]
                    if not urls_to_try:
                        # Already tried all sources for this item, got 0
                        failed_slots.append((basename, item_name, FAIL_NO_URLS))
                        print("  SKIP {}: no URLs found (cached)".format(basename), flush=True)
                        continue
                else:
                    from scripts.translate_place_name import get_search_names
                    name_en_data = item.get("name_en", "").strip() or None
                    if name_en_data and name_en_data != item_name:
                        name_ru = item_name
                        name_en = name_en_data
                    else:
                        name_ru, name_en = get_search_names(item_name)
                    if name_en and name_en != name_ru:
                        print(
                            "  Fetching URLs for '{}' / '{}'...".format(
                                name_ru, name_en,
                            ),
                        )
                    else:
                        print("  Fetching URLs for '{}'...".format(item_name))
                    names_to_try = [name_ru]
                    if name_en and name_en != name_ru:
                        names_to_try.append(name_en)
                    aliases = item.get("aliases") or []
                    for a in aliases[:2]:
                        if isinstance(a, str) and a.strip() and a not in names_to_try:
                            names_to_try.append(a.strip())
                    combined, num_sources = _fetch_urls_round_robin(
                        names_to_try,
                        city="Moscow",
                        city_ru="Москва",
                        max_per_source=5,
                        failed_urls=failed_urls,
                        excluded_sources=_excluded_sources,
                        failure_counts=_failure_counts,
                        project_root=_PROJECT_ROOT,
                    )
                    urls_from_yandex = any(
                        _YANDEX_AVATARS in u for u in combined
                    )
                    if combined:
                        print(
                            "  Round-robin: {} URL(s) from {} sources".format(
                                len(combined), num_sources,
                            ),
                        )
                    urls_to_try = [u for u in combined if u not in failed_urls][:40]
                    url_sources = num_sources
                    _url_cache[item_name] = (urls_to_try, url_sources)
                    if not urls_to_try:
                        failed_slots.append((basename, item_name, FAIL_NO_URLS))
                        stats["no_urls"] += 1
                        print("  SKIP {}: no URLs found".format(basename), flush=True)
                        continue

            downloaded_this_slot = False
            last_fail_reason: Optional[str] = None
            total_urls_tried = len(urls_to_try)
            scale = min(
                max(1, url_sources),
                MAX_SOURCES_FOR_DELAY_SCALE,
            )
            delay_sec = DELAY_BETWEEN_REQUESTS_SEC / scale
            # File missing or needs replacement: try to download
            print("  DOWNLOAD {}: attempting ({} URL(s) available)".format(
                basename, len(urls_to_try)), flush=True)
            for url_idx, url in enumerate(urls_to_try, 1):
                url_idx_str = str(url_idx)
                time.sleep(delay_sec)
                attempts_for_this_basename += 1
                # Max URLs per slot scales with sources (round-robin = less
                # load per site)
                max_urls_per_slot = max(3, min(15, url_sources * 2))
                if attempts_for_this_basename > max_urls_per_slot:
                    break
                data = None
                if any(ord(c) >= 128 for c in url):
                    fetch_url = _url_to_ascii(url)
                    if fetch_url is None:
                        continue
                else:
                    fetch_url = url
                for retry in range(URL_NETWORK_RETRIES):
                    try:
                        req = urllib.request.Request(
                            fetch_url,
                            headers={"User-Agent": "ExcursionGuide/1.0"},
                        )
                        with urllib.request.urlopen(req, timeout=20) as resp:
                            ct = (resp.headers.get("Content-Type") or "").lower()
                            if ct and (
                                ct.startswith("text/") or
                                "application/json" in ct
                            ):
                                last_fail_reason = "non-image content-type"
                                print(
                                    "  DOWNLOAD {}: URL {}/{} failed (non-image content-type: {})".format(
                                        basename, url_idx_str, total_urls_tried, ct,
                                    ),
                                    flush=True,
                                )
                                stats["non_image"] += 1
                                fail_log_lines.append(
                                    "{}\t{}\t{}\t{}".format(
                                        basename, item_name,
                                        "non-image content-type", url,
                                    ),
                                )
                                break
                            data = resp.read()
                        break
                    except (urllib.error.URLError, socket.timeout,
                            TimeoutError, OSError, UnicodeEncodeError) as e:
                        # Network / HTTP / timeout / encoding errors: skip URL
                        if isinstance(e, (socket.timeout, TimeoutError)):
                            last_fail_reason = FAIL_TIMEOUT
                        elif isinstance(e, UnicodeEncodeError):
                            last_fail_reason = "URL encoding"
                        else:
                            last_fail_reason = FAIL_NETWORK
                        if retry < URL_NETWORK_RETRIES - 1:
                            time.sleep(URL_RETRY_DELAY_SEC)
                        else:
                            if last_fail_reason == FAIL_TIMEOUT:
                                stats["timeout"] += 1
                                print(
                                    "  DOWNLOAD {}: URL {}/{} failed ({})".format(
                                        basename, url_idx_str, total_urls_tried, FAIL_TIMEOUT,
                                    ),
                                )
                            else:
                                stats["network"] += 1
                                print(
                                    "  DOWNLOAD {}: URL {}/{} failed ({})".format(
                                        basename, url_idx_str, total_urls_tried, last_fail_reason or FAIL_NETWORK,
                                    ),
                                )
                            break
                try:
                    if data is None or len(data) < MIN_IMAGE_BYTES:
                        if not last_fail_reason:
                            last_fail_reason = FAIL_TOO_SMALL
                        if data is not None and len(data) < MIN_IMAGE_BYTES:
                            print(
                                "  DOWNLOAD {}: URL {}/{} failed ({})".format(
                                    basename, url_idx_str, total_urls_tried, FAIL_TOO_SMALL,
                                ),
                                flush=True,
                            )
                            stats["too_small"] += 1
                            fail_log_lines.append(
                                "{}\t{}\t{}\t{}".format(
                                    basename, item_name,
                                    FAIL_TOO_SMALL, url,
                                ),
                            )
                        elif data is None:
                            print(
                                "  DOWNLOAD {}: URL {}/{} failed ({})".format(
                                    basename, url_idx_str, total_urls_tried, last_fail_reason or "no data",
                                ),
                                flush=True,
                            )
                        continue

                    # Check hash before writing: skip if duplicate of any existing
                    new_hash = image_content_hash_from_bytes(
                        data, min_bytes=MIN_IMAGE_BYTES,
                    )
                    if new_hash and new_hash in existing_hash_values:
                        dup_of = next(
                            (n for n, h in existing_hashes.items() if h == new_hash),
                            None,
                        )
                        if dup_of:
                            print(
                                "  DOWNLOAD {}: URL {}/{} failed (dedup: duplicate of {})".format(
                                    basename, url_idx_str, total_urls_tried, dup_of,
                                ),
                                flush=True,
                            )
                            last_fail_reason = FAIL_DUPLICATE.format(dup_of)
                            stats["dups"] += 1
                            fail_log_lines.append(
                                "{}\t{}\t{}\t{}".format(
                                    basename, item_name,
                                    FAIL_DUPLICATE.format(dup_of), url,
                                ),
                            )
                            time.sleep(DELAY_AFTER_REJECT_SEC)
                        continue

                    # Write to temp file first
                    temp_path = images_dir / (basename + ".tmp")
                    temp_path.write_bytes(data)

                    # Validate uniqueness again (perceptual vs SHA256 consistency)
                    current_hashes = _get_existing_hashes(
                        images_dir, images_root=images_root,
                    )
                    new_hash = image_content_hash(temp_path, min_bytes=MIN_IMAGE_BYTES)
                    if new_hash:
                        if new_hash in forbidden_hashes:
                            dest = forbidden_dir / "rejected_{}_{}.jpg".format(
                                path.stem, new_hash[:8],
                            )
                            try:
                                shutil.copy2(str(temp_path), str(dest))
                            except OSError:
                                pass
                            temp_path.unlink()
                            print(
                                "  DOWNLOAD {}: URL {}/{} failed (dedup: forbidden hash)".format(
                                    basename, url_idx_str, total_urls_tried,
                                ),
                                flush=True,
                            )
                            last_fail_reason = FAIL_FORBIDDEN
                            stats["forbidden"] += 1
                            fail_log_lines.append(
                                "{}\t{}\t{}\t{}".format(
                                    basename, item_name, FAIL_FORBIDDEN, url,
                                ),
                            )
                            time.sleep(DELAY_AFTER_REJECT_SEC)
                            continue
                        is_unique, dup_of = _validate_uniqueness(
                            temp_path, current_hashes, basename,
                        )
                        if not is_unique and dup_of:
                            print(
                                "  DOWNLOAD {}: URL {}/{} failed (dedup: duplicate of {})".format(
                                    basename, url_idx_str, total_urls_tried, dup_of,
                                ),
                                flush=True,
                            )
                            temp_path.unlink()
                            last_fail_reason = FAIL_DUPLICATE.format(dup_of)
                            stats["dups"] += 1
                            fail_log_lines.append(
                                "{}\t{}\t{}\t{}".format(
                                    basename, item_name,
                                    FAIL_DUPLICATE.format(dup_of), url,
                                ),
                            )
                            time.sleep(DELAY_AFTER_REJECT_SEC)
                            continue

                    # Optional: AI image identification
                    if use_ai_identify:
                        try:
                            from scripts.image_identify import image_matches_item
                            _aliases: list[str] = list(
                                item.get("aliases") or [],
                            )
                            _ne = str(item.get("name_en", "") or "").strip()
                            if _ne and _ne != item_name:
                                _aliases.insert(0, _ne)
                            if not image_matches_item(
                                temp_path, item_name,
                                guide_context=guide_name or "place",
                                aliases=_aliases if _aliases else None,
                            ):
                                print(
                                    "  DOWNLOAD {}: URL {}/{} failed (AI reject: does not match '{}')".format(
                                        basename, url_idx_str, total_urls_tried, item_name,
                                    ),
                                    flush=True,
                                )
                                temp_path.unlink()
                                last_fail_reason = FAIL_AI_REJECT
                                stats["ai_reject"] += 1
                                fail_log_lines.append(
                                    "{}\t{}\t{}\t{}".format(
                                        basename, item_name,
                                        FAIL_AI_REJECT, url,
                                    ),
                                )
                                time.sleep(DELAY_AFTER_REJECT_SEC)
                                continue
                        except Exception as e:
                            print(
                                "  AI check failed ({}), accepting image.".format(e),
                                file=sys.stderr,
                            )

                    # Accept: rename temp to final (never overwrite existing
                    # unless force_overwrite or we already removed a dup)
                    if path.exists() and not force_overwrite:
                        temp_path.unlink()
                        print(
                            "  DOWNLOAD {}: URL {}/{} skipped (file exists, use --force-overwrite)".format(
                                basename, url_idx_str, total_urls_tried,
                            ),
                            flush=True,
                        )
                        continue
                    temp_path.rename(path)
                    print(
                        "  DOWNLOAD {}: URL {}/{} SUCCESS (dedup: unique)".format(
                            basename, url_idx_str, total_urls_tried,
                        ),
                        flush=True,
                    )
                    # Validate again after save (ensure still unique)
                    current_hashes = _get_existing_hashes(
                        images_dir, images_root=images_root,
                    )
                    ok, dup_of = _validate_uniqueness(path, current_hashes, basename)
                    if not ok and dup_of:
                        print(
                            "  DOWNLOAD {}: validation failed after save (dedup: duplicate of {}), "
                            "trying next URL".format(basename, dup_of),
                            flush=True,
                        )
                        path.unlink()
                        if basename in existing_hashes:
                            del existing_hashes[basename]
                        last_fail_reason = FAIL_DUPLICATE.format(dup_of)
                        time.sleep(DELAY_AFTER_REJECT_SEC)
                        continue

                    final_hash = image_content_hash(path, min_bytes=MIN_IMAGE_BYTES)
                    if final_hash:
                        existing_hashes[basename] = final_hash
                    distinct_count += 1
                    downloaded_count += 1
                    stats["downloaded"] += 1
                    downloaded_this_slot = True
                    print(
                        "  DOWNLOAD {}: SUCCESS (dedup: unique, {}/4 for {})".format(
                            basename, distinct_count, item_name,
                        ),
                        flush=True,
                    )
                    time.sleep(DELAY_AFTER_DOWNLOAD_SEC)
                    break
                except urllib.error.URLError as e:
                    temp_path = images_dir / (basename + ".tmp")
                    if temp_path.exists():
                        temp_path.unlink()
                    reason = getattr(e, "reason", None)
                    if reason is not None and isinstance(
                        reason, (socket.timeout, TimeoutError),
                    ):
                        last_fail_reason = FAIL_TIMEOUT
                        print(
                            "  DOWNLOAD {}: URL {}/{} failed ({})".format(
                                basename, url_idx_str, total_urls_tried, FAIL_TIMEOUT,
                            ),
                            flush=True,
                        )
                    else:
                        last_fail_reason = FAIL_NETWORK
                        print(
                            "  DOWNLOAD {}: URL {}/{} failed ({})".format(
                                basename, url_idx_str, total_urls_tried, FAIL_NETWORK,
                            ),
                            flush=True,
                        )
                    continue
                except (socket.timeout, TimeoutError, OSError) as e:
                    temp_path = images_dir / (basename + ".tmp")
                    if temp_path.exists():
                        temp_path.unlink()
                    if isinstance(e, (socket.timeout, TimeoutError)):
                        last_fail_reason = FAIL_TIMEOUT
                        print(
                            "  DOWNLOAD {}: URL {}/{} failed ({})".format(
                                basename, url_idx_str, total_urls_tried, FAIL_TIMEOUT,
                            ),
                            flush=True,
                        )
                    else:
                        last_fail_reason = FAIL_NETWORK
                        print(
                            "  DOWNLOAD {}: URL {}/{} failed ({})".format(
                                basename, url_idx_str, total_urls_tried, FAIL_NETWORK,
                            ),
                            flush=True,
                        )
                    continue
                except Exception as e:
                    temp_path = images_dir / (basename + ".tmp")
                    if temp_path.exists():
                        temp_path.unlink()
                    last_fail_reason = "error: {}".format(e)
                    print(
                        "  DOWNLOAD {}: URL {}/{} failed (error: {})".format(
                            basename, url_idx_str, total_urls_tried, str(e)[:50],
                        ),
                        flush=True,
                    )
                    continue

            # Second chance: if we had URLs but all failed (e.g. duplicate), try
            # Yandex search for this place to get different images
            urls_second: list[str] = []
            if (
                not downloaded_this_slot
                and not path.exists()
                and total_urls_tried > 0
                and not urls_from_yandex
            ):
                print(
                    "  All URLs failed for {}, fetching different URLs from "
                    "Yandex...".format(basename),
                )
                urls_second = _fetch_yandex_urls_for_place(
                    item_name, city="Москва", max_images=10,
                )
                total_urls_tried += len(urls_second)
                existing_hashes_2 = _get_existing_hashes(
                    images_dir, images_root=images_root,
                )
                existing_hash_values_2 = set(existing_hashes_2.values())
                for url in urls_second:
                    time.sleep(DELAY_BETWEEN_REQUESTS_SEC)
                    try:
                        req = urllib.request.Request(
                            url,
                            headers={"User-Agent": "ExcursionGuide/1.0"},
                        )
                        with urllib.request.urlopen(req, timeout=20) as resp:
                            data = resp.read()
                    except (urllib.error.URLError, socket.timeout,
                            TimeoutError, OSError):
                        continue
                    if not data or len(data) < MIN_IMAGE_BYTES:
                        continue
                    new_hash_2 = image_content_hash_from_bytes(
                        data, min_bytes=MIN_IMAGE_BYTES,
                    )
                    if new_hash_2 and new_hash_2 in existing_hash_values_2:
                        continue
                    temp_path = images_dir / (basename + ".tmp")
                    temp_path.write_bytes(data)
                    current_hashes = _get_existing_hashes(
                        images_dir, images_root=images_root,
                    )
                    new_hash = image_content_hash(
                        temp_path, min_bytes=MIN_IMAGE_BYTES,
                    )
                    if new_hash and new_hash in forbidden_hashes:
                        temp_path.unlink()
                        continue
                    is_unique, dup_of = _validate_uniqueness(
                        temp_path, current_hashes, basename,
                    )
                    if not is_unique and dup_of:
                        temp_path.unlink()
                        continue
                    if use_ai_identify:
                        try:
                            from scripts.image_identify import image_matches_item
                            _aliases: list[str] = list(
                                item.get("aliases") or [],
                            )
                            _ne = str(item.get("name_en", "") or "").strip()
                            if _ne and _ne != item_name:
                                _aliases.insert(0, _ne)
                            if not image_matches_item(
                                temp_path, item_name,
                                guide_context=guide_name or "place",
                                aliases=_aliases if _aliases else None,
                            ):
                                temp_path.unlink()
                                continue
                        except Exception:
                            pass
                    if path.exists() and not force_overwrite:
                        temp_path.unlink()
                        continue
                    temp_path.rename(path)
                    ok, dup_of = _validate_uniqueness(
                        path,
                        _get_existing_hashes(
                            images_dir, images_root=images_root,
                        ),
                        basename,
                    )
                    if not ok and dup_of:
                        path.unlink()  # Remove just-downloaded dup only
                        continue
                    final_hash = image_content_hash(
                        path, min_bytes=MIN_IMAGE_BYTES,
                    )
                    if final_hash:
                        existing_hashes[basename] = final_hash
                    distinct_count += 1
                    downloaded_count += 1
                    stats["downloaded"] += 1
                    downloaded_this_slot = True
                    print(
                        "  DOWNLOAD {}: SUCCESS (dedup: unique, {}/4 for {}, from Yandex)".format(
                            basename, distinct_count, item_name,
                        ),
                        flush=True,
                    )
                    time.sleep(DELAY_AFTER_DOWNLOAD_SEC)
                    break

            # If we couldn't download a distinct image for this slot, record it
            if not downloaded_this_slot and not path.exists():
                reason = last_fail_reason
                if not reason:
                    reason = (
                        FAIL_NO_URLS if total_urls_tried == 0 else "all URLs failed"
                    )
                failed_slots.append((basename, item_name, reason))
                print(
                    "  DOWNLOAD {}: FAILED (reason: {}, {} URLs tried)".format(
                        basename, reason, total_urls_tried,
                    ),
                    flush=True,
                )

        results[item_name] = distinct_count

    print(
        "\nDownload summary: {} distinct images downloaded across {} items".format(
            downloaded_count, len(results),
        ),
    )
    _print_stats(stats)
    if failed_slots:
        print("\nDownload failures (detail):")
        for bn, iname, reason in failed_slots:
            print("  {} ({}): {}".format(bn, iname, reason))
        _write_download_todo(images_dir, guide_name, failed_slots)
    else:
        _write_download_todo(images_dir, guide_name, [])
    if fail_log_lines:
        _append_fail_log(images_dir, fail_log_lines)
    return results, stats


def _print_stats(stats: dict[str, int]) -> None:
    """Print running stats (downloaded, banned, dups, no URLs, etc.)."""
    parts = [str(stats.get("downloaded", 0)) + " downloaded"]
    for k, v in [
        ("banned", "banned"), ("moved", "moved"), ("dups", "dups"),
        ("no_urls", "no URLs"), ("network", "network"), ("timeout", "timeout"),
        ("forbidden", "forbidden"), ("ai_reject", "AI reject"),
        ("too_small", "too small"), ("non_image", "non-image"),
        ("other", "other"),
    ]:
        n = stats.get(k, 0)
        if n > 0:
            parts.append("{} {}".format(n, v))
    if len(parts) > 1:
        print("  Stats: {}".format(", ".join(parts)))


def validate_item_images_format(
    items: list[dict],
    images_dir: Path,
    guide_name: str = "guide",
) -> tuple[bool, list[str]]:
    """
    Validate that each item has exactly 4 images in format name_1, name_2, name_3, name_4.

    Checks forbidden folder every time: files whose hash is in forbidden/ (or
    FORBIDDEN_IMAGE_HASHES) are treated as missing. Images are distinct, no duplicates.

    Returns: (is_valid, list_of_errors)
    """
    from scripts.validate_images_per_item import _basename

    forbidden_hashes = _load_forbidden_hashes(images_dir) | set(FORBIDDEN_IMAGE_HASHES)
    errors: list[str] = []

    for i, item in enumerate(items, 1):
        name = item.get("name", "?")
        images = item.get("images") or []
        basenames = [_basename(img) for img in images]

        # Filter to standard format (_1, _2, _3, _4) and sort
        standard_basenames = sorted([
            bn for bn in basenames
            if bn.endswith("_1.jpg") or bn.endswith("_2.jpg") or
            bn.endswith("_3.jpg") or bn.endswith("_4.jpg")
        ])

        if len(standard_basenames) != 4:
            errors.append(
                "{} item {} ({!r}): expected exactly 4 images in format "
                "name_1.jpg, name_2.jpg, name_3.jpg, name_4.jpg, got {}: {}".format(
                    guide_name, i, name, len(standard_basenames),
                    standard_basenames,
                ),
            )
            continue

        # Verify format: must have _1, _2, _3, _4
        expected_suffixes = {"_1.jpg", "_2.jpg", "_3.jpg", "_4.jpg"}
        actual_suffixes = {bn[-6:] for bn in standard_basenames}
        if actual_suffixes != expected_suffixes:
            errors.append(
                "{} item {} ({!r}): missing required suffixes. "
                "Expected: {}, Got: {}".format(
                    guide_name, i, name, sorted(expected_suffixes),
                    sorted(actual_suffixes),
                ),
            )
            continue

        # Check all 4 files exist (and are not in forbidden folder by hash)
        missing = []
        for bn in standard_basenames:
            path = images_dir / bn
            if not path.exists() or path.stat().st_size < MIN_IMAGE_BYTES:
                missing.append(bn)
                continue
            h = image_content_hash(path, min_bytes=MIN_IMAGE_BYTES)
            if h and h in forbidden_hashes:
                missing.append(bn)
        if missing:
            errors.append(
                "{} item {} ({!r}): missing files: {}".format(
                    guide_name, i, name, missing,
                ),
            )
            continue

        # Check all 4 are distinct (different content hash)
        # Also check against all other items in the guide
        hashes = []
        all_other_hashes: set[str] = set()
        
        # Collect hashes from all other items first
        for j, other_item in enumerate(items, 1):
            if j == i:
                continue
            other_images = other_item.get("images") or []
            other_basenames = [_basename(img) for img in other_images]
            other_standard = sorted([
                bn for bn in other_basenames
                if bn.endswith("_1.jpg") or bn.endswith("_2.jpg") or
                bn.endswith("_3.jpg") or bn.endswith("_4.jpg")
            ])
            for other_bn in other_standard:
                other_path = images_dir / other_bn
                if not other_path.exists():
                    continue
                other_h = image_content_hash(
                    other_path, min_bytes=MIN_IMAGE_BYTES,
                )
                if other_h and other_h not in forbidden_hashes:
                    all_other_hashes.add(other_h)
        
        for bn in standard_basenames:
            path = images_dir / bn
            h = image_content_hash(path, min_bytes=MIN_IMAGE_BYTES)
            if not h:
                errors.append(
                    "{} item {} ({!r}): could not hash {}".format(
                        guide_name, i, name, bn,
                    ),
                )
                break
            hashes.append(h)
            
            # Check if this image is duplicate of another item
            if h in all_other_hashes:
                errors.append(
                    "{} item {} ({!r}): image {} is duplicate of another item".format(
                        guide_name, i, name, bn,
                    ),
                )

        if len(hashes) == 4 and len(set(hashes)) < 4:
            errors.append(
                "{} item {} ({!r}): duplicate images within item (need 4 "
                "distinct images per item)".format(guide_name, i, name),
            )

    return len(errors) == 0, errors


if __name__ == "__main__":
    print(
        "Download is run via build_pdf.py. Example:",
        file=sys.stderr,
    )
    print(
        "  python scripts/build_pdf.py --guide monasteries --download-only",
        file=sys.stderr,
    )
    print(
        "  python scripts/build_pdf.py --all-guides --download-only",
        file=sys.stderr,
    )
    sys.exit(0)
