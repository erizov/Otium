# -*- coding: utf-8 -*-
"""Resolve Wikimedia Commons file URLs (search + imageinfo) for guide assets."""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

_API = "https://commons.wikimedia.org/w/api.php"
_USER_AGENT = (
    "ExcursionGuide/1.0 (Commons API; urllib; contact: project maintainer)"
)


def _api_get(params: dict[str, str]) -> dict[str, Any] | None:
    q = urllib.parse.urlencode(params)
    url = "{}?{}".format(_API, q)
    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, OSError, ValueError) as e:
        print("Commons API GET failed: {}".format(e), file=sys.stderr)
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
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
