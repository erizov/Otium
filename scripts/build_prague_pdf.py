# -*- coding: utf-8 -*-
"""HTML + PDF for Prague from files under prague/images/."""

from __future__ import annotations

import argparse
import sys
from html import escape
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from prague.data.places_registry import PRAGUE_PLACES, PraguePlace

from scripts.build_pdf import (
    _pdf_via_playwright,
    _strip_empty_pdf_pages,
    _strip_pdf_metadata,
)
from scripts.city_guide_core import MIN_IMAGE_BYTES, smallest_same_stem_image_rel

PRAGUE_HTML_NAME = "prague_guide.html"
PRAGUE_PDF_NAME = "prague_guide.pdf"

_TITLE_SYMBOLS: tuple[tuple[str, str], ...] = (
    (
        "images/guide_coat_of_arms.svg",
        "Coat of arms of Prague (Wikimedia Commons)",
    ),
    (
        "images/guide_flag.svg",
        "Flag of Prague (Wikimedia Commons)",
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


def _place_has_displayable_body(p: PraguePlace) -> bool:
    if _nonempty(p.get("description")):
        return True
    if _nonempty(p.get("history")):
        return True
    if _nonempty(p.get("significance")):
        return True
    facts = p.get("facts") or []
    if any(str(x).strip() for x in facts):
        return True
    stories = p.get("stories") or []
    return any(str(x).strip() for x in stories)


def _places_with_local_images(root: Path) -> list[PraguePlace]:
    out: list[PraguePlace] = []
    for p in PRAGUE_PLACES:
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


def _place_meta_line(p: PraguePlace) -> str | None:
    parts: list[str] = []
    if _nonempty(p.get("address")):
        parts.append("Address: {}".format(p["address"].strip()))
    if _nonempty(p.get("architecture_style")):
        parts.append("Style: {}".format(p["architecture_style"].strip()))
    if _nonempty(p.get("year_built")):
        parts.append("Period: {}".format(str(p["year_built"]).strip()))
    if not parts:
        return None
    return " | ".join(parts)


def _html_paragraphs(text: str) -> str:
    chunks = [t.strip() for t in text.split("\n\n") if t.strip()]
    return "\n".join(
        "<p class=\"prose\">{}</p>".format(escape(c)) for c in chunks
    )


def _rel_to_src(rel: str) -> str:
    return "../{}".format(rel.lstrip("/").replace("\\", "/"))


def _image_srcs_for_place(root: Path, p: PraguePlace) -> list[str]:
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


def _place_block(p: PraguePlace, img_srcs: list[str]) -> str:
    name_en = escape(p.get("name_en", ""))
    name_plain = p.get("name_en", "")
    sub_cs = p.get("subtitle_cs", "")
    sub_html = (
        '<p class="sub-cs">{}</p>'.format(escape(sub_cs))
        if _nonempty(sub_cs)
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
    if _nonempty(p.get("description")):
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
            if str(f).strip()
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
            if str(s).strip()
        )
        if st_li:
            chunks.append(
                "<h4>Stories and legends</h4>\n"
                "<ul class=\"stories\">{}</ul>".format(st_li),
            )
    if _nonempty(p.get("history")):
        chunks.append("<h4>History</h4>")
        chunks.append(_html_paragraphs(p["history"]))
    if _nonempty(p.get("significance")):
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
        '<div class="prague-title-symbols" '
        'aria-label="Prague coat of arms and flag">',
        '<p class="title-strip-label">City symbols</p>',
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


def _build_html(root: Path, places: list[PraguePlace]) -> str:
    font_href = (
        "https://fonts.googleapis.com/css2?"
        "family=Cormorant+Garamond:wght@600&"
        "family=Source+Sans+3:wght@400;600&display=swap"
    )
    blocks: list[str] = [_cover_otium_html()]
    blocks.append(
        '<header class="guide-title">'
        "{}"
        "<h1 class=\"guide-title-main\">Prague</h1>"
        "<p class=\"lead\">Guide. Places in this edition: {}.</p>"
        "</header>".format(_heraldry_html(root), len(places)),
    )
    for p in places:
        srcs = _image_srcs_for_place(root, p)
        if not srcs and not (
            p.get("suppress_images_for_pdf") and _place_has_displayable_body(p)
        ):
            continue
        blocks.append(_place_block(p, srcs))
    body_inner = "\n".join(blocks)
    css = """
body { font-family: 'Source Sans 3', sans-serif; margin: 2rem;
  color: #1a1a1a; font-size: 11pt; }
.cover-otium { page-break-after: always; min-height: auto;
  padding: 1.15rem 0.85rem 1.35rem; box-sizing: border-box; }
.otium-logo { font-family: 'Cormorant Garamond', serif; font-size: 2.15rem;
  font-weight: 600; letter-spacing: 0.18em; margin-bottom: 0.85rem; }
.otiump { margin: 0.42rem 0; line-height: 1.42; text-align: justify;
  max-width: 38rem; font-size: 0.95rem; }
.guide-title { page-break-after: auto; margin-bottom: 0.55rem;
  page-break-inside: avoid; }
.prague-title-symbols { margin-bottom: 0.28rem; }
.title-strip-label { font-size: 0.72rem; text-transform: uppercase;
  letter-spacing: 0.08em; color: #555; margin: 0.5rem 0 0.25rem;
  text-align: center; width: 100%; }
.heraldry-strip { display: flex; flex-wrap: wrap; align-items: center;
  justify-content: center; gap: 0.35rem 0.55rem; margin: 0.2rem 0 0.45rem; }
.heraldry-fig { margin: 0; }
.heraldry-fig img { width: auto; display: block; margin: 0 auto;
  border-radius: 2px; }
.heraldry-coat-book img { max-height: 3.35rem; object-fit: contain; }
.guide-title h1.guide-title-main { font-family: 'Cormorant Garamond',
  serif; font-size: 2.35rem; margin-bottom: 0.5rem; font-weight: 600; }
.lead { color: #444; font-size: 1.05rem; }
.place { margin-bottom: 2.2rem; page-break-inside: auto; }
h3 { font-size: 1.22rem; margin: 1.2rem 0 0.35rem; }
h4 { font-size: 0.95rem; text-transform: uppercase;
  letter-spacing: 0.06em; margin: 1rem 0 0.4rem; color: #333; }
.sub-cs { color: #555; font-size: 0.95rem; margin: 0 0 0.5rem;
  font-style: italic; }
.place-meta { font-size: 0.92rem; color: #353535; margin: 0 0 0.75rem;
  line-height: 1.4; }
.place-fig { margin: 0.5rem 0 1rem; }
img { max-width: 100%; height: auto; display: block; border-radius: 4px; }
.prose, .place-desc p { margin: 0.45rem 0; line-height: 1.5;
  text-align: justify; }
ul.facts, ul.stories { margin: 0.3rem 0 0.6rem 1.2rem; padding: 0; }
ul.facts li, ul.stories li { margin: 0.25rem 0; line-height: 1.45; }
"""
    return (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n<head>\n'
        '<meta charset="utf-8"/>\n'
        "<title>Guide · Prague · OTIUM</title>\n"
        '<link rel="stylesheet" href="{}"/>\n'
        "<style>\n{}</style>\n</head>\n<body>\n{}\n</body>\n</html>\n"
    ).format(font_href, css, body_inner)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build Prague HTML/PDF using files under prague/images."
        ),
    )
    parser.add_argument(
        "--prague-root",
        type=Path,
        default=_PROJECT_ROOT / "prague",
        help="Prague tree root (default: prague/)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory (default: prague/output/)",
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
    prague_root = args.prague_root.resolve()
    out_dir = (
        args.output_dir.resolve()
        if args.output_dir
        else prague_root / "output"
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    places = _places_with_local_images(prague_root)
    if not places:
        print(
            "No places with local images (>= {} bytes). "
            "Fill prague_places.json and run "
            "scripts/download_prague_images.py.".format(MIN_IMAGE_BYTES),
            file=sys.stderr,
        )
        return 2

    html_path = out_dir / PRAGUE_HTML_NAME
    html_path.write_text(_build_html(prague_root, places), encoding="utf-8")
    print("Written:", html_path)

    if args.html_only:
        print("Places in HTML: {}".format(len(places)))
        return 0

    pdf_path = out_dir / PRAGUE_PDF_NAME
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
        static_site_root=prague_root,
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
