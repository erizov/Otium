# -*- coding: utf-8 -*-
"""Patch American guide image overrides, addresses, Casa Barragán swap."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from american_architecture.data.image_overrides import IMAGE_URL_OVERRIDES

PLACES = ROOT / "american_architecture" / "data" / "american_architecture_places.json"
EXPAND = (
    ROOT
    / "american_architecture"
    / "data"
    / "american_architecture_places_pdf_expand.json"
)
SEEDS = ROOT / "american_architecture" / "data" / "style_examples_seeds.py"
GUIDE = ROOT / "american_architecture"

IMAGE_PATCHES: dict[str, str] = {
    "art_deco_americas_chicago_temple": (
        "https://upload.wikimedia.org/wikipedia/commons/2/25/"
        "Chicago_Temple_Building4.jpg"
    ),
    "art_deco_americas_empire_state": (
        "https://www.esbnyc.com/sites/default/files/2020-01/ESB%20Day.jpg"
    ),
    "midcentury_modern_brasilia": (
        "https://wikiway.com/upload/hl-photo/1cc/5fe/"
        "sobor-presvyatoy-devy-marii_40.jpg"
    ),
    "midcentury_modern_eames_house": (
        "https://images.adsttc.com/media/images/5ee9/482a/b357/6578/"
        "8b00/003c/large_jpg/shutterstock_1095854558.jpg?1592346653"
    ),
    "postmodern_portland_building": (
        "https://avatars.mds.yandex.net/i?id="
        "f4eeb4afa982894f6516eabbb07683f8_l-5220706-images-thumbs"
        "&ref=rim&n=13&w=1080&h=991"
    ),
    "latin_colonial_baroque_ouro_preto_sao_francisco": (
        "https://bigfoto.name/uploads/posts/2022-02/"
        "1643707687_35-bigfoto-name-p-anninskoe-barokko-v-arkhitekture-83.jpg"
    ),
    "latin_modernism_rio_cathedral": (
        "https://insideinside.org/wp-content/uploads/2023/06/"
        "archdiocese-of-rio-de-1.jpg"
    ),
    "latin_modernism_torre_latinoamericana": (
        "https://upload.wikimedia.org/wikipedia/commons/c/c3/"
        "Latinoamerica_tower%2C_Mexico_City_2022_p2.jpg"
    ),
}

# address_ru, address_en
ADDRESSES: dict[str, tuple[str, str]] = {
    "art_deco_americas_chicago_temple": (
        "Уэст-Уашингтон-стрит, 77, Чикаго",
        "West Washington Street, 77, Chicago",
    ),
    "art_deco_americas_empire_state": (
        "Пятая авеню, 350, Нью-Йорк",
        "Fifth Avenue, 350, New York",
    ),
    "midcentury_modern_brasilia": (
        "Эспланада дос Министérios, Бразилиа",
        "Esplanada dos Ministérios, Brasília",
    ),
    "midcentury_modern_eames_house": (
        "Шото-Бульвар, 203, Лос-Анджелес",
        "Chautauqua Boulevard, 203, Los Angeles",
    ),
    "postmodern_portland_building": (
        "SW 5th Avenue, 1120, Портленд",
        "SW 5th Avenue, 1120, Portland",
    ),
    "latin_colonial_baroque_ouro_preto_sao_francisco": (
        "Ларгу-ди-Кoимбра, 174, Уру-Прету",
        "Largo de Coimbra, 174, Ouro Preto",
    ),
    "latin_modernism_rio_cathedral": (
        "Аvenida República do Chile, 245, Рио-де-Жанейро",
        "Av. República do Chile, 245, Rio de Janeiro",
    ),
    "latin_modernism_torre_latinoamericana": (
        "Эхе-Сентраль Ласаро Карденас, 2, Мехико",
        "Eje Central Lázaro Cárdenas, 2, Mexico City",
    ),
    "latin_modernism_planalto": (
        "Праса dos Três Poderes, Бразилиа",
        "Praça dos Três Poderes, Brasília",
    ),
    "latin_modernism_unam_central": (
        "Аvenida Universidad 3000, Мехико",
        "Av. Universidad 3000, Mexico City",
    ),
    "latin_modernism_mam": (
        "Аvenida Infante Dom Henrique, 85, Рио-де-Жанейро",
        "Av. Infante Dom Henrique, 85, Rio de Janeiro",
    ),
    "art_deco_americas_chrysler": (
        "Лексington Avenue, 405, Нью-Йорк",
        "Lexington Avenue, 405, New York",
    ),
    "art_deco_americas_rockefeller": (
        "Рокфеллер-плаза, 45, Нью-Йорк",
        "Rockefeller Plaza, 45, New York",
    ),
    "midcentury_modern_stahl_house": (
        "Woods Drive, 1636, Лос-Анджелес",
        "Woods Drive, 1636, Los Angeles",
    ),
    "midcentury_modern_salk": (
        "North Torrey Pines Road, 10010, Ла-Холья",
        "North Torrey Pines Road, 10010, La Jolla",
    ),
}

TORRE_LATINOAMERICANA: dict[str, Any] = {
    "slug": "latin_modernism_torre_latinoamericana",
    "category": "latin_modernism",
    "name_ru": "Латиноамериканская башня",
    "name_en": "Torre Latinoamericana",
    "subtitle_en": "Torre Latinoamericana",
    "image_rel_path": "images/styles/latin_modernism_torre_latinoamericana.jpg",
    "image_source_url": IMAGE_PATCHES["latin_modernism_torre_latinoamericana"],
    "license_note": "See Wikimedia Commons file page for license.",
    "attribution": "Wikimedia Commons contributors",
    "year_built": "1949–1956",
    "architecture_style": "Латиноамериканский модернизм",
    "architecture_style_en": "Latin American Modernism",
    "address": ADDRESSES["latin_modernism_torre_latinoamericana"][0],
    "address_en": ADDRESSES["latin_modernism_torre_latinoamericana"][1],
    "description": (
        "Стальной небоскрёб в центре Мехико; "
        "завершён в 1956 году, один из первых высотных домов города."
    ),
    "description_ru": (
        "Стальной небоскрёб в центре Мехико; "
        "завершён в 1956 году, один из первых высотных домов города."
    ),
    "description_en": (
        "Steel-frame tower in central Mexico City; "
        "completed in 1956 among the city's first skyscrapers."
    ),
    "history": "",
    "history_ru": "",
    "history_en": "",
    "significance": "",
    "significance_ru": "",
    "significance_en": "",
    "facts": [
        "Период: 1949–1956.",
        "Адрес: Эхе-Сентраль Ласаро Карденас, 2, Мехико.",
    ],
    "facts_ru": [
        "Период: 1949–1956.",
        "Адрес: Эхе-Сентраль Ласаро Карденас, 2, Мехико.",
    ],
    "facts_en": [
        "Period: 1949–1956.",
        "Address: Eje Central Lázaro Cárdenas, 2, Mexico City.",
    ],
}


def _patch_row(row: dict[str, Any]) -> dict[str, Any]:
    slug = str(row.get("slug") or "")
    if slug in IMAGE_PATCHES:
        row = dict(row)
        row["image_source_url"] = IMAGE_PATCHES[slug]
    if slug in ADDRESSES:
        addr_ru, addr_en = ADDRESSES[slug]
        row = dict(row)
        row["address"] = addr_ru
        row["address_en"] = addr_en
    return row


def _replace_casa_barragan(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        if str(row.get("slug") or "") == "latin_modernism_casa_barragan":
            out.append(TORRE_LATINOAMERICANA)
            continue
        out.append(row)
    return out


def _download(slugs: set[str]) -> None:
    from scripts.apply_worship_wave1 import _download_commons

    places = json.loads(PLACES.read_text(encoding="utf-8"))
    expand = json.loads(EXPAND.read_text(encoding="utf-8"))
    by_slug = {
        str(r.get("slug") or ""): r
        for r in places + expand
    }
    for slug in slugs:
        row = by_slug.get(slug)
        if not row:
            continue
        url = IMAGE_PATCHES.get(slug) or str(row.get("image_source_url") or "")
        if not url:
            continue
        dest = GUIDE / str(row["image_rel_path"])
        if dest.is_file():
            dest.unlink(missing_ok=True)
        ok = _download_commons(
            GUIDE,
            row,
            url,
            retries_429=4,
            pause_429_sec=35.0,
        )
        print("  {} -> {}".format(slug, "ok" if ok else "fail"))


def _patch_seeds() -> None:
    text = SEEDS.read_text(encoding="utf-8")
    old = (
        "        _ex('casa_barragan', 'Дом Барраганa', 'Casa Luis Barragán', "
        "year='1947–1948', city_ru='Мехико', city_en='Mexico City', "
        "history_ru='Цвет и стены Баррагана.', "
        "history_en='Barragán colour and walls.', commons_url=''),"
    )
    new = (
        "        _ex('torre_latinoamericana', 'Латиноамериканская башня', "
        "'Torre Latinoamericana', year='1949–1956', city_ru='Мехико', "
        "city_en='Mexico City', "
        "history_ru='Стальной небоскрёб в центре Мехико, завершён в 1956.', "
        "history_en='Steel-frame tower in Mexico City, completed 1956.', "
        "commons_url=''),"
    )
    if old in text:
        SEEDS.write_text(text.replace(old, new), encoding="utf-8")
        print("Updated style_examples_seeds.py")


def main() -> int:
    places: list[dict[str, Any]] = json.loads(
        PLACES.read_text(encoding="utf-8"),
    )
    places = _replace_casa_barragan([_patch_row(r) for r in places])
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

    _patch_seeds()

    old_img = GUIDE / "images/styles/latin_modernism_casa_barragan.jpg"
    if old_img.is_file():
        old_img.unlink(missing_ok=True)

    slugs = set(IMAGE_PATCHES)
    print("Downloading images...")
    _download(slugs)
    print("Patched places + expand; {} image overrides".format(len(IMAGE_PATCHES)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
