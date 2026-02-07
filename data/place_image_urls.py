# -*- coding: utf-8 -*-
"""URL изображений 50 мест Москвы для загрузки."""

_base = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/"
    "St_Basil%27s_Cathedral_Moscow_2006.jpg/500px-St_Basil%27s_"
    "Cathedral_Moscow_2006.jpg"
)
PLACE_IMAGE_DOWNLOADS: dict[str, str] = {}
for key in [
    "red_square_1.jpg", "arbat_1.jpg", "boulevard_ring_1.jpg", "sadovoe_1.jpg",
    "vorobyovy_view_1.jpg", "patriarch_ponds_1.jpg", "chistye_1.jpg",
    "kitay_gorod_1.jpg", "zamoskvorechye_1.jpg", "hamovniki_1.jpg",
    "izmaylovo_kremlin_1.jpg", "winzavod_1.jpg", "artplay_1.jpg",
    "metro_komsomolskaya_1.jpg", "metro_mayakovskaya_1.jpg",
    "metro_novoslobodskaya_1.jpg", "metro_revolution_1.jpg", "neskuchny_view_1.jpg",
    "nikolskaya_st_1.jpg", "tverskaya_1.jpg", "kuznetsky_1.jpg", "detsky_mir_1.jpg",
    "gum_place_1.jpg", "ohotny_1.jpg", "lubyanka_1.jpg", "teatralnaya_1.jpg",
    "manezhnaya_1.jpg", "three_stations_1.jpg", "rizhsky_1.jpg", "alex_garden_1.jpg",
    "zaryadye_park_1.jpg", "moskva_river_1.jpg", "stone_bridge_1.jpg",
    "crimean_bridge_1.jpg", "poklonnaya_1.jpg", "luzhniki_1.jpg",
    "ostankino_tower_1.jpg", "zoo_1.jpg", "aptekarsky_place_1.jpg",
    "tretyakov_area_1.jpg", "prechistenka_1.jpg", "sretensky_1.jpg",
    "rozhdestvensky_1.jpg", "yauza_emb_1.jpg", "city_place_1.jpg",
    "new_arbat_1.jpg", "metro_kropotkinskaya_1.jpg", "metro_arbatskaya_1.jpg",
    "marfo_marinsky_1.jpg", "vdnh_place_1.jpg",
]:
    PLACE_IMAGE_DOWNLOADS[key] = _base

PLACE_IMAGE_FALLBACKS: dict[str, list[str]] = {}
