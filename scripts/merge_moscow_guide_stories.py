# -*- coding: utf-8 -*-
"""
Merge Moscow ``*_stories.py`` snippets into ``moscow/data/moscow_places.json``.

Each place gets ``stories_ru`` / ``stories_en`` lists (tourist-style side notes).
Use ``--bilingual`` to Wikipedia-fetch the missing language edition.

Usage:
  python scripts/merge_moscow_guide_stories.py
  python scripts/merge_moscow_guide_stories.py --bilingual
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_narrative import (
    _cyrillic_letter_ratio,
    _extract_english_lead,
    has_cyrillic,
    is_synthetic_tourist_story,
    pick_text_field,
    text_for_edition,
)
from scripts.city_guide_translate import get_edition_translator, translate_for_edition
from scripts.fetch_place_stories import (
    MAX_STORY_CHARS,
    MIN_STORY_CHARS,
    fetch_story_for_place_lang,
)
from scripts.guide_loader import GUIDES, load_places, load_stories


_CATEGORY_EN: dict[str, str] = {
    "monasteries": "monastery",
    "places_of_worship": "place of worship",
    "museums": "museum",
    "palaces": "palace",
    "parks": "park",
    "sculptures": "monument",
    "theaters": "theatre",
    "bridges": "bridge",
    "markets": "market",
    "libraries": "library",
    "metro": "metro station",
    "cemeteries": "cemetery",
    "landmarks": "landmark",
    "buildings": "historic building",
    "squares": "square",
    "viewpoints": "viewpoint",
    "railway_stations": "railway station",
    "places": "city landmark",
}


_CATEGORY_THEME: dict[str, str] = {
    "monasteries": "spiritual and monastic heritage",
    "places_of_worship": "religious life",
    "museums": "cultural collections",
    "palaces": "imperial and aristocratic history",
    "parks": "green city spaces",
    "sculptures": "public memory and art",
    "theaters": "performing arts",
    "bridges": "river crossings and engineering",
    "markets": "everyday commerce",
    "libraries": "learning and books",
    "metro": "Soviet-era transport design",
    "cemeteries": "memorial landscapes",
    "landmarks": "city identity",
    "buildings": "architectural history",
    "squares": "civic gathering places",
    "viewpoints": "panoramas over the city",
    "railway_stations": "rail travel history",
    "places": "urban landmarks",
}


def _synthetic_en_tourist_story(row: dict[str, Any]) -> str:
    """English hook from curated fields when Wikipedia has no EN snippet."""
    history = str(row.get("history") or "").strip()
    year = str(row.get("year_built") or "").strip()
    if not year:
        match = re.search(r"\b(1[5-9]\d{2}|20\d{2})\b", history)
        if match:
            year = match.group(1)
    category = str(row.get("category") or "")
    cat = _CATEGORY_EN.get(category, "sight")
    theme = _CATEGORY_THEME.get(category, "cultural heritage")
    parts = [
        "A notable Moscow {}, part of the city's {}.".format(cat, theme),
    ]
    if year:
        parts.append("Its story reaches back to {}.".format(year))
    return _trim_tourist_snippet(" ".join(parts))


def _clean_story_for_edition(
    story: str,
    edition: str,
    row: dict[str, Any],
) -> str:
    text = str(story).strip()
    if not text or is_synthetic_tourist_story(text):
        return ""
    if text_for_edition(text, edition):
        trimmed = _trim_tourist_snippet(text) or text
        return "" if is_synthetic_tourist_story(trimmed) else trimmed
    if edition == "en":
        lead = _extract_english_lead(text)
        if lead:
            trimmed = _trim_tourist_snippet(lead) or lead
            return "" if is_synthetic_tourist_story(trimmed) else trimmed
    return ""


def _story_lookup() -> dict[str, str]:
    """Place display name (RU) -> story text from category registries."""
    out: dict[str, str] = {}
    for guide in GUIDES:
        stories = load_stories(guide)
        for place in load_places(guide):
            name = str(place.get("name") or "").strip()
            if not name:
                continue
            story = str(stories.get(name) or "").strip()
            if story:
                out[name] = story
    return out


def classify_story_edition(story: str) -> str:
    """Return ``ru`` or ``en`` for a single story snippet."""
    if text_for_edition(story, "ru"):
        return "ru"
    if text_for_edition(story, "en"):
        return "en"
    if has_cyrillic(story) and _cyrillic_letter_ratio(story) >= 0.35:
        return "ru"
    return "en"


def _trim_tourist_snippet(text: str) -> str:
    import re

    parts = re.split(r"(?<=[.!?…])\s+", text.strip())
    out: list[str] = []
    for part in parts:
        if len(" ".join(out + [part])) <= MAX_STORY_CHARS:
            out.append(part)
        else:
            break
    snippet = " ".join(out).strip() if out else text[:MAX_STORY_CHARS].strip()
    if len(snippet) < MIN_STORY_CHARS:
        return ""
    if len(snippet) > MAX_STORY_CHARS:
        snippet = snippet[: MAX_STORY_CHARS - 3].rsplit(" ", 1)[0] + "..."
    return snippet


def _fallback_story_from_narrative(
    row: dict[str, Any],
    edition: str,
) -> str:
    """Tourist-style snippet from curated history / significance."""
    chunks: list[str] = []
    for base in ("history", "significance"):
        text = pick_text_field(row, edition, base)
        if text:
            chunks.append(text)
    if not chunks:
        return ""
    return _trim_tourist_snippet(" ".join(chunks))


def _fill_missing_edition(
    row: dict[str, Any],
    edition: str,
    *,
    bilingual: bool,
) -> str:
    """Return a story for *edition* (``ru`` or ``en``)."""
    key = "stories_{}".format(edition)
    existing = row.get(key) or []
    if existing and str(existing[0]).strip():
        return str(existing[0]).strip()

    name = str(row.get("name_ru") or "").strip()
    if bilingual:
        fetched = fetch_story_for_place_lang(name, edition)
        if fetched:
            return fetched

    alt = "en" if edition == "ru" else "ru"
    alt_key = "stories_{}".format(alt)
    alt_items = row.get(alt_key) or []
    if alt_items:
        tr = get_edition_translator()
        if tr is not None:
            translated = translate_for_edition(
                str(alt_items[0]),
                edition,
                kind="prose",
                translator=tr,
            )
            if translated:
                return _trim_tourist_snippet(translated) or translated
    return ""


def _apply_story_fields(
    row: dict[str, Any],
    story: str,
    *,
    bilingual: bool,
) -> tuple[bool, bool]:
    """Set stories_ru / stories_en on *row*. Returns (ru_added, en_added)."""
    if is_synthetic_tourist_story(story):
        return False, False
    edition = classify_story_edition(story)
    ru_added = en_added = False
    if edition == "ru":
        row["stories_ru"] = [story]
        ru_added = True
    else:
        row["stories_en"] = [story]
        en_added = True

    if bilingual:
        for target in ("ru", "en"):
            key = "stories_{}".format(target)
            if row.get(key):
                continue
            filled = _fill_missing_edition(row, target, bilingual=True)
            if filled and not is_synthetic_tourist_story(filled):
                row[key] = [filled]
                if target == "ru":
                    ru_added = True
                else:
                    en_added = True
    return ru_added, en_added


def merge_stories(
    places_path: Path,
    *,
    bilingual: bool = False,
    fetch_missing_en: bool = False,
    fetch_missing_ru: bool = False,
) -> dict[str, int]:
    rows: list[dict[str, Any]] = json.loads(
        places_path.read_text(encoding="utf-8"),
    )
    lookup = _story_lookup()
    stats = {
        "rows": len(rows),
        "with_any_story": 0,
        "with_ru": 0,
        "with_en": 0,
        "missing_source": 0,
    }
    for row in rows:
        if not isinstance(row, dict):
            continue
        row.pop("stories", None)
        name = str(row.get("name_ru") or "").strip()
        story = lookup.get(name, "")
        if not story:
            stats["missing_source"] += 1
            row.pop("stories_ru", None)
            row.pop("stories_en", None)
            if bilingual:
                for target in ("ru", "en"):
                    filled = _fill_missing_edition(
                        row,
                        target,
                        bilingual=True,
                    )
                    if filled:
                        row["stories_{}".format(target)] = [filled]
                if row.get("stories_ru") or row.get("stories_en"):
                    stats["with_any_story"] += 1
                if row.get("stories_ru"):
                    stats["with_ru"] += 1
                if row.get("stories_en"):
                    stats["with_en"] += 1
            continue
        ru_ok, en_ok = _apply_story_fields(
            row,
            story,
            bilingual=bilingual or fetch_missing_en or fetch_missing_ru,
        )
        if fetch_missing_en and not row.get("stories_en"):
            fetched = fetch_story_for_place_lang(name, "en")
            if fetched:
                row["stories_en"] = [fetched]
                en_ok = True
        if fetch_missing_ru and not row.get("stories_ru"):
            fetched = fetch_story_for_place_lang(name, "ru")
            if fetched:
                row["stories_ru"] = [fetched]
                ru_ok = True
        if ru_ok or en_ok:
            stats["with_any_story"] += 1
        if row.get("stories_ru"):
            stats["with_ru"] += 1
        if row.get("stories_en"):
            stats["with_en"] += 1

    finalize_story_editions(rows)

    places_path.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return stats


def finalize_story_editions(rows: list[dict[str, Any]]) -> None:
    """Keep only curated ``stories_ru`` / ``stories_en`` for each edition."""
    for row in rows:
        if not isinstance(row, dict):
            continue
        for edition in ("ru", "en"):
            key = "stories_{}".format(edition)
            raw = row.get(key) or []
            if not raw:
                row.pop(key, None)
                continue
            cleaned = _clean_story_for_edition(str(raw[0]), edition, row)
            if cleaned and not is_synthetic_tourist_story(cleaned):
                row[key] = [cleaned]
            else:
                row.pop(key, None)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Merge Moscow place stories into moscow_places.json.",
    )
    parser.add_argument(
        "--bilingual",
        action="store_true",
        help="Wikipedia-fetch missing RU/EN story edition.",
    )
    parser.add_argument(
        "--fetch-missing-en",
        action="store_true",
        help="Wikipedia-fetch EN stories only where stories_en is absent.",
    )
    parser.add_argument(
        "--fetch-missing-ru",
        action="store_true",
        help="Wikipedia-fetch RU stories only where stories_ru is absent.",
    )
    parser.add_argument(
        "--places-json",
        type=Path,
        default=_PROJECT_ROOT / "moscow" / "data" / "moscow_places.json",
    )
    args = parser.parse_args()
    stats = merge_stories(
        args.places_json,
        bilingual=args.bilingual,
        fetch_missing_en=args.fetch_missing_en,
        fetch_missing_ru=args.fetch_missing_ru,
    )
    print(
        "Merged stories: {} / {} places "
        "(ru: {}, en: {}, no source: {})".format(
            stats["with_any_story"],
            stats["rows"],
            stats["with_ru"],
            stats["with_en"],
            stats["missing_source"],
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
