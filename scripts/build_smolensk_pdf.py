# -*- coding: utf-8 -*-
"""HTML + PDF для Смоленска по уже лежащим в smolensk/images файлам."""

from __future__ import annotations

import argparse
import sys
from html import escape
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from smolensk.data.places_registry import SMOLENSK_PLACES, SmolenskPlace

from scripts.build_pdf import (
    _pdf_via_playwright,
    _strip_empty_pdf_pages,
    _strip_pdf_metadata,
)
from scripts.city_guide_core import MIN_IMAGE_BYTES, smallest_same_stem_image_rel


# Компактные иллюстрации для ранних карточек (стр. PDF 4–6 после титула).
_COMPACT_FIGURE_SLUGS: frozenset[str] = frozenset()
# Несколько кадров в один ряд (шире и выше, чем place-pdf-compact-fig).
_HORIZONTAL_FIG_ROW_SLUGS: frozenset[str] = frozenset(
    {
        "kremlin_memorial_burial",
        "kremlin_towers_view",
        "kutuzov_monument",
        "voznesensky_monastery",
    },
)
# Ровно два кадра — слева и справа (одна строка, ~половина ширины).
_HORIZONTAL_FIG_PAIR_SLUGS: frozenset[str] = frozenset(
    {
        "kremlin_memorial_burial",
        "kremlin_towers_view",
    },
)
SMOL_HTML_NAME = "smolensk_guide.html"
SMOL_PDF_NAME = "smolensk_guide.pdf"
_HERALD_COAT_REL = "images/guide_coat_of_arms.png"
_HERALD_FLAG_REL = "images/guide_flag.png"
# Исторические гербы и флаги — титул (файлы из download_smolensk_images).
_TITLE_HISTORY_COATS: tuple[tuple[str, str], ...] = (
    (
        "images/title_coat_governorate_1856.svg",
        "Герб смоленской губернии, 1856 (Commons)",
    ),
    (
        "images/title_coat_city_2000_il76m.jpg",
        "Герб города Смоленска, 2000 (Ил-76М), Commons",
    ),
    (
        "images/title_coat_oblast.svg",
        "Герб Смоленской области (SVG), Commons",
    ),
    (
        "images/title_coat_vinkler.gif",
        "Герб Смоленска по Винклеру, Commons",
    ),
    (
        "images/title_coat_soviet.png",
        "Герб Смоленска (советский вариант), Commons",
    ),
)
_TITLE_UNIVERSITIES: tuple[tuple[str, str], ...] = (
    (
        "images/title_univ_regional_3810.jpg",
        "Смоленский государственный университет",
    ),
    (
        "images/title_univ_regional_3827.jpg",
        "Смоленская государственная сельскохозяйственная академия",
    ),
    (
        "images/title_univ_regional_3840.jpg",
        "Смоленский государственный институт искусств",
    ),
    (
        "images/title_univ_regional_3866.jpg",
        (
            "Смоленский государственный медицинский университет "
            "Министерства здравоохранения Российской Федерации"
        ),
    ),
    (
        "images/title_univ_regional_3868.jpg",
        "Смоленский государственный университет спорта",
    ),
    (
        "images/title_univ_regional_3870.jpg",
        "Смоленская Православная Духовная Семинария",
    ),
    (
        "images/title_univ_regional_3986.jpg",
        (
            "Смоленский филиал Национального исследовательского "
            "университета «МЭИ»"
        ),
    ),
    (
        "images/title_univ_regional_4031.jpg",
        (
            "Смоленский филиал Российского экономического университета "
            "имени Г.В. Плеханова"
        ),
    ),
    (
        "images/title_univ_regional_4092.jpg",
        (
            "Смоленский филиал Финансового университета при Правительстве "
            "Российской Федерации"
        ),
    ),
    (
        "images/title_univ_regional_4337.jpg",
        (
            "Смоленский филиал Российской академии народного хозяйства и "
            "государственной службы при Президенте РФ"
        ),
    ),
)

_OTIUM_PARAS: tuple[str, ...] = (
    "OTIUM — это практика осмысленного досуга. В античной традиции otium "
    "означало не отдых от труда, а время, в котором человек возвращается к "
    "взгляду, памяти и мышлению. Это время без утилитарной цели, без "
    "спешки, без требования результата.",
    "Мы создаём маршруты не для «посещения», а для пребывания. Не для "
    "потребления культуры, а для внимательного присутствия в ней.",
    "OTIUM работает с пространствами, где время уплотняется: архитектурой, "
    "сакральными местами, кино, памятью, ландшафтом. Мы не стремимся "
    "охватить всё и не обещаем «лучшее». Мы отбираем немногое — то, что "
    "выдерживает тишину и повторный взгляд.",
    "OTIUM — это не гид и не сервис. Это приглашение к прогулке без "
    "обязательств. К маршруту, который можно прервать. К месту, где можно "
    "задержаться.",
    "OTIUM существует для тех, кто хочет смотреть медленно.",
)


def _place_has_displayable_body(p: SmolenskPlace) -> bool:
    """True if the place has text blocks worth a PDF section without photos."""
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


def _places_with_local_images(root: Path) -> list[SmolenskPlace]:
    out: list[SmolenskPlace] = []
    for p in SMOLENSK_PLACES:
        if p.get("suppress_images_for_pdf"):
            if _place_has_displayable_body(p):
                out.append(p)
            continue
        rel = p.get("image_rel_path")
        if not rel:
            continue
        if smallest_same_stem_image_rel(root, rel) is not None:
            out.append(p)
    out.sort(key=lambda x: (x.get("name_ru", ""), x.get("slug", "")))
    return out


def _nonempty(s: str | None) -> bool:
    return bool(s and str(s).strip())


def _place_meta_line(p: SmolenskPlace) -> str | None:
    parts: list[str] = []
    if _nonempty(p.get("address")):
        parts.append("Адрес: {}".format(p["address"].strip()))
    if _nonempty(p.get("architecture_style")):
        parts.append("Стиль: {}".format(p["architecture_style"].strip()))
    if _nonempty(p.get("year_built")):
        parts.append("Годы: {}".format(str(p["year_built"]).strip()))
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


def _image_srcs_for_place(root: Path, p: SmolenskPlace) -> list[str]:
    """Локальные картинки объекта: основная, затем additional_images."""
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


def _place_block(p: SmolenskPlace, img_srcs: list[str]) -> str:
    name_ru = escape(p.get("name_ru", ""))
    name_plain = p.get("name_ru", "")
    sub_en = p.get("subtitle_en", "")
    sub_html = (
        '<p class="sub-en">{}</p>'.format(escape(sub_en))
        if _nonempty(sub_en)
        else ""
    )
    meta = _place_meta_line(p)
    meta_html = (
        '<p class="place-meta">{}</p>'.format(escape(meta))
        if meta
        else ""
    )
    slug = p.get("slug", "x")
    place_cls = "place"
    if slug in _COMPACT_FIGURE_SLUGS:
        place_cls = "place place-pdf-compact-fig"
    chunks: list[str] = [
        '<section class="{}" id="{}">'.format(place_cls, escape(slug)),
        "<h3>{}</h3>".format(name_ru),
        sub_html,
        meta_html,
    ]
    row_open = slug in _HORIZONTAL_FIG_ROW_SLUGS and len(img_srcs) > 1
    row_class = "place-pdf-fig-row"
    if row_open and slug in _HORIZONTAL_FIG_PAIR_SLUGS:
        row_class = "place-pdf-fig-row place-pdf-fig-row--pair"
    if row_open:
        chunks.append('<div class="{}">'.format(row_class))
    for i, src in enumerate(img_srcs):
        alt = name_plain if i == 0 else "{} — вид {}".format(name_plain, i + 1)
        chunks.append(
            '<figure class="place-fig"><img src="{}" alt="{}"/></figure>'.format(
                escape(src),
                escape(alt),
            )
        )
    if row_open:
        chunks.append("</div>")
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
                "<h4>Факты и детали</h4>\n<ul class=\"facts\">{}</ul>".format(
                    lis,
                )
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
                "<h4>Истории и легенды</h4>\n"
                "<ul class=\"stories\">{}</ul>".format(st_li),
            )
    if _nonempty(p.get("history")):
        chunks.append("<h4>История</h4>")
        chunks.append(_html_paragraphs(p["history"]))
    if _nonempty(p.get("significance")):
        chunks.append("<h4>Значение</h4>")
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


def _univ_caption_text(alt: object) -> str:
    """Текст подписи вуза (как в _TITLE_UNIVERSITIES)."""
    if isinstance(alt, tuple):
        return "".join(alt)
    return str(alt)


def _university_figure_html(root: Path, rel: str, alt: object) -> str:
    """Логотип вуза с официальным названием под изображением."""
    resolved = smallest_same_stem_image_rel(root, rel)
    if not resolved:
        return ""
    caption = _univ_caption_text(alt)
    src = _rel_to_src(resolved)
    return (
        '<figure class="heraldry-fig heraldry-univ heraldry-univ-captioned" '
        'title="{}">'
        '<img src="{}" alt="{}"/>'
        '<figcaption class="univ-name-caption">{}</figcaption>'
        "</figure>".format(
            escape(caption),
            escape(src),
            escape(caption),
            escape(caption),
        )
    )


def _universities_section_html(root: Path) -> str:
    """Блок «Региональные вузы» в конце путеводителя."""
    figs: list[str] = []
    for rel, alt in _TITLE_UNIVERSITIES:
        fig = _university_figure_html(root, rel, alt)
        if fig:
            figs.append(fig)
    if not figs:
        return ""
    inner = "\n".join(figs)
    return (
        '<section class="guide-universities" aria-label="Региональные вузы">'
        '<p class="title-strip-label title-strip-label-univ">'
        "Региональные вузы</p>"
        '<div class="heraldry-strip heraldry-universities">'
        "{}"
        "</div>"
        "</section>"
    ).format(inner)


def _heraldry_html(root: Path) -> str:
    """Титул: исторические гербы, девиз, герб/флаг области."""
    chunks: list[str] = [
        '<div class="smolensk-title-symbols" '
        'aria-label="Исторические гербы и символика области">',
        '<p class="title-strip-label">Исторические и справочные гербы</p>',
        '<div class="heraldry-strip heraldry-history">',
    ]
    for rel, alt in _TITLE_HISTORY_COATS:
        fig = _fig_if_exists(root, rel, alt, "heraldry-coat-hist")
        if fig:
            chunks.append(fig)
    chunks.append("</div>")
    chunks.append(
        '<div class="heraldry-motto">'
        '<p class="motto-oldslav">Руси сторожевый градъ</p>'
        '<p class="motto-region">Смоленщина — край солнечный</p>'
        "</div>"
    )
    chunks.append('<p class="title-strip-label">Область (книжный герб и флаг)</p>')
    chunks.append('<div class="heraldry-strip heraldry-official">')
    coat_fig = _fig_if_exists(
        root,
        _HERALD_COAT_REL,
        "Герб Смоленской области",
        "heraldry-coat-book",
    )
    if coat_fig:
        chunks.append(coat_fig)
    flag_fig = _fig_if_exists(
        root,
        _HERALD_FLAG_REL,
        "Флаг Смоленской области",
        "heraldry-flag-book",
    )
    if flag_fig:
        chunks.append(flag_fig)
    chunks.append("</div></div>")
    return "\n".join(chunks)


def _cover_otium_html() -> str:
    paras = "\n".join(
        '<p class="otiump">{}</p>'.format(escape(t)) for t in _OTIUM_PARAS
    )
    return (
        '<section class="cover-otium">'
        '<h1 class="otium-logo">OTIUM</h1>'
        "{}"
        "</section>"
    ).format(paras)


def _build_html(root: Path, places: list[SmolenskPlace]) -> str:
    font_href = (
        "https://fonts.googleapis.com/css2?"
        "family=Cormorant+Garamond:wght@600&family=Ponomar&"
        "family=Source+Sans+3:wght@400;600&display=swap"
    )
    blocks: list[str] = [_cover_otium_html()]
    blocks.append(
        '<header class="guide-title">'
        "{}"
        "<h1 class=\"guide-title-main\">Смоленск</h1>"
        "<p class=\"lead\">Путеводитель. Объектов в этом выпуске: {}.</p>"
        "</header>".format(_heraldry_html(root), len(places)),
    )
    for p in places:
        srcs = _image_srcs_for_place(root, p)
        if not srcs and not (
            p.get("suppress_images_for_pdf") and _place_has_displayable_body(p)
        ):
            continue
        blocks.append(_place_block(p, srcs))
    univ = _universities_section_html(root)
    if univ:
        blocks.append(univ)
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
.smolensk-title-symbols { margin-bottom: 0.28rem; }
.guide-universities { margin-top: 2rem; page-break-inside: avoid; }
.title-strip-label { font-size: 0.72rem; text-transform: uppercase;
  letter-spacing: 0.08em; color: #555; margin: 0.5rem 0 0.25rem;
  text-align: center; width: 100%; }
.title-strip-label-univ { margin-top: 0.12rem; margin-bottom: 0.04rem;
  font-size: 0.58rem; }
.heraldry-strip { display: flex; flex-wrap: wrap; align-items: center;
  justify-content: center; gap: 0.45rem 0.65rem; margin: 0.2rem 0 0.45rem; }
.heraldry-strip.heraldry-universities { gap: 0.35rem 0.55rem;
  margin: 0.2rem 0 0.45rem; }
.heraldry-fig { margin: 0; }
.heraldry-fig img { width: auto; display: block; margin: 0 auto;
  border-radius: 2px; }
.heraldry-coat-hist img { max-height: 3.2rem; max-width: 3.5rem;
  object-fit: contain; }
.heraldry-coat-book img, .heraldry-flag-book img { max-height: 4.75rem;
  object-fit: contain; }
.heraldry-flag-book img { max-height: 3.35rem; }
.heraldry-fig.heraldry-univ img { max-height: 2.45rem; max-width: 6.25rem;
  object-fit: contain; }
figure.heraldry-fig.heraldry-univ.heraldry-univ-captioned {
  display: flex; flex-direction: column; align-items: center;
  max-width: 10.5rem; margin: 0.05rem 0.12rem; }
figure.heraldry-fig.heraldry-univ .univ-name-caption {
  font-family: 'Source Sans 3', sans-serif; font-size: 0.58rem;
  line-height: 1.18; text-align: center; margin: 0.12rem 0 0;
  padding: 0 0.08rem; max-width: 10.25rem; color: #2a2a2a; }
.heraldry-motto { text-align: center; max-width: 16rem; margin: 0.12rem auto;
  width: 100%; }
.motto-oldslav { font-family: 'Ponomar', 'Cormorant Garamond', serif;
  font-size: 1.02rem; line-height: 1.12; margin: 0 0 0.12rem; }
.motto-region { font-family: 'Ponomar', 'Cormorant Garamond', serif;
  font-size: 0.82rem; line-height: 1.15; margin: 0; color: #2a2a2a; }
.guide-title h1.guide-title-main { font-family: 'Ponomar', 'Cormorant Garamond',
  serif; font-size: 2.35rem; margin-bottom: 0.5rem; font-weight: 600; }
.lead { color: #444; font-size: 1.05rem; }
.place { margin-bottom: 2.2rem; page-break-inside: auto; }
h3 { font-size: 1.22rem; margin: 1.2rem 0 0.35rem; }
h4 { font-size: 0.95rem; text-transform: uppercase;
  letter-spacing: 0.06em; margin: 1rem 0 0.4rem; color: #333; }
.sub-en { color: #555; font-size: 0.95rem; margin: 0 0 0.5rem;
  font-style: italic; }
.place-meta { font-size: 0.92rem; color: #353535; margin: 0 0 0.75rem;
  line-height: 1.4; }
.place-fig { margin: 0.5rem 0 1rem; }
.place-pdf-compact-fig .place-fig { margin: 0.22rem 0 0.38rem; }
.place-pdf-compact-fig .place-fig img {
  max-height: 8.6rem; width: auto; max-width: 100%; object-fit: contain;
  margin: 0 auto; }
.place-pdf-fig-row {
  display: flex; flex-direction: row; flex-wrap: wrap;
  align-items: flex-end; justify-content: center;
  gap: 0.45rem 0.55rem; margin: 0.55rem 0 1.05rem; }
.place-pdf-fig-row .place-fig {
  flex: 1 1 30%; margin: 0; min-width: 26%; max-width: 100%; }
.place-pdf-fig-row .place-fig img {
  width: 100%; height: auto; max-height: 16.5rem; object-fit: contain;
  margin: 0 auto; }
.place-pdf-fig-row--pair {
  flex-wrap: nowrap; justify-content: space-between;
  align-items: flex-end; gap: 0.5rem 0.65rem; }
.place-pdf-fig-row--pair .place-fig {
  flex: 1 1 47%; min-width: 0; max-width: 50%; }
img { max-width: 100%; height: auto; display: block; border-radius: 4px; }
.prose, .place-desc p { margin: 0.45rem 0; line-height: 1.5;
  text-align: justify; }
ul.facts, ul.stories { margin: 0.3rem 0 0.6rem 1.2rem; padding: 0; }
ul.facts li, ul.stories li { margin: 0.25rem 0; line-height: 1.45; }
"""
    return (
        "<!DOCTYPE html>\n"
        '<html lang="ru">\n<head>\n'
        '<meta charset="utf-8"/>\n'
        "<title>Путеводитель · Смоленск · OTIUM</title>\n"
        '<link rel="stylesheet" href="{}"/>\n'
        "<style>\n{}</style>\n</head>\n<body>\n{}\n</body>\n</html>\n"
    ).format(font_href, css, body_inner)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build Smolensk HTML/PDF using only existing files under "
            "smolensk/images."
        ),
    )
    parser.add_argument(
        "--smolensk-root",
        type=Path,
        default=_PROJECT_ROOT / "smolensk",
        help="Smolensk tree root (default: smolensk/)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Where to write HTML/PDF (default: smolensk/output/)",
    )
    parser.add_argument(
        "--image-wait-ms",
        type=int,
        default=30000,
        metavar="MS",
        help="Playwright wait for images (default 30000).",
    )
    args = parser.parse_args()
    smol_root = args.smolensk_root.resolve()
    out_dir = (
        args.output_dir.resolve()
        if args.output_dir
        else smol_root / "output"
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    places = _places_with_local_images(smol_root)
    if not places:
        print(
            "No places with local images (>= {} bytes). "
            "Fill smolensk_places.json and run "
            "scripts/download_smolensk_images.py.".format(MIN_IMAGE_BYTES),
            file=sys.stderr,
        )
        return 2

    html_path = out_dir / SMOL_HTML_NAME
    pdf_path = out_dir / SMOL_PDF_NAME
    html_path.write_text(_build_html(smol_root, places), encoding="utf-8")
    print("Written:", html_path)

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
        static_site_root=smol_root,
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
