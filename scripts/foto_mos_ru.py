# -*- coding: utf-8 -*-
"""
Fetch image URLs from the Moscow photo bank https://foto.mos.ru/

Uses Playwright to search by place name and extract direct image URLs.
Content is free to use with source attribution (mos.ru).
"""

from __future__ import annotations

import re
import time
from urllib.parse import quote, urljoin

_BASE = "https://foto.mos.ru"


def search_foto_mos_ru(
    query: str,
    max_images: int = 10,
    headless: bool = True,
) -> list[str]:
    """
    Search foto.mos.ru by query (Russian place name) and return image URLs.

    Returns up to max_images direct image URLs. Uses Playwright to handle
    client-rendered content.
    """
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    except ImportError:
        return []

    found: set[str] = set()
    query_clean = query.strip() if query else ""
    if not query_clean:
        return []

    search_url = _BASE + "/search?text=" + quote(query_clean, encoding="utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        try:
            page.goto(search_url, wait_until="domcontentloaded", timeout=20000)
            time.sleep(3)
            content = page.content()
            _extract_image_urls(content, _BASE, found)
            if len(found) < max_images:
                time.sleep(2)
                content = page.content()
                _extract_image_urls(content, _BASE, found)
            # Try main page search form if search URL returned few results
            if len(found) < 2:
                page.goto(_BASE + "/", wait_until="domcontentloaded", timeout=15000)
                time.sleep(2)
                search_input = page.query_selector(
                    'input[type="search"], input[name*="search"], '
                    'input[placeholder*="Найти"], input[placeholder*="найти"]'
                )
                if search_input:
                    search_input.fill(query_clean[:100])
                    time.sleep(1)
                    page.keyboard.press("Enter")
                    time.sleep(3)
                    _extract_image_urls(page.content(), _BASE, found)
        except (PWTimeout, Exception):
            pass
        finally:
            browser.close()

    return list(found)[:max_images]


def _extract_image_urls(html: str, base: str, out: set[str]) -> None:
    """Extract image URLs from HTML into out (foto.mos.ru or known CDN)."""
    # img src
    for m in re.finditer(
        r'<img[^>]+(?:src|data-src)=["\']([^"\']+)["\']',
        html,
        re.IGNORECASE,
    ):
        url = m.group(1).strip()
        if not url or url.startswith("data:"):
            continue
        url = urljoin(base, url.split("?")[0])
        if _is_image_url(url):
            out.add(url)
    # picture source
    for m in re.finditer(
        r'<source[^>]+srcset=["\']([^"\']+)["\']',
        html,
        re.IGNORECASE,
    ):
        for part in m.group(1).split(","):
            url = part.strip().split()[0] if part.strip() else ""
            url = urljoin(base, url.split("?")[0])
            if _is_image_url(url):
                out.add(url)
    # Links to foto.mos.ru that look like image paths
    for m in re.finditer(
        r'https?://[^"\s<>\)]+foto\.mos\.ru[^"\s<>\)]*\.(?:jpg|jpeg|png|webp)',
        html,
        re.IGNORECASE,
    ):
        url = m.group(0).split("?")[0]
        out.add(url)


def _is_image_url(url: str) -> bool:
    if not url or "foto.mos.ru" not in url:
        return False
    lower = url.lower()
    return (
        ".jpg" in lower or ".jpeg" in lower or
        ".png" in lower or ".webp" in lower or
        "/photo" in lower or "/foto" in lower or "/image" in lower or
        "/media/" in lower
    )
