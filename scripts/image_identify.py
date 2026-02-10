# -*- coding: utf-8 -*-
"""
AI-generated image identification to skip wrong downloads.

Optional: if enabled, after downloading an image we ask an AI vision model
whether the image matches the expected item (e.g. monastery, church). If not,
we skip the image and try the next URL.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))


def image_matches_item(
    image_path: Path,
    item_name: str,
    guide_context: str = "",
) -> bool:
    """
    Return True if the image appears to show the given item (e.g. place name).

    Uses OpenAI Vision API if OPENAI_API_KEY is set; otherwise returns True
    (no-op, accept image). Guide context can hint the type (e.g. "monastery").
    """
    if not image_path.exists() or not image_path.is_file():
        return False
    if image_path.stat().st_size < 500:
        return False

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return True

    try:
        import base64
        import json
        import urllib.request
    except ImportError:
        return True

    try:
        with open(image_path, "rb") as f:
            b64 = base64.standard_b64encode(f.read()).decode("ascii")
    except OSError:
        return False

    prompt = (
        "Does this image show the following place or object? "
        "Answer only yes or no. Place/object: {}. {}".format(
            item_name,
            "Context: " + guide_context if guide_context else "",
        ).strip()
    )
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "data:image/jpeg;base64," + b64,
                        },
                    },
                ],
            },
        ],
        "max_tokens": 10,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=data,
        headers={
            "Authorization": "Bearer " + api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return True

    choices = result.get("choices") or []
    if not choices:
        return True
    text = (choices[0].get("message") or {}).get("content") or ""
    return "yes" in text.lower().strip()
