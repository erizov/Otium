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
    aliases: Optional[list[str]] = None,
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

    ctx = guide_context or "place"
    _ctx_map = {
        "places_of_worship": "church or place of worship in Moscow",
        "monasteries": "monastery in Moscow",
        "parks": "park in Moscow",
        "museums": "museum in Moscow",
        "palaces": "palace in Moscow",
        "buildings": "building in Moscow",
        "sculptures": "sculpture or monument in Moscow",
        "places": "place or landmark in Moscow",
        "squares": "square or plaza in Moscow",
        "metro": "metro station in Moscow",
        "theaters": "theater building in Moscow",
        "viewpoints": "viewpoint or observation deck in Moscow",
        "bridges": "bridge in Moscow",
        "markets": "market or food hall in Moscow",
        "libraries": "library building in Moscow",
        "railway_stations": "railway station in Moscow",
        "cemeteries": "cemetery or necropolis in Moscow",
        "landmarks": "iconic landmark or building in Moscow",
        "cafes": "cafe or restaurant in Moscow",
    }
    ctx = _ctx_map.get(ctx, ctx)
    place_desc = item_name
    if aliases:
        extra = " (also known as: {})".format(", ".join(aliases[:5]))
        place_desc = item_name + extra
    prompt = (
        "Does this image show THIS SPECIFIC place (and not a different similar "
        "building)? Reject if the image appears AI-generated, synthetic, or a "
        "digital rendering. Reject if the image contains people or crowds. "
        "Answer only yes or no. Place: {}. Context: {}.".format(
            place_desc, ctx,
        )
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
