# -*- coding: utf-8 -*-
"""Append 10 popular UK religious-historic landmarks to English expand JSON."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

EXPAND = (
    ROOT
    / "english_architecture"
    / "data"
    / "english_architecture_places_pdf_expand.json"
)
GUIDE = ROOT / "english_architecture"

_LICENSE = "See Wikimedia Commons file page for license."
_ATTRIBUTION = "Wikimedia Commons contributors"

NEW_ROWS: list[dict[str, Any]] = [
    {
        "slug": "english_gothic_winchester_cathedral",
        "category": "english_gothic",
        "name_ru": "Винчестерский собор",
        "name_en": "Winchester Cathedral",
        "subtitle_en": "Winchester Cathedral",
        "image_rel_path": (
            "images/styles/english_gothic_winchester_cathedral.jpg"
        ),
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/6/6b/"
            "Winchester_Cathedral.jpg"
        ),
        "year_built": "1079–1532",
        "architecture_style": "Английская готика (XIII–XVI вв.)",
        "architecture_style_en": "English Gothic (13th–16th c.)",
        "address": "Катедрал-лейн, 9, Винчестер SO23 9LS",
        "address_en": "9 The Close, Winchester SO23 9LS",
        "description": (
            "Один из крупнейших готических соборов Европы; "
            "древняя базилика королей Уэссекса."
        ),
        "description_ru": (
            "Один из крупнейших готических соборов Европы; "
            "древняя базилика королей Уэссекса."
        ),
        "description_en": (
            "One of Europe's largest Gothic cathedrals; "
            "ancient church of the West Saxon kings."
        ),
    },
    {
        "slug": "english_gothic_wells_cathedral",
        "category": "english_gothic",
        "name_ru": "Собор Уэллса",
        "name_en": "Wells Cathedral",
        "subtitle_en": "Wells Cathedral",
        "image_rel_path": "images/styles/english_gothic_wells_cathedral.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/0/0f/"
            "Wells_Cathedral.jpg"
        ),
        "year_built": "XII–XIV вв.",
        "architecture_style": "Английская готика (XIII–XVI вв.)",
        "architecture_style_en": "English Gothic (13th–16th c.)",
        "address": "Катедрал-Грин, Уэлс BA5 2UE",
        "address_en": "Cathedral Green, Wells BA5 2UE",
        "description": (
            "Раннеготический собор с скульптурным фасадом "
            "и часами астрономических часов."
        ),
        "description_ru": (
            "Раннеготический собор с скульптурным фасадом "
            "и часами астрономических часов."
        ),
        "description_en": (
            "Early Gothic cathedral with sculptured west front "
            "and medieval astronomical clock."
        ),
    },
    {
        "slug": "norman_st_albans_cathedral",
        "category": "norman",
        "name_ru": "Собор Сент-Олбанса",
        "name_en": "St Albans Cathedral",
        "subtitle_en": "St Albans Cathedral",
        "image_rel_path": "images/styles/norman_st_albans_cathedral.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/3/33/"
            "St_Albans_Cathedral.jpg"
        ),
        "year_built": "XI–XIV вв.",
        "architecture_style": "Норманнская архитектура (XI–XII вв.)",
        "architecture_style_en": "Norman architecture (11th–12th c.)",
        "address": "Сампсон-эвеню, Сент-Олбанс AL1 1BY",
        "address_en": "Sumpter Yard, St Albans AL1 1BY",
        "description": (
            "Длиннейший неф средневековой Англии на месте "
            "мученичества святого Албана."
        ),
        "description_ru": (
            "Длиннейший неф средневековой Англии на месте "
            "мученичества святого Албана."
        ),
        "description_en": (
            "Longest medieval nave in England on the site "
            "of Saint Alban's martyrdom."
        ),
    },
    {
        "slug": "norman_glasgow_cathedral",
        "category": "norman",
        "name_ru": "Глазгоский собор",
        "name_en": "Glasgow Cathedral",
        "subtitle_en": "Glasgow Cathedral",
        "image_rel_path": "images/styles/norman_glasgow_cathedral.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/b/bb/"
            "Cathedral%2C_Glasgow%2C_Scotland-LCCN2001706003.jpg"
        ),
        "year_built": "XII–XIV вв.",
        "architecture_style": "Норманнская архитектура (XI–XII вв.)",
        "architecture_style_en": "Norman architecture (11th–12th c.)",
        "address": "Катедрал-сквер, Глазго G4 0UZ",
        "address_en": "Castle Street, Glasgow G4 0QZ",
        "description": (
            "Шотландская готика на могиле святого Мунго; "
            "редкий собор, переживший Реформацию."
        ),
        "description_ru": (
            "Шотландская готика на могиле святого Мунго; "
            "редкий собор, переживший Реформацию."
        ),
        "description_en": (
            "Scottish Gothic over Saint Mungo's tomb; "
            "rare cathedral that survived the Reformation."
        ),
    },
    {
        "slug": "english_gothic_st_giles_edinburgh",
        "category": "english_gothic",
        "name_ru": "Собор Святого Гиля",
        "name_en": "St Giles' Cathedral",
        "subtitle_en": "St Giles' Cathedral, Edinburgh",
        "image_rel_path": "images/styles/english_gothic_st_giles_edinburgh.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/7/7a/"
            "St_Giles_Cathedral_Edinburgh.jpg"
        ),
        "year_built": "XII–XVI вв.",
        "architecture_style": "Английская готика (XIII–XVI вв.)",
        "architecture_style_en": "English Gothic (13th–16th c.)",
        "address": "Хай-стрит, Эдинбург EH1 1RE",
        "address_en": "High Street, Edinburgh EH1 1RE",
        "description": (
            "Коронный шпиль на Роял-Майл; "
            "приходская церковь Эдинбурга."
        ),
        "description_ru": (
            "Коронный шпиль на Роял-Майл; "
            "приходская церковь Эдинбурга."
        ),
        "description_en": (
            "Crown steeple on the Royal Mile; "
            "parish church of Edinburgh."
        ),
    },
    {
        "slug": "english_gothic_tintern_abbey",
        "category": "english_gothic",
        "name_ru": "Аббатство Тинтерн",
        "name_en": "Tintern Abbey",
        "subtitle_en": "Tintern Abbey",
        "image_rel_path": "images/styles/english_gothic_tintern_abbey.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/b/b0/"
            "Tintern_Abbey_and_Courtyard.jpg"
        ),
        "year_built": "1131–1536",
        "architecture_style": "Английская готика (XIII–XVI вв.)",
        "architecture_style_en": "English Gothic (13th–16th c.)",
        "address": "Аббат-роуд, Тинтерн, Чепстоу NP16 6SE",
        "address_en": "Abbey Road, Tintern, Chepstow NP16 6SE",
        "description": (
            "Руины цистерцианского аббатства в долине Уай; "
            "романтический символ Уэльса."
        ),
        "description_ru": (
            "Руины цистерцианского аббатства в долине Уай; "
            "романтический символ Уэльса."
        ),
        "description_en": (
            "Cistercian abbey ruins in the Wye Valley; "
            "Romantic icon of Wales."
        ),
    },
    {
        "slug": "norman_fountains_abbey",
        "category": "norman",
        "name_ru": "Аббатство Фаунтинс",
        "name_en": "Fountains Abbey",
        "subtitle_en": "Fountains Abbey",
        "image_rel_path": "images/styles/norman_fountains_abbey.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/5/5b/"
            "Fountains_Abbey.jpg"
        ),
        "year_built": "1132–1539",
        "architecture_style": "Норманнская архитектура (XI–XII вв.)",
        "architecture_style_en": "Norman architecture (11th–12th c.)",
        "address": "Фаунтинс, Рипон HG4 3DY",
        "address_en": "Fountains, Ripon HG4 3DY",
        "description": (
            "Крупнейшие монастырские руины Великобритании; "
            "объект ЮНЕСКО в Йоркшире."
        ),
        "description_ru": (
            "Крупнейшие монастырские руины Великобритании; "
            "объект ЮНЕСКО в Йоркшире."
        ),
        "description_en": (
            "Largest monastic ruins in Britain; "
            "UNESCO site in Yorkshire."
        ),
    },
    {
        "slug": "english_gothic_worcester_cathedral",
        "category": "english_gothic",
        "name_ru": "Вустерский собор",
        "name_en": "Worcester Cathedral",
        "subtitle_en": "Worcester Cathedral",
        "image_rel_path": "images/styles/english_gothic_worcester_cathedral.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/f/fb/"
            "Worcester_Cathedral.jpg"
        ),
        "year_built": "1084–1504",
        "architecture_style": "Английская готика (XIII–XVI вв.)",
        "architecture_style_en": "English Gothic (13th–16th c.)",
        "address": "Колледж-ярд, 8, Вустер WR1 2LA",
        "address_en": "8 College Yard, Worcester WR1 2LA",
        "description": (
            "Место захоронения короля Иоанна; "
            "норманнский крипта и поздняя готика."
        ),
        "description_ru": (
            "Место захоронения короля Иоанна; "
            "норманнский крипта и поздняя готика."
        ),
        "description_en": (
            "Burial place of King John; "
            "Norman crypt and late Gothic choir."
        ),
    },
    {
        "slug": "victorian_brompton_oratory",
        "category": "victorian",
        "name_ru": "Оратория Бромптон",
        "name_en": "Brompton Oratory",
        "subtitle_en": "Brompton Oratory",
        "image_rel_path": "images/styles/victorian_brompton_oratory.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/1/13/"
            "Brompton_Oratory.jpg"
        ),
        "year_built": "1880–1893",
        "architecture_style": "Викторианская эпоха (1837–1901)",
        "architecture_style_en": "Victorian (1837–1901)",
        "address": "Бромптон-роуд, Лондон SW7 2RP",
        "address_en": "Brompton Road, London SW7 2RP",
        "description": (
            "Католическая базилика в итальянском барокко; "
            "второй по величине церковный купол Лондона."
        ),
        "description_ru": (
            "Католическая базилика в итальянском барокко; "
            "второй по величине церковный купол Лондона."
        ),
        "description_en": (
            "Catholic basilica in Italian Baroque style; "
            "London's second-largest church dome."
        ),
    },
    {
        "slug": "norman_temple_church_london",
        "category": "norman",
        "name_ru": "Темпл-черч",
        "name_en": "Temple Church",
        "subtitle_en": "Temple Church, London",
        "image_rel_path": "images/styles/norman_temple_church_london.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/e/e3/"
            "Temple_Church_5%2C_London%2C_UK_-_Diliff.jpg"
        ),
        "year_built": "1162–1240",
        "architecture_style": "Норманнская архитектура (XI–XII вв.)",
        "architecture_style_en": "Norman architecture (11th–12th c.)",
        "address": "Темпл, Лондон EC4Y 7BB",
        "address_en": "Temple, London EC4Y 7BB",
        "description": (
            "Круглая церковь тамплиеров в Сити; "
            "романский ротонда и готический хор."
        ),
        "description_ru": (
            "Круглая церковь тамплиеров в Сити; "
            "романский ротонда и готический хор."
        ),
        "description_en": (
            "Templars' round church in the City; "
            "Romanesque rotunda and Gothic chancel."
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
    out.setdefault("history", out.get("description", ""))
    out.setdefault("history_ru", out.get("description_ru", ""))
    out.setdefault("history_en", out.get("description_en", ""))
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
    from scripts.city_guide_jerusalem_style_images import (
        _candidate_urls,
        _download_place_image,
    )

    for row in rows:
        slug = str(row.get("slug") or "")
        url = str(row.get("image_source_url") or "").strip()
        dest = GUIDE / str(row["image_rel_path"])
        if dest.is_file():
            dest.unlink(missing_ok=True)
        ordered = _candidate_urls(url, 1280)
        ok, _err = _download_place_image(
            ordered,
            dest,
            timeout_sec=60,
            retries_429=5,
            pause_429_sec=50.0,
        )
        print("  {} -> {}".format(slug, "ok" if ok else "fail"))
        time.sleep(18.0)


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
    print("Downloading {} new images...".format(len(added)))
    _download(added)
    print("Added {} rows (total expand: {})".format(len(added), len(merged)))
    for row in added:
        print("  + {} ({})".format(row["name_en"], row["category"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
