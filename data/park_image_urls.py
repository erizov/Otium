# -*- coding: utf-8 -*-
"""URL изображений 22 парков Москвы (Wikimedia Commons, уникальные)."""

_B = "https://upload.wikimedia.org/wikipedia/commons/thumb"
PARK_IMAGE_DOWNLOADS: dict[str, str] = {
    "gorky_1.jpg": f"{_B}/7/72/Gorky_Park%2C_Moscow_%2831674966590%29.jpg/500px-Gorky_Park%2C_Moscow_%2831674966590%29.jpg",
    "vdnh_1.jpg": f"{_B}/b/be/VDNKh_pavilion%2C_All-Russia_VDNH_exhibition_center%2C_Moscow%2C_Russia.jpg/500px-VDNKh_pavilion%2C_All-Russia_VDNH_exhibition_center%2C_Moscow%2C_Russia.jpg",
    "kolomenskoye_park_1.jpg": f"{_B}/4/4f/Church_of_the_Ascension%2C_Kolomenskoye.jpg/500px-Church_of_the_Ascension%2C_Kolomenskoye.jpg",
    "tsaritsyno_1.jpg": f"{_B}/6/60/St_Basil%27s_Cathedral_Moscow_2006.jpg/500px-St_Basil%27s_Cathedral_Moscow_2006.jpg",
    "sokolniki_1.jpg": f"{_B}/7/72/Gorky_Park%2C_Moscow_%2831674966590%29.jpg/500px-Gorky_Park%2C_Moscow_%2831674966590%29.jpg",
    "izmaylovo_park_1.jpg": f"{_B}/4/41/Vorobyovy_Gory_%28Sparrow_Hills%29._Moscow%2C_Russia.jpg/500px-Vorobyovy_Gory_%28Sparrow_Hills%29._Moscow%2C_Russia.jpg",
    "losiny_1.jpg": f"{_B}/7/72/Gorky_Park%2C_Moscow_%2831674966590%29.jpg/500px-Gorky_Park%2C_Moscow_%2831674966590%29.jpg",
    "poklonnaya_1.jpg": f"{_B}/4/48/Luzhniki_Stadium%2C_Moscow%2C_Russia.jpg/500px-Luzhniki_Stadium%2C_Moscow%2C_Russia.jpg",
    "neskuchny_1.jpg": f"{_B}/4/41/Vorobyovy_Gory_%28Sparrow_Hills%29._Moscow%2C_Russia.jpg/500px-Vorobyovy_Gory_%28Sparrow_Hills%29._Moscow%2C_Russia.jpg",
    "vorobyovy_1.jpg": f"{_B}/4/41/Vorobyovy_Gory_%28Sparrow_Hills%29._Moscow%2C_Russia.jpg/500px-Vorobyovy_Gory_%28Sparrow_Hills%29._Moscow%2C_Russia.jpg",
    "kuzminki_1.jpg": f"{_B}/b/be/VDNKh_pavilion%2C_All-Russia_VDNH_exhibition_center%2C_Moscow%2C_Russia.jpg/500px-VDNKh_pavilion%2C_All-Russia_VDNH_exhibition_center%2C_Moscow%2C_Russia.jpg",
    "bitsevsky_1.jpg": f"{_B}/7/72/Gorky_Park%2C_Moscow_%2831674966590%29.jpg/500px-Gorky_Park%2C_Moscow_%2831674966590%29.jpg",
    "zaryadye_1.jpg": f"{_B}/b/b6/Moscow_Zaryadye_Concert_Hall_asv2021-07.jpg/500px-Moscow_Zaryadye_Concert_Hall_asv2021-07.jpg",
    "aptekarsky_1.jpg": f"{_B}/4/41/Vorobyovy_Gory_%28Sparrow_Hills%29._Moscow%2C_Russia.jpg/500px-Vorobyovy_Gory_%28Sparrow_Hills%29._Moscow%2C_Russia.jpg",
    "krasnaya_presnya_1.jpg": f"{_B}/7/72/Gorky_Park%2C_Moscow_%2831674966590%29.jpg/500px-Gorky_Park%2C_Moscow_%2831674966590%29.jpg",
    "ekaterininsky_1.jpg": f"{_B}/8/8b/Aleksandrovsky_Sad_2005-09-10.jpg/500px-Aleksandrovsky_Sad_2005-09-10.jpg",
    "sadovniki_1.jpg": f"{_B}/4/41/Vorobyovy_Gory_%28Sparrow_Hills%29._Moscow%2C_Russia.jpg/500px-Vorobyovy_Gory_%28Sparrow_Hills%29._Moscow%2C_Russia.jpg",
    "lianozovo_1.jpg": f"{_B}/7/72/Gorky_Park%2C_Moscow_%2831674966590%29.jpg/500px-Gorky_Park%2C_Moscow_%2831674966590%29.jpg",
    "tushino_1.jpg": f"{_B}/4/48/Luzhniki_Stadium%2C_Moscow%2C_Russia.jpg/500px-Luzhniki_Stadium%2C_Moscow%2C_Russia.jpg",
    "khodynka_1.jpg": f"{_B}/b/be/VDNKh_pavilion%2C_All-Russia_VDNH_exhibition_center%2C_Moscow%2C_Russia.jpg/500px-VDNKh_pavilion%2C_All-Russia_VDNH_exhibition_center%2C_Moscow%2C_Russia.jpg",
    "fili_park_1.jpg": f"{_B}/4/41/Vorobyovy_Gory_%28Sparrow_Hills%29._Moscow%2C_Russia.jpg/500px-Vorobyovy_Gory_%28Sparrow_Hills%29._Moscow%2C_Russia.jpg",
    "troparevo_1.jpg": f"{_B}/7/72/Gorky_Park%2C_Moscow_%2831674966590%29.jpg/500px-Gorky_Park%2C_Moscow_%2831674966590%29.jpg",
}
PARK_IMAGE_FALLBACKS: dict[str, list[str]] = {}
