# -*- coding: utf-8 -*-
"""Tests for place photo row layout in PDF HTML."""

from __future__ import annotations

from scripts.city_guide_place_figures import place_figures_layout_html


def test_place_figures_layout_pair_row() -> None:
    html = place_figures_layout_html(
        ["a.jpg", "b.jpg"],
        "Test Place",
        "en",
    )
    assert "place-pdf-fig-row--pair" in html
    assert html.count("<figure") == 2
    assert "place-pdf-fig-rows-stack" not in html


def test_place_figure_layout_css_uses_viewport_caps() -> None:
    from scripts.city_guide_place_figures import place_figure_layout_css

    css = place_figure_layout_css()
    assert "48vh" in css
    assert "50vh" in css or "52vh" in css
    assert "42vh" in css
    assert "place-fig--hi-res" in css
    compact = place_figure_layout_css(compact=True)
    assert "34vh" in compact


def test_pair_row_equal_height_styles() -> None:
    from pathlib import Path
    from scripts.city_guide_place_figures import (
        pair_row_equal_img_styles,
        place_figures_layout_html,
    )

    root = Path(__file__).resolve().parent
    wide = root / "wide.png"
    tall = root / "tall.png"
    try:
        from PIL import Image

        Image.new("RGB", (1600, 600), "red").save(wide)
        Image.new("RGB", (800, 1200), "blue").save(tall)
        styles = pair_row_equal_img_styles([wide, tall])
        assert styles[0] == styles[1]
        assert "height:" in styles[0]
        html = place_figures_layout_html(
            ["a.jpg", "b.jpg"],
            "Pair Place",
            "en",
            image_paths=[wide, tall],
        )
        assert html.count("height:") >= 2
    finally:
        wide.unlink(missing_ok=True)
        tall.unlink(missing_ok=True)


def test_row_equal_height_styles_triple() -> None:
    from pathlib import Path
    from scripts.city_guide_place_figures import (
        place_figure_row_html,
        row_equal_img_styles,
    )

    root = Path(__file__).resolve().parent
    paths: list[Path] = []
    try:
        from PIL import Image

        specs = [(1400, 700), (1200, 900), (1600, 800)]
        for i, (w, h) in enumerate(specs):
            path = root / "tri_{}.png".format(i)
            Image.new("RGB", (w, h), "red").save(path)
            paths.append(path)
        styles = row_equal_img_styles(paths, row_kind="triple")
        assert len(styles) == 3
        assert styles[0] == styles[1] == styles[2]
        assert "height:" in styles[0]
        html = place_figure_row_html(
            [(1, "a.jpg"), (2, "b.jpg"), (3, "c.jpg")],
            "Triple Place",
            row_kind="triple",
            edition="en",
            row_paths=paths,
        )
        assert "place-pdf-fig-row--triple" in html
        assert html.count('style="height:') == 3
    finally:
        for path in paths:
            path.unlink(missing_ok=True)


def test_row_equal_height_upscales_to_fill() -> None:
    from pathlib import Path
    from scripts.city_guide_place_figures import row_equal_img_styles

    root = Path(__file__).resolve().parent
    small = root / "small_row.png"
    large = root / "large_row.png"
    try:
        from PIL import Image

        Image.new("RGB", (100, 100), "red").save(small)
        Image.new("RGB", (1600, 1200), "blue").save(large)
        styles = row_equal_img_styles([small, large], row_kind="pair")
        assert styles[0] == styles[1]
        h = int(styles[0].split("height: ")[1].split("px")[0])
        assert h > 100
    finally:
        small.unlink(missing_ok=True)
        large.unlink(missing_ok=True)


def test_row_equal_height_hi_res_pair_uses_more_space() -> None:
    from pathlib import Path
    from scripts.city_guide_place_figures import row_equal_img_styles

    root = Path(__file__).resolve().parent
    a = root / "pair_a.png"
    b = root / "pair_b.png"
    try:
        from PIL import Image

        Image.new("RGB", (1280, 960), "red").save(a)
        Image.new("RGB", (1280, 960), "blue").save(b)
        styles = row_equal_img_styles([a, b], row_kind="pair")
        h = int(styles[0].split("height: ")[1].split("px")[0])
        assert h >= 340
    finally:
        a.unlink(missing_ok=True)
        b.unlink(missing_ok=True)


def test_place_figures_layout_triple_rows() -> None:
    html = place_figures_layout_html(
        ["a.jpg", "b.jpg", "c.jpg", "d.jpg", "e.jpg"],
        "Smolensk Place",
        "en",
    )
    assert "place-pdf-fig-rows-stack" in html
    assert "place-pdf-fig-row--triple" in html
    assert "place-pdf-fig-row--pair" in html
    assert html.count("<figure") == 5
