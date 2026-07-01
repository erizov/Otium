# -*- coding: utf-8 -*-
"""Map style chapters to city-guide place slugs."""

from __future__ import annotations

CITY_STYLE_POOL: dict[str, list[tuple[str, str]]] = {
    "roman_britain": [("london", "london_natural_history_museum"), ("boston", "boston_revere_beach")],
    "norman": [("london", "london_tower_of_london")],
    "english_gothic": [("london", "london_palace_westminster"), ("london", "london_westminster_abbey"), ("london", "london_big_ben"), ("philadelphia", "philadelphia_eastern_state_penitentiary"), ("philadelphia", "philadelphia_boathouse_row"), ("philadelphia", "philadelphia_pennsylvania_academy_fine_arts")],
    "tudor": [("boston", "boston_paul_revere_house")],
    "elizabethan_jacobean": [("london", "london_shakespeare_globe")],
    "palladian_wren": [("london", "london_st_pauls_cathedral"), ("london", "london_st_pauls_aerial_cropped")],
    "georgian": [("boston", "boston_faneuil_hall"), ("boston", "boston_old_north_church"), ("philadelphia", "philadelphia_independence_hall"), ("philadelphia", "philadelphia_christ_church_philadelphia")],
    "regency": [],
    "victorian": [("london", "london_tower_bridge"), ("london", "london_kew_gardens"), ("boston", "boston_public_garden"), ("philadelphia", "philadelphia_reading_terminal_market"), ("philadelphia", "philadelphia_zoo")],
    "arts_crafts": [],
    "edwardian": [],
    "art_deco": [("philadelphia", "philadelphia_thirtieth_street_station")],
    "modernism": [("boston", "boston_quincy_market"), ("boston", "boston_city_hall"), ("boston", "boston_christian_science_plaza"), ("philadelphia", "philadelphia_love_park")],
    "brutalism": [("boston", "boston_new_england_aquarium")],
    "contemporary": [("london", "london_tate_modern"), ("london", "london_tate_britain"), ("boston", "boston_museum_of_fine_arts_boston"), ("philadelphia", "philadelphia_national_constitution_center")],
}
