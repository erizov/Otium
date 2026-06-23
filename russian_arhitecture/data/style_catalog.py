# -*- coding: utf-8 -*-
"""30 Russian architectural styles with 2–3 landmark examples each."""

from __future__ import annotations

from typing import Any

# category key -> (title_ru, title_en, style_intro_ru, style_intro_en)
STYLE_META: dict[str, tuple[str, str, str, str]] = {
    "ancient_rus": (
        "Древнерусское зодчество (X–XVII вв.)",
        "Early Rus architecture (10th–17th c.)",
        "Каменное зодчество Киевской Руси: крестово-купольные храмы, "
        "мозаики и фрески, компактные притворы и массивные стены.",
        "Stone architecture of Kyivan Rus: cross-in-square churches, "
        "mosaics and frescoes, compact narthexes and thick walls.",
    ),
    "novgorod_school": (
        "Новгородская школа (XII–XV вв.)",
        "Novgorod school (12th–15th c.)",
        "Своеобразие новгородских храмов — пониженные купола, "
        "асимметричные фасады и декоративная кирпичная кладка.",
        "Novgorod churches: low domes, asymmetrical façades, "
        "and ornamental brickwork.",
    ),
    "pskov_school": (
        "Псковская школа (XIV–XVI вв.)",
        "Pskov school (14th–16th c.)",
        "Псковские мастера сочетали лаконичные объёмы с "
        "колокольнями-«восьмёрками» и звонницами у стен.",
        "Pskov masters combined compact volumes with "
        "octagonal belfries and wall bell towers.",
    ),
    "moscow_fifteenth_sixteenth": (
        "Московское зодчество (XV–XVI вв.)",
        "Muscovite architecture (15th–16th c.)",
        "Кремлёвские соборы объединяют итальянские мотивы "
        "порталов с русской традицией купольных композиций.",
        "Kremlin cathedrals blend Italian portal motifs with "
        "Russian dome compositions.",
    ),
    "tent_roof": (
        "Шатровый стиль (XVI в.)",
        "Tent-roof style (16th c.)",
        "Шатровые храмы без внутренних опор — эксперимент "
        "московского зодчества эпохи Ивана Грозного.",
        "Tent-roof churches without internal pillars — a "
        "Muscovite experiment of Ivan the Terrible's era.",
    ),
    "uzorochye": (
        "Русское узорочье (XVII в.)",
        "Muscovite ornamental style (17th c.)",
        "Пышный декор из кокошников, поясков и наличников "
        "в эпоху Смуты и первых Романовых.",
        "Rich kokoshniks, cornices and carved window surrounds "
        "in the Time of Troubles and early Romanov era.",
    ),
    "naryshkin_baroque": (
        "Нарышкинское барокко (конец XVII в.)",
        "Naryshkin Baroque (late 17th c.)",
        "Московское «барокко под куполом»: вертикальные ряды "
        "кокошников и белокаменная резьба.",
        "Moscow 'baroque under the dome': vertical kokoshnik "
        "tiers and white-stone carving.",
    ),
    "petrine_baroque": (
        "Петровское барокко (начало XVIII в.)",
        "Petrine Baroque (early 18th c.)",
        "Первые петербургские ансамбли северного барокко "
        "и рациональная сетка «регулярного города».",
        "Early Petersburg ensembles of Northern Baroque and "
        "the rational grid of the planned capital.",
    ),
    "elizabethan_baroque": (
        "Елизаветинское барокко (середина XVIII в.)",
        "Elizabethan Baroque (mid-18th c.)",
        "Роскошь дворцов Растрелли: изогнутые фасады, золото "
        "и праздничная пластика стен.",
        "Rastrelli's palace luxury: curved façades, gilding "
        "and festive wall plasticity.",
    ),
    "early_classicism": (
        "Ранний классицизм (вторая половина XVIII в.)",
        "Early Neoclassicism (late 18th c.)",
        "Античные ордера и строгая симметрия в академической "
        "архитектуре Екатерининской эпохи.",
        "Antique orders and strict symmetry in Catherine-era "
        "academic architecture.",
    ),
    "mature_classicism": (
        "Зрелый русский классицизм (конец XVIII — начало XIX вв.)",
        "Mature Russian Neoclassicism (late 18th–early 19th c.)",
        "Монументальные ансамбли столицы: адмиралтейская стрела, "
        "дворцы и соборы-ротонды.",
        "Monumental capital ensembles: Admiralty spire, palaces "
        "and rotunda cathedrals.",
    ),
    "empire": (
        "Ампир (первая треть XIX в.)",
        "Empire style (first third of the 19th c.)",
        "Торжественность империи: колоннады, триумфальные мотивы "
        "и парадная градостроительная ось.",
        "Imperial grandeur: colonnades, triumphal motifs and "
        "ceremonial urban axes.",
    ),
    "russo_byzantine": (
        "Русско-византийский стиль (середина XIX в.)",
        "Russo-Byzantine style (mid-19th c.)",
        "Константин Тон соединил византийские формы с "
        "государственным символизмом православной империи.",
        "Konstantin Thon merged Byzantine forms with the "
        "state symbolism of Orthodox empire.",
    ),
    "eclecticism": (
        "Эклектика (вторая половина XIX в.)",
        "Eclecticism (late 19th c.)",
        "Свободное смешение исторических стилей в музеях, "
        "вокзалах и городских особняках.",
        "Free mixing of historical styles in museums, stations "
        "and urban mansions.",
    ),
    "pseudo_russian": (
        "Псевдорусский стиль (вторая половина XIX в.)",
        "Pseudo-Russian style (late 19th c.)",
        "Романтическое обращение к допетровской традиции "
        "в торговых и общественных зданиях.",
        "Romantic revival of pre-Petrine tradition in "
        "commercial and public buildings.",
    ),
    "neo_russian": (
        "Неорусский стиль (рубеж XIX–XX вв.)",
        "Neo-Russian style (turn of the 20th c.)",
        "Национальный модерн: сказочные мотивы, майолика "
        "и выразительные силуэты вокзалов и галерей.",
        "National Art Nouveau: fairy-tale motifs, majolica "
        "and expressive silhouettes of stations and galleries.",
    ),
    "art_nouveau": (
        "Модерн (ар-нуво, рубеж XIX–XX вв.)",
        "Art Nouveau (turn of the 20th c.)",
        "Плавные линии, растительный орнамент и новые "
        "конструктивные материалы в городской среде.",
        "Flowing lines, plant ornament and new structural "
        "materials in the urban fabric.",
    ),
    "neoclassicism_early20": (
        "Неоклассицизм (начало XX в.)",
        "Neoclassicism (early 20th c.)",
        "Возврат к античным формам в банках, вокзалах "
        "и доходных домах Серебряного века.",
        "Return to antique forms in banks, stations and "
        "Silver Age apartment buildings.",
    ),
    "avant_garde": (
        "Авангард / конструктивизм (1920–1930‑е гг.)",
        "Avant-garde / Constructivism (1920s–1930s)",
        "Функция и конструкция: стекло и бетон, эксперимент "
        "жилья и общественных клубов.",
        "Function and structure: glass and concrete, housing "
        "and workers' club experiments.",
    ),
    "stalinist": (
        "Сталинская архитектура / «сталинский ампир» (1930–1950‑е)",
        "Stalinist architecture (1930s–1950s)",
        "Монументальные высотки, парадные магистрали "
        "и торжественное оформление метро.",
        "Monumental skyscrapers, parade avenues and "
        "ceremonial metro interiors.",
    ),
    "panel_housing": (
        "Типовое индустриальное домостроение (1950–1980‑е)",
        "Industrial panel housing (1950s–1980s)",
        "Серийные панельные дома и микрорайоны массовой "
        "застройки хрущёвско-брежневской эпохи.",
        "Serial panel blocks and mass housing micro-districts "
        "of the Khrushchev–Brezhnev era.",
    ),
    "soviet_modernism": (
        "Советский модернизм (1960–1980‑е гг.)",
        "Soviet modernism (1960s–1980s)",
        "Лаконичные объёмы, инженерные конструкции "
        "и функциональные дворцы культуры.",
        "Concise volumes, engineering structures and "
        "functional palaces of culture.",
    ),
    "stalinist_neoclassicism": (
        "Сталинский неоклассицизм (1930–1950‑е гг.)",
        "Stalinist Neoclassicism (1930s–1950s)",
        "Классические ордера в советском гражданском здании: "
        "отели, ведомства и жилые дома на проспектах.",
        "Classical orders in Soviet civic buildings: hotels, "
        "ministries and avenue apartment houses.",
    ),
    "art_deco": (
        "Ар-деко (1920–1930‑е гг.)",
        "Art Deco (1920s–1930s)",
        "Геометрический декор и парадная представительность "
        "в театрах и кинотеатрах.",
        "Geometric décor and ceremonial representation "
        "in theaters and cinemas.",
    ),
    "post_constructivism": (
        "Постконструктивизм (1930‑е гг.)",
        "Post-constructivism (1930s)",
        "Переход от авангарда к неоклассике: строгие фасады "
        "с элементами конструктивизма.",
        "Transition from avant-garde to neoclassicism: "
        "austere façades with constructivist traces.",
    ),
    "regional_soviet": (
        "Региональное советское зодчество (1960–1980‑е)",
        "Regional Soviet architecture (1960s–1980s)",
        "Крупные спортивные и культурные комплексы "
        "в региональных центрах СССР.",
        "Large sports and cultural complexes in Soviet "
        "regional capitals.",
    ),
    "brutalism": (
        "Брутализм (1960–1970‑е гг.)",
        "Brutalism (1960s–1970s)",
        "Открытый бетон, массивные консоли и выразительная "
        "конструкция общественных зданий.",
        "Exposed concrete, massive cantilevers and expressive "
        "structure in public buildings.",
    ),
    "soviet_neoclassicism_revival": (
        "Советский неоклассицизм (возрождение, 1940–1950‑е)",
        "Soviet neoclassicism revival (1940s–1950s)",
        "Послевоенное восстановление исторических ансамблей "
        "и парадная реконструкция магистралей.",
        "Post-war restoration of historic ensembles and "
        "ceremonial reconstruction of avenues.",
    ),
    "postmodernism": (
        "Постмодернизм (конец 1980‑х — 2000‑е)",
        "Postmodernism (late 1980s–2000s)",
        "Ироничное цитирование исторических форм "
        "в общественных и коммерческих проектах.",
        "Ironic quotation of historical forms in public "
        "and commercial projects.",
    ),
    "contemporary": (
        "Современный российский стиль (2000‑е — н. в.)",
        "Contemporary Russian architecture (2000s–present)",
        "Международные стеклянные башни, набережные "
        "и ландшафтные общественные пространства.",
        "International glass towers, embankments and "
        "landscape public realms.",
    ),
}


def _ex(
    suffix: str,
    name_ru: str,
    name_en: str,
    *,
    architect_ru: str = "",
    architect_en: str = "",
    year: str = "",
    city_ru: str = "",
    city_en: str = "",
    history_ru: str = "",
    history_en: str = "",
    significance_ru: str = "",
    significance_en: str = "",
    reuse_from: str = "",
    commons_url: str = "",
) -> dict[str, Any]:
    return {
        "suffix": suffix,
        "name_ru": name_ru,
        "name_en": name_en,
        "architect_ru": architect_ru,
        "architect_en": architect_en,
        "year": year,
        "city_ru": city_ru,
        "city_en": city_en,
        "history_ru": history_ru,
        "history_en": history_en,
        "significance_ru": significance_ru,
        "significance_en": significance_en,
        "reuse_from": reuse_from,
        "commons_url": commons_url,
    }


STYLE_EXAMPLES: dict[str, list[dict[str, Any]]] = {
    "ancient_rus": [
        _ex(
            "kyiv_sophia",
            "Софийский собор в Киеве",
            "Saint Sophia Cathedral, Kyiv",
            year="1037",
            city_ru="Киев",
            city_en="Kyiv",
            history_ru=(
                "Заложен при Ярославе Мудром; сохранил уникальные "
                "мозаики и фрески XI века."
            ),
            history_en=(
                "Founded under Yaroslav the Wise; preserves unique "
                "11th-century mosaics and frescoes."
            ),
            significance_ru="Образец византийского влияния на зодчество Киевской Руси.",
            significance_en="A model of Byzantine influence on Kyivan Rus architecture.",
            reuse_from="kyiv/images/kyiv_saint_sophia.jpg",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "f/fd/Saint_Sophia%27s_Cathedral%2C_Kyiv.jpg"
            ),
        ),
        _ex(
            "vladimir_assumption",
            "Успенский собор во Владимире",
            "Dormition Cathedral, Vladimir",
            year="1158–1160",
            city_ru="Владимир",
            city_en="Vladimir",
            history_ru="Построен Андреем Боголюбским; фрески Андрея Рублева.",
            history_en="Built by Andrey Bogolyubsky; home to frescoes by Andrei Rublev.",
            significance_ru="Вершина белокаменного зодчества Владимиро-Суздальской Руси.",
            significance_en="Peak of white-stone architecture in Vladimir-Suzdal Rus.",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "4/4b/Vladimir_Cathedral.jpg"
            ),
        ),
        _ex(
            "nerl_church",
            "Церковь Покрова на Нерли",
            "Church of the Intercession on the Nerl",
            year="1165",
            city_ru="Боголюбово",
            city_en="Bogolyubovo",
            history_ru="Один из самых изящных храмов домонгольской Руси.",
            history_en="One of the most graceful churches of pre-Mongol Rus.",
            significance_ru="Символ гармонии архитектуры и пейзажа.",
            significance_en="A symbol of harmony between architecture and landscape.",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "8/8a/Church_of_the_Intercession_on_the_Nerl.jpg"
            ),
        ),
    ],
    "novgorod_school": [
        _ex(
            "transfiguration_ilyina",
            "Церковь Спаса Преображения на Ильине",
            "Church of the Transfiguration on Ilyina Street",
            year="1374",
            city_ru="Великий Новгород",
            city_en="Veliky Novgorod",
            history_ru="Знаменита фресками Феофана Грека.",
            history_en="Famous for frescoes by Theophanes the Greek.",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "9/9e/Novgorod_Church_of_Transfiguration_on_Ilyina_Street.jpg"
            ),
        ),
        _ex(
            "theodore_stratilat",
            "Церковь Фёдора Стратилата на Ручью",
            "Church of Theodore Stratelates on the Brook",
            year="1360-е",
            city_ru="Великий Новгород",
            city_en="Veliky Novgorod",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "2/2e/Novgorod_Fedorovskaya_church.jpg"
            ),
        ),
        _ex(
            "novgorod_kremlin",
            "Новгородский кремль (детинец)",
            "Novgorod Kremlin (Detinets)",
            year="XI–XV вв.",
            city_ru="Великий Новгород",
            city_en="Veliky Novgorod",
            history_ru="Включает Софийский собор — духовный центр республики.",
            history_en="Includes St Sophia Cathedral, spiritual heart of the republic.",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "5/5a/Novgorod_Kremlin.jpg"
            ),
        ),
    ],
    "pskov_school": [
        _ex(
            "pskov_kremlin",
            "Псковский кремль",
            "Pskov Kremlin",
            year="XIV–XV вв.",
            city_ru="Псков",
            city_en="Pskov",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "6/6e/Pskov_kremlin.jpg"
            ),
        ),
        _ex(
            "vasily_gorka",
            "Церковь Василия на Горке",
            "Church of St Basil on the Hill",
            year="XV в.",
            city_ru="Псков",
            city_en="Pskov",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "1/1e/Pskov_Vasily_on_Gorka.jpg"
            ),
        ),
        _ex(
            "epiphany_zapskovye",
            "Церковь Богоявления с Запсковья",
            "Epiphany Church from Zapskovye",
            year="XV в.",
            city_ru="Псков",
            city_en="Pskov",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "7/7a/Pskov_Epiphany_Church.jpg"
            ),
        ),
    ],
    "moscow_fifteenth_sixteenth": [
        _ex(
            "kremlin_dormition",
            "Успенский собор Московского Кремля",
            "Dormition Cathedral of the Moscow Kremlin",
            architect_ru="Аристотель Фиораванти",
            architect_en="Aristotele Fioravanti",
            year="1479",
            city_ru="Москва",
            city_en="Moscow",
            reuse_from=(
                "moscow/images/moscow_places_of_worship/"
                "uspensky_kremlin_1.jpg"
            ),
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "8/8d/Cathedral_of_the_Dormition_in_the_Moscow_Kremlin.jpg"
            ),
        ),
        _ex(
            "kremlin_archangel",
            "Архангельский собор Московского Кремля",
            "Archangel Cathedral of the Moscow Kremlin",
            architect_ru="Алевиз Новый",
            architect_en="Aloisio the New",
            year="1508",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "4/4e/Moscow_Arkangelsky_Cathedral.jpg"
            ),
        ),
        _ex(
            "ivan_bell_tower",
            "Колокольня Ивана Великого",
            "Ivan the Great Bell Tower",
            architect_ru="Бон Фрязин",
            architect_en="Bon Fryazin",
            year="1508",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "f/f5/Ivan_the_Great_Bell_Tower.jpg"
            ),
        ),
    ],
    "tent_roof": [
        _ex(
            "ascension_kolomenskoye",
            "Церковь Вознесения в Коломенском",
            "Church of the Ascension in Kolomenskoye",
            year="1532",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "5/5c/Church_of_the_Ascension_in_Kolomenskoye.jpg"
            ),
        ),
        _ex(
            "st_basil",
            "Храм Василия Блаженного",
            "Saint Basil's Cathedral",
            architect_ru="Барма и Постник",
            architect_en="Barma and Postnik",
            year="1561",
            city_ru="Москва",
            city_en="Moscow",
            reuse_from="moscow/images/moscow_places_of_worship/st_basil_1.jpg",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "6/60/St_Basil%27s_Cathedral_Moscow_2006.jpg"
            ),
        ),
        _ex(
            "transfiguration_ostro",
            "Церковь Преображения в селе Остров",
            "Church of the Transfiguration, Ostrov village",
            year="XVI в.",
            city_ru="Московская область",
            city_en="Moscow region",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "9/9a/Ostrov_Church_of_Transfiguration.jpg"
            ),
        ),
    ],
    "uzorochye": [
        _ex(
            "trinity_nikitniki",
            "Церковь Троицы в Никитниках",
            "Church of the Trinity in Nikitniki",
            year="XVII в.",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "3/3e/Moscow_Nikitniki_Church.jpg"
            ),
        ),
        _ex(
            "nativity_putinki",
            "Церковь Рождества Богородицы в Путинках",
            "Church of the Nativity of the Theotokos in Putinki",
            year="1652",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "8/8f/Putinki_Church_Moscow.jpg"
            ),
        ),
        _ex(
            "terem_palace",
            "Теремной дворец Московского Кремля",
            "Terem Palace of the Moscow Kremlin",
            year="1635–1636",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "2/2e/Terem_Palace_Moscow.jpg"
            ),
        ),
    ],
    "naryshkin_baroque": [
        _ex(
            "intercession_fili",
            "Церковь Покрова в Филях",
            "Church of the Intercession in Fili",
            year="1693",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "4/4e/Church_of_the_Intercession_at_Fili.jpg"
            ),
        ),
        _ex(
            "trinity_lykovo",
            "Церковь Троицы в Троице-Лыкове",
            "Trinity Church in Troitse-Lykovo",
            year="1698–1703",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "1/1a/Troitse-Lykovo_Church.jpg"
            ),
        ),
        _ex(
            "boris_gleb_zyuzino",
            "Церковь Бориса и Глеба в Зюзино",
            "Church of Boris and Gleb in Zyuzino",
            year="1688–1704",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "5/5e/Zyuzino_Church.jpg"
            ),
        ),
    ],
    "petrine_baroque": [
        _ex(
            "peter_paul_cathedral",
            "Петропавловский собор",
            "Peter and Paul Cathedral",
            architect_ru="Доменико Трезини",
            architect_en="Domenico Trezzini",
            year="1712–1733",
            city_ru="Санкт-Петербург",
            city_en="Saint Petersburg",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "5/5e/Peter_and_Paul_Cathedral_in_Saint_Petersburg.jpg"
            ),
        ),
        _ex(
            "twelve_collegia",
            "Здание Двенадцати коллегий",
            "Twelve Collegia building",
            architect_ru="Доменико Трезини",
            architect_en="Domenico Trezzini",
            year="1722–1742",
            city_ru="Санкт-Петербург",
            city_en="Saint Petersburg",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "8/8e/Twelve_Collegia_Building.jpg"
            ),
        ),
        _ex(
            "summer_palace",
            "Летний дворец Петра I",
            "Summer Palace of Peter the Great",
            architect_ru="Доменико Трезини",
            architect_en="Domenico Trezzini",
            year="1710–1714",
            city_ru="Санкт-Петербург",
            city_en="Saint Petersburg",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "6/6e/Summer_Palace_of_Peter_the_Great.jpg"
            ),
        ),
    ],
    "elizabethan_baroque": [
        _ex(
            "winter_palace",
            "Зимний дворец",
            "Winter Palace",
            architect_ru="Бартоломео Растрелли",
            architect_en="Bartolomeo Rastrelli",
            year="1754–1762",
            city_ru="Санкт-Петербург",
            city_en="Saint Petersburg",
            reuse_from="spb/images/palaces/spb_winter_palace.jpg",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "7/74/RUS-2016-Aerial-SPB-Winter_Palace_%28crop%29.jpg"
            ),
        ),
        _ex(
            "catherine_palace",
            "Большой Екатерининский дворец",
            "Catherine Palace",
            architect_ru="Бартоломео Растрелли",
            architect_en="Bartolomeo Rastrelli",
            year="1752–1756",
            city_ru="Пушкин",
            city_en="Pushkin",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "6/6e/Catherine_Palace_in_Tsarskoe_Selo.jpg"
            ),
        ),
        _ex(
            "smolny_cathedral",
            "Смольный собор",
            "Smolny Cathedral",
            architect_ru="Бартоломео Растрелли",
            architect_en="Bartolomeo Rastrelli",
            year="1748–1764",
            city_ru="Санкт-Петербург",
            city_en="Saint Petersburg",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "e/e3/Smolny_2013_1.jpg"
            ),
        ),
    ],
    "early_classicism": [
        _ex(
            "academy_of_arts",
            "Академия художеств",
            "Imperial Academy of Arts",
            architect_ru="Жан-Батист Валлен-Деламот, Александр Кокоринов",
            architect_en="Jean-Baptiste Vallin de la Mothe, Alexander Kokorinov",
            year="1764–1788",
            city_ru="Санкт-Петербург",
            city_en="Saint Petersburg",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "4/4e/Russian_Academy_of_Arts_building.jpg"
            ),
        ),
        _ex(
            "marble_palace",
            "Мраморный дворец",
            "Marble Palace",
            architect_ru="Антонио Ринальди",
            architect_en="Antonio Rinaldi",
            year="1768–1785",
            city_ru="Санкт-Петербург",
            city_en="Saint Petersburg",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "8/8e/Marble_Palace_SPB.jpg"
            ),
        ),
        _ex(
            "pashkov_house",
            "Дом Пашкова",
            "Pashkov House",
            architect_ru="Василий Баженов",
            architect_en="Vasily Bazhenov",
            year="1784–1786",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "5/5e/Pashkov_house.jpg"
            ),
        ),
    ],
    "mature_classicism": [
        _ex(
            "tauride_palace",
            "Таврический дворец",
            "Tauride Palace",
            architect_ru="Иван Старов",
            architect_en="Ivan Starov",
            year="1783–1789",
            city_ru="Санкт-Петербург",
            city_en="Saint Petersburg",
            reuse_from="spb/images/palaces/spb_tauride_palace.jpg",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "2/2e/Tauride_Palace.jpg"
            ),
        ),
        _ex(
            "admiralty",
            "Главное Адмиралтейство",
            "Admiralty building",
            architect_ru="Андрей Захаров",
            architect_en="Andreyan Zakharov",
            year="1806–1823",
            city_ru="Санкт-Петербург",
            city_en="Saint Petersburg",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "9/9e/Admiralty_SPB.jpg"
            ),
        ),
        _ex(
            "kazan_cathedral_spb",
            "Казанский собор",
            "Kazan Cathedral",
            architect_ru="Андрей Воронихин",
            architect_en="Andrey Voronikhin",
            year="1801–1811",
            city_ru="Санкт-Петербург",
            city_en="Saint Petersburg",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "f/f1/Kazan_Cathedral_SPB.jpg"
            ),
        ),
    ],
    "empire": [
        _ex(
            "triumphal_gate_moscow",
            "Триумфальные ворота",
            "Triumphal Arch",
            architect_ru="Осип Бове",
            architect_en="Osip Bove",
            year="1829–1834",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "4/4e/Triumphal_Arch_of_Moscow.jpg"
            ),
        ),
        _ex(
            "isaac_cathedral",
            "Исаакиевский собор",
            "Saint Isaac's Cathedral",
            architect_ru="Огюст Монферран",
            architect_en="Auguste de Montferrand",
            year="1818–1858",
            city_ru="Санкт-Петербург",
            city_en="Saint Petersburg",
            reuse_from="spb/images/places_of_worship/spb_isaac_cathedral.jpg",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "8/83/Saint_Isaac%27s_Cathedral_in_SPB.jpeg"
            ),
        ),
        _ex(
            "stock_exchange",
            "Здание Биржи",
            "Old Stock Exchange",
            architect_ru="Жан Тома де Томон",
            architect_en="Jean-Thomas de Thomon",
            year="1805–1816",
            city_ru="Санкт-Петербург",
            city_en="Saint Petersburg",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "6/6e/Old_Stock_Exchange_Building_SPB.jpg"
            ),
        ),
    ],
    "russo_byzantine": [
        _ex(
            "christ_savior",
            "Храм Христа Спасителя",
            "Cathedral of Christ the Saviour",
            architect_ru="Константин Тон",
            architect_en="Konstantin Thon",
            year="1839–1883",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "5/5e/Cathedral_of_Christ_the_Saviour.jpg"
            ),
        ),
        _ex(
            "grand_kremlin_palace",
            "Большой Кремлёвский дворец",
            "Grand Kremlin Palace",
            architect_ru="Константин Тон",
            architect_en="Konstantin Thon",
            year="1838–1849",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "4/4e/Grand_Kremlin_Palace.jpg"
            ),
        ),
        _ex(
            "armoury",
            "Оружейная палата",
            "Armoury Chamber",
            architect_ru="Константин Тон",
            architect_en="Konstantin Thon",
            year="1844–1851",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "8/8e/Armoury_Chamber_Moscow.jpg"
            ),
        ),
    ],
    "eclecticism": [
        _ex(
            "historical_museum",
            "Исторический музей",
            "State Historical Museum",
            architect_ru="Владимир Шервуд, Анатолий Семёнов",
            architect_en="Vladimir Sherwood, Anatoly Semenov",
            year="1875–1883",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "6/6e/State_Historical_Museum_Moscow.jpg"
            ),
        ),
        _ex(
            "igumnov_house",
            "Дом Игумнова",
            "Igumnov House",
            architect_ru="Николай Поздеев",
            architect_en="Nikolay Pozdeyev",
            year="1888–1895",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "3/3e/Igumnov_House.jpg"
            ),
        ),
        _ex(
            "polytechnic_museum",
            "Политехнический музей",
            "Polytechnic Museum",
            year="1872–1877",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "5/5e/Polytechnical_Museum_Moscow.jpg"
            ),
        ),
    ],
    "pseudo_russian": [
        _ex(
            "gum",
            "Верхние торговые ряды (ГУМ)",
            "Upper Trading Rows (GUM)",
            architect_ru="Александр Померанцев",
            architect_en="Alexander Pomerantsev",
            year="1890–1893",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "0/08/GUM_department_store_Moscow.jpg"
            ),
        ),
        _ex(
            "savior_on_blood",
            "Храм Спаса на Крови",
            "Church of the Savior on Blood",
            architect_ru="Альфред Парланд",
            architect_en="Alfred Parland",
            year="1883–1907",
            city_ru="Санкт-Петербург",
            city_en="Saint Petersburg",
            reuse_from="spb/images/places_of_worship/spb_savior_on_blood.jpg",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "4/4e/Church_of_the_Savior_on_Blood.jpg"
            ),
        ),
        _ex(
            "city_duma",
            "Здание Московской городской думы",
            "Moscow City Duma building",
            architect_ru="Дмитрий Чичагов",
            architect_en="Dmitry Chichagov",
            year="1890–1892",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "8/8e/Moscow_City_Duma.jpg"
            ),
        ),
    ],
    "neo_russian": [
        _ex(
            "yaroslavsky_station",
            "Ярославский вокзал",
            "Yaroslavsky railway terminal",
            architect_ru="Фёдор Шехтель",
            architect_en="Fyodor Shekhtel",
            year="1902–1904",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "5/5e/Yaroslavsky_Rail_Terminal.jpg"
            ),
        ),
        _ex(
            "tretyakov_facade",
            "Третьяковская галерея (фасад Васнецова)",
            "Tretyakov Gallery (Vasnetsov façade)",
            architect_ru="Виктор Васнецов",
            architect_en="Victor Vasnetsov",
            year="1906",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "4/4e/Tretyakov_Gallery_building.jpg"
            ),
        ),
        _ex(
            "feodorovsky_cathedral",
            "Собор Феодоровской иконы Божией Матери",
            "Feodorovsky Cathedral",
            architect_ru="Степан Кричинский",
            architect_en="Stepan Krichinsky",
            year="1911–1914",
            city_ru="Санкт-Петербург",
            city_en="Saint Petersburg",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "6/6e/Feodorovsky_Cathedral.jpg"
            ),
        ),
    ],
    "art_nouveau": [
        _ex(
            "ryabushinsky_mansion",
            "Особняк Рябушинского",
            "Ryabushinsky Mansion",
            architect_ru="Фёдор Шехтель",
            architect_en="Fyodor Shekhtel",
            year="1900–1903",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "8/8e/Ryabushinsky_Mansion.jpg"
            ),
        ),
        _ex(
            "singer_house",
            "Дом компании «Зингер»",
            "Singer House",
            architect_ru="Павел Сюзор",
            architect_en="Pavel Suzor",
            year="1902–1904",
            city_ru="Санкт-Петербург",
            city_en="Saint Petersburg",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "3/3f/Singer_House.jpg"
            ),
        ),
        _ex(
            "vitebsky_station",
            "Витебский вокзал",
            "Vitebsky railway station",
            architect_ru="Станислав Бржозовский",
            architect_en="Stanislav Brzozowski",
            year="1904",
            city_ru="Санкт-Петербург",
            city_en="Saint Petersburg",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "4/4e/Vitebsky_railway_station.jpg"
            ),
        ),
    ],
    "neoclassicism_early20": [
        _ex(
            "kyivsky_station",
            "Киевский вокзал",
            "Kyivsky railway terminal",
            architect_ru="Иван Рерберг",
            architect_en="Ivan Rerberg",
            year="1914–1918",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "5/5e/Kiyevsky_Railway_Terminal.jpg"
            ),
        ),
        _ex(
            "isakov_apartment",
            "Доходный дом И. П. Исакова",
            "I. P. Isakov apartment house",
            architect_ru="Лев Кекушев",
            architect_en="Lev Kekushev",
            year="1904–1906",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "6/6e/Kekushev_apartment_house.jpg"
            ),
        ),
        _ex(
            "azov_don_bank",
            "Азовско-Донской банк",
            "Azov-Don Bank",
            architect_ru="Фёдор Лидваль",
            architect_en="Fyodor Lidval",
            year="1907–1913",
            city_ru="Санкт-Петербург",
            city_en="Saint Petersburg",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "8/8e/Azov-Don_Commercial_Bank.jpg"
            ),
        ),
    ],
    "avant_garde": [
        _ex(
            "shukhov_tower",
            "Шуховская башня",
            "Shukhov Tower",
            architect_ru="Владимир Шухов",
            architect_en="Vladimir Shukhov",
            year="1922",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "5/5e/Shukhov_tower.jpg"
            ),
        ),
        _ex(
            "narkomfin",
            "Дом Наркомфина",
            "Narkomfin Building",
            architect_ru="Моисей Гинзбург, Игнатий Милинис",
            architect_en="Moisei Ginzburg, Ignaty Milinis",
            year="1928–1930",
            city_ru="Москва",
            city_en="Moscow",
            reuse_from="moscow/images/moscow_osobnjaki/narkomfin_1.jpg",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "4/4e/Narkomfin_Building.jpg"
            ),
        ),
        _ex(
            "zuev_club",
            "ДК имени Зуева",
            "Zuev Workers' Club",
            architect_ru="Илья Голосов",
            architect_en="Ilya Golosov",
            year="1927–1929",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "6/6e/Zuev_Workers%27_Club.jpg"
            ),
        ),
    ],
    "stalinist": [
        _ex(
            "msu_main_building",
            "Главное здание МГУ",
            "MSU main building",
            architect_ru="Лев Руднев",
            architect_en="Lev Rudnev",
            year="1949–1953",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "5/5e/Moscow_State_University_main_building.jpg"
            ),
        ),
        _ex(
            "komsomolskaya_metro",
            "Станция метро «Комсомольская-кольцевая»",
            "Komsomolskaya metro station",
            architect_ru="Алексей Щусев и др.",
            architect_en="Alexey Shchusev et al.",
            year="1952",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "4/4e/Komsomolskaya-Koltsevaya_Metro_Station.jpg"
            ),
        ),
        _ex(
            "vdnh_main_pavilion",
            "Главный павильон ВДНХ",
            "VDNKh main pavilion",
            architect_ru="Георгий Щуко, Евгений Столяров",
            architect_en="Georgy Schuko, Yevgeny Stolyarov",
            year="1954",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "6/6e/VDNKh_main_pavilion.jpg"
            ),
        ),
    ],
    "panel_housing": [
        _ex(
            "k7_series",
            "Жилые дома серии К-7",
            "K-7 panel housing series",
            year="с 1958",
            city_ru="Москва и др.",
            city_en="Moscow and other cities",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "8/8e/Khrushchyovka_in_Moscow.jpg"
            ),
        ),
        _ex(
            "p44_series",
            "Дома серии П-44",
            "P-44 panel series",
            year="с 1978",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "5/5e/Panel_building_Moscow.jpg"
            ),
        ),
        _ex(
            "cheremushki",
            "Микрорайон Черёмушки",
            "Cheryomushki micro-district",
            year="1956–1959",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "4/4e/Cheryomushki_district.jpg"
            ),
        ),
    ],
    "soviet_modernism": [
        _ex(
            "ostankino_tower",
            "Останкинская телебашня",
            "Ostankino Tower",
            architect_ru="Николай Никитин",
            architect_en="Nikolai Nikitin",
            year="1963–1967",
            city_ru="Москва",
            city_en="Moscow",
            reuse_from="moscow/images/moscow_places/ostankino_tower_1.jpg",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "1/1e/Ostankino_Tower.jpg"
            ),
        ),
        _ex(
            "kremlin_palace",
            "Дворец съездов в Кремле",
            "Kremlin Palace of Congresses",
            architect_ru="Михаил Посохин и др.",
            architect_en="Mikhail Posokhin et al.",
            year="1961",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "6/6e/Kremlin_Palace_of_Congresses.jpg"
            ),
        ),
        _ex(
            "tass_building",
            "Здание ТАСС",
            "TASS building",
            architect_ru="Дмитрий Чечулин",
            architect_en="Dmitry Chechulin",
            year="1960-е",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "8/8e/TASS_building_Moscow.jpg"
            ),
        ),
    ],
    "stalinist_neoclassicism": [
        _ex(
            "hotel_moscow",
            "Гостиница «Москва»",
            "Hotel Moskva",
            architect_ru="Алексей Щусев и др.",
            architect_en="Alexey Shchusev et al.",
            year="1932–1935",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "5/5e/Hotel_Moskva_Moscow.jpg"
            ),
        ),
        _ex(
            "gagarin_square_house",
            "Дом на площади Гагарина",
            "Gagarin Square apartment house",
            year="1949–1955",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "4/4e/Stalinist_apartment_Moscow.jpg"
            ),
        ),
        _ex(
            "kutuzovsky_avenue",
            "Застройка Кутузовского проспекта",
            "Kutuzovsky Avenue ensemble",
            year="1940–1950-е",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "6/6e/Kutuzovsky_Prospekt.jpg"
            ),
        ),
    ],
    "art_deco": [
        _ex(
            "red_army_theater",
            "Центральный театр Красной Армии",
            "Central Red Army Theatre",
            architect_ru="Константин Алабян, Василий Симбирцев",
            architect_en="Konstantin Alabyan, Vasily Simbirsky",
            year="1934–1940",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "8/8e/Central_Army_Theater.jpg"
            ),
        ),
        _ex(
            "rodina_cinema",
            "Кинотеатр «Родина»",
            "Rodina Cinema",
            architect_ru="Ярослав Щуко",
            architect_en="Yaroslav Shchuko",
            year="1937–1938",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "5/5e/Rodina_Cinema_Moscow.jpg"
            ),
        ),
        _ex(
            "metro_art_deco",
            "Станции московского метро (элементы ар-деко)",
            "Moscow metro stations (Art Deco elements)",
            year="1930–1950-е",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "4/4e/Mayakovskaya_metro_station.jpg"
            ),
        ),
    ],
    "post_constructivism": [
        _ex(
            "zil_palace",
            "Дворец культуры ЗИЛ",
            "ZIL Palace of Culture",
            architect_ru="братья Веснины",
            architect_en="Vesnin brothers",
            year="1930–1937",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "6/6e/ZIL_Palace_of_Culture.jpg"
            ),
        ),
        _ex(
            "mohovaya_house",
            "Жилой дом на Моховой",
            "Mohovaya Street apartment house",
            architect_ru="Иван Жолтовский",
            architect_en="Ivan Zholtovsky",
            year="1934",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "8/8e/Mohovaya_Street_building.jpg"
            ),
        ),
        _ex(
            "arktika_hotel",
            "Гостиница «Арктика»",
            "Arktika Hotel",
            year="1933–1936",
            city_ru="Мурманск",
            city_en="Murmansk",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "5/5e/Arktika_Hotel_Murmansk.jpg"
            ),
        ),
    ],
    "regional_soviet": [
        _ex(
            "yubileyny_palace",
            "Дворец спорта «Юбилейный»",
            "Yubileyny Sports Palace",
            year="1967",
            city_ru="Санкт-Петербург",
            city_en="Saint Petersburg",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "6/6e/Yubileyny_Sports_Palace.jpg"
            ),
        ),
        _ex(
            "luzhniki_stadium",
            "Стадион «Лужники»",
            "Luzhniki Stadium",
            year="1956",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "5/5e/Luzhniki_Stadium.jpg"
            ),
        ),
        _ex(
            "novosibirsk_opera",
            "Театр оперы и балета (Новосибирск)",
            "Novosibirsk Opera and Ballet Theatre",
            year="1931–1945",
            city_ru="Новосибирск",
            city_en="Novosibirsk",
            reuse_from="novosibirsk/images/novosibirsk_opera_ballet.jpg",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "4/4e/Novosibirsk_Opera_and_Ballet_Theatre.jpg"
            ),
        ),
    ],
    "brutalism": [
        _ex(
            "bioorganic_chemistry",
            "Институт биоорганической химии РАН",
            "Institute of Bioorganic Chemistry RAS",
            year="1976–1984",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "8/8e/IBCh_RAS_building.jpg"
            ),
        ),
        _ex(
            "aviators_house",
            "Дом авиаторов на Беговой",
            "House of Aviators, Begovaya",
            architect_ru="Андрей Меерсон",
            architect_en="Andrey Meerson",
            year="1973–1978",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "5/5e/House_of_Aviators_Moscow.jpg"
            ),
        ),
        _ex(
            "ras_presidium",
            "Комплекс Президиума РАН",
            "RAS Presidium complex",
            year="1970–1990-е",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "6/6e/RAS_Presidium_building.jpg"
            ),
        ),
    ],
    "soviet_neoclassicism_revival": [
        _ex(
            "vdnh_pavilion_revival",
            "Главный павильон ВДНХ (реконструкция)",
            "VDNKh main pavilion (restored)",
            year="1954",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "6/6e/VDNKh_main_pavilion.jpg"
            ),
        ),
        _ex(
            "nevsky_prospect",
            "Реконструкция Невского проспекта",
            "Nevsky Prospect reconstruction",
            year="1940–1950-е",
            city_ru="Санкт-Петербург",
            city_en="Saint Petersburg",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "c/c2/Spb_06-2012_Nevsky_various_02.jpg"
            ),
        ),
        _ex(
            "postwar_kutuzovsky",
            "Послевоенная застройка Кутузовского",
            "Post-war Kutuzovsky ensemble",
            year="1940–1950-е",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "6/6e/Kutuzovsky_Prospekt.jpg"
            ),
        ),
    ],
    "postmodernism": [
        _ex(
            "pokrovka_theatre",
            "Театр на Покровке",
            "Pokrovka Theatre",
            architect_ru="Александр Великанов",
            architect_en="Alexander Velikanov",
            year="1990-е",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "8/8e/Pokrovka_Theatre.jpg"
            ),
        ),
        _ex(
            "tower_2000",
            "Бизнес-центр «Башня 2000»",
            "Tower 2000 business centre",
            year="1996–2001",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "5/5e/Tower_2000_Moscow.jpg"
            ),
        ),
        _ex(
            "balchug_kempinski",
            "Отель «Балчуг Кемпински»",
            "Balchug Kempinski Hotel",
            year="1990-е",
            city_ru="Москва",
            city_en="Moscow",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "6/6e/Balchug_Kempinski.jpg"
            ),
        ),
    ],
    "contemporary": [
        _ex(
            "moscow_city",
            "Москва-Сити",
            "Moscow International Business Center",
            year="2000–2020-е",
            city_ru="Москва",
            city_en="Moscow",
            reuse_from="moscow/images/moscow_landmarks/moscow_city_2.jpg",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "5/5e/Moscow_International_Business_Center.jpg"
            ),
        ),
        _ex(
            "zaryadye_park",
            "Парк «Зарядье»",
            "Zaryadye Park",
            year="2017",
            city_ru="Москва",
            city_en="Moscow",
            reuse_from="moscow/images/moscow_landmarks/zaryadye_bridge_1.jpg",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "6/6e/Zaryadye_Park_Moscow.jpg"
            ),
        ),
        _ex(
            "lakhta_center",
            "Лахта-центр",
            "Lakhta Center",
            year="2018",
            city_ru="Санкт-Петербург",
            city_en="Saint Petersburg",
            commons_url=(
                "https://upload.wikimedia.org/wikipedia/commons/"
                "4/4e/Lakhta_Center.jpg"
            ),
        ),
    ],
}

STYLE_ORDER: tuple[str, ...] = tuple(STYLE_META.keys())
