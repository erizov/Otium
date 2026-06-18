# -*- coding: utf-8 -*-
"""
Enhance Moscow ``stories_ru`` / ``stories_en`` from legacy HTML in ``moscow/output/``.

Matches places by normalized Russian title (``name_ru``). No translation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_narrative import (
    _extract_english_lead,
    is_synthetic_tourist_story,
    text_for_edition,
)
from scripts.fetch_place_stories import MAX_STORY_CHARS, MIN_STORY_CHARS
from scripts.merge_moscow_guide_stories import finalize_story_editions

_OUTPUT_DIR = _PROJECT_ROOT / "moscow" / "output"
_PLACES_JSON = _PROJECT_ROOT / "moscow" / "data" / "moscow_places.json"

_HTML_GLOBS = (
    "Moscow_Complete_Guide.html",
    "Moscow_Complete_Guide_edit.html",
    "*_guide.html",
    "*_guide_opt.html",
    "html/*.html",
)

def _norm_name(name: str) -> str:
    s = unescape(name)
    s = re.sub(r"^\d+\.\s*", "", s)
    s = re.sub(r"[«»\"'„“”]", "", s)
    s = re.sub(r"\s+", " ", s).strip().lower()
    s = s.replace("ё", "е")
    return s


def _trim_story(text: str) -> str:
    s = re.sub(r"\s+", " ", unescape(text)).strip()
    if len(s) < MIN_STORY_CHARS:
        return ""
    if len(s) > MAX_STORY_CHARS:
        s = s[: MAX_STORY_CHARS - 3].rsplit(" ", 1)[0] + "..."
    return s


class _LegacyGuideParser(HTMLParser):
    """Extract place title + story-text from legacy monastery sections."""

    def __init__(self) -> None:
        super().__init__()
        self.stories: dict[str, str] = {}
        self._in_section = False
        self._in_title = False
        self._in_story = False
        self._title_buf: list[str] = []
        self._story_buf: list[str] = []
        self._current_title = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        cls = dict(attrs).get("class") or ""
        if tag == "section" and "monastery" in cls.split():
            self._in_section = True
            self._current_title = ""
            self._title_buf = []
            self._story_buf = []
            return
        if not self._in_section:
            return
        if tag == "h2" and "monastery-title" in cls.split():
            self._in_title = True
            self._title_buf = []
        elif tag == "p" and "story-text" in cls.split():
            self._in_story = True
            self._story_buf = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "section" and self._in_section:
            self._in_section = False
            return
        if tag == "h2" and self._in_title:
            self._in_title = False
            self._current_title = "".join(self._title_buf).strip()
        elif tag == "p" and self._in_story:
            self._in_story = False
            story = _trim_story("".join(self._story_buf))
            if self._current_title and story:
                key = _norm_name(self._current_title)
                prev = self.stories.get(key, "")
                if len(story) > len(prev):
                    self.stories[key] = story

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_buf.append(data)
        elif self._in_story:
            self._story_buf.append(data)


def _collect_html_paths(output_dir: Path) -> list[Path]:
    seen: set[Path] = set()
    ordered: list[Path] = []
    for pattern in _HTML_GLOBS:
        for path in sorted(output_dir.glob(pattern)):
            if not path.is_file():
                continue
            if path.name.startswith("moscow_guide"):
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            ordered.append(path)
    return ordered


def load_stories_from_output(output_dir: Path) -> dict[str, str]:
    merged: dict[str, str] = {}
    for path in _collect_html_paths(output_dir):
        parser = _LegacyGuideParser()
        try:
            parser.feed(path.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            continue
        for key, story in parser.stories.items():
            prev = merged.get(key, "")
            if len(story) > len(prev):
                merged[key] = story
    return merged


def _match_story(
    name_ru: str,
    lookup: dict[str, str],
) -> str:
    key = _norm_name(name_ru)
    if key in lookup:
        return lookup[key]
    for lk, story in lookup.items():
        if key.startswith(lk) or lk.startswith(key):
            if len(key) >= 8 and len(lk) >= 8:
                return story
    return ""


def _should_replace(current: str, candidate: str, edition: str) -> bool:
    if not candidate:
        return False
    if not current:
        return True
    if is_synthetic_tourist_story(current):
        return True
    return len(candidate) > len(current) + 20


def enhance_places(
    places_path: Path,
    output_dir: Path,
) -> dict[str, int]:
    lookup = load_stories_from_output(output_dir)
    rows: list[dict[str, Any]] = json.loads(
        places_path.read_text(encoding="utf-8"),
    )
    stats = {"lookup": len(lookup), "ru_updated": 0, "en_updated": 0}
    for row in rows:
        if not isinstance(row, dict):
            continue
        name = str(row.get("name_ru") or "").strip()
        if not name:
            continue
        story = _match_story(name, lookup)
        if not story:
            continue
        if text_for_edition(story, "ru"):
            edition = "ru"
        elif text_for_edition(story, "en"):
            edition = "en"
        else:
            lead = _extract_english_lead(story)
            if lead:
                edition = "en"
                story = lead
            else:
                edition = "ru"
        key = "stories_{}".format(edition)
        current = ""
        raw = row.get(key) or []
        if raw:
            current = str(raw[0]).strip()
        if _should_replace(current, story, edition):
            row[key] = [story]
            stats["{}_updated".format(edition)] += 1
    finalize_story_editions(rows)
    places_path.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return stats


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Enhance Moscow stories from moscow/output HTML.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=_OUTPUT_DIR,
    )
    parser.add_argument(
        "--places-json",
        type=Path,
        default=_PLACES_JSON,
    )
    args = parser.parse_args()
    stats = enhance_places(args.places_json, args.output_dir)
    print(
        "Legacy stories loaded: {} | RU updated: {} | EN updated: {}".format(
            stats["lookup"],
            stats["ru_updated"],
            stats["en_updated"],
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
