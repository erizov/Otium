# -*- coding: utf-8 -*-
"""Curated seed examples with bilingual text."""

from __future__ import annotations

from typing import Any


def _ex(
    suffix: str,
    name_ru: str,
    name_en: str,
    *,
    year: str = "",
    city_ru: str = "",
    city_en: str = "",
    history_ru: str = "",
    history_en: str = "",
    significance_ru: str = "",
    significance_en: str = "",
    commons_url: str = "",
) -> dict[str, Any]:
    return {
        "suffix": suffix,
        "name_ru": name_ru,
        "name_en": name_en,
        "year": year,
        "city_ru": city_ru,
        "city_en": city_en,
        "history_ru": history_ru,
        "history_en": history_en,
        "significance_ru": significance_ru,
        "significance_en": significance_en,
        "commons_url": commons_url,
    }


STYLE_EXAMPLES: dict[str, list[dict[str, Any]]] = {
    "roman_germania": [
        _ex('porta_nigra', 'Порта Нигра', 'Porta Nigra', year='II в.', city_ru='Трир', city_en='Trier', history_ru='Римские городские ворота из песчаника.', history_en='Roman city gate in sandstone.', commons_url='https://upload.wikimedia.org/wikipedia/commons/9/93/Porta_Nigra_2013.jpg'),
        _ex('pantheon_trier', 'Константиновы термы', 'Aula Palatina', year='IV в.', city_ru='Трир', city_en='Trier', history_ru='Базилика Константина — зал имперской аудиенции.', history_en='Constantine basilica — imperial audience hall.', commons_url='https://upload.wikimedia.org/wikipedia/commons/1/1e/Aula_Palatina_Trier.jpg'),
        _ex('colonia_upc', 'Кёльнский собор (римские основания)', 'Cologne Cathedral site', year='IV в.', city_ru='Кёльн', city_en='Cologne', history_ru='Город римской Колонии Агриппины.', history_en='City of Roman Colonia Claudia Ara Agrippinensium.', commons_url='https://upload.wikimedia.org/wikipedia/commons/1/1b/K%C3%B6lner_Dom_mit_Rhein.jpg'),
        _ex('limes_gate', 'Саальбург', 'Saalburg Roman fort', year='II в.', city_ru='Бад-Хомбург', city_en='Bad Homburg', history_ru='Реконструированный римский форпост Лимеса.', history_en='Reconstructed Limes frontier fort.', commons_url=''),
    ],
    "romanesque": [
        _ex('speyer', 'Кафедральный собор Шпайера', 'Speyer Cathedral', year='1030–1106', city_ru='Шпайер', city_en='Speyer', history_ru='Имперский собор с подземной усыпальницей.', history_en='Imperial cathedral with crypt burials.', commons_url='https://upload.wikimedia.org/wikipedia/commons/4/4f/Speyer_Cathedral_in_Speyer.jpg'),
        _ex('mainz', 'Собор Майнца', 'Mainz Cathedral', year='XI–XIII вв.', city_ru='Майнц', city_en='Mainz', history_ru='Красный песчаник на берегу Рейна.', history_en='Red sandstone on the Rhine.', commons_url=''),
        _ex('worms', 'Собор Вормса', 'Worms Cathedral', year='XI–XIII вв.', city_ru='Вормс', city_en='Worms', history_ru='Один из трёх имперских кафедральных соборов Рейна.', history_en='One of three Rhenish imperial cathedrals.', commons_url=''),
        _ex('goslar', 'Дворцовая капелла Гослара', 'Goslar Imperial Chapel', year='XI в.', city_ru='Гослар', city_en='Goslar', history_ru='Капелла императорского дворца.', history_en='Chapel of the imperial palace.', commons_url=''),
    ],
    "gothic": [
        _ex('cologne', 'Кёльнский собор', 'Cologne Cathedral', year='1248–1880', city_ru='Кёльн', city_en='Cologne', history_ru='Двухбашенный собор с готическим шпилем.', history_en='Twin-towered cathedral with Gothic spire.', commons_url='https://upload.wikimedia.org/wikipedia/commons/1/1b/K%C3%B6lner_Dom_mit_Rhein.jpg'),
        _ex('ulm', 'Собор Ульма', 'Ulm Minster', year='1377–1890', city_ru='Ульм', city_en='Ulm', history_ru='Самый высокий церковный шпиль мира.', history_en="World's tallest church spire.", commons_url=''),
        _ex('marienkirche_lubeck', 'Мариенкирхе', "St. Mary's Lübeck", year='XIII–XIV вв.', city_ru='Любек', city_en='Lübeck', history_ru='Кирпичная базилика Ганзы.', history_en='Brick basilica of the Hanse.', commons_url=''),
        _ex('frauenkirche_munich', 'Фрауэнкирхе', 'Frauenkirche Munich', year='XV в.', city_ru='Мюнхен', city_en='Munich', history_ru='Купола-луковицы — символ Мюнхена.', history_en='Onion domes — symbol of Munich.', commons_url=''),
    ],
    "renaissance": [
        _ex('heidelberg', 'Гейдельбергский замок', 'Heidelberg Castle', year='XIII–XVII вв.', city_ru='Гейдельберг', city_en='Heidelberg', history_ru='Руины замка над Неккаром.', history_en='Castle ruins above the Neckar.', commons_url=''),
        _ex('landshut', 'Замок Траусниц', 'Trausnitz Castle', year='XIII–XVI вв.', city_ru='Ландсхут', city_en='Landshut', history_ru='Виттельсбахский резиденциальный замок.', history_en='Wittelsbach residential castle.', commons_url=''),
        _ex('augsburg', 'Ратуша Аугсбурга', 'Augsburg Town Hall', year='1615–1624', city_ru='Аугсбург', city_en='Augsburg', history_ru='Золотой зал эпохи Возрождения.', history_en='Golden Hall of the Renaissance.', commons_url=''),
        _ex('schloss_lichtenstein', 'Замок Лихтенштайн', 'Lichtenstein Castle', year='1840–1842', city_ru='Лихтенштайн', city_en='Lichtenstein', history_ru='Романтическая неоготическая вилла.', history_en='Romantic Neo-Gothic villa.', commons_url=''),
    ],
    "baroque": [
        _ex('wurzburg', 'Резиденция Вюрцбурга', 'Würzburg Residence', year='1720–1744', city_ru='Вюрцбург', city_en='Würzburg', history_ru='Дворец с фресками Тьеполо.', history_en='Palace with Tiepolo frescoes.', commons_url=''),
        _ex('sanssouci', 'Сан-Суси', 'Sanssouci', year='1745–1747', city_ru='Потсдам', city_en='Potsdam', history_ru='Летний дворец Фридриха Великого.', history_en="Frederick the Great's summer palace.", commons_url='https://upload.wikimedia.org/wikipedia/commons/5/5b/Sanssouci_Potsdam.jpg'),
        _ex('karlskirche', 'Карлскирхе', 'Karlskirche', year='1716–1737', city_ru='Вена', city_en='Vienna', history_ru='Купол и колонны римских триумфальных мотивов.', history_en='Dome with triumphal column motifs.', commons_url=''),
        _ex('schonbrunn', 'Шёнбрунн', 'Schönbrunn Palace', year='1696–1712', city_ru='Вена', city_en='Vienna', history_ru='Имперская резиденция Габсбургов.', history_en='Habsburg imperial residence.', commons_url=''),
    ],
    "rococo": [
        _ex('amalienburg', 'Амалиенбург', 'Amalienburg', year='1734–1739', city_ru='Мюнхен', city_en='Munich', history_ru='Охотничий павильон Нимфенбурга.', history_en='Hunting pavilion at Nymphenburg.', commons_url=''),
        _ex('wieskirche', 'Визкирхе', 'Wieskirche', year='1745–1754', city_ru='Штаинген', city_en='Steingaden', history_ru='Паломническая церковь в долине.', history_en='Pilgrimage church in the Alps.', commons_url=''),
        _ex('zwinger', 'Цвингер', 'Zwinger', year='1710–1728', city_ru='Дрезден', city_en='Dresden', history_ru='Барокко-рококо ансамбль двора.', history_en='Court baroque-rococo ensemble.', commons_url=''),
        _ex('residenz_munich', 'Мюнхенская резиденция', 'Munich Residenz', year='XVI–XVIII вв.', city_ru='Мюнхен', city_en='Munich', history_ru='Антиквариум и рокайльные залы.', history_en='Antiquarium and rocaille halls.', commons_url=''),
    ],
    "neoclassicism": [
        _ex('brandenburg_gate', 'Бранденбургские ворота', 'Brandenburg Gate', year='1788–1791', city_ru='Берлин', city_en='Berlin', history_ru='Неоклассические ворота с квадригой.', history_en='Neoclassical gate with quadriga.', commons_url='https://upload.wikimedia.org/wikipedia/commons/a/a6/Brandenburger_Tor_abends.jpg'),
        _ex('altes_museum', 'Альтес-музей', 'Altes Museum', year='1823–1830', city_ru='Берлин', city_en='Berlin', history_ru='Музей Шинкеля на острове.', history_en='Schinkel museum on Museum Island.', commons_url=''),
        _ex('walhalla', 'Вальхалла', 'Walhalla', year='1830–1842', city_ru='Донаустауф', city_en='Donaustauf', history_ru='Зал славы Людвига I.', history_en='Hall of fame by Ludwig I.', commons_url=''),
        _ex('konigsplatz', 'Кёнигсплац', 'Königsplatz Munich', year='1816–1862', city_ru='Мюнхен', city_en='Munich', history_ru='Античные храмы-музеи на площади.', history_en='Temple-museums on the square.', commons_url=''),
    ],
    "historicism": [
        _ex('neuschwanstein', 'Нойшванштайн', 'Neuschwanstein Castle', year='1869–1886', city_ru='Фюссен', city_en='Füssen', history_ru='Романтический замок Людвига II.', history_en="Ludwig II's romantic castle.", commons_url='https://upload.wikimedia.org/wikipedia/commons/b/b5/Schloss_Neuschwanstein_2013.jpg'),
        _ex('reichstag', 'Рейхстаг', 'Reichstag', year='1884–1894', city_ru='Берлин', city_en='Berlin', history_ru='Парламент с куполом Вармана.', history_en='Parliament with Norman Foster dome.', commons_url='https://upload.wikimedia.org/wikipedia/commons/7/7e/Reichstagsgeb%C3%A4ude_Berlin_Germany.jpg'),
        _ex('kolner_haus', 'Кёльнский вокзал', 'Cologne Central Station', year='1859', city_ru='Кёльн', city_en='Cologne', history_ru='Стеклянно-железный навес XIX века.', history_en='19th-century iron-and-glass train shed.', commons_url=''),
        _ex('semperoper', 'Земперопера', 'Semperoper', year='1878', city_ru='Дрезден', city_en='Dresden', history_ru='Опера в стиле итальянского Возрождения.', history_en='Opera in Italian Renaissance style.', commons_url=''),
    ],
    "art_nouveau": [
        _ex('hackesche_hofe', 'Хакеске-Хофе', 'Hackesche Höfe', year='1906–1907', city_ru='Берлин', city_en='Berlin', history_ru='Восстановленные арт-нуво дворы.', history_en='Restored Art Nouveau courtyards.', commons_url=''),
        _ex('sprudelhof', 'Шпрудельхоф', 'Sprudelhof', year='1905–1911', city_ru='Бад-Наугейм', city_en='Bad Nauheim', history_ru='Курортные виллы югендстиля.', history_en='Spa villas in Jugendstil.', commons_url=''),
        _ex('secession_vienna', 'Сецессион', 'Vienna Secession', year='1897–1898', city_ru='Вена', city_en='Vienna', history_ru='Золотой купол Ольбриха.', history_en="Olbrich's golden dome.", commons_url=''),
        _ex('hundertwasser', 'Дом Хундертвассера', 'Hundertwasserhaus', year='1983–1985', city_ru='Вена', city_en='Vienna', history_ru='Органическая жилая композиция.', history_en='Organic residential composition.', commons_url=''),
    ],
    "modernism": [
        _ex('aeg_turbine', 'Турбинный цех АЭГ', 'AEG Turbine Factory', year='1909', city_ru='Берлин', city_en='Berlin', history_ru='Стальной каркас Бехренса.', history_en='Behrens steel-frame factory.', commons_url=''),
        _ex('fagus', 'Фагус', 'Fagus Factory', year='1911–1925', city_ru='Альфельд', city_en='Alfeld', history_ru='Стеклянный угол Гропиуса.', history_en='Gropius glass corner.', commons_url=''),
        _ex('einstein_tower', 'Башня Эйнштейна', 'Einstein Tower', year='1919–1924', city_ru='Потсдам', city_en='Potsdam', history_ru='Экспрессионистская обсерватория.', history_en='Expressionist observatory.', commons_url=''),
        _ex('weissenhof', 'Вайсенхоф', 'Weissenhof Estate', year='1927', city_ru='Штутгарт', city_en='Stuttgart', history_ru='Выставка жилого модерна.', history_en='Housing exhibition of modernism.', commons_url=''),
    ],
    "bauhaus": [
        _ex('bauhaus_dessau', 'Здание Баухауса', 'Bauhaus Dessau', year='1925–1926', city_ru='Дессау', city_en='Dessau', history_ru='Стеклянный фасад Гропиуса.', history_en='Gropius glass workshop wing.', commons_url=''),
        _ex('masters_houses', 'Дома мастеров', "Masters' Houses", year='1925–1926', city_ru='Дессау', city_en='Dessau', history_ru='Жилые дома преподавателей.', history_en="Teachers' residential houses.", commons_url=''),
        _ex('falkenberg', 'Посёлок Фалькенберг', 'Törten Estate', year='1926–1928', city_ru='Дессау', city_en='Dessau', history_ru='Социальное жильё Баухауса.', history_en='Bauhaus social housing.', commons_url=''),
        _ex('unité_berlin', "Unité d'Habitation Berlin", 'Unité Berlin', year='1957–1958', city_ru='Берлин', city_en='Berlin', history_ru='Корбюзье в послевоенном Берлине.', history_en='Le Corbusier in post-war Berlin.', commons_url=''),
    ],
    "expressionism": [
        _ex('chilehaus', 'Чилехаус', 'Chilehaus', year='1922–1924', city_ru='Гамбург', city_en='Hamburg', history_ru='Кирпичный экспрессионистский офис.', history_en='Brick Expressionist office.', commons_url=''),
        _ex('ig_farben', 'Дом ИГ Фарбен', 'IG Farben Building', year='1928–1930', city_ru='Франкфурт', city_en='Frankfurt', history_ru='Модернистский корпоративный блок.', history_en='Modernist corporate block.', commons_url=''),
        _ex('goetheanum', 'Гётеанум', 'Goetheanum', year='1924–1928', city_ru='Дорнах', city_en='Dornach', history_ru='Деревянный центр антропософии.', history_en='Anthroposophy centre in concrete.', commons_url=''),
        _ex('lichtburg', 'Лихтбург', 'Lichtburg Essen', year='1928', city_ru='Эссен', city_en='Essen', history_ru='Кинотеатр-экспрессионистский зал.', history_en='Expressionist cinema hall.', commons_url=''),
    ],
    "nazi_monumental": [
        _ex('olympiastadion', 'Олимпийский стадион', 'Olympiastadion Berlin', year='1934–1936', city_ru='Берлин', city_en='Berlin', history_ru='Стадион Олимпиады 1936 года.', history_en='1936 Olympics stadium.', commons_url=''),
        _ex('reichsparteitag', 'Центр съездов', 'Congress Hall Nuremberg', year='1935–1937', city_ru='Нюрнберг', city_en='Nuremberg', history_ru='Незавершённый кольцевой зал.', history_en='Unfinished ring congress hall.', commons_url=''),
        _ex('prora', 'Прора', 'Prora', year='1936–1939', city_ru='Рюген', city_en='Rügen', history_ru='Курорт-комплекс Красной армии флота.', history_en='Seaside Strength Through Joy complex.', commons_url=''),
        _ex('tempelhof', 'Темпельхоф', 'Tempelhof Airport', year='1936–1941', city_ru='Берлин', city_en='Berlin', history_ru='Монументальный авиационный терминал.', history_en='Monumental airport terminal.', commons_url=''),
    ],
    "postwar_modern": [
        _ex('hansaviertel', 'Ганзавиртель', 'Hansaviertel', year='1957', city_ru='Берлин', city_en='Berlin', history_ru='Международная выставка жилья.', history_en='Interbau housing exhibition.', commons_url=''),
        _ex('berlin_phil', 'Берлинская филармония', 'Berlin Philharmonic', year='1960–1963', city_ru='Берлин', city_en='Berlin', history_ru='Золотая концертная зала Шаруне.', history_en="Scharoun's gold concert hall.", commons_url=''),
        _ex('fernsehturm', 'Телебашня', 'Berlin TV Tower', year='1965–1969', city_ru='Берлин', city_en='Berlin', history_ru='Символ ГДР на Александерплац.', history_en='GDR symbol on Alexanderplatz.', commons_url=''),
        _ex('krolloper_site', 'Культурфорум', 'Kulturforum', year='1960–1980', city_ru='Берлин', city_en='Berlin', history_ru='Музейный квартал Западного Берлина.', history_en='West Berlin museum quarter.', commons_url=''),
    ],
    "brutalism": [
        _ex('marienkirche_mod', 'Новая Национальная галерея', 'Neue Nationalgalerie', year='1965–1968', city_ru='Берлин', city_en='Berlin', history_ru='Сталь и стекло Миса ван дер Роэ.', history_en='Mies van der Rohe steel-and-glass pavilion.', commons_url=''),
        _ex('bielefeld_univ', 'Университет Билефельда', 'Bielefeld University', year='1969–1978', city_ru='Билефельд', city_en='Bielefeld', history_ru='Кампус на платформе.', history_en='Platform campus architecture.', commons_url=''),
        _ex('klinikum', 'Клиникум Ахена', 'Aachen University Hospital', year='1971–1985', city_ru='Ахен', city_en='Aachen', history_ru='Бетонный медицинский комплекс.', history_en='Concrete medical complex.', commons_url=''),
        _ex('rwe_tower', 'RWE Tower', 'RWE Tower Essen', year='1994–1996', city_ru='Эссен', city_en='Essen', history_ru='Высотный офис позднего модерна.', history_en='Late-modern office tower.', commons_url=''),
    ],
    "contemporary": [
        _ex('jewish_museum', 'Еврейский музей', 'Jewish Museum Berlin', year='1989–1999', city_ru='Берлин', city_en='Berlin', history_ru='Зигзаг Либескинда.', history_en='Libeskind zigzag plan.', commons_url=''),
        _ex('hauptbahnhof', 'Главный вокзал', 'Berlin Hauptbahnhof', year='2006', city_ru='Берлин', city_en='Berlin', history_ru='Стеклянный купол над пересечением.', history_en='Glass dome over crossing lines.', commons_url=''),
        _ex('elbphilharmonie', 'Эльбфилармония', 'Elbphilharmonie', year='2007–2016', city_ru='Гамбург', city_en='Hamburg', history_ru='Стеклянная волна на складе.', history_en='Glass wave on warehouse base.', commons_url=''),
        _ex('allianz_arena', 'Аллианц Арена', 'Allianz Arena', year='2002–2005', city_ru='Мюнхен', city_en='Munich', history_ru='Подушкообразный фасад стадиона.', history_en='Inflatable façade stadium.', commons_url=''),
    ],
}
