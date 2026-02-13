# -*- coding: utf-8 -*-
"""
Translate place names for image search (Russian <-> English).

Uses OpenAI API if OPENAI_API_KEY is set; otherwise returns the original.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

_CACHE: dict[str, str] = {}


def _has_cyrillic(text: str) -> bool:
    """True if text contains Cyrillic characters."""
    return bool(re.search(r"[\u0400-\u04FF]", text))


def translate_to_english(name: str) -> str:
    """
    Translate place name to English (for image search on Commons/Pixabay/Pexels).

    If name is already ASCII/English, returns as-is. If Cyrillic, uses OpenAI
    to translate. Caches results. Returns original on API failure.
    """
    if not name or not _has_cyrillic(name):
        return name
    if name in _CACHE:
        return _CACHE[name]
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        return name
    try:
        import urllib.request
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Translate this Moscow place name to English. "
                        "Return ONLY the English name, nothing else. "
                        "Example: Храм Василия Блаженного -> Saint Basil's Cathedral. "
                        "Name: {}".format(name)
                    ),
                },
            ],
            "max_tokens": 50,
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=data,
            headers={
                "Authorization": "Bearer " + key,
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        choices = result.get("choices") or []
        if choices:
            text = (
                (choices[0].get("message") or {}).get("content") or ""
            ).strip()
            if text and text != name:
                _CACHE[name] = text
                return text
    except Exception:
        pass
    _CACHE[name] = name
    return name


def translate_to_russian(name: str) -> str:
    """
    Translate place name to Russian (for Yandex search).

    If name has Cyrillic, returns as-is. If English, uses OpenAI to translate.
    Caches results.
    """
    if not name or _has_cyrillic(name):
        return name
    cache_key = "en2ru:" + name
    if cache_key in _CACHE:
        return _CACHE[cache_key]
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        return name
    try:
        import urllib.request
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Translate this Moscow place name to Russian. "
                        "Return ONLY the Russian name, nothing else. "
                        "Name: {}".format(name)
                    ),
                },
            ],
            "max_tokens": 50,
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=data,
            headers={
                "Authorization": "Bearer " + key,
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        choices = result.get("choices") or []
        if choices:
            text = (
                (choices[0].get("message") or {}).get("content") or ""
            ).strip()
            if text and text != name:
                _CACHE[cache_key] = text
                return text
    except Exception:
        pass
    _CACHE[cache_key] = name
    return name


def get_search_names(item_name: str) -> tuple[str, str | None]:
    """
    Return (name_ru, name_en) for image search. Try both for better coverage.

    If item_name has Cyrillic: name_ru=original, name_en=AI-translated.
    If item_name is English: name_ru=AI-translated, name_en=original.
    """
    if _has_cyrillic(item_name):
        name_ru = item_name
        name_en = translate_to_english(item_name)
        return name_ru, name_en if (name_en and name_en != name_ru) else None
    name_en = item_name
    name_ru = translate_to_russian(item_name)
    secondary = name_ru if (name_ru and name_ru != name_en) else None
    return name_en, secondary
