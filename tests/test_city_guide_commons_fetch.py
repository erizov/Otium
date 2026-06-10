# -*- coding: utf-8 -*-
"""Tests for city-scoped Wikimedia Commons image resolution."""

from __future__ import annotations

from scripts.city_guide_commons_fetch import _text_matches_city
from scripts.city_guide_commons_fetch import commons_city_file_tokens


def test_commons_city_file_tokens_volgograd() -> None:
    tokens = commons_city_file_tokens("volgograd")
    assert "volgograd" in tokens
    assert "stalingrad" in tokens


def test_moscow_kazan_filename_not_volgograd() -> None:
    moscow = commons_city_file_tokens("moscow")
    volgograd = commons_city_file_tokens("volgograd")
    name = "Cathedral_of_Our_Lady_of_Kazan_1.jpg"
    assert _text_matches_city(name, moscow) is False
    assert _text_matches_city(name, volgograd) is False


def test_volgograd_kazan_snippet_matches() -> None:
    volgograd = commons_city_file_tokens("volgograd")
    blob = (
        "Kazan Cathedral 2014-01-22.jpg "
        "… Kazan Cathedral in Volgograd, Russia …"
    )
    assert _text_matches_city(blob, volgograd) is True
