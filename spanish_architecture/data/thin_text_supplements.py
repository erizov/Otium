# -*- coding: utf-8 -*-
"""Supplemental prose for places under the minimum word count."""

from __future__ import annotations

import re
from typing import Any

MIN_NARRATIVE_WORDS = 20

# slug -> (extra_history_ru, extra_history_en, extra_significance_ru,
#           extra_significance_en)
_SUPPLEMENTS: dict[str, tuple[str, str, str, str]] = {
    "catalan_gothic_barcelona_cathedral": (
        "Готический неф и клуатр с тринадцатью белыми гусями; "
        "западный фасад завершён в XIX веке.",
        "Gothic nave and cloister with thirteen geese; façade "
        "completed in the nineteenth century.",
        "Возведён на месте римского храма; сердце исторического "
        "квартала Барри-Готик.",
        "Cathedral on a Roman temple site; heart of the Barri "
        "Gòtic.",
    ),
    "catalan_gothic_generalitat": (
        "Готический фасад 1596–1619 годов; двор Pati dels "
        "Tarongers с апельсиновыми деревьями.",
        "Gothic façade 1596–1619; Pati dels Tarongers "
        "orange-tree courtyard.",
        "Резиденция правительства Каталонии со времён "
        "средневековья.",
        "Seat of the Catalan government since the medieval era.",
    ),
    "catalan_gothic_girona_cathedral": (
        "Готический свод пролётом 23 метра и монументальная "
        "барочная лестница у фасада.",
        "Wide Gothic vault span of 23 m; monumental baroque "
        "staircase façade.",
        "Доминирует над силуэтом старого города Жироны на холме.",
        "Dominates the skyline of Girona old town.",
    ),
    "catalan_gothic_llotja_mar": (
        "Торговый зал со спиральными колоннами без капителей; "
        "архитектор Guillem Sagrera.",
        "Trading hall with spiral columns without capitals; "
        "architect Guillem Sagrera.",
        "1380–1392 годы; символ морской торговли и богатства "
        "Барселоны.",
        "1380–1392; symbol of Barcelona maritime commerce.",
    ),
    "catalan_gothic_manresa": (
        "Готическая церковь связана с духовным путём Ignacio de "
        "Loyola через Манресу.",
        "Gothic church linked to the spiritual journey of "
        "Ignatius of Loyola.",
        "Образец провинциальной каталонской готики в "
        "индустриальном городе.",
        "Provincial Catalan Gothic in industrial Manresa.",
    ),
    "catalan_gothic_santa_maria_mar": (
        "Зальная церковь на стройных колоннах; её строили "
        "морские купцы и цеховые братства.",
        "Hall church with slender columns; built by shipowners "
        "and guilds.",
        "1329–1383 годы; шедевр средиземноморской каталонской "
        "готики.",
        "1329–1383; masterpiece of Catalan Mediterranean Gothic.",
    ),
    "catalan_gothic_santa_maria_pi": (
        "Массивная розетка и восьмигранная колокольня на площади "
        "Plaça del Pi.",
        "Massive rose window and octagonal bell tower on the "
        "Plaça del Pi.",
        "Приходская церковь XIV века — важный памятник готики "
        "Барселоны.",
        "Fourteenth-century parish church of Gothic Barcelona.",
    ),
    "catalan_modernisme_bellesguard": (
        "Башня Gaudí в неоготическом духе на месте "
        "средневекового замка на холме.",
        "Torre Bellesguard; Gaudí neo-Gothic tower on medieval "
        "site.",
        "1900–1909 годы; открывает виды на Барселону и горы "
        "Collserola.",
        "1900–1909; views over Barcelona and Collserola.",
    ),
    "catalan_modernisme_casa_amatller": (
        "Неоготический фасад Josep Puig i Cadafalch для семьи "
        "шоколадных фабрикантов Amatller.",
        "Josep Puig i Cadafalch Neo-Gothic façade; chocolate "
        "heir Amatller.",
        "1898–1900 годы; часть квартала Illa de la Discòrdia.",
        "1898–1900; part of the Illa de la Discòrdia block.",
    ),
    "catalan_modernisme_casa_batllo": (
        "Фасад с балконами «костей и масок» и крышей из мозаики "
        "trencadís.",
        "Casa Batlló façade bone-and-mask balconies; trencadís "
        "mosaic roof.",
        "1904–1906 годы; Gaudí на Passeig de Gràcia; объект "
        "UNESCO.",
        "1904–1906 Gaudí on Passeig de Gràcia; UNESCO.",
    ),
    "catalan_modernisme_casa_mila": (
        "Волнистый каменный фасад La Pedrera и скульптурные "
        "дымоходы на крыше.",
        "La Pedrera undulating stone façade; rooftop warrior "
        "chimneys.",
        "1906–1912 годы; жилой дом Gaudí; наследие UNESCO.",
        "1906–1912 Gaudí apartment block; UNESCO World Heritage.",
    ),
    "catalan_modernisme_casa_punxes": (
        "«Дом шипов» с башнями, напоминающими замок; автор Puig "
        "i Cadafalch.",
        "Casa de les Punxes; medieval castle-inspired Puig i "
        "Cadafalch spires.",
        "1905 год; проспект Diagonal; неороманский модернизм.",
        "1905 on the Diagonal; Neo-Romanesque Modernisme.",
    ),
    "catalan_modernisme_casa_vicens": (
        "Первый дом Gaudí с мудéjarской плиткой и коваными "
        "решётками в Gràcia.",
        "Gaudí's first house; Mudéjar-style tile and iron "
        "grillwork in Gràcia.",
        "1883–1885 годы; ранний манифест каталонского "
        "модернизма, UNESCO.",
        "1883–1885; UNESCO early Modernisme manifesto.",
    ),
    "catalan_modernisme_palau_musica": (
        "Концертный зал Lluís Domènech i Montaner с витражным "
        "стеклянным куполом.",
        "Lluís Domènech i Montaner concert hall; stained-glass "
        "skylight.",
        "1905–1908 годы; UNESCO — музыкальная архитектура "
        "модернизма.",
        "1905–1908; UNESCO Modernisme and music architecture.",
    ),
    "catalan_modernisme_park_guell": (
        "Парк Gaudí с мозаичной скамьёй-змеёй и залом с "
        "дорическими колоннами.",
        "Gaudí park with trencadís serpent bench and hypostyle "
        "hall.",
        "1900–1914 годы; из жилого проекта вырос общественный "
        "парк UNESCO.",
        "1900–1914; failed housing estate turned public park, "
        "UNESCO.",
    ),
    "catalan_modernisme_sagrada_familia": (
        "Gaudí использовал гиперболические параболоиды; "
        "возведено восемь башен, другие планируются.",
        "Antoni Gaudí hyperbolic paraboloids; eight completed "
        "towers, more planned.",
        "Строится с 1882 года; часть творений Gaudí в Барселоне "
        "под охраной UNESCO.",
        "1882–ongoing; UNESCO part of Gaudí works in Barcelona.",
    ),
    "catalan_modernisme_sant_pau": (
        "Больница с павильонами и подземными коридорами; автор "
        "Domènech i Montaner.",
        "Hospital de la Santa Creu i Sant Pau; pavilions and "
        "underground tunnels.",
        "1902–1930 годы; UNESCO — «лечебный город» модернизма.",
        "1902–1930 Domènech i Montaner; UNESCO healing city.",
    ),
    "churrigueresque_cartuja_sacristy": (
        "Сакристия картузианского монастыря Гранады; мраморная "
        "облицовка Francisco Hurtado Izquierdo.",
        "Cartuja Granada sacristy; Francisco Hurtado Izquierdo "
        "marble revetment.",
        "1727–1764 годы; «сikstinskaya кapella» испанского "
        "барокко.",
        "1727–1764; 'Sistine Chapel' of Spanish baroque.",
    ),
    "churrigueresque_hospital_cruz": (
        "Госпиталь de la Santa Cruz; платерескo-портал и "
        "чурригерескo-алтари внутри.",
        "Hospital de la Santa Cruz; Plateresque portal then "
        "Churrigueresque altars.",
        "1504–1514 годы; Enrique Egas; образец ренessanсного "
        "госпиталя Испании.",
        "1504–1514 by Enrique Egas; model Renaissance hospital "
        "of Spain.",
    ),
    "churrigueresque_la_compania": (
        "Иезuитская церковь Саламанки с экстремальной "
        "штукатуркой и фасадом-ретábulo.",
        "Jesuit church in Salamanca; extreme stucco and "
        "integrated altarpiece façade.",
        "1745–1765 годы; эталонный интерьер стиля чурригерескo.",
        "1745–1765; textbook Churrigueresque interior.",
    ),
    "churrigueresque_salamanca_facade": (
        "Новый фасад собора братьев Churriguera; волнообразная "
        "каменная стена.",
        "Churriguera brothers' new cathedral façade; undulating "
        "wall of stone.",
        "1730–1755 годы; вершина испанского "
        "чурригерескo-ornamenta.",
        "1730–1755; peak of Spanish Churrigueresque ornament.",
    ),
    "churrigueresque_transparente": (
        "Transparente Narciso Tomé в Толедo; световой колодец за "
        "главным алтарём.",
        "Narciso Tomé's Transparente in Toledo; light shaft "
        "behind high altar.",
        "1729–1732 годы; синтез скульптуры, живописи и "
        "архитектуры.",
        "1729–1732; baroque fusion of sculpture, painting, "
        "architecture.",
    ),
    "churrigueresque_valladolid_univ": (
        "Фасад университета Вalladolid; чурригереско-каменная "
        "стена 1715 года.",
        "University façade in Valladolid; Churrigueresque stone "
        "curtain of 1715.",
        "1715–1718 годы; проект монаха Fray Pedro de la "
        "Visitación.",
        "1715–1718 design by Fray Pedro de la Visitación.",
    ),
    "churrigueresque_vera_cruz": (
        "Церковь Vera Cruz в Саламанке с поздними "
        "чурригерескo-ретábulo.",
        "Iglesia de la Vera Cruz in Salamanca; late "
        "Churrigueresque retablos.",
        "XVIII век; украшение университетского квартала города.",
        "Eighteenth-century chapel ornament in the university "
        "quarter.",
    ),
    "contemporary_azkuna": (
        "Azkuna Zentroa; интерьеры Philippe Starck в бывшем "
        "винном складе Бильbao.",
        "Azkuna Zentroa Philippe Starck interior; former wine "
        "warehouse Bilbao.",
        "2005–2010 годы; культурная регенерация Alhóndiga "
        "Bilbao.",
        "2005–2010; cultural regeneration of Alhóndiga Bilbao.",
    ),
    "contemporary_caixaforum": (
        "Пристройка Herzog & de Meuron из ржавой стали к бывшей "
        "электростанции Мадрида.",
        "Herzog & de Meuron rusted steel extension; former "
        "Madrid power station.",
        "2001–2008 годы; адаптивное использование и вертикальный "
        "сад.",
        "2001–2008; adaptive reuse and vertical garden wall.",
    ),
    "contemporary_city_arts": (
        "Белые бетонные оболочки Santiago Calatrava в Городе "
        "искусств и наук.",
        "Santiago Calatrava white concrete shells; City of Arts "
        "and Sciences Valencia.",
        "1991–2005 годы; иkona позднего структурного "
        "экспрессионизма.",
        "1991–2005; iconic late-twentieth-century structural "
        "expressionism.",
    ),
    "contemporary_ciudad_cultura": (
        "Гранитные «сколы» Peter Eisenman на холме Gaiás в "
        "Сантьяgo de Compostela.",
        "Peter Eisenman fractured granite shells; City of "
        "Culture Santiago.",
        "1999–2013 годы; декonstruktivistский ландшафт на "
        "окраине Galicia.",
        "1999–2013; Deconstructivist landscape on Gaiás hill.",
    ),
    "contemporary_congress_madrid": (
        "Кongресс-центр Norman Foster из стали и стекла в Campo "
        "de las Naciones.",
        "Norman Foster steel-and-glass congress centre; Campo de "
        "las Naciones.",
        "2003–2007 годы; институциональная современная "
        "архитектура Мадрида.",
        "2003–2007; institutional contemporary architecture in "
        "Madrid.",
    ),
    "contemporary_forum_barcelona": (
        "Здание форума Herbert Bayer; треугольный навес на "
        "набережной 2004 года.",
        "Herbert Bayer forum building; triangular waterfront "
        "canopy 2004.",
        "Архитектура события Всемирного форума культур 2004 "
        "года.",
        "Event architecture of the 2004 Universal Forum of "
        "Cultures.",
    ),
    "contemporary_guggenheim": (
        "Музей Frank Gehry с титановыми волнами на набережной "
        "Бильbao.",
        "Frank Gehry titanium curves; Bilbao riverfront museum "
        "1997.",
        "1991–1997 годы; катализатор городской регенерации "
        "Бильbao.",
        "1991–1997; catalyst of Bilbao urban regeneration cited "
        "worldwide.",
    ),
    "contemporary_maat": (
        "Керамический фасад Amanda Levete у музея MAAT на берегу "
        "Тежu.",
        "Amanda Levete ceramic tile façade; MAAT Lisbon "
        "waterfront museum.",
        "2012–2016 годы; искусство, архитектура и технологии в "
        "Лиссabonе.",
        "2012–2016; art, architecture and technology on the "
        "Tagus.",
    ),
    "contemporary_metropol_parasol": (
        "Деревянный навес Jürgen Mayer; крупнейшая "
        "ламинированная деревянная конструкция.",
        "Jürgen Mayer laminated timber parasol; world's largest "
        "wooden structure.",
        "2004–2011 годы; площадь La Encarnación над раскопками "
        "Севильи.",
        "2004–2011 La Encarnación; Seville archaeological plaza.",
    ),
    "contemporary_w_barcelona": (
        "Отель Ricardo Bofill в форме паруса со стеклянным "
        "фасадом на Barceloneta.",
        "Ricardo Bofill sail-shaped hotel; glass façade on "
        "Barceloneta beach.",
        "2006–2009 годы; символ набережной послеолympiйской "
        "Барселоны.",
        "2006–2009; waterfront landmark of post-Olympic "
        "Barcelona.",
    ),
    "eclectic_historicism_atocha": (
        "Железный вокальный зал Alberto de Palacio; связь с "
        "инженерными традициями Gustave Eiffel.",
        "Atocha station iron train shed; Alberto de Palacio and "
        "Gustave Eiffel link.",
        "1888–1892 годы; в 1992 году превращён в тропический "
        "сад.",
        "1888–1892; transformed with a tropical garden in 1992.",
    ),
    "eclectic_historicism_bolsa_porto": (
        "Биржа с неoklassическим фасадом и внутренним Арабским "
        "залом.",
        "Palácio da Bolsa; neo-classical exterior and Arab Hall "
        "interior.",
        "1842–1910 годы; символ торговой гордости Порту XIX "
        "века.",
        "1842–1910; nineteenth-century commercial pride of "
        "Porto.",
    ),
    "eclectic_historicism_casino_madrid": (
        "Клуб Casino de Madrid с эклектичными интерьерами у Gran "
        "Vía.",
        "Casino de Madrid club; eclectic interiors and Gran Vía "
        "proximity.",
        "1902–1910 годы; светская архитектура belle époque.",
        "1902–1910; secular architecture of Belle Époque elite.",
    ),
    "eclectic_historicism_gran_via": (
        "Ось Gran Vía с небоскрёbами в духе Чикagо и театрами "
        "1910–1929 годов.",
        "Gran Vía axis in Madrid; Chicago-style towers and "
        "theatres 1910–1929.",
        "Символ буржуазной модернизации испанской столицы "
        "раннего XX века.",
        "Symbol of bourgeois urban modernisation, early "
        "twentieth century.",
    ),
    "eclectic_historicism_metropolis": (
        "Edificio Metrópolis на углу Gran Vía; купол и "
        "скульптура в духе Beaux-Arts.",
        "Edificio Metrópolis corner on Gran Vía; Beaux-Arts dome "
        "and sculpture.",
        "1907–1911 годы; Jules и Raymond Février; икona Мадрида.",
        "1907–1911 by Jules and Raymond Février; Madrid icon.",
    ),
    "eclectic_historicism_palacio_comunicaciones": (
        "Камень, чугун и стекло; эклектичная ратуша Palacio de "
        "Cibeles.",
        "Palacio de Cibeles; stone, iron and glass eclectic city "
        "hall.",
        "1904–1917 годы; Antonio Palacios; сегодня мэриия "
        "Мадрида.",
        "1904–1917 by Antonio Palacios; now Madrid City Hall.",
    ),
    "eclectic_historicism_palacio_cristal": (
        "Стеклянный павильон 1887 года из чугуна и изогнутого "
        "стекла в парке Retiro.",
        "Retiro glass pavilion of 1887; cast iron and curved "
        "glass in Retiro Park.",
        "Выставочная архитектура по мотивам лондонского "
        "Хрустального дворца.",
        "Exhibition architecture inspired by the Crystal Palace "
        "model.",
    ),
    "franco_estado_novo_arco_victoria": (
        "Тriумфальная арка Arco de la Victoria в районе Moncloa "
        "в Мадridе.",
        "Arco de la Victoria Madrid; Franco triumphal arch at "
        "Moncloa.",
        "1950–1956 годы; монумент послегражданской политической "
        "архитектуры.",
        "1950–1956; post-Civil War political monumentality.",
    ),
    "franco_estado_novo_ciudad_universitaria": (
        "Университетский город с факультетскими pavilions и "
        "рационалистической планировкой.",
        "Ciudad Universitaria Madrid; faculty pavilions and "
        "rationalist planning.",
        "1927–1980 годы; государственная университетская "
        "архитектура эпохи Franco.",
        "1927–1980; state university architecture under Franco.",
    ),
    "franco_estado_novo_estadio_nacional": (
        "Национальный стadion у Jamor; арена эпохи Estado Novo.",
        "Estádio Nacional Lisbon; Estado Novo sports arena at "
        "Jamor.",
        "1944 год; спортивная monumentальность португальского "
        "режима и Jamor.",
        "1944; national stadium and fascist-era leisure at "
        "Jamor.",
    ),
    "franco_estado_novo_ministerio_aire": (
        "Министерство авиации на Paseo de la Castellana; "
        "гранитный блок рационалистско-фашистского стиля.",
        "Air Ministry Madrid; rationalist-fascist granite block "
        "1943.",
        "1943 год; военная архитектура столицы эпохи Franco "
        "и символ режима.",
        "Military architecture of the Franco regime capital on "
        "Paseo de la Castellana.",
    ),
    "franco_estado_novo_monument_discoveries": (
        "Padrão dos Descobrimentos в форме каравеллы на берегу "
        "Тежu в Лиссabonе.",
        "Padrão dos Descobrimentos; ship-shaped monument on the "
        "Tagus in Lisbon.",
        "1940–1960 годы; монумент эпохи Estado Novo в честь "
        "мореплавателей.",
        "1940–1960 Estado Novo celebration of explorers.",
    ),
    "franco_estado_novo_ponte_25_abril": (
        "Висячий мост через Тежу длиной 2277 м; ранее мост "
        "Salazar.",
        "Suspension bridge over the Tagus; 2,277 m, formerly "
        "Salazar Bridge.",
        "1962–1966 годы; инженерия United States Steel.",
        "1962–1966; engineered by United States Steel.",
    ),
    "franco_estado_novo_valle_caidos": (
        "Базилика, вырубленная в гранитном хребте; крест высотой "
        "150 м.",
        "Basilica carved in granite ridge; 150 m cross in Sierra "
        "de Guadarrama.",
        "1940–1958 годы; спорный мемориал эпохи Franco.",
        "1940–1958 Franco memorial; controversial monumentality.",
    ),
    "herrerian_aranjuez": (
        "Королевский дворец с дворами и садами на равнине Тахo; "
        "расширения Bourbon.",
        "Royal palace courtyard and gardens on the Tagus plain; "
        "Bourbon extensions.",
        "1561–1775 годы; королевский ландшафт UNESCO в Aranjuez.",
        "1561–1775; UNESCO royal landscape of Aranjuez.",
    ),
    "herrerian_el_escorial": (
        "План Juan de Herrera; гранитная масса и силуэт с "
        "четырьмя башнями.",
        "Juan de Herrera grid plan; granite mass and four-tower "
        "silhouette.",
        "1563–1584 годы для Philip II; монастырь, дворец, "
        "pantheon и библиотека.",
        "1563–1584 for Philip II; monastery, palace, pantheon, "
        "library.",
    ),
    "herrerian_moncloa": (
        "Мадридский дворец с мотивами Escorial; гранит и строгие "
        "классические линии.",
        "Madrid palace with Escorial motifs; granite and severe "
        "classical lines.",
        "XVII век; влияние стиля Эрреры в районе Moncloa.",
        "Seventeenth-century Herrerian influence near Moncloa.",
    ),
    "herrerian_palacio_carlos_v": (
        "Ренessanсный дворец «круг в квадрате» внутри Альгамбры; "
        "Pedro Machuca.",
        "Renaissance circle-in-square palace inside the "
        "Alhambra; Pedro Machuca.",
        "1527–1564 годы; суровый гранит контрастирует с "
        "насridским декором.",
        "1527–1564; austere granite contrasts Nasrid ornament.",
    ),
    "herrerian_segovia_bridge": (
        "Мост 1584 года; гранитные арки над ущельем реки Eresma.",
        "Segovia bridge of 1584; granite arches over the Eresma "
        "gorge.",
        "Инженерный проект Philip II, связывающий кварталы "
        "Segovia.",
        "Philip II engineering linking Segovia quarters.",
    ),
    "herrerian_valladolid_cathedral": (
        "Проект Juan de Herrera; незавершённые купольные башни "
        "собора.",
        "Juan de Herrera project; unfinished dome towers in "
        "Valladolid.",
        "1589–1699 годы; собор эскoriальского стиля в Castile.",
        "1589–1699; Escorial-style cathedral of Castile.",
    ),
    "herrerian_villa_magna": (
        "Зagorodная вилла провинции Valladolid; строгость и "
        "сетка плана Эрреры.",
        "Country villa in Valladolid province; Herrerian "
        "sobriety and grid.",
        "XVI век; дворянская резиденция на равнине Castile.",
        "Sixteenth-century noble retreat on the Castilian plain.",
    ),
    "isabelline_gothic_capilla_condestable": (
        "Звёздный свод кapеллы в соборе Burgos; плаmenеющая "
        "геометрия звёзд.",
        "Star-vaulted chapel in Burgos Cathedral; flamboyant "
        "star geometry.",
        "1482–1496 годы; работа семьи Simón de Colonia.",
        "1482–1496; work of the Simón de Colonia family.",
    ),
    "isabelline_gothic_el_parral": (
        "Аvgustinский монастырь Segovia; изящный изабеллинский "
        "клуatr.",
        "Augustinian monastery in Segovia; delicate Isabelline "
        "tracery cloister.",
        "1477–1494 годы; монастырь на склоне над Segovia.",
        "1477–1494; hillside monastery overlooking Segovia.",
    ),
    "isabelline_gothic_miraflores": (
        "Кartuzianский монастырь; alabaster-гrobницы John II и "
        "Isabella of Portugal.",
        "Carthusian charterhouse; alabaster tombs of John II and "
        "Isabella of Portugal.",
        "1482–1496 годы; скульптурный шедевр Gil de Siloé в "
        "Burgos.",
        "Sculptural masterpiece by Gil de Siloé in Burgos.",
    ),
    "isabelline_gothic_san_gregorio": (
        "Фасад Colegio de San Gregorio; каменная кружevная "
        "резьба.",
        "Plateresque-Isabelline façade of San Gregorio college; "
        "rich stone lace.",
        "Кollegio для подготовки королевских чиновников в XV "
        "веке.",
        "Training school for royal administrators, fifteenth "
        "century.",
    ),
    "isabelline_gothic_san_juan_reyes": (
        "Монастырь заказан Ferdinand и Isabella; фасад с цепями "
        "и Moorish декором.",
        "Monastery commissioned by Ferdinand and Isabella; "
        "chain-and-moor façade decoration.",
        "1477–1504 годы; вершина изабеллинской готики Толедo.",
        "1477–1504; pinnacle of Isabelline Gothic in Toledo.",
    ),
    "isabelline_gothic_san_pablo_valladolid": (
        "Изабelлинский фасад с гербами и скульптурными нишами.",
        "Isabelline façade with heraldic shields and sculptural "
        "niches.",
        "Dominican церковь; ориентир исторического центра "
        "Valladolid и изабеллинский шедевр.",
        "Dominican church; landmark of Valladolid historic "
        "centre and Isabelline masterpiece.",
    ),
    "isabelline_gothic_toledo_portal": (
        "Зapadный портал собора Толедo; тиmpan с Тайной вечерей.",
        "West portal of Toledo Cathedral; sculpted Last Supper "
        "tympanum.",
        "Изабelлинская скульптура primada-кatedral Испании и "
        "западного портала.",
        "Isabelline sculpture at Spain's primate cathedral "
        "west portal.",
    ),
    "islamic_iberia_alcazar_seville": (
        "Patio de las Doncellas и зал послов с мудéjarской "
        "штукатуркой.",
        "Patio de las Doncellas and Ambassadors' Hall with "
        "Mudéjar stucco.",
        "Действующая резиденция; слои от Almohad до Pedro I of "
        "Castile.",
        "Still a royal residence; layers from Almohad to Pedro I "
        "of Castile.",
    ),
    "islamic_iberia_alhambra": (
        "Насridские дворцы на холме Assabica; stucco, muqarnas и "
        "калligraphические пояса.",
        "Nasrid palaces on the Assabica hill; stucco, muqarnas "
        "and inscription bands.",
        "Объект UNESCO; символ Granada и завершения Реконquista "
        "1492 года.",
        "UNESCO site; symbol of Granada and the 1492 "
        "Reconquista.",
    ),
    "islamic_iberia_aljaferia": (
        "Taifa-дворец Banu Hud; кирpич, арочные залы и "
        "деревянные потолки.",
        "Taifa palace of the Banu Hud; brick halls, arches and "
        "timber ceilings.",
        "Позже резиденция королей Aragon; ядро Cortes в "
        "Zaragoza.",
        "Later an Aragonese royal seat; core of the Zaragoza "
        "Cortes.",
    ),
    "islamic_iberia_banos_magdalena": (
        "Исlamский hammam со звёздными световыми отверстиями в "
        "каменных свodax.",
        "Islamic hammam with star-shaped light openings in stone "
        "vaults.",
        "Редкий образец гражданской архитектуры кordobского "
        "халифата.",
        "Rare example of civic architecture in caliphal Córdoba.",
    ),
    "islamic_iberia_comares": (
        "Тронный зал с muqarnas-куpolом и легендарным троном у "
        "окна.",
        "Throne room with muqarnas dome and the legendary throne "
        "by the window.",
        "Политический центр двора Nasrid в XIV веке.",
        "Political heart of the fourteenth-century Nasrid court.",
    ),
    "islamic_iberia_giralda": (
        "Almohad-минaret около 104 м; позже добавлен "
        "Renaissance-кolokольня.",
        "Almohad minaret about 104 m high; a Renaissance belfry "
        "was added later.",
        "Бывший минaret Great Mosque; символ skyline Севильи.",
        "Former Great Mosque minaret; icon of the Seville "
        "skyline.",
    ),
    "islamic_iberia_medina_azahara": (
        "Халифский город западнее Córdoba; Rich Hall и базilical "
        "тронный зал.",
        "Caliphal city west of Córdoba; Rich Hall and basilical "
        "throne room.",
        "UNESCO; роскошь Abd al-Rahman III в IX веке.",
        "UNESCO site; ninth-century splendour of Abd al-Rahman "
        "III.",
    ),
    "islamic_iberia_mezquita_cordoba": (
        "Колонны из spolia; красные и белые клинья арок создают "
        "ритм зала.",
        "Spolia columns; alternating red and white voussoirs "
        "rhythm the hall.",
        "Расширена al-Hakam II; позже в центре встроен "
        "христианский choir.",
        "Expanded by al-Hakam II; later a Christian choir was "
        "inserted at centre.",
    ),
    "islamic_iberia_palacio_partal": (
        "Портик с аркадами отражается в бассейне; сохранённый "
        "садовый павильон.",
        "Arcaded portico reflected in the pool; a preserved "
        "garden pavilion.",
        "Один из ранних насridских ансамблей Альгамбры.",
        "One of the earliest surviving Nasrid structures in the "
        "Alhambra.",
    ),
    "islamic_iberia_torre_del_oro": (
        "Двенadцатигранная башня на Guadalquivir; связана с "
        "цепью через реку.",
        "Dodecagonal tower on the Guadalquivir; linked to a "
        "chain across the river.",
        "Построена при Almohad; сегодня морской музей Севильи.",
        "Built under Almohad rule; now a maritime museum.",
    ),
    "manuelin_alcobaca_detail": (
        "Цistercianское аббатство Alcobaça; мануэlino-дополнения "
        "к готической церкви.",
        "Cistercian Abbey of Alcobaça; Manueline additions to "
        "the Gothic church.",
        "UNESCO; королевские гrobницы Pedro I и Inês de Castro.",
        "UNESCO; royal tombs of Pedro I and Inês de Castro.",
    ),
    "manuelin_batalha_unfinished": (
        "Незавершённые kapelлы с восьмигранными столбами и "
        "ребрами свodov «морских канатов».",
        "Unfinished chapels with octagonal piers and sea-rope "
        "vault ribs.",
        "Переход от поздней готики к манuэlino после битвы 1385 "
        "года.",
        "Transition from Late Gothic to Manueline after the 1385 "
        "battle.",
    ),
    "manuelin_belem_church": (
        "Церковь Santa Maria de Belém; ребра свodov наподобие "
        "перевёрнутых корпусов.",
        "Church of Santa Maria de Belém; rib vaults like "
        "upturned ship hulls.",
        "Часть ансамбля Jerónimos; королевское покровительство.",
        "Part of the Jerónimos Monastery ensemble; royal "
        "patronage.",
    ),
    "manuelin_belem_tower": (
        "Укреплённая башня у estuary Тежu; мануэlino-бastionы и "
        "араbesque-балконы.",
        "Fortified tower on the Tagus estuary; Manueline "
        "bastions and arabesque balconies.",
        "1514–1520 годы; Francisco de Arruda; икona эпохи "
        "открытий.",
        "1514–1520 by Francisco de Arruda; Age of Discovery "
        "icon.",
    ),
    "manuelin_casa_bicos": (
        "Пирамидальный «алмазный» фасад в Лиссabonе; 1523 год, "
        "Brás de Albuquerque.",
        "Pyramidal diamond-point façade in Lisbon; 1523, Brás de "
        "Albuquerque.",
        "Редкий гражданский мануэlino на Rua dos Bacalhoeiros.",
        "Rare Manueline civic façade on the Rua dos "
        "Bacalhoeiros.",
    ),
    "manuelin_convento_cristo": (
        "Charola — шестнадцатигранная тамплиерская рotonda; "
        "манuэlino-окно Chapter House.",
        "Charola — sixteen-sided Templar rotunda; Manueline "
        "window of the Chapter House.",
        "Штаб-квартира ордена Христа в Tomar; ансамбль UNESCO.",
        "Tomar headquarters of the Order of Christ; UNESCO "
        "ensemble.",
    ),
    "manuelin_evora_manueline": (
        "Манuэlino-ворота замка Évora; armillary sphere и "
        "морские канаты.",
        "Manueline gate at Évora castle; armillary sphere and "
        "maritime ropes.",
        "Провинциальный манuэlino в историческом Évora под "
        "UNESCO.",
        "Provincial Manueline in UNESCO historic Évora.",
    ),
    "manuelin_jeronimos": (
        "Манuэlino-клуatr и церковь; гrobница Vasco da Gama "
        "внутри.",
        "Manueline cloister and church; Vasco da Gama's tomb "
        "inside.",
        "UNESCO; известняковая ажурность и морские мотивы "
        "Лиссabonа.",
        "UNESCO; limestone lacework and maritime motifs in "
        "Lisbon.",
    ),
    "manuelin_porto_silva": (
        "Фасад Casa do Silva; манuэlino-окna в центре Порту.",
        "Casa do Silva façade; Manueline window frames in Porto "
        "centre.",
        "Купеческий дом XVI века; северный манuэlino.",
        "Sixteenth-century merchant house of northern Manueline.",
    ),
    "manuelin_setubal_convent": (
        "Клуатр Convento da Graça в Сетубале; пышные "
        "мануэlino-каpitели и резные своды.",
        "Convento da Graça cloister; florid Manueline capitals "
        "in Setúbal.",
        "1520-е годы; важная мастерская южного "
        "мануэlino в Португалии.",
        "1520s Manueline workshop of southern Portugal by the "
        "Tagus estuary.",
    ),
    "mudejar_cristo_luz": (
        "Бывшая мечеть 999 года; подковообразные арки и "
        "квадратное основание минareta.",
        "Former mosque of 999; horseshoe arches and a square "
        "minaret base.",
        "Ранний мудéjar; переход от исlamского к христианскому "
        "культу.",
        "Early Mudéjar transition from Islamic to Christian "
        "worship.",
    ),
    "mudejar_monasterio_piedra": (
        "Cistercianский монастырь с кирpичными мудéjar-деталями "
        "среди водопadov парка.",
        "Cistercian monastery with brick Mudéjar details amid "
        "park waterfalls.",
        "XII–XIII века; синтез романского монастыря и исlamского "
        "орнамента.",
        "Twelfth–thirteenth c.; synthesis of monastic Romanesque "
        "and Islamic ornament.",
    ),
    "mudejar_san_martin_toledo": (
        "Кирpичный фасад с вложенными арками; приходская церковь "
        "XIII века.",
        "Brick façade with nested arches; thirteenth-century "
        "Toledo parish church.",
        "Образец тoledского мудéjar после Реконquista.",
        "Model of Toledan Mudéjar after the Reconquista.",
    ),
    "mudejar_teruel_towers": (
        "Кирpичные колокольни с полихромной керамикой и "
        "glazированными фризами.",
        "Brick bell towers with polychrome ceramics and glazed "
        "friezes.",
        "UNESCO «Mudejar of Aragon»; иконы skyline Тeruel.",
        "UNESCO Mudejar of Aragon; icons of the Teruel skyline.",
    ),
    "neoclassicism_bank_spain": (
        "Штаб-квартира Banco de España; monumentальный "
        "эклектично-неоклассический блок.",
        "Bank of Spain headquarters; monumental "
        "eclectic-neoclassical block.",
        "1884–1891 годы; Eduardo Adaro и Severiano de la Puerta.",
        "1884–1891 by Eduardo Adaro and Severiano de la Puerta.",
    ),
    "neoclassicism_cadiz_monument": (
        "Monument конституции 1812 года; колонна и "
        "алlegorические фигуры.",
        "Monument to the 1812 Constitution in Cádiz; column and "
        "allegorical figures.",
        "1812–1830 годы; либeralный неoklassицизм после "
        "наполеоновских войн.",
        "1812–1830; liberal neoclassicism after the Napoleonic "
        "wars.",
    ),
    "neoclassicism_lisbon_academy": (
        "Академия изящных искусств; неoklassический portico и "
        "музей скульптуры.",
        "Academy of Fine Arts Lisbon; neoclassical portico and "
        "sculpture museum.",
        "1836–1855 годы; центр подготовки португальского "
        "неoklassицизма и скульптуры.",
        "1836–1855; training centre of Portuguese neoclassicism "
        "and sculpture.",
    ),
    "neoclassicism_prado": (
        "Неoklassический музей Juan de Villanueva; сводные залы "
        "Paseo del Prado.",
        "Juan de Villanueva neoclassical museum; vaulted halls "
        "on the Paseo del Prado.",
        "1785–1819 годы; ядро национальной художественной "
        "коллекции Испании.",
        "1785–1819; core of Spain's national art collection.",
    ),
    "neoclassicism_puerta_alcala": (
        "Гранитная триумфальная арка; пять проёмов для Charles "
        "III в Мадridе.",
        "Granite triumphal arch; five openings for Charles III "
        "in Madrid.",
        "1769–1778 годы; Francesco Sabatini; неoklassические "
        "городские ворота.",
        "1769–1778 by Francesco Sabatini; neoclassical city "
        "gate.",
    ),
    "neoclassicism_royal_palace": (
        "Королевский дворец Philip V; двор Sabatini и потolki "
        "Tiepolo.",
        "Philip V royal palace Madrid; Sabatini courtyard and "
        "Tiepolo ceilings.",
        "1738–1755 годы на месте пожара Alcázar; крупнейший "
        "королевский дворец Европы.",
        "1738–1755 on Alcázar fire site; largest royal palace in "
        "Europe.",
    ),
    "neoclassicism_teatro_real": (
        "Мadriдская opera; неoklassический portico и "
        "подковообразный зал.",
        "Madrid opera house; neoclassical portico and horseshoe "
        "auditorium.",
        "1818–1850 годы; главный лирический театр Испании и "
        "королевской оперы.",
        "1818–1850; principal lyric theatre of Spain and royal "
        "opera.",
    ),
    "plateresque_alcala": (
        "Фасад Colegio Mayor San Ildefonso; пokrovительство "
        "Cardinal Cisneros.",
        "Colegio Mayor San Ildefonso façade; patronage of "
        "Cardinal Cisneros.",
        "1499–1516 годы; здесь позже учился Miguel de Cervantes.",
        "1499–1516; where Miguel de Cervantes later studied.",
    ),
    "plateresque_casa_consistorial": (
        "Plateresque-эkran ратуши Сalamanки; балконы над Plaza "
        "Mayor.",
        "Salamanca town hall Plateresque screen; balconies over "
        "the Plaza Mayor.",
        "Гражданский платерескo университетского города и "
        "ратуши Salamanca.",
        "Civic Plateresque heart of the university city and "
        "Salamanca town hall.",
    ),
    "plateresque_casa_pilatos": (
        "Сevильский дворец с мудéjar-patio и "
        "платерескo-штукатуркой.",
        "Seville mansion blending Mudéjar patios and Plateresque "
        "stucco.",
        "1483–1539 годы; образец андalusийского дворянского "
        "домa.",
        "1483–1539; model Andalusian noble palace.",
    ),
    "plateresque_monterrey": (
        "Palacio de Monterrey; угловые башни и гранитный дворец "
        "Сalamanки.",
        "Palacio de Monterrey; corner towers and granite "
        "Salamanca palace.",
        "1539–1559 годы; резиденция графов Monterrey.",
        "1539–1559 aristocratic seat of the counts of Monterrey.",
    ),
    "plateresque_plasencia": (
        "Сobor с поздne-готическими свodами и ренessanсным "
        "платерескo.",
        "Cathedral mixing Late Gothic vaults and Renaissance "
        "Plateresque.",
        "Два архитектурных стиля рядом в Plasencia.",
        "Two architects' styles side by side in Plasencia.",
    ),
    "plateresque_salamanca_univ": (
        "Plateresque-фасад 1415–1533 годов; medallions и символ "
        "граната.",
        "Plateresque façade 1415–1533; medallions and "
        "pomegranate symbols.",
        "Фасад Quinta patio — иkona испанского ренessanсного "
        "университета.",
        "Quinta patio façade — icon of the Spanish Renaissance "
        "university.",
    ),
    "plateresque_seville_ayuntamiento": (
        "Ратуша Сevили; Diego de Riaño и двор в стиле Эрреры.",
        "Seville city hall; Diego de Riaño Plateresque then "
        "Herrera courtyard.",
        "1527–1596 годы; сердце Plaza de San Francisco.",
        "1527–1596; civic heart on the Plaza de San Francisco.",
    ),
    "portuguese_art_nouveau_aveiro_major": (
        "Casa do Major Pessoa; azulejo-панели и ар-nouveau ковка "
        "в Aveiro.",
        "Casa do Major Pessoa; azulejo panels and whiplash "
        "ironwork in Aveiro.",
        "1909 год; провинциальный ар-nouveau на Ria de Aveiro.",
        "1909; provincial Art Nouveau on the Ria de Aveiro.",
    ),
    "portuguese_art_nouveau_cafe_majestic": (
        "Café Majestic; зеркala и деревo в интерьере belle "
        "époque.",
        "Café Majestic; mirrors and wood in Art Nouveau Belle "
        "Époque café.",
        "1921 год, Порту; светское место встречи буржуазии.",
        "1921 Porto; secular gathering place of the bourgeoisie.",
    ),
    "portuguese_art_nouveau_livraria_lello": (
        "Livraria Lello; красная лестница и витражи ар-nouveau в "
        "Порту.",
        "Livraria Lello; red staircase and Art Nouveau stained "
        "glass in Porto.",
        "1906 год, Xavier Esteves; икona португальского Arte "
        "Nova.",
        "1906 Xavier Esteves; icon of Portuguese Arte Nova.",
    ),
    "portuguese_art_nouveau_medeiros_almeida": (
        "Особняк-музей Medeiros e Almeida; интерьеры ар-nouveau "
        "в Лиссabonе.",
        "Medeiros e Almeida museum mansion; Art Nouveau "
        "interiors in Lisbon.",
        "1896–1903 годы; дом коллекционера, ставший музеем.",
        "1896–1903; collector's house turned museum.",
    ),
    "portuguese_art_nouveau_palacio_sereias": (
        "Palácio das Sereias; мотивы siren и штукатурка "
        "ар-nouveau.",
        "Palácio das Sereias; mermaid motifs and Art Nouveau "
        "stucco in Lisbon.",
        "1905–1909 годы; ректорат университета с богатым "
        "фасадом.",
        "1905–1909; university rectory with ornate façade.",
    ),
    "portuguese_art_nouveau_rossio_station": (
        "Фасад станции Rossio; неo-манuэlino и ар-nouveau "
        "железo.",
        "Rossio station façade; Manueline revival and Art "
        "Nouveau iron.",
        "1886–1890 годы; portal в центре Лиссabonа.",
        "1886–1890; neo-Manueline portal in Lisbon centre.",
    ),
    "portuguese_art_nouveau_serralves_early": (
        "Casa de Serralves; вилла ар-deco и формальные сады "
        "Порту.",
        "Casa de Serralves; Art Deco villa and formal gardens in "
        "Porto.",
        "1925–1944 годы; переход от Arte Nova к ар-deco.",
        "1925–1944; transition from Arte Nova to Art Deco.",
    ),
    "portuguese_baroque_bom_jesus": (
        "Baroque-лестница sanctuario Бragi; зигzag-каpelы на "
        "горе Espinho.",
        "Baroque stairway at Braga sanctuary; zigzag chapels "
        "climbing Mount Espinho.",
        "1722–1811 годы; лandscape-архитектура паломничества.",
        "1722–1811; landscape architecture of pilgrimage.",
    ),
    "portuguese_baroque_clerigos": (
        "Башня Nicolau Nasoni 75 м; гранитный baroque-ориентир "
        "Порту.",
        "Nicolau Nasoni tower 75 m; granite baroque landmark of "
        "Porto.",
        "1754–1763 годы; церковь и башня братства Clérigos.",
        "1754–1763; Clerigos brotherhood church and tower.",
    ),
    "portuguese_baroque_estrela": (
        "Basílica da Estrela; kupol и розовый мрамор интерьера.",
        "Basílica da Estrela; dome and pink marble interior in "
        "Lisbon.",
        "1779–1790 годы; обet Maria I после рождения наследника.",
        "1779–1790 Maria I's vow after an heir was born.",
    ),
    "portuguese_baroque_mafra": (
        "Basilica с twin-бashнями; дворец-монастырь João V.",
        "Basilica with twin towers; royal palace-monastery of "
        "João V.",
        "1717–1755 годы; 40 000 м² — крупнейший baroque-ансамбль "
        "Португалии.",
        "1717–1755; 40,000 m² — largest Portuguese baroque "
        "ensemble.",
    ),
    "portuguese_baroque_mercy_porto": (
        "Церковь Misericórdia; фасад Nicolau Nasoni и "
        "позолоченный интерьер.",
        "Misericórdia church in Porto; Nicolau Nasoni façade and "
        "gilded interior.",
        "1747–1750 годы; baroque-архитектура братства "
        "милосердия.",
        "1747–1750; charity brotherhood baroque architecture.",
    ),
    "portuguese_baroque_pantheon": (
        "Kupol Santa Engrácia; национальный pantheon с 1966 "
        "года.",
        "Santa Engrácia dome; baroque-national pantheon since "
        "1966.",
        "1681–1966 годы; долго незавершённая «Patela» Лиссabonа.",
        "1681–1966 — long unfinished 'Patela' of Lisbon.",
    ),
    "portuguese_baroque_queluz": (
        "Rococo-дворец и сады у дороги Sintra; Mirror Room и "
        "azulejo-галереи.",
        "Rococo palace gardens on the Sintra road; Mirror Room "
        "and tiled galleries.",
        "1747–1792 годы; летний двор до землетрясения 1755 года.",
        "1747–1792; royal summer court before the 1755 "
        "earthquake.",
    ),
    "portuguese_baroque_raio": (
        "Дворец Raio в Braga; синий azulejo-фасад и "
        "baroque-балконы.",
        "Raio palace in Braga; blue tile façade and baroque "
        "balconies.",
        "1755–1756 годы; гражданский baroque André Soares.",
        "1755–1756 civic baroque mansion by André Soares.",
    ),
    "portuguese_baroque_santa_clara_porto": (
        "Santa Clara в Порту; резное деревo и мрамор внутри.",
        "Santa Clara church in Porto; gilded wood and carved "
        "marble interior.",
        "1627–1693 годы; жemчужина северного baroque Португалии.",
        "1627–1693; northern Portuguese baroque jewel.",
    ),
    "portuguese_baroque_sao_roque": (
        "São Roque; kapelла São João Baptista из драгоценных "
        "камней.",
        "São Roque church; Chapel of St John the Baptist in "
        "precious stones.",
        "1500–1610 годы; иezuitские мраморные kapelлы Лиссabonа.",
        "1500–1610 Jesuit marble chapels in Lisbon.",
    ),
    "postwar_modern_barceloneta_hotels": (
        "Отельные блоки Barceloneta 1950-х; морской "
        "туристический modern.",
        "1950s Barceloneta hotel blocks; seaside tourism modern "
        "architecture.",
        "Эпоха Franco; открытие Средизemnomorya массовому "
        "туризму и отдыху.",
        "Franco-era opening to Mediterranean mass tourism and "
        "leisure.",
    ),
    "postwar_modern_benidorm": (
        "Высотные башни курорта Benidorm; skyline Levante и "
        "Poniente.",
        "Benidorm high-rise resort; Levante and Poniente tower "
        "skyline.",
        "1960–70-е годы; модель массового туризма Costa Blanca.",
        "1960s–70s mass tourism urban model on the Costa Blanca.",
    ),
    "postwar_modern_chamartin": (
        "Станция Chamartín; современный железnodorожный узел "
        "севера Мадрида.",
        "Chamartín station; modern rail hub north of Madrid "
        "1970s.",
        "1970–1980-е годы; модernизация транспорта и линий AVE.",
        "Transport modernisation and AVE high-speed connections.",
    ),
    "postwar_modern_edificio_espana": (
        "Edificio España 117 м; кирpично-kamenная башня Plaza "
        "España.",
        "Edificio España 117 m; brick and stone tower on Plaza "
        "España.",
        "1948–1953 годы; братья Otamendi; skyline эпохи Franco.",
        "1948–1953; Otamendi brothers Franco-era skyline.",
    ),
    "postwar_modern_social_housing": (
        "Corralas и панельные кvartалы Franco; государственное "
        "массовое жильё.",
        "Franco-era corralas and slab blocks; state-sponsored "
        "mass housing Madrid.",
        "1950–1970 годы; социальная архитектура городской "
        "миграции.",
        "1950–1970 social architecture of urban migration.",
    ),
    "postwar_modern_torre_madrid": (
        "Torre de Madrid 142 м; первый небоскрёb Plaza España.",
        "Torre de Madrid 142 m; first Madrid skyscraper near "
        "Plaza España.",
        "1954–1957 годы; иkona послевоенной вертикальной "
        "modernизации.",
        "1954–1957; post-war vertical modernisation icon.",
    ),
    "postwar_modern_torre_picasso": (
        "Torre Picasso 157 м; стальная башня Minoru Yamasaki в "
        "AZCA.",
        "Torre Picasso 157 m; Minoru Yamasaki steel tower in "
        "AZCA Madrid.",
        "1982–1988 годы; международный поздний modern "
        "корпоративного skyline.",
        "1982–1988; international late-modern corporate skyline.",
    ),
    "rationalist_interwar_casa_blok": (
        "Casa Bloc Sant Andreu; социальное жильё GATCPAC с общей "
        "крышей.",
        "Casa Bloc Sant Andreu; GATCPAC social housing with "
        "shared roof.",
        "1933–1936 годы; Josep Lluís Sert и Torres Clavé.",
        "1933–1936 by Josep Lluís Sert and Torres Clavé.",
    ),
    "rationalist_interwar_casa_flores": (
        "Casa de las Flores; рационalist balconies Eduardo "
        "Mancebo.",
        "Casa de las Flores Madrid; Eduardo Mancebo rationalist "
        "balconies.",
        "1930–1932 годы; ранняя межвоенная moderna жилья "
        "Мадрида.",
        "1930–1932; early Spanish interwar housing modernity.",
    ),
    "rationalist_interwar_casa_junceda": (
        "Casa Junceda — жилой дом GATCPAC в квартале "
        "Eixample Барселоны.",
        "Casa Junceda; GATCPAC apartment block in Barcelona "
        "Eixample.",
        "1930 год; функционalist balconies, плоская крыша "
        "и общая терраса.",
        "1930 functionalist balconies and shared flat roof "
        "terrace.",
    ),
    "rationalist_interwar_club_union": (
        "Club de la Unión; строгий классический рационализм "
        "центра.",
        "Club de la Unión; stripped classical rationalism in "
        "Madrid centre.",
        "1925–1929 годы; элитный клуб межвоенной modernы.",
        "1925–1929; elite social club modern architecture.",
    ),
    "rationalist_interwar_nautical_club": (
        "Reial Club Marítim — рационalist-клуб на "
        "набережной Barceloneta.",
        "Reial Club Marítim Barcelona; rationalist waterfront "
        "clubhouse.",
        "1930–1940 годы; морская досуговая архитектура "
        "портового квартала.",
        "1930–1940; maritime leisure architecture at Barceloneta "
        "waterfront.",
    ),
    "rationalist_interwar_pueblo_espanol": (
        "Pueblo Español 1929; полномасшtabные копии региональной "
        "архитектуры.",
        "Pueblo Español 1929 Expo; full-scale regional "
        "architecture replicas.",
        "Архитектурный музей Montjuïc; historicism для "
        "экспозиции.",
        "Architectural museum on Montjuïc; historicism meets "
        "display.",
    ),
    "rationalist_interwar_telefonica": (
        "Edificio Telefónica 89 м; ранний небоскрёb Gran Vía.",
        "Edificio Telefónica Gran Vía; 89 m early Madrid "
        "skyscraper.",
        "1926–1929 годы; Ignacio de Cárdenas; рационalist-башня.",
        "1926–1929 Ignacio de Cárdenas; rationalist tower.",
    ),
    "roman_hispania_aqueduct_segovia": (
        "Высота около 28,5 м; 167 арок из гранита без раствора в "
        "верхнем ярусе.",
        "About 28.5 m high; 167 granite arches, dry-jointed in "
        "the upper tier.",
        "UNESCO с 1985 года; подавал воду из реки Frío.",
        "UNESCO since 1985; carried water from the Frío river.",
    ),
    "roman_hispania_bridge_alcantara": (
        "Шесть арок через Тахо; триумфальная арка с посвящением "
        "императору Trajan.",
        "Six arches over the Tagus; triumphal arch dedicated to "
        "Emperor Trajan.",
        "Построен около 104 н.э. инженером Cayo Julio Lacer.",
        "Built c. 104 CE by the engineer Gaius Julius Lacer.",
    ),
    "roman_hispania_italica": (
        "Амфiteatr на 25 000 мест; город ветеранов Second "
        "Spanish Legion.",
        "Amphitheatre for about 25,000; town for veterans of the "
        "Second Spanish Legion.",
        "Родина императоров Trajan и Hadrian; раскопки у "
        "Santiponce.",
        "Birthplace of emperors Trajan and Hadrian; excavated "
        "near Santiponce.",
    ),
    "roman_hispania_tarragona": (
        "Амфiteatr II века на склоне к морю; arena для "
        "gladiatorских игр.",
        "Second-century amphitheatre on the sea slope; arena for "
        "gladiatorial games.",
        "Часть римской Tarraco, столицы Hispania Citerior; "
        "UNESCO.",
        "Part of Roman Tarraco, capital of Hispania Citerior; "
        "UNESCO site.",
    ),
    "roman_hispania_theatre_merida": (
        "Сцена с мраморной scaenae frons; вместимость около "
        "шести тысяч зрителей.",
        "Marble scaenae frons stage; seated about six thousand "
        "spectators.",
        "Основан при Augustus; сердце Augusta Emerita, столицы "
        "Lusitania.",
        "Founded under Augustus; core of Augusta Emerita, "
        "capital of Lusitania.",
    ),
    "romanesque_fromista": (
        "Центрический kupol на pendentives; kamenная церковь на "
        "Camino.",
        "Central dome on pendentives; stone church on the Camino "
        "route.",
        "Образец чистой romanesque-геометрии в Palencia.",
        "Model of pure Romanesque geometry in Palencia.",
    ),
    "romanesque_jaca": (
        "Первый cathedral Aragon; шахmatная kladка на стенах.",
        "First cathedral of Aragon; chequerboard stone on "
        "exterior walls.",
        "XI век; отправная точка Aragonese Romanesque route.",
        "Eleventh century; starting point of the Aragonese "
        "Romanesque route.",
    ),
    "romanesque_san_isidoro": (
        "Royal pantheon с frescos XI века; Leónese "
        "romanesque-церковь.",
        "Royal pantheon with eleventh-century frescoes; Leonese "
        "Romanesque church.",
        "Panteón de los Reyes — «Сikstinskaya kapelла» "
        "romanesque Испании.",
        "Panteón de los Reyes — a 'Sistine Chapel' of Romanesque "
        "Spain.",
    ),
    "romanesque_santiago": (
        "Фасад Obradoiro и botafumeiro; крипta с мощами апостола "
        "James.",
        "Obradoiro façade and botafumeiro; crypt with relics of "
        "Saint James.",
        "Кульминация Camino de Santiago; объект UNESCO.",
        "Climax of the Camino de Santiago; UNESCO World "
        "Heritage.",
    ),
    "romanesque_santo_domingo_silos": (
        "Двухъярусный cloister с резными каpitелями библейских "
        "сюжетов.",
        "Two-storey cloister with capitals carved with biblical "
        "scenes.",
        "Benedictine abbey Castile; центр monastic reform XI "
        "века.",
        "Benedictine abbey of Castile; centre of "
        "eleventh-century monastic reform.",
    ),
    "spanish_baroque_cartuja_granada": (
        "Cartuja Granada; polychrome-мрамор sacristy и "
        "tabernacle.",
        "Granada Charterhouse; polychrome marbles of sacristy "
        "and tabernacle.",
        "1506–1654 годы; baroque-избыток у подножия Sierra "
        "Nevada.",
        "1506–1654; baroque excess at the foot of Sierra Nevada.",
    ),
    "spanish_baroque_el_paular": (
        "Monastery в Sierra de Guadarrama; кirpичный baroque и "
        "горный пейзаж.",
        "Monastery in the Sierra de Guadarrama; brick baroque "
        "and mountain setting.",
        "XVII век; королевское убежище у Rascafría.",
        "Seventeenth-century royal retreat near Rascafría.",
    ),
    "spanish_baroque_granada_cathedral": (
        "План Diego de Siloé; позже baroque-kupol преemников.",
        "Diego de Siloé plan; later baroque dome by his "
        "successors.",
        "1523–1704 годы; сердце хristian Granada после 1492 "
        "года.",
        "1523–1704; heart of Christian Granada after 1492.",
    ),
    "spanish_baroque_obradoiro": (
        "Baroque-фасад Fernando Casas y Novoa собора Santiago "
        "1750 года.",
        "Fernando de Casas y Novoa baroque façade of Santiago "
        "Cathedral, 1750.",
        "Galician baroque-ориентир паломников на Obradoiro.",
        "Galician baroque pilgrimage landmark on Obradoiro "
        "square.",
    ),
    "spanish_baroque_plaza_mayor": (
        "Проект Juan Gómez de Mora; единые kirpичные фасады и "
        "porticos.",
        "Juan Gómez de Mora design; uniform brick façades and "
        "porticos.",
        "1617–1619 годы для Philip III; образец baroque-площади "
        "Испании.",
        "1617–1619 for Philip III; model Spanish baroque square.",
    ),
    "spanish_baroque_san_francisco": (
        "Kupol-церковь Madrid; Francisco Cabezas и plan "
        "греческого креста.",
        "Domed church in Madrid; Francisco Cabezas and large "
        "Greek-cross plan.",
        "1761–1784 годы; переход baroque к neoclassicism в "
        "Мадridе.",
        "1761–1784; neoclassical-baroque transition in Madrid.",
    ),
    "spanish_baroque_tavera": (
        "Hospital Tavera Toledo; kupol-церковь и симметричный "
        "двор.",
        "Hospital de Tavera in Toledo; domed church and "
        "symmetrical courtyard.",
        "1541–1603 годы; здесь похоронены El Greco и знать.",
        "1541–1603; El Greco and nobles buried here.",
    ),
    "visigothic_san_juan_banos": (
        "Освящена в 661 году королём Reccared; basílica с "
        "тройной apse.",
        "Consecrated in 661 by King Reccared; basilica plan with "
        "triple apse.",
        "Редкий храм VII века в Castilla y León.",
        "Rare surviving seventh-century church in Castilla y "
        "León.",
    ),
    "visigothic_san_pedro_mata": (
        "Руины monastic церкви VII века около Toledo; открытые "
        "раскопки.",
        "Ruins of a seventh-century monastic church near Toledo; "
        "open archaeological excavations.",
        "Свидетельство вестgотского присутствия в столице "
        "короны.",
        "Evidence of Visigothic presence in the Visigothic "
        "capital.",
    ),
    "visigothic_santa_comba": (
        "Малая basílica у озера Castro; kamenная kladка без "
        "штукатурки.",
        "Small lakeside basilica at Castro; stone masonry left "
        "without external render.",
        "Образец галисийского вестgотского зodчества в Ourense.",
        "Model of Galician Visigothic architecture in Ourense.",
    ),
    "visigothic_santa_lucia": (
        "Тройной nef и horseshoe arches; VII век в Extremadura.",
        "Triple nave and horseshoe arches; seventh century in "
        "Extremadura.",
        "Связана с вестgотской традицией до арабского "
        "завоевания.",
        "Linked to Visigothic tradition before the Arab "
        "conquest.",
    ),
    "visigothic_vega_del_mar": (
        "Basílica с двойной apse на Costa del Sol.",
        "Basilica with a double apse on the Costa del Sol shore.",
        "Один из немногих андalusийских вестgотских памятников у "
        "Marbella.",
        "One of few Andalusian Visigothic monuments near "
        "Marbella.",
    ),
}


def _word_count(place: dict[str, Any]) -> int:
    ru = " ".join(
        str(place.get(k) or "")
        for k in ("history_ru", "significance_ru")
    ).strip()
    en = " ".join(
        str(place.get(k) or "")
        for k in ("history_en", "significance_en")
    ).strip()
    text = ru if len(ru.split()) >= len(en.split()) else en
    return len(re.findall(r"[\w']+", text, re.UNICODE))


def apply_thin_text_supplements(place: dict[str, Any]) -> dict[str, Any]:
    """Append supplemental prose when narrative is under MIN_NARRATIVE_WORDS."""
    slug = str(place.get("slug") or "")
    if _word_count(place) >= MIN_NARRATIVE_WORDS:
        return place
    block = _SUPPLEMENTS.get(slug)
    if not block:
        return place
    merged = dict(place)
    for ru_key, en_key, idx_ru, idx_en in (
        ("history_ru", "history_en", 0, 1),
        ("significance_ru", "significance_en", 2, 3),
    ):
        extra_ru = block[idx_ru].strip()
        extra_en = block[idx_en].strip()
        if extra_ru:
            cur = str(merged.get(ru_key) or "").strip()
            merged[ru_key] = (cur + " " + extra_ru).strip() if cur else extra_ru
        if extra_en:
            cur = str(merged.get(en_key) or "").strip()
            merged[en_key] = (cur + " " + extra_en).strip() if cur else extra_en
    desc_ru = " ".join(
        x
        for x in (
            str(merged.get("history_ru") or "").strip(),
            str(merged.get("significance_ru") or "").strip(),
        )
        if x
    )
    desc_en = " ".join(
        x
        for x in (
            str(merged.get("history_en") or "").strip(),
            str(merged.get("significance_en") or "").strip(),
        )
        if x
    )
    if desc_ru:
        merged["description_ru"] = desc_ru
        merged["description"] = desc_ru
    if desc_en:
        merged["description_en"] = desc_en
    if merged.get("history_ru"):
        merged["history"] = merged["history_ru"]
    if merged.get("significance_ru"):
        merged["significance"] = merged["significance_ru"]
    return merged
