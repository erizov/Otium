# -*- coding: utf-8 -*-
"""Migrate American ecclesiastical chapter and apply Wave 1 worship expand."""

from __future__ import annotations

import argparse
import importlib
import json
import shutil
import sys
import time
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.architecture_guide_runtime import load_parts  # noqa: E402
from scripts.city_guide_standard_whitelist import clear_whitelist_cache  # noqa: E402
from scripts.city_guide_commons_fetch import configure_commons_api_throttle  # noqa: E402
from scripts.city_guide_jerusalem_style_images import (  # noqa: E402
    _candidate_urls,
    _download_place_image,
)
from scripts.worship_wave1_data import (  # noqa: E402
    AMERICAN_ECCLESIASTICAL_MIGRATION,
    AMERICAN_ECCLESIASTICAL_SOURCES,
    wave1_seeds,
)

_LICENSE = "See Wikimedia Commons file page for license."
_ATTRIBUTION = "Wikimedia Commons contributors"


def _style_titles(module: str) -> tuple[dict[str, tuple[str, str, str, str]], tuple[str, ...]]:
    catalog = importlib.import_module("{}.data.style_catalog".format(module))
    return catalog.STYLE_META, catalog.STYLE_ORDER


def _style_title(
    style_meta: dict[str, tuple[str, str, str, str]],
    style_key: str,
    lang: str,
) -> str:
    meta = style_meta[style_key]
    return meta[0] if lang == "ru" else meta[1]


def _slug(style_key: str, suffix: str) -> str:
    return "{}_{}".format(style_key, suffix)


def _image_rel(slug: str) -> str:
    return "images/styles/{}.jpg".format(slug)


def _expand_path(module: str) -> Path:
    return (
        _PROJECT_ROOT
        / module
        / "data"
        / "{}_places_pdf_expand.json".format(module)
    )


def _seed_row(
    module: str,
    seed: tuple[str, ...],
    style_meta: dict[str, tuple[str, str, str, str]],
) -> dict[str, Any]:
    (
        style_key,
        suffix,
        name_ru,
        name_en,
        year,
        city_ru,
        city_en,
        history_ru,
        history_en,
        commons_url,
        city_ref,
    ) = seed
    slug = _slug(style_key, suffix)
    style_ru = _style_title(style_meta, style_key, "ru")
    style_en = _style_title(style_meta, style_key, "en")
    desc_ru = history_ru or name_ru
    desc_en = history_en or name_en
    row: dict[str, Any] = {
        "slug": slug,
        "category": style_key,
        "name_ru": name_ru,
        "name_en": name_en,
        "subtitle_en": name_en,
        "image_rel_path": _image_rel(slug),
        "image_source_url": commons_url,
        "license_note": _LICENSE,
        "attribution": _ATTRIBUTION,
        "year_built": year,
        "architecture_style": style_ru,
        "architecture_style_en": style_en,
        "address": city_ru,
        "address_en": city_en,
        "description": desc_ru,
        "description_ru": desc_ru,
        "description_en": desc_en,
        "history": history_ru,
        "history_ru": history_ru,
        "history_en": history_en,
        "significance": "",
        "significance_ru": "",
        "significance_en": "",
        "facts": ["Период: {}.".format(year), "Город: {}.".format(city_ru)],
        "facts_ru": ["Период: {}.".format(year), "Город: {}.".format(city_ru)],
        "facts_en": ["Period: {}.".format(year), "City: {}.".format(city_en)],
    }
    if city_ref:
        row["_city_ref"] = city_ref
    return row


def _load_expand(module: str) -> list[dict[str, Any]]:
    path = _expand_path(module)
    if not path.is_file():
        return []
    blob = json.loads(path.read_text(encoding="utf-8"))
    return list(blob) if isinstance(blob, list) else []


def _write_expand(module: str, rows: list[dict[str, Any]]) -> Path:
    path = _expand_path(module)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def _migration_map() -> dict[str, tuple[str, str]]:
    out: dict[str, tuple[str, str]] = {}
    for old_suffix, style_key, new_suffix in AMERICAN_ECCLESIASTICAL_MIGRATION:
        old_slug = "ecclesiastical_ny_montreal_{}".format(old_suffix)
        out[old_slug] = (style_key, new_suffix)
        out[_slug(style_key, new_suffix)] = (style_key, new_suffix)
    return out


def _rename_ecclesiastical_image(
    guide_root: Path,
    old_suffix: str,
    new_rel: str,
) -> None:
    old_rel = "images/styles/ecclesiastical_ny_montreal_{}.jpg".format(
        old_suffix,
    )
    old_path = guide_root / old_rel
    new_path = guide_root / new_rel
    if new_path.is_file() and new_path.stat().st_size >= 500:
        if old_path.is_file():
            old_path.unlink(missing_ok=True)
        return
    if old_path.is_file():
        new_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(old_path), str(new_path))


def _migrated_ecclesiastical_row(
    module: str,
    old_suffix: str,
    style_key: str,
    new_suffix: str,
    style_meta: dict[str, tuple[str, str, str, str]],
    guide_root: Path,
) -> dict[str, Any]:
    src = AMERICAN_ECCLESIASTICAL_SOURCES[old_suffix]
    (
        name_ru,
        name_en,
        year,
        city_ru,
        city_en,
        desc_ru,
        desc_en,
        history_ru,
        history_en,
        commons_url,
    ) = src
    slug = _slug(style_key, new_suffix)
    new_rel = _image_rel(slug)
    _rename_ecclesiastical_image(guide_root, old_suffix, new_rel)
    style_ru = _style_title(style_meta, style_key, "ru")
    style_en = _style_title(style_meta, style_key, "en")
    return {
        "slug": slug,
        "category": style_key,
        "name_ru": name_ru,
        "name_en": name_en,
        "subtitle_en": name_en,
        "image_rel_path": new_rel,
        "image_source_url": commons_url,
        "license_note": _LICENSE,
        "attribution": _ATTRIBUTION,
        "year_built": year,
        "architecture_style": style_ru,
        "architecture_style_en": style_en,
        "address": city_ru,
        "address_en": city_en,
        "description": desc_ru,
        "description_ru": desc_ru,
        "description_en": desc_en,
        "history": history_ru,
        "history_ru": history_ru,
        "history_en": history_en,
        "significance": "",
        "significance_ru": "",
        "significance_en": "",
        "facts": ["Период: {}.".format(year), "Город: {}.".format(city_ru)],
        "facts_ru": ["Период: {}.".format(year), "Город: {}.".format(city_ru)],
        "facts_en": ["Period: {}.".format(year), "City: {}.".format(city_en)],
    }


def migrate_american_ecclesiastical(project_root: Path) -> list[dict[str, Any]]:
    module = "american_architecture"
    style_meta, _ = _style_titles(module)
    guide_root = project_root / module
    migrated: list[dict[str, Any]] = []
    for old_suffix, style_key, new_suffix in AMERICAN_ECCLESIASTICAL_MIGRATION:
        row = _migrated_ecclesiastical_row(
            module,
            old_suffix,
            style_key,
            new_suffix,
            style_meta,
            guide_root,
        )
        migrated.append(row)
    wave1 = [
        _seed_row(module, seed, style_meta)
        for seed in wave1_seeds(module)
    ]
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for row in migrated + wave1:
        slug = str(row.get("slug") or "")
        if slug in seen:
            continue
        seen.add(slug)
        out.append(row)
    _write_expand(module, out)
    return out


def write_wave1_expand(module: str) -> list[dict[str, Any]]:
    style_meta, _ = _style_titles(module)
    rows = [_seed_row(module, seed, style_meta) for seed in wave1_seeds(module)]
    _write_expand(module, rows)
    return rows


def _city_row(
    project_root: Path,
    city_ref: str,
) -> dict[str, Any] | None:
    if ":" not in city_ref:
        return None
    city, slug = city_ref.split(":", 1)
    places_path = project_root / city / "data" / "{}_places.json".format(city)
    if not places_path.is_file():
        return None
    for row in json.loads(places_path.read_text(encoding="utf-8")):
        if str(row.get("slug") or "") == slug:
            row = dict(row)
            row["city"] = city
            return row
    return None


def _copy_city_image(
    project_root: Path,
    parts: Any,
    guide_root: Path,
    city_row: dict[str, Any],
    dest_rel: str,
) -> bool:
    city = str(city_row.get("city") or "")
    rel = str(city_row.get("image_rel_path") or "")
    if not city or not rel:
        return False
    return bool(parts.copy_city_image(
        project_root,
        guide_root,
        city,
        rel,
        dest_rel,
    ))


def _download_commons(
    guide_root: Path,
    row: dict[str, Any],
    url: str,
    *,
    retries_429: int,
    pause_429_sec: float,
) -> bool:
    dest = guide_root / str(row["image_rel_path"])
    dest.parent.mkdir(parents=True, exist_ok=True)
    ordered = _candidate_urls(url, 1280)
    ok, _err = _download_place_image(
        ordered,
        dest,
        timeout_sec=60,
        retries_429=retries_429,
        pause_429_sec=pause_429_sec,
    )
    return bool(ok and dest.is_file())


def resolve_expand_images(
    project_root: Path,
    module: str,
    *,
    commons_delay: float = 3.5,
    retries_429: int = 5,
    pause_429_sec: float = 55.0,
    commons_api_gap: float = 4.5,
    allow_alt_sources: bool = False,
) -> dict[str, int]:
    configure_commons_api_throttle(
        min_gap_sec=commons_api_gap,
        retries_429=retries_429,
        pause_429_sec=pause_429_sec,
    )
    parts = load_parts(module)
    guide_root = project_root / module
    whitelist_path = parts.default_whitelist_path()
    min_bytes = int(parts.MIN_IMAGE_BYTES)
    stats = {
        "already": 0,
        "copied_city": 0,
        "catalog_url": 0,
        "alt_source": 0,
        "missing": 0,
    }
    rows = _load_expand(module)
    for row in rows:
        dest_rel = str(row.get("image_rel_path") or "")
        dest = guide_root / dest_rel
        if dest.is_file() and dest.stat().st_size >= min_bytes:
            stats["already"] += 1
            continue
        copied = False
        city_ref = str(row.get("_city_ref") or "").strip()
        if city_ref:
            city_row = _city_row(project_root, city_ref)
            if city_row and _copy_city_image(
                project_root,
                parts,
                guide_root,
                city_row,
                dest_rel,
            ):
                url = str(city_row.get("image_source_url") or "")
                if url and not str(row.get("image_source_url") or "").strip():
                    row["image_source_url"] = url
                copied = True
                stats["copied_city"] += 1
        if not copied:
            url = str(row.get("image_source_url") or "").strip()
            if url and _download_commons(
                guide_root,
                row,
                url,
                retries_429=retries_429,
                pause_429_sec=pause_429_sec,
            ):
                copied = True
                stats["catalog_url"] += 1
                time.sleep(commons_delay)
        if not copied and allow_alt_sources:
            from scripts.resolve_architecture_guide_images import (
                _candidate_image_urls,
                _city_slug_from_row,
                _download_first_url,
            )

            slug_city = _city_slug_from_row(parts, row)
            alt_urls = _candidate_image_urls(
                parts,
                row,
                slug_city=slug_city,
                whitelist_path=whitelist_path,
            )
            if alt_urls:
                catalog = str(row.get("image_source_url") or "").strip()
                got = _download_first_url(
                    parts,
                    guide_root,
                    row,
                    alt_urls,
                    retries_429=retries_429,
                    pause_429_sec=pause_429_sec,
                )
                if got:
                    row["image_source_url"] = got
                    copied = True
                    if catalog and got == catalog:
                        stats["catalog_url"] += 1
                    else:
                        stats["alt_source"] += 1
                    time.sleep(commons_delay)
        if not copied:
            stats["missing"] += 1
    _write_expand(module, rows)
    return stats


def remove_ecclesiastical_from_catalog(project_root: Path) -> None:
    path = project_root / "american_architecture" / "data" / "style_catalog.py"
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    out: list[str] = []
    skip = False
    for line in lines:
        if '"ecclesiastical_ny_montreal"' in line:
            skip = True
            continue
        if skip:
            if line.strip() == "),":
                skip = False
            continue
        if '"ecclesiastical_ny_montreal",' in line:
            continue
        out.append(line)
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def apply_wave1(
    project_root: Path,
    *,
    migrate_only: bool = False,
    download_images: bool = True,
    allow_alt_sources: bool = False,
) -> dict[str, Any]:
    report: dict[str, Any] = {"modules": {}}
    clear_whitelist_cache()
    remove_ecclesiastical_from_catalog(project_root)
    american_rows = migrate_american_ecclesiastical(project_root)
    report["american_migrated"] = len(AMERICAN_ECCLESIASTICAL_MIGRATION)
    report["american_expand_total"] = len(american_rows)
    if not migrate_only:
        report["modules"] = {}
        for module in ("german_architecture", "english_architecture"):
            rows = write_wave1_expand(module)
            report["modules"][module] = {"expand_rows": len(rows)}
        report["modules"]["american_architecture"] = {
            "expand_rows": len(american_rows),
        }
        if download_images:
            for module in (
                "german_architecture",
                "english_architecture",
                "american_architecture",
            ):
                stats = resolve_expand_images(
                    project_root,
                    module,
                    allow_alt_sources=allow_alt_sources,
                )
                report["modules"][module]["image_stats"] = stats
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply worship Wave 1 expand data.")
    parser.add_argument(
        "--migrate-only",
        action="store_true",
        help="Only migrate American ecclesiastical chapter.",
    )
    parser.add_argument(
        "--no-download",
        action="store_true",
        help="Skip Commons / city image download for expand rows.",
    )
    parser.add_argument(
        "--allow-alt-sources",
        action="store_true",
        help="Use Flickr / Openverse / Geograph via city-guide discovery.",
    )
    args = parser.parse_args()
    report = apply_wave1(
        _PROJECT_ROOT,
        migrate_only=args.migrate_only,
        download_images=not args.no_download,
        allow_alt_sources=args.allow_alt_sources,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
