# -*- coding: utf-8 -*-
"""Merge EN/RU narrative and image fields across place JSON sources."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from scripts.city_guide_core import is_substantive_text, place_has_pdf_image
from scripts.city_guide_narrative import (
    is_usable_narrative_text,
    text_for_edition,
)

_PROSE_BASES = ("description", "history", "significance")
_LIST_BASES = ("facts", "stories")
_IMAGE_KEYS = (
    "image_rel_path",
    "image_source_url",
    "additional_images",
    "suppress_images_for_pdf",
    "license_note",
    "attribution",
)
_META_KEYS = (
    "address",
    "year_built",
    "architecture_style",
    "category",
    "name_ru",
    "name_en",
    "subtitle_en",
    "subtitle_ru",
)


def detail_key_for_slug(
    city_slug: str,
    slug: str,
    detail_keys: set[str],
) -> str | None:
    """Match main slug to ``*_place_details.json`` key (with/without prefix)."""
    if slug in detail_keys:
        return slug
    prefixed = "{}_{}".format(city_slug, slug)
    if prefixed in detail_keys:
        return prefixed
    prefix = "{}_".format(city_slug)
    if slug.startswith(prefix):
        short = slug[len(prefix):]
        if short in detail_keys:
            return short
    return None


def _edition_of_text(text: str) -> str | None:
    if not is_substantive_text(text):
        return None
    if text_for_edition(text, "en"):
        return "en"
    if text_for_edition(text, "ru"):
        return "ru"
    return None


def _target_key(base: str, edition: str) -> str:
    return "{}_{}".format(base, edition)


def _prose_candidates(
    place: Mapping[str, Any],
    detail: Mapping[str, Any],
    base: str,
) -> list[tuple[str, str]]:
    """(edition, text) pairs from place row and detail overlay."""
    out: list[tuple[str, str]] = []
    keys = (
        base,
        "{}_en".format(base),
        "{}_ru".format(base),
    )
    for src in (place, detail):
        for key in keys:
            raw = str(src.get(key) or "").strip()
            if not raw:
                continue
            edition = _edition_of_text(raw)
            if edition and is_usable_narrative_text(raw):
                out.append((edition, raw))
    return out


def _list_candidates(
    place: Mapping[str, Any],
    detail: Mapping[str, Any],
    base: str,
) -> list[tuple[str, list[str]]]:
    out: list[tuple[str, list[str]]] = []
    keys = (
        base,
        "{}_en".format(base),
        "{}_ru".format(base),
    )
    for src in (place, detail):
        for key in keys:
            raw = src.get(key)
            if not isinstance(raw, list):
                continue
            en_items: list[str] = []
            ru_items: list[str] = []
            for item in raw:
                text = str(item).strip()
                if not is_usable_narrative_text(text):
                    continue
                if text_for_edition(text, "en"):
                    en_items.append(text)
                elif text_for_edition(text, "ru"):
                    ru_items.append(text)
            if en_items:
                out.append(("en", en_items))
            if ru_items:
                out.append(("ru", ru_items))
    return out


def _pick_longer_prose(
    candidates: list[tuple[str, str]],
) -> dict[str, str]:
    best: dict[str, str] = {}
    for edition, text in candidates:
        cur = best.get(edition, "")
        if len(text) > len(cur):
            best[edition] = text
    return best


def _pick_richer_list(
    candidates: list[tuple[str, list[str]]],
) -> dict[str, list[str]]:
    best: dict[str, list[str]] = {}
    for edition, items in candidates:
        cur = best.get(edition, [])
        cur_len = sum(len(x) for x in cur)
        new_len = sum(len(x) for x in items)
        if new_len > cur_len:
            best[edition] = items
    return best


def edition_narrative_chars(place: Mapping[str, Any], edition: str) -> int:
    total = 0
    for base in _PROSE_BASES:
        for key in (_target_key(base, edition), base):
            raw = str(place.get(key) or "").strip()
            if raw and text_for_edition(raw, edition):
                total += len(raw)
    list_key = (
        "facts" if edition == "en" else "facts_ru"
    )
    for key in (list_key, "facts", "facts_en", "facts_ru"):
        raw = place.get(key)
        if not isinstance(raw, list):
            continue
        for item in raw:
            text = str(item).strip()
            if text and text_for_edition(text, edition):
                total += len(text)
    return total


def merge_image_fields(
    target: dict[str, Any],
    source: Mapping[str, Any],
) -> bool:
    """Copy image-related keys from *source* when *target* lacks them."""
    changed = False
    for key in _IMAGE_KEYS:
        if target.get(key) not in (None, "", [], {}):
            continue
        val = source.get(key)
        if val in (None, "", [], {}):
            continue
        target[key] = val
        changed = True
    return changed


def merge_meta_fields(
    target: dict[str, Any],
    source: Mapping[str, Any],
) -> bool:
    changed = False
    for key in _META_KEYS:
        if is_substantive_text(str(target.get(key) or "")):
            continue
        val = source.get(key)
        if val in (None, "", [], {}):
            continue
        target[key] = val
        changed = True
    return changed


def reconcile_place_row(
    place: dict[str, Any],
    detail: Mapping[str, Any] | None,
) -> bool:
    """
    Normalize narrative into ``*_en`` / ``*_ru`` keys from place + detail.

    Richer edition text wins per field; does not translate across languages.
    """
    detail = detail or {}
    changed = False
    if merge_image_fields(place, detail):
        changed = True
    if merge_meta_fields(place, detail):
        changed = True

    for base in _PROSE_BASES:
        picked = _pick_longer_prose(_prose_candidates(place, detail, base))
        for edition, text in picked.items():
            key = _target_key(base, edition)
            if str(place.get(key) or "").strip() != text:
                place[key] = text
                changed = True

    for base in _LIST_BASES:
        picked = _pick_richer_list(_list_candidates(place, detail, base))
        for edition, items in picked.items():
            key = _target_key(base, edition)
            if place.get(key) != items:
                place[key] = items
                changed = True

    for base in _PROSE_BASES:
        en_key = _target_key(base, "en")
        en_text = str(place.get(en_key) or "").strip()
        if en_text and text_for_edition(en_text, "en"):
            if str(place.get(base) or "").strip() != en_text:
                place[base] = en_text
                changed = True

    en_facts = place.get("facts_en") or []
    if isinstance(en_facts, list) and en_facts:
        if place.get("facts") != en_facts:
            place["facts"] = list(en_facts)
            changed = True

    return changed


def load_place_details(data_dir: Path, city_slug: str) -> dict[str, dict]:
    merged: dict[str, dict] = {}
    pattern = "{}_place_details*.json".format(city_slug)
    for path in sorted(data_dir.glob(pattern)):
        blob = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(blob, dict):
            merged.update(blob)
    return merged


def reconcile_city_places(
    project_root: Path,
    city_slug: str,
    *,
    dry_run: bool = False,
) -> dict[str, int]:
    """
    Reconcile main ``*_places.json`` with detail overlays.

    Image/place rows come from the main registry (more places with images).
    Text is merged from whichever source has richer EN or RU per field.
    """
    data_dir = project_root / city_slug / "data"
    main_path = data_dir / "{}_places.json".format(city_slug)
    if not main_path.is_file():
        return {"places": 0, "changed": 0, "en_chars": 0, "ru_chars": 0}

    places: list[dict[str, Any]] = json.loads(
        main_path.read_text(encoding="utf-8"),
    )
    details = load_place_details(data_dir, city_slug)
    detail_keys = set(details)
    city_root = project_root / city_slug

    with_images = [
        p for p in places
        if place_has_pdf_image(city_root, p)
    ]
    without_images = [
        p for p in places
        if not place_has_pdf_image(city_root, p)
    ]
    use_image_source = len(with_images) >= len(without_images)
    canonical = with_images if use_image_source else places

    changed = 0
    en_chars = 0
    ru_chars = 0
    for place in canonical:
        if not isinstance(place, dict):
            continue
        slug = str(place.get("slug") or "").strip()
        if not slug:
            continue
        dkey = detail_key_for_slug(city_slug, slug, detail_keys)
        detail = details.get(dkey or "", {})
        if reconcile_place_row(place, detail):
            changed += 1
        en_chars += edition_narrative_chars(place, "en")
        ru_chars += edition_narrative_chars(place, "ru")

    if changed and not dry_run:
        by_slug = {str(p.get("slug") or ""): p for p in canonical}
        out_rows: list[dict[str, Any]] = []
        for row in places:
            slug = str(row.get("slug") or "")
            out_rows.append(by_slug.get(slug, row))
        main_path.write_text(
            json.dumps(out_rows, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    return {
        "places": len(canonical),
        "changed": changed,
        "en_chars": en_chars,
        "ru_chars": ru_chars,
        "image_source": "main_with_images" if use_image_source else "main_all",
    }
