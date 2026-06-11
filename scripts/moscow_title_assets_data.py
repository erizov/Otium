# -*- coding: utf-8 -*-
"""Load Moscow title-page heraldry and university metadata."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_DATA_PATH = _PROJECT_ROOT / "moscow" / "data" / "moscow_title_assets.json"


def moscow_title_assets_path() -> Path:
    return _DATA_PATH


def load_moscow_title_assets() -> dict[str, Any]:
    """Parse ``moscow/data/moscow_title_assets.json``."""
    raw = _DATA_PATH.read_text(encoding="utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("moscow_title_assets.json must be a JSON object")
    return data


def moscow_history_coats(edition: str) -> tuple[tuple[str, str], ...]:
    """(image rel, caption) for historical heraldry strip."""
    key = "caption_ru" if edition == "ru" else "caption_en"
    rows: list[tuple[str, str]] = []
    for item in load_moscow_title_assets().get("history_coats", []):
        if not isinstance(item, dict):
            continue
        image = item.get("image")
        caption = item.get(key) or item.get("caption_ru")
        if isinstance(image, str) and isinstance(caption, str):
            rows.append((image, caption))
    return tuple(rows)


def _university_image_rel(item: dict[str, Any], edition: str) -> str | None:
    """Edition-specific logo path; RU may reuse ``image_en`` (e.g. MFTI)."""
    if edition == "ru":
        keys = ("image_ru", "image_en", "image")
    else:
        keys = ("image_en", "image")
    for key in keys:
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def moscow_universities(
    edition: str,
) -> tuple[tuple[str, str, bool, bool], ...]:
    """
    (image rel, caption, dark_bg, large_logo) for the university strip.

    ``dark_bg`` requests a dark pill behind light-on-transparent logos.
    ``large_logo`` bumps max-height for wide/low-contrast marks (e.g. MFTI).
    """
    key = "name_ru" if edition == "ru" else "name_en"
    rows: list[tuple[str, str, bool, bool]] = []
    for item in load_moscow_title_assets().get("universities", []):
        if not isinstance(item, dict):
            continue
        image = _university_image_rel(item, edition)
        caption = item.get(key) or item.get("name_ru")
        dark_bg = bool(item.get("dark_bg"))
        large_logo = bool(item.get("large_logo"))
        if isinstance(image, str) and isinstance(caption, str):
            rows.append((image, caption, dark_bg, large_logo))
    return tuple(rows)


def moscow_bundled_asset_pairs() -> tuple[tuple[str, str], ...]:
    """(images/dest rel, data/bundled rel) copied into ``moscow/images/``."""
    pairs: list[tuple[str, str]] = []
    for item in load_moscow_title_assets().get("universities", []):
        if not isinstance(item, dict):
            continue
        bundled = item.get("bundled")
        if not isinstance(bundled, str) or not bundled.strip():
            continue
        dest = _university_image_rel(item, "en") or item.get("image")
        if isinstance(dest, str) and dest.strip():
            pairs.append((dest.strip(), bundled.strip()))
    return tuple(pairs)


def install_moscow_bundled_assets(output_dir: Path) -> int:
    """Copy git-tracked bundled logos into ``moscow/images/``."""
    root = output_dir.resolve()
    installed = 0
    for dest_rel, bundled_rel in moscow_bundled_asset_pairs():
        src = root / bundled_rel.replace("\\", "/")
        dest = root / dest_rel.replace("\\", "/")
        if not src.is_file():
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(src.read_bytes())
        installed += 1
    return installed


def moscow_download_pairs() -> tuple[tuple[str, list[str]], ...]:
    """(dest rel, source URLs) for ``download_moscow_title_assets``."""
    data = load_moscow_title_assets()
    pairs: list[tuple[str, list[str]]] = []
    for block_key in ("history_coats", "official_symbols", "universities"):
        for item in data.get(block_key, []):
            if not isinstance(item, dict):
                continue
            if item.get("bundled"):
                continue
            image = _university_image_rel(item, "en") or item.get("image")
            urls = item.get("urls")
            if not isinstance(image, str) or not isinstance(urls, list):
                continue
            clean_urls = [u for u in urls if isinstance(u, str) and u.strip()]
            if clean_urls:
                pairs.append((image, clean_urls))
    return tuple(pairs)
