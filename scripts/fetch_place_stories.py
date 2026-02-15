# -*- coding: utf-8 -*-
"""
Fetch optional short stories per place from Wikipedia (round-robin en/ru).

Stories are historical or memorable snippets to help readers remember a place.
Writes data/<guide>_stories.py. Only adds a story when info is available.

Usage:
  python scripts/fetch_place_stories.py [--guide GUIDE] [--dry-run]

  --guide: only fetch for this guide (default: all).
  --dry-run: print what would be written, do not write files.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.core import ensure_utf8_console
from scripts.guide_loader import (
    GUIDES,
    load_places,
    _GUIDE_STORIES_VAR,
)

ensure_utf8_console()

USER_AGENT = "ExcursionGuide/1.0 (place stories)"
REQUEST_DELAY_SEC = 1.2
MAX_STORY_CHARS = 420
MIN_STORY_CHARS = 40


def _wikipedia_search(place_name: str, lang: str = "en") -> list[int]:
    """Return list of page IDs from Wikipedia search. lang: en or ru."""
    base = "https://en.wikipedia.org/w/api.php" if lang == "en" else (
        "https://ru.wikipedia.org/w/api.php"
    )
    city = "Moscow" if lang == "en" else "Москва"
    q = "{} {}".format(place_name, city)
    params = {
        "action": "query",
        "list": "search",
        "srsearch": q,
        "srlimit": 3,
        "format": "json",
    }
    url = "{}?{}".format(base, urllib.parse.urlencode(params))
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return []
    hits = data.get("query", {}).get("search") or []
    return [h["pageid"] for h in hits]


def _wikipedia_extract(page_id: int, lang: str = "en") -> str:
    """Get intro extract for a Wikipedia page. Returns plain text or empty."""
    base = "https://en.wikipedia.org/w/api.php" if lang == "en" else (
        "https://ru.wikipedia.org/w/api.php"
    )
    params = {
        "action": "query",
        "pageids": page_id,
        "prop": "extracts",
        "exintro": 1,
        "explaintext": 1,
        "exsentences": 5,
        "format": "json",
    }
    url = "{}?{}".format(base, urllib.parse.urlencode(params))
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return ""
    pages = data.get("query", {}).get("pages") or {}
    p = pages.get(str(page_id)) or {}
    return (p.get("extract") or "").strip()


def _pick_story_snippet(text: str) -> str:
    """
    Prefer a sentence with a year (historical); trim to MAX_STORY_CHARS.
    """
    if not text or len(text) < MIN_STORY_CHARS:
        return ""
    # Prefer sentence containing a 4-digit year
    year_match = re.search(r"[.!?]\s*[^.!?]*\b(19|20)\d{2}\b[^.!?]*[.!?]", text)
    if year_match:
        snippet = (year_match.group(0).strip() or "").lstrip(".!? \t")
        if MIN_STORY_CHARS <= len(snippet) <= MAX_STORY_CHARS:
            return snippet
        if len(snippet) > MAX_STORY_CHARS:
            return snippet[: MAX_STORY_CHARS - 3].rsplit(" ", 1)[0] + "..."
    # Else take first 1–2 sentences up to MAX_STORY_CHARS
    parts = re.split(r"(?<=[.!?])\s+", text)
    out: list[str] = []
    for p in parts:
        if len(" ".join(out + [p])) <= MAX_STORY_CHARS:
            out.append(p)
        else:
            break
    if not out:
        out = [text[:MAX_STORY_CHARS].rsplit(" ", 1)[0] + "..."]
    result = " ".join(out).strip()
    if len(result) < MIN_STORY_CHARS:
        return ""
    return result[:MAX_STORY_CHARS]


def _fetch_story_for_place(place_name: str) -> str:
    """
    Try Wikipedia en then ru (round-robin); return story snippet or empty.
    """
    for lang in ("en", "ru"):
        time.sleep(REQUEST_DELAY_SEC)
        page_ids = _wikipedia_search(place_name, lang=lang)
        for pid in page_ids:
            time.sleep(REQUEST_DELAY_SEC * 0.5)
            extract = _wikipedia_extract(pid, lang=lang)
            if extract:
                story = _pick_story_snippet(extract)
                if story:
                    return story
    return ""


def _write_stories_file(
    guide: str,
    stories: dict[str, str],
    dry_run: bool,
) -> None:
    """Write data/<guide>_stories.py with the stories dict."""
    if guide not in _GUIDE_STORIES_VAR:
        return
    var_name = _GUIDE_STORIES_VAR[guide]
    path = _PROJECT_ROOT / "data" / "{}_stories.py".format(guide)
    lines = [
        "# -*- coding: utf-8 -*-",
        '"""Optional short stories per place (Wikipedia)."""',
        "",
        "{}: dict[str, str] = {{".format(var_name),
    ]
    for k in sorted(stories.keys()):
        v = stories[k]
        k_esc = k.replace("\\", "\\\\").replace('"', '\\"')
        v_esc = v.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
        lines.append('    "{}": "{}",'.format(k_esc, v_esc))
    lines.append("}")
    lines.append("")
    content = "\n".join(lines) + "\n"
    if dry_run:
        print("[dry-run] {}: {} story(ies)".format(path.name, len(stories)))
        for name, story in sorted(stories.items()):
            print("  {}: {}...".format(name, (story[:50] + "…") if len(story) > 50 else story))
        return
    path.write_text(content, encoding="utf-8")
    print("Wrote {} ({} stories).".format(path, len(stories)))


def fetch_guide(guide: str, dry_run: bool) -> int:
    """Fetch stories for one guide. Returns number of stories found."""
    places = load_places(guide)
    stories: dict[str, str] = {}
    for place in places:
        name = (place.get("name") or "").strip()
        if not name:
            continue
        story = _fetch_story_for_place(name)
        if story:
            stories[name] = story
    _write_stories_file(guide, stories, dry_run)
    return len(stories)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch optional place stories from Wikipedia (en/ru).",
    )
    parser.add_argument(
        "--guide",
        type=str,
        default="",
        help="Only fetch this guide (default: all).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not write files.",
    )
    args = parser.parse_args()
    guides = [args.guide] if args.guide else GUIDES
    if args.guide and args.guide not in GUIDES:
        print("Unknown guide: {}.".format(args.guide), file=sys.stderr)
        return 1
    total = 0
    for g in guides:
        n = fetch_guide(g, args.dry_run)
        total += n
    print("Total: {} story(ies).".format(total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
