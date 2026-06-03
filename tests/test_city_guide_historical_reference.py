# -*- coding: utf-8 -*-
"""Historical reference section EN/RU parity."""

from __future__ import annotations

from scripts.city_guide_historical_reference_ru import (
    HISTORICAL_SECTION_TITLE_EN,
    historical_reference_section_html,
    reference_text_en_for_any_city,
    reference_text_ru_for_any_city,
)
from scripts.city_guide_translate import EditionTranslator, set_edition_translator


def test_bangkok_en_historical_via_ru_translate(monkeypatch) -> None:
    monkeypatch.delenv("CITY_GUIDE_NO_TRANSLATE", raising=False)

    class _FakeTranslator(EditionTranslator):
        def translate(self, text, *, src, dst, kind="prose"):  # type: ignore[override]
            assert src == "ru" and dst == "en"
            return "English historical overview for Bangkok."

    set_edition_translator(_FakeTranslator(enabled=True))
    try:
        ru = reference_text_ru_for_any_city("bangkok")
        assert "Бангкок" in ru
        en = reference_text_en_for_any_city("bangkok")
        assert en == "English historical overview for Bangkok."
        html = historical_reference_section_html(
            en,
            section_title=HISTORICAL_SECTION_TITLE_EN,
        )
        assert "Historical overview" in html
        assert "historical-reference" in html
    finally:
        set_edition_translator(None)
