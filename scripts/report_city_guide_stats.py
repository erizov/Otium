# -*- coding: utf-8 -*-
"""Summarise place counts, image files, and missing fields per city guide."""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_core import is_curated_place_row
from scripts.city_guide_core import is_substantive_text
from scripts.city_guide_core import PDF_MAX_IMAGES_PER_PLACE
from scripts.city_guide_core import smallest_same_stem_image_rel

_README = _PROJECT_ROOT / "docs" / "CITY_GUIDES_README.md"
_SECTION_START = "<!-- city-guide-stats -->\n"
_SECTION_END = "<!-- /city-guide-stats -->\n"

_ROOT_README = _PROJECT_ROOT / "README.md"
_PLACE_COUNTS_START = "<!-- city-guide-place-counts -->\n"
_PLACE_COUNTS_END = "<!-- /city-guide-place-counts -->\n"
_IMAGE_PER_PLACE_START = "<!-- city-guide-image-per-place -->\n"
_IMAGE_PER_PLACE_END = "<!-- /city-guide-image-per-place -->\n"

_IMAGE_SUFFIXES = frozenset({
    ".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg",
})

_REGISTRY: tuple[tuple[str, str, str], ...] = (
    ("amsterdam", "amsterdam.data.places_registry", "AMSTERDAM_PLACES"),
    ("athens", "athens.data.places_registry", "ATHENS_PLACES"),
    ("bangkok", "bangkok.data.places_registry", "BANGKOK_PLACES"),
    ("barcelona", "barcelona.data.places_registry", "BARCELONA_PLACES"),
    ("berlin", "berlin.data.places_registry", "BERLIN_PLACES"),
    ("boston", "boston.data.places_registry", "BOSTON_PLACES"),
    ("budapest", "budapest.data.places_registry", "BUDAPEST_PLACES"),
    ("chernivtsi", "chernivtsi.data.places_registry", "CHERNIVTSI_PLACES"),
    ("copenhagen", "copenhagen.data.places_registry", "COPENHAGEN_PLACES"),
    ("dubai", "dubai.data.places_registry", "DUBAI_PLACES"),
    ("dublin", "dublin.data.places_registry", "DUBLIN_PLACES"),
    ("florence", "florence.data.places_registry", "FLORENCE_PLACES"),
    ("istanbul", "istanbul.data.places_registry", "ISTANBUL_PLACES"),
    ("jerusalem", "jerusalem.data.places_registry", "JERUSALEM_PLACES"),
    ("kazan", "kazan.data.places_registry", "KAZAN_PLACES"),
    ("kharkiv", "kharkiv.data.places_registry", "KHARKIV_PLACES"),
    ("kyiv", "kyiv.data.places_registry", "KYIV_PLACES"),
    ("lisbon", "lisbon.data.places_registry", "LISBON_PLACES"),
    ("london", "london.data.places_registry", "LONDON_PLACES"),
    ("los_angeles", "los_angeles.data.places_registry", "LOS_ANGELES_PLACES"),
    ("lviv", "lviv.data.places_registry", "LVIV_PLACES"),
    ("madrid", "madrid.data.places_registry", "MADRID_PLACES"),
    ("minsk", "minsk.data.places_registry", "MINSK_PLACES"),
    ("montreal", "montreal.data.places_registry", "MONTREAL_PLACES"),
    ("new_york", "new_york.data.places_registry", "NEW_YORK_PLACES"),
    ("novosibirsk", "novosibirsk.data.places_registry", "NOVOSIBIRSK_PLACES"),
    ("odessa", "odessa.data.places_registry", "ODESSA_PLACES"),
    ("paris", "paris.data.places_registry", "PARIS_PLACES"),
    ("philadelphia", "philadelphia.data.places_registry", "PHILADELPHIA_PLACES"),
    ("prague", "prague.data.places_registry", "PRAGUE_PLACES"),
    ("rome", "rome.data.places_registry", "ROME_PLACES"),
    ("san_francisco", "san_francisco.data.places_registry", "SAN_FRANCISCO_PLACES"),
    ("singapore", "singapore.data.places_registry", "SINGAPORE_PLACES"),
    ("smolensk", "smolensk.data.places_registry", "SMOLENSK_PLACES"),
    ("spb", "spb.data.places_registry", "SPB_PLACES"),
    ("tokyo", "tokyo.data.places_registry", "TOKYO_PLACES"),
    ("tver", "tver.data.places_registry", "TVER_PLACES"),
    ("vatican", "vatican.data.places_registry", "VATICAN_PLACES"),
    ("venice", "venice.data.places_registry", "VENICE_PLACES"),
    ("vienna", "vienna.data.places_registry", "VIENNA_PLACES"),
    ("vladivostok", "vladivostok.data.places_registry", "VLADIVOSTOK_PLACES"),
    ("volgograd", "volgograd.data.places_registry", "VOLGOGRAD_PLACES"),
    ("vologda", "vologda.data.places_registry", "VOLOGDA_PLACES"),
    ("yaroslavl", "yaroslavl.data.places_registry", "YAROSLAVL_PLACES"),
)


def _count_images(city_root: Path) -> int:
    img_dir = city_root / "images"
    if not img_dir.is_dir():
        return 0
    n = 0
    for path in img_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in _IMAGE_SUFFIXES:
            n += 1
    return n


def _no_substantive_facts(place: dict) -> bool:
    facts = place.get("facts") or []
    return not any(is_substantive_text(str(f)) for f in facts)


def _substantive_list_count(place: dict, key: str) -> int:
    items = place.get(key) or []
    if not isinstance(items, list):
        return 0
    return sum(1 for x in items if is_substantive_text(str(x)))


def _list_len(place: dict, key: str) -> int:
    items = place.get(key) or []
    return len(items) if isinstance(items, list) else 0


def _fmt_avg(numer: int, denom: int) -> str:
    if denom <= 0:
        return "0.0"
    return "{:.1f}".format(numer / denom)


def _missing_count(places: list[dict], key: str) -> int:
    return sum(
        1 for p in places if not is_substantive_text(p.get(key))
    )


def _load_places(module_name: str, attr: str) -> list[dict]:
    mod = importlib.import_module(module_name)
    raw = getattr(mod, attr)
    return [dict(p) for p in raw]


def _count_pdf_eligible_images(root: Path, place: dict) -> int:
    if place.get("suppress_images_for_pdf"):
        return -1
    n = 0
    rel = place.get("image_rel_path")
    if rel and smallest_same_stem_image_rel(root, rel):
        n += 1
    for item in place.get("additional_images") or []:
        er = item.get("image_rel_path")
        if er and smallest_same_stem_image_rel(root, er):
            n += 1
    return min(n, PDF_MAX_IMAGES_PER_PLACE)


def _image_per_place_row(
    slug: str,
    places: list[dict],
) -> tuple[str, int, int, int, int, int]:
    root = _PROJECT_ROOT / slug
    c0 = c1 = c2 = cskip = 0
    for p in places:
        n = _count_pdf_eligible_images(root, p)
        if n < 0:
            cskip += 1
        elif n == 0:
            c0 += 1
        elif n == 1:
            c1 += 1
        else:
            c2 += 1
    return slug, len(places), cskip, c0, c1, c2


def build_image_per_place_section() -> str:
    """Markdown table: places with 0 / 1 / 2 on-disk PDF images per city."""
    rows: list[tuple[str, int, int, int, int, int]] = []
    for slug, mod, attr in _REGISTRY:
        rows.append(_image_per_place_row(slug, _load_places(mod, attr)))
    moscow_path = _PROJECT_ROOT / "moscow" / "data" / "moscow_places.json"
    moscow_places = json.loads(moscow_path.read_text(encoding="utf-8"))
    rows.append(_image_per_place_row("moscow", moscow_places))
    rows.sort(key=lambda r: r[0])

    t0 = t1 = t2 = 0
    body_lines: list[str] = []
    for slug, total, skip, c0, c1, c2 in rows:
        body_lines.append(
            "| `{}` | {} | {} | {} | {} | {} |\n".format(
                slug, total, skip, c0, c1, c2,
            ),
        )
        t0 += c0
        t1 += c1
        t2 += c2
    eligible = sum(r[1] - r[2] for r in rows)
    intro = (
        "## Place images per city\n\n"
        "On-disk raster count per registry place (primary + "
        "``additional_images``, capped at 2). **skip** = "
        "``suppress_images_for_pdf``. Refresh: "
        "``python scripts/report_city_guide_stats.py --write-readme`` "
        "or ``python scripts/stats_city_guide_images_per_place.py``.\n\n"
        "| City | places | skip | 0 img | 1 img | 2 img |\n"
        "|------|-------:|-----:|------:|------:|------:|\n"
    )
    footer = (
        "\n| **TOTAL** | **{}** | **{}** | **{}** | **{}** | **{}** |\n"
        "\n**PDF-eligible:** {} places · **0 img:** {} ({:.1f}%) · "
        "**1 img:** {} ({:.1f}%) · **2 img:** {} ({:.1f}%).\n"
    ).format(
        sum(r[1] for r in rows),
        sum(r[2] for r in rows),
        t0,
        t1,
        t2,
        eligible,
        t0,
        100.0 * t0 / eligible if eligible else 0.0,
        t1,
        100.0 * t1 / eligible if eligible else 0.0,
        t2,
        100.0 * t2 / eligible if eligible else 0.0,
    )
    return (
        _IMAGE_PER_PLACE_START
        + intro
        + "".join(body_lines)
        + footer
        + _IMAGE_PER_PLACE_END
    )


def _markdown_table(rows: list[tuple[str, ...]]) -> str:
    header = (
        "| City | Places | Images | obj/place | "
        "no year | no style | no addr | no desc | "
        "no facts | no history | no sig. |\n"
    )
    sep = (
        "|------|-------:|-------:|----------:|"
        "--------:|---------:|--------:|---------:|"
        "----------:|-----------:|---------:|\n"
    )
    lines = [header, sep]
    for r in rows:
        lines.append("| {} |\n".format(" | ".join(str(x) for x in r)))
    return "".join(lines)


def _curated_counts_from_json() -> list[tuple[str, int, int]]:
    """Return (city_slug, curated_count, expand_count) sorted by city."""
    from scripts.city_guide_registry_common import pdf_expand_sidecar_paths

    rows: list[tuple[str, int, int]] = []
    for main in sorted(_PROJECT_ROOT.glob("*/data/*_places.json")):
        city = main.parent.parent.name
        raw = json.loads(main.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            continue
        curated = sum(
            1
            for p in raw
            if isinstance(p, dict) and is_curated_place_row(p)
        )
        expand_n = 0
        for expand_path in pdf_expand_sidecar_paths(main.parent, city):
            if not expand_path.is_file():
                continue
            expand_raw = json.loads(expand_path.read_text(encoding="utf-8"))
            if isinstance(expand_raw, list):
                expand_n += len(expand_raw)
        rows.append((city, curated, expand_n))
    return rows


def build_place_counts_section() -> str:
    """Markdown table of unique curated places per city (from ``*_places.json``)."""
    rows = _curated_counts_from_json()
    total_places = sum(n for _city, n, _ex in rows)
    total_expand = sum(ex for _city, _n, ex in rows)
    intro = (
        "## Unique places per city\n\n"
        "Curated rows in ``<city>/data/<city>_places.json`` after heading/image "
        "dedup (PDF size-band fillers excluded). Run global dedup first: "
        "``python scripts/dedupe_city_guide_places.py --write``.\n\n"
        "Refresh: ``python scripts/report_city_guide_stats.py --write-readme``\n\n"
    )
    header = "| City | Places |\n|------|-------:|\n"
    body = "".join(
        "| `{}` | {} |\n".format(city, n)
        for city, n, _ex in rows
    )
    footer = (
        "\n**Totals:** {} cities · **{}** unique curated places · "
        "{} PDF expand sidecar rows (filler images; not counted in Places).\n"
    ).format(len(rows), total_places, total_expand)
    return _PLACE_COUNTS_START + intro + header + body + footer + _PLACE_COUNTS_END


def _write_marked_section(
    path: Path,
    section: str,
    start: str,
    end: str,
) -> None:
    old = path.read_text(encoding="utf-8") if path.is_file() else ""
    if start in old and end in old:
        head, _, tail = old.partition(start)
        _, _, tail = tail.partition(end)
        new = head + section + tail
    else:
        sep = "" if old.endswith("\n\n") or not old.strip() else "\n\n"
        new = old.rstrip() + sep + section + "\n"
    path.write_text(new, encoding="utf-8")


def build_chart_section() -> str:
    out_rows: list[tuple[str, ...]] = []
    for slug, mod, attr in _REGISTRY:
        city_root = _PROJECT_ROOT / slug
        all_places = _load_places(mod, attr)
        places = [p for p in all_places if is_curated_place_row(p)]
        n_pl = len(places)
        n_im = _count_images(city_root)
        n_facts = sum(_substantive_list_count(p, "facts") for p in places)
        n_stories = sum(_substantive_list_count(p, "stories") for p in places)
        n_extra = sum(_list_len(p, "additional_images") for p in places)
        n_objects = n_facts + n_stories + n_extra
        out_rows.append(
            (
                "`{}`".format(slug),
                str(n_pl),
                str(n_im),
                _fmt_avg(n_objects, n_pl),
                str(_missing_count(places, "year_built")),
                str(_missing_count(places, "architecture_style")),
                str(_missing_count(places, "address")),
                str(_missing_count(places, "description")),
                str(sum(1 for p in places if _no_substantive_facts(p))),
                str(_missing_count(places, "history")),
                str(_missing_count(places, "significance")),
            ),
        )
    table = _markdown_table(out_rows)
    intro = (
        "## Registry statistics\n\n"
        "Merged registries (`*places.json` + detail JSON; PDF fillers excluded). "
        "**Images** = raster/SVG files under `<city>/images/` (recursive). "
        "**obj/place** = average count of substantive list items per place "
        "(facts + stories + additional_images). "
        "Columns **no year** through **no sig.** count places where that "
        "field is missing or placeholder-only (`—`, `-`, `n/a`, …), using "
        "`is_substantive_text()` in `scripts/city_guide_core.py`. "
        "**no facts** means no substantive `facts` list item.\n\n"
        "Refresh: `python scripts/report_city_guide_stats.py --write`\n\n"
    )
    return _SECTION_START + intro + table + _SECTION_END


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="Update docs/CITY_GUIDES_README.md with the registry chart.",
    )
    parser.add_argument(
        "--write-readme",
        action="store_true",
        help="Update README.md with the unique-places-per-city table.",
    )
    parser.add_argument(
        "--fail-desc-pct",
        type=float,
        default=None,
        metavar="PCT",
        help="Exit 1 if any city has more than PCT%% missing descriptions.",
    )
    args = parser.parse_args()
    section = build_chart_section()
    if args.fail_desc_pct is not None:
        threshold = float(args.fail_desc_pct)
        for slug, mod, attr in _REGISTRY:
            places = [
                p for p in _load_places(mod, attr) if is_curated_place_row(p)
            ]
            if not places:
                continue
            n_miss = _missing_count(places, "description")
            pct = 100.0 * n_miss / len(places)
            if pct > threshold:
                print(
                    "FAIL {}: {:.0f}%% missing description (> {:.0f}%%)".format(
                        slug,
                        pct,
                        threshold,
                    ),
                    file=sys.stderr,
                )
                return 1
    if args.write:
        _write_marked_section(_README, section, _SECTION_START, _SECTION_END)
        print("Wrote chart into", _README, file=sys.stderr)
    if args.write_readme:
        counts = build_place_counts_section()
        _write_marked_section(
            _ROOT_README,
            counts,
            _PLACE_COUNTS_START,
            _PLACE_COUNTS_END,
        )
        images = build_image_per_place_section()
        _write_marked_section(
            _ROOT_README,
            images,
            _IMAGE_PER_PLACE_START,
            _IMAGE_PER_PLACE_END,
        )
        print("Wrote place counts into", _ROOT_README, file=sys.stderr)
        print("Wrote image-per-place stats into", _ROOT_README, file=sys.stderr)
    if not args.write and not args.write_readme:
        if args.fail_desc_pct is None:
            sys.stdout.write(section)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
