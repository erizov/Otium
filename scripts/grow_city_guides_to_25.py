# -*- coding: utf-8 -*-
"""Grow per-city guides to >=25 places using Wikimedia Commons search.

Reads each ``<slug>/data/<slug>_places.json``, appends new rows for slugs
not yet present, resolves ``commons_file`` via search + batched imageinfo,
writes JSON back. Also creates new city trees when ``--bootstrap <slug>``.

Requires network for Commons API.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_USER_AGENT = "ExcursionGuide/1.0 (grow_city_guides_to_25.py)"

_MIN_PLACES = 25

_STATIC_COMMONS_PATH = Path(__file__).resolve().parent / (
    "grow_existing_static_commons.json"
)


def _load_static_commons_map() -> dict[str, dict[str, str]]:
    """Optional curated titles when Commons search is rate-limited."""
    if not _STATIC_COMMONS_PATH.is_file():
        return {}
    raw = json.loads(_STATIC_COMMONS_PATH.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        return {}
    out: dict[str, dict[str, str]] = {}
    for key, val in raw.items():
        if not isinstance(val, dict):
            continue
        out[str(key)] = {
            str(a): str(b)
            for a, b in val.items()
            if isinstance(a, str) and isinstance(b, str)
        }
    return out


_STATIC_COMMONS_FILE: dict[str, dict[str, str]] = _load_static_commons_map()
_BAD_SUFFIX = (".pdf", ".webm", ".djvu", ".tif", ".tiff")

# Cities that shipped with 12 curated rows; each needs 13 more.
_EXISTING_12: tuple[str, ...] = (
    "amsterdam",
    "athens",
    "bangkok",
    "copenhagen",
    "dubai",
    "dublin",
    "istanbul",
    "lisbon",
    "london",
    "los_angeles",
    "san_francisco",
    "singapore",
    "tokyo",
    "vatican",
)

# (slug, name_en, category, commons_search_query)
_SEEDS: dict[str, list[tuple[str, str, str, str]]] = {}

_SEEDS["amsterdam"] = [
    ("amsterdam_begijnhof", "Begijnhof", "public_space", "Begijnhof Amsterdam"),
    ("amsterdam_magere_brug", "Magere Brug", "bridges", "Magere Brug Amsterdam"),
    ("amsterdam_concertgebouw", "Royal Concertgebouw", "theaters", "Concertgebouw Amsterdam"),
    ("amsterdam_rembrandt_house", "Rembrandt House Museum", "museums", "Rembrandt House Amsterdam"),
    ("amsterdam_artis", "Artis Zoo", "parks", "Artis Zoo Amsterdam entrance"),
    ("amsterdam_hermitage_amsterdam", "Hermitage Amsterdam", "museums", "Hermitage Amsterdam museum"),
    ("amsterdam_portuguese_synagogue", "Portuguese Synagogue", "places_of_worship", "Portuguese Synagogue Amsterdam"),
    ("amsterdam_de_gooyer", "De Gooyer windmill", "landmarks", "De Gooyer windmill Amsterdam"),
    ("amsterdam_bloemenmarkt", "Singel flower market", "markets", "Bloemenmarkt Amsterdam Singel"),
    ("amsterdam_foam", "Foam photography museum", "museums", "Foam photography museum Amsterdam"),
    ("amsterdam_eye_film", "EYE Film Institute", "museums", "EYE Film Institute Amsterdam"),
    ("amsterdam_adam_tower", "A'DAM Tower", "landmarks", "Overhoeks tower Amsterdam"),
    ("amsterdam_scheepvaartmuseum", "National Maritime Museum", "museums", "Scheepvaartmuseum Amsterdam"),
]

_SEEDS["athens"] = [
    ("athens_benaki_museum", "Benaki Museum", "museums", "Benaki Museum Athens"),
    ("athens_lycabettus", "Mount Lycabettus", "viewpoints", "Lycabettus hill Athens"),
    ("athens_kerameikos", "Kerameikos cemetery", "cemeteries", "Kerameikos Athens"),
    ("athens_national_garden", "National Garden", "parks", "National Garden Athens Zappeion"),
    ("athens_byzantine_museum", "Byzantine and Christian Museum", "museums", "Byzantine Museum Athens"),
    ("athens_filopappou", "Filopappou Hill", "viewpoints", "Philopappos monument Athens"),
    ("athens_psyrri", "Psyrri quarter", "overview", "Psyrri Athens street"),
    ("athens_sounion", "Temple of Poseidon Sounion", "places_of_worship", "Temple Poseidon Sounion Greece"),
    ("athens_kaisariani", "Kaisariani Monastery", "places_of_worship", "Kaisariani Monastery Athens"),
    ("athens_numismatic_museum", "Numismatic Museum", "museums", "Numismatic Museum Athens"),
    ("athens_hadrian_library", "Hadrian's Library", "landmarks", "Hadrians Library Athens Agora"),
    ("athens_museum_of_cycladic", "Museum of Cycladic Art", "museums", "Museum of Cycladic Art Athens"),
    ("athens_stavros_niarchos", "Stavros Niarchos Foundation", "overview", "Stavros Niarchos Foundation Cultural Center"),
]

_SEEDS["bangkok"] = [
    ("bangkok_wat_phrakaew", "Wat Phra Kaew", "places_of_worship", "Wat Phra Kaew Bangkok"),
    ("bangkok_mbk_center", "MBK Center", "markets", "MBK Center Bangkok"),
    ("bangkok_iconsiam", "ICONSIAM", "overview", "ICONSIAM Bangkok"),
    ("bangkok_national_museum", "National Museum Bangkok", "museums", "National Museum Bangkok"),
    ("bangkok_wat_ratchanatdaram", "Wat Ratchanatdaram", "places_of_worship", "Loha Prasat Wat Ratchanatdaram Bangkok"),
    ("bangkok_siam_paragon", "Siam Paragon", "overview", "Siam Paragon Bangkok"),
    ("bangkok_asiatique", "Asiatique riverfront", "markets", "Asiatique Bangkok"),
    ("bangkok_mahanakhon", "King Power Mahanakhon", "landmarks", "Mahanakhon tower Bangkok"),
    ("bangkok_jim_thompson_art", "Jim Thompson Art Center", "museums", "Jim Thompson House Bangkok"),
    ("bangkok_wat_kalayanamit", "Wat Kalayanamit", "places_of_worship", "Wat Kalayanamit Bangkok"),
    ("bangkok_chatuchak_park", "Chatuchak Park", "parks", "Chatuchak Park Bangkok"),
    ("bangkok_roayal_barges", "Royal Barges Museum", "museums", "Royal Barges Museum Bangkok"),
    ("bangkok_bang_namphueng", "Bang Krachao", "parks", "Bang Krachao Bangkok green lung"),
]

_SEEDS["copenhagen"] = [
    ("copenhagen_rosenborg", "Rosenborg Castle", "palaces", "Rosenborg Castle Copenhagen"),
    ("copenhagen_christiansborg", "Christiansborg Palace", "palaces", "Christiansborg Palace Copenhagen"),
    ("copenhagen_round_tower", "Round Tower", "landmarks", "Round Tower Copenhagen"),
    ("copenhagen_assistens", "Assistens Cemetery", "cemeteries", "Assistens Kirkegard Copenhagen"),
    ("copenhagen_designmuseum", "Designmuseum Denmark", "museums", "Designmuseum Denmark Copenhagen"),
    ("copenhagen_torvehallerne", "Torvehallerne market", "markets", "Torvehallerne Copenhagen"),
    ("copenhagen_botanical", "Botanical Garden", "parks", "University Botanical Garden Copenhagen"),
    ("copenhagen_black_diamond", "Black Diamond library", "libraries", "Black Diamond Copenhagen library"),
    ("copenhagen_bakken", "Bakken amusement park", "parks", "Bakken Klampenborg"),
    ("copenhagen_church_marble", "Marble Church", "places_of_worship", "Frederiks Kirke Copenhagen"),
    ("copenhagen_glyptotek", "Ny Carlsberg Glyptotek", "museums", "Ny Carlsberg Glyptotek Copenhagen"),
    ("copenhagen_kastellet", "Kastellet fortress", "landmarks", "Kastellet Copenhagen"),
    ("copenhagen_superkilen", "Superkilen park", "parks", "Superkilen Copenhagen"),
]

_SEEDS["dublin"] = [
    ("dublin_kilmainham", "Kilmainham Gaol", "museums", "Kilmainham Gaol Dublin"),
    ("dublin_guinness_storehouse", "Guinness Storehouse", "museums", "Guinness Storehouse Dublin"),
    ("dublin_phoenix_park", "Phoenix Park", "parks", "Phoenix Park Dublin"),
    ("dublin_merrion_square", "Merrion Square", "public_space", "Merrion Square Dublin"),
    ("dublin_epic_museum", "EPIC Irish Emigration Museum", "museums", "EPIC museum Dublin docklands"),
    ("dublin_jameson", "Jameson Distillery Bow St", "museums", "Jameson Distillery Dublin"),
    ("dublin_st_michan", "St Michan's Church", "places_of_worship", "St Michans Church Dublin"),
    ("dublin_marsh_library", "Marsh's Library", "libraries", "Marshs Library Dublin"),
    ("dublin_chester_beatty", "Chester Beatty Library", "museums", "Chester Beatty Library Dublin"),
    ("dublin_grand_canal", "Grand Canal Dock", "overview", "Grand Canal Dock Dublin"),
    ("dublin_howth", "Howth head", "viewpoints", "Howth harbour Ireland"),
    ("dublin_national_gallery", "National Gallery of Ireland", "museums", "National Gallery Ireland Dublin"),
    ("dublin_swift_alley", "Temple Bar cultural quarter", "overview", "Temple Bar Dublin street"),
]

_SEEDS["dubai"] = [
    ("dubai_expo_city", "Expo City Dubai", "overview", "Expo 2020 Dubai pavilion"),
    ("dubai_la_mer", "La Mer beachfront", "overview", "La Mer Dubai Jumeirah"),
    ("dubai_city_walk", "City Walk Dubai", "overview", "City Walk Dubai"),
    ("dubai_hatta", "Hatta Dam", "viewpoints", "Hatta Dam UAE"),
    ("dubai_gold_souk", "Gold Souk Deira", "markets", "Dubai Gold Souk Deira"),
        ("dubai_spice_deira", "Deira Old Souk", "markets", "Spice souk Deira Dubai"),
    ("dubai_jumeirah_mosque", "Jumeirah Mosque", "places_of_worship", "Jumeirah Mosque Dubai"),
    ("dubai_kite_beach", "Kite Beach", "parks", "Kite Beach Dubai"),
    ("dubai_dubai_hills", "Dubai Hills Park", "parks", "Dubai Hills Park"),
    ("dubai_opera", "Dubai Opera", "theaters", "Dubai Opera building"),
    ("dubai_safa_park", "Safa Park", "parks", "Safa Park Dubai"),
    ("dubai_wild_wadi", "Wild Wadi Waterpark", "parks", "Wild Wadi Dubai"),
    ("dubai_alserkal", "Alserkal Avenue", "overview", "Alserkal Avenue Dubai"),
]

_SEEDS["istanbul"] = [
    ("istanbul_rustem_pasha", "Rüstem Pasha Mosque", "places_of_worship", "Rustem Pasha Mosque Istanbul"),
    ("istanbul_ortakoy", "Ortaköy Mosque", "places_of_worship", "Ortakoy Mosque Istanbul"),
    ("istanbul_istanbul_modern", "Istanbul Museum of Modern Art", "museums", "Istanbul Modern museum"),
    ("istanbul_pera_museum", "Pera Museum", "museums", "Pera Museum Istanbul"),
    ("istanbul_miniaturk", "Miniaturk", "museums", "Miniaturk Istanbul"),
    ("istanbul_pierre_loti", "Pierre Loti Hill", "viewpoints", "Pierre Loti Hill Istanbul"),
    ("istanbul_beylerbeyi", "Beylerbeyi Palace", "palaces", "Beylerbeyi Palace Istanbul"),
    ("istanbul_rahmi_museum", "Rahmi M. Koç Museum", "museums", "Rahmi Koc Museum Istanbul"),
    ("istanbul_balat", "Balat district", "overview", "Balat Istanbul colorful houses"),
    ("istanbul_kadikoy_market", "Kadıköy market street", "markets", "Kadikoy market Istanbul"),
    ("istanbul_emirgan_park", "Emirgan Park", "parks", "Emirgan Park Istanbul tulips"),
    ("istanbul_sakirin", "Şakirin Mosque", "places_of_worship", "Sakirin Mosque Istanbul"),
    ("istanbul_vialand", "Vialand theme gate", "overview", "Isfanbul theme park Istanbul"),
]

_SEEDS["lisbon"] = [
    ("lisbon_oceanario", "Oceanário de Lisboa", "museums", "Oceanario Lisbon"),
    ("lisbon_padrao_descobrimentos", "Padrão dos Descobrimentos", "landmarks", "Padrao dos Descobrimentos Lisbon"),
    ("lisbon_25_abril_bridge", "25 de Abril Bridge", "bridges", "25 de Abril Bridge Lisbon"),
    ("lisbon_estrela_basilica", "Estrela Basilica", "places_of_worship", "Estrela Basilica Lisbon"),
    ("lisbon_miradouro_graca", "Miradouro da Graça", "viewpoints", "Miradouro da Graca Lisbon"),
    ("lisbon_cais_colunas", "Cais das Colunas", "public_space", "Cais das Colunas Lisbon"),
    ("lisbon_praca_municipio", "Praça do Município", "public_space", "Praca do Municipio Lisbon"),
    ("lisbon_parque_eduardo_vii", "Parque Eduardo VII", "parks", "Parque Eduardo VII Lisbon"),
    ("lisbon_gulbenkian", "Calouste Gulbenkian Museum", "museums", "Gulbenkian Museum Lisbon"),
    ("lisbon_miradouro_senhora_monte", "Miradouro da Senhora do Monte", "viewpoints", "Miradouro Senhora do Monte Lisbon"),
    ("lisbon_palacio_belem", "Belém Palace", "palaces", "Belem Palace Lisbon"),
    ("lisbon_campo_pequeno", "Campo Pequeno bullring", "landmarks", "Campo Pequeno Lisbon"),
    ("lisbon_aqueduto_agua_livre", "Águas Livres Aqueduct", "bridges", "Aguas Livres Aqueduct Lisbon"),
]

_SEEDS["london"] = [
    ("london_tate_britain", "Tate Britain", "museums", "Tate Britain London"),
    ("london_natural_history", "Natural History Museum", "museums", "Natural History Museum London"),
    ("london_hyde_park", "Hyde Park", "parks", "Hyde Park London"),
    ("london_kensington_palace", "Kensington Palace", "palaces", "Kensington Palace London"),
    ("london_camden_market", "Camden Market", "markets", "Camden Market London"),
    ("london_notting_hill", "Notting Hill Portobello", "markets", "Portobello Road market"),
    ("london_va_museum", "Victoria and Albert Museum", "museums", "Victoria and Albert Museum London"),
    ("london_churchill_war_rooms", "Churchill War Rooms", "museums", "Churchill War Rooms London"),
    ("london_shakespeare_globe", "Shakespeare's Globe", "theaters", "Shakespeare Globe London"),
    ("london_canary_wharf", "Canary Wharf", "overview", "Canary Wharf London"),
    ("london_greenwich_observatory", "Royal Observatory Greenwich", "museums", "Royal Observatory Greenwich"),
    ("london_kew_gardens", "Kew Gardens Palm House", "parks", "Kew Gardens Palm House"),
    ("london_borough_market", "Borough Market", "markets", "Borough Market London"),
]

_SEEDS["los_angeles"] = [
    ("los_angeles_the_broad", "The Broad", "museums", "The Broad museum Los Angeles"),
    ("los_angeles_lacma", "LACMA", "museums", "LACMA Los Angeles"),
    ("los_angeles_union_station", "Union Station LA", "railway_stations", "Union Station Los Angeles"),
    ("los_angeles_olvera_street", "Olvera Street", "markets", "Olvera Street Los Angeles"),
    ("los_angeles_cathedral", "Cathedral of Our Lady", "places_of_worship", "Cathedral of Our Lady of the Angels"),
    ("los_angeles_nhm_la", "Natural History Museum LA", "museums", "Natural History Museum Los Angeles"),
    ("los_angeles_last_bookstore", "The Last Bookstore", "libraries", "Last Bookstore Los Angeles"),
    ("los_angeles_petersen", "Petersen Automotive Museum", "museums", "Petersen Automotive Museum"),
    ("los_angeles_crypto_arena", "Crypto.com Arena", "theaters", "Staples Center Los Angeles exterior"),
    ("los_angeles_rodeo_drive", "Rodeo Drive", "overview", "Rodeo Drive Beverly Hills"),
    ("los_angeles_paramount_studio", "Paramount Pictures gate", "landmarks", "Paramount Pictures studio gate"),
    ("los_angeles_malibu_pier", "Malibu Pier", "landmarks", "Malibu Pier California"),
    ("los_angeles_exposition_park", "Exposition Park Rose Garden", "parks", "Exposition Park Los Angeles"),
]

_SEEDS["san_francisco"] = [
    ("san_francisco_exploratorium", "Exploratorium", "museums", "Exploratorium San Francisco"),
    ("san_francisco_de_young", "de Young Museum", "museums", "de Young museum San Francisco"),
    ("san_francisco_legion_honor", "Legion of Honor", "museums", "Legion of Honor museum San Francisco"),
    ("san_francisco_coit_tower", "Coit Tower", "landmarks", "Coit Tower San Francisco"),
    ("san_francisco_fishermans_wharf", "Fisherman's Wharf", "overview", "Fishermans Wharf San Francisco"),
    ("san_francisco_golden_gate_park", "Golden Gate Park", "parks", "Golden Gate Park San Francisco"),
    ("san_francisco_palace_fine_arts", "Palace of Fine Arts", "landmarks", "Palace of Fine Arts San Francisco"),
    ("san_francisco_castro", "Castro Theatre", "theaters", "Castro Theatre San Francisco"),
    ("san_francisco_mission_dolores", "Mission Dolores", "places_of_worship", "Mission Dolores San Francisco"),
    ("san_francisco_salesforce_park", "Salesforce Park", "parks", "Salesforce Transit Center park"),
    ("san_francisco_ferry_building", "Ferry Building", "markets", "Ferry Building San Francisco"),
    ("san_francisco_twin_peaks", "Twin Peaks view", "viewpoints", "Twin Peaks San Francisco view"),
    ("san_francisco_sutro_baths", "Sutro Baths ruins", "landmarks", "Sutro Baths San Francisco"),
]

_SEEDS["singapore"] = [
    ("singapore_sentosa", "Sentosa Island", "overview", "Sentosa Singapore beach"),
    ("singapore_orchard_road", "Orchard Road", "overview", "Orchard Road Singapore"),
    ("singapore_macritchie", "MacRitchie Reservoir", "parks", "MacRitchie Reservoir Singapore"),
    ("singapore_singapore_zoo", "Singapore Zoo", "parks", "Singapore Zoo entrance"),
    ("singapore_jewel_changi", "Jewel Changi Airport", "landmarks", "Jewel Changi Airport waterfall"),
    ("singapore_fort_canning", "Fort Canning Park", "parks", "Fort Canning Park Singapore"),
    ("singapore_peranakan_museum", "Peranakan Museum", "museums", "Peranakan Museum Singapore"),
    ("singapore_sultan_mosque", "Sultan Mosque", "places_of_worship", "Sultan Mosque Singapore Kampong Glam"),
    ("singapore_esplanade", "Esplanade Theatres", "theaters", "Esplanade Theatres on the Bay"),
    ("singapore_singapore_flyer", "Singapore Flyer", "landmarks", "Singapore Flyer"),
    ("singapore_southern_ridges", "Henderson Waves", "bridges", "Henderson Waves Singapore"),
    ("singapore_little_india", "Little India Serangoon", "overview", "Little India Singapore street"),
    ("singapore_buddha_relic_out", "Chinatown Buddha Tooth exterior", "places_of_worship", "Buddha Tooth Relic Temple Singapore facade"),
]

_SEEDS["tokyo"] = [
    ("tokyo_shinjuku_gyoen", "Shinjuku Gyoen", "parks", "Shinjuku Gyoen Tokyo"),
    ("tokyo_ueno_park", "Ueno Park", "parks", "Ueno Park Tokyo"),
    ("tokyo_national_museum", "Tokyo National Museum", "museums", "Tokyo National Museum Honkan"),
    ("tokyo_ginza", "Ginza crossing", "overview", "Ginza Tokyo street"),
    ("tokyo_akihabara", "Akihabara Electric Town", "markets", "Akihabara Tokyo"),
    ("tokyo_roppongi_hills", "Roppongi Hills Mori Tower", "landmarks", "Roppongi Hills Tokyo"),
    ("tokyo_oedo_odaiba", "Odaiba Statue of Liberty", "landmarks", "Odaiba Statue of Liberty Tokyo"),
    ("tokyo_hamarikyu", "Hamarikyu Garden", "parks", "Hamarikyu Garden Tokyo"),
    ("tokyo_nezu_museum", "Nezu Museum", "museums", "Nezu Museum Tokyo"),
    ("tokyo_yanaka_ginza", "Yanaka Ginza", "markets", "Yanaka Ginza Tokyo"),
    ("tokyo_zojoji", "Zōjō-ji Temple", "places_of_worship", "Zojoji temple Tokyo"),
    ("tokyo_edo_tokyo_museum", "Edo-Tokyo Museum", "museums", "Edo-Tokyo Museum"),
    ("tokyo_sumida_park", "Sumida Park", "parks", "Sumida Park Tokyo Skytree"),
]

_SEEDS["vatican"] = [
    ("vatican_raphael_rooms", "Raphael Rooms", "museums", "Raphael Rooms Vatican"),
    ("vatican_cortile_pigna", "Court of the Pigna", "landmarks", "Cortile della Pigna Vatican"),
    ("vatican_biblioteca_apostolica", "Vatican Apostolic Library", "libraries", "Vatican Library ceiling"),
    ("vatican_necropolis_scavi", "Vatican excavations area", "museums", "Vatican scavi necropolis"),
    ("vatican_audience_hall", "Paul VI Audience Hall", "theaters", "Paul VI Audience Hall Vatican"),
    ("vatican_ethnological_museum", "Anima Mundi Museum Vatican", "museums", "Vatican ethnological museum"),
    ("vatican_carriage_pavilion", "Carriage Pavilion Vatican", "museums", "Papal carriages Vatican"),
    ("vatican_gregorian_egyptian", "Gregorian Egyptian Museum", "museums", "Gregorian Egyptian Museum Vatican"),
    ("vatican_gregorian_etruscan", "Gregorian Etruscan Museum", "museums", "Gregorian Etruscan Museum Vatican"),
    ("vatican_pinacoteca_vatican", "Vatican Pinacoteca gallery", "museums", "Vatican Pinacoteca gallery"),
    ("vatican_cupola_exterior", "Saint Peter's dome exterior", "landmarks", "Saint Peters dome exterior Vatican"),
    ("vatican_swiss_guard_gate", "Porta Sant'Anna", "landmarks", "Porta Sant Anna Vatican"),
    ("vatican_obelisk_st_peters", "Vatican Obelisk", "landmarks", "Vatican Obelisk Saint Peters Square"),
]


def _commons_search_title(query: str, *, pause: float) -> str | None:
    """Return first raster-like Commons file *title* (no ``File:`` prefix)."""
    q = urllib.parse.urlencode(
        {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srnamespace": "6",
            "format": "json",
            "srlimit": "20",
        },
    )
    url = "https://commons.wikimedia.org/w/api.php?" + q
    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    payload: dict[str, Any] | None = None
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            break
        except (urllib.error.URLError, OSError, ValueError, ConnectionResetError):
            time.sleep(2.0 + attempt * 3.0)
    if payload is None:
        return None
    time.sleep(pause)
    for hit in payload.get("query", {}).get("search", []):
        title = hit.get("title", "")
        if not title.startswith("File:"):
            continue
        name = title[5:]
        low = name.lower()
        if any(low.endswith(s) for s in (".pdf", ".webm", ".djvu", ".svg")):
            continue
        if low.endswith((".jpg", ".jpeg", ".png", ".webp", ".gif")):
            return name
    for hit in payload.get("query", {}).get("search", []):
        title = hit.get("title", "")
        if title.startswith("File:"):
            name = title[5:]
            low = name.lower()
            if not any(low.endswith(s) for s in _BAD_SUFFIX):
                return name
    return None


def _batch_commons_urls(
    titles: list[str],
    *,
    pause_sec: float,
) -> dict[str, str]:
    if not titles:
        return {}
    pipe = "|".join(
        ("File:" + t) if not t.startswith("File:") else t
        for t in titles
    )
    q = urllib.parse.urlencode(
        {
            "action": "query",
            "titles": pipe,
            "prop": "imageinfo",
            "iiprop": "url",
            "format": "json",
        },
    )
    url = "https://commons.wikimedia.org/w/api.php?" + q
    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    wait = 6.0
    data: dict[str, Any] | None = None
    for attempt in range(12):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            print(
                "  429 batch: sleep {:.0f}s ({}/12)".format(wait, attempt + 1),
                file=sys.stderr,
            )
            time.sleep(wait)
            wait = min(wait * 1.5, 180.0)
        except (ConnectionResetError, urllib.error.URLError, OSError):
            print(
                "  batch retry {}/12 (connection reset)".format(attempt + 1),
                file=sys.stderr,
            )
            time.sleep(wait)
            wait = min(wait * 1.2, 120.0)
    if data is None:
        raise SystemExit("Commons batch query failed (rate limit)")
    by_title: dict[str, str] = {}
    for page in data["query"]["pages"].values():
        t = page.get("title", "")
        if t.startswith("File:"):
            t = t[5:]
        if "imageinfo" not in page:
            continue
        by_title[t] = str(page["imageinfo"][0]["url"])
    out: dict[str, str] = {}
    for want in titles:
        if want in by_title:
            out[want] = by_title[want]
            continue
        low = want.casefold()
        hit = None
        for got, u in by_title.items():
            if got.casefold() == low:
                hit = u
                break
        if hit is None:
            raise SystemExit(
                "Missing imageinfo for {!r} (got {!r})".format(
                    want,
                    sorted(by_title),
                ),
            )
        out[want] = hit
    time.sleep(max(0.0, pause_sec))
    return out


def _finalize_row(
    partial: dict[str, Any],
    *,
    url_map: dict[str, str],
) -> dict[str, Any]:
    slug = partial["slug"]
    cf = partial.get("commons_file")
    cached = partial.get("image_source_url")
    if cached:
        src = str(cached)
    elif cf:
        src = url_map.get(cf)
    else:
        src = None
    if not src:
        raise SystemExit(
            "Missing image URL for {} (commons_file={!r})".format(slug, cf),
        )
    row = {k: v for k, v in partial.items() if k not in ("commons_file",)}
    row["image_source_url"] = src
    row["image_rel_path"] = "images/{}.jpg".format(slug)
    row["license_note"] = "See Wikimedia Commons file page for license."
    row["attribution"] = "Wikimedia Commons contributors"
    return row


def _generic_place_row(
    slug: str,
    name_en: str,
    category: str,
    *,
    address: str,
    commons_file: str,
) -> dict[str, Any]:
    return {
        "slug": slug,
        "category": category,
        "name_en": name_en,
        "address": address,
        "description": (
            "Notable city landmark; see Commons file page for photograph "
            "context and reuse terms."
        ),
        "facts": [
            "Check opening hours and ticketing on official sites before travel.",
            "Crowds peak on weekends and public holidays.",
        ],
        "commons_file": commons_file,
    }


def _grow_existing(
    *,
    pause_search: float,
    batch_size: int,
    batch_pause: float,
) -> None:
    needed_files: list[str] = []
    work: list[tuple[str, Path, list[dict[str, Any]], list[dict[str, Any]]]] = []

    for slug in _EXISTING_12:
        path = _PROJECT_ROOT / slug / "data" / "{}_places.json".format(slug)
        rows = json.loads(path.read_text(encoding="utf-8"))
        if len(rows) >= _MIN_PLACES:
            print(slug, "skip (already", len(rows), "places)")
            continue
        seeds = _SEEDS.get(slug)
        if not seeds:
            raise SystemExit("No seeds for {}".format(slug))
        have = {r["slug"] for r in rows}
        partials: list[dict[str, Any]] = []
        for place_slug, name_en, category, query in seeds:
            if place_slug in have:
                continue
            title = _STATIC_COMMONS_FILE.get(slug, {}).get(place_slug)
            if not title:
                title = _commons_search_title(query, pause=pause_search)
            if not title:
                raise SystemExit(
                    "Commons search found no raster for {} ({!r})".format(
                        place_slug,
                        query,
                    ),
                )
            partials.append(
                _generic_place_row(
                    place_slug,
                    name_en,
                    category,
                    address="See official visitor information.",
                    commons_file=title,
                ),
            )
        for p in partials:
            cf = p.get("commons_file")
            if cf and cf not in needed_files:
                needed_files.append(cf)
        work.append((slug, path, rows, partials))

    url_map: dict[str, str] = {}
    for i in range(0, len(needed_files), batch_size):
        batch = needed_files[i : i + batch_size]
        url_map.update(_batch_commons_urls(batch, pause_sec=batch_pause))

    for slug, path, rows, partials in work:
        have = {r["slug"] for r in rows}
        for raw in partials:
            fin = _finalize_row(dict(raw), url_map=url_map)
            if fin["slug"] in have:
                continue
            rows.append(fin)
            have.add(fin["slug"])
        if len(rows) < _MIN_PLACES:
            raise SystemExit(
                "{} still has only {} places".format(slug, len(rows)),
            )
        path.write_text(
            json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(slug, "->", len(rows), "places")


# --- Bootstrap packs (25 seeds each) for new Eastern European / Russian ---

def _pack(
    items: list[tuple[str, str, str, str]],
) -> list[tuple[str, str, str, str]]:
    if len(items) != 25:
        raise ValueError("expected 25 seeds, got {}".format(len(items)))
    return items


_BOOTSTRAP: dict[str, list[tuple[str, str, str, str]]] = {}

_BOOTSTRAP["minsk"] = _pack(
    [
        ("minsk_national_library", "National Library of Belarus", "libraries", "National Library of Belarus Minsk"),
        ("minsk_independence_square", "Independence Square", "public_space", "Independence Square Minsk"),
        ("minsk_red_church", "Church of Saints Simon and Helena", "places_of_worship", "Red Church Minsk"),
        ("minsk_gorky_park", "Gorky Park", "parks", "Gorky Park Minsk"),
        ("minsk_opera_ballet", "National Opera and Ballet", "theaters", "National Opera and Ballet Theatre Minsk"),
        ("minsk_trinity_hill", "Trinity Hill", "overview", "Trinity Hill Minsk Belarus"),
        ("minsk_island_tears", "Island of Tears", "landmarks", "Island of Tears Minsk"),
        ("minsk_national_art_museum", "National Art Museum", "museums", "National Art Museum Minsk"),
        ("minsk_victory_square", "Victory Square", "public_space", "Victory Square Minsk"),
        ("minsk_war_museum", "Great Patriotic War Museum", "museums", "Belarusian Great Patriotic War Museum Minsk"),
        ("minsk_chelyuskinites", "Chelyuskinites Park", "parks", "Chelyuskinites Park Minsk"),
        ("minsk_minsk_arena", "Minsk Arena", "theaters", "Minsk Arena"),
        ("minsk_october_square", "October Square", "public_space", "October Square Minsk"),
        ("minsk_yakub_kolas", "Yakub Kolas Square", "public_space", "Yakub Kolas Square Minsk"),
        ("minsk_palace_republic", "Palace of the Republic", "theaters", "Palace of the Republic Minsk"),
        ("minsk_belarusian_state_circus", "Belarusian State Circus", "theaters", "Belarusian State Circus Minsk"),
        ("minsk_city_gate", "Minsk triumphal arch", "landmarks", "Minsk triumphal arch"),
        ("minsk_holy_spirit_cathedral", "Holy Spirit Cathedral", "places_of_worship", "Holy Spirit Cathedral Minsk"),
        ("minsk_sts_peter_paul", "Church of Sts Peter and Paul", "places_of_worship", "Church of Saints Peter and Paul Minsk"),
        ("minsk_upper_town", "Upper Town Minsk", "overview", "Minsk Upper Town street"),
        ("minsk_kastrycnickaja", "October Street", "overview", "October Street Minsk"),
        ("minsk_belarus_station", "Minsk railway station", "railway_stations", "Minsk railway station"),
        ("minsk_drozdy", "Drozdy reservoir", "viewpoints", "Drozdy Minsk"),
        ("minsk_all_saints", "Church of All Saints", "places_of_worship", "Church of All Saints Minsk"),
        ("minsk_national_history", "Belarusian History Museum", "museums", "Belarusian history museum Minsk"),
    ],
)

_BOOTSTRAP["kyiv"] = _pack(
    [
        ("kyiv_saint_sophia", "Saint Sophia Cathedral", "places_of_worship", "Saint Sophia Cathedral Kyiv"),
        ("kyiv_pechersk_lavra", "Kyiv Pechersk Lavra", "places_of_worship", "Kyiv Pechersk Lavra"),
        ("kyiv_maidan", "Independence Square", "public_space", "Maidan Nezalezhnosti Kyiv"),
        ("kyiv_st_michael", "St Michael Golden Domed Monastery", "places_of_worship", "St Michaels Golden Domed Monastery Kyiv"),
        ("kyiv_motherland", "Motherland Monument", "landmarks", "Motherland Monument Kyiv"),
        ("kyiv_andrews_descent", "Andriyivskyy Descent", "overview", "Andriyivskyy Descent Kyiv"),
        ("kyiv_st_andrew_church", "St Andrews Church Kyiv", "places_of_worship", "Saint Andrews Church Kyiv"),
        ("kyiv_golden_gate", "Golden Gate", "landmarks", "Golden Gate Kyiv"),
        ("kyiv_mariinsky_palace", "Mariinsky Palace", "palaces", "Mariinsky Palace Kyiv"),
        ("kyiv_national_opera", "National Opera of Ukraine", "theaters", "National Opera House Kyiv"),
        ("kyiv_st_volodymyr_cathedral", "St Volodymyr Cathedral", "places_of_worship", "St Volodymyrs Cathedral Kyiv"),
        ("kyiv_st_nicholas", "St Nicholas Cathedral", "places_of_worship", "St Nicholas Cathedral Kyiv"),
        ("kyiv_house_chimeras", "House with Chimaeras", "landmarks", "House with Chimaeras Kyiv"),
        ("kyiv_national_museum", "National Art Museum of Ukraine", "museums", "National Art Museum of Ukraine Kyiv"),
        ("kyiv_mystetskyi", "Mystetskyi Arsenal", "museums", "Mystetskyi Arsenal Kyiv"),
        ("kyiv_podil", "Podil district", "overview", "Podil Kyiv street"),
        ("kyiv_contract_house", "Contract House", "landmarks", "Contract House Kyiv"),
        ("kyiv_sts_cyril_methodius", "St Cyrils Monastery", "places_of_worship", "Church of Saint Cyril Kyiv"),
        ("kyiv_hryshko_garden", "Hryshko National Botanical Garden", "parks", "Grishko botanical garden Kyiv"),
        ("kyiv_mariinsky_park", "Mariinsky Park", "parks", "Mariinsky Park Kyiv"),
        ("kyiv_bridge_klitschko", "Glass Bridge Kyiv", "bridges", "Klitschko Pedestrian Bridge Kyiv"),
        ("kyiv_lavra_bell_tower", "Great Lavra Bell Tower", "landmarks", "Great Lavra Bell Tower Kyiv"),
        ("kyiv_one_street_museum", "One Street Museum", "museums", "One Street Museum Kyiv"),
        ("kyiv_bessarabka", "Bessarabsky Market", "markets", "Bessarabsky Market Kyiv"),
        ("kyiv_pechersk_district", "Pechersk government quarter", "overview", "Pechersk Kyiv buildings"),
    ],
)

_BOOTSTRAP["odessa"] = _pack(
    [
        ("odessa_potemkin_stairs", "Potemkin Stairs", "landmarks", "Potemkin Stairs Odessa"),
        ("odessa_opera_theatre", "Odessa Opera and Ballet Theater", "theaters", "Odessa Opera and Ballet Theater"),
        ("odessa_deribasovskaya", "Deribasovskaya Street", "overview", "Deribasovskaya Street Odessa"),
        ("odessa_city_hall", "Odessa City Hall", "landmarks", "Odessa City Hall"),
        ("odessa_passage", "Odessa Passage", "markets", "Odessa Passage"),
        ("odessa_transfiguration_cathedral", "Transfiguration Cathedral", "places_of_worship", "Transfiguration Cathedral Odessa"),
        ("odessa_spaso_preobrazhensky", "Saviour Transfiguration Cathedral", "places_of_worship", "Orthodox cathedral Odessa Ukraine"),
        ("odessa_vorontsov_palace", "Vorontsov Palace", "palaces", "Vorontsov Palace Odessa"),
        ("odessa_lanzheron_beach", "Lanzheron Beach", "overview", "Lanzheron beach Odessa"),
        ("odessa_archeology_museum", "Odessa Archaeology Museum", "museums", "Odessa Archaeological Museum"),
        ("odessa_fine_arts_museum", "Odessa Fine Arts Museum", "museums", "Odessa Museum of Western and Eastern Art"),
        ("odessa_mother_in_law_bridge", "Mother-in-law Bridge", "bridges", "Mother-in-law bridge Odessa"),
        ("odessa_shah_palace", "Shah Palace Odessa", "palaces", "Shah Palace Odessa"),
        ("odessa_prymorsky_boulevard", "Primorsky Boulevard", "public_space", "Primorsky Boulevard Odessa"),
        ("odessa_port", "Odessa Sea Port", "overview", "Port of Odessa"),
        ("odessa_shevchenko_park", "Shevchenko Park Odessa", "parks", "Shevchenko Park Odessa"),
        ("odessa_odessa_catacombs", "Museum of Partisan Glory", "museums", "Odessa Catacombs museum"),
        ("odessa_st_paul_cathedral", "St Pauls Lutheran Cathedral", "places_of_worship", "Lutheran church Odessa"),
        ("odessa_bristol_hotel", "Bristol Hotel Odessa", "landmarks", "Bristol Hotel Odessa"),
        ("odessa_french_boulevard", "French Boulevard Odessa", "overview", "French Boulevard Odessa"),
        ("odessa_odessa_film_studio", "Odessa Film Studio", "landmarks", "Odessa Film Studio"),
        ("odessa_green_theatre", "Green Theatre Odessa", "theaters", "Green Theatre Odessa"),
        ("odessa_richelieu", "Duke de Richelieu monument", "sculptures", "Duke de Richelieu monument Odessa"),
        ("odessa_museum_western_eastern", "Museum of Western and Eastern Art", "museums", "Odessa Museum of Western and Eastern Art"),
        ("odessa_black_sea_coast", "Odessa Gulf coast", "viewpoints", "Black Sea coast Odessa"),
    ],
)

_BOOTSTRAP["lviv"] = _pack(
    [
        ("lviv_rynok_square", "Rynok Square", "public_space", "Market Square Lviv"),
        ("lviv_latin_cathedral", "Latin Cathedral", "places_of_worship", "Latin cathedral Lviv"),
        ("lviv_armenian_cathedral", "Armenian Cathedral", "places_of_worship", "Armenian Cathedral Lviv"),
        ("lviv_boitsov", "Boim Chapel", "places_of_worship", "Boim Chapel Lviv"),
        ("lviv_opera_house", "Lviv Opera House", "theaters", "Lviv Theatre of Opera and Ballet"),
        ("lviv_high_castle", "High Castle Hill", "viewpoints", "High Castle Lviv"),
        ("lviv_bernardine_church", "Bernardine church", "places_of_worship", "Bernardine church Lviv"),
        ("lviv_dominican_church", "Dominican church Lviv", "places_of_worship", "Dominican church Lviv"),
        ("lviv_st_george_cathedral", "St Georges Cathedral", "places_of_worship", "Cathedral of Saint George Lviv"),
        ("lviv_potocki_palace", "Potocki Palace", "palaces", "Potocki Palace Lviv"),
        ("lviv_italian_courtyard", "Italian Courtyard", "landmarks", "Italian courtyard Lviv"),
        ("lviv_pharmacy_museum", "Pharmacy Museum", "museums", "Pharmacy Museum Under the Black Eagle Lviv"),
        ("lviv_arsenal_museum", "Arsenal Museum", "museums", "Arsenal Museum Lviv"),
        ("lviv_brewery_museum", "Beer brewing museum Lviv", "museums", "Lvivarnya museum"),
        ("lviv_jewish_hospital", "Golden Rose synagogue area", "places_of_worship", "Golden Rose Synagogue Lviv"),
        ("lviv_basilian_monastery", "Basilian monastery", "places_of_worship", "Basilian monastery Lviv"),
        ("lviv_lychakiv_cemetery", "Lychakiv Cemetery", "cemeteries", "Lychakiv Cemetery"),
        ("lviv_stryi_park", "Stryi Park", "parks", "Stryi Park Lviv"),
        ("lviv_ivan_franko_university", "University of Lviv main", "landmarks", "University of Lviv building"),
        ("lviv_bandinelli_palace", "Bandinelli Palace", "palaces", "Bandinelli Palace Lviv"),
        ("lviv_korniakt_tower", "Korniakt Tower", "landmarks", "Korniakt Tower Lviv"),
        ("lviv_dormition_church", "Dormition Church", "places_of_worship", "Church of the Assumption Lviv"),
        ("lviv_solomiya_krushelnytska", "Solomiya Krushelnytska Lviv Opera", "theaters", "Lviv opera house facade"),
        ("lviv_ploshcha_mickiewicz", "Mickiewicz Square", "public_space", "Mickiewicz Square Lviv"),
        ("lviv_villa_biennale", "Palace of Culture Lviv", "theaters", "Palace of Culture Lviv"),
    ],
)

_BOOTSTRAP["chernivtsi"] = _pack(
    [
        ("chernivtsi_university", "Chernivtsi University Residence", "palaces", "Chernivtsi University UNESCO"),
        ("chernivtsi_theatre", "Chernivtsi Drama Theatre", "theaters", "Chernivtsi Theatre"),
        ("chernivtsi_town_hall", "Town Hall Chernivtsi", "landmarks", "Chernivtsi town hall"),
        ("chernivtsi_olha_kobylianska", "Olha Kobylianska Street", "overview", "Olha Kobylianska street Chernivtsi"),
        ("chernivtsi_st_nicholas", "St Nicholas Church", "places_of_worship", "Saint Nicholas Church Chernivtsi"),
        ("chernivtsi_st_onesimus", "Church of St Onuphrius", "places_of_worship", "Wooden church Chernivtsi Ukraine"),
        ("chernivtsi_romanian_orthodox", "Cathedral of the Holy Spirit", "places_of_worship", "Cathedral Holy Spirit Chernivtsi"),
        ("chernivtsi_central_square", "Central Square", "public_space", "Central Square Chernivtsi"),
        ("chernivtsi_music_drama", "Bukovinian Music Drama Theatre", "theaters", "Music drama theatre Chernivtsi"),
        ("chernivtsi_shevchenko_monument", "Shevchenko monument", "sculptures", "Taras Shevchenko monument Chernivtsi"),
        ("chernivtsi_public_library", "Chernivtsi Regional Library", "libraries", "Chernivtsi library building"),
        ("chernivtsi_train_station", "Chernivtsi railway station", "railway_stations", "Chernivtsi railway station"),
        ("chernivtsi_park_popa", "Popa Park", "parks", "Central park Chernivtsi"),
        ("chernivtsi_jewish_cemetery", "Jewish cemetery Chernivtsi", "cemeteries", "Jewish cemetery Chernivtsi"),
        ("chernivtsi_armenian_church", "Armenian church Chernivtsi", "places_of_worship", "Armenian church Chernivtsi"),
        ("chernivtsi_polish_church", "Polish church Chernivtsi", "places_of_worship", "Polish church Chernivtsi"),
        ("chernivtsi_assumption_church", "Church of the Assumption", "places_of_worship", "Church of the Assumption Chernivtsi"),
        ("chernivtsi_regional_museum", "Bukovinian Museum", "museums", "Bukovinian Museum Chernivtsi"),
        ("chernivtsi_art_museum", "Chernivtsi Art Museum", "museums", "Art museum Chernivtsi"),
        ("chernivtsi_synagogue_tempel", "Temple Synagogue Chernivtsi", "places_of_worship", "Temple Synagogue Chernivtsi"),
        ("chernivtsi_historical_museum", "Chernivtsi regional lore exhibits", "museums", "Chernivtsi museum building"),
        ("chernivtsi_bridge", "Pedestrian bridge over Prut", "bridges", "Bridge Prut river Chernivtsi"),
        ("chernivtsi_villa", "Villa of Justice", "landmarks", "Justice building Chernivtsi"),
        ("chernivtsi_market", "Musical fountain square", "landmarks", "Fountain Chernivtsi theatre"),
        ("chernivtsi_unesco_gate", "University gate Chernivtsi", "landmarks", "Chernivtsi University gate"),
    ],
)

_BOOTSTRAP["kharkiv"] = _pack(
    [
        ("kharkiv_freedom_square", "Freedom Square", "public_space", "Freedom Square Kharkiv"),
        ("kharkiv_derzhprom", "Derzhprom building", "landmarks", "Derzhprom Kharkiv"),
        ("kharkiv_annunciation_cathedral", "Annunciation Cathedral", "places_of_worship", "Annunciation Cathedral Kharkiv"),
        ("kharkiv_assumption_cathedral", "Dormition Cathedral", "places_of_worship", "Dormition Cathedral Kharkiv"),
        ("kharkiv_pokrovsky_monastery", "Pokrovsky Monastery", "places_of_worship", "Pokrovsky Monastery Kharkiv"),
        ("kharkiv_mirror_stream", "Mirror Stream fountain", "landmarks", "Mirror Stream Kharkiv"),
        ("kharkiv_gorky_park", "Gorky Park Kharkiv", "parks", "Maxim Gorky Park Kharkiv"),
        ("kharkiv_botanical_garden", "Kharkiv Botanical Garden", "parks", "Kharkiv botanical garden"),
        ("kharkiv_art_museum", "Kharkiv Art Museum", "museums", "Kharkiv Art Museum"),
        ("kharkiv_history_museum", "Kharkiv History Museum", "museums", "Kharkiv historical museum"),
        ("kharkiv_opera", "Kharkiv Opera House", "theaters", "Kharkiv Opera and Ballet Theatre"),
        ("kharkiv_university_yellow_building", "V. N. Karazin University main", "landmarks", "Karazin University main building"),
        ("kharkiv_pushkinskaya", "Pushkinskaya Street", "overview", "Pushkinskaya street Kharkiv"),
        ("kharkiv_sumskaya", "Sumska Street", "overview", "Sumska street Kharkiv"),
        ("kharkiv_blagoveshchensky", "Kharkiv circus", "theaters", "Kharkiv circus building"),
        ("kharkiv_barabashov", "Barabashov market", "markets", "Barabashovo market Kharkiv"),
        ("kharkiv_zoo", "Kharkiv Zoo", "parks", "Kharkiv Zoo"),
        ("kharkiv_steel_rollers", "Metalist Stadium", "landmarks", "Metalist Stadium Kharkiv"),
        ("kharkiv_polytechnic", "Kharkiv Polytechnic Institute", "landmarks", "Kharkiv Polytechnic Institute building"),
        ("kharkiv_lopan_river", "Lopan river embankment", "overview", "Lopan river Kharkiv"),
        ("kharkiv_constitution_square", "Constitution Square", "public_space", "Constitution Square Kharkiv"),
        ("kharkiv_young_guard", "Young Guard monument", "sculptures", "Young Guard monument Kharkiv"),
        ("kharkiv_synagogue", "Kharkiv Choral Synagogue", "places_of_worship", "Choral Synagogue Kharkiv"),
        ("kharkiv_railway_station", "Kharkiv railway station", "railway_stations", "Kharkiv railway station"),
        ("kharkiv_shevchenko_garden", "Shevchenko Garden", "parks", "Shevchenko Garden Kharkiv"),
    ],
)

_BOOTSTRAP["vladivostok"] = _pack(
    [
        ("vladivostok_golden_bridge", "Zolotoy Bridge", "bridges", "Zolotoy Rog Bridge Vladivostok"),
        ("vladivostok_russky_bridge", "Russky Bridge", "bridges", "Russky Bridge Vladivostok"),
        ("vladivostok_eagle_nest", "Eagle's Nest Hill", "viewpoints", "Eagles Nest hill Vladivostok"),
        ("vladivostok_train_station", "Vladivostok railway station", "railway_stations", "Vladivostok railway station"),
        ("vladivostok_submarine_c56", "C-56 Submarine Museum", "museums", "Submarine C-56 Vladivostok"),
        ("vladivostok_navy_cathedral", "Pacific Fleet Cathedral", "places_of_worship", "Orthodox church Vladivostok"),
        ("vladivostok_sportivnaya_harbour", "Sportivnaya Harbour", "overview", "Sportivnaya harbour Vladivostok"),
        ("vladivostok_arseniev_museum", "Arseniev State Museum", "museums", "Vladivostok museum building"),
        ("vladivostok_triumphal_arch", "Triumphal Arch", "landmarks", "Triumphal Arch Vladivostok"),
        ("vladivostok_korabelnaya_embankment", "Korabelnaya Embankment", "overview", "Korabelnaya embankment Vladivostok"),
        ("vladivostok_tokarevskiy", "Tokarevskiy Lighthouse", "landmarks", "Tokarevskiy lighthouse Vladivostok"),
        ("vladivostok_federal_university", "FEFU campus Russky Island", "landmarks", "Far Eastern Federal University Vladivostok"),
        ("vladivostok_svetlanskaya", "Svetlanskaya Street", "overview", "Svetlanskaya street Vladivostok"),
        ("vladivostok_nikolai_chapel", "Chapel of Saint Nicholas", "places_of_worship", "Lutheran church Vladivostok"),
        ("vladivostok_oceanarium", "Primorsky Oceanarium", "museums", "Primorsky Oceanarium Russky Island"),
        ("vladivostok_minny_gorodok", "Minny Gorodok fort", "landmarks", "Vladivostok fortress museum"),
        ("vladivostok_zolotoy_rog", "Zolotoy Rog bay", "viewpoints", "Zolotoy Rog Vladivostok"),
        ("vladivostok_central_square", "Central Square Vladivostok", "public_space", "Central Square Vladivostok"),
        ("vladivostok_millionka", "Millionka district", "overview", "Millionka Vladivostok"),
        ("vladivostok_orlinoe_gnezdo_view", "Observation deck Orlinoye", "viewpoints", "Orlinoye gnezdo Vladivostok"),
        ("vladivostok_borodinskaya", "Borodinskaya battery", "landmarks", "Voroshilov battery Vladivostok"),
        ("vladivostok_pokrovsky_park", "Pokrovsky Park", "parks", "Pokrovsky Park Vladivostok"),
        ("vladivostok_maritime_university", "Maritime State University", "landmarks", "Maritime University Vladivostok"),
        ("vladivostok_amursky_zaliv", "Amur Bay coast", "overview", "Amur Bay Vladivostok"),
        ("vladivostok_skala_park", "Seaside boardwalk", "parks", "Vladivostok park"),
    ],
)

_BOOTSTRAP["novosibirsk"] = _pack(
    [
        ("novosibirsk_opera_ballet", "Novosibirsk Opera and Ballet", "theaters", "Novosibirsk Opera and Ballet Theatre"),
        ("novosibirsk_lenin_square", "Lenin Square", "public_space", "Lenin Square Novosibirsk"),
        ("novosibirsk_akademgorodok", "Akademgorodok", "overview", "Akademgorodok Novosibirsk"),
        ("novosibirsk_zoo", "Novosibirsk Zoo", "parks", "Novosibirsk Zoo"),
        ("novosibirsk_art_museum", "Novosibirsk State Art Museum", "museums", "Novosibirsk Art Museum"),
        ("novosibirsk_local_lore", "Novosibirsk State Museum", "museums", "Novosibirsk State Museum of Local Lore"),
        ("novosibirsk_chapel_nicholas", "Chapel of Saint Nicholas", "places_of_worship", "Chapel Saint Nicholas Novosibirsk"),
        ("novosibirsk_alexander_nevsky", "Alexander Nevsky Cathedral", "places_of_worship", "Alexander Nevsky Cathedral Novosibirsk"),
        ("novosibirsk_transfiguration", "Church of the Transfiguration", "places_of_worship", "Transfiguration Cathedral Novosibirsk"),
        ("novosibirsk_ob_river", "Ob River embankment", "overview", "Ob river embankment Novosibirsk"),
        ("novosibirsk_mikhailovskaya", "Mikhailovskaya embankment", "public_space", "Mikhailovskaya embankment Novosibirsk"),
        ("novosibirsk_budker_institute", "Budker Institute", "landmarks", "Budker Institute of Nuclear Physics"),
        ("novosibirsk_globus", "Globus shopping centre", "markets", "Globus Novosibirsk"),
        ("novosibirsk_railway_station", "Novosibirsk Glavny railway station", "railway_stations", "Novosibirsk railway station"),
        ("novosibirsk_expo_centre", "Novosibirsk Expo Centre", "overview", "Expocentre Novosibirsk"),
        ("novosibirsk_pervomaysky", "Pervomaysky Park", "parks", "Pervomaysky Park Novosibirsk"),
        ("novosibirsk_central_park", "Central Park Novosibirsk", "parks", "Central Park Novosibirsk"),
        ("novosibirsk_studencheskaya", "Studencheskaya embankment", "overview", "Studencheskaya Novosibirsk"),
        ("novosibirsk_business_centre", "Ob River monument", "landmarks", "Ob river monument Novosibirsk"),
        ("novosibirsk_planetarium", "Novosibirsk Planetarium", "museums", "Novosibirsk Planetarium"),
        ("novosibirsk_botanical_garden", "Central Siberian Botanical Garden", "parks", "Central Siberian Botanical Garden"),
        ("novosibirsk_technopark", "Academpark", "overview", "Akademgorodok Novosibirsk institute"),
        ("novosibirsk_metro_bridge", "Metro bridge Ob", "bridges", "Novosibirsk metro bridge"),
        ("novosibirsk_krasny_avenue", "Krasny Avenue", "overview", "Krasny Avenue Novosibirsk"),
        ("novosibirsk_siberia_hotel", "Marriott Siberia tower", "landmarks", "Marriott Novosibirsk"),
    ],
)

_BOOTSTRAP["tver"] = _pack(
    [
        ("tver_travel_palace", "Travel Palace", "palaces", "Travel Palace Tver"),
        ("tver_white_trinity", "White Trinity Church", "places_of_worship", "White Trinity Church Tver"),
        ("tver_resurrection_cathedral", "Resurrection Cathedral", "places_of_worship", "Resurrection Cathedral Tver"),
        ("tver_river_station", "Tver river station", "landmarks", "Tver river station Volga"),
        ("tver_st_catherine", "Saint Catherine Church", "places_of_worship", "Orthodox church Tver Russia"),
        ("tver_afanasy_nikitin", "Afanasy Nikitin monument", "sculptures", "Afanasy Nikitin monument Tver"),
        ("tver_trekhsvyatskaya", "Trekhsvyatskaya Street", "overview", "Trekhsvyatskaya street Tver"),
        ("tver_river_volga_embankment", "Volga embankment Tver", "public_space", "Volga embankment Tver"),
        ("tver_regional_art_museum", "Tver Regional Art Gallery", "museums", "Tver Art Gallery"),
        ("tver_local_lore_museum", "Tver Regional Museum", "museums", "Tver regional museum"),
        ("tver_michael_garden", "City Garden Tver", "parks", "City garden Tver"),
        ("tver_railway_station", "Tver railway station", "railway_stations", "Tver railway station"),
        ("tver_saint_michael", "Saint Michael Church", "places_of_worship", "Church of Michael Tver"),
        ("tver_borisoglebsky", "Borisoglebsky Monastery", "places_of_worship", "Borisoglebsky monastery Tver"),
        ("tver_otechestvo", "Tver drama theatre", "theaters", "Tver drama theatre"),
        ("tver_steamboat_rex", "Old Volga steamship museum", "museums", "River museum Tver"),
        ("tver_yard", "Tver Carriage Yard", "landmarks", "Tver Yamskaya street"),
        ("tver_puppet_theatre", "Tver Puppet Theatre", "theaters", "Tver puppet theatre"),
        ("tver_pushkin_statue", "Pushkin monument Tver", "sculptures", "Pushkin monument Tver"),
        ("tver_soviet_square", "Soviet Square Tver", "public_space", "Soviet Square Tver"),
        ("tver_smolensky_cathedral", "Smolensk Cathedral", "places_of_worship", "Smolensky cathedral Tver"),
        ("tver_museum_life", "Museum of Tver life", "museums", "Museum of Tver life"),
        ("tver_bridge_volga", "Old Volga bridge", "bridges", "Volga bridge Tver"),
        ("tver_fire_tower", "Fire observation tower", "landmarks", "Fire tower Tver"),
        ("tver_university", "Tver State University", "landmarks", "Tver State University building"),
    ],
)

_BOOTSTRAP["yaroslavl"] = _pack(
    [
        ("yaroslavl_assumption_cathedral", "Assumption Cathedral", "places_of_worship", "Assumption Cathedral Yaroslavl"),
        ("yaroslavl_st_elijah", "Church of Elijah the Prophet", "places_of_worship", "Church of Elijah the Prophet Yaroslavl"),
        ("yaroslavl_volga_embankment", "Volga embankment", "public_space", "Volga embankment Yaroslavl"),
        ("yaroslavl_strelka", "Strelka park", "parks", "Strelka Yaroslavl Volga Kotorosl"),
        ("yaroslavl_spassky_monastery", "Spassky Monastery", "places_of_worship", "Spassky Monastery Yaroslavl"),
        ("yaroslavl_transfiguration_monastery", "Transfiguration Monastery", "places_of_worship", "Transfiguration Monastery Yaroslavl"),
        ("yaroslavl_meteorological_tower", "Yaroslavl tower museum", "museums", "Yaroslavl tower"),
        ("yaroslavl_museum_reserve", "Yaroslavl Museum-Reserve", "museums", "Yaroslavl museum reserve"),
        ("yaroslavl_volkov_theatre", "Volkov Theatre", "theaters", "Volkov Theatre Yaroslavl"),
        ("yaroslavl_university", "Demidov pillar Yaroslavl State University", "landmarks", "Yaroslavl State University"),
        ("yaroslavl_kremlin", "Yaroslavl Kremlin", "landmarks", "Yaroslavl Kremlin"),
        ("yaroslavl_fedorovskiy", "Church of Fedorovskaya Icon", "places_of_worship", "Church of Archangel Michael Yaroslavl"),
        ("yaroslavl_ring_street", "Ring Boulevard", "overview", "Ring street Yaroslavl"),
        ("yaroslavl_pereslavl_gate", "Znamenskaya Tower", "landmarks", "Znamenskaya tower Yaroslavl"),
        ("yaroslavl_art_museum", "Yaroslavl Art Museum", "museums", "Yaroslavl Art Museum"),
        ("yaroslavl_planetarium", "Yaroslavl Planetarium", "museums", "Yaroslavl Planetarium"),
        ("yaroslavl_bear_intersection", "Bear monument", "sculptures", "Yaroslavl city coat of arms bear"),
        ("yaroslavl_demidov_pillar", "Demidovsky Pillar", "landmarks", "Demidov pillar Yaroslavl"),
        ("yaroslavl_railway_station", "Yaroslavl railway station", "railway_stations", "Yaroslavl railway station"),
        ("yaroslavl_tolga_monastery", "Tolga Monastery", "places_of_worship", "Tolga Monastery Yaroslavl"),
        ("yaroslavl_korovniky", "Korovniki churches", "places_of_worship", "Church of John Chrysostom Yaroslavl"),
        ("yaroslavl_mashinostroiteley", "Victory park Yaroslavl", "parks", "Victory park Yaroslavl"),
        ("yaroslavl_red_square", "Red Square Yaroslavl", "public_space", "Red Square Yaroslavl"),
        ("yaroslavl_volga_bridge", "Oktyabrsky bridge", "bridges", "Oktyabrsky bridge Yaroslavl"),
        ("yaroslavl_motor_ship_museum", "River ship museum", "museums", "River museum Yaroslavl"),
    ],
)


def _bootstrap_city(
    slug: str,
    *,
    pause_search: float,
    batch_size: int,
    batch_pause: float,
) -> None:
    seeds = _BOOTSTRAP.get(slug)
    if not seeds:
        raise SystemExit("Unknown bootstrap slug {!r}".format(slug))
    city_root = _PROJECT_ROOT / slug
    data_dir = city_root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    path = data_dir / "{}_places.json".format(slug)
    if path.is_file():
        rows = json.loads(path.read_text(encoding="utf-8"))
        if len(rows) >= _MIN_PLACES:
            print(
                slug,
                "skip bootstrap (already",
                len(rows),
                "places)",
            )
            return
    else:
        rows = []
    have = {r["slug"] for r in rows}
    partials: list[dict[str, Any]] = []
    needed_files: list[str] = []
    for place_slug, name_en, category, query in seeds:
        if place_slug in have:
            continue
        title = _STATIC_COMMONS_FILE.get(slug, {}).get(place_slug)
        if not title:
            title = _commons_search_title(query, pause=pause_search)
        if not title:
            raise SystemExit(
                "Commons search found no raster for {} ({!r})".format(
                    place_slug,
                    query,
                ),
            )
        partials.append(
            _generic_place_row(
                place_slug,
                name_en,
                category,
                address="See official visitor information.",
                commons_file=title,
            ),
        )
    for p in partials:
        cf = p.get("commons_file")
        if cf and cf not in needed_files:
            needed_files.append(cf)
    url_map: dict[str, str] = {}
    for i in range(0, len(needed_files), batch_size):
        batch = needed_files[i : i + batch_size]
        url_map.update(_batch_commons_urls(batch, pause_sec=batch_pause))
    for raw in partials:
        fin = _finalize_row(dict(raw), url_map=url_map)
        if fin["slug"] in have:
            continue
        rows.append(fin)
        have.add(fin["slug"])
    if len(rows) < _MIN_PLACES:
        raise SystemExit(
            "{} has only {} places".format(slug, len(rows)),
        )
    path.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(slug, "bootstrap ->", len(rows), "places at", path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pause-search",
        type=float,
        default=1.85,
        help=(
            "seconds between Commons search API calls "
            "(default 1.85; raise if you hit HTTP 429)"
        ),
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=5,
        help="titles per imageinfo batch (default 5)",
    )
    parser.add_argument(
        "--batch-pause",
        type=float,
        default=3.5,
        help="seconds after each imageinfo batch (default 3.5)",
    )
    parser.add_argument(
        "--bootstrap",
        nargs="*",
        default=[],
        metavar="SLUG",
        help="bootstrap these cities to 25 places (after grow unless --no-grow)",
    )
    parser.add_argument(
        "--no-grow",
        action="store_true",
        help="skip growing the 14 legacy guides (bootstrap only)",
    )
    args = parser.parse_args()

    if not args.no_grow:
        _grow_existing(
            pause_search=args.pause_search,
            batch_size=args.batch_size,
            batch_pause=args.batch_pause,
        )
    for slug in args.bootstrap:
        _bootstrap_city(
            slug,
            pause_search=args.pause_search,
            batch_size=args.batch_size,
            batch_pause=args.batch_pause,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
