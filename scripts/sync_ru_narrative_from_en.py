# -*- coding: utf-8 -*-
"""
Sync RU place narrative from EN when the Russian edition has less text.

Translates missing or shorter RU fields from EN sources (Ollama/OpenAI/cache).
Does not overwrite RU fields that are already longer than their EN counterpart.

Usage::

  python scripts/sync_ru_narrative_from_en.py --dry-run
  python scripts/sync_ru_narrative_from_en.py --cities chernivtsi kyiv
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Mapping

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_edition_reconcile import edition_narrative_chars
from scripts.city_guide_narrative import text_for_edition, translate_for_edition
from scripts.city_guide_registry_common import pdf_expand_sidecar_paths
from scripts.city_guide_sparse_narrative import (
    ProviderCircuitBreaker,
    _best_opposite_source,
    _edition_has_usable_field,
    _field_keys_for_edition,
    _read_field,
    _write_text_field,
    place_edition_needs_fill,
)
from scripts.city_guide_translate import (
    EditionTranslator,
    OllamaFatalError,
)
from scripts.enrich_places_gigachat_common import discover_cities, load_dotenv

_PROSE_BASES = ("description", "history", "significance")


def _field_chars(place: Mapping[str, Any], edition: str, base: str) -> int:
    total = 0
    for key in _field_keys_for_edition(edition, base):
        text = _read_field(place, key)
        if text and text_for_edition(text, edition):
            total += len(text)
    return total


def _facts_chars(place: Mapping[str, Any], edition: str) -> int:
    total = 0
    for key in _field_keys_for_edition(edition, "facts"):
        raw = place.get(key)
        if not isinstance(raw, list):
            continue
        for item in raw:
            text = str(item).strip()
            if text and text_for_edition(text, edition):
                total += len(text)
    return total


def place_needs_ru_sync(place: Mapping[str, Any]) -> bool:
    """True when EN has more narrative than RU or RU edition still needs fill."""
    if place_edition_needs_fill(place, "ru"):
        return edition_narrative_chars(place, "en") > 0
    return edition_narrative_chars(place, "en") > edition_narrative_chars(
        place, "ru",
    )


def sync_place_ru_from_en(
    place: dict[str, Any],
    *,
    translator: EditionTranslator,
    breaker: ProviderCircuitBreaker | None = None,
    delay: float = 0.0,
    cache_only: bool = False,
) -> bool:
    """Translate EN fields into RU when RU is missing or shorter."""
    from scripts.city_guide_translate import _cache_key

    cache = translator._mem if cache_only else None
    changed = False
    for base in _PROSE_BASES:
        en_len = _field_chars(place, "en", base)
        ru_len = _field_chars(place, "ru", base)
        if en_len <= ru_len:
            continue
        if _edition_has_usable_field(place, "ru", base) and ru_len >= en_len:
            continue
        src = _best_opposite_source(place, "ru", base)
        if not src:
            continue
        translated: str | None = None
        if cache_only and cache is not None:
            key = _cache_key(src, src="en", dst="ru", kind="prose")
            cached = cache.get(key, "").strip()
            if cached and text_for_edition(cached, "ru"):
                translated = cached
        else:
            try:
                translated = translate_for_edition(
                    src,
                    "ru",
                    kind="prose",
                    translator=translator,
                )
            except OllamaFatalError as exc:
                print("Ollama fatal: {}".format(exc), file=sys.stderr)
                if breaker is not None:
                    breaker.suspend_forever("ollama_translate")
                return changed
        if not translated:
            if breaker is not None and not cache_only:
                breaker.record_failure("ollama_translate")
            continue
        _write_text_field(place, "ru", base, translated)
        changed = True
        if breaker is not None:
            breaker.record_success("ollama_translate")
        if delay > 0:
            time.sleep(delay)

    en_facts = _facts_chars(place, "en")
    ru_facts = _facts_chars(place, "ru")
    if en_facts > ru_facts:
        src_items: list[str] = []
        for key in ("facts_en", "facts"):
            raw = place.get(key)
            if not isinstance(raw, list):
                continue
            for item in raw:
                text = str(item).strip()
                if text and text_for_edition(text, "en"):
                    src_items.append(text)
            if src_items:
                break
        out: list[str] = []
        for text in src_items[:8]:
            translated_fact: str | None = None
            if cache_only and cache is not None:
                key = _cache_key(text, src="en", dst="ru", kind="prose")
                cached = cache.get(key, "").strip()
                if cached and text_for_edition(cached, "ru"):
                    translated_fact = cached
            else:
                try:
                    translated_fact = translate_for_edition(
                        text,
                        "ru",
                        kind="prose",
                        translator=translator,
                    )
                except OllamaFatalError as exc:
                    print("Ollama fatal: {}".format(exc), file=sys.stderr)
                    if breaker is not None:
                        breaker.suspend_forever("ollama_translate")
                    break
            if translated_fact:
                out.append(translated_fact)
            if delay > 0:
                time.sleep(delay)
        if out and (not place.get("facts_ru") or ru_facts < en_facts):
            place["facts_ru"] = out
            if not place.get("facts") or not any(
                text_for_edition(str(x), "ru") for x in (place.get("facts") or [])
            ):
                place["facts"] = list(out)
            changed = True
    return changed


def _place_files(data_dir: Path, city_slug: str) -> list[Path]:
    paths: list[Path] = []
    main = data_dir / "{}_places.json".format(city_slug)
    if main.is_file():
        paths.append(main)
    paths.extend(pdf_expand_sidecar_paths(data_dir, city_slug))
    return paths


def sync_city(
    project_root: Path,
    city_slug: str,
    *,
    translator: EditionTranslator,
    breaker: ProviderCircuitBreaker,
    dry_run: bool,
    delay: float,
    cache_only: bool = False,
) -> dict[str, int]:
    stats = {"candidates": 0, "updated": 0, "files": 0}
    data_dir = project_root / city_slug / "data"
    for path in _place_files(data_dir, city_slug):
        places: list[dict[str, Any]] = json.loads(
            path.read_text(encoding="utf-8"),
        )
        file_changed = False
        for place in places:
            if not isinstance(place, dict):
                continue
            if not place_needs_ru_sync(place):
                continue
            stats["candidates"] += 1
            if dry_run:
                continue
            if sync_place_ru_from_en(
                place,
                translator=translator,
                breaker=breaker,
                delay=delay,
                cache_only=cache_only,
            ):
                stats["updated"] += 1
                file_changed = True
        if file_changed and not dry_run:
            path.write_text(
                json.dumps(places, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            stats["files"] += 1
    return stats


def main() -> int:
    load_dotenv(_PROJECT_ROOT)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=_PROJECT_ROOT,
    )
    parser.add_argument(
        "--cities",
        nargs="*",
        metavar="SLUG",
        default=None,
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--delay",
        type=float,
        default=0.0,
        metavar="SEC",
    )
    parser.add_argument(
        "--cache-only",
        action="store_true",
        help="Apply only cached EN→RU translations (no API calls).",
    )
    args = parser.parse_args()
    root = args.project_root.resolve()
    cities = discover_cities(root, args.cities)
    if not cities:
        print("No cities found.", file=sys.stderr)
        return 2

    tr = EditionTranslator(enabled=True)
    if not args.cache_only and tr is None and not args.dry_run:
        print(
            "No translator (set OLLAMA_HOST or OPENAI_API_KEY).",
            file=sys.stderr,
        )
        return 2

    breaker = ProviderCircuitBreaker()
    total_candidates = 0
    total_updated = 0
    for city in cities:
        stats = sync_city(
            root,
            city,
            translator=tr,
            breaker=breaker,
            dry_run=args.dry_run,
            delay=args.delay,
            cache_only=args.cache_only,
        )
        if stats["candidates"] or stats["updated"]:
            print(
                "{:16} candidates={:4} updated={:4} files={}".format(
                    city,
                    stats["candidates"],
                    stats["updated"],
                    stats["files"],
                ),
            )
        total_candidates += stats["candidates"]
        total_updated += stats["updated"]

    mode = "would sync" if args.dry_run else "synced"
    print(
        "Total {}: {} place(s) in {} cities.".format(
            mode, total_updated or total_candidates, len(cities),
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
