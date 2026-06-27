# -*- coding: utf-8 -*-
"""Leading architects per Russian Architecture style chapter."""

from __future__ import annotations

# style_key -> (name_ru, name_en, note_ru, note_en)
_Arch = tuple[str, str, str, str]

STYLE_ARCHITECTS: dict[str, list[_Arch]] = {
    "ancient_rus": [
        (
            "Византийские мастера",
            "Byzantine masters",
            "Привезли в Киев и Новгород крестово-купольный тип "
            "и приёмы мозаичной росписи.",
            "Brought the cross-in-square type and mosaic techniques "
            "to Kyiv and Novgorod.",
        ),
    ],
    "novgorod_school": [
        (
            "Пётр Китира",
            "Peter Kitiros",
            "Строитель церкви Спаса на Ильине — образец "
            "новгородской пластики и фресок Феофана Грека.",
            "Builder of the Church of the Transfiguration on Ilyina "
            "Street, famed for its frescoes by Theophanes the Greek.",
        ),
        (
            "Новгородские артели",
            "Novgorod workshops",
            "Передавали приёмы кирпичной кладки и низких "
            "барабанов из поколения в поколение.",
            "Passed down brickwork and low-drum dome techniques "
            "from generation to generation.",
        ),
    ],
    "pskov_school": [
        (
            "Созон Хромой",
            "Sosson the Lame",
            "Легендарный псковский зодчий; его имя связано "
            "с традицией звонниц и компактных храмов.",
            "Legendary Pskov builder linked to the tradition "
            "of bell towers and compact churches.",
        ),
        (
            "Псковские мастерские",
            "Pskov workshops",
            "Славились лаконичными объёмами, «восьмёрками» "
            "колоколен и пристройками к стенам.",
            "Known for concise volumes, octagonal belfries "
            "and structures attached to fortress walls.",
        ),
    ],
    "moscow_fifteenth_sixteenth": [
        (
            "Аристотель Фиораванти",
            "Aristotele Fioravanti",
            "Итальянец при дворе Ивана III; перестроил "
            "Успенский собор Московского кремля.",
            "Italian architect at Ivan III's court; rebuilt "
            "the Kremlin Dormition Cathedral.",
        ),
        (
            "Алевиз Фрязин Новый",
            "Aloisio the New",
            "Спроектировал Архангельский собор и ввёл "
            "итальянские мотивы в московский Кремль.",
            "Designed the Archangel Cathedral and introduced "
            "Italian motifs into the Moscow Kremlin.",
        ),
        (
            "Постник Яковлев",
            "Postnik Yakovlev",
            "Приписывают участие в соборах Кремля и "
            "храмовых комплексах XVI века.",
            "Traditionally credited with Kremlin cathedrals "
            "and major sixteenth-century church ensembles.",
        ),
    ],
    "tent_roof": [
        (
            "Барма и Постник",
            "Barma and Postnik",
            "Народная традиция связывает их с собором "
            "Василия Блаженного на Красной площади.",
            "Folk tradition links them to Saint Basil's "
            "Cathedral on Red Square.",
        ),
        (
            "Московские мастера шатров",
            "Moscow tent-roof masters",
            "Экспериментировали с восьмёрками и шатрами "
            "без внутренних опор — уникально для Руси.",
            "Experimented with octagons and tent roofs "
            "without internal pillars — rare in Rus.",
        ),
    ],
    "uzorochye": [
        (
            "Бажен Огурцов",
            "Bazhen Ogurtsov",
            "Один из ведущих мастеров узорочья; работал "
            "над теремами и церковными декорами.",
            "A leading ornamental-style master; worked on "
            "terem chambers and church ornament.",
        ),
        (
            "Осип Старцев",
            "Osip Startsev",
            "Строил храмы с насыщенным декором кокошников "
            "в Москве и Подмосковье.",
            "Built churches rich in kokoshnik ornament "
            "in Moscow and its region.",
        ),
    ],
    "naryshkin_baroque": [
        (
            "Яков Бухвостов",
            "Yakov Bukhvostov",
            "Главный мастер «барокко под куполом»: вертикаль "
            "кокошников и белокаменная резьба.",
            "Leading master of 'baroque under the dome': "
            "vertical kokoshnik tiers and white-stone carving.",
        ),
        (
            "Пётр Потапов",
            "Peter Potapov",
            "Спроектировал церковь Покрова в Филях — "
            "образец нарышкинского стиля.",
            "Designed the Intercession Church at Fili — "
            "a hallmark of Naryshkin Baroque.",
        ),
        (
            "Осип Старцев",
            "Osip Startsev",
            "Соединял изящные фасады с традиционной "
            "русской планировкой храма.",
            "Combined refined façades with traditional "
            "Russian church planning.",
        ),
    ],
    "petrine_baroque": [
        (
            "Доменико Трезини",
            "Domenico Trezzini",
            "Заложил сетку Петербурга; Петропавловский собор "
            "и первые каменные ансамбли столицы.",
            "Laid out Petersburg's grid; designed Peter and "
            "Paul Cathedral and early stone ensembles.",
        ),
        (
            "Жан-Батист Леблон",
            "Jean-Baptiste Le Blond",
            "Планировал парадные перспективы и дворцовые "
            "ансамбли на Неве.",
            "Planned ceremonial vistas and palace ensembles "
            "along the Neva.",
        ),
        (
            "Джакомо Кваренги",
            "Giacomo Quarenghi",
            "Ввёл строгий классицизм в Смольный институт "
            "и дворцовые постройки.",
            "Introduced strict Neoclassicism in the Smolny "
            "Institute and palace buildings.",
        ),
    ],
    "elizabethan_baroque": [
        (
            "Бартоломео Растрелли",
            "Bartolomeo Rastrelli",
            "Автор Зимнего дворца и Екатерининского — "
            "праздничная роскошь елизаветинской эпохи.",
            "Architect of the Winter and Catherine Palaces — "
            "the festive luxury of Elizabeth's reign.",
        ),
        (
            "Савва Чевакинский",
            "Savva Chevakinsky",
            "Строил Смольный собор — один из крупнейших "
            "барочных храмов России.",
            "Built Smolny Cathedral — among Russia's "
            "largest Baroque churches.",
        ),
        (
            "Андрей Квасов",
            "Andrei Kvasov",
            "Работал над дворцовыми резиденциями "
            "и парадными интерьерами столицы.",
            "Worked on palace residences and ceremonial "
            "interiors of the capital.",
        ),
    ],
    "early_classicism": [
        (
            "Антонио Ринальди",
            "Antonio Rinaldi",
            "Мраморный дворец и оранжереи — изысканный "
            "ранний классицизм Екатерины II.",
            "Marble Palace and orangeries — refined early "
            "Neoclassicism of Catherine II.",
        ),
        (
            "Юрий Фельтен",
            "Yury Felten",
            "Придворный архитектор; сочетал античные формы "
            "с инженерными задачами.",
            "Court architect; combined antique forms "
            "with engineering challenges.",
        ),
        (
            "Иван Старов",
            "Ivan Starov",
            "Таврический дворец и храмы с ротондами — "
            "строгая симметрия академизма.",
            "Tauride Palace and rotunda churches — "
            "strict symmetry of academic classicism.",
        ),
    ],
    "mature_classicism": [
        (
            "Джакомо Кваренги",
            "Giacomo Quarenghi",
            "Смольный и Александринский театр — эталон "
            "зрелого петербургского классицизма.",
            "Smolny and the Alexandrinsky Theatre — models "
            "of mature Petersburg Neoclassicism.",
        ),
        (
            "Жан-Тома де Томон",
            "Jean-Thomas de Thomon",
            "Автор стрелки Васильевского острова "
            "и ансамбля Биржи.",
            "Designer of the Spit of Vasilyevsky Island "
            "and the Exchange ensemble.",
        ),
        (
            "Андрейан Захаров",
            "Andreyan Zakharov",
            "Здание Адмиралтейства — символ зрелого "
            "русского классицизма.",
            "The Admiralty building — an emblem of mature "
            "Russian Neoclassicism.",
        ),
        (
            "Карл Росси",
            "Carlo Rossi",
            "Дворцовая площадь и улицы-каноны — "
            "градостроительная классика ампира.",
            "Palace Square and enfilade streets — urban "
            "classicism on the eve of Empire.",
        ),
    ],
    "empire": [
        (
            "Карл Росси",
            "Carlo Rossi",
            "Общественные здания и ансамбли Санкт-Петербурга "
            "в духе имперской парадности.",
            "Public buildings and ensembles in Saint Petersburg "
            "in the spirit of imperial ceremony.",
        ),
        (
            "Андрейан Захаров",
            "Andreyan Zakharov",
            "Продолжил классическую линию в монументальных "
            "гражданских сооружениях.",
            "Continued the classical line in monumental "
            "civic structures.",
        ),
        (
            "Василий Стасов",
            "Vasily Stasov",
            "Триумфальные ворота и Казанский собор — "
            "торжественный ампир Александра I.",
            "Triumphal Gate and Kazan Cathedral — "
            "the ceremonial Empire of Alexander I.",
        ),
        (
            "Огюст Монферран",
            "Auguste de Montferrand",
            "Исаакиевский собор — вершина русского ампира "
            "и инженерного мастерства.",
            "Saint Isaac's Cathedral — the summit of Russian "
            "Empire style and engineering skill.",
        ),
    ],
    "russo_byzantine": [
        (
            "Константин Тон",
            "Konstantin Thon",
            "Автор «Образцовых проектов» и Храма Христа Спасителя; "
            "создал государственный византийско-русский стиль.",
            "Author of 'Model Designs' and Christ the Savior "
            "Cathedral; shaped the state Russo-Byzantine style.",
        ),
        (
            "Виктор Гартман",
            "Viktor Hartmann",
            "Сотрудничал с Тоном; проектировал храмы "
            "и общественные здания в византийском духе.",
            "Collaborated with Thon; designed churches "
            "and public buildings in a Byzantine spirit.",
        ),
    ],
    "eclecticism": [
        (
            "Владимир Шервуд",
            "Vladimir Sherwood",
            "Исторический музей на Красной площади — "
            "образец русско-византийской эклектики.",
            "State Historical Museum on Red Square — "
            "a model of Russo-Byzantine eclecticism.",
        ),
        (
            "Константин Быковский",
            "Konstantin Bykovsky",
            "Вокзалы и общественные здания со смешением "
            "неоренессанса и русских мотивов.",
            "Railway stations and public buildings mixing "
            "Neo-Renaissance and Russian motifs.",
        ),
        (
            "Альфред Парланд",
            "Alfred Parland",
            "Спас на Крови — романтическая эклектика "
            "поздней империи.",
            "Church of the Savior on Blood — romantic "
            "eclecticism of the late empire.",
        ),
    ],
    "pseudo_russian": [
        (
            "Владимир Шервуд",
            "Vladimir Sherwood",
            "Развивал псевдорусский стиль в торговых "
            "и музейных зданиях Москвы.",
            "Developed the pseudo-Russian style in Moscow's "
            "commercial and museum buildings.",
        ),
        (
            "Роберт-Фридрих Мельцер",
            "Robert-Friedrich Meltzer",
            "Оформлял фасады с килевидными крышами "
            "и теремными мотивами.",
            "Designed façades with gabled roofs "
            "and terem-like motifs.",
        ),
    ],
    "neo_russian": [
        (
            "Сергей Малютин",
            "Sergei Malyutin",
            "Участвовал в проектах неорусского модерна, "
            "включая мотивы народного зодчества.",
            "Contributed to Neo-Russian Art Nouveau projects "
            "drawing on folk architecture.",
        ),
        (
            "Иван Фомин",
            "Ivan Fomin",
            "Сочетал неорусские формы с классической "
            "школой и монументальностью.",
            "Combined Neo-Russian forms with classical "
            "training and monumentality.",
        ),
        (
            "Фёдор Шехтель",
            "Fyodor Schechtel",
            "Ярославский вокзал — сказочный силуэт "
            "и майолика национального модерна.",
            "Yaroslavsky Station — a fairy-tale silhouette "
            "and majolica of national Art Nouveau.",
        ),
    ],
    "art_nouveau": [
        (
            "Фёдор Шехтель",
            "Fyodor Schechtel",
            "Главный мастер русского модерна: особняки "
            "Рябушинского, Саввы Морозова, театры.",
            "Leading master of Russian Art Nouveau: Ryabushinsky "
            "and Morozov mansions, theatres.",
        ),
        (
            "Лев Кекушев",
            "Lev Kekushev",
            "Московские доходные дома с плавными линиями "
            "и скульптурным декором.",
            "Moscow apartment buildings with flowing lines "
            "and sculptural ornament.",
        ),
        (
            "Уильям Волкот",
            "William Walcot",
            "Петербургский модерн: вокзалы и общественные "
            "здания в плавных формах.",
            "Petersburg Art Nouveau: stations and public "
            "buildings in flowing forms.",
        ),
    ],
    "neoclassicism_early20": [
        (
            "Иван Фомин",
            "Ivan Fomin",
            "Неоклассические банки и клубы Серебряного века "
            "с лаконичными портиками.",
            "Neoclassical banks and Silver Age clubs "
            "with concise porticos.",
        ),
        (
            "Владимир Щуко",
            "Vladimir Shchuko",
            "Киевский вокзал и общественные здания — "
            "монументальный неоклассицизм.",
            "Kyiv Station and public buildings — "
            "monumental Neoclassicism.",
        ),
        (
            "Иван Жолтовский",
            "Ivan Zholtovsky",
            "Доходные дома и особняки с античными "
            "мотивами начала XX века.",
            "Apartment houses and mansions with antique "
            "motifs of the early twentieth century.",
        ),
    ],
    "avant_garde": [
        (
            "Владимир Шухов",
            "Vladimir Shukhov",
            "Инженер-новатор: гиперболоидные башни, "
            "перекрытия и выставочные павильоны.",
            "Engineering innovator: hyperboloid towers, "
            "roof structures and exhibition pavilions.",
        ),
        (
            "Моисей Гинзбург",
            "Moisei Ginzburg",
            "Теоретик и автор Наркомфина — жильё "
            "и общественные здания авангарда.",
            "Theorist and author of Narkomfin — avant-garde "
            "housing and public buildings.",
        ),
        (
            "Константин Мельников",
            "Konstantin Melnikov",
            "Экспериментальные формы: павильоны, гаражи "
            "и знаменитый собственный дом.",
            "Experimental forms: pavilions, garages "
            "and his famous own house.",
        ),
    ],
    "constructivism": [
        (
            "Братья Веснины",
            "The Vesnin brothers",
            "Александр, Леонид и Виктор — Дом правительства "
            "и проекты рабочих клубов.",
            "Alexander, Leonid and Viktor — the House of "
            "Government and workers' club projects.",
        ),
        (
            "Моисей Гинзбург",
            "Moisei Ginzburg",
            "Разработал типологию социалистического жилья "
            "и принципы функционализма.",
            "Developed typologies of socialist housing "
            "and functionalist principles.",
        ),
    ],
    "stalinist": [
        (
            "Лев Руднев",
            "Lev Rudnev",
            "Главное здание МГУ — символ сталинского "
            "ампира и послевоенной монументальности.",
            "MSU main building — a symbol of Stalinist "
            "Empire and post-war monumentality.",
        ),
        (
            "Владимир Гельфрейх",
            "Vladimir Gelfreikh",
            "Высотки на Котельнической и Кудринской — "
            "парадная вертикаль Москвы.",
            "Skyscrapers on Kotelnicheskaya and Kudrinskaya "
            "— Moscow's ceremonial skyline.",
        ),
        (
            "Алексей Душкин",
            "Alexey Dushkin",
            "Станции метро «Маяковская» и «Кропоткинская» — "
            "дворцы под землёй.",
            "Mayakovskaya and Kropotkinskaya metro stations "
            "— palaces underground.",
        ),
    ],
    "panel_housing": [
        (
            "Виталий Лагутенко",
            "Vitaly Lagutenko",
            "Пионер серийного домостроения; разработал "
            "ранние панельные серии массового жилья.",
            "Pioneer of industrial housing; developed early "
            "panel series for mass construction.",
        ),
        (
            "Гипронисельстрой и Гражданпроект",
            "Giproniselstroy and Grazhdanproekt",
            "Типовые проекты хрущёвок и брежневок "
            "для всего СССР.",
            "Standard designs of Khrushchevka and "
            "Brezhnev-era blocks across the USSR.",
        ),
    ],
    "soviet_modernism": [
        (
            "Яков Белопольский",
            "Yakov Belopolsky",
            "Дворец спорта в Лужниках — крупные "
            "конструктивные пролёты модернизма.",
            "Luzhniki Sports Palace — large structural "
            "spans of Soviet modernism.",
        ),
        (
            "Юрий Плохов",
            "Yuri Plokhov",
            "Общественные здания с лаконичными объёмами "
            "и выразительными каркасами.",
            "Public buildings with concise volumes "
            "and expressive frames.",
        ),
        (
            "Николай Суетин",
            "Nikolai Suetin",
            "Ученик Малевича; архитектура и дизайн "
            "на стыке авангарда и модернизма.",
            "Malevich's pupil; architecture and design "
            "between avant-garde and modernism.",
        ),
    ],
    "stalinist_neoclassicism": [
        (
            "Иван Жолтовский",
            "Ivan Zholtovsky",
            "Перешёл к монументальному неоклассицизму "
            "в советских гражданских зданиях.",
            "Turned to monumental Neoclassicism "
            "in Soviet civic buildings.",
        ),
        (
            "Алексей Душкин",
            "Alexey Dushkin",
            "Ведомственные здания и станции метро "
            "с классическими ордерами.",
            "Ministry buildings and metro stations "
            "with classical orders.",
        ),
        (
            "Владимир Щуко",
            "Vladimir Shchuko",
            "Библиотека имени Ленина — строгий "
            "неоклассический ансамбль.",
            "Lenin Library — a strict Neoclassical ensemble.",
        ),
    ],
    "art_deco": [
        (
            "Иван Фомин",
            "Ivan Fomin",
            "Театры и клубы с геометрическим декором "
            "и парадными интерьерами.",
            "Theatres and clubs with geometric décor "
            "and ceremonial interiors.",
        ),
        (
            "Алексей Щусев",
            "Alexey Shchusev",
            "Мавзолей Ленина и вокзалы — монументальность "
            "и стилизованный декор.",
            "Lenin's Mausoleum and stations — monumentality "
            "and stylized ornament.",
        ),
    ],
    "post_constructivism": [
        (
            "Аркадий Лангман",
            "Arkady Langman",
            "Здание Совета труда и обороны (Госдума) — "
            "строгий фасад на рубеже стилей.",
            "Council of Labor and Defense building (State Duma) "
            "— an austere façade between styles.",
        ),
        (
            "Илья Голосов",
            "Ilya Golosov",
            "Поздние работы сочетают конструктивизм "
            "с неоклассическими элементами.",
            "Late works combine Constructivism "
            "with Neoclassical elements.",
        ),
    ],
    "regional_soviet": [
        (
            "Евгений Васильев",
            "Yevgeny Vasiliev",
            "Новосибирский театр оперы и балета — "
            "крупный региональный ансамбль.",
            "Novosibirsk Opera and Ballet Theatre — "
            "a major regional ensemble.",
        ),
        (
            "Региональные Гипрогражданы",
            "Regional Giprogor design institutes",
            "Проектировали Дворцы спорта и культуры "
            "в столицах союзных республик.",
            "Designed sports and culture palaces "
            "in union-republic capitals.",
        ),
    ],
    "brutalism": [
        (
            "Евгений Стамо",
            "Yevgeny Stamo",
            "Автор типовых проектов и экспериментальных "
            "бетонных общественных зданий.",
            "Author of standard designs and experimental "
            "concrete public buildings.",
        ),
        (
            "Яков Белопольский",
            "Yakov Belopolsky",
            "Крупные спортивные комплексы с открытыми "
            "конструкциями и бетоном.",
            "Large sports complexes with exposed "
            "structures and concrete.",
        ),
    ],
    "soviet_neoclassicism_revival": [
        (
            "Алексей Щусев",
            "Alexey Shchusev",
            "Послевоенная реконструкция центра Москвы "
            "и парадные магистрали.",
            "Post-war reconstruction of central Moscow "
            "and ceremonial avenues.",
        ),
        (
            "Иван Жолтовский",
            "Ivan Zholtovsky",
            "Восстановление исторических ансамблей "
            "в классических формах.",
            "Restoration of historic ensembles "
            "in classical forms.",
        ),
    ],
    "postmodernism": [
        (
            "Юрий Плохов",
            "Yuri Plokhov",
            "Поздние работы с цитатами исторических "
            "стилей в общественных зданиях.",
            "Late works quoting historical styles "
            "in public buildings.",
        ),
        (
            "Михаил Посохин",
            "Mikhail Posokhin",
            "Кремлёвский Дворец съездов — монумент "
            "с модернистской и цитатной логикой.",
            "Kremlin Palace of Congresses — a monument "
            "with modernist and quotation logic.",
        ),
    ],
    "neo_eclectic": [
        (
            "Александр Боков",
            "Alexander Bokov",
            "Постсоветские жилые и офисные комплексы "
            "со смешением стилей.",
            "Post-Soviet residential and office complexes "
            "mixing historical styles.",
        ),
        (
            "Московские мастерские 1990–2010‑х",
            "Moscow studios of the 1990s–2010s",
            "Цитировали классику, модерн и ар-деко "
            "в новой застройке.",
            "Quoted classicism, Art Nouveau and Art Deco "
            "in new construction.",
        ),
    ],
    "contemporary": [
        (
            "Сергей Скуратов",
            "Sergey Skuratov",
            "Жилые и общественные проекты с выразительной "
            "пластикой и фактурой материалов.",
            "Residential and public projects with expressive "
            "form and material texture.",
        ),
        (
            "Рем Кулхаас",
            "Rem Koolhaas",
            "Гараж-музей в парке Горького — международный "
            "контемпорари в исторической среде.",
            "Garage Museum in Gorky Park — international "
            "contemporary architecture in a historic setting.",
        ),
        (
            "Meganom (Илья Уткин, Артур Лисовский)",
            "Meganom (Ilya Utkin, Artur Lisovsky)",
            "Небоскрёбы Москва-Сити и набережные — "
            "современный деловой силуэт.",
            "Moscow City towers and embankments — "
            "a contemporary business skyline.",
        ),
    ],
}
