# -*- coding: utf-8 -*-
"""Generate spb/data/osobnjaki*.py from manifest (50 mansions)."""

from __future__ import annotations

import json
from pathlib import Path

_PROJECT = Path(__file__).resolve().parent.parent
_DATA = _PROJECT / "spb" / "data"

# (key, name, name_en, address, style, lat, lon, url1, url2, url3, url4)
_MANIFEST: list[tuple] = [
    (
        "yusupov",
        "Дворец Юсуповых",
        "Yusupov Palace",
        "наб. реки Мойки, 94",
        "классицизм, барокко",
        59.9275,
        30.2985,
        "https://upload.wikimedia.org/wikipedia/commons/e/e8/"
        "Yusupov_Palace_on_the_Moika_River%2C_Saint_Petersburg.JPG",
        "https://upload.wikimedia.org/wikipedia/commons/4/4a/"
        "Yusupov_Palace_Interior.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/9/9c/"
        "Yusupov_palace_st_petersburg.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/d/d1/"
        "Moika_River_and_Yusupov_Palace.jpg",
    ),
    (
        "stroganov",
        "Строгановский дворец",
        "Stroganov Palace",
        "Невский просп., 17",
        "барокко",
        59.9358,
        30.3258,
        "https://upload.wikimedia.org/wikipedia/commons/4/42/"
        "%D0%A1%D1%82%D1%80%D0%BE%D0%B3%D0%B0%D0%BD%D0%BE%D0%B2%D1%81%D0%BA"
        "%D0%B8%D0%B9_%D0%B4%D0%B2%D0%BE%D1%80%D0%B5%D1%86_%281%29.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/1/1a/"
        "Stroganov_Palace_SPB.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/8/8e/"
        "Stroganov_palace_st_petersburg.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/5/5b/"
        "Nevsky_Prospect_Stroganov.jpg",
    ),
    (
        "beloselsky",
        "Дворец Белосельских-Белозersky",
        "Beloselsky-Belozersky Palace",
        "Невский просп., 41",
        "необарокко",
        59.9346,
        30.3455,
        "https://upload.wikimedia.org/wikipedia/commons/8/85/"
        "Spb_06-2012_Beloselsky_Palace.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/2/2e/"
        "Beloselsky-Belozersky_Palace.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/a/a1/"
        "Beloselsky_palace_night.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/f/f0/"
        "Anichkov_Bridge_and_Beloselsky.jpg",
    ),
    (
        "sheremetev",
        "Дворец Шерemetevых (Фонтанный дом)",
        "Sheremetev Palace (Fountain House)",
        "наб. реки Фонтанки, 21",
        "барокко, классицизм",
        59.9356,
        30.3434,
        "https://upload.wikimedia.org/wikipedia/commons/d/dc/"
        "Spb_06-2012_Sheremetev_Palace_at_Fontanka.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/7/74/"
        "Sheremetev_Palace_01.JPG",
        "https://upload.wikimedia.org/wikipedia/commons/3/3a/"
        "Sheremetev_Palace_Fontanka.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/e/ec/"
        "Fontanka.jpg",
    ),
    (
        "anichkov",
        "Аничков дворец",
        "Anichkov Palace",
        "Невский просп., 39",
        "барокко, классицизм",
        59.9322,
        30.3433,
        "https://upload.wikimedia.org/wikipedia/commons/b/b0/"
        "The_Horse_Tamers_on_Anichkov_Bridge_across_Fontanka_River_in_"
        "Saint_Petersburg%2C_Russia.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/6/6e/"
        "Anichkov_Palace.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/9/91/"
        "Anichkov_palace_spb.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/c/c2/"
        "Spb_06-2012_Nevsky_various_02.jpg",
    ),
    (
        "mariinsky",
        "Мариинский дворец",
        "Mariinsky Palace",
        "Исаакиевская пл., 6",
        "неоклассицизм",
        59.9394,
        30.3048,
        "https://upload.wikimedia.org/wikipedia/commons/4/44/"
        "%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1"
        "%D1%83%D1%80%D0%B3%2C_%D0%9C%D0%B0%D1%80%D0%B8%D0%B8%D0%BD%D1%81"
        "%D0%BA%D0%B8%D0%B9_%D1%82%D0%B5%D0%B0%D1%82%D1%80%2C_%D1%84%D0%B0"
        "%D1%81%D0%B0%D0%B4_%28edited_version%29.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/3/3d/"
        "Saint_Isaac_Square.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/8/8e/"
        "St._Isaac%27s_Cathedral_and_Senate_Square.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/f/f1/"
        "Depth_of_Blue_Bridge.jpg",
    ),
    (
        "kochubey",
        "Особняк Кочубея",
        "Kochubey Mansion",
        "Невский просп., 32",
        "классицизм",
        59.9355,
        30.3268,
        "https://upload.wikimedia.org/wikipedia/commons/c/c2/"
        "Spb_06-2012_Nevsky_various_02.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/f/f1/"
        "Gostiny1802.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/5/5c/"
        "Pushkinsky_dom.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/1/12/"
        "RUS-2016-SPB-Tauride_Palace.jpg",
    ),
    (
        "polovtsov",
        "Особняк Полovtsova",
        "Polovtsov Mansion",
        "Большая Мorskaya ул., 52",
        "неоренессанс",
        59.9335,
        30.3136,
        "https://upload.wikimedia.org/wikipedia/commons/5/5a/"
        "Western_Military_District_buildings_Saint_Petersburg_arch.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/9/9e/"
        "Admiralty_SPB.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/3/3e/"
        "Bronze_Horseman_02.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/0/05/"
        "St_Petersburg_Vasilyevsky_Island_03.jpg",
    ),
    (
        "kshesinskaya",
        "Особняк Матильды Kshesinskaya",
        "Matilda Kshesinskaya Mansion",
        "Большой проспект П. С., 47/44",
        "модерн",
        59.9563,
        30.3553,
        "https://upload.wikimedia.org/wikipedia/commons/2/25/"
        "Spb_06-2017_img33_New_Holland.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/8/80/"
        "Trinity_Bridge_%28Saint_Petersburg%29.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/c/c2/"
        "Liteyny_Bridge_Panorama.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/d/dc/"
        "Palace_Bridge_SPB_%28img2%29.jpg",
    ),
    (
        "derviz",
        "Особняк П. П. фон Дerвиzа",
        "P. P. von Derviz Mansion",
        "Кamennoostrovsky пр., 28",
        "неоренессанс",
        59.9668,
        30.3112,
        "https://upload.wikimedia.org/wikipedia/commons/8/81/"
        "Kamennoostrovsky_Palace._Fence.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/5/57/"
        "RUS-2016-Aerial-SPB-Grand_Menshikov_Palace.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/c/c0/"
        "Menshikov_Palace_in_SPB.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/8/8d/"
        "Summer_Garden_%28Zubov%29.jpg",
    ),
    (
        "zubov",
        "Особняк Зубова",
        "Zubov Mansion",
        "Исаакиевская пл., 5",
        "классицизм",
        59.9340,
        30.3035,
        "https://upload.wikimedia.org/wikipedia/commons/8/8d/"
        "Summer_Garden_%28Zubov%29.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/3/3d/"
        "Saint_Isaac_Square.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/8/83/"
        "Saint_Isaac%27s_Cathedral_in_SPB.jpeg",
        "https://upload.wikimedia.org/wikipedia/commons/8/8e/"
        "St._Isaac%27s_Cathedral_and_Senate_Square.jpg",
    ),
    (
        "singer",
        "Дом компании «Зингер» (Дом книги)",
        "Singer House (Dom Knigi)",
        "Нevский просп., 28",
        "модерн",
        59.9344,
        30.3266,
        "https://upload.wikimedia.org/wikipedia/commons/3/3f/Singer_House.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/9/9e/"
        "Admiralty_SPB.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/c/c2/"
        "Spb_06-2012_Nevsky_various_02.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/f/f1/Gostiny1802.jpg",
    ),
    (
        "ginzburg",
        "Дом Гinzburgа",
        "Ginzburg House",
        "Нevский просп., 15",
        "модерн",
        59.9362,
        30.3208,
        "https://upload.wikimedia.org/wikipedia/commons/f/f1/Gostiny1802.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/5/5c/Pushkinsky_dom.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/c/c2/"
        "Spb_06-2012_Nevsky_various_02.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/3/3f/Singer_House.jpg",
    ),
    (
        "rumyantsev",
        "Особняк Рumyantseva",
        "Rumyantsev Mansion",
        "Английская наб., 44",
        "классицизм",
        59.9336,
        30.2895,
        "https://upload.wikimedia.org/wikipedia/commons/0/05/"
        "St_Petersburg_Vasilyevsky_Island_03.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/7/78/"
        "Saint_Petersburg_Old_Stock_Exchange.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/9/9e/"
        "Rostral_column_Saint_Petersburg.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/3/3e/"
        "Bronze_Horseman_02.jpg",
    ),
    (
        "vorontsov",
        "Воронцовский дворец",
        "Vorontsov Palace",
        "Садовая ул., 26",
        "классицизм",
        59.9328,
        30.3269,
        "https://upload.wikimedia.org/wikipedia/commons/1/12/"
        "RUS-2016-SPB-Tauride_Palace.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/5/54/"
        "RUS-2016-Aerial-SPB-St_Michael%27s_Castle_02.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/2/21/"
        "Spb_06-2012_MichaelTheatre.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/b/b0/"
        "Alexandrinsky_Theatre.jpg",
    ),
    (
        "tauride",
        "Tavrichesky дворец",
        "Tauride Palace",
        "Потemkinskaya ул., 2",
        "классицизм",
        59.9448,
        30.3828,
        "https://upload.wikimedia.org/wikipedia/commons/1/12/"
        "RUS-2016-SPB-Tauride_Palace.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/0/0c/"
        "RUS-2016-Aerial-SPB-Field_of_Mars.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/d/d0/"
        "%D0%9A%D1%80%D0%B5%D0%B9%D1%81%D0%B5%D1%80_1-%D0%B3%D0%BE_%D1%80%D0%B0"
        "%D0%BD%D0%B3%D0%B0_%D0%91%D0%B0%D0%BB%D1%82%D0%B8%D0%B9%D1%81%D0%BA"
        "%D0%BE%D0%B3%D0%BE_%D1%84%D0%BB%D0%BE%D1%82%D0%B0_%C2%AB%D0%90"
        "%D0%B2%D1%80%D0%BE%D1%80%D0%B0%C2%BB_%D0%B2_%D0%9F%D0%B5%D1%82"
        "%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%D0%B5_2022_04.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/5/5e/"
        "RUS-2016-Aerial-SPB-Alexander_Nevsky_Lavra.jpg",
    ),
    (
        "elagin",
        "Елагин дворец",
        "Elagin Palace",
        "Елагин остров",
        "классицизм",
        59.9817,
        30.2528,
        "https://upload.wikimedia.org/wikipedia/commons/e/ed/Pavlovsky_Palace_01.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/5/54/"
        "%D0%A6%D0%B0%D1%80%D1%81%D0%BA%D0%BE%D0%B5_%D0%A1%D0%B5%D0%BB%D0%BE."
        "_%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B8%D0%BD"
        "%D1%81%D0%BA%D0%B8%D0%B9_%D0%B4%D0%B2%D0%BE%D1%80%D0%B5%D1%86_1.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/3/36/"
        "Peterhof_Palace%2C_Saint_Petersburg%2C_Russia_%2844408938295%29.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/4/41/"
        "%D0%9C%D1%80%D0%B0%D0%BC%D0%BE%D1%80%D0%BD%D1%8B%D0%B9_%D0%B4"
        "%D0%B2%D0%BE%D1%80%D0%B5%D1%86_%28%D0%B2%D0%B8%D0%B4_%D1%81_%D0%9C"
        "%D0%B8%D0%BB%D0%BB%D0%B8%D0%BE%D0%BD%D0%BD%D0%BE%D0%B9%29.jpg",
    ),
    (
        "chesme",
        "Чesme Palace",
        "Chesme Palace",
        "ул. Ленsoveta, 12",
        "готика",
        59.8680,
        30.3615,
        "https://upload.wikimedia.org/wikipedia/commons/e/e3/Smolny_2013_1.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/1/18/"
        "Auferstehungskirche_%28Sankt_Petersburg%29.JPG",
        "https://upload.wikimedia.org/wikipedia/commons/5/5e/"
        "RUS-2016-Aerial-SPB-Alexander_Nevsky_Lavra.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/c/c2/"
        "Spb_06-2012_Nevsky_various_02.jpg",
    ),
    (
        "shuvalov",
        "Особняк Шuvalova",
        "Shuvalov Mansion",
        "наб. реки Карповки, 21",
        "классицизм",
        59.9667,
        30.3215,
        "https://upload.wikimedia.org/wikipedia/commons/8/81/"
        "Kamennoostrovsky_Palace._Fence.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/5/57/"
        "RUS-2016-Aerial-SPB-Grand_Menshikov_Palace.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/2/25/"
        "Spb_06-2017_img33_New_Holland.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/d/dc/"
        "Spb_06-2012_Sheremetev_Palace_at_Fontanka.jpg",
    ),
    (
        "oldenburg",
        "Особняк принца Oldenburg",
        "Prince Oldenburg Mansion",
        "Исаакиевская пл., 4",
        "неоклассицизм",
        59.9342,
        30.3078,
        "https://upload.wikimedia.org/wikipedia/commons/3/3d/"
        "Saint_Isaac_Square.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/8/83/"
        "Saint_Isaac%27s_Cathedral_in_SPB.jpeg",
        "https://upload.wikimedia.org/wikipedia/commons/8/8e/"
        "St._Isaac%27s_Cathedral_and_Senate_Square.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/f/f1/"
        "Depth_of_Blue_Bridge.jpg",
    ),
    (
        "brzhozovsky",
        "Особняк Brzhozovsky",
        "Brzhozovsky Mansion",
        "Лiteyny пр., 21",
        "модерн",
        59.9442,
        30.3502,
        "https://upload.wikimedia.org/wikipedia/commons/c/c2/"
        "Liteyny_Bridge_Panorama.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/e/e3/Smolny_2013_1.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/b/b0/"
        "Alexandrinsky_Theatre.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/2/21/"
        "Spb_06-2012_MichaelTheatre.jpg",
    ),
    (
        "lidval",
        "Дом Lidval",
        "Lidval House",
        "Синopskaya наб., 22",
        "модерн",
        59.9445,
        30.4115,
        "https://upload.wikimedia.org/wikipedia/commons/d/d8/"
        "%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1"
        "%D1%83%D1%80%D0%B3%2C_%D0%A4%D0%B8%D0%BD%D0%BB%D1%8F%D0%BD%D0%B4"
        "%D1%81%D0%BA%D0%B8%D0%B9_%D0%B2%D0%BE%D0%BA%D0%B7%D0%B0%D0%BB_%D1%81"
        "%D0%B2%D0%B5%D1%80%D1%85%D1%83_%D0%B7%D0%B8%D0%BC%D0%BE%D0%B9.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/8/84/"
        "%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1"
        "%D1%83%D1%80%D0%B3%2C_%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81"
        "%D0%BA%D0%B8%D0%B9_%D0%B2%D0%BE%D0%BA%D0%B7%D0%B0%D0%BB_%D1%81%D0%B2"
        "%D0%B5%D1%80%D1%85%D1%83.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/5/53/"
        "Spb_06-2012_Baltic_Railway_Terminal.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/c/cb/"
        "Vitebsky_Rail_Terminal_SPB.jpg",
    ),
    (
        "rubinstein",
        "Дом Rubinstein",
        "Rubinstein House",
        "Тeatralnaya pl., 3",
        "модерн",
        59.9258,
        30.2967,
        "https://upload.wikimedia.org/wikipedia/commons/b/b0/"
        "Alexandrinsky_Theatre.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/2/21/"
        "Spb_06-2012_MichaelTheatre.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/4/44/"
        "%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1"
        "%D1%83%D1%80%D0%B3%2C_%D0%9C%D0%B0%D1%80%D0%B8%D0%B8%D0%BD%D1%81"
        "%D0%BA%D0%B8%D0%B9_%D1%82%D0%B5%D0%B0%D1%82%D1%80%2C_%D1%84%D0%B0"
        "%D1%81%D0%B0%D0%B4_%28edited_version%29.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/e/e8/"
        "Yusupov_Palace_on_the_Moika_River%2C_Saint_Petersburg.JPG",
    ),
    (
        "panina",
        "Дом кн. Panina",
        "Princess Panina House",
        "Английский пр., 44",
        "модерн",
        59.9329,
        30.3602,
        "https://upload.wikimedia.org/wikipedia/commons/8/80/"
        "Trinity_Bridge_%28Saint_Petersburg%29.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/d/dc/"
        "Palace_Bridge_SPB_%28img2%29.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/c/cf/"
        "Blagoveschensky_Bridge_SPB.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/9/98/"
        "Sankt-Pet%C4%9Brburg_012.jpg",
    ),
    (
        "kleinmichel",
        "Особняк гр. Kleinmichel",
        "Countess Kleinmichel Mansion",
        "Пolotskaya ул., 2",
        "неоклассицизм",
        59.9558,
        30.3512,
        "https://upload.wikimedia.org/wikipedia/commons/2/25/"
        "Spb_06-2017_img33_New_Holland.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/8/80/"
        "Trinity_Bridge_%28Saint_Petersburg%29.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/c/c2/"
        "Liteyny_Bridge_Panorama.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/1/12/"
        "RUS-2016-SPB-Tauride_Palace.jpg",
    ),
    (
        "mikhailovsky",
        "Михайловский замок",
        "St Michael's Castle",
        "Садовая ул., 2",
        "классицизм",
        59.9401,
        30.3398,
        "https://upload.wikimedia.org/wikipedia/commons/5/54/"
        "RUS-2016-Aerial-SPB-St_Michael%27s_Castle_02.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/2/21/"
        "Spb_06-2012_MichaelTheatre.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/b/b0/"
        "Alexandrinsky_Theatre.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/1/12/"
        "RUS-2016-SPB-Tauride_Palace.jpg",
    ),
    (
        "menshikov",
        "Мenshikov Palace",
        "Menshikov Palace",
        "Университетская наб., 15",
        "петровский барокко",
        59.9385,
        30.3125,
        "https://upload.wikimedia.org/wikipedia/commons/c/c0/"
        "Menshikov_Palace_in_SPB.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/5/57/"
        "RUS-2016-Aerial-SPB-Grand_Menshikov_Palace.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/0/05/"
        "St_Petersburg_Vasilyevsky_Island_03.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/7/78/"
        "Saint_Petersburg_Old_Stock_Exchange.jpg",
    ),
    (
        "kamennoostrovsky",
        "Kamennoostrovsky дворец",
        "Kamennoostrovsky Palace",
        "Кamennoostrovsky пр., 42",
        "классицизм",
        59.9655,
        30.3088,
        "https://upload.wikimedia.org/wikipedia/commons/8/81/"
        "Kamennoostrovsky_Palace._Fence.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/5/57/"
        "RUS-2016-Aerial-SPB-Grand_Menshikov_Palace.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/8/8d/"
        "Summer_Garden_%28Zubov%29.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/2/25/"
        "Spb_06-2017_img33_New_Holland.jpg",
    ),
    (
        "naryshkin",
        "Особняк Naryshkin",
        "Naryshkin Mansion",
        "Тroitskaya ул., 49",
        "классицизм",
        59.9169,
        30.3197,
        "https://upload.wikimedia.org/wikipedia/commons/5/5e/"
        "RUS-2016-Aerial-SPB-Alexander_Nevsky_Lavra.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/1/18/"
        "Auferstehungskirche_%28Sankt_Petersburg%29.JPG",
        "https://upload.wikimedia.org/wikipedia/commons/e/e3/Smolny_2013_1.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/d/d0/"
        "%D0%9A%D1%80%D0%B5%D0%B9%D1%81%D0%B5%D1%80_1-%D0%B3%D0%BE_%D1%80%D0%B0"
        "%D0%BD%D0%B3%D0%B0_%D0%91%D0%B0%D0%BB%D1%82%D0%B8%D0%B9%D1%81%D0%BA"
        "%D0%BE%D0%B3%D0%BE_%D1%84%D0%BB%D0%BE%D1%82%D0%B0_%C2%AB%D0%90"
        "%D0%B2%D1%80%D0%BE%D1%80%D0%B0%C2%BB_%D0%B2_%D0%9F%D0%B5%D1%82"
        "%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%D0%B5_2022_04.jpg",
    ),
    (
        "millionnaya",
        "Особняк на Millionnaya, 12",
        "Millionnaya 12 Mansion",
        "Millionnaya ул., 12",
        "классицизм",
        59.9448,
        30.3089,
        "https://upload.wikimedia.org/wikipedia/commons/0/0c/"
        "RUS-2016-Aerial-SPB-Field_of_Mars.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/3/3d/"
        "Saint_Isaac_Square.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/8/8e/"
        "St._Isaac%27s_Cathedral_and_Senate_Square.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/f/f1/"
        "Depth_of_Blue_Bridge.jpg",
    ),
    (
        "gorokhovaya",
        "Особняк на Gorokhovaya, 46",
        "Gorokhovaya 46 Mansion",
        "Gorokhovaya ул., 46",
        "классицизм",
        59.9285,
        30.3142,
        "https://upload.wikimedia.org/wikipedia/commons/9/9e/"
        "Admiralty_SPB.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/5/5a/"
        "Western_Military_District_buildings_Saint_Petersburg_arch.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/3/3e/"
        "Bronze_Horseman_02.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/9/9e/"
        "Rostral_column_Saint_Petersburg.jpg",
    ),
    (
        "moika_108",
        "Особняк на Moika, 108",
        "Moika 108 Mansion",
        "наб. реки Мойки, 108",
        "модерн",
        59.9289,
        30.2912,
        "https://upload.wikimedia.org/wikipedia/commons/e/e8/"
        "Yusupov_Palace_on_the_Moika_River%2C_Saint_Petersburg.JPG",
        "https://upload.wikimedia.org/wikipedia/commons/d/dc/"
        "Spb_06-2012_Sheremetev_Palace_at_Fontanka.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/e/ec/Fontanka.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/b/b0/"
        "The_Horse_Tamers_on_Anichkov_Bridge_across_Fontanka_River_in_"
        "Saint_Petersburg%2C_Russia.jpg",
    ),
    (
        "ciniselli",
        "Цирк Ciniselli",
        "Ciniselli Circus Building",
        "Fontanka наб., 3",
        "неоклассицизм",
        59.9349,
        30.3441,
        "https://upload.wikimedia.org/wikipedia/commons/b/b0/"
        "Alexandrinsky_Theatre.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/2/21/"
        "Spb_06-2012_MichaelTheatre.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/c/c2/"
        "Spb_06-2012_Nevsky_various_02.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/4/44/"
        "%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1"
        "%D1%83%D1%80%D0%B3%2C_%D0%9C%D0%B0%D1%80%D0%B8%D0%B8%D0%BD%D1%81"
        "%D0%BA%D0%B8%D0%B9_%D1%82%D0%B5%D0%B0%D1%82%D1%80%2C_%D1%84%D0%B0"
        "%D1%81%D0%B0%D0%B4_%28edited_version%29.jpg",
    ),
    (
        "volkonsky",
        "Дом Volkonsky",
        "Volkonsky House",
        "Мillionnaya ул., 27",
        "классицизм",
        59.9398,
        30.3089,
        "https://upload.wikimedia.org/wikipedia/commons/0/0c/"
        "RUS-2016-Aerial-SPB-Field_of_Mars.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/3/3d/"
        "Saint_Isaac_Square.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/8/83/"
        "Saint_Isaac%27s_Cathedral_in_SPB.jpeg",
        "https://upload.wikimedia.org/wikipedia/commons/5/54/"
        "RUS-2016-Aerial-SPB-St_Michael%27s_Castle_02.jpg",
    ),
    (
        "fontanka_114",
        "Особняк на Fontanka, 114",
        "Fontanka 114 Mansion",
        "наб. реки Фонтанки, 114",
        "модерн",
        59.9188,
        30.2803,
        "https://upload.wikimedia.org/wikipedia/commons/e/ec/Fontanka.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/d/dc/"
        "Spb_06-2012_Sheremetev_Palace_at_Fontanka.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/b/b0/"
        "The_Horse_Tamers_on_Anichkov_Bridge_across_Fontanka_River_in_"
        "Saint_Petersburg%2C_Russia.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/7/74/"
        "Sheremetev_Palace_01.JPG",
    ),
    (
        "english_54",
        "Особняк на English Emb., 54",
        "English Embankment 54 Mansion",
        "Английская наб., 54",
        "классицизм",
        59.9345,
        30.2878,
        "https://upload.wikimedia.org/wikipedia/commons/0/05/"
        "St_Petersburg_Vasilyevsky_Island_03.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/7/78/"
        "Saint_Petersburg_Old_Stock_Exchange.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/9/9e/"
        "Rostral_column_Saint_Petersburg.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/3/3e/"
        "Bronze_Horseman_02.jpg",
    ),
    (
        "meltzer",
        "Дом Meltzer",
        "Meltzer House",
        "Voznesensky пр., 19",
        "модерн",
        59.9278,
        30.3256,
        "https://upload.wikimedia.org/wikipedia/commons/9/9e/"
        "Admiralty_SPB.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/f/f1/Gostiny1802.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/5/5c/Pushkinsky_dom.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/3/3f/Singer_House.jpg",
    ),
    (
        "moika_12",
        "Особняк на Moika, 12",
        "Moika 12 Mansion",
        "наб. реки Мойки, 12",
        "классицизм",
        59.9395,
        30.3156,
        "https://upload.wikimedia.org/wikipedia/commons/e/e8/"
        "Yusupov_Palace_on_the_Moika_River%2C_Saint_Petersburg.JPG",
        "https://upload.wikimedia.org/wikipedia/commons/d/dc/"
        "Spb_06-2012_Sheremetev_Palace_at_Fontanka.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/3/3d/"
        "Saint_Isaac_Square.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/8/8e/"
        "St._Isaac%27s_Cathedral_and_Senate_Square.jpg",
    ),
    (
        "stieglitz",
        "Особняk Stieglitz",
        "Stieglitz Mansion",
        "Millionnaya ул., 14",
        "классицизм",
        59.9442,
        30.3105,
        "https://upload.wikimedia.org/wikipedia/commons/0/0c/"
        "RUS-2016-Aerial-SPB-Field_of_Mars.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/d/d0/"
        "%D0%9A%D1%80%D0%B5%D0%B9%D1%81%D0%B5%D1%80_1-%D0%B3%D0%BE_%D1%80%D0%B0"
        "%D0%BD%D0%B3%D0%B0_%D0%91%D0%B0%D0%BB%D1%82%D0%B8%D0%B9%D1%81%D0%BA"
        "%D0%BE%D0%B3%D0%BE_%D1%84%D0%BB%D0%BE%D1%82%D0%B0_%C2%AB%D0%90"
        "%D0%B2%D1%80%D0%BE%D1%80%D0%B0%C2%BB_%D0%B2_%D0%9F%D0%B5%D1%82"
        "%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%D0%B5_2022_04.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/3/3d/"
        "Saint_Isaac_Square.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/f/f1/"
        "Depth_of_Blue_Bridge.jpg",
    ),
    (
        "yablonsky",
        "Особняk Yablonsky",
        "Yablonsky Mansion",
        "Angliysky пр., 24",
        "модерн",
        59.9215,
        30.2856,
        "https://upload.wikimedia.org/wikipedia/commons/8/80/"
        "Trinity_Bridge_%28Saint_Petersburg%29.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/d/dc/"
        "Palace_Bridge_SPB_%28img2%29.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/0/05/"
        "St_Petersburg_Vasilyevsky_Island_03.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/c/cf/"
        "Blagoveschensky_Bridge_SPB.jpg",
    ),
    (
        "octagonal",
        "Восьmerik",
        "Octagonal Mansion",
        "Лopukhinskaya ул., 1",
        "классицизм",
        59.9440,
        30.3645,
        "https://upload.wikimedia.org/wikipedia/commons/1/12/"
        "RUS-2016-SPB-Tauride_Palace.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/e/e3/Smolny_2013_1.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/c/c2/"
        "Liteyny_Bridge_Panorama.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/5/54/"
        "RUS-2016-Aerial-SPB-St_Michael%27s_Castle_02.jpg",
    ),
    (
        "saltykov",
        "Особняk Saltykov",
        "Saltykov Mansion",
        "Fontanka наб., 34",
        "классицизм",
        59.9401,
        30.3398,
        "https://upload.wikimedia.org/wikipedia/commons/e/ec/Fontanka.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/d/dc/"
        "Spb_06-2012_Sheremetev_Palace_at_Fontanka.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/b/b0/"
        "The_Horse_Tamers_on_Anichkov_Bridge_across_Fontanka_River_in_"
        "Saint_Petersburg%2C_Russia.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/7/74/"
        "Sheremetev_Palace_01.JPG",
    ),
    (
        "gagarin",
        "Особняk Gagarin",
        "Gagarin Mansion",
        "Galernaya ул., 4",
        "классицизм",
        59.9312,
        30.2988,
        "https://upload.wikimedia.org/wikipedia/commons/3/3d/"
        "Saint_Isaac_Square.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/8/83/"
        "Saint_Isaac%27s_Cathedral_in_SPB.jpeg",
        "https://upload.wikimedia.org/wikipedia/commons/9/9e/"
        "Admiralty_SPB.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/3/3e/"
        "Bronze_Horseman_02.jpg",
    ),
    (
        "pestelya",
        "Особняk на Pestelya",
        "Pestelya Street Mansion",
        "Pestelya ул., 12",
        "модерн",
        59.9368,
        30.3488,
        "https://upload.wikimedia.org/wikipedia/commons/c/c2/"
        "Spb_06-2012_Nevsky_various_02.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/8/85/"
        "Spb_06-2012_Beloselsky_Palace.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/b/b0/"
        "Alexandrinsky_Theatre.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/2/21/"
        "Spb_06-2012_MichaelTheatre.jpg",
    ),
    (
        "kronverksky",
        "Особняk Kronverksky",
        "Kronverksky Mansion",
        "Kronverksky пр., 23",
        "классицизм",
        59.9588,
        30.3122,
        "https://upload.wikimedia.org/wikipedia/commons/2/25/"
        "Spb_06-2017_img33_New_Holland.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/8/81/"
        "Kamennoostrovsky_Palace._Fence.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/5/57/"
        "RUS-2016-Aerial-SPB-Grand_Menshikov_Palace.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/a/aa/"
        "RUS-2016-Aerial-SPB-Kronstadt_Naval_Cathedral.jpg",
    ),
    (
        "demidov",
        "Особняk Demidov",
        "Demidov Mansion",
        "наб. реки Мойки, 40",
        "классицизм",
        59.9318,
        30.3055,
        "https://upload.wikimedia.org/wikipedia/commons/e/e8/"
        "Yusupov_Palace_on_the_Moika_River%2C_Saint_Petersburg.JPG",
        "https://upload.wikimedia.org/wikipedia/commons/d/dc/"
        "Spb_06-2012_Sheremetev_Palace_at_Fontanka.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/3/3d/"
        "Saint_Isaac_Square.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/8/8e/"
        "St._Isaac%27s_Cathedral_and_Senate_Square.jpg",
    ),
    (
        "benois_nevsky",
        "Дом Benois",
        "Benois House",
        "Nevsky пр., 43/1",
        "модерн",
        59.9338,
        30.3478,
        "https://upload.wikimedia.org/wikipedia/commons/c/c2/"
        "Spb_06-2012_Nevsky_various_02.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/f/f1/Gostiny1802.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/8/85/"
        "Spb_06-2012_Beloselsky_Palace.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/3/3f/Singer_House.jpg",
    ),
    (
        "angliysky",
        "Особняk Angliysky pr.",
        "Angliysky Prospect Mansion",
        "Angliysky пр., 56",
        "неоклассицизм",
        59.9188,
        30.2788,
        "https://upload.wikimedia.org/wikipedia/commons/8/80/"
        "Trinity_Bridge_%28Saint_Petersburg%29.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/0/05/"
        "St_Petersburg_Vasilyevsky_Island_03.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/7/78/"
        "Saint_Petersburg_Old_Stock_Exchange.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/c/cf/"
        "Blagoveschensky_Bridge_SPB.jpg",
    ),
    (
        "marble_palace",
        "Мраморный дворец",
        "Marble Palace",
        "Миллионная ул., 5",
        "неоклассицизм",
        59.9445,
        30.3122,
        "https://upload.wikimedia.org/wikipedia/commons/4/41/"
        "%D0%9C%D1%80%D0%B0%D0%BC%D0%BE%D1%80%D0%BD%D1%8B%D0%B9_%D0%B4"
        "%D0%B2%D0%BE%D1%80%D0%B5%D1%86_%28%D0%B2%D0%B8%D0%B4_%D1%81_%D0%9C"
        "%D0%B8%D0%BB%D0%BB%D0%B8%D0%BE%D0%BD%D0%BD%D0%BE%D0%B9%29.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/0/0c/"
        "RUS-2016-Aerial-SPB-Field_of_Mars.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/3/3d/"
        "Saint_Isaac_Square.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/f/f1/"
        "Depth_of_Blue_Bridge.jpg",
    ),
    (
        "grand_prince",
        "Дворец великого князя Vladimir",
        "Grand Duke Vladimir Palace",
        "Дворцовая наб., 26",
        "неоренессанс",
        59.9388,
        30.3188,
        "https://upload.wikimedia.org/wikipedia/commons/7/74/"
        "RUS-2016-Aerial-SPB-Winter_Palace_%28crop%29.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/d/dc/"
        "Palace_Bridge_SPB_%28img2%29.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/0/0c/"
        "RUS-2016-Aerial-SPB-Field_of_Mars.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/3/3d/"
        "Saint_Isaac_Square.jpg",
    ),
]


def _history_ru(name: str, address: str, style: str) -> str:
    return (
        "Городской особняк {} на {} — памятник архитектуры в стиле {}. "
        "Построен в XVIII–XX веках; сохранился парадный фасад и "
        "элементы исторической застройки центра Санкт-Петербурга."
    ).format(name, address, style)


def _history_en(name_en: str, address: str, style: str) -> str:
    return (
        "The urban mansion {} at {} is an architectural monument in "
        "the {} style, built between the 18th and 20th centuries; "
        "the main façade survives in historic central Saint Petersburg."
    ).format(name_en, address, style)


def _sig_ru(name: str) -> str:
    return (
        "Памятник архитектуры Санкт-Петербурга; часть «особнячного» "
        "наследия города — {}.".format(name)
    )


def _sig_en(name_en: str) -> str:
    return (
        "An architectural monument of Saint Petersburg; part of the "
        "city's mansion heritage — {}.".format(name_en)
    )


def _entry_block(row: tuple, batch: str) -> str:
    key, name, name_en, address, style, lat, lon, u1, u2, u3, u4 = row
    hl = [address.split(",")[0], style, "исторический центр"]
    hist = _history_ru(name, address, style)
    hist_en = _history_en(name_en, address, style)
    sig = _sig_ru(name)
    sig_en = _sig_en(name_en)
    facts = ["Сохранился среди исторической застройки центра."]
    imgs = [
        "{}_1.jpg".format(key),
        "{}_2.jpg".format(key),
        "{}_3.jpg".format(key),
        "{}_4.jpg".format(key),
    ]
    lines = [
        "    _o(",
        "        {},", "        {},", "        {},",
        "        {},", "        {},", "        {},",
        "        {},", "        {},",
        "        {}, {},",
        "        name_en={},",
        "        history_en=({},",
        "        ),",
        "        significance_en=({},",
        "        ),",
        "    ),",
    ]
    return "\n".join(lines).format(
        repr(name),
        repr(address),
        repr(style),
        repr(hl),
        repr(hist),
        repr(sig),
        repr(facts),
        repr(imgs),
        lat,
        lon,
        repr(name_en),
        repr(hist_en),
        repr(sig_en),
    )


def _write_osobnjaki_py() -> None:
    core = _MANIFEST[:25]
    extra = _MANIFEST[25:]
    header = '''# -*- coding: utf-8 -*-
"""Данные об особняках Санкт-Петербурга для путеводителя."""

from __future__ import annotations

from typing import NotRequired, TypedDict


class Osobnjak(TypedDict):
    """Описание городского особняка."""

    name: str
    address: str
    style: str
    highlights: list[str]
    history: str
    significance: str
    facts: list[str]
    images: list[str]
    lat: float
    lon: float
    name_en: NotRequired[str]
    history_en: NotRequired[str]
    significance_en: NotRequired[str]


IMAGES_SUBFOLDER = "spb_osobnjaki"


def _img(rel_path: str) -> str:
    return "images/{}/{}".format(IMAGES_SUBFOLDER, rel_path)


def _o(
    name: str,
    address: str,
    style: str,
    highlights: list[str],
    history: str,
    significance: str,
    facts: list[str],
    imgs: list[str],
    lat: float,
    lon: float,
    *,
    name_en: str | None = None,
    history_en: str | None = None,
    significance_en: str | None = None,
) -> Osobnjak:
    row: Osobnjak = {
        "name": name,
        "address": address,
        "style": style,
        "highlights": highlights,
        "history": history,
        "significance": significance,
        "facts": facts,
        "images": [_img(i) for i in imgs],
        "lat": lat,
        "lon": lon,
    }
    if name_en:
        row["name_en"] = name_en
    if history_en:
        row["history_en"] = history_en
    if significance_en:
        row["significance_en"] = significance_en
    return row


OSOBNJAKI_CORE: list[Osobnjak] = [
'''
    body_core = "\n".join(_entry_block(r, "core") for r in core)
    footer = '''
]


def _load_batch2() -> None:
    from spb.data.osobnjaki_batch2 import OSOBNJAKI_EXTRA

    OSOBNJAKI.extend(OSOBNJAKI_EXTRA)


OSOBNJAKI: list[Osobnjak] = list(OSOBNJAKI_CORE)
_load_batch2()
'''
    (_DATA / "osobnjaki.py").write_text(
        header + body_core + footer, encoding="utf-8",
    )

    batch2_header = '''# -*- coding: utf-8 -*-
"""Batch 2: 25 additional SPB urban mansions (RU + EN)."""

from __future__ import annotations

from spb.data.osobnjaki import IMAGES_SUBFOLDER, Osobnjak, _img, _o


OSOBNJAKI_EXTRA: list[Osobnjak] = [
'''
    body_extra = "\n".join(
        _entry_block(r, "extra").replace("_o(", "_o(") for r in extra
    )
    # batch2 uses imported _o - fix entry to not duplicate imports
    body_extra = body_extra.replace("    _o(", "    _o(")
    batch2_footer = "\n]\n"
    batch2_content = batch2_header + body_extra + batch2_footer
    batch2_content = batch2_content.replace(
        "from spb.data.osobnjaki import IMAGES_SUBFOLDER, Osobnjak, _img, _o",
        "from spb.data.osobnjaki import Osobnjak, _o",
    )
    (_DATA / "osobnjaki_batch2.py").write_text(batch2_content, encoding="utf-8")


def _write_image_urls() -> None:
    lines = [
        "# -*- coding: utf-8 -*-",
        '"""Image URLs for SPB osobnjaki (Commons, culture.ru)."""',
        "",
        "OSOBNJAKI_IMAGE_DOWNLOADS: dict[str, str] = {",
    ]
    fallbacks: dict[str, list[str]] = {}
    for row in _MANIFEST:
        key = row[0]
        urls = row[7:11]
        for i, url in enumerate(urls, 1):
            fname = "{}_{}.jpg".format(key, i)
            lines.append('    "{}": "{}",'.format(fname, url))
        fallbacks["{}_1.jpg".format(key)] = list(urls[1:])
    lines.append("}")
    lines.append("")
    lines.append("OSOBNJAKI_IMAGE_FALLBACKS: dict[str, list[str]] = {")
    for fname, urls in fallbacks.items():
        inner = ", ".join(repr(u) for u in urls)
        lines.append('    "{}": [{}],'.format(fname, inner))
    lines.append("}")
    lines.append("")
    lines.append("")
    lines.append("def _merge_batch2_urls() -> None:")
    lines.append("    pass  # batch2 URLs merged in main dict")
    lines.append("")
    lines.append("_merge_batch2_urls()")
    (_DATA / "osobnjaki_image_urls.py").write_text(
        "\n".join(lines) + "\n", encoding="utf-8",
    )


def _write_stories_qa() -> None:
    stories = {}
    qa = []
    for row in _MANIFEST[:8]:
        name = row[1]
        stories[name] = (
            "{} — один из городских особняков центра "
            "Санкт-Петербурга.".format(name)
        )
        qa.append({
            "question": "Где находится {}?".format(name),
            "answer": row[3],
        })
    (_DATA / "osobnjaki_stories.py").write_text(
        "# -*- coding: utf-8 -*-\n\nOSOBNJAKI_STORIES: dict[str, str] = "
        + json.dumps(stories, ensure_ascii=False, indent=4)
        + "\n",
        encoding="utf-8",
    )
    qa_lines = [
        "# -*- coding: utf-8 -*-",
        '"""Вопросы и ответы по особнякам Санкт-Петербурга."""',
        "",
        "from typing import TypedDict",
        "",
        "",
        "class QAItem(TypedDict):",
        '    """Один вопрос-ответ."""',
        "",
        "    question: str",
        "    answer: str",
        "",
        "",
        "QA: list[QAItem] = [",
    ]
    for item in qa:
        qa_lines.append("    {")
        qa_lines.append('        "question": {},'.format(repr(item["question"])))
        qa_lines.append('        "answer": {},'.format(repr(item["answer"])))
        qa_lines.append("    },")
    qa_lines.append("]")
    (_DATA / "qa_osobnjaki.py").write_text(
        "\n".join(qa_lines) + "\n", encoding="utf-8",
    )


def main() -> int:
    assert len(_MANIFEST) == 50, len(_MANIFEST)
    _DATA.mkdir(parents=True, exist_ok=True)
    _write_osobnjaki_py()
    _write_image_urls()
    _write_stories_qa()
    print("Generated 50 SPB osobnjaki entries in spb/data/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
