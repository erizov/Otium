# -*- coding: utf-8 -*-
"""Shared HTML/PDF builder for Jerusalem-style Latin city guides."""

from __future__ import annotations

import argparse
import sys
from html import escape
from pathlib import Path
from typing import Any

from scripts.build_pdf import (
    _pdf_via_playwright,
    _strip_empty_pdf_pages,
    _strip_pdf_metadata,
)
from scripts.city_guide_core import (
    MIN_IMAGE_BYTES,
    copy_built_guide_pdf_to_final_guides,
    is_substantive_text,
    smallest_same_stem_image_rel,
)
from scripts.city_guide_historical_reference_ru import (
    HERALDRY_CHAPTER_LABEL_RU,
    historical_reference_section_html,
    reference_text_ru_for_city,
)
from scripts.city_guide_typography import guide_inline_css
from scripts.city_guide_typography import typography_triple

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


def _place_has_displayable_body(p: dict[str, Any]) -> bool:
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


def places_with_local_images(
    root: Path,
    places: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for p in places:
        if p.get("suppress_images_for_pdf"):
            if _place_has_displayable_body(p):
                out.append(p)
            continue
        rel = p.get("image_rel_path")
        if not rel:
            continue
        if smallest_same_stem_image_rel(root, rel) is not None:
            out.append(p)
    key_fn = lambda x: (str(x.get("name_en", "")), str(x.get("slug", "")))
    out.sort(key=key_fn)
    return out


def _place_meta_line(p: dict[str, Any]) -> str | None:
    parts: list[str] = []
    if is_substantive_text(p.get("address")):
        parts.append("Address: {}".format(str(p["address"]).strip()))
    if is_substantive_text(p.get("architecture_style")):
        parts.append("Style: {}".format(str(p["architecture_style"]).strip()))
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


def _image_srcs_for_place(
    root: Path,
    p: dict[str, Any],
) -> list[str]:
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


def _subtitle_html(p: dict[str, Any]) -> str:
    if is_substantive_text(p.get("subtitle_en")):
        t = str(p["subtitle_en"])
        return '<p class="sub-en">{}</p>'.format(escape(t))
    if is_substantive_text(p.get("subtitle_it")):
        t = str(p["subtitle_it"])
        return '<p class="sub-it">{}</p>'.format(escape(t))
    if is_substantive_text(p.get("subtitle_ja")):
        t = str(p["subtitle_ja"])
        return '<p class="sub-ja" lang="ja">{}</p>'.format(escape(t))
    if is_substantive_text(p.get("subtitle_he")):
        t = str(p["subtitle_he"])
        return '<p class="sub-he" dir="rtl" lang="he">{}</p>'.format(
            escape(t),
        )
    return ""


def place_block(p: dict[str, Any], img_srcs: list[str]) -> str:
    name_en = escape(str(p.get("name_en", "")))
    name_plain = str(p.get("name_en", ""))
    sub_html = _subtitle_html(p)
    meta = _place_meta_line(p)
    meta_html = (
        '<p class="place-meta">{}</p>'.format(escape(meta))
        if meta
        else ""
    )
    slug = str(p.get("slug", "x"))
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
                _html_paragraphs(str(p["description"])),
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
                "<ul class=\"stories\">{}</ul>".format(st_li)
            )
    if is_substantive_text(p.get("history")):
        chunks.append("<h4>History</h4>")
        chunks.append(_html_paragraphs(str(p["history"])))
    if is_substantive_text(p.get("significance")):
        chunks.append("<h4>Significance</h4>")
        chunks.append(_html_paragraphs(str(p["significance"])))
    chunks.append("</section>")
    return "\n".join(chunks)


def fig_if_exists(
    root: Path,
    rel: str,
    alt: str,
    extra_class: str,
) -> str:
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


def heraldry_html(
    root: Path,
    title_symbols_class: str,
    title_symbols: tuple[tuple[str, str], ...],
) -> str:
    label_esc = escape(HERALDRY_CHAPTER_LABEL_RU)
    chunks: list[str] = [
        '<div class="{}" aria-label="{}">'.format(
            title_symbols_class,
            label_esc,
        ),
        '<p class="title-strip-label">{}</p>'.format(label_esc),
        '<div class="heraldry-strip heraldry-official">',
    ]
    for rel, alt in title_symbols:
        fig = fig_if_exists(root, rel, alt, "heraldry-coat-book")
        if fig:
            chunks.append(fig)
    chunks.append("</div></div>")
    return "\n".join(chunks)


def cover_otium_html() -> str:
    paras = "\n".join(
        '<p class="otiump">{}</p>'.format(escape(t)) for t in _OTIUM_PARAS_EN
    )
    return (
        '<section class="cover-otium">'
        '<h1 class="otium-logo">OTIUM</h1>'
        "{}"
        "</section>"
    ).format(paras)


def build_html(
    root: Path,
    *,
    city_slug: str,
    display_title: str,
    title_symbols_class: str,
    title_symbols: tuple[tuple[str, str], ...],
    places: list[dict[str, Any]],
    html_lang: str,
) -> str:
    font_href, _, _ = typography_triple(city_slug)
    blocks: list[str] = [cover_otium_html()]
    blocks.append(
        '<header class="guide-title">'
        "{}"
        "<h1 class=\"guide-title-main\">{}</h1>"
        "<p class=\"lead\">Guide. Places in this edition: {}.</p>"
        "</header>".format(
            heraldry_html(root, title_symbols_class, title_symbols),
            escape(display_title),
            len(places),
        ),
    )
    hist = historical_reference_section_html(
        reference_text_ru_for_city(city_slug),
    )
    if hist:
        blocks.append(hist)
    for p in places:
        srcs = _image_srcs_for_place(root, p)
        if not srcs and not (
            p.get("suppress_images_for_pdf") and _place_has_displayable_body(p)
        ):
            continue
        blocks.append(place_block(p, srcs))
    body_inner = "\n".join(blocks)
    css = guide_inline_css(title_symbols_class, city_slug)
    return (
        "<!DOCTYPE html>\n"
        '<html lang="{}">\n<head>\n'
        '<meta charset="utf-8"/>\n'
        "<title>Guide · {} · OTIUM</title>\n"
        '<link rel="stylesheet" href="{}"/>\n'
        "<style>\n{}</style>\n</head>\n<body>\n{}\n</body>\n</html>\n"
    ).format(html_lang, escape(display_title), font_href, css, body_inner)


def run_build_pdf_main(
    *,
    project_root: Path,
    city_slug: str,
    city_root: Path,
    display_title: str,
    title_symbols_class: str,
    title_symbols: tuple[tuple[str, str], ...],
    places: list[dict[str, Any]],
    html_name: str,
    pdf_name: str,
    argv: list[str] | None,
    html_lang: str = "en",
) -> int:
    parser = argparse.ArgumentParser(
        description="Build {} HTML/PDF.".format(display_title),
    )
    parser.add_argument(
        "--city-root",
        type=Path,
        default=city_root,
        help="City tree root (default: {}/)".format(city_slug),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory (default: <city>/output/)",
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
    args = parser.parse_args(argv)
    root = args.city_root.resolve()
    out_dir = (
        args.output_dir.resolve()
        if args.output_dir
        else root / "output"
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    built = places_with_local_images(root, places)
    if not built:
        print(
            "No places with local images (>= {} bytes). "
            "Run download script first.".format(MIN_IMAGE_BYTES),
            file=sys.stderr,
        )
        return 2

    html_path = out_dir / html_name
    html_path.write_text(
        build_html(
            root,
            city_slug=city_slug,
            display_title=display_title,
            title_symbols_class=title_symbols_class,
            title_symbols=title_symbols,
            places=built,
            html_lang=html_lang,
        ),
        encoding="utf-8",
    )
    print("Written:", html_path)

    if args.html_only:
        print("Places in HTML: {}".format(len(built)))
        return 0

    pdf_path = out_dir / pdf_name
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
        static_site_root=root,
    ):
        _strip_empty_pdf_pages(pdf_path)
        _strip_pdf_metadata(pdf_path)
        copy_built_guide_pdf_to_final_guides(project_root, pdf_path)
        print("Written:", pdf_path)
        print("Places in PDF: {}".format(len(built)))
        return 0
    print(
        "PDF failed: pip install playwright && playwright install chromium",
        file=sys.stderr,
    )
    return 1
