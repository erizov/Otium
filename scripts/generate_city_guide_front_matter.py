# -*- coding: utf-8 -*-
"""Generate city primer + trip plans JSON (one file per city, EN + RU)."""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_front_matter import (
    ITINERARY_KEYS,
    front_matter_json_path,
    save_front_matter,
    top_places_for_prompt,
)
from scripts.city_guide_naming import is_pdf_filler_slug
from scripts.city_guide_sparse_narrative import (
    ask_gigachat_place_json,
    ask_openai_place_json,
    gigachat_configured,
    openai_configured,
)
from scripts.enrich_places_gigachat_common import load_dotenv
from scripts.rag.city_map import names_for_slug

def _discover_slugs(project_root: Path) -> list[str]:
    scripts_dir = project_root / "scripts"
    out: list[str] = []
    for path in sorted(scripts_dir.glob("build_*_pdf.py")):
        stem = path.stem
        if not stem.startswith("build_") or not stem.endswith("_pdf"):
            continue
        slug = stem[len("build_") : -len("_pdf")]
        places = project_root / slug / "data" / "{}_places.json".format(slug)
        if places.is_file():
            out.append(slug)
    return out


def _load_places(project_root: Path, city_slug: str) -> list[dict[str, Any]]:
    path = project_root / city_slug / "data" / "{}_places.json".format(
        city_slug,
    )
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("{}: expected JSON array".format(path))
    return [p for p in raw if isinstance(p, dict)]


def _build_prompt(
    *,
    city_slug: str,
    display_title: str,
    edition: str,
    top_rows: list[dict[str, Any]],
) -> str:
    names = names_for_slug(city_slug)
    city_label = names.name_ru if edition == "ru" else names.name_en
    place_lines = []
    for row in top_rows:
        line = "- {} (slug: {})".format(row["title"], row["slug"])
        if row.get("blurb"):
            line += ": {}".format(row["blurb"])
        place_lines.append(line)
    places_block = "\n".join(place_lines) if place_lines else "(none)"
    lang_rule = (
        "Язык ответа: русский. Все строки JSON — только на русском."
        if edition == "ru"
        else "Output language: English only."
    )
    durations = ", ".join(ITINERARY_KEYS)
    return (
        "You write practical front matter for a printed city guide (OTIUM).\n"
        "City: {city} ({slug}).\n"
        "Display title: {title}.\n\n"
        "Featured places (use ONLY these slugs in itinerary stops):\n"
        "{places}\n\n"
        "Return ONE JSON object with this shape:\n"
        "{{\n"
        '  "primer": {{\n'
        '    "climate": "2-4 sentences on seasons, rain, heat, what to pack",\n'
        '    "transport": "2-4 sentences: metro/tram/bus/taxi, tickets, airport",\n'
        '    "etiquette": "2-4 sentences: dress, tipping, quiet zones, photos",\n'
        '    "overview_paragraphs": ["optional 1-2 short paragraphs tying the city"]\n'
        "  }},\n"
        '  "itineraries": {{\n'
        '    "4h": {{"title": "...", "intro": "1-2 sentences", '
        '"stops": [{{"slug": "...", "minutes": 45, "note": "why"}}]}},\n'
        '    "1d": {{...}},\n'
        '    "2d": {{...}},\n'
        '    "5d": {{...}}\n'
        "  }}\n"
        "}}\n\n"
        "Rules:\n"
        "- Itinerary keys must be exactly: {durations}.\n"
        "- 4h: 2-4 stops; 1d: 4-6; 2d: 6-9; 5d: 10-14.\n"
        "- Every stop.slug MUST be from the featured list.\n"
        "- Do not invent museums or sites not in the list.\n"
        "- minutes is optional integer (visit time).\n"
        "- Be practical for walkers; cluster by neighbourhood when possible.\n"
        "- Avoid landmark boilerplate; no marketing hype.\n\n"
        "{lang}\n"
    ).format(
        city=city_label,
        slug=city_slug,
        title=display_title,
        places=places_block,
        durations=durations,
        lang=lang_rule,
    )


def _sanitize_stop(
    raw: Any,
    valid_slugs: frozenset[str],
) -> dict[str, Any] | None:
    if not isinstance(raw, dict):
        return None
    slug = str(raw.get("slug") or "").strip()
    if not slug or slug not in valid_slugs:
        return None
    out: dict[str, Any] = {"slug": slug}
    note = str(raw.get("note") or "").strip()
    if note:
        out["note"] = note
    minutes = raw.get("minutes")
    if isinstance(minutes, (int, float)) and minutes > 0:
        out["minutes"] = int(minutes)
    name = str(raw.get("name") or "").strip()
    if name:
        out["name"] = name
    return out


def _sanitize_edition_payload(
    parsed: dict[str, Any],
    valid_slugs: frozenset[str],
) -> dict[str, Any]:
    primer_in = parsed.get("primer")
    primer_out: dict[str, Any] = {}
    if isinstance(primer_in, dict):
        for key in ("climate", "transport", "etiquette"):
            text = str(primer_in.get(key) or "").strip()
            if text:
                primer_out[key] = text
        paras = primer_in.get("overview_paragraphs")
        if isinstance(paras, list):
            clean = [str(p).strip() for p in paras if str(p).strip()]
            if clean:
                primer_out["overview_paragraphs"] = clean[:3]

    trips_in = parsed.get("itineraries")
    trips_out: dict[str, Any] = {}
    if isinstance(trips_in, dict):
        for key in ITINERARY_KEYS:
            plan = trips_in.get(key)
            if not isinstance(plan, dict):
                continue
            stops_raw = plan.get("stops")
            stops: list[dict[str, Any]] = []
            if isinstance(stops_raw, list):
                for item in stops_raw:
                    stop = _sanitize_stop(item, valid_slugs)
                    if stop:
                        stops.append(stop)
            if not stops:
                continue
            entry: dict[str, Any] = {"stops": stops}
            title = str(plan.get("title") or "").strip()
            intro = str(plan.get("intro") or "").strip()
            if title:
                entry["title"] = title
            if intro:
                entry["intro"] = intro
            trips_out[key] = entry

    out: dict[str, Any] = {}
    if primer_out:
        out["primer"] = primer_out
    if trips_out:
        out["itineraries"] = trips_out
    return out


def _ask_edition(
    prompt: str,
    edition: str,
    *,
    openai_model: str | None,
    gigachat_model: str,
) -> dict[str, Any] | None:
    if edition == "ru" and gigachat_configured():
        return ask_gigachat_place_json(prompt, model=gigachat_model)
    if openai_configured():
        return ask_openai_place_json(prompt, model=openai_model)
    if edition == "ru" and openai_configured():
        return ask_openai_place_json(prompt, model=openai_model)
    return None


def _merge_edition(
    doc: dict[str, Any],
    edition: str,
    payload: dict[str, Any],
) -> None:
    primer = payload.get("primer")
    if isinstance(primer, dict) and primer:
        doc.setdefault("primer", {})
        if isinstance(doc["primer"], dict):
            doc["primer"][edition] = primer
    trips = payload.get("itineraries")
    if isinstance(trips, dict) and trips:
        doc.setdefault("itineraries", {})
        if isinstance(doc["itineraries"], dict):
            doc["itineraries"][edition] = trips


def generate_city(
    project_root: Path,
    city_slug: str,
    *,
    display_title: str | None,
    top_n: int,
    editions: tuple[str, ...],
    dry_run: bool,
    force: bool,
    openai_model: str | None,
    gigachat_model: str,
    delay: float,
) -> bool:
    path = front_matter_json_path(project_root, city_slug)
    if path.is_file() and not force:
        print("{}: skip (exists; use --force)".format(city_slug))
        return True

    places = _load_places(project_root, city_slug)
    curated = [
        p
        for p in places
        if not is_pdf_filler_slug(str(p.get("slug") or ""))
    ]
    if not curated:
        print("{}: no curated places".format(city_slug), file=sys.stderr)
        return False

    title = display_title or names_for_slug(city_slug).name_en
    valid_slugs = frozenset(
        str(p.get("slug") or "").strip()
        for p in curated
        if str(p.get("slug") or "").strip()
    )

    doc: dict[str, Any] = {
        "city_slug": city_slug,
        "display_title": title,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "top_place_slugs": [],
    }

    for edition in editions:
        top_rows = top_places_for_prompt(curated, edition, limit=top_n)
        if not top_rows:
            print("{} {}: no top places".format(city_slug, edition))
            continue
        doc["top_place_slugs"] = [r["slug"] for r in top_rows]
        prompt = _build_prompt(
            city_slug=city_slug,
            display_title=title,
            edition=edition,
            top_rows=top_rows,
        )
        if dry_run:
            print("[dry-run] {} ({}) — {} places".format(
                city_slug, edition, len(top_rows),
            ))
            continue

        parsed = _ask_edition(
            prompt,
            edition,
            openai_model=openai_model,
            gigachat_model=gigachat_model,
        )
        if not parsed:
            print(
                "{} {}: LLM failed or not configured".format(
                    city_slug, edition,
                ),
                file=sys.stderr,
            )
            return False
        clean = _sanitize_edition_payload(parsed, valid_slugs)
        if not clean:
            print(
                "{} {}: empty after sanitize".format(city_slug, edition),
                file=sys.stderr,
            )
            return False
        _merge_edition(doc, edition, clean)
        print("{} {}: ok".format(city_slug, edition))
        if delay > 0:
            time.sleep(delay)

    if dry_run:
        return True
    if not doc.get("primer") and not doc.get("itineraries"):
        return False
    out_path = save_front_matter(project_root, city_slug, doc)
    print("Written: {}".format(out_path))
    return True


def main() -> int:
    load_dotenv(_PROJECT_ROOT)
    parser = argparse.ArgumentParser(
        description="Generate city primer + trip plans JSON for guide PDFs.",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=_PROJECT_ROOT,
    )
    parser.add_argument(
        "--cities",
        nargs="*",
        metavar="SLUG",
        help="City slugs (default: all with build_*_pdf.py)",
    )
    parser.add_argument(
        "--display-title",
        help="Override display title for prompts",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=12,
        metavar="N",
        help="Top N places in LLM context (default 12)",
    )
    parser.add_argument(
        "--edition",
        choices=("en", "ru", "both"),
        default="both",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--delay", type=float, default=2.0)
    parser.add_argument("--openai-model", default=None)
    parser.add_argument("--gigachat-model", default="GigaChat")
    args = parser.parse_args()
    root = args.project_root.resolve()
    slugs = sorted(set(args.cities)) if args.cities else _discover_slugs(root)
    if not slugs:
        print("No cities found.", file=sys.stderr)
        return 2

    if args.edition == "both":
        editions: tuple[str, ...] = ("en", "ru")
    else:
        editions = (args.edition,)

    if not args.dry_run and not openai_configured() and not gigachat_configured():
        print(
            "Set OPENAI_API_KEY and/or GIGA_AUTH_KEY in .env",
            file=sys.stderr,
        )
        return 2

    ok = failed = 0
    for slug in slugs:
        if generate_city(
            root,
            slug,
            display_title=args.display_title,
            top_n=max(3, args.top),
            editions=editions,
            dry_run=args.dry_run,
            force=args.force,
            openai_model=args.openai_model,
            gigachat_model=args.gigachat_model,
            delay=args.delay,
        ):
            ok += 1
        else:
            failed += 1
    print("Done: {} ok, {} failed.".format(ok, failed))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
