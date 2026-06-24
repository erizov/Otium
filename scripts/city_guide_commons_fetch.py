# -*- coding: utf-8 -*-
"""Resolve Wikimedia Commons file URLs (search + imageinfo) for guide assets."""

from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

_API = "https://commons.wikimedia.org/w/api.php"
_USER_AGENT = (
    "ExcursionGuide/1.0 (Commons API; urllib; contact: project maintainer)"
)

_LAST_API_CALL = 0.0
_MIN_API_GAP_SEC = 2.0
_RETRIES_429 = 5
_PAUSE_429_SEC = 45.0


def configure_commons_api_throttle(
    *,
    min_gap_sec: float = 2.0,
    retries_429: int = 5,
    pause_429_sec: float = 45.0,
) -> None:
    """Tune spacing and 429 backoff for bulk Commons API use."""
    global _MIN_API_GAP_SEC, _RETRIES_429, _PAUSE_429_SEC
    _MIN_API_GAP_SEC = max(0.5, float(min_gap_sec))
    _RETRIES_429 = max(1, int(retries_429))
    _PAUSE_429_SEC = max(5.0, float(pause_429_sec))

# Historic / alternate spellings for Commons filename + snippet checks.
_CITY_EXTRA_FILE_TOKENS: dict[str, frozenset[str]] = {
    "volgograd": frozenset({
        "volgograd", "stalingrad", "волгоград", "сталинград",
    }),
    "spb": frozenset({
        "petersburg", "petrograd", "leningrad", "sankt", "peterburg",
        "санкт", "петербург",
    }),
    "moscow": frozenset({"moscow", "moskva", "москва", "kremlin", "кремл"}),
    "kyiv": frozenset({"kyiv", "kiev", "київ", "киев"}),
    "istanbul": frozenset({"istanbul", "constantinople", "стамбул"}),
}


def _api_get(params: dict[str, str]) -> dict[str, Any] | None:
    global _LAST_API_CALL
    q = urllib.parse.urlencode(params)
    url = "{}?{}".format(_API, q)
    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    for attempt in range(_RETRIES_429):
        gap = _MIN_API_GAP_SEC - (time.monotonic() - _LAST_API_CALL)
        if gap > 0:
            time.sleep(gap)
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt + 1 < _RETRIES_429:
                wait = _PAUSE_429_SEC + attempt * 15.0
                print(
                    "Commons API 429: sleep {:.0f}s, retry {}/{} ...".format(
                        wait, attempt + 1, _RETRIES_429,
                    ),
                    file=sys.stderr,
                )
                time.sleep(wait)
                continue
            print("Commons API GET failed: {}".format(e), file=sys.stderr)
            return None
        except (urllib.error.URLError, OSError, ValueError) as e:
            print("Commons API GET failed: {}".format(e), file=sys.stderr)
            return None
        _LAST_API_CALL = time.monotonic()
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return None
    return None


def commons_file_upload_url(file_title: str) -> str | None:
    """Return preferred upload URL for File:Title (SVG/PNG) or None."""
    title = file_title.strip()
    if not title.lower().startswith("file:"):
        title = "File:{}".format(title)
    data = _api_get(
        {
            "action": "query",
            "format": "json",
            "titles": title,
            "prop": "imageinfo",
            "iiprop": "url|mime",
        },
    )
    if not data or "error" in data or "query" not in data:
        return None
    pages = data["query"].get("pages") or {}
    for _pid, page in pages.items():
        infos = page.get("imageinfo") or []
        if not infos:
            continue
        info = infos[0]
        mime = str(info.get("mime", "")).lower()
        if "svg" in mime or "png" in mime or "jpeg" in mime:
            u = info.get("url")
            if isinstance(u, str) and u.startswith("https://"):
                return u
    return None


def commons_city_file_tokens(city_slug: str) -> frozenset[str]:
    """Lower-case tokens expected in a city-correct Commons file name."""
    from scripts.rag.city_map import names_for_slug

    slug = city_slug.strip().lower()
    names = names_for_slug(slug)
    tokens: set[str] = {
        slug,
        slug.replace("_", " "),
        slug.replace("_", ""),
    }
    if names.name_en:
        tokens.add(names.name_en.lower())
        for part in names.name_en.lower().replace("-", " ").split():
            if len(part) >= 3:
                tokens.add(part)
    if names.name_ru:
        tokens.add(names.name_ru.lower())
    tokens.update(_CITY_EXTRA_FILE_TOKENS.get(slug, frozenset()))
    return frozenset(t for t in tokens if t)


def _text_matches_city(text: str, tokens: frozenset[str]) -> bool:
    low = text.lower()
    return any(tok in low for tok in tokens if len(tok) >= 3)


def _is_raster_commons_name(name: str) -> bool:
    low = name.lower()
    if any(low.endswith(s) for s in (".pdf", ".webm", ".djvu", ".svg")):
        return False
    return low.endswith((".jpg", ".jpeg", ".png", ".webp", ".gif"))


def commons_search_raster_title_for_city(
    search_phrase: str,
    city_slug: str,
    *,
    srlimit: int = 20,
) -> str | None:
    """
    Return the first raster Commons file title scoped to ``city_slug``.

    Matches when the city token appears in the file name or search snippet.
    Skips hits that clearly belong to another guide city (e.g. Moscow Kazan
    cathedral when growing Volgograd).
    """
    phrase = search_phrase.strip()
    if not phrase:
        return None
    city_tokens = commons_city_file_tokens(city_slug)
    if not city_tokens:
        return None
    other_slugs = set(_CITY_EXTRA_FILE_TOKENS) - {city_slug.strip().lower()}
    other_tokens: set[str] = set()
    for other in other_slugs:
        other_tokens.update(commons_city_file_tokens(other))
    other_tokens -= city_tokens

    data = _api_get(
        {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": phrase,
            "srnamespace": "6",
            "srlimit": str(srlimit),
        },
    )
    if not data or "error" in data or "query" not in data:
        return None

    hits = data["query"].get("search") or []
    for hit in hits:
        title = str(hit.get("title") or "")
        if not title.startswith("File:"):
            continue
        name = title[5:]
        if not _is_raster_commons_name(name):
            continue
        snippet = str(hit.get("snippet") or "")
        blob = "{} {}".format(name, snippet)
        if not _text_matches_city(blob, city_tokens):
            continue
        if _text_matches_city(blob, other_tokens):
            continue
        return name
    return None


def commons_search_first_image_url(
    search_phrase: str,
    *,
    prefer_suffix: str = ".svg",
) -> str | None:
    """First Commons File: hit matching prefer_suffix (default .svg)."""
    phrase = search_phrase.strip()
    if not phrase:
        return None
    data = _api_get(
        {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": phrase,
            "srnamespace": "6",
            "srlimit": "12",
        },
    )
    if not data or "error" in data or "query" not in data:
        return None
    hits = data["query"].get("search") or []
    titles: list[str] = []
    for h in hits:
        t = h.get("title")
        if isinstance(t, str) and t.startswith("File:"):
            titles.append(t)
    if prefer_suffix:
        lowered = prefer_suffix.lower()
        titles.sort(
            key=lambda x: (0 if x.lower().endswith(lowered) else 1, x),
        )
    for t in titles:
        u = commons_file_upload_url(t)
        if u:
            return u
    return None
