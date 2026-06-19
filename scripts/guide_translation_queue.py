# -*- coding: utf-8 -*-
"""Build and apply batch translation queues for city guide places."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterator, Mapping

from scripts.city_guide_narrative import (
    is_usable_narrative_text,
    polish_display_title,
    text_for_edition,
)
from scripts.city_guide_registry_common import pdf_expand_sidecar_paths
from scripts.city_guide_sparse_narrative import (
    _field_keys_for_edition,
    _json_has_usable_narrative_for_edition,
    _read_field,
    place_edition_needs_fill,
)

_PROSE_BASES = ("description", "history", "significance")
_NAME_BASE = "name"
_SLUG_TITLE_RE = re.compile(r"^[a-z0-9_]+$")


def discover_cities(project_root: Path) -> list[str]:
    out: list[str] = []
    for path in sorted(project_root.glob("*/data/*_places.json")):
        out.append(path.parent.parent.name)
    return out


def _place_files(data_dir: Path, city_slug: str) -> list[Path]:
    paths: list[Path] = []
    main = data_dir / "{}_places.json".format(city_slug)
    if main.is_file():
        paths.append(main)
    if city_slug == "spb":
        for more_name in (
            "spb_places_more.json",
            "spb_places_expansion_m2026.json",
            "spb_places_osobnjaki.json",
        ):
            more = data_dir / more_name
            if more.is_file():
                paths.append(more)
    paths.extend(pdf_expand_sidecar_paths(data_dir, city_slug))
    return paths


def _load_places(path: Path) -> list[dict[str, Any]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        return []
    return [p for p in raw if isinstance(p, dict)]


def _target_key(base: str, dst: str) -> str:
    if base == _NAME_BASE:
        return "name_ru" if dst == "ru" else "name_en"
    if dst == "ru":
        return "{}_ru".format(base)
    return "{}_en".format(base)


def _best_source_text(
    place: Mapping[str, Any],
    base: str,
    src: str,
) -> str | None:
    for key in _field_keys_for_edition(src, base):
        text = _read_field(place, key)
        if not text:
            continue
        if is_usable_narrative_text(text) and text_for_edition(text, src):
            return text
    return None


def _job_id(city: str, slug: str, field: str, src: str, dst: str, idx: int | None) -> str:
    parts = [city, slug, field, "{}-{}".format(src, dst)]
    if idx is not None:
        parts.append(str(idx))
    return "/".join(parts)


def iter_translation_jobs(
    project_root: Path,
    city_slug: str,
) -> Iterator[dict[str, Any]]:
    """Yield jobs where opposite edition has text and target edition is empty."""
    data_dir = project_root / city_slug / "data"
    for path in _place_files(data_dir, city_slug):
        rel = path.relative_to(project_root).as_posix()
        for place in _load_places(path):
            slug = str(place.get("slug") or "").strip()
            if not slug:
                continue
            for base in (_NAME_BASE,) + _PROSE_BASES:
                if base == _NAME_BASE:
                    kinds = ("name",)
                else:
                    kinds = ("prose",)
                for dst in ("ru", "en"):
                    src = "en" if dst == "ru" else "ru"
                    if not place_edition_needs_fill(place, dst):
                        continue
                    if not _json_has_usable_narrative_for_edition(place, src):
                        continue
                    text = _best_source_text(place, base, src)
                    if not text:
                        continue
                    kind = kinds[0]
                    yield {
                        "id": _job_id(city_slug, slug, base, src, dst, None),
                        "city": city_slug,
                        "source_file": rel,
                        "slug": slug,
                        "field": base,
                        "src_lang": src,
                        "dst_lang": dst,
                        "source_text": text,
                        "target_key": _target_key(base, dst),
                        "kind": kind,
                    }
            for dst in ("ru", "en"):
                src = "en" if dst == "ru" else "ru"
                if not place_edition_needs_fill(place, dst):
                    continue
                if not _json_has_usable_narrative_for_edition(place, src):
                    continue
                src_key = "facts" if src == "en" else "facts_ru"
                dst_key = _target_key("facts", dst)
                raw = place.get(src_key) or place.get("facts")
                if not isinstance(raw, list):
                    continue
                for idx, item in enumerate(raw):
                    text = str(item).strip()
                    if not (
                        is_usable_narrative_text(text)
                        and text_for_edition(text, src)
                    ):
                        continue
                    yield {
                        "id": _job_id(
                            city_slug, slug, "facts", src, dst, idx,
                        ),
                        "city": city_slug,
                        "source_file": rel,
                        "slug": slug,
                        "field": "facts",
                        "fact_index": idx,
                        "src_lang": src,
                        "dst_lang": dst,
                        "source_text": text,
                        "target_key": dst_key,
                        "kind": "prose",
                    }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        if isinstance(obj, dict):
            out.append(obj)
    return out


def collab_arrays_from_jobs(
    jobs: list[dict[str, Any]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    en_to_ru: list[dict[str, str]] = []
    ru_to_en: list[dict[str, str]] = []
    for job in jobs:
        row = {
            "id": str(job["id"]),
            "text": str(job["source_text"]),
        }
        if job.get("src_lang") == "en":
            en_to_ru.append(row)
        else:
            ru_to_en.append(row)
    return en_to_ru, ru_to_en


def ru_slug_title_jobs(
    project_root: Path,
    city_slug: str,
) -> list[dict[str, Any]]:
    """Places whose RU title looks like a slug but EN name exists."""
    jobs: list[dict[str, Any]] = []
    data_dir = project_root / city_slug / "data"
    for path in _place_files(data_dir, city_slug):
        rel = path.relative_to(project_root).as_posix()
        for place in _load_places(path):
            slug = str(place.get("slug") or "").strip()
            if not slug:
                continue
            ru_name = polish_display_title(
                str(place.get("name_ru") or place.get("name") or ""),
            )
            if not ru_name or not _SLUG_TITLE_RE.fullmatch(ru_name):
                continue
            en_name = _best_source_text(place, _NAME_BASE, "en")
            if not en_name:
                continue
            jobs.append({
                "id": _job_id(city_slug, slug, "name_ru_from_en", "en", "ru", None),
                "city": city_slug,
                "source_file": rel,
                "slug": slug,
                "field": "name",
                "src_lang": "en",
                "dst_lang": "ru",
                "source_text": en_name,
                "target_key": "name_ru",
                "kind": "name",
            })
    return jobs
