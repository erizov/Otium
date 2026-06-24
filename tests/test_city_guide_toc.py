# -*- coding: utf-8 -*-
"""Tests for city guide table of contents."""

from __future__ import annotations

from pathlib import Path

from scripts.city_guide_toc import (
    GuideTocEntry,
    GUIDE_TOC_ID,
    category_chapter_anchor,
    guide_toc_back_link_html,
    guide_toc_html,
    guide_toc_html_category_chapters,
    guide_toc_title,
    normalize_title_for_sort,
    place_sort_key,
    toc_entries_for_flat_places,
    toc_entries_for_jerusalem_guide,
)
from scripts.city_guide_typography import guide_pdf_pagination_css


def test_normalize_title_for_sort_strips_guillemets() -> None:
    assert normalize_title_for_sort("«Гоголь-центр»") == "гоголь-центр"
    assert normalize_title_for_sort("«Депо Москва»") == "депо москва"
    assert (
        normalize_title_for_sort("«Рабочий и колхозница»")
        == "рабочий и колхозница"
    )


def test_place_sort_key_ignores_quotes() -> None:
    places = [
        {
            "slug": "quoted",
            "name_ru": "«Гоголь-центр»",
        },
        {
            "slug": "alpha",
            "name_ru": "Александровский сад",
        },
    ]
    key = place_sort_key("ru")
    ordered = sorted(places, key=key)
    assert [p["slug"] for p in ordered] == ["alpha", "quoted"]


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
    assert 'id="{}"'.format(GUIDE_TOC_ID) in html
    assert 'href="#berlin_gate"' in html
    assert 'href="#berlin_wall"' in html
    assert "toc-item--sub" in html


def test_guide_toc_html_category_chapters_nested_examples() -> None:
    html = guide_toc_html_category_chapters(
        (
            GuideTocEntry("guide-historical", "Historical overview"),
            GuideTocEntry(
                category_chapter_anchor("empire"),
                "12. Empire style",
                level=1,
            ),
            GuideTocEntry("empire_isaac", "Saint Isaac's Cathedral", level=2),
            GuideTocEntry("empire_kazan", "Kazan Cathedral", level=2),
        ),
        "en",
    )
    assert 'class="toc-chapters"' in html
    assert 'class="toc-examples"' in html
    assert "toc-item--example" in html
    assert "12. Empire style" in html
    assert 'href="#empire_isaac"' in html
    assert "Kazan Cathedral" in html
    assert "toc-item--sub" not in html


def test_guide_toc_back_link_points_to_contents() -> None:
    en = guide_toc_back_link_html("en")
    ru = guide_toc_back_link_html("ru")
    assert 'href="#{}"'.format(GUIDE_TOC_ID) in en
    assert "Contents" in en
    assert "Содержание" in ru


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
        section_places=places[:1],
    )
    assert [e.label for e in entries2] == ["Alpha"]


def test_toc_uses_explicit_section_places(tmp_path: Path) -> None:
    places = [
        {
            "slug": "alpha_place",
            "name_en": "Alpha",
            "image_rel_path": "images/alpha.jpg",
        },
        {
            "slug": "beta_place",
            "name_en": "Beta",
            "image_rel_path": "images/beta.jpg",
        },
    ]
    images = tmp_path / "images"
    images.mkdir()
    (images / "alpha.jpg").write_bytes(b"x" * 600)

    def has_section(root: Path, place: dict) -> bool:
        return bool(place.get("image_rel_path"))

    entries = toc_entries_for_jerusalem_guide(
        tmp_path,
        places,
        "en",
        city_slug="sample",
        project_root=None,
        has_section=has_section,
        section_places=[places[0]],
    )
    assert [e.anchor for e in entries] == ["alpha_place"]


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


def test_guide_pdf_pagination_css_toc_page_breaks() -> None:
    css = guide_pdf_pagination_css()
    assert "page-break-before: always" in css
    assert "page-break-after: always" in css
    assert ".place-lead" in css
