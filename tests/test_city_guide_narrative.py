# -*- coding: utf-8 -*-
"""Tests for merged place narrative rendering."""

from __future__ import annotations

import re

from scripts.city_guide_naming import clean_wikimedia_display_title
from scripts.city_guide_narrative import (
    GuideNarrativeDeduper,
    clean_pixabay_artifacts,
    group_into_paragraphs,
    is_pixabay_stub,
    is_reference_boilerplate,
    is_usable_narrative_text,
    merge_narrative_html,
    narrative_sentence_blocks,
    place_heading_plain,
    text_for_edition,
)


def test_text_for_edition_en_ru() -> None:
    assert text_for_edition("Neo-Gothic revival facade.", "en")
    assert not text_for_edition("Neo-Gothic revival facade.", "ru")
    assert text_for_edition("Неоготический фасад.", "ru")
    assert not text_for_edition("Неоготический фасад.", "en")
    assert text_for_edition("1850–1870", "en")
    assert text_for_edition("1850–1870", "ru")


def test_merge_narrative_drops_section_headings_and_dupes() -> None:
    place = {
        "description": "The gate faces Paris. It marks unity.",
        "facts": ["It marks unity.", "Bronze quadriga crowns the attic."],
        "history": "Built in the late eighteenth century.",
        "significance": "The gate faces Paris.",
    }
    html = merge_narrative_html(place, "en", GuideNarrativeDeduper())
    assert "<h4>" not in html
    assert "Facts and details" not in html
    assert html.count("The gate faces Paris.") == 1
    assert "Bronze quadriga" in html
    assert "late eighteenth century" in html


def test_ru_edition_excludes_english_body() -> None:
    place = {
        "description": "English overview only.",
        "description_ru": "Краткое описание на русском.",
        "history": "English history.",
        "history_ru": "История на русском языке.",
    }
    blocks = narrative_sentence_blocks(place, "ru")
    flat = " ".join(" ".join(b) for b in blocks)
    assert "English" not in flat
    assert "русском" in flat


def test_cross_edition_fallback_with_mock_translator(monkeypatch) -> None:
    monkeypatch.delenv("CITY_GUIDE_NO_TRANSLATE", raising=False)
    from scripts.city_guide_translate import EditionTranslator, set_edition_translator

    class _FakeTranslator(EditionTranslator):
        def translate(self, text, *, src, dst, kind="prose"):  # type: ignore[override]
            if dst == "ru":
                return "Русское название" if kind == "name" else "Русский текст."
            return "English name" if kind == "name" else "English text."

    set_edition_translator(_FakeTranslator(enabled=True))
    try:
        place = {
            "name_en": "Hotel W Barcelona",
            "description": "Modern hotel on the seafront.",
            "history": "Opened in 2018.",
        }
        assert place_heading_plain(place, "ru") == "Русское название"
        html = merge_narrative_html(place, "ru", GuideNarrativeDeduper())
        assert "Русский текст." in html
        assert "Modern hotel" not in html
    finally:
        set_edition_translator(None)


def test_two_paragraphs_when_rich() -> None:
    overview = ["One.", "Two.", "Three.", "Four."]
    context = ["Five.", "Six.", "Seven."]
    paras = group_into_paragraphs(overview, context)
    assert len(paras) == 2
    assert paras[0].startswith("One.")
    assert "Seven." in paras[1]


def test_mixed_script_rejected_for_ru() -> None:
    assert not text_for_edition(
        "The Kyiv Lavra (Ukrainian: Києво-Печерська лавра).",
        "ru",
    )
    assert text_for_edition(
        "Києво-Печерська лавра — православний монастирський ансамбль.",
        "ru",
    )


def test_guide_deduper_across_places() -> None:
    deduper = GuideNarrativeDeduper()
    first = merge_narrative_html(
        {"description": "Shared sentence across two cards."},
        "en",
        deduper,
    )
    second = merge_narrative_html(
        {"description": "Shared sentence across two cards."},
        "en",
        deduper,
    )
    assert "Shared sentence" in first
    assert second == ""


def test_en_landmark_stub_not_rendered() -> None:
    place = {
        "name_en": "ICONSIAM",
        "description": "ICONSIAM — landmark in Bangkok.",
    }
    html = merge_narrative_html(place, "en", GuideNarrativeDeduper())
    assert html == ""
    assert not text_for_edition("ICONSIAM — landmark in Bangkok.", "en")


def test_historic_landmark_stub_not_rendered() -> None:
    place = {
        "description": (
            "Golden Gate is a historic and cultural landmark in Kyiv."
        ),
    }
    html = merge_narrative_html(place, "en", GuideNarrativeDeduper())
    assert "landmark in Kyiv" not in html
    assert html == ""


def test_mixed_stub_and_real_keeps_real_only() -> None:
    place = {
        "description": (
            "Carmo Convent ruins — landmark in Lisbon. "
            "Elevador de Santa Justa lands almost at the gate."
        ),
    }
    html = merge_narrative_html(place, "en", GuideNarrativeDeduper())
    assert "landmark in Lisbon" not in html
    assert "Elevador de Santa Justa" in html


def test_ru_landmark_stub_not_rendered() -> None:
    place = {
        "name_ru": "Мечеть Тон Сон",
        "description_ru": "Мечеть Тон Сон — достопримечательность в Бангкоке.",
    }
    html = merge_narrative_html(place, "ru", GuideNarrativeDeduper())
    assert html == ""
    assert not text_for_edition(
        "Мечеть Тон Сон — достопримечательность в Бангкоке.",
        "ru",
    )


def test_ru_landmark_stub_only_description_empty() -> None:
    place = {
        "description_ru": "Scala Cinema — знаковая достопримечательность Бангкока.",
    }
    html = merge_narrative_html(place, "ru", GuideNarrativeDeduper())
    assert "достопримечательность" not in html
    assert html == ""


def test_landmark_stub_skipped_when_facts_exist() -> None:
    place = {
        "description": "ICONSIAM — landmark in Bangkok.",
        "facts": [
            "Check opening hours and ticketing on official sites before travel.",
            "Riverfront mall with evening light shows on the Chao Phraya.",
        ],
        "history": "Opened as a mixed-use retail anchor in 2018.",
        "significance": "Signature skyline shopping destination.",
    }
    html = merge_narrative_html(place, "en", GuideNarrativeDeduper())
    assert "landmark in Bangkok" not in html
    assert "Riverfront mall" in html
    assert "2018" in html
    assert "Check opening hours" not in html


def test_chao_phraya_merges_facts_history_significance() -> None:
    place = {
        "description": (
            "Orange-flag express boats skip-stop between old city wats "
            "and modern hotels—cheap deck seating with river breeze."
        ),
        "facts": [
            "Tourist boats cost more but add narration and fewer transfers.",
            "Evening ICONSIAM ferries link shopping malls with light shows.",
        ],
        "history": (
            "Canal city logistics moved toward motorised ferries as roads "
            "choked; river remains a commuter spine."
        ),
        "significance": (
            "The scenic spine tying Wat Arun, Tha Tien, and Sathorn piers."
        ),
    }
    html = merge_narrative_html(place, "en", GuideNarrativeDeduper())
    assert "Orange-flag express boats" in html
    assert "Tourist boats cost more" in html
    assert "ICONSIAM ferries" in html
    assert "motorised ferries" in html
    assert "Wat Arun" in html


def test_clean_wikimedia_titles() -> None:
    assert clean_wikimedia_display_title("Scala Cinema (I).jpg") == "Scala Cinema"
    assert (
        clean_wikimedia_display_title("St Louis Church Bangkok 2018 02.jpg")
        == "St Louis Church Bangkok"
    )
    assert clean_wikimedia_display_title("Ton Son Mosque (I).jpg") == "Ton Son Mosque"
    assert (
        clean_wikimedia_display_title(
            "Amsterdam (NL), Koninklijk Paleis -- 2015 -- 7193.jpg",
        )
        == "Koninklijk Paleis"
    )
    assert (
        clean_wikimedia_display_title("Amsterdam photochrom2.jpg")
        == "Amsterdam photochrom"
    )
    assert (
        clean_wikimedia_display_title("Amsterdam Royal Palace 1699.jpg")
        == "Amsterdam Royal Palace"
    )


def test_dedupe_pdf_sidecar_drops_duplicate_headings() -> None:
    from scripts.city_guide_core import dedupe_pdf_sidecar_places

    places = [
        {
            "slug": "amsterdam_noorderkerk",
            "name_en": "Noorderkerk",
            "image_rel_path": "images/amsterdam_noorderkerk.jpg",
        },
        {
            "slug": "amsterdam_pdfband_1_abc",
            "name_en": "Noorderkerk.jpg",
            "image_rel_path": "images/amsterdam_pdfband_1.jpg",
        },
    ]
    out = dedupe_pdf_sidecar_places(places, city_slug="amsterdam")
    assert len(out) == 1
    assert out[0]["slug"] == "amsterdam_noorderkerk"


def test_dedupe_curated_drops_city_suffix_heading_dupes() -> None:
    from scripts.city_guide_core import dedupe_curated_places

    url = (
        "https://upload.wikimedia.org/wikipedia/commons/1/1a/"
        "Assumption_Cathedral_in_Yaroslavl_01.jpg"
    )
    places = [
        {
            "slug": "yaroslavl_assumption_cathedral",
            "name_en": "Assumption Cathedral",
            "image_source_url": url,
        },
        {
            "slug": "yaroslavl_assumption_ext",
            "name_en": "Assumption Cathedral",
            "image_source_url": url,
        },
        {
            "slug": "yaroslavl_assumption",
            "name_en": "Assumption Cathedral Yaroslavl",
            "image_source_url": url,
        },
    ]
    out = dedupe_curated_places(places, "yaroslavl")
    assert len(out) == 1
    assert out[0]["slug"] == "yaroslavl_assumption_cathedral"


def test_en_heading_does_not_fall_back_to_cyrillic() -> None:
    place = {
        "slug": "moscow_monasteries_0",
        "name_ru": "Спасо-Андроников монастырь",
        "name_en": "",
    }
    heading = place_heading_plain(place, "en")
    assert heading != "Спасо-Андроников монастырь"
    assert heading == "Monasteries 0"


def test_place_heading_from_slug() -> None:
    from scripts.city_guide_naming import title_from_place_slug

    assert title_from_place_slug("dubai_gold_souk") == "Dubai Gold Souk"
    place = {"slug": "dubai_gold_souk"}
    assert place_heading_plain(place, "en") == "Dubai Gold Souk"
    assert place_heading_plain(place, "ru") == "Dubai Gold Souk"


def test_descriptive_place_slug_from_title() -> None:
    from scripts.city_guide_naming import descriptive_place_slug

    used: set[str] = {"berlin_brandenburg_gate"}
    slug = descriptive_place_slug(
        "berlin",
        "141227 Berliner Dom.jpg",
        used,
    )
    assert slug == "berlin_berliner_dom"
    assert "pdfband" not in slug
    slug2 = descriptive_place_slug("berlin", "Berliner Dom", used | {slug})
    assert slug2 == "berlin_berliner_dom_2"
    slug3 = descriptive_place_slug(
        "dubai",
        "Dubai (19225459).jpeg",
        set(),
    )
    assert slug3 == "dubai_landmark"
    assert not re.search(r"\d{7,}", slug3)
    slug4 = descriptive_place_slug(
        "dubai",
        "Downtown Montreal (8392011668).jpg",
        {slug3},
    )
    assert slug4 == "dubai_downtown_montreal"
    assert not re.search(r"\d{7,}", slug4)


def test_clean_place_display_title_strips_asset_ids() -> None:
    from scripts.city_guide_naming import clean_place_display_title

    assert clean_place_display_title("Dubai (19225459).jpeg") == "Dubai"
    assert (
        clean_place_display_title("Downtown Montreal (8392011668).jpg")
        == "Downtown Montreal"
    )
    assert clean_place_display_title("141227 Berliner Dom") == "Berliner Dom"


def test_place_meta_line_address_vs_location() -> None:
    from scripts.city_guide_narrative import place_meta_line

    labels = {"style": "Style:", "period": "Period:"}
    museum = {
        "category": "museums",
        "address": "ул. Волхонка, 12",
        "visit_hours_ru": "вт–вс 11:00–20:00",
    }
    meta = place_meta_line(museum, "ru", labels)
    assert meta is not None
    assert "Адрес:" in meta
    assert "ул. Волхонка, 12" in meta
    assert "Часы работы:" in meta
    monument = {
        "category": "sculptures",
        "location": "Красная пл.",
    }
    meta2 = place_meta_line(monument, "ru", labels)
    assert meta2 is not None
    assert "Место:" in meta2
    assert "Адрес:" not in meta2
    metro = {
        "category": "metro",
        "metro_line": "Замоскворецкая линия (зелёная)",
        "location": "Триумфальная пл.",
    }
    meta3 = place_meta_line(metro, "ru", labels)
    assert meta3 is not None
    assert "Линия:" in meta3
    assert "Место:" in meta3
    assert "Адрес:" not in meta3


def test_pdfband_heading_uses_cleaned_name_not_slug() -> None:
    place = {
        "slug": "chernivtsi_pdfband_10_99e791d5",
        "name_en": "Будинок з левами.jpg",
        "subtitle_en": "Будинок з левами.jpg",
    }
    assert place_heading_plain(place, "en") == "Будинок з левами"
    assert place_heading_plain(place, "ru") == "Будинок з левами"


def test_pdfband_slug_fallback_without_name() -> None:
    from scripts.city_guide_naming import title_from_pdf_filler_slug

    assert title_from_pdf_filler_slug(
        "chernivtsi_pdfband_10_99e791d5",
    ) == "Chernivtsi"
    place = {"slug": "chernivtsi_pdfband_10_99e791d5"}
    assert place_heading_plain(place, "en") == "Chernivtsi"


def test_place_heading_strips_filename_artifacts() -> None:
    place = {
        "name_en": "Scala Cinema (I).jpg",
        "subtitle_en": "Scala Cinema (I).jpg",
    }
    assert place_heading_plain(place, "en") == "Scala Cinema"


def test_subtitle_hidden_when_same_as_heading() -> None:
    from scripts.city_guide_narrative import subtitle_html_for_edition

    place = {
        "name_en": "Scala Cinema (I).jpg",
        "subtitle_en": "Scala Cinema (I).jpg",
    }
    assert subtitle_html_for_edition(place, "en") == ""


def test_en_ru_dedupe_parity_with_translation_keys() -> None:
    from scripts.city_guide_translate import EditionTranslator, set_edition_translator

    class _FakeTranslator(EditionTranslator):
        def translate(self, text, *, src, dst, kind="prose"):  # type: ignore[override]
            if dst == "ru":
                return "Русский: " + text
            return "English: " + text

    set_edition_translator(_FakeTranslator(enabled=True))
    try:
        shared = {
            "description": "Shared sentence across two cards.",
        }
        en_ded = GuideNarrativeDeduper()
        ru_ded = GuideNarrativeDeduper()
        first_en = merge_narrative_html(shared, "en", en_ded)
        second_en = merge_narrative_html(shared, "en", en_ded)
        first_ru = merge_narrative_html(shared, "ru", ru_ded)
        second_ru = merge_narrative_html(shared, "ru", ru_ded)
        assert "Shared sentence" in first_en
        assert second_en == ""
        assert "Русский:" in first_ru
        assert second_ru == ""
    finally:
        set_edition_translator(None)


def test_pixabay_stub_detection_and_cleaning() -> None:
    stub = (
        "Photo tags: church, tower. "
        "Reference image context: https://pixabay.com/photos/foo/"
    )
    assert is_pixabay_stub(stub)
    assert clean_pixabay_artifacts(stub) == ""
    minimal = "St Paul's is a church in London."
    assert is_pixabay_stub(minimal)
    real = (
        "St Paul's Cathedral dominates the City skyline. "
        "Photo tags: dome, church."
    )
    assert not is_pixabay_stub(real)
    cleaned = clean_pixabay_artifacts(real)
    assert "Photo tags" not in cleaned
    assert "St Paul's Cathedral" in cleaned


def test_guide_illustration_meta_cleaning() -> None:
    text = (
        "Особняк купца Будникова конца XIX века. "
        "Иллюстрации в гиде — локальные снимки Smolensk_Budnikov*."
    )
    cleaned = clean_pixabay_artifacts(text)
    assert "Иллюстрации в гиде" not in cleaned
    assert cleaned.startswith("Особняк купца")
    inline = (
        "Свято-Троицкий монастырь: ансамбль с собором; "
        "на иллюстрации — общий вид обители."
    )
    cleaned_inline = clean_pixabay_artifacts(inline)
    assert "на иллюстрации" not in cleaned_inline
    assert cleaned_inline.endswith("собором")
    fact = "На иллюстрации — кадр серии Commons 2013 года."
    assert clean_pixabay_artifacts(fact) == ""
    extra = (
        "Режим работы магазина лучше уточнять на сайте. "
        "Дополнительный кадр в гиде — локальный снимок Smolensk_Knigi1."
    )
    cleaned_extra = clean_pixabay_artifacts(extra)
    assert "Дополнительный кадр" not in cleaned_extra
    assert cleaned_extra.endswith("на сайте")
    assert clean_pixabay_artifacts(
        "Дополнительные кадры в гиде — ещё два исторических вида крепости",
    ) == ""
    bridge = (
        "Пешим туристам удобнее смотреть мост с набережной. "
        "Дополнительный кадр — современный вид мостов через Днепр (Commons, 2013)."
    )
    cleaned_bridge = clean_pixabay_artifacts(bridge)
    assert "Дополнительный кадр" not in cleaned_bridge
    assert cleaned_bridge.endswith("набережной")
    park = (
        "Городской парк с аллеями и прудами; "
        "в гиде — семнадцать локальных кадров Smolensk_Lopatinskiy*."
    )
    cleaned_park = clean_pixabay_artifacts(park)
    assert "в гиде" not in cleaned_park
    assert cleaned_park.endswith("прудами")
    assert clean_pixabay_artifacts(
        "Фото в гиде — сам монумент в красном граните; "
        "виды площади перенесены в карточку театра",
    ) == ""
    fountain = "Работает сезонно; в гиде — локальные кадры"
    cleaned_fountain = clean_pixabay_artifacts(fountain)
    assert "в гиде" not in cleaned_fountain
    assert cleaned_fountain == "Работает сезонно"
    commons = (
        "Фасад с проспекта Ленина (Commons) и дополнительный кадр."
    )
    cleaned_commons = clean_pixabay_artifacts(commons)
    assert "(Commons)" not in cleaned_commons
    assert cleaned_commons.startswith("Фасад с проспекта")
    assert clean_pixabay_artifacts(
        "Иллюстрация — летний ракурс (Commons: «Памятник…»)",
    ) == ""
    obelisk = (
        "Обелиск в честь защитников; на Commons отнесён к мемориалу в парке"
    )
    cleaned_obelisk = clean_pixabay_artifacts(obelisk)
    assert "Commons" not in cleaned_obelisk
    assert cleaned_obelisk.endswith("защитников")


def test_reference_boilerplate_detection() -> None:
    book = (
        "Елена Юрьевна Крижевская Москва изнутри. "
        "Серия «Искусство с блогерами» "
        "Текст предоставлен издательством h p://www.li res.ru/pages/biblio_book/ "
        "ISBN 978-5-04-108335-9 Аннотация «Москва изнутри» с Еленой Крижевской"
    )
    assert is_reference_boilerplate(book)
    assert not is_usable_narrative_text(book)
    toc = (
        "Донской пр-д, д. 9 Центросоюз (Росстат), ул. Мясницкая, д. 39 "
        "571 Дом Мельникова, Кривоарбатский пер., д. 10 575 Клуб Русакова, "
        "581 Клуб Зуева, ул. Лесная, д. 18 583 9. Сталинская архитектура "
        "585 МГУ, ул. Ленинские Горы, д. 1 590 МИД"
    )
    assert is_reference_boilerplate(toc)
    real = (
        "Дом Пашкова на Воздвиженке — один из лучших образцов "
        "классицизма в Москве; построен в XVIII веке."
    )
    assert not is_reference_boilerplate(real)


def test_split_sentences_preserves_initials() -> None:
    from scripts.city_guide_narrative import split_sentences

    sents = split_sentences("Архитектор — В. И. Баженов.")
    assert sents == ["Архитектор — В. И. Баженов."]
    joined = split_sentences(
        "Архитектор — В. И. Баженов. С 2007 — отдел рукописей РГБ.",
    )
    assert joined == [
        "Архитектор — В. И. Баженов.",
        "С 2007 — отдел рукописей РГБ.",
    ]
