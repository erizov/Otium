# -*- coding: utf-8 -*-
"""Tests for city guide table of contents."""

from __future__ import annotations

from pathlib import Path

from scripts.city_guide_toc import (
    GuideTocEntry,
    category_chapter_anchor,
    guide_toc_html,
    guide_toc_title,
    toc_entries_for_flat_places,
    toc_entries_for_jerusalem_guide,
)


def test_guide_toc_title_localized() -> None:
    assert guide_toc_title("en") == "Contents"
    assert guide_toc_title("ru") == "Содержание"


def test_guide_toc_html_links_to_anchors() -> None:
    html = guide_toc_html(
        (
            GuideTocEntry("berlin_gate", "Brandenburg Gate"),
            GuideTocEntry("berlin_wall", "Wall Memorial", level=2),
        ),
        "en",
    )
    assert 'class="guide-toc"' in html
    assert 'href="#berlin_gate"' in html
    assert 'href="#berlin_wall"' in html
    assert "toc-item--sub" in html


def test_toc_entries_follow_place_list(tmp_path: Path) -> None:
    places = [
        {
            "slug": "alpha_place",
            "name_en": "Alpha",
            "category": "landmarks",
            "image_rel_path": "images/alpha.jpg",
        },
        {
            "slug": "beta_place",
            "name_en": "Beta",
            "category": "landmarks",
            "image_rel_path": "images/beta.jpg",
        },
    ]
    images = tmp_path / "images"
    images.mkdir()
    for name in ("alpha.jpg", "beta.jpg"):
        (images / name).write_bytes(b"x" * 600)

    def has_section(root: Path, place: dict) -> bool:
        return bool(place.get("image_rel_path"))

    entries = toc_entries_for_jerusalem_guide(
        tmp_path,
        places,
        "en",
        city_slug="sample",
        project_root=None,
        sort_key=lambda p: str(p.get("name_en") or ""),
        has_section=has_section,
    )
    labels = [e.label for e in entries]
    assert labels == ["Alpha", "Beta"]

    places.pop()
    entries2 = toc_entries_for_jerusalem_guide(
        tmp_path,
        places,
        "en",
        city_slug="sample",
        project_root=None,
        sort_key=lambda p: str(p.get("name_en") or ""),
        has_section=has_section,
    )
    assert [e.label for e in entries2] == ["Alpha"]


def test_toc_reflects_renamed_place() -> None:
    place = {
        "slug": "same_slug",
        "name_en": "New Title",
        "name_ru": "Новое название",
    }
    en = toc_entries_for_flat_places([place], "en")
    ru = toc_entries_for_flat_places([place], "ru")
    assert en[0].label == "New Title"
    assert ru[0].label == "Новое название"


def test_category_chapter_anchor() -> None:
    assert category_chapter_anchor("railway_stations") == "cat-railway-stations"
