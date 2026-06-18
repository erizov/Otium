# -*- coding: utf-8 -*-
"""Bake EN narrative fields for Moscow places (parity with RU source data)."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_core import is_substantive_text, places_for_pdf
from scripts.city_guide_narrative import (
    _extract_english_lead,
    text_for_edition,
)
from scripts.city_guide_translate import (
    EditionTranslator,
    get_edition_translator,
    set_edition_translator,
    translate_for_edition,
)
from scripts.city_guide_naming import title_from_place_slug
from scripts.merge_moscow_guide_stories import _fill_missing_edition


def _english_wikipedia_queries(row: dict[str, Any]) -> list[str]:
    queries: list[str] = []
    seen: set[str] = set()

    def add(q: str) -> None:
        s = " ".join(str(q).split()).strip()
        if len(s) < 4 or s.lower() in seen:
            return
        seen.add(s.lower())
        queries.append(s)

    for key in ("name_en",):
        add(str(row.get(key) or ""))

    slug = str(row.get("slug") or "").strip()
    if slug:
        add(title_from_place_slug(slug))

    rel = str(row.get("image_rel_path") or "")
    stem = Path(rel).stem if rel else ""
    if stem:
        base = re.sub(r"_\d+$", "", stem)
        base = base.replace("_", " ").strip()
        if base:
            add("{} Moscow".format(base.title()))
            add("{} monument Moscow".format(base.title()))

    name_ru = str(row.get("name_ru") or row.get("name") or "").strip()
    if name_ru.lower().startswith("памятник "):
        subject = name_ru[len("Памятник ") :].strip()
        add("Monument to {}".format(subject))
        add("{} monument Moscow".format(subject))

    add(name_ru)
    return queries


def _wikipedia_en_history(row: dict[str, Any]) -> str | None:
    from scripts.fetch_place_stories import fetch_story_for_place_lang

    for query in _english_wikipedia_queries(row):
        story = fetch_story_for_place_lang(query, "en")
        if story and text_for_edition(story, "en"):
            return story
    return None


_BAD_EN_PLACE_NAME_RE = re.compile(
    r"^(?:list of|battle of|make way for ducklings|moscow theater hostage|"
    r"animal farm|antilia|2018 moscow|schism|presnensky district|"
    r"sculpture and architecture)",
    re.IGNORECASE,
)


def _is_bad_english_place_name(name: str) -> bool:
    s = str(name or "").strip()
    if not s:
        return True
    if s.lower() == "moscow":
        return True
    return bool(_BAD_EN_PLACE_NAME_RE.match(s))


def _english_wikipedia_name(row: dict[str, Any]) -> str | None:
    from scripts.fetch_place_stories import (
        fetch_english_title_via_russian_page,
        fetch_wikipedia_page_title,
    )

    name_ru = str(row.get("name_ru") or row.get("name") or "").strip()
    if name_ru:
        via_ru = fetch_english_title_via_russian_page(name_ru)
        if (
            via_ru
            and text_for_edition(via_ru, "en")
            and not _is_bad_english_place_name(via_ru)
        ):
            return via_ru
    for query in _english_wikipedia_queries(row)[:4]:
        title = fetch_wikipedia_page_title(query, "en", city_suffix="Moscow")
        if (
            title
            and text_for_edition(title, "en")
            and not _is_bad_english_place_name(title)
        ):
            return title
    return None


def _translate_field(
    text: str,
    *,
    kind: str,
    tr: Any,
) -> str | None:
    raw = str(text or "").strip()
    if not is_substantive_text(raw):
        return None
    if text_for_edition(raw, "en"):
        return raw
    return translate_for_edition(raw, "en", kind=kind, translator=tr)


def _english_story_fallback(row: dict[str, Any]) -> str | None:
    items = row.get("stories_en") or []
    if not items:
        return None
    raw = str(items[0]).strip()
    if text_for_edition(raw, "en"):
        return raw
    lead = _extract_english_lead(raw)
    return lead if is_substantive_text(lead) else None


def _reconcile_place(
    row: dict[str, Any],
    tr: Any,
    *,
    cache_only: bool = False,
    fetch_wikipedia: bool = False,
) -> bool:
    changed = False
    name_ru = str(row.get("name_ru") or row.get("name") or "").strip()
    if name_ru and not str(row.get("name_en") or "").strip():
        name_en = _translate_field(name_ru, kind="name", tr=tr)
        if name_en:
            row["name_en"] = name_en
            changed = True

    for base in ("history", "significance"):
        src = str(row.get(base) or "").strip()
        en_key = "{}_en".format(base)
        if src and not str(row.get(en_key) or "").strip():
            translated = _translate_field(src, kind="prose", tr=tr)
            if translated:
                row[en_key] = translated
                changed = True

    if not str(row.get("history_en") or "").strip():
        story_en = _english_story_fallback(row)
        if story_en:
            row["history_en"] = story_en
            changed = True

    if (
        fetch_wikipedia
        and not str(row.get("history_en") or "").strip()
        and is_substantive_text(str(row.get("history") or ""))
    ):
        wiki = _wikipedia_en_history(row)
        if wiki:
            row["history_en"] = wiki
            if not row.get("stories_en"):
                row["stories_en"] = [wiki]
            changed = True

    facts = row.get("facts") or []
    if isinstance(facts, list) and facts and not row.get("facts_en"):
        en_facts: list[str] = []
        for item in facts:
            translated = _translate_field(str(item), kind="prose", tr=tr)
            if translated:
                en_facts.append(translated)
        if en_facts:
            row["facts_en"] = en_facts
            changed = True

    style = str(row.get("architecture_style") or "").strip()
    if style and not str(row.get("architecture_style_en") or "").strip():
        style_en = _translate_field(style, kind="prose", tr=tr)
        if style_en:
            row["architecture_style_en"] = style_en
            changed = True

    if not cache_only:
        for edition in ("ru", "en"):
            key = "stories_{}".format(edition)
            items = row.get(key) or []
            if items and str(items[0]).strip():
                continue
            filled = _fill_missing_edition(row, edition, bilingual=True)
            if filled:
                row[key] = [filled]
                changed = True

    return changed


def reconcile_moscow_places_json(
    places_path: Path,
    project_root: Path | None = None,
    *,
    dry_run: bool = False,
    cache_only: bool = False,
    fetch_wikipedia: bool = False,
    pdf_only: bool = False,
) -> tuple[int, int]:
    """
    Fill missing EN fields from RU narrative in ``moscow_places.json``.

    Returns ``(places_updated, places_total)``.
    """
    tr = get_edition_translator(project_root)
    if tr is None:
        print(
            "Moscow EN reconcile skipped: translator unavailable "
            "(unset CITY_GUIDE_NO_TRANSLATE and configure Ollama/.env).",
            file=sys.stderr,
        )
        return 0, 0
    if cache_only:
        tr = EditionTranslator(
            project_root=project_root,
            cache_path=tr._cache_file,
            cache_only=True,
        )
        set_edition_translator(tr)

    path = places_path.resolve()
    rows: list[dict[str, Any]] = json.loads(path.read_text(encoding="utf-8"))
    pdf_slugs: set[str] | None = None
    if pdf_only and project_root is not None:
        city_root = project_root / "moscow"
        pdf_slugs = {
            str(p.get("slug") or "")
            for p in places_for_pdf(city_root, rows, city_slug="moscow")
        }
    updated = 0
    for row in rows:
        slug = str(row.get("slug") or "")
        wiki_ok = fetch_wikipedia and (
            not pdf_only or pdf_slugs is None or slug in pdf_slugs
        )
        if _reconcile_place(
            row,
            tr,
            cache_only=cache_only,
            fetch_wikipedia=wiki_ok,
        ):
            updated += 1
    if updated and not dry_run:
        path.write_text(
            json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return updated, len(rows)


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--places",
        type=Path,
        default=_PROJECT_ROOT / "moscow" / "data" / "moscow_places.json",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--cache-only",
        action="store_true",
        help="Use translation cache only (no Ollama/OpenAI calls).",
    )
    parser.add_argument(
        "--fetch-wikipedia",
        action="store_true",
        help="Fetch EN Wikipedia intros for places still missing history_en.",
    )
    parser.add_argument(
        "--pdf-only",
        action="store_true",
        help="With --fetch-wikipedia, only fill PDF-eligible places.",
    )
    args = parser.parse_args()
    updated, total = reconcile_moscow_places_json(
        args.places,
        _PROJECT_ROOT,
        dry_run=args.dry_run,
        cache_only=args.cache_only,
        fetch_wikipedia=args.fetch_wikipedia,
        pdf_only=args.pdf_only,
    )
    print("Updated {}/{} places in {}".format(updated, total, args.places))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
