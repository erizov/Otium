# -*- coding: utf-8 -*-
"""
Fill sparse Russian place narratives via GigaChat (RU fields only).

Targets rows in ``<city>/data/<city>_places.json`` that have a name but no
substantive ``history`` / ``significance`` / ``facts`` / ``stories``.

Requires ``GIGA_AUTH_KEY`` in ``.env`` (project root).

Usage:
  python scripts/enrich_ru_places_gigachat.py --dry-run --limit 3
  python scripts/enrich_ru_places_gigachat.py --cities moscow --delay 2
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
from scripts.city_guide_registry_common import pdf_expand_sidecar_paths
from scripts.enrich_places_gigachat_common import (
    discover_cities,
    extract_json,
    gigachat_failed,
    gigachat_refusal,
    load_dotenv,
)
from scripts.gigachat_client import ask_gigachat

_CULTURE_RU_STUB = "Архитектурный объект из каталога"


def _load_dotenv() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    load_dotenv(_PROJECT_ROOT / ".env")


def _place_display_name(place: dict[str, Any]) -> str:
    for key in ("name_ru", "name", "name_en"):
        value = str(place.get(key) or "").strip()
        if value:
            return value
    return str(place.get("slug") or "?")


def _field_is_stub(field: str | None) -> bool:
    if not field:
        return True
    text = str(field).strip()
    if not text:
        return True
    if _CULTURE_RU_STUB in text:
        return True
    from scripts.city_guide_narrative import is_landmark_boilerplate

    if is_landmark_boilerplate(text):
        return True
    return not is_substantive_text(text)


def place_needs_ru_narrative(place: dict[str, Any]) -> bool:
    """True when the row has a title but no real RU narrative body."""
    if not _place_display_name(place) or _place_display_name(place) == "?":
        return False
    if not _field_is_stub(place.get("history")):
        return False
    if not _field_is_stub(place.get("significance")):
        return False
    if not _field_is_stub(place.get("description")):
        return False
    facts = place.get("facts") or []
    if any(is_substantive_text(str(x)) for x in facts):
        return False
    stories = place.get("stories") or []
    if any(is_substantive_text(str(x)) for x in stories):
        return False
    return True


def _load_place_details(city_slug: str) -> dict[str, Any]:
    path = _PROJECT_ROOT / city_slug / "data" / "{}_place_details.json".format(
        city_slug,
    )
    if not path.is_file():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        return raw if isinstance(raw, dict) else {}
    except json.JSONDecodeError:
        return {}


def _build_prompt(
    place: dict[str, Any],
    city_slug: str,
    details: dict[str, Any] | None = None,
) -> str:
    name = _place_display_name(place)
    lines = [
        "Ты редактор русскоязычного путеводителя ({}).".format(city_slug),
        "Напиши достоверный текст об объекте «{}».".format(name),
        "",
        "Уже известно (не повторяй дословно, не выдумывай нового):",
    ]
    for label, key in (
        ("Адрес", "address"),
        ("Год / период", "year_built"),
        ("Стиль", "architecture_style"),
        ("Категория", "category"),
    ):
        val = str(place.get(key) or "").strip()
        if val:
            lines.append("- {}: {}".format(label, val))
    url = str(place.get("culture_ru_url") or "").strip()
    if url:
        lines.append("- Источник: {}".format(url))
    if details:
        for label, key in (
            ("Описание (справка)", "description"),
            ("История (справка)", "history"),
            ("Значение (справка)", "significance"),
        ):
            val = str(details.get(key) or "").strip()
            if val:
                lines.append("- {}: {}".format(label, val[:400]))
        dfacts = details.get("facts")
        if isinstance(dfacts, list):
            for fact in dfacts[:4]:
                val = str(fact).strip()
                if val:
                    lines.append("- Факт (справка): {}".format(val[:200]))
    lines.extend(
        [
            "",
            "Верни ТОЛЬКО JSON без markdown:",
            "{",
            '  "skip": false,',
            '  "history": "1–2 абзаца живым языком: история, роль, '
            "запоминающиеся факты\",",
            '  "significance": "одно короткое предложение — зачем идти",',
            '  "facts": ["3–5 коротких фактов без повторов из history"],',
            '  "year_built": "год или период, если известен, иначе пустая строка",',
            '  "architecture_style": "стиль, если известен, иначе пустая строка"',
            "}",
            "",
            "Если достоверных сведений нет — "
            '{"skip": true, "reason": "кратко почему"}.',
            "Не выдумывай даты, имена и события. Без списков в history.",
        ],
    )
    return "\n".join(lines)


def _apply_enrichment(
    place: dict[str, Any],
    data: dict[str, Any],
) -> bool:
    if data.get("skip"):
        return False
    changed = False

    description = str(data.get("description") or "").strip()
    if description and not _field_is_stub(description):
        if _field_is_stub(place.get("description_ru")):
            place["description_ru"] = description
            changed = True
        elif _field_is_stub(place.get("description")):
            place["description"] = description
            changed = True

    history = str(data.get("history") or "").strip()
    if history and not _field_is_stub(history):
        if _field_is_stub(place.get("history_ru")):
            place["history_ru"] = history
            changed = True
        elif _field_is_stub(place.get("history")):
            place["history"] = history
            changed = True

    significance = str(data.get("significance") or "").strip()
    if significance and not _field_is_stub(significance):
        if _field_is_stub(place.get("significance_ru")):
            place["significance_ru"] = significance
            changed = True
        elif _field_is_stub(place.get("significance")):
            place["significance"] = significance
            changed = True

    facts_in = data.get("facts")
    if isinstance(facts_in, list):
        facts = [
            str(x).strip() for x in facts_in if is_substantive_text(str(x))
        ]
        existing_ru = place.get("facts_ru") or []
        existing = place.get("facts") or []
        has_ru = any(is_substantive_text(str(x)) for x in existing_ru)
        has_any = any(is_substantive_text(str(x)) for x in existing)
        if facts and not has_ru:
            place["facts_ru"] = facts[:6]
            changed = True
        elif facts and not has_any:
            place["facts"] = facts[:6]
            changed = True

    year = str(data.get("year_built") or "").strip()
    if year and not _field_is_stub(year):
        if _field_is_stub(place.get("year_built")):
            place["year_built"] = year
            changed = True

    style = str(data.get("architecture_style") or "").strip()
    if style and not _field_is_stub(style):
        if _field_is_stub(place.get("architecture_style_ru")):
            place["architecture_style_ru"] = style
            changed = True
        elif _field_is_stub(place.get("architecture_style")):
            place["architecture_style"] = style
            changed = True

    return changed


def _discover_cities(selected: list[str] | None) -> list[str]:
    if selected:
        return selected
    out: list[str] = []
    for child in sorted(_PROJECT_ROOT.iterdir()):
        if not child.is_dir():
            continue
        slug = child.name
        if (child / "data" / "{}_places.json".format(slug)).is_file():
            out.append(slug)
    return out


def _place_json_paths(data_dir: Path, city_slug: str) -> list[Path]:
    paths: list[Path] = []
    main = data_dir / "{}_places.json".format(city_slug)
    if main.is_file():
        paths.append(main)
    if city_slug == "spb":
        for more_name in (
            "spb_places_more.json",
            "spb_places_expansion_m2026.json",
            "spb_places_osobnjaki.json",
        ):
            more = data_dir / more_name
            if more.is_file():
                paths.append(more)
    paths.extend(pdf_expand_sidecar_paths(data_dir, city_slug))
    return paths


def _process_city(
    city_slug: str,
    *,
    dry_run: bool,
    limit: int | None,
    delay: float,
    model: str,
) -> tuple[int, int, int]:
    data_dir = _PROJECT_ROOT / city_slug / "data"
    paths = _place_json_paths(data_dir, city_slug)
    if not paths:
        return 0, 0, 0

    details_map = _load_place_details(city_slug)
    updated = skipped = errors = 0
    remaining = limit

    for path in paths:
        places: list[dict[str, Any]] = json.loads(
            path.read_text(encoding="utf-8"),
        )
        targets = [p for p in places if place_needs_ru_narrative(p)]
        if remaining is not None:
            targets = targets[:remaining]
            remaining = max(0, (remaining or 0) - len(targets))

        file_updated = 0
        for place in targets:
            slug = str(place.get("slug") or "?")
            name = _place_display_name(place)
            detail = details_map.get(slug)
            detail_dict = detail if isinstance(detail, dict) else None
            prompt = _build_prompt(place, city_slug, detail_dict)
            if dry_run:
                print(
                    "[dry-run] {} / {} — {} ({})".format(
                        city_slug, slug, name, path.name,
                    ),
                )
                continue

            raw = ask_gigachat(prompt, model=model, max_tokens=1200)
            if gigachat_failed(raw):
                print(
                    "{} / {}: {}".format(city_slug, slug, raw),
                    file=sys.stderr,
                )
                errors += 1
                if delay > 0:
                    time.sleep(delay)
                continue

            if gigachat_refusal(raw):
                print(
                    "{} / {}: skip (GigaChat policy refusal)".format(
                        city_slug, slug,
                    ),
                )
                skipped += 1
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
                reason = str(parsed.get("reason") or "нет данных").strip()
                print("{} / {}: skip ({})".format(city_slug, slug, reason))
                skipped += 1
            elif _apply_enrichment(place, parsed):
                print("{} / {}: updated".format(city_slug, slug))
                updated += 1
                file_updated += 1
            else:
                print("{} / {}: no changes".format(city_slug, slug))
                skipped += 1

            if delay > 0:
                time.sleep(delay)

        if not dry_run and file_updated:
            path.write_text(
                json.dumps(places, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            print("Written", path)

        if remaining is not None and remaining <= 0:
            break

    return updated, skipped, errors


def main() -> int:
    _load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cities",
        nargs="+",
        metavar="SLUG",
        help="City slug(s); default: all cities with sparse RU rows.",
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

    cities = _discover_cities(args.cities)
    total_up = total_sk = total_err = total_targets = 0

    for city_slug in cities:
        data_dir = _PROJECT_ROOT / city_slug / "data"
        n = 0
        for path in _place_json_paths(data_dir, city_slug):
            places = json.loads(path.read_text(encoding="utf-8"))
            n += sum(1 for p in places if place_needs_ru_narrative(p))
        if not n:
            continue
        print("\n=== {} ({} sparse) ===".format(city_slug, n))
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
        total_targets += n

    print(
        "\nDone: {} updated, {} skipped, {} errors "
        "({} cities with sparse rows).".format(
            total_up, total_sk, total_err, len(cities),
        ),
    )
    return 1 if total_err else 0


if __name__ == "__main__":
    raise SystemExit(main())
