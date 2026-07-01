# -*- coding: utf-8 -*-
"""Map style chapters to city-guide place slugs."""

from __future__ import annotations

CITY_STYLE_POOL: dict[str, list[tuple[str, str]]] = {
    "colonial_americas": [("new_york", "new_york_washington_square_arch"), ("boston", "boston_missionchurchboston"), ("philadelphia", "philadelphia_elfreths_alley"), ("philadelphia", "philadelphia_christ_church_philadelphia"), ("philadelphia", "philadelphia_fort_mifflin"), ("los_angeles", "los_angeles_griffith_sign_view"), ("los_angeles", "los_angeles_california_science_center"), ("los_angeles", "los_angeles_the_broad"), ("los_angeles", "los_angeles_union_station"), ("los_angeles", "los_angeles_rodeo_drive"), ("los_angeles", "los_angeles_mission_san_gabriel"), ("san_francisco", "san_francisco_mission_dolores"), ("montreal", "montreal_old_port_montreal"), ("montreal", "montreal_place_jacques_cartier")],
    "federal": [("new_york", "new_york_ellis_island_immigration_museum"), ("new_york", "new_york_federal_hall_nyc"), ("boston", "boston_massachusetts_state_house"), ("boston", "boston_jfk_presidential_library"), ("boston", "boston_city_hall"), ("san_francisco", "san_francisco_alcatraz")],
    "greek_revival": [("boston", "boston_quincy_market")],
    "gothic_revival": [("new_york", "new_york_trinity_church_wall_street"), ("philadelphia", "philadelphia_eastern_state_penitentiary"), ("montreal", "montreal_notre_dame_montreal"), ("montreal", "montreal_marche_bonsecours"), ("montreal", "montreal_notre_dame_neiges_cemetery"), ("montreal", "montreal_eglise_saint_patrick_montreal"), ("montreal", "montreal_cimetiere_notre_dame_neiges_chapel")],
    "victorian_americas": [("new_york", "new_york_brooklyn_bridge"), ("new_york", "new_york_american_museum_natural_history"), ("new_york", "new_york_tenement_museum_nyc"), ("boston", "boston_public_garden"), ("philadelphia", "philadelphia_city_hall"), ("philadelphia", "philadelphia_reading_terminal_market"), ("philadelphia", "philadelphia_boathouse_row"), ("philadelphia", "philadelphia_pennsylvania_academy_fine_arts"), ("philadelphia", "philadelphia_zoo"), ("san_francisco", "san_francisco_painted_ladies"), ("san_francisco", "san_francisco_chinatown_gate")],
    "chicago_school": [("new_york", "new_york_flatiron_building"), ("new_york", "new_york_one_world_trade_center"), ("san_francisco", "san_francisco_transamerica")],
    "beaux_arts": [("new_york", "new_york_statue_of_liberty"), ("new_york", "new_york_metropolitan_museum_of_art"), ("new_york", "new_york_ny_public_library_main"), ("boston", "boston_widener_library"), ("boston", "boston_museum_of_fine_arts_boston"), ("philadelphia", "philadelphia_museum_of_art"), ("san_francisco", "san_francisco_ferry_building"), ("san_francisco", "san_francisco_palace_fine_arts")],
    "prairie_style": [("new_york", "new_york_guggenheim_museum")],
    "art_deco_americas": [("new_york", "new_york_empire_state_building"), ("new_york", "new_york_rockefeller_center"), ("new_york", "new_york_chrysler_building"), ("new_york", "new_york_yankee_stadium"), ("new_york", "new_york_rockefeller_top_of_rock"), ("philadelphia", "philadelphia_thirtieth_street_station"), ("los_angeles", "los_angeles_griffith_observatory"), ("san_francisco", "san_francisco_golden_gate_bridge"), ("san_francisco", "san_francisco_coit_tower"), ("san_francisco", "san_francisco_castro")],
    "international_style": [],
    "midcentury_modern": [("boston", "boston_christian_science_plaza"), ("los_angeles", "los_angeles_la_brea_tar_pits")],
    "brutalism_americas": [("boston", "boston_new_england_aquarium"), ("montreal", "montreal_habitat_67"), ("montreal", "montreal_biodome_montreal")],
    "postmodern": [("boston", "boston_public_library_mckim")],
    "latin_colonial_baroque": [],
    "latin_modernism": [],
    "contemporary_americas": [("new_york", "new_york_the_vessel"), ("new_york", "new_york_whitney_museum_meatpacking"), ("philadelphia", "philadelphia_national_constitution_center"), ("los_angeles", "los_angeles_walt_disney_concert_hall"), ("los_angeles", "los_angeles_cathedral"), ("los_angeles", "los_angeles_crypto_arena"), ("montreal", "montreal_mcgill_campus"), ("montreal", "montreal_museum_fine_arts"), ("montreal", "montreal_insectarium")],
}
