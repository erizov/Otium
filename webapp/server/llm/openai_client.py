# -*- coding: utf-8 -*-
"""OpenAI client wrapper (optional, enabled via OPENAI_API_KEY)."""

from __future__ import annotations

import json
from typing import Any

from openai import OpenAI


def _extract_json(text: str) -> dict[str, Any] | None:
    try:
        obj = json.loads(text)
        return obj if isinstance(obj, dict) else None
    except json.JSONDecodeError:
        pass
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end < 0 or end <= start:
        return None
    try:
        obj = json.loads(text[start : end + 1])
        return obj if isinstance(obj, dict) else None
    except json.JSONDecodeError:
        return None


def chat_json(model: str, messages: list[dict[str, str]]) -> tuple[dict[str, Any] | None, str]:
    """
    Call OpenAI chat and request JSON output when possible.

    Returns (parsed_json_or_none, raw_text).
    """
    client = OpenAI()
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.4,
            response_format={"type": "json_object"},
        )
    except Exception:
        # Fallback for models that don't support JSON mode.
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.4,
        )
    raw = (resp.choices[0].message.content or "").strip()
    parsed = _extract_json(raw)
    return parsed, raw

