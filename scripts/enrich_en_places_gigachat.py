# -*- coding: utf-8 -*-
"""
Fill sparse English place narratives via GigaChat (EN fields only).

Targets rows with an English title (``name_en`` or Latin ``name``) and no
substantive English body (``description`` / ``history`` / ``significance`` /
``facts`` / ``stories``). Writes original English prose — not a translation.

Requires ``GIGA_AUTH_KEY`` in ``.env``.

Usage:
  python scripts/enrich_en_places_gigachat.py --dry-run --limit 3
  python scripts/enrich_en_places_gigachat.py --cities berlin --delay 2
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_core import is_substantive_text
from scripts.enrich_places_gigachat_common import (
    discover_cities,
    extract_json,
    field_is_stub,
    gigachat_failed,
    has_cyrillic,
    is_english_narrative,
    load_dotenv,
)
from scripts.gigachat_client import ask_gigachat

_GENERIC_FACT_STUBS = frozenset(
    {
        "check opening hours and ticketing on official sites before travel.",
        "crowds peak on weekends and public holidays.",
    },
)


def _english_place_name(place: dict[str, Any]) -> str:
    for key in ("name_en", "name"):
        value = str(place.get(key) or "").strip()
        if value and not has_cyrillic(value):
            return value
    return ""


def _fact_is_generic(fact: str) -> bool:
    return str(fact).strip().lower() in _GENERIC_FACT_STUBS


def _has_english_narrative(place: dict[str, Any]) -> bool:
    for key in ("description", "history", "significance"):
        if is_english_narrative(place.get(key)):
            return True
    for key in ("facts", "stories"):
        for item in place.get(key) or []:
            text = str(item).strip()
            if not is_substantive_text(text):
                continue
            if _fact_is_generic(text):
                continue
            if is_english_narrative(text):
                return True
    return False


def place_needs_en_narrative(place: dict[str, Any]) -> bool:
    """English edition row: Latin title, no real English narrative yet."""
    if not _english_place_name(place):
        return False
    return not _has_english_narrative(place)


def _field_needs_en_write(field: str | None) -> bool:
    if field_is_stub(field):
        return True
    text = str(field or "").strip()
    if text and has_cyrillic(text):
        return True
    return False


def _build_prompt(place: dict[str, Any], city_slug: str) -> str:
    name = _english_place_name(place)
    city_title = city_slug.replace("_", " ").title()
    lines = [
        "You edit an English-language city guide ({}, {}).".format(
            city_title, city_slug,
        ),
        'Write original English copy about "{}".'.format(name),
        "",
        "Known metadata (use if accurate; do not invent beyond this):",
    ]
    for label, key in (
        ("Address", "address"),
        ("Year / period", "year_built"),
        ("Style", "architecture_style"),
        ("Category", "category"),
    ):
        val = str(place.get(key) or "").strip()
        if val and not has_cyrillic(val):
            lines.append("- {}: {}".format(label, val))
        elif val and key in ("year_built", "architecture_style"):
            lines.append("- {}: (see place; write in English)".format(label))
    url = str(place.get("culture_ru_url") or place.get("source_url") or "").strip()
    if url:
        lines.append("- Reference URL: {}".format(url))
    lines.extend(
        [
            "",
            "Rules:",
            "- Write in English only.",
            "- Do NOT translate from Russian or any other language.",
            "- Write fresh guidebook prose from established public facts.",
            "- Do not invent dates, names, or events.",
            "- If you lack reliable facts, return skip.",
            "",
            "Return ONLY JSON (no markdown):",
            "{",
            '  "skip": false,',
            '  "description": "optional 1 short overview paragraph",',
            '  "history": "1–2 human paragraphs: history, role, memorable facts",',
            '  "significance": "one short sentence — why visit",',
            '  "facts": ["3–5 short bullet facts, no repeats from history"],',
            '  "year_built": "year or period in English, or empty string",',
            '  "architecture_style": "style in English, or empty string"',
            "}",
            "",
            'If insufficient reliable facts: {"skip": true, "reason": "brief"}.',
            "No bullet lists inside history or description.",
        ],
    )
    return "\n".join(lines)


def _apply_enrichment(place: dict[str, Any], data: dict[str, Any]) -> bool:
    if data.get("skip"):
        return False
    changed = False

    description = str(data.get("description") or "").strip()
    if description and is_english_narrative(description):
        if _field_needs_en_write(place.get("description")):
            place["description"] = description
            changed = True

    history = str(data.get("history") or "").strip()
    if history and is_english_narrative(history):
        if _field_needs_en_write(place.get("history")):
            place["history"] = history
            changed = True

    significance = str(data.get("significance") or "").strip()
    if significance and is_english_narrative(significance):
        if _field_needs_en_write(place.get("significance")):
            place["significance"] = significance
            changed = True

    facts_in = data.get("facts")
    if isinstance(facts_in, list):
        facts = [
            str(x).strip()
            for x in facts_in
            if is_english_narrative(str(x)) and not _fact_is_generic(str(x))
        ]
        existing = place.get("facts") or []
        has_real_en = any(
            is_english_narrative(str(x)) and not _fact_is_generic(str(x))
            for x in existing
        )
        if facts and not has_real_en:
            place["facts"] = facts[:6]
            changed = True

    year = str(data.get("year_built") or "").strip()
    if year and is_english_narrative(year):
        if _field_needs_en_write(place.get("year_built")):
            place["year_built"] = year
            changed = True

    style = str(data.get("architecture_style") or "").strip()
    if style and is_english_narrative(style):
        if _field_needs_en_write(place.get("architecture_style")):
            place["architecture_style"] = style
            changed = True

    return changed


def _process_city(
    city_slug: str,
    *,
    dry_run: bool,
    limit: int | None,
    delay: float,
    model: str,
) -> tuple[int, int, int]:
    path = _PROJECT_ROOT / city_slug / "data" / "{}_places.json".format(
        city_slug,
    )
    places: list[dict[str, Any]] = json.loads(
        path.read_text(encoding="utf-8"),
    )
    targets = [p for p in places if place_needs_en_narrative(p)]
    if limit is not None:
        targets = targets[:limit]

    updated = skipped = errors = 0
    for place in targets:
        slug = str(place.get("slug") or "?")
        name = _english_place_name(place)
        if dry_run:
            print("[dry-run] {} / {} — {}".format(city_slug, slug, name))
            continue

        raw = ask_gigachat(_build_prompt(place, city_slug), model=model)
        if gigachat_failed(raw):
            print("{} / {}: {}".format(city_slug, slug, raw), file=sys.stderr)
            errors += 1
            if delay > 0:
                time.sleep(delay)
            continue

        parsed = extract_json(raw)
        if not parsed:
            print(
                "{} / {}: cannot parse JSON".format(city_slug, slug),
                file=sys.stderr,
            )
            errors += 1
            if delay > 0:
                time.sleep(delay)
            continue

        if parsed.get("skip"):
            reason = str(parsed.get("reason") or "no data").strip()
            print("{} / {}: skip ({})".format(city_slug, slug, reason))
            skipped += 1
        elif _apply_enrichment(place, parsed):
            print("{} / {}: updated".format(city_slug, slug))
            updated += 1
        else:
            print("{} / {}: no changes".format(city_slug, slug))
            skipped += 1

        if delay > 0:
            time.sleep(delay)

    if not dry_run and updated:
        path.write_text(
            json.dumps(places, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print("Written", path)

    return updated, skipped, errors


def main() -> int:
    load_dotenv(_PROJECT_ROOT)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cities",
        nargs="+",
        metavar="SLUG",
        help="City slug(s); default: all cities with sparse EN rows.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        metavar="N",
        help="Max places per city (for testing).",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        metavar="SEC",
        help="Pause between API calls (default 2.0).",
    )
    parser.add_argument(
        "--model",
        default="GigaChat",
        help="GigaChat model name (default GigaChat).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List targets only; no API calls.",
    )
    args = parser.parse_args()

    cities = discover_cities(_PROJECT_ROOT, args.cities)
    total_up = total_sk = total_err = 0

    for city_slug in cities:
        path = _PROJECT_ROOT / city_slug / "data" / "{}_places.json".format(
            city_slug,
        )
        places = json.loads(path.read_text(encoding="utf-8"))
        n = sum(1 for p in places if place_needs_en_narrative(p))
        if not n:
            continue
        print("\n=== {} ({} need EN) ===".format(city_slug, n))
        up, sk, err = _process_city(
            city_slug,
            dry_run=args.dry_run,
            limit=args.limit,
            delay=args.delay,
            model=args.model,
        )
        total_up += up
        total_sk += sk
        total_err += err

    print(
        "\nDone: {} updated, {} skipped, {} errors.".format(
            total_up, total_sk, total_err,
        ),
    )
    return 1 if total_err else 0


if __name__ == "__main__":
    raise SystemExit(main())
