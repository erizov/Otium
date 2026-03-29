# -*- coding: utf-8 -*-
"""
Build spb/data/spb_places_expansion_m2026.json from Commons.

Each row is either an exact file title (underscores; API may normalize spaces)
or a search query (first image hit). Run once after editing the table below.
"""

from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_OUT = _PROJECT_ROOT / "spb" / "data" / "spb_places_expansion_m2026.json"
_UA = {"User-Agent": "ExcursionGuide/1.0 (Commons search; batch expand SPB)"}

# slug, category, name_ru, subtitle_en, exact_file OR None, search_query OR None
_SPEC: tuple[tuple[str, str, str, str, str | None, str | None], ...] = (
    # buildings (20)
    (
        "mariinsky_2_theatre_building",
        "buildings",
        "Мариинский театр (новая сцена)",
        "Mariinsky II theatre",
        "Mariinsky-2 interiors 14.jpg",
        None,
    ),
    (
        "baltic_house_building",
        "buildings",
        "БДТ им. Г. А. Товстоногова (здание)",
        "Baltic House theatre",
        None,
        "Baltic House Saint Petersburg building",
    ),
    (
        "maly_drama_theatre_building",
        "buildings",
        "Малый драматический театр",
        "Maly Drama Theatre SPB",
        None,
        "Maly Drama Theatre Saint Petersburg",
    ),
    (
        "capella_spb_building",
        "buildings",
        "Придворная певческая капелла (здание)",
        "Court Chapel building",
        "0537Ca5. Санкт-Петербург. Главное здание Придворной певческой капеллы.jpg",
        None,
    ),
    (
        "mining_university_spb_main",
        "buildings",
        "Горный институт (корпус)",
        "Mining University SPB",
        "Spb Vasilievsky Island Mining College asv2019-09 img3.jpg",
        None,
    ),
    (
        "emperor_transport_university_spb",
        "buildings",
        "Императорский университет путей сообщения",
        "Emperor Alexander transport university",
        "4867. St. Petersburg State Transport University.jpg",
        None,
    ),
    (
        "house_of_scientists_spb",
        "buildings",
        "Дом учёных РАН",
        "House of Scientists SPB",
        None,
        "House of Scientists Saint Petersburg",
    ),
    (
        "tolstoy_house_spb",
        "buildings",
        "Дом Л. Н. Толстого",
        "Tolstoy House SPB",
        "Tolstoy house 1910—1912 - panoramio.jpg",
        None,
    ),
    (
        "muruzi_house_spb",
        "buildings",
        "Дом Мурузи",
        "Muruzi House",
        "Дом Мурузи-1.JPG",
        None,
    ),
    (
        "pavel_suzor_apartment_building",
        "buildings",
        "Доходный дом П. И. Сузора",
        "Pavel Suzor building",
        "354. St. Petersburg. Nevsky Prospect, 54.jpg",
        None,
    ),
    (
        "dom_knigi_nevsky",
        "buildings",
        "Дом книги (Невский проспект)",
        "Dom Knigi bookstore",
        "Dom Knigi StPetersburg.JPG",
        None,
    ),
    (
        "passage_department_store_spb",
        "buildings",
        "Торговый дом «Пассаж»",
        "Passage department store",
        "Spb 06-2012 Inside the Passage.jpg",
        None,
    ),
    (
        "eliseevsky_shop_facade_spb",
        "buildings",
        "Елисеевский магазин (фасад)",
        "Eliseevsky shop facade",
        "Saint Petersburg.- Eliseevsky shop (en2018) (3).jpg",
        None,
    ),
    (
        "philharmonia_building_nevsky30",
        "buildings",
        "Здание филармонии (Невский, 30)",
        "Philharmonia building",
        "Newskij 30 fasad.jpg",
        None,
    ),
    (
        "polytechnic_university_main_spb",
        "buildings",
        "Политехнический университет (главный корпус)",
        "SPbPU main building",
        None,
        "Polytechnic University Saint Petersburg main building",
    ),
    (
        "herzen_university_main_spb",
        "buildings",
        "РГПУ им. А. И. Герцена",
        "Herzen University main",
        None,
        "Herzen University Saint Petersburg building",
    ),
    (
        "itmo_kronverksky_building",
        "buildings",
        "Университет ИТМО (корпус)",
        "ITMO University building",
        "SPbSU ITMO.jpg",
        None,
    ),
    (
        "smolny_institute_wing_spb",
        "buildings",
        "Смольный институт",
        "Smolny institute",
        "RUS-2016-SPB-Smolny Institute 02.jpg",
        None,
    ),
    (
        "kitayskaya_birzha_spb",
        "buildings",
        "Здание бывшей биржи (ракурс)",
        "Old Stock Exchange alternate view",
        "Old Saint Petersburg Stock Exchange-2025-09-msu---2578.jpg",
        None,
    ),
    (
        "trezzini_building_spb",
        "buildings",
        "Здание Канцелярии проектов (Трезини)",
        "Trezzini office building",
        None,
        "Twelve Collegia building Saint Petersburg",
    ),
    # sculptures (20)
    (
        "chizhik_pyzhik_monument",
        "sculptures",
        "Памятник Чижику-Пыжику",
        "Chizhik Pyzhik",
        "Chizhik-Pyzhik memorial.jpg",
        None,
    ),
    (
        "monument_athena_petrovsky_gate",
        "sculptures",
        "Скульптура Афины (Петровские ворота)",
        "Athena Polias Petrovsky Gate",
        "Petrovsky gate Athena Polias in Saint Petersburg.jpg",
        None,
    ),
    (
        "monument_griboedov_spb",
        "sculptures",
        "Памятник А. С. Грибоедову",
        "Griboyedov monument",
        None,
        "Griboyedov monument Saint Petersburg",
    ),
    (
        "monument_lermontov_spb",
        "sculptures",
        "Памятник М. Ю. Лермонтову",
        "Lermontov monument SPB",
        None,
        "Lermontov monument Saint Petersburg",
    ),
    (
        "monument_nekrasov_spb",
        "sculptures",
        "Памятник Н. А. Некрасову",
        "Nekrasov monument SPB",
        None,
        "Nekrasov monument Saint Petersburg",
    ),
    (
        "monument_saltykov_shchedrin_spb",
        "sculptures",
        "Памятник М. Е. Салтыкову-Щедрину",
        "Saltykov-Shchedrin monument",
        None,
        "Saltykov-Shchedrin monument Saint Petersburg",
    ),
    (
        "monument_nikitin_spb",
        "sculptures",
        "Памятник И. С. Никитину",
        "Nikitin monument SPB",
        None,
        "Nikitin monument Saint Petersburg",
    ),
    (
        "monument_radishchev_spb",
        "sculptures",
        "Памятник А. Н. Радищеву",
        "Radishchev monument",
        None,
        "Radishchev monument Saint Petersburg",
    ),
    (
        "monument_belinsky_spb",
        "sculptures",
        "Памятник В. Г. Белинскому",
        "Belinsky monument",
        None,
        "Belinsky monument Saint Petersburg",
    ),
    (
        "monument_dobrolyubov_spb",
        "sculptures",
        "Памятник Н. А. Добролюбову",
        "Dobrolyubov monument",
        None,
        "Dobrolyubov monument Saint Petersburg",
    ),
    (
        "monument_herzen_spb",
        "sculptures",
        "Памятник А. И. Герцену",
        "Herzen monument",
        None,
        "Herzen monument Saint Petersburg",
    ),
    (
        "monument_pushkin_pushkinskaya_street",
        "sculptures",
        "Памятник А. С. Пушкину (Пушкинская улица)",
        "Pushkin monument Pushkinskaya street",
        "Памятник Пушкину А.С. на Пушкинской улице.jpg",
        None,
    ),
    (
        "monument_gorky_spb",
        "sculptures",
        "Памятник А. М. Горькому",
        "Gorky monument SPB",
        None,
        "Gorky monument Saint Petersburg",
    ),
    (
        "monument_mayakovsky_spb",
        "sculptures",
        "Памятник В. В. Маяковскому",
        "Mayakovsky monument",
        None,
        "Mayakovsky monument Saint Petersburg",
    ),
    (
        "monument_blockade_leningrad_spb",
        "sculptures",
        "Монумент героическим защитникам Ленинграда",
        "Siege of Leningrad monument",
        None,
        "Monument to Heroic Defenders of Leningrad",
    ),
    (
        "monument_suvorov_trinity_bridge",
        "sculptures",
        "Памятник А. В. Суворову (у Троицкого моста)",
        "Suvorov monument near Trinity Bridge",
        "Памятник Суворову возле Троицкого моста.jpg",
        None,
    ),
    (
        "bronze_horseman_wide_spb",
        "sculptures",
        "Медный всадник (ракурс)",
        "Bronze Horseman view",
        None,
        "Bronze Horseman Saint Petersburg",
    ),
    (
        "bank_bridge_griffins_spb",
        "sculptures",
        "Грифоны Банковского моста",
        "Bank Bridge griffins",
        None,
        "Bank Bridge griffins Saint Petersburg",
    ),
    (
        "anichkov_bridge_horses_spb",
        "sculptures",
        "Кони Аничкова моста",
        "Anichkov Bridge horses",
        None,
        "Anichkov Bridge horse Saint Petersburg",
    ),
    (
        "rostral_column_detail_spb",
        "sculptures",
        "Ростральная колонна (деталь)",
        "Rostral column detail",
        None,
        "Rostral column Saint Petersburg",
    ),
    # metro (10)
    (
        "ozerki_metro_station",
        "metro_stations",
        "Станция метро «Озерки»",
        "Ozerki metro",
        "Metro_SPB_Line2_Ozerki.jpg",
        None,
    ),
    (
        "udelnaya_metro_station",
        "metro_stations",
        "Станция метро «Удельная»",
        "Udelnaya metro",
        "Metro_SPB_Line2_Udelnaya_Main.jpg",
        None,
    ),
    (
        "pionerskaya_metro_station",
        "metro_stations",
        "Станция метро «Пионерская»",
        "Pionerskaya metro",
        "Metro_SPB_Line2_Pionerskaya.jpg",
        None,
    ),
    (
        "bukharestskaya_metro_station",
        "metro_stations",
        "Станция метро «Бухарестская»",
        "Bukharestskaya metro",
        "Metro_SPB_Line5_Bukharestskaya.jpg",
        None,
    ),
    (
        "volkovskaya_metro_station",
        "metro_stations",
        "Станция метро «Волковская»",
        "Volkovskaya metro",
        "Metro_SPB_Line5_Volkovskaya.jpg",
        None,
    ),
    (
        "elektrosila_metro_station",
        "metro_stations",
        "Станция метро «Электросила»",
        "Elektrosila metro",
        "Metro_SPB_Line2_Elektrosila.jpg",
        None,
    ),
    (
        "park_pobedy_metro_station_spb",
        "metro_stations",
        "Станция метро «Парк Победы»",
        "Park Pobedy metro",
        "Metro_SPB_Line2_Park_Pobedy.jpg",
        None,
    ),
    (
        "moskovskaya_metro_station_spb",
        "metro_stations",
        "Станция метро «Московская»",
        "Moskovskaya metro",
        "Metro_SPB_Line2_Moskovskaya.jpg",
        None,
    ),
    (
        "zvezdnaya_metro_station_spb",
        "metro_stations",
        "Станция метро «Звёздная»",
        "Zvezdnaya metro",
        "Metro_SPB_Line2_Zvezdnaya.jpg",
        None,
    ),
    (
        "novocherkasskaya_metro_station",
        "metro_stations",
        "Станция метро «Новочеркасская»",
        "Novocherkasskaya metro",
        "Metro_SPB_Line4_Novocherkasskaya.jpg",
        None,
    ),
    # monasteries (3)
    (
        "sergieva_primorskaya_pustyn",
        "monasteries",
        "Свято-Троицкая Сергиева Приморская пустынь",
        "Sergieva Primorskaya Pustyn",
        "Troice-Sergieva pustyn 2.JPG",
        None,
    ),
    (
        "kazanskaya_bogoroditsky_monastery_spb",
        "monasteries",
        "Казанский монастырь",
        "Kazan Monastery SPB",
        None,
        "Kazan monastery Saint Petersburg",
    ),
    (
        "ioannpredtechensky_monastery_spb",
        "monasteries",
        "Подворье Леушинского монастыря (Иоанно-Богословская церковь)",
        "Leushinsky metochion St John church",
        "254. Некрасова ул. 31. Иоанно-Богословская церковь. Подворье Леушинского монастыря.JPG",
        None,
    ),
    # churches (20)
    (
        "sampsonievsky_cathedral",
        "places_of_worship",
        "Сампсониевский собор",
        "Sampsonievsky Cathedral",
        "SPB Sampsonievsky Cathedral.jpg",
        None,
    ),
    (
        "vladimirskaya_church_lit",
        "places_of_worship",
        "Собор Владимирской иконы Божией Матери",
        "Vladimirskaya Church",
        None,
        "Vladimirskaya Church Saint Petersburg",
    ),
    (
        "st_nicholas_morskoy_sobor_spb",
        "places_of_worship",
        "Николо-Морской собор",
        "St Nicholas Maritime Cathedral",
        "Nikolsky Cathedral SPB 1.jpg",
        None,
    ),
    (
        "andreevsky_cathedral_spb",
        "places_of_worship",
        "Андреевский собор",
        "Saint Andrew Cathedral SPB",
        None,
        "Saint Andrew's Cathedral Saint Petersburg",
    ),
    (
        "svyato_troitsky_izmailovsky",
        "places_of_worship",
        "Троицкий собор Измайловского полка",
        "Trinity Izmailovsky cathedral",
        None,
        "Trinity cathedral Izmailovsky regiment Saint Petersburg",
    ),
    (
        "blagoveshchenskaya_church_spb",
        "places_of_worship",
        "Благовещенская церковь",
        "Annunciation church SPB",
        None,
        "Blagoveshchenskaya church Saint Petersburg",
    ),
    (
        "bulgarian_church_spb",
        "places_of_worship",
        "Церковь святых Кирилла и Мефодия",
        "SS. Cyril and Methodius church",
        "St. Petersburg. Belfry and the Gateway Church of of Cyril and Methodius. Ligovsky Prospect,128-a..JPG",
        None,
    ),
    (
        "lutheran_church_saint_katarina",
        "places_of_worship",
        "Лютеранская церковь святой Екатерины",
        "St Katarina Lutheran",
        None,
        "St Katarina church Saint Petersburg",
    ),
    (
        "finnish_lutheran_church_spb",
        "places_of_worship",
        "Финская лютеранская церковь",
        "Finnish church SPB",
        None,
        "Finnish church Saint Petersburg",
    ),
    (
        "st_mary_lutheran_spb",
        "places_of_worship",
        "Церковь святой Марии",
        "St Mary Lutheran SPB",
        None,
        "St Mary's church Saint Petersburg Lutheran",
    ),
    (
        "church_savior_on_waters_spb",
        "places_of_worship",
        "Храм Спаса-на-Водах",
        "Saviour on Waters",
        None,
        "Church of the Saviour on Waters Saint Petersburg",
    ),
    (
        "church_st_catherine_kadetskaya",
        "places_of_worship",
        "Церковь св. Екатерины",
        "St Catherine church SPB",
        None,
        "St Catherine church Saint Petersburg",
    ),
    (
        "kronstadt_naval_cathedral_exterior",
        "places_of_worship",
        "Морской Никольский собор (Кронштадт)",
        "Kronstadt Naval Cathedral",
        "Kronstadt Naval Cathedral.jpg",
        None,
    ),
    (
        "church_resurrection_smolenskoe",
        "places_of_worship",
        "Воскресенский Новодевичий монастырь (собор)",
        "Voskresensky Novodevichy cathedral",
        None,
        "Voskresensky Novodevichy monastery cathedral",
    ),
    (
        "church_transfiguration_lit",
        "places_of_worship",
        "Церковь Спаса Преображения",
        "Transfiguration church SPB",
        None,
        "Church of Transfiguration Saint Petersburg",
    ),
    (
        "church_st_tatiana_spb",
        "places_of_worship",
        "Церковь святой Татианы",
        "St Tatiana church",
        None,
        "St Tatiana church Saint Petersburg",
    ),
    (
        "chapel_st_xenia_spb",
        "places_of_worship",
        "Часовня святой Ксении",
        "St Xenia chapel",
        None,
        "St Xenia chapel Saint Petersburg",
    ),
    (
        "church_st_elizabeth_spb",
        "places_of_worship",
        "Церковь святой Елизаветы",
        "St Elizabeth church",
        None,
        "St Elizabeth church Saint Petersburg",
    ),
    (
        "lavra_trinity_cathedral_interior",
        "places_of_worship",
        "Свято-Троицкий собор Александро-Невской лавры",
        "Holy Trinity Lavra cathedral",
        None,
        "Holy Trinity Cathedral Alexander Nevsky Lavra",
    ),
    (
        "feodorovsky_cathedral_spb",
        "places_of_worship",
        "Феодоровский собор",
        "Feodorovsky Cathedral",
        None,
        "Feodorovsky Cathedral Saint Petersburg",
    ),
)


def _existing_slugs() -> set[str]:
    slugs: set[str] = set()
    data_dir = _PROJECT_ROOT / "spb" / "data"
    for name in ("spb_places.json", "spb_places_more.json"):
        path = data_dir / name
        if path.is_file():
            for row in json.loads(path.read_text(encoding="utf-8")):
                s = row.get("slug")
                if s:
                    slugs.add(s)
    return slugs


def _image_url_for_title(fname: str) -> str | None:
    params = {
        "action": "query",
        "titles": "File:" + fname,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json",
    }
    q = urllib.parse.urlencode(params)
    req = urllib.request.Request(
        "https://commons.wikimedia.org/w/api.php?" + q,
        headers=_UA,
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.load(resp)
    except (urllib.error.URLError, OSError):
        return None
    for page in data.get("query", {}).get("pages", {}).values():
        if "missing" in page:
            return None
        ii = page.get("imageinfo") or []
        if not ii:
            return None
        return ii[0].get("url")
    return None


def _search_first_image_url(query: str) -> tuple[str | None, str | None]:
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srnamespace": "6",
        "format": "json",
        "srlimit": "8",
    }
    q = urllib.parse.urlencode(params)
    req = urllib.request.Request(
        "https://commons.wikimedia.org/w/api.php?" + q,
        headers=_UA,
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.load(resp)
    except (urllib.error.URLError, OSError):
        return None, None
    titles = [
        item["title"]
        for item in data.get("query", {}).get("search", [])
    ]
    for title in titles:
        if not title.startswith("File:"):
            continue
        low = title.lower()
        if low.endswith(".pdf") or low.endswith(".djvu"):
            continue
        fname = title[5:]
        url = _image_url_for_title(fname)
        if url:
            return url, fname
        time.sleep(0.15)
    return None, None


def _folder_for_category(cat: str) -> str:
    return {
        "buildings": "buildings",
        "sculptures": "sculptures",
        "metro_stations": "metro_stations",
        "monasteries": "monasteries",
        "places_of_worship": "places_of_worship",
    }[cat]


def main() -> int:
    existing = _existing_slugs()
    places: list[dict[str, Any]] = []
    errors: list[str] = []

    for slug, cat, name_ru, subtitle_en, exact, search in _SPEC:
        if slug in existing:
            errors.append("skip duplicate slug: {}".format(slug))
            continue
        url: str | None = None
        src_fname: str | None = None
        if exact:
            url = _image_url_for_title(exact)
            src_fname = exact
            time.sleep(0.2)
        if not url and search:
            url, src_fname = _search_first_image_url(search)
            time.sleep(0.35)
        if not url or not src_fname:
            errors.append("FAIL {} / {}".format(slug, exact or search))
            continue
        low = src_fname.lower()
        ext = ".jpg"
        if low.endswith(".png"):
            ext = ".png"
        elif low.endswith(".jpeg"):
            ext = ".jpeg"
        rel = "images/{}/{}{}".format(_folder_for_category(cat), slug, ext)
        places.append(
            {
                "slug": slug,
                "category": cat,
                "name_ru": name_ru,
                "subtitle_en": subtitle_en,
                "image_source_url": url,
                "image_rel_path": rel,
                "license_note": "See Wikimedia Commons file page for license.",
                "attribution": "Wikimedia Commons contributors",
            }
        )

    for line in errors:
        print(line, file=sys.stderr)

    if len(places) != len(_SPEC):
        print(
            "Expected {} rows, got {} (see errors).".format(
                len(_SPEC), len(places),
            ),
            file=sys.stderr,
        )
        return 1

    _OUT.parent.mkdir(parents=True, exist_ok=True)
    _OUT.write_text(
        json.dumps(places, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("Wrote {} -> {}".format(len(places), _OUT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
