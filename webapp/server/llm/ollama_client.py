# -*- coding: utf-8 -*-
"""Ollama HTTP client (local) with model scoring."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

import requests


@dataclass(frozen=True)
class OllamaModel:
    name: str
    score: float


_RE_B = re.compile(r"(?P<num>\d+(?:\.\d+)?)\s*b\b", re.IGNORECASE)
_RE_MIX = re.compile(r"(?P<experts>\d+)\s*x\s*(?P<each>\d+(?:\.\d+)?)b", re.I)


def _estimate_params_b(name: str) -> float | None:
    """
    Heuristic parameter estimate in billions from model name.

    Examples:
    - "llama3.1:70b" -> 70
    - "qwen2.5:14b-instruct" -> 14
    - "mixtral:8x7b" -> 56
    """
    s = name.replace("_", " ").replace("-", " ").lower()
    m = _RE_MIX.search(s)
    if m:
        try:
            return float(m.group("experts")) * float(m.group("each"))
        except ValueError:
            return None
    m = _RE_B.search(s)
    if not m:
        return None
    try:
        return float(m.group("num"))
    except ValueError:
        return None


def _family_rank(name: str) -> float:
    s = name.lower()
    # Rough quality preference (when sizes are similar).
    if "llama3" in s or "llama 3" in s:
        return 9.0
    if "qwen2.5" in s or "qwen 2.5" in s:
        return 8.8
    if "qwen2" in s or "qwen 2" in s:
        return 8.3
    if "mixtral" in s:
        return 8.2
    if "mistral" in s:
        return 7.8
    if "gemma" in s:
        return 7.4
    if "phi" in s:
        return 6.8
    return 7.0


def score_model(name: str) -> float:
    params = _estimate_params_b(name)
    if params is None:
        params_score = 0.0
    else:
        # Log-like scaling: large jumps matter, but don't dwarf family.
        params_score = min(params, 120.0) / 10.0
    return _family_rank(name) * 10.0 + params_score


def list_models(base_url: str = "http://localhost:11434") -> list[OllamaModel]:
    url = f"{base_url.rstrip('/')}/api/tags"
    res = requests.get(url, timeout=5)
    res.raise_for_status()
    data = res.json()
    models = data.get("models") or []
    out: list[OllamaModel] = []
    for item in models:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", "")).strip()
        if not name:
            continue
        out.append(OllamaModel(name=name, score=score_model(name)))
    out.sort(key=lambda m: m.score, reverse=True)
    return out


def best_model_name(models: list[OllamaModel]) -> str | None:
    return models[0].name if models else None


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


def chat_json(
    model: str,
    messages: list[dict[str, str]],
    base_url: str = "http://localhost:11434",
) -> tuple[dict[str, Any] | None, str]:
    """
    Call Ollama chat with JSON response request.

    Returns (parsed_json_or_none, raw_text).
    """
    url = f"{base_url.rstrip('/')}/api/chat"
    payload: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.4},
    }
    res = requests.post(url, json=payload, timeout=120)
    res.raise_for_status()
    data = res.json()
    msg = data.get("message") or {}
    raw = str(msg.get("content", "") or "")
    parsed = _extract_json(raw)
    return parsed, raw

