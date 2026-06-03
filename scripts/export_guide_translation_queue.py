# -*- coding: utf-8 -*-
"""
Export EN↔RU translation jobs for Google Colab (or any batch translator).

Writes under ``translations/``:

- ``queue/queue.jsonl`` — full job metadata (apply step reads this)
- ``collab/en_to_ru.json`` — ``[{"id","text"}, ...]``
- ``collab/ru_to_en.json`` — same for RU→EN
- ``collab/en_to_ru.jsonl`` / ``ru_to_en.jsonl`` — one row per line (large files)

Usage::

  python scripts/export_guide_translation_queue.py
  python scripts/export_guide_translation_queue.py --cities chernivtsi prague
  python scripts/export_guide_translation_queue.py --split-by-city
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.guide_translation_queue import (
    collab_arrays_from_jobs,
    discover_cities,
    iter_translation_jobs,
    ru_slug_title_jobs,
    write_jsonl,
)


def main() -> int:
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
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=_PROJECT_ROOT / "translations",
    )
    parser.add_argument(
        "--split-by-city",
        action="store_true",
        help="Also write per-city queue + collab JSON under queue/by_city/.",
    )
    parser.add_argument(
        "--include-slug-titles",
        action="store_true",
        help="Add name_ru jobs when RU title is a slug but EN name exists.",
    )
    args = parser.parse_args()
    root = args.project_root.resolve()
    cities = args.cities if args.cities else discover_cities(root)
    if not cities:
        print("No cities found.", file=sys.stderr)
        return 2

    out = args.out_dir.resolve()
    queue_dir = out / "queue"
    collab_dir = out / "collab"
    jobs: list[dict] = []
    for city in cities:
        city_jobs = list(iter_translation_jobs(root, city))
        if args.include_slug_titles:
            city_jobs.extend(ru_slug_title_jobs(root, city))
        jobs.extend(city_jobs)
        if args.split_by_city and city_jobs:
            write_jsonl(queue_dir / "by_city" / "{}.jsonl".format(city), city_jobs)
            e2r, r2e = collab_arrays_from_jobs(city_jobs)
            by = collab_dir / "by_city"
            by.mkdir(parents=True, exist_ok=True)
            (by / "{}_en_to_ru.json".format(city)).write_text(
                json.dumps(e2r, ensure_ascii=False, indent=0),
                encoding="utf-8",
            )
            (by / "{}_ru_to_en.json".format(city)).write_text(
                json.dumps(r2e, ensure_ascii=False, indent=0),
                encoding="utf-8",
            )

    write_jsonl(queue_dir / "queue.jsonl", jobs)
    en_to_ru, ru_to_en = collab_arrays_from_jobs(jobs)
    collab_dir.mkdir(parents=True, exist_ok=True)
    (collab_dir / "en_to_ru.json").write_text(
        json.dumps(en_to_ru, ensure_ascii=False),
        encoding="utf-8",
    )
    (collab_dir / "ru_to_en.json").write_text(
        json.dumps(ru_to_en, ensure_ascii=False),
        encoding="utf-8",
    )
    write_jsonl(collab_dir / "en_to_ru.jsonl", en_to_ru)
    write_jsonl(collab_dir / "ru_to_en.jsonl", ru_to_en)

    meta = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cities": cities,
        "job_count": len(jobs),
        "en_to_ru_count": len(en_to_ru),
        "ru_to_en_count": len(ru_to_en),
    }
    (out / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        "Wrote {} jobs (EN->RU: {}, RU->EN: {}) to {}".format(
            len(jobs),
            len(en_to_ru),
            len(ru_to_en),
            out,
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
