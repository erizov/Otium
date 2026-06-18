# -*- coding: utf-8 -*-
"""Discover image URLs from city-trusted official / tourism hosts."""

from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable
from pathlib import Path
from urllib.parse import urlparse

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_standard_whitelist import load_prefixes_from_markdown

_USER_AGENT = (
    "ExcursionGuide/1.0 (trusted image discovery; Python urllib)"
)
_OPENVERSE = "https://api.openverse.org/v1/images/"
_WIKI_API = "https://{lang}.wikipedia.org/w/api.php"

# Hosts listed for facts/RAG — not used for image discovery.
_FACTS_ONLY_HOSTS = frozenset({
    "www.unesco.org",
    "www.wikidata.org",
    "en.wikipedia.org",
    "en.m.wikipedia.org",
    "ru.wikipedia.org",
    "de.wikipedia.org",
    "fr.wikipedia.org",
    "it.wikipedia.org",
    "es.wikipedia.org",
    "ca.wikipedia.org",
    "tr.wikipedia.org",
    "ja.wikipedia.org",
    "he.wikipedia.org",
    "el.wikipedia.org",
    "pt.wikipedia.org",
    "nl.wikipedia.org",
    "da.wikipedia.org",
    "th.wikipedia.org",
    "commons.wikimedia.org",
})

_IMAGE_EXT_RE = re.compile(
    r"\.(?:jpe?g|png|webp|gif)(?:\?|$)",
    re.IGNORECASE,
)


def trusted_image_hosts(whitelist_path: Path) -> tuple[str, ...]:
    """
    Official / tourism netloc names from ``SOURCES_WHITELIST.md``.

    Skips Wikipedia, UNESCO, Wikidata, and Commons (handled elsewhere).
    """
    if not whitelist_path.is_file():
        return ()
    prefixes = load_prefixes_from_markdown(whitelist_path)
    hosts: set[str] = set()
    for prefix in prefixes:
        parsed = urlparse(prefix)
        host = (parsed.netloc or "").lower().strip()
        if not host or host in _FACTS_ONLY_HOSTS:
            continue
        if "wikimedia.org" in host:
            continue
        hosts.add(host)
    return tuple(sorted(hosts))


def _host_allowed(url: str, allowed_hosts: frozenset[str]) -> bool:
    host = urlparse(url).netloc.lower()
    if not host:
        return False
    if host in allowed_hosts:
        return True
    return any(host == h or host.endswith("." + h) for h in allowed_hosts)


def _looks_like_image_url(url: str) -> bool:
    low = url.lower().split("?", 1)[0]
    if _IMAGE_EXT_RE.search(low):
        return True
    if "/images/" in low or "/media/" in low or "/uploads/" in low:
        return True
    return False


def _api_get(url: str, timeout: int = 45) -> dict | None:
    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, OSError, TimeoutError):
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def openverse_trusted_urls(
    query: str,
    allowed_hosts: frozenset[str],
    *,
    max_urls: int = 5,
) -> list[str]:
    """Openverse hits whose image or landing page is on a trusted host."""
    phrase = query.strip()
    if not phrase or not allowed_hosts:
        return []
    params = urllib.parse.urlencode({
        "q": phrase[:120],
        "page_size": str(min(max_urls * 4, 20)),
        "page": "1",
    })
    data = _api_get("{}?{}".format(_OPENVERSE, params))
    if not data:
        return []
    out: list[str] = []
    seen: set[str] = set()
    for row in data.get("results") or []:
        for key in ("url", "thumbnail"):
            src = str(row.get(key) or "").strip()
            if not src.startswith("https://"):
                continue
            landing = str(row.get("foreign_landing_url") or src)
            if not (
                _host_allowed(src, allowed_hosts)
                or _host_allowed(landing, allowed_hosts)
            ):
                continue
            if src in seen:
                continue
            seen.add(src)
            out.append(src)
            break
        if len(out) >= max_urls:
            break
    return out


def wikipedia_lead_image_urls(
    query: str,
    *,
    lang: str = "en",
    max_urls: int = 2,
) -> list[str]:
    """Lead/original image from the top Wikipedia search hit."""
    phrase = query.strip()
    if not phrase:
        return []
    params = urllib.parse.urlencode({
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": phrase,
        "gsrlimit": str(max_urls),
        "prop": "pageimages",
        "piprop": "original",
    })
    api = _WIKI_API.format(lang=lang)
    data = _api_get("{}?{}".format(api, params))
    if not data:
        return []
    pages = data.get("query", {}).get("pages") or {}
    out: list[str] = []
    for page in pages.values():
        info = (page.get("original") or {}).get("source")
        if isinstance(info, str) and info.startswith("https://"):
            out.append(info)
    return out


def discover_trusted_image_urls(
    query: str,
    *,
    whitelist_path: Path,
    url_is_whitelisted: Callable[..., bool],
    exclude_url: str = "",
    max_per_source: int = 3,
) -> list[str]:
    """
  Yield unique whitelisted URLs: Openverse (trusted hosts), then Wikipedia.

  Commons is handled by the caller.
  """
    hosts = trusted_image_hosts(whitelist_path)
    allowed = frozenset(hosts)
    seen: set[str] = set()
    out: list[str] = []

    def _add(url: str) -> None:
        u = url.strip()
        if not u or u == exclude_url or u in seen:
            return
        if not _looks_like_image_url(u):
            return
        if not url_is_whitelisted(u, whitelist_path=whitelist_path):
            return
        seen.add(u)
        out.append(u)

    for u in openverse_trusted_urls(
        query, allowed, max_urls=max_per_source,
    ):
        _add(u)

    for lang in ("en", "ru"):
        for u in wikipedia_lead_image_urls(
            query, lang=lang, max_urls=max_per_source,
        ):
            _add(u)

    return out
