# -*- coding: utf-8 -*-
"""Patch American guide images (batch 2) and localized addresses."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from american_architecture.data.image_reuse import extra_image_rel  # noqa: E402
from scripts.city_guide_jerusalem_style_images import (  # noqa: E402
    _candidate_urls,
    _download_place_image,
)

PLACES = ROOT / "american_architecture" / "data" / "american_architecture_places.json"
EXPAND = (
    ROOT
    / "american_architecture"
    / "data"
    / "american_architecture_places_pdf_expand.json"
)
GUIDE = ROOT / "american_architecture"

PRIMARY_URLS: dict[str, str] = {
    "gothic_revival_quito_voto_nacional": (
        "https://upload.wikimedia.org/wikipedia/commons/0/04/"
        "Basilica_del_Voto_Nacional.jpg"
    ),
    "gothic_revival_st_cecilia_nyc": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/"
        "St-cecilia-church-nyc.jpg/1280px-St-cecilia-church-nyc.jpg"
    ),
    "gothic_revival_toronto_st_james": (
        "https://www.doorsopenontario.on.ca/events/toronto/"
        "st-james-cathedral/2025-Toronto-St-James-Cathedral-1500px.jpg"
    ),
    "art_deco_americas_christ_redeemer": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/"
        "Redentor_Over_Clouds_1.jpg/1280px-Redentor_Over_Clouds_1.jpg"
    ),
    "midcentury_modern_space_needle": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/"
        "Seattle_%28WA%2C_USA%29%2C_Space_Needle_--_2022_--_1498.jpg/"
        "1280px-Seattle_%28WA%2C_USA%29%2C_Space_Needle_--_2022_--_1498.jpg"
    ),
}

ADDITIONAL_URLS: dict[str, str] = {
    "greek_revival_custom_house_nyc": (
        "https://calendar.aiany.org/wp-content/uploads/sites/3/2017/10/"
        "12-Alexander-Hamilton-U.S.-Custom-House_Cass-Gilbert-1907_"
        "David-Sundberg-Esto.jpg"
    ),
    "gothic_revival_st_patricks_montreal": (
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/"
        "0d/8d/fb/71/inside.jpg?w=1400&h=800&s=1"
    ),
    "gothic_revival_st_patricks_old_nyc": (
        "https://media.timeout.com/images/105961242/image.webp"
    ),
    "gothic_revival_cathedral_st_john": (
        "https://i.archi.ru/i/650/406956.jpg"
    ),
    "latin_colonial_baroque_quito_compania": (
        "https://upload.wikimedia.org/wikipedia/commons/6/6a/"
        "54_Iglesia_de_la_Compania_de_Jesus_%281%29.JPG"
    ),
    "midcentury_modern_saint_joseph_oratory": (
        "https://upload.wikimedia.org/wikipedia/commons/7/70/"
        "Basilica_in_St._Joseph_Oratory.jpg"
    ),
}

REMOVE_SLUGS = frozenset({"midcentury_modern_basilica_st_joseph_montreal"})

# address_ru, address_en — country-local conventions
ADDRESSES: dict[str, tuple[str, str]] = {
    "greek_revival_custom_house_nyc": (
        "Боулинг-Грин, 1, Нью-Йорк",
        "1 Bowling Green, New York",
    ),
    "gothic_revival_st_patricks_old_nyc": (
        "Малберри-стрит, 263, Нью-Йорк",
        "263 Mulberry Street, New York",
    ),
    "gothic_revival_st_cecilia_nyc": (
        "Ист-106-я улица, 125, Нью-Йорк",
        "125 East 106th Street, New York",
    ),
    "gothic_revival_cathedral_st_john": (
        "Амстердам-авеню, 1047, Нью-Йорк",
        "1047 Amsterdam Avenue, New York",
    ),
    "gothic_revival_st_patricks_montreal": (
        "бульвар Рене-Левек, 454, Монреаль",
        "454 René-Lévesque Boulevard West, Montreal",
    ),
    "midcentury_modern_saint_joseph_oratory": (
        "Куин-Мэри-роуд, 3800, Монреаль",
        "3800 Queen Mary Road, Montreal",
    ),
    "gothic_revival_toronto_st_james": (
        "Кинг-стрит Ист, 106, Торонто",
        "106 King Street East, Toronto",
    ),
    "gothic_revival_quito_voto_nacional": (
        "Венесуэла и Карчи, Кито",
        "Venezuela y Carchi, Quito",
    ),
    "latin_colonial_baroque_quito_compania": (
        "Гарсиа Морено, Кито",
        "García Moreno, Quito",
    ),
    "art_deco_americas_christ_redeemer": (
        "парк Тижука, Рио-де-Жанейро",
        "Parque Nacional da Tijuca, Rio de Janeiro",
    ),
    "midcentury_modern_space_needle": (
        "Брод-стрит, 400, Сиэтл",
        "400 Broad Street, Seattle",
    ),
}


def _set_additional(row: dict[str, Any], url: str) -> dict[str, Any]:
    slug = str(row.get("slug") or "")
    out = dict(row)
    out["additional_images"] = [{
        "image_rel_path": extra_image_rel(slug),
        "image_source_url": url,
    }]
    return out


def _patch_row(row: dict[str, Any]) -> dict[str, Any]:
    slug = str(row.get("slug") or "")
    if slug in PRIMARY_URLS:
        row = dict(row)
        row["image_source_url"] = PRIMARY_URLS[slug]
    if slug in ADDITIONAL_URLS:
        row = _set_additional(row, ADDITIONAL_URLS[slug])
    if slug in ADDRESSES:
        addr_ru, addr_en = ADDRESSES[slug]
        row = dict(row)
        row["address"] = addr_ru
        row["address_en"] = addr_en
    return row


def _download_url(url: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    ordered = _candidate_urls(url, 1280)
    ok, _err = _download_place_image(
        ordered,
        dest,
        timeout_sec=60,
        retries_429=4,
        pause_429_sec=35.0,
    )
    return bool(ok and dest.is_file())


def _download_images(
    by_slug: dict[str, dict[str, Any]],
    slugs: set[str],
) -> None:
    for slug in sorted(slugs):
        row = by_slug.get(slug)
        if not row:
            continue
        if slug in PRIMARY_URLS:
            dest = GUIDE / str(row["image_rel_path"])
            if dest.is_file():
                dest.unlink(missing_ok=True)
            ok = _download_url(PRIMARY_URLS[slug], dest)
            print("  primary {} -> {}".format(slug, "ok" if ok else "fail"))
        if slug in ADDITIONAL_URLS:
            rel = extra_image_rel(slug)
            dest = GUIDE / rel
            if slug == "midcentury_modern_saint_joseph_oratory":
                src = (
                    GUIDE
                    / "images/styles/"
                    "midcentury_modern_basilica_st_joseph_montreal.jpg"
                )
                if src.is_file():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dest)
                    print("  secondary {} -> copied".format(slug))
                    continue
            if dest.is_file():
                dest.unlink(missing_ok=True)
            ok = _download_url(ADDITIONAL_URLS[slug], dest)
            print("  secondary {} -> {}".format(slug, "ok" if ok else "fail"))


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
    expand = [
        _patch_row(r)
        for r in expand
        if str(r.get("slug") or "") not in REMOVE_SLUGS
    ]
    EXPAND.write_text(
        json.dumps(expand, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    basilica_img = (
        GUIDE / "images/styles/midcentury_modern_basilica_st_joseph_montreal.jpg"
    )
    if basilica_img.is_file():
        basilica_img.unlink(missing_ok=True)

    by_slug = {
        str(r.get("slug") or ""): r
        for r in places + expand
    }
    slugs = set(PRIMARY_URLS) | set(ADDITIONAL_URLS)
    print("Downloading images...")
    _download_images(by_slug, slugs)

    print(
        "Patched {} primary, {} secondary, removed {}".format(
            len(PRIMARY_URLS),
            len(ADDITIONAL_URLS),
            len(REMOVE_SLUGS),
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
