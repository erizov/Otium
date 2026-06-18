# -*- coding: utf-8 -*-
"""Batch 2: 30 additional Moscow urban mansions (RU + EN)."""

from __future__ import annotations

from moscow.data.osobnjaki import IMAGES_SUBFOLDER, Osobnjak


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
    name_en: str,
    history_en: str,
    significance_en: str,
) -> Osobnjak:
    return {
        "name": name,
        "name_en": name_en,
        "address": address,
        "style": style,
        "highlights": highlights,
        "history": history,
        "history_en": history_en,
        "significance": significance,
        "significance_en": significance_en,
        "facts": facts,
        "images": [_img(i) for i in imgs],
        "lat": lat,
        "lon": lon,
    }


OSOBNJAKI_EXTRA: list[Osobnjak] = [
    _o(
        "Дом общества политкаторжан",
        "ул. Поварская, 33",
        "модерн, неоклассика",
        ["Поварская", "историческая память", "фасад с колоннами"],
        "Особняк на Поварской построен в начале XX века. С 1920-х "
        "годов здание связано с обществом политкаторжан; сохранился "
        "парадный фасад и элементы интерьеров.",
        "Памятник архитектуры на Поварской; связь с историей "
        "революционного движения.",
        ["Поварская — «золотая миля» старой Москвы."],
        ["politkatorzh_1.jpg", "politkatorzh_2.jpg",
         "politkatorzh_3.jpg", "politkatorzh_4.jpg"],
        55.7568, 37.5863,
        name_en="House of the Political Prisoners Society",
        history_en=(
            "A mansion on Povarskaya Street built in the early 20th century. "
            "Since the 1920s the building has been linked to the Society of "
            "Political Prisoners; the main façade and interior details survive."
        ),
        significance_en=(
            "A monument of architecture on Povarskaya; tied to the history "
            "of the revolutionary movement."
        ),
    ),
    _o(
        "Дом Г. А. Палибина",
        "ул. Бурденко, 23",
        "модерн",
        ["Бурденко", "декоративный фасад", "исторический центр"],
        "Особняк начала XX века на улице Бурденко; построен для "
        "Г. А. Палибина. Декоративный фасад в духе московского модерна.",
        "Памятник модерна в районе Хамовники; часть исторической "
        "застройки.",
        ["Бурденко — тихая улица у Патриарших."],
        ["palibin_1.jpg", "palibin_2.jpg", "palibin_3.jpg", "palibin_4.jpg"],
        55.7389, 37.5771,
        name_en="G. A. Palibin House",
        history_en=(
            "An early-20th-century mansion on Burdenko Street built for "
            "G. A. Palibin, with a decorative Art Nouveau façade."
        ),
        significance_en=(
            "An Art Nouveau monument in Khamovniki; part of the historic "
            "streetscape."
        ),
    ),
    _o(
        "Дом газеты «Известия»",
        "Пушкинская пл., 5",
        "конструктивизм",
        ["Пушкинская", "типография", "авангард"],
        "Здание редакции «Известий» построено в 1927 году по проекту "
        "Г. Б. Бархина в духе конструктивизма. Круглый зал заседаний и "
        "строгая геометрия фасада — символ советской журналистики.",
        "Памятник конструктивизма на Пушкинской; одно из знаковых "
        "зданий авангарда Москвы.",
        ["Бархин — автор павильона «Рабочий и колхозница» на ВДНХ."],
        ["izvestia_dom_1.jpg", "izvestia_dom_2.jpg",
         "izvestia_dom_3.jpg", "izvestia_dom_4.jpg"],
        55.7661, 37.6054,
        name_en="Izvestia Newspaper Building",
        history_en=(
            "The Izvestia editorial building (1927) by G. B. Barkhin is a "
            "Constructivist landmark with a circular assembly hall and "
            "strict geometric façade."
        ),
        significance_en=(
            "A Constructivist monument on Pushkinskaya Square; one of "
            "Moscow's iconic avant-garde buildings."
        ),
    ),
    _o(
        "Дом общества «Динамо»",
        "ул. Большая Лубянка, 1/15",
        "конструктивизм, сталинский ампир",
        ["Лубянка", "спортивное общество", "исторический центр"],
        "Здание на Большой Лубянке построено для спортивного общества "
        "«Динамо»; сочетает черты конструктивизма и позднего ампира. "
        "Сохранился парадный фасад и спортивная символика.",
        "Памятник архитектуры 1930-х годов; связь с историей "
        "советского спорта.",
        ["«Динамо» — одно из старейших спортивных обществ СССР."],
        ["dynamo_dom_1.jpg", "dynamo_dom_2.jpg",
         "dynamo_dom_3.jpg", "dynamo_dom_4.jpg"],
        55.7607, 37.6262,
        name_en="Dynamo Society House",
        history_en=(
            "A building on Bolshaya Lubyanka for the Dynamo sports "
            "society, combining Constructivist and later Empire-style "
            "features."
        ),
        significance_en=(
            "A 1930s architectural monument linked to the history of "
            "Soviet sport."
        ),
    ),
    _o(
        "Дом Наркомфина",
        "Новинский бульвар, 25/1",
        "конструктивизм",
        ["Моисей Гинзбург", "жилой дом-общежитие", "UNESCO candidate"],
        "Жилой дом Наркомата финансов построен в 1928–1930 годах по "
        "проекту М. Я. Гинзбурга и И. В. Милиниса. Один из главных "
        "памятников конструктивизма в мире; галереи, «трансформируемые» "
        "квартиры, экспериментальная планировка.",
        "Шедевр конструктивизма; объект культурного наследия "
        "федерального значения.",
        ["В том же квартале — дом-музей Шаляпина."],
        ["narkomfin_1.jpg", "narkomfin_2.jpg",
         "narkomfin_3.jpg", "narkomfin_4.jpg"],
        55.7536, 37.5848,
        name_en="Narkomfin Building",
        history_en=(
            "The Narkomfin apartment house (1928–1930) by Moisei Ginzburg "
            "and Ignaty Milinis is a world-famous Constructivist landmark "
            "with galleries and experimental flat layouts."
        ),
        significance_en=(
            "A masterpiece of Constructivism; a federally protected "
            "heritage site."
        ),
    ),
    _o(
        "Дом книги",
        "Орликов пер., 3, стр. 1",
        "конструктивизм",
        ["Орликов", "издательство", "авангард"],
        "Здание «Дома книги» построено в 1930-е годы для издательства; "
        "строгая геометрия фасада, большие витрины, функциональная "
        "планировка — типичный пример московского конструктивизма.",
        "Памятник архитектуры 1930-х; часть истории книгоиздания "
        "в СССР.",
        ["Орликов переулок — тихая улица у «Красных ворот»."],
        ["dom_knigi_1.jpg", "dom_knigi_2.jpg",
         "dom_knigi_3.jpg", "dom_knigi_4.jpg"],
        55.7708, 37.6474,
        name_en="Dom Knigi (House of Books)",
        history_en=(
            "The House of Books was built in the 1930s for a publishing "
            "house, with strict geometry and large display windows typical "
            "of Moscow Constructivism."
        ),
        significance_en=(
            "A 1930s architectural monument tied to Soviet publishing "
            "history."
        ),
    ),
    _o(
        "Особняк С. И. Смирнова",
        "Тверской бульвар, 26/8",
        "модерн",
        ["Ф. О. Шехтель", "Тверской бульвар", "башня"],
        "Построен в 1897–1899 годах по проекту Ф. О. Шехтеля для "
        "С. И. Смирнова. Асимметричный объём, башня и декоративная "
        "кладка — характерные черты московского модерна.",
        "Памятник модерна на Тверском бульваре; работа Шехтеля.",
        ["Тверской бульвар — прогулочная зона центра."],
        ["smirnov_tversk_1.jpg", "smirnov_tversk_2.jpg",
         "smirnov_tversk_3.jpg", "smirnov_tversk_4.jpg"],
        55.7612, 37.5988,
        name_en="S. I. Smirnov Mansion",
        history_en=(
            "Built in 1897–1899 by Fyodor Schechtel for S. I. Smirnov, "
            "with an asymmetrical volume, tower, and decorative masonry."
        ),
        significance_en=(
            "An Art Nouveau monument on Tverskoy Boulevard; a Schechtel "
            "masterpiece."
        ),
    ),
    _o(
        "Дом архитектора Ф. О. Шехтеля",
        "Ермолаевский пер., 28",
        "модерн",
        ["собственный дом", "мастерская", "Шехтель"],
        "Собственный особняк Ф. О. Шехтеля построен в 1896 году. "
        "Архитектор жил и работал здесь; фасад и интерьеры отражают "
        "его почерк — плавные линии модерна и богатый декор.",
        "Памятник модерна; дом-музей архитектора московского модерна.",
        ["Шехтель — автор особняков Рябушинского и Морозовой."],
        ["schechtel_house_1.jpg", "schechtel_house_2.jpg",
         "schechtel_house_3.jpg", "schechtel_house_4.jpg"],
        55.7628, 37.6015,
        name_en="F. O. Schechtel House",
        history_en=(
            "Fyodor Schechtel's own mansion (1896) where he lived and "
            "worked; the façade and interiors reflect his Art Nouveau "
            "style."
        ),
        significance_en=(
            "An Art Nouveau monument; home of the master of Moscow "
            "Modern architecture."
        ),
    ),
    _o(
        "Дом «Утро России»",
        "ул. Мясницкая, 10",
        "модерн",
        ["Ф. О. Шехтель", "типография", "керамика"],
        "Доходный дом и типография «Утро России» построены в 1907 году "
        "по проекту Ф. О. Шехтеля. Керамический декор, стилизованные "
        "растительные мотивы, богатый фасад — яркий образец модерна.",
        "Памятник московского модерна; синтез архитектуры и декора.",
        ["Мясницкая — одна из древнейших улиц Москвы."],
        ["utro_rossii_1.jpg", "utro_rossii_2.jpg",
         "utro_rossii_3.jpg", "utro_rossii_4.jpg"],
        55.7589, 37.6342,
        name_en="Utro Rossii House",
        history_en=(
            "The Utro Rossii printing house (1907) by Schechtel features "
            "ceramic décor and rich Art Nouveau façades on Myasnitskaya."
        ),
        significance_en=(
            "A Moscow Art Nouveau monument combining architecture and "
            "decorative art."
        ),
    ),
    _o(
        "Дом профессора В. Ф. Снегирёва",
        "ул. Плющиха, 62, стр. 2",
        "модерн",
        ["Р. И. Клейн", "Плющиха", "история гинекологии"],
        "Особняк построен в 1893–1894 годах по проекту Р. И. Клейна для "
        "профессора В. Ф. Снегирёва. Декоративный фасад в духе модерна, "
        "сохранившиеся интерьеры.",
        "Памятник модерна на Плющихе; редкий особняк Хамовников.",
        ["Снегирёв — основоположник отечественной гинекологии."],
        ["snegirev_1.jpg", "snegirev_2.jpg", "snegirev_3.jpg", "snegirev_4.jpg"],
        55.7372, 37.5748,
        name_en="Professor V. F. Snegirev House",
        history_en=(
            "Built in 1893–1894 by Roman Klein for Professor Vladimir "
            "Snegirev, with a decorative Art Nouveau façade."
        ),
        significance_en=(
            "An Art Nouveau monument on Plyushchikha Street in "
            "Khamovniki."
        ),
    ),
    _o(
        "Особняк В. А. Морозовой",
        "ул. Мясницкая, 35",
        "модерн, неорусский",
        ["С. В. Малютин", "керамика", "купеческий дом"],
        "Доходный дом В. А. Морозовой построен в начале XX века; "
        "фасад украшен керамическими панно по эскизам С. В. Малютина. "
        "Яркий пример московского модерна и неорусского декора.",
        "Памятник модерна на Мясницкой; связь с семьёй Морозовых.",
        ["Морозовы — известная купеческая династия."],
        ["morozova_varvara_1.jpg", "morozova_varvara_2.jpg",
         "morozova_varvara_3.jpg", "morozova_varvara_4.jpg"],
        55.7654, 37.6389,
        name_en="V. A. Morozova Mansion",
        history_en=(
            "Varvara Morozova's apartment house features ceramic panels "
            "after Sergey Malyutin's designs — a vivid Moscow Modern "
            "landmark."
        ),
        significance_en=(
            "An Art Nouveau monument on Myasnitskaya linked to the "
            "Morozov merchant family."
        ),
    ),
    _o(
        "Дом А. И. Хлудова",
        "ул. Пречистенка, 5/7",
        "классицизм",
        ["Пречистенка", "усадебный дом", "колонный портик"],
        "Городская усадьба Хлудовых известна с XVIII века. Каменный "
        "особняк с классическим портиком; сохранились парадные залы.",
        "Памятник классицизма на Пречистенке; часть исторического "
        "квартала.",
        ["Пречистенка — «золотая миля» старой Москвы."],
        ["khludov_1.jpg", "khludov_2.jpg", "khludov_3.jpg", "khludov_4.jpg"],
        55.7418, 37.5958,
        name_en="A. I. Khludov House",
        history_en=(
            "The Khludov town estate dates to the 18th century, with a "
            "stone mansion and classical portico on Prechistenka."
        ),
        significance_en=(
            "A Neoclassical monument in the historic Prechistenka "
            "quarter."
        ),
    ),
    _o(
        "Доходный дом Ф. И. Кекушева",
        "ул. Остоженка, 21",
        "модерн",
        ["Ф. И. Кекушев", "Остоженка", "керамика"],
        "Доходный дом построен в 1900–1903 годах по проекту Ф. И. "
        "Кекушева. Декоративный фасад с керамикой и асимметричной "
        "композицией — характерный модерн начала XX века.",
        "Памятник модерна на Остоженке; работа Кекушева.",
        ["Кекушев — автор «Дома с пауками» на Большой Никитской."],
        ["kekushev_ost_1.jpg", "kekushev_ost_2.jpg",
         "kekushev_ost_3.jpg", "kekushev_ost_4.jpg"],
        55.7415, 37.6042,
        name_en="F. I. Kekushev Apartment House",
        history_en=(
            "Built in 1900–1903 by Lev Kekushev on Ostozhenka with "
            "ceramic décor and an asymmetrical Art Nouveau composition."
        ),
        significance_en=(
            "An Art Nouveau monument on Ostozhenka Street."
        ),
    ),
    _o(
        "Дом М. А. Щапова",
        "ул. Погодинская, 12",
        "модерн",
        ["Погодинская", "декоративный фасад", "Хамовники"],
        "Особняк начала XX века на Погодинской; богатый лепной и "
        "керамический декор фасада. Памятник московского модерна в "
        "районе Хамовники.",
        "Редкий особняк модерна на Погодинской; часть исторической "
        "застройки.",
        ["Погодинская названа в честь историка М. П. Погодина."],
        ["shchapov_1.jpg", "shchapov_2.jpg", "shchapov_3.jpg", "shchapov_4.jpg"],
        55.7348, 37.5721,
        name_en="M. A. Shchapov House",
        history_en=(
            "An early-20th-century mansion on Pogodinskaya with rich "
            "stucco and ceramic façade decoration."
        ),
        significance_en=(
            "A rare Art Nouveau mansion in Khamovniki."
        ),
    ),
    _o(
        "Дом Коробкова",
        "Покровский бульвар, 14",
        "модерн",
        ["Покровка", "Ф. И. Кекушев", "керамика"],
        "Доходный дом Коробкова построен в начале XX века; фасад с "
        "керамическим декором и башенкой. Характерный пример "
        "московского модерна на Покровке.",
        "Памятник модерна; часть исторической застройки Басманного "
        "района.",
        ["Покровка — одна из старинных улиц Москвы."],
        ["korobkov_1.jpg", "korobkov_2.jpg", "korobkov_3.jpg", "korobkov_4.jpg"],
        55.7589, 37.6489,
        name_en="Korobkov House",
        history_en=(
            "Korobkov's apartment house on Pokrovsky Boulevard features "
            "ceramic décor and a turret typical of Moscow Art Nouveau."
        ),
        significance_en=(
            "An Art Nouveau monument in the historic Pokrovka area."
        ),
    ),
    _o(
        "Особняк С. И. Мамонтова",
        "Спиридоновка, 10",
        "модерн, эклектика",
        ["Спиридоновка", "меценат", "исторический центр"],
        "Городская усадьба на Спиридоновке связана с именем мецената "
        "С. И. Мамонтова. Каменный особняк с декоративным фасадом; "
        "часть исторического квартала у Патриарших.",
        "Памятник архитектуры; связь с культурной историей Москвы.",
        ["Мамонтов — меценат и организатор «Русских сезонов»."],
        ["mamontov_1.jpg", "mamontov_2.jpg", "mamontov_3.jpg", "mamontov_4.jpg"],
        55.7582, 37.5948,
        name_en="S. I. Mamontov Mansion",
        history_en=(
            "A town estate on Spiridonovka linked to patron Savva "
            "Mamontov, with a decorative stone mansion near Patriarch "
            "Ponds."
        ),
        significance_en=(
            "An architectural monument tied to Moscow's cultural "
            "history."
        ),
    ),
    _o(
        "Городская усадьба Голицыных",
        "Никитский бульвар, 50",
        "классицизм, ампир",
        ["Никитские ворота", "усадебный дом", "колонный портик"],
        "Усадьба Голицыных на Никитском бульваре известна с XVIII "
        "века. Главный дом перестроен в начале XIX века в духе ампира; "
        "сохранился сад и парадные залы.",
        "Памятник усадебной архитектуры у Никитских ворот.",
        ["Никитский бульвар — прогулочная зона центра."],
        ["golitsyn_1.jpg", "golitsyn_2.jpg", "golitsyn_3.jpg", "golitsyn_4.jpg"],
        55.7528, 37.6012,
        name_en="Golitsyn Town Estate",
        history_en=(
            "The Golitsyn estate on Nikitsky Boulevard dates to the "
            "18th century; the main house was rebuilt in Empire style "
            "in the early 19th century."
        ),
        significance_en=(
            "A manor-house monument near Nikitsky Gate."
        ),
    ),
    _o(
        "Дом И. К. Цветкова",
        "Пречистенская наб., 14",
        "неорусский стиль",
        ["В. М. Васнецов", "керамика", "набережная"],
        "Особняк построен в 1900-е годы для коллекционера И. К. "
        "Цветкова; фасад в неорусском стиле с керамическими "
        "вставками. С 1929 года — филиал ГМИИ им. А. С. Пушкина.",
        "Памятник неорусского стиля на набережной; музейное здание.",
        ["Цветков собрал коллекцию древнерусского искусства."],
        ["tsvetkov_1.jpg", "tsvetkov_2.jpg", "tsvetkov_3.jpg", "tsvetkov_4.jpg"],
        55.7398, 37.6018,
        name_en="I. K. Tsvetkov House",
        history_en=(
            "Built for collector Ivan Tsvetkov in Neo-Russian style with "
            "ceramic insets; since 1929 a branch of the Pushkin Museum."
        ),
        significance_en=(
            "A Neo-Russian monument on Prechistenskaya Embankment."
        ),
    ),
    _o(
        "Дом Второва",
        "ул. Остоженка, 17",
        "модерн, неоклассика",
        ["Остоженка", "купеческий особняк", "исторический центр"],
        "Особняк начала XX века на Остоженке; построен для купца "
        "Второва. Богатый декор фасада, сохранившиеся элементы "
        "интерьеров.",
        "Памятник архитектуры на Остоженке; часть «золотой мили».",
        ["Остоженка — одна из престижных улиц центра."],
        ["vtorov_1.jpg", "vtorov_2.jpg", "vtorov_3.jpg", "vtorov_4.jpg"],
        55.7421, 37.6028,
        name_en="Vtorov House",
        history_en=(
            "An early-20th-century merchant mansion on Ostozhenka built "
            "for the Vtorov family with rich façade decoration."
        ),
        significance_en=(
            "An architectural monument on prestigious Ostozhenka Street."
        ),
    ),
    _o(
        "Дом Прокофьева-Белгородского",
        "ул. Пречистенка, 15",
        "классицизм",
        ["Пречистенка", "усадебный дом", "исторический центр"],
        "Каменный особняк начала XIX века на Пречистенке; строгий "
        "классический фасад, сохранившиеся парадные залы.",
        "Памятник классицизма; часть исторической застройки "
        "Пречистенки.",
        ["Пречистенка — тихая улица центра."],
        ["prokofiev_bg_1.jpg", "prokofiev_bg_2.jpg",
         "prokofiev_bg_3.jpg", "prokofiev_bg_4.jpg"],
        55.7412, 37.5978,
        name_en="Prokofiev-Belgorodsky House",
        history_en=(
            "An early-19th-century stone mansion on Prechistenka with a "
            "strict classical façade and ceremonial halls."
        ),
        significance_en=(
            "A Neoclassical monument in the historic Prechistenka "
            "quarter."
        ),
    ),
    _o(
        "Дом Бахрушина",
        "ул. Бахрушина, 28–32",
        "модерн, эклектика",
        ["Бахрушин", "театральный музей", "купеческий дом"],
        "Городская усадьба Бахрушиных на улице Бахрушина; главный дом "
        "перестроен в начале XX века. С 1980-х — Театральный музей им. "
        "А. А. Бахрушина.",
        "Памятник архитектуры; центр театральной истории России.",
        ["Бахрушин — основатель театрального музея."],
        ["bakhrushin_1.jpg", "bakhrushin_2.jpg",
         "bakhrushin_3.jpg", "bakhrushin_4.jpg"],
        55.7318, 37.6342,
        name_en="Bakhrushin House",
        history_en=(
            "The Bakhrushin town estate was rebuilt in the early 20th "
            "century; since the 1980s it houses the Bakhrushin Theatre "
            "Museum."
        ),
        significance_en=(
            "An architectural monument and centre of Russian theatre "
            "history."
        ),
    ),
    _o(
        "Усадьба Луниных",
        "ул. Остоженка, 5",
        "классицизм, ампир",
        ["Остоженка", "музей Востока", "усадебный дом"],
        "Городская усадьба Луниных на Остоженке; главный дом в стиле "
        "классицизма. С 1970-х — Государственный музей изобразительных "
        "искусств народов Востока.",
        "Памятник усадебной архитектуры; музейное здание мирового "
        "значения.",
        ["Коллекция музея Востока — одна из крупнейших в мире."],
        ["lunin_1.jpg", "lunin_2.jpg", "lunin_3.jpg", "lunin_4.jpg"],
        55.7448, 37.6058,
        name_en="Lunin Town Estate",
        history_en=(
            "The Lunin estate on Ostozhenka houses the State Museum of "
            "Oriental Art since the 1970s; the main house is Neoclassical."
        ),
        significance_en=(
            "A manor-house monument and world-class museum building."
        ),
    ),
    _o(
        "Дом Нащокина",
        "ул. Покровка, 10",
        "классицизм",
        ["Покровка", "усадебный дом", "исторический центр"],
        "Городская усадьба Нащокина известна с XVIII века. Каменный "
        "особняк с классическим декором; сохранился в составе "
        "исторической застройки Покровки.",
        "Памятник классицизма на Покровке.",
        ["Покровка — одна из древних улиц Москвы."],
        ["nashchokin_1.jpg", "nashchokin_2.jpg",
         "nashchokin_3.jpg", "nashchokin_4.jpg"],
        55.7598, 37.6512,
        name_en="Nashchokin House",
        history_en=(
            "The Nashchokin town estate on Pokrovka dates to the 18th "
            "century, with a stone mansion and classical décor."
        ),
        significance_en=(
            "A Neoclassical monument on historic Pokrovka Street."
        ),
    ),
    _o(
        "Здание банка Рябушинского",
        "Биржевая пл., 1",
        "модерн",
        ["Ф. О. Шехтель", "Биржевая", "керамика"],
        "Банк товарищества Рябушинского построен в 1900–1903 годах по "
        "проекту Ф. О. Шехтеля. Керамический декор, стилизованные "
        "растительные мотивы — яркий образец московского модерна.",
        "Памятник модерна на Биржевой площади; работа Шехтеля.",
        ["Рядом — Китай-город и Ивановская площадь."],
        ["ryabushinsky_bank_1.jpg", "ryabushinsky_bank_2.jpg",
         "ryabushinsky_bank_3.jpg", "ryabushinsky_bank_4.jpg"],
        55.7538, 37.6342,
        name_en="Ryabushinsky Bank Building",
        history_en=(
            "The Ryabushinsky partnership bank (1900–1903) by Schechtel "
            "on Birzhevaya Square features ceramic Art Nouveau décor."
        ),
        significance_en=(
            "An Art Nouveau monument on Birzhevaya Square."
        ),
    ),
    _o(
        "Особняк на Спиридоновке, 36",
        "Спиридоновка, 36",
        "модерн",
        ["Спиридоновка", "декоративный фасад", "Патриаршие"],
        "Каменный особняк начала XX века на Спиридоновке; "
        "асимметричный фасад, декоративная кладка. Часть исторического "
        "квартала особняков у Патриарших прудов.",
        "Памятник модерна; тихая улица исторического центра.",
        ["Спиридоновка — одна из «особнячных» улиц Москвы."],
        ["spiridonovka_36_1.jpg", "spiridonovka_36_2.jpg",
         "spiridonovka_36_3.jpg", "spiridonovka_36_4.jpg"],
        55.7578, 37.5912,
        name_en="Spiridonovka 36 Mansion",
        history_en=(
            "An early-20th-century stone mansion on Spiridonovka with "
            "an asymmetrical façade near Patriarch Ponds."
        ),
        significance_en=(
            "An Art Nouveau monument on a historic mansion street."
        ),
    ),
    _o(
        "Дом Союзов (усадьба Долгоруковых)",
        "ул. Большая Дмитровка, 1",
        "классицизм, ампир",
        ["Колонный зал", "Долгоруковы", "исторический центр"],
        "Усадьба князей Долгоруковых известна с XVIII века. Здание "
        "перестраивалось; знаменитый Колонный зал — одно из крупнейших "
        "безопорных залов России. С 1931 года — Дом Союзов.",
        "Памятник архитектуры; символ общественной и культурной "
        "жизни Москвы.",
        ["В Колонном зале проходили концерты и съездов."],
        ["dolgorukov_1.jpg", "dolgorukov_2.jpg",
         "dolgorukov_3.jpg", "dolgorukov_4.jpg"],
        55.7589, 37.6142,
        name_en="House of the Unions (Dolgorukov Estate)",
        history_en=(
            "The Dolgorukov princes' estate includes the famous Column "
            "Hall; since 1931 the House of the Unions on Bolshaya "
            "Dmitrovka."
        ),
        significance_en=(
            "An architectural monument and symbol of Moscow's public "
            "and cultural life."
        ),
    ),
    _o(
        "Дом Соллогуба",
        "пер. Трехпрудный, 5",
        "классицизм",
        ["Трехпрудный", "литературная история", "исторический центр"],
        "Городская усадьба на Трехпрудном переулке связана с "
        "литературной историей Москвы. Каменный особняк XIX века с "
        "классическим фасадом.",
        "Памятник классицизма у Патриарших прудов.",
        ["Трехпрудный — тихий переулок центра."],
        ["sollogub_1.jpg", "sollogub_2.jpg",
         "sollogub_3.jpg", "sollogub_4.jpg"],
        55.7638, 37.5928,
        name_en="Sollogub House",
        history_en=(
            "A 19th-century stone mansion on Trekhprudny Lane linked to "
            "Moscow's literary history."
        ),
        significance_en=(
            "A Neoclassical monument near Patriarch Ponds."
        ),
    ),
    _o(
        "Дом-музей А. С. Пушкина (усадьба Хрущёва-Селезнёва)",
        "ул. Пречистенка, 12/2",
        "ампир, классицизм",
        ["Пушкин", "усадебный дом", "музей"],
        "Главное здание Государственного музея А. С. Пушкина — "
        "ампирная усадьба на Пречистенке. Построена в начале XIX "
        "века; экспозиция посвящена жизни и творчеству поэта.",
        "Крупнейший пушкинский музей России; памятник ампира.",
        ["Усадьба — один из символов «золотой мили»."],
        ["pushkin_museum_house_1.jpg", "pushkin_museum_house_2.jpg",
         "pushkin_museum_house_3.jpg", "pushkin_museum_house_4.jpg"],
        55.7425, 37.5972,
        name_en="Pushkin Museum Main House",
        history_en=(
            "The main building of the Pushkin State Museum is an Empire "
            "manor on Prechistenka dedicated to the poet's life and work."
        ),
        significance_en=(
            "Russia's leading Pushkin museum; an Empire-style monument."
        ),
    ),
    _o(
        "Дом Боткина",
        "Староконюшенный пер., 32",
        "модерн, неоклассика",
        ["Арбат", "врач-филантроп", "исторический центр"],
        "Особняк на Староконюшенный переулке связан с именем врача и "
        "филантропа Боткина. Построен в начале XX века; богатый декор "
        "фасада, сохранившиеся интерьеры.",
        "Памятник архитектуры у Арбата; часть исторической застройки.",
        ["Боткин — основатель первой в России клиники."],
        ["botkin_1.jpg", "botkin_2.jpg", "botkin_3.jpg", "botkin_4.jpg"],
        55.7458, 37.5898,
        name_en="Botkin House",
        history_en=(
            "A mansion on Starokonyushenny Lane linked to physician "
            "Sergey Botkin, with rich early-20th-century decoration."
        ),
        significance_en=(
            "An architectural monument near the Arbat."
        ),
    ),
    _o(
        "Дом Мазепина",
        "ул. Большая Никитская, 12",
        "модерн",
        ["Никитская", "декоративный фасад", "исторический центр"],
        "Особняк начала XX века на Большой Никитской; декоративный "
        "фасад в стиле модерн. Сохранился среди исторической застройки "
        "центра.",
        "Памятник модерна на Никитской; часть «особнячного» квартала.",
        ["Большая Никитская — одна из старинных улиц Москвы."],
        ["mazepin_1.jpg", "mazepin_2.jpg", "mazepin_3.jpg", "mazepin_4.jpg"],
        55.7548, 37.6018,
        name_en="Mazepin House",
        history_en=(
            "An early-20th-century Art Nouveau mansion on Bolshaya "
            "Nikitskaya with a decorative façade."
        ),
        significance_en=(
            "An Art Nouveau monument in the historic Nikitskaya quarter."
        ),
    ),
]
