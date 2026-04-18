# -*- coding: utf-8 -*-
"""Verify each place has a primary image file on disk (>= min bytes)."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_core import min_bytes_for_filename

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


def _load_places(module_name: str, attr: str) -> list[dict]:
    mod = importlib.import_module(module_name)
    raw = getattr(mod, attr)
    return [dict(p) for p in raw]


def _check_city(
    slug: str,
    module_name: str,
    attr: str,
    min_places: int,
) -> list[str]:
    errs: list[str] = []
    root = _PROJECT_ROOT / slug
    try:
        places = _load_places(module_name, attr)
    except Exception as exc:
        return ["{}: import/load failed: {}".format(slug, exc)]
    if min_places > 0 and len(places) < min_places:
        errs.append(
            "{}: expected >= {} places, got {}".format(
                slug, min_places, len(places),
            ),
        )
    for i, p in enumerate(places):
        name = p.get("name_en", p.get("slug", "?"))
        rel = p.get("image_rel_path")
        if not rel:
            errs.append(
                "{} place {} ({!r}): missing image_rel_path".format(
                    slug, i + 1, name,
                ),
            )
            continue
        path = (root / rel).resolve()
        try:
            path.relative_to(root.resolve())
        except ValueError:
            errs.append(
                "{} place {} ({!r}): image path escapes city root".format(
                    slug, i + 1, name,
                ),
            )
            continue
        if not path.is_file():
            errs.append(
                "{} place {} ({!r}): missing file {}".format(
                    slug, i + 1, name, rel,
                ),
            )
            continue
        size = path.stat().st_size
        floor = min_bytes_for_filename(path.name)
        if size < floor:
            errs.append(
                "{} place {} ({!r}): {} too small ({} < {})".format(
                    slug, i + 1, name, rel, size, floor,
                ),
            )
    return errs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cities",
        nargs="*",
        metavar="SLUG",
        help="only these slugs (default: all registry rows)",
    )
    parser.add_argument(
        "--min-places",
        type=int,
        default=0,
        metavar="N",
        help="fail if any selected city has fewer than N places (default 0)",
    )
    args = parser.parse_args()
    want = frozenset(args.cities) if args.cities else None
    all_errs: list[str] = []
    for slug, mod, attr in _REGISTRY:
        if want is not None and slug not in want:
            continue
        all_errs.extend(
            _check_city(slug, mod, attr, args.min_places),
        )
    if all_errs:
        for line in all_errs:
            print(line, file=sys.stderr)
        return 1
    print("OK:", len(_REGISTRY), "guides checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
