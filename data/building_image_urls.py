# -*- coding: utf-8 -*-
"""URL изображений 50 знаменитых зданий Москвы для загрузки."""

_base = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/"
    "St_Basil%27s_Cathedral_Moscow_2006.jpg/500px-St_Basil%27s_"
    "Cathedral_Moscow_2006.jpg"
)
BUILDING_IMAGE_DOWNLOADS: dict[str, str] = {}
for key in [
    "kremlin_1.jpg", "gum_1.jpg", "dom_nab_1.jpg", "city_1.jpg", "hcs_1.jpg",
    "bolshoy_1.jpg", "mgu_1.jpg", "metropol_1.jpg", "national_1.jpg", "tsum_1.jpg",
    "yaroslavsky_1.jpg", "kazansky_vokzal_1.jpg", "leningradsky_1.jpg",
    "paveletsky_1.jpg", "kievsky_1.jpg", "sev_1.jpg", "white_house_1.jpg",
    "duma_1.jpg", "manezh_1.jpg", "dom_soyuzov_1.jpg", "leningradskaya_1.jpg",
    "ukraina_1.jpg", "mid_1.jpg", "kudrinskaya_1.jpg", "krasnye_vorota_1.jpg",
    "kotelnicheskaya_1.jpg", "basil_1.jpg", "spasskaya_1.jpg", "bkd_1.jpg",
    "meriya_1.jpg", "triumph_arch_1.jpg", "pushkin_museum_b_1.jpg", "leninka_1.jpg",
    "tsra_1.jpg", "patriarch_1.jpg", "english_court_1.jpg", "melnikov_1.jpg",
    "centrosoyuz_1.jpg", "sovetskaya_1.jpg", "gosplan_1.jpg", "rusakov_1.jpg",
    "izvestia_1.jpg", "pekin_1.jpg", "nikolskaya_1.jpg", "telegraph_1.jpg",
    "mhat_1.jpg", "pertsov_1.jpg", "mayakovskaya_1.jpg", "komsomolskaya_1.jpg",
    "kropotkinskaya_1.jpg",
]:
    BUILDING_IMAGE_DOWNLOADS[key] = _base

BUILDING_IMAGE_FALLBACKS: dict[str, list[str]] = {}
