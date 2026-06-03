# -*- coding: utf-8 -*-
"""Tests for hardened Ollama translation path."""

from __future__ import annotations

import types


def test_ollama_failure_does_not_raise(monkeypatch) -> None:
    """
    When Ollama is configured but unreachable, translate should return None,
    not raise (so sparse-fill can continue).
    """

    class _FakeRequestException(Exception):
        pass

    fake_requests = types.SimpleNamespace()
    fake_requests.RequestException = _FakeRequestException

    def _post(*_args, **_kwargs):
        raise _FakeRequestException("connection refused")

    fake_requests.post = _post

    monkeypatch.setitem(__import__("sys").modules, "requests", fake_requests)
    monkeypatch.setenv("USE_OLLAMA", "1")
    monkeypatch.setenv("OLLAMA_HOST", "http://127.0.0.1:11434")

    from scripts.city_guide_translate import OllamaOnlyEditionTranslator
    from scripts.city_guide_translate import translate_for_edition

    tr = OllamaOnlyEditionTranslator(enabled=True)
    assert (
        translate_for_edition(
            "English text.",
            "ru",
            translator=tr,
        )
        is None
    )

