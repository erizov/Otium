# -*- coding: utf-8 -*-
"""HTML + PDF для SPB только по уже лежащим в spb/images файлам."""

from __future__ import annotations

import argparse
import sys
from html import escape
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from spb.data.places_registry import SPB_PLACES, SpbPlace

from scripts.build_pdf import (
    _pdf_via_playwright,
    _strip_empty_pdf_pages,
    _strip_pdf_metadata,
)

MIN_IMAGE_BYTES = 500
SPB_HTML_NAME = "spb_guide.html"
SPB_PDF_NAME = "spb_guide.pdf"
_HERALD_COAT_REL = "images/guide_coat_of_arms.png"
_HERALD_FLAG_REL = "images/guide_flag.svg"
_TITLE_HISTORY_COATS: tuple[tuple[str, str], ...] = (
    (
        "images/title_spb_coat_proposal_xix.svg",
        "Проект герба Санкт-Петербурга, XIX в. (Commons)",
    ),
    (
        "images/title_spb_coat_1730_1856.svg",
        "Герб Петербурга 1730–1856 (Commons)",
    ),
    (
        "images/title_russian_empire_great_coat_1882_1917.jpg",
        "Большой герб Российской империи, 1882–1917 (Commons)",
    ),
)
_TITLE_UNIVERSITIES: tuple[tuple[str, str], ...] = (
    (
        "images/title_univ_spbgu.jpg",
        (
            "Санкт-Петербургский государственный университет "
            "(здание Двенадцати коллегий)"
        ),
    ),
    (
        "images/title_univ_itmo.png",
        "Национальный исследовательский университет ИТМО",
    ),
    (
        "images/title_univ_spbpu.png",
        (
            "Санкт-Петербургский политехнический университет "
            "Петра Великого"
        ),
    ),
    (
        "images/title_univ_leti.svg",
        (
            "Санкт-Петербургский национальный исследовательский "
            "электротехнический университет им. В. И. Ульянова (Ленина)"
        ),
    ),
    (
        "images/title_univ_herzen.jpg",
        (
            "Российский государственный педагогический университет "
            "им. А. И. Герцена"
        ),
    ),
    (
        "images/title_univ_unecon.jpg",
        "Санкт-Петербургский государственный экономический университет",
    ),
    (
        "images/title_univ_pavlov.jpg",
        (
            "Первый Санкт-Петербургский государственный медицинский "
            "университет им. академика И. П. Павлова"
        ),
    ),
    (
        "images/title_univ_rshu.jpg",
        (
            "Российский государственный гидрометеорологический "
            "университет"
        ),
    ),
    (
        "images/title_univ_lesgaft.png",
        (
            "Национальный государственный университет физической "
            "культуры, спорта и здоровья им. П. Ф. Лесгафта"
        ),
    ),
    (
        "images/title_univ_pushkin.jpg",
        (
            "Санкт-Петербургский государственный университет "
            "(г. Пушкин)"
        ),
    ),
)

# (заголовок раздела, одна, две–четыре, пять+)
_CHAPTER: dict[str, tuple[str, str, str, str]] = {
    "palaces": ("Дворцы", "дворец", "дворца", "дворцов"),
    "places_of_worship": (
        "Храмы и святыни",
        "храм",
        "храма",
        "храмов",
    ),
    "landmarks": (
        "Достопримечательности",
        "достопримечательность",
        "достопримечательности",
        "достопримечательностей",
    ),
    "squares": ("Площади", "площадь", "площади", "площадей"),
    "theaters": ("Театры", "театр", "театра", "театров"),
    "museums": ("Музеи", "музей", "музея", "музеев"),
    "bridges": ("Мосты", "мост", "моста", "мостов"),
    "metro_stations": (
        "Станции метро",
        "станция",
        "станции",
        "станций",
    ),
    "railway_stations": (
        "Вокзалы",
        "вокзал",
        "вокзала",
        "вокзалов",
    ),
    "parks": ("Парки и сады", "парк", "парка", "парков"),
    "monasteries": (
        "Монастыри",
        "монастырь",
        "монастыря",
        "монастырей",
    ),
    "sculptures": (
        "Скульптуры и памятники",
        "скульптура и памятник",
        "скульптуры и памятника",
        "скульптур и памятников",
    ),
    "buildings": ("Здания", "здание", "здания", "зданий"),
    "markets": ("Рынки", "рынок", "рынка", "рынков"),
    "cafes": ("Кафе и гастрономия", "", "", ""),
    "libraries": (
        "Библиотеки",
        "библиотека",
        "библиотеки",
        "библиотек",
    ),
    "viewpoints": (
        "Виды и смотровые точки",
        "точка",
        "точки",
        "точек",
    ),
    "cemeteries": (
        "Кладбища",
        "кладбище",
        "кладбища",
        "кладбищ",
    ),
}

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


def _ru_count_phrase(n: int, one: str, few: str, many: str) -> str:
    na = abs(n) % 100
    n1 = na % 10
    if 10 <= na <= 20:
        w = many
    elif n1 == 1:
        w = one
    elif 2 <= n1 <= 4:
        w = few
    else:
        w = many
    return "{} {}".format(n, w)


def _chapter_heading(cat: str, count: int) -> tuple[str, str]:
    meta = _CHAPTER.get(
        cat,
        ("Раздел", "объект", "объекта", "объектов"),
    )
    title, one, few, many = meta
    h2 = "{} Санкт-Петербурга".format(title)
    if cat == "cafes":
        sub = "{} кафе".format(count)
    else:
        sub = _ru_count_phrase(count, one, few, many)
    return h2, sub


def _places_with_local_images(spb_root: Path) -> list[SpbPlace]:
    out: list[SpbPlace] = []
    for p in SPB_PLACES:
        rel = p.get("image_rel_path")
        if not rel:
            continue
        path = spb_root / rel
        if path.is_file() and path.stat().st_size >= MIN_IMAGE_BYTES:
            out.append(p)
    out.sort(
        key=lambda x: (
            x.get("category", ""),
            x.get("name_ru", ""),
        ),
    )
    return out


def _counts_by_category(places: list[SpbPlace]) -> dict[str, int]:
    c: dict[str, int] = {}
    for p in places:
        k = p.get("category", "misc")
        c[k] = c.get(k, 0) + 1
    return c


def _nonempty(s: str | None) -> bool:
    return bool(s and str(s).strip())


def _place_meta_line(p: SpbPlace) -> str | None:
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


def _image_srcs_for_place(root: Path, p: SpbPlace) -> list[str]:
    """Основное + доп. фото, только если файлы на диске."""
    out: list[str] = []
    primary = p.get("image_rel_path")
    if primary:
        pp = root / primary
        if pp.is_file() and pp.stat().st_size >= MIN_IMAGE_BYTES:
            out.append(_rel_to_src(primary))
    for extra in p.get("additional_images") or []:
        rel = extra.get("image_rel_path")
        if not rel:
            continue
        path = root / rel
        if path.is_file() and path.stat().st_size >= MIN_IMAGE_BYTES:
            out.append(_rel_to_src(rel))
    return out


def _place_figures_html(name_plain: str, img_srcs: list[str]) -> str:
    if not img_srcs:
        return ""
    figs: list[str] = []
    for i, src in enumerate(img_srcs):
        alt = name_plain if i == 0 else "{} (фото {})".format(name_plain, i + 1)
        figs.append(
            '<figure class="place-fig"><img src="{}" alt="{}"/></figure>'.format(
                escape(src),
                escape(alt),
            )
        )
    if len(figs) == 1:
        return figs[0]
    return '<div class="place-fig-row">\n{}\n</div>'.format("\n".join(figs))


def _place_block(p: SpbPlace, img_srcs: list[str]) -> str:
    name_plain = p.get("name_ru", "")
    name_ru = escape(name_plain)
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
    chunks: list[str] = [
        '<section class="place" id="{}">'.format(escape(p.get("slug", "x"))),
        "<h3>{}</h3>".format(name_ru),
        sub_html,
        meta_html,
        _place_figures_html(name_plain, img_srcs),
    ]
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


def _rel_to_src(rel: str) -> str:
    return "../{}".format(rel.lstrip("/").replace("\\", "/"))


def _fig_if_exists(root: Path, rel: str, alt: str, extra_class: str) -> str:
    path = root / rel
    if not path.is_file() or path.stat().st_size < MIN_IMAGE_BYTES:
        return ""
    src = _rel_to_src(rel)
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


def _univ_fig_if_exists(root: Path, rel: str, alt: str) -> str:
    """Титул: вуз с видимой подписью (официальное имя) под эмблемой."""
    path = root / rel
    if not path.is_file() or path.stat().st_size < MIN_IMAGE_BYTES:
        return ""
    src = _rel_to_src(rel)
    ea = escape(alt)
    return (
        '<div class="heraldry-univ-cell">'
        '<figure class="heraldry-fig heraldry-univ" title="{}">'
        '<img src="{}" alt="{}"/>'
        '<figcaption class="heraldry-univ-caption">{}</figcaption>'
        "</figure>"
        "</div>"
    ).format(ea, escape(src), ea, ea)


def _heraldry_html(spb_root: Path) -> str:
    """Титул: исторические гербы, девиз, герб/флаг города, ведущие вузы."""
    chunks: list[str] = [
        '<div class="spb-title-symbols" aria-label="Гербы, флаг и вузы '
        'Санкт-Петербурга">',
        '<p class="title-strip-label">Исторические гербы</p>',
        '<div class="heraldry-strip heraldry-history">',
    ]
    for rel, alt in _TITLE_HISTORY_COATS:
        fig = _fig_if_exists(spb_root, rel, alt, "heraldry-coat-hist")
        if fig:
            chunks.append(fig)
    chunks.append("</div>")
    chunks.append(
        '<div class="heraldry-motto">'
        '<p class="motto-line">Город федерального значения</p>'
        "</div>"
    )
    chunks.append(
        '<p class="title-strip-label">Символика города (нынешний герб '
        "и флаг)</p>"
    )
    chunks.append('<div class="heraldry-strip heraldry-official">')
    coat_p = spb_root / _HERALD_COAT_REL
    if coat_p.is_file() and coat_p.stat().st_size >= MIN_IMAGE_BYTES:
        chunks.append(
            _fig_if_exists(
                spb_root,
                _HERALD_COAT_REL,
                "Герб Санкт-Петербурга",
                "heraldry-coat-book",
            )
        )
    flag_p = spb_root / _HERALD_FLAG_REL
    if flag_p.is_file() and flag_p.stat().st_size >= MIN_IMAGE_BYTES:
        chunks.append(
            _fig_if_exists(
                spb_root,
                _HERALD_FLAG_REL,
                "Флаг Санкт-Петербурга",
                "heraldry-flag-book",
            )
        )
    chunks.append("</div>")
    chunks.append(
        '<p class="title-strip-label">'
        "Ведущие вузы Санкт-Петербурга"
        "</p>"
    )
    chunks.append('<div class="heraldry-strip heraldry-universities">')
    for rel, alt in _TITLE_UNIVERSITIES:
        fig = _univ_fig_if_exists(spb_root, rel, alt)
        if fig:
            chunks.append(fig)
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


def _build_html(spb_root: Path, places: list[SpbPlace]) -> str:
    font_href = (
        "https://fonts.googleapis.com/css2?"
        "family=Cormorant+Garamond:wght@600&family=Source+Sans+3:wght@400;600"
        "&display=swap"
    )
    counts = _counts_by_category(places)
    blocks: list[str] = [_cover_otium_html()]
    blocks.append(
        '<header class="guide-title">'
        "{}"
        "<h1>Санкт-Петербург</h1>"
        "<p class=\"lead\">Путеводитель. Объектов в этом выпуске: {}.</p>"
        "</header>".format(_heraldry_html(spb_root), len(places)),
    )
    last_cat: str | None = None
    for p in places:
        cat = p.get("category", "misc")
        if cat != last_cat:
            h2, sub = _chapter_heading(cat, counts.get(cat, 0))
            blocks.append(
                '<div class="chapter-head">'
                "<h2>{}</h2>"
                '<p class="chapter-count">{}</p>'
                "</div>".format(escape(h2), escape(sub)),
            )
            last_cat = cat
        srcs = _image_srcs_for_place(spb_root, p)
        if not srcs:
            continue
        blocks.append(_place_block(p, srcs))
    body_inner = "\n".join(blocks)
    css = """
body { font-family: 'Source Sans 3', sans-serif; margin: 2rem;
  color: #1a1a1a; font-size: 11pt; }
.cover-otium { page-break-after: always; min-height: 85vh;
  padding: 2rem 1rem 3rem; box-sizing: border-box; }
.otium-logo { font-family: 'Cormorant Garamond', serif; font-size: 3rem;
  font-weight: 600; letter-spacing: 0.2em; margin-bottom: 2rem; }
.otiump { margin: 0.9rem 0; line-height: 1.55; text-align: justify;
  max-width: 40rem; }
.guide-title { page-break-after: always; margin-bottom: 1rem;
  page-break-inside: avoid; }
.spb-title-symbols { margin-bottom: 0.45rem; }
.title-strip-label { font-size: 0.72rem; text-transform: uppercase;
  letter-spacing: 0.08em; color: #555; margin: 0.5rem 0 0.25rem;
  text-align: center; width: 100%; }
.title-strip-note { font-size: 0.68rem; color: #666; margin: 0 0 0.35rem;
  text-align: center; max-width: 38rem; margin-left: auto;
  margin-right: auto; line-height: 1.35; }
.heraldry-strip { display: flex; flex-wrap: wrap; align-items: center;
  justify-content: center; gap: 0.35rem 0.55rem; margin: 0.2rem 0 0.45rem; }
.heraldry-strip.heraldry-universities { gap: 0.2rem 0.35rem;
  margin: 0.12rem 0 0.35rem; align-items: flex-start; }
.heraldry-fig { margin: 0; }
.heraldry-fig img { width: auto; display: block; margin: 0 auto;
  border-radius: 2px; }
.heraldry-coat-hist img { max-height: 2.55rem; max-width: 2.85rem;
  object-fit: contain; }
.heraldry-coat-book img { max-height: 4.2rem; object-fit: contain; }
.heraldry-flag-book img { max-height: 2.75rem; object-fit: contain; }
.heraldry-univ-cell { flex: 0 1 5.6rem; max-width: 5.85rem;
  display: flex; justify-content: center; }
.heraldry-univ .heraldry-fig { width: 100%; }
.heraldry-univ .heraldry-fig img { max-height: 1.05rem; max-width: 100%;
  object-fit: contain; }
.heraldry-univ-caption { font-size: 0.52rem; line-height: 1.18;
  margin: 0.12rem 0 0; padding: 0 0.06rem; color: #252525;
  text-align: center; font-weight: 500; }
.heraldry-motto { text-align: center; max-width: 18rem; margin: 0.18rem auto;
  width: 100%; }
.motto-line { font-family: 'Cormorant Garamond', serif; font-size: 1rem;
  margin: 0; color: #333; line-height: 1.35; }
.guide-title h1 { font-family: 'Cormorant Garamond', serif; font-size: 2.4rem;
  margin-bottom: 0.5rem; }
.lead { color: #444; font-size: 1.05rem; }
.chapter-head { margin-top: 2.2rem; border-bottom: 1px solid #bbb;
  padding-bottom: 0.35rem;
  page-break-after: avoid; break-after: avoid; }
/* Первый объект главы не переносим на следующую страницу без заголовка. */
.chapter-head + .place { page-break-before: avoid; break-before: avoid; }
h2 { font-family: 'Cormorant Garamond', serif; font-size: 1.55rem;
  margin: 0 0 0.25rem; }
.chapter-count { margin: 0 0 1rem; color: #333; font-size: 1rem; }
.place { margin-bottom: 2.5rem; page-break-inside: avoid; }
h3 { font-size: 1.22rem; margin: 1.2rem 0 0.35rem; }
h4 { font-size: 0.95rem; text-transform: uppercase;
  letter-spacing: 0.06em; margin: 1rem 0 0.4rem; color: #333; }
.sub-en { color: #555; font-size: 0.95rem; margin: 0 0 0.5rem;
  font-style: italic; }
.place-meta { font-size: 0.92rem; color: #353535; margin: 0 0 0.75rem;
  line-height: 1.4; }
.place-fig { margin: 0.5rem 0 1rem; }
.place-fig-row { display: flex; flex-wrap: wrap; gap: 0.45rem 0.65rem;
  align-items: flex-start; margin: 0.45rem 0 0.85rem;
  page-break-inside: avoid; }
.place-fig-row .place-fig { flex: 1 1 42%; max-width: calc(50% - 0.35rem);
  margin: 0; min-width: 9.5rem; box-sizing: border-box; }
.place-fig-row .place-fig img { width: 100%; height: auto; }
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
        "<title>Путеводитель · Санкт-Петербург · OTIUM</title>\n"
        '<link rel="stylesheet" href="{}"/>\n'
        "<style>\n{}</style>\n</head>\n<body>\n{}\n</body>\n</html>\n"
    ).format(font_href, css, body_inner)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build SPB HTML/PDF using only existing files under spb/images.",
    )
    parser.add_argument(
        "--spb-root",
        type=Path,
        default=_PROJECT_ROOT / "spb",
        help="SPB tree root (default: spb/)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Where to write HTML/PDF (default: spb/output/)",
    )
    parser.add_argument(
        "--image-wait-ms",
        type=int,
        default=30000,
        metavar="MS",
        help="Playwright wait for images (default 30000).",
    )
    args = parser.parse_args()
    spb_root = args.spb_root.resolve()
    out_dir = (
        args.output_dir.resolve()
        if args.output_dir
        else spb_root / "output"
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    places = _places_with_local_images(spb_root)
    if not places:
        print(
            "No places with local images (>= {} bytes). "
            "Fill SPB_PLACES and run scripts/download_spb_images.py.".format(
                MIN_IMAGE_BYTES,
            ),
            file=sys.stderr,
        )
        return 2

    html_path = out_dir / SPB_HTML_NAME
    pdf_path = out_dir / SPB_PDF_NAME
    html_path.write_text(_build_html(spb_root, places), encoding="utf-8")
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
        static_site_root=spb_root,
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
