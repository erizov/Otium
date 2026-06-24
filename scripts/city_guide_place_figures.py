"""HTML layout for place photos in city guide PDFs.

Row rule (2+ images): every image in a row shares one computed height —
the largest height that fits all columns under the resolution cap. Images
may upscale to fill column width; side margins come from ``object-fit:
contain`` and flex centering.
"""

from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Sequence

# Hi-res sources may use taller layout caps; small files stay modest.
_HI_RES_MIN_PX = 1200
_LO_RES_MAX_PX = 520
# Approximate printable width / viewport for row height equalization.
# Match flex rows: ~100% body width minus side margins and inter-image gaps.
_ROW_VIEWPORT_H_PX = 900
_ROW_VIEWPORT_W_PX = 1000
_ROW_BODY_MARGIN_PX = 32
_ROW_CONTENT_W_PX = _ROW_VIEWPORT_W_PX - 2 * _ROW_BODY_MARGIN_PX
_ROW_GAP_PX = 12
_SOLO_MIN_WIDTH_PCT = 70
_ROW_IMG_STYLE = (
    ' style="height: {0}px; max-height: {0}px; width: auto; '
    'max-width: 100%; object-fit: contain;"'
)


def _ui_strings(edition: str) -> dict[str, str]:
    from scripts.city_guide_jerusalem_style_pdf import guide_ui_strings

    return guide_ui_strings(edition)


def place_figure_layout_css(*, compact: bool = False) -> str:
    """Shared CSS for place photo rows (pair / triple / stack)."""
    if compact:
        solo = "34vh"
        pair = "28vh"
        triple = "22vh"
        hi_solo = "38vh"
        hi_pair = "32vh"
        hi_triple = "26vh"
        lo_solo = "22vh"
        lo_pair = "18vh"
        lo_triple = "14vh"
    else:
        solo = "48vh"
        pair = "44vh"
        triple = "30vh"
        hi_solo = "52vh"
        hi_pair = "52vh"
        hi_triple = "42vh"
        lo_solo = "30vh"
        lo_pair = "26vh"
        lo_triple = "18vh"
    return """
.place-fig {{ page-break-inside: avoid; break-inside: avoid-page;
  margin: 0.5rem 0 1rem; }}
.place-fig img {{
  page-break-inside: avoid; break-inside: avoid-page;
  max-height: {solo}; width: auto; max-width: 100%;
  object-fit: contain; margin-left: auto; margin-right: auto; }}
.place-fig--hi-res img {{ max-height: {hi_solo}; }}
.place-fig--lo-res img {{ max-height: {lo_solo}; }}
.place-fig--solo {{
  display: flex; justify-content: center; align-items: flex-end;
  width: 100%; margin-left: auto; margin-right: auto; }}
.place-fig--solo img {{
  width: {solo_min}%; min-width: {solo_min}%; max-width: 100%;
  height: auto; object-fit: contain;
  margin-left: auto; margin-right: auto; }}
.place-fig--solo.place-fig--hi-res img {{ max-height: {hi_solo}; }}
.place-fig--solo.place-fig--lo-res img {{ max-height: {lo_solo}; }}
.place-pdf-fig-row {{
  display: flex; flex-direction: row; flex-wrap: wrap;
  align-items: flex-end; justify-content: center;
  gap: 0.45rem 0.55rem; margin: 0.55rem 0 1.05rem;
  page-break-inside: avoid; break-inside: avoid-page; }}
.place-pdf-fig-row .place-fig {{
  flex: 1 1 30%; margin: 0; min-width: 26%; max-width: 100%; }}
.place-pdf-fig-row .place-fig img {{
  width: auto; max-width: 100%; height: auto; max-height: {pair};
  object-fit: contain; margin: 0 auto; }}
.place-pdf-fig-row--pair {{
  flex-wrap: nowrap; justify-content: space-between;
  align-items: flex-end; gap: 0.5rem 0.65rem; }}
.place-pdf-fig-row--pair .place-fig {{
  flex: 1 1 47%; min-width: 0; max-width: 50%;
  display: flex; align-items: flex-end; justify-content: center; }}
.place-pdf-fig-row--pair .place-fig img {{
  max-height: {pair}; object-fit: contain; }}
.place-pdf-fig-row--pair .place-fig--hi-res img {{ max-height: {hi_pair}; }}
.place-pdf-fig-row--pair .place-fig--lo-res img {{ max-height: {lo_pair}; }}
.place-pdf-fig-row--pair .place-fig--row-sized img,
.place-pdf-fig-row--triple .place-fig--row-sized img,
.place-pdf-fig-row--many .place-fig--row-sized img {{
  width: auto; max-width: 100%; object-fit: contain; margin: 0 auto; }}
.place-pdf-fig-row .place-fig--row-sized.place-fig--hi-res img,
.place-pdf-fig-row .place-fig--row-sized.place-fig--lo-res img {{
  max-height: unset; }}
.place-pdf-fig-rows-stack {{
  display: flex; flex-direction: column; gap: 0.5rem;
  margin: 0.55rem 0 1.05rem;
  page-break-inside: avoid; break-inside: avoid-page; }}
.place-pdf-fig-row--triple {{
  display: flex; flex-direction: row; flex-wrap: nowrap;
  align-items: flex-end; justify-content: center;
  gap: 0.4rem 0.48rem; margin: 0;
  page-break-inside: avoid; break-inside: avoid-page; }}
.place-pdf-fig-row--triple .place-fig {{
  flex: 1 1 0; margin: 0; min-width: 0; max-width: none;
  display: flex; align-items: flex-end; justify-content: center; }}
.place-pdf-fig-row--triple .place-fig img {{
  max-height: {triple}; object-fit: contain; margin: 0 auto; }}
.place-pdf-fig-row--triple .place-fig--hi-res img {{ max-height: {hi_triple}; }}
.place-pdf-fig-row--triple .place-fig--lo-res img {{ max-height: {lo_triple}; }}
.place-pdf-fig-row--many {{
  flex-wrap: nowrap; justify-content: center; align-items: flex-end;
  gap: 0.35rem 0.42rem; }}
.place-pdf-fig-row--many .place-fig {{
  flex: 1 1 0; margin: 0; min-width: 0; max-width: none;
  display: flex; align-items: flex-end; justify-content: center; }}
.place-pdf-fig-row--many .place-fig img {{
  max-height: {triple}; object-fit: contain; margin: 0 auto; }}
""".format(
        solo=solo,
        pair=pair,
        triple=triple,
        hi_solo=hi_solo,
        hi_pair=hi_pair,
        hi_triple=hi_triple,
        lo_solo=lo_solo,
        lo_pair=lo_pair,
        lo_triple=lo_triple,
        solo_min=_SOLO_MIN_WIDTH_PCT,
    )


def _figure_img_dims(path: Path | None) -> tuple[int, int] | None:
    if path is None or not path.is_file():
        return None
    try:
        from PIL import Image

        with Image.open(path) as im:
            return im.size
    except Exception:
        return None


def _figure_res_class(path: Path | None) -> str:
    dims = _figure_img_dims(path)
    if not dims:
        return ""
    w, h = dims
    longest = max(w, h)
    if longest >= _HI_RES_MIN_PX:
        return " place-fig--hi-res"
    if longest <= _LO_RES_MAX_PX:
        return " place-fig--lo-res"
    return ""


def _fit_height_in_cell(
    width: int,
    height: int,
    max_h_px: int,
    col_w_px: int,
) -> float:
    """Largest height with width <= *col_w_px* and height <= *max_h_px*."""
    if width <= 0 or height <= 0:
        return float(max_h_px)
    h_at_full_width = col_w_px * height / width
    return min(float(max_h_px), h_at_full_width)


def _row_equal_height_px(
    dims_list: list[tuple[int, int]],
    max_h_px: int,
    col_w_px: int,
) -> int:
    """Max equal height so every image fits its column (may upscale)."""
    if not dims_list:
        return max_h_px
    caps = [
        _fit_height_in_cell(w, h, max_h_px, col_w_px)
        for w, h in dims_list
    ]
    return max(1, int(min(caps)))


def _row_col_width_px(count: int) -> int:
    """Pixel width of one flex column in a row (gaps between cells)."""
    if count <= 0:
        return _ROW_CONTENT_W_PX
    gap_total = max(0, count - 1) * _ROW_GAP_PX
    return max(1, (_ROW_CONTENT_W_PX - gap_total) // count)


def _row_tier_longest(paths: Sequence[Path | None]) -> int:
    tier_longest = 0
    for path in paths:
        dims = _figure_img_dims(path)
        if dims:
            tier_longest = max(tier_longest, max(dims))
    return tier_longest


def _row_max_height_px(
    paths: Sequence[Path | None],
    row_kind: str,
    *,
    compact: bool = False,
    height_scale: float = 1.0,
) -> int:
    tier_longest = _row_tier_longest(paths)
    if row_kind == "pair":
        if tier_longest >= _HI_RES_MIN_PX:
            vh = 34.0 if compact else 52.0
        elif tier_longest > 0 and tier_longest <= _LO_RES_MAX_PX:
            vh = 18.0 if compact else 26.0
        else:
            vh = 30.0 if compact else 46.0
    else:
        if tier_longest >= _HI_RES_MIN_PX:
            vh = 28.0 if compact else 42.0
        elif tier_longest > 0 and tier_longest <= _LO_RES_MAX_PX:
            vh = 14.0 if compact else 20.0
        else:
            vh = 24.0 if compact else 36.0
    scaled = int(_ROW_VIEWPORT_H_PX * vh / 100.0 * max(1.0, height_scale))
    return max(1, scaled)


def row_equal_img_styles(
    paths: Sequence[Path | None],
    *,
    row_kind: str = "pair",
    compact: bool = False,
    height_scale: float = 1.0,
) -> list[str]:
    """Equal inline heights — fill each column up to the row resolution cap."""
    count = len(paths)
    if count < 2:
        return [""] * count
    max_h = _row_max_height_px(
        paths,
        row_kind,
        compact=compact,
        height_scale=height_scale,
    )
    col_w = _row_col_width_px(count)
    dims: list[tuple[int, int]] = []
    for path in paths:
        size = _figure_img_dims(path)
        if size:
            dims.append(size)
    if dims:
        target = _row_equal_height_px(dims, max_h, col_w)
    else:
        target = max_h
    if height_scale > 1.0:
        target = min(int(target * height_scale), max_h)
    if target <= 0:
        return [""] * count
    style = _ROW_IMG_STYLE.format(target)
    return [style] * count


def inject_figure_img_extra(fig_html: str, img_extra: str) -> str:
    """Apply row sizing attrs/classes to a pre-built ``<figure>`` chunk."""
    if not img_extra.strip():
        return fig_html
    if "place-fig--row-sized" not in fig_html:
        fig_html = fig_html.replace(
            'class="place-fig',
            'class="place-fig place-fig--row-sized',
            1,
        )
    return fig_html.replace(
        "<img ",
        "<img {} ".format(img_extra.strip()),
        1,
    )


def pair_row_equal_img_styles(
    paths: Sequence[Path | None],
) -> list[str]:
    """Backward-compatible alias for two-image rows."""
    return row_equal_img_styles(paths, row_kind="pair")


def figure_res_class_suffix(path: Path | None) -> str:
    """Leading-space class suffix for hi-/lo-res place figures."""
    return _figure_res_class(path)


def figure_img_dimension_attrs(path: Path | None) -> str:
    """``width``/``height`` attributes when the file can be read."""
    return _figure_img_attrs(path)


def _figure_img_attrs(path: Path | None) -> str:
    dims = _figure_img_dims(path)
    if not dims:
        return ""
    w, h = dims
    return ' width="{}" height="{}"'.format(w, h)


def _figure_element(
    src: str,
    alt: str,
    path: Path | None = None,
    *,
    img_extra: str = "",
    solo: bool = False,
) -> str:
    fig_cls = "place-fig{}".format(_figure_res_class(path))
    if solo:
        fig_cls += " place-fig--solo"
    if img_extra.strip():
        fig_cls += " place-fig--row-sized"
    attrs = _figure_img_attrs(path)
    return (
        '<figure class="{}"><img src="{}" alt="{}"{}{}'
        "/></figure>"
    ).format(fig_cls, escape(src), escape(alt), attrs, img_extra)


def _path_at(
    image_paths: Sequence[Path | None] | None,
    index: int,
) -> Path | None:
    if image_paths is None or index >= len(image_paths):
        return None
    return image_paths[index]


def place_figure_html(
    name_plain: str,
    src: str,
    edition: str,
    *,
    index: int = 0,
    image_path: Path | None = None,
) -> str:
    """Single ``<figure>`` for one place photo."""
    s = _ui_strings(edition)
    alt = (
        name_plain
        if index == 0
        else s["img_alt_extra"].format(name_plain, index + 1)
    )
    return _figure_element(src, alt, image_path, solo=True)


def place_figure_row_html(
    img_slice: list[tuple[int, str]],
    name_plain: str,
    *,
    row_kind: str,
    edition: str,
    image_paths: Sequence[Path | None] | None = None,
    row_paths: Sequence[Path | None] | None = None,
    row_height_scale: float = 1.0,
) -> str:
    """One horizontal row of figures; ``row_kind``: pair | triple | many."""
    s = _ui_strings(edition)
    row_class = "place-pdf-fig-row place-pdf-fig-row--{}".format(row_kind)
    parts: list[str] = ['<div class="{}">'.format(row_class)]
    row_path_list: list[Path | None] = []
    for pos, (seq_i, src) in enumerate(img_slice):
        if row_paths is not None:
            row_path_list.append(_path_at(row_paths, pos))
        else:
            idx0 = max(seq_i - 1, 0)
            row_path_list.append(_path_at(image_paths, idx0))
    img_extras: list[str]
    if len(img_slice) >= 2:
        scale = row_height_scale if row_kind in ("triple", "many") else 1.0
        if row_kind in ("triple", "many"):
            from scripts.smolensk_guide_image_layout import (
                resolve_triple_row_height_scale,
            )

            scale = resolve_triple_row_height_scale(scale)
        img_extras = row_equal_img_styles(
            row_path_list,
            row_kind=row_kind,
            height_scale=scale,
        )
    else:
        img_extras = [""] * len(img_slice)
    for pos, (seq_i, src) in enumerate(img_slice):
        idx0 = max(seq_i - 1, 0)
        alt = (
            name_plain
            if idx0 == 0
            else s["img_alt_extra"].format(name_plain, seq_i)
        )
        path = row_path_list[pos]
        parts.append(
            _figure_element(src, alt, path, img_extra=img_extras[pos])
        )
    parts.append("</div>")
    return "\n".join(parts)


def place_figure_rows_max_three_html(
    indexed: list[tuple[int, str]],
    name_plain: str,
    edition: str,
    *,
    image_paths: Sequence[Path | None] | None = None,
    triple_row_height_scale: float = 1.0,
) -> str:
    """Stack rows of up to three images (Smolensk-style multi-photo places)."""
    from scripts.smolensk_guide_image_layout import (
        resolve_triple_row_height_scale,
    )

    triple_row_height_scale = resolve_triple_row_height_scale(
        triple_row_height_scale,
    )
    s = _ui_strings(edition)
    if not indexed:
        return ""
    if len(indexed) == 1:
        seq_i, src_one = indexed[0]
        idx0 = max(seq_i - 1, 0)
        alt_one = (
            name_plain
            if idx0 == 0
            else s["img_alt_extra"].format(name_plain, seq_i)
        )
        return _figure_element(
            src_one,
            alt_one,
            _path_at(image_paths, idx0),
            solo=True,
        )
    row_chunks: list[str] = []
    i = 0
    n = len(indexed)
    while i < n:
        remaining = n - i
        if remaining >= 3:
            row_chunks.append(
                place_figure_row_html(
                    indexed[i : i + 3],
                    name_plain,
                    row_kind="triple",
                    edition=edition,
                    image_paths=image_paths,
                    row_height_scale=triple_row_height_scale,
                )
            )
            i += 3
        elif remaining == 2:
            row_chunks.append(
                place_figure_row_html(
                    indexed[i : i + 2],
                    name_plain,
                    row_kind="pair",
                    edition=edition,
                    image_paths=image_paths,
                )
            )
            i += 2
        else:
            seq_i, src_one = indexed[i]
            idx0 = max(seq_i - 1, 0)
            alt_one = (
                name_plain
                if idx0 == 0
                else s["img_alt_extra"].format(name_plain, seq_i)
            )
            row_chunks.append(
                _figure_element(
                    src_one,
                    alt_one,
                    _path_at(image_paths, idx0),
                )
            )
            i += 1
    inner = "\n".join(row_chunks)
    return (
        '<div class="place-pdf-fig-rows-stack">\n{}\n</div>'.format(inner)
    )


def place_figures_layout_html(
    img_srcs: Sequence[str],
    name_plain: str,
    edition: str,
    *,
    start_index: int = 0,
    image_paths: Sequence[Path | None] | None = None,
    triple_row_height_scale: float = 1.0,
) -> str:
    """Lay out place photos: ≤2 in one row; >2 in rows of up to three."""
    if not img_srcs:
        return ""
    indexed = [
        (start_index + i + 1, src)
        for i, src in enumerate(img_srcs)
    ]
    if len(indexed) <= 2:
        if len(indexed) == 1:
            seq_i, src_one = indexed[0]
            idx0 = max(seq_i - 1, 0)
            s = _ui_strings(edition)
            alt_one = (
                name_plain
                if idx0 == 0
                else s["img_alt_extra"].format(name_plain, seq_i)
            )
            return _figure_element(
                src_one,
                alt_one,
                _path_at(image_paths, idx0),
                solo=True,
            )
        return place_figure_row_html(
            indexed,
            name_plain,
            row_kind="pair",
            edition=edition,
            image_paths=image_paths,
        )
    return place_figure_rows_max_three_html(
        indexed,
        name_plain,
        edition,
        image_paths=image_paths,
        triple_row_height_scale=triple_row_height_scale,
    )


try:
    from scripts.smolensk_guide_image_layout import install_typography_patch

    install_typography_patch()
except ImportError:
    pass
