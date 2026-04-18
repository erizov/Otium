# -*- coding: utf-8 -*-
"""Summarise place counts, image files, and missing fields per city guide."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_core import is_substantive_text

_README = _PROJECT_ROOT / "docs" / "CITY_GUIDES_README.md"
_SECTION_START = "<!-- city-guide-stats -->\n"
_SECTION_END = "<!-- /city-guide-stats -->\n"

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


def build_chart_section() -> str:
    out_rows: list[tuple[str, ...]] = []
    for slug, mod, attr in _REGISTRY:
        city_root = _PROJECT_ROOT / slug
        places = _load_places(mod, attr)
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
        "Merged registries (`*places.json` + detail JSON where applicable). "
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
        help="Update docs/CITY_GUIDES_README.md with this chart.",
    )
    args = parser.parse_args()
    section = build_chart_section()
    if args.write:
        old = _README.read_text(encoding="utf-8") if _README.is_file() else ""
        if _SECTION_START in old and _SECTION_END in old:
            head, _, tail = old.partition(_SECTION_START)
            _, _, tail = tail.partition(_SECTION_END)
            new = head + section + tail
        else:
            sep = "" if old.endswith("\n\n") or not old.strip() else "\n\n"
            new = old.rstrip() + sep + section + "\n"
        _README.write_text(new, encoding="utf-8")
        print("Wrote chart into", _README, file=sys.stderr)
    else:
        sys.stdout.write(section)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
