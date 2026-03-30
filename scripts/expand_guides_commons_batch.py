# -*- coding: utf-8 -*-
"""One-off helper: append new places using Commons search (JPEG only).

Loads each city's *_places.json, adds up to ``target_add`` entries from
``candidates`` when a JPG image is found. Skips slugs already present or
when search returns no suitable file.

Run from repo root::

    python scripts/expand_guides_commons_batch.py

Requires network; sleeps between Commons API calls.
"""

from __future__ import annotations

import json
import random
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_COMMONS_API = (
    "https://commons.wikimedia.org/w/api.php"
    "?action=query&format=json&generator=search&gsrnamespace=6"
    "&prop=imageinfo&iiprop=url"
)
_USER_AGENT = (
    "ExcursionGuide-Expand/1.0 (educational city guides; "
    "local batch; Python urllib)"
)
_SEARCH_SLEEP_SEC = 1.35
_SAVE_SLEEP_SEC = 0.35


def _search_first_jpeg_url(query: str) -> tuple[str | None, str | None]:
    url = _COMMONS_API + "&" + urllib.parse.urlencode(
        {"gsrsearch": query, "gsrlimit": 12},
    )
    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    with urllib.request.urlopen(req, timeout=90) as resp:
        blob = json.loads(resp.read().decode("utf-8"))
    pages = blob.get("query", {}).get("pages") or {}
    best: tuple[int, str, str] | None = None
    for page in pages.values():
        title = page.get("title") or ""
        lt = title.lower()
        if not (lt.endswith(".jpg") or lt.endswith(".jpeg")):
            continue
        info = (page.get("imageinfo") or [{}])[0]
        u = info.get("url")
        if not u:
            continue
        if "upload.wikimedia.org" not in u.lower():
            continue
        # Prefer titles that look like photos (shorter queries match poorly).
        score = len(title)
        if best is None or score < best[0]:
            best = (score, u, title)
    if not best:
        return None, None
    return best[1], best[2]


def _place_record(
    slug: str,
    category: str,
    name_en: str,
    subtitle_key: str,
    subtitle_val: str,
    image_url: str,
) -> dict[str, Any]:
    return {
        "slug": slug,
        "category": category,
        "name_en": name_en,
        subtitle_key: subtitle_val,
        "image_source_url": image_url,
        "image_rel_path": "images/{}.jpg".format(slug),
        "license_note": "See Wikimedia Commons file page for license.",
        "attribution": "Wikimedia Commons contributors",
    }


def _load_cfg() -> dict[str, Any]:
    # target_add in 5..20 inclusive (deterministic but varied per city).
    bases = {
        "barcelona": 8,
        "berlin": 14,
        "boston": 7,
        "budapest": 9,
        "florence": 12,
        "madrid": 10,
        "new_york": 13,
        "philadelphia": 6,
        "prague": 11,
        "rome": 14,
        "venice": 11,
        "vienna": 9,
        "montreal": 17,
        "paris": 10,
    }
    rng = random.Random(202603301)
    target = {
        k: min(20, max(5, v + rng.randint(-1, 2)))
        for k, v in bases.items()
    }
    return {
        "barcelona": {
            "subtitle_key": "subtitle_ca",
            "rel_json": "barcelona/data/barcelona_places.json",
            "target_add": target["barcelona"],
            "candidates": [
                (
                    "mnac_palau_nacional",
                    "museums",
                    "Museu Nacional d'Art de Catalunya (MNAC)",
                    "Palau Nacional",
                    "Palau Nacional Barcelona MNAC",
                ),
                (
                    "monastery_pedralbes",
                    "places_of_worship",
                    "Monastery of Pedralbes",
                    "Monestir de Pedralbes",
                    "Monastery of Pedralbes Barcelona",
                ),
                (
                    "casa_amatller_barcelona",
                    "landmarks",
                    "Casa Amatller",
                    "Casa Amatller",
                    "Casa Amatller Barcelona Passeig de Gràcia",
                ),
                (
                    "santa_maria_del_pi",
                    "places_of_worship",
                    "Basilica of Santa Maria del Pi",
                    "Santa Maria del Pi",
                    "Santa Maria del Pi Barcelona facade",
                ),
                (
                    "basilica_de_la_merce",
                    "places_of_worship",
                    "Basilica of La Mercè",
                    "Basílica de la Mercè",
                    "Basilica La Mercè Barcelona exterior",
                ),
                (
                    "cosmo_caixa_barcelona",
                    "museums",
                    "CosmoCaixa Barcelona",
                    "CosmoCaixa",
                    "CosmoCaixa Barcelona museum building",
                ),
                (
                    "hotel_w_barcelona",
                    "landmarks",
                    "Hotel W Barcelona",
                    "Hotel Vela",
                    "Hotel W Barcelona sail building beach",
                ),
                (
                    "llotja_de_la_mar_barcelona",
                    "landmarks",
                    "Llotja de la Mar",
                    "Llotja de la Mar",
                    "Llotja de la Mar Barcelona Gothic",
                ),
                (
                    "bunkers_carmel_barcelona",
                    "viewpoints",
                    "Bunkers del Carmel",
                    "Turó de la Rovira",
                    "Bunkers del Carmel Barcelona view",
                ),
                (
                    "parc_del_laberint",
                    "parks",
                    "Parc del Laberint d'Horta",
                    "Parc del Laberint",
                    "Parc del Laberint Horta Barcelona",
                ),
                (
                    "poble_espanyol",
                    "misc",
                    "Poble Espanyol",
                    "Poble Espanyol",
                    "Poble Espanyol Barcelona Montjuic",
                ),
                (
                    "palau_reial_pedralbes",
                    "palaces",
                    "Royal Palace of Pedralbes",
                    "Palau Reial de Pedralbes",
                    "Palau Reial Pedralbes Barcelona",
                ),
            ],
        },
        "berlin": {
            "subtitle_key": "subtitle_de",
            "rel_json": "berlin/data/berlin_places.json",
            "target_add": target["berlin"],
            "candidates": [
                (
                    "humboldt_forum_berlin",
                    "museums",
                    "Humboldt Forum",
                    "Berliner Schloss",
                    "Humboldt Forum Berlin facade",
                ),
                (
                    "traenenpalast_berlin",
                    "museums",
                    "Tränenpalast (Palace of Tears)",
                    "Tränenpalast",
                    "Tränenpalast Berlin Friedrichstraße",
                ),
                (
                    "deutsches_historisches_museum",
                    "museums",
                    "Deutsches Historisches Museum",
                    "DHM",
                    "Deutsches Historisches Museum Berlin Zeughaus",
                ),
                (
                    "berlin_zoo_entrance",
                    "misc",
                    "Berlin Zoological Garden",
                    "Zoologischer Garten",
                    "Berlin Zoo entrance elephants gate",
                ),
                (
                    "neue_wache_berlin",
                    "landmarks",
                    "Neue Wache",
                    "Neue Wache",
                    "Neue Wache Berlin Unter den Linden",
                ),
                (
                    "teufelsberg_berlin",
                    "viewpoints",
                    "Teufelsberg listening station",
                    "Teufelsberg",
                    "Teufelsberg Berlin radar dome",
                ),
                (
                    "mauerpark_berlin",
                    "parks",
                    "Mauerpark",
                    "Mauerpark",
                    "Mauerpark Berlin amphitheatre",
                ),
                (
                    "soviet_memorial_treptow",
                    "landmarks",
                    "Soviet War Memorial (Treptower Park)",
                    "Treptower Park",
                    "Soviet War Memorial Treptower Park Berlin",
                ),
                (
                    "berlinische_galerie",
                    "museums",
                    "Berlinische Galerie",
                    "Berlinische Galerie",
                    "Berlinische Galerie Berlin building",
                ),
                (
                    "museum_fuer_naturkunde_berlin",
                    "museums",
                    "Museum für Naturkunde",
                    "Naturkundemuseum",
                    "Museum für Naturkunde Berlin dinosaur hall",
                ),
                (
                    "berlin_aquarium",
                    "museums",
                    "Berlin Aquarium",
                    "Aquarium Berlin",
                    "Aquarium Berlin building",
                ),
                (
                    "futurium_berlin",
                    "museums",
                    "Futurium",
                    "Futurium",
                    "Futurium Berlin building",
                ),
                (
                    "little_big_city_berlin",
                    "museums",
                    "Little Big City Berlin",
                    "Little Big City",
                    "Little Big City Berlin miniature",
                ),
                (
                    "lustgarten_museumsinsel",
                    "parks",
                    "Lustgarten (Museum Island)",
                    "Lustgarten",
                    "Lustgarten Berlin Museumsinsel Altes Museum",
                ),
                (
                    "tempelhofer_feld",
                    "parks",
                    "Tempelhofer Feld",
                    "Tempelhofer Feld",
                    "Tempelhofer Feld Berlin former airport",
                ),
            ],
        },
        "boston": {
            "subtitle_key": "subtitle_en",
            "rel_json": "boston/data/boston_places.json",
            "target_add": target["boston"],
            "candidates": [
                (
                    "prudential_center_boston",
                    "landmarks",
                    "Prudential Tower",
                    "Back Bay",
                    "Prudential Tower Boston sky view",
                ),
                (
                    "christian_science_plaza",
                    "places_of_worship",
                    "The First Church of Christ, Scientist",
                    "Christian Science Plaza",
                    "Christian Science Plaza Boston reflecting pool",
                ),
                (
                    "castle_island_boston",
                    "landmarks",
                    "Fort Independence (Castle Island)",
                    "South Boston",
                    "Castle Island Boston Fort Independence",
                ),
                (
                    "mit_stata_center",
                    "buildings",
                    "MIT Stata Center",
                    "Cambridge",
                    "MIT Stata Center Cambridge Massachusetts",
                ),
                (
                    "longfellow_bridge",
                    "bridges",
                    "Longfellow Bridge",
                    "Charles River",
                    "Longfellow Bridge Boston night",
                ),
                (
                    "harvard_yard_gate",
                    "landmarks",
                    "Harvard Yard",
                    "Cambridge",
                    "Harvard Yard Cambridge Massachusetts gate",
                ),
                (
                    "harvard_art_museums",
                    "museums",
                    "Harvard Art Museums",
                    "Cambridge",
                    "Harvard Art Museums Renzo Piano glass roof",
                ),
                (
                    "mapparium_boston",
                    "museums",
                    "Mapparium (Mary Baker Eddy Library)",
                    "Christian Science Center",
                    "Mapparium globe room Boston",
                ),
                (
                    "revere_beach",
                    "misc",
                    "Revere Beach",
                    "Revere",
                    "Revere Beach Massachusetts pavilion",
                ),
            ],
        },
        "budapest": {
            "subtitle_key": "subtitle_hu",
            "rel_json": "budapest/data/budapest_places.json",
            "target_add": target["budapest"],
            "candidates": [
                (
                    "hungarian_national_museum",
                    "museums",
                    "Hungarian National Museum",
                    "Magyar Nemzeti Múzeum",
                    "Hungarian National Museum Budapest facade",
                ),
                (
                    "museum_of_applied_arts_budapest",
                    "museums",
                    "Museum of Applied Arts",
                    "Iparművészeti Múzeum",
                    "Museum of Applied Arts Budapest building",
                ),
                (
                    "palace_of_arts_budapest",
                    "theaters",
                    "Müpa Budapest (Palace of Arts)",
                    "Müpa",
                    "Palace of Arts Budapest Müpa exterior",
                ),
                (
                    "szimpla_kert",
                    "misc",
                    "Szimpla Kert",
                    "Kazinczy utca",
                    "Szimpla Kert ruin bar Budapest",
                ),
                (
                    "gellert_hotel_budapest",
                    "landmarks",
                    "Hotel Gellért",
                    "Szent Gellért tér",
                    "Hotel Gellért Budapest facade thermal",
                ),
                (
                    "szent_istvan_park",
                    "parks",
                    "Szent István Park",
                    "Újpest",
                    "Szent István Park Budapest",
                ),
                (
                    "kopaszi_gat",
                    "parks",
                    "Kopaszi-gát",
                    "Kopaszi-gát",
                    "Kopaszi gát Budapest Danube",
                ),
                (
                    "buda_hill_funicular",
                    "misc",
                    "Buda Castle Funicular",
                    "Sikló",
                    "Budapest Castle Hill funicular",
                ),
                (
                    "gresham_palace_budapest",
                    "palaces",
                    "Four Seasons Gresham Palace",
                    "Gresham-palota",
                    "Gresham Palace Budapest Danube",
                ),
                (
                    "aquincum_museum",
                    "museums",
                    "Aquincum Museum",
                    "Aquincum Múzeum",
                    "Aquincum Museum Budapest Roman ruins",
                ),
                (
                    "budapest_history_museum",
                    "museums",
                    "Budapest History Museum",
                    "Budapesti Történeti Múzeum",
                    "Budapest History Museum Buda Castle",
                ),
            ],
        },
        "florence": {
            "subtitle_key": "subtitle_it",
            "rel_json": "florence/data/florence_places.json",
            "target_add": target["florence"],
            "candidates": [
                (
                    "bargello_museum",
                    "museums",
                    "Museo Nazionale del Bargello",
                    "Bargello",
                    "Bargello museum Florence courtyard",
                ),
                (
                    "casa_buonarroti",
                    "museums",
                    "Casa Buonarroti",
                    "Casa Buonarroti",
                    "Casa Buonarroti Florence facade",
                ),
                (
                    "rose_garden_florence",
                    "parks",
                    "Giardino delle Rose",
                    "Giardino delle Rose",
                    "Rose Garden Florence Michelangelo hill",
                ),
                (
                    "san_marco_museum_florence",
                    "museums",
                    "San Marco Museum",
                    "Museo di San Marco",
                    "San Marco museum Florence cloister",
                ),
                (
                    "santa_maria_del_carmine",
                    "places_of_worship",
                    "Basilica of Santa Maria del Carmine",
                    "Cappella Brancacci",
                    "Santa Maria del Carmine Florence facade",
                ),
                (
                    "ognissanti_florence",
                    "places_of_worship",
                    "Ognissanti",
                    "Ognissanti",
                    "Ognissanti church Florence facade",
                ),
                (
                    "basilica_annunziata",
                    "places_of_worship",
                    "Basilica della Santissima Annunziata",
                    "Santissima Annunziata",
                    "Santissima Annunziata Florence square",
                ),
                (
                    "villa_bardini_garden",
                    "parks",
                    "Giardino Bardini",
                    "Villa Bardini",
                    "Bardini Garden Florence view Duomo",
                ),
                (
                    "stibbert_museum",
                    "museums",
                    "Stibbert Museum",
                    "Museo Stibbert",
                    "Stibbert Museum Florence villa",
                ),
                (
                    "piazza_massimo_azeglio",
                    "squares",
                    "Piazza Massimo d'Azeglio",
                    "Piazza d'Azeglio",
                    "Piazza Massimo d'Azeglio Florence",
                ),
                (
                    "tuscany_hall_opera",
                    "theaters",
                    "Teatro del Maggio Musicale Fiorentino",
                    "Opera di Firenze",
                    "Opera di Firenze Florence building",
                ),
                (
                    "fountain_neptune_florence",
                    "sculptures",
                    "Fountain of Neptune",
                    "Fontana del Nettuno",
                    "Fountain of Neptune Piazza della Signoria",
                ),
                (
                    "torre_arnolfo_palazzo_vecchio",
                    "landmarks",
                    "Torre d'Arnolfo",
                    "Palazzo Vecchio tower",
                    "Arnolfo tower Palazzo Vecchio Florence",
                ),
            ],
        },
        "madrid": {
            "subtitle_key": "subtitle_es",
            "rel_json": "madrid/data/madrid_places.json",
            "target_add": target["madrid"],
            "candidates": [
                (
                    "cybeles_palace_madrid",
                    "landmarks",
                    "Cybele Palace (City Hall)",
                    "Palacio de Cibeles",
                    "Palacio de Cibeles Madrid facade",
                ),
                (
                    "caixaforum_madrid",
                    "museums",
                    "CaixaForum Madrid",
                    "CaixaForum",
                    "CaixaForum Madrid vertical garden",
                ),
                (
                    "basilica_san_francisco_grande",
                    "places_of_worship",
                    "Royal Basilica of San Francisco el Grande",
                    "San Francisco el Grande",
                    "Basilica San Francisco el Grande Madrid dome",
                ),
                (
                    "plaza_colon_madrid",
                    "squares",
                    "Plaza de Colón",
                    "Plaza de Colón",
                    "Plaza de Colón Madrid monument",
                ),
                (
                    "sorolla_museum",
                    "museums",
                    "Sorolla Museum",
                    "Museo Sorolla",
                    "Museo Sorolla Madrid garden",
                ),
                (
                    "royal_botanical_garden_madrid",
                    "parks",
                    "Royal Botanical Garden of Madrid",
                    "Real Jardín Botánico",
                    "Real Jardín Botánico Madrid greenhouse",
                ),
                (
                    "ermita_san_antonio_florida",
                    "places_of_worship",
                    "Hermitage of San Antonio de la Florida",
                    "Ermita Florida",
                    "Ermita de San Antonio de la Florida Madrid Goya",
                ),
                (
                    "museo_cerralbo",
                    "museums",
                    "Cerralbo Museum",
                    "Museo Cerralbo",
                    "Museo Cerralbo Madrid palace",
                ),
                (
                    "zarzuela_theatre",
                    "theaters",
                    "Teatro de la Zarzuela",
                    "Teatro de la Zarzuela",
                    "Teatro de la Zarzuela Madrid facade",
                ),
                (
                    "plaza_de_cibeles_fountain",
                    "landmarks",
                    "Cibeles Fountain",
                    "Fuente de Cibeles",
                    "Fuente de Cibeles Madrid night",
                ),
                (
                    "national_archaeological_museum_madrid",
                    "museums",
                    "National Archaeological Museum",
                    "MAN Madrid",
                    "Museo Arqueológico Nacional Madrid building",
                ),
                (
                    "temple_romano_madrid",
                    "landmarks",
                    "Temple of Debod vicinity (Roman remains Madrid)",
                    "Madrid Romana",
                    "Roman remains Madrid archaeological",
                ),
            ],
        },
        "new_york": {
            "subtitle_key": "subtitle_en",
            "rel_json": "new_york/data/new_york_places.json",
            "target_add": target["new_york"],
            "candidates": [
                (
                    "tenement_museum_nyc",
                    "museums",
                    "Tenement Museum",
                    "Lower East Side",
                    "Tenement Museum New York Orchard Street",
                ),
                (
                    "yankee_stadium",
                    "landmarks",
                    "Yankee Stadium",
                    "The Bronx",
                    "Yankee Stadium exterior Bronx",
                ),
                (
                    "radio_city_music_hall",
                    "theaters",
                    "Radio City Music Hall",
                    "Rockefeller Center",
                    "Radio City Music Hall New York facade",
                ),
                (
                    "lincoln_center_plaza",
                    "landmarks",
                    "Lincoln Center for the Performing Arts",
                    "Upper West Side",
                    "Lincoln Center New York plaza fountain",
                ),
                (
                    "cathedral_st_john_divine",
                    "places_of_worship",
                    "Cathedral of St. John the Divine",
                    "Morningside Heights",
                    "Cathedral Saint John the Divine New York exterior",
                ),
                (
                    "whitney_museum_meatpacking",
                    "museums",
                    "Whitney Museum of American Art",
                    "Meatpacking District",
                    "Whitney Museum New York Renzo Piano building",
                ),
                (
                    "uss_intrepid_museum",
                    "museums",
                    "Intrepid Sea, Air & Space Museum",
                    "Hudson River",
                    "Intrepid museum New York aircraft carrier",
                ),
                (
                    "rockefeller_top_of_rock",
                    "viewpoints",
                    "Top of the Rock",
                    "30 Rockefeller Plaza",
                    "Top of the Rock observation deck New York",
                ),
                (
                    "brooklyn_dumbo_view",
                    "viewpoints",
                    "Dumbo, Brooklyn",
                    "Brooklyn waterfront",
                    "DUMBO Brooklyn Manhattan Bridge view",
                ),
                (
                    "federal_hall_nyc",
                    "landmarks",
                    "Federal Hall",
                    "Wall Street",
                    "Federal Hall National Memorial New York",
                ),
                (
                    "trinity_church_wall_street",
                    "places_of_worship",
                    "Trinity Church",
                    "Broadway at Wall Street",
                    "Trinity Church Wall Street New York",
                ),
                (
                    "stonewall_inn_monument",
                    "landmarks",
                    "Stonewall National Monument",
                    "Christopher Street",
                    "Stonewall Inn New York Greenwich Village",
                ),
                (
                    "brooklyn_public_library_central",
                    "libraries",
                    "Brooklyn Public Library (Central)",
                    "Grand Army Plaza",
                    "Brooklyn Public Library Central Library facade",
                ),
                (
                    "united_nations_headquarters",
                    "landmarks",
                    "United Nations Headquarters",
                    "First Avenue",
                    "United Nations Headquarters New York building",
                ),
            ],
        },
        "philadelphia": {
            "subtitle_key": "subtitle_en",
            "rel_json": "philadelphia/data/philadelphia_places.json",
            "target_add": target["philadelphia"],
            "candidates": [
                (
                    "mutter_museum",
                    "museums",
                    "Mütter Museum",
                    "College of Physicians",
                    "Mütter Museum Philadelphia exterior",
                ),
                (
                    "national_constitution_center",
                    "museums",
                    "National Constitution Center",
                    "Independence Mall",
                    "National Constitution Center Philadelphia",
                ),
                (
                    "academy_natural_sciences",
                    "museums",
                    "Academy of Natural Sciences of Drexel University",
                    "Logan Square",
                    "Academy of Natural Sciences Philadelphia building",
                ),
                (
                    "penn_museum",
                    "museums",
                    "Penn Museum",
                    "University of Pennsylvania",
                    "Penn Museum Philadelphia facade",
                ),
                (
                    "philadelphia_magic_gardens",
                    "landmarks",
                    "Philadelphia Magic Gardens",
                    "South Street",
                    "Philadelphia Magic Gardens mosaic",
                ),
                (
                    "philadelphia_30th_reading_viaduct",
                    "landmarks",
                    "The Rail Park",
                    "Callowhill",
                    "Philadelphia Rail Park elevated",
                ),
                (
                    "bartram_garden",
                    "parks",
                    "Bartram's Garden",
                    "Schuylkill River",
                    "Bartram's Garden Philadelphia historic house",
                ),
                (
                    "wissahickon_valley_park",
                    "parks",
                    "Wissahickon Valley Park",
                    "Fairmount",
                    "Wissahickon Valley Park Philadelphia creek",
                ),
                (
                    "fort_mifflin",
                    "landmarks",
                    "Fort Mifflin",
                    "Delaware River",
                    "Fort Mifflin Philadelphia",
                ),
                (
                    "shofuso_house",
                    "landmarks",
                    "Shofuso Japanese House and Garden",
                    "Fairmount Park",
                    "Shofuso Japanese House Philadelphia",
                ),
            ],
        },
        "prague": {
            "subtitle_key": "subtitle_cs",
            "rel_json": "prague/data/prague_places.json",
            "target_add": target["prague"],
            "candidates": [
                (
                    "wallenstein_garden",
                    "parks",
                    "Wallenstein Garden",
                    "Valdštejnská zahrada",
                    "Wallenstein Garden Prague palace",
                ),
                (
                    "national_technical_museum_prague",
                    "museums",
                    "National Technical Museum",
                    "Národní technické muzeum",
                    "National Technical Museum Prague building",
                ),
                (
                    "emauzy_monastery",
                    "places_of_worship",
                    "Emmaus Monastery",
                    "Na Slovanech",
                    "Emauzy monastery Prague Gothic",
                ),
                (
                    "kinsky_palace_old_town",
                    "palaces",
                    "Kinský Palace (Old Town Square)",
                    "Palác Kinských",
                    "Kinsky Palace Old Town Square Prague",
                ),
                (
                    "infant_jesus_prague_church",
                    "places_of_worship",
                    "Church of Our Lady Victorious",
                    "Pražské Jezulátko",
                    "Infant Jesus of Prague church",
                ),
                (
                    "klementinum_mirror_chapel",
                    "places_of_worship",
                    "Mirror Chapel (Klementinum)",
                    "Klementinum",
                    "Mirror Chapel Klementinum Prague",
                ),
                (
                    "naplavka_riverside",
                    "misc",
                    "Náplavka (Rašínovo nábřeží)",
                    "Rašínovo nábřeží",
                    "Naplavka Prague river embankment",
                ),
                (
                    "divadlo_na_vinohradech",
                    "theaters",
                    "Vinohrady Theatre",
                    "Divadlo na Vinohradech",
                    "Divadlo na Vinohradech Prague facade",
                ),
                (
                    "stromovka_park",
                    "parks",
                    "Stromovka (Royal Game Reserve)",
                    "Královská obora",
                    "Stromovka park Prague pond",
                ),
                (
                    "letna_metronome",
                    "landmarks",
                    "Letná Metronome",
                    "Metronom na Letné",
                    "Letna Metronome Prague",
                ),
                (
                    "troya_botanical_garden",
                    "parks",
                    "Prague Botanic Garden Troja",
                    "Botanická zahrada Troja",
                    "Prague Botanic Garden Troja greenhouse",
                ),
                (
                    "zizkov_tower",
                    "landmarks",
                    "Žižkov Television Tower",
                    "Žižkovská věž",
                    "Zizkov Television Tower Prague babies",
                ),
                (
                    "vysehrad_cemetery_slavin",
                    "cemeteries",
                    "Vyšehrad Cemetery",
                    "Slavín",
                    "Vysehrad cemetery Prague Slavin",
                ),
            ],
        },
        "rome": {
            "subtitle_key": "subtitle_it",
            "rel_json": "rome/data/rome_places.json",
            "target_add": target["rome"],
            "candidates": [
                (
                    "campo_de_fiori",
                    "squares",
                    "Campo de' Fiori",
                    "Campo de' Fiori",
                    "Campo de Fiori Rome market",
                ),
                (
                    "basilica_santa_maria_maggiore",
                    "places_of_worship",
                    "Basilica of Santa Maria Maggiore",
                    "Santa Maria Maggiore",
                    "Santa Maria Maggiore Rome facade",
                ),
                (
                    "basilica_san_paolo_fuori",
                    "places_of_worship",
                    "Basilica of Saint Paul Outside the Walls",
                    "San Paolo fuori le Mura",
                    "Basilica Saint Paul Outside the Walls Rome",
                ),
                (
                    "gianicolo_terrace",
                    "viewpoints",
                    "Gianicolo (Janiculum) overlook",
                    "Gianicolo",
                    "Gianicolo terrace Rome view",
                ),
                (
                    "palazzo_barberini",
                    "museums",
                    "Palazzo Barberini",
                    "Galleria Nazionale d'Arte Antica",
                    "Palazzo Barberini Rome facade",
                ),
                (
                    "capuchin_crypt_rome",
                    "museums",
                    "Capuchin Crypt",
                    "Santa Maria della Concezione",
                    "Capuchin Crypt Rome bones",
                ),
                (
                    "mausoleum_of_augustus",
                    "landmarks",
                    "Mausoleum of Augustus",
                    "Mausoleo di Augusto",
                    "Mausoleum of Augustus Rome exterior",
                ),
                (
                    "jewish_ghetto_portico_octavia",
                    "landmarks",
                    "Portico d'Ottavia",
                    "Jewish Ghetto",
                    "Portico d'Ottavia Rome",
                ),
                (
                    "testaccio_monte",
                    "landmarks",
                    "Monte Testaccio",
                    "Testaccio",
                    "Monte Testaccio Rome",
                ),
                (
                    "basilica_san_clemente",
                    "places_of_worship",
                    "Basilica of San Clemente",
                    "San Clemente",
                    "Basilica San Clemente Rome courtyard",
                ),
                (
                    "villa_farnesina",
                    "museums",
                    "Villa Farnesina",
                    "Villa Farnesina",
                    "Villa Farnesina Rome Trastevere fresco",
                ),
                (
                    "piazza_del_campidoglio",
                    "squares",
                    "Piazza del Campidoglio",
                    "Campidoglio",
                    "Piazza del Campidoglio Rome Michelangelo",
                ),
                (
                    "park_villa_borghese_lake",
                    "parks",
                    "Villa Borghese lake",
                    "Laghetto Villa Borghese",
                    "Villa Borghese lake Rome",
                ),
                (
                    "villa_sciarra",
                    "parks",
                    "Villa Sciarra",
                    "Gianicolo",
                    "Villa Sciarra Rome garden",
                ),
            ],
        },
        "venice": {
            "subtitle_key": "subtitle_it",
            "rel_json": "venice/data/venice_places.json",
            "target_add": target["venice"],
            "candidates": [
                (
                    "ca_rezzonico",
                    "museums",
                    "Ca' Rezzonico",
                    "Museo del Settecento Veneziano",
                    "Ca Rezzonico Venice facade canal",
                ),
                (
                    "scuola_grande_san_rocco",
                    "museums",
                    "Scuola Grande di San Rocco",
                    "Tintoretto",
                    "Scuola Grande San Rocco Venice facade",
                ),
                (
                    "santa_maria_formosa",
                    "places_of_worship",
                    "Santa Maria Formosa",
                    "Campo Santa Maria Formosa",
                    "Santa Maria Formosa Venice church",
                ),
                (
                    "campo_santa_margherita",
                    "squares",
                    "Campo Santa Margherita",
                    "Dorsoduro",
                    "Campo Santa Margherita Venice",
                ),
                (
                    "san_francesco_della_vigna",
                    "places_of_worship",
                    "San Francesco della Vigna",
                    "San Francesco della Vigna",
                    "San Francesco della Vigna Venice facade",
                ),
                (
                    "san_zaccaria_venice",
                    "places_of_worship",
                    "San Zaccaria",
                    "San Zaccaria",
                    "San Zaccaria Venice church facade",
                ),
                (
                    "campo_san_polo",
                    "squares",
                    "Campo San Polo",
                    "San Polo",
                    "Campo San Polo Venice",
                ),
                (
                    "giardini_biennale",
                    "parks",
                    "Giardini della Biennale",
                    "Giardini",
                    "Giardini Biennale Venice pavilion",
                ),
                (
                    "lido_di_venezia_beach",
                    "misc",
                    "Lido di Venezia beaches",
                    "Lido",
                    "Lido Venice beach Adriatic",
                ),
                (
                    "punta_della_dogana",
                    "landmarks",
                    "Punta della Dogana",
                    "Punta della Dogana",
                    "Punta della Dogana Venice Tadao Ando",
                ),
                (
                    "santa_maria_dei_miracoli",
                    "places_of_worship",
                    "Santa Maria dei Miracoli",
                    "Marble church",
                    "Santa Maria dei Miracoli Venice marble",
                ),
                (
                    "arsenale_gate_land",
                    "landmarks",
                    "Arsenale gate (land entrance)",
                    "Arsenale di Venezia",
                    "Venice Arsenale gate lions",
                ),
                (
                    "fondaco_dei_tedeschi_roof",
                    "viewpoints",
                    "Fondaco dei Tedeschi rooftop view",
                    "DFS Venezia",
                    "Fondaco Tedeschi Venice terrace view",
                ),
            ],
        },
        "vienna": {
            "subtitle_key": "subtitle_de",
            "rel_json": "vienna/data/vienna_places.json",
            "target_add": target["vienna"],
            "candidates": [
                (
                    "mozarthaus_vienna",
                    "museums",
                    "Mozarthaus Vienna",
                    "Domgasse 5",
                    "Mozarthaus Vienna museum facade",
                ),
                (
                    "haus_der_musik_vienna",
                    "museums",
                    "House of Music",
                    "Haus der Musik",
                    "Haus der Musik Vienna entrance",
                ),
                (
                    "judenplatz_holocaust_memorial",
                    "landmarks",
                    "Judenplatz Holocaust Memorial",
                    "Nameless Library",
                    "Judenplatz Holocaust memorial Vienna",
                ),
                (
                    "ankeruhr_vienna",
                    "landmarks",
                    "Ankeruhr",
                    "Hoher Markt",
                    "Ankeruhr Vienna clock",
                ),
                (
                    "tiergarten_schoenbrunn",
                    "misc",
                    "Schönbrunn Zoo",
                    "Tiergarten Schönbrunn",
                    "Schonbrunn Zoo Vienna pandas pavilion",
                ),
                (
                    "technisches_museum_wien",
                    "museums",
                    "Vienna Museum of Science and Technology",
                    "Technisches Museum",
                    "Technisches Museum Vienna building",
                ),
                (
                    "ruprechtskirche_vienna",
                    "places_of_worship",
                    "Church of St. Rupert",
                    "Ruprechtskirche",
                    "Ruprechtskirche Vienna oldest church",
                ),
                (
                    "urania_vienna",
                    "landmarks",
                    "Urania Observatory",
                    "Urania",
                    "Urania Vienna observatory building",
                ),
                (
                    "alois_drasche_park",
                    "parks",
                    "Schweizergarten",
                    "Schweizergarten",
                    "Schweizergarten Vienna Belvedere pond",
                ),
                (
                    "spanische_hofreitschule_facade",
                    "landmarks",
                    "Spanish Riding School façade",
                    "Hofburg",
                    "Spanish Riding School Vienna Michaelerplatz",
                ),
            ],
        },
        "montreal": {
            "subtitle_key": "subtitle_fr",
            "rel_json": "montreal/data/montreal_places.json",
            "target_add": target["montreal"],
            "candidates": [
                (
                    "mont_royal_cross_view",
                    "landmarks",
                    "Mount Royal Cross",
                    "Croix du mont Royal",
                    "Mount Royal Cross Montreal lookout",
                ),
                (
                    "pointe_a_calliere",
                    "museums",
                    "Pointe-à-Callière Museum",
                    "Musée Pointe-à-Callière",
                    "Pointe a Calliere museum Montreal Old Port",
                ),
                (
                    "planetarium_rio_tinto_alcan",
                    "museums",
                    "Rio Tinto Alcan Planetarium",
                    "Planétarium",
                    "Montreal planetarium building",
                ),
                (
                    "atwater_market",
                    "markets",
                    "Atwater Market",
                    "Marché Atwater",
                    "Atwater Market Montreal interior",
                ),
                (
                    "notre_dame_neiges_cemetery",
                    "cemeteries",
                    "Notre Dame des Neiges Cemetery",
                    "Cimetière Notre-Dame-des-Neiges",
                    "Notre Dame des Neiges cemetery Montreal",
                ),
                (
                    "montreal_insectarium",
                    "museums",
                    "Montreal Insectarium",
                    "Insectarium",
                    "Montreal Insectarium building",
                ),
                (
                    "biodome_montreal",
                    "museums",
                    "Montreal Biodome",
                    "Biodôme",
                    "Biodome Montreal Olympic Park",
                ),
                (
                    "eglise_saint_patrick_montreal",
                    "places_of_worship",
                    "Saint Patrick's Basilica",
                    "Saint-Patrick",
                    "Saint Patrick Basilica Montreal",
                ),
                (
                    "rue_saint_paul_old_montreal",
                    "misc",
                    "Rue Saint-Paul",
                    "Vieux-Montréal",
                    "Rue Saint-Paul Old Montreal cafes",
                ),
                (
                    "chalet_du_mont_royal",
                    "landmarks",
                    "Mount Royal Chalet",
                    "Chalet du Mont-Royal",
                    "Mount Royal Chalet Montreal",
                ),
                (
                    "lachine_canal_locks",
                    "landmarks",
                    "Lachine Canal",
                    "Canal de Lachine",
                    "Lachine Canal Montreal pathway",
                ),
                (
                    "parc_la_fontaine",
                    "parks",
                    "La Fontaine Park",
                    "Parc La Fontaine",
                    "Parc La Fontaine Montreal pond",
                ),
                (
                    "place_des_arts_montreal",
                    "theaters",
                    "Place des Arts",
                    "Quartier des spectacles",
                    "Place des Arts Montreal exterior",
                ),
                (
                    "grande_bibliotheque_banq",
                    "libraries",
                    "Grande Bibliothèque (BAnQ)",
                    "Grande Bibliothèque",
                    "Grande Bibliotheque Montreal building",
                ),
                (
                    "orange_julep_gibeau",
                    "landmarks",
                    "Gibeau Orange Julep",
                    "Decarie",
                    "Orange Julep Montreal building",
                ),
                (
                    "stade_uniprix",
                    "landmarks",
                    "IGA Stadium (Uniprix)",
                    "Jarry Park",
                    "Stade IGA Montreal tennis",
                ),
                (
                    "mccord_museum_montreal",
                    "museums",
                    "McCord Stewart Museum",
                    "Musée McCord",
                    "McCord Museum Montreal Sherbrooke",
                ),
                (
                    "cimetiere_notre_dame_neiges_chapel",
                    "cemeteries",
                    "Notre-Dame-des-Neiges (chapel entrance)",
                    "Cimetière montagne",
                    "Notre Dame des Neiges Montreal chapel",
                ),
                (
                    "ile_sainte_helene_jean_drapeau",
                    "landmarks",
                    "Île Sainte-Hélène",
                    "Parc Jean-Drapeau",
                    "Ile Sainte Helene Montreal Biosphere view",
                ),
            ],
        },
        "paris": {
            "subtitle_key": "subtitle_fr",
            "rel_json": "paris/data/paris_places.json",
            "target_add": target["paris"],
            "candidates": [
                (
                    "musee_rodin_paris",
                    "museums",
                    "Musée Rodin",
                    "Hôtel Biron",
                    "Musee Rodin Paris garden thinker",
                ),
                (
                    "musee_cluny",
                    "museums",
                    "Musée de Cluny",
                    "Musée national du Moyen Âge",
                    "Musee de Cluny Paris exterior",
                ),
                (
                    "parc_monceau",
                    "parks",
                    "Parc Monceau",
                    "Parc Monceau",
                    "Parc Monceau Paris rotunda",
                ),
                (
                    "musee_quai_branly",
                    "museums",
                    "Musée du quai Branly – Jacques Chirac",
                    "Quai Branly",
                    "Musee du quai Branly Paris vegetated wall",
                ),
                (
                    "cite_des_sciences",
                    "museums",
                    "Cité des sciences et de l'industrie",
                    "Parc de la Villette",
                    "Cite des sciences Paris Geode",
                ),
                (
                    "musee_carnavalet",
                    "museums",
                    "Carnavalet Museum",
                    "Musée Carnavalet",
                    "Musee Carnavalet Paris courtyard",
                ),
                (
                    "institut_du_monde_arabe",
                    "museums",
                    "Arab World Institute",
                    "Institut du monde arabe",
                    "Institut du monde arabe Paris facade",
                ),
                (
                    "pont_des_arts",
                    "bridges",
                    "Pont des Arts",
                    "Pont des Arts",
                    "Pont des Arts Paris Seine",
                ),
                (
                    "hotel_de_sens",
                    "palaces",
                    "Hôtel de Sens",
                    "Le Marais",
                    "Hotel de Sens Paris medieval",
                ),
                (
                    "bois_de_vincennes_lake",
                    "parks",
                    "Bois de Vincennes",
                    "Lac Daumesnil",
                    "Bois de Vincennes Paris lake",
                ),
                (
                    "sacre_coeur_steps",
                    "landmarks",
                    "Basilica of Sacré-Cœur (approach)",
                    "Montmartre",
                    "Sacré-Cœur Montmartre stairs",
                ),
                (
                    "place_des_vosges",
                    "squares",
                    "Place des Vosges",
                    "Le Marais",
                    "Place des Vosges Paris arcades",
                ),
            ],
        },
    }


def main() -> int:
    cfg = _load_cfg()
    for city, block in cfg.items():
        path = _PROJECT_ROOT / block["rel_json"]
        rows: list[dict[str, Any]] = json.loads(
            path.read_text(encoding="utf-8"),
        )
        have = {r.get("slug") for r in rows if isinstance(r, dict)}
        subtitle_key: str = block["subtitle_key"]
        cap: int = int(block["target_add"])
        added: list[dict[str, Any]] = []
        for (
            slug,
            category,
            name_en,
            subtitle_val,
            query,
        ) in block["candidates"]:
            if len(added) >= cap:
                break
            if slug in have:
                continue
            if "skip" in slug or "duplicate" in slug.lower():
                continue
            u, title = _search_first_jpeg_url(query)
            time.sleep(_SEARCH_SLEEP_SEC)
            if not u:
                print("{}: no JPEG for {}".format(city, slug))
                continue
            rec = _place_record(
                slug, category, name_en, subtitle_key, subtitle_val, u,
            )
            added.append(rec)
            have.add(slug)
            print("{}: + {} [{}]".format(city, slug, title))
        if added:
            rows.extend(added)
            path.write_text(
                json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            print("{} saved +{} entries".format(city, len(added)))
        time.sleep(_SAVE_SLEEP_SEC)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
