# -*- coding: utf-8 -*-
"""Compare Moscow_Complete guide vs moscow_places.json / built PDF guide."""

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

from scripts.city_guide_core import places_for_pdf
from scripts.guide_loader import GUIDES, load_places

CHAPTER_TO_CATEGORY: dict[int, str] = {
    1: "monasteries",
    2: "places_of_worship",
    3: "parks",
    4: "museums",
    5: "palaces",
    6: "buildings",
    7: "sculptures",
    8: "places",
    9: "squares",
    10: "metro",
    11: "theaters",
    12: "viewpoints",
    13: "bridges",
    14: "markets",
    15: "libraries",
    16: "railway_stations",
    17: "cemeteries",
    18: "landmarks",
    19: "cafes",
    20: "osobnjaki",
}


def _norm(name: str) -> str:
    s = unescape(name or "").strip().lower()
    s = re.sub(r"^\d+\.\s*", "", s)
    s = re.sub(r"\s+", " ", s)
    s = s.replace("ё", "е")
    return s


def _parse_complete_html(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    rows: list[dict[str, Any]] = []
    current_ch: int | None = None
    for line in text.splitlines():
        m_ch = re.search(
            r'id="ch-(\d+)"',
            line,
        )
        if m_ch and "chapter-intro" in line:
            current_ch = int(m_ch.group(1))
        m_title = re.search(
            r'<h2 class="monastery-title">([^<]+)</h2>',
            line,
        )
        if m_title:
            title = unescape(m_title.group(1).strip())
            title = re.sub(r"^\d+\.\s*", "", title).strip()
            rows.append(
                {
                    "title": title,
                    "chapter": current_ch,
                    "category": CHAPTER_TO_CATEGORY.get(current_ch or 0, "?"),
                },
            )
    return rows


def _match_place(
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


def _load_json_places() -> list[dict[str, Any]]:
    path = _PROJECT_ROOT / "moscow" / "data" / "moscow_places.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _registry_counts() -> dict[str, int]:
    out: dict[str, int] = {}
    for guide in GUIDES:
        out[guide] = len(load_places(guide))
    return out


def main() -> int:
    complete_html = _PROJECT_ROOT / "moscow" / "output" / (
        "Moscow_Complete_Guide.html"
    )
    if not complete_html.is_file():
        print("Missing:", complete_html, file=sys.stderr)
        return 2

    complete_rows = _parse_complete_html(complete_html)
    json_places = _load_json_places()
    by_norm: dict[str, dict[str, Any]] = {}
    for p in json_places:
        for key in ("name_ru", "name_en"):
            n = _norm(str(p.get(key) or ""))
            if n:
                by_norm[n] = p

    missing_json: list[dict[str, Any]] = []
    matched_json = 0
    for row in complete_rows:
        if _match_place(row["title"], by_norm):
            matched_json += 1
        else:
            missing_json.append(row)

    # PDF inclusion (image filter)
    moscow_root = _PROJECT_ROOT / "moscow"

    pdf_places = places_for_pdf(
        moscow_root,
        json_places,
        city_slug="moscow",
        sort_key=lambda p: str(p.get("name_ru") or p.get("name_en") or ""),
    )
    pdf_slugs = {str(p.get("slug")) for p in pdf_places}

    in_pdf = 0
    not_in_pdf: list[dict[str, Any]] = []
    no_narrative: list[dict[str, Any]] = []
    for row in complete_rows:
        place = _match_place(row["title"], by_norm)
        if not place:
            continue
        slug = str(place.get("slug") or "")
        if slug in pdf_slugs:
            in_pdf += 1
            hist = str(place.get("history") or "").strip()
            desc = str(place.get("description_ru") or place.get("description") or "")
            if not hist and not desc and not place.get("facts"):
                no_narrative.append(
                    {"title": row["title"], "slug": slug},
                )
        else:
            not_in_pdf.append(
                {
                    "title": row["title"],
                    "slug": slug,
                    "category": row["category"],
                    "has_image_field": bool(place.get("image_rel_path")),
                },
            )

    reg = _registry_counts()
    print("=== Moscow Complete vs city guide gap ===")
    print("Complete guide places:", len(complete_rows))
    print("moscow_places.json:", len(json_places))
    print("Registry total (data/*.py):", sum(reg.values()))
    print("In PDF (with image):", len(pdf_slugs))
    print()
    print("Matched Complete -> JSON:", matched_json)
    print("Missing from JSON entirely:", len(missing_json))
    print("Matched but excluded from PDF:", len(not_in_pdf))
    print("In PDF but thin narrative:", len(no_narrative))
    print()

    if missing_json:
        print("-- Missing from moscow_places.json (by chapter) --")
        by_cat = Counter(r["category"] for r in missing_json)
        for cat, n in by_cat.most_common():
            print("  {}: {}".format(cat, n))
        print("  Examples:")
        for row in missing_json[:15]:
            print("    [{}] {}".format(
                row["category"],
                row["title"].encode("utf-8", "replace").decode("utf-8"),
            ))

    if not_in_pdf:
        print()
        print("-- In JSON but not in PDF (no usable image) --")
        by_cat2 = Counter(r["category"] for r in not_in_pdf)
        for cat, n in by_cat2.most_common():
            print("  {}: {}".format(cat, n))
        print("  Examples:")
        for row in not_in_pdf[:15]:
            print("    [{}] {} ({})".format(
                row["category"],
                row["title"].encode("utf-8", "replace").decode("utf-8"),
                row["slug"],
            ))

    print()
    print("=== Summary ===")
    complete_in_pdf = matched_json - len(not_in_pdf)
    print(
        "Complete guide coverage in city PDF: {}/{} ({:.0f}%)".format(
            complete_in_pdf,
            len(complete_rows),
            100.0 * complete_in_pdf / max(len(complete_rows), 1),
        ),
    )
    print(
        "Registry places with images on disk: {}/{}".format(
            len(pdf_slugs),
            len(json_places),
        ),
    )

    report_path = _PROJECT_ROOT / "moscow" / "data" / "moscow_complete_gap.json"
    report_path.write_text(
        json.dumps(
            {
                "complete_total": len(complete_rows),
                "json_total": len(json_places),
                "registry_total": sum(reg.values()),
                "pdf_total": len(pdf_slugs),
                "missing_from_json": missing_json,
                "excluded_from_pdf": not_in_pdf,
                "thin_narrative_in_pdf": no_narrative,
                "registry_by_guide": reg,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print()
    print("Full report:", report_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
