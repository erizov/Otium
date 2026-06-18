# -*- coding: utf-8 -*-
"""Merge missing Moscow unified-guide places using existing data only."""

from __future__ import annotations

import json
import re
import shutil
import sys
from html import unescape
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_core import (
    MIN_IMAGE_BYTES,
    place_has_pdf_image,
    smallest_same_stem_image_rel,
)
from scripts.extract_moscow_complete_pdf_images import _parse_complete_sections

_MOSCOW = _PROJECT_ROOT / "moscow"
_PLACES_PATH = _MOSCOW / "data" / "moscow_places.json"
_MISSING_PATH = _MOSCOW / "data" / "moscow_pdf_missing_from_unified.json"
_COMPLETE_HTML = _MOSCOW / "output" / "Moscow_Complete_Guide.html"


def _norm(name: str) -> str:
    s = unescape(name or "").strip().lower()
    s = re.sub(r"^\d+\.\s*", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.replace("ё", "е")


def _build_lookup(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    by_norm: dict[str, dict[str, Any]] = {}
    for row in rows:
        for key in ("name_ru", "name_en", "name"):
            n = _norm(str(row.get(key) or ""))
            if n:
                by_norm[n] = row
    return by_norm


def _match_title(
    title: str,
    by_norm: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    cn = _norm(title)
    if cn in by_norm:
        return by_norm[cn]
    best: dict[str, Any] | None = None
    best_len = 0
    for jn, place in by_norm.items():
        if cn in jn or jn in cn:
            overlap = min(len(cn), len(jn))
            if overlap > best_len:
                best_len = overlap
                best = place
    return best


def _resolve_existing_rel(moscow_root: Path, rel: str) -> str | None:
    rel = rel.lstrip("/").replace("\\", "/")
    if rel.startswith("images/"):
        candidate = moscow_root / rel
    else:
        candidate = moscow_root / "images" / rel
    if candidate.is_file() and candidate.stat().st_size >= MIN_IMAGE_BYTES:
        return "images/" + candidate.relative_to(moscow_root / "images").as_posix()
    chosen = smallest_same_stem_image_rel(moscow_root, rel)
    if chosen:
        return chosen
    return None


def _wire_image_from_complete(
    place: dict[str, Any],
    complete_index: dict[str, list[str]],
    by_norm: dict[str, dict[str, Any]],
) -> bool:
    name = str(place.get("name_ru") or place.get("name") or "").strip()
    rels = complete_index.get(_norm(name)) or []
    for rel in rels:
        resolved = _resolve_existing_rel(_MOSCOW, rel)
        if resolved:
            place["image_rel_path"] = resolved
            return True
    return False


def _wire_image_from_stem(place: dict[str, Any]) -> bool:
    rel = str(place.get("image_rel_path") or "")
    if not rel:
        return False
    resolved = _resolve_existing_rel(_MOSCOW, rel)
    if resolved and resolved != rel:
        place["image_rel_path"] = resolved
    return bool(resolved and place_has_pdf_image(_MOSCOW, place))


def merge_missing_moscow_unified_places(
    *,
    dry_run: bool = False,
) -> dict[str, int]:
    rows: list[dict[str, Any]] = json.loads(
        _PLACES_PATH.read_text(encoding="utf-8"),
    )
    by_slug = {str(p.get("slug")): p for p in rows}
    missing = json.loads(_MISSING_PATH.read_text(encoding="utf-8")).get(
        "missing",
        [],
    )
    complete_index: dict[str, list[str]] = {}
    if _COMPLETE_HTML.is_file():
        complete_index = _parse_complete_sections(_COMPLETE_HTML)
    by_norm = _build_lookup(rows)

    stats = {
        "missing_total": len(missing),
        "already_had_image": 0,
        "wired_from_complete": 0,
        "wired_from_stem": 0,
        "still_no_image": 0,
    }

    for item in missing:
        slug = str(item.get("slug") or "")
        place = by_slug.get(slug)
        if place is None:
            continue
        if place_has_pdf_image(_MOSCOW, place):
            stats["already_had_image"] += 1
            continue
        if _wire_image_from_complete(place, complete_index, by_norm):
            stats["wired_from_complete"] += 1
            continue
        if _wire_image_from_stem(place):
            stats["wired_from_stem"] += 1
            continue
        stats["still_no_image"] += 1

    if not dry_run:
        _PLACES_PATH.write_text(
            json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return stats


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    stats = merge_missing_moscow_unified_places(dry_run=args.dry_run)
    print(json.dumps(stats, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
