# -*- coding: utf-8 -*-
"""Append 10 popular German/Austrian religious-historic landmarks."""

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
    / "german_architecture"
    / "data"
    / "german_architecture_places_pdf_expand.json"
)
GUIDE = ROOT / "german_architecture"

_LICENSE = "See Wikimedia Commons file page for license."
_ATTRIBUTION = "Wikimedia Commons contributors"

NEW_ROWS: list[dict[str, Any]] = [
    {
        "slug": "baroque_melk_abbey",
        "category": "baroque",
        "name_ru": "Монастырь Мельк",
        "name_en": "Melk Abbey",
        "subtitle_en": "Melk Abbey",
        "image_rel_path": "images/styles/baroque_melk_abbey.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/4/47/Melk_Abbey.jpg"
        ),
        "year_built": "1702–1736",
        "architecture_style": "Барокко (XVII–XVIII вв.)",
        "architecture_style_en": "Baroque (17th–18th c.)",
        "address": "Абт-Бертольд-Дитмайр-штрассе, 1, 3390 Мельк",
        "address_en": "Abt-Berthold-Dietmayr-Straße 1, 3390 Melk",
        "description": (
            "Бенедиктинское аббатство над Дунаем; "
            "жёлтый барочный ансамбль, объект Всемирного наследия ЮНЕСКО."
        ),
        "description_ru": (
            "Бенедиктинское аббатство над Дунаем; "
            "жёлтый барочный ансамбль, объект Всемирного наследия ЮНЕСКО."
        ),
        "description_en": (
            "Benedictine abbey above the Danube; "
            "yellow Baroque ensemble, UNESCO World Heritage Site."
        ),
    },
    {
        "slug": "baroque_salzburg_cathedral",
        "category": "baroque",
        "name_ru": "Собор Зальцбурга",
        "name_en": "Salzburg Cathedral",
        "subtitle_en": "Salzburg Cathedral",
        "image_rel_path": "images/styles/baroque_salzburg_cathedral.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/8/8c/"
            "Salzburger_Dom.jpg"
        ),
        "year_built": "1614–1628",
        "architecture_style": "Барокко (XVII–XVIII вв.)",
        "architecture_style_en": "Baroque (17th–18th c.)",
        "address": "Домплац, 1а, 5020 Зальцбург",
        "address_en": "Domplatz 1a, 5020 Salzburg",
        "description": (
            "Кафедральный собор на Домплац; "
            "место крещения Моцарта, купола и фасад итальянского барокко."
        ),
        "description_ru": (
            "Кафедральный собор на Домплац; "
            "место крещения Моцарта, купола и фасад итальянского барокко."
        ),
        "description_en": (
            "Cathedral on Domplatz; "
            "Mozart's baptism church with Italian Baroque domes."
        ),
    },
    {
        "slug": "rococo_vierzehnheiligen",
        "category": "rococo",
        "name_ru": "Вирцхенхайлиген",
        "name_en": "Basilica of the Fourteen Holy Helpers",
        "subtitle_en": "Vierzehnheiligen Basilica",
        "image_rel_path": "images/styles/rococo_vierzehnheiligen.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/8/8a/"
            "Vierzehnheiligen_Luftbild_Winter-20240120-RM-152340.jpg"
        ),
        "year_built": "1743–1772",
        "architecture_style": "Рококо (XVIII в.)",
        "architecture_style_en": "Rococo (18th c.)",
        "address": "Фирцхенхайлиген, 3, 96288 Бад-Штаффельштайн",
        "address_en": "Vierzehnheiligen 3, 96288 Bad Staffelstein",
        "description": (
            "Паломническая базилика Баухзена; "
            "овал в плане и светлый рокайль Баварии."
        ),
        "description_ru": (
            "Паломническая базилика Баухзена; "
            "овал в плане и светлый рокайль Баварии."
        ),
        "description_en": (
            "Balthasar Neumann pilgrimage basilica; "
            "oval plan and luminous Bavarian Rococo."
        ),
    },
    {
        "slug": "renaissance_wartburg",
        "category": "renaissance",
        "name_ru": "Вартбург",
        "name_en": "Wartburg Castle",
        "subtitle_en": "Wartburg Castle",
        "image_rel_path": "images/styles/renaissance_wartburg.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/4/48/"
            "Wartburg_castle.jpg"
        ),
        "year_built": "XI–XIX вв.",
        "architecture_style": "Возрождение и маньеризм (XVI в.)",
        "architecture_style_en": "Renaissance and Mannerism (16th c.)",
        "address": "Ауф-дер-Вартбург, 1, 99817 Айзенах",
        "address_en": "Auf der Wartburg 1, 99817 Eisenach",
        "description": (
            "Замок над Эйзенахом; "
            "место ссылки Лютера и объекта ЮНЕСКО."
        ),
        "description_ru": (
            "Замок над Эйзенахом; "
            "место ссылки Лютера и объекта ЮНЕСКО."
        ),
        "description_en": (
            "Hilltop castle above Eisenach; "
            "Luther's refuge and UNESCO World Heritage Site."
        ),
    },
    {
        "slug": "gothic_kaiserburg_nuremberg",
        "category": "gothic",
        "name_ru": "Кайзербург",
        "name_en": "Imperial Castle of Nuremberg",
        "subtitle_en": "Imperial Castle of Nuremberg",
        "image_rel_path": "images/styles/gothic_kaiserburg_nuremberg.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/3/3d/"
            "Kaiserburg_Nuernberg_March_2007_003.jpg"
        ),
        "year_built": "XI–XV вв.",
        "architecture_style": "Немецкая готика (XIII–XVI вв.)",
        "architecture_style_en": "German Gothic (13th–16th c.)",
        "address": "Бург, 17, 90403 Нюрнберг",
        "address_en": "Burg 17, 90403 Nuremberg",
        "description": (
            "Имперский замок на скале над Старым городом; "
            "резиденция императоров Священной Римской империи."
        ),
        "description_ru": (
            "Имперский замок на скале над Старым городом; "
            "резиденция императоров Священной Римской империи."
        ),
        "description_en": (
            "Imperial castle on the rock above the Old Town; "
            "residence of Holy Roman emperors."
        ),
    },
    {
        "slug": "historicism_hofburg_vienna",
        "category": "historicism",
        "name_ru": "Хофбург",
        "name_en": "Hofburg Vienna",
        "subtitle_en": "Hofburg Vienna",
        "image_rel_path": "images/styles/historicism_hofburg_vienna.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/7/78/"
            "Wien_-_Michaelerplatz_-_View_WSW_on_Hofburg.jpg"
        ),
        "year_built": "XIII–XX вв.",
        "architecture_style": "Историзм (XIX в.)",
        "architecture_style_en": "Historicism (19th c.)",
        "address": "Михаэлеркуппель, 1010 Вена",
        "address_en": "Michaelerkuppel, 1010 Vienna",
        "description": (
            "Имперская резиденция Габсбургов; "
            "ансамбль дворцовых дворов в центре Вены."
        ),
        "description_ru": (
            "Имперская резиденция Габсбургов; "
            "ансамбль дворцовых дворов в центре Вены."
        ),
        "description_en": (
            "Habsburg imperial residence; "
            "palace complex at the heart of Vienna."
        ),
    },
    {
        "slug": "baroque_asamkirche_munich",
        "category": "baroque",
        "name_ru": "Азамкирхе",
        "name_en": "Asamkirche",
        "subtitle_en": "Asamkirche, Munich",
        "image_rel_path": "images/styles/baroque_asamkirche_munich.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/1/12/"
            "Asamkirche_Munich.JPG"
        ),
        "year_built": "1733–1746",
        "architecture_style": "Барокко (XVII–XVIII вв.)",
        "architecture_style_en": "Baroque (17th–18th c.)",
        "address": "Зендлингер-штрассе, 32, 80331 Мюнхен",
        "address_en": "Sendlinger Straße 32, 80331 Munich",
        "description": (
            "Камерная церковь братьев Азам; "
            "позднебарочный фасад на узкой улице."
        ),
        "description_ru": (
            "Камерная церковь братьев Азам; "
            "позднебарочный фасад на узкой улице."
        ),
        "description_en": (
            "Intimate church by the Asam brothers; "
            "Late Baroque façade on a narrow lane."
        ),
    },
    {
        "slug": "baroque_charlottenburg_palace",
        "category": "baroque",
        "name_ru": "Дворец Шарлоттенбург",
        "name_en": "Charlottenburg Palace",
        "subtitle_en": "Charlottenburg Palace",
        "image_rel_path": "images/styles/baroque_charlottenburg_palace.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/5/52/"
            "Schloss_Charlottenburg_nachts_%28Zuschnitt%29.jpg"
        ),
        "year_built": "1695–1713",
        "architecture_style": "Барокко (XVII–XVIII вв.)",
        "architecture_style_en": "Baroque (17th–18th c.)",
        "address": "Шпандауер-дамм, 10–22, 14059 Берлин",
        "address_en": "Spandauer Damm 10-22, 14059 Berlin",
        "description": (
            "Главная резиденция прусских королей в Берлине; "
            "барочный дворец с куполом и садом."
        ),
        "description_ru": (
            "Главная резиденция прусских королей в Берлине; "
            "барочный дворец с куполом и садом."
        ),
        "description_en": (
            "Principal Prussian royal residence in Berlin; "
            "Baroque palace with dome and park."
        ),
    },
    {
        "slug": "baroque_mariazell_basilica",
        "category": "baroque",
        "name_ru": "Базилика Мариацель",
        "name_en": "Mariazell Basilica",
        "subtitle_en": "Mariazell Basilica",
        "image_rel_path": "images/styles/baroque_mariazell_basilica.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/d/d2/"
            "Basilika_Mariazell.jpg"
        ),
        "year_built": "1644–1683",
        "architecture_style": "Барокко (XVII–XVIII вв.)",
        "architecture_style_en": "Baroque (17th–18th c.)",
        "address": "Мариацеллер-штрассе, 43, 8630 Мариацель",
        "address_en": "Mariazeller Straße 43, 8630 Mariazell",
        "description": (
            "Главная австрийская паломническая святыня; "
            "барочная базилика в Штирии."
        ),
        "description_ru": (
            "Главная австрийская паломническая святыня; "
            "барочная базилика в Штирии."
        ),
        "description_en": (
            "Austria's principal pilgrimage shrine; "
            "Baroque basilica in Styria."
        ),
    },
    {
        "slug": "gothic_hohensalzburg",
        "category": "gothic",
        "name_ru": "Крепость Хоэнзальцбург",
        "name_en": "Hohensalzburg Fortress",
        "subtitle_en": "Hohensalzburg Fortress",
        "image_rel_path": "images/styles/gothic_hohensalzburg.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/4/4b/"
            "Festung_Hohensalzburg_von_Nordost.jpg"
        ),
        "year_built": "1077–XVI в.",
        "architecture_style": "Немецкая готика (XIII–XVI вв.)",
        "architecture_style_en": "German Gothic (13th–16th c.)",
        "address": "Мёнхсберг, 34, 5020 Зальцбург",
        "address_en": "Mönchsberg 34, 5020 Salzburg",
        "description": (
            "Средневековая крепость над Зальцбургом; "
            "одна из крупнейших сохранившихся замков Европы."
        ),
        "description_ru": (
            "Средневековая крепость над Зальцбургом; "
            "одна из крупнейших сохранившихся замков Европы."
        ),
        "description_en": (
            "Medieval fortress above Salzburg; "
            "one of Europe's largest preserved castles."
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
        time.sleep(20.0)


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
