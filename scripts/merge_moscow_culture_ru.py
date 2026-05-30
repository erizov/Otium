# -*- coding: utf-8 -*-
"""Merge culture.ru catalog rows into moscow_places.json (images + source URL)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

_STOPWORDS = frozenset(
    {
        "москва",
        "московский",
        "московская",
        "здание",
        "проект",
        "ныне",
        "им",
        "имени",
        "г",
        "года",
        "в",
        "на",
        "и",
        "the",
    },
)


def _norm_name(value: str) -> str:
    s = value.strip().lower().replace("ё", "е")
    s = re.sub(r"\([^)]*\)", " ", s)
    s = re.sub(r"«[^»]*»", " ", s)
    s = re.sub(r"[^a-zа-я0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _tokens(value: str) -> set[str]:
    return {t for t in _norm_name(value).split() if t and t not in _STOPWORDS}


def _token_score(title: str, place_name: str) -> float:
    a, b = _tokens(title), _tokens(place_name)
    if not a or not b:
        return 0.0
    inter = len(a & b)
    if inter < 2 and not (a <= b or b <= a):
        return 0.0
    return inter / len(a | b)


def _best_match(
    title: str,
    title_norm: str,
    places: list[dict[str, Any]],
    used_slugs: set[str],
) -> dict[str, Any] | None:
    if not title_norm:
        return None
    exact = [
        p
        for p in places
        if _norm_name(str(p.get("name_ru") or "")) == title_norm
        and str(p.get("slug") or "") not in used_slugs
    ]
    if len(exact) == 1:
        return exact[0]
    partial: list[tuple[float, dict[str, Any]]] = []
    for p in places:
        slug = str(p.get("slug") or "")
        if slug in used_slugs:
            continue
        name = str(p.get("name_ru") or "")
        name_norm = _norm_name(name)
        if not name_norm:
            continue
        if title_norm in name_norm or name_norm in title_norm:
            partial.append((0.95, p))
            continue
        score = _token_score(title, name)
        if score >= 0.45:
            partial.append((score, p))
    if not partial:
        return None
    partial.sort(key=lambda x: x[0], reverse=True)
    best_score, best = partial[0]
    if len(partial) > 1 and partial[1][0] >= best_score - 0.05:
        return None
    return best


def _culture_ru_slug(row: dict[str, Any]) -> str:
    cid = row.get("culture_ru_id")
    return "moscow_culture_ru_{}".format(cid if cid is not None else "unknown")


def _append_row(
    places: list[dict[str, Any]],
    row: dict[str, Any],
) -> dict[str, Any]:
    slug = _culture_ru_slug(row)
    rel = "images/moscow_culture_ru/{}.jpg".format(slug)
    place: dict[str, Any] = {
        "slug": slug,
        "category": "culture_ru_architecture",
        "name_ru": str(row.get("name_ru") or "").strip(),
        "name_en": "",
        "subtitle_en": str(row.get("address") or "").strip(),
        "history": (
            "Архитектурный объект из каталога «Культура.РФ» "
            "(Москва). Подробности — на странице источника."
        ),
        "significance": "",
        "facts": [],
        "architecture_style": "",
        "address": str(row.get("address") or "").strip(),
        "image_rel_path": rel,
        "image_source_url": str(row.get("image_source_url") or "").strip(),
        "culture_ru_url": str(row.get("page_url") or "").strip(),
        "license_note": "See culture.ru institute page for media terms.",
        "attribution": "Культура.РФ (culture.ru)",
        "lat": row.get("lat"),
        "lon": row.get("lon"),
    }
    places.append(place)
    return place


def _apply_row(hit: dict[str, Any], row: dict[str, Any]) -> bool:
    changed = False
    img = str(row.get("image_source_url") or "").strip()
    page = str(row.get("page_url") or "").strip()
    if img and not hit.get("image_source_url"):
        hit["image_source_url"] = img
        changed = True
    if page:
        if hit.get("culture_ru_url") != page:
            hit["culture_ru_url"] = page
            changed = True
    if not hit.get("license_note"):
        hit["license_note"] = "See culture.ru institute page for media terms."
        changed = True
    if not hit.get("attribution"):
        hit["attribution"] = "Культура.РФ (culture.ru)"
        changed = True
    addr = str(row.get("address") or "").strip()
    if addr and not str(hit.get("address") or "").strip():
        hit["address"] = addr
        changed = True
    lat, lon = row.get("lat"), row.get("lon")
    if lat is not None and hit.get("lat") is None:
        hit["lat"] = lat
        changed = True
    if lon is not None and hit.get("lon") is None:
        hit["lon"] = lon
        changed = True
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--catalog",
        type=Path,
        default=_PROJECT_ROOT / "moscow" / "data" / "moscow_culture_ru_catalog.json",
    )
    parser.add_argument(
        "--places",
        type=Path,
        default=_PROJECT_ROOT / "moscow" / "data" / "moscow_places.json",
    )
    parser.add_argument(
        "--append-unmatched",
        action="store_true",
        help="Add catalog rows with no place match as new guide entries.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
    )
    args = parser.parse_args()

    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    places = json.loads(args.places.read_text(encoding="utf-8"))
    used_slugs: set[str] = set()
    matched = 0
    updated = 0
    appended = 0
    for row in catalog:
        title = str(row.get("name_ru") or "")
        title_norm = str(row.get("name_norm") or "") or _norm_name(title)
        hit = _best_match(title, title_norm, places, used_slugs)
        if hit:
            matched += 1
            used_slugs.add(str(hit.get("slug") or ""))
            if _apply_row(hit, row):
                updated += 1
            continue
        if args.append_unmatched and row.get("image_source_url"):
            _append_row(places, row)
            appended += 1

    print(
        "catalog={} matched={} updated={} appended={}".format(
            len(catalog),
            matched,
            updated,
            appended,
        ),
    )
    if args.dry_run:
        return 0
    args.places.write_text(
        json.dumps(places, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("Written", args.places)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
