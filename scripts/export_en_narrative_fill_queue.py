# -*- coding: utf-8 -*-
"""
Export EN places missing narrative for Google Colab LLM fill.

Each job prompts for historical, political, cultural, and religious
significance (mapped to description_en, history_en, significance_en, facts).

Writes under ``translations/``:

- ``queue/en_narrative_fill.jsonl`` — full jobs (prompt + metadata)
- ``collab/en_narrative_fill.json`` — ``[{"id","prompt"}, ...]`` for Colab
- ``meta/en_narrative_fill_summary.json`` — counts per city

Apply results manually or extend ``apply_guide_translation_results.py``.

Usage::

  python scripts/export_en_narrative_fill_queue.py
  python scripts/export_en_narrative_fill_queue.py --cities dubai prague
  python scripts/list_en_narrative_gaps.py
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

from scripts.en_narrative_fill_queue import (
    discover_cities,
    iter_en_narrative_fill_jobs,
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
        help="Also write collab/en_narrative_fill_<city>.json per city.",
    )
    args = parser.parse_args()
    root = args.project_root.resolve()
    cities = args.cities if args.cities else discover_cities(root)
    if not cities:
        print("No cities found.", file=sys.stderr)
        return 2

    jobs: list[dict] = []
    by_city: dict[str, int] = {}
    by_city_jobs: dict[str, list[dict]] = {}
    llm_generate = 0
    translate_hint = 0
    for city in cities:
        city_jobs = list(iter_en_narrative_fill_jobs(root, city))
        by_city[city] = len(city_jobs)
        by_city_jobs[city] = city_jobs
        for job in city_jobs:
            if job.get("has_ru_source"):
                translate_hint += 1
            else:
                llm_generate += 1
        jobs.extend(city_jobs)

    out = args.out_dir.resolve()
    queue_path = out / "queue" / "en_narrative_fill.jsonl"
    collab_path = out / "collab" / "en_narrative_fill.json"
    summary_path = out / "meta" / "en_narrative_fill_summary.json"

    write_jsonl(queue_path, jobs)
    collab_path.parent.mkdir(parents=True, exist_ok=True)
    collab_path.write_text(
        json.dumps(
            [{"id": j["id"], "prompt": j["prompt"]} for j in jobs],
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_jobs": len(jobs),
        "llm_generate_en": llm_generate,
        "has_ru_source_alternative": translate_hint,
        "by_city": by_city,
    }
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    if args.split_by_city:
        collab_dir = collab_path.parent
        for city, city_jobs in by_city_jobs.items():
            if not city_jobs:
                continue
            city_path = collab_dir / "en_narrative_fill_{}.json".format(city)
            city_path.write_text(
                json.dumps(
                    [{"id": j["id"], "prompt": j["prompt"]} for j in city_jobs],
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

    print("EN narrative gaps: {} place(s) in {} cities".format(
        len(jobs), len([c for c, n in by_city.items() if n]),
    ))
    print("  LLM generate (no RU source): {}".format(llm_generate))
    print("  Has RU source (translate or regenerate): {}".format(
        translate_hint,
    ))
    print("Written: {}".format(queue_path))
    print("Colab:   {}".format(collab_path))
    print("Notebook: translations/collab/en_narrative_fill_colab.ipynb")
    print("Summary: {}".format(summary_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
