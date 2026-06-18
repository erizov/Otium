# -*- coding: utf-8 -*-
"""Audit address/schedule expectations vs moscow_places.json."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_place_meta import (
    ADDRESS_EXPECTED,
    ADDRESS_OPTIONAL,
    SCHEDULE_EXPECTED,
    pick_street_address,
    pick_visit_hours,
    place_category,
)

# Open-air or always-accessible; no fixed hours unless a museum on site.
SCHEDULE_OPTIONAL: frozenset[str] = frozenset({
    "bridges",
    "cemeteries",
    "landmarks",
    "metro",
    "monasteries",
    "osobnjaki",
    "palaces",
    "parks",
    "places",
    "places_of_worship",
    "railway_stations",
    "sculptures",
    "squares",
    "viewpoints",
    "buildings",
})

SCHEDULE_KEYS = (
    "hours",
    "hours_ru",
    "hours_en",
    "opening_hours",
    "schedule",
    "schedule_ru",
    "schedule_en",
    "visit_hours",
)

HOURS_HINT_RE = (
    "режим",
    "часы работы",
    "opening hours",
    "open daily",
    "closed mon",
    "ticket",
    "билет",
    "10:",
    "11:",
    "09:",
    "–",
    "—",
)


def _has_schedule(place: dict) -> bool:
    if pick_visit_hours(place, "ru") or pick_visit_hours(place, "en"):
        return True
    for key in SCHEDULE_KEYS:
        if str(place.get(key) or "").strip():
            return True
    for key in ("facts", "facts_en", "stories", "stories_en", "stories_ru"):
        raw = place.get(key)
        if not isinstance(raw, list):
            continue
        for item in raw:
            low = str(item).lower()
            if any(h in low for h in HOURS_HINT_RE):
                return True
    desc = " ".join(
        str(place.get(k) or "")
        for k in ("description", "description_en", "significance", "history")
    ).lower()
    return any(h in desc for h in ("opening hours", "часы работы", "режим работы"))


def audit(city_slug: str) -> dict:
    path = _PROJECT_ROOT / city_slug / "data" / f"{city_slug}_places.json"
    places = json.loads(path.read_text(encoding="utf-8"))
    by_cat: dict[str, dict[str, int]] = defaultdict(
        lambda: {
            "total": 0,
            "has_address": 0,
            "missing_address": 0,
            "unexpected_address": 0,
            "has_schedule": 0,
            "missing_schedule": 0,
            "unexpected_schedule": 0,
        },
    )
    issues: list[str] = []
    for p in places:
        cat = place_category(p)
        slug = str(p.get("slug") or "?")
        name = str(p.get("name_ru") or p.get("name_en") or slug)
        by_cat[cat]["total"] += 1
        addr = pick_street_address(p)
        sched = _has_schedule(p)
        if addr:
            by_cat[cat]["has_address"] += 1
            if cat in ADDRESS_OPTIONAL:
                by_cat[cat]["unexpected_address"] += 1
                issues.append(
                    f"address_on_optional:{slug}:{name[:40]}",
                )
        else:
            by_cat[cat]["missing_address"] += 1
            if cat in ADDRESS_EXPECTED:
                issues.append(f"missing_address:{slug}:{name[:40]}")
        if sched:
            by_cat[cat]["has_schedule"] += 1
            if cat not in SCHEDULE_EXPECTED:
                by_cat[cat]["unexpected_schedule"] += 1
        else:
            by_cat[cat]["missing_schedule"] += 1
            if cat in SCHEDULE_EXPECTED:
                issues.append(f"missing_schedule:{slug}:{name[:40]}")
    return {
        "city": city_slug,
        "places": len(places),
        "by_category": dict(sorted(by_cat.items())),
        "issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--city", default="moscow")
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    report = audit(args.city)
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
        print("Wrote", args.out)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
