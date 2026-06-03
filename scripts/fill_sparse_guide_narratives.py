# -*- coding: utf-8 -*-
"""
Fill sparse city-guide place narratives before PDF builds.

For each sparse EN or RU card (title/meta only, no real body):

1. ``OPENAI_API_KEY`` — JSON narrative (English or Russian per edition)
2. ``GIGA_AUTH_KEY`` — same prompt shape, output language in prompt
3. ``PIXABAY_API_KEY`` — tag hints → minimal EN copy (EN only, if both LLMs
   failed)
4. ``OLLAMA_HOST`` / ``OLLAMA_MODEL`` — translate from the opposite edition
   when it already has usable narrative text

Per city (unless ``--dry-run-only``): lists sparse rows, fills JSON, then
runs ``audit_guide_edition_gaps`` on that city.

Usage::

  python scripts/fill_sparse_guide_narratives.py --dry-run-only --cities bangkok
  python scripts/fill_sparse_guide_narratives.py --cities bangkok --limit 3
  python scripts/fill_sparse_guide_narratives.py
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.audit_guide_edition_gaps import audit_city, format_audit_line
from scripts.city_guide_sparse_narrative import ProviderCircuitBreaker, process_city
from scripts.enrich_places_gigachat_common import discover_cities, load_dotenv


def _print_city_audit(city_slug: str, *, with_translate: bool) -> dict[str, int]:
    stats = audit_city(_PROJECT_ROOT, city_slug, use_translate=with_translate)
    print(format_audit_line(city_slug, stats), flush=True)
    return stats


def main() -> int:
    load_dotenv(_PROJECT_ROOT)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cities",
        nargs="+",
        metavar="SLUG",
        help="City slug(s); default: all cities with places JSON.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        metavar="N",
        help="Max sparse places per JSON file (testing).",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        metavar="SEC",
        help="Pause between LLM API calls (default 2.0).",
    )
    parser.add_argument(
        "--openai-model",
        default=None,
        metavar="MODEL",
        help="OpenAI model (default OPENAI_MODEL or gpt-4o-mini).",
    )
    parser.add_argument(
        "--gigachat-model",
        default="GigaChat",
        help="GigaChat model name (default GigaChat).",
    )
    parser.add_argument(
        "--dry-run-only",
        action="store_true",
        help="List sparse rows and audit only; no API calls or JSON writes.",
    )
    parser.add_argument(
        "--resume-from",
        metavar="SLUG",
        help="Skip cities before this slug (alphabetical discover order).",
    )
    parser.add_argument(
        "--with-translate",
        action="store_true",
        help="Use translator in post-fill audit (slow; matches PDF render).",
    )
    args = parser.parse_args()

    cities = discover_cities(_PROJECT_ROOT, args.cities)
    if not cities:
        print("No cities found.", file=sys.stderr)
        return 2

    if args.resume_from:
        resume = args.resume_from.strip().lower()
        if resume not in cities:
            print(
                "Unknown --resume-from {!r}; cities: {}".format(
                    resume, ", ".join(cities),
                ),
                file=sys.stderr,
            )
            return 2
        cities = cities[cities.index(resume) :]

    breaker = ProviderCircuitBreaker(
        fail_threshold=3,
        suspend_places=1000,
    )
    grand = {
        "en_openai": 0,
        "en_gigachat": 0,
        "en_pixabay": 0,
        "en_translate": 0,
        "ru_openai": 0,
        "ru_gigachat": 0,
        "ru_translate": 0,
        "still_sparse_en": 0,
        "still_sparse_ru": 0,
    }

    failed_cities: list[str] = []

    for city_slug in cities:
        print("\n=== {} ===".format(city_slug), flush=True)

        print("--- sparse (before) ---", flush=True)
        try:
            process_city(
                _PROJECT_ROOT,
                city_slug,
                breaker=breaker,
                dry_run=True,
                limit=args.limit,
                openai_model=args.openai_model,
                gigachat_model=args.gigachat_model,
                delay=args.delay,
            )
        except Exception as exc:
            print(
                "sparse preview failed for {}: {}".format(city_slug, exc),
                file=sys.stderr,
            )

        if args.dry_run_only:
            print("--- audit ---", flush=True)
            _print_city_audit(city_slug, with_translate=args.with_translate)
            continue

        try:
            stats = process_city(
                _PROJECT_ROOT,
                city_slug,
                breaker=breaker,
                dry_run=False,
                limit=args.limit,
                openai_model=args.openai_model,
                gigachat_model=args.gigachat_model,
                delay=args.delay,
            )
        except Exception as exc:
            print(
                "FAILED {}: {}".format(city_slug, exc),
                file=sys.stderr,
            )
            failed_cities.append(city_slug)
            continue

        for key in grand:
            grand[key] += stats.get(key, 0)

        print("--- audit (after) ---", flush=True)
        _print_city_audit(city_slug, with_translate=args.with_translate)

    if args.dry_run_only:
        return 0

    if failed_cities:
        print(
            "\nCities with errors: {}".format(", ".join(failed_cities)),
            file=sys.stderr,
        )

    print(
        "\nDone — EN: openai={en_openai} gigachat={en_gigachat} "
        "pixabay={en_pixabay} translate_ru={en_translate} "
        "still_sparse={still_sparse_en} | "
        "RU: openai={ru_openai} gigachat={ru_gigachat} "
        "translate_en={ru_translate} still_sparse={still_sparse_ru}".format(
            **grand,
        ),
        flush=True,
    )
    if grand["still_sparse_en"] or grand["still_sparse_ru"] or failed_cities:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
