# -*- coding: utf-8 -*-
"""Append 10 tourist / historical landmarks to American expand JSON."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

EXPAND = (
    ROOT
    / "american_architecture"
    / "data"
    / "american_architecture_places_pdf_expand.json"
)

_LICENSE = "See Wikimedia Commons file page for license."
_ATTRIBUTION = "Wikimedia Commons contributors"

NEW_ROWS: list[dict[str, Any]] = [
    {
        "slug": "art_deco_americas_golden_gate_bridge",
        "category": "art_deco_americas",
        "name_ru": "Мост Золотые Ворота",
        "name_en": "Golden Gate Bridge",
        "subtitle_en": "Golden Gate Bridge",
        "image_rel_path": (
            "images/styles/art_deco_americas_golden_gate_bridge.jpg"
        ),
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/a/ac/"
            "Golden_Gate_Bridge_Yang_Ming_Line.jpg"
        ),
        "_city_ref": "san_francisco:san_francisco_golden_gate_bridge",
        "year_built": "1933–1937",
        "architecture_style": "Ар-деко в Америке (1920–1940)",
        "architecture_style_en": "Art Deco in the Americas (1920–1940)",
        "address": "US 101, Сан-Франциско",
        "address_en": "US 101, San Francisco",
        "description": (
            "Подвесной мост через пролив Золотые Ворота; "
            "открыт в 1937 году, символ Сан-Франциско."
        ),
        "description_ru": (
            "Подвесной мост через пролив Золотые Ворота; "
            "открыт в 1937 году, символ Сан-Франциско."
        ),
        "description_en": (
            "Suspension bridge across the Golden Gate strait; "
            "opened in 1937 and an icon of San Francisco."
        ),
    },
    {
        "slug": "beaux_arts_statue_of_liberty",
        "category": "beaux_arts",
        "name_ru": "Статуя Свободы",
        "name_en": "Statue of Liberty",
        "subtitle_en": "Statue of Liberty",
        "image_rel_path": "images/styles/beaux_arts_statue_of_liberty.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/d/d3/"
            "Statue_of_Liberty%2C_NY.jpg"
        ),
        "_city_ref": "new_york:new_york_statue_of_liberty",
        "year_built": "1884–1886",
        "architecture_style": "Бо-ар (1890–1930)",
        "architecture_style_en": "Beaux-Arts (1890–1930)",
        "address": "Остров Свободы, Нью-Йорк",
        "address_en": "Liberty Island, New York",
        "description": (
            "Неоклассическая статуя в Нью-Йоркской гавани; "
            "подарок Франции, открыта в 1886 году."
        ),
        "description_ru": (
            "Неоклассическая статуя в Нью-Йоркской гавани; "
            "подарок Франции, открыта в 1886 году."
        ),
        "description_en": (
            "Neoclassical statue in New York Harbor; "
            "a gift from France, dedicated in 1886."
        ),
    },
    {
        "slug": "victorian_americas_brooklyn_bridge",
        "category": "victorian_americas",
        "name_ru": "Бруклинский мост",
        "name_en": "Brooklyn Bridge",
        "subtitle_en": "Brooklyn Bridge",
        "image_rel_path": (
            "images/styles/victorian_americas_brooklyn_bridge.jpg"
        ),
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/0/00/"
            "Brooklyn_Bridge_Manhattan.jpg"
        ),
        "_city_ref": "new_york:new_york_brooklyn_bridge",
        "year_built": "1869–1883",
        "architecture_style": "Викторианская Америка (1860–1900)",
        "architecture_style_en": "Victorian America (1860–1900)",
        "address": "Бруклинский мост, Нью-Йорк",
        "address_en": "Brooklyn Bridge, New York",
        "description": (
            "Подвесной мост через Ист-Ривер; "
            "соединяет Манхэттен и Бруклин, открыт в 1883 году."
        ),
        "description_ru": (
            "Подвесной мост через Ист-Ривер; "
            "соединяет Манхэттен и Бруклин, открыт в 1883 году."
        ),
        "description_en": (
            "Suspension bridge over the East River; "
            "links Manhattan and Brooklyn, opened in 1883."
        ),
    },
    {
        "slug": "greek_revival_lincoln_memorial",
        "category": "greek_revival",
        "name_ru": "Мемориал Линкольна",
        "name_en": "Lincoln Memorial",
        "subtitle_en": "Lincoln Memorial",
        "image_rel_path": "images/styles/greek_revival_lincoln_memorial.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/6/62/"
            "Lincoln_Memorial_east_side.JPG"
        ),
        "year_built": "1914–1922",
        "architecture_style": "Греческое возрождение (1820–1860)",
        "architecture_style_en": "Greek Revival (1820–1860)",
        "address": "Lincoln Memorial Circle NW, 2, Вашингтон",
        "address_en": "2 Lincoln Memorial Circle NW, Washington",
        "description": (
            "Греческий дорический храм на Национальной аллее; "
            "посвящён Аврааму Линкольну, открыт в 1922 году."
        ),
        "description_ru": (
            "Греческий дорический храм на Национальной аллее; "
            "посвящён Аврааму Линкольну, открыт в 1922 году."
        ),
        "description_en": (
            "Doric Greek temple on the National Mall; "
            "honours Abraham Lincoln, dedicated in 1922."
        ),
    },
    {
        "slug": "federal_white_house",
        "category": "federal",
        "name_ru": "Белый дом",
        "name_en": "White House",
        "subtitle_en": "White House",
        "image_rel_path": "images/styles/federal_white_house.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/5/59/"
            "South_facade_of_the_White_House%2C_Washington_DC.jpg"
        ),
        "year_built": "1792–1800",
        "architecture_style": "Федеральный стиль (1780–1830)",
        "architecture_style_en": "Federal style (1780–1830)",
        "address": "Пенсильвания-авеню, 1600, Вашингтон",
        "address_en": "1600 Pennsylvania Avenue NW, Washington",
        "description": (
            "Резиденция и рабочее место президента США; "
            "построен в неопалладианском стиле, заселён с 1800 года."
        ),
        "description_ru": (
            "Резиденция и рабочее место президента США; "
            "построен в неопалладианском стиле, заселён с 1800 года."
        ),
        "description_en": (
            "Residence and office of the U.S. president; "
            "built in Neoclassical style, occupied since 1800."
        ),
    },
    {
        "slug": "beaux_arts_palacio_bellas_artes",
        "category": "beaux_arts",
        "name_ru": "Дворец изящных искусств",
        "name_en": "Palacio de Bellas Artes",
        "subtitle_en": "Palacio de Bellas Artes, Mexico City",
        "image_rel_path": "images/styles/beaux_arts_palacio_bellas_artes.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/8/85/"
            "Mexico_City_Palacio_de_bellas_artes.jpg"
        ),
        "year_built": "1904–1934",
        "architecture_style": "Бо-ар (1890–1930)",
        "architecture_style_en": "Beaux-Arts (1890–1930)",
        "address": "Аvenida Juárez, Мехико",
        "address_en": "Avenida Juárez, Mexico City",
        "description": (
            "Культурный дворец в центре Мехико; "
            "мраморный фасад, купол и фрески Диего Риверы."
        ),
        "description_ru": (
            "Культурный дворец в центре Мехико; "
            "мраморный фасад, купол и фрески Диего Риверы."
        ),
        "description_en": (
            "Cultural palace in central Mexico City; "
            "marble façade, dome and murals by Diego Rivera."
        ),
    },
    {
        "slug": "art_deco_americas_christ_redeemer",
        "category": "art_deco_americas",
        "name_ru": "Христос-Искупитель",
        "name_en": "Christ the Redeemer",
        "subtitle_en": "Christ the Redeemer, Rio de Janeiro",
        "image_rel_path": "images/styles/art_deco_americas_christ_redeemer.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/4/4f/"
            "Christ_the_Redeemer_-_Cristo_Redentor.jpg"
        ),
        "year_built": "1922–1931",
        "architecture_style": "Ар-деко в Америке (1920–1940)",
        "architecture_style_en": "Art Deco in the Americas (1920–1940)",
        "address": "Пик Корковаду, Рио-де-Жанейро",
        "address_en": "Corcovado, Rio de Janeiro",
        "description": (
            "Ар-деко статуя на вершине Корковаду; "
            "высота 30 метров, открыта в 1931 году."
        ),
        "description_ru": (
            "Ар-деко статуя на вершине Корковаду; "
            "высота 30 метров, открыта в 1931 году."
        ),
        "description_en": (
            "Art Deco statue atop Corcovado mountain; "
            "30 metres tall, inaugurated in 1931."
        ),
    },
    {
        "slug": "midcentury_modern_space_needle",
        "category": "midcentury_modern",
        "name_ru": "Спейс Нидл",
        "name_en": "Space Needle",
        "subtitle_en": "Space Needle, Seattle",
        "image_rel_path": "images/styles/midcentury_modern_space_needle.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/f/fd/"
            "Seattle_from_Space_Needle_June_2018_003.jpg"
        ),
        "year_built": "1961–1962",
        "architecture_style": "Мидсенчури-модерн (1945–1970)",
        "architecture_style_en": "Mid-century Modern (1945–1970)",
        "address": "Брод-стрит, 400, Сиэтл",
        "address_en": "400 Broad Street, Seattle",
        "description": (
            "Башня-наблюдательная для Всемирной выставки 1962 года; "
            "высота 184 метра, символ Сиэтла."
        ),
        "description_ru": (
            "Башня-наблюдательная для Всемирной выставки 1962 года; "
            "высота 184 метра, символ Сиэтла."
        ),
        "description_en": (
            "Observation tower built for the 1962 World's Fair; "
            "184 metres high, a symbol of Seattle."
        ),
    },
    {
        "slug": "contemporary_americas_cn_tower",
        "category": "contemporary_americas",
        "name_ru": "Башня CN",
        "name_en": "CN Tower",
        "subtitle_en": "CN Tower, Toronto",
        "image_rel_path": "images/styles/contemporary_americas_cn_tower.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/4/43/"
            "CN_Tower%2C_Toronto%2C_Canada_%28Unsplash_DJ_kOgH5u0o%29.jpg"
        ),
        "year_built": "1973–1976",
        "architecture_style": "Современная архитектура Америк (1990-е — наст.)",
        "architecture_style_en": "Contemporary Americas (1990s–present)",
        "address": "Фронт-стрит, 301, Торонто",
        "address_en": "301 Front Street West, Toronto",
        "description": (
            "Бетонная телебашня на берегу озера Онтарио; "
            "высота 553 метра, открыта в 1976 году."
        ),
        "description_ru": (
            "Бетонная телебашня на берегу озера Онтарио; "
            "высота 553 метра, открыта в 1976 году."
        ),
        "description_en": (
            "Concrete telecommunications tower on Lake Ontario; "
            "553 metres tall, opened in 1976."
        ),
    },
    {
        "slug": "victorian_americas_chateau_frontenac",
        "category": "victorian_americas",
        "name_ru": "Шато Фронтенак",
        "name_en": "Château Frontenac",
        "subtitle_en": "Château Frontenac, Quebec City",
        "image_rel_path": (
            "images/styles/victorian_americas_chateau_frontenac.jpg"
        ),
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/b/bf/"
            "Ch%C3%A2teau_Frontenac_after_a_freezing_rain_day_in_Quebec_city.jpg"
        ),
        "year_built": "1892–1893",
        "architecture_style": "Викторианская Америка (1860–1900)",
        "architecture_style_en": "Victorian America (1860–1900)",
        "address": "Рю де Каррьер, 1, Квебек",
        "address_en": "1 Rue des Carrières, Quebec City",
        "description": (
            "Отель в стиле шато на мысе в Квебеке; "
            "доминирует над Старым городом, открыт в 1893 году."
        ),
        "description_ru": (
            "Отель в стиле шато на мысе в Квебеке; "
            "доминирует над Старым городом, открыт в 1893 году."
        ),
        "description_en": (
            "Château-style hotel on a cape in Quebec City; "
            "dominates the Old Town, opened in 1893."
        ),
    },
]


def _finalize(row: dict[str, Any]) -> dict[str, Any]:
    year = str(row.get("year_built") or "")
    city_ru = str(row.get("address") or "").split(",")[-1].strip()
    city_en = str(row.get("address_en") or "").split(",")[-1].strip()
    out = dict(row)
    out.setdefault("license_note", _LICENSE)
    out.setdefault("attribution", _ATTRIBUTION)
    out.setdefault("history", "")
    out.setdefault("history_ru", "")
    out.setdefault("history_en", "")
    out.setdefault("significance", "")
    out.setdefault("significance_ru", "")
    out.setdefault("significance_en", "")
    out["facts"] = ["Период: {}.".format(year), "Город: {}.".format(city_ru)]
    out["facts_ru"] = out["facts"]
    out["facts_en"] = [
        "Period: {}.".format(year),
        "City: {}.".format(city_en),
    ]
    return out


def _download(rows: list[dict[str, Any]]) -> None:
    from scripts.apply_worship_wave1 import _copy_city_image, _download_commons

    guide_root = ROOT / "american_architecture"
    parts_mod = __import__(
        "scripts.architecture_guide_runtime",
        fromlist=["load_parts"],
    )
    parts = parts_mod.load_parts("american_architecture")
    city_index_mod = __import__(
        "american_architecture.data.city_places_index",
        fromlist=["load_city_index"],
    )
    city_index = city_index_mod.load_city_index(ROOT)

    for row in rows:
        slug = str(row.get("slug") or "")
        dest_rel = str(row["image_rel_path"])
        dest = guide_root / dest_rel
        copied = False
        city_ref = str(row.get("_city_ref") or "").strip()
        if city_ref:
            city_row = city_index.get(city_ref)
            if city_row and _copy_city_image(
                ROOT,
                parts,
                guide_root,
                city_row,
                dest_rel,
            ):
                copied = True
                print("  {} -> copied city".format(slug))
        if not copied:
            url = str(row.get("image_source_url") or "").strip()
            if dest.is_file():
                dest.unlink(missing_ok=True)
            ok = _download_commons(
                guide_root,
                row,
                url,
                retries_429=4,
                pause_429_sec=35.0,
            )
            print("  {} -> {}".format(slug, "ok" if ok else "fail"))


def main() -> int:
    existing: list[dict[str, Any]] = json.loads(
        EXPAND.read_text(encoding="utf-8"),
    )
    seen = {str(r.get("slug") or "") for r in existing}
    added: list[dict[str, Any]] = []
    for raw in NEW_ROWS:
        slug = str(raw["slug"])
        if slug in seen:
            continue
        added.append(_finalize(raw))
    if not added:
        print("No new rows to add")
        return 0
    merged = existing + added
    EXPAND.write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    _download(added)
    print("Added {} rows (total expand: {})".format(len(added), len(merged)))
    for row in added:
        print("  + {} ({})".format(row["name_en"], row["category"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
