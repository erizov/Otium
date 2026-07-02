# -*- coding: utf-8 -*-
"""Explicit image URLs for guide places."""

from __future__ import annotations

from typing import Any

IMAGE_URL_OVERRIDES: dict[str, tuple[str, str | None]] = {
    "roman_britain_hadrians_wall": (
        "https://upload.wikimedia.org/wikipedia/commons/f/f5/"
        "Hadrian%27s_Wall_west_of_Housesteads_3.jpg",
        None,
    ),
    "art_nouveau_turkey_cafe": (
        "https://upload.wikimedia.org/wikipedia/commons/7/75/The_Turkey_Cafe%2C_Granby_Street_%E2%80%93_4_-_geograph.org.uk_-_8127111.jpg",
        None,
    ),
    "art_nouveau_royal_arcade_norwich": (
        "https://upload.wikimedia.org/wikipedia/commons/d/dd/Royal_Arcade%2C_Norwich%2C_Inglaterra%2C_2022-11-19%2C_DD_32.jpg",
        None,
    ),
    "art_nouveau_queens_cross_church": (
        "https://upload.wikimedia.org/wikipedia/commons/d/dc/Queens_Cross_Church07a.jpg",
        None,
    ),
    "art_nouveau_harrods_food_hall": (
        "https://i.pinimg.com/originals/d5/e7/c0/d5e7c01cffd89f1d8d177280ec4325d4.jpg",
        None,
    ),
    "art_nouveau_everards_printing": (
        "https://upload.wikimedia.org/wikipedia/commons/4/47/Everard%27s_Printing_Works%2C_Bristol.jpg",
        None,
    ),
    "georgian_bath_royal_crescent": (
        "https://upload.wikimedia.org/wikipedia/commons/4/45/Royal_Crescent%2C_Bath.jpg",
        None,
    ),
    "georgian_bath_circus": (
        "https://wikiway.com/upload/hl-photo/3e3/2ed/bat_5.jpg",
        None,
    ),
    "english_gothic_salisbury_cathedral": (
        "https://upload.wikimedia.org/wikipedia/commons/1/1c/Salisbury_Cathedral%2C_Cathedral_Close%2C_Wiltshire.jpg",
        None,
    ),
    "english_gothic_salisbury": (
        "https://upload.wikimedia.org/wikipedia/commons/1/1c/Salisbury_Cathedral%2C_Cathedral_Close%2C_Wiltshire.jpg",
        None,
    ),
    "brutalism_national_theatre": (
        "https://upload.wikimedia.org/wikipedia/commons/7/73/National_Theatre_London.jpg",
        None,
    ),
    "art_deco_daily_telegraph": (
        "https://upload.wikimedia.org/wikipedia/commons/1/12/Fleet_Street%2C_former_Daily_Telegraph_headquarters_-_geograph.org.uk_-_2244211.jpg",
        None,
    ),
    "art_deco_willesden_synagogue": (
        "https://upload.wikimedia.org/wikipedia/commons/c/ce/Synagogue_on_Parkside%2C_Willesden_-_geograph.org.uk_-_62124.jpg",
        None,
    ),
    "arts_crafts_blackwell": (
        "https://upload.wikimedia.org/wikipedia/commons/e/ec/Bowness-on-Windermere%2C_Blackwell%2C_the_Arts_and_Crafts_House_-_geograph.org.uk_-_7612905.jpg",
        None,
    ),
    "arts_crafts_red_house": (
        "https://upload.wikimedia.org/wikipedia/commons/0/03/The_Red_House%2C_Bexleyheath.JPG",
        None,
    ),
    "brutalism_alexandra_road": (
        "https://i.ytimg.com/vi/qDNwgbJBHko/maxresdefault.jpg",
        None,
    ),
    "brutalism_clifton_cathedral": (
        "https://upload.wikimedia.org/wikipedia/commons/3/31/Clifton_Cathedral_-_PXL_20260331_133707156.jpg",
        None,
    ),
    "edwardian_lloyds_register": (
        "https://upload.wikimedia.org/wikipedia/commons/5/5e/Lloyd%27s_register.JPG",
        None,
    ),
    "georgian_bath_abbey": (
        "https://upload.wikimedia.org/wikipedia/commons/9/97/Bath_Abbey_Exterior%2C_Somerset%2C_UK_-_Diliff.jpg",
        None,
    ),
    "georgian_bevis_marks_synagogue": (
        "https://upload.wikimedia.org/wikipedia/commons/2/22/Bevis_Marks_Synagogue_05.JPG",
        None,
    ),
    "palladian_wren_greenwich": (
        "https://upload.wikimedia.org/wikipedia/commons/b/b0/Royal_Naval_College_Greenwich_view_from_the_Thames.jpg",
        None,
    ),
    "regency_regent_street": (
        "https://www.malls.ru/upload/iblock/0cd/Depositphotos_26296747_l_2015.jpg",
        None,
    ),
    "roman_britain_fishbourne": (
        "https://upload.wikimedia.org/wikipedia/commons/7/75/Fishbourne_palace_north_wing.JPG",
        None,
    ),
    "tudor_st_james_piccadilly": (
        "https://upload.wikimedia.org/wikipedia/commons/a/ac/St_James_Church_Piccadilly_1.jpg",
        None,
    ),
}
PRIMARY_IMAGE_REUSE: dict[str, tuple[str, str]] = {}
SECOND_IMAGE_REUSE: dict[str, tuple[str, str]] = {}


def apply_image_url_overrides(place: dict[str, Any]) -> dict[str, Any]:
    slug = str(place.get("slug") or "")
    override = IMAGE_URL_OVERRIDES.get(slug)
    if not override:
        return place
    primary, secondary = override
    merged = dict(place)
    merged["image_source_url"] = primary
    if secondary:
        merged["additional_images"] = [{
            "image_source_url": secondary,
        }]
    else:
        merged.pop("additional_images", None)
    return merged
