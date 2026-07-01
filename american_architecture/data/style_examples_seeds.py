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
    "colonial_americas": [
        _ex('mission_san_antonio', 'Миссия Сан-Антонио', 'Mission San Antonio de Valero', year='1718–', city_ru='Сан-Антонио', city_en='San Antonio', history_ru='Испанская миссия Техаса.', history_en='Spanish mission in Texas.', commons_url=''),
        _ex('independence_hall', 'Индепенденс-холл', 'Independence Hall', year='1753', city_ru='Филадельфия', city_en='Philadelphia', history_ru='Место подписания Декларации.', history_en='Declaration signing site.', commons_url=''),
        _ex('santa_fe', 'Санта-Фе', 'San Miguel Chapel', year='1610–', city_ru='Санта-Фе', city_en='Santa Fe', history_ru='Старейшая церковь США.', history_en='Oldest church in the USA.', commons_url=''),
        _ex('castillo_san_marcos', 'Кастильо-де-Сан-Маркос', 'Castillo de San Marcos', year='1672–1695', city_ru='Сент-Огастин', city_en='St. Augustine', history_ru='Испанская крепость Флориды.', history_en='Spanish Florida fortress.', commons_url=''),
    ],
    "federal": [
        _ex('massachusetts_state', 'Капитолий Массачусетса', 'Massachusetts State House', year='1795–1798', city_ru='Бостон', city_en='Boston', history_ru='Золотой купол Булфинча.', history_en='Bulfinch golden dome.', commons_url=''),
        _ex('monticello', 'Монтиселло', 'Monticello', year='1768–1809', city_ru='Шарлоттсвилл', city_en='Charlottesville', history_ru='Дом Томаса Джефферсона.', history_en="Thomas Jefferson's house.", commons_url=''),
        _ex('us_capitol', 'Капитолий США', 'United States Capitol', year='1793–', city_ru='Вашингтон', city_en='Washington D.C.', history_ru='Купол и ротонда Конгресса.', history_en='Congress dome and rotunda.', commons_url=''),
        _ex('faneuil_hall', 'Фаньюил-холл', 'Faneuil Hall', year='1742–1763', city_ru='Бостон', city_en='Boston', history_ru='Колониально-федеральный рынок.', history_en='Colonial-Federal marketplace.', commons_url=''),
    ],
    "greek_revival": [
        _ex('parthenon_nashville', 'Парфенон Нэшвилла', 'Parthenon Nashville', year='1897', city_ru='Нэшвилл', city_en='Nashville', history_ru='Полномасштабная копия.', history_en='Full-scale replica.', commons_url=''),
        _ex('second_bank', 'Второй банк США', 'Second Bank of the US', year='1818–1824', city_ru='Филадельфия', city_en='Philadelphia', history_ru='Дорический портик Стрикланда.', history_en='Strickland Doric portico.', commons_url=''),
        _ex('custom_house_nyc', 'Таможня Нью-Йорка', 'U.S. Custom House New York', year='1899–1907', city_ru='Нью-Йорк', city_en='New York', history_ru='Неоклассика на Боулинг-Грин.', history_en='Neoclassical at Bowling Green.', commons_url=''),
        _ex('metropolitan_cathedral_mexico', 'Собор Мехико', 'Mexico City Metropolitan Cathedral', year='1573–1813', city_ru='Мехико', city_en='Mexico City', history_ru='Колониальный барокко-классицизм.', history_en='Colonial Baroque-Classicism.', commons_url=''),
    ],
    "gothic_revival": [
        _ex('st_patrick', 'Собор Святого Патрика', "St Patrick's Cathedral", year='1858–1878', city_ru='Нью-Йорк', city_en='New York', history_ru='Неоготический собор на Пятой авеню.', history_en='Neo-Gothic cathedral on Fifth Avenue.', commons_url=''),
        _ex('trinity_church', 'Троицкий собор', 'Trinity Church Boston', year='1872–1877', city_ru='Бостон', city_en='Boston', history_ru='Ричардсоновская неоготика.', history_en='Richardson Neo-Gothic.', commons_url=''),
        _ex('cathedral_st_john', 'Собор Святого Иоанна', 'Cathedral of St. John the Divine', year='1892–', city_ru='Нью-Йорк', city_en='New York', history_ru='Крупнейший собор мира (незавершён).', history_en="World's largest cathedral (unfinished).", commons_url=''),
        _ex('sao_paulo_cathedral', 'Собор Сан-Паулу', 'São Paulo Cathedral', year='1913–1967', city_ru='Сан-Паулу', city_en='São Paulo', history_ru='Неоготика Южной Америки.', history_en='South American Neo-Gothic.', commons_url=''),
    ],
    "victorian_americas": [
        _ex('breakers', 'Брейкерс', 'The Breakers', year='1893–1895', city_ru='Ньюпорт', city_en='Newport', history_ru='Вилла Вандербильтов.', history_en='Vanderbilt seaside villa.', commons_url=''),
        _ex('painted_ladies', 'Раскрашенные леди', 'Painted Ladies', year='1892–1896', city_ru='Сан-Франциско', city_en='San Francisco', history_ru='Викторианские дома на Элам-Парк.', history_en='Victorian houses at Alamo Square.', commons_url=''),
        _ex('biltmore', 'Билтмор', 'Biltmore Estate', year='1889–1895', city_ru='Эшвилл', city_en='Asheville', history_ru='Шато Ричарда Морриса Ханта.', history_en="Hunt's château.", commons_url=''),
        _ex('teatro_colon', 'Театр Колон', 'Teatro Colón', year='1908', city_ru='Буэнос-Айрес', city_en='Buenos Aires', history_ru='Оперный театр Южной Америки.', history_en="South America's opera house.", commons_url=''),
    ],
    "chicago_school": [
        _ex('wainwright', 'Вейнрайт-билдинг', 'Wainwright Building', year='1890–1891', city_ru='Сент-Луис', city_en='St. Louis', history_ru='Ранний небоскрёб Салливана.', history_en='Sullivan early skyscraper.', commons_url=''),
        _ex('home_insurance', 'Home Insurance Building', 'Home Insurance Building', year='1884–1885', city_ru='Чикаго', city_en='Chicago', history_ru='Первый каркасный небоскрёб.', history_en='First skeletal skyscraper.', commons_url=''),
        _ex('Monadnock', 'Монаднок-билдинг', 'Monadnock Building', year='1891–1893', city_ru='Чикаго', city_en='Chicago', history_ru='Кирпичный монолит Бёрнхэма.', history_en='Burnham brick monolith.', commons_url=''),
        _ex('flatiron', 'Флэтайрон', 'Flatiron Building', year='1902', city_ru='Нью-Йорк', city_en='New York', history_ru='Треугольный офисный клин.', history_en='Triangular office wedge.', commons_url=''),
    ],
    "beaux_arts": [
        _ex('grand_central', 'Гранд-Сентрал', 'Grand Central Terminal', year='1903–1913', city_ru='Нью-Йорк', city_en='New York', history_ru='Вокзал с созвездием на своде.', history_en='Terminal with celestial ceiling.', commons_url=''),
        _ex('nypl', 'Нью-Йоркская публичная библиотека', 'New York Public Library', year='1897–1911', city_ru='Нью-Йорк', city_en='New York', history_ru='Львиные ворота на Брайант-парк.', history_en='Lion-guarded entrance at Bryant Park.', commons_url=''),
        _ex('union_station_dc', 'Юнион-стейшн', 'Union Station Washington', year='1907–1908', city_ru='Вашингтон', city_en='Washington D.C.', history_ru='Монументальный вокзал столицы.', history_en='Monumental capital station.', commons_url=''),
        _ex('metropolitan_museum', 'Метрополитен-музей', 'Metropolitan Museum of Art', year='1874–', city_ru='Нью-Йорк', city_en='New York', history_ru='Фасад на Пятой авеню.', history_en='Fifth Avenue façade.', commons_url=''),
    ],
    "prairie_style": [
        _ex('robie_house', 'Дом Роби', 'Robie House', year='1909–1910', city_ru='Чикаго', city_en='Chicago', history_ru='Эталон прерийного стиля.', history_en='Canonical Prairie house.', commons_url=''),
        _ex('fallingwater', 'Дом над водопадом', 'Fallingwater', year='1936–1939', city_ru='Милл-Ран', city_en='Mill Run', history_ru='Дом Райта над ручьём.', history_en='Wright house over the stream.', commons_url=''),
        _ex('guggenheim', 'Гуггенхайм', 'Guggenheim Museum', year='1956–1959', city_ru='Нью-Йорк', city_en='New York', history_ru='Спиральный музей Райта.', history_en="Wright's spiral museum.", commons_url=''),
        _ex('unity_temple', 'Храм Юнити', 'Unity Temple', year='1905–1908', city_ru='Оук-Парк', city_en='Oak Park', history_ru='Бетонная церковь Райта.', history_en='Wright concrete church.', commons_url=''),
    ],
    "art_deco_americas": [
        _ex('chrysler', 'Крайслер-билдинг', 'Chrysler Building', year='1928–1930', city_ru='Нью-Йорк', city_en='New York', history_ru='Коронный шпиль ар-деко.', history_en='Art Deco crowned spire.', commons_url=''),
        _ex('empire_state', 'Эмпайр-стейт', 'Empire State Building', year='1930–1931', city_ru='Нью-Йорк', city_en='New York', history_ru='Символ межвоенного Манхэттена.', history_en='Interwar Manhattan symbol.', commons_url=''),
        _ex('rockefeller', 'Рокфеллер-центр', 'Rockefeller Center', year='1930–1939', city_ru='Нью-Йорк', city_en='New York', history_ru='Комплекс ар-деко площадей.', history_en='Art Deco plaza complex.', commons_url=''),
        _ex('kavanagh', 'Каванаг', 'Kavanagh Building', year='1934–1936', city_ru='Буэнос-Айрес', city_en='Buenos Aires', history_ru='Ар-деко Южной Америки.', history_en='South American Art Deco.', commons_url=''),
    ],
    "international_style": [
        _ex('seagram', 'Сигрэм-билдинг', 'Seagram Building', year='1954–1958', city_ru='Нью-Йорк', city_en='New York', history_ru='Бронзовый каркас Миса.', history_en='Mies bronze tower.', commons_url=''),
        _ex('lever_house', 'Lever House', 'Lever House', year='1950–1952', city_ru='Нью-Йорк', city_en='New York', history_ru='Стеклянный куб на Парк-авеню.', history_en='Glass cube on Park Avenue.', commons_url=''),
        _ex('pampulha', 'Капелла Пампулья', 'Church of Saint Francis', year='1940–1943', city_ru='Белу-Оризонти', city_en='Belo Horizonte', history_ru='Нимейер и Портинари.', history_en='Niemeyer and Portinari.', commons_url=''),
        _ex('un_hq', 'Штаб-квартира ООН', 'United Nations Headquarters', year='1949–1952', city_ru='Нью-Йорк', city_en='New York', history_ru='Международный модернизм.', history_en='International modernism.', commons_url=''),
    ],
    "midcentury_modern": [
        _ex('stahl_house', 'Дом Сталя', 'Stahl House', year='1959–1960', city_ru='Лос-Анджелес', city_en='Los Angeles', history_ru='Стеклянный павильон над Голливудом.', history_en='Glass pavilion above Hollywood.', commons_url=''),
        _ex('eames_house', 'Дом Эймса', 'Eames House', year='1949', city_ru='Лос-Анджелес', city_en='Los Angeles', history_ru='Стальной каркас Чарльза и Рэй.', history_en='Charles and Ray steel frame.', commons_url=''),
        _ex('salk', 'Институт Солка', 'Salk Institute', year='1959–1965', city_ru='Ла-Холья', city_en='La Jolla', history_ru='Бетон и океан Хана.', history_en='Kahn concrete and ocean.', commons_url=''),
        _ex('brasilia', 'Бразилиа', 'Cathedral of Brasília', year='1958–1970', city_ru='Бразилиа', city_en='Brasília', history_ru='Столица Нимейера.', history_en="Niemeyer's planned capital.", commons_url=''),
    ],
    "brutalism_americas": [
        _ex('boston_city_hall', 'Ратуша Бостона', 'Boston City Hall', year='1963–1968', city_ru='Бостон', city_en='Boston', history_ru='Бруталистский гражданский центр.', history_en='Brutalist civic centre.', commons_url=''),
        _ex('geisel_library', 'Библиотека Гайзеля', 'Geisel Library', year='1968–1970', city_ru='Сан-Диего', city_en='San Diego', history_ru='Бетонный куб Гинсберга.', history_en='Ginsberg concrete cube.', commons_url=''),
        _ex('habitat_67', 'Хабитат 67', 'Habitat 67', year='1967', city_ru='Монреаль', city_en='Montreal', history_ru='Модульное жильё Сафди.', history_en='Safdie modular housing.', commons_url=''),
        _ex('sesc_pompeia', 'SESC Pompéia', 'SESC Pompéia', year='1977–1986', city_ru='Сан-Паулу', city_en='São Paulo', history_ru='Адаптивное использование Лины Бо Барди.', history_en='Lina Bo Bardi adaptive reuse.', commons_url=''),
    ],
    "postmodern": [
        _ex('at_and_t', 'AT&T Building', '550 Madison Avenue', year='1978–1984', city_ru='Нью-Йорк', city_en='New York', history_ru='Фронтон Джонсона.', history_en="Johnson's Chippendale top.", commons_url=''),
        _ex('portland_building', 'Портленд-билдинг', 'Portland Building', year='1980–1982', city_ru='Портленд', city_en='Portland', history_ru='Цветной постмодерн Грейвза.', history_en='Graves colourful postmodern.', commons_url=''),
        _ex('piazza_italia', "Пьяцца д'Италия", "Piazza d'Italia", year='1975–1979', city_ru='Новый Орлеан', city_en='New Orleans', history_ru='Постмодерн Мурa.', history_en="Moore's postmodern square.", commons_url=''),
        _ex('world_financial', 'Puerto Madero', 'Puente de la Mujer', year='1998–2001', city_ru='Буэнос-Айрес', city_en='Buenos Aires', history_ru='Калатрава в доках.', history_en='Calatrava in the docks.', commons_url=''),
    ],
    "latin_colonial_baroque": [
        _ex('santo_domingo', 'Собор Санто-Доминго', 'Cathedral of Santo Domingo', year='1514–1541', city_ru='Санто-Доминго', city_en='Santo Domingo', history_ru='Старейший собор Америки.', history_en='Oldest cathedral in the Americas.', commons_url=''),
        _ex('quisquitania', 'Церковь Сан-Франсиско Кито', 'Church of San Francisco Quito', year='1534–1680', city_ru='Кито', city_en='Quito', history_ru='Барокко с золотым интерьером.', history_en='Baroque with gilded interior.', commons_url=''),
        _ex('santa_prisca', 'Санта-Приска', 'Santa Prisca Taxco', year='1751–1758', city_ru='Таско', city_en='Taxco', history_ru='Мексиканский чурригереско.', history_en='Mexican Churrigueresque.', commons_url=''),
        _ex('convento_sao_bento', 'Монастырь Сан-Бенту', 'Mosteiro de São Bento', year='1617–', city_ru='Рио-де-Жанейро', city_en='Rio de Janeiro', history_ru='Португальский барокко Бразилии.', history_en='Portuguese Baroque in Brazil.', commons_url=''),
    ],
    "latin_modernism": [
        _ex('torre_latinoamericana', 'Латиноамериканская башня', 'Torre Latinoamericana', year='1949–1956', city_ru='Мехико', city_en='Mexico City', history_ru='Стальной небоскрёб в центре Мехико, завершён в 1956.', history_en='Steel-frame tower in Mexico City, completed 1956.', commons_url=''),
        _ex('planalto', 'Дворец Планалту', 'Palácio do Planalto', year='1958–1960', city_ru='Бразилиа', city_en='Brasília', history_ru='Президентский дворец Нимейера.', history_en='Niemeyer presidential palace.', commons_url=''),
        _ex('unam_central', 'Городской кампус УНАМ', 'UNAM Central Campus', year='1949–1952', city_ru='Мехико', city_en='Mexico City', history_ru="Модернизм и муралы О'Гормана.", history_en="O'Gorman modernism and murals.", commons_url=''),
        _ex('mam', 'Музей современного искусства Рио', 'MAM Rio', year='1954–1955', city_ru='Рио-де-Жанейро', city_en='Rio de Janeiro', history_ru='Конкретный модерн Афонсу Рейди.', history_en='Reidy concrete modern.', commons_url=''),
    ],
    "contemporary_americas": [
        _ex('guggenheim_bilbao', 'Гуггенхайм Бильбао', 'Guggenheim Museum Bilbao', year='1991–1997', city_ru='Бильбао', city_en='Bilbao', history_ru='Титаноблоб Гери.', history_en='Gehry titanium curves.', commons_url=''),
        _ex('hearst_tower', 'Хёрст-тауэр', 'Hearst Tower', year='2003–2006', city_ru='Нью-Йорк', city_en='New York', history_ru='Диагональная сетка Фостера.', history_en='Foster diagrid tower.', commons_url=''),
        _ex('walt_disney', 'Концертный зал Диснея', 'Walt Disney Concert Hall', year='1999–2003', city_ru='Лос-Анджелес', city_en='Los Angeles', history_ru='Стальной Гери в даунтауне.', history_en='Gehry steel in downtown LA.', commons_url=''),
        _ex('museo_sumaya', 'Музей Сумайи', 'Museo Soumaya', year='2011', city_ru='Мехико', city_en='Mexico City', history_ru='Алюминиевый фасад в Плаза-Карсо.', history_en='Aluminium façade at Plaza Carso.', commons_url=''),
    ],
}
