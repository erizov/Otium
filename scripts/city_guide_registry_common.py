# -*- coding: utf-8 -*-
"""Shared registry load helpers (PDF expand sidecar, detail merge)."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.city_guide_core import is_excluded_place_category
from scripts.city_guide_naming import pdf_expand_sidecar_filename


def pdf_expand_sidecar_paths(data_dir: Path, city_slug: str) -> tuple[Path, ...]:
    """Sidecar JSON files that hold PDF size-band filler rows."""
    names = [
        pdf_expand_sidecar_filename(city_slug),
    ]
    if city_slug == "spb":
        names.append("spb_places_pdf_size_expand.json")
    elif city_slug == "smolensk":
        names.append("smolensk_places_pdf_size_expand.json")
    out: list[Path] = []
    for name in names:
        p = data_dir / name
        if p.is_file():
            out.append(p)
    return tuple(out)


def load_pdf_expand_rows(data_dir: Path, city_slug: str) -> list[dict]:
    rows: list[dict] = []
    for path in pdf_expand_sidecar_paths(data_dir, city_slug):
        blob = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(blob, list):
            rows.extend(blob)
    return rows


def drop_empty_place_rows(rows: list[dict]) -> list[dict]:
    """Remove stray ``{}`` entries and excluded food categories."""
    out: list[dict] = []
    for row in rows:
        if not (row.get("slug") or row.get("image_rel_path")):
            continue
        if is_excluded_place_category(str(row.get("category") or "")):
            continue
        out.append(row)
    return out


def merge_detail_overlays(
    rows: list[dict],
    data_dir: Path,
    city_slug: str,
    *,
    skip_merge: frozenset[str] | None = None,
) -> list[dict]:
    skip = skip_merge or frozenset({"additional_images"})
    merged: dict[str, dict] = {}
    pattern = "{}_place_details*.json".format(city_slug)
    for path in sorted(data_dir.glob(pattern)):
        blob = json.loads(path.read_text(encoding="utf-8"))
        merged.update(blob)
    if not merged:
        return rows
    for row in rows:
        slug = str(row.get("slug") or "")
        block = merged.get(slug)
        if block is None and city_slug:
            prefixed = "{}_{}".format(city_slug, slug)
            block = merged.get(prefixed)
            if block is None and slug.startswith("{}_".format(city_slug)):
                block = merged.get(slug[len(city_slug) + 1:])
        if not block:
            continue
        for key, val in block.items():
            if key in skip:
                continue
            if val in (None, "", [], {}):
                continue
            row[key] = val
    return rows


def second_image_sidecar_path(data_dir: Path, city_slug: str) -> Path:
    return data_dir / "{}_second_images.json".format(city_slug)


def load_second_image_sidecar(data_dir: Path, city_slug: str) -> dict[str, list[dict]]:
    path = second_image_sidecar_path(data_dir, city_slug)
    if not path.is_file():
        return {}
    blob = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(blob, dict):
        return {}
    return blob


def save_second_image_sidecar(
    data_dir: Path,
    city_slug: str,
    sidecar: dict[str, list[dict]],
) -> None:
    path = second_image_sidecar_path(data_dir, city_slug)
    path.write_text(
        json.dumps(sidecar, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def merge_second_image_sidecar(
    rows: list[dict],
    data_dir: Path,
    city_slug: str,
) -> list[dict]:
    """Attach sidecar ``additional_images`` when JSON has none."""
    side = load_second_image_sidecar(data_dir, city_slug)
    if not side:
        return rows
    for row in rows:
        slug = str(row.get("slug") or "")
        if not slug or row.get("additional_images"):
            continue
        extra = side.get(slug)
        if extra:
            row["additional_images"] = extra
    return rows


def derive_second_image_rel(primary_rel: str) -> str:
    rel = primary_rel.replace("\\", "/").lstrip("/")
    parent = Path(rel).parent
    stem = Path(rel).stem
    suffix = Path(rel).suffix or ".jpg"
    if parent.as_posix() in (".", ""):
        return "{}_b{}".format(stem, suffix)
    return str(parent / "{}_b{}".format(stem, suffix)).replace("\\", "/")
