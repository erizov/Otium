# -*- coding: utf-8 -*-
"""HTML + PDF для SPB только по уже лежащим в spb/images файлам."""

from __future__ import annotations

import argparse
import shutil
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
from scripts.city_guide_core import (
    copy_built_guide_pdf_to_final_guides,
    places_for_pdf,
)
from scripts.city_guide_historical_reference_ru import (
    HERALDRY_CHAPTER_LABEL_EN,
    HERALDRY_CHAPTER_LABEL_RU,
    HISTORICAL_SECTION_TITLE_EN,
    HISTORICAL_SECTION_TITLE_RU,
    historical_reference_section_html,
    reference_text_en_for_city,
    reference_text_ru_for_any_city,
)
from scripts.city_guide_jerusalem_style_pdf import guide_ui_strings

MIN_IMAGE_BYTES = 500
SPB_HTML_NAME = "spb_guide.html"
SPB_PDF_NAME = "spb_guide.pdf"
_HERALD_COAT_REL = "images/guide_coat_of_arms.png"
_HERALD_FLAG_REL = "images/guide_flag.svg"
_TITLE_HISTORY_COATS: tuple[tuple[str, str], ...] = (
    (
        "images/title_spb_coat_proposal_xix.svg",
        "Проект герба Санкт-Петербурга, XIX в.",
    ),
    (
        "images/title_spb_coat_1730_1856.svg",
        "Герб Петербурга 1730–1856",
    ),
    (
        "images/title_russian_empire_great_coat_1882_1917.jpg",
        "Большой герб Российской империи, 1882–1917",
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

_CHAPTER_EN: dict[str, tuple[str, str, str]] = {
    "palaces": ("Palaces", "palace", "palaces"),
    "places_of_worship": (
        "Temples and shrines",
        "temple",
        "temples",
    ),
    "landmarks": ("Landmarks", "landmark", "landmarks"),
    "squares": ("Squares", "square", "squares"),
    "theaters": ("Theatres", "theatre", "theatres"),
    "museums": ("Museums", "museum", "museums"),
    "bridges": ("Bridges", "bridge", "bridges"),
    "metro_stations": ("Metro stations", "station", "stations"),
    "railway_stations": ("Railway stations", "station", "stations"),
    "parks": ("Parks and gardens", "park", "parks"),
    "monasteries": ("Monasteries", "monastery", "monasteries"),
    "sculptures": (
        "Sculptures and monuments",
        "sculpture or monument",
        "sculptures and monuments",
    ),
    "buildings": ("Buildings", "building", "buildings"),
    "markets": ("Markets", "market", "markets"),
    "cafes": ("Cafés and gastronomy", "", ""),
    "libraries": ("Libraries", "library", "libraries"),
    "viewpoints": ("Views and viewpoints", "viewpoint", "viewpoints"),
    "cemeteries": ("Cemeteries", "cemetery", "cemeteries"),
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

_OTIUM_PARAS_EN: tuple[str, ...] = (
    "OTIUM is the practice of meaningful leisure. In the classical "
    "tradition, otium is not time away from work but time when one "
    "returns to sight, memory, and thinking—without utilitarian goals, "
    "hurry, or pressure to produce a result.",
    "We design routes not for ticking boxes but for staying present—not "
    "for consuming culture but for being inside it with attention.",
    "OTIUM works with spaces where time thickens: architecture, sacred "
    "places, cinema, memory, landscape. We do not try to cover everything "
    "or promise a 'best of' list; we keep a small selection that survives "
    "silence and a second look.",
    "OTIUM is neither a tour operator nor a service. It is an invitation "
    "to walk without obligation—to follow a route you can interrupt—to "
    "linger where the light asks for another minute.",
    "OTIUM is for those who want to look slowly.",
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


def _en_count_phrase(n: int, one: str, many: str) -> str:
    if n == 1:
        return "1 {}".format(one)
    return "{} {}".format(n, many)


def _chapter_heading(cat: str, count: int, edition: str) -> tuple[str, str]:
    if edition == "ru":
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
    meta_en = _CHAPTER_EN.get(
        cat,
        ("Section", "item", "items"),
    )
    title_en, one_en, many_en = meta_en
    h2 = "{} of Saint Petersburg".format(title_en)
    if cat == "cafes":
        sub = "{} cafés".format(count)
    else:
        sub = _en_count_phrase(count, one_en, many_en)
    return h2, sub


def _places_with_local_images(spb_root: Path) -> list[SpbPlace]:
    return places_for_pdf(
        spb_root,
        SPB_PLACES,
        sort_key=lambda x: (x.get("category", ""), x.get("name_ru", "")),
    )


def _counts_by_category(places: list[SpbPlace]) -> dict[str, int]:
    c: dict[str, int] = {}
    for p in places:
        k = p.get("category", "misc")
        c[k] = c.get(k, 0) + 1
    return c


def _nonempty(s: str | None) -> bool:
    return bool(s and str(s).strip())


def _place_meta_line(p: SpbPlace, edition: str) -> str | None:
    s = guide_ui_strings(edition)
    parts: list[str] = []
    if _nonempty(p.get("address")):
        parts.append("{} {}".format(s["address"], p["address"].strip()))
    if _nonempty(p.get("architecture_style")):
        parts.append(
            "{} {}".format(s["style"], p["architecture_style"].strip()),
        )
    if _nonempty(p.get("year_built")):
        parts.append(
            "{} {}".format(s["period"], str(p["year_built"]).strip()),
        )
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


def _place_figures_html(
    name_plain: str,
    img_srcs: list[str],
    edition: str,
) -> str:
    if not img_srcs:
        return ""
    s = guide_ui_strings(edition)
    figs: list[str] = []
    for i, src in enumerate(img_srcs):
        if i == 0:
            alt = name_plain
        else:
            alt = s["img_alt_extra"].format(name_plain, i + 1)
        figs.append(
            '<figure class="place-fig"><img src="{}" alt="{}"/></figure>'.format(
                escape(src),
                escape(alt),
            )
        )
    if len(figs) == 1:
        return figs[0]
    return '<div class="place-fig-row">\n{}\n</div>'.format("\n".join(figs))


def _place_block(p: SpbPlace, img_srcs: list[str], edition: str) -> str:
    s = guide_ui_strings(edition)
    name_ru = p.get("name_ru", "")
    sub_en = p.get("subtitle_en", "")
    if edition == "ru":
        name_plain = name_ru
        title_plain = name_ru
        title_html = escape(name_ru)
        sub_html = (
            '<p class="sub-en">{}</p>'.format(escape(sub_en))
            if _nonempty(sub_en)
            else ""
        )
    else:
        title_plain = sub_en.strip() if _nonempty(sub_en) else name_ru
        title_html = escape(title_plain)
        sub_html = (
            '<p class="sub-en">{}</p>'.format(escape(name_ru))
            if _nonempty(sub_en) and _nonempty(name_ru)
            else ""
        )
    meta = _place_meta_line(p, edition)
    meta_html = (
        '<p class="place-meta">{}</p>'.format(escape(meta))
        if meta
        else ""
    )
    chunks: list[str] = [
        '<section class="place" id="{}">'.format(escape(p.get("slug", "x"))),
        "<h3>{}</h3>".format(title_html),
        sub_html,
        meta_html,
        _place_figures_html(title_plain, img_srcs, edition),
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
                "<h4>{}</h4>\n<ul class=\"facts\">{}</ul>".format(
                    escape(s["facts_heading"]),
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
                "<h4>{}</h4>\n"
                "<ul class=\"stories\">{}</ul>".format(
                    escape(s["stories_heading"]),
                    st_li,
                )
            )
    if _nonempty(p.get("history")):
        chunks.append("<h4>{}</h4>".format(escape(s["history_heading"])))
        chunks.append(_html_paragraphs(p["history"]))
    if _nonempty(p.get("significance")):
        chunks.append(
            "<h4>{}</h4>".format(escape(s["significance_heading"])),
        )
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


def _heraldry_html(spb_root: Path, edition: str) -> str:
    """Титул: исторические гербы, девиз, герб/флаг города, ведущие вузы."""
    if edition == "ru":
        herald_label = HERALDRY_CHAPTER_LABEL_RU
        aria = "Гербы, флаг и вузы Санкт-Петербурга"
        motto = "Город федерального значения"
        official_lbl = "Символика города (нынешний герб и флаг)"
        coat_alt = "Герб Санкт-Петербурга"
        flag_alt = "Флаг Санкт-Петербурга"
        univ_lbl = "Ведущие вузы Санкт-Петербурга"
    else:
        herald_label = HERALDRY_CHAPTER_LABEL_EN
        aria = "Coats of arms, flag, and universities of Saint Petersburg"
        motto = "City of federal significance"
        official_lbl = "City symbols (current coat of arms and flag)"
        coat_alt = "Coat of arms of Saint Petersburg"
        flag_alt = "Flag of Saint Petersburg"
        univ_lbl = "Major universities of Saint Petersburg"
    chunks: list[str] = [
        '<div class="spb-title-symbols" aria-label="{}">'.format(escape(aria)),
        '<p class="title-strip-label">{}</p>'.format(
            escape(herald_label),
        ),
        '<div class="heraldry-strip heraldry-history">',
    ]
    for rel, alt in _TITLE_HISTORY_COATS:
        fig = _fig_if_exists(spb_root, rel, alt, "heraldry-coat-hist")
        if fig:
            chunks.append(fig)
    chunks.append("</div>")
    chunks.append(
        '<div class="heraldry-motto">'
        '<p class="motto-line">{}</p>'
        "</div>".format(escape(motto))
    )
    chunks.append(
        '<p class="title-strip-label">{}</p>'.format(escape(official_lbl))
    )
    chunks.append('<div class="heraldry-strip heraldry-official">')
    coat_p = spb_root / _HERALD_COAT_REL
    if coat_p.is_file() and coat_p.stat().st_size >= MIN_IMAGE_BYTES:
        chunks.append(
            _fig_if_exists(
                spb_root,
                _HERALD_COAT_REL,
                coat_alt,
                "heraldry-coat-book",
            )
        )
    flag_p = spb_root / _HERALD_FLAG_REL
    if flag_p.is_file() and flag_p.stat().st_size >= MIN_IMAGE_BYTES:
        chunks.append(
            _fig_if_exists(
                spb_root,
                _HERALD_FLAG_REL,
                flag_alt,
                "heraldry-flag-book",
            )
        )
    chunks.append("</div>")
    chunks.append(
        '<p class="title-strip-label">'
        "{}"
        "</p>".format(escape(univ_lbl))
    )
    chunks.append('<div class="heraldry-strip heraldry-universities">')
    for rel, alt in _TITLE_UNIVERSITIES:
        fig = _univ_fig_if_exists(spb_root, rel, alt)
        if fig:
            chunks.append(fig)
    chunks.append("</div></div>")
    return "\n".join(chunks)


def _cover_otium_html(edition: str) -> str:
    src = _OTIUM_PARAS if edition == "ru" else _OTIUM_PARAS_EN
    paras = "\n".join(
        '<p class="otiump">{}</p>'.format(escape(t)) for t in src
    )
    return (
        '<section class="cover-otium">'
        '<h1 class="otium-logo">OTIUM</h1>'
        "{}"
        "</section>"
    ).format(paras)


def _build_html(
    spb_root: Path,
    places: list[SpbPlace],
    edition: str,
    *,
    project_root: Path,
) -> str:
    font_href = (
        "https://fonts.googleapis.com/css2?"
        "family=Cormorant+Garamond:wght@600&family=Source+Sans+3:wght@400;600"
        "&display=swap"
    )
    s = guide_ui_strings(edition)
    counts = _counts_by_category(places)
    blocks: list[str] = [_cover_otium_html(edition)]
    if edition == "ru":
        city_h1 = "Санкт-Петербург"
        doc_lang = "ru"
    else:
        city_h1 = "Saint Petersburg"
        doc_lang = "en"
    blocks.append(
        '<header class="guide-title">'
        "{}"
        "<h1>{}</h1>"
        "<p class=\"lead\">{}</p>"
        "</header>".format(
            _heraldry_html(spb_root, edition),
            escape(city_h1),
            escape(s["lead"].format(len(places))),
        ),
    )
    if edition == "ru":
        hist_body = reference_text_ru_for_any_city("spb", project_root)
        hist_title = HISTORICAL_SECTION_TITLE_RU
    else:
        hist_body = reference_text_en_for_city("spb")
        hist_title = HISTORICAL_SECTION_TITLE_EN
    hist = historical_reference_section_html(
        hist_body,
        section_title=hist_title,
    )
    if hist:
        blocks.append(hist)
    last_cat: str | None = None
    for p in places:
        cat = p.get("category", "misc")
        if cat != last_cat:
            h2, sub = _chapter_heading(cat, counts.get(cat, 0), edition)
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
        blocks.append(_place_block(p, srcs, edition))
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
.historical-reference { margin: 0.75rem 0 1.15rem;
  page-break-inside: auto; }
.historical-reference h2 { font-family: 'Cormorant Garamond', serif;
  font-size: 1.28rem; font-weight: 600; margin: 0.4rem 0 0.55rem; }
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
    doc_title = s["html_title"].format(city_h1)
    return (
        "<!DOCTYPE html>\n"
        '<html lang="{}">\n<head>\n'
        '<meta charset="utf-8"/>\n'
        "<title>{}</title>\n"
        '<link rel="stylesheet" href="{}"/>\n'
        "<style>\n{}</style>\n</head>\n<body>\n{}\n</body>\n</html>\n"
    ).format(doc_lang, escape(doc_title), font_href, css, body_inner)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build SPB HTML/PDF using only existing files under spb/images "
            "(en/ru editions)."
        ),
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
    parser.add_argument(
        "--lang",
        dest="langs",
        nargs="+",
        choices=("en", "ru"),
        default=("en", "ru"),
        metavar="LANG",
        help="Guide edition language(s): en, ru (default: both).",
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
    skipped = len(SPB_PLACES) - len(places)
    if skipped:
        print(
            "Skipped {} place(s) without a local image.".format(skipped),
        )
    if not places:
        print(
            "No places with local images (>= {} bytes). "
            "Fill SPB_PLACES and run scripts/download_spb_images.py.".format(
                MIN_IMAGE_BYTES,
            ),
            file=sys.stderr,
        )
        return 2

    stem = SPB_PDF_NAME[:-4]
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
            _build_html(spb_root, places, edition, project_root=_PROJECT_ROOT),
            encoding="utf-8",
        )
        print("Written:", html_path)
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
            copy_built_guide_pdf_to_final_guides(_PROJECT_ROOT, pdf_path)
            print("Written:", pdf_path)
        else:
            print(
                "PDF failed ({}): pip install playwright && "
                "playwright install chromium".format(edition),
                file=sys.stderr,
            )
            return 1
    print("Places in PDF: {}".format(len(places)))
    primary = "en" if "en" in langs else langs[0]
    shutil.copy2(
        out_dir / "{}_{}.html".format(stem, primary),
        out_dir / SPB_HTML_NAME,
    )
    shutil.copy2(
        out_dir / "{}_{}.pdf".format(stem, primary),
        out_dir / SPB_PDF_NAME,
    )
    print("Primary edition ({}): {}".format(primary, out_dir / SPB_PDF_NAME))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
