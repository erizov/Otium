# -*- coding: utf-8 -*-
"""Build russian_arhitecture_places.json and link local images."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from russian_arhitecture.data.image_overrides import (  # noqa: E402
    apply_image_url_overrides,
)
from russian_arhitecture.data.place_narratives import (  # noqa: E402
    apply_narrative_overrides,
)
from russian_arhitecture.data.guide_image_policy import (  # noqa: E402
    strip_extra_images,
)
from russian_arhitecture.data.city_places_index import (  # noqa: E402
    load_city_index,
)
from russian_arhitecture.data.image_reuse import (  # noqa: E402
    attach_from_city_ref,
    link_additional_images,
    prune_missing_additional_images,
    strip_internal_image_keys,
)
from russian_arhitecture.data.guide_exclusions import (  # noqa: E402
    is_catalog_suffix_excluded,
    is_slug_excluded,
    pool_for_style,
)
from russian_arhitecture.data.style_catalog import (  # noqa: E402
    STYLE_EXAMPLES,
    STYLE_META,
    STYLE_ORDER,
)
from russian_arhitecture.data.style_targets import (  # noqa: E402
    style_example_target,
)

MIN_IMAGE_BYTES = 500
_LICENSE = "See Wikimedia Commons file page for license."
_ATTRIBUTION = "Wikimedia Commons contributors"


def _slug(style_key: str, suffix: str) -> str:
    return "{}_{}".format(style_key, suffix)


def _image_rel(slug: str) -> str:
    return "images/styles/{}.jpg".format(slug)


def _style_title(style_key: str, edition: str) -> str:
    meta = STYLE_META[style_key]
    return meta[0] if edition == "ru" else meta[1]


def _style_intro(style_key: str, edition: str) -> str:
    meta = STYLE_META[style_key]
    return meta[2] if edition == "ru" else meta[3]


def _normalize_name(name: str) -> str:
    return re.sub(r"\s+", " ", name.strip().lower())


def _unique_suffix(base: str, used: set[str]) -> str:
    slug_base = re.sub(r"[^a-z0-9_]+", "_", base.lower()).strip("_")
    if not slug_base:
        slug_base = "example"
    if len(slug_base) > 48:
        slug_base = slug_base[:48]
    candidate = slug_base
    counter = 2
    while candidate in used:
        candidate = "{}_{}".format(slug_base, counter)
        counter += 1
    used.add(candidate)
    return candidate


_BUILDING_TYPE_STYLES = frozenset({
    "телебашня",
    "телебашня, смотровая",
})


_STYLE_KEYWORDS = (
    "конструктив",
    "модерн",
    "ампир",
    "неокласс",
    "стиль",
    "русс",
    "барокко",
    "классиц",
    "готик",
    "эклект",
)


def _sidecar_architect(city_style: str, style_key: str) -> str:
    """Return architect name from sidecar when it is not a style label."""
    raw = city_style.strip()
    if not raw:
        return ""
    low = raw.lower()
    if low in _BUILDING_TYPE_STYLES:
        return ""
    chapter = _style_title(style_key, "ru").lower()
    if raw.lower() == chapter:
        return ""
    if any(k in low for k in _STYLE_KEYWORDS):
        return ""
    return raw


def _ex_from_city(
    city_ref: str,
    city_row: dict[str, Any],
    *,
    suffix: str,
) -> dict[str, Any]:
    city = str(city_row["city"])
    return {
        "suffix": suffix,
        "name_ru": city_row["name_ru"],
        "name_en": city_row["name_en"] or city_row["name_ru"],
        "year": city_row.get("year_built") or "",
        "city_ru": city_row.get("address") or city,
        "city_en": city_row.get("address") or city,
        "history_ru": city_row.get("history_ru") or "",
        "history_en": city_row.get("history_en") or "",
        "significance_ru": city_row.get("significance_ru") or "",
        "significance_en": city_row.get("significance_en") or "",
        "city_style": city_row.get("architecture_style") or "",
        "commons_url": city_row.get("image_source_url") or "",
        "_city_ref": city_ref,
    }


def _collect_style_examples(
    style_key: str,
    city_index: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    target = style_example_target(style_key)
    examples: list[dict[str, Any]] = []
    used_suffixes: set[str] = set()
    seen_city_refs: set[str] = set()
    seen_names: set[str] = set()

    def _try_add(ex: dict[str, Any]) -> bool:
        if len(examples) >= target:
            return False
        city_ref = str(ex.get("_city_ref") or "").strip()
        if city_ref:
            if city_ref in seen_city_refs:
                return False
            seen_city_refs.add(city_ref)
        name_key = _normalize_name(str(ex.get("name_ru") or ""))
        if name_key and name_key in seen_names:
            return False
        if name_key:
            seen_names.add(name_key)
        suffix = str(ex.get("suffix") or "").strip()
        if not suffix or suffix in used_suffixes:
            suffix = _unique_suffix(
                city_ref.split(":", 1)[-1] if city_ref else name_key,
                used_suffixes,
            )
        else:
            used_suffixes.add(suffix)
        ex = dict(ex)
        ex["suffix"] = suffix
        examples.append(ex)
        return len(examples) < target

    for ex in STYLE_EXAMPLES.get(style_key, []):
        suffix = str(ex.get("suffix") or "").strip()
        if suffix and is_catalog_suffix_excluded(suffix):
            continue
        seed = dict(ex)
        _try_add(seed)

    for city, place_slug in pool_for_style(style_key):
        if len(examples) >= target:
            break
        city_ref = "{}:{}".format(city, place_slug)
        if city_ref in seen_city_refs:
            continue
        city_row = city_index.get(city_ref)
        if not city_row:
            continue
        suffix = _unique_suffix(place_slug, used_suffixes)
        _try_add(_ex_from_city(city_ref, city_row, suffix=suffix))

    return examples


def _description_ru(ex: dict[str, Any], style_key: str) -> str:
    parts: list[str] = []
    hist = str(ex.get("history_ru") or "").strip()
    if hist:
        parts.append(hist)
    sig = str(ex.get("significance_ru") or "").strip()
    if sig:
        parts.append(sig)
    if not parts:
        return ""
    return " ".join(parts)


def _description_en(ex: dict[str, Any], style_key: str) -> str:
    parts: list[str] = []
    hist = str(ex.get("history_en") or ex.get("history_ru") or "").strip()
    if hist:
        parts.append(hist)
    sig = str(ex.get("significance_en") or ex.get("significance_ru") or "").strip()
    if sig:
        parts.append(sig)
    if not parts:
        return ""
    return " ".join(parts)


def _facts_ru(ex: dict[str, Any], style_key: str) -> list[str]:
    facts: list[str] = []
    arch = str(ex.get("architect_ru") or "").strip()
    if arch:
        facts.append("Архитектор: {}.".format(arch))
    year = str(ex.get("year") or "").strip()
    if year:
        facts.append("Период: {}.".format(year))
    city = str(ex.get("city_ru") or "").strip()
    if city:
        facts.append("Город: {}.".format(city))
    return facts


def _facts_en(ex: dict[str, Any], style_key: str) -> list[str]:
    facts: list[str] = []
    arch = str(ex.get("architect_en") or ex.get("architect_ru") or "").strip()
    if arch:
        facts.append("Architect: {}.".format(arch))
    year = str(ex.get("year") or "").strip()
    if year:
        facts.append("Period: {}.".format(year))
    city = str(ex.get("city_en") or ex.get("city_ru") or "").strip()
    if city:
        facts.append("City: {}.".format(city))
    return facts


def _place_row(style_key: str, ex: dict[str, Any]) -> dict[str, Any]:
    slug = _slug(style_key, str(ex["suffix"]))
    if is_slug_excluded(slug):
        return {}
    rel = _image_rel(slug)
    arch_ru = str(ex.get("architect_ru") or "").strip()
    arch_en = str(ex.get("architect_en") or arch_ru).strip()
    city_ref = str(ex.get("_city_ref") or "").strip()
    city_style = str(ex.get("city_style") or "").strip()
    if city_ref and not arch_ru:
        sidecar_arch = _sidecar_architect(city_style, style_key)
        if sidecar_arch:
            arch_ru = sidecar_arch
            arch_en = sidecar_arch
            ex = dict(ex)
            ex["architect_ru"] = arch_ru
            ex["architect_en"] = arch_en
    style_ru = _style_title(style_key, "ru")
    style_en = _style_title(style_key, "en")
    row: dict[str, Any] = {
        "slug": slug,
        "category": style_key,
        "name_ru": ex["name_ru"],
        "subtitle_en": ex["name_en"],
        "image_rel_path": rel,
        "image_source_url": ex.get("commons_url", ""),
        "license_note": _LICENSE,
        "attribution": _ATTRIBUTION,
        "year_built": str(ex.get("year") or ""),
        "architecture_style": style_ru,
        "architecture_style_en": style_en,
        "address": str(ex.get("city_ru") or ""),
        "address_en": str(ex.get("city_en") or ex.get("city_ru") or ""),
        "description": _description_ru(ex, style_key),
        "description_ru": _description_ru(ex, style_key),
        "description_en": _description_en(ex, style_key),
        "history": str(ex.get("history_ru") or ""),
        "history_ru": str(ex.get("history_ru") or ""),
        "history_en": str(ex.get("history_en") or ex.get("history_ru") or ""),
        "significance": str(ex.get("significance_ru") or ""),
        "significance_ru": str(ex.get("significance_ru") or ""),
        "significance_en": str(
            ex.get("significance_en") or ex.get("significance_ru") or "",
        ),
        "facts": _facts_ru(ex, style_key),
        "facts_ru": _facts_ru(ex, style_key),
        "facts_en": _facts_en(ex, style_key),
    }
    reuse = str(ex.get("reuse_from") or "").strip()
    if reuse:
        row["_reuse_from"] = reuse
    city_ref = str(ex.get("_city_ref") or "").strip()
    if city_ref:
        row["_city_ref"] = city_ref
    return apply_narrative_overrides(row)


def _link_image(
    project_root: Path,
    guide_root: Path,
    row: dict[str, Any],
    city_index: dict[str, dict[str, Any]],
) -> str:
    """Copy primary image or report missing. Returns status token."""
    dest_rel = str(row["image_rel_path"])
    dest = guide_root / dest_rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.is_file() and dest.stat().st_size >= MIN_IMAGE_BYTES:
        link_additional_images(project_root, guide_root, row)
        return "exists"

    city_ref = str(row.get("_city_ref") or "").strip()
    if city_ref:
        city_row = city_index.get(city_ref)
        if city_row:
            city = str(city_row["city"])
            rel = str(city_row["image_rel_path"])
            src = project_root / city / rel
            if src.is_file() and src.stat().st_size >= MIN_IMAGE_BYTES:
                shutil.copy2(src, dest)
                link_additional_images(project_root, guide_root, row)
                return "copied"

    reuse = str(row.get("_reuse_from") or "").strip()
    if reuse:
        src = project_root / reuse.replace("/", "\\")
        if not src.is_file():
            src = project_root / reuse
        if src.is_file() and src.stat().st_size >= MIN_IMAGE_BYTES:
            shutil.copy2(src, dest)
            link_additional_images(project_root, guide_root, row)
            return "copied"

    if dest.is_file() and dest.stat().st_size >= MIN_IMAGE_BYTES:
        link_additional_images(project_root, guide_root, row)
        return "exists"
    return "missing"


def generate_places(
    project_root: Path,
    *,
    link_images: bool = True,
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    guide_root = project_root / "russian_arhitecture"
    city_index = load_city_index(project_root)
    rows: list[dict[str, Any]] = []
    stats = {"copied": 0, "exists": 0, "missing": 0}
    for style_key in STYLE_ORDER:
        examples = _collect_style_examples(style_key, city_index)
        for ex in examples:
            row = _place_row(style_key, ex)
            if not row:
                continue
            attach_from_city_ref(row, city_index, project_root)
            row = strip_extra_images(apply_image_url_overrides(row))
            if link_images:
                status = _link_image(
                    project_root,
                    guide_root,
                    row,
                    city_index,
                )
                stats[status] = stats.get(status, 0) + 1
                prune_missing_additional_images(guide_root, row)
                strip_internal_image_keys(row)
            rows.append(strip_extra_images(row))
    return rows, stats


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate russian_arhitecture_places.json from style catalog.",
    )
    parser.add_argument(
        "--no-link-images",
        action="store_true",
        help="Only write JSON; do not copy reused images",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=_PROJECT_ROOT,
    )
    args = parser.parse_args()
    rows, stats = generate_places(
        args.project_root,
        link_images=not args.no_link_images,
    )
    out = (
        args.project_root
        / "russian_arhitecture"
        / "data"
        / "russian_arhitecture_places.json"
    )
    out.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("Wrote {} places to {}".format(len(rows), out))
    if not args.no_link_images:
        second = sum(
            1
            for row in rows
            if row.get("additional_images")
        )
        print(
            "Images: copied={}, exists={}, missing={}, with_second={}".format(
                stats.get("copied", 0),
                stats.get("exists", 0),
                stats.get("missing", 0),
                second,
            ),
        )
    per_style: dict[str, int] = {}
    for row in rows:
        cat = str(row.get("category") or "")
        per_style[cat] = per_style.get(cat, 0) + 1
    for style_key in STYLE_ORDER:
        count = per_style.get(style_key, 0)
        target = style_example_target(style_key)
        mark = "ok" if count == target else "SHORT"
        print("  {}: {} / {} {}".format(style_key, count, target, mark))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
