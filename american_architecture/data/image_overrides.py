# -*- coding: utf-8 -*-
"""Explicit image URLs for guide places."""

from __future__ import annotations

from typing import Any

IMAGE_URL_OVERRIDES: dict[str, tuple[str, str | None]] = {
    "international_style_unitarian_church_dallas": (
        "https://avatars.mds.yandex.net/i?id="
        "93b3b50e9ef198e622c65d17c281ba66_l-5234649-images-thumbs&n=13",
        None,
    ),
    "beaux_arts_mary_queen_of_the_world": (
        "https://upload.wikimedia.org/wikipedia/commons/4/4a/"
        "Mary%2C_Queen_of_the_World_Cathedral_in_Montreal.jpg",
        None,
    ),
    "gothic_revival_st_patrick": (
        "https://www.mbbarch.com/wp-content/uploads/2019/07/295.jpg",
        None,
    ),
    "gothic_revival_trinity_wall_street": (
        "https://www.mbbarch.com/wp-content/uploads/2022/11/"
        "2022CP05-0162-1920x1714.gif",
        None,
    ),
    "art_deco_americas_chicago_temple": (
        "https://upload.wikimedia.org/wikipedia/commons/2/25/"
        "Chicago_Temple_Building4.jpg",
        None,
    ),
    "art_deco_americas_empire_state": (
        "https://www.esbnyc.com/sites/default/files/2020-01/ESB%20Day.jpg",
        None,
    ),
    "midcentury_modern_brasilia": (
        "https://wikiway.com/upload/hl-photo/1cc/5fe/"
        "sobor-presvyatoy-devy-marii_40.jpg",
        None,
    ),
    "midcentury_modern_eames_house": (
        "https://images.adsttc.com/media/images/5ee9/482a/b357/6578/"
        "8b00/003c/large_jpg/shutterstock_1095854558.jpg?1592346653",
        None,
    ),
    "postmodern_portland_building": (
        "https://avatars.mds.yandex.net/i?id="
        "f4eeb4afa982894f6516eabbb07683f8_l-5220706-images-thumbs"
        "&ref=rim&n=13&w=1080&h=991",
        None,
    ),
    "latin_colonial_baroque_ouro_preto_sao_francisco": (
        "https://bigfoto.name/uploads/posts/2022-02/"
        "1643707687_35-bigfoto-name-p-anninskoe-barokko-v-arkhitekture-83.jpg",
        None,
    ),
    "latin_modernism_rio_cathedral": (
        "https://insideinside.org/wp-content/uploads/2023/06/"
        "archdiocese-of-rio-de-1.jpg",
        None,
    ),
    "latin_modernism_torre_latinoamericana": (
        "https://upload.wikimedia.org/wikipedia/commons/c/c3/"
        "Latinoamerica_tower%2C_Mexico_City_2022_p2.jpg",
        None,
    ),
    "gothic_revival_quito_voto_nacional": (
        "https://upload.wikimedia.org/wikipedia/commons/0/04/"
        "Basilica_del_Voto_Nacional.jpg",
        None,
    ),
    "gothic_revival_st_cecilia_nyc": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/"
        "St-cecilia-church-nyc.jpg/1280px-St-cecilia-church-nyc.jpg",
        None,
    ),
    "gothic_revival_toronto_st_james": (
        "https://www.doorsopenontario.on.ca/events/toronto/"
        "st-james-cathedral/2025-Toronto-St-James-Cathedral-1500px.jpg",
        None,
    ),
    "art_deco_americas_christ_redeemer": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/"
        "Redentor_Over_Clouds_1.jpg/1280px-Redentor_Over_Clouds_1.jpg",
        None,
    ),
    "midcentury_modern_space_needle": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/"
        "Seattle_%28WA%2C_USA%29%2C_Space_Needle_--_2022_--_1498.jpg/"
        "1280px-Seattle_%28WA%2C_USA%29%2C_Space_Needle_--_2022_--_1498.jpg",
        None,
    ),
    "colonial_americas_independence_hall": (
        "https://www.timetravelturtle.com/wp-content/uploads/2012/07/"
        "USA-2012-2_new.jpg",
        None,
    ),
    "victorian_americas_chateau_frontenac": (
        "https://avatars.mds.yandex.net/i?id="
        "8e9066151ecf16f10125da21b72c3b40_l-2769679-images-thumbs&n=13",
        None,
    ),
}

ADDITIONAL_IMAGE_URL_OVERRIDES: dict[str, str] = {
    "greek_revival_custom_house_nyc": (
        "https://calendar.aiany.org/wp-content/uploads/sites/3/2017/10/"
        "12-Alexander-Hamilton-U.S.-Custom-House_Cass-Gilbert-1907_"
        "David-Sundberg-Esto.jpg"
    ),
    "gothic_revival_st_patricks_montreal": (
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/"
        "0d/8d/fb/71/inside.jpg?w=1400&h=800&s=1"
    ),
    "gothic_revival_st_patricks_old_nyc": (
        "https://media.timeout.com/images/105961242/image.webp"
    ),
    "gothic_revival_cathedral_st_john": (
        "https://i.archi.ru/i/650/406956.jpg"
    ),
    "latin_colonial_baroque_quito_compania": (
        "https://upload.wikimedia.org/wikipedia/commons/6/6a/"
        "54_Iglesia_de_la_Compania_de_Jesus_%281%29.JPG"
    ),
}

PRIMARY_IMAGE_REUSE: dict[str, tuple[str, str]] = {}
SECOND_IMAGE_REUSE: dict[str, tuple[str, str]] = {}


def apply_image_url_overrides(place: dict[str, Any]) -> dict[str, Any]:
    slug = str(place.get("slug") or "")
    merged = dict(place)
    changed = False
    override = IMAGE_URL_OVERRIDES.get(slug)
    if override:
        primary, secondary = override
        merged["image_source_url"] = primary
        changed = True
        if secondary:
            merged["additional_images"] = [{
                "image_source_url": secondary,
            }]
        elif slug not in ADDITIONAL_IMAGE_URL_OVERRIDES:
            merged.pop("additional_images", None)
    extra_url = ADDITIONAL_IMAGE_URL_OVERRIDES.get(slug)
    if extra_url:
        from american_architecture.data.image_reuse import extra_image_rel

        merged["additional_images"] = [{
            "image_rel_path": extra_image_rel(slug),
            "image_source_url": extra_url,
        }]
        changed = True
    if not changed:
        return place
    return merged
