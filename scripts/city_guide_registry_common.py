# -*- coding: utf-8 -*-
"""Shared registry load helpers (PDF expand sidecar, detail merge)."""

from __future__ import annotations

import json
from pathlib import Path

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
    """Remove stray ``{}`` entries from JSON arrays."""
    return [r for r in rows if r.get("slug") or r.get("image_rel_path")]


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
        block = merged.get(row.get("slug"))
        if not block:
            continue
        for key, val in block.items():
            if key in skip:
                continue
            if val in (None, "", [], {}):
                continue
            row[key] = val
    return rows
