# -*- coding: utf-8 -*-
"""Tests for sparse narrative fill detection and Pixabay fallback."""

from __future__ import annotations

from scripts.city_guide_sparse_narrative import (
    compose_en_from_pixabay_hints,
    place_edition_needs_fill,
    ProviderCircuitBreaker,
)


def test_sparse_ru_landmark_stub_detected() -> None:
    place = {
        "name_ru": "Scala Cinema",
        "description_ru": "Scala Cinema — достопримечательность в Бангкоке.",
    }
    assert place_edition_needs_fill(place, "ru")


def test_sparse_stub_detected_en() -> None:
    place = {
        "name_en": "ICONSIAM",
        "description": "ICONSIAM — landmark in Bangkok.",
    }
    assert place_edition_needs_fill(place, "en")


def test_rich_place_not_sparse() -> None:
    place = {
        "description": (
            "Orange-flag express boats skip-stop between old city wats."
        ),
        "facts": ["Tourist boats cost more but add narration."],
        "history": "Canal city logistics moved toward motorised ferries.",
    }
    assert not place_edition_needs_fill(place, "en")


def test_compose_en_from_pixabay_hints() -> None:
    place = {"name_en": "Scala Cinema", "category": "landmarks"}
    data = compose_en_from_pixabay_hints(
        place,
        "bangkok",
        {"tags": "cinema, bangkok, art deco", "page_url": "https://ex.example"},
    )
    assert "Scala Cinema" in data["description"]
    assert "cinema" in data["history"].lower()
    assert data["facts"]


def test_provider_circuit_breaker_suspends_after_three_failures() -> None:
    breaker = ProviderCircuitBreaker(fail_threshold=3, suspend_places=1000)
    assert breaker.allowed("openai")

    breaker.record_failure("openai")
    breaker.record_failure("openai")
    assert breaker.allowed("openai")

    breaker.record_failure("openai")
    assert not breaker.allowed("openai")
    assert breaker.suspension_left("openai") == 1000

    breaker.on_new_place()
    assert breaker.suspension_left("openai") == 999

    for _ in range(999):
        breaker.on_new_place()
    assert breaker.allowed("openai")


def test_translate_failures_count_per_attempt(monkeypatch) -> None:
    """
    Each failed Ollama translate attempt should count toward suspension.
    """
    from scripts.city_guide_sparse_narrative import fill_edition_from_opposite
    from scripts.city_guide_translate import EditionTranslator

    class _AlwaysFailTranslator(EditionTranslator):
        def translate(self, text, *, src, dst, kind="prose"):  # type: ignore[override]
            return None

    breaker = ProviderCircuitBreaker(fail_threshold=3, suspend_places=1000)
    place = {
        "description": "English description.",
        "history": "English history.",
        "significance": "English significance.",
    }
    changed = fill_edition_from_opposite(
        place,
        "ru",
        translator=_AlwaysFailTranslator(enabled=True),
        breaker=breaker,
        delay=0.0,
    )
    assert not changed
    assert not breaker.allowed("ollama_translate")


def test_ollama_500_suspends_forever(monkeypatch) -> None:
    from scripts.city_guide_sparse_narrative import fill_edition_from_opposite
    from scripts.city_guide_sparse_narrative import ProviderCircuitBreaker
    from scripts.city_guide_translate import EditionTranslator, OllamaFatalError

    class _FatalTranslator(EditionTranslator):
        def translate(self, text, *, src, dst, kind="prose"):  # type: ignore[override]
            raise OllamaFatalError("Ollama server error 500")

    breaker = ProviderCircuitBreaker(fail_threshold=3, suspend_places=1000)
    place = {"description": "English description."}
    changed = fill_edition_from_opposite(
        place,
        "ru",
        translator=_FatalTranslator(enabled=True),
        breaker=breaker,
        delay=0.0,
    )
    assert not changed
    assert not breaker.allowed("ollama_translate")
    assert breaker.suspension_left("ollama_translate") >= 10**6
