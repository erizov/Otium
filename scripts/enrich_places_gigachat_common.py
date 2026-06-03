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
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()
    elif text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    candidates = [text]
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        candidates.append(text[start : end + 1])
    for candidate in candidates:
        cleaned = candidate.strip()
        cleaned = re.sub(r",\s*}", "}", cleaned)
        cleaned = re.sub(r",\s*]", "]", cleaned)
        try:
            obj = json.loads(cleaned)
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            continue
    return None


def gigachat_refusal(text: str) -> bool:
    """True when GigaChat declined (policy / safety), not a JSON payload."""
    low = text.lower()
    markers = (
        "генеративные языковые модели",
        "чувствительными темами",
        "временно ограничены",
        "не могу ответить",
        "не могу предоставить",
    )
    return any(m in low for m in markers)


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
    from scripts.city_guide_narrative import is_landmark_boilerplate

    if is_landmark_boilerplate(text):
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
