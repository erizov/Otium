# -*- coding: utf-8 -*-
"""Shared helpers for GigaChat place narrative enrichment."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from scripts.city_guide_core import is_substantive_text

_CULTURE_RU_STUB = "Архитектурный объект из каталога"
_CYRILLIC_RE = re.compile(r"[\u0400-\u04FF]")


def load_dotenv(project_root: Path) -> None:
    try:
        from dotenv import load_dotenv as _ld
    except ImportError:
        return
    _ld(project_root / ".env")


def extract_json(text: str) -> dict[str, Any] | None:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        obj = json.loads(text)
        return obj if isinstance(obj, dict) else None
    except json.JSONDecodeError:
        pass
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end <= start:
        return None
    try:
        obj = json.loads(text[start : end + 1])
        return obj if isinstance(obj, dict) else None
    except json.JSONDecodeError:
        return None


def has_cyrillic(text: str) -> bool:
    return bool(_CYRILLIC_RE.search(text))


def field_is_stub(field: str | None) -> bool:
    if not field:
        return True
    text = str(field).strip()
    if not text:
        return True
    if _CULTURE_RU_STUB in text:
        return True
    return not is_substantive_text(text)


def is_english_narrative(text: str | None) -> bool:
    """Substantive text that is not Cyrillic (English / Latin script)."""
    if field_is_stub(text):
        return False
    return not has_cyrillic(str(text))


def gigachat_failed(raw: str) -> bool:
    low = raw.strip().lower()
    return low.startswith("ошибка") or low.startswith("error")


def discover_cities(project_root: Path, selected: list[str] | None) -> list[str]:
    if selected:
        return selected
    out: list[str] = []
    for child in sorted(project_root.iterdir()):
        if not child.is_dir():
            continue
        slug = child.name
        if (child / "data" / "{}_places.json".format(slug)).is_file():
            out.append(slug)
    return out
