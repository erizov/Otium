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
    "roman_britain": [
        _ex('bath', 'Бани в Бате', 'Roman Baths Bath', year='I–IV вв.', city_ru='Бат', city_en='Bath', history_ru='Храм Сульис Минервы и термы.', history_en='Temple of Sulis Minerva and baths.', commons_url=''),
        _ex('hadrians_wall', 'Вал Адриана', "Hadrian's Wall", year='122–128', city_ru='Северная Англия', city_en='Northern England', history_ru='Пограничная линия римской обороны.', history_en='Roman frontier defence line.', commons_url=''),
        _ex('fishbourne', 'Фишборн', 'Fishbourne Roman Palace', year='I в.', city_ru='Фишборн', city_en='Fishbourne', history_ru='Крупнейший римский дворец Британии.', history_en="Britain's largest Roman palace.", commons_url=''),
        _ex('london_wall', 'Лондиниум', 'London Wall', year='II–III вв.', city_ru='Лондон', city_en='London', history_ru='Фрагменты римских укреплений.', history_en='Fragments of Roman fortifications.', commons_url=''),
    ],
    "norman": [
        _ex('durham', 'Собор Дарема', 'Durham Cathedral', year='1093–1133', city_ru='Дарем', city_en='Durham', history_ru='Своды и рибовые арки.', history_en='Vaults and ribbed arches.', commons_url=''),
        _ex('tower_london', 'Лондонский Тауэр', 'Tower of London', year='1078–', city_ru='Лондон', city_en='London', history_ru='Белая башня Вильгельма Завоевателя.', history_en="William the Conqueror's White Tower.", commons_url=''),
        _ex('ely', 'Собор Или', 'Ely Cathedral', year='1083–1375', city_ru='Или', city_en='Ely', history_ru='Октогон и западная башня.', history_en='Octagon and west tower.', commons_url=''),
        _ex('canterbury', 'Кентерберийский собор', 'Canterbury Cathedral', year='1070–', city_ru='Кентербери', city_en='Canterbury', history_ru='Место паломничества и убийства Бекета.', history_en='Pilgrimage site and Becket martyrdom.', commons_url=''),
    ],
    "english_gothic": [
        _ex('westminster', 'Вестминстерское аббатство', 'Westminster Abbey', year='1245–', city_ru='Лондон', city_en='London', history_ru='Коронации и похороны монархов.', history_en='Coronations and royal burials.', commons_url=''),
        _ex('salisbury', 'Солсберийский собор', 'Salisbury Cathedral', year='1220–1258', city_ru='Солсбери', city_en='Salisbury', history_ru='Самый высокий шпиль Британии.', history_en="Britain's tallest spire.", commons_url=''),
        _ex('york_minster', 'Йоркский минстер', 'York Minster', year='1220–1472', city_ru='Йорк', city_en='York', history_ru='Великое восточное окно.', history_en='Great East Window.', commons_url=''),
        _ex('kings_college', 'Капелла Кингс-колледжа', "King's College Chapel", year='1446–1515', city_ru='Кембридж', city_en='Cambridge', history_ru='Перпендикулярный фанерный свод.', history_en='Perpendicular fan vault.', commons_url=''),
    ],
    "tudor": [
        _ex('hampton_court', 'Хэмптон-корт', 'Hampton Court Palace', year='1514–', city_ru='Лондон', city_en='London', history_ru='Дворец Генриха VIII и Вильгельма III.', history_en='Palace of Henry VIII and William III.', commons_url=''),
        _ex('hardwick', 'Хардвик-холл', 'Hardwick Hall', year='1590–1597', city_ru='Дербишир', city_en='Derbyshire', history_ru='Стекло и камень Бесс Хардвик.', history_en="Bess of Hardwick's glass and stone.", commons_url=''),
        _ex('layer_marney', 'Лейер-Марни', 'Layer Marney Tower', year='1520–1523', city_ru='Эссекс', city_en='Essex', history_ru='Кирпичная воротная башня.', history_en='Brick gatehouse tower.', commons_url=''),
        _ex('little_moreton', 'Литл-Мортон', 'Little Moreton Hall', year='XV–XVI вв.', city_ru='Чешир', city_en='Cheshire', history_ru='Деревянный каркасный особняк.', history_en='Half-timbered manor house.', commons_url=''),
    ],
    "elizabethan_jacobean": [
        _ex('hatfield', 'Хатфилд-хаус', 'Hatfield House', year='1607–1612', city_ru='Хатфилд', city_en='Hatfield', history_ru='Яковианский дворец с садом.', history_en='Jacobean palace with gardens.', commons_url=''),
        _ex('audley_end', 'Одли-Энд', 'Audley End House', year='1605–1614', city_ru='Эссекс', city_en='Essex', history_ru='Парадный яковианский особняк.', history_en='Ceremonial Jacobean mansion.', commons_url=''),
        _ex('bolsover', 'Болсовер', 'Bolsover Castle', year='1612–1617', city_ru='Дербишир', city_en='Derbyshire', history_ru='Маленький романтический замок.', history_en='Small romantic castle.', commons_url=''),
        _ex('queens_house', 'Куинз-хаус', "Queen's House", year='1616–1635', city_ru='Лондон', city_en='London', history_ru='Первый классический дворец Англии.', history_en="England's first classical palace.", commons_url=''),
    ],
    "palladian_wren": [
        _ex('st_pauls', 'Собор Святого Павла', "St Paul's Cathedral", year='1675–1710', city_ru='Лондон', city_en='London', history_ru='Купол Кристофера Рена.', history_en="Christopher Wren's dome.", commons_url=''),
        _ex('royal_hospital', 'Королевский госпиталь', 'Royal Hospital Chelsea', year='1682–1692', city_ru='Лондон', city_en='London', history_ru='Кварталы пенсионеров Вренa.', history_en="Wren's Chelsea pensioners' quarters.", commons_url=''),
        _ex('chiswick', 'Чизик-хаус', 'Chiswick House', year='1726–1729', city_ru='Лондон', city_en='London', history_ru='Палладианская вилла Бurlington.', history_en="Burlington's Palladian villa.", commons_url=''),
        _ex('greenwich', 'Гринвич', 'Old Royal Naval College', year='1696–1712', city_ru='Лондон', city_en='London', history_ru='Барочно-классический ансамбль.', history_en='Baroque-classical riverside ensemble.', commons_url=''),
    ],
    "georgian": [
        _ex('bath_royal_crescent', 'Королевский полумесяц', 'Royal Crescent', year='1767–1775', city_ru='Бат', city_en='Bath', history_ru='Палладианская дуга террас.', history_en='Palladian arc of terraces.', commons_url=''),
        _ex('bath_circus', 'Цирк', 'The Circus Bath', year='1754–1768', city_ru='Бат', city_en='Bath', history_ru='Круговая площадь Вуда.', history_en="Wood's circular square.", commons_url=''),
        _ex('bedford_square', 'Бедфорд-сквер', 'Bedford Square', year='1775–1783', city_ru='Лондон', city_en='London', history_ru='Сохранённый георгианский квартал.', history_en='Intact Georgian square.', commons_url=''),
        _ex('holkham', 'Холкем-холл', 'Holkham Hall', year='1734–1764', city_ru='Норфолк', city_en='Norfolk', history_ru='Палладианский загородный дом.', history_en='Palladian country house.', commons_url=''),
    ],
    "regency": [
        _ex('brighton_pavilion', 'Королевский павильон', 'Royal Pavilion', year='1815–1822', city_ru='Брайтон', city_en='Brighton', history_ru='Индо-сарацинский дворец Георга IV.', history_en="George IV's Indo-Saracenic palace.", commons_url=''),
        _ex('regent_street', 'Риджент-стрит', 'Regent Street', year='1813–1823', city_ru='Лондон', city_en='London', history_ru='Кривая торговая ось Нэша.', history_en="Nash's curving shopping axis.", commons_url=''),
        _ex('park_crescent', 'Парк-кресент', 'Park Crescent', year='1812–1820', city_ru='Лондон', city_en='London', history_ru='Полукруглый классический фасад.', history_en='Semicircular classical façade.', commons_url=''),
        _ex('john_nash_terrace', 'Карлтон-хаус-террас', 'Carlton House Terrace', year='1827–1833', city_ru='Лондон', city_en='London', history_ru='Белокаменные неоклассические фасады.', history_en='White stucco Neoclassical fronts.', commons_url=''),
    ],
    "victorian": [
        _ex('palace_westminster', 'Вестминстерский дворец', 'Palace of Westminster', year='1840–1870', city_ru='Лондон', city_en='London', history_ru='Парламент Барри и Пьюджина.', history_en="Barry and Pugin's Parliament.", commons_url=''),
        _ex('st_pancras', 'Сент-Панкрас', 'St Pancras Station', year='1868', city_ru='Лондон', city_en='London', history_ru='Викторианский вокзал-неоготика.', history_en='Victorian Neo-Gothic terminus.', commons_url=''),
        _ex('albert_memorial', 'Мемориал Альберта', 'Albert Memorial', year='1872–1876', city_ru='Лондон', city_en='London', history_ru='Эклектический памятник в Кенсингтоне.', history_en='Eclectic memorial in Kensington.', commons_url=''),
        _ex('natural_history', 'Музей естествознания', 'Natural History Museum', year='1873–1881', city_ru='Лондон', city_en='London', history_ru='Романо-византийский фасад Уотерхауса.', history_en='Waterhouse Romanesque façade.', commons_url=''),
    ],
    "arts_crafts": [
        _ex('red_house', 'Красный дом', 'Red House', year='1859–1860', city_ru='Бекслихит', city_en='Bexleyheath', history_ru='Дом Морриса и Вебба.', history_en="Morris and Webb's house.", commons_url=''),
        _ex('wightwick', 'Уайтвик', 'Wightwick Manor', year='1887–1893', city_ru='Вулвергемптон', city_en='Wolverhampton', history_ru='Манер Морриса и Пре-Рафаэлитов.', history_en='Morris and Pre-Raphaelite interiors.', commons_url=''),
        _ex('blackwell', 'Блэквелл', 'Blackwell', year='1898–1900', city_ru='Уиндермир', city_en='Windermere', history_ru='Озёрный дом Бэквелла.', history_en='Baillie Scott lakeside house.', commons_url=''),
        _ex('standen', 'Стэнден', 'Standen House', year='1891–1894', city_ru='Вест-Суссекс', city_en='West Sussex', history_ru='Семейный дом Филиппа Уэбба.', history_en='Philip Webb family home.', commons_url=''),
    ],
    "edwardian": [
        _ex('lloyds_building_prec', 'Адмиралтейство', 'Admiralty Arch', year='1910', city_ru='Лондон', city_en='London', history_ru='Триумфальная арка к Молу.', history_en='Triumphal arch to The Mall.', commons_url=''),
        _ex('daily_express', 'Дели-экспресс', 'Daily Express Building', year='1932', city_ru='Лондон', city_en='London', history_ru='Ар-деко фасад Флит-стрит.', history_en='Fleet Street Art Deco façade.', commons_url=''),
        _ex('middlesbrough_town', 'Ратуша Мидлсбро', 'Middlesbrough Town Hall', year='1883–1889', city_ru='Мидлсбро', city_en='Middlesbrough', history_ru='Викторианско-эдвардианская ратуша.', history_en='Victorian-Edwardian town hall.', commons_url=''),
        _ex('lloyds_register', "Lloyd's Register", "Lloyd's Register London", year='1901', city_ru='Лондон', city_en='London', history_ru='Купольный офис на Фенчёрч-стрит.', history_en='Domed office on Fenchurch Street.', commons_url=''),
    ],
    "art_deco": [
        _ex('hoover', 'Здание Хувера', 'Hoover Building', year='1932–1938', city_ru='Лондон', city_en='London', history_ru='Белый фасад с зелёными деталями.', history_en='White façade with green trim.', commons_url=''),
        _ex('broadcasting_house', 'Broadcasting House', 'Broadcasting House', year='1932', city_ru='Лондон', city_en='London', history_ru='Штаб-квартира Би-би-си.', history_en='BBC headquarters.', commons_url=''),
        _ex('marine_court', 'Marine Court', 'Marine Court', year='1936–1938', city_ru='Сент-Леонардс', city_en='St Leonards', history_ru='Океанский лайнер в архитектуре.', history_en='Ocean-liner architecture.', commons_url=''),
        _ex('daily_telegraph', 'Daily Telegraph', 'Daily Telegraph Building', year='1928–1930', city_ru='Лондон', city_en='London', history_ru='Ар-деко на Флит-стрит.', history_en='Fleet Street Art Deco.', commons_url=''),
    ],
    "modernism": [
        _ex('highpoint', 'Хайпоинт', 'Highpoint I', year='1933–1935', city_ru='Лондон', city_en='London', history_ru='Жилой блок Любеткина.', history_en='Lubetkin apartment block.', commons_url=''),
        _ex('royal_festival', 'Фестиваль-холл', 'Royal Festival Hall', year='1948–1951', city_ru='Лондон', city_en='London', history_ru='Центр Фестиваля Британии.', history_en='Festival of Britain centrepiece.', commons_url=''),
        _ex('barbican', 'Барбикан', 'Barbican Estate', year='1965–1976', city_ru='Лондон', city_en='London', history_ru='Бруталистский жилой комплекс.', history_en='Brutalist residential complex.', commons_url=''),
        _ex('centre_point', 'Centre Point', 'Centre Point', year='1963–1966', city_ru='Лондон', city_en='London', history_ru='Офисная башня на Тоттенхэм-корт-роуд.', history_en='Office tower on Tottenham Court Road.', commons_url=''),
    ],
    "brutalism": [
        _ex('hayward', 'Хейуорд', 'Hayward Gallery', year='1968', city_ru='Лондон', city_en='London', history_ru='Бетонная галерея на Южном берегу.', history_en='Concrete gallery on South Bank.', commons_url=''),
        _ex('trellick', 'Треллик-тауэр', 'Trellick Tower', year='1968–1972', city_ru='Лондон', city_en='London', history_ru='Жилая башня Голдинга.', history_en='Goldfinger residential tower.', commons_url=''),
        _ex('national_theatre', 'Национальный театр', 'National Theatre', year='1967–1976', city_ru='Лондон', city_en='London', history_ru='Бетонные террасы Ласдунa.', history_en="Lasdun's concrete terraces.", commons_url=''),
        _ex('alexandra_road', 'Александра-роуд', 'Alexandra Road Estate', year='1972–1978', city_ru='Лондон', city_en='London', history_ru='Зигзагообразный жилой фасад.', history_en='Zigzag housing façade.', commons_url=''),
    ],
    "contemporary": [
        _ex('lloyd_whs', 'Ллойд-Билдинг', "Lloyd's building", year='1978–1986', city_ru='Лондон', city_en='London', history_ru='Хай-тек Роджерса.', history_en='Rogers High-Tech.', commons_url=''),
        _ex('gherkin', 'Свисс-Ре', '30 St Mary Axe', year='2001–2004', city_ru='Лондон', city_en='London', history_ru='Биоморфная башня Фостера.', history_en="Foster's biomorphic tower.", commons_url=''),
        _ex('tate_modern', 'Тейт Модерн', 'Tate Modern', year='1995–2000', city_ru='Лондон', city_en='London', history_ru='Бывшая электростанция Бэнксайда.', history_en='Former Bankside power station.', commons_url=''),
        _ex('shard', 'Шард', 'The Shard', year='2009–2012', city_ru='Лондон', city_en='London', history_ru='Стеклянный пик Лондон-Бридж.', history_en='Glass spike at London Bridge.', commons_url=''),
    ],
}
