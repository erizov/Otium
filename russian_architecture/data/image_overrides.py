# -*- coding: utf-8 -*-
"""Explicit Commons URLs for guide places that need better photos."""

from __future__ import annotations

from typing import Any

from russian_architecture.data.image_reuse import extra_image_rel

_SOVETSKAYA_HOTEL_URLS: tuple[str, str] = (
    "https://upload.wikimedia.org/wikipedia/commons/9/95/"
    "Sovietsky_Hotel.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/1/14/"
    "Moscow_-_Hotel_Sovietskaya_01.jpg",
)

_MOSCOW_BUILDINGS_30_SLUGS = frozenset({
    "stalinist_moscow_buildings_30_2",
})

_KREMLIN_DORMITION = (
    "https://upload.wikimedia.org/wikipedia/commons/"
    "8/8d/Cathedral_of_the_Dormition_in_the_Moscow_Kremlin.jpg"
)
_VLADIMIR_ASSUMPTION = (
    "https://upload.wikimedia.org/wikipedia/commons/e/eb/"
    "%D0%A3%D1%81%D0%BF%D0%B5%D0%BD%D1%81%D0%BA%D0%B8%D0%B9_%D1%81%D0%BE%D0%B1%D0%BE%D1%80_"
    "%D0%92%D0%BB%D0%B0%D0%B4%D0%B8%D0%BC%D0%B8%D1%80_3.jpg"
)
_KREMLIN_DORMITION_SECOND = (
    "https://upload.wikimedia.org/wikipedia/commons/1/13/"
    "Assumption_Cathedral_in_Moscow_01.JPG"
)
_HOUSE_ON_EMBANKMENT = (
    "https://avatars.mds.yandex.net/get-altay/2389272/"
    "2a000001750218b563de0fcbfa5c4919cf70/XXL"
)
_POLITKATORZHAN = (
    "https://mosculture.ru/wp-content/uploads/2014/09/DSC07806.jpg"
)
_STATE_DUMA = (
    "https://cdnstatic.rg.ru/uploads/images/2025/10/01/"
    "ria_8184749hr_967.jpg"
)
_BELORUSSKY_RAIL = (
    "https://avatars.mds.yandex.net/i?id="
    "6f9e77b8923cc389aac2922e9fa48e4b_l-5205578-images-thumbs"
    "&ref=rim&n=13&w=1200&h=776"
)
_BELORUSSKY_RAIL_SECOND = (
    "https://live.staticflickr.com/3870/"
    "14284718169_2c3de612d0_b.jpg"
)
_KOMSOMOLSKAYA_METRO = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/"
    "MosMetro_KomsomolskayaKL_img2_asv2018-01.jpg/1920px-"
    "MosMetro_KomsomolskayaKL_img2_asv2018-01.jpg"
)
_RED_ARMY_THEATER = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/"
    "Russian_Army_Theatre.jpg/1920px-Russian_Army_Theatre.jpg"
)
_PAVELETSKY_RAIL = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/"
    "Paveletsky_railway_station_Moscow_2013.jpg/1280px-"
    "Paveletsky_railway_station_Moscow_2013.jpg"
)
_PROSPEKT_MIRA_METRO = (
    "https://avatars.mds.yandex.net/i?id="
    "b9173812b1cb5b11cf05dad885a7c17f_l-9834718-images-thumbs&n=13"
)
_PARK_KULTURY_METRO = (
    "https://www.m24.ru/b/d/nBkSUhL2h1Ajms6zLr6BrNOp2Z318Ji-mifGnuWR9mOBdDebBizCnTY8"
    "qdJf6ReJ58vU9meMMok3Ee2nhSR6ISeO9G1N_wjJ=T_DixojC49qmDLl8Gxfmjw.jpg"
)
_TASS_BUILDING = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/"
    "Moscow_TASS_3542.JPG/1920px-Moscow_TASS_3542.JPG"
)
_HISTORICAL_MUSEUM = (
    "https://avatars.mds.yandex.net/get-altay/11244149/"
    "2a0000018c1957b167557229d2e63bd15649/orig"
)
_TSARITSYNO_PALACE = (
    "https://cdn.culture.ru/images/"
    "7d3568d7-16f3-5c44-a77a-00431eb359ce"
)
_NARKOMFIN = (
    "https://www.mos.ru/upload/newsfeed/newsfeed/"
    "ac031e59f91440389548f25517d28f57(9).png"
)
_ZUEV_CLUB = (
    "https://i.archi.ru/i/226989.jpg"
)
_MARIINSKY_PALACE = (
    "https://upload.wikimedia.org/wikipedia/commons/e/e9/"
    "St._Petersburg_-_Mariinsky_Palace_-_"
    "%D0%9C%D0%B0%D1%80%D0%B8%D0%B8%D0%BDc%D0%BA%D0%B8%D0%B9_%D0%B4%D0%B2%D0%BE%D1%80%D0%B5%D1%86_-_"
    "panoramio.jpg"
)
_RGB_LIBRARY = (
    "https://live.staticflickr.com/4240/"
    "35255414955_b9a05e8a35_b.jpg"
)
_YAROSLAVSKY = (
    "https://upload.wikimedia.org/wikipedia/commons/9/90/"
    "%D0%AF%D1%80%D0%BE%D1%81%D0%BB%D0%B0%D0%B2%D1%81%D0%BA%D0%B8%D0%B9_%D0%B2%D0%BE%D0%BA%D0%B7%D0%B0%D0%BB_%2820220720135756%29.jpg"
)
_VITEBSKY = (
    "https://upload.wikimedia.org/wikipedia/commons/f/f6/"
    "Vitebsky_Rail_Terminal_Vestibule_1.jpg"
)
_CHRIST_SAVIOR = (
    "https://upload.wikimedia.org/wikipedia/commons/3/3c/"
    "Panoramio_-_V%26A_Dudush_-_Moscow._%D0%A5%D1%80%D0%B0%D0%BC_%D0%A5%D1%80%D0%B8%D1%81%D1%82%D0%B0_%D0%A1%D0%BF%D0%B0%D1%81%D0%B8%D1%82%D0%B5%D0%BB%D1%8F._Moscow._The_Cathedral_of_Christ_the_Saviour.jpg"
)
_RUKAVISHNIK = (
    "https://upload.wikimedia.org/wikipedia/commons/9/9a/"
    "Rukavishnikov_mansion_in_Moscow.jpg"
)
_MHAT = (
    "https://avatars.mds.yandex.net/get-altay/1632633/"
    "2a0000016995e3a28db47dd6524bfa659240/orig"
)
_IGUMNOV = (
    "https://upload.wikimedia.org/wikipedia/commons/0/0c/"
    "Moscow._Igumnov_House_P8100250_2800.jpg"
)
_MOROZOV = (
    "https://upload.wikimedia.org/wikipedia/commons/2/26/"
    "Morozov_Mansion_Vozdvizhenka_str_16_str_1_2016-04-12_2515.jpg"
)
_VASNETSOV = (
    "https://upload.wikimedia.org/wikipedia/commons/b/bf/"
    "%D0%94%D0%BE%D0%BC-%D0%BC%D1%83%D0%B7%D0%B5%D0%B9_%D0%92._%D0%9C._"
    "%D0%92%D0%B0%D1%81%D0%BD%D0%B5%D1%86%D0%BE%D0%B2%D0%B0_%28%D1%84%D0%BE%D1%82%D0%BE_%D0%B0%D0%B2%D0%B3%D1%83%D1%81%D1%82_2024%29.jpg"
)
_YAROSLAVSKY = (
    "https://upload.wikimedia.org/wikipedia/commons/9/90/"
    "%D0%AF%D1%80%D0%BE%D1%81%D0%BB%D0%B0%D0%B2%D1%81%D0%BA%D0%B8%D0%B9_%D0%B2%D0%BE%D0%BA%D0%B7%D0%B0%D0%BB_%2820220720135756%29.jpg"
)
_VITEBSKY = (
    "https://upload.wikimedia.org/wikipedia/commons/f/f6/"
    "Vitebsky_Rail_Terminal_Vestibule_1.jpg"
)
_VTOROV = (
    "https://avatars.mds.yandex.net/get-altay/11551715/"
    "2a00000191beae09e8ef80998fcd5798e46d/orig"
)
_ZIL = (
    "https://gazeta-danilovsky-vestnik.ru/wp-content/uploads/"
    "2022/09/62bb0c1582682c42ddcc5323-scaled.jpg"
)
_ZARYADYE_VIEWPOINT_URLS: tuple[str, str] = (
    "https://avatars.mds.yandex.net/get-altay/934739/"
    "2a0000015eece6b22dded6460617c641affa/orig",
    "https://conceptsandprojects.com/wp-content/uploads/"
    "2020/08/40360_Zaryadye-Park_KP1_12-e1600329160360.jpg",
)

# slug -> (primary_url, secondary_url or None)
IMAGE_URL_OVERRIDES: dict[str, tuple[str, str | None]] = {
    "tent_roof_st_basil": (
        "https://upload.wikimedia.org/wikipedia/commons/"
        "3/3d/Saint_Basil%27s_Cathedral_-_Moscow_-_Russia_-_01.jpg",
        None,
    ),
    "moscow_fifteenth_sixteenth_kremlin_dormition": (
        _KREMLIN_DORMITION,
        _KREMLIN_DORMITION_SECOND,
    ),
    "ancient_rus_vladimir_assumption": (
        _VLADIMIR_ASSUMPTION,
        None,
    ),
    "ancient_rus_moscow_places_of_worship_3_2": (
        _KREMLIN_DORMITION,
        _KREMLIN_DORMITION_SECOND,
    ),
    "petrine_baroque_peter_paul_cathedral": (
        "https://upload.wikimedia.org/wikipedia/commons/"
        "5/5e/Peter_and_Paul_Cathedral_in_Saint_Petersburg.jpg",
        None,
    ),
    "elizabethan_baroque_smolny_cathedral": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/"
        "e/e3/Smolny_2013_1.jpg/1280px-Smolny_2013_1.jpg",
        None,
    ),
    "uzorochye_trinity_nikitniki": (
        "https://um.mos.ru/content/house/media/1649/"
        "163dbeadef408a.jpg",
        None,
    ),
    "uzorochye_moscow_places_of_worship_21_2": (
        "https://live.staticflickr.com/4086/"
        "5210982333_2cfbe14e4f_b.jpg",
        None,
    ),
    "novgorod_school_transfiguration_ilyina": (
        "https://upload.wikimedia.org/wikipedia/commons/"
        "9/9e/Novgorod_Church_of_Transfiguration_on_Ilyina_Street.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/"
        "8/8f/Church_of_the_Transfiguration_on_Ilina_Street.jpg",
    ),
    "regional_soviet_luzhniki_stadium": (
        "https://upload.wikimedia.org/wikipedia/commons/"
        "0/0c/Luzhniki_stadium_Moscow.jpg",
        None,
    ),
    "constructivism_narkomfin": (
        _NARKOMFIN,
        None,
    ),
    "constructivism_zuev_club": (
        _ZUEV_CLUB,
        None,
    ),
    "russo_byzantine_moscow_places_of_worship_0_2": (
        "https://upload.wikimedia.org/wikipedia/commons/"
        "4/4e/Vasilevsky_spusk_and_Cathedral_of_Vasily_the_Blessed.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/"
        "f/f3/St._Basil%27s.jpg",
    ),
    "eclecticism_moscow_osobnjaki_5_2": (_RUKAVISHNIK, None),
    "eclecticism_historical_museum": (_HISTORICAL_MUSEUM, None),
    "eclecticism_moscow_osobnjaki_4_2": (_MOROZOV, None),
    "eclecticism_moscow_osobnjaki_7_2": (_IGUMNOV, None),
    "eclecticism_moscow_buildings_37_2": (_MHAT, None),
    "russo_byzantine_christ_savior": (_CHRIST_SAVIOR, None),
    "neo_russian_yaroslavsky_station": (_YAROSLAVSKY, None),
    "art_nouveau_vitebsky_station": (_VITEBSKY, None),
    "neoclassicism_early20_moscow_osobnjaki_38_2": (_VTOROV, None),
    "neoclassicism_early20_spb_osobnjaki_5_2": (
        _MARIINSKY_PALACE,
        None,
    ),
    "art_nouveau_singer_house": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/"
        "3/3f/Singer_House.jpg/1280px-Singer_House.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/"
        "9/9e/Singer_House%2C_St._Petersburg.jpg/1280px-"
        "Singer_House%2C_St._Petersburg.jpg",
    ),
    "avant_garde_moscow_buildings_33_2": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/"
        "%D0%97%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5_%D0%98%D0%B7%D0%B2%D0%B5%D1%81%D1%82%D0%B8%D0%B9._"
        "%D0%92%D0%B8%D0%B4_%D1%81_%D0%BA%D1%80%D1%8B%D1%88%D0%B8_%D0%BE%D1%82%D0%B5%D0%BB%D1%8F_"
        "%D0%A1%D1%82%D0%B0%D0%BD%D0%B4%D0%90%D1%80%D1%82.jpg/1280px-"
        "%D0%97%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5_%D0%98%D0%B7%D0%B2%D0%B5%D1%81%D1%82%D0%B8%D0%B9._"
        "%D0%92%D0%B8%D0%B4_%D1%81_%D0%BA%D1%80%D1%8B%D1%88%D0%B8_%D0%BE%D1%82%D0%B5%D0%BB%D1%8F_"
        "%D0%A1%D1%82%D0%B0%D0%BD%D0%B4%D0%90%D1%80%D1%82.jpg",
        None,
    ),
    "avant_garde_moscow_buildings_2_2": (
        _HOUSE_ON_EMBANKMENT,
        None,
    ),
    "avant_garde_moscow_buildings_29_2": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/"
        "%D0%97%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5_%D0%A6%D0%B5%D0%BD%D1%82%D1%80%D0%BE%D1%81%D0%BE%D1%8E%D0%B7%D0%B0_"
        "2011-01_2.jpg/1280px-"
        "%D0%97%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5_%D0%A6%D0%B5%D0%BD%D1%82%D1%80%D0%BE%D1%81%D0%BE%D1%8E%D0%B7%D0%B0_"
        "2011-01_2.jpg",
        None,
    ),
    "constructivism_moscow_osobnjaki_25_2": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/"
        "Moscow%2C_Orlikov_Lane%2C_Central_Agricultural_Library_building_%28"
        "31154197020%29.jpg/1280px-Moscow%2C_Orlikov_Lane%2C_Central_"
        "Agricultural_Library_building_%2831154197020%29.jpg",
        None,
    ),
    "stalinist_moscow_railway_stations_4_2": (
        _BELORUSSKY_RAIL,
        None,
    ),
    "stalinist_moscow_buildings_17_2": (
        "https://upload.wikimedia.org/wikipedia/commons/b/b8/"
        "Moscow_-_2024_-_The_Kudrinskaya_high-rise.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/8/8c/"
        "%D0%92%D1%8B%D1%81%D0%BE%D1%82%D0%BA%D0%B0_%D0%BD%D0%B0_%D0%9A%D1%83%D0%B4%D1%80%D0%B8%D0%BD%D1%81%D0%BA%D0%BE%D0%B9_"
        "%D0%BF%D0%BB%D0%BE%D1%89%D0%B0%D0%B4%D0%B8_%D0%B2%D0%B5%D1%87%D0%B5%D1%80%D0%BE%D0%BC_-_panoramio.jpg",
    ),
    "contemporary_zaryadye_park": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/"
        "4/4f/Zaryadye_Park_floating_bridge_Moscow.jpg/1280px-"
        "Zaryadye_Park_floating_bridge_Moscow.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/c/c1/"
        "%D0%9F%D0%B0%D1%80%D0%BA_%D0%97%D0%B0%D1%80%D1%8F%D0%B4%D1%8C%D0%B5_%D0%B2_%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B5._"
        "%D0%A4%D0%BE%D1%82%D0%BE_73.jpg",
    ),
    "post_constructivism_moscow_buildings_2_2": (
        _HOUSE_ON_EMBANKMENT,
        None,
    ),
    "post_constructivism_moscow_osobnjaki_20_2": (
        _POLITKATORZHAN,
        None,
    ),
    "post_constructivism_moscow_osobnjaki_24_2": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/"
        "Moscow_Narkomfin_6891.jpg/1280px-Moscow_Narkomfin_6891.jpg",
        None,
    ),
    "neoclassicism_early20_moscow_buildings_11_2": (
        _STATE_DUMA,
        None,
    ),
    "art_deco_moscow_railway_stations_6_2": (
        _PAVELETSKY_RAIL,
        None,
    ),
    "art_deco_moscow_metro_11_2": (
        _PROSPEKT_MIRA_METRO,
        None,
    ),
    "art_deco_moscow_metro_15_2": (
        _PARK_KULTURY_METRO,
        None,
    ),
    "art_deco_red_army_theater": (
        _RED_ARMY_THEATER,
        None,
    ),
    "stalinist_komsomolskaya_metro": (
        _KOMSOMOLSKAYA_METRO,
        None,
    ),
    "soviet_modernism_tass_building": (
        _TASS_BUILDING,
        None,
    ),
    "stalinist_neoclassicism_moscow_railway_stations_4_2": (
        _BELORUSSKY_RAIL,
        None,
    ),
    "russo_byzantine_moscow_places_of_worship_3_2": (
        _KREMLIN_DORMITION,
        _KREMLIN_DORMITION_SECOND,
    ),
    "soviet_modernism_moscow_viewpoints_1_2": _ZARYADYE_VIEWPOINT_URLS,
    "postmodernism_moscow_viewpoints_1_2": _ZARYADYE_VIEWPOINT_URLS,
    "contemporary_moscow_viewpoints_1_2": _ZARYADYE_VIEWPOINT_URLS,
    "pseudo_russian_moscow_palaces_2_2": (
        "https://upload.wikimedia.org/wikipedia/commons/9/9b/"
        "Tsaritsino_from_helicopter-1.jpg",
        "https://avatars.mds.yandex.net/i?id="
        "1c4579f2690370c21430f17b669292f4_l-4230301-images-thumbs&n=13",
    ),
    "pseudo_russian_moscow_palaces_15_2": (
        _TSARITSYNO_PALACE,
        None,
    ),
    "neo_eclectic_moscow_palaces_2_2": (
        "https://upload.wikimedia.org/wikipedia/commons/b/bc/"
        "%D0%9C%D1%83%D0%B7%D0%B5%D0%B9-%D0%B7%D0%B0%D0%BF%D0%BE%D0%B2%D0%B5%D0%B4%D0%BD%D0%B8%D0%BA_"
        "%D0%A6%D0%B0%D1%80%D0%B8%D1%86%D1%8B%D0%BD%D0%BE_-_panoramio_%284%29.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/"
        "5/5e/Tsaritsyno_Moscow_Grand_Palace.jpg/1280px-"
        "Tsaritsyno_Moscow_Grand_Palace.jpg",
    ),
    "post_constructivism_zil_palace": (_ZIL, None),
    "constructivism_moscow_buildings_2_2": (
        _HOUSE_ON_EMBANKMENT,
        None,
    ),
    "constructivism_moscow_buildings_29_2": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/"
        "%D0%97%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5_%D0%A6%D0%B5%D0%BD%D1%82%D1%80%D0%BE%D1%81%D0%BE%D1%8E%D0%B7%D0%B0_"
        "2011-01_2.jpg/1280px-"
        "%D0%97%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5_%D0%A6%D0%B5%D0%BD%D1%82%D1%80%D0%BE%D1%81%D0%BE%D1%8E%D0%B7%D0%B0_"
        "2011-01_2.jpg",
        None,
    ),
    "art_deco_metro_art_deco": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/"
        "e/ef/Vertical_panorama_of_the_Mayakovskaya_Metro_Station.jpg/"
        "1280px-Vertical_panorama_of_the_Mayakovskaya_Metro_Station.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/"
        "f/f6/MosMetro_KomsomolskayaKL_img2_asv2018-01.jpg/1280px-"
        "MosMetro_KomsomolskayaKL_img2_asv2018-01.jpg",
    ),
    "neo_russian_moscow_osobnjaki_2_2": (_VASNETSOV, None),
    "art_nouveau_moscow_osobnjaki_2_2": (_VASNETSOV, None),
    "uzorochye_terem_palace": (
        "https://um.mos.ru/content/iblock/d2d/temodvo02.jpg",
        None,
    ),
    "naryshkin_baroque_trinity_lykovo": (
        "https://avatars.mds.yandex.net/get-altay/14333651/"
        "2a00000195988c361b1d37d8db94e746e252/XXL_height",
        None,
    ),
    "naryshkin_baroque_intercession_fili": (
        "https://upload.wikimedia.org/wikipedia/commons/e/eb/"
        "Moscow_Church_in_Fili.JPG",
        None,
    ),
    "petrine_baroque_twelve_collegia": (
        "https://upload.wikimedia.org/wikipedia/commons/4/4e/"
        "Building_of_the_Twelve_Collegia_%28from_the_territory_of_"
        "St_Petersburg_State_University%29.jpg",
        None,
    ),
    "avant_garde_moscow_libraries_0_2": (_RGB_LIBRARY, None),
    "soviet_neoclassicism_revival_moscow_libraries_0_2": (
        _RGB_LIBRARY,
        None,
    ),
    "soviet_modernism_moscow_buildings_22_2": (
        "https://griven-russia.com/projects/000020/000020.jpg",
        None,
    ),
}

# slug -> (city, rel_path under city folder) for local copy fallback
PRIMARY_IMAGE_REUSE: dict[str, tuple[str, str]] = {
    "eclecticism_moscow_osobnjaki_5_2": (
        "moscow",
        "images/moscow_osobnjaki/rukavishnikov_2.jpg",
    ),
}
for _slug in _MOSCOW_BUILDINGS_30_SLUGS:
    PRIMARY_IMAGE_REUSE[_slug] = (
        "moscow",
        "images/moscow_buildings/sovetskaya_1.jpg",
    )

PRIMARY_IMAGE_REUSE["moscow_fifteenth_sixteenth_kremlin_dormition"] = (
    "moscow",
    "images/moscow_buildings/kremlin_2.jpg",
)
PRIMARY_IMAGE_REUSE["ancient_rus_moscow_places_of_worship_3_2"] = (
    "moscow",
    "images/moscow_buildings/kremlin_2.jpg",
)
PRIMARY_IMAGE_REUSE["uzorochye_moscow_places_of_worship_21_2"] = (
    "moscow",
    "images/moscow_places_of_worship/simeon_stolpnik_3.jpg",
)

SECOND_IMAGE_REUSE: dict[str, tuple[str, str]] = {
    "neo_eclectic_moscow_palaces_2_2": (
        "moscow",
        "images/moscow_parks/tsaritsyno_3.jpg",
    ),
    "russo_byzantine_moscow_places_of_worship_0_2": (
        "moscow",
        "images/moscow_places_of_worship/st_basil_1.jpg",
    ),
}
for _slug in _MOSCOW_BUILDINGS_30_SLUGS:
    SECOND_IMAGE_REUSE[_slug] = (
        "moscow",
        "images/moscow_buildings/sovetskaya_2.jpg",
    )
PRIMARY_IMAGE_REUSE["stalinist_moscow_buildings_17_2"] = (
    "moscow",
    "images/moscow_buildings/kudrinskaya_3.jpg",
)
SECOND_IMAGE_REUSE["stalinist_moscow_buildings_17_2"] = (
    "moscow",
    "images/moscow_buildings/kudrinskaya_4.jpg",
)


def apply_image_url_overrides(place: dict[str, Any]) -> dict[str, Any]:
    """Set primary/secondary image URLs when an override exists."""
    slug = str(place.get("slug") or "")
    override = IMAGE_URL_OVERRIDES.get(slug)
    if not override and slug in _MOSCOW_BUILDINGS_30_SLUGS:
        override = _SOVETSKAYA_HOTEL_URLS
    if not override:
        return place
    primary, secondary = override
    merged = dict(place)
    merged["image_source_url"] = primary
    if secondary:
        merged["additional_images"] = [{
            "image_rel_path": extra_image_rel(slug),
            "image_source_url": secondary,
        }]
    else:
        merged.pop("additional_images", None)
    return merged
