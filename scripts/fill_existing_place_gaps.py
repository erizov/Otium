# -*- coding: utf-8 -*-
"""
Fill narrative gaps for **existing** place rows only.

Policy:
- Never append a new place unless it already has slug, image, and fetched text.
- Remove empty ``{}`` stubs from place lists.
- When one edition has narrative and the other does not, record translation
  direction (``en_to_ru`` / ``ru_to_en``) instead of generating new facts.
- When neither edition has narrative but the row has an image, fetch a short
  description from Wikipedia / Wikidata (Commons filename → search title).

Writes ``translations/meta/place_gap_report.json`` with per-row actions.

Usage::

  python scripts/fill_existing_place_gaps.py --report-only
  python scripts/fill_existing_place_gaps.py --fetch --cities dublin lviv
  python scripts/fill_existing_place_gaps.py --fetch
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_core import place_has_pdf_image
from scripts.city_guide_naming import (
    clean_wikimedia_display_title,
    filler_display_title,
    is_pdf_filler_slug,
)
from scripts.city_guide_narrative import (
    is_landmark_boilerplate,
    is_usable_narrative_text,
    text_for_edition,
)
from scripts.city_guide_registry_common import pdf_expand_sidecar_paths
from scripts.city_guide_sparse_narrative import (
    _json_has_usable_narrative_for_edition,
    place_edition_needs_fill,
)
from scripts.fix_banned_place_text import (
    _extract_usable,
    _first_sentences,
    _wikidata_blurb,
)
from scripts.guide_translation_queue import discover_cities, iter_translation_jobs
from scripts.rag.city_map import names_for_slug
from scripts.rag.config import rag_paths
from scripts.rag.fetch_sources import _mw_extract

_DETAIL_SUFFIX_RE = re.compile(
    r"\s*[-–—]\s*"
    r"(?:Interior|Exterior|Detail|View|Façade|Facade|Night|Day|"
    r"Panorama|Overview|Main\s+entrance)\s*$",
    re.IGNORECASE,
)

GapAction = Literal[
    "ok",
    "translate_en_to_ru",
    "translate_ru_to_en",
    "translate_both",
    "fetch_needed",
    "skip_no_image",
    "remove_empty",
]


@dataclass(frozen=True)
class PlaceGap:
    city: str
    slug: str
    source_file: str
    action: GapAction
    has_image: bool
    needs_en: bool
    needs_ru: bool
    has_en_source: bool
    has_ru_source: bool
    place_name: str


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _place_files(data_dir: Path, city_slug: str) -> list[Path]:
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


def _load_rows(path: Path) -> list[dict[str, Any]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        return []
    return [p for p in raw if isinstance(p, dict)]


def _is_empty_stub(row: dict[str, Any]) -> bool:
    if row:
        return False
    return True


def _display_name(place: dict[str, Any]) -> str:
    filler = filler_display_title(place)
    if filler:
        return filler
    for key in ("name_en", "name_ru", "name", "subtitle_en"):
        raw = clean_wikimedia_display_title(str(place.get(key) or ""))
        if raw:
            return raw
    return str(place.get("slug") or "?")


def _prepare_fetch_title(place: dict[str, Any]) -> None:
    """Ensure ``name_en`` is a cleaned Commons/Wikipedia search title."""
    for key in ("name_en", "subtitle_en", "name", "subtitle_ru", "name_ru"):
        raw = clean_wikimedia_display_title(str(place.get(key) or ""))
        if raw and not is_pdf_filler_slug(raw):
            place["name_en"] = raw
            return


def _wiki_title_candidates(
    place: dict[str, Any],
    city_slug: str,
) -> list[str]:
    city_en = names_for_slug(city_slug).name_en
    base = clean_wikimedia_display_title(_display_name(place))
    short = _DETAIL_SUFFIX_RE.sub("", base).strip() or base
    out: list[str] = []
    for name in (short, base):
        if not name:
            continue
        for cand in (
            "{}, {}".format(name, city_en),
            "{} ({})".format(name, city_en),
            name,
        ):
            if cand not in out:
                out.append(cand)
    return out


def _fetch_place_description(
    place: dict[str, Any],
    *,
    city_slug: str,
    sleep_sec: float,
) -> tuple[str, str, str]:
    """Return (description, wikidata_qid, source_lang) — never a landmark stub."""
    paths = rag_paths(_PROJECT_ROOT)
    qid = ""
    for lang, host in (("en", "en.wikipedia.org"), ("ru", "ru.wikipedia.org")):
        for title in _wiki_title_candidates(place, city_slug):
            time.sleep(sleep_sec)
            try:
                _url, extract, extra = _mw_extract(
                    paths,
                    host=host,
                    language=lang,
                    title=title,
                    sleep_sec=sleep_sec,
                    force=False,
                )
            except Exception:
                continue
            qid = str(extra.get("wikidata_qid") or "").strip() or qid
            if not _extract_usable(extract):
                continue
            desc = _first_sentences(extract)
            if (
                desc
                and not is_landmark_boilerplate(desc)
                and is_usable_narrative_text(desc)
                and text_for_edition(desc, lang)
            ):
                return desc, qid, lang
    if qid:
        for lang in ("en", "ru"):
            time.sleep(sleep_sec * 0.5)
            blurb = _wikidata_blurb(
                paths,
                qid,
                lang=lang,
                sleep_sec=sleep_sec,
            )
            if (
                blurb
                and not is_landmark_boilerplate(blurb)
                and is_usable_narrative_text(blurb)
                and text_for_edition(blurb, lang)
            ):
                return blurb, qid, lang
    return "", qid, ""


def classify_place(
    place: dict[str, Any],
    *,
    city: str,
    source_file: str,
    city_root: Path,
) -> PlaceGap:
    slug = str(place.get("slug") or "").strip()
    if _is_empty_stub(place):
        return PlaceGap(
            city=city,
            slug=slug or "(empty)",
            source_file=source_file,
            action="remove_empty",
            has_image=False,
            needs_en=False,
            needs_ru=False,
            has_en_source=False,
            has_ru_source=False,
            place_name="",
        )
    if not slug:
        return PlaceGap(
            city=city,
            slug="(no slug)",
            source_file=source_file,
            action="skip_no_image",
            has_image=False,
            needs_en=True,
            needs_ru=True,
            has_en_source=False,
            has_ru_source=False,
            place_name=_display_name(place),
        )

    has_image = place_has_pdf_image(city_root, place)
    needs_en = place_edition_needs_fill(place, "en")
    needs_ru = place_edition_needs_fill(place, "ru")
    has_en = _json_has_usable_narrative_for_edition(place, "en")
    has_ru = _json_has_usable_narrative_for_edition(place, "ru")

    if not needs_en and not needs_ru:
        action: GapAction = "ok"
    elif needs_en and needs_ru:
        action = "fetch_needed" if has_image else "skip_no_image"
    elif needs_ru and has_en:
        action = "translate_en_to_ru"
    elif needs_en and has_ru:
        action = "translate_ru_to_en"
    elif needs_ru and not has_en:
        action = "fetch_needed" if has_image else "skip_no_image"
    elif needs_en and not has_ru:
        action = "fetch_needed" if has_image else "skip_no_image"
    else:
        action = "translate_both"

    return PlaceGap(
        city=city,
        slug=slug,
        source_file=source_file,
        action=action,
        has_image=has_image,
        needs_en=needs_en,
        needs_ru=needs_ru,
        has_en_source=has_en,
        has_ru_source=has_ru,
        place_name=_display_name(place),
    )


def _fetch_into_place(
    place: dict[str, Any],
    *,
    city_slug: str,
    sleep_sec: float,
) -> bool:
    _prepare_fetch_title(place)
    desc, _qid, lang = _fetch_place_description(
        place,
        city_slug=city_slug,
        sleep_sec=sleep_sec,
    )
    if not desc or not lang:
        return False
    if lang == "ru":
        place["description_ru"] = desc
    else:
        place["description_en"] = desc
        if not place.get("description"):
            place["description"] = desc
    return True


def scan_city(
    city_slug: str,
) -> tuple[list[PlaceGap], dict[Path, list[dict[str, Any]]]]:
    city_root = _PROJECT_ROOT / city_slug
    data_dir = city_root / "data"
    gaps: list[PlaceGap] = []
    files: dict[Path, list[dict[str, Any]]] = {}
    for path in _place_files(data_dir, city_slug):
        rows = _load_rows(path)
        rel = path.relative_to(_PROJECT_ROOT).as_posix()
        files[path] = rows
        for place in rows:
            gaps.append(
                classify_place(
                    place,
                    city=city_slug,
                    source_file=rel,
                    city_root=city_root,
                ),
            )
    return gaps, files


def _remove_empty_stubs(
    files: dict[Path, list[dict[str, Any]]],
) -> int:
    removed = 0
    for path, rows in files.items():
        kept = [r for r in rows if not _is_empty_stub(r)]
        removed += len(rows) - len(kept)
        files[path] = kept
    return removed


def _write_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def fill_city(
    city_slug: str,
    *,
    fetch: bool,
    sleep_sec: float,
    dry_run: bool,
) -> dict[str, int]:
    stats = {
        "removed_empty": 0,
        "fetched": 0,
        "fetch_failed": 0,
        "files_written": 0,
    }
    gaps, files = scan_city(city_slug)
    stats["removed_empty"] = _remove_empty_stubs(files)

    if fetch:
        city_root = _PROJECT_ROOT / city_slug
        for path, rows in files.items():
            file_changed = False
            for place in rows:
                gap = classify_place(
                    place,
                    city=city_slug,
                    source_file=path.relative_to(_PROJECT_ROOT).as_posix(),
                    city_root=city_root,
                )
                if gap.action != "fetch_needed":
                    continue
                if dry_run:
                    print(
                        "[dry-run] fetch {} / {}".format(city_slug, gap.slug),
                    )
                    continue
                before = json.dumps(place, sort_keys=True)
                ok = _fetch_into_place(
                    place,
                    city_slug=city_slug,
                    sleep_sec=sleep_sec,
                )
                if ok and json.dumps(place, sort_keys=True) != before:
                    stats["fetched"] += 1
                    file_changed = True
                    print("  fetched {} / {}".format(city_slug, gap.slug))
                else:
                    stats["fetch_failed"] += 1
                    print(
                        "  fetch failed {} / {}".format(city_slug, gap.slug),
                        file=sys.stderr,
                    )
                time.sleep(sleep_sec)
            if file_changed and not dry_run:
                _write_rows(path, rows)
                stats["files_written"] += 1

    if stats["removed_empty"] and not dry_run:
        for path, rows in files.items():
            if len(rows) != len(_load_rows(path)):
                _write_rows(path, rows)
                stats["files_written"] += 1

    return stats


def build_report(
    gaps: list[PlaceGap],
    *,
    translation_jobs: list[dict[str, Any]],
) -> dict[str, Any]:
    by_action: dict[str, int] = {}
    for gap in gaps:
        by_action[gap.action] = by_action.get(gap.action, 0) + 1

    en_to_ru_jobs = [j for j in translation_jobs if j.get("src_lang") == "en"]
    ru_to_en_jobs = [j for j in translation_jobs if j.get("src_lang") == "ru"]

    rows = [
        {
            "city": g.city,
            "slug": g.slug,
            "source_file": g.source_file,
            "action": g.action,
            "place_name": g.place_name,
            "has_image": g.has_image,
            "needs_en": g.needs_en,
            "needs_ru": g.needs_ru,
        }
        for g in gaps
        if g.action not in ("ok",)
    ]

    return {
        "generated_at": _utc_now(),
        "summary": {
            "places_scanned": len(gaps),
            "by_action": by_action,
            "translate_en_to_ru_places": by_action.get(
                "translate_en_to_ru", 0,
            ),
            "translate_ru_to_en_places": by_action.get(
                "translate_ru_to_en", 0,
            ),
            "fetch_needed": by_action.get("fetch_needed", 0),
            "skip_no_image": by_action.get("skip_no_image", 0),
            "remove_empty": by_action.get("remove_empty", 0),
            "translation_jobs_en_to_ru": len(en_to_ru_jobs),
            "translation_jobs_ru_to_en": len(ru_to_en_jobs),
        },
        "gaps": rows,
        "translation_sample_en_to_ru": en_to_ru_jobs[:5],
        "translation_sample_ru_to_en": ru_to_en_jobs[:5],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cities",
        nargs="*",
        default=None,
        metavar="SLUG",
    )
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="Fetch Wikipedia text for rows with image and no narrative.",
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Write gap report only; do not modify JSON.",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=2.0,
        metavar="SEC",
        help="Pause between Wikipedia calls (default 2.0).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
    )
    args = parser.parse_args()

    cities = args.cities if args.cities else discover_cities(_PROJECT_ROOT)
    if not cities:
        print("No cities found.", file=sys.stderr)
        return 2

    all_gaps: list[PlaceGap] = []
    totals = {
        "removed_empty": 0,
        "fetched": 0,
        "fetch_failed": 0,
        "files_written": 0,
    }

    for city in cities:
        print("Scanning {}…".format(city), flush=True)
        if args.report_only and not args.fetch:
            gaps, files = scan_city(city)
            removed = _remove_empty_stubs(files)
            totals["removed_empty"] += removed
            all_gaps.extend(gaps)
            continue

        part = fill_city(
            city,
            fetch=bool(args.fetch),
            sleep_sec=float(args.sleep),
            dry_run=bool(args.dry_run),
        )
        for key in totals:
            totals[key] += part[key]
        gaps, _files = scan_city(city)
        all_gaps.extend(gaps)

    translation_jobs: list[dict[str, Any]] = []
    for city in cities:
        translation_jobs.extend(iter_translation_jobs(_PROJECT_ROOT, city))

    report = build_report(all_gaps, translation_jobs=translation_jobs)
    report["fill_stats"] = totals

    out_dir = _PROJECT_ROOT / "translations" / "meta"
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / "place_gap_report.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    for action, fname in (
        ("translate_en_to_ru", "translate_en_to_ru_places.jsonl"),
        ("translate_ru_to_en", "translate_ru_to_en_places.jsonl"),
        ("fetch_needed", "fetch_needed_places.jsonl"),
    ):
        rows = [
            {
                "city": g.city,
                "slug": g.slug,
                "place_name": g.place_name,
                "source_file": g.source_file,
            }
            for g in all_gaps
            if g.action == action
        ]
        if rows:
            path = out_dir / fname
            with path.open("w", encoding="utf-8") as fh:
                for row in rows:
                    fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    summary = report["summary"]
    print("--- summary ---", flush=True)
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
    print("Report:", report_path.relative_to(_PROJECT_ROOT), flush=True)
    print("Fill stats:", totals, flush=True)

    if args.dry_run:
        return 0

    if args.report_only:
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
