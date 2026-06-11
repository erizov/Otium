# -*- coding: utf-8 -*-
"""Moscow guide stories merged into moscow_places.json."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.city_guide_narrative import (
    is_synthetic_tourist_story,
    text_for_edition,
)

_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_moscow_places_have_curated_edition_stories() -> None:
    path = _PROJECT_ROOT / "moscow" / "data" / "moscow_places.json"
    rows = json.loads(path.read_text(encoding="utf-8"))
    with_ru = with_en = 0
    for row in rows:
        ru = row.get("stories_ru") or []
        en = row.get("stories_en") or []
        if ru:
            with_ru += 1
        if en:
            with_en += 1
        for item in ru + en:
            text = str(item)
            assert not is_synthetic_tourist_story(text)
        for item in ru:
            assert text_for_edition(str(item), "ru")
        for item in en:
            assert text_for_edition(str(item), "en")
    assert with_ru >= 200
