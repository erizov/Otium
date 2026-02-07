# -*- coding: utf-8 -*-
"""URL изображений 30 музеев Москвы (Wikimedia Commons) для загрузки."""

_base = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/"
    "Cathedral_of_Christ_the_Saviour%2C_Moscow%2C_Russia.jpg/"
    "500px-Cathedral_of_Christ_the_Saviour%2C_Moscow%2C_Russia.jpg"
)
MUSEUM_IMAGE_DOWNLOADS: dict[str, str] = {}
for key in [
    "history_1.jpg", "tretyakov_1.jpg", "pushkin_museum_1.jpg", "armory_1.jpg",
    "kolomenskoye_muz_1.jpg", "tsaritsyno_muz_1.jpg", "garage_1.jpg",
    "polytech_1.jpg", "darvin_1.jpg", "cosmos_1.jpg", "borodino_1.jpg",
    "ww2_museum_1.jpg", "moscow_muz_1.jpg", "pushkin_house_1.jpg",
    "gorky_house_1.jpg", "tretyakov_krymsky_1.jpg", "shusev_1.jpg",
    "paleo_1.jpg", "orient_1.jpg", "vasnetsov_1.jpg", "kuskovo_1.jpg",
    "ostankino_1.jpg", "jewish_muz_1.jpg", "icon_muz_1.jpg", "az_muz_1.jpg",
    "presnya_1.jpg", "modern_history_1.jpg", "bulgakov_1.jpg",
    "dom_naberezhnoy_1.jpg", "decorative_1.jpg",
]:
    MUSEUM_IMAGE_DOWNLOADS[key] = _base

MUSEUM_IMAGE_FALLBACKS: dict[str, list[str]] = {}
