# -*- coding: utf-8 -*-
"""Supplemental prose for places under the minimum word count."""

from __future__ import annotations

import re
from typing import Any

MIN_NARRATIVE_WORDS = 20

# slug -> (extra_history_ru, extra_history_en, extra_significance_ru,
#           extra_significance_en)
_SUPPLEMENTS: dict[str, tuple[str, str, str, str]] = {
    "etruscan_roman_colosseum": (
        "Вместимость достигала примерно пятидесяти тысяч зрителей; "
        "под ареной — лабиринт служебных помещений.",
        "It seated about fifty thousand spectators; a service "
        "labyrinth lies beneath the arena.",
        "Образец римского бетона, сводов и организации "
        "массовых зрелищ.",
        "A landmark of Roman concrete, vaulting and mass spectacle.",
    ),
    "etruscan_roman_pantheon": (
        "Купол из бетона с отверстием окулуса освещает зал "
        "диаметром сорок три метра.",
        "A concrete dome with the open oculus lights a hall "
        "forty-three metres wide.",
        "Древнейший сохранившийся крупный свод мира; "
        "образец римской инженерии.",
        "The best-preserved great Roman vault; an engineering "
        "icon.",
    ),
    "romanesque_pisa_cathedral": (
        "Мраморный собор начат в 1063 году на Пьяцца-деи-Мираколи.",
        "The marble cathedral was begun in 1063 on the Campo "
        "dei Miracoli.",
        "Ядро ансамбля с Пизанской башней и баптистерием.",
        "Core of the ensemble with the Leaning Tower and "
        "baptistery.",
    ),
    "romanesque_san_miniato": (
        "Фасад с мозаикой Христа и зелёно-белым мрамором "
        "возвышается над Арно.",
        "A Christ mosaic and green-white marble façade rise "
        "above the Arno.",
        "Высокий романский интерьер с византийскими "
        "настенными мозаиками.",
        "A lofty Romanesque interior with Byzantine wall "
        "mosaics.",
    ),
    "romanesque_sant_ambrogio": (
        "Атрий с античными колоннами ведёт к залу с "
        "мозаиками и деревянным потолком.",
        "An atrium of antique columns leads to a hall with "
        "mosaics and a timber ceiling.",
        "Главный храм Милана и образец ломбардского "
        "романского стиля.",
        "Milan's principal church and a Lombard Romanesque "
        "model.",
    ),
    "romanesque_cathedral_modena": (
        "Рельефы Вилджельмо на портале рассказывают библейские "
        "сюжеты в камне.",
        "Wiligelmo's portal reliefs narrate biblical scenes in "
        "stone.",
        "Собор Ланфранко и романский шедевр Падании.",
        "Lanfranco's cathedral and a Romanesque masterpiece of "
        "the Po Valley.",
    ),
    "norman_sicilian_monreale": (
        "Золотые мозаики в куполе и апсиде покрывают "
        "шесть тысяч квадратных метров.",
        "Golden mosaics in the dome and apse cover six thousand "
        "square metres.",
        "Синтез норманнской, византийской и арабской культуры "
        "на Сицилии.",
        "Synthesis of Norman, Byzantine and Arab culture in "
        "Sicily.",
    ),
    "norman_sicilian_cefalu": (
        "Византийский Христос Пантократор в апсиде доминирует "
        "над нефом.",
        "A Byzantine Christ Pantocrator in the apse dominates "
        "the nave.",
        "Норманнский собор на берегу Тирренского моря.",
        "Norman cathedral on the Tyrrhenian shore.",
    ),
    "norman_sicilian_palatine_chapel": (
        "Золотые мозаики и арабские деревянные потолки "
        "украшают королевскую капеллу.",
        "Golden mosaics and Arab wooden ceilings adorn the "
        "royal chapel.",
        "Жемчужина Палермского норманнского дворца.",
        "Jewel of the Norman palace in Palermo.",
    ),
    "norman_sicilian_zisa": (
        "Летняя резиденция с фонтанным залом и "
        "арабо-норманнскими декоративными мотивами.",
        "A summer residence with a fountain hall and "
        "Arab-Norman decorative motifs.",
        "Памятник сицилийского двора эпохи Вильгельма II.",
        "Monument of the Sicilian court under William II.",
    ),
    "norman_sicilian_cathedral_palermo": (
        "Фасад перестраивался; внутри — мозаики и королевские "
        "гробницы.",
        "The façade was rebuilt; inside are mosaics and royal "
        "tombs.",
        "Главный храм норманнской Палермо.",
        "Principal church of Norman Palermo.",
    ),
    "norman_sicilian_san_giovanni": (
        "Гипогей с саркофагами норманнских правителей под "
        "соборным полом.",
        "A hypogeum with Norman rulers' sarcophagi lies beneath "
        "the cathedral floor.",
        "Связь палермитанского собора с королевскими "
        "погребениями.",
        "Links the Palermo cathedral to royal burials.",
    ),
    "high_renaissance_tempietto": (
        "Круглый периптер на Яникуле отмечает место, "
        "связанное с апостолом Петром.",
        "A circular peripteros on the Janiculum marks a site "
        "linked to Saint Peter.",
        "Эталон центрического храма Высокого Возрождения.",
        "Model centric temple of the High Renaissance.",
    ),
    "high_renaissance_palazzo_teatro_olimpico": (
        "Сцена с перспективными улицами — последний проект "
        "Андреа Палладио.",
        "The stage with perspectival streets was Andrea "
        "Palladio's final project.",
        "Старейший крытый театр эпохи Возрождения.",
        "Oldest surviving Renaissance indoor theatre.",
    ),
    "rococo_late_baroque_palazzo_madama": (
        "Барочная лестница Juvarra ведёт в парадные залы "
        "бывшей резиденции.",
        "Juvarra's Baroque staircase leads to the state rooms "
        "of the former residence.",
        "Сегодня музей в историческом центре Турина.",
        "Now a museum in Turin's historic centre.",
    ),
    "romantic_eclectic_stazione_milano": (
        "Каменный фасад с скульптурой и стеклянным навесом "
        "скрывает огромный зал.",
        "A stone façade with sculpture and a glass canopy "
        "fronts a vast hall.",
        "Ворота миланского модерна и символ городской "
        "мобильности.",
        "Gateway of Milanese modernity and urban mobility.",
    ),
    "contemporary_citylife": (
        "Башни Хадид, Либескинда и Араты окружают парк "
        "и торговые галереи.",
        "Towers by Hadid, Libeskind and Arata frame a park "
        "and retail galleries.",
        "Крупнейшая деловая регенерация Милана после "
        "Expo 2015.",
        "Milan's largest business regeneration after Expo 2015.",
    ),
    "high_renaissance_santa_maria_formosa": (
        "Фасады Кодуччи обращены к каналу и площади.",
        "Codussi's façades address both canal and campo.",
        "Редкий пример венецианской центрической церкви "
        "эпохи Высокого Возрождения.",
        "A rare Venetian High Renaissance centric church.",
    ),
    "high_renaissance_palazzo_ducale_uffizi": (
        "Коридор Вазари связывает Палаццо Веккьо с Уффици.",
        "Vasari's corridor links the Palazzo Vecchio to the Uffizi.",
        "Прототип европейского музейного квартала.",
        "Prototype of the European museum quarter.",
    ),
    "high_renaissance_palazzo_chiericati": (
        "Портик на уровне улицы открывает городскую резиденцию.",
        "A street-level portico opens the urban palace.",
        "Образец палладианской пропорции для частных дворцов.",
        "Model Palladian proportion for private palaces.",
    ),
    "high_renaissance_cortile_belvedere": (
        "Двор соединяет Ватиканский дворец с садами.",
        "The courtyard links the Vatican palace to the gardens.",
        "Ранняя схема музейного движения по этажам.",
        "Early multi-level museum circulation.",
    ),
    "high_renaissance_san_giorgio": (
        "Белый мраморный фасад отражается в водах бассейна.",
        "The white marble façade mirrors the basin waters.",
        "Классический храм Палладио, видимый с Сан-Марко.",
        "Palladio's temple seen from San Marco.",
    ),
    "high_renaissance_palazzo_massimo2": (
        "Лоджия Рафаэля сохраняет фрески и росписи.",
        "Raphael's loggia retains fresco cycles.",
        "Загородная вилла у Тибра для папских банкетов.",
        "A Tiber-side villa for papal entertainments.",
    ),
    "mannerism_palazzo_del_te": (
        "Залы украшены иллюзорными фресками Романо.",
        "Rooms carry Giulio Romano's illusionistic frescoes.",
        "Маньеристская игра масштаба и сюжета.",
        "Mannerist play of scale and narrative.",
    ),
    "mannerism_cappella_pauline": (
        "Купол и стены расписал поздний Микеланджело.",
        "Michelangelo painted the late frescoes on walls and vault.",
        "Ключевой памятник римского маньеризма.",
        "Key monument of Roman Mannerism.",
    ),
    "mannerism_orvieto_well": (
        "Две винтовые лестницы не пересекаются внутри ствола.",
        "Twin ramps descend without meeting inside the shaft.",
        "Инженерный шедевр Антонио да Сангалло Младшего.",
        "Engineering masterpiece by Antonio da Sangallo the Younger.",
    ),
    "mannerism_palazzo_binder": (
        "Фасад украшен гротесками и стукко.",
        "The façade bears grotesques and stucco.",
        "Сиенский дворец эпохи позднего Возрождения.",
        "Sienese palace of the late Renaissance.",
    ),
    "mannerism_villa_lante": (
        "Каскадные фонтаны спускаются террасами к партеру.",
        "Cascade fountains step down to the parterre.",
        "Образцовый маньеристский сад XVI века.",
        "Exemplary sixteenth-century Mannerist garden.",
    ),
    "mannerism_santa_maria_novella": (
        "Мраморный фасад Альберти завершён в 1470 году.",
        "Alberti's marble façade was completed around 1470.",
        "Теоретический мост от Возрождения к маньеризму.",
        "Theoretical bridge from Renaissance to Mannerism.",
    ),
    "baroque_san_carlo": (
        "Овальный купол и волнистые стены Борромини.",
        "Borromini's oval dome and undulating walls.",
        "Компактный шедевр римского барокко.",
        "Compact masterpiece of Roman Baroque.",
    ),
    "sicilian_baroque_san_benedetto": (
        "Лестница ведёт к витиеатому фасаду на улице.",
        "A staircase climbs to the ornate street façade.",
        "Катанская школа сицилийского барокко.",
        "Catania school of Sicilian Baroque.",
    ),
    "sicilian_baroque_duomo_ragusa": (
        "Собор господствует над старым городом Ибла.",
        "The cathedral crowns Ibla's old town.",
        "Вал ди Ното включён в список ЮНЕСКО.",
        "Val di Noto is a UNESCO World Heritage site.",
    ),
    "sicilian_baroque_palazzo_biscari": (
        "Балконный зал выходит на порт Катании.",
        "The balcony hall overlooks Catania's port.",
        "Светский дворец сицилийского барокко.",
        "Secular palace of Sicilian Baroque.",
    ),
    "sicilian_baroque_san_giuseppe": (
        "Волнистый фронтон доминирует над площадью.",
        "A curving pediment dominates the square.",
        "Динамика рагузской барочной линии.",
        "Dynamism of Ragusa's Baroque skyline.",
    ),
    "sicilian_baroque_palazzo_nicolaci": (
        "Кованые балконы украшают главный фасад.",
        "Wrought-iron balconies line the main front.",
        "Гражданская архитектура восстановленного Ното.",
        "Civic architecture of rebuilt Noto.",
    ),
    "sicilian_baroque_duomo_modica": (
        "Лестница из сотни ступеней поднимается к хору.",
        "A hundred steps climb to the choir terrace.",
        "Городской ландшафт Модики вокруг дуомо.",
        "Modica's terraced townscape around the duomo.",
    ),
    "rococo_late_baroque_palazzo_carignano": (
        "Кирпичный волнистый фасад Гварини в Турине.",
        "Guarini's undulating brick front in Turin.",
        "Северный поздний барокко переходит в рококо.",
        "Northern late Baroque turning toward Rococo.",
    ),
    "rococo_late_baroque_venaria": (
        "Парадный двор ведёт к охотничьим апартаментам.",
        "The court leads to royal hunting apartments.",
        "Крупнейший савойский дворцовый комплекс.",
        "Largest Savoy palace complex.",
    ),
    "rococo_late_baroque_stupinigi": (
        "Центральный зал увенчан охотничьей сценой.",
        "The central hall is crowned by a hunting scene.",
        "Загородная резиденция савойского двора.",
        "Savoy court country residence.",
    ),
    "rococo_late_baroque_la_reggia": (
        "Парадные залы выходят на площадь Castello.",
        "State rooms open toward Piazza Castello.",
        "Столица позднего барокко Пьемонта.",
        "Capital of Piedmontese late Baroque.",
    ),
    "rococo_late_baroque_santa_croce": (
        "Фасад вырезан из светлого местного известняка.",
        "The façade is carved from pale local limestone.",
        "Леччезе барокко с пышным декором.",
        "Lecce Baroque with exuberant ornament.",
    ),
    "rococo_late_baroque_palazzo_reale_naples": (
        "Дворец смотрит на плещадь перед собором.",
        "The palace faces the cathedral square.",
        "Испанское наместничество и неаполитанский двор.",
        "Spanish viceregal and Neapolitan court life.",
    ),
    "neoclassicism_la_scala": (
        "Зрительный зал в форме подковы открыт с 1778 года.",
        "The horseshoe auditorium opened in 1778.",
        "Главный оперный театр миланского неоклассицизма.",
        "Chief opera house of Milanese Neoclassicism.",
    ),
    "neoclassicism_basilica_san_francesco": (
        "Колоннада обрамляет площадь перед Пьяцца-дель-Плебисцито.",
        "A colonnade frames the square before Plebiscito.",
        "Неаполитанский неоклассический ансамбль.",
        "Neapolitan Neoclassical ensemble.",
    ),
    "romantic_eclectic_castello_brolio": (
        "Неоготические башни возвышаются над виноградниками.",
        "Neo-Gothic towers rise above Chianti vineyards.",
        "Романтическое переосмысление средневекового замка.",
        "Romantic reimagining of a medieval castle.",
    ),
    "romantic_eclectic_vittoriale": (
        "Амфитеатр и мавзолей входят в комплекс на озере.",
        "An amphitheatre and mausoleum stand on Lake Garda.",
        "Эклектический памятник Д'Аннунцио.",
        "D'Annunzio's eclectic memorial landscape.",
    ),
    "romantic_eclectic_mole_antonelliana": (
        "Шпиль высотой 167 метров виден из всего Турина.",
        "A 167-metre spire is visible across Turin.",
        "Символ инженерной эклектики объединённой Италии.",
        "Symbol of united Italy's engineering eclecticism.",
    ),
    "romantic_eclectic_palazzo_castello": (
        "Замок на скале над Триестским заливом.",
        "The castle stands on a cliff above Trieste harbour.",
        "Романтическая резиденция Максимилиана Габсбурга.",
        "Romantic residence of Maximilian of Habsburg.",
    ),
    "liberty_galleria_vittorio": (
        "Стеклянный купол перекрывает крестообразный пассаж.",
        "A glass dome covers the cruciform passage.",
        "Салон миланской жизни конца XIX века.",
        "Salon of late nineteenth-century Milanese life.",
    ),
    "liberty_casa_fiorita": (
        "Керамические цветы покрывают эркеры фасада.",
        "Ceramic flowers cover the bay windows.",
        "Туринский Stile Liberty в жилой архитектуре.",
        "Turin Stile Liberty in residential design.",
    ),
    "liberty_villino_idale": (
        "Растительный орнамент обрамляет окна и балконы.",
        "Floral ornament frames windows and balconies.",
        "Миланский модерн начала XX века.",
        "Early twentieth-century Milanese Art Nouveau.",
    ),
    "liberty_villino_florio": (
        "Дворец Флорио украшен майоликой и ковкой.",
        "Floral majolica and ironwork decorate the palace.",
        "Сицилийский вариант Stile Liberty.",
        "Sicilian variant of Stile Liberty.",
    ),
    "liberty_casa_galimberti": (
        "Майоликовые панели покрывают весь фасад.",
        "Majolica panels sheath the entire façade.",
        "Один из самых ярких домов Милана в стиле Либерти.",
        "Among Milan's boldest Liberty houses.",
    ),
    "liberty_palazzo_castello_liberty": (
        "Декор модерна украшает набережную Арно.",
        "Art Nouveau décor lines the Arno embankment.",
        "Флорентийский модерн для музейного квартала.",
        "Florentine modernism for the museum quarter.",
    ),
    "liberty_villa_necchi": (
        "Бассейн и сад интегрированы в строгий объём Понти.",
        "A pool and garden are set into Ponti's rigorous volume.",
        "Музей FAI открывает интерьеры для посетителей.",
        "FAI museum opens the interiors to visitors.",
    ),
    "liberty_grand_hotel": (
        "Парадные залы выходят на Пьяцца Венеция.",
        "Grand halls address Piazza Venezia.",
        "Светская архитектура римского модерна.",
        "Secular architecture of Roman Art Nouveau.",
    ),
    "liberty_palazzo_exhibition": (
        "Колоннада обрамляет выставочные залы на Виа Национале.",
        "A colonnade frames exhibition halls on Via Nazionale.",
        "Культурный центр римского модерна.",
        "Cultural centre of Roman Art Nouveau.",
    ),
    "rationalism_palazzo_gioia": (
        "Горизонтальные ленты окон ритмируют фасад.",
        "Horizontal window bands rhythm the façade.",
        "Ранний итальянский рационализм в Милане.",
        "Early Italian Rationalism in Milan.",
    ),
    "rationalism_casa_del_fascio": (
        "Стеклянный угол раскрывает внутренний атриум.",
        "A glass corner reveals the interior atrium.",
        "Террани задаёт канон рационалистского дворца.",
        "Terragni sets the Rationalist palace canon.",
    ),
    "rationalism_santelia": (
        "Монумент увековечивает автора Città Nuova.",
        "The memorial honours the author of Città Nuova.",
        "Мост между футуризмом и рационализмом.",
        "Bridge between Futurism and Rationalism.",
    ),
    "rationalism_palazzo_justice": (
        "Башни и аркада формируют городской фронт.",
        "Towers and arcades shape the urban front.",
        "Монументальное здание суда Пьочентини.",
        "Piacentini's monumental courthouse.",
    ),
    "rationalism_colonia_montecatini": (
        "Корпуса санатория ориентированы на солнечную сторону.",
        "Sanatorium wings orient to the sunny exposure.",
        "Функционализм и гигиена межвоенной Италии.",
        "Functionalism and hygiene in interwar Italy.",
    ),
    "rationalism_palazzo_justice2": (
        "Галерея размещена в королевском дворце Турина.",
        "The gallery occupies Turin's royal palace.",
        "Рационалистическая реставрация музейных залов.",
        "Rationalist restoration of museum rooms.",
    ),
    "fascist_rationalism_eur": (
        "Мрамор и линейные оси оформляют квартал выставки.",
        "Marble and axial planning shape the fair quarter.",
        "Образец монументального razionalismo 1930-х.",
        "Exemplar of 1930s monumental Razionalismo.",
    ),
    "fascist_rationalism_foro_italico": (
        "Мозаики изображают спортивные сцены на стенах.",
        "Mosaics depict athletic scenes on the walls.",
        "Пропагандистский спортивный комплекс Рима.",
        "Rome's propaganda sports complex.",
    ),
    "fascist_rationalism_stazione_termini": (
        "Волнообразный бетонный навес над главным залом.",
        "A wave-like concrete canopy covers the main hall.",
        "Послевоенное завершение вокзала Монтюори.",
        "Montuori's post-war completion of Termini.",
    ),
    "fascist_rationalism_palazzo_littorio": (
        "Дворец партии был разрушен после войны.",
        "The party palace was destroyed after the war.",
        "Напоминание о политической архитектуре эпохи.",
        "Reminder of the era's political architecture.",
    ),
    "fascist_rationalism_mattatoio": (
        "Кирпичные павильоны перестроены под культуру.",
        "Brick pavilions were converted for culture.",
        "Адаптивное использование индустриального наследия.",
        "Adaptive reuse of industrial heritage.",
    ),
    "postwar_modern_galfa": (
        "Башня доминирует над миланским Corso Como.",
        "The tower dominates Milan's Corso Como.",
        "Офисный модернизм конца 1950-х.",
        "Late 1950s office modernism.",
    ),
    "postwar_modern_church_autostrada": (
        "Бетонные оболочки скрывают световые щели.",
        "Concrete shells conceal narrow light slits.",
        "Сакральный модернизм Микелуччи на A1.",
        "Michelucci's sacred modernism on the A1.",
    ),
    "postwar_modern_gallaratese": (
        "Галереи и лоджии повторяют тип жилого блока.",
        "Galleries and loggias repeat the housing type.",
        "Типологический модернизм Росси.",
        "Rossi's typological modernism.",
    ),
    "postwar_modern_san_giovanni_battista": (
        "Цилиндрический объём возвышается над Маджией.",
        "A cylindrical volume rises above the Maggia valley.",
        "Тессинская школа Марио Ботты.",
        "Mario Botta's Ticino school.",
    ),
    "postwar_modern_olivetti": (
        "Стекло и бетон оформляют административный корпус.",
        "Glass and concrete shape the admin wing.",
        "Корпоративный кампус Ивреа.",
        "Ivrea corporate campus.",
    ),
    "postwar_modern_pirelli": (
        "Стройная башня Понти и Роджи определяет силуэт.",
        "Ponti and Rogers' slender tower defines the skyline.",
        "Первый миланский небоскрёб после войны.",
        "Milan's first post-war skyscraper.",
    ),
    "postwar_modern_torre_velasca": (
        "Расширяющийся верх напоминает средневековую башню.",
        "The swelling top echoes a medieval tower.",
        "Икона неореалистического Милана.",
        "Icon of Neorealist Milan.",
    ),
    "brutalism_san_giovanni_bosco": (
        "Наклонные бетонные плоскости формируют интерьер.",
        "Sloping concrete planes shape the interior.",
        "Поздний брутализм Никола в Турине.",
        "Nicola's late Brutalism in Turin.",
    ),
    "brutalism_convento_annunciata": (
        "Монастырь Монтегнакули использует сырой бетон и свет.",
        "Montegnagoli's monastery pairs raw concrete with light.",
        "Сакральный брутализм миланской школы.",
        "Sacred Brutalism of the Milan school.",
    ),
    "brutalism_church_resistenza": (
        "Алтарная стена обращена к парку памяти.",
        "The altar wall addresses a memorial park.",
        "Мемориальная церковь послевоенного Сопротивления.",
        "Memorial church to the wartime Resistance.",
    ),
    "brutalism_church_longarone": (
        "Храм напоминает о катастрофе плотины Вайонт.",
        "The church recalls the Vajont dam disaster.",
        "Монументальный брутализм Пьемонта.",
        "Piedmont monumental Brutalism.",
    ),
    "brutalism_university_cagliari": (
        "Кампус Монсеррато выстроен из необработанного бетона.",
        "The Monserrato campus is built in raw concrete.",
        "Образовательный брутализм Сардинии.",
        "Sardinian educational Brutalism.",
    ),
    "brutalism_church_autostrada_brut": (
        "Массивные опоры несут бетонную часовню.",
        "Massive piers carry the concrete chapel.",
        "Инфраструктурный брутализм на трассе A1.",
        "Infrastructure Brutalism on the A1 motorway.",
    ),
    "brutalism_fire_station": (
        "Скарпа встроил станцию в венецианский остров.",
        "Scarpa embedded the station in a Venetian island.",
        "Брутализм в диалоге с исторической тканью.",
        "Brutalism in dialogue with historic fabric.",
    ),
    "postmodern_tendenza_museum_modena": (
        "Порта переосмыслил музей как городской фрагмент.",
        "Porta reconceived the museum as an urban fragment.",
        "Постмодернистская институция Эмилии.",
        "Postmodern institution of Emilia.",
    ),
    "postmodern_tendenza_theatre_bologna": (
        "Реконструкция цитирует исторические фасады.",
        "Reconstruction quotes historic façades.",
        "Tendenza и контекстуальная перестройка.",
        "Tendenza and contextual rebuilding.",
    ),
    "postmodern_tendenza_piazza_italia": (
        "Колонны-карикатуры окружают фонтан.",
        "Caricature columns surround the fountain.",
        "Грасси и постмодернизм Палермо.",
        "Graves and Palermo's postmodern turn.",
    ),
    "postmodern_tendenza_palazzo_italia": (
        "Классические мотивы реинтерпретированы в фасаде.",
        "Classical motifs are reinterpreted on the façade.",
        "Неоклассический постмодерн Милана.",
        "Milan's neoclassical postmodern turn.",
    ),
    "postmodern_tendenza_celtic": (
        "Павильон демонстрировал кельтское искусство на Биеннале.",
        "The pavilion presented Celtic art at the Biennale.",
        "Постмодернистский временный павильон в Гиардини.",
        "Postmodern temporary pavilion in the Giardini.",
    ),
    "postmodern_tendenza_church_resurrection": (
        "Приходской храм объединяет традицию и новые формы.",
        "The parish church merges tradition with new forms.",
        "Сакральный постмодерн Турина.",
        "Turin's sacred postmodern architecture.",
    ),
    "contemporary_maxxi": (
        "Пространство организовано пересекающимися лентами.",
        "Space is organised by intersecting bands.",
        "Первый римский музей только XXI века.",
        "Rome's first museum devoted solely to the 21st century.",
    ),
    "contemporary_prada": (
        "Золотая и алюминиевая облицовка контрастирует с заводом.",
        "Gold and aluminium cladding contrasts with the factory.",
        "Кулхаас и адаптивное культурное пространство.",
        "Koolhaas and adaptive cultural space.",
    ),
    "contemporary_jubilee": (
        "Три бетонные оболочки окружают приходской зал.",
        "Three concrete shells wrap the parish hall.",
        "Меир и современная римская сакральность.",
        "Meier and contemporary Roman sacred architecture.",
    ),
    "contemporary_porta_nuova": (
        "Небоскрёбы образуют новый деловой горизонт.",
        "Skyscrapers form a new business skyline.",
        "Крупнейшая городская регенерация Милана.",
        "Milan's largest urban regeneration project.",
    ),
    "contemporary_parco_della_musica": (
        "Три концертных зала соединены общим лобби.",
        "Three concert halls share a common lobby.",
        "Пиано и музыкальный кампус XXI века.",
        "Piano and a twenty-first-century music campus.",
    ),
    "contemporary_bosco_verticale": (
        "Деревья на террасах формируют живой фасад.",
        "Trees on terraces create a living façade.",
        "Боэри и экологическая высотная архитектура.",
        "Boeri and ecological high-rise design.",
    ),
    "contemporary_snfcc": (
        "Пространство музея выстроено динамичными траекториями.",
        "The museum volume is shaped by dynamic routes.",
        "Культурная инфраструктура римского Flaminio.",
        "Cultural infrastructure of Rome's Flaminio quarter.",
    ),
    "mannerism_palazzo_thiene": (
        "Заказчики — семья Тьене; позже дворец достраивал Винченцо Скамоцци.",
        "Commissioned by the Thiene family; Vicenzo Scamozzi later "
        "completed the palace.",
        "Переход от готического объёма к классическим пропорциям "
        "Палладио.",
        "Bridge from a Gothic shell to Palladio's classical "
        "proportions.",
    ),
    "sicilian_baroque_noto_cathedral": (
        "Фасад из местного известняка образует золотистую "
        "перспективу Via Nicolaci.",
        "Local limestone façades form Noto's golden street "
        "perspective on Via Nicolaci.",
        "Символ перестройки Вал-ди-Ното после катастрофы 1693 года.",
        "Emblem of Val di Noto's rebuilding after the 1693 disaster.",
    ),
    "sicilian_baroque_duomo_ragusa": (
        "Купол и фасад завершены по проекту Розарио Гальярди.",
        "Dome and façade were finished to Rosario Gagliardi's design.",
        "Доминирует над барочным силуэтом Рагузы-Ибла.",
        "Dominates the Baroque skyline of Ragusa Ibla.",
    ),
    "romantic_eclectic_galleria_umberto": (
        "Крестообразный план с куполом перекликается с миланской "
        "Галлерией Виктория Эммануэля II.",
        "Its cruciform plan and dome echo Milan's Galleria "
        "Vittorio Emanuele II.",
        "Железо и стекло как символ неаполитанской модернизации "
        "после объединения Италии.",
        "Iron and glass as a symbol of post-unification Naples.",
    ),
    "romanesque_san_zeno": (
        "Тройной портал украшен рельефами XII века.",
        "The triple portal bears twelfth-century reliefs.",
        "Главный романский храм Вероны.",
        "Verona's principal Romanesque church.",
    ),
    "norman_sicilian_martorana": (
        "Мозаики сочетают византийскую технику и арабские мотивы.",
        "Mosaics blend Byzantine technique with Arab motifs.",
        "Жемчужина палермитанского зодчества.",
        "Jewel of Palermitan architecture.",
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
