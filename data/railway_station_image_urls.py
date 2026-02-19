# -*- coding: utf-8 -*-
"""Image URLs filled by place name (Commons, Pixabay, Pexels, Openverse, Pastvu, etc.). Round-robin fallbacks per slot."""

RAILWAY_STATION_IMAGE_DOWNLOADS: dict[str, str] = {
    "belorussky_1.jpg": "https://live.staticflickr.com/3870/14284718169_2c3de612d0_b.jpg",
    "belorussky_2.jpg": "https://upload.wikimedia.org/wikipedia/commons/e/e3/Belorussky_Rail_Terminal_%28%D0%91%D0%B5%D0%BB%D0%BE%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9_%D0%B2%D0%BE%D0%BA%D0%B7%D0%B0%D0%BB%29_%285833421585%29.jpg",
    "belorussky_3.jpg": "https://live.staticflickr.com/3847/14858454037_e2ab7ef087_b.jpg",
    "belorussky_4.jpg": "https://upload.wikimedia.org/wikipedia/commons/7/73/Moscow%2C_EP20_locomotive_at_Ilyicha_depot_%2821237171922%29.jpg",
    "kazansky_1.jpg": "https://live.staticflickr.com/8372/29704295836_7a91d1325f_b.jpg",
    "kazansky_2.jpg": "https://upload.wikimedia.org/wikipedia/commons/9/9e/%D0%9A%D0%B0%D0%B7%D0%B0%D0%BD%D1%81%D0%BA%D0%B8%D0%B9_%D0%B2%D0%BE%D0%BA%D0%B7%D0%B0%D0%BB.JPG",
    "kazansky_3.jpg": "https://upload.wikimedia.org/wikipedia/commons/7/75/Moscow%2C_Kazansky_Rail_Terminal_barricades_%2825346101329%29.jpg",
    "kazansky_4.jpg": "https://live.staticflickr.com/4137/4887942049_0126d93fb1_b.jpg",
    "kievsky_1.jpg": "https://live.staticflickr.com/5604/14925557364_6765406f97_b.jpg",
    "kievsky_2.jpg": "https://live.staticflickr.com/4110/5171724345_62e4c578b8_b.jpg",
    "kievsky_3.jpg": "https://upload.wikimedia.org/wikipedia/commons/1/16/Kiyevsky_station_%28%D0%9A%D0%B8%D0%B5%D0%B2%D1%81%D0%BA%D0%B8%D0%B9_%D0%B2%D0%BE%D0%BA%D0%B7%D0%B0%D0%BB%29%2C_Moscow_%2814925557364%29.jpg",
    "kievsky_4.jpg": "https://upload.wikimedia.org/wikipedia/commons/7/77/%D0%9A%D0%B8%D0%B5%D0%B2%D1%81%D0%BA%D0%B8%D0%B9_%D0%B2%D0%BE%D0%BA%D0%B7%D0%B0%D0%BB_%D0%B2_%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B5.jpg",
    "kursky_1.jpg": "https://upload.wikimedia.org/wikipedia/commons/8/8b/Moscow%2C_Kursky_Rail_Terminal_%2830887128223%29.jpg",
    "kursky_2.jpg": "https://upload.wikimedia.org/wikipedia/commons/8/8f/%D0%9A%D1%83%D1%80%D1%81%D0%BA%D0%B8%D0%B9_%D0%B2%D0%BE%D0%BA%D0%B7%D0%B0%D0%BB_2014.JPG",
    "kursky_3.jpg": "https://live.staticflickr.com/8341/28847501790_0e64be07e5_b.jpg",
    "kursky_4.jpg": "https://upload.wikimedia.org/wikipedia/commons/4/4d/Moscow%2C_Kursky_Rail_Terminal_%2830887128593%29.jpg",
    "leningradsky_1.jpg": "https://live.staticflickr.com/4131/5222992815_9429223fd3_b.jpg",
    "leningradsky_2.jpg": "https://live.staticflickr.com/4153/5222992487_d0277d8cc9_b.jpg",
    "leningradsky_3.jpg": "https://live.staticflickr.com/3800/18897635525_469137ca6d.jpg",
    "leningradsky_4.jpg": "https://upload.wikimedia.org/wikipedia/commons/2/21/%D0%9B%D0%B5%D0%BD%D0%B8%D0%BD%D0%B3%D1%80%D0%B0%D0%B4%D1%81%D0%BA%D0%B8%D0%B9_%D0%B2%D0%BE%D0%BA%D0%B7%D0%B0%D0%BB_%2820220720133300%29.jpg",
    "paveletsky_1.jpg": "https://live.staticflickr.com/8652/15908546523_a71d0219ec_b.jpg",
    "paveletsky_2.jpg": "https://upload.wikimedia.org/wikipedia/commons/e/ed/%D0%9F%D0%B0%D0%B2%D0%B5%D0%BB%D0%B5%D1%86%D0%BA%D0%B8%D0%B9_%D0%B2%D0%BE%D0%BA%D0%B7%D0%B0%D0%BB_-_panoramio.jpg",
    "paveletsky_3.jpg": "https://upload.wikimedia.org/wikipedia/commons/5/5b/Lenin_Funeral_Train%2C_Moscow.JPG",
    "paveletsky_4.jpg": "https://live.staticflickr.com/7465/16215357886_4bf08e13f7_b.jpg",
    "rizhsky_station_1.jpg": "https://upload.wikimedia.org/wikipedia/commons/7/7d/Moscow_Riga_Railway_Terminal_2011.JPG",
    "rizhsky_station_2.jpg": "https://upload.wikimedia.org/wikipedia/commons/4/4e/%D0%AD%D0%9F2%D0%94-0002%2C_%D0%A0%D0%B8%D0%B6%D1%81%D0%BA%D0%B8%D0%B9_%D0%B2%D0%BE%D0%BA%D0%B7%D0%B0%D0%BB.jpg",
    "rizhsky_station_3.jpg": "https://upload.wikimedia.org/wikipedia/commons/4/4d/Moscow_Square_near_Riga_Railway_Terminal_2011.JPG",
    "rizhsky_station_4.jpg": "https://upload.wikimedia.org/wikipedia/commons/2/26/Rizhsky_Rail_Terminal_%28%D0%A0%D0%B8%D0%B6%D1%81%D0%BA%D0%B8%D0%B9_%D0%B2%D0%BE%D0%BA%D0%B7%D0%B0%D0%BB%29_%2830760374543%29.jpg",
    "savyolovsky_1.jpg": "https://upload.wikimedia.org/wikipedia/commons/0/03/%D0%A1%D0%B0%D0%B2%D1%91%D0%BB%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9_%D0%B2%D0%BE%D0%BA%D0%B7%D0%B0%D0%BB_%28%D0%BE%D0%BA%D1%82%D1%8F%D0%B1%D1%80%D1%8C_2016%29.jpg",
    "savyolovsky_2.jpg": "https://live.staticflickr.com/4493/37489352770_cb85fd7539_b.jpg",
    "savyolovsky_3.jpg": "https://live.staticflickr.com/4506/37038405064_1b6be4618d_b.jpg",
    "savyolovsky_4.jpg": "https://live.staticflickr.com/4473/37489352660_b46dfe96ed_b.jpg",
    "yaroslavsky_1.jpg": "https://live.staticflickr.com/3781/18892406212_0b785c247c.jpg",
    "yaroslavsky_2.jpg": "https://upload.wikimedia.org/wikipedia/commons/9/90/%D0%AF%D1%80%D0%BE%D1%81%D0%BB%D0%B0%D0%B2%D1%81%D0%BA%D0%B8%D0%B9_%D0%B2%D0%BE%D0%BA%D0%B7%D0%B0%D0%BB_%2820220720135756%29.jpg",
    "yaroslavsky_3.jpg": "https://live.staticflickr.com/866/26411680347_f577b7406e_b.jpg",
    "yaroslavsky_4.jpg": "https://upload.wikimedia.org/wikipedia/commons/c/c8/Pammene_rhediella_%2826411680347%29.jpg",
}

RAILWAY_STATION_IMAGE_FALLBACKS: dict[str, list[str]] = {
}

