# -*- coding: utf-8 -*-
"""Report missing names/narratives per guide edition."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_narrative import (
    GuideNarrativeDeduper,
    merge_narrative_html,
    place_heading_plain,
    polish_display_title,
)
from scripts.city_guide_sparse_narrative import (
    _json_has_usable_narrative_for_edition,
    place_edition_needs_fill,
)
from scripts.city_guide_translate import get_edition_translator


def _discover_cities(root: Path) -> list[str]:
    out: list[str] = []
    for path in sorted(root.glob("*/data/*_places.json")):
        out.append(path.parent.parent.name)
    return out


def _is_slug_title(title: str) -> bool:
    return bool(re.fullmatch(r"[a-z0-9_]+", title))


def _has_source(place: dict, edition: str) -> bool:
    if edition == "ru":
        keys = (
            "description_ru",
            "history_ru",
            "significance_ru",
            "description",
            "history",
            "significance",
        )
    else:
        keys = (
            "description_en",
            "history_en",
            "significance_en",
            "description",
            "history",
            "significance",
        )
    for key in keys:
        val = str(place.get(key) or "").strip()
        if len(val) >= 40:
            return True
    facts_key = "facts_ru" if edition == "ru" else "facts"
    facts = place.get(facts_key) or place.get("facts") or []
    return any(len(str(x).strip()) >= 20 for x in facts)


def _ru_title_is_slug(place: dict) -> bool:
    for key in ("name_ru", "name"):
        val = polish_display_title(str(place.get(key) or ""))
        if val and _is_slug_title(val):
            return True
    return False


def _audit_places_fast(places: list[dict]) -> dict[str, int]:
    """JSON-only scan — no merge/translate (instant)."""
    stats = {
        "places": len(places),
        "ru_slug_title": 0,
        "ru_empty_narr": 0,
        "en_empty_narr": 0,
        "ru_missing_src": 0,
        "en_missing_src": 0,
        "cross_fill_ru": 0,
        "cross_fill_en": 0,
    }
    for place in places:
        if _ru_title_is_slug(place):
            stats["ru_slug_title"] += 1
        ru_empty = place_edition_needs_fill(place, "ru")
        en_empty = place_edition_needs_fill(place, "en")
        if ru_empty:
            stats["ru_empty_narr"] += 1
        if en_empty:
            stats["en_empty_narr"] += 1
        if not _has_source(place, "ru"):
            stats["ru_missing_src"] += 1
        if not _has_source(place, "en"):
            stats["en_missing_src"] += 1
        if ru_empty and _json_has_usable_narrative_for_edition(place, "en"):
            stats["cross_fill_ru"] += 1
        if en_empty and _json_has_usable_narrative_for_edition(place, "ru"):
            stats["cross_fill_en"] += 1
    return stats


def audit_places(
    places: list[dict],
    *,
    use_translate: bool,
) -> dict[str, int]:
    if not use_translate:
        return _audit_places_fast(places)

    stats = {
        "places": len(places),
        "ru_slug_title": 0,
        "ru_empty_narr": 0,
        "en_empty_narr": 0,
        "ru_missing_src": 0,
        "en_missing_src": 0,
        "cross_fill_ru": 0,
        "cross_fill_en": 0,
    }
    tr = get_edition_translator()
    for place in places:
        deduper = GuideNarrativeDeduper()
        ru_title = place_heading_plain(place, "ru", translator=tr)
        if _is_slug_title(ru_title):
            stats["ru_slug_title"] += 1
        ru_html = merge_narrative_html(place, "ru", deduper)
        deduper = GuideNarrativeDeduper()
        en_html = merge_narrative_html(place, "en", deduper)
        if not ru_html:
            stats["ru_empty_narr"] += 1
        if not en_html:
            stats["en_empty_narr"] += 1
        if not _has_source(place, "ru"):
            stats["ru_missing_src"] += 1
        if not _has_source(place, "en"):
            stats["en_missing_src"] += 1
        if not ru_html and _has_source(place, "en"):
            stats["cross_fill_ru"] += 1
        if not en_html and _has_source(place, "ru"):
            stats["cross_fill_en"] += 1
    return stats


def audit_city(root: Path, city_slug: str, *, use_translate: bool) -> dict[str, int]:
    from scripts.city_guide_registry_common import pdf_expand_sidecar_paths

    data_dir = root / city_slug / "data"
    paths: list[Path] = []
    main = data_dir / "{}_places.json".format(city_slug)
    if main.is_file():
        paths.append(main)
    paths.extend(pdf_expand_sidecar_paths(data_dir, city_slug))
    places: list[dict] = []
    for path in paths:
        raw = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(raw, list):
            places.extend(raw)
    return audit_places(places, use_translate=use_translate)


def format_audit_line(city_slug: str, stats: dict[str, int]) -> str:
    return (
        "{:16} places {:4}  RU slug titles {:4}  "
        "empty RU narr {:4}  empty EN narr {:4}  "
        "need EN->RU {:4}  need RU->EN {:4}".format(
            city_slug,
            stats["places"],
            stats["ru_slug_title"],
            stats["ru_empty_narr"],
            stats["en_empty_narr"],
            stats["cross_fill_ru"],
            stats["cross_fill_en"],
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cities",
        "--city",
        dest="cities",
        action="append",
        default=[],
        metavar="SLUG",
        help="City slug(s); default: all cities with places JSON.",
    )
    parser.add_argument(
        "--with-translate",
        action="store_true",
        help=(
            "Merge narratives with live translation like PDF build "
            "(slow; default is fast JSON-only scan)."
        ),
    )
    args = parser.parse_args()
    cities = args.cities or _discover_cities(_PROJECT_ROOT)
    totals = {
        "places": 0,
        "ru_slug_title": 0,
        "ru_empty_narr": 0,
        "en_empty_narr": 0,
        "ru_missing_src": 0,
        "en_missing_src": 0,
        "cross_fill_ru": 0,
        "cross_fill_en": 0,
    }
    tr = get_edition_translator() if args.with_translate else None
    print(
        "Mode: {}".format(
            "rendered HTML + translator"
            if args.with_translate
            else "fast JSON fields (no translate)",
        ),
        flush=True,
    )
    if args.with_translate:
        print(
            "Translator: {}".format(
                "enabled" if tr is not None else "unavailable",
            ),
            flush=True,
        )
    for city in cities:
        print("Auditing {}…".format(city), flush=True)
        stats = audit_city(_PROJECT_ROOT, city, use_translate=args.with_translate)
        for key in totals:
            totals[key] += stats[key]
        print(format_audit_line(city, stats), flush=True)
    print("--- totals ---", flush=True)
    print(json.dumps(totals, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
