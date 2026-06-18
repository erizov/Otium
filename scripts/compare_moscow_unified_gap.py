# -*- coding: utf-8 -*-
"""Places in any Moscow category/complete guide but not in moscow_guide."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from html import unescape
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

_MOSCOW_OUT = _PROJECT_ROOT / "moscow" / "output"
_REPORT = (
    _PROJECT_ROOT / "moscow" / "data" / "moscow_pdf_missing_from_unified.json"
)


def _norm(name: str) -> str:
    s = unescape(name or "").strip().lower()
    s = re.sub(r"^\d+\.\s*", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.replace("ё", "е")


def _parse_category_html(path: Path) -> list[str]:
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


def _parse_unified_slugs(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    text = path.read_text(encoding="utf-8")
    return set(re.findall(r'<section class="place" id="([^"]+)"', text))


def _build_lookup(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    by_norm: dict[str, dict[str, Any]] = {}
    for row in rows:
        for key in ("name_ru", "name_en", "name"):
            n = _norm(str(row.get(key) or ""))
            if n:
                by_norm[n] = row
    return by_norm


def _match_title(
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


def _source_html_files(out_dir: Path) -> list[Path]:
    sources: list[Path] = []
    for html in sorted(out_dir.glob("*_guide.html")):
        stem = html.stem
        if "_opt" in stem or "_edit" in stem:
            continue
        if stem in ("moscow_guide", "moscow_guide_en", "moscow_guide_ru"):
            continue
        sources.append(html)
    complete = out_dir / "Moscow_Complete_Guide.html"
    if complete.is_file():
        sources.append(complete)
    return sources


def main() -> int:
    places_path = _PROJECT_ROOT / "moscow" / "data" / "moscow_places.json"
    places: list[dict[str, Any]] = json.loads(
        places_path.read_text(encoding="utf-8"),
    )
    by_norm = _build_lookup(places)

    unified_path = _MOSCOW_OUT / "moscow_guide.html"
    if not unified_path.is_file():
        unified_path = _MOSCOW_OUT / "moscow_guide_ru.html"
    unified_slugs = _parse_unified_slugs(unified_path)

    sources = _source_html_files(_MOSCOW_OUT)
    missing: dict[str, dict[str, Any]] = {}
    unmatched: list[dict[str, Any]] = []
    by_source: dict[str, list[str]] = defaultdict(list)

    for src in sources:
        for title in _parse_category_html(src):
            place = _match_title(title, by_norm)
            if place is None:
                unmatched.append(
                    {
                        "title_ru": title,
                        "source_guides": [src.name],
                    },
                )
                by_source[src.name].append(title)
                continue
            slug = str(place.get("slug") or "")
            if not slug or slug in unified_slugs:
                continue
            name_ru = str(place.get("name_ru") or place.get("name") or title)
            if slug not in missing:
                missing[slug] = {
                    "slug": slug,
                    "title_ru": name_ru,
                    "title_en": place.get("name_en"),
                    "category": place.get("category"),
                    "source_guides": [],
                }
            missing[slug]["source_guides"].append(src.name)
            by_source[src.name].append(name_ru)

    rows = sorted(
        missing.values(),
        key=lambda r: (str(r.get("category") or ""), str(r.get("title_ru") or "")),
    )
    for row in rows:
        row["source_guides"] = sorted(set(row["source_guides"]))

    report = {
        "unified_html": unified_path.name,
        "unified_place_count": len(unified_slugs),
        "source_guides_scanned": [p.name for p in sources],
        "missing_count": len(rows),
        "unmatched_title_count": len(unmatched),
        "by_category": dict(
            Counter(str(r.get("category") or "?") for r in rows).most_common(),
        ),
        "by_source_guide": {
            k: len(v) for k, v in sorted(by_source.items(), key=lambda x: -len(x[1]))
        },
        "missing": rows,
        "unmatched_titles": unmatched,
    }
    _REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("=== Missing from moscow_guide ===")
    print("Unified:", unified_path.name, "places:", len(unified_slugs))
    print("Missing (in other guides, not unified):", len(rows))
    print()
    print("By category:")
    for cat, n in Counter(str(r.get("category") or "?") for r in rows).most_common():
        print("  {}: {}".format(cat, n))
    print()
    print("Top source guides:")
    for src, n in list(report["by_source_guide"].items())[:10]:
        print("  {}: {}".format(src, n))
    print()
    for row in rows:
        print(
            "[{}] {} ({})".format(
                row.get("category"),
                row.get("title_ru"),
                row.get("slug"),
            ),
        )
        print("    in: {}".format(", ".join(row["source_guides"])))
    print()
    print("Full report:", _REPORT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
