# -*- coding: utf-8 -*-
"""RU/EN display titles for architecture guide TOC and headings."""

from __future__ import annotations

# slug -> (name_ru, name_en)
TOC_NAME_OVERRIDES: dict[str, tuple[str, str]] = {
    "ancient_rus_kyiv_sophia": (
        "Софийский собор в Киеве",
        "Saint Sophia Cathedral in Kyiv",
    ),
    "ancient_rus_vladimir_assumption": (
        "Успенский собор во Владимире",
        "Dormition Cathedral in Vladimir",
    ),
    "ancient_rus_moscow_places_of_worship_3_2": (
        "Успенский собор Московского Кремля",
        "Dormition Cathedral of the Moscow Kremlin",
    ),
    "novgorod_school_moscow_places_of_worship_8_2": (
        "Церковь Троицы в Никитниках",
        "Church of the Trinity in Nikitniki",
    ),
    "novgorod_school_moscow_places_of_worship_7_2": (
        "Церковь Рождества Богородицы в Путинках",
        "Church of the Nativity of the Virgin in Putinki",
    ),
    "pskov_school_moscow_places_of_worship_16_2": (
        "Церковь Зачатия Анны в углу",
        "Church of the Conception of St Anne",
    ),
    "pskov_school_moscow_places_of_worship_17_2": (
        "Церковь Николы в Хамовниках",
        "Church of St Nicholas in Khamovniki",
    ),
    "moscow_fifteenth_sixteenth_moscow_places_of_worship_4_2": (
        "Благовещенский собор Московского Кремля",
        "Annunciation Cathedral of the Moscow Kremlin",
    ),
    "tent_roof_moscow_places_of_worship_18_2": (
        "Церковь Николы в Кленниках",
        "Church of St Nicholas in Klenniki",
    ),
    "tent_roof_moscow_places_of_worship_19_2": (
        "Церковь Воскресения в Кадашах",
        "Church of the Resurrection in Kadashi",
    ),
    "uzorochye_moscow_places_of_worship_21_2": (
        "Храм Симеона Столпника на Поварской",
        "St Simeon Stylites Church on Povarskaya",
    ),
    "uzorochye_moscow_places_of_worship_23_2": (
        "Церковь Успения в Гончарах",
        "Church of the Dormition in Gonchary",
    ),
    "naryshkin_baroque_moscow_places_of_worship_27_2": (
        "Церковь Успения в Вешняках",
        "Church of the Dormition in Veshnyaki",
    ),
    "naryshkin_baroque_moscow_places_of_worship_26_2": (
        "Церковь Рождества Христова в Измайлове",
        "Church of the Nativity in Izmaylovo",
    ),
    "early_classicism_moscow_palaces_5_2": (
        "Усадьба Архангельское",
        "Arkhangelskoye estate",
    ),
    "empire_moscow_places_of_worship_11_2": (
        "Храм Большое Вознесение у Никитских ворот",
        "Church of the Great Ascension at Nikitsky Gate",
    ),
    "avant_garde_moscow_libraries_0_2": (
        "Российская государственная библиотека",
        "Russian State Library",
    ),
    "russo_byzantine_moscow_monasteries_6_2": (
        "Крутицкое подворье",
        "Krutitsy Metochion",
    ),
    "eclecticism_historical_museum": (
        "Исторический музей",
        "State Historical Museum",
    ),
    "eclecticism_moscow_osobnjaki_7_2": (
        "Особняк И. Н. Игумнова",
        "Igumnov House",
    ),
    "eclecticism_moscow_osobnjaki_4_2": (
        "Особняк А. А. Морозова",
        "Morozov Mansion",
    ),
    "eclecticism_moscow_osobnjaki_5_2": (
        "Дом Рукавишникова",
        "Rukavishnikov House",
    ),
    "eclecticism_moscow_buildings_37_2": (
        "Здание МХАТ им. Горького",
        "Moscow Art Theatre building",
    ),
    "eclecticism_moscow_osobnjaki_35_2": (
        "Особняк С. И. Мамонтова",
        "Mamontov Mansion",
    ),
    "pseudo_russian_moscow_palaces_15_2": (
        "Усадьба Царицыно (Большой дворец)",
        "Tsaritsyno Grand Palace",
    ),
    "neo_russian_moscow_osobnjaki_2_2": (
        "Дом-музей В. М. Васнецова",
        "Vasnetsov House Museum",
    ),
    "neo_russian_moscow_osobnjaki_6_2": (
        "Дом Перцовой",
        "Pertsov House",
    ),
    "neo_russian_moscow_railway_stations_1_2": (
        "Казанский вокзал",
        "Kazansky railway terminal",
    ),
    "art_nouveau_moscow_buildings_6_2": (
        "Гостиница «Метрополь»",
        "Hotel Metropol",
    ),
    "art_nouveau_moscow_osobnjaki_8_2": (
        "Особняк Зинаиды Морозовой",
        "Zinaida Morozova Mansion",
    ),
    "art_nouveau_moscow_osobnjaki_14_2": (
        "Дом Е. И. Козицкой",
        "Kozitsky House",
    ),
    "neoclassicism_early20_moscow_osobnjaki_48_2": (
        "Дом Боткина",
        "Botkin House",
    ),
    "neoclassicism_early20_moscow_buildings_11_2": (
        "Государственная Дума",
        "State Duma building",
    ),
    "neoclassicism_early20_spb_osobnjaki_5_2": (
        "Мариинский дворец",
        "Mariinsky Palace",
    ),
    "neoclassicism_early20_moscow_osobnjaki_38_2": (
        "Дом Второва",
        "Vtorov House",
    ),
    "avant_garde_moscow_buildings_29_2": (
        "Здание Центросоюза",
        "Centrosoyuz Building",
    ),
    "avant_garde_moscow_buildings_33_2": (
        "Здание «Известий»",
        "Izvestia Building",
    ),
    "avant_garde_moscow_buildings_2_2": (
        "Дом на набережной",
        "House on the Embankment",
    ),
    "constructivism_moscow_osobnjaki_23_2": (
        "Дом общества «Динамо»",
        "Dinamo Society House",
    ),
    "constructivism_moscow_osobnjaki_25_2": (
        "Дом книги",
        "Dom Knigi (House of Books)",
    ),
    "constructivism_moscow_buildings_32_2": (
        "ДК имени Русакова",
        "Rusakov Workers' Club",
    ),
    "avant_garde_moscow_buildings_32_2": (
        "ДК имени Русакова",
        "Rusakov Workers' Club",
    ),
    "art_deco_moscow_metro_0_2": (
        "Маяковская",
        "Mayakovskaya metro station",
    ),
    "art_deco_moscow_metro_8_2": (
        "Новокузнецкая",
        "Novokuznetskaya metro station",
    ),
    "art_deco_moscow_metro_11_2": (
        "Проспект Мира (кольцевая)",
        "Prospekt Mira metro station (Koltsevaya line)",
    ),
    "art_deco_moscow_metro_14_2": (
        "Курская (кольцевая)",
        "Kurskaya metro station (Koltsevaya line)",
    ),
    "art_deco_moscow_railway_stations_6_2": (
        "Павелецкий вокзал",
        "Paveletsky railway terminal",
    ),
    "art_deco_moscow_metro_15_2": (
        "Парк культуры (кольцевая)",
        "Park Kultury metro station (Koltsevaya line)",
    ),
    "post_constructivism_moscow_osobnjaki_20_2": (
        "Дом общества политкаторжан",
        "House of the Political Prisoners Society",
    ),
    "stalinist_moscow_buildings_17_2": (
        "Высотка на Кудринской",
        "Kudrinskaya skyscraper",
    ),
    "stalinist_moscow_parks_1_2": (
        "ВДНХ",
        "VDNH main ensemble",
    ),
    "stalinist_moscow_buildings_30_2": (
        "Гостиница «Советская»",
        "Sovetskaya Hotel",
    ),
    "stalinist_moscow_railway_stations_4_2": (
        "Белорусский вокзал",
        "Belorussky railway terminal",
    ),
    "panel_housing_moscow_landmarks_6_2": (
        "Памятник «Рабочий и колхозница»",
        "Worker and Kolkhoz Woman monument",
    ),
    "soviet_modernism_moscow_buildings_9_2": (
        "Здание СЭВ",
        "Comecon Building",
    ),
    "soviet_modernism_moscow_buildings_22_2": (
        "Здание мэрии Москвы (быв. СЭВ)",
        "Moscow City Hall (former Comecon building)",
    ),
    "soviet_modernism_moscow_viewpoints_1_2": (
        "Парк «Зарядье» (панорамная палуба)",
        "Zaryadye Park viewing platform",
    ),
    "soviet_modernism_tass_building": (
        "Здание ТАСС",
        "TASS building",
    ),
    "regional_soviet_moscow_landmarks_3_2": (
        "Гостиница «Украина»",
        "Ukraina Hotel",
    ),
    "postmodernism_moscow_theaters_4_2": (
        "Театр «Современник»",
        "Sovremennik Theatre",
    ),
    "postmodernism_moscow_theaters_9_2": (
        "«Гоголь-центр»",
        "Gogol Centre",
    ),
    "contemporary_moscow_places_7_2": (
        "Измайловский кремль",
        "Izmaylovo Kremlin",
    ),
    "contemporary_moscow_viewpoints_2_2": (
        "Останкинская телебашня",
        "Ostankino TV Tower",
    ),
}
