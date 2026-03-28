# -*- coding: utf-8 -*-
"""Проверка URL источников по spb/docs/SOURCES_WHITELIST.md."""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlparse

_URL_RE = re.compile(r"https://[^\s\|`<>\"]+")


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def default_whitelist_path() -> Path:
    return _project_root() / "spb" / "docs" / "SOURCES_WHITELIST.md"


def _strip_trailing_junk(url: str) -> str:
    return url.rstrip(").,;]")


def load_prefixes_from_markdown(path: Path) -> tuple[str, ...]:
    """Читает whitelist-файл и возвращает уникальные URL-префиксы (длинные первыми)."""
    text = path.read_text(encoding="utf-8")
    found: set[str] = set()
    for m in _URL_RE.finditer(text):
        u = _strip_trailing_junk(m.group(0))
        if u:
            found.add(u)
    return tuple(sorted(found, key=len, reverse=True))


@lru_cache(maxsize=1)
def _cached_prefixes(path_str: str) -> tuple[str, ...]:
    return load_prefixes_from_markdown(Path(path_str))


def clear_whitelist_cache() -> None:
    """Сброс кэша (для тестов)."""
    _cached_prefixes.cache_clear()


def url_is_whitelisted(
    url: str,
    *,
    whitelist_path: Path | None = None,
) -> bool:
    """True, если url разрешён whitelist и доп. правилами для Commons/Вики.

    Дополнения к букве таблицы в MD (раздел F и фото Commons):
    - любой путь на commons.wikimedia.org и upload.wikimedia.org;
    - ru.wikipedia.org только с путём /wiki/... (статьи).
    """
    raw = url.strip()
    if not raw.startswith("https://"):
        return False
    path = whitelist_path or default_whitelist_path()
    if not path.is_file():
        return False
    prefixes = _cached_prefixes(str(path.resolve()))
    parsed = urlparse(raw)
    host = parsed.netloc.lower()
    if host in ("commons.wikimedia.org", "upload.wikimedia.org"):
        return True
    if host in ("ru.wikipedia.org", "ru.m.wikipedia.org"):
        return parsed.path.startswith("/wiki/")
    for p in prefixes:
        if raw.startswith(p):
            return True
    return False


def collect_bad_urls(
    urls: list[str],
    *,
    whitelist_path: Path | None = None,
) -> list[str]:
    """Возвращает urls, не прошедшие проверку."""
    out: list[str] = []
    for u in urls:
        if not url_is_whitelisted(u, whitelist_path=whitelist_path):
            out.append(u)
    return out
