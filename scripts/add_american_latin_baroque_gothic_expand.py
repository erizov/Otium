# -*- coding: utf-8 -*-
"""Append 10 non-US Baroque / Gothic Revival rows to American expand JSON."""

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
        "slug": "latin_colonial_baroque_quito_compania",
        "category": "latin_colonial_baroque",
        "name_ru": "Церковь Компании Иисуса",
        "name_en": "Church of the Society of Jesus",
        "subtitle_en": "Church of the Society of Jesus, Quito",
        "image_rel_path": (
            "images/styles/latin_colonial_baroque_quito_compania.jpg"
        ),
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/e/e3/"
            "Iglesia_de_La_Compa%C3%B1%C3%ADa%2C_Quito%2C_Ecuador%2C_"
            "2015-07-22%2C_DD_116-118_HDR.JPG"
        ),
        "year_built": "1605–1765",
        "architecture_style": "Латиноамериканский колониальный барокко",
        "architecture_style_en": "Latin American colonial Baroque",
        "address": "Гарсиа Морено, Кито",
        "address_en": "García Moreno, Quito",
        "description": (
            "Иезуитский храм в историческом центре Кито; "
            "завершён в 1765 году, интерьер покрыт золотым листом."
        ),
        "description_ru": (
            "Иезуитский храм в историческом центре Кито; "
            "завершён в 1765 году, интерьер покрыт золотым листом."
        ),
        "description_en": (
            "Jesuit church in Quito's historic center, "
            "completed in 1765; interior covered in gold leaf."
        ),
        "history": "",
        "history_ru": "",
        "history_en": "",
    },
    {
        "slug": "latin_colonial_baroque_ouro_preto_sao_francisco",
        "category": "latin_colonial_baroque",
        "name_ru": "Церковь Святого Франциска Ассизского",
        "name_en": "Church of Saint Francis of Assisi",
        "subtitle_en": "Church of Saint Francis of Assisi, Ouro Preto",
        "image_rel_path": (
            "images/styles/"
            "latin_colonial_baroque_ouro_preto_sao_francisco.jpg"
        ),
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/e/eb/"
            "Igreja_de_S%C3%A3o_Francisco_de_Assis%2C_Ouro_Preto.jpg"
        ),
        "year_built": "1766–1810",
        "architecture_style": "Латиноамериканский колониальный барокко",
        "architecture_style_en": "Latin American colonial Baroque",
        "address": "Праса Антониу Диаш, Уру-Прету",
        "address_en": "Praça Antônio Dias, Ouro Preto",
        "description": (
            "Барочная церковь в Уру-Прету; "
            "скульптуры Алейжадинью, росписи Мануэля да Коста Аттаиде."
        ),
        "description_ru": (
            "Барочная церковь в Уру-Прету; "
            "скульптуры Алейжадинью, росписи Мануэля да Коста Аттаиде."
        ),
        "description_en": (
            "Baroque church in Ouro Preto with sculpture by "
            "Aleijadinho and paintings by Manoel da Costa Ataíde."
        ),
        "history": "",
        "history_ru": "",
        "history_en": "",
    },
    {
        "slug": "latin_colonial_baroque_oaxaca_santo_domingo",
        "category": "latin_colonial_baroque",
        "name_ru": "Храм Санто-Доминго",
        "name_en": "Church of Santo Domingo de Guzmán",
        "subtitle_en": "Church of Santo Domingo de Guzmán, Oaxaca",
        "image_rel_path": (
            "images/styles/latin_colonial_baroque_oaxaca_santo_domingo.jpg"
        ),
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/e/e4/"
            "Church_of_Santo_Domingo_Oaxaca.jpg"
        ),
        "year_built": "1572–1666",
        "architecture_style": "Латиноамериканский колониальный барокко",
        "architecture_style_en": "Latin American colonial Baroque",
        "address": "Маседонио Алькала, Оахака",
        "address_en": "Macedonio Alcalá, Oaxaca",
        "description": (
            "Доминиканский храм в Оахаке; "
            "фасад и капилла Розария — образец мексиканского барокко."
        ),
        "description_ru": (
            "Доминиканский храм в Оахаке; "
            "фасад и капилла Розария — образец мексиканского барокко."
        ),
        "description_en": (
            "Dominican church in Oaxaca; façade and Rosary Chapel "
            "are a noted example of Mexican Baroque."
        ),
        "history": "",
        "history_ru": "",
        "history_en": "",
    },
    {
        "slug": "latin_colonial_baroque_cartagena_san_pedro_claver",
        "category": "latin_colonial_baroque",
        "name_ru": "Церковь Сан-Педро Клавера",
        "name_en": "Church of San Pedro Claver",
        "subtitle_en": "Church of San Pedro Claver, Cartagena",
        "image_rel_path": (
            "images/styles/"
            "latin_colonial_baroque_cartagena_san_pedro_claver.jpg"
        ),
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/2/21/"
            "Iglesia_de_San_Pedro_Claver%2C_Cartagena_05.jpg"
        ),
        "year_built": "1580–1654",
        "architecture_style": "Латиноамериканский колониальный барокко",
        "architecture_style_en": "Latin American colonial Baroque",
        "address": "Пласа-де-Сан-Педро-Клавер, Картахена",
        "address_en": "Plaza de San Pedro Claver, Cartagena",
        "description": (
            "Иезуитский храм в Картахене, посвящённый "
            "святому Петру Клаверу; рядом его гробница."
        ),
        "description_ru": (
            "Иезуитский храм в Картахене, посвящённый "
            "святому Петру Клаверу; рядом его гробница."
        ),
        "description_en": (
            "Jesuit church in Cartagena dedicated to Saint "
            "Peter Claver; his tomb adjoins the sanctuary."
        ),
        "history": "",
        "history_ru": "",
        "history_en": "",
    },
    {
        "slug": "latin_colonial_baroque_salvador_sao_francisco",
        "category": "latin_colonial_baroque",
        "name_ru": "Церковь и конвент Сан-Франсиску",
        "name_en": "Church and Convent of Saint Francis",
        "subtitle_en": "Church and Convent of Saint Francis, Salvador",
        "image_rel_path": (
            "images/styles/latin_colonial_baroque_salvador_sao_francisco.jpg"
        ),
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/8/8c/"
            "Igreja_de_S%C3%A3o_Francisco_Salvador_2019-6875.jpg"
        ),
        "year_built": "1708–1723",
        "architecture_style": "Латиноамериканский колониальный барокко",
        "architecture_style_en": "Latin American colonial Baroque",
        "address": "Ларгу-ду-Крузейру-ди-Сан-Франсиску, Салвадор",
        "address_en": "Largo do Cruzeiro de São Francisco, Salvador",
        "description": (
            "Францисканский храм в Салвадоре; "
            "интерьер отделан позолоченной резьбой по дереву."
        ),
        "description_ru": (
            "Францисканский храм в Салвадоре; "
            "интерьер отделан позолоченной резьбой по дереву."
        ),
        "description_en": (
            "Franciscan church in Salvador; interior lined "
            "with gilded wood carving in Portuguese Baroque style."
        ),
        "history": "",
        "history_ru": "",
        "history_en": "",
    },
    {
        "slug": "gothic_revival_quito_voto_nacional",
        "category": "gothic_revival",
        "name_ru": "Базилика Голосования",
        "name_en": "Basílica del Voto Nacional",
        "subtitle_en": "Basílica del Voto Nacional, Quito",
        "image_rel_path": (
            "images/styles/gothic_revival_quito_voto_nacional.jpg"
        ),
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/4/44/"
            "Quito_as_from_panecillo_Basilica.jpg"
        ),
        "year_built": "1892–1909",
        "architecture_style": "Готическое возрождение (1830–1900)",
        "architecture_style_en": "Gothic Revival (1830–1900)",
        "address": "Карчи и Венесуэла, Кито",
        "address_en": "Carchi and Venezuela, Quito",
        "description": (
            "Неоготическая базилика в Кито; "
            "строительство начато в 1892 году, освящена в 1988 году."
        ),
        "description_ru": (
            "Неоготическая базилика в Кито; "
            "строительство начато в 1892 году, освящена в 1988 году."
        ),
        "description_en": (
            "Neo-Gothic basilica in Quito; construction "
            "began in 1892 and the church was consecrated in 1988."
        ),
        "history": "",
        "history_ru": "",
        "history_en": "",
    },
    {
        "slug": "gothic_revival_la_plata_cathedral",
        "category": "gothic_revival",
        "name_ru": "Собор Ла-Платы",
        "name_en": "Cathedral of La Plata",
        "subtitle_en": "Cathedral of La Plata",
        "image_rel_path": (
            "images/styles/gothic_revival_la_plata_cathedral.jpg"
        ),
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/d/d4/"
            "CATEDRAL_de_LA_PLATA%2C_ARGENTINA.jpg"
        ),
        "year_built": "1884–1932",
        "architecture_style": "Готическое возрождение (1830–1900)",
        "architecture_style_en": "Gothic Revival (1830–1900)",
        "address": "Калье 14 и 51, Ла-Плата",
        "address_en": "Calle 14 and 51, La Plata",
        "description": (
            "Кафедральный собор Ла-Платы в неоготическом "
            "стиле; один из крупнейших храмов Южной Америки."
        ),
        "description_ru": (
            "Кафедральный собор Ла-Платы в неоготическом "
            "стиле; один из крупнейших храмов Южной Америки."
        ),
        "description_en": (
            "Neo-Gothic cathedral of La Plata; among the "
            "largest church buildings in South America."
        ),
        "history": "",
        "history_ru": "",
        "history_en": "",
    },
    {
        "slug": "gothic_revival_cordoba_capuchinos",
        "category": "gothic_revival",
        "name_ru": "Церковь Капуцинов",
        "name_en": "Church of the Capuchins",
        "subtitle_en": "Church of the Capuchins, Córdoba",
        "image_rel_path": (
            "images/styles/gothic_revival_cordoba_capuchinos.jpg"
        ),
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/1/13/"
            "Iglesia_de_los_Capuchinos_-_C%C3%B3rdoba_%28Argentina%29.jpg"
        ),
        "year_built": "1926–1933",
        "architecture_style": "Готическое возрождение (1830–1900)",
        "architecture_style_en": "Gothic Revival (1830–1900)",
        "address": "Кордова",
        "address_en": "Córdoba",
        "description": (
            "Неоготическая церковь в Кордове; "
            "спроектирована Огюстом Босси, освящена в 1933 году."
        ),
        "description_ru": (
            "Неоготическая церковь в Кордове; "
            "спроектирована Огюстом Босси, освящена в 1933 году."
        ),
        "description_en": (
            "Neo-Gothic church in Córdoba designed by "
            "Auguste Bossi; consecrated in 1933."
        ),
        "history": "",
        "history_ru": "",
        "history_en": "",
    },
    {
        "slug": "gothic_revival_vancouver_christ_church",
        "category": "gothic_revival",
        "name_ru": "Кафедральный собор Крайст-Чёрч",
        "name_en": "Christ Church Cathedral",
        "subtitle_en": "Christ Church Cathedral, Vancouver",
        "image_rel_path": (
            "images/styles/gothic_revival_vancouver_christ_church.jpg"
        ),
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/1/12/"
            "ChristChurchCathedral_Vancouver_BC_CA_2011-05-12.JPG"
        ),
        "year_built": "1889–1894",
        "architecture_style": "Готическое возрождение (1830–1900)",
        "architecture_style_en": "Gothic Revival (1830–1900)",
        "address": "Баррард-стрит, 690, Ванкувер",
        "address_en": "Burrard Street, 690, Vancouver",
        "description": (
            "Англиканский кафедральный собор в Ванкувере; "
            "построен в 1894 году в стиле неоготики."
        ),
        "description_ru": (
            "Англиканский кафедральный собор в Ванкувере; "
            "построен в 1894 году в стиле неоготики."
        ),
        "description_en": (
            "Anglican cathedral in Vancouver; built in "
            "1894 in Gothic Revival style."
        ),
        "history": "",
        "history_ru": "",
        "history_en": "",
    },
    {
        "slug": "gothic_revival_toronto_st_james",
        "category": "gothic_revival",
        "name_ru": "Кафедральный собор Святого Иакова",
        "name_en": "Cathedral Church of St. James",
        "subtitle_en": "Cathedral Church of St. James, Toronto",
        "image_rel_path": (
            "images/styles/gothic_revival_toronto_st_james.jpg"
        ),
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/c/cc/"
            "Cathedral_Church_of_St._James%2C_Toronto%2C_Ontario%2C_"
            "2025-08-25_04.jpg"
        ),
        "year_built": "1850–1873",
        "architecture_style": "Готическое возрождение (1830–1900)",
        "architecture_style_en": "Gothic Revival (1830–1900)",
        "address": "Кинг-стрит Ист, 106, Торонто",
        "address_en": "King Street East, 106, Toronto",
        "description": (
            "Англиканский кафедральный собор Торонто; "
            "шпиль высотой 93 метра — один из старейших приходов города."
        ),
        "description_ru": (
            "Англиканский кафедральный собор Торонто; "
            "шпиль высотой 93 метра — один из старейших приходов города."
        ),
        "description_en": (
            "Anglican cathedral of Toronto; its 93-metre "
            "spire rises over one of the city's oldest parishes."
        ),
        "history": "",
        "history_ru": "",
        "history_en": "",
    },
]


def _finalize(row: dict[str, Any]) -> dict[str, Any]:
    year = str(row.get("year_built") or "")
    city_ru = str(row.get("address") or "").split(",")[-1].strip()
    city_en = str(row.get("address_en") or "").split(",")[-1].strip()
    if "," not in str(row.get("address") or ""):
        city_ru = str(row.get("address") or "")
        city_en = str(row.get("address_en") or "")
    out = dict(row)
    out.setdefault("license_note", _LICENSE)
    out.setdefault("attribution", _ATTRIBUTION)
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
    from scripts.apply_worship_wave1 import _download_commons

    guide_root = ROOT / "american_architecture"
    for row in rows:
        url = str(row.get("image_source_url") or "").strip()
        if not url:
            continue
        dest = guide_root / str(row["image_rel_path"])
        if dest.is_file() and dest.stat().st_size >= 50_000:
            continue
        _download_commons(
            guide_root,
            row,
            url,
            retries_429=4,
            pause_429_sec=35.0,
        )


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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
