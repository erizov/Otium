# -*- coding: utf-8 -*-
"""Tests for EN/RU place reconciliation."""

from __future__ import annotations

from scripts.city_guide_edition_reconcile import (
    detail_key_for_slug,
    reconcile_place_row,
)
from scripts.city_guide_sparse_narrative import place_edition_needs_fill


def test_detail_slug_alias_smolensk() -> None:
    keys = {"smolensk_dormition_cathedral", "smolensk_kremlin_wall"}
    assert detail_key_for_slug("smolensk", "dormition_cathedral", keys) == (
        "smolensk_dormition_cathedral"
    )
    assert detail_key_for_slug("smolensk", "smolensk_kremlin_wall", keys) == (
        "smolensk_kremlin_wall"
    )


def test_reconcile_merges_en_main_and_ru_details() -> None:
    place = {
        "slug": "dormition_cathedral",
        "description": "English overview of the cathedral.",
        "history": "Built over centuries.",
        "facts": ["English fact."],
    }
    detail = {
        "description": "Русское описание собора.",
        "history": "История на русском языке.",
        "facts": ["Русский факт."],
    }
    assert reconcile_place_row(place, detail)
    assert place["description_en"] == "English overview of the cathedral."
    assert place["description_ru"] == "Русское описание собора."
    assert not place_edition_needs_fill(place, "en")
    assert not place_edition_needs_fill(place, "ru")
