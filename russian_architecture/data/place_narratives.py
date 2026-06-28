# -*- coding: utf-8 -*-
"""Curated place prose overrides (RU/EN) for thin or corrupted city data."""

from __future__ import annotations

from typing import Any

from russian_architecture.data.toc_name_overrides import TOC_NAME_OVERRIDES

# slug -> (description_ru, description_en, history_ru, history_en,
#          significance_ru, significance_en)
_OVERRIDES: dict[str, tuple[str, str, str, str, str, str]] = {
    "moscow_fifteenth_sixteenth_kremlin_archangel": (
        "Архангельский собор Московского Кремля — усыпальница "
        "великих князей и царей, возведённая Алевизом Новым.",
        "The Archangel Cathedral of the Moscow Kremlin is the "
        "necropolis of grand princes and tsars, built by Aloisio "
        "the New.",
        "Построен в 1505–1508 годах итальянским зодчим Алевизом "
        "Новым на месте старого Архангельского собора. До переноса "
        "столицы в Петербург здесь хоронили правителей — от Ивана "
        "Калиты до первых Романовых; в соборе более 50 захоронений "
        "и иконостас XVII века. С 1918 года храм — музей в составе "
        "Кремля.",
        "Built in 1505–1508 by the Italian architect Aloisio the "
        "New on the site of an earlier cathedral. Until the capital "
        "moved to St Petersburg it was the main burial church of "
        "Muscovite rulers from Ivan Kalita to the early Romanovs; "
        "more than fifty tombs and a 17th-century iconostasis "
        "survive inside. A Kremlin museum since 1918.",
        "Некрополь династий Рюриковичей и первых Романовых; "
        "единственный в Кремле храм-усыпальница правителей.",
        "Necropolis of the Rurikids and early Romanovs; the Kremlin's "
        "only rulers' burial church.",
    ),
    "pskov_school_vasily_gorka": (
        "Церковь Василия на Горке — один из лучших памятников "
        "псковской школы XV века на Октябрьском проспекте.",
        "The Church of St Basil on the Hill is a fine 15th-century "
        "monument of the Pskov school on October Avenue.",
        "Каменный храм вырос на месте деревянной церкви XIV века. "
        "Трёхапсидный объём увенчан одной главой; стены украшены "
        "ступенчатыми арками и поясками из плинфы — характерный "
        "псковский декор. Храм входит в серию памятников псковского "
        "зодчества, внесённую в список Всемирного наследия ЮНЕСКО.",
        "The stone church replaced a 14th-century wooden predecessor. "
        "A triple-apsed volume carries a single dome; stepped arches "
        "and brick cornices typify Pskov ornament. It belongs to the "
        "UNESCO-listed Pskov school of architecture.",
        "Памятник демонстрирует лаконичный объём и выразительную "
        "кирпичную пластику псковских мастеров.",
        "The church shows the compact volumes and ornamental brick "
        "work of Pskov builders.",
    ),
    "tent_roof_ascension_kolomenskoye": (
        "Церковь Вознесения в Коломенском — первый шатровый храм "
        "на русской земле и образец московского зодчества 1530-х.",
        "The Ascension Church in Kolomenskoye is the earliest stone "
        "tent-roof church in Russia and a landmark of 1530s Moscow.",
        "Построена в 1532 году в честь рождения царевича Ивана "
        "(будущего Ивана Грозного). Восьмигранный шатёр без "
        "внутренних опор восходит к деревянным башням и сторожевым "
        "постройкам; под шатром — молельный зал с керамическим "
        "иконостасом. Включена в список Всемирного наследия ЮНЕСКО.",
        "Built in 1532 to mark the birth of Tsarevich Ivan (the "
        "future Ivan the Terrible). An octagonal tent rises without "
        "interior pillars, echoing wooden towers; the prayer hall "
        "beneath retains a ceramic iconostasis. UNESCO World Heritage.",
        "Шатровая форма стала символом московского эксперимента "
        "эпохи Ивана IV.",
        "The tent form became the emblem of Muscovite architectural "
        "experiment under Ivan IV.",
    ),
    "tent_roof_st_basil": (
        "Собор Покрова на Рву, известный как храм Василия Блаженного, "
        "— главный шедевр московского шатрового зодчества XVI века.",
        "The Intercession Cathedral on the Moat, known as Saint "
        "Basil's, is the chief masterpiece of 16th-century Muscovite "
        "tent-roof design.",
        "Заложен в 1555–1561 годах по повелению Ивана IV в память "
        "взятия Казани. Девять отдельных церквей на общем подклете "
        "образуют праздничный силуэт Красной площади; центральная "
        "глава восходит к шатру Вознесения в Коломенском.",
        "Founded in 1555–1561 by Ivan IV to commemorate the capture "
        "of Kazan. Nine churches on a common platform create the "
        "festive skyline of Red Square; the central tower echoes "
        "Kolomenskoye's Ascension tent.",
        "Уникальный ансамбль сочетает шатры, главки и яркую "
        "роспись фасадов.",
        "A unique ensemble of tents, domes and vivid façade painting.",
    ),
    "tent_roof_transfiguration_ostro": (
        "Церковь Преображения в селе Остров — редкий памятник "
        "шатрового типа Подмосковья XVI века.",
        "The Church of the Transfiguration at Ostrov is a rare "
        "16th-century tent-roof church in the Moscow region.",
        "Возведена в конце XVI века; четырёхугольный шатёр на "
        "высоком барабане завершает компактный четверик. Храм "
        "сохранил черты перехода от крестово-купольной схемы к "
        "шатровым экспериментам московских мастерских.",
        "Built in the late 16th century; a square tent on a tall "
        "drum crowns a compact cube. It preserves the transition "
        "from cross-in-square plans to Muscovite tent experiments.",
        "Важный пример распространения шатровой формы за пределами "
        "Кремля и Коломенского.",
        "An important example of the tent form beyond the Kremlin "
        "and Kolomenskoye.",
    ),
    "stalinist_msu_main_building": (
        "Главное здание МГУ на Воробьёвых горах — одна из семи "
        "сталинских высоток и символ советского неоклассицизма.",
        "The MSU main building on Sparrow Hills is one of the seven "
        "Stalinist skyscrapers and a symbol of Soviet neoclassicism.",
        "Спроектировано Львом Рудневым, строительство велось "
        "1949–1953 годов. 36-этажная башня со шпилом завершает "
        "университетский ансамбль; фасады облицованы гранитом и "
        "терракотой, интерьеры украшены мозаиками и лепниной.",
        "Designed by Lev Rudnev and built 1949–1953. A 36-storey "
        "tower with spire anchors the campus; granite and terracotta "
        "façades enclose mosaic and stucco interiors.",
        "Высотка задаёт силуэт юго-запада Москвы и эпоху послевоенного "
        "«сталинского ампира».",
        "The skyscraper shapes Moscow's south-western skyline and "
        "the post-war Stalinist Empire style.",
    ),
    "stalinist_komsomolskaya_metro": (
        "Кольцевая «Комсомольская» — парадная станция московского "
        "метро в стиле сталинского неоклассицизма.",
        "Komsomolskaya (ring line) is a ceremonial Moscow Metro "
        "station in Stalinist neoclassical style.",
        "Открыта в 1952 году по проекту Алексея Щусева. Зал украшен "
        "мозаиками Павла Корина на темы военной славы России, "
        "бронзовыми люстрами и мраморными колоннами; своды "
        "напоминают зал дворца.",
        "Opened in 1952 to designs by Alexey Shchusev. Pavel Korin's "
        "mosaics celebrate Russia's military glory; bronze chandeliers "
        "and marble columns give the vaults a palace-like character.",
        "Образцовая «дворцовая» станция первого кольца.",
        "A model 'palace' station of the first ring line.",
    ),
    "stalinist_vdnh_main_pavilion": (
        "Главный павильон ВДНХ — центральный монумент сталинского "
        "ампира на выставочном комплексе.",
        "The VDNKh main pavilion is the central Stalinist Empire "
        "monument of the exhibition complex.",
        "Построен в 1954 году по проекту Георгия Щуко и Евгения "
        "Столярова. Портик с барельефом и высокие аркады образуют "
        "парадную ось площади Колхозов; интерьер отделан мрамором "
        "и лепниной.",
        "Built in 1954 by Georgy Schuko and Yevgeny Stolyarov. "
        "A portico with bas-relief and tall arcades form the ceremonial "
        "axis of Kolkhoz Square; interiors are finished in marble "
        "and stucco.",
        "Символ послевоенного представительства достижений СССР.",
        "A symbol of post-war Soviet achievement on display.",
    ),
    "petrine_baroque_summer_garden_2": (
        "Летний сад — старейший регулярный парк Петербурга, заложенный "
        "при Петре I на острове между Невой и Фонтанкой.",
        "The Summer Garden is St Petersburg's oldest formal park, "
        "laid out under Peter the Great between the Neva and Fontanka.",
        "Первые работы начались в 1704 году; с 1712 года планировку "
        "вёл Жан-Батист Леблон по образцу Версаля. Прямые аллеи, "
        "боскеты, фонтаны и скульптуры создавали парадное пространство "
        "для двора; ограда с решёткой Кваренги завершила ансамбль "
        "в 1784 году.",
        "Work began in 1704; from 1712 Jean-Baptiste Le Blond shaped "
        "a Versailles-inspired layout. Straight alleys, bosquets, "
        "fountains and sculpture formed a courtly promenade; Quarenghi's "
        "cast-iron grille completed the ensemble in 1784.",
        "Парк связывает петровский барокко с классицизмом и хранит "
        "одну из лучших коллекций садовой скульптуры России.",
        "The garden links Petrine Baroque with Classicism and holds "
        "one of Russia's finest collections of garden sculpture.",
    ),
    "elizabethan_baroque_pavlovsk_palace_2": (
        "Павловский дворец — классический дворец-загородная резиденция "
        "к югу от Петербурга, центр ансамбля Павловска.",
        "Pavlovsk Palace is a Neoclassical country residence south "
        "of St Petersburg, core of the Pavlovsk ensemble.",
        "Строительство велось в 1782–1825 годах для великих князей "
        "Павла и Марии Фёдоровны; главные авторы — Чарльз Камерон, "
        "Винченцо Бренна, Андрей Воронихин. Дворец на высоком берегу "
        "Славянки окружён парком в духе английского пейзажа.",
        "Built 1782–1825 for Grand Duke Paul and Maria Feodorovna; "
        "Charles Cameron, Vincenzo Brenna and Andrey Voronikhin led "
        "the work. The palace stands on a bluff above the Slavyanka, "
        "within an English-style landscape park.",
        "Интерьеры и парк образуют единый музей классицизма; ансамбль "
        "внесён в список Всемирного наследия ЮНЕСКО.",
        "Interiors and park form a unified museum of Classicism; "
        "the ensemble is UNESCO World Heritage.",
    ),
    "panel_housing_k7_series": (
        "Серия К-7 — один из первых массовых типовых панельных домов "
        "в СССР, освоенных с конца 1950-х годов.",
        "The K-7 series was among the first mass panel-housing types "
        "deployed across the USSR from the late 1950s.",
        "Четырёхэтажные секции собирались из керамзитобетонных панелей "
        "на заводах домостроения; планировки были унифицированы, "
        "а фасады получили характерную горизонтальную разбивку. "
        "Серия стала символом хрущёвской массовой жилищной программы "
        "и определила облик спальных районов Москвы и других городов.",
        "Four-storey blocks were assembled from expanded-clay concrete "
        "panels in house-building factories; layouts were standardised "
        "and façades gained a characteristic horizontal banding. "
        "The series epitomised Khrushchev-era mass housing and shaped "
        "the skyline of Moscow and other cities.",
        "Типовой образец индустриального домостроения 1950–1980-х.",
        "A model of Soviet industrialised housing of the 1950s–1980s.",
    ),
    "panel_housing_p44_series": (
        "Серия П-44 — распространённый тип панельного дома позднего "
        "советского периода с улучшенными планировками.",
        "The P-44 series is a widespread late-Soviet panel block with "
        "improved apartment layouts.",
        "Освоена с конца 1970-х годов; девятиэтажные корпуса получили "
        "более просторные кухни и комнаты по сравнению с ранними "
        "хрущёвками. П-44 формировала жилую среду новых микрорайонов "
        "и до сих пор определяет облик многих районов Москвы.",
        "Introduced in the late 1970s; nine-storey sections offered "
        "roomier kitchens and rooms than early Khrushchev-era flats. "
        "P-44 blocks shaped new micro-districts and still define many "
        "Moscow neighbourhoods.",
        "Показатель эволюции типового жилищного строительства СССР.",
        "Shows the evolution of Soviet standard housing construction.",
    ),
    "post_constructivism_zil_palace": (
        "Дворец культуры ЗИЛ — монумент переходного периода от "
        "конструктивизма к неоклассике 1930-х годов.",
        "The ZIL Palace of Culture is a monument of the transition "
        "from Constructivism to Neoclassicism in the 1930s.",
        "Спроектирован братьями Весниными в 1930–1937 годах для "
        "рабочих автозавода. Объёмный зал на колоннах, строгая "
        "геометрия фасада и парадная лестница сочетают авангардные "
        "приёмы с монументальным характером сталинской эпохи.",
        "Designed by the Vesnin brothers in 1930–1937 for the motor "
        "works. A columned auditorium hall, strict façade geometry "
        "and ceremonial stairs blend avant-garde devices with the "
        "monumental tone of the Stalin era.",
        "Важный памятник постконструктивизма и клубного зодчества.",
        "A key monument of post-Constructivism and workers' club design.",
    ),
    "post_constructivism_mohovaya_house": (
        "Жилой дом на Моховой улице — образец московского "
        "постконструктивизма 1934 года.",
        "The Mohovaya Street apartment house is a Moscow "
        "post-Constructivist landmark of 1934.",
        "Автор проекта — Иван Жолтовский; фасад сочетает строгую "
        "сетку окон с классическими пропорциями и лаконичным "
        "декором. Дом демонстрирует поиски советских архитекторов "
        "между авангардом и неоклассическим возрождением.",
        "Designed by Ivan Zholtovsky; the façade pairs a strict "
        "window grid with classical proportions and restrained "
        "ornament. The building shows Soviet architects navigating "
        "between avant-garde and Neoclassical revival.",
        "Показательный жилой дом эпохи постконструктивизма.",
        "A representative post-Constructivist apartment block.",
    ),
    "post_constructivism_arktika_hotel": (
        "Гостиница «Арктика» в Мурманске — северный памятник "
        "советского модернизма 1930-х годов.",
        "The Arktika Hotel in Murmansk is a northern monument of "
        "1930s Soviet modernism.",
        "Возведена в 1933–1936 годах как крупнейшая гостиница "
        "Заполярья; массивный объём и сдержанный декор отражают "
        "климатические и индустриальные условия Кольского края. "
        "Здание долгое время задавало архитектурный облик города.",
        "Built in 1933–1936 as the largest hotel in the Far North; "
        "its massive volume and restrained décor respond to the "
        "climate and industry of the Kola region. For decades it "
        "shaped Murmansk's skyline.",
        "Редкий пример постконструктивизма за Полярным кругом.",
        "A rare post-Constructivist work above the Arctic Circle.",
    ),
    "regional_soviet_yubileyny_palace": (
        "Дворец спорта «Юбилейный» на Петроградской стороне — "
        "один из главных спортивных залов Ленинграда–Петербурга.",
        "The Yubileyny Sports Palace on the Petrograd Side is one "
        "of Leningrad–St Petersburg's principal arenas.",
        "Построен в 1967 году по проекту Александра Васильева, "
        "Юрия Шеваржинского и Владимира Кубинского. Круглый в плане "
        "зал на 7 000 зрителей обслуживал хоккей, концерты и "
        "массовые мероприятия; фасад сочетает стекло и бетонные "
        "кольца в духе советского модернизма.",
        "Built in 1967 to designs by Alexander Vasiliev, Yuri "
        "Shevarzhinsky and Vladimir Kubinsky. A circular hall seating "
        "7,000 hosted hockey, concerts and mass events; glass and "
        "concrete rings express Soviet modernism.",
        "Символ ленинградского спорта и концертной жизни 1960–1980-х.",
        "A symbol of Leningrad sport and concert life in the 1960s–80s.",
    ),
    "regional_soviet_luzhniki_stadium": (
        "Стадион «Лужники» — главная спортивная арена СССР и России.",
        "Luzhniki Stadium is the principal sports arena of the USSR "
        "and Russia.",
        "Открыт в 1956 году как Центральный стадион имени В. И. "
        "Ленина в комплексе на Ленинских горах. Большая спортивная "
        "арена, плавательный бассейн и трибуны образуют ансамбль "
        "у Москвы-реки; стадион неоднократно реконструировался, "
        "сохраняя роль центра крупнейших соревнований.",
        "Opened in 1956 as the Lenin Central Stadium in the Lenin "
        "Hills complex. The main arena, swimming pool and stands "
        "form an ensemble on the Moskva River; repeatedly rebuilt, "
        "it remains the country's premier competition venue.",
        "Ключевой памятник регионального советского спортивного "
        "зодчества.",
        "A key monument of regional Soviet sports architecture.",
    ),
    "regional_soviet_novosibirsk_opera": (
        "Новосибирский театр оперы и балета — крупнейший театр "
        "Сибири и символ советского культурного освоения региона.",
        "The Novosibirsk Opera and Ballet Theatre is Siberia's "
        "largest theatre and a symbol of Soviet cultural expansion.",
        "Строительство велось в 1931–1945 годах по проекту "
        "Александра Крячкова; монументальный неоклассический "
        "объём с колоннадой доминирует над центром города. "
        "Открытие театра стало событием всесоюзного значения.",
        "Built in 1931–1945 to Alexander Kryachkov's design; a "
        "monumental Neoclassical volume with a colonnade dominates "
        "the city centre. Its opening was an event of Union-wide "
        "importance.",
        "Важнейший образец регионального советского зодчества.",
        "The foremost example of regional Soviet architecture.",
    ),
    "postmodernism_moscow_theaters_4_2": (
        "Театр «Современник» — одна из главных драматических сцен "
        "Москвы, основанная в эпоху «оттепели».",
        "The Sovremennik Theatre is one of Moscow's leading drama "
        "stages, founded during the Thaw.",
        "Создан в 1956 году как студия молодых актёров; с 1964 года "
        "размещается в здании на Чистопрудном бульваре. Репертуар "
        "сочетает классику и современную драматургию; театр стал "
        "символом обновления сценической жизни 1960-х.",
        "Founded in 1956 as a young actors' studio; since 1964 it "
        "has occupied the building on Chistoprudny Boulevard. Its "
        "repertoire mixes classics and new drama and became an "
        "emblem of 1960s stage renewal.",
        "Культовая площадка московского театра второй половины "
        "XX века.",
        "An iconic Moscow theatre of the late 20th century.",
    ),
    "mature_classicism_kazan_cathedral_spb": (
        "Казанский собор на Невском проспекте — шедевр зрелого "
        "классицизма, созданный Андреем Воронихиным.",
        "Kazan Cathedral on Nevsky Prospekt is a mature "
        "Neoclassical masterpiece by Andrey Voronikhin.",
        "Строительство велось в 1801–1811 годах на месте каменной "
        "церкви Казанской иконы Божией Матери. Полукруглая "
        "колоннада из 96 колонн коринфского ордера обращена к "
        "Невскому проспекту; в интерьере — икона Казанской "
        "Божией Матери. После революции храм закрыли; с 1930-х "
        "здесь размещался Музей атеизма, в 1990-е собор возвращён "
        "церкви.",
        "Built in 1801–1811 on the site of an earlier church of "
        "Our Lady of Kazan. A semicircular colonnade of "
        "ninety-six Corinthian columns faces Nevsky Prospekt; the "
        "interior holds the venerated Kazan icon. Closed after "
        "1917, it housed the Museum of the History of Religion "
        "from the 1930s and was returned to the church in the "
        "1990s.",
        "Главный храмовый памятник Воронихина и доминанта "
        "центральной магистрали Петербурга.",
        "Voronikhin's principal church and the dominant landmark "
        "of central St Petersburg.",
    ),
    "mature_classicism_tauride_palace": (
        "Таврический дворец — строгий классицистический ансамбль "
        "Ивана Старова на Шпалерной улице.",
        "Tauride Palace is Ivan Starov's austere Neoclassical "
        "ensemble on Shpalernaya Street.",
        "Возведён в 1783–1789 годах для князя Григория Потёмкина; "
        "за парадным двором — Таврический сад. Скромные фасады "
        "контрастируют с роскошью парадных залов. В 1906–1917 "
        "годах здесь работала Государственная дума и Временное "
        "правительство; в 1918 году собралось Учредительное "
        "собрание.",
        "Built in 1783–1789 for Prince Grigory Potemkin; the "
        "Tauride Garden lies behind the main courtyard. Restrained "
        "façades contrast with lavish state rooms. From 1906 to "
        "1917 it housed the State Duma and the Provisional "
        "Government; the Constituent Assembly met here in 1918.",
        "Символ петербургского классицизма и политической истории "
        "начала XX века.",
        "A symbol of Petersburg classicism and early twentieth-"
        "century political history.",
    ),
    "pseudo_russian_savior_on_blood": (
        "Храм Спаса на Крови — памятник «русского стиля» на канале "
        "Грибоедова, возведённый Альфредом Парландом.",
        "The Church of the Savior on Blood is a Russian Revival "
        "memorial on the Griboedov Canal, built by Alfred Parland.",
        "Заложен в 1883 году на месте покушения на императора "
        "Александра II (1 марта 1881 года). Строительство "
        "завершено в 1907 году; пять куполов и яркая "
        "керамическая отделка фасадов напоминают московские "
        "храмы XVII века. Интерьеры украшены мозаиками по "
        "эскизам В. М. Васнецова и других художников.",
        "Founded in 1883 on the site of the assassination of "
        "Emperor Alexander II (1 March 1881). Completed in 1907; "
        "five domes and vivid ceramic ornament echo seventeenth-"
        "century Moscow churches. Interiors are lined with mosaics "
        "after designs by Viktor Vasnetsov and other artists.",
        "Один из самых узнаваемых храмов Петербурга и крупнейших "
        "мозаичных ансамблей Европы.",
        "One of St Petersburg's best-known churches and among "
        "Europe's largest mosaic ensembles.",
    ),
    "early_classicism_mikhailovsky_castle_2": (
        "Михайловский замок — резиденция императора Павла I, "
        "возведённая в конце XVIII века.",
        "Mikhailovsky Castle is Emperor Paul I's residence, built "
        "at the end of the eighteenth century.",
        "Строительство велось в 1797–1801 годах по проектам "
        "Винченцо Бренны, Василия Баженова и Ивана Старова. "
        "Замок окружён каналами и напоминает крепость; в центре — "
        "восьмиугольный двор. Павел I переехал сюда из Зимнего "
        "дворца и был убит в 1801 году в собственных покоях. "
        "Сегодня в здании — филиал Русского музея.",
        "Built in 1797–1801 to designs by Vincenzo Brenna, Vasily "
        "Bazhenov and Ivan Starov. Canals surround the castle-like "
        "volume; an octagonal courtyard lies at its heart. Paul I "
        "moved here from the Winter Palace and was killed in 1801 "
        "in his apartments. The building now houses a branch of "
        "the Russian Museum.",
        "Редкий образец «костюмированной» архитектуры рубежа "
        "XVIII–XIX веков в центре Петербурга.",
        "A rare example of theatrical turn-of-the-century "
        "architecture in central St Petersburg.",
    ),
    "empire_mikhailovsky_castle_2": (
        "Михайловский замок Павла I — редкий для Петербурга тип "
        "укреплённой императорской резиденции.",
        "Emperor Paul I's Mikhailovsky Castle is a rare fortified "
        "imperial residence type in St Petersburg.",
        "Строгий силуэт с каналами и восьмиугольным двором "
        "скрывает парадные интерьеры Винченцо Бренны. После "
        "гибели Павла I в 1801 году дворец служил военным "
        "учреждениям; ныне здесь филиал Русского музея с "
        "реставрированными залами.",
        "A strict silhouette with canals and an octagonal courtyard "
        "conceals Brenna's state interiors. After Paul's death in "
        "1801 the palace housed military institutions; today a "
        "Russian Museum branch displays restored halls.",
        "Образец «костюмированной» архитектуры рубежа XVIII–XIX "
        "веков.",
        "A specimen of theatrical turn-of-the-century architecture.",
    ),
    "russo_byzantine_christ_savior": (
        "Храм Христа Спасителя — главный храм Русской "
        "Православной Церкви на берегу Москвы-реки.",
        "The Cathedral of Christ the Saviour is the principal "
        "church of the Russian Orthodox Church on the Moskva "
        "River embankment.",
        "Первый храм заложен в 1839 году по проекту "
        "К. А. Тона в память победы 1812 года; освящён в "
        "1883 году. В 1931 году собор взорван; на его месте "
        "планировали Дворец Советов. Восстановлен в 1990–2000 "
        "годах как точная копия первоначального здания.",
        "The first cathedral was begun in 1839 to Konstantin "
        "Thon's design as a memorial to the war of 1812 and "
        "consecrated in 1883. It was demolished in 1931; a "
        "Palace of Soviets was planned on the site. Rebuilt "
        "in 1990–2000 as a close replica of the original.",
        "Символ духовного возрождения и крупнейший "
        "православный храм столицы.",
        "A symbol of spiritual renewal and the capital's "
        "largest Orthodox church.",
    ),
    "eclecticism_moscow_osobnjaki_5_2": (
        "Дом Рукавишникова на Большой Никитской — "
        "городская усадьба с парадным фасадом в эклектике.",
        "The Rukavishnikov House on Bolshaya Nikitskaya is an "
        "urban mansion with an eclectic parade façade.",
        "Усадьба известна с XVIII века; каменный особняк "
        "перестраивался в XIX веке и принадлежал роду "
        "Рукавишниковых. Сохранились фасад с арочными "
        "окнами и элементы интерьеров.",
        "The estate dates to the eighteenth century; the stone "
        "mansion was rebuilt in the nineteenth century for the "
        "Rukavishnikov family. An arched façade and interior "
        "fragments survive.",
        "Памятник усадебной архитектуры на одной из старинных "
        "улиц центра.",
        "A monument of mansion architecture on one of the "
        "historic streets of the centre.",
    ),
    "eclecticism_moscow_osobnjaki_4_2": (
        "Особняк А. А. Морозова на Воздвиженке — один из "
        "самых ярких домов московской эклектики.",
        "Arseny Morozov's mansion on Vozdvizhenka is one of "
        "Moscow's boldest eclectic town houses.",
        "Построен в 1895–1899 годах по проекту В. А. "
        "Каменского. Необычный фасад с башней и розовой "
        "отделкой; по легенде, императрица запретила строить "
        "«подобное» в Москве.",
        "Built in 1895–1899 to Viktor Kamensky's design. An "
        "unusual towered façade with pink ornament; legend "
        "claims the empress forbade building anything similar "
        "in Moscow.",
        "Символ модерна и эклектики на Воздвиженке.",
        "A landmark of Art Nouveau and eclecticism on "
        "Vozdvizhenka.",
    ),
    "neo_russian_yaroslavsky_station": (
        "Ярославский вокзал на Комсомольской площади — "
        "главный «сибирский» вокзал Москвы в неорусском стиле.",
        "Yaroslavsky terminal on Komsomolskaya Square is Moscow's "
        "principal Siberian railway station in Neo-Russian style.",
        "Первый каменный вокзал вырос здесь в 1860-е; нынешнее "
        "здание перестроено в 1902–1904 годах по проекту "
        "Ф. О. Шехтеля, с участием А. В. Щусева. Фасад с "
        "килевидными крышами, арками и майоликой напоминает "
        "древнерусский терем; отсюда отправляется "
        "Транссибирский экспресс.",
        "A stone terminal rose here in the 1860s; the present "
        "building was rebuilt in 1902–1904 to Fyodor Shekhtel's "
        "design with Alexey Shchusev. Gabled roofs, arches and "
        "majolica evoke a Russian terem; the Trans-Siberian "
        "Express departs from its platforms.",
        "Сказочный силуэт Шехтеля и начало пути на восток "
        "страны.",
        "Shekhtel's fairy-tale silhouette and the gateway to "
        "Russia's east.",
    ),
    "neo_russian_feodorovsky_cathedral": (
        "Собор Феодоровской иконы Божией Матери в Царском "
        "Селе — храм неорусского стиля для императорской семьи.",
        "The Feodorovsky Cathedral in Pushkin is a Neo-Russian "
        "church built for the imperial family.",
        "Возведён в 1911–1914 годах по проекту С. С. "
        "Кричинского рядом с Александровским дворцом. "
        "Пятоглавый храм с кирпичным декором и "
        "шатровыми главками задумывался как домовая церковь "
        "Романовых; в советское время был разрушен и "
        "восстановлен в 2010-х.",
        "Built in 1911–1914 to Stepan Krichinsky's design near "
        "the Alexander Palace. Five domes, ornamental brick and "
        "tent-like cupolas formed the Romanovs' house church; "
        "badly damaged in Soviet times, it was restored in the "
        "2010s.",
        "Редкий образец позднего неорусского стиля "
        "императорского пригорода.",
        "A rare late Neo-Russian monument of the imperial "
        "suburb.",
    ),
    "art_nouveau_ryabushinsky_mansion": (
        "Особняк Рябушинского на Малой Никитской — один из "
        "главных шедевров московского модерна Ф. О. Шехтеля.",
        "The Ryabushinsky Mansion on Malaya Nikitskaya is one "
        "of Fyodor Shekhtel's chief Art Nouveau masterpieces.",
        "Построен в 1900–1903 годах для купца С. П. "
        "Рябушинского. Асимметричный фасад, витражи и "
        "знаменитая «лестница-волна» внутри; интерьеры "
        "сохранили декор модерна. С 1965 года здесь "
        "музей-квартира М. Горького.",
        "Built in 1900–1903 for merchant S. P. Ryabushinsky. "
        "An asymmetrical façade, stained glass and the famous "
        "wave staircase; Art Nouveau interiors survive. Since "
        "1965 it has housed the Gorky House Museum.",
        "Образец синтеза архитектуры, декоративного искусства "
        "и быта рубежа веков.",
        "A synthesis of architecture, decorative art and "
        "fin-de-siècle life.",
    ),
    "moscow_fifteenth_sixteenth_kremlin_dormition": (
        "Успенский собор — главный храм Московского Кремля и "
        "место венчания русских государей.",
        "The Dormition Cathedral is the principal church of "
        "the Moscow Kremlin and the site of Russian coronations.",
        "Построен в 1475–1479 годах итальянским зодчим "
        "Аристотелем Фиораванти на месте собора XIV века. "
        "Фиораванти соединил традицию русского пятиглавия с "
        "ренессансной конструкцией; до 1917 года здесь "
        "венчались на царство от Ивана IV до Николая II.",
        "Built in 1475–1479 by Aristotele Fioravanti on the "
        "site of a fourteenth-century cathedral. He combined "
        "the Russian five-dome scheme with Renaissance "
        "structure; from Ivan IV to Nicholas II, Russian "
        "rulers were crowned here until 1917.",
        "Усыпальница митрополитов и патриархов; образец "
        "кремлёвского зодчества эпохи Ивана III.",
        "Burial place of metropolitans and patriarchs; a "
        "landmark of Kremlin architecture under Ivan III.",
    ),
    "pskov_school_epiphany_zapskovye": (
        "Церковь Богоявления с Запсковья — жемчужина "
        "псковского зодчества на правом берегу Великой.",
        "The Epiphany Church from Zapskovye is a gem of "
        "Pskov architecture on the right bank of the Velikaya.",
        "Возведена в конце XV — начале XVI века; к "
        "храму примыкает отдельная колокольня. Строгий "
        "кубический объём, три апсиды и лаконичный декор "
        "характерны для псковской школы.",
        "Erected in the late fifteenth or early sixteenth "
        "century with a freestanding bell tower. A compact "
        "cubic volume, three apses and restrained ornament "
        "typify the Pskov school.",
        "Один из лучших сохранившихся памятников "
        "средневекового Пскова вне Крома.",
        "One of the best-preserved medieval monuments of "
        "Pskov beyond the Krom.",
    ),
    "pskov_school_pskov_kremlin": (
        "Псковский кремль (Кром) — древнее ядро города на "
        "высоком мысе у слияния рек.",
        "The Pskov Kremlin (Krom) is the ancient core of the "
        "city on a high cape at the confluence of rivers.",
        "Крепость складывалась с X века; каменные стены и "
        "башни — в основном XV–XVII веков. В ансамбле — "
        "Троицкий собор, Довмонтов город, Приказные палаты.",
        "The fortress grew from the tenth century; most stone "
        "walls and towers date from the fifteenth to "
        "seventeenth centuries. The ensemble includes Trinity "
        "Cathedral, Dovmont's Town and the Prikaz Chambers.",
        "Символ оборонительной славы Псковской земли и "
        "центр городской истории.",
        "A symbol of Pskov's defensive history and the "
        "focus of the city's past.",
    ),
    "novgorod_school_theodore_stratilat": (
        "Церковь Фёдора Стратилата на Ручью — один из "
        "ранних новгородских храмов с фресками XIV века.",
        "The Church of Theodore Stratelates on the Brook is "
        "an early Novgorod church with fourteenth-century "
        "frescoes.",
        "Построена в 1360–1361 годах на торговом берегу "
        "Волхова. Четырёхстолпный четверик с тремя апсидами "
        "сохранил росписи, в том числе образы святых в "
        "полный рост.",
        "Built in 1360–1361 on the trading bank of the "
        "Volkhov. Its four-pier cube with three apses "
        "preserves frescoes including full-length saints.",
        "Образец новгородской школы до влияния московского "
        "узорочья.",
        "An example of the Novgorod school before Moscow "
        "ornamental influence.",
    ),
    "novgorod_school_transfiguration_ilyina": (
        "Церковь Спаса Преображения на Ильине — памятник "
        "новгородского зодчества 1374 года с фресками Феофана Грека.",
        "The Church of the Transfiguration on Ilyina Street is a "
        "1374 Novgorod monument with frescoes by Theophanes the Greek.",
        "Построена в 1374 году; росписи Феофана Грека (1378) — "
        "один из вершинных памятников византийско-новгородской "
        "живописи XIV века.",
        "Built in 1374; frescoes by Theophanes the Greek (1378) "
        "rank among the finest monuments of fourteenth-century "
        "Byzantine-Novgorod painting.",
        "Главный храм новгородской школы на Торговой стороне.",
        "The principal church of the Novgorod school on the "
        "commercial side of the city.",
    ),
    "mature_classicism_pushkin_house_2": (
        "Дом-музей А. С. Пушкина на Арбате — мемориальный "
        "особняк в стиле ампира.",
        "The Pushkin House Museum on the Arbat is a memorial "
        "mansion in Empire style.",
        "Построен в 1814 году; с 1986 года — музей поэта. "
        "Интерьеры восстановлены по документам XIX века.",
        "Built in 1814; a museum to the poet since 1986. "
        "Interiors were restored from nineteenth-century records.",
        "Важный адрес московской литературной топографии.",
        "A key address on Moscow's literary map.",
    ),
    "early_classicism_tauride_palace_2": (
        "Таврический дворец — строгий классицистический ансамбль "
        "Ивана Старова на Шпалерной улице.",
        "Tauride Palace is Ivan Starov's austere Neoclassical "
        "ensemble on Shpalernaya Street.",
        "Возведён в 1783–1789 годах для князя Григория Потёмкина; "
        "за парадным двором — Таврический сад.",
        "Built in 1783–1789 for Prince Grigory Potemkin; the "
        "Tauride Garden lies behind the main courtyard.",
        "Символ петербургского классицизма и политической истории "
        "начала XX века.",
        "A symbol of Petersburg classicism and early twentieth-"
        "century political history.",
    ),
    "mature_classicism_tauride_palace": (
        "Таврический дворец — ансамбль зрелого классицизма на "
        "Шпалерной улице.",
        "Tauride Palace is a mature Neoclassical ensemble on "
        "Shpalernaya Street.",
        "Строгие фасады скрывают парадные залы; с 1906 года здесь "
        "работала Государственная дума.",
        "Restrained façades conceal state rooms; from 1906 the "
        "State Duma met here.",
        "Памятник эпохи Потёмкина и рубежа империи и революции.",
        "A monument to Potemkin's era and the imperial–revolutionary "
        "turn.",
    ),
    "empire_tauride_palace_2": (
        "Таврический дворец — резиденция князя Потёмкина, позже "
        "центр политической жизни Петербурга.",
        "Tauride Palace was Prince Potemkin's residence and later "
        "a centre of Petersburg political life.",
        "В 1918 году здесь собралось Учредительное собрание; "
        "сегодня — Межпарламентская ассамблея СНГ.",
        "The Constituent Assembly met here in 1918; today it "
        "houses the CIS Interparliamentary Assembly.",
        "Классицистический облик и гражданская память.",
        "Neoclassical form and civic memory.",
    ),
    "empire_triumphal_gate_moscow": (
        "Триумфальные ворота на Кутузовском проспекте — "
        "монумент победе 1812 года.",
        "The Triumphal Arch on Kutuzovsky Prospekt commemorates "
        "the victory of 1812.",
        "Первые ворота у Тверской заставы возвёл О. И. Бове "
        "в 1829–1834 годах; нынешняя копия на Поклонной горе "
        "открыта в 1968 году по обмерам оригинала.",
        "O. I. Bove built the first arch at Tverskaya Zastava in "
        "1829–1834; the present replica on Poklonnaya Hill opened "
        "in 1968 from the original drawings.",
        "Образец русской триумфальной архитектуры и символ "
        "Отечественной войны.",
        "A model of Russian triumphal architecture and a symbol "
        "of the Patriotic War.",
    ),
    "neo_russian_tretyakov_facade": (
        "Государственная Третьяковская галерея — музей русского "
        "искусства с фасадом по эскизу В. М. Васнецова.",
        "The State Tretyakov Gallery is Russia's national museum "
        "of Russian art with a façade after Viktor Vasnetsov's "
        "design.",
        "Основана П. М. Третьяковым в 1856 году; здание в "
        "Лаврушинском переулке расширялось в 1900–1906 годах "
        "в неорусском стиле.",
        "Founded by Pavel Tretyakov in 1856; the Lavrushinsky "
        "Lane building was enlarged in 1900–1906 in Neo-Russian "
        "style.",
        "Фасад Васнецова — один из узнаваемых символов "
        "Замоскворечья.",
        "Vasnetsov's façade is a landmark of Zamoskvorechye.",
    ),
    "art_nouveau_vitebsky_station": (
        "Витебский вокзал — один из старейших вокзалов России "
        "и шедевр петербургского модерна.",
        "Vitebsky station is one of Russia's oldest rail terminals "
        "and a masterpiece of St Petersburg Art Nouveau.",
        "Нынешнее здание 1904 года с витражами и кованым декором "
        "сохранило атмосферу рубежа веков; отправление в "
        "Пушкин и Павловск.",
        "The 1904 building with stained glass and wrought iron "
        "preserves fin-de-siècle atmosphere; trains to Pushkin "
        "and Pavlovsk.",
        "Образец модерна в транспортной архитектуре.",
        "A model of Art Nouveau in transport architecture.",
    ),
    "neoclassicism_early20_isakov_apartment": (
        "Доходный дом И. П. Исакова — образец московского "
        "модерна Льва Кекушева.",
        "The I. P. Isakov apartment house is a Moscow Art Nouveau "
        "work by Lev Kekushev.",
        "Построен в 1904–1906 годах на Большой Никитской; "
        "асимметричный фасад, эркеры и скульптурный декор.",
        "Built in 1904–1906 on Bolshaya Nikitskaya; an "
        "asymmetrical façade with bay windows and sculptural "
        "ornament.",
        "Памятник эпохи «золотой мили».",
        "A monument of the golden-mile era.",
    ),
    "avant_garde_melnikov_house": (
        "Дом Мельникова — шедевр конструктивизма и личная "
        "мастерская архитектора.",
        "Melnikov House is a Constructivist masterpiece and the "
        "architect's own studio.",
        "Построен в 1927–1929 годах на Кривоарбатском переулке; "
        "два пересекающихся цилиндра с шестиугольными окнами.",
        "Built in 1927–1929 on Krivoarbatsky Lane; two "
        "intersecting cylinders with hexagonal windows.",
        "Один из главных символов московского авангарда.",
        "One of the chief symbols of Moscow avant-garde.",
    ),
    "avant_garde_shukhov_tower": (
        "Шуховская башня — гиперболоидная конструкция Владимира "
        "Шухова на Шаболовке.",
        "The Shukhov Tower is Vladimir Shukhov's hyperboloid "
        "structure on Shabolovka.",
        "Возведена в 1922 году как радиопередающая башня; "
        "сетчатая стальная оболочка стала эталоном инженерной "
        "эстетики XX века.",
        "Erected in 1922 as a radio tower; its steel lattice "
        "shell became an icon of twentieth-century engineering.",
        "Памятник мировой инженерной мысли.",
        "A monument of world engineering.",
    ),
    "constructivism_zuev_club": (
        "ДК имени Зуева — клуб работников текстильной фабрики "
        "в духе конструктивизма.",
        "The Zuev Workers' Club served a textile factory in "
        "Constructivist style.",
        "Спроектирован Ильёй Голосовым в 1927–1929 годах; "
        "стеклянный цилиндр на массивном постаменте.",
        "Designed by Ilya Golosov in 1927–1929; a glass cylinder "
        "on a massive pedestal.",
        "Один из самых узнаваемых клубов Москвы.",
        "One of Moscow's most recognisable workers' clubs.",
    ),
    "constructivism_rusakov_club": (
        "ДК имени Русакова — клуб Мельникова для работников "
        "коммунального хозяйства.",
        "The Rusakov Workers' Club is Melnikov's club for "
        "municipal workers.",
        "Три консольных объёма зрительного зала вынесены на "
        "фасад; внутри — зал на 800 мест.",
        "Three cantilevered auditorium volumes project from the "
        "façade; the hall seats 800.",
        "Шедевр конструктивизма на Стромынке.",
        "A Constructivist masterpiece on Stromynka.",
    ),
    "avant_garde_moscow_buildings_2_2": (
        "",
        "The House on the Embankment is a residential complex by "
        "Boris Iofan for the Soviet party elite.",
        "",
        "Built in 1927–1931; more than 500 flats housed Voroshilov, "
        "Mikoyan, Khrushchev and Kosygin, with a cinema, shops and "
        "clinic in the block. Many residents were repressed in the "
        "1930s; a museum in one entrance has told their stories since "
        "1989.",
        "",
        "An outstanding Constructivist monument and symbol of 1930s "
        "nomenklatura life on Bolotnaya Embankment.",
    ),
    "constructivism_moscow_buildings_2_2": (
        "",
        "The House on the Embankment is a residential complex by "
        "Boris Iofan for the Soviet party elite.",
        "",
        "Built in 1927–1931; more than 500 flats housed Voroshilov, "
        "Mikoyan, Khrushchev and Kosygin, with a cinema, shops and "
        "clinic in the block. Many residents were repressed in the "
        "1930s; a museum in one entrance has told their stories since "
        "1989.",
        "",
        "An outstanding Constructivist monument and symbol of 1930s "
        "nomenklatura life on Bolotnaya Embankment.",
    ),
    "post_constructivism_moscow_buildings_2_2": (
        "",
        "The House on the Embankment is a residential complex by "
        "Boris Iofan for the Soviet party elite.",
        "",
        "Built in 1927–1931; more than 500 flats housed Voroshilov, "
        "Mikoyan, Khrushchev and Kosygin, with a cinema, shops and "
        "clinic in the block. Many residents were repressed in the "
        "1930s; a museum in one entrance has told their stories since "
        "1989.",
        "",
        "An outstanding Constructivist monument and symbol of 1930s "
        "nomenklatura life on Bolotnaya Embankment.",
    ),
    "constructivism_narkomfin": (
        "Дом Наркомфина — жилой комплекс Моисея Гинзбурга и "
        "Игнатия Милиниса на Новинском бульваре.",
        "The Narkomfin Building is a housing block by Moisei "
        "Ginzburg and Ignaty Milinis on Novinsky Boulevard.",
        "Построен в 1928–1930 годах как эксперимент "
        "коллективного быта: галереи, «трансформируемые» "
        "квартиры, разделение жилых и общественных функций.",
        "Built in 1928–1930 as an experiment in collective "
        "living: galleries, transformable flats, and a split "
        "between private and communal spaces.",
        "Один из главных памятников конструктивизма в мире; "
        "объект культурного наследия федерального значения.",
        "One of the world's foremost Constructivist landmarks; "
        "a federally protected heritage site.",
    ),
    "soviet_modernism_tass_building": (
        "Здание ТАСС — монумент советского модернизма на "
        "Тверской улице.",
        "The TASS building is a monument of Soviet modernism on "
        "Tverskaya Street.",
        "Построено в 1960-е годы по проекту Дмитрия Чечулина; "
        "строгий объём с ритмом вертикальных пилонов.",
        "Built in the 1960s to Dmitry Chechulin's design; a "
        "strict volume with a rhythm of vertical pylons.",
        "Символ советской информационной системы.",
        "A symbol of the Soviet news agency.",
    ),
    "stalinist_neoclassicism_gagarin_square_house": (
        "Дом на площади Гагарина — жилой корпус сталинского "
        "ампира на Ленинском проспекте.",
        "The Gagarin Square apartment house is a Stalinist Empire "
        "residential block on Leninsky Prospekt.",
        "Возведён в 1949–1955 годах; портики, башенки и "
        "парадный масштаб типичны для послевоенной застройки.",
        "Built in 1949–1955; porticos, turrets and ceremonial "
        "scale typify post-war development.",
        "Часть ансамбля площади Гагарина.",
        "Part of the Gagarin Square ensemble.",
    ),
    "stalinist_neoclassicism_kutuzovsky_avenue": (
        "Застройка Кутузовского проспекта — ансамбль "
        "сталинского ампира 1940–1950-х годов.",
        "Kutuzovsky Avenue is an ensemble of Stalinist Empire "
        "architecture from the 1940s–50s.",
        "Высотные жилые дома, посольства и общественные здания "
        "формируют парадную магистраль запада Москвы.",
        "High-rise housing, embassies and public buildings form "
        "the ceremonial westward artery of Moscow.",
        "Силуэт проспекта — визитная карточка эпохи.",
        "The avenue's skyline is a hallmark of the era.",
    ),
    "art_deco_red_army_theater": (
        "Центральный театр Красной Армии (ЦТКА) — монумент "
        "ар-деко и сталинского ампира.",
        "The Central Red Army Theatre (CTKA) combines Art Deco "
        "and Stalinist Empire.",
        "Построен в 1934–1940 годах; пятиконечная звезда над "
        "залом и монументальный интерьер.",
        "Built in 1934–1940; a five-pointed star crowns the hall "
        "with a monumental interior.",
        "Главная сцена военно-патриотического репертуара.",
        "The principal stage for military-patriotic repertoire.",
    ),
    "art_nouveau_singer_house": (
        "Дом компании «Зингер» на Невском проспекте — "
        "один из символов петербургского модерна.",
        "The Singer Company House on Nevsky Prospekt is one "
        "of St Petersburg's Art Nouveau landmarks.",
        "Построен в 1902–1904 годах по проекту П. Ю. Сюзора "
        "для российского представительства фирмы швейных "
        "машин. Стеклянный купол с золочёным орлом "
        "поднимается над угловым участком; с 1938 года "
        "здание известно как «Дом книги».",
        "Built in 1902–1904 to Pavel Suzor's design for the "
        "Singer sewing-machine company. A glass dome with a "
        "gilded eagle crowns the corner site; since 1938 the "
        "building has been known as the House of Books.",
        "Доминианта Невского проспекта и памятник "
        "коммерческого модерна.",
        "A Nevsky Prospekt landmark and monument of "
        "commercial Art Nouveau.",
    ),
    "novgorod_school_moscow_places_of_worship_7_2": (
        "Церковь Рождества Богородицы в Путинках — один из "
        "последних храмов московского узорочья с трёхшатровым "
        "завершением.",
        "The Church of the Nativity of the Theotokos in Putinki "
        "is among the last Moscow uzorochye churches with a "
        "triple-tent façade.",
        "Построена в 1649–1652 годах; название — от «пути» "
        "(здесь находился посольский двор). Уникальное "
        "трёхшатровое завершение и богатый кирпичный декор; "
        "сохранился иконостас XVII века.",
        "Built in 1649–1652; the name recalls the embassy "
        "quarter («puti»). A triple-tent crown and rich brick "
        "ornament; the seventeenth-century iconostasis survives.",
        "Образец московского узорочья; единственный в Москве "
        "храм с трёхшатровым завершением.",
        "A Moscow uzorochye landmark; the city's only church "
        "with a triple-tent crown.",
    ),
    "ancient_rus_moscow_places_of_worship_3_2": (
        "Успенский собор — главный храм Московского Кремля и "
        "место венчания русских государей.",
        "The Dormition Cathedral is the principal church of "
        "the Moscow Kremlin and the site of Russian coronations.",
        "Построен в 1475–1479 годах итальянским зодчим "
        "Аристотелем Фиораванти на месте собора XIV века. "
        "До 1917 года здесь венчались на царство от Ивана IV "
        "до Николая II; хоронили митрополитов и патриархов.",
        "Built in 1475–1479 by Aristotele Fioravanti on the "
        "site of a fourteenth-century cathedral. Russian rulers "
        "were crowned here until 1917; metropolitans and "
        "patriarchs were buried within.",
        "Главный храм Российского государства до 1917 года; "
        "образец кремлёвского зодчества XV века.",
        "Russia's principal cathedral until 1917; a landmark "
        "of fifteenth-century Kremlin architecture.",
    ),
    "uzorochye_terem_palace": (
        "Теремной дворец — жилой комплекс русских государей "
        "в Московском Кремле, вершина московского узорочья.",
        "The Terem Palace is the royal residential block of "
        "the Moscow Kremlin and a peak of Moscow uzorochye.",
        "Возведён в 1635–1636 годах на месте более ранних "
        "построек; золочёные кровли, наличники и кокошники "
        "украшают фасады. Соединён с Грановитой палатой и "
        "соборами Кремля в единый царский ансамбль.",
        "Built in 1635–1636 on earlier foundations; gilded "
        "roofs, window surrounds and kokoshnik ornament "
        "decorate the façades. Linked to the Faceted Chamber "
        "and Kremlin cathedrals in one royal ensemble.",
        "Резиденция царской семьи до переноса столицы в "
        "Петербург; редкий сохранившийся терем XVII века.",
        "Home of the tsar's family until the capital moved "
        "to St Petersburg; a rare surviving seventeenth-century "
        "terem.",
    ),
    "uzorochye_nativity_putinki": (
        "Церковь Рождества Богородицы в Путинках — шедевр "
        "московского узорочья с трёхшатровым завершением.",
        "The Church of the Nativity in Putinki is a masterpiece "
        "of Moscow uzorochye with a triple-tent crown.",
        "Построена в 1649–1652 годах на Малой Дмитровке. "
        "Три декоративных шатра на фасаде и насыщенный "
        "кирпичный декор создают праздничный силуэт; "
        "иконостас XVII века сохранился до наших дней.",
        "Built in 1649–1652 on Malaya Dmitrovka. Three "
        "decorative tents and dense brick ornament give a "
        "festive skyline; the seventeenth-century iconostasis "
        "survives.",
        "Единственный в Москве храм с трёхшатровым "
        "завершением; образец позднего узорочья.",
        "Moscow's only triple-tent church; a late uzorochye "
        "landmark.",
    ),
    "uzorochye_trinity_nikitniki": (
        "Церковь Троицы в Никитниках — домовый храм купца "
        "Никитникова в духе московского узорочья.",
        "The Church of the Trinity in Nikitniki is the "
        "merchant Nikitnikov's house church in Moscow uzorochye.",
        "Построена в 1628–1653 годах в Китай-городе. "
        "Нарядный кирпичный декор, шатровая колокольня и "
        "асимметричная композиция; в интерьере — росписи "
        "Симона Ушакова 1650-х годов.",
        "Built in 1628–1653 in Kitay-gorod. Ornamental brickwork, "
        "a tent bell tower and an asymmetric plan; Simon Ushakov's "
        "1650s frescoes remain inside.",
        "Памятник посадского зодчества XVII века; музей и "
        "действующий храм.",
        "A seventeenth-century parish masterpiece; museum and "
        "working church.",
    ),
    "elizabethan_baroque_winter_palace": (
        "Зимний дворец — главная императорская резиденция "
        "в Санкт-Петербурге и ядро Эрмитажа.",
        "The Winter Palace was the principal imperial residence "
        "in St Petersburg and forms the core of the Hermitage.",
        "Построен в 1754–1762 годах Бартоломео Растрелли на "
        "Дворцовой набережной; зелёные фасады с белыми колоннами "
        "и золочёные шпили определяют ансамбль Дворцовой площади. "
        "После 1917 года дворец стал музеем мирового значения.",
        "Built in 1754–1762 by Bartolomeo Rastrelli on the "
        "Palace Embankment; green façades with white columns and "
        "gilded spires anchor Palace Square. Since 1917 it has "
        "housed a world-class museum.",
        "Вершина елизаветинского барокко и символ имперской "
        "столицы на Неве.",
        "The summit of Elizabethan Baroque and an emblem of "
        "the imperial capital on the Neva.",
    ),
    "elizabethan_baroque_smolny_cathedral": (
        "Смольный собор — кафедральный храм Смольного "
        "воспитательного дома, шедевр Растрелли.",
        "Smolny Cathedral is the centrepiece of the Smolny "
        "Institute ensemble and a masterpiece by Rastrelli.",
        "Строительство велось в 1748–1764 годах; голубые "
        "фасады с белым декором и колокольня высотой около "
        "93 метров образуют один из узнаваемых силуэтов "
        "Петербурга. Собор завершён только в XIX веке.",
        "Built between 1748 and 1764; blue façades with white "
        "ornament and a bell tower about 93 metres high form "
        "one of Petersburg's best-known silhouettes. The cathedral "
        "was completed only in the nineteenth century.",
        "Образец пышного елизаветинского барокко на берегу "
        "Невы.",
        "A landmark of lavish Elizabethan Baroque on the Neva.",
    ),
    "elizabethan_baroque_stroganov_palace_2": (
        "Дворец Строгановых на Невском проспекте — "
        "городской особняк знатного рода.",
        "The Stroganov Palace on Nevsky Prospect is the "
        "urban mansion of a noble family.",
        "Перестроен в 1752–1754 годах Бартоломео Растрелли "
        "для графа Сергея Строганова; парадная лестница, "
        "Минералогический кабинет и парадные залы сохранили "
        "роскошь XVIII века. Сегодня — филиал Русского музея.",
        "Rebuilt in 1752–1754 by Bartolomeo Rastrelli for "
        "Count Sergei Stroganov; the grand staircase, mineral "
        "cabinet and state rooms preserve eighteenth-century "
        "splendour. Today it is a branch of the Russian Museum.",
        "Редкий образец дворцовой архитектуры середины XVIII "
        "века в центре Петербурга.",
        "A rare mid-eighteenth-century palace in central "
        "St Petersburg.",
    ),
    "petrine_baroque_summer_palace": (
        "Летний дворец Петра I — скромная царская резиденция "
        "на набережной Фонтанки.",
        "Peter the Great's Summer Palace is a modest royal "
        "residence on the Fontanka embankment.",
        "Возведён в 1710–1714 годах по проекту Доменико "
        "Трезини для первого петербургского периода жизни "
        "императора. Двухэтажный каменный дом с мезонином "
        "сохранил интерьеры и мебель эпохи Петра.",
        "Built in 1710–1714 to Domenico Trezzini's design for "
        "Peter's early years in the new capital. The two-storey "
        "stone house with mezzanine still holds period interiors "
        "and furnishings.",
        "Один из старейших сохранившихся дворцов Петербурга "
        "и памятник петровского барокко.",
        "One of Petersburg's oldest surviving palaces and a "
        "monument of Petrine Baroque.",
    ),
    "petrine_baroque_twelve_collegia": (
        "Здание Двенадцати коллегий — административный "
        "центр реформ Петра I на Стрелке Васильевского "
        "острова.",
        "The Twelve Collegia building was the administrative "
        "hub of Peter the Great's reforms on Vasilyevsky Island.",
        "Строилось в 1722–1742 годах по проекту Доменико "
        "Трезини; фасад длиной около 400 метров объединял "
        "министерства империи. Сегодня здесь главное здание "
        "Санкт-Петербургского государственного университета.",
        "Built in 1722–1742 to Domenico Trezzini's design; "
        "a façade about 400 metres long housed the imperial "
        "colleges. It now serves as the main building of St "
        "Petersburg State University.",
        "Ключевой памятник петровского барокко и символ "
        "российской государственности.",
        "A key Petrine Baroque monument and a symbol of "
        "Russian state administration.",
    ),
    "petrine_baroque_menshikov_palace_2": (
        "Дворец Меншикова — первый каменный дворец "
        "Санкт-Петербурга на Университетской набережной.",
        "The Menshikov Palace is the first stone palace in "
        "St Petersburg on the University Embankment.",
        "Возведён в 1710–1714 годах для первого губернатора "
        "города Александра Меншикова; над проектом работали "
        "Джованни Мария Фонтана, Иоганн Георг Шедель и другие "
        "мастера. Парадные залы и голландская печь отражают "
        "ранний петровский вкус.",
        "Built in 1710–1714 for the city's first governor, "
        "Alexander Menshikov; Giovanni Maria Fontana, Johann "
        "Georg Schädel and other masters worked on the design. "
        "State rooms and Dutch tile stoves reflect early "
        "Petrine taste.",
        "Начало каменного Петербурга и музей раннего "
        "XVIII века.",
        "The birth of stone Petersburg and a museum of the "
        "early eighteenth century.",
    ),
    "naryshkin_baroque_intercession_fili": (
        "Церковь Покрова в Филях — шедевр нарышкинского "
        "барокко на бывшей усадьбе Нарышкиных.",
        "The Church of the Intercession in Fili is a "
        "masterpiece of Naryshkin Baroque on the former "
        "Naryshkin estate.",
        "Построена в 1690–1693 годах; белокаменный храм "
        "с пятиглавием, восьмериками и богатым наличным "
        "декором стал образцом «московского барокко». "
        "Интерьер сохраняет резной иконостас и росписи.",
        "Built in 1690–1693; the white-stone five-domed church "
        "with octagonal tiers and rich window surrounds became "
        "a model of Moscow Baroque. The interior keeps a carved "
        "iconostasis and murals.",
        "Один из высших памятников московского зодчества "
        "конца XVII века.",
        "One of the finest monuments of late seventeenth-century "
        "Moscow architecture.",
    ),
    "contemporary_lakhta_center": (
        "Лахта-центр — небоскрёб и штаб-квартира «Газпрома» "
        "на берегу Финского залива.",
        "Lakhta Center is a supertall tower and Gazprom "
        "headquarters on the Gulf of Finland shore.",
        "Высота 462 метра; строительство завершено в 2018 "
        "году по проекту бюро RMJM (Тони Кеттл). Вертикальный "
        "силуэт с витым фасадом и общественные пространства "
        "у подножия задали новый акцент панораме Петербурга.",
        "At 462 metres, it was completed in 2018 to a design "
        "by RMJM (Tony Kettle). A twisting façade and public "
        "spaces at the base add a new focal point to the "
        "city skyline.",
        "Самое высокое здание Европы и символ современного "
        "Петербурга.",
        "Europe's tallest building and a symbol of contemporary "
        "St Petersburg.",
    ),
    "avant_garde_moscow_libraries_0_2": (
        "Российская государственная библиотека — крупнейшее "
        "книгохранилище страны на Воздвиженке.",
        "The Russian State Library is the country's largest "
        "book repository on Vozdvizhenka Street.",
        "Основана в 1862 году как Румянцевский музей; "
        "главное здание на Воздвиженке возводилось в "
        "1928–1958 годах. Фонды насчитывают более 47 млн "
        "единиц хранения.",
        "Founded in 1862 as the Rumyantsev Museum; the main "
        "building on Vozdvizhenka was built between 1928 and "
        "1958. Its collections hold more than 47 million items.",
        "Национальное книгохранилище и памятник монументальной "
        "архитектуры сталинского периода.",
        "The national library and a monument of Stalin-era "
        "monumental architecture.",
    ),
}

_NAME_OVERRIDES: dict[str, tuple[str, str]] = dict(TOC_NAME_OVERRIDES)

_ADDRESS_OVERRIDES: dict[str, tuple[str, str]] = {
    "avant_garde_melnikov_house": (
        "ул. Кривоарбатский переулок, 10",
        "10 Krivoarbatsky Lane",
    ),
    "avant_garde_moscow_libraries_0_2": (
        "ул. Воздвиженка, 3/5",
        "3/5 Vozdvizhenka Street",
    ),
    "petrine_baroque_menshikov_palace_2": (
        "Университетская набережная, 15",
        "15 University Embankment",
    ),
    "elizabethan_baroque_stroganov_palace_2": (
        "Невский проспект, 17",
        "17 Nevsky Prospect",
    ),
    "elizabethan_baroque_winter_palace": (
        "Дворцовая набережная, 38",
        "38 Palace Embankment",
    ),
}

_MAX_SENTENCES: dict[str, int] = {
    "petrine_baroque_summer_garden_2": 15,
    "elizabethan_baroque_pavlovsk_palace_2": 15,
    "early_classicism_mikhailovsky_castle_2": 15,
    "empire_mikhailovsky_castle_2": 15,
    "mature_classicism_pushkin_house_2": 8,
    "early_classicism_tauride_palace_2": 8,
    "mature_classicism_tauride_palace": 8,
    "empire_tauride_palace_2": 8,
}


def narrative_override_for_slug(slug: str) -> dict[str, str] | None:
    block = _OVERRIDES.get(slug)
    if not block:
        return None
    return {
        "description_ru": block[0],
        "description_en": block[1],
        "history_ru": block[2],
        "history_en": block[3],
        "significance_ru": block[4],
        "significance_en": block[5],
    }


def apply_narrative_overrides(place: dict[str, Any]) -> dict[str, Any]:
    """Return a shallow copy with curated text fields when defined."""
    slug = str(place.get("slug") or "")
    override = narrative_override_for_slug(slug)
    name_pair = _NAME_OVERRIDES.get(slug)
    address_pair = _ADDRESS_OVERRIDES.get(slug)
    if not override and not name_pair and not address_pair:
        return place
    merged = dict(place)
    if name_pair:
        merged["name_ru"] = name_pair[0]
        merged["name_en"] = name_pair[1]
        merged["subtitle_en"] = name_pair[1]
    if address_pair:
        merged["address"] = address_pair[0]
        merged["address_en"] = address_pair[1]
    if not override:
        return merged
    for key, value in override.items():
        if value:
            merged[key] = value
            if key.startswith("description_"):
                edition = key.rsplit("_", 1)[-1]
                if edition in ("ru", "en"):
                    merged["description"] = (
                        value if edition == "ru" else merged.get("description")
                    )
    if override.get("description_ru"):
        merged["description"] = override["description_ru"]
    if override.get("history_ru"):
        merged["history"] = override["history_ru"]
    if override.get("significance_ru"):
        merged["significance"] = override["significance_ru"]
    return merged


def max_sentences_for_slug(slug: str) -> int | None:
    return _MAX_SENTENCES.get(slug)
