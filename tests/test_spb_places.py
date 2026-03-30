# -*- coding: utf-8 -*-

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from spb.data.places_registry import SPB_PLACES  # noqa: E402
from scripts.build_spb_pdf import _chapter_heading, _ru_count_phrase  # noqa: E402


def test_spb_places_minimum_v1_count() -> None:
    assert len(SPB_PLACES) >= 100


def test_each_place_has_required_image_fields() -> None:
    for p in SPB_PLACES:
        assert p.get("slug")
        assert p.get("category")
        assert p.get("name_ru")
        assert p.get("image_rel_path")
        assert p.get("image_source_url")


def test_chapter_heading_sculptures_plural() -> None:
    h2, sub = _chapter_heading("sculptures", 3)
    assert "Скульптуры и памятники" in h2
    assert "Санкт-Петербурга" in h2
    assert sub == "3 скульптуры и памятника"


def test_ru_plural_museums_phrase() -> None:
    assert _ru_count_phrase(5, "музей", "музея", "музеев") == "5 музеев"
    assert _ru_count_phrase(1, "музей", "музея", "музеев") == "1 музей"


def test_winter_palace_merged_details() -> None:
    wp = next(p for p in SPB_PLACES if p.get("slug") == "winter_palace")
    assert wp.get("address")
    assert wp.get("history")
