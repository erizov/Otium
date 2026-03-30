# -*- coding: utf-8 -*-

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from spb.whitelist import (  # noqa: E402
    clear_whitelist_cache,
    default_whitelist_path,
    load_prefixes_from_markdown,
    url_is_whitelisted,
)


@pytest.fixture(autouse=True)
def _clear_whitelist_cache() -> None:
    clear_whitelist_cache()
    yield
    clear_whitelist_cache()


def test_default_whitelist_file_exists() -> None:
    p = default_whitelist_path()
    assert p.is_file(), p


def test_load_prefixes_non_empty() -> None:
    p = default_whitelist_path()
    prefs = load_prefixes_from_markdown(p)
    assert len(prefs) >= 10
    assert any("hermitagemuseum" in x for x in prefs)


def test_hermitage_and_commons() -> None:
    p = default_whitelist_path()
    assert url_is_whitelisted(
        "https://www.hermitagemuseum.org/wps/portal/hermitage",
        whitelist_path=p,
    )
    assert url_is_whitelisted(
        "https://commons.wikimedia.org/wiki/File:Spb.jpg",
        whitelist_path=p,
    )
    assert url_is_whitelisted(
        "https://upload.wikimedia.org/wikipedia/commons/1/1a/X.png",
        whitelist_path=p,
    )


def test_ru_wiki_article_path_only() -> None:
    p = default_whitelist_path()
    assert url_is_whitelisted(
        "https://ru.wikipedia.org/wiki/%D0%AD%D1%80%D0%BC%D0%B8%D1%82%D0%B0%D0%B6",
        whitelist_path=p,
    )
    assert not url_is_whitelisted(
        "https://ru.wikipedia.org/w/index.php?title=Test",
        whitelist_path=p,
    )


def test_rejects_random_host() -> None:
    p = default_whitelist_path()
    assert not url_is_whitelisted("https://example.com/foo", whitelist_path=p)
