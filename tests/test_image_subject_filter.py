# -*- coding: utf-8 -*-
"""Tests for offline person/animal subject filter."""

from __future__ import annotations

import os

import pytest

from scripts.image_subject_filter import check_image_bytes
from scripts.image_subject_filter import evaluate_detections
from scripts.image_subject_filter import subject_filter_enabled


def test_evaluate_rejects_large_centered_person() -> None:
    dets = [(0, 25.0, 25.0, 75.0, 75.0, 0.9)]
    result = evaluate_detections(dets, 100, 100)
    assert not result.accept
    assert result.reason == "person_main"


def test_evaluate_accepts_tiny_person() -> None:
    dets = [(0, 0.0, 0.0, 5.0, 5.0, 0.9)]
    result = evaluate_detections(dets, 100, 100)
    assert result.accept


def test_evaluate_rejects_crowd() -> None:
    dets = [
        (0, 0.0, 0.0, 20.0, 20.0, 0.9),
        (0, 25.0, 0.0, 45.0, 20.0, 0.9),
        (0, 50.0, 0.0, 70.0, 20.0, 0.9),
    ]
    result = evaluate_detections(dets, 100, 100)
    assert not result.accept
    assert result.reason == "crowd"


def test_evaluate_rejects_animal_main() -> None:
    dets = [(16, 10.0, 10.0, 90.0, 90.0, 0.9)]
    result = evaluate_detections(dets, 100, 100)
    assert not result.accept
    assert result.reason == "animal_main"


def test_check_bytes_disabled_explicitly() -> None:
    os.environ["SUBJECT_FILTER"] = "0"
    assert not subject_filter_enabled()
    tiny = b"\xff\xd8\xff" + b"\x00" * 600
    assert check_image_bytes(tiny).accept


def test_check_bytes_enabled_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SUBJECT_FILTER", raising=False)
    assert subject_filter_enabled()


def test_check_bytes_fail_open_without_model(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from io import BytesIO

    from PIL import Image

    monkeypatch.setenv("SUBJECT_FILTER", "1")
    monkeypatch.setenv("SUBJECT_FILTER_FAIL_OPEN", "1")
    monkeypatch.setattr(
        "scripts.image_subject_filter.detect_person_animal_boxes",
        lambda _img: [],
    )
    monkeypatch.setattr(
        "scripts.image_subject_filter._get_session",
        lambda: None,
    )
    buf = BytesIO()
    Image.new("RGB", (64, 64), color=(120, 80, 40)).save(buf, format="JPEG")
    assert check_image_bytes(buf.getvalue()).accept
