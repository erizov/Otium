# -*- coding: utf-8 -*-
"""City-agnostic storage for guide places and editable overlays."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class CityPaths:
    """Filesystem locations for one city guide."""

    city_slug: str
    city_root: Path

    @property
    def data_dir(self) -> Path:
        return self.city_root / "data"

    @property
    def images_dir(self) -> Path:
        return self.city_root / "images"

    @property
    def places_json(self) -> Path:
        return self.data_dir / f"{self.city_slug}_places.json"

    @property
    def details_glob(self) -> str:
        return f"{self.city_slug}_place_details*.json"

    @property
    def overlay_details_path(self) -> Path:
        return self.data_dir / f"{self.city_slug}_place_details_more.json"


def discover_cities(project_root: Path) -> list[str]:
    """Find city slugs by locating `<city>/data/<city>_places.json`."""
    out: list[str] = []
    for child in project_root.iterdir():
        if not child.is_dir():
            continue
        data_dir = child / "data"
        if not data_dir.is_dir():
            continue
        slug = child.name
        if (data_dir / f"{slug}_places.json").is_file():
            out.append(slug)
    return sorted(out)


def cities_ui_order(project_root: Path) -> list[str]:
    """Same slugs as ``discover_cities``, with Moscow first when present."""
    cities = discover_cities(project_root)
    if "moscow" in cities:
        return ["moscow"] + sorted(c for c in cities if c != "moscow")
    return cities


def city_paths(project_root: Path, city_slug: str) -> CityPaths:
    root = project_root / city_slug
    return CityPaths(city_slug=city_slug, city_root=root)


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_city_places(project_root: Path, city_slug: str) -> list[dict[str, Any]]:
    """
    Load merged places for a city.

    Merge semantics replicate `<city>/data/places_registry.py`:
    - base list from `<city>_places.json`
    - overlay detail files `<city>_place_details*.json` merged in filename order
    - detail keys overwrite base keys (except `additional_images`)
    - ignore empty values (None / "" / [] / {})
    """
    paths = city_paths(project_root, city_slug)
    raw = _load_json(paths.places_json)
    if not isinstance(raw, list):
        raise ValueError(f"Expected list in {paths.places_json}")
    rows: list[dict[str, Any]] = []
    for item in raw:
        if isinstance(item, dict):
            rows.append(dict(item))
    merged_details: dict[str, dict[str, Any]] = {}
    for detail_path in sorted(paths.data_dir.glob(paths.details_glob)):
        blob = _load_json(detail_path)
        if isinstance(blob, dict):
            for slug, block in blob.items():
                if not isinstance(slug, str) or not isinstance(block, dict):
                    continue
                merged_details[slug] = dict(block)
    skip_merge = {"additional_images"}
    for row in rows:
        slug = row.get("slug")
        if not isinstance(slug, str) or not slug:
            continue
        block = merged_details.get(slug)
        if not block:
            continue
        for key, val in block.items():
            if key in skip_merge:
                continue
            if val in (None, "", [], {}):
                continue
            row[key] = val
        editor_images = row.get("editor_images")
        if isinstance(editor_images, list):
            filtered: list[dict[str, Any]] = []
            for it in editor_images:
                if not isinstance(it, dict):
                    continue
                rel = str(it.get("image_rel_path") or "").strip()
                if not rel:
                    continue
                filtered.append(
                    {
                        "image_rel_path": rel,
                        "image_source_url": str(it.get("image_source_url") or "").strip(),
                    }
                )
            row["additional_images"] = filtered[:4]
    return rows


def load_overlay_details(project_root: Path, city_slug: str) -> dict[str, dict[str, Any]]:
    paths = city_paths(project_root, city_slug)
    if not paths.overlay_details_path.is_file():
        return {}
    blob = _load_json(paths.overlay_details_path)
    if not isinstance(blob, dict):
        return {}
    out: dict[str, dict[str, Any]] = {}
    for slug, block in blob.items():
        if isinstance(slug, str) and isinstance(block, dict):
            out[slug] = dict(block)
    return out


def _prune_empty(obj: Any) -> Any:
    if isinstance(obj, dict):
        out: dict[str, Any] = {}
        for k, v in obj.items():
            pruned = _prune_empty(v)
            if pruned in (None, "", [], {}):
                continue
            out[k] = pruned
        return out
    if isinstance(obj, list):
        items = [_prune_empty(x) for x in obj]
        items = [x for x in items if x not in (None, "", [], {})]
        return items
    return obj


def apply_place_patch(
    project_root: Path,
    city_slug: str,
    slug: str,
    patch: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """
    Merge a patch dict into the overlay details for one place.

    Patch semantics:
    - Keys in patch overwrite existing overlay keys for that slug.
    - Empty values are pruned (so user can delete by sending empty string/list).
    """
    paths = city_paths(project_root, city_slug)
    overlay = load_overlay_details(project_root, city_slug)
    current = dict(overlay.get(slug, {}))
    for key, val in patch.items():
        current[key] = val
    current = _prune_empty(current)
    if current in (None, "", [], {}):
        overlay.pop(slug, None)
    else:
        overlay[slug] = current  # type: ignore[assignment]
    paths.data_dir.mkdir(parents=True, exist_ok=True)
    paths.overlay_details_path.write_text(
        json.dumps(overlay, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    return overlay

