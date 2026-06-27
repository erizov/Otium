# -*- coding: utf-8 -*-
"""Curated place prose overrides."""

from __future__ import annotations

from typing import Any

from italian_architecture.data.thin_text_supplements import (
    apply_thin_text_supplements,
)

# slug -> (description_ru, description_en, history_ru, history_en,
#          significance_ru, significance_en)
_OVERRIDES: dict[str, tuple[str, str, str, str, str, str]] = {
    "high_renaissance_st_peters": (
        "Собор Святого Петра в Ватикане — главный храм "
        "католической Церкви и один из крупнейших церквей мира.",
        "St Peter's Basilica in Vatican City is the principal "
        "church of Catholicism and one of the largest churches "
        "ever built.",
        "Строительство началось в 1506 году по проекту "
        "Донато Браманте; позже над куполом и планом работали "
        "Рафаэль, Антонио да Сангалло Младший, Микеланджело, "
        "Джакомо делла Порта и Карло Мaderно. Фасад завершён "
        "в 1614 году, внутреннее убранство и площадь перед "
        "собором оформлялись до 1626 года.",
        "Work began in 1506 to Donato Bramante's design; "
        "Raphael, Antonio da Sangallo the Younger, Michelangelo, "
        "Giacomo della Porta and Carlo Maderno later shaped the "
        "dome and plan. The façade was finished in 1614 and the "
        "interior and forecourt by 1626.",
        "Купол Микеланджело задаёт силуэт Рима; собор "
        "символизирует триумф контрреформации и папского Рима.",
        "Michelangelo's dome defines the Roman skyline; the "
        "basilica embodies Counter-Reformation triumph and papal "
        "authority.",
    ),
    "romantic_eclectic_altare_patria": (
        "Отечественный алтарь на Пьяцца Венеция — "
        "монументальное здание из белого мрамора, "
        "посвящённое первому королю объединённой Италии.",
        "The Vittoriano on Piazza Venezia is a monumental "
        "white-marble complex dedicated to Victor Emmanuel II, "
        "first king of united Italy.",
        "Проект Giuseppe Sacconi выиграл конкурс 1885 года; "
        "строительство длилось до 1935 года с многочисленными "
        "доработками. Комплекс с колоннами, лестницами и "
        "конными группами закрывает восточный склон "
        "Капитолийского холма.",
        "Giuseppe Sacconi won the 1885 competition; building "
        "continued with revisions until 1935. Colonnades, "
        "stairways and equestrian sculpture cover the eastern "
        "Capitoline slope.",
        "Символ Risorgimento и национального пантеона; "
        "с террасы открывается панорама на Римский форум.",
        "Emblem of the Risorgimento and a national pantheon; "
        "its terraces overlook the Roman Forum.",
    ),
    "fascist_rationalism_palazzo_civilta": (
        "Дворец итальянской цивилизации в квартале EUR "
        "известен как «Квадратный Колизей» благодаря "
        "шести рядам арок.",
        "The Palazzo della Civiltà Italiana in EUR is nicknamed "
        "the Square Colosseum for its six tiers of arches.",
        "Здание спроектировали Giovanni Guerrini, Ernesto "
        "Bruno La Padula и Mario Romano; работы завершены "
        "в 1942 году для отложенной всемирной выставки. "
        "С 2015 года здесь размещается штаб-квартира Fendi.",
        "Giovanni Guerrini, Ernesto Bruno La Padula and Mario "
        "Romano designed it; construction finished in 1942 for "
        "a deferred world's fair. Fendi has headquartered here "
        "since 2015.",
        "Образец монументального neoclassical rationalism "
        "эпохи фашизма и визитная карточка EUR.",
        "A landmark of Fascist-era monumental rationalism and "
        "the icon of the EUR district.",
    ),
    "fascist_rationalism_colosseo_quadrato": (
        "Консульский дворец входит в ансамбль EUR — "
        "выставочного квартала, задуманного в 1930‑е годы.",
        "The Palazzo dei Congressi belongs to EUR, the "
        "exhibition quarter planned in the 1930s.",
        "Квартал строился для Всемирной выставки 1942 года; "
        "после войны EUR стал деловым и административным "
        "районом южного Рима. Консульский дворец принимает "
        "конгрессы и выставки рядом с «Квадратным Колизеем».",
        "EUR was prepared for a 1942 world's fair; after the "
        "war it became a business district. The congress palace "
        "hosts events beside the Square Colosseum.",
        "Показывает сочетание классических пропорций и "
        "модернистской планировки в итальянском "
        "razionalismo.",
        "Shows how classical proportions met modern planning "
        "in Italian Razionalismo.",
    ),
    "contemporary_maxxi": (
        "MAXXI — Национальный музей XXI века искусств в "
        "Риме, спроектированный Zaha Hadid.",
        "MAXXI is Rome's National Museum of 21st Century Arts, "
        "designed by Zaha Hadid.",
        "Музей открылся в 2010 году на месте бывших "
        "казарм Montello. Просторные бетонные ленты, "
        "перекрытия и мостики создают «потоковое» "
        "пространство для экспозиций и перформансов.",
        "It opened in 2010 on a former Montello barracks site. "
        "Flowing concrete bands, bridges and ramps create "
        "continuous gallery space for exhibitions and events.",
        "Первый в Италии музей, посвящённый только "
        "современному искусству и архитектуре.",
        "Italy's first museum devoted exclusively to "
        "contemporary art and architecture.",
    ),
    "contemporary_snfcc": (
        "Национальный центр современного искусства в "
        "руководстве — культурный комплекс эпохи "
        "urban regeneration в Риме.",
        "The National Centre for Contemporary Arts in the "
        "guide marks a cultural hub of Rome's recent "
        "urban renewal.",
        "Проект связан с развитием Flaminio и музейной "
        "инфраструктурой после MAXXI. Здание Hadid "
        "демонстрирует динамичные пересечения "
        "пространств и световые шлюзы.",
        "The scheme belongs to Flaminio's regeneration and "
        "Rome's new museum infrastructure after MAXXI. "
        "Hadid's building uses intersecting routes and "
        "top-lighted galleries.",
        "Расширяет карту современной архитектуры "
        "итальянской столицы.",
        "Extends the map of contemporary architecture in "
        "the capital.",
    ),
    "early_renaissance_rome_villa_farnesina_2": (
        "Вилла Фарнезина на Тибре — элегантная "
        "резиденция раннего XVI века с фресками "
        "высокого класса.",
        "Villa Farnesina on the Tiber is an elegant early "
        "sixteenth-century villa with outstanding frescoes.",
        "Около 1510 года Agostino Chigi поручил постройку "
        "Baldassare Peruzzi; Raphael, Sebastiano del Piombo "
        "и Sodoma расписали залы мифологическими "
        "сюжетами. Вилла сохранила гармонию архитектуры "
        "и живописи эпохи Высокого Возрождения.",
        "Around 1510 Agostino Chigi commissioned Baldassare "
        "Peruzzi; Raphael, Sebastiano del Piombo and Sodoma "
        "painted mythological cycles in its rooms. The villa "
        "preserves High Renaissance unity of architecture "
        "and painting.",
        "Galatea Raphael и «триумф» Galatea — эталон "
        "светского искусства papal Rome.",
        "Raphael's Galatea and the Loggia frescoes are "
        "landmarks of secular papal Rome.",
    ),
    "early_renaissance_rome_quirinal_palace_2": (
        "Квиринальский дворец на одноимённом холме — "
        "официальная резиденция президента Италии.",
        "The Quirinal Palace on its namesake hill is the "
        "official residence of the President of Italy.",
        "Папы Римские расширяли дворец с 1583 года; "
        "после объединения Италии здесь жили короли, "
        "а с 1946 года — президенты. Государственные "
        "залы и сады открываются для экскурсий в "
        "отдельные дни.",
        "Popes enlarged the palace from 1583; Italian kings "
        "lived here after unification and presidents since "
        "1946. State rooms and gardens open for tours on "
        "selected days.",
        "Смена караула у дворца — популярное "
        "представление; ансамбль отражает "
        "четыре столетия придворной жизни.",
        "The changing of the guard draws visitors; the "
        "ensemble reflects four centuries of court life.",
    ),
    "baroque_rome_santa_maria_sopra_minerva_2": (
        "Санта‑Мария‑сопра‑Минерва — единственный "
        "готический зал в Риме с богатым "
        "барокко внутри.",
        "Santa Maria sopra Minerva is Rome's only "
        "Gothic-aisled church, richly furnished in "
        "the Baroque era.",
        "Доминиканский конvent вырос на месте храма "
        "Минервы. Капеллы украшали Filippo Lippi, "
        "Melozzo da Forlì и другие; внутри стоит "
        "«Христос‑носитель» Микеланджelo. Перед "
        "фасадом — obelisk на спине слона Bernini.",
        "A Dominican convent rose over a temple of Minerva. "
        "Chapels were enriched by Filippo Lippi and Melozzo "
        "da Forlì; Michelangelo's Christ the Redeemer "
        "stands inside. Bernini's elephant obelisk fronts "
        "the church.",
        "Тихий контраст с соседним Пантеоном и "
        "площадью della Minerva.",
        "A quiet contrast to the nearby Pantheon and "
        "Piazza della Minerva.",
    ),
    "baroque_rome_galleria_borghese_2": (
        "Галерея Боргезе в вилле XVII века хранит "
        "шедевры Bernini и Caravaggio.",
        "The Galleria Borghese in a seventeenth-century "
        "villa holds masterpieces by Bernini and Caravaggio.",
        "Scipione Borghese поручил виллу Flaminio Ponzio "
        "и Giovanni Vasanzio; в залах установлены "
        "«Аполлон и Дафна», «Плутон и Прозерпина» и "
        "«Давид» Bernini. Часть коллекции ушла в Лувр "
        "при Napoleone.",
        "Scipione Borghese commissioned Flaminio Ponzio and "
        "Giovanni Vasanzio; Bernini's Apollo and Daphne, "
        "Pluto and Proserpina and David were made for these "
        "rooms. Napoleonic pressures sent some antiquities "
        "to the Louvre.",
        "Вход по двухчасовым сеансам — бронируйте "
        "заранее в сезон.",
        "Timed two-hour entries limit crowds—book well "
        "ahead in peak season.",
    ),
    "neoclassicism_florence_mercato_centrale_2": (
        "Mercato Centrale — стеклянный рыночный зал 1914 года "
        "в квартале San Lorenzo.",
        "Mercato Centrale is a 1914 glass-and-brick market "
        "hall in Florence's San Lorenzo quarter.",
        "Giuseppe Martelli спроектировал здание после "
        "разрушения старого рынка в Первую мировую. "
        "Сталь, стекло и ар‑нуво‑детали создают "
        "светлый интерьер с лавками тосканской кухни.",
        "Giuseppe Martelli designed it after the old market "
        "was lost in World War I. Steel, glass and Art "
        "Nouveau ornament create a bright hall of Tuscan "
        "food stalls.",
        "Образец гражданской архитектуры между "
        "liberty и modernism во Флоренции.",
        "A civic landmark bridging Liberty and modern "
        "architecture in Florence.",
    ),
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
    if not override:
        return apply_thin_text_supplements(place)
    merged = dict(place)
    for key, value in override.items():
        if value:
            merged[key] = value
    if override.get("description_ru"):
        merged["description"] = override["description_ru"]
    if override.get("history_ru"):
        merged["history"] = override["history_ru"]
    if override.get("significance_ru"):
        merged["significance"] = override["significance_ru"]
    return apply_thin_text_supplements(merged)


def max_sentences_for_slug(slug: str) -> int | None:
    """Optional per-slug narrative length cap."""
    return None
