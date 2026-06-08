# -*- coding: utf-8 -*-
"""Remove Pixabay filler phrases and URLs from place JSON narrative fields."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_core import is_substantive_text
from scripts.city_guide_narrative import (
    clean_pixabay_artifacts,
    is_pixabay_stub,
)
from scripts.city_guide_registry_common import pdf_expand_sidecar_paths

_TEXT_KEYS = (
    "description",
    "description_en",
    "description_ru",
    "history",
    "history_en",
    "history_ru",
    "significance",
    "significance_en",
    "significance_ru",
)
_LIST_KEYS = (
    "facts",
    "facts_en",
    "facts_ru",
    "stories",
    "stories_en",
    "stories_ru",
)


def _scrub_text(value: str) -> str | None:
    """Return cleaned text, or None to drop the field."""
    raw = str(value).strip()
    if not raw:
        return None
    if is_pixabay_stub(raw):
        return None
    cleaned = clean_pixabay_artifacts(raw)
    if not cleaned or not is_substantive_text(cleaned):
        return None
    return cleaned


def _scrub_list(items: list[Any]) -> list[str] | None:
    out: list[str] = []
    for item in items:
        text = _scrub_text(str(item))
        if text:
            out.append(text)
    return out if out else None


def scrub_place(place: dict[str, Any]) -> bool:
    """Mutate *place*; return True when anything changed."""
    changed = False
    for key in _TEXT_KEYS:
        if key not in place:
            continue
        cleaned = _scrub_text(str(place.get(key) or ""))
        if cleaned is None:
            if place.pop(key, None) is not None:
                changed = True
        elif cleaned != str(place.get(key) or "").strip():
            place[key] = cleaned
            changed = True
    for key in _LIST_KEYS:
        raw = place.get(key)
        if not isinstance(raw, list):
            continue
        cleaned = _scrub_list(raw)
        if cleaned is None:
            if place.pop(key, None) is not None:
                changed = True
        elif cleaned != raw:
            place[key] = cleaned
            changed = True
    return changed


def _place_files(data_dir: Path, city_slug: str) -> list[Path]:
    paths: list[Path] = []
    main = data_dir / "{}_places.json".format(city_slug)
    if main.is_file():
        paths.append(main)
    paths.extend(pdf_expand_sidecar_paths(data_dir, city_slug))
    return paths


def scrub_city(project_root: Path, city_slug: str, *, dry_run: bool) -> int:
    data_dir = project_root / city_slug / "data"
    places_changed = 0
    for path in _place_files(data_dir, city_slug):
        raw = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            continue
        file_changed = False
        for place in raw:
            if not isinstance(place, dict):
                continue
            if scrub_place(place):
                places_changed += 1
                file_changed = True
        if file_changed and not dry_run:
            path.write_text(
                json.dumps(raw, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
    return places_changed


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
        "--dry-run",
        action="store_true",
        help="Report counts without writing JSON.",
    )
    args = parser.parse_args()
    root = args.project_root.resolve()
    if args.cities:
        cities = list(args.cities)
    else:
        cities = sorted(
            p.parent.parent.name
            for p in root.glob("*/data/*_places.json")
        )
    total = 0
    for city in cities:
        n = scrub_city(root, city, dry_run=args.dry_run)
        if n:
            print("{}: {} place(s)".format(city, n))
            total += n
    mode = "would scrub" if args.dry_run else "scrubbed"
    print("Total {}: {} place(s) in {} cities".format(
        mode, total, len(cities),
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
