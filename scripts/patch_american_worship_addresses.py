# -*- coding: utf-8 -*-
"""Patch American worship expand rows: addresses and Trinity Wall Street."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from american_architecture.data.image_overrides import IMAGE_URL_OVERRIDES

EXPAND = (
    ROOT
    / "american_architecture"
    / "data"
    / "american_architecture_places_pdf_expand.json"
)

# address_ru, address_en — country-local conventions (US/CAN EN: number first)
ADDRESSES: dict[str, tuple[str, str]] = {
    "gothic_revival_st_patrick": (
        "Пятая авеню, 625, Нью-Йорк",
        "625 Fifth Avenue, New York",
    ),
    "gothic_revival_st_patricks_old_nyc": (
        "Малберри-стрит, 263, Нью-Йорк",
        "263 Mulberry Street, New York",
    ),
    "gothic_revival_trinity_wall_street": (
        "Бродвей, 89, Нью-Йорк",
        "89 Broadway, New York",
    ),
    "victorian_americas_st_ignatius_loyola": (
        "Парк-авеню, 980, Нью-Йорк",
        "980 Park Avenue, New York",
    ),
    "gothic_revival_st_cecilia_nyc": (
        "Ист-106-я улица, 125, Нью-Йорк",
        "125 East 106th Street, New York",
    ),
    "latin_colonial_baroque_notre_dame_montreal": (
        "Нотр-Дам, 110, Монреаль",
        "110 Notre-Dame Street West, Montreal",
    ),
    "midcentury_modern_saint_joseph_oratory": (
        "Куин-Мэри-роуд, 3800, Монреаль",
        "3800 Queen Mary Road, Montreal",
    ),
    "beaux_arts_mary_queen_of_the_world": (
        "ул. де ла Катедраль, 1085, Монреаль",
        "1085 Rue de la Cathédrale, Montreal",
    ),
    "gothic_revival_st_patricks_montreal": (
        "бульвар Рене-Левек, 454, Монреаль",
        "454 René-Lévesque Boulevard West, Montreal",
    ),
    "international_style_unitarian_church_dallas": (
        "Норманди-авеню, 4015, Даллас",
        "4015 Normandy Avenue, Dallas",
    ),
    "federal_philadelphia_christ_church": (
        "Норт-Америкен-стрит, 20, Филадельфия",
        "20 North American Street, Philadelphia",
    ),
    "federal_boston_old_north": (
        "Сейлем-стрит, 193, Бостон",
        "193 Salem Street, Boston",
    ),
    "greek_revival_boston_kings_chapel": (
        "Тремонт-стрит, 58, Бостон",
        "58 Tremont Street, Boston",
    ),
    "victorian_americas_riverside_church": (
        "Риверсайд-драйв, 490, Нью-Йорк",
        "490 Riverside Drive, New York",
    ),
    "beaux_arts_brooklyn_cathedral": (
        "Флатбуш-авеню, 75, Бруклин",
        "75 Flatbush Avenue, Brooklyn",
    ),
    "midcentury_modern_los_angeles_cathedral": (
        "Гранд-авеню, 555, Лос-Анджелес",
        "555 Grand Avenue, Los Angeles",
    ),
    "gothic_revival_washington_national_cathedral": (
        "Массачусетс-авеню, 3101, Вашингтон",
        "3101 Massachusetts Avenue NW, Washington",
    ),
    "federal_philadelphia_cathedral_basilica": (
        "Логан-сквер, 18, Филадельфия",
        "18th Street and Benjamin Franklin Parkway, Philadelphia",
    ),
    "prairie_style_unity_temple": (
        "Лейк-стрит, 875, Оук-Парк",
        "875 Lake Street, Oak Park",
    ),
}

TRINITY_WALL_STREET = {
    "slug": "gothic_revival_trinity_wall_street",
    "category": "gothic_revival",
    "name_ru": "Троицкая церковь на Уолл-стрит",
    "name_en": "Trinity Church Wall Street",
    "subtitle_en": "Trinity Church Wall Street",
    "image_rel_path": "images/styles/gothic_revival_trinity_wall_street.jpg",
    "image_source_url": (
        "https://www.mbbarch.com/wp-content/uploads/2022/11/"
        "2022CP05-0162-1920x1714.gif"
    ),
    "license_note": "See source website for license.",
    "attribution": "Murphy Burnham & Buttrick Architects",
    "year_built": "1846",
    "architecture_style": "Готическое возрождение (1830–1900)",
    "architecture_style_en": "Gothic Revival (1830–1900)",
    "address": "Бродвей, 89, Нью-Йорк",
    "address_en": "89 Broadway, New York",
    "description": "Англиканская церковь на Уолл-стрит с готическим шпилем.",
    "description_ru": "Англиканская церковь на Уолл-стрит с готическим шпилем.",
    "description_en": "Anglican church on Wall Street with Gothic spire.",
    "history": "Третья постройка прихода с 1696 года.",
    "history_ru": "Третья постройка прихода с 1696 года.",
    "history_en": "Third church of the parish founded in 1696.",
    "significance": "",
    "significance_ru": "",
    "significance_en": "",
    "facts": ["Период: 1846.", "Адрес: Бродвей, 89, Нью-Йорк."],
    "facts_ru": ["Период: 1846.", "Адрес: Бродвей, 89, Нью-Йорк."],
    "facts_en": ["Period: 1846.", "Address: 89 Broadway, New York."],
}


def _apply_image_urls(row: dict) -> dict:
    slug = str(row.get("slug") or "")
    override = IMAGE_URL_OVERRIDES.get(slug)
    if override:
        row = dict(row)
        row["image_source_url"] = override[0]
    return row


def _download_overrides(rows: list[dict]) -> None:
    from scripts.apply_worship_wave1 import _download_commons

    guide_root = ROOT / "american_architecture"
    old_trinity = guide_root / "images/styles/gothic_revival_trinity_nyc.jpg"
    if old_trinity.is_file():
        old_trinity.unlink(missing_ok=True)
    for row in rows:
        slug = str(row.get("slug") or "")
        if slug not in IMAGE_URL_OVERRIDES:
            continue
        url = IMAGE_URL_OVERRIDES[slug][0]
        dest = guide_root / str(row["image_rel_path"])
        if dest.is_file():
            dest.unlink(missing_ok=True)
        _download_commons(
            guide_root,
            row,
            url,
            retries_429=3,
            pause_429_sec=30.0,
        )


def main() -> int:
    rows: list[dict] = json.loads(EXPAND.read_text(encoding="utf-8"))
    out: list[dict] = []
    for row in rows:
        slug = str(row.get("slug") or "")
        if slug == "gothic_revival_trinity_nyc":
            out.append(TRINITY_WALL_STREET)
            continue
        if slug in ADDRESSES:
            addr_ru, addr_en = ADDRESSES[slug]
            row["address"] = addr_ru
            row["address_en"] = addr_en
        out.append(_apply_image_urls(row))
    EXPAND.write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    _download_overrides(out)
    print("Patched {} expand rows".format(len(out)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
