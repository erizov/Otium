# -*- coding: utf-8 -*-
"""Build EN narrative fill jobs for places missing English text."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterator, Mapping

from scripts.city_guide_naming import (
    is_pdf_filler_slug,
    title_from_place_slug,
)
from scripts.city_guide_narrative import polish_display_title
from scripts.city_guide_registry_common import pdf_expand_sidecar_paths
from scripts.city_guide_sparse_narrative import (
    _json_has_usable_narrative_for_edition,
    place_edition_needs_fill,
)
from scripts.rag.city_map import names_for_slug

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
    paths.extend(pdf_expand_sidecar_paths(data_dir, city_slug))
    return paths


def _load_places(path: Path) -> list[dict[str, Any]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        return []
    return [p for p in raw if isinstance(p, dict)]


def _place_name_en(place: Mapping[str, Any]) -> str:
    for key in ("name_en", "name", "subtitle_en"):
        raw = polish_display_title(str(place.get(key) or ""))
        if raw and not _SLUG_TITLE_RE.fullmatch(raw):
            if not re.search(r"[\u0400-\u04FF]", raw):
                return raw
    slug = str(place.get("slug") or "")
    if slug and not is_pdf_filler_slug(slug):
        return title_from_place_slug(slug)
    return slug or "?"


def _hint_lines(place: Mapping[str, Any]) -> list[str]:
    hints: list[str] = []
    for key in (
        "address",
        "year_built",
        "architecture_style",
        "category",
        "subtitle_en",
        "subtitle_ru",
    ):
        val = str(place.get(key) or "").strip()
        if val:
            hints.append("{}: {}".format(key, val))
    return hints


def build_en_significance_prompt(
    *,
    city_slug: str,
    place: Mapping[str, Any],
) -> str:
    """Colab/LLM prompt: historical, political, cultural, religious angles."""
    names = names_for_slug(city_slug)
    city_name = names.name_en
    place_name = _place_name_en(place)
    slug = str(place.get("slug") or "").strip()
    hints = _hint_lines(place)
    hint_block = "\n".join(hints) if hints else "(none in registry)"
    ru_note = ""
    if _json_has_usable_narrative_for_edition(place, "ru"):
        ru_note = (
            "\nNote: Russian narrative exists in the registry — "
            "use it only as a hint; write fresh English, do not translate "
            "word-for-word unless facts match.\n"
        )
    return (
        "You write English text for a printed city guide (OTIUM).\n\n"
        "City: {city} (slug: {city_slug})\n"
        "Place: {place} (slug: {slug})\n"
        "Registry hints:\n{hints}\n"
        "{ru_note}"
        "Write about THIS place in THIS city only. Cover what you are "
        "confident about across these angles:\n"
        "1. Historical significance (founding, dates, key events)\n"
        "2. Political significance (if any — power, borders, protests, "
        "state roles; omit if not applicable)\n"
        "3. Cultural significance (art, heritage, daily life, UNESCO, "
        "traditions)\n"
        "4. Religious significance (if any — faith, rites, pilgrimage; "
        "omit or note secular use if not applicable)\n\n"
        "Rules:\n"
        "- Do NOT invent facts, dates, names, or quotes.\n"
        "- If uncertain, omit the claim or use cautious wording.\n"
        "- Put folklore/legends only in stories_en[], not in facts.\n"
        "- facts_en[]: short verifiable bullets only.\n"
        "- Do not repeat the same sentence in description, history, "
        "and significance.\n\n"
        "Return JSON only:\n"
        "{{\n"
        '  "description_en": "2-4 sentence visitor overview",\n'
        '  "history_en": "paragraph or empty string",\n'
        '  "significance_en": "paragraph on political/cultural/religious '
        'import as relevant",\n'
        '  "facts_en": ["...", "..."],\n'
        '  "stories_en": ["optional legend ..."]\n'
        "}}\n"
    ).format(
        city=city_name,
        city_slug=city_slug,
        place=place_name,
        slug=slug,
        hints=hint_block,
        ru_note=ru_note,
    )


def iter_en_narrative_fill_jobs(
    project_root: Path,
    city_slug: str,
) -> Iterator[dict[str, Any]]:
    """Places missing usable English narrative in JSON."""
    data_dir = project_root / city_slug / "data"
    names = names_for_slug(city_slug)
    for path in _place_files(data_dir, city_slug):
        rel = path.relative_to(project_root).as_posix()
        for place in _load_places(path):
            slug = str(place.get("slug") or "").strip()
            if not slug or is_pdf_filler_slug(slug):
                continue
            if not place_edition_needs_fill(place, "en"):
                continue
            has_ru = _json_has_usable_narrative_for_edition(place, "ru")
            job_id = "{}/{}".format(city_slug, slug)
            yield {
                "id": job_id,
                "city_slug": city_slug,
                "city_name_en": names.name_en,
                "slug": slug,
                "place_name_en": _place_name_en(place),
                "source_file": rel,
                "has_ru_source": has_ru,
                "suggested_action": "translate_from_ru" if has_ru else "llm_generate_en",
                "prompt": build_en_significance_prompt(
                    city_slug=city_slug,
                    place=place,
                ),
            }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
