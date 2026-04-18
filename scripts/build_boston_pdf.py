# -*- coding: utf-8 -*-
"""HTML + PDF for Boston from files under boston/images/."""

from __future__ import annotations

import argparse
import sys
from html import escape
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from boston.data.places_registry import BOSTON_PLACES, BostonPlace

from scripts.build_pdf import (
    _pdf_via_playwright,
    _strip_empty_pdf_pages,
    _strip_pdf_metadata,
)
from scripts.city_guide_core import MIN_IMAGE_BYTES, is_substantive_text, smallest_same_stem_image_rel
from scripts.city_guide_typography import guide_inline_css, typography_triple
from scripts.city_guide_historical_reference_ru import (
    HERALDRY_CHAPTER_LABEL_RU,
    historical_reference_section_html,
    reference_text_ru_for_city,
)

BOSTON_HTML_NAME = "boston_guide.html"
BOSTON_PDF_NAME = "boston_guide.pdf"

_TITLE_SYMBOLS: tuple[tuple[str, str], ...] = (
    (
        "images/guide_coat_of_arms.svg",
        "Seal of Boston, Massachusetts",
    ),
    (
        "images/guide_flag.svg",
        "Flag of Boston",
    ),
)

_OTIUM_PARAS_EN: tuple[str, ...] = (
    "OTIUM is the practice of deliberate leisure. In the classical sense, "
    "otium is not escape from work but time when attention returns to "
    "memory, landscape, and thought — without a utilitarian deadline.",
    "We shape routes for lingering, not for checklist tourism. The goal "
    "is presence in a place rather than consumption of sights.",
    "OTIUM is not a tour operator. It is an invitation to walk, pause, "
    "and leave a route unfinished if the light on a façade deserves "
    "another minute.",
)


def _place_has_displayable_body(p: BostonPlace) -> bool:
    if is_substantive_text(p.get("description")):
        return True
    if is_substantive_text(p.get("history")):
        return True
    if is_substantive_text(p.get("significance")):
        return True
    facts = p.get("facts") or []
    if any(is_substantive_text(str(x)) for x in facts):
        return True
    stories = p.get("stories") or []
    return any(is_substantive_text(str(x)) for x in stories)


def _places_with_local_images(root: Path) -> list[BostonPlace]:
    out: list[BostonPlace] = []
    for p in BOSTON_PLACES:
        if p.get("suppress_images_for_pdf"):
            if _place_has_displayable_body(p):
                out.append(p)
            continue
        rel = p.get("image_rel_path")
        if not rel:
            continue
        if smallest_same_stem_image_rel(root, rel) is not None:
            out.append(p)
    out.sort(key=lambda x: (x.get("name_en", ""), x.get("slug", "")))
    return out


def _nonempty(s: str | None) -> bool:
    return bool(s and str(s).strip())


def _place_meta_line(p: BostonPlace) -> str | None:
    parts: list[str] = []
    if is_substantive_text(p.get("address")):
        parts.append("Address: {}".format(p["address"].strip()))
    if is_substantive_text(p.get("architecture_style")):
        parts.append("Style: {}".format(p["architecture_style"].strip()))
    if is_substantive_text(p.get("year_built")):
        parts.append("Period: {}".format(str(p["year_built"]).strip()))
    if not parts:
        return None
    return " | ".join(parts)


def _html_paragraphs(text: str) -> str:
    chunks = [
        t.strip() for t in text.split("\n\n")
        if is_substantive_text(t.strip())
    ]
    return "\n".join(
        "<p class=\"prose\">{}</p>".format(escape(c)) for c in chunks
    )


def _rel_to_src(rel: str) -> str:
    return "../{}".format(rel.lstrip("/").replace("\\", "/"))


def _image_srcs_for_place(root: Path, p: BostonPlace) -> list[str]:
    if p.get("suppress_images_for_pdf"):
        return []
    out: list[str] = []
    rel = p.get("image_rel_path")
    if rel:
        chosen = smallest_same_stem_image_rel(root, rel)
        if chosen:
            out.append(_rel_to_src(chosen))
    for item in p.get("additional_images") or []:
        er = item.get("image_rel_path")
        if not er:
            continue
        chosen_extra = smallest_same_stem_image_rel(root, er)
        if chosen_extra:
            out.append(_rel_to_src(chosen_extra))
    return out


def _place_block(p: BostonPlace, img_srcs: list[str]) -> str:
    name_en = escape(p.get("name_en", ""))
    name_plain = p.get("name_en", "")
    sub_es = p.get("subtitle_en", "")
    sub_html = (
        '<p class="sub-en">{}</p>'.format(escape(sub_es))
        if is_substantive_text(sub_es)
        else ""
    )
    meta = _place_meta_line(p)
    meta_html = (
        '<p class="place-meta">{}</p>'.format(escape(meta))
        if meta
        else ""
    )
    slug = p.get("slug", "x")
    chunks: list[str] = [
        '<section class="place" id="{}">'.format(escape(slug)),
        "<h3>{}</h3>".format(name_en),
        sub_html,
        meta_html,
    ]
    for i, src in enumerate(img_srcs):
        alt = name_plain if i == 0 else "{} — view {}".format(
            name_plain, i + 1,
        )
        chunks.append(
            '<figure class="place-fig"><img src="{}" alt="{}"/></figure>'.format(
                escape(src),
                escape(alt),
            )
        )
    if is_substantive_text(p.get("description")):
        chunks.append(
            '<div class="place-desc">{}</div>'.format(
                _html_paragraphs(p["description"]),
            )
        )
    facts = p.get("facts") or []
    if facts:
        lis = "\n".join(
            "<li>{}</li>".format(escape(str(f).strip()))
            for f in facts
            if is_substantive_text(str(f).strip())
        )
        if lis:
            chunks.append(
                "<h4>Facts and details</h4>\n"
                "<ul class=\"facts\">{}</ul>".format(lis)
            )
    stories = p.get("stories") or []
    if stories:
        st_li = "\n".join(
            "<li>{}</li>".format(escape(str(s).strip()))
            for s in stories
            if is_substantive_text(str(s).strip())
        )
        if st_li:
            chunks.append(
                "<h4>Stories and legends</h4>\n"
                "<ul class=\"stories\">{}</ul>".format(st_li),
            )
    if is_substantive_text(p.get("history")):
        chunks.append("<h4>History</h4>")
        chunks.append(_html_paragraphs(p["history"]))
    if is_substantive_text(p.get("significance")):
        chunks.append("<h4>Significance</h4>")
        chunks.append(_html_paragraphs(p["significance"]))
    chunks.append("</section>")
    return "\n".join(chunks)


def _fig_if_exists(root: Path, rel: str, alt: str, extra_class: str) -> str:
    resolved = smallest_same_stem_image_rel(root, rel)
    if not resolved:
        return ""
    src = _rel_to_src(resolved)
    return (
        '<figure class="heraldry-fig {}" title="{}">'
        '<img src="{}" alt="{}"/>'
        "</figure>".format(
            extra_class,
            escape(alt),
            escape(src),
            escape(alt),
        )
    )


def _heraldry_html(root: Path) -> str:
    chunks: list[str] = [
        '<div class="boston-title-symbols" '
        'aria-label="boston city arms and regional flag">',
        '<p class="title-strip-label">{}</p>'.format(escape(HERALDRY_CHAPTER_LABEL_RU)),
        '<div class="heraldry-strip heraldry-official">',
    ]
    for rel, alt in _TITLE_SYMBOLS:
        fig = _fig_if_exists(root, rel, alt, "heraldry-coat-book")
        if fig:
            chunks.append(fig)
    chunks.append("</div></div>")
    return "\n".join(chunks)


def _cover_otium_html() -> str:
    paras = "\n".join(
        '<p class="otiump">{}</p>'.format(escape(t)) for t in _OTIUM_PARAS_EN
    )
    return (
        '<section class="cover-otium">'
        '<h1 class="otium-logo">OTIUM</h1>'
        "{}"
        "</section>"
    ).format(paras)


def _build_html(root: Path, places: list[BostonPlace]) -> str:
    font_href, _, _ = typography_triple("boston")
    blocks: list[str] = [_cover_otium_html()]
    blocks.append(
        '<header class="guide-title">'
        "{}"
        "<h1 class=\"guide-title-main\">Boston</h1>"
        "<p class=\"lead\">Guide. Places in this edition: {}.</p>"
        "</header>".format(_heraldry_html(root), len(places)),
    )
    hist = historical_reference_section_html(
        reference_text_ru_for_city("boston"),
    )
    if hist:
        blocks.append(hist)
    for p in places:
        srcs = _image_srcs_for_place(root, p)
        if not srcs and not (
            p.get("suppress_images_for_pdf") and _place_has_displayable_body(p)
        ):
            continue
        blocks.append(_place_block(p, srcs))
    body_inner = "\n".join(blocks)
    css = guide_inline_css("boston-title-symbols", "boston")
    return (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n<head>\n'
        '<meta charset="utf-8"/>\n'
        "<title>Guide · Boston · OTIUM</title>\n"
        '<link rel="stylesheet" href="{}"/>\n'
        "<style>\n{}</style>\n</head>\n<body>\n{}\n</body>\n</html>\n"
    ).format(font_href, css, body_inner)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build Boston HTML/PDF using files under boston/images."
        ),
    )
    parser.add_argument(
        "--boston-root",
        type=Path,
        default=_PROJECT_ROOT / "boston",
        help="Boston tree root (default: boston/)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory (default: boston/output/)",
    )
    parser.add_argument(
        "--html-only",
        action="store_true",
        help="Write HTML only; skip Playwright PDF.",
    )
    parser.add_argument(
        "--image-wait-ms",
        type=int,
        default=30000,
        metavar="MS",
        help="Playwright wait for images (default 30000).",
    )
    args = parser.parse_args()
    boston_root = args.boston_root.resolve()
    out_dir = (
        args.output_dir.resolve()
        if args.output_dir
        else boston_root / "output"
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    places = _places_with_local_images(boston_root)
    if not places:
        print(
            "No places with local images (>= {} bytes). "
            "Fill boston_places.json and run "
            "scripts/download_boston_images.py.".format(MIN_IMAGE_BYTES),
            file=sys.stderr,
        )
        return 2

    html_path = out_dir / BOSTON_HTML_NAME
    html_path.write_text(_build_html(boston_root, places), encoding="utf-8")
    print("Written:", html_path)

    if args.html_only:
        print("Places in HTML: {}".format(len(places)))
        return 0

    pdf_path = out_dir / BOSTON_PDF_NAME
    footer = (
        "<div style='font-size:9px;text-align:center;width:100%'>"
        "<span class='pageNumber'></span> / <span class='totalPages'></span>"
        "</div>"
    )
    header = "<div style='font-size:9px;width:100%'></div>"
    if _pdf_via_playwright(
        html_path,
        pdf_path,
        image_wait_timeout_ms=args.image_wait_ms,
        display_header_footer=True,
        footer_template=footer,
        header_template=header,
        static_site_root=boston_root,
    ):
        _strip_empty_pdf_pages(pdf_path)
        _strip_pdf_metadata(pdf_path)
        print("Written:", pdf_path)
        print("Places in PDF: {}".format(len(places)))
        return 0
    print(
        "PDF failed: pip install playwright && playwright install chromium",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
