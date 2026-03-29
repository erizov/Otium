# -*- coding: utf-8 -*-
"""Генерация spb_places_more.json через поиск на Commons (одноразово / по запросу)."""

from __future__ import annotations

import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_PLACES_MAIN = _PROJECT_ROOT / "spb" / "data" / "spb_places.json"
_OUT = _PROJECT_ROOT / "spb" / "data" / "spb_places_more.json"
_MIN_BYTES = 2500
_DELAY = 0.35
_USER_AGENT = (
    "ExcursionGuide-PlacesMore/1.0 (Commons API; local SPB guide expansion)"
)

# (slug, category, name_ru, subtitle_en, commons_search_query)
_CANDIDATES: tuple[tuple[str, str, str, str, str], ...] = (
    ("alexander_nevsky_bridge", "bridges", "Мост Александра Невского",
     "Alexander Nevsky Bridge", "Alexander Nevsky Bridge Saint Petersburg"),
    ("liteyny_prospekt_metro", "metro_stations",
     "Станция метро «Лиговский проспект»", "Ligovsky Prospekt metro",
     "Ligovsky Prospekt metro station Saint Petersburg"),
    ("dostoevsky_metro", "metro_stations", "Станция метро «Достоевская»",
     "Dostoevskaya metro", "Dostoevskaya Saint Petersburg metro"),
    ("sportivnaya_metro", "metro_stations", "Станция метро «Спортивная»",
     "Sportivnaya metro Saint Petersburg", "Sportivnaya metro SPB"),
    ("petrogradskaya_metro", "metro_stations", "Станция метро «Петроградская»",
     "Petrogradskaya metro", "Petrogradskaya metro station"),
    ("gorkovskaya_metro", "metro_stations", "Станция метро «Горьковская»",
     "Gorkovskaya metro", "Gorkovskaya metro Saint Petersburg"),
    ("vasileostrovskaya_metro", "metro_stations",
     "Станция метро «Василеостровская»", "Vasileostrovskaya metro",
     "Vasileostrovskaya metro station"),
    ("primorskaya_metro", "metro_stations", "Станция метро «Приморская»",
     "Primorskaya metro", "Primorskaya metro Saint Petersburg"),
    ("obvodny_kanal_metro", "metro_stations",
     "Станция метро «Обводный канал»", "Obvodny Kanal metro",
     "Obvodny Kanal metro station"),
    ("frunzenskaya_metro", "metro_stations", "Станция метро «Фрунзенская»",
     "Frunzenskaya metro SPB", "Frunzenskaya metro Saint Petersburg"),
    ("pushkinskaya_metro", "metro_stations", "Станция метро «Пушкинская»",
     "Pushkinskaya metro SPB", "Pushkinskaya metro Saint Petersburg"),
    ("teatralnaya_metro", "metro_stations", "Станция метро «Театральная»",
     "Teatralnaya metro SPB", "Teatralnaya Ploshchad metro"),
    ("spasskaya_metro", "metro_stations", "Станция метро «Спасская»",
     "Spasskaya metro", "Spasskaya metro Saint Petersburg"),
    ("nevsky_prospekt_metro", "metro_stations",
     "Станция метро «Невский проспект»", "Nevsky Prospekt metro",
     "Nevsky Prospekt metro station"),
    ("gostiny_dvor_metro", "metro_stations",
     "Станция метро «Гостиный двор»", "Gostiny Dvor metro",
     "Gostiny Dvor metro station"),
    ("mayakovskaya_metro", "metro_stations", "Станция метро «Маяковская»",
     "Mayakovskaya metro SPB", "Mayakovskaya metro Saint Petersburg"),
    ("alexander_nevsky_metro", "metro_stations",
     "Станция метро «Площадь Александра Невского»",
     "Ploshchad Alexandra Nevskogo metro",
     "Ploshchad Alexandra Nevskogo metro station"),
    ("elizarovskaya_metro", "metro_stations", "Станция метро «Елизаровская»",
     "Elizarovskaya metro", "Elizarovskaya metro station"),
    ("ulitsa_dybenko_metro", "metro_stations",
     "Станция метро «Улица Дыбенко»", "Ulitsa Dybenko metro",
     "Ulitsa Dybenko metro station"),
    ("prospekt_bolshevikov_metro", "metro_stations",
     "Станция метро «Проспект Большевиков»",
     "Prospekt Bolshevikov metro", "Prospekt Bolshevikov metro"),
    ("parnas_metro", "metro_stations", "Станция метро «Парнас»",
     "Parnas metro", "Parnas metro Saint Petersburg"),
    ("begovaya_metro", "metro_stations", "Станция метро «Беговая»",
     "Begovaya metro", "Begovaya metro Saint Petersburg"),
    ("zenit_metro", "metro_stations", "Станция метро «Зенит»",
     "Zenit metro", "Zenit metro station Saint Petersburg"),
    ("staraya_derevnya_metro", "metro_stations",
     "Станция метро «Старая деревня»", "Staraya Derevnya metro",
     "Staraya Derevnya metro"),
    ("chkalovskaya_metro", "metro_stations", "Станция метро «Чкаловская»",
     "Chkalovskaya metro SPB", "Chkalovskaya metro Saint Petersburg"),
    ("krestovsky_ostrov_metro", "metro_stations",
     "Станция метро «Крестовский остров»", "Krestovsky Ostrov metro",
     "Krestovsky Ostrov metro"),
    ("admiralteyskaya_metro", "metro_stations",
     "Станция метро «Адмиралтейская»", "Admiralteyskaya metro",
     "Admiralteyskaya metro station"),
    ("sennaya_metro", "metro_stations", "Станция метро «Сенная площадь»",
     "Sennaya Ploshchad metro", "Sennaya Ploshchad metro station"),
    ("technolog_institut_metro", "metro_stations",
     "Станция метро «Технологический институт»",
     "Tekhnologichesky Institut metro",
     "Tekhnologichesky Institut metro Saint Petersburg"),
    ("vosstaniya_metro", "metro_stations",
     "Станция метро «Площадь Восстания»", "Ploshchad Vosstaniya metro",
     "Ploshchad Vosstaniya metro interior"),
    ("ladoga_metro", "metro_stations", "Станция метро «Ладожская»",
     "Ladozhskaya metro", "Ladozhskaya metro station"),
    ("proletarskaya_metro", "metro_stations", "Станция метро «Пролетарская»",
     "Proletarskaya metro SPB", "Proletarskaya metro Saint Petersburg"),
    ("rybatskoye_metro", "metro_stations", "Станция метро «Рыбацкое»",
     "Rybatskoye metro", "Rybatskoye metro station"),
    ("kupchino_metro", "metro_stations", "Станция метро «Купчино»",
     "Kupchino metro", "Kupchino metro station"),
    ("mezhdunarodnaya_metro", "metro_stations",
     "Станция метро «Международная»", "Mezhdunarodnaya metro SPB",
     "Mezhdunarodnaya metro Saint Petersburg"),
    ("prospekt_slavy_metro", "metro_stations",
     "Станция метро «Проспект Славы»", "Prospekt Slavy metro",
     "Prospekt Slavy metro station"),
    ("dunaiskaya_metro", "metro_stations", "Станция метро «Дунайская»",
     "Dunaiskaya metro", "Dunaiskaya metro Saint Petersburg"),
    ("shushary_metro", "metro_stations", "Станция метро «Шушары»",
     "Shushary metro", "Shushary metro station"),
    ("blagoveshchensky_bridge_detail", "bridges", "Благовещенский мост",
     "Blagoveshchensky Bridge", "Blagoveshchensky Bridge Saint Petersburg"),
    ("tuchkov_bridge", "bridges", "Тучков мост", "Tuchkov Bridge",
     "Tuchkov bridge Saint Petersburg"),
    ("lomonosov_bridge", "bridges", "Ломоносовский мост",
     "Lomonosov Bridge", "Lomonosov Bridge Saint Petersburg"),
    ("egyptian_bridge_spb", "bridges", "Египетский мост",
     "Egyptian Bridge", "Egyptian Bridge Saint Petersburg"),
    ("blue_bridge_spb", "bridges", "Синий мост", "Blue Bridge Saint Petersburg",
     "Blue Bridge Saint Isaac Square"),
    ("italian_bridge", "bridges", "Итальянский мост", "Italian Bridge SPB",
     "Italian Bridge Saint Petersburg"),
    ("first_ingenieur_bridge", "bridges", "Первый Инженерный мост",
     "First Engineer Bridge", "First Engineer Bridge Saint Petersburg"),
    ("kokushkin_bridge", "bridges", "Кокушкин мост", "Kokushkin bridge",
     "Kokushkin bridge Saint Petersburg"),
    ("red_bridge_spb", "bridges", "Красный мост", "Red Bridge SPB",
     "Red Bridge Saint Petersburg Moika"),
    ("pikalov_bridge", "bridges", "Пикалов мост", "Pikalov bridge",
     "Pikalov bridge Saint Petersburg"),
    ("kazan_cathedral_view_square", "squares", "Казанская площадь",
     "Kazanskaya Square", "Kazanskaya Ploshchad Saint Petersburg"),
    ("ostrovsky_square", "squares", "Площадь Островского",
     "Ostrovsky Square", "Ostrovsky Square Saint Petersburg"),
    ("mikhailovsky_square", "squares", "Михайловская площадь",
     "Mikhailovskaya Square", "Mikhailovskaya Square Saint Petersburg"),
    ("art_square_spb", "squares", "Площадь Искусств", "Arts Square",
     "Arts Square Saint Petersburg"),
    ("lenin_razliv_museum", "museums", "Музей-дача Ленина в Разливе",
     "Lenin Razliv museum", "Razliv Lenin museum"),
    ("central_museum_railway_spb", "museums",
     "Музей железных дорог России", "Russian Railways museum SPB",
     "Railway museum Saint Petersburg"),
    ("microminiatures_museum", "museums", "Музей микроминиатюр «Русский левша»",
     "Russian Lefty museum", "Russian Lefty museum Saint Petersburg"),
    ("zoological_garden_spb", "museums", "Зоологический сад (старый)",
     "Old zoo SPB", "Saint Petersburg zoo entrance"),
    ("museum_anna_akhmatova", "museums", "Музей Анны Ахматовой",
     "Anna Akhmatova museum", "Anna Akhmatova museum Fountain House"),
    ("museum_blockade_spb", "museums", "Музей обороны и блокады Ленинграда",
     "State Memorial Museum of Defence and Siege",
     "Siege of Leningrad museum"),
    ("cabinet_of_curiosities_spb", "museums", "Кунсткамера (фасад)",
     "Kunstkamera facade", "Kunstkamera Saint Petersburg facade"),
    ("mikhailovsky_palace_facade", "museums", "Русский музей, Михайловский дворец",
     "Russian Museum Mikhailovsky Palace", "Mikhailovsky Palace facade"),
    ("marble_palace_russian_museum", "museums", "Мраморный дворец (Русский музей)",
     "Marble Palace Russian Museum", "Marble Palace Saint Petersburg"),
    ("stieglitz_museum", "museums", "Музей прикладного искусства Штиглица",
     "Stieglitz museum", "Stieglitz museum Saint Petersburg"),
    ("museum_political_history", "museums",
     "Музей политической истории России", "Museum of Political History",
     "Museum of Political History Saint Petersburg"),
    ("museum_sound_spb", "museums", "Музей звуки", "Museum of Sound SPB",
     "Sound museum Saint Petersburg"),
    ("vodka_museum_spb", "museums", "Музей водки", "Vodka Museum SPB",
     "Vodka museum Saint Petersburg"),
    ("bread_museum_spb", "museums", "Музей хлеба", "Bread museum SPB",
     "Museum of bread Saint Petersburg"),
    ("museum_urban_sculpture", "museums", "Музей городской скульптуры",
     "Museum of Urban Sculpture", "Museum urban sculpture Saint Petersburg"),
    ("yusupov_garden", "parks", "Сад дворца Юсуповых", "Yusupov Garden",
     "Yusupov garden Moika"),
    ("apollon_garden", "parks", "Сад Аполлона", "Apollo Garden Peterhof",
     "Apollo garden Peterhof"),
    ("alexandria_park_peterhof", "parks", "Парк Александрия (Петергоф)",
     "Alexandria Park Peterhof", "Alexandria park Peterhof"),
    ("english_park_gatchina", "parks", "Английский парк (Гатчина)",
     "English park Gatchina", "English garden Gatchina Palace"),
    ("sylvia_park_gatchina", "parks", "Парк Сильвия (Гатчина)",
     "Sylvia Park Gatchina", "Sylvia Gatchina park"),
    ("prioratsky_palace_gatchina", "palaces", "Приоратский дворец",
     "Prioratsky Palace", "Prioratsky Palace Gatchina"),
    ("bathroom_cottage_gatchina", "palaces", "Банный домик (Гатчина)",
     "Bathhouse Gatchina", "Bathhouse Gatchina palace"),
    ("vladimir_palace", "palaces", "Владимирский дворец",
     "Vladimir Palace", "Vladimir Palace Saint Petersburg"),
    ("mariinsky_palace_spb", "palaces", "Мариинский дворец",
     "Mariinsky Palace", "Mariinsky Palace Saint Petersburg"),
    ("beloselsky_belozersky_palace", "palaces", "Дворец Белосельских-Белозерских",
     "Beloselsky-Belozersky Palace", "Beloselsky-Belozersky Palace"),
    ("stroganov_palace_facade", "palaces", "Дворец Строгановых (фасад)",
     "Stroganov Palace facade", "Stroganov Palace Nevsky"),
    ("new_mikhailovsky_palace", "palaces", "Новый Михайловский дворец",
     "New Mikhailovsky Palace", "New Mikhailovsky Palace Russian Museum"),
    ("cottage_palace_peterhof", "palaces", "Дворец-коттедж (Петергоф)",
     "Cottage Palace Peterhof", "Cottage palace Peterhof"),
    ("farm_palace_peterhof", "palaces", "Фермерский дворец (Петергоф)",
     "Farm Palace Peterhof", "Farm palace Peterhof Alexandria"),
    ("hermitage_theatre_building", "theaters", "Эрмитажный театр",
     "Hermitage Theatre", "Hermitage Theatre building"),
    ("maly_drama_theatre", "theaters", "МДТ Европейский", "MDT theatre SPB",
     "Maly Drama Theatre Saint Petersburg"),
    ("bolshoy_drama_theatre", "theaters", "БДТ им. Товстоногова",
     "Tovstonogov Bolshoi Drama", "Tovstonogov theatre Saint Petersburg"),
    ("comedy_theatre_spb", "theaters", "Театр Комедии", "Comedy Theatre SPB",
     "Comedy Theatre Saint Petersburg"),
    ("music_hall_spb", "theaters", "Санкт-Петербургский музыкально-драматический "
     "театр «Музыкальный зал»", "Music Hall Theatre", "Music Hall SPB theatre"),
    ("youth_theatre_on_fontanka", "theaters", "Молодёжный театр на Фонтанке",
     "Youth Theatre Fontanka", "Youth Theatre Fontanka"),
    ("church_saint_catherine_spb", "places_of_worship",
     "Евангелическо-лютеранская церковь Святой Екатерины",
     "St Catherine Lutheran", "Saint Catherine Lutheran church Saint Petersburg"),
    ("reformed_church_spb", "places_of_worship",
     "Церковь Святого Петра (реформатская)", "Reformed Church SPB",
     "Reformed church Saint Petersburg"),
    ("armenian_church_spb", "places_of_worship", "Армянская церковь",
     "Armenian church SPB", "Armenian church Saint Petersburg"),
    ("catholic_church_spb", "places_of_worship",
     "Костёл Святой Екатерины", "Catholic church Saint Catherine SPB",
     "Catholic church Nevsky Saint Petersburg"),
    ("church_resurrection_smolnogo", "places_of_worship",
     "Воскресенский Смольный собор", "Smolny Resurrection Cathedral",
     "Smolny Cathedral interior"),
    ("prince_vladimir_cathedral", "places_of_worship",
     "Собор князя Владимира", "Prince Vladimir Cathedral",
     "Prince Vladimir cathedral Saint Petersburg"),
    ("john_rylsky_church", "places_of_worship",
     "Церковь Иоанна Рыльского", "Saint John of Rila church SPB",
     "John of Rila church Saint Petersburg"),
    ("annunciation_church_vasilievsky", "places_of_worship",
     "Благовещенская церковь (Васильевский остров)",
     "Annunciation Church Vasilyevsky", "Annunciation church Vasilyevsky Island"),
    ("smolny_institute_building", "landmarks", "Смольный институт",
     "Smolny Institute", "Smolny institute building"),
    ("temple_friendship_spb", "places_of_worship",
     "Храм дружбы народов", "Friendship of Peoples temple",
     "Temple friendship peoples Saint Petersburg"),
    ("monument_catherine_ii", "sculptures", "Памятник Екатерине II",
     "Monument to Catherine II", "Monument Catherine II Ostrovsky Square"),
    ("monument_glinka", "sculptures", "Памятник Глинке", "Glinka monument SPB",
     "Glinka monument Saint Petersburg"),
    ("monument_lomonosov", "sculptures", "Памятник Ломоносову",
     "Lomonosov monument", "Lomonosov monument Saint Petersburg"),
    ("monument_pushkin_arts_square", "sculptures", "Памятник Пушкину (пл. Искусств)",
     "Pushkin monument Arts Square", "Pushkin Arts Square monument"),
    ("monument_krylov", "sculptures", "Памятник Крылову", "Krylov monument",
     "Ivan Krylov monument Summer Garden"),
    ("monument_charles_twelve", "sculptures", "Памятник Карлу XII",
     "Monument to Charles XII", "Charles XII monument Saint Petersburg"),
    ("sphinx_quay", "sculptures", "Квартал со сфинксами", "Quay with Sphinxes",
     "Sphinxes University embankment"),
    ("lion_bridge_sculpture", "sculptures", "Львиный мостик", "Bridge of Four Lions",
     "Bridge of Four Lions Saint Petersburg"),
    ("newa_gate", "landmarks", "Невские ворота Кронштадта", "Neva Gate Kronstadt",
     "Neva gate Kronstadt"),
    ("kronstadt_yacht_club", "landmarks", "Яхт-клуб Кронштадта",
     "Kronstadt yacht club", "Kronstadt yacht club"),
    ("fort_emperor_paul_kronstadt", "landmarks", "Форт Император Павел I",
     "Fort Emperor Paul", "Fort Paul Kronstadt"),
    ("lighthouse_tolbukhin", "landmarks", "Маяк Толбухин", "Tolbukhin lighthouse",
     "Tolbukhin lighthouse Kotlin"),
    ("petrovsky_stadium_exterior", "landmarks", "Стадион «Петровский»",
     "Petrovsky Stadium", "Petrovsky Stadium Saint Petersburg"),
    ("saint_isaac_square_view", "viewpoints", "Исаакиевская площадь (вид)",
     "St Isaac's Square view", "Saint Isaac's Square panorama"),
    ("rooftop_view_spb_generic", "viewpoints", "Панорама центра СПб",
     "Central SPB panorama", "Saint Petersburg skyline aerial"),
    ("english_embankment_view", "viewpoints", "Английская набережная",
     "English Embankment", "English embankment Saint Petersburg"),
    ("kutuzov_embankment", "landmarks", "Набережная Кутузова",
     "Kutuzov embankment", "Kutuzov embankment Saint Petersburg"),
    ("grenadersky_bridge", "bridges", "Гренадерский мост",
     "Grenadersky Bridge", "Grenadersky bridge Saint Petersburg"),
    ("staro_kalinkin_bridge", "bridges", "Старо-Калинкин мост",
     "Staro-Kalinkin Bridge", "Staro-Kalinkin bridge"),
    ("teatralny_bridge", "bridges", "Театральный мост", "Teatralny bridge",
     "Teatralny bridge Saint Petersburg"),
    ("alexander_park_tsarskoye", "parks", "Александровский парк (Царское Село)",
     "Alexander Park Tsarskoye Selo", "Alexander Park Tsarskoye Selo"),
    ("free_cruiser_museum", "museums", "Музей ледокола «Красин»",
     "Icebreaker Krasin museum", "Icebreaker Krasin museum"),
    ("cruiser_avrora_museum", "museums", "Крейсер «Аврора»", "Cruiser Aurora",
     "Aurora cruiser museum Saint Petersburg"),
    ("museum_cosmonautics_spb", "museums", "Музей космонавтики",
     "Cosmonautics museum SPB", "Museum cosmonautics Saint Petersburg"),
    ("central_park_culture_rest", "parks", "ЦПКиО им. Кирова",
     "Central Park Kirov", "Central park culture Saint Petersburg"),
    ("piskaryovskoye_cemetery", "cemeteries", "Пискарёвское мемориальное кладбище",
     "Piskaryovskoye Memorial Cemetery", "Piskaryovskoye cemetery"),
    ("bogoslovskoe_cemetery", "cemeteries", "Богословское кладбище",
     "Bogoslovskoe cemetery", "Bogoslovskoe cemetery Saint Petersburg"),
    ("volkovskoye_cemetery", "cemeteries", "Волковское лютеранское кладбище",
     "Volkovo Lutheran cemetery", "Volkovo cemetery Saint Petersburg"),
    ("literatorskie_mostki", "cemeteries", "Литераторские мостки",
     "Literatorskie Mostki", "Literatorskie bridge Volkovo"),
    ("national_pushkin_library", "libraries",
     "Российская национальная библиотека", "National Library reading room",
     "National Library of Russia reading room"),
    ("library_russian_academy", "libraries", "Библиотека РАН",
     "Library Russian Academy", "Library Russian Academy Sciences SPB"),
    ("synod_library", "libraries", "Синодальная библиотека",
     "Synodal library", "Synodal library Saint Petersburg"),
    ("apteka_pudova_building", "buildings", "Дом Пудова (аптека)",
     "Pudov pharmacy building", "Pudov pharmacy Nevsky"),
    ("wawelberg_building", "buildings", "Дом Вавельберга", "Wawelberg House",
     "Wawelberg house Nevsky"),
    ("zinger_passage_interior", "markets", "Дом Зингера (пассаж)",
     "Singer House passage", "Singer House Saint Petersburg interior"),
    ("eliseevsky_merchants_yard", "markets", "Елисеевский магазин (интерьер)",
     "Eliseevsky shop interior", "Eliseevsky shop Saint Petersburg"),
    ("gostiny_dvor_facade", "markets", "Гостиный двор (фасад)",
     "Gostiny Dvor facade", "Gostiny Dvor Saint Petersburg facade"),
    ("kuznechny_market", "markets", "Кузнечный рынок", "Kuznechny market",
     "Kuznechny market Saint Petersburg"),
    ("sennoy_market", "markets", "Сенной рынок", "Sennoy market",
     "Sennoy market Saint Petersburg"),
    ("andreevsky_market", "markets", "Андреевский рынок", "Andreevsky market",
     "Andreevsky market Saint Petersburg"),
    ("literary_cafe_spb", "cafes", "Литературное кафе", "Literary cafe SPB",
     "Literary cafe Saint Petersburg"),
    ("coffee_museum_spb", "cafes", "Музей кофе", "Coffee museum SPB",
     "Coffee museum Saint Petersburg"),
    ("alexander_nevsky_lavra_gate", "monasteries", "Лавра Александра Невского",
     "Alexander Nevsky Lavra gate", "Alexander Nevsky Lavra gate"),
    ("ioannovsky_monastery", "monasteries", "Иоанновский монастырь",
     "Ioannovsky Monastery", "Ioannovsky monastery Saint Petersburg"),
    ("novodevichy_convent_spb", "monasteries", "Воскресенский Новодевичий монастырь",
     "Voskresensky Novodevichy", "Novodevichy monastery Saint Petersburg"),
    ("vyborg_side_churches_view", "landmarks", "Выборгская сторона (панорама)",
     "Vyborg side panorama", "Vyborg side Saint Petersburg panorama"),
    ("repin_institute_building", "buildings", "Институт имени Репина",
     "Repin institute", "Repin institute building Saint Petersburg"),
    ("conservatory_building_spb", "buildings", "Консерватория им. Римского-Корсакова",
     "Conservatory building", "Rimsky-Korsakov conservatory building"),
    ("stock_exchange_spit", "landmarks", "Стрелка Васильевского острова",
     "Spit of Vasilievsky Island", "Spit Vasilievsky Island stock exchange"),
    ("menshikov_palace_oranienbaum", "palaces", "Дворец Меншикова (Ораниенбаум)",
     "Menshikov Palace Oranienbaum", "Menshikov palace Lomonosov"),
    ("kikin_palace", "palaces", "Кикины палаты", "Kikin Hall",
     "Kikin chambers Saint Petersburg"),
    ("house_ball_museum", "museums", "Дом Бенуа", "Benois House museum",
     "Benois family museum Saint Petersburg"),
    ("museum_anthropology_ethnography", "museums", "Кунсткамера (зал)",
     "Museum of Anthropology hall", "Museum Anthropology Ethnography Kunstkamera"),
)


def _search_titles(query: str) -> list[str]:
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srnamespace": 6,
            "srlimit": "10",
            "format": "json",
        },
    )
    req = urllib.request.Request(
        "https://commons.wikimedia.org/w/api.php?" + params,
        headers={"User-Agent": _USER_AGENT},
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.load(resp)
    return [x["title"] for x in data["query"]["search"]]


def _image_url_and_size(title: str) -> tuple[str | None, int]:
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "titles": title,
            "prop": "imageinfo",
            "iiprop": "url|size",
            "format": "json",
        },
    )
    req = urllib.request.Request(
        "https://commons.wikimedia.org/w/api.php?" + params,
        headers={"User-Agent": _USER_AGENT},
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.load(resp)
    for page in data["query"]["pages"].values():
        if "missing" in page:
            return None, 0
        ii = (page.get("imageinfo") or [{}])[0]
        return ii.get("url"), int(ii.get("size") or 0)
    return None, 0


def _pick_url(query: str) -> tuple[str | None, str | None]:
    for title in _search_titles(query):
        low = title.lower()
        if any(x in low for x in (".pdf", ".djvu", "djvu")):
            continue
        url, size = _image_url_and_size(title)
        if url and size >= _MIN_BYTES:
            return url, title
    return None, None


def _suffix_from_url(url: str) -> str:
    path = url.split("?", 1)[0].lower()
    if path.endswith(".svg"):
        return ".svg"
    if path.endswith(".png"):
        return ".png"
    if path.endswith(".webp"):
        return ".webp"
    return ".jpg"


def main() -> int:
    existing = json.loads(_PLACES_MAIN.read_text(encoding="utf-8"))
    have = {row["slug"] for row in existing}
    out: list[dict] = []
    skipped_dup = 0
    failed = 0
    for slug, cat, name_ru, subtitle_en, query in _CANDIDATES:
        if slug in have:
            skipped_dup += 1
            continue
        url, picked = _pick_url(query)
        time.sleep(_DELAY)
        if not url:
            print("no image:", slug, query[:60], file=sys.stderr)
            failed += 1
            continue
        suf = _suffix_from_url(url)
        rel = "images/{}/{}{}".format(cat, slug, suf)
        out.append(
            {
                "slug": slug,
                "category": cat,
                "name_ru": name_ru,
                "subtitle_en": subtitle_en,
                "image_source_url": url,
                "image_rel_path": rel,
                "license_note": "See Wikimedia Commons file page for license.",
                "attribution": "Wikimedia Commons contributors",
            },
        )
        print("ok", slug, picked[:50] if picked else "")
    _OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        "Wrote {} rows to {} (skipped dup {}, failed {})".format(
            len(out),
            _OUT,
            skipped_dup,
            failed,
        ),
    )
    if len(existing) + len(out) < 200:
        print(
            "WARNING: total places {} + {} < 200; add more candidates.".format(
                len(existing),
                len(out),
            ),
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
