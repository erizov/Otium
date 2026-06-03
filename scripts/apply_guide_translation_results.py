# -*- coding: utf-8 -*-
"""
Apply Colab translation results back into city guide JSON.

Expects ``translations/results/en_to_ru_results.jsonl`` and
``ru_to_en_results.jsonl`` (or combined ``results.jsonl``) with lines::

  {"id": "city/slug/field/en-ru", "translated": "..."}

Matches ids against ``translations/queue/queue.jsonl``.

Usage::

  python scripts/apply_guide_translation_results.py --dry-run
  python scripts/apply_guide_translation_results.py --overlay
  python scripts/apply_guide_translation_results.py --write-places
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_narrative import (
    is_usable_narrative_text,
    text_for_edition,
)
from scripts.guide_translation_queue import read_jsonl


def _load_results(paths: list[Path]) -> dict[str, str]:
    by_id: dict[str, str] = {}
    for path in paths:
        if not path.is_file():
            continue
        for row in read_jsonl(path):
            jid = str(row.get("id") or "").strip()
            text = str(
                row.get("translated") or row.get("text") or "",
            ).strip()
            if jid and text:
                by_id[jid] = text
    return by_id


def _apply_to_place(
    place: dict[str, Any],
    job: dict[str, Any],
    translated: str,
) -> bool:
    dst = str(job.get("dst_lang") or "")
    if not text_for_edition(translated, dst):
        return False
    if not is_usable_narrative_text(translated):
        return False
    key = str(job.get("target_key") or "")
    if job.get("field") == "facts":
        idx = job.get("fact_index")
        if idx is None:
            return False
        raw = place.get(key)
        if not isinstance(raw, list):
            raw = []
            place[key] = raw
        while len(raw) <= int(idx):
            raw.append("")
        raw[int(idx)] = translated
        return True
    if not key:
        return False
    place[key] = translated
    return True


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
        default=_PROJECT_ROOT / "translations" / "queue" / "queue.jsonl",
    )
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=_PROJECT_ROOT / "translations" / "results",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
    )
    parser.add_argument(
        "--overlay",
        action="store_true",
        help="Write patches to <city>_place_details_more.json (default).",
    )
    parser.add_argument(
        "--write-places",
        action="store_true",
        help="Rewrite source *_places.json / sidecar files in place.",
    )
    args = parser.parse_args()
    root = args.project_root.resolve()
    queue_path = args.queue.resolve()
    if not queue_path.is_file():
        print("Missing queue: {}".format(queue_path), file=sys.stderr)
        return 2

    res_dir = args.results_dir.resolve()
    result_paths = [
        res_dir / "en_to_ru_results.jsonl",
        res_dir / "ru_to_en_results.jsonl",
        res_dir / "results.jsonl",
    ]
    translated_by_id = _load_results(result_paths)
    if not translated_by_id:
        print("No results found in {}".format(res_dir), file=sys.stderr)
        return 2

    jobs = read_jsonl(queue_path)
    job_by_id = {str(j["id"]): j for j in jobs if j.get("id")}

    use_overlay = args.overlay or not args.write_places
    patches: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    file_places: dict[Path, list[dict[str, Any]]] = {}
    applied = 0
    skipped = 0

    for jid, text in translated_by_id.items():
        job = job_by_id.get(jid)
        if not job:
            skipped += 1
            continue
        city = str(job["city"])
        slug = str(job["slug"])
        rel = str(job["source_file"])
        path = root / rel
        if use_overlay:
            block = patches[city].setdefault(slug, {})
            key = str(job.get("target_key") or "")
            if job.get("field") == "facts":
                idx = job.get("fact_index")
                if idx is None:
                    skipped += 1
                    continue
                facts = block.setdefault(key, [])
                if not isinstance(facts, list):
                    facts = []
                    block[key] = facts
                while len(facts) <= int(idx):
                    facts.append("")
                if text_for_edition(text, str(job["dst_lang"])) and (
                    is_usable_narrative_text(text)
                ):
                    facts[int(idx)] = text
                    applied += 1
                else:
                    skipped += 1
            elif key and text_for_edition(
                text, str(job["dst_lang"]),
            ) and is_usable_narrative_text(text):
                block[key] = text
                applied += 1
            else:
                skipped += 1
        else:
            if path not in file_places:
                file_places[path] = json.loads(
                    path.read_text(encoding="utf-8"),
                )
            place = next(
                (
                    p for p in file_places[path]
                    if str(p.get("slug")) == slug
                ),
                None,
            )
            if place is None:
                skipped += 1
                continue
            if _apply_to_place(place, job, text):
                applied += 1
            else:
                skipped += 1

    if args.dry_run:
        print(
            "Dry run: would apply {} (skipped {})".format(applied, skipped),
        )
        return 0

    if use_overlay:
        for city, slug_map in patches.items():
            out_path = (
                root / city / "data"
                / "{}_place_details_more.json".format(city)
            )
            overlay: dict[str, Any] = {}
            if out_path.is_file():
                overlay = json.loads(out_path.read_text(encoding="utf-8"))
            if not isinstance(overlay, dict):
                overlay = {}
            for slug, block in slug_map.items():
                cur = overlay.get(slug)
                if isinstance(cur, dict):
                    cur.update(block)
                    overlay[slug] = cur
                else:
                    overlay[slug] = block
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(
                json.dumps(overlay, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            print("Updated overlay {}".format(out_path.relative_to(root)))

    if args.write_places:
        for path, places in file_places.items():
            path.write_text(
                json.dumps(places, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            print("Updated {}".format(path.relative_to(root)))

    print("Applied {} translations (skipped {}).".format(applied, skipped))
    return 0 if applied else 1


if __name__ == "__main__":
    raise SystemExit(main())
