# -*- coding: utf-8 -*-
"""Load city guide places that have local images."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

MIN_IMAGE_BYTES = 500

_CITY_ROOTS = ('madrid', 'barcelona', 'lisbon')


def _local_additional_images(
    project_root: Path,
    city: str,
    row: dict[str, Any],
) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for extra in row.get("additional_images") or []:
        if len(out) >= 1:
            break
        if not isinstance(extra, dict):
            continue
        rel = str(extra.get("image_rel_path") or "").strip()
        if not rel:
            continue
        path = project_root / city / rel
        if not path.is_file() or path.stat().st_size < MIN_IMAGE_BYTES:
            continue
        out.append({
            "image_rel_path": rel,
            "image_source_url": str(extra.get("image_source_url") or ""),
        })
    return out


def load_city_index(project_root: Path) -> dict[str, dict[str, Any]]:
    """Map ``city:slug`` -> place row with ``city`` and ``image_rel_path``."""
    index: dict[str, dict[str, Any]] = {}
    for city in _CITY_ROOTS:
        data_dir = project_root / city / "data"
        if not data_dir.is_dir():
            continue
        for path in sorted(data_dir.glob("*places*.json")):
            try:
                rows = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            if not isinstance(rows, list):
                continue
            for row in rows:
                if not isinstance(row, dict):
                    continue
                slug = str(row.get("slug") or "").strip()
                rel = str(row.get("image_rel_path") or "").strip()
                if not slug or not rel:
                    continue
                img = project_root / city / rel
                if not img.is_file() or img.stat().st_size < MIN_IMAGE_BYTES:
                    continue
                key = "{}:{}".format(city, slug)
                index[key] = {
                    "city": city,
                    "slug": slug,
                    "name_ru": str(row.get("name_ru") or ""),
                    "name_en": str(
                        row.get("subtitle_en") or row.get("name_en") or "",
                    ),
                    "image_rel_path": rel,
                    "image_source_url": str(
                        row.get("image_source_url") or "",
                    ),
                    "history_ru": str(
                        row.get("history_ru") or row.get("history") or "",
                    ),
                    "history_en": str(
                        row.get("history_en") or row.get("history") or "",
                    ),
                    "significance_ru": str(
                        row.get("significance_ru")
                        or row.get("significance")
                        or "",
                    ),
                    "significance_en": str(
                        row.get("significance_en")
                        or row.get("significance")
                        or "",
                    ),
                    "year_built": str(row.get("year_built") or ""),
                    "architecture_style": str(
                        row.get("architecture_style") or "",
                    ),
                    "address": str(row.get("address") or ""),
                    "additional_images": _local_additional_images(
                        project_root,
                        city,
                        row,
                    ),
                }
    return index
