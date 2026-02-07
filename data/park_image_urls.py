# -*- coding: utf-8 -*-
"""URL изображений 20 парков Москвы (Wikimedia Commons) для загрузки."""

PARK_IMAGE_DOWNLOADS: dict[str, str] = {}
# Placeholder: one working Commons thumb per filename (same image for build)
_base = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/"
    "St_Basil%27s_Cathedral_Moscow_2006.jpg/500px-St_Basil%27s_"
    "Cathedral_Moscow_2006.jpg"
)
for i, key in enumerate([
    "gorky_1.jpg", "vdnh_1.jpg", "kolomenskoye_park_1.jpg", "tsaritsyno_1.jpg",
    "sokolniki_1.jpg", "izmaylovo_park_1.jpg", "losiny_1.jpg", "poklonnaya_1.jpg",
    "neskuchny_1.jpg", "vorobyovy_1.jpg", "kuzminki_1.jpg", "bitsevsky_1.jpg",
    "zaryadye_1.jpg", "aptekarsky_1.jpg", "krasnaya_presnya_1.jpg",
    "ekaterininsky_1.jpg", "sadovniki_1.jpg", "lianozovo_1.jpg",
    "tushino_1.jpg", "khodynka_1.jpg",
], 1):
    PARK_IMAGE_DOWNLOADS[key] = _base

PARK_IMAGE_FALLBACKS: dict[str, list[str]] = {}
