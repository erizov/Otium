# -*- coding: utf-8 -*-
"""Patch German guide images (exterior) and localized addresses."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.city_guide_jerusalem_style_images import (  # noqa: E402
    _candidate_urls,
    _download_place_image,
)

PLACES = ROOT / "german_architecture" / "data" / "german_architecture_places.json"
EXPAND = (
    ROOT
    / "german_architecture"
    / "data"
    / "german_architecture_places_pdf_expand.json"
)
GUIDE = ROOT / "german_architecture"

# slug -> Wikimedia Commons (exterior, >= ~1200 px where possible)
PRIMARY_URLS: dict[str, str] = {
    "roman_germania_porta_nigra": (
        "https://upload.wikimedia.org/wikipedia/commons/d/d3/"
        "Trier_Porta_Nigra.jpg"
    ),
    "romanesque_worms": (
        "https://upload.wikimedia.org/wikipedia/commons/5/5d/"
        "Worms-Dom_St_Peter_02-2007-gje.jpg"
    ),
    "romanesque_speyer": (
        "https://upload.wikimedia.org/wikipedia/commons/e/ea/"
        "Speyer_-_Altstadt_-_Altp%C3%B6rtel_-_Blick_auf_Domfassade_"
        "und_Kircht%C3%BCrme_mit_Abendsonne.jpg"
    ),
    "romanesque_mainz": (
        "https://upload.wikimedia.org/wikipedia/commons/4/49/"
        "Mainz_Cathedral.jpg"
    ),
    "gothic_marienkirche_lubeck": (
        "https://upload.wikimedia.org/wikipedia/commons/2/21/"
        "Marienkirche_L%C3%BCbeck.jpg"
    ),
    "gothic_regensburg_cathedral": (
        "https://upload.wikimedia.org/wikipedia/commons/7/77/"
        "GER_Regensburg%2C_Dom_St._Peter_0001.jpg"
    ),
    "gothic_ulm_minster": (
        "https://upload.wikimedia.org/wikipedia/commons/b/b0/"
        "ULM_a._Donau._Westansicht_des_M%C3%BCnsters.jpg"
    ),
    "renaissance_heidelberg": (
        "https://upload.wikimedia.org/wikipedia/commons/c/c2/"
        "Old_town_of_Heidelberg%2C_Castle_and_Old_Bridge_2.jpg"
    ),
    "baroque_dresden_frauenkirche": (
        "https://upload.wikimedia.org/wikipedia/commons/2/22/"
        "Dresden_Frauenkirche.jpg"
    ),
    "baroque_schonbrunn": (
        "https://upload.wikimedia.org/wikipedia/commons/c/c0/"
        "Schloss_Sch%C3%B6nbrunn_Wien_2014.jpg"
    ),
    "rococo_wieskirche": (
        "https://upload.wikimedia.org/wikipedia/commons/1/19/Wieskirche.jpg"
    ),
    "rococo_zwinger": (
        "https://upload.wikimedia.org/wikipedia/commons/e/ee/"
        "Sachsen%2C_Dresden%2C_Zwinger_NIK_7197.jpg"
    ),
    "neoclassicism_walhalla": (
        "https://upload.wikimedia.org/wikipedia/commons/5/5e/"
        "Walhalla_Donaustauf.jpg"
    ),
    "historicism_new_synagogue_berlin": (
        "https://upload.wikimedia.org/wikipedia/commons/a/a0/"
        "New_Synagogue_Berlin.jpg"
    ),
    "art_nouveau_hundertwasser": (
        "https://upload.wikimedia.org/wikipedia/commons/7/70/"
        "Hundertwasserhaus.jpg"
    ),
    "art_nouveau_hackesche_hofe": (
        "https://upload.wikimedia.org/wikipedia/commons/f/fe/"
        "Berlin_Hackesche_H%C3%B6fe.jpg"
    ),
    "expressionism_lichtburg": (
        "https://upload.wikimedia.org/wikipedia/commons/8/87/"
        "Lichtburg_Essen.jpg"
    ),
    "nazi_monumental_tempelhof": (
        "https://upload.wikimedia.org/wikipedia/commons/4/45/"
        "TempelhofExterior.jpg"
    ),
    "nazi_monumental_reichsparteitag": (
        "https://upload.wikimedia.org/wikipedia/commons/6/66/"
        "Kongresshalle_Nuremberg.jpg"
    ),
    "postwar_modern_berlin_phil": (
        "https://upload.wikimedia.org/wikipedia/commons/6/65/"
        "Berliner_Philharmonie.jpg"
    ),
    "postwar_modern_hansaviertel": (
        "https://upload.wikimedia.org/wikipedia/commons/7/73/"
        "Interbau_Berlin-Hansaviertel_with_snow_2025-02-14_03.jpg"
    ),
    "postwar_modern_krolloper_site": (
        "https://upload.wikimedia.org/wikipedia/commons/9/96/"
        "Kulturforum_Berlin.jpg"
    ),
    "postwar_modern_fernsehturm": (
        "https://upload.wikimedia.org/wikipedia/commons/1/11/"
        "Berlin_TV_Tower.jpg"
    ),
    "brutalism_bielefeld_univ": (
        "https://upload.wikimedia.org/wikipedia/commons/5/52/"
        "Universit%C3%A4t_Bielefeld.jpg"
    ),
}

# PDF expand rows that mirror main slugs
PRIMARY_ALIASES: dict[str, str] = {
    "romanesque_worms_cathedral": "romanesque_worms",
    "romanesque_speyer_cathedral": "romanesque_speyer",
    "romanesque_mainz_cathedral": "romanesque_mainz",
}

# address_ru, address_en — Germany-local conventions
ADDRESSES: dict[str, tuple[str, str]] = {
    "roman_germania_porta_nigra": (
        "Порта-Нигра-плац, 54290 Трир",
        "Porta-Nigra-Platz, 54290 Trier",
    ),
    "romanesque_worms": (
        "Домплац, 1, 67547 Вормс",
        "Domplatz 1, 67547 Worms",
    ),
    "romanesque_speyer": (
        "Домплац, 67346 Шпайер",
        "Domplatz, 67346 Speyer",
    ),
    "romanesque_mainz": (
        "Маркт, 10, 55116 Майнц",
        "Markt 10, 55116 Mainz",
    ),
    "gothic_marienkirche_lubeck": (
        "Мариенкирххоф, 1, 23552 Любек",
        "Marienkirchhof 1, 23552 Lübeck",
    ),
    "gothic_regensburg_cathedral": (
        "Домплац, 5, 93047 Регенсбург",
        "Domplatz 5, 93047 Regensburg",
    ),
    "gothic_ulm_minster": (
        "Мюнстерплац, 21, 89073 Ульм",
        "Münsterplatz 21, 89073 Ulm",
    ),
    "renaissance_heidelberg": (
        "Шлоссхоф, 1, 69117 Гейдельберг",
        "Schlosshof 1, 69117 Heidelberg",
    ),
    "baroque_dresden_frauenkirche": (
        "Ноймаркт, 01067 Дрезден",
        "Neumarkt, 01067 Dresden",
    ),
    "baroque_schonbrunn": (
        "Шёнбруннер Шлоссштрассе, 47, 1130 Вена",
        "Schönbrunner Schloßstraße 47, 1130 Vienna",
    ),
    "rococo_wieskirche": (
        "Вис, 12, 86989 Штайнгаден",
        "Wies 12, 86989 Steingaden",
    ),
    "rococo_zwinger": (
        "Зофиенштрассе, 01067 Дрезден",
        "Sophienstraße, 01067 Dresden",
    ),
    "neoclassicism_walhalla": (
        "Вальхаллаштрассе, 48, 93093 Донаустауф",
        "Walhallastraße 48, 93093 Donaustauf",
    ),
    "historicism_new_synagogue_berlin": (
        "Ораниенбургер-штрассе, 28–30, 10117 Берлин",
        "Oranienburger Straße 28-30, 10117 Berlin",
    ),
    "art_nouveau_hundertwasser": (
        "Кегельгассе, 36–38, 1030 Вена",
        "Kegelgasse 36-38, 1030 Vienna",
    ),
    "art_nouveau_hackesche_hofe": (
        "Розенталер-штрассе, 40–41, 10178 Берлин",
        "Rosenthaler Straße 40-41, 10178 Berlin",
    ),
    "expressionism_lichtburg": (
        "Лихтбургплац, 1, 45127 Эссен",
        "Lichtburgplatz 1, 45127 Essen",
    ),
    "nazi_monumental_tempelhof": (
        "Плац-дер-Люфтбрюке, 5, 12101 Берлин",
        "Platz der Luftbrücke 5, 12101 Berlin",
    ),
    "nazi_monumental_reichsparteitag": (
        "Байернштрассе, 110, 90478 Нюрнберг",
        "Bayernstraße 110, 90478 Nuremberg",
    ),
    "postwar_modern_berlin_phil": (
        "Херберт-фон-Караян-штрассе, 1, 10785 Берлин",
        "Herbert-von-Karajan-Straße 1, 10785 Berlin",
    ),
    "postwar_modern_hansaviertel": (
        "Альтонаер-штрассе, 10557 Берлин",
        "Altonaer Straße, 10557 Berlin",
    ),
    "postwar_modern_krolloper_site": (
        "Маттэикирхплац, 10785 Берлин",
        "Matthäikirchplatz, 10785 Berlin",
    ),
    "postwar_modern_fernsehturm": (
        "Панорамаштрассе, 1А, 10178 Берлин",
        "Panoramastraße 1A, 10178 Berlin",
    ),
    "brutalism_bielefeld_univ": (
        "Университетсштрассе, 25, 33615 Билефельд",
        "Universitätsstraße 25, 33615 Bielefeld",
    ),
}

ADDRESS_ALIASES: dict[str, str] = dict(PRIMARY_ALIASES)


def _effective_primary(slug: str) -> str | None:
    if slug in PRIMARY_URLS:
        return PRIMARY_URLS[slug]
    base = PRIMARY_ALIASES.get(slug)
    if base:
        return PRIMARY_URLS.get(base)
    return None


def _effective_address(slug: str) -> tuple[str, str] | None:
    if slug in ADDRESSES:
        return ADDRESSES[slug]
    base = ADDRESS_ALIASES.get(slug)
    if base:
        return ADDRESSES.get(base)
    return None


def _patch_row(row: dict[str, Any]) -> dict[str, Any]:
    slug = str(row.get("slug") or "")
    url = _effective_primary(slug)
    addr = _effective_address(slug)
    if not url and not addr:
        return row
    out = dict(row)
    if url:
        out["image_source_url"] = url
    if addr:
        out["address"], out["address_en"] = addr
    return out


def _download_url(url: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    ordered = _candidate_urls(url, 1280)
    ok, _err = _download_place_image(
        ordered,
        dest,
        timeout_sec=60,
        retries_429=6,
        pause_429_sec=55.0,
    )
    return bool(ok and dest.is_file())


def _download_images(by_slug: dict[str, dict[str, Any]], slugs: set[str]) -> None:
    for slug in sorted(slugs):
        row = by_slug.get(slug)
        if not row:
            continue
        url = _effective_primary(slug)
        if not url:
            continue
        dest = GUIDE / str(row["image_rel_path"])
        if dest.is_file():
            dest.unlink(missing_ok=True)
        ok = _download_url(url, dest)
        print("  {} -> {}".format(slug, "ok" if ok else "fail"))
        time.sleep(45.0)


def _write_image_overrides() -> None:
    path = GUIDE / "data" / "image_overrides.py"
    lines = [
        "# -*- coding: utf-8 -*-",
        '"""Explicit image URLs for guide places."""',
        "",
        "from __future__ import annotations",
        "",
        "from typing import Any",
        "",
        "IMAGE_URL_OVERRIDES: dict[str, tuple[str, str | None]] = {",
    ]
    all_slugs = sorted(set(PRIMARY_URLS) | set(PRIMARY_ALIASES))
    for slug in all_slugs:
        url = _effective_primary(slug)
        if not url:
            continue
        lines.append('    "{}": ('.format(slug))
        lines.append('        "{}",'.format(url))
        lines.append("        None,")
        lines.append("    ),")
    lines.extend([
        "}",
        "PRIMARY_IMAGE_REUSE: dict[str, tuple[str, str]] = {}",
        "SECOND_IMAGE_REUSE: dict[str, tuple[str, str]] = {}",
        "",
        "",
        "def apply_image_url_overrides(place: dict[str, Any]) -> dict[str, Any]:",
        '    slug = str(place.get("slug") or "")',
        "    override = IMAGE_URL_OVERRIDES.get(slug)",
        "    if not override:",
        "        return place",
        "    primary, secondary = override",
        "    merged = dict(place)",
        '    merged["image_source_url"] = primary',
        "    if secondary:",
        '        merged["additional_images"] = [{',
        '            "image_source_url": secondary,',
        "        }]",
        "    else:",
        '        merged.pop("additional_images", None)',
        "    return merged",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    places: list[dict[str, Any]] = json.loads(
        PLACES.read_text(encoding="utf-8"),
    )
    places = [_patch_row(r) for r in places]
    PLACES.write_text(
        json.dumps(places, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    expand: list[dict[str, Any]] = json.loads(
        EXPAND.read_text(encoding="utf-8"),
    )
    expand = [_patch_row(r) for r in expand]
    EXPAND.write_text(
        json.dumps(expand, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    _write_image_overrides()

    by_slug = {str(r.get("slug") or ""): r for r in places + expand}
    slugs = set(PRIMARY_URLS) | set(PRIMARY_ALIASES)
    print("Downloading images (throttled)...")
    _download_images(by_slug, slugs)

    print(
        "Patched {} images, {} address sets".format(
            len(PRIMARY_URLS),
            len(ADDRESSES),
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
