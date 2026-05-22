# -*- coding: utf-8 -*-
"""Extra place seeds to reach 30 curated rows per city (historic / religious bias)."""

from __future__ import annotations

# (slug, name_en, category, commons_search_query)
EXTRA_SEEDS: dict[str, list[tuple[str, str, str, str]]] = {}

# --- Legacy 12-place packs: +5 each (12 + 13 existing + 5 = 30) ---

EXTRA_SEEDS["amsterdam"] = [
    ("amsterdam_oude_kerk", "Oude Kerk", "places_of_worship", "Oude Kerk Amsterdam"),
    ("amsterdam_nieuwe_kerk", "Nieuwe Kerk", "places_of_worship", "Nieuwe Kerk Amsterdam Dam"),
    ("amsterdam_westerkerk", "Westerkerk", "places_of_worship", "Westerkerk Amsterdam"),
    ("amsterdam_national_monument", "National Monument", "memorials", "National Monument Amsterdam Dam"),
    ("amsterdam_museum_het_schip", "Museum Het Schip", "museums", "Het Schip Amsterdam school"),
]

EXTRA_SEEDS["athens"] = [
    ("athens_panagia_kapnikarea", "Church of Panagia Kapnikarea", "places_of_worship", "Kapnikarea church Athens"),
    ("athens_tower_winds", "Tower of the Winds", "landmarks", "Tower of the Winds Athens Agora"),
    ("athens_monastiraki", "Monastiraki Square", "public_space", "Monastiraki square Athens"),
    ("athens_panathenaic", "Panathenaic Stadium", "landmarks", "Panathenaic Stadium Athens"),
    ("athens_ancient_agora_temple", "Temple of Hephaestus", "places_of_worship", "Temple Hephaestus Athens Agora"),
]

EXTRA_SEEDS["bangkok"] = [
    ("bangkok_wat_arun", "Wat Arun", "places_of_worship", "Wat Arun Bangkok"),
    ("bangkok_wat_suthat", "Wat Suthat", "places_of_worship", "Wat Suthat Bangkok Giant Swing"),
    ("bangkok_wat_benchamabophit", "Wat Benchamabophit", "places_of_worship", "Marble Temple Bangkok"),
    ("bangkok_grand_palace", "Grand Palace", "palaces", "Grand Palace Bangkok"),
    ("bangkok_ananta_samakhom", "Ananta Samakhom Throne Hall", "landmarks", "Ananta Samakhom Throne Hall Bangkok"),
]

EXTRA_SEEDS["copenhagen"] = [
    ("copenhagen_frederiks_kirke", "Frederik's Church", "places_of_worship", "Frederiks Kirke Copenhagen"),
    ("copenhagen_church_holmen", "Church of Holmen", "places_of_worship", "Church of Holmen Copenhagen"),
    ("copenhagen_grundtvigs", "Grundtvig's Church", "places_of_worship", "Grundtvigs Church Copenhagen"),
    ("copenhagen_amalienborg", "Amalienborg Palace", "palaces", "Amalienborg Palace Copenhagen"),
    ("copenhagen_church_trinitatis", "Trinitatis Church", "places_of_worship", "Trinitatis Church Copenhagen Round Tower"),
]

EXTRA_SEEDS["dublin"] = [
    ("dublin_christ_church", "Christ Church Cathedral", "places_of_worship", "Christ Church Cathedral Dublin"),
    ("dublin_st_patricks", "St Patrick's Cathedral", "places_of_worship", "St Patricks Cathedral Dublin"),
    ("dublin_castle", "Dublin Castle", "landmarks", "Dublin Castle"),
    ("dublin_glasnevin", "Glasnevin Cemetery", "cemeteries", "Glasnevin Cemetery Dublin"),
    ("dublin_book_of_kells", "Trinity College Library", "libraries", "Trinity College Library Dublin Long Room"),
]

EXTRA_SEEDS["dubai"] = [
    ("dubai_grand_mosque", "Grand Mosque Dubai", "places_of_worship", "Grand Mosque Dubai"),
    ("dubai_al_fahidi", "Al Fahidi Historical District", "overview", "Al Fahidi Dubai heritage"),
    ("dubai_etihad_museum", "Etihad Museum", "museums", "Etihad Museum Dubai"),
    ("dubai_heritage_village", "Hatta Heritage Village", "museums", "Hatta heritage village UAE"),
    ("dubai_qasr_al_hosn", "Qasr Al Hosn", "landmarks", "Qasr Al Hosn Abu Dhabi fort"),
]

EXTRA_SEEDS["istanbul"] = [
    ("istanbul_suleymaniye", "Süleymaniye Mosque", "places_of_worship", "Suleymaniye Mosque Istanbul"),
    ("istanbul_chora", "Chora Church museum", "places_of_worship", "Chora Church Istanbul mosaic"),
    ("istanbul_fatih_mosque", "Fatih Mosque", "places_of_worship", "Fatih Mosque Istanbul"),
    ("istanbul_eyup_sultan", "Eyüp Sultan Mosque", "places_of_worship", "Eyup Sultan Mosque Istanbul"),
    ("istanbul_valens_aqueduct", "Valens Aqueduct", "landmarks", "Valens Aqueduct Istanbul"),
]

EXTRA_SEEDS["lisbon"] = [
    ("lisbon_jeronimos", "Jerónimos Monastery", "places_of_worship", "Jeronimos Monastery Lisbon"),
    ("lisbon_se_cathedral", "Lisbon Cathedral", "places_of_worship", "Lisbon Cathedral Se"),
    ("lisbon_carmo_ruins", "Carmo Convent ruins", "places_of_worship", "Carmo Convent ruins Lisbon"),
    ("lisbon_sao_vicente", "São Vicente de Fora", "places_of_worship", "Sao Vicente de Fora Lisbon"),
    ("lisbon_national_pantheon", "National Pantheon", "places_of_worship", "National Pantheon Lisbon"),
]

EXTRA_SEEDS["london"] = [
    ("london_westminster_abbey", "Westminster Abbey", "places_of_worship", "Westminster Abbey London"),
    ("london_st_pauls", "St Paul's Cathedral", "places_of_worship", "St Pauls Cathedral London"),
    ("london_tower_of_london", "Tower of London", "landmarks", "Tower of London White Tower"),
    ("london_british_museum", "British Museum", "museums", "British Museum London Great Court"),
    ("london_houses_of_parliament", "Palace of Westminster", "landmarks", "Palace of Westminster London"),
]

EXTRA_SEEDS["los_angeles"] = [
    ("los_angeles_cathedral_our_lady", "Cathedral of Our Lady of the Angels", "places_of_worship", "Cathedral of Our Lady of the Angels Los Angeles"),
    ("los_angeles_mission_san_gabriel", "Mission San Gabriel", "places_of_worship", "Mission San Gabriel Arcangel"),
    ("los_angeles_getty_center", "Getty Center", "museums", "Getty Center Los Angeles"),
    ("los_angeles_hollywood_sign", "Hollywood Sign", "landmarks", "Hollywood Sign view"),
    ("los_angeles_griffith_observatory", "Griffith Observatory", "landmarks", "Griffith Observatory Los Angeles"),
]

EXTRA_SEEDS["san_francisco"] = [
    ("san_francisco_mission_dolores", "Mission San Francisco de Asís", "places_of_worship", "Mission Dolores San Francisco"),
    ("san_francisco_grace_cathedral", "Grace Cathedral", "places_of_worship", "Grace Cathedral San Francisco"),
    ("san_francisco_presidio", "Presidio of San Francisco", "landmarks", "Presidio San Francisco Golden Gate"),
    ("san_francisco_coit_tower", "Coit Tower", "landmarks", "Coit Tower San Francisco"),
    ("san_francisco_asian_art", "Asian Art Museum", "museums", "Asian Art Museum San Francisco"),
]

EXTRA_SEEDS["singapore"] = [
    ("singapore_sultan_mosque", "Sultan Mosque", "places_of_worship", "Sultan Mosque Singapore Kampong Glam"),
    ("singapore_thian_hock_keng", "Thian Hock Keng Temple", "places_of_worship", "Thian Hock Keng temple Singapore"),
    ("singapore_st_andrews", "St Andrew's Cathedral", "places_of_worship", "St Andrews Cathedral Singapore"),
    ("singapore_fort_canning", "Fort Canning Park", "landmarks", "Fort Canning Singapore"),
    ("singapore_national_gallery", "National Gallery Singapore", "museums", "National Gallery Singapore"),
]

EXTRA_SEEDS["tokyo"] = [
    ("tokyo_sensoji", "Sensō-ji", "places_of_worship", "Sensoji temple Asakusa Tokyo"),
    ("tokyo_meiji_shrine", "Meiji Shrine", "places_of_worship", "Meiji Shrine Tokyo"),
    ("tokyo_zojoji", "Zōjō-ji Temple", "places_of_worship", "Zojoji temple Tokyo"),
    ("tokyo_nezu_shrine", "Nezu Shrine", "places_of_worship", "Nezu Shrine Tokyo"),
    ("tokyo_imperial_palace", "Imperial Palace East Gardens", "landmarks", "Imperial Palace East Gardens Tokyo"),
]

EXTRA_SEEDS["vatican"] = [
    ("vatican_st_peters_square", "St Peter's Square", "public_space", "St Peters Square Vatican"),
    ("vatican_sistine_chapel", "Sistine Chapel", "places_of_worship", "Sistine Chapel Vatican"),
    ("vatican_vatican_museums", "Vatican Museums", "museums", "Vatican Museums spiral staircase"),
    ("vatican_castel_sant_angelo", "Castel Sant'Angelo", "landmarks", "Castel Sant Angelo Rome"),
    ("vatican_papal_archbasilica", "Archbasilica of St John Lateran", "places_of_worship", "Archbasilica of Saint John Lateran Rome"),
]

# --- Eastern / Russian packs at 25: +5 each ---

for _slug, _items in (
    ("chernivtsi", [
        ("chernivtsi_catholic_church", "Catholic Church of the Holy Cross", "places_of_worship", "Catholic church Chernivtsi"),
        ("chernivtsi_glory_monument", "Glory Memorial", "memorials", "Glory memorial Chernivtsi"),
        ("chernivtsi_prut_park", "Prut River park", "parks", "Prut river Chernivtsi"),
        ("chernivtsi_bukovyna_art", "Bukovyna Art Museum branch", "museums", "Bukovyna art Chernivtsi"),
        ("chernivtsi_paper_museum", "Paper Museum", "museums", "Paper museum Chernivtsi"),
    ]),
    ("kharkiv", [
        ("kharkiv_blagoveshchensky", "Annunciation Cathedral Kharkiv", "places_of_worship", "Annunciation Cathedral Kharkiv"),
        ("kharkiv_pokrovsky", "Pokrovsky Monastery", "places_of_worship", "Pokrovsky Monastery Kharkiv"),
        ("kharkiv_mirror_stream", "Mirror Stream fountain", "landmarks", "Mirror Stream Kharkiv"),
        ("kharkiv_dormition", "Dormition Cathedral Kharkiv", "places_of_worship", "Dormition Cathedral Kharkiv"),
        ("kharkiv_choral_synagogue", "Kharkiv Choral Synagogue", "places_of_worship", "Choral Synagogue Kharkiv"),
    ]),
    ("kyiv", [
        ("kyiv_st_florian", "St Florian Monastery", "places_of_worship", "St Florian Monastery Kyiv"),
        ("kyiv_st_alexander", "St Alexander Roman Catholic church", "places_of_worship", "St Alexander church Kyiv"),
        ("kyiv_sts_constantine", "St Constantine and Helena", "places_of_worship", "St Constantine church Kyiv"),
        ("kyiv_sts_boris_gleb", "St Boris and Gleb Monastery", "places_of_worship", "Vydubychi Monastery Kyiv"),
        ("kyiv_st_nicholas", "St Nicholas Roman Catholic Cathedral", "places_of_worship", "St Nicholas church Kyiv"),
    ]),
    ("lviv", [
        ("lviv_dominican_church", "Dominican church", "places_of_worship", "Dominican church Lviv"),
        ("lviv_bernardine", "Bernardine church", "places_of_worship", "Bernardine church Lviv"),
        ("lviv_carmelite", "Carmelite church", "places_of_worship", "Carmelite church Lviv"),
        ("lviv_st_george", "St George's Cathedral", "places_of_worship", "St Georges Cathedral Lviv"),
        ("lviv_jesuit_church", "Jesuit church Lviv", "places_of_worship", "Jesuit church Lviv"),
    ]),
    ("minsk", [
        ("minsk_st_elizabeth", "St Elizabeth Convent", "places_of_worship", "St Elizabeth Convent Minsk"),
        ("minsk_st_roch", "St Roch church", "places_of_worship", "St Roch church Minsk"),
        ("minsk_sts_simon_helena", "Red Church", "places_of_worship", "Church of Saints Simon and Helena Minsk"),
        ("minsk_catholic_cathedral", "Archcathedral of the Blessed Virgin Mary", "places_of_worship", "Catholic cathedral Minsk"),
        ("minsk_memorial_island", "Island of Tears", "memorials", "Island of Tears Minsk"),
    ]),
    ("novosibirsk", [
        ("novosibirsk_alexander_nevsky", "Alexander Nevsky Cathedral", "places_of_worship", "Alexander Nevsky Cathedral Novosibirsk"),
        ("novosibirsk_transfiguration", "Church of the Transfiguration", "places_of_worship", "Transfiguration church Novosibirsk"),
        ("novosibirsk_chapel_nicholas", "Chapel of Saint Nicholas", "places_of_worship", "Chapel Saint Nicholas Novosibirsk"),
        ("novosibirsk_opera", "Novosibirsk Opera and Ballet", "theaters", "Novosibirsk Opera Theatre"),
        ("novosibirsk_state_museum", "Novosibirsk State Museum", "museums", "Novosibirsk State Museum"),
    ]),
    ("odessa", [
        ("odessa_spaso_preobrazhensky", "Spaso-Preobrazhensky Cathedral", "places_of_worship", "Spaso Preobrazhensky Cathedral Odessa"),
        ("odessa_st_paul_lutheran", "St Paul Lutheran Cathedral", "places_of_worship", "Lutheran cathedral Odessa"),
        ("odessa_archeological_museum", "Odessa Archaeology Museum", "museums", "Odessa Archaeological Museum"),
        ("odessa_potemkin", "Potemkin Stairs", "landmarks", "Potemkin Stairs Odessa"),
        ("odessa_primorsky", "Primorsky Boulevard", "public_space", "Primorsky Boulevard Odessa"),
    ]),
    ("tver", [
        ("tver_white_trinity", "White Trinity Church", "places_of_worship", "White Trinity Church Tver"),
        ("tver_resurrection", "Resurrection Cathedral Tver", "places_of_worship", "Resurrection Cathedral Tver"),
        ("tver_borisoglebsky", "Borisoglebsky Monastery", "places_of_worship", "Borisoglebsky monastery Tver"),
        ("tver_smolensky", "Smolensk Cathedral Tver", "places_of_worship", "Smolensky cathedral Tver"),
        ("tver_travel_palace", "Travel Palace Tver", "palaces", "Travel Palace Tver"),
    ]),
    ("vladivostok", [
        ("vladivostok_pacific_fleet_cathedral", "Pacific Fleet Cathedral", "places_of_worship", "Pacific Fleet Cathedral Vladivostok"),
        ("vladivostok_chapel_nicholas", "Chapel of Saint Nicholas", "places_of_worship", "Chapel Saint Nicholas Vladivostok"),
        ("vladivostok_submarine_c56", "C-56 Submarine Museum", "museums", "C-56 submarine Vladivostok"),
        ("vladivostok_tokarevskiy", "Tokarevskiy Lighthouse", "landmarks", "Tokarevskiy lighthouse Vladivostok"),
        ("vladivostok_golden_bridge", "Zolotoy Bridge", "bridges", "Zolotoy Bridge Vladivostok"),
    ]),
    ("yaroslavl", [
        ("yaroslavl_assumption", "Assumption Cathedral Yaroslavl", "places_of_worship", "Assumption Cathedral Yaroslavl"),
        ("yaroslavl_st_elijah", "Church of Elijah the Prophet", "places_of_worship", "Church of Elijah the Prophet Yaroslavl"),
        ("yaroslavl_transfiguration", "Transfiguration Monastery", "places_of_worship", "Transfiguration Monastery Yaroslavl"),
        ("yaroslavl_tolga", "Tolga Monastery", "places_of_worship", "Tolga Monastery Yaroslavl"),
        ("yaroslavl_spassky", "Spassky Monastery", "places_of_worship", "Spassky Monastery Yaroslavl"),
    ]),
):
    EXTRA_SEEDS[_slug] = _items

# --- Small Russian guides ---

EXTRA_SEEDS["kazan"] = [
    ("kazan_temple_all_religions", "Temple of All Religions", "places_of_worship", "Temple of All Religions Kazan"),
    ("kazan_epiphany_cathedral", "Epiphany Cathedral Kazan", "places_of_worship", "Epiphany Cathedral Kazan"),
    ("kazan_nikolsky_cathedral", "Nikolsky Cathedral Kazan", "places_of_worship", "Nikolsky Cathedral Kazan"),
    ("kazan_mardzhani_museum", "Mardzhani Museum", "museums", "Mardzhani museum Kazan"),
    ("kazan_tatarstan_museum", "National Museum of Tatarstan", "museums", "National Museum Tatarstan Kazan"),
    ("kazan_kazan_icon", "Kazan Mother of God icon church", "places_of_worship", "Kazan Bogoroditsky monastery"),
    ("kazan_transfiguration", "Transfiguration Monastery Kazan", "places_of_worship", "Transfiguration monastery Kazan"),
    ("kazan_st_john_baptist", "St John the Baptist Church", "places_of_worship", "St John Baptist church Kazan"),
    ("kazan_muslim_board", "Qol Sharif museum", "museums", "Kul Sharif museum Kazan Kremlin"),
    ("kazan_syuyumbike_leans", "Söyembikä leaning tower", "landmarks", "Soyembika tower Kazan Kremlin"),
    ("kazan_riverside_kremlin", "Kremlin embankment Kazan", "public_space", "Kazan Kremlin embankment"),
    ("kazan_tukay_square", "Tukay Square", "public_space", "Tukay square Kazan"),
    ("kazan_chak_chak_museum", "Chak-Chak Museum", "museums", "Chak Chak museum Kazan"),
    ("kazan_university_main", "Kazan Federal University", "landmarks", "Kazan Federal University main building"),
    ("kazan_our_lady_kazan", "Church of Our Lady of Kazan", "places_of_worship", "Church Our Lady Kazan"),
    ("kazan_st_peter_paul_old", "Old Peter and Paul Cathedral", "places_of_worship", "Peter and Paul cathedral Kazan"),
    ("kazan_muslim_prayer", "Mardzhani Mosque", "places_of_worship", "Mardzhani mosque Kazan"),
    ("kazan_kremlin_wall_gate", "Kremlin Spasskaya Tower", "landmarks", "Spasskaya tower Kazan Kremlin"),
    ("kazan_volga_embankment", "Volga embankment Kazan", "public_space", "Volga river embankment Kazan"),
    ("kazan_family_center_view", "Kazan Family Center view", "landmarks", "Kazan Family Center cup"),
]

EXTRA_SEEDS["vologda"] = [
    ("vologda_st_sophia_cathedral", "Saint Sophia Cathedral Vologda", "places_of_worship", "Saint Sophia Cathedral Vologda"),
    ("vologda_dmitry_prilutsky", "Dmitry Prilutsky church", "places_of_worship", "Dmitry Prilutsky church Vologda"),
    ("vologda_st_dmitry", "St Dmitry church on Navolok", "places_of_worship", "St Dmitry church Vologda"),
    ("vologda_church_lazarus", "Church of St Lazarus", "places_of_worship", "Church St Lazarus Vologda"),
    ("vologda_house_of_peter", "House of Peter I", "museums", "House of Peter the Great Vologda"),
    ("vologda_regional_art", "Vologda Regional Art Gallery", "museums", "Vologda art gallery"),
    ("vologda_military_glory", "Museum of Military Glory", "museums", "Museum military glory Vologda"),
    ("vologda_convent_zosima", "Zosima and Savvatiy convent", "places_of_worship", "Zosima Savvatiy convent Vologda"),
    ("vologda_church_john", "Church of St John the Baptist", "places_of_worship", "Church John Baptist Vologda"),
    ("vologda_wonderworkers", "Cathedral of the Wonderworkers", "places_of_worship", "Cathedral Wonderworkers Vologda"),
    ("vologda_architectural_museum", "Architectural and Ethnographic Museum", "museums", "Architectural ethnographic museum Vologda"),
    ("vologda_obelisk", "Obelisk of Glory", "memorials", "Obelisk glory Vologda"),
    ("vologda_world_war_memorial", "Victory Square memorial", "memorials", "Victory square Vologda"),
    ("vologda_regional_museum", "Vologda State Museum", "museums", "Vologda state museum"),
    ("vologda_church_kazan", "Kazan church Vologda", "places_of_worship", "Kazan church Vologda"),
    ("vologda_st_basil", "St Basil church", "places_of_worship", "St Basil church Vologda"),
    ("vologda_museum_economy", "Museum of Economy", "museums", "Museum economy Vologda"),
    ("vologda_gallery_artists", "Artists Union gallery", "museums", "Art gallery Vologda"),
    ("vologda_spaso_preobrazhensky", "Spaso-Preobrazhensky church", "places_of_worship", "Spaso Preobrazhensky Vologda"),
    ("vologda_st_paraskeva", "St Paraskeva church", "places_of_worship", "St Paraskeva church Vologda"),
]

EXTRA_SEEDS["volgograd"] = [
    ("volgograd_lenin_avenue", "Lenin Avenue", "overview", "Lenin avenue Volgograd"),
    ("volgograd_historical_museum", "Volgograd Historical Museum", "museums", "Volgograd historical museum"),
    ("volgograd_old_sarepta", "Museum Old Sarepta", "museums", "Old Sarepta museum Volgograd"),
    ("volgograd_church_nicholas", "Church of St Nicholas", "places_of_worship", "St Nicholas church Volgograd"),
    ("volgograd_rotonda", "Pantheon of Glory", "memorials", "Pantheon glory Volgograd"),
    ("volgograd_square_fighters", "Square of Fallen Fighters", "memorials", "Square fallen fighters Volgograd"),
    ("volgograd_trinitarian_church", "Trinitarian Church", "places_of_worship", "Trinitarian church Volgograd"),
    ("volgograd_church_nativity", "Church of the Nativity", "places_of_worship", "Nativity church Volgograd"),
    ("volgograd_memorial_hall", "Hall of Military Glory", "memorials", "Hall military glory Mamayev Kurgan"),
    ("volgograd_grudinina", "Grudinina machine-gun nest", "memorials", "Grudinina nest Volgograd"),
    ("volgograd_fine_arts", "Volgograd Regional Art Museum", "museums", "Fine arts museum Volgograd"),
    ("volgograd_gagarin_street", "Gagarin Street view", "overview", "Gagarin street Volgograd"),
    ("volgograd_church_michael", "St Michael church", "places_of_worship", "St Michael church Volgograd"),
    ("volgograd_river_port", "Volga river port", "overview", "Volga port Volgograd"),
    ("volgograd_cultural_center", "Volgograd cultural centre", "theaters", "Palace culture Volgograd"),
    ("volgograd_stalingrad_memorial", "Stalingrad battle memorial wall", "memorials", "Stalingrad memorial Volgograd"),
    ("volgograd_orthodox_old", "Old Believers church", "places_of_worship", "Old believers church Volgograd"),
    ("volgograd_volga_deutsche", "Volga Germans museum", "museums", "Volga Germans museum Volgograd"),
]

EXTRA_SEEDS["jerusalem"] = [
    ("jerusalem_church_pater_noster", "Church of the Pater Noster", "places_of_worship", "Church of the Pater Noster Jerusalem"),
    ("jerusalem_dominus_flevit", "Dominus Flevit Church", "places_of_worship", "Dominus Flevit church Jerusalem"),
    ("jerusalem_pool_bethesda", "Pool of Bethesda", "places_of_worship", "Pool of Bethesda Jerusalem"),
    ("jerusalem_church_flagellation", "Church of the Flagellation", "places_of_worship", "Church of the Flagellation Jerusalem"),
    ("jerusalem_garden_tomb", "Garden Tomb", "places_of_worship", "Garden Tomb Jerusalem"),
    ("jerusalem_damascus_gate", "Damascus Gate", "landmarks", "Damascus Gate Jerusalem"),
    ("jerusalem_mount_zion", "Mount Zion", "overview", "Mount Zion Jerusalem"),
    ("jerusalem_church_visitation", "Church of the Visitation", "places_of_worship", "Church of the Visitation Ein Kerem"),
]

EXTRA_SEEDS["boston"] = [
    ("boston_old_north_church", "Old North Church", "places_of_worship", "Old North Church Boston"),
    ("boston_paul_revere_house", "Paul Revere House", "museums", "Paul Revere House Boston"),
]

EXTRA_SEEDS["philadelphia"] = [
    ("philadelphia_christ_church", "Christ Church Philadelphia", "places_of_worship", "Christ Church Philadelphia"),
    ("philadelphia_betsy_ross_house", "Betsy Ross House", "museums", "Betsy Ross House Philadelphia"),
]

# Backup top-up when Commons search skips (simple queries).
TOPUP_SEEDS: dict[str, list[tuple[str, str, str, str]]] = {
    "bangkok": [
        ("bangkok_wat_arun_view", "Wat Arun view", "places_of_worship", "Wat Arun Thailand"),
        ("bangkok_grand_palace_gate", "Grand Palace gate", "palaces", "Grand Palace Bangkok Thailand"),
        ("bangkok_wat_phra_kaew_ext", "Wat Phra Kaew", "places_of_worship", "Wat Phra Kaew Bangkok"),
        ("bangkok_wat_suthat_swing", "Giant Swing", "landmarks", "Giant Swing Bangkok"),
    ],
    "boston": [
        ("boston_kings_chapel", "King's Chapel", "places_of_worship", "Kings Chapel Boston"),
        ("boston_trinity_church", "Trinity Church Boston", "places_of_worship", "Trinity Church Boston Copley"),
    ],
    "philadelphia": [
        ("philadelphia_liberty_bell", "Liberty Bell", "landmarks", "Liberty Bell Philadelphia"),
        ("philadelphia_independence_hall", "Independence Hall", "landmarks", "Independence Hall Philadelphia"),
    ],
    "copenhagen": [
        ("copenhagen_marmorkirken", "Marble Church", "places_of_worship", "Marble Church Copenhagen"),
        ("copenhagen_rosenborg_ext", "Rosenborg", "palaces", "Rosenborg Castle Copenhagen Denmark"),
        ("copenhagen_nyhavn", "Nyhavn", "overview", "Nyhavn Copenhagen"),
        ("copenhagen_little_mermaid", "Little Mermaid", "landmarks", "Little Mermaid Copenhagen"),
        ("copenhagen_tivoli", "Tivoli Gardens", "parks", "Tivoli Gardens Copenhagen"),
    ],
    "dublin": [
        ("dublin_st_patricks_ext", "St Patrick's Cathedral", "places_of_worship", "St Patricks Cathedral Dublin"),
        ("dublin_castle_ext", "Dublin Castle", "landmarks", "Dublin Castle Ireland"),
        ("dublin_ha_penny", "Ha'penny Bridge", "bridges", "Ha penny Bridge Dublin"),
    ],
    "kharkiv": [
        ("kharkiv_freedom_square", "Freedom Square", "public_space", "Freedom Square Kharkiv"),
        ("kharkiv_mirror_stream_ext", "Mirror Stream", "landmarks", "Mirror Stream fountain Kharkiv"),
        ("kharkiv_annunciation_ext", "Annunciation Cathedral", "places_of_worship", "Annunciation Cathedral Kharkiv"),
    ],
    "kyiv": [
        ("kyiv_st_michael_ext", "St Michael Monastery", "places_of_worship", "St Michaels Monastery Kyiv"),
        ("kyiv_andriyivsky", "Andriyivsky Descent", "overview", "Andriyivsky Descent Kyiv"),
        ("kyiv_golden_gate_ext", "Golden Gate", "landmarks", "Golden Gate Kyiv"),
    ],
    "lisbon": [
        ("lisbon_jeronimos_ext", "Jerónimos Monastery", "places_of_worship", "Jeronimos Monastery Lisbon"),
        ("lisbon_belem_tower", "Belém Tower", "landmarks", "Belem Tower Lisbon"),
    ],
    "london": [
        ("london_tower_bridge", "Tower Bridge", "bridges", "Tower Bridge London"),
        ("london_buckingham", "Buckingham Palace", "palaces", "Buckingham Palace London"),
        ("london_westminster_ext", "Westminster Abbey", "places_of_worship", "Westminster Abbey London"),
        ("london_st_pauls_ext", "St Paul's Cathedral", "places_of_worship", "St Pauls Cathedral London"),
        ("london_big_ben", "Palace of Westminster clock", "landmarks", "Big Ben London"),
    ],
    "los_angeles": [
        ("los_angeles_hollywood_sign_ext", "Hollywood Sign", "landmarks", "Hollywood Sign Los Angeles"),
        ("los_angeles_getty_ext", "Getty Center", "museums", "Getty Center Los Angeles"),
        ("los_angeles_griffith_obs", "Griffith Observatory", "landmarks", "Griffith Observatory Los Angeles"),
    ],
    "lviv": [
        ("lviv_latin_cathedral", "Latin Cathedral", "places_of_worship", "Latin Cathedral Lviv"),
        ("lviv_bernardine_ext", "Bernardine church", "places_of_worship", "Bernardine church Lviv"),
    ],
    "novosibirsk": [
        ("novosibirsk_opera_ext", "Novosibirsk Opera", "theaters", "Novosibirsk Opera Theatre"),
        ("novosibirsk_alexander_nevsky_ext", "Alexander Nevsky Cathedral", "places_of_worship", "Alexander Nevsky Cathedral Novosibirsk"),
        ("novosibirsk_zoo_ext", "Novosibirsk Zoo", "parks", "Novosibirsk Zoo"),
    ],
    "odessa": [
        ("odessa_potemkin_ext", "Potemkin Stairs", "landmarks", "Potemkin Stairs Odessa"),
        ("odessa_opera_ext", "Odessa Opera", "theaters", "Odessa Opera and Ballet Theater"),
    ],
    "san_francisco": [
        ("san_francisco_golden_gate", "Golden Gate Bridge", "bridges", "Golden Gate Bridge San Francisco"),
        ("san_francisco_alcatraz", "Alcatraz Island", "landmarks", "Alcatraz San Francisco"),
        ("san_francisco_painted_ladies", "Painted Ladies", "landmarks", "Painted Ladies San Francisco"),
        ("san_francisco_fishermans_wharf", "Fisherman's Wharf", "overview", "Fishermans Wharf San Francisco"),
        ("san_francisco_city_hall", "San Francisco City Hall", "landmarks", "San Francisco City Hall"),
        ("san_francisco_mission_dolores_ext", "Mission Dolores", "places_of_worship", "Mission Dolores San Francisco"),
        ("san_francisco_transamerica", "Transamerica Pyramid", "landmarks", "Transamerica Pyramid San Francisco"),
        ("san_francisco_lombard", "Lombard Street", "landmarks", "Lombard Street San Francisco"),
        ("san_francisco_palace_fine_arts", "Palace of Fine Arts", "landmarks", "Palace of Fine Arts San Francisco"),
        ("san_francisco_coit_tower_ext", "Coit Tower", "landmarks", "Coit Tower San Francisco"),
    ],
    "singapore": [
        ("singapore_merlion", "Merlion Park", "landmarks", "Merlion Singapore"),
        ("singapore_marina_bay", "Marina Bay Sands", "landmarks", "Marina Bay Sands Singapore"),
        ("singapore_thian_hock_ext", "Thian Hock Keng", "places_of_worship", "Thian Hock Keng temple Singapore"),
        ("singapore_gardens_bay", "Gardens by the Bay", "parks", "Gardens by the Bay Singapore"),
        ("singapore_buddha_tooth", "Buddha Tooth Relic Temple", "places_of_worship", "Buddha Tooth Relic Temple Singapore"),
    ],
    "tokyo": [
        ("tokyo_sensoji_ext", "Sensō-ji", "places_of_worship", "Sensoji temple Tokyo"),
        ("tokyo_meiji_ext", "Meiji Shrine", "places_of_worship", "Meiji Shrine Tokyo"),
        ("tokyo_imperial_palace_ext", "Imperial Palace", "landmarks", "Imperial Palace Tokyo"),
        ("tokyo_skytree", "Tokyo Skytree", "landmarks", "Tokyo Skytree"),
        ("tokyo_shibuya", "Shibuya Crossing", "overview", "Shibuya crossing Tokyo"),
    ],
    "tver": [
        ("tver_volga_embankment_ext", "Volga embankment", "public_space", "Volga embankment Tver"),
        ("tver_resurrection_ext", "Resurrection Cathedral", "places_of_worship", "Resurrection Cathedral Tver"),
        ("tver_travel_palace_ext", "Travel Palace", "palaces", "Travel Palace Tver"),
    ],
    "vatican": [
        ("vatican_st_peters_ext", "St Peter's Basilica", "places_of_worship", "St Peters Basilica Vatican"),
        ("vatican_sistine_ext", "Sistine Chapel", "places_of_worship", "Sistine Chapel Vatican"),
        ("vatican_castel_angelo_ext", "Castel Sant'Angelo", "landmarks", "Castel Sant Angelo Rome"),
        ("vatican_st_peters_square_ext", "St Peter's Square", "public_space", "St Peters Square Vatican"),
    ],
    "vladivostok": [
        ("vladivostok_golden_bridge_ext", "Zolotoy Bridge", "bridges", "Zolotoy Bridge Vladivostok"),
        ("vladivostok_submarine_ext", "C-56 Submarine", "museums", "C-56 submarine Vladivostok"),
        ("vladivostok_russky_bridge_ext", "Russky Bridge", "bridges", "Russky Bridge Vladivostok"),
        ("vladivostok_railway_ext", "Vladivostok station", "railway_stations", "Vladivostok railway station"),
    ],
    "volgograd": [
        ("volgograd_motherland_ext", "Motherland Calls", "monuments", "The Motherland Calls Volgograd"),
        ("volgograd_panorama_ext", "Panorama Museum", "museums", "Panorama museum Stalingrad Volgograd"),
        ("volgograd_embankment_ext", "Volga embankment", "public_space", "Volgograd embankment"),
        ("volgograd_alexander_nevsky_ext", "Alexander Nevsky Cathedral", "places_of_worship", "Alexander Nevsky Cathedral Volgograd"),
        ("volgograd_pavlov_ext", "Pavlov's House", "memorials", "Pavlovs House Volgograd"),
    ],
    "vologda": [
        ("vologda_sophia_cathedral_ext", "Saint Sophia Cathedral", "places_of_worship", "Saint Sophia Cathedral Vologda"),
        ("vologda_kremlin_ext", "Vologda Kremlin", "overview", "Vologda Kremlin"),
        ("vologda_spaso_prilutsky_ext", "Spaso-Prilutsky Monastery", "places_of_worship", "Spaso-Prilutsky Monastery"),
        ("vologda_lace_museum_ext", "Museum of Lace", "museums", "Museum of lace Vologda"),
        ("vologda_resurrection_ext", "Resurrection Cathedral", "places_of_worship", "Resurrection Cathedral Vologda"),
        ("vologda_river_ext", "Vologda River", "public_space", "Vologda river"),
        ("vologda_house_peter_ext", "House of Peter I", "museums", "House of Peter the Great Vologda"),
        ("vologda_regional_museum_ext", "Regional Museum", "museums", "Vologda museum"),
        ("vologda_church_john_ext", "St John church", "places_of_worship", "Church John Baptist Vologda Russia"),
        ("vologda_dmitry_ext", "Dmitry Prilutsky church", "places_of_worship", "Dmitry Prilutsky Vologda"),
        ("vologda_art_gallery_ext", "Art Gallery", "museums", "Vologda art gallery"),
    ],
    "yaroslavl": [
        ("yaroslavl_assumption_ext", "Assumption Cathedral", "places_of_worship", "Assumption Cathedral Yaroslavl"),
        ("yaroslavl_st_elijah_ext", "Church of Elijah", "places_of_worship", "Church of Elijah the Prophet Yaroslavl"),
        ("yaroslavl_volga_ext", "Volga embankment", "public_space", "Volga embankment Yaroslavl"),
    ],
    "kazan": [
        ("kazan_kremlin_ext", "Kazan Kremlin", "overview", "Kazan Kremlin"),
        ("kazan_kul_sharif_ext", "Kul Sharif Mosque", "places_of_worship", "Kul Sharif Mosque Kazan"),
        ("kazan_bauman_ext", "Bauman Street", "public_space", "Bauman Street Kazan"),
    ],
    "athens": [
        ("athens_temple_hephaestus", "Temple of Hephaestus", "places_of_worship", "Hephaestus temple Athens"),
        ("athens_monastiraki_metro", "Monastiraki", "public_space", "Monastiraki Athens"),
    ],
    "chernivtsi": [
        ("chernivtsi_resurrection_church", "Resurrection Church", "places_of_worship", "Resurrection church Chernivtsi"),
        ("chernivtsi_train_depot", "Railway station hall", "landmarks", "Chernivtsi railway station"),
    ],
    "dubai": [
        ("dubai_jumeirah_mosque_ext", "Jumeirah Mosque", "places_of_worship", "Jumeirah Mosque Dubai"),
        ("dubai_al_fahidi_district", "Al Fahidi", "overview", "Al Fahidi Dubai creek"),
    ],
    "istanbul": [
        ("istanbul_blue_mosque_ext", "Blue Mosque", "places_of_worship", "Sultan Ahmed Mosque Istanbul"),
        ("istanbul_topkapi_gate", "Topkapi Palace", "palaces", "Topkapi Palace Istanbul"),
    ],
}
