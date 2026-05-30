# -*- coding: utf-8 -*-
"""Image URLs filled by place name (Commons, Pixabay, Pexels, Openverse, Pastvu, etc.). Round-robin fallbacks per slot."""

CEMETERY_IMAGE_DOWNLOADS: dict[str, str] = {
    "armyanskoe_1.jpg": "https://upload.wikimedia.org/wikipedia/commons/9/9d/20220223_Armenian_Cemetery_%28Moscow%29_12.jpg",
    "armyanskoe_2.jpg": "https://live.staticflickr.com/65535/51823052869_8bd9b0a08b_b.jpg",
    "armyanskoe_3.jpg": "https://core-renderer-tiles.maps.yandex.ru/tiles",
    "armyanskoe_4.jpg": "https://upload.wikimedia.org/wikipedia/commons/2/2c/20220223_Armenian_Cemetery_%28Moscow%29_13.jpg",
    "donskoy_cemetery_1.jpg": "https://upload.wikimedia.org/wikipedia/commons/b/b5/%D0%9D%D0%BE%D0%B2%D0%BE%D0%B5_%D0%94%D0%BE%D0%BD%D1%81%D0%BA%D0%BE%D0%B5_%D0%BA%D0%BB%D0%B0%D0%B4%D0%B1%D0%B8%D1%89%D0%B5_%2820.08.06%29_-_panoramio.jpg",
    "donskoy_cemetery_2.jpg": "https://live.staticflickr.com/5684/24078378165_f14dff1f57_b.jpg",
    "donskoy_cemetery_3.jpg": "https://live.staticflickr.com/5824/23782762710_b9a61290b1_b.jpg",
    "donskoy_cemetery_4.jpg": "https://upload.wikimedia.org/wikipedia/commons/a/a8/Donskoye_Cemetery_20201219_173032.jpg",
    "kuntsevo_cemetery_1.jpg": "https://upload.wikimedia.org/wikipedia/commons/3/36/%D0%9D%D0%B0%D0%B4%D0%B3%D1%80%D0%BE%D0%B1%D0%BD%D1%8B%D0%B9_%D0%BF%D0%B0%D0%BC%D1%8F%D1%82%D0%BD%D0%B8%D0%BA_%D0%B0%D0%BB%D1%8C%D0%BF%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%83_%D0%92%D0%B8%D1%82%D0%B0%D0%BB%D0%B8%D1%8E_%D0%90%D0%B1%D0%B0%D0%BB%D0%B0%D0%BA%D0%BE%D0%B2%D1%83%2C_1993._%D0%91%D1%80%D0%BE%D0%BD%D0%B7%D0%B0%2C_%D0%BA%D0%B0%D0%BC%D0%B5%D0%BD%D1%8C._%D0%9A%D1%83%D0%BD%D1%86%D0%B5%D0%B2%D1%81%D0%BA%D0%BE%D0%B5_%D0%BA%D0%BB%D0%B0%D0%B4%D0%B1%D0%B8%D1%89%D0%B5%2C_%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0.jpg",
    "kuntsevo_cemetery_2.jpg": "https://upload.wikimedia.org/wikipedia/commons/4/4c/%D0%9F%D0%B0%D0%BC%D1%8F%D1%82%D0%BD%D0%B8%D0%BA-%D1%81%D0%BA%D1%83%D0%BB%D1%8C%D0%BF%D1%82%D1%83%D1%80%D0%B0_%D0%BF%D0%BE%D1%8D%D1%82%D0%B0_%D0%92%D0%B0%D1%81%D0%B8%D0%BB%D0%B8%D1%8F_%D0%A4%D1%91%D0%B4%D0%BE%D1%80%D0%BE%D0%B2%D0%B0.jpg",
    "kuntsevo_cemetery_3.jpg": "https://img.pastvu.com/d/z/x/u/zxumo325cqiefnvzq1.jpg",
    "kuntsevo_cemetery_4.jpg": "https://images.pexels.com/photos/15402746/pexels-photo-15402746.jpeg",
    "mitinskoe_1.jpg": "https://upload.wikimedia.org/wikipedia/commons/0/0c/%D0%9C%D0%B8%D1%82%D0%B8%D0%BD%D1%81%D0%BA%D0%BE%D0%B5_%D0%BA%D0%BB%D0%B0%D0%B4%D0%B1%D0%B8%D1%89%D0%B5%2C%D0%BC.%D0%9C%D0%B8%D1%82%D0%B8%D0%BD%D0%BE%2C_%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%2C_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F._-_panoramio_-_Oleg_Yu.Novikov_%2818%29.jpg",
    "mitinskoe_2.jpg": "https://avatars.mds.yandex.net/get-altay/14306621/2a000001934adddb8c0ada762ba63e17cb43/orig",
    "mitinskoe_3.jpg": "https://upload.wikimedia.org/wikipedia/commons/b/bc/%D0%9C%D0%B8%D1%82%D0%B8%D0%BD%D1%81%D0%BA%D0%BE%D0%B5_%D0%BA%D0%BB%D0%B0%D0%B4%D0%B1%D0%B8%D1%89%D0%B5%2C%D0%BC.%D0%9C%D0%B8%D1%82%D0%B8%D0%BD%D0%BE%2C_%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%2C_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F._-_panoramio_-_Oleg_Yu.Novikov_%2826%29.jpg",
    "mitinskoe_4.jpg": "https://avatars.mds.yandex.net/get-altay/14306621/2a000001934adddb8c0ada762ba63e17cb43/XXXL",
    "novodevichy_cemetery_1.jpg": "https://live.staticflickr.com/2299/2085486148_63024c336d_b.jpg",
    "novodevichy_cemetery_2.jpg": "https://upload.wikimedia.org/wikipedia/commons/b/b1/Post-2009_gravesite_of_Nikolai_Gogol_in_Novodevichy_Cemetery%2C_Moscow%2C_Russia.jpg",
    "novodevichy_cemetery_3.jpg": "https://live.staticflickr.com/5126/5249657075_3aa830a847_b.jpg",
    "novodevichy_cemetery_4.jpg": "https://upload.wikimedia.org/wikipedia/commons/e/ee/%D0%9D%D0%BE%D0%B2%D0%BE%D0%B4%D0%B5%D0%B2%D0%B8%D1%87%D1%8C%D0%B5_%D0%BA%D0%BB%D0%B0%D0%B4%D0%B1%D0%B8%D1%89%D0%B5_%28%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%29.jpg",
    "pyatnitskoe_1.jpg": "https://upload.wikimedia.org/wikipedia/commons/0/06/Moscow_-_Piatnitskoe_Cemetery_-_Grave_of_Valeryan_Pereverzev_-_2025-05-18_-_p4.jpg",
    "pyatnitskoe_2.jpg": "https://upload.wikimedia.org/wikipedia/commons/1/1d/%D0%9C%D0%BE%D0%B3%D0%B8%D0%BB%D0%B0_%D0%90.%D0%A1._%D0%A2%D1%80%D0%BE%D0%B8%D1%86%D0%BA%D0%BE%D0%B9._%D0%9F%D1%8F%D1%82%D0%BD%D0%B8%D1%86%D0%BA%D0%BE%D0%B5_%D0%BA%D0%BB%D0%B0%D0%B4%D0%B1%D0%B8%D1%89%D0%B5._%D0%9A%D0%B0%D0%BB%D1%83%D0%B3%D0%B0.jpg",
    "pyatnitskoe_3.jpg": "https://core-renderer-tiles.maps.yandex.ru/tiles",
    "pyatnitskoe_4.jpg": "https://upload.wikimedia.org/wikipedia/commons/9/91/Moscow_-_Piatnitskoe_Cemetery_-_Grave_of_Novikovy_-_2025-05-18_-_p2.jpg",
    "troekurovo_1.jpg": "https://upload.wikimedia.org/wikipedia/commons/d/d6/Moscow_20200916_122131.jpg",
    "troekurovo_2.jpg": "https://upload.wikimedia.org/wikipedia/commons/0/03/%D0%A0%D1%83%D0%B4%D0%BD%D0%B5%D0%B2_%D0%AE%D1%80%D0%B8%D0%B9_%D0%98%D0%B2%D0%B0%D0%BD%D0%BE%D0%B2%D0%B8%D1%87_2017_%D0%A2%D1%80%D0%BE%D0%B5%D0%BA%D1%83%D1%80%D0%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%B5_%D0%BA%D0%BB%D0%B0%D0%B4%D0%B1%D0%B8%D1%89%D0%B5.jpg",
    "troekurovo_3.jpg": "https://upload.wikimedia.org/wikipedia/commons/8/86/Moscow_20200916_125023.jpg",
    "troekurovo_4.jpg": "https://upload.wikimedia.org/wikipedia/commons/1/10/%D0%A2%D1%80%D0%BE%D0%B5%D0%BA%D1%83%D1%80%D0%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%B5_%D0%BA%D0%BB%D0%B0%D0%B4%D0%B1%D0%B8%D1%89%D0%B5_%D0%97%D0%B2%D0%B5%D0%BD%D0%B8%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D1%81%D0%BA%D0%B8%D0%B9.jpg",
    "vagankovo_1.jpg": "https://upload.wikimedia.org/wikipedia/commons/8/8f/%D0%92%D0%B0%D0%B3%D0%B0%D0%BD%D1%8C%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%B5_%D0%BA%D0%BB%D0%B0%D0%B4%D0%B1%D0%B8%D1%89%D0%B5_%28crop%29.jpg",
    "vagankovo_2.jpg": "https://upload.wikimedia.org/wikipedia/commons/3/37/%D0%92%D0%B0%D0%B3%D0%B0%D0%BD%D1%8C%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%B5_%D0%BA%D0%BB%D0%B0%D0%B4%D0%B1%D0%B8%D1%89%D0%B5.JPG",
    "vagankovo_3.jpg": "https://upload.wikimedia.org/wikipedia/commons/a/a1/%D0%92%D0%B0%D0%B9%D0%BB%D1%8C_%D0%93._%D0%B8_%D0%A2._-_%D0%92%D0%B0%D0%B3%D0%B0%D0%BD%D1%8C%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%B5_%D0%BA%D0%BB%D0%B0%D0%B4%D0%B1%D0%B8%D1%89%D0%B5.jpg",
    "vagankovo_4.jpg": "https://upload.wikimedia.org/wikipedia/commons/c/ca/%D0%91%D0%B0%D1%83%D0%BC%D0%B0%D0%BD_%D0%9D%D0%B8%D0%BA%D0%BE%D0%BB%D0%B0%D0%B9%2C_%D1%80%D0%B5%D0%B2%D0%BE%D0%BB%D1%8E%D1%86%D0%B8%D0%BE%D0%BD%D0%B5%D1%80._%D0%92%D0%B0%D0%B3%D0%B0%D0%BD%D1%8C%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%B5_%D0%BA%D0%BB%D0%B0%D0%B4%D0%B1%D0%B8%D1%89%D0%B5.jpg",
    "vvedenskoe_1.jpg": "https://upload.wikimedia.org/wikipedia/commons/f/f3/Moscow%2C_Gospitalny_Val_Street%2C_tram_passing_by_the_cemetery_gate_%2894%29.jpg",
    "vvedenskoe_2.jpg": "https://upload.wikimedia.org/wikipedia/commons/f/ff/%D0%9A%D0%BB%D1%8E%D0%B5%D0%B2%D0%B0_%D0%9D.%D0%93._%D0%A0%D0%BE%D1%81%D0%BA%D0%B8%D0%BD_%D0%93.%D0%98._%D0%A0%D0%BE%D1%81%D0%BA%D0%B8%D0%BD_%D0%92.%D0%98._%D0%92%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D1%81%D0%BA%D0%BE%D0%B5_%D0%BA%D0%BB%D0%B0%D0%B4%D0%B1%D0%B8%D1%89%D0%B5_2.JPG",
    "vvedenskoe_3.jpg": "https://core-renderer-tiles.maps.yandex.ru/tiles",
    "vvedenskoe_4.jpg": "https://upload.wikimedia.org/wikipedia/commons/1/1e/%D0%92%D0%B0%D1%81%D0%BD%D0%B5%D1%86%D0%BE%D0%B2_%D0%92%D0%B8%D0%BA%D1%82%D0%BE%D1%80%2C_%D1%85%D1%83%D0%B4%D0%BE%D0%B6%D0%BD%D0%B8%D0%BA._%D0%92%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D1%81%D0%BA%D0%BE%D0%B5_%D0%BA%D0%BB%D0%B0%D0%B4%D0%B1%D0%B8%D1%89%D0%B5.jpg",
}

CEMETERY_IMAGE_FALLBACKS: dict[str, list[str]] = {
    "kuntsevo_cemetery_1.jpg": [
        "https://img.pastvu.com/d/z/x/u/zxumo325cqiefnvzq1.jpg",
        "https://images.pexels.com/photos/15402746/pexels-photo-15402746.jpeg",
    ],
    "kuntsevo_cemetery_2.jpg": [
        "https://images.pexels.com/photos/5059248/pexels-photo-5059248.jpeg",
        "https://img.pastvu.com/d/z/x/u/zxumo325cqiefnvzq1.jpg",
        "https://images.pexels.com/photos/15402746/pexels-photo-15402746.jpeg",
    ],
    "kuntsevo_cemetery_3.jpg": [
        "https://images.pexels.com/photos/5059248/pexels-photo-5059248.jpeg",
        "https://upload.wikimedia.org/wikipedia/commons/3/36/%D0%9D%D0%B0%D0%B4%D0%B3%D1%80%D0%BE%D0%B1%D0%BD%D1%8B%D0%B9_%D0%BF%D0%B0%D0%BC%D1%8F%D1%82%D0%BD%D0%B8%D0%BA_%D0%B0%D0%BB%D1%8C%D0%BF%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%83_%D0%92%D0%B8%D1%82%D0%B0%D0%BB%D0%B8%D1%8E_%D0%90%D0%B1%D0%B0%D0%BB%D0%B0%D0%BA%D0%BE%D0%B2%D1%83%2C_1993._%D0%91%D1%80%D0%BE%D0%BD%D0%B7%D0%B0%2C_%D0%BA%D0%B0%D0%BC%D0%B5%D0%BD%D1%8C._%D0%9A%D1%83%D0%BD%D1%86%D0%B5%D0%B2%D1%81%D0%BA%D0%BE%D0%B5_%D0%BA%D0%BB%D0%B0%D0%B4%D0%B1%D0%B8%D1%89%D0%B5%2C_%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0.jpg",
        "https://images.pexels.com/photos/15402746/pexels-photo-15402746.jpeg",
    ],
    "kuntsevo_cemetery_4.jpg": [
        "https://images.pexels.com/photos/5059248/pexels-photo-5059248.jpeg",
        "https://upload.wikimedia.org/wikipedia/commons/3/36/%D0%9D%D0%B0%D0%B4%D0%B3%D1%80%D0%BE%D0%B1%D0%BD%D1%8B%D0%B9_%D0%BF%D0%B0%D0%BC%D1%8F%D1%82%D0%BD%D0%B8%D0%BA_%D0%B0%D0%BB%D1%8C%D0%BF%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%83_%D0%92%D0%B8%D1%82%D0%B0%D0%BB%D0%B8%D1%8E_%D0%90%D0%B1%D0%B0%D0%BB%D0%B0%D0%BA%D0%BE%D0%B2%D1%83%2C_1993._%D0%91%D1%80%D0%BE%D0%BD%D0%B7%D0%B0%2C_%D0%BA%D0%B0%D0%BC%D0%B5%D0%BD%D1%8C._%D0%9A%D1%83%D0%BD%D1%86%D0%B5%D0%B2%D1%81%D0%BA%D0%BE%D0%B5_%D0%BA%D0%BB%D0%B0%D0%B4%D0%B1%D0%B8%D1%89%D0%B5%2C_%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0.jpg",
        "https://img.pastvu.com/d/z/x/u/zxumo325cqiefnvzq1.jpg",
    ],
}

