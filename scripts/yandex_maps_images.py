# -*- coding: utf-8 -*-
"""
Fetch images from Yandex Maps by place name.

Searches Yandex Maps for a place and extracts photo URLs. Uses Playwright
to handle JavaScript-rendered content.
"""

from __future__ import annotations

import re
import sys
import time
from pathlib import Path
from typing import Optional
from urllib.parse import quote

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))


def search_place_by_name(
    name: str,
    city: str = "Москва",
    max_images: int = 4,
    headless: bool = True,
) -> list[str]:
    """
    Search Yandex Maps by place name and extract photo URLs.

    Args:
        name: Place name (e.g., "Красная площадь", "Новодевичий монастырь")
        city: City name (default: "Москва")
        max_images: Maximum number of images to return
        headless: Run browser in headless mode

    Returns:
        List of image URLs (prefer high-resolution)
    """
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    except ImportError:
        print(
            "Error: playwright not installed. Run: pip install playwright && "
            "playwright install chromium",
            file=sys.stderr,
        )
        return []

    query = "{} {}".format(name, city).strip()
    url = "https://yandex.ru/maps/?text={}".format(
        quote(query, encoding="utf-8"),
    )

    image_urls: list[str] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            time.sleep(5)  # Wait for search results and map

            # Try to find photos section
            # Yandex Maps photos are often in a carousel or gallery
            # Look for image URLs in page content
            content = page.content()

            # Extract image URLs from page
            # Yandex Maps uses various CDN patterns for photos
            found_urls: set[str] = set()

            # Pattern 1: Yandex CDN image URLs
            # avatars.mds.yandex.net/get-images-cbir/..., get-altay/..., i?id=...
            cdn_pattern = r'https://avatars\.mds\.yandex\.net/[^"\s<>\)]+'
            cdn_matches = re.findall(cdn_pattern, content, re.IGNORECASE)
            for url in cdn_matches:
                clean_url = url.split("?")[0]
                if any(
                    p in clean_url
                    for p in [
                        "/get-images-cbir/", "/get-altay/", "/get-images/",
                        "/get-vh/", "/i?id=",
                    ]
                ):
                    found_urls.add(clean_url)

            # Pattern 2: Direct image URLs in img tags
            img_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
            img_matches = re.findall(img_pattern, content, re.IGNORECASE)
            for url in img_matches:
                if "yandex" in url.lower() and any(
                    ext in url.lower() for ext in [".jpg", ".jpeg", ".png", ".webp"]
                ):
                    clean_url = url.split("?")[0]
                    found_urls.add(clean_url)

            # Pattern 3: data-src or data-lazy-src attributes
            lazy_pattern = r'(?:data-src|data-lazy-src)=["\']([^"\']+)["\']'
            lazy_matches = re.findall(lazy_pattern, content, re.IGNORECASE)
            for url in lazy_matches:
                if "yandex" in url.lower():
                    clean_url = url.split("?")[0]
                    found_urls.add(clean_url)

            # Click first search result to open place card (photos are there)
            try:
                first_result_selectors = [
                    '[class*="search-snippet-view"]',
                    'a[class*="search-business-snippet-view"]',
                    '.business-snippet-view',
                    '[data-index="0"]',
                    'ul[class*="search"] li a',
                    '.scroll__container a[href*="/org/"]',
                ]
                clicked = False
                for selector in first_result_selectors:
                    try:
                        el = page.query_selector(selector)
                        if el:
                            el.click()
                            clicked = True
                            break
                    except Exception:
                        continue
                if not clicked:
                    # Fallback: click first link that looks like an org/place link
                    try:
                        org_links = page.query_selector_all('a[href*="/org/"]')
                        if org_links:
                            org_links[0].click()
                            clicked = True
                    except Exception:
                        pass
                if clicked:
                    time.sleep(5)
                    content = page.content()
                    cdn_matches = re.findall(cdn_pattern, content, re.IGNORECASE)
                    if not cdn_matches:
                        time.sleep(3)
                        content = page.content()
                        cdn_matches = re.findall(cdn_pattern, content, re.IGNORECASE)
                    for url in cdn_matches:
                        clean_url = url.split("?")[0]
                        if any(
                            p in clean_url
                            for p in [
                                "/get-images-cbir/", "/get-altay/", "/get-images/",
                                "/get-vh/", "/i?id=",
                            ]
                        ):
                            found_urls.add(clean_url)
                    img_matches = re.findall(img_pattern, content, re.IGNORECASE)
                    for url in img_matches:
                        if "yandex" in url.lower() and any(
                            ext in url.lower() for ext in [".jpg", ".jpeg", ".png", ".webp"]
                        ):
                            found_urls.add(url.split("?")[0])
                    lazy_matches = re.findall(lazy_pattern, content, re.IGNORECASE)
                    for url in lazy_matches:
                        if "yandex" in url.lower():
                            found_urls.add(url.split("?")[0])
            except Exception:
                pass

            # Try clicking "Фото" (Photos) in the place card
            try:
                photo_selectors = [
                    'a[href*="photos"]',
                    'button:has-text("Фото")',
                    '[aria-label*="Фото"]',
                    '[class*="photo"]',
                ]
                for selector in photo_selectors:
                    try:
                        element = page.query_selector(selector)
                        if element:
                            element.click()
                            time.sleep(3)
                            content_after = page.content()
                            for url in re.findall(
                                cdn_pattern, content_after, re.IGNORECASE
                            ):
                                clean_url = url.split("?")[0]
                                if any(
                                    p in clean_url
                                    for p in [
                                        "/get-images-cbir/", "/get-altay/",
                                        "/get-images/", "/get-vh/", "/i?id=",
                                    ]
                                ):
                                    found_urls.add(clean_url)
                            for url in re.findall(img_pattern, content_after, re.IGNORECASE):
                                if "yandex" in url.lower():
                                    found_urls.add(url.split("?")[0])
                            break
                    except Exception:
                        continue
            except Exception:
                pass

            # Convert to list and limit
            image_urls = list(found_urls)[:max_images]

            # If no images found via regex, try to get images from page
            if not image_urls:
                # Try to find img tags
                img_elements = page.query_selector_all("img")
                for img in img_elements[:20]:  # Limit to first 20 images
                    src = img.get_attribute("src") or img.get_attribute("data-src")
                    if src and "yandex" in src.lower() and any(
                        ext in src.lower() for ext in [".jpg", ".jpeg", ".png", ".webp"]
                    ):
                        clean_url = src.split("?")[0]
                        if clean_url not in image_urls:
                            image_urls.append(clean_url)
                            if len(image_urls) >= max_images:
                                break

        except PWTimeout:
            print(
                "Warning: Timeout loading Yandex Maps page for {}".format(query),
                file=sys.stderr,
            )
        except Exception as e:
            print(
                "Error fetching images for {}: {}".format(query, e),
                file=sys.stderr,
            )
        finally:
            browser.close()

    return image_urls[:max_images]


def get_place_images(
    name: str,
    city: str = "Москва",
    max_images: int = 4,
    retry: int = 2,
) -> list[str]:
    """
    Get images for a place with retry logic.

    Args:
        name: Place name
        city: City name
        max_images: Maximum images to return
        retry: Number of retries on failure

    Returns:
        List of image URLs
    """
    for attempt in range(retry + 1):
        urls = search_place_by_name(name, city, max_images, headless=True)
        if urls:
            return urls
        if attempt < retry:
            time.sleep(3)
    return []


def search_yandex_images(
    name: str,
    city: str = "Москва",
    max_images: int = 10,
) -> list[str]:
    """
    Search Yandex Images (yandex.ru/images) by place name.

    Alternative to Maps; may return more URLs when Maps finds none.
    """
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    except ImportError:
        return []

    query = "{} {}".format(name, city).strip()
    search_url = (
        "https://yandex.ru/images/search?text="
        + quote(query, encoding="utf-8")
    )
    found_urls: set[str] = set()
    cdn_pattern = r'https://avatars\.mds\.yandex\.net/[^"\s<>\)]+'
    path_patterns = [
        "/get-images-cbir/", "/get-altay/", "/get-images/",
        "/get-vh/", "/i?id=",
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
            time.sleep(4)
            content = page.content()
            for url in re.findall(cdn_pattern, content, re.IGNORECASE):
                clean_url = url.split("?")[0]
                if any(p in clean_url for p in path_patterns):
                    found_urls.add(clean_url)
            if not found_urls:
                time.sleep(3)
                content = page.content()
                for url in re.findall(cdn_pattern, content, re.IGNORECASE):
                    clean_url = url.split("?")[0]
                    if any(p in clean_url for p in path_patterns):
                        found_urls.add(clean_url)
        except (PWTimeout, Exception):
            pass
        finally:
            browser.close()

    return list(found_urls)[:max_images]


def main() -> int:
    """CLI: test search for a place."""
    if len(sys.argv) < 2:
        print("Usage: python yandex_maps_images.py <place_name> [city]")
        print('Example: python yandex_maps_images.py "Красная площадь" Москва')
        return 1

    name = sys.argv[1]
    city = sys.argv[2] if len(sys.argv) > 2 else "Москва"

    print("Searching Yandex Maps for: {} ({})".format(name, city))
    urls = get_place_images(name, city, max_images=4)

    if urls:
        print("\nFound {} images:".format(len(urls)))
        for i, url in enumerate(urls, 1):
            print("  {}. {}".format(i, url))
    else:
        print("\nNo images found.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
