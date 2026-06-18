# -*- coding: utf-8 -*-
"""Audit Moscow output PDFs vs unified moscow_guide; write moscow_pdf.json."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from html import unescape
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_core import places_for_pdf
from scripts.city_guide_narrative import (
    GuideNarrativeDeduper,
    merge_narrative_html,
    text_for_edition,
)
from scripts.guide_constants import BUILD_GUIDES

_MOSCOW_OUT = _PROJECT_ROOT / "moscow" / "output"
_REPORT = _PROJECT_ROOT / "moscow" / "data" / "moscow_pdf.json"

_CATEGORY_STEMS = tuple("{}_guide".format(g) for g in BUILD_GUIDES) + (
    "cafes_guide",
    "Moscow_Complete_Guide",
)
_UNIFIED_STEMS = ("moscow_guide_en", "moscow_guide_ru")


def _scan_pdfs(out_dir: Path) -> list[Path]:
    """Canonical top-level Moscow output PDFs (no backups / bare stems)."""
    out: list[Path] = []
    for pdf in sorted(out_dir.glob("*.pdf")):
        if pdf.parent != out_dir:
            continue
        name = pdf.name
        if re.search(r"_\d{8}_\d{6}\.pdf$", name):
            continue
        if name in ("Moscow_Complete.pdf",):
            continue
        stem = pdf.stem
        if stem.endswith("_opt"):
            continue
        if stem.endswith("_guide") or stem in _UNIFIED_STEMS:
            out.append(pdf)
            continue
        if stem == "moscow_guide":
            out.append(pdf)
            continue
        if stem == "Moscow_Complete_Guide":
            out.append(pdf)
    return out


def _norm(name: str) -> str:
    s = unescape(name or "").strip().lower()
    s = re.sub(r"^\d+\.\s*", "", s)
    s = re.sub(r"\s+", " ", s)
    s = s.replace("ё", "е")
    return s


def _parse_category_html(path: Path) -> list[str]:
    """Titles from legacy category guide HTML (``h2.monastery-title``)."""
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    titles: list[str] = []
    for m in re.finditer(
        r'<h2 class="monastery-title">([^<]+)</h2>',
        text,
    ):
        title = unescape(m.group(1).strip())
        title = re.sub(r"^\d+\.\s*", "", title).strip()
        if title:
            titles.append(title)
    return titles


def _parse_unified_html(path: Path) -> list[str]:
    """Place slugs from Jerusalem-style unified guide HTML."""
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    return re.findall(r'<section class="place" id="([^"]+)"', text)


def _pdf_inventory_row(path: Path) -> dict[str, Any]:
    st = path.stat()
    stem = path.stem
    html = path.with_suffix(".html")
    if stem.endswith("_opt"):
        html = _MOSCOW_OUT / ("{}.html".format(stem.replace("_opt", "")))
    place_count = 0
    if stem in _UNIFIED_STEMS or stem == "moscow_guide":
        slugs = _parse_unified_html(html)
        place_count = len(slugs)
    elif html.is_file():
        place_count = len(_parse_category_html(html))
    return {
        "file": path.name,
        "path": str(path.relative_to(_PROJECT_ROOT)).replace("\\", "/"),
        "bytes": st.st_size,
        "mtime_iso": st.st_mtime,
        "html_companion": html.name if html.is_file() else None,
        "place_count": place_count,
    }


def _build_lookup(
    rows: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    by_norm: dict[str, dict[str, Any]] = {}
    for row in rows:
        for key in ("name_ru", "name_en", "name"):
            n = _norm(str(row.get(key) or ""))
            if n:
                by_norm[n] = row
    return by_norm


def _match_slug(
    title: str,
    by_norm: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    cn = _norm(title)
    if cn in by_norm:
        return by_norm[cn]
    best: dict[str, Any] | None = None
    best_len = 0
    for jn, place in by_norm.items():
        if cn in jn or jn in cn:
            overlap = min(len(cn), len(jn))
            if overlap > best_len:
                best_len = overlap
                best = place
    return best


def _display_name(place: dict[str, Any], edition: str) -> str:
    if edition == "en":
        for key in ("name_en", "subtitle_en"):
            val = str(place.get(key) or "").strip()
            if val and text_for_edition(val, "en"):
                return val
        hist = str(place.get("history_en") or "").strip()
        if hist and text_for_edition(hist, "en"):
            return hist.split(".")[0].strip()[:80]
        stories = place.get("stories_en") or []
        if stories:
            lead = str(stories[0]).strip()
            if text_for_edition(lead, "en"):
                return lead.split(".")[0].strip()[:80]
        return str(place.get("name_ru") or place.get("name") or "").strip()
    for key in ("name_ru", "name"):
        val = str(place.get(key) or "").strip()
        if val:
            return val
    return str(place.get("slug") or "")


def _edition_needed(row: dict[str, Any]) -> str:
    if row.get("missing_from_unified"):
        if row.get("missing_en") and row.get("missing_ru"):
            return "both"
        if row.get("missing_en"):
            return "en"
        return "ru"
    if row.get("missing_en"):
        return "en"
    if row.get("missing_ru"):
        return "ru"
    return "none"


def _has_en_narrative(place: dict[str, Any]) -> bool:
    html = merge_narrative_html(place, "en", GuideNarrativeDeduper())
    return bool(html.strip())


def _has_ru_narrative(place: dict[str, Any]) -> bool:
    html = merge_narrative_html(place, "ru", GuideNarrativeDeduper())
    return bool(html.strip())


def _dedupe_missing(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_slug: dict[str, dict[str, Any]] = {}
    for row in rows:
        slug = str(row.get("slug") or "")
        if not slug:
            continue
        prev = by_slug.get(slug)
        if prev is None:
            by_slug[slug] = row
            continue
        prev_sources = set(prev.get("source_pdfs") or [])
        prev_sources.update(row.get("source_pdfs") or [])
        prev["source_pdfs"] = sorted(prev_sources)
        for key in ("missing_en", "missing_ru", "missing_from_unified"):
            prev[key] = prev.get(key) or row.get(key)
    return sorted(by_slug.values(), key=lambda r: (
        str(r.get("category") or ""),
        str(r.get("name_ru") or r.get("name_en") or ""),
    ))


def main() -> int:
    out_dir = _MOSCOW_OUT
    if not out_dir.is_dir():
        print("Missing:", out_dir, file=sys.stderr)
        return 2

    pdf_rows: list[dict[str, Any]] = []
    for pdf in _scan_pdfs(out_dir):
        pdf_rows.append(_pdf_inventory_row(pdf))

    places_path = _PROJECT_ROOT / "moscow" / "data" / "moscow_places.json"
    json_places: list[dict[str, Any]] = json.loads(
        places_path.read_text(encoding="utf-8"),
    )
    by_norm = _build_lookup(json_places)
    moscow_root = _PROJECT_ROOT / "moscow"

    unified_en_slugs = set(_parse_unified_html(out_dir / "moscow_guide_en.html"))
    unified_ru_slugs = set(_parse_unified_html(out_dir / "moscow_guide_ru.html"))
    pdf_eligible_slugs = {
        str(p.get("slug") or "")
        for p in places_for_pdf(moscow_root, json_places, city_slug="moscow")
    }

    # Union of places appearing in category / complete PDF companions.
    source_titles: dict[str, set[str]] = {}
    for stem in _CATEGORY_STEMS:
        html = out_dir / "{}.html".format(stem)
        pdf_name = "{}.pdf".format(stem)
        for title in _parse_category_html(html):
            source_titles.setdefault(title, set()).add(pdf_name)

    missing_from_unified: list[dict[str, Any]] = []
    seen_slugs: set[str] = set()

    for title, pdfs in sorted(source_titles.items()):
        place = _match_slug(title, by_norm)
        if place is None:
            missing_from_unified.append(
                {
                    "slug": None,
                    "category": "?",
                    "name_ru": title,
                    "name_en": None,
                    "title_ru": title,
                    "title_en": None,
                    "edition": "both",
                    "missing_from_unified": True,
                    "missing_en": True,
                    "missing_ru": True,
                    "reason": "no_json_match",
                    "has_local_image": False,
                    "source_pdfs": sorted(pdfs),
                },
            )
            continue
        slug = str(place.get("slug") or "")
        if slug in seen_slugs:
            continue
        seen_slugs.add(slug)
        in_en = slug in unified_en_slugs
        in_ru = slug in unified_ru_slugs
        if in_en and in_ru:
            continue
        has_img = slug in pdf_eligible_slugs
        if not has_img:
            reason = "no_local_image"
        else:
            reason = "not_in_unified_pdf"
        name_ru = _display_name(place, "ru")
        name_en = _display_name(place, "en")
        title_en = name_en if name_en and text_for_edition(name_en, "en") else None
        entry = {
            "slug": slug,
            "category": str(place.get("category") or ""),
            "name_ru": name_ru,
            "name_en": title_en,
            "title_ru": name_ru,
            "title_en": title_en,
            "edition": "",
            "missing_from_unified": not (in_en and in_ru),
            "missing_en": not in_en,
            "missing_ru": not in_ru,
            "reason": reason,
            "has_local_image": has_img,
            "source_pdfs": sorted(pdfs),
        }
        entry["edition"] = _edition_needed(entry)
        missing_from_unified.append(entry)

    # Places in unified PDF but thin EN narrative vs RU.
    thin_en: list[dict[str, Any]] = []
    for slug in sorted(unified_en_slugs & unified_ru_slugs):
        place = next(
            (p for p in json_places if str(p.get("slug")) == slug),
            None,
        )
        if place is None:
            continue
        if _has_ru_narrative(place) and not _has_en_narrative(place):
            name_ru = _display_name(place, "ru")
            name_en = _display_name(place, "en")
            title_en = (
                name_en if name_en and text_for_edition(name_en, "en") else None
            )
            entry = {
                "slug": slug,
                "category": str(place.get("category") or ""),
                "name_ru": name_ru,
                "name_en": title_en,
                "title_ru": name_ru,
                "title_en": title_en,
                "edition": "en",
                "missing_from_unified": False,
                "missing_en": True,
                "missing_ru": False,
                "reason": "thin_en_narrative",
                "has_local_image": True,
                "source_pdfs": ["moscow_guide_en.pdf"],
            }
            thin_en.append(entry)

    missing_all = _dedupe_missing(missing_from_unified + thin_en)

    report = {
        "generated_from": str(out_dir.relative_to(_PROJECT_ROOT)).replace(
            "\\", "/",
        ),
        "pdfs_scanned": pdf_rows,
        "unified_en_places": len(unified_en_slugs),
        "unified_ru_places": len(unified_ru_slugs),
        "pdf_eligible_in_json": len(pdf_eligible_slugs),
        "source_pdf_union_places": len(source_titles),
        "missing_total": len(missing_all),
        "missing_not_in_unified": sum(
            1 for r in missing_all if r.get("missing_from_unified")
        ),
        "missing_thin_en_only": sum(
            1 for r in missing_all if r.get("reason") == "thin_en_narrative"
        ),
        "missing_no_image": sum(
            1 for r in missing_all if r.get("reason") == "no_local_image"
        ),
        "by_edition": dict(
            Counter(str(r.get("edition") or "?") for r in missing_all).most_common(),
        ),
        "by_category": dict(
            Counter(str(r.get("category") or "?") for r in missing_all).most_common(),
        ),
        "missing": missing_all,
    }

    _REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("=== Moscow PDF inventory ===")
    print("PDFs (top-level):", len(pdf_rows))
    print("Unified EN/RU places:", len(unified_en_slugs), len(unified_ru_slugs))
    print("Missing items (deduped):", len(missing_all))
    print("  not in unified:", report["missing_not_in_unified"])
    print("  thin EN narrative:", report["missing_thin_en_only"])
    print("  no local image:", report["missing_no_image"])
    print()
    print("By category:")
    for cat, n in Counter(
        str(r.get("category") or "?") for r in missing_all
    ).most_common(12):
        print("  {}: {}".format(cat, n))
    print()
    print("Report:", _REPORT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
