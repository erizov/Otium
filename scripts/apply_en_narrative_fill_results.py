# -*- coding: utf-8 -*-
"""
Apply Colab EN narrative fill results into city guide JSON.

Expects ``translations/results/en_narrative_fill_results.jsonl`` with lines::

  {"id": "city/slug", "ok": true, "description_en": "...", ...}

Matches ids against ``translations/queue/en_narrative_fill.jsonl``.

Usage::

  python scripts/apply_en_narrative_fill_results.py --dry-run
  python scripts/apply_en_narrative_fill_results.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_narrative import is_usable_narrative_text, text_for_edition
from scripts.guide_translation_queue import read_jsonl

_FIELDS = (
    "description_en",
    "history_en",
    "significance_en",
)
_LIST_FIELDS = ("facts_en", "stories_en")


def _load_jobs(path: Path) -> dict[str, dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for row in read_jsonl(path):
        jid = str(row.get("id") or "").strip()
        if jid:
            by_id[jid] = row
    return by_id


def _load_results(paths: list[Path]) -> dict[str, dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for path in paths:
        if not path.is_file():
            continue
        for row in read_jsonl(path):
            jid = str(row.get("id") or "").strip()
            if jid and row.get("ok", True) is not False:
                by_id[jid] = row
    return by_id


def _coerce_str_list(raw: Any) -> list[str]:
    if not isinstance(raw, list):
        return []
    out: list[str] = []
    for item in raw:
        text = str(item).strip()
        if text and is_usable_narrative_text(text):
            if text_for_edition(text, "en"):
                out.append(text)
    return out


def _apply_row(place: dict[str, Any], row: dict[str, Any]) -> int:
    changed = 0
    for key in _FIELDS:
        text = str(row.get(key) or "").strip()
        if not text:
            continue
        if not is_usable_narrative_text(text):
            continue
        if not text_for_edition(text, "en"):
            continue
        place[key] = text
        if key == "description_en":
            if not str(place.get("description") or "").strip():
                place["description"] = text
        elif key == "history_en":
            if not str(place.get("history") or "").strip():
                place["history"] = text
        elif key == "significance_en":
            if not str(place.get("significance") or "").strip():
                place["significance"] = text
        changed += 1
    for key in _LIST_FIELDS:
        items = _coerce_str_list(row.get(key))
        if not items:
            continue
        place[key] = items
        base = key.replace("_en", "")
        if base in ("facts", "stories") and not place.get(base):
            place[base] = list(items)
        changed += 1
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=_PROJECT_ROOT,
    )
    parser.add_argument(
        "--queue",
        type=Path,
        default=_PROJECT_ROOT / "translations" / "queue" / "en_narrative_fill.jsonl",
    )
    parser.add_argument(
        "--results",
        type=Path,
        nargs="*",
        default=[
            _PROJECT_ROOT / "translations" / "results" / "en_narrative_fill_results.jsonl",
        ],
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = args.project_root.resolve()
    jobs = _load_jobs(args.queue.resolve())
    results = _load_results([p.resolve() for p in args.results])
    if not jobs:
        print("No jobs in queue.", file=sys.stderr)
        return 2
    if not results:
        print("No results found.", file=sys.stderr)
        return 2

    by_file: dict[str, list[tuple[str, dict[str, Any]]]] = {}
    missing_job = 0
    for jid, row in results.items():
        job = jobs.get(jid)
        if not job:
            missing_job += 1
            continue
        src = str(job.get("source_file") or "")
        slug = str(job.get("slug") or "")
        if not src or not slug:
            continue
        by_file.setdefault(src, []).append((slug, row))

    updated_places = 0
    updated_files = 0
    for rel, pairs in sorted(by_file.items()):
        path = root / rel
        if not path.is_file():
            print("Missing file: {}".format(rel), file=sys.stderr)
            continue
        places: list[dict[str, Any]] = json.loads(
            path.read_text(encoding="utf-8"),
        )
        by_slug = {
            str(p.get("slug") or ""): p
            for p in places
            if isinstance(p, dict)
        }
        file_changed = 0
        for slug, row in pairs:
            place = by_slug.get(slug)
            if not place:
                continue
            n = _apply_row(place, row)
            if n:
                updated_places += 1
                file_changed += 1
        if file_changed:
            updated_files += 1
            print("{}: {} place(s)".format(rel, file_changed))
            if not args.dry_run:
                path.write_text(
                    json.dumps(places, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )

    print(
        "Applied: {} place(s) in {} file(s); {} result id(s) not in queue.".format(
            updated_places,
            updated_files,
            missing_job,
        ),
    )
    if args.dry_run:
        print("(dry run — no files written)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
