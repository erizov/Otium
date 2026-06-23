# -*- coding: utf-8 -*-
"""Build russian_arhitecture_places.json and link local images."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from russian_arhitecture.data.style_catalog import (  # noqa: E402
    STYLE_EXAMPLES,
    STYLE_META,
    STYLE_ORDER,
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


def _description_ru(ex: dict[str, Any], style_key: str) -> str:
    parts: list[str] = []
    intro = _style_intro(style_key, "ru")
    if intro:
        parts.append(intro)
    hist = str(ex.get("history_ru") or "").strip()
    if hist:
        parts.append(hist)
    sig = str(ex.get("significance_ru") or "").strip()
    if sig:
        parts.append(sig)
    if not parts:
        parts.append(
            "Пример {}.".format(_style_title(style_key, "ru").lower()),
        )
    return " ".join(parts)


def _description_en(ex: dict[str, Any], style_key: str) -> str:
    parts: list[str] = []
    intro = _style_intro(style_key, "en")
    if intro:
        parts.append(intro)
    hist = str(ex.get("history_en") or ex.get("history_ru") or "").strip()
    if hist:
        parts.append(hist)
    sig = str(ex.get("significance_en") or ex.get("significance_ru") or "").strip()
    if sig:
        parts.append(sig)
    if not parts:
        parts.append(
            "An example of {}.".format(_style_title(style_key, "en").lower()),
        )
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
    facts.append("Стиль: {}.".format(_style_title(style_key, "ru")))
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
    facts.append("Style: {}.".format(_style_title(style_key, "en")))
    return facts


def _place_row(style_key: str, ex: dict[str, Any]) -> dict[str, Any]:
    slug = _slug(style_key, str(ex["suffix"]))
    rel = _image_rel(slug)
    arch_ru = str(ex.get("architect_ru") or "").strip()
    arch_en = str(ex.get("architect_en") or arch_ru).strip()
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
        "architecture_style": arch_ru or _style_title(style_key, "ru"),
        "architecture_style_en": arch_en or _style_title(style_key, "en"),
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
    return row


def _link_image(
    project_root: Path,
    guide_root: Path,
    row: dict[str, Any],
) -> str:
    """Copy reused image or report missing. Returns status token."""
    dest_rel = str(row["image_rel_path"])
    dest = guide_root / dest_rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.is_file() and dest.stat().st_size >= MIN_IMAGE_BYTES:
        return "exists"
    reuse = str(row.pop("_reuse_from", "") or "").strip()
    if reuse:
        src = project_root / reuse.replace("/", "\\")
        if not src.is_file():
            src = project_root / reuse
        if src.is_file() and src.stat().st_size >= MIN_IMAGE_BYTES:
            shutil.copy2(src, dest)
            return "copied"
    if dest.is_file() and dest.stat().st_size >= MIN_IMAGE_BYTES:
        return "exists"
    return "missing"


def generate_places(
    project_root: Path,
    *,
    link_images: bool = True,
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    guide_root = project_root / "russian_arhitecture"
    rows: list[dict[str, Any]] = []
    stats = {"copied": 0, "exists": 0, "missing": 0}
    for style_key in STYLE_ORDER:
        for ex in STYLE_EXAMPLES.get(style_key, []):
            row = _place_row(style_key, ex)
            if link_images:
                status = _link_image(project_root, guide_root, row)
                stats[status] = stats.get(status, 0) + 1
            else:
                row.pop("_reuse_from", None)
            rows.append(row)
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
        print(
            "Images: copied={}, exists={}, missing={}".format(
                stats.get("copied", 0),
                stats.get("exists", 0),
                stats.get("missing", 0),
            ),
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
