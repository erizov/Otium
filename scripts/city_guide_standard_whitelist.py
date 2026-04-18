# -*- coding: utf-8 -*-
"""Reusable URL whitelist checks (same rules as jerusalem/whitelist.py)."""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlparse

_URL_RE = re.compile(r"https://[^\s\|`<>\"]+")


def whitelist_path_for_city(project_root: Path, city_slug: str) -> Path:
    return project_root / city_slug / "docs" / "SOURCES_WHITELIST.md"


def _strip_trailing_junk(url: str) -> str:
    return url.rstrip(").,;]")


def load_prefixes_from_markdown(path: Path) -> tuple[str, ...]:
    text = path.read_text(encoding="utf-8")
    found: set[str] = set()
    for m in _URL_RE.finditer(text):
        u = _strip_trailing_junk(m.group(0))
        if u:
            found.add(u)
    return tuple(sorted(found, key=len, reverse=True))


@lru_cache(maxsize=32)
def _cached_prefixes(path_str: str) -> tuple[str, ...]:
    return load_prefixes_from_markdown(Path(path_str))


def clear_whitelist_cache() -> None:
    _cached_prefixes.cache_clear()


def url_is_whitelisted(
    url: str,
    *,
    whitelist_path: Path | None = None,
) -> bool:
    raw = url.strip()
    if not raw.startswith("https://"):
        return False
    if not whitelist_path or not whitelist_path.is_file():
        return False
    prefixes = _cached_prefixes(str(whitelist_path.resolve()))
    parsed = urlparse(raw)
    host = parsed.netloc.lower()
    if host in ("commons.wikimedia.org", "upload.wikimedia.org"):
        return True
    wiki_hosts = (
        "en.wikipedia.org",
        "en.m.wikipedia.org",
        "de.wikipedia.org",
        "fr.wikipedia.org",
        "it.wikipedia.org",
        "es.wikipedia.org",
        "tr.wikipedia.org",
        "ja.wikipedia.org",
        "he.wikipedia.org",
        "el.wikipedia.org",
        "pt.wikipedia.org",
        "nl.wikipedia.org",
        "da.wikipedia.org",
        "th.wikipedia.org",
    )
    if host in wiki_hosts:
        return parsed.path.startswith("/wiki/")
    for p in prefixes:
        if raw.startswith(p):
            return True
    return False
