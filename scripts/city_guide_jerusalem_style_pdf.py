# -*- coding: utf-8 -*-
"""Shared HTML/PDF builder for Jerusalem-style Latin city guides."""

from __future__ import annotations

import argparse
import shutil
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
    places_for_pdf,
    smallest_same_stem_image_rel,
)
from scripts.city_guide_historical_reference_ru import (
    HERALDRY_CHAPTER_LABEL_EN,
    HERALDRY_CHAPTER_LABEL_RU,
    HISTORICAL_SECTION_TITLE_EN,
    historical_reference_section_html,
    reference_text_en_for_city,
    reference_text_ru_for_any_city,
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

# Max place sections per Playwright pass (avoids Chromium string limit).
PDF_CHUNK_MAX_PLACES = 35

_OTIUM_PARAS_RU: tuple[str, ...] = (
    "OTIUM — практика нарочитого досуга. В античном смысле otium — не "
    "побег от работы, а время, когда внимание возвращается к памяти, "
    "пейзажу и мысли — без прикладного дедлайна.",
    "Мы выстраиваем маршруты для неспешного присутствия, а не для "
    "чек-листа достопримечательностей: важно быть в месте, а не "
    "«потреблять» виды.",
    "OTIUM — не туроператор. Это приглашение пройтись, остановиться "
    "и оставить маршрут незавершённым, если свет на фасаде заслуживает "
    "ещё минуты.",
)


def _guide_strings(edition: str) -> dict[str, str]:
    """UI chrome for one PDF language edition (en or ru)."""
    if edition == "ru":
        return {
            "lead": "Путеводитель. Объектов в этом выпуске: {}.",
            "facts_heading": "Факты и детали",
            "stories_heading": "Истории и легенды",
            "history_heading": "История",
            "significance_heading": "Значение",
            "address": "Адрес:",
            "style": "Стиль:",
            "period": "Период:",
            "img_alt_extra": "{} — вид {}",
            "html_title": "Путеводитель · {} · OTIUM",
        }
    return {
        "lead": "Guide. Places in this edition: {}.",
        "facts_heading": "Facts and details",
        "stories_heading": "Stories and legends",
        "history_heading": "History",
        "significance_heading": "Significance",
        "address": "Address:",
        "style": "Style:",
        "period": "Period:",
        "img_alt_extra": "{} — view {}",
        "html_title": "Guide · {} · OTIUM",
    }


def _place_sort_key(p: dict[str, Any]) -> tuple[str, str]:
    name = (p.get("name_en") or "").strip()
    if not name:
        name = (p.get("name_ru") or "").strip()
    return (name.lower(), str(p.get("slug", "")))


def places_with_local_images(
    root: Path,
    places: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return places_for_pdf(root, places, sort_key=_place_sort_key)


def _place_meta_line(p: dict[str, Any], edition: str) -> str | None:
    s = _guide_strings(edition)
    parts: list[str] = []
    if is_substantive_text(p.get("address")):
        parts.append(
            "{} {}".format(s["address"], str(p["address"]).strip()),
        )
    if is_substantive_text(p.get("architecture_style")):
        parts.append(
            "{} {}".format(
                s["style"],
                str(p["architecture_style"]).strip(),
            ),
        )
    if is_substantive_text(p.get("year_built")):
        parts.append(
            "{} {}".format(s["period"], str(p["year_built"]).strip()),
        )
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
    pairs: tuple[tuple[str, str, str | None], ...] = (
        ("subtitle_en", "sub-en", None),
        ("subtitle_de", "sub-de", None),
        ("subtitle_fr", "sub-fr", None),
        ("subtitle_es", "sub-es", None),
        ("subtitle_it", "sub-it", None),
        ("subtitle_ca", "sub-ca", None),
        ("subtitle_hu", "sub-hu", None),
        ("subtitle_cs", "sub-cs", None),
        ("subtitle_ja", "sub-ja", "ja"),
        ("subtitle_he", "sub-he", "he"),
    )
    for key, cls, lang_attr in pairs:
        if not is_substantive_text(p.get(key)):
            continue
        t = str(p[key])
        if lang_attr:
            return '<p class="{}" dir="{}" lang="{}">{}</p>'.format(
                cls,
                "rtl" if lang_attr == "he" else "ltr",
                lang_attr,
                escape(t),
            )
        return '<p class="{}">{}</p>'.format(cls, escape(t))
    return ""


def _place_title_parts(p: dict[str, Any], edition: str) -> tuple[str, str]:
    """(escaped heading HTML, plain string for img alt)."""
    if edition == "ru":
        nr = (p.get("name_ru") or "").strip()
        if nr:
            return escape(nr), nr
        ne = (p.get("name_en") or "").strip()
        if ne:
            return escape(ne), ne
    else:
        ne = (p.get("name_en") or "").strip()
        if ne:
            return escape(ne), ne
        nr = (p.get("name_ru") or "").strip()
        if nr:
            return escape(nr), nr
    slug = str(p.get("slug", "place"))
    return escape(slug), slug


def place_block(p: dict[str, Any], img_srcs: list[str], edition: str) -> str:
    s = _guide_strings(edition)
    name_h, name_plain = _place_title_parts(p, edition)
    sub_html = _subtitle_html(p)
    meta = _place_meta_line(p, edition)
    meta_html = (
        '<p class="place-meta">{}</p>'.format(escape(meta))
        if meta
        else ""
    )
    slug = str(p.get("slug", "x"))
    chunks: list[str] = [
        '<section class="place" id="{}">'.format(escape(slug)),
        "<h3>{}</h3>".format(name_h),
        sub_html,
        meta_html,
    ]
    for i, src in enumerate(img_srcs):
        alt = (
            name_plain
            if i == 0
            else s["img_alt_extra"].format(name_plain, i + 1)
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
                "<h4>{}</h4>\n"
                "<ul class=\"facts\">{}</ul>".format(
                    escape(s["facts_heading"]),
                    lis,
                )
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
                "<h4>{}</h4>\n"
                "<ul class=\"stories\">{}</ul>".format(
                    escape(s["stories_heading"]),
                    st_li,
                )
            )
    if is_substantive_text(p.get("history")):
        chunks.append("<h4>{}</h4>".format(escape(s["history_heading"])))
        chunks.append(_html_paragraphs(str(p["history"])))
    if is_substantive_text(p.get("significance")):
        chunks.append(
            "<h4>{}</h4>".format(escape(s["significance_heading"])),
        )
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
    edition: str,
) -> str:
    label = (
        HERALDRY_CHAPTER_LABEL_RU
        if edition == "ru"
        else HERALDRY_CHAPTER_LABEL_EN
    )
    label_esc = escape(label)
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


def cover_otium_html(edition: str) -> str:
    paras_src = _OTIUM_PARAS_RU if edition == "ru" else _OTIUM_PARAS_EN
    paras = "\n".join(
        '<p class="otiump">{}</p>'.format(escape(t)) for t in paras_src
    )
    return (
        '<section class="cover-otium">'
        '<h1 class="otium-logo">OTIUM</h1>'
        "{}"
        "</section>"
    ).format(paras)


def _historical_reference_block(
    city_slug: str,
    edition: str,
    project_root: Path | None,
) -> str:
    if edition == "ru":
        return historical_reference_section_html(
            reference_text_ru_for_any_city(city_slug, project_root),
        )
    body_en = reference_text_en_for_city(city_slug)
    if not body_en:
        return ""
    return historical_reference_section_html(
        body_en,
        section_title=HISTORICAL_SECTION_TITLE_EN,
    )


def _preamble_blocks(
    root: Path,
    *,
    city_slug: str,
    display_title: str,
    title_symbols_class: str,
    title_symbols: tuple[tuple[str, str], ...],
    places_count: int,
    edition: str,
    project_root: Path | None,
) -> list[str]:
    s = _guide_strings(edition)
    blocks: list[str] = [cover_otium_html(edition)]
    blocks.append(
        '<header class="guide-title">'
        "{}"
        "<h1 class=\"guide-title-main\">{}</h1>"
        "<p class=\"lead\">{}</p>"
        "</header>".format(
            heraldry_html(
                root,
                title_symbols_class,
                title_symbols,
                edition,
            ),
            escape(display_title),
            escape(s["lead"].format(places_count)),
        ),
    )
    hist = _historical_reference_block(city_slug, edition, project_root)
    if hist:
        blocks.append(hist)
    return blocks


def _place_section_blocks(
    root: Path,
    places: list[dict[str, Any]],
    edition: str,
) -> list[str]:
    out: list[str] = []
    for p in places:
        srcs = _image_srcs_for_place(root, p)
        if not srcs:
            continue
        out.append(place_block(p, srcs, edition))
    return out


def _wrap_guide_html(
    body_blocks: list[str],
    *,
    city_slug: str,
    display_title: str,
    title_symbols_class: str,
    edition: str,
    html_lang_attr: str | None = None,
) -> str:
    s = _guide_strings(edition)
    font_href, _, _ = typography_triple(city_slug)
    css = guide_inline_css(title_symbols_class, city_slug)
    root_lang = html_lang_attr if html_lang_attr else edition
    body_inner = "\n".join(body_blocks)
    return (
        "<!DOCTYPE html>\n"
        '<html lang="{}">\n<head>\n'
        '<meta charset="utf-8"/>\n'
        "<title>{}</title>\n"
        '<link rel="stylesheet" href="{}"/>\n'
        "<style>\n{}</style>\n</head>\n<body>\n{}\n</body>\n</html>\n"
    ).format(
        root_lang,
        escape(s["html_title"].format(display_title)),
        font_href,
        css,
        body_inner,
    )


def build_html(
    root: Path,
    *,
    city_slug: str,
    display_title: str,
    title_symbols_class: str,
    title_symbols: tuple[tuple[str, str], ...],
    places: list[dict[str, Any]],
    edition: str,
    html_lang_attr: str | None = None,
    project_root: Path | None = None,
) -> str:
    blocks = _preamble_blocks(
        root,
        city_slug=city_slug,
        display_title=display_title,
        title_symbols_class=title_symbols_class,
        title_symbols=title_symbols,
        places_count=len(places),
        edition=edition,
        project_root=project_root,
    )
    blocks.extend(_place_section_blocks(root, places, edition))
    return _wrap_guide_html(
        blocks,
        city_slug=city_slug,
        display_title=display_title,
        title_symbols_class=title_symbols_class,
        edition=edition,
        html_lang_attr=html_lang_attr,
    )


def _pdf_via_playwright_chunked(
    *,
    root: Path,
    out_dir: Path,
    stem: str,
    edition: str,
    places: list[dict[str, Any]],
    pdf_path: Path,
    city_slug: str,
    display_title: str,
    title_symbols_class: str,
    title_symbols: tuple[tuple[str, str], ...],
    html_lang_attr: str | None,
    project_root: Path | None,
    image_wait_timeout_ms: int,
    footer: str,
    header: str,
) -> bool:
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        print("pypdf required for chunked PDF merge.", file=sys.stderr)
        return False

    place_blocks = _place_section_blocks(root, places, edition)
    preface = _preamble_blocks(
        root,
        city_slug=city_slug,
        display_title=display_title,
        title_symbols_class=title_symbols_class,
        title_symbols=title_symbols,
        places_count=len(places),
        edition=edition,
        project_root=project_root,
    )
    chunk_list: list[list[str]] = []
    for i in range(0, len(place_blocks), PDF_CHUNK_MAX_PLACES):
        section = place_blocks[i : i + PDF_CHUNK_MAX_PLACES]
        if i == 0:
            chunk_list.append(preface + section)
        else:
            chunk_list.append(section)

    chunk_pdfs: list[Path] = []
    try:
        for idx, chunk_blocks in enumerate(chunk_list):
            print(
                "  PDF chunk {}/{}...".format(idx + 1, len(chunk_list)),
            )
            chunk_html_path = out_dir / "{}_{}_chunk_{}.html".format(
                stem,
                edition,
                idx,
            )
            chunk_pdf_path = out_dir / "{}_{}_chunk_{}.pdf".format(
                stem,
                edition,
                idx,
            )
            chunk_html_path.write_text(
                _wrap_guide_html(
                    chunk_blocks,
                    city_slug=city_slug,
                    display_title=display_title,
                    title_symbols_class=title_symbols_class,
                    edition=edition,
                    html_lang_attr=html_lang_attr,
                ),
                encoding="utf-8",
            )
            if not _pdf_via_playwright(
                chunk_html_path,
                chunk_pdf_path,
                image_wait_timeout_ms=image_wait_timeout_ms,
                display_header_footer=True,
                footer_template=footer,
                header_template=header,
                static_site_root=root,
            ):
                return False
            chunk_pdfs.append(chunk_pdf_path)

        writer = PdfWriter()
        for chunk_pdf in chunk_pdfs:
            reader = PdfReader(str(chunk_pdf))
            for page in reader.pages:
                writer.add_page(page)
        writer.write(str(pdf_path))
        return True
    finally:
        for chunk_pdf in chunk_pdfs:
            if chunk_pdf.is_file():
                try:
                    chunk_pdf.unlink()
                except OSError:
                    pass
        for idx in range(len(chunk_list)):
            chunk_html = out_dir / "{}_{}_chunk_{}.html".format(
                stem,
                edition,
                idx,
            )
            if chunk_html.is_file():
                try:
                    chunk_html.unlink()
                except OSError:
                    pass


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
    html_lang_attr: str | None = None,
) -> int:
    parser = argparse.ArgumentParser(
        description="Build {} HTML/PDF (en/ru editions).".format(display_title),
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
    parser.add_argument(
        "--lang",
        dest="langs",
        nargs="+",
        choices=("en", "ru"),
        default=("en", "ru"),
        metavar="LANG",
        help="Guide edition language(s): en, ru (default: both).",
    )
    args = parser.parse_args(argv)
    root = args.city_root.resolve()
    out_dir = (
        args.output_dir.resolve()
        if args.output_dir
        else root / "output"
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    if not pdf_name.endswith(".pdf") or not html_name.endswith(".html"):
        print(
            "pdf_name must end with .pdf and html_name with .html "
            "(e.g. berlin_guide.pdf).",
            file=sys.stderr,
        )
        return 2
    stem = pdf_name[:-4]
    if html_name[:-5] != stem:
        print(
            "html_name stem must match pdf_name stem (e.g. "
            "berlin_guide.html + berlin_guide.pdf).",
            file=sys.stderr,
        )
        return 2

    built = places_with_local_images(root, places)
    skipped = len(places) - len(built)
    if skipped:
        print(
            "Skipped {} place(s) without a local image.".format(skipped),
        )
    if not built:
        print(
            "No places with local images (>= {} bytes). "
            "Run download script first.".format(MIN_IMAGE_BYTES),
            file=sys.stderr,
        )
        return 2

    langs: tuple[str, ...] = tuple(dict.fromkeys(args.langs))
    footer = (
        "<div style='font-size:9px;text-align:center;width:100%'>"
        "<span class='pageNumber'></span> / <span class='totalPages'></span>"
        "</div>"
    )
    header = "<div style='font-size:9px;width:100%'></div>"

    for edition in langs:
        html_path = out_dir / "{}_{}.html".format(stem, edition)
        pdf_path = out_dir / "{}_{}.pdf".format(stem, edition)
        html_path.write_text(
            build_html(
                root,
                city_slug=city_slug,
                display_title=display_title,
                title_symbols_class=title_symbols_class,
                title_symbols=title_symbols,
                places=built,
                edition=edition,
                html_lang_attr=html_lang_attr,
                project_root=project_root,
            ),
            encoding="utf-8",
        )
        print("Written:", html_path)
        if args.html_only:
            continue
        use_chunked = len(built) > PDF_CHUNK_MAX_PLACES
        if use_chunked:
            pdf_ok = _pdf_via_playwright_chunked(
                root=root,
                out_dir=out_dir,
                stem=stem,
                edition=edition,
                places=built,
                pdf_path=pdf_path,
                city_slug=city_slug,
                display_title=display_title,
                title_symbols_class=title_symbols_class,
                title_symbols=title_symbols,
                html_lang_attr=html_lang_attr,
                project_root=project_root,
                image_wait_timeout_ms=args.image_wait_ms,
                footer=footer,
                header=header,
            )
        else:
            pdf_ok = _pdf_via_playwright(
                html_path,
                pdf_path,
                image_wait_timeout_ms=args.image_wait_ms,
                display_header_footer=True,
                footer_template=footer,
                header_template=header,
                static_site_root=root,
            )
        if pdf_ok:
            _strip_empty_pdf_pages(pdf_path)
            _strip_pdf_metadata(pdf_path)
            copy_built_guide_pdf_to_final_guides(project_root, pdf_path)
            print("Written:", pdf_path)
        else:
            print(
                "PDF failed ({}): pip install playwright && "
                "playwright install chromium".format(edition),
                file=sys.stderr,
            )
            return 1

    if args.html_only:
        print("Places in HTML: {}".format(len(built)))
    else:
        print("Places in PDF: {}".format(len(built)))

    primary = "en" if "en" in langs else langs[0]
    shutil.copy2(
        out_dir / "{}_{}.html".format(stem, primary),
        out_dir / html_name,
    )
    if not args.html_only:
        shutil.copy2(
            out_dir / "{}_{}.pdf".format(stem, primary),
            out_dir / pdf_name,
        )
        print("Primary edition ({}): {}".format(primary, out_dir / pdf_name))

    return 0


# Stable import name for SPB/Smolensk builders (same mapping as _guide_strings).
guide_ui_strings = _guide_strings
