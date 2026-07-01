# -*- coding: utf-8 -*-
"""Explicit image URLs for guide places."""

from __future__ import annotations

from typing import Any

IMAGE_URL_OVERRIDES: dict[str, tuple[str, str | None]] = {
    "historicism_vienna_votivkirche": (
        "https://upload.wikimedia.org/wikipedia/commons/0/05/Votivkirche_bei_Nacht_sl1.jpg",
        None,
    ),
    "art_nouveau_hackesche_hofe": (
        "https://upload.wikimedia.org/wikipedia/commons/f/fe/Berlin_Hackesche_H%C3%B6fe.jpg",
        None,
    ),
    "art_nouveau_hundertwasser": (
        "https://upload.wikimedia.org/wikipedia/commons/7/70/Hundertwasserhaus.jpg",
        None,
    ),
    "baroque_dresden_frauenkirche": (
        "https://upload.wikimedia.org/wikipedia/commons/2/22/Dresden_Frauenkirche.jpg",
        None,
    ),
    "baroque_schonbrunn": (
        "https://upload.wikimedia.org/wikipedia/commons/c/c0/Schloss_Sch%C3%B6nbrunn_Wien_2014.jpg",
        None,
    ),
    "brutalism_bielefeld_univ": (
        "https://upload.wikimedia.org/wikipedia/commons/5/52/Universit%C3%A4t_Bielefeld.jpg",
        None,
    ),
    "expressionism_lichtburg": (
        "https://upload.wikimedia.org/wikipedia/commons/8/87/Lichtburg_Essen.jpg",
        None,
    ),
    "gothic_marienkirche_lubeck": (
        "https://upload.wikimedia.org/wikipedia/commons/2/21/Marienkirche_L%C3%BCbeck.jpg",
        None,
    ),
    "gothic_regensburg_cathedral": (
        "https://upload.wikimedia.org/wikipedia/commons/7/77/GER_Regensburg%2C_Dom_St._Peter_0001.jpg",
        None,
    ),
        "gothic_ulm_minster": (
        "https://upload.wikimedia.org/wikipedia/commons/7/71/Ulm-Minster-0160.jpg",
        None,
    ),
    "historicism_new_synagogue_berlin": (
        "https://upload.wikimedia.org/wikipedia/commons/a/a0/New_Synagogue_Berlin.jpg",
        None,
    ),
    "nazi_monumental_reichsparteitag": (
        "https://upload.wikimedia.org/wikipedia/commons/6/66/Kongresshalle_Nuremberg.jpg",
        None,
    ),
        "nazi_monumental_tempelhof": (
        "https://upload.wikimedia.org/wikipedia/commons/4/45/TempelhofExterior.jpg",
        None,
    ),
        "neoclassicism_walhalla": (
        "https://upload.wikimedia.org/wikipedia/commons/b/b0/Walhalla-Memorial_01.jpg",
        None,
    ),
        "postwar_modern_berlin_phil": (
        "https://upload.wikimedia.org/wikipedia/commons/6/65/Berliner_Philharmonie.jpg",
        None,
    ),
    "postwar_modern_fernsehturm": (
        "https://upload.wikimedia.org/wikipedia/commons/1/11/Berlin_TV_Tower.jpg",
        None,
    ),
        "postwar_modern_hansaviertel": (
        "https://upload.wikimedia.org/wikipedia/commons/7/73/Interbau_Berlin-Hansaviertel_with_snow_2025-02-14_03.jpg",
        None,
    ),
    "postwar_modern_krolloper_site": (
        "https://upload.wikimedia.org/wikipedia/commons/9/96/Kulturforum_Berlin.jpg",
        None,
    ),
        "renaissance_heidelberg": (
        "https://upload.wikimedia.org/wikipedia/commons/5/51/Heidelberg_Schloss.jpg",
        None,
    ),
        "rococo_wieskirche": (
        "https://upload.wikimedia.org/wikipedia/commons/8/87/Steingaden%2C_Wieskirche_002.jpg",
        None,
    ),
        "rococo_zwinger": (
        "https://irecommend.ru/sites/default/files/imagecache/copyright1/user-images/1294913/Rn6iY1ZjT76JAqmVwT2KWA.jpg",
        None,
    ),
        "roman_germania_porta_nigra": (
        "https://upload.wikimedia.org/wikipedia/commons/6/6a/Porta_Nigra_bei_Nacht.jpg",
        None,
    ),
        "romanesque_mainz": (
        "https://upload.wikimedia.org/wikipedia/commons/7/79/Mainz_Cathedral_-_Mainz%2C_Germany_-_panoramio.jpg",
        None,
    ),
        "romanesque_mainz_cathedral": (
        "https://upload.wikimedia.org/wikipedia/commons/7/79/Mainz_Cathedral_-_Mainz%2C_Germany_-_panoramio.jpg",
        None,
    ),
        "romanesque_speyer": (
        "https://upload.wikimedia.org/wikipedia/commons/0/03/Speyer_Dom_Luft.jpg",
        None,
    ),
        "romanesque_speyer_cathedral": (
        "https://upload.wikimedia.org/wikipedia/commons/0/03/Speyer_Dom_Luft.jpg",
        None,
    ),
        "romanesque_worms": (
        "https://upload.wikimedia.org/wikipedia/commons/0/00/Worms-Dom_St_Peter-22-2007-gje.jpg",
        None,
    ),
        "romanesque_worms_cathedral": (
        "https://upload.wikimedia.org/wikipedia/commons/0/00/Worms-Dom_St_Peter-22-2007-gje.jpg",
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
