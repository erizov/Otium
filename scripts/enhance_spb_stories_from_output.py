# -*- coding: utf-8 -*-
"""
Enhance SPB ``stories_ru`` / ``stories_en`` from HTML in ``spb/output/``.

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

from scripts.city_guide_narrative import _extract_english_lead, text_for_edition
from scripts.fetch_place_stories import MAX_STORY_CHARS, MIN_STORY_CHARS
from scripts.city_guide_narrative import is_synthetic_tourist_story
from scripts.merge_moscow_guide_stories import finalize_story_editions

_OUTPUT_DIR = _PROJECT_ROOT / "spb" / "output"
_DATA_DIR = _PROJECT_ROOT / "spb" / "data"
_PLACE_FILES = (
    "spb_places.json",
    "spb_places_more.json",
    "spb_places_expansion_m2026.json",
    "spb_places_pdf_size_expand.json",
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


class _SpbGuideParser(HTMLParser):
    """Extract place title + story from ``section.place`` blocks."""

    def __init__(self) -> None:
        super().__init__()
        self.stories: dict[str, str] = {}
        self._in_place = False
        self._in_h3 = False
        self._in_stories = False
        self._in_li = False
        self._title_buf: list[str] = []
        self._story_buf: list[str] = []
        self._current_title = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        cls = dict(attrs).get("class") or ""
        if tag == "section" and "place" in cls.split():
            self._in_place = True
            self._current_title = ""
            self._title_buf = []
            return
        if not self._in_place:
            return
        if tag == "h3":
            self._in_h3 = True
            self._title_buf = []
        elif tag == "ul" and "stories" in cls.split():
            self._in_stories = True
        elif tag == "li" and self._in_stories:
            self._in_li = True
            self._story_buf = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "section" and self._in_place:
            self._in_place = False
            return
        if tag == "h3" and self._in_h3:
            self._in_h3 = False
            self._current_title = "".join(self._title_buf).strip()
        elif tag == "ul" and self._in_stories:
            self._in_stories = False
        elif tag == "li" and self._in_li:
            self._in_li = False
            story = _trim_story("".join(self._story_buf))
            if self._current_title and story:
                key = _norm_name(self._current_title)
                prev = self.stories.get(key, "")
                if len(story) > len(prev):
                    self.stories[key] = story

    def handle_data(self, data: str) -> None:
        if self._in_h3:
            self._title_buf.append(data)
        elif self._in_li:
            self._story_buf.append(data)


def _collect_html_paths(output_dir: Path) -> list[Path]:
    ordered: list[Path] = []
    seen: set[Path] = set()
    for name in ("spb_guide_ru.html", "spb_guide_en.html", "spb_guide.html"):
        path = output_dir / name
        if path.is_file():
            resolved = path.resolve()
            if resolved not in seen:
                seen.add(resolved)
                ordered.append(path)
    return ordered


def load_stories_from_output(output_dir: Path) -> dict[str, str]:
    merged: dict[str, str] = {}
    for path in _collect_html_paths(output_dir):
        parser = _SpbGuideParser()
        try:
            parser.feed(path.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            continue
        for key, story in parser.stories.items():
            prev = merged.get(key, "")
            if len(story) > len(prev):
                merged[key] = story
    return merged


def _match_story(name_ru: str, lookup: dict[str, str]) -> str:
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


def _load_all_rows(data_dir: Path) -> list[tuple[Path, list[dict[str, Any]]]]:
    loaded: list[tuple[Path, list[dict[str, Any]]]] = []
    for name in _PLACE_FILES:
        path = data_dir / name
        if not path.is_file():
            continue
        rows: list[dict[str, Any]] = json.loads(
            path.read_text(encoding="utf-8"),
        )
        loaded.append((path, rows))
    return loaded


def enhance_places(
    data_dir: Path,
    output_dir: Path,
) -> dict[str, int]:
    lookup = load_stories_from_output(output_dir)
    stats = {"lookup": len(lookup), "ru_updated": 0, "en_updated": 0}
    for path, rows in _load_all_rows(data_dir):
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
            current = str((row.get(key) or [""])[0]).strip()
            if _should_replace(current, story, edition):
                row[key] = [story]
                if edition == "ru":
                    stats["ru_updated"] += 1
                else:
                    stats["en_updated"] += 1
        finalize_story_editions(rows)
        path.write_text(
            json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return stats


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Enhance SPB stories from spb/output HTML.",
    )
    parser.add_argument("--data-dir", type=Path, default=_DATA_DIR)
    parser.add_argument("--output-dir", type=Path, default=_OUTPUT_DIR)
    args = parser.parse_args()
    stats = enhance_places(args.data_dir, args.output_dir)
    print(
        "Enhanced from {} HTML stories (ru: {}, en: {})".format(
            stats["lookup"],
            stats["ru_updated"],
            stats["en_updated"],
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
