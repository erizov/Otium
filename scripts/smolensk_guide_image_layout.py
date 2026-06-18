# -*- coding: utf-8 -*-
"""Smolensk-only image sizing: title heraldry, welcome block, triple rows."""

from __future__ import annotations

# Inline height cap multiplier for 3-across place photo rows.
SMOLENSK_TRIPLE_ROW_HEIGHT_SCALE = 1.58


def _building_smolensk_guide() -> bool:
    """True while build_smolensk_pdf._build_html is running."""
    try:
        from scripts import build_smolensk_pdf as bsp

        return bool(getattr(bsp, "_SMOLENSK_BUILD_ACTIVE", False))
    except ImportError:
        return False


def _smolensk_build_context() -> bool:
    """True during Smolensk HTML assembly (flag or call stack)."""
    if _building_smolensk_guide():
        return True
    import inspect

    for frame in inspect.stack()[2:14]:
        path = frame.filename.replace("\\", "/")
        if path.endswith("/build_smolensk_pdf.py"):
            return True
    return False


def resolve_triple_row_height_scale(requested: float) -> float:
    """Apply Smolensk default when caller did not set an explicit scale."""
    if requested != 1.0:
        return requested
    _ensure_build_smolensk_patch()
    if _smolensk_build_context():
        return SMOLENSK_TRIPLE_ROW_HEIGHT_SCALE
    return 1.0


def smolensk_image_css_extra() -> str:
    """CSS overrides appended when build_smolensk_pdf assembles guide styles."""
    return """
.guide-welcome-closing .welcome-closing-head {
  font-size: 1.85rem; margin: 0.55rem 0 0.9rem; line-height: 1.15; }
.heraldry-coat-hist img {
  max-height: 8.5rem; max-width: 9.5rem; object-fit: contain; }
.heraldry-coat-book img, .heraldry-flag-book img {
  max-height: 6.25rem; object-fit: contain; }
.heraldry-flag-book img { max-height: 4.5rem; }
.welcome-closing-fig img {
  max-height: 66vh; }
.welcome-closing-fig.place-fig--hi-res img {
  max-height: 80vh; }
.welcome-closing-fig.place-fig--lo-res img { max-height: 46vh; }
.guide-welcome-closing .place-pdf-fig-row--pair .place-fig img {
  max-height: 54vh; }
.guide-welcome-closing .place-pdf-fig-row--pair .place-fig--hi-res img {
  max-height: 62vh; }
.guide-welcome-closing .place-pdf-fig-row--pair .place-fig--lo-res img {
  max-height: 36vh; }
.guide-welcome-closing .place-pdf-fig-row--pair .place-fig--row-sized img {
  height: auto !important; max-height: 62vh !important; }
.guide-welcome-closing .place-pdf-fig-row--triple .place-fig img {
  max-height: 54vh; }
.guide-welcome-closing .place-pdf-fig-row--triple .place-fig--hi-res img {
  max-height: 66vh; }
.guide-welcome-closing .place-pdf-fig-row--triple .place-fig--lo-res img {
  max-height: 38vh; }
.place .place-pdf-fig-row--triple .place-fig img {
  max-height: 44vh; }
.place .place-pdf-fig-row--triple .place-fig--hi-res img {
  max-height: 58vh; }
.place .place-pdf-fig-row--triple .place-fig--lo-res img {
  max-height: 28vh; }
.place .place-pdf-fig-row--many .place-fig img {
  max-height: 44vh; }
.place .place-pdf-fig-row--many .place-fig--hi-res img {
  max-height: 58vh; }
"""


def _ensure_build_smolensk_patch() -> None:
    """Wrap _build_html so triple-row scaling and CSS know the build is active."""
    try:
        import scripts.build_smolensk_pdf as bsp
    except ImportError:
        return
    if getattr(bsp, "_SMOLENSK_IMAGE_HOOKS", False):
        return
    if not hasattr(bsp, "_build_html"):
        return
    orig_build = bsp._build_html

    def _build_html_with_flag(*args, **kwargs):
        bsp._SMOLENSK_BUILD_ACTIVE = True
        try:
            return orig_build(*args, **kwargs)
        finally:
            bsp._SMOLENSK_BUILD_ACTIVE = False

    bsp._build_html = _build_html_with_flag
    bsp._SMOLENSK_BUILD_ACTIVE = False
    bsp._SMOLENSK_IMAGE_HOOKS = True


def install_typography_patch() -> None:
    """Hook Smolensk image CSS into guide_pdf_pagination_css."""
    import scripts.city_guide_typography as typography

    orig_css = typography.guide_pdf_pagination_css
    if getattr(orig_css, "_smolensk_image_patch", False):
        return

    def guide_pdf_pagination_css(*, toc_h2_extra: str = "") -> str:
        _ensure_build_smolensk_patch()
        css = orig_css(toc_h2_extra=toc_h2_extra)
        if _smolensk_build_context():
            return css + smolensk_image_css_extra()
        return css

    guide_pdf_pagination_css._smolensk_image_patch = True  # type: ignore[attr-defined]
    typography.guide_pdf_pagination_css = guide_pdf_pagination_css
