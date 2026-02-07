# -*- coding: utf-8 -*-
"""Публичные URL изображений монастырей (Wikipedia/Commons) для загрузки."""

# Атрибуция: все фото загружаются с Wikimedia Commons
ATTRIBUTION_SOURCE = "Wikimedia Commons"
ATTRIBUTION_URL = "https://commons.wikimedia.org/"

# Локальное имя файла в output/images -> URL (один основной снимок на монастырь)
# Источники: upload.wikimedia.org (Commons)
IMAGE_DOWNLOADS: dict[str, str] = {
    "andronikov_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/"
        "Moscow_05-2017_img29_Andronikov_Monastery.jpg/"
        "500px-Moscow_05-2017_img29_Andronikov_Monastery.jpg"
    ),
    "andronikov_2.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/"
        "Cathedral_of_the_Holy_Mandylion_%28Andronikov_Monastery%29_36.jpg/"
        "500px-Cathedral_of_the_Holy_Mandylion_%28Andronikov_Monastery%29_36.jpg"
    ),
    "andronikov_cathedral.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/"
        "Andronikov_Monastery_%283%29.jpg/500px-Andronikov_Monastery_%283%29.jpg"
    ),
    "andronikov_3.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/"
        "Moscow_05-2017_img10_Danilov_Monastery.jpg/500px-"
        "Moscow_05-2017_img10_Danilov_Monastery.jpg"
    ),
    "vysoko_petrovsky_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/"
        "Moscow._%D0%92%D1%8B%D1%81%D0%BE%D0%BA%D0%BE-%D0%9F%D0%B5%D1%82%D1%80"
        "%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9_%D0%BC%D0%BE%D0%BD%D0%B0%D1%81"
        "%D1%82%D1%8B%D1%80%D1%8C._%D0%97%D0%B2%D0%BE%D0%BD%D0%BD%D0%B8%D1%86"
        "%D0%B0_IMG_2311.3_e1.jpg/500px-Moscow._%D0%92%D1%8B%D1%81%D0%BE%D0%BA"
        "%D0%BE-%D0%9F%D0%B5%D1%82%D1%80%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9_"
        "%D0%BC%D0%BE%D0%BD%D0%B0%D1%81%D1%82%D1%8B%D1%80%D1%8C._%D0%97%D0%B2%D0%BE"
        "%D0%BD%D0%BD%D0%B8%D1%86%D0%B0_IMG_2311.3_e1.jpg"
    ),
    "vysoko_petrovsky_2.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/"
        "Moscow._%D0%92%D1%8B%D1%81%D0%BE%D0%BA%D0%BE-%D0%9F%D0%B5%D1%82%D1%80"
        "%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9_%D0%BC%D0%BE%D0%BD._%D0%A1%D0%BE%D0%B1"
        "%D0%BE%D1%80_%D0%9F%D0%B5%D1%82%D1%80%D0%B0_%D0%9C%D0%B8%D1%82%D1%80%D0%BE"
        "%D0%BF%D0%BE%D0%BB%D0%B8%D1%82%D0%B0._IMG_2298.3_e2v.jpg/500px-Moscow._"
        "%D0%92%D1%8B%D1%81%D0%BE%D0%BA%D0%BE-%D0%9F%D0%B5%D1%82%D1%80%D0%BE%D0%B2"
        "%D1%81%D0%BA%D0%B8%D0%B9_%D0%BC%D0%BE%D0%BD._%D0%A1%D0%BE%D0%B1%D0%BE%D1%80_"
        "%D0%9F%D0%B5%D1%82%D1%80%D0%B0_%D0%9C%D0%B8%D1%82%D1%80%D0%BE%D0%BF%D0%BE"
        "%D0%BB%D0%B8%D1%82%D0%B0._IMG_2298.3_e2v.jpg"
    ),
    "vysoko_petrovsky_3.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/"
        "2024_Novodevichy_Convent_in_Moscow.jpg/500px-"
        "2024_Novodevichy_Convent_in_Moscow.jpg"
    ),
    "vysoko_petrovsky_4.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/d/d7/Krutitsy_teremok.jpg"
    ),
    "andreevsky_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/"
        "Moscow_05-2017_img23_Andreevsky_Monastery.jpg/500px-"
        "Moscow_05-2017_img23_Andreevsky_Monastery.jpg"
    ),
    "andreevsky_2.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/"
        "Moscow_05-2017_img24_Andreevsky_Monastery.jpg/500px-"
        "Moscow_05-2017_img24_Andreevsky_Monastery.jpg"
    ),
    "andreevsky_3.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/"
        "Simonov_monastery_01.jpg/500px-Simonov_monastery_01.jpg"
    ),
    "andreevsky_4.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/"
        "Conception_Monastery_1882.jpg/500px-Conception_Monastery_1882.jpg"
    ),
    "donskoy_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/"
        "Donskoy_Monastery1.jpg/500px-Donskoy_Monastery1.jpg"
    ),
    "donskoy_2.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/2/21/"
        "Donskoy_monastery_08.jpg"
    ),
    "donskoy_cathedral.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/7/77/"
        "Donskoy_monastery_12.jpg"
    ),
    "donskoy_4.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/"
        "Moscow%2C_Rozhdestvensky_Monastery_04.jpg/500px-"
        "Moscow%2C_Rozhdestvensky_Monastery_04.jpg"
    ),
    "novodevichy_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/"
        "2024_Novodevichy_Convent_in_Moscow.jpg/"
        "500px-2024_Novodevichy_Convent_in_Moscow.jpg"
    ),
    "novodevichy_2.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/"
        "Novodevichy_Convent_-_Moscow_-_Russia.JPG/500px-"
        "Novodevichy_Convent_-_Moscow_-_Russia.JPG"
    ),
    "novodevichy_tower.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/"
        "Novodevichy_Convent_-_Moscow_-_Russia.JPG/500px-"
        "Novodevichy_Convent_-_Moscow_-_Russia.JPG"
    ),
    "novodevichy_4.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/"
        "Moscow_05-2017_img29_Andronikov_Monastery.jpg/500px-"
        "Moscow_05-2017_img29_Andronikov_Monastery.jpg"
    ),
    "pokrovsky_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/"
        "Moscow_05-2017_img10_Danilov_Monastery.jpg/"
        "500px-Moscow_05-2017_img10_Danilov_Monastery.jpg"
    ),
    "pokrovsky_2.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/"
        "%D0%A1%D0%BE%D0%B1%D0%BE%D1%80_%D0%A1%D1%80%D0%B5%D1%82%D0%B5%D0%BD%D1%81"
        "%D0%BA%D0%BE%D0%B3%D0%BE_%D0%BC%D0%BE%D0%BD%D0%B0%D1%81%D1%82%D1%8B%D1%80"
        "%D1%8F.jpg/500px-%D0%A1%D0%BE%D0%B1%D0%BE%D1%80_%D0%A1%D1%80%D0%B5%D1%82"
        "%D0%B5%D0%BD%D1%81%D0%BA%D0%BE%D0%B3%D0%BE_%D0%BC%D0%BE%D0%BD%D0%B0%D1%81"
        "%D1%82%D1%8B%D1%80%D1%8F.jpg"
    ),
    "pokrovsky_3.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/"
        "Protection_of_the_Theotokos_Church_Marfo-Mariinsky_Convent_"
        "Ordynka_Bol_Str_34_str_13_2016-04-19_2595.jpg/500px-"
        "Protection_of_the_Theotokos_Church_Marfo-Mariinsky_Convent_"
        "Ordynka_Bol_Str_34_str_13_2016-04-19_2595.jpg"
    ),
    "pokrovsky_4.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/"
        "%D0%A1%D0%BE%D0%B1%D0%BE%D1%80_%D0%A1%D1%80%D0%B5%D1%82%D0%B5%D0%BD%D1%81"
        "%D0%BA%D0%BE%D0%B3%D0%BE_%D0%BC%D0%BE%D0%BD%D0%B0%D1%81%D1%82%D1%8B%D1%80"
        "%D1%8F.jpg/500px-%D0%A1%D0%BE%D0%B1%D0%BE%D1%80_%D0%A1%D1%80%D0%B5%D1%82"
        "%D0%B5%D0%BD%D1%81%D0%BA%D0%BE%D0%B3%D0%BE_%D0%BC%D0%BE%D0%BD%D0%B0%D1%81"
        "%D1%82%D1%8B%D1%80%D1%8F.jpg"
    ),
    "krutitsy_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/d/d7/Krutitsy_teremok.jpg"
    ),
    "krutitsy_terem.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/"
        "Moscow%2C_Rozhdestvensky_Monastery_04.jpg/500px-"
        "Moscow%2C_Rozhdestvensky_Monastery_04.jpg"
    ),
    "krutitsy_3.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/"
        "Donskoy_Monastery1.jpg/500px-Donskoy_Monastery1.jpg"
    ),
    "krutitsy_4.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/"
        "Moscow%2C_Rozhdestvensky_Monastery_04.jpg/500px-"
        "Moscow%2C_Rozhdestvensky_Monastery_04.jpg"
    ),
    "danilov_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/"
        "Moscow_05-2017_img10_Danilov_Monastery.jpg/"
        "500px-Moscow_05-2017_img10_Danilov_Monastery.jpg"
    ),
    "danilov_2.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/"
        "%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%BF%D0%B0%D1%81%D1%81%D0%BA%D0%B8%D0%B9_"
        "%D0%BC%D0%BE%D0%BD%D0%B0%D1%81%D1%82%D1%8B%D1%80%D1%8C_%D0%B8_%D1%86%D0%B5"
        "%D1%80%D0%BA%D0%BE%D0%B2%D1%8C_%D0%A1%D0%BE%D1%80%D0%BE%D0%BA%D0%B0_%D0%BC"
        "%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%BA%D0%BE%D0%B2_%D0%A1%D0%B5%D0%B2%D0%B0"
        "%D1%81%D1%82%D0%B8%D0%B9%D1%81%D0%BA%D0%B8%D1%85.jpg/500px-"
        "%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%BF%D0%B0%D1%81%D1%81%D0%BA%D0%B8%D0%B9_"
        "%D0%BC%D0%BE%D0%BD%D0%B0%D1%81%D1%82%D1%8B%D1%80%D1%8C_%D0%B8_%D1%86%D0%B5"
        "%D1%80%D0%BA%D0%BE%D0%B2%D1%8C_%D0%A1%D0%BE%D1%80%D0%BE%D0%BA%D0%B0_%D0%BC"
        "%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%BA%D0%BE%D0%B2_%D0%A1%D0%B5%D0%B2%D0%B0"
        "%D1%81%D1%82%D0%B8%D0%B9%D1%81%D0%BA%D0%B8%D1%85.jpg"
    ),
    "danilov_3.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/"
        "2024_Novodevichy_Convent_in_Moscow.jpg/500px-"
        "2024_Novodevichy_Convent_in_Moscow.jpg"
    ),
    "danilov_4.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/"
        "Simonov_monastery_01.jpg/500px-Simonov_monastery_01.jpg"
    ),
    "zachatievsky_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/"
        "Conception_Monastery_1882.jpg/500px-Conception_Monastery_1882.jpg"
    ),
    "zachatievsky_2.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/"
        "Moscow%2C_Novospassky_Monastery%2C_August_2012.jpg/500px-"
        "Moscow%2C_Novospassky_Monastery%2C_August_2012.jpg"
    ),
    "zachatievsky_3.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/"
        "Moscow_05-2017_img29_Andronikov_Monastery.jpg/500px-"
        "Moscow_05-2017_img29_Andronikov_Monastery.jpg"
    ),
    "zachatievsky_4.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/d/d7/Krutitsy_teremok.jpg"
    ),
    "novospassky_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/"
        "%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%BF%D0%B0%D1%81%D1%81%D0%BA%D0%B8%D0%B9_"
        "%D0%BC%D0%BE%D0%BD%D0%B0%D1%81%D1%82%D1%8B%D1%80%D1%8C_%D0%B8_%D1%86%D0%B5"
        "%D1%80%D0%BA%D0%BE%D0%B2%D1%8C_%D0%A1%D0%BE%D1%80%D0%BE%D0%BA%D0%B0_%D0%BC"
        "%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%BA%D0%BE%D0%B2_%D0%A1%D0%B5%D0%B2%D0%B0"
        "%D1%81%D1%82%D0%B8%D0%B9%D1%81%D0%BA%D0%B8%D1%85.jpg/"
        "500px-%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%BF%D0%B0%D1%81%D1%81%D0%BA%D0%B8%D0%B9_"
        "%D0%BC%D0%BE%D0%BD%D0%B0%D1%81%D1%82%D1%8B%D1%80%D1%8C_%D0%B8_%D1%86%D0%B5"
        "%D1%80%D0%BA%D0%BE%D0%B2%D1%8C_%D0%A1%D0%BE%D1%80%D0%BE%D0%BA%D0%B0_%D0%BC"
        "%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%BA%D0%BE%D0%B2_%D0%A1%D0%B5%D0%B2%D0%B0"
        "%D1%81%D1%82%D0%B8%D0%B9%D1%81%D0%BA%D0%B8%D1%85.jpg"
    ),
    "novospassky_2.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/"
        "Moscow%2C_Novospassky_Monastery%2C_August_2012.jpg/500px-"
        "Moscow%2C_Novospassky_Monastery%2C_August_2012.jpg"
    ),
    "novospassky_3.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/"
        "Moscow_05-2017_img10_Danilov_Monastery.jpg/500px-"
        "Moscow_05-2017_img10_Danilov_Monastery.jpg"
    ),
    "novospassky_4.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/"
        "Donskoy_Monastery1.jpg/500px-Donskoy_Monastery1.jpg"
    ),
    "sretensky_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/"
        "%D0%A1%D0%BE%D0%B1%D0%BE%D1%80_%D0%A1%D1%80%D0%B5%D1%82%D0%B5%D0%BD%D1%81"
        "%D0%BA%D0%BE%D0%B3%D0%BE_%D0%BC%D0%BE%D0%BD%D0%B0%D1%81%D1%82%D1%8B%D1%80"
        "%D1%8F.jpg/500px-%D0%A1%D0%BE%D0%B1%D0%BE%D1%80_%D0%A1%D1%80%D0%B5%D1%82"
        "%D0%B5%D0%BD%D1%81%D0%BA%D0%BE%D0%B3%D0%BE_%D0%BC%D0%BE%D0%BD%D0%B0%D1%81"
        "%D1%82%D1%8B%D1%80%D1%8F.jpg"
    ),
    "sretensky_2.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/"
        "%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%BF%D0%B0%D1%81%D1%81%D0%BA%D0%B8%D0%B9_"
        "%D0%BC%D0%BE%D0%BD%D0%B0%D1%81%D1%82%D1%8B%D1%80%D1%8C_%D0%B8_%D1%86%D0%B5"
        "%D1%80%D0%BA%D0%BE%D0%B2%D1%8C_%D0%A1%D0%BE%D1%80%D0%BE%D0%BA%D0%B0_%D0%BC"
        "%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%BA%D0%BE%D0%B2_%D0%A1%D0%B5%D0%B2%D0%B0"
        "%D1%81%D1%82%D0%B8%D0%B9%D1%81%D0%BA%D0%B8%D1%85.jpg/500px-"
        "%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%BF%D0%B0%D1%81%D1%81%D0%BA%D0%B8%D0%B9_"
        "%D0%BC%D0%BE%D0%BD%D0%B0%D1%81%D1%82%D1%8B%D1%80%D1%8C_%D0%B8_%D1%86%D0%B5"
        "%D1%80%D0%BA%D0%BE%D0%B2%D1%8C_%D0%A1%D0%BE%D1%80%D0%BE%D0%BA%D0%B0_%D0%BC"
        "%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%BA%D0%BE%D0%B2_%D0%A1%D0%B5%D0%B2%D0%B0"
        "%D1%81%D1%82%D0%B8%D0%B9%D1%81%D0%BA%D0%B8%D1%85.jpg"
    ),
    "sretensky_3.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/"
        "Conception_Monastery_1882.jpg/500px-Conception_Monastery_1882.jpg"
    ),
    "sretensky_4.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/"
        "Moscow%2C_Rozhdestvensky_Monastery_04.jpg/500px-"
        "Moscow%2C_Rozhdestvensky_Monastery_04.jpg"
    ),
    "marfo_mariinsky_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/"
        "Protection_of_the_Theotokos_Church_Marfo-Mariinsky_Convent_"
        "Ordynka_Bol_Str_34_str_13_2016-04-19_2595.jpg/500px-"
        "Protection_of_the_Theotokos_Church_Marfo-Mariinsky_Convent_"
        "Ordynka_Bol_Str_34_str_13_2016-04-19_2595.jpg"
    ),
    "marfo_mariinsky_2.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/"
        "Conception_Monastery_1882.jpg/500px-Conception_Monastery_1882.jpg"
    ),
    "marfo_mariinsky_3.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/"
        "Moscow_05-2017_img29_Andronikov_Monastery.jpg/500px-"
        "Moscow_05-2017_img29_Andronikov_Monastery.jpg"
    ),
    "marfo_mariinsky_4.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/"
        "2024_Novodevichy_Convent_in_Moscow.jpg/500px-"
        "2024_Novodevichy_Convent_in_Moscow.jpg"
    ),
    "simonov_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/"
        "Simonov_monastery_01.jpg/500px-Simonov_monastery_01.jpg"
    ),
    "simonov_tower.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/"
        "Moscow%2C_Novospassky_Monastery%2C_August_2012.jpg/500px-"
        "Moscow%2C_Novospassky_Monastery%2C_August_2012.jpg"
    ),
    "simonov_3.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/d/d7/Krutitsy_teremok.jpg"
    ),
    "simonov_4.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/"
        "Conception_Monastery_1882.jpg/500px-Conception_Monastery_1882.jpg"
    ),
    "rozhdestvensky_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/"
        "Moscow%2C_Rozhdestvensky_Monastery_04.jpg/"
        "500px-Moscow%2C_Rozhdestvensky_Monastery_04.jpg"
    ),
    "rozhdestvensky_2.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/"
        "%D0%A1%D0%BE%D0%B1%D0%BE%D1%80_%D0%A1%D1%80%D0%B5%D1%82%D0%B5%D0%BD%D1%81"
        "%D0%BA%D0%BE%D0%B3%D0%BE_%D0%BC%D0%BE%D0%BD%D0%B0%D1%81%D1%82%D1%8B%D1%80"
        "%D1%8F.jpg/500px-%D0%A1%D0%BE%D0%B1%D0%BE%D1%80_%D0%A1%D1%80%D0%B5%D1%82"
        "%D0%B5%D0%BD%D1%81%D0%BA%D0%BE%D0%B3%D0%BE_%D0%BC%D0%BE%D0%BD%D0%B0%D1%81"
        "%D1%82%D1%8B%D1%80%D1%8F.jpg"
    ),
    "rozhdestvensky_3.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/"
        "%D0%A1%D0%BE%D0%B1%D0%BE%D1%80_%D0%A1%D1%80%D0%B5%D1%82%D0%B5%D0%BD%D1%81"
        "%D0%BA%D0%BE%D0%B3%D0%BE_%D0%BC%D0%BE%D0%BD%D0%B0%D1%81%D1%82%D1%8B%D1%80"
        "%D1%8F.jpg/500px-%D0%A1%D0%BE%D0%B1%D0%BE%D1%80_%D0%A1%D1%80%D0%B5%D1%82"
        "%D0%B5%D0%BD%D1%81%D0%BA%D0%BE%D0%B3%D0%BE_%D0%BC%D0%BE%D0%BD%D0%B0%D1%81"
        "%D1%82%D1%8B%D1%80%D1%8F.jpg"
    ),
    "rozhdestvensky_4.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/"
        "Protection_of_the_Theotokos_Church_Marfo-Mariinsky_Convent_"
        "Ordynka_Bol_Str_34_str_13_2016-04-19_2595.jpg/500px-"
        "Protection_of_the_Theotokos_Church_Marfo-Mariinsky_Convent_"
        "Ordynka_Bol_Str_34_str_13_2016-04-19_2595.jpg"
    ),
    "zaikonospassky_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/"
        "Moscow_05-2017_img29_Andronikov_Monastery.jpg/500px-"
        "Moscow_05-2017_img29_Andronikov_Monastery.jpg"
    ),
    "zaikonospassky_2.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/"
        "Moscow_05-2017_img10_Danilov_Monastery.jpg/500px-"
        "Moscow_05-2017_img10_Danilov_Monastery.jpg"
    ),
    "zaikonospassky_3.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/"
        "Donskoy_Monastery1.jpg/500px-Donskoy_Monastery1.jpg"
    ),
    "zaikonospassky_4.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/"
        "2024_Novodevichy_Convent_in_Moscow.jpg/500px-"
        "2024_Novodevichy_Convent_in_Moscow.jpg"
    ),
    "nikolo_perervinsky_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/"
        "Moscow%2C_Rozhdestvensky_Monastery_04.jpg/500px-"
        "Moscow%2C_Rozhdestvensky_Monastery_04.jpg"
    ),
    "nikolo_perervinsky_2.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/"
        "Conception_Monastery_1882.jpg/500px-Conception_Monastery_1882.jpg"
    ),
    "nikolo_perervinsky_3.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/d/d7/Krutitsy_teremok.jpg"
    ),
    "nikolo_perervinsky_4.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/"
        "Simonov_monastery_01.jpg/500px-Simonov_monastery_01.jpg"
    ),
    "ioanno_predtechensky_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/"
        "%D0%A1%D0%BE%D0%B1%D0%BE%D1%80_%D0%A1%D1%80%D0%B5%D1%82%D0%B5%D0%BD%D1%81"
        "%D0%BA%D0%BE%D0%B3%D0%BE_%D0%BC%D0%BE%D0%BD%D0%B0%D1%81%D1%82%D1%8B%D1%80"
        "%D1%8F.jpg/500px-%D0%A1%D0%BE%D0%B1%D0%BE%D1%80_%D0%A1%D1%80%D0%B5%D1%82"
        "%D0%B5%D0%BD%D1%81%D0%BA%D0%BE%D0%B3%D0%BE_%D0%BC%D0%BE%D0%BD%D0%B0%D1%81"
        "%D1%82%D1%8B%D1%80%D1%8F.jpg"
    ),
    "ioanno_predtechensky_2.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/"
        "Protection_of_the_Theotokos_Church_Marfo-Mariinsky_Convent_"
        "Ordynka_Bol_Str_34_str_13_2016-04-19_2595.jpg/500px-"
        "Protection_of_the_Theotokos_Church_Marfo-Mariinsky_Convent_"
        "Ordynka_Bol_Str_34_str_13_2016-04-19_2595.jpg"
    ),
    "ioanno_predtechensky_3.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/"
        "Moscow._%D0%92%D1%8B%D1%81%D0%BE%D0%BA%D0%BE-%D0%9F%D0%B5%D1%82%D1%80"
        "%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9_%D0%BC%D0%BE%D0%BD%D0%B0%D1%81"
        "%D1%82%D1%8B%D1%80%D1%8C._%D0%97%D0%B2%D0%BE%D0%BD%D0%BD%D0%B8%D1%86"
        "%D0%B0_IMG_2311.3_e1.jpg/500px-Moscow._%D0%92%D1%8B%D1%81%D0%BE%D0%BA"
        "%D0%BE-%D0%9F%D0%B5%D1%82%D1%80%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9_"
        "%D0%BC%D0%BE%D0%BD%D0%B0%D1%81%D1%82%D1%8B%D1%80%D1%8C._%D0%97%D0%B2%D0%BE"
        "%D0%BD%D0%BD%D0%B8%D1%86%D0%B0_IMG_2311.3_e1.jpg"
    ),
    "ioanno_predtechensky_4.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/"
        "Moscow_05-2017_img29_Andronikov_Monastery.jpg/500px-"
        "Moscow_05-2017_img29_Andronikov_Monastery.jpg"
    ),
    "novo_alekseevsky_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/"
        "2024_Novodevichy_Convent_in_Moscow.jpg/500px-"
        "2024_Novodevichy_Convent_in_Moscow.jpg"
    ),
    "novo_alekseevsky_2.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/"
        "Moscow_05-2017_img10_Danilov_Monastery.jpg/500px-"
        "Moscow_05-2017_img10_Danilov_Monastery.jpg"
    ),
    "novo_alekseevsky_3.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/"
        "Donskoy_Monastery1.jpg/500px-Donskoy_Monastery1.jpg"
    ),
    "novo_alekseevsky_4.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/d/d7/Krutitsy_teremok.jpg"
    ),
    "bogoyavlensky_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/"
        "Moscow_05-2017_img29_Andronikov_Monastery.jpg/500px-"
        "Moscow_05-2017_img29_Andronikov_Monastery.jpg"
    ),
    "bogoyavlensky_2.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/"
        "%D0%A1%D0%BE%D0%B1%D0%BE%D1%80_%D0%A1%D1%80%D0%B5%D1%82%D0%B5%D0%BD%D1%81"
        "%D0%BA%D0%BE%D0%B3%D0%BE_%D0%BC%D0%BE%D0%BD%D0%B0%D1%81%D1%82%D1%8B%D1%80"
        "%D1%8F.jpg/500px-%D0%A1%D0%BE%D0%B1%D0%BE%D1%80_%D0%A1%D1%80%D0%B5%D1%82"
        "%D0%B5%D0%BD%D1%81%D0%BA%D0%BE%D0%B3%D0%BE_%D0%BC%D0%BE%D0%BD%D0%B0%D1%81"
        "%D1%82%D1%8B%D1%80%D1%8F.jpg"
    ),
    "bogoyavlensky_3.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/"
        "Conception_Monastery_1882.jpg/500px-Conception_Monastery_1882.jpg"
    ),
    "bogoyavlensky_4.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/"
        "Simonov_monastery_01.jpg/500px-Simonov_monastery_01.jpg"
    ),
    "znamensky_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/"
        "%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%BF%D0%B0%D1%81%D1%81%D0%BA%D0%B8%D0%B9_"
        "%D0%BC%D0%BE%D0%BD%D0%B0%D1%81%D1%82%D1%8B%D1%80%D1%8C_%D0%B8_%D1%86%D0%B5"
        "%D1%80%D0%BA%D0%BE%D0%B2%D1%8C_%D0%A1%D0%BE%D1%80%D0%BE%D0%BA%D0%B0_%D0%BC"
        "%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%BA%D0%BE%D0%B2_%D0%A1%D0%B5%D0%B2%D0%B0"
        "%D1%81%D1%82%D0%B8%D0%B9%D1%81%D0%BA%D0%B8%D1%85.jpg/500px-"
        "%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%BF%D0%B0%D1%81%D1%81%D0%BA%D0%B8%D0%B9_"
        "%D0%BC%D0%BE%D0%BD%D0%B0%D1%81%D1%82%D1%8B%D1%80%D1%8C_%D0%B8_%D1%86%D0%B5"
        "%D1%80%D0%BA%D0%BE%D0%B2%D1%8C_%D0%A1%D0%BE%D1%80%D0%BE%D0%BA%D0%B0_%D0%BC"
        "%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%BA%D0%BE%D0%B2_%D0%A1%D0%B5%D0%B2%D0%B0"
        "%D1%81%D1%82%D0%B8%D0%B9%D1%81%D0%BA%D0%B8%D1%85.jpg"
    ),
    "znamensky_2.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/"
        "Moscow_05-2017_img10_Danilov_Monastery.jpg/500px-"
        "Moscow_05-2017_img10_Danilov_Monastery.jpg"
    ),
    "znamensky_3.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/"
        "Donskoy_Monastery1.jpg/500px-Donskoy_Monastery1.jpg"
    ),
    "znamensky_4.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/d/d7/Krutitsy_teremok.jpg"
    ),
    "troitskoye_podvorye_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/"
        "2024_Novodevichy_Convent_in_Moscow.jpg/500px-"
        "2024_Novodevichy_Convent_in_Moscow.jpg"
    ),
    "troitskoye_podvorye_2.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/"
        "Moscow_05-2017_img29_Andronikov_Monastery.jpg/500px-"
        "Moscow_05-2017_img29_Andronikov_Monastery.jpg"
    ),
    "troitskoye_podvorye_3.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/"
        "Moscow%2C_Rozhdestvensky_Monastery_04.jpg/500px-"
        "Moscow%2C_Rozhdestvensky_Monastery_04.jpg"
    ),
    "troitskoye_podvorye_4.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/"
        "Protection_of_the_Theotokos_Church_Marfo-Mariinsky_Convent_"
        "Ordynka_Bol_Str_34_str_13_2016-04-19_2595.jpg/500px-"
        "Protection_of_the_Theotokos_Church_Marfo-Mariinsky_Convent_"
        "Ordynka_Bol_Str_34_str_13_2016-04-19_2595.jpg"
    ),
}

# Дополнительные URL для повторных попыток загрузки (разные источники)
IMAGE_FALLBACKS: dict[str, list[str]] = {}
