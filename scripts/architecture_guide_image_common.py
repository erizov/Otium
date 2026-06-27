# -*- coding: utf-8 -*-
"""Shared image helpers for architecture guide modules."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Callable

MIN_IMAGE_BYTES = 500
MAX_IMAGES_PER_PLACE = 2


def extra_image_rel(place_slug: str) -> str:
    return "images/styles/{}_2.jpg".format(place_slug)


def has_local_image(guide_root: Path, rel: str) -> bool:
    path = guide_root / rel
    return path.is_file() and path.stat().st_size >= MIN_IMAGE_BYTES


def copy_city_image(
    project_root: Path,
    guide_root: Path,
    city: str,
    src_rel: str,
    dest_rel: str,
) -> bool:
    src = project_root / city / src_rel
    dest = guide_root / dest_rel
    if not src.is_file() or src.stat().st_size < MIN_IMAGE_BYTES:
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.is_file() and dest.stat().st_size >= MIN_IMAGE_BYTES:
        return True
    shutil.copy2(src, dest)
    return dest.is_file() and dest.stat().st_size >= MIN_IMAGE_BYTES


def _local_additional_images(
    project_root: Path,
    city: str,
    row: dict[str, Any],
) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for extra in row.get("additional_images") or []:
        if len(out) >= 1:
            break
        if not isinstance(extra, dict):
            continue
        rel = str(extra.get("image_rel_path") or "").strip()
        if not rel:
            continue
        path = project_root / city / rel
        if not path.is_file() or path.stat().st_size < MIN_IMAGE_BYTES:
            continue
        out.append({
            "image_rel_path": rel,
            "image_source_url": str(extra.get("image_source_url") or ""),
        })
    return out


def make_load_city_index(
    city_roots: tuple[str, ...],
) -> Callable[[Path], dict[str, dict[str, Any]]]:
    """Build ``load_city_index`` for the given city guide roots."""

    def load_city_index(
        project_root: Path,
    ) -> dict[str, dict[str, Any]]:
        index: dict[str, dict[str, Any]] = {}
        for city in city_roots:
            data_dir = project_root / city / "data"
            if not data_dir.is_dir():
                continue
            for path in sorted(data_dir.glob("*places*.json")):
                try:
                    rows = json.loads(path.read_text(encoding="utf-8"))
                except (json.JSONDecodeError, OSError):
                    continue
                if not isinstance(rows, list):
                    continue
                for row in rows:
                    if not isinstance(row, dict):
                        continue
                    slug = str(row.get("slug") or "").strip()
                    rel = str(row.get("image_rel_path") or "").strip()
                    if not slug or not rel:
                        continue
                    img = project_root / city / rel
                    if (
                        not img.is_file()
                        or img.stat().st_size < MIN_IMAGE_BYTES
                    ):
                        continue
                    key = "{}:{}".format(city, slug)
                    index[key] = {
                        "city": city,
                        "slug": slug,
                        "name_ru": str(row.get("name_ru") or ""),
                        "name_en": str(
                            row.get("subtitle_en")
                            or row.get("name_en")
                            or "",
                        ),
                        "image_rel_path": rel,
                        "image_source_url": str(
                            row.get("image_source_url") or "",
                        ),
                        "history_ru": str(
                            row.get("history_ru")
                            or row.get("history")
                            or "",
                        ),
                        "history_en": str(
                            row.get("history_en")
                            or row.get("history")
                            or "",
                        ),
                        "significance_ru": str(
                            row.get("significance_ru")
                            or row.get("significance")
                            or "",
                        ),
                        "significance_en": str(
                            row.get("significance_en")
                            or row.get("significance")
                            or "",
                        ),
                        "year_built": str(row.get("year_built") or ""),
                        "architecture_style": str(
                            row.get("architecture_style") or "",
                        ),
                        "address": str(row.get("address") or ""),
                        "additional_images": _local_additional_images(
                            project_root,
                            city,
                            row,
                        ),
                    }
        return index

    return load_city_index


def city_additional_sources(
    city_row: dict[str, Any],
    project_root: Path,
) -> list[dict[str, str]]:
    city = str(city_row.get("city") or "")
    out: list[dict[str, str]] = []
    for extra in city_row.get("additional_images") or []:
        if len(out) >= MAX_IMAGES_PER_PLACE - 1:
            break
        if not isinstance(extra, dict):
            continue
        rel = str(extra.get("image_rel_path") or "").strip()
        if not rel:
            continue
        path = project_root / city / rel
        if path.is_file() and path.stat().st_size >= MIN_IMAGE_BYTES:
            out.append({
                "src_rel": rel,
                "image_source_url": str(
                    extra.get("image_source_url") or "",
                ),
            })
    return out


def make_attach_additional_image_rows(
    single_image_slugs: frozenset[str],
    image_url_overrides: dict[str, Any],
) -> Callable[[dict[str, Any], dict[str, Any] | None, Path], None]:
    def attach_additional_image_rows(
        row: dict[str, Any],
        city_row: dict[str, Any] | None,
        project_root: Path,
    ) -> None:
        if not city_row:
            return
        slug = str(row.get("slug") or "").strip()
        if not slug or slug in single_image_slugs:
            return
        if slug in image_url_overrides:
            return
        sources = city_additional_sources(city_row, project_root)
        if not sources:
            return
        src = sources[0]
        row["additional_images"] = [{
            "image_rel_path": extra_image_rel(slug),
            "image_source_url": src["image_source_url"],
            "_src_city": str(city_row["city"]),
            "_src_rel": src["src_rel"],
        }]

    return attach_additional_image_rows


def link_additional_images(
    project_root: Path,
    guide_root: Path,
    row: dict[str, Any],
) -> int:
    slug = str(row.get("slug") or "").strip()
    if not slug:
        return 0
    linked = 0
    extras = row.get("additional_images")
    if not isinstance(extras, list):
        extras = []
    for extra in extras:
        if not isinstance(extra, dict):
            continue
        dest_rel = str(extra.get("image_rel_path") or extra_image_rel(slug))
        if has_local_image(guide_root, dest_rel):
            linked += 1
            continue
        city = str(extra.get("_src_city") or "").strip()
        src_rel = str(extra.get("_src_rel") or "").strip()
        if city and src_rel and copy_city_image(
            project_root,
            guide_root,
            city,
            src_rel,
            dest_rel,
        ):
            linked += 1
        break
    return linked


def make_attach_from_city_ref(
    attach_additional_image_rows: Callable[
        [dict[str, Any], dict[str, Any] | None, Path],
        None,
    ],
) -> Callable[[dict[str, Any], dict[str, dict[str, Any]], Path], None]:
    def attach_from_city_ref(
        row: dict[str, Any],
        city_index: dict[str, dict[str, Any]],
        project_root: Path,
    ) -> None:
        city_ref = str(row.get("_city_ref") or "").strip()
        if not city_ref:
            return
        attach_additional_image_rows(
            row,
            city_index.get(city_ref),
            project_root,
        )

    return attach_from_city_ref


def prune_missing_additional_images(
    guide_root: Path,
    row: dict[str, Any],
) -> None:
    extras = row.get("additional_images")
    if not isinstance(extras, list):
        return
    kept: list[dict[str, Any]] = []
    for extra in extras:
        if not isinstance(extra, dict):
            continue
        rel = str(extra.get("image_rel_path") or "").strip()
        if rel and has_local_image(guide_root, rel):
            kept.append(extra)
    if kept:
        row["additional_images"] = kept
    else:
        row.pop("additional_images", None)


def strip_internal_image_keys(row: dict[str, Any]) -> None:
    for extra in row.get("additional_images") or []:
        if isinstance(extra, dict):
            extra.pop("_src_city", None)
            extra.pop("_src_rel", None)
    row.pop("_city_ref", None)
    row.pop("_reuse_from", None)
