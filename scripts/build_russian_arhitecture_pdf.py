# -*- coding: utf-8 -*-
"""HTML + PDF for Russian Architecture guide (style chapters)."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from html import escape
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from russian_arhitecture.data.places_registry import (  # noqa: E402
    RUSSIAN_ARHITECTURE_PLACES,
    CityPlace,
)
from russian_arhitecture.data.style_catalog import (  # noqa: E402
    STYLE_META,
    STYLE_ORDER,
)
from russian_arhitecture.data.style_architects import (  # noqa: E402
    STYLE_ARCHITECTS,
)
from russian_arhitecture.data.place_narratives import (  # noqa: E402
    apply_narrative_overrides,
    max_sentences_for_slug,
)
from russian_arhitecture.data.guide_image_policy import (  # noqa: E402
    SINGLE_IMAGE_SLUGS,
)
from russian_arhitecture.data.style_intros_extended import (  # noqa: E402
    style_intro_paragraphs,
)
from russian_arhitecture.data.history_heraldry import (  # noqa: E402
    history_coats_for_pdf,
)

from scripts.build_pdf import (  # noqa: E402
    PDF_FOOTER_EMPTY,
    PDF_FOOTER_PAGE_NUMBERS,
    _pdf_via_playwright,
    _strip_empty_pdf_pages,
    _strip_pdf_metadata,
    apply_continuous_page_footers,
)
from scripts.city_guide_core import (  # noqa: E402
    copy_built_guide_pdf_to_final_guides,
    drop_excluded_category_places,
    is_substantive_text,
    place_has_pdf_image,
)
from scripts.city_guide_jerusalem_style_pdf import PDF_CHUNK_MAX_PLACES  # noqa: E402
from scripts.city_guide_narrative import (  # noqa: E402
    GuideNarrativeDeduper,
    _collect_text_field_sentence_pairs,
    _dedupe_sentence_pairs,
    _fallback_narrative_paragraph,
    filter_stories,
    place_heading_plain,
    place_meta_line,
    subtitle_html_for_edition,
)
from scripts.city_guide_place_figures import (  # noqa: E402
    place_figure_layout_css,
    place_figures_layout_html,
)
from scripts.city_guide_historical_reference_ru import (  # noqa: E402
    HISTORICAL_SECTION_TITLE_EN,
    HISTORICAL_SECTION_TITLE_RU,
    historical_reference_section_html,
    reference_text_en_for_any_city,
    reference_text_ru_for_any_city,
)
from scripts.city_guide_jerusalem_style_pdf import guide_ui_strings  # noqa: E402
from scripts.city_guide_typography import guide_pdf_pagination_css  # noqa: E402
from scripts.city_guide_toc import (  # noqa: E402
    GuideTocEntry,
    category_chapter_anchor,
    guide_toc_back_link_html,
    guide_toc_html_category_chapters,
    toc_entries_for_category_guide,
)

MIN_IMAGE_BYTES = 500
HTML_NAME = "russian_arhitecture_guide.html"
PDF_NAME = "russian_arhitecture_guide.pdf"
_STYLE_INDEX = {k: i for i, k in enumerate(STYLE_ORDER)}
_HISTORY_COATS: tuple[tuple[str, str, str], ...] = history_coats_for_pdf()

_TITLE_SYMBOLS: tuple[tuple[str, str], ...] = (
    (
        "images/guide_coat_of_arms.svg",
        "Coat of arms of the Russian Federation",
    ),
    (
        "images/guide_flag.svg",
        "Flag of Russia",
    ),
    (
        "images/guide_coat_imperial.svg",
        "Coat of arms of the Russian Empire",
    ),
    (
        "images/guide_flag_imperial.svg",
        "Flag of the Russian Empire (black-yellow-white)",
    ),
    (
        "images/guide_coat_soviet.svg",
        "Coat of arms of the Soviet Union",
    ),
    (
        "images/guide_flag_soviet.svg",
        "Flag of the Soviet Union",
    ),
)

_OTIUM_PARAS: tuple[str, ...] = (
    "OTIUM — это практика осмысленного досуга. В античной традиции otium "
    "означало не отдых от труда, а время, в котором человек возвращается к "
    "взгляду, памяти и мышлению.",
    "Мы создаём маршруты не для «посещения», а для пребывания — для "
    "внимательного присутствия в архитектуре и памяти места.",
    "OTIUM существует для тех, кто хочет смотреть медленно.",
)
_OTIUM_PARAS_EN: tuple[str, ...] = (
    "OTIUM is the practice of meaningful leisure — time when attention "
    "returns to sight, memory and thought without utilitarian hurry.",
    "We design routes for staying present in architecture, not for "
    "checklist tourism.",
    "OTIUM is for those who want to look slowly.",
)

_GENERIC_NARRATIVE_RE = re.compile(
    r"^(?:пример|an example of|памятник относится к направлению|"
    r"the monument belongs to the)\b",
    re.IGNORECASE,
)
_STYLE_FALLBACK_RE = re.compile(
    r"памятник относится к направлению|the monument belongs to the",
    re.IGNORECASE,
)


def _dedupe_architecture_guide_places(
    places: list[CityPlace],
) -> list[CityPlace]:
    """Drop duplicate headings/images within each style chapter only."""
    from scripts.city_guide_core import dedupe_pdf_sidecar_places

    by_cat: dict[str, list[CityPlace]] = {}
    for place in places:
        cat = str(place.get("category") or "misc")
        by_cat.setdefault(cat, []).append(place)
    out: list[CityPlace] = []
    for cat in STYLE_ORDER:
        chunk = by_cat.get(cat)
        if not chunk:
            continue
        out.extend(
            dedupe_pdf_sidecar_places(
                chunk,
                city_slug="russian_arhitecture",
            ),
        )
    for cat, chunk in by_cat.items():
        if cat in _STYLE_INDEX:
            continue
        out.extend(
            dedupe_pdf_sidecar_places(
                chunk,
                city_slug="russian_arhitecture",
            ),
        )
    return out


def _is_generic_example_sentence(sentence: str) -> bool:
    s = str(sentence or "").strip()
    if not s:
        return True
    if _GENERIC_NARRATIVE_RE.match(s):
        return True
    return bool(_STYLE_FALLBACK_RE.search(s))


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


def _style_chapter_title(cat: str, edition: str) -> str:
    meta = STYLE_META.get(cat, ("Раздел", "Section", "", ""))
    base = meta[0] if edition == "ru" else meta[1]
    order = _STYLE_INDEX.get(cat)
    if order is None:
        return base
    return "{}. {}".format(order + 1, base)


def _style_intro_text(cat: str, edition: str) -> str:
    meta = STYLE_META.get(cat, ("", "", "", ""))
    return (meta[2] if edition == "ru" else meta[3]).strip()


def _style_intro_html(cat: str, edition: str) -> str:
    paras = style_intro_paragraphs(cat, edition)
    if not paras:
        intro = _style_intro_text(cat, edition)
        if not intro:
            return ""
        paras = [intro]
    return "\n".join(
        '<p class="chapter-intro">{}</p>'.format(escape(p)) for p in paras
    )


def _architecture_narrative_html(
    place: CityPlace,
    edition: str,
    deduper: GuideNarrativeDeduper,
) -> str:
    """Place prose: one block, 2–20 sentences, no generic placeholders."""
    place = apply_narrative_overrides(place)
    slug = str(place.get("slug") or "")
    pairs: list[tuple[str, str]] = []
    pairs.extend(
        _collect_text_field_sentence_pairs(place, edition, "description"),
    )
    pairs.extend(
        _collect_text_field_sentence_pairs(place, edition, "history"),
    )
    pairs.extend(
        _collect_text_field_sentence_pairs(place, edition, "significance"),
    )
    pairs = [
        (sent, key)
        for sent, key in pairs
        if not _is_generic_example_sentence(sent)
    ]
    sents = _dedupe_sentence_pairs(pairs, deduper)
    if len(sents) < 2:
        fb = _fallback_narrative_paragraph(place, edition)
        if fb and not _is_generic_example_sentence(fb):
            sents.append(fb)
    cap = max_sentences_for_slug(slug) or 20
    sents = sents[:cap]
    if not sents:
        return ""
    body = " ".join(sents)
    inner = '<p class="prose">{}</p>'.format(escape(body))
    return '<div class="place-desc">{}</div>'.format(inner)


def _missing_image_places(guide_root: Path) -> list[str]:
    missing: list[str] = []
    for place in RUSSIAN_ARHITECTURE_PLACES:
        slug = str(place.get("slug") or "")
        srcs, _paths = _image_entries_for_place(guide_root, place)
        if not srcs:
            missing.append(slug)
    return missing


def _style_architects_html(cat: str, edition: str) -> str:
    rows = STYLE_ARCHITECTS.get(cat) or []
    if not rows:
        return ""
    label = (
        "Главные архитекторы"
        if edition == "ru"
        else "Leading architects"
    )
    items: list[str] = []
    for name_ru, name_en, note_ru, note_en in rows:
        name = name_ru if edition == "ru" else name_en
        note = note_ru if edition == "ru" else note_en
        items.append(
            "<li><strong>{}</strong> — {}</li>".format(
                escape(name),
                escape(note),
            ),
        )
    return (
        '<div class="chapter-architects">'
        '<p class="chapter-architects-label">{}</p>'
        '<ul class="chapter-architects-list">{}</ul>'
        "</div>"
    ).format(escape(label), "\n".join(items))


def _chapter_heading(cat: str, count: int, edition: str) -> tuple[str, str]:
    h2 = _style_chapter_title(cat, edition)
    if edition == "ru":
        sub = _ru_count_phrase(count, "пример", "примера", "примеров")
    else:
        sub = _en_count_phrase(count, "example", "examples")
    return h2, sub


def _rel_to_src(rel: str) -> str:
    return "../{}".format(rel.lstrip("/").replace("\\", "/"))


def _counts_by_category(places: list[CityPlace]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for place in places:
        key = str(place.get("category") or "misc")
        counts[key] = counts.get(key, 0) + 1
    return counts


def _image_entries_for_place(
    root: Path,
    place: CityPlace,
) -> tuple[list[str], list[Path]]:
    srcs: list[str] = []
    paths: list[Path] = []
    primary = place.get("image_rel_path")
    if primary:
        path = root / primary
        if path.is_file() and path.stat().st_size >= MIN_IMAGE_BYTES:
            srcs.append(_rel_to_src(primary))
            paths.append(path)
    for extra in place.get("additional_images") or []:
        if str(place.get("slug") or "") in SINGLE_IMAGE_SLUGS:
            break
        rel = extra.get("image_rel_path")
        if not rel:
            continue
        path = root / rel
        if path.is_file() and path.stat().st_size >= MIN_IMAGE_BYTES:
            srcs.append(_rel_to_src(rel))
            paths.append(path)
    return srcs, paths


def _image_srcs_for_place(root: Path, place: CityPlace) -> list[str]:
    srcs, _paths = _image_entries_for_place(root, place)
    return srcs


def _places_with_local_images(guide_root: Path) -> list[CityPlace]:
    rows = drop_excluded_category_places(list(RUSSIAN_ARHITECTURE_PLACES))
    rows = _dedupe_architecture_guide_places(rows)
    out = [p for p in rows if place_has_pdf_image(guide_root, p)]
    out.sort(
        key=lambda row: (
            _STYLE_INDEX.get(str(row.get("category") or ""), 999),
            str(row.get("name_ru") or ""),
        ),
    )
    return out


def _heraldry_html(root: Path, edition: str) -> str:
    hist_figs: list[str] = []
    for rel, alt_en, alt_ru in _HISTORY_COATS:
        path = root / rel
        if not path.is_file():
            continue
        alt = alt_ru if edition == "ru" else alt_en
        hist_figs.append(
            '<figure class="heraldry-fig heraldry-coat-hist">'
            '<img src="{}" alt="{}"/>'
            "</figure>".format(
                escape(_rel_to_src(rel)),
                escape(alt),
            ),
        )
    official_figs: list[str] = []
    for rel, alt in _TITLE_SYMBOLS:
        path = root / rel
        if not path.is_file():
            continue
        if path.suffix.lower() != ".svg" and path.stat().st_size < MIN_IMAGE_BYTES:
            continue
        cls = (
            "heraldry-flag-book"
            if "flag" in rel
            else "heraldry-coat-book"
        )
        official_figs.append(
            '<figure class="heraldry-fig {}">'
            '<img src="{}" alt="{}"/>'
            "</figure>".format(
                cls,
                escape(_rel_to_src(rel)),
                escape(alt),
            ),
        )
    if not hist_figs and not official_figs:
        return ""
    chunks: list[str] = [
        '<div class="russian_arhitecture-title-symbols">',
    ]
    if hist_figs:
        hist_label = (
            "Исторические гербы"
            if edition == "ru"
            else "Historical coats of arms"
        )
        chunks.append(
            '<p class="title-strip-label">{}</p>'.format(escape(hist_label)),
        )
        chunks.append(
            '<div class="heraldry-strip heraldry-history">'
            "{}"
            "</div>".format("\n".join(hist_figs)),
        )
    if official_figs:
        off_label = (
            "Современная символика"
            if edition == "ru"
            else "Modern symbols"
        )
        chunks.append(
            '<p class="title-strip-label">{}</p>'.format(escape(off_label)),
        )
        chunks.append(
            '<div class="heraldry-strip heraldry-official">'
            "{}"
            "</div>".format("\n".join(official_figs)),
        )
    chunks.append("</div>")
    return "\n".join(chunks)


def _cover_otium_html(edition: str) -> str:
    paras = _OTIUM_PARAS if edition == "ru" else _OTIUM_PARAS_EN
    body = "\n".join(
        '<p class="otiump">{}</p>'.format(escape(t)) for t in paras
    )
    return (
        '<section class="cover-otium">'
        '<h1 class="otium-logo">OTIUM</h1>'
        "{}"
        "</section>"
    ).format(body)


def _place_block(
    place: CityPlace,
    img_srcs: list[str],
    edition: str,
    deduper: GuideNarrativeDeduper,
    *,
    image_paths: list[Path] | None = None,
) -> str:
    title_plain = place_heading_plain(place, edition)
    title_html = escape(title_plain)
    sub_html = subtitle_html_for_edition(place, edition)
    meta = place_meta_line(place, edition, guide_ui_strings(edition))
    meta_html = (
        '<p class="place-meta">{}</p>'.format(escape(meta))
        if meta
        else ""
    )
    chunks: list[str] = [
        '<section class="place" id="{}">'.format(
            escape(str(place.get("slug") or "x")),
        ),
        '<div class="place-lead">',
        "<h3>{}</h3>".format(title_html),
        guide_toc_back_link_html(edition),
        sub_html,
        meta_html,
    ]
    if img_srcs:
        chunks.append(
            place_figures_layout_html(
                img_srcs,
                title_plain,
                edition,
                image_paths=image_paths,
            ),
        )
    chunks.append("</div>")
    narrative = _architecture_narrative_html(place, edition, deduper)
    if narrative:
        chunks.append(narrative)
    stories = filter_stories(place, edition)
    story_lines = [
        str(st).strip()
        for st in stories
        if is_substantive_text(str(st).strip())
    ]
    if story_lines:
        inner = "\n".join(
            '<p class="prose place-story">{}</p>'.format(escape(line))
            for line in story_lines
        )
        chunks.append('<div class="place-story-block">{}</div>'.format(inner))
    chunks.append("</section>")
    return "\n".join(chunks)


def _build_html(
    guide_root: Path,
    places: list[CityPlace],
    edition: str,
    *,
    project_root: Path,
    deduper: GuideNarrativeDeduper | None = None,
    include_front_matter: bool = True,
    initial_last_cat: str | None = None,
    category_counts: dict[str, int] | None = None,
    lead_place_count: int | None = None,
    toc_places: list[CityPlace] | None = None,
) -> str:
    narrative_deduper = deduper or GuideNarrativeDeduper()
    font_href = (
        "https://fonts.googleapis.com/css2?"
        "family=Cormorant+Garamond:wght@600&family=Source+Sans+3:wght@400;600"
        "&display=swap"
    )
    strings = guide_ui_strings(edition)
    counts = (
        category_counts
        if category_counts is not None
        else _counts_by_category(places)
    )
    lead_n = lead_place_count if lead_place_count is not None else len(places)
    blocks: list[str] = []
    if include_front_matter:
        blocks.append(_cover_otium_html(edition))
    if edition == "ru":
        city_h1 = "Русская архитектура"
        doc_lang = "ru"
    else:
        city_h1 = "Russian Architecture"
        doc_lang = "en"
    if include_front_matter:
        blocks.append(
            '<header class="guide-title">'
            "{}"
            "<h1>{}</h1>"
            '<p class="lead">{}</p>'
            "</header>".format(
                _heraldry_html(guide_root, edition),
                escape(city_h1),
                escape(strings["lead"].format(lead_n)),
            ),
        )
        if edition == "ru":
            hist_body = reference_text_ru_for_any_city(
                "russian_arhitecture",
                project_root,
            )
            hist_title = HISTORICAL_SECTION_TITLE_RU
        else:
            hist_body = reference_text_en_for_any_city(
                "russian_arhitecture",
                project_root,
            )
            hist_title = HISTORICAL_SECTION_TITLE_EN
        toc_entries: list[GuideTocEntry] = []
        if hist_body and str(hist_body).strip():
            toc_entries.append(
                GuideTocEntry("guide-historical", hist_title),
            )
        toc_source = toc_places if toc_places is not None else places
        toc_entries.extend(
            toc_entries_for_category_guide(
                toc_source,
                edition,
                chapter_title=_chapter_heading,
                counts_by_category=counts,
                has_section=lambda row: bool(
                    _image_srcs_for_place(guide_root, row),
                ),
            ),
        )
        toc_html = guide_toc_html_category_chapters(toc_entries, edition)
        if toc_html:
            blocks.append(toc_html)
        hist = historical_reference_section_html(
            hist_body,
            section_title=hist_title,
            edition=edition,
        )
        if hist:
            blocks.append(hist)
    last_cat = initial_last_cat
    for place in places:
        cat = str(place.get("category") or "misc")
        if cat != last_cat:
            h2, sub = _chapter_heading(cat, counts.get(cat, 0), edition)
            intro_html = _style_intro_html(cat, edition)
            architects_html = _style_architects_html(cat, edition)
            blocks.append(
                '<div class="chapter-head" id="{}">'
                "<h2>{}</h2>"
                "{}"
                "{}{}"
                "</div>".format(
                    escape(category_chapter_anchor(cat)),
                    escape(h2),
                    guide_toc_back_link_html(edition),
                    intro_html,
                    architects_html,
                ),
            )
            last_cat = cat
        srcs, paths = _image_entries_for_place(guide_root, place)
        if not srcs:
            continue
        blocks.append(
            _place_block(
                place,
                srcs,
                edition,
                narrative_deduper,
                image_paths=paths,
            ),
        )
    body_inner = "\n".join(blocks)
    css = """
body { font-family: 'Source Sans 3', sans-serif; margin: 2rem;
  color: #1a1a1a; font-size: 11pt; }
.cover-otium { page-break-after: always; min-height: 85vh;
  padding: 2rem 1rem 3rem; box-sizing: border-box; }
.otium-logo { font-family: 'Cormorant Garamond', serif; font-size: 3rem;
  font-weight: 600; letter-spacing: 0.2em; margin-bottom: 2rem; }
.otiump { margin: 0.9rem 0; line-height: 1.55; text-align: justify; }
.guide-title { page-break-after: always; margin-bottom: 1rem;
  page-break-inside: avoid; }
.historical-reference { margin: 0.75rem 0 1.15rem;
  page-break-inside: auto; page-break-after: auto; break-after: auto; }
.historical-reference + .chapter-head {
  page-break-before: avoid; break-before: avoid-page; }
.historical-reference h2 { font-family: 'Cormorant Garamond', serif;
  font-size: 1.28rem; font-weight: 600; margin: 0.4rem 0 0.55rem; }
.russian_arhitecture-title-symbols { margin-bottom: 0.45rem; }
.title-strip-label { font-size: 0.62rem; letter-spacing: 0.06em;
  text-transform: uppercase; color: #666; text-align: center;
  margin: 0.35rem 0 0.15rem; }
.heraldry-strip { display: flex; flex-wrap: wrap; align-items: center;
  justify-content: center; gap: 0.35rem 0.55rem; margin: 0.2rem 0 0.45rem; }
.heraldry-coat-hist img { max-height: 4.2rem; }
.heraldry-fig img { max-height: 4.2rem; object-fit: contain; display: block;
  margin: 0 auto; }
.guide-title h1 { font-family: 'Cormorant Garamond', serif; font-size: 2.4rem;
  margin-bottom: 0.5rem; }
.lead { color: #444; font-size: 1.05rem; }
"""
    css += guide_pdf_pagination_css(
        toc_h2_extra="font-family: 'Cormorant Garamond', serif",
    )
    css += """
.chapter-head { margin-top: 2.2rem; border-bottom: 1px solid #bbb;
  padding-bottom: 0.35rem;
  page-break-before: always; break-before: page;
  page-break-after: avoid; break-after: avoid; }
.chapter-head + .place { page-break-before: avoid; break-before: avoid; }
h2 { font-family: 'Cormorant Garamond', serif; font-size: 1.55rem;
  margin: 0 0 0.25rem; }
.chapter-intro { margin: 0.35rem 0 0.45rem; line-height: 1.5;
  text-align: justify; color: #333; font-size: 1rem; }
.chapter-architects { margin: 0.2rem 0 0.55rem;
  page-break-before: avoid; break-before: avoid-page;
  page-break-inside: avoid; break-inside: avoid-page;
  page-break-after: avoid; break-after: avoid-page; }
.chapter-architects-label { margin: 0.35rem 0 0.25rem; font-size: 0.95rem;
  font-weight: 600; color: #2a2a2a; }
.chapter-architects-list { margin: 0.15rem 0 0.45rem 1.15rem; padding: 0;
  font-size: 0.92rem; line-height: 1.45; color: #333; }
.chapter-architects-list li { margin: 0.22rem 0; }
.guide-toc ul.toc-examples { list-style: none; margin: 0.15rem 0 0.55rem 1.15rem;
  padding: 0; }
.guide-toc ol.toc-chapters { columns: 3; column-gap: 1.1rem; }
.guide-toc { page-break-after: auto; break-after: auto; }
.guide-toc li.toc-item--example { font-size: 0.82rem; margin: 0.14rem 0;
  line-height: 1.35; }
.guide-toc li.toc-item--chapter { margin-top: 0.32rem; }
.guide-toc ol.toc-chapters { margin: 0.35rem 0 0.65rem 1.25rem; padding: 0;
  list-style: none; }
.guide-toc ol.toc-preamble { margin: 0.35rem 0 0.65rem 1.25rem; padding: 0;
  list-style: none; }
.place { margin-bottom: 2.5rem; page-break-inside: avoid; }
h3 { font-size: 1.22rem; margin: 1.2rem 0 0.35rem; }
.sub-en { color: #555; font-size: 0.95rem; margin: 0 0 0.5rem;
  font-style: italic; }
.place-meta { font-size: 0.92rem; color: #353535; margin: 0 0 0.75rem;
  line-height: 1.4; }
"""
    css += place_figure_layout_css()
    css += """
img { max-width: 100%; height: auto; display: block; border-radius: 4px; }
.prose, .place-desc p { margin: 0.45rem 0; line-height: 1.5;
  text-align: justify; }
.place-story-block { margin: 0.5rem 0 0.75rem 0; }
.place-story-block .place-story { font-style: italic; color: #4a5568; }
ul.facts { margin: 0.3rem 0 0.6rem 1.2rem; padding: 0; }
ul.facts li { margin: 0.25rem 0; line-height: 1.45; }
"""
    doc_title = strings["html_title"].format(city_h1)
    return (
        "<!DOCTYPE html>\n"
        '<html lang="{}">\n<head>\n'
        '<meta charset="utf-8"/>\n'
        "<title>{}</title>\n"
        '<link rel="stylesheet" href="{}"/>\n'
        "<style>\n{}</style>\n</head>\n<body>\n{}\n</body>\n</html>\n"
    ).format(doc_lang, escape(doc_title), font_href, css, body_inner)


def _pdf_via_playwright_chunked(
    *,
    guide_root: Path,
    out_dir: Path,
    stem: str,
    edition: str,
    places: list[CityPlace],
    pdf_path: Path,
    project_root: Path,
    image_wait_timeout_ms: int,
    header: str,
    deduper: GuideNarrativeDeduper,
) -> bool:
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        print("pypdf required for chunked PDF merge.", file=sys.stderr)
        return False

    category_counts = _counts_by_category(places)
    chunk_places_list = [
        places[i : i + PDF_CHUNK_MAX_PLACES]
        for i in range(0, len(places), PDF_CHUNK_MAX_PLACES)
    ]
    chunk_pdfs: list[Path] = []
    last_cat: str | None = None
    try:
        for idx, chunk_places in enumerate(chunk_places_list):
            print(
                "  PDF chunk {}/{}...".format(idx + 1, len(chunk_places_list)),
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
                _build_html(
                    guide_root,
                    chunk_places,
                    edition,
                    project_root=project_root,
                    deduper=deduper,
                    include_front_matter=(idx == 0),
                    initial_last_cat=last_cat,
                    category_counts=category_counts,
                    lead_place_count=len(places),
                    toc_places=places,
                ),
                encoding="utf-8",
            )
            if chunk_places:
                last_cat = str(chunk_places[-1].get("category") or "misc")
            if not _pdf_via_playwright(
                chunk_html_path,
                chunk_pdf_path,
                image_wait_timeout_ms=image_wait_timeout_ms,
                display_header_footer=True,
                footer_template=PDF_FOOTER_EMPTY,
                header_template=header,
                static_site_root=guide_root,
            ):
                return False
            chunk_pdfs.append(chunk_pdf_path)

        writer = PdfWriter()
        for chunk_pdf in chunk_pdfs:
            reader = PdfReader(str(chunk_pdf))
            for page in reader.pages:
                writer.add_page(page)
        writer.write(str(pdf_path))
        apply_continuous_page_footers(pdf_path)
        return True
    finally:
        for chunk_pdf in chunk_pdfs:
            if chunk_pdf.is_file():
                try:
                    chunk_pdf.unlink()
                except OSError:
                    pass
        for idx in range(len(chunk_places_list)):
            for suffix in (".html", ".pdf"):
                path = out_dir / "{}_{}_chunk_{}{}".format(
                    stem,
                    edition,
                    idx,
                    suffix,
                )
                if path.is_file():
                    try:
                        path.unlink()
                    except OSError:
                        pass


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build Russian Architecture HTML/PDF (style chapters, en/ru)."
        ),
    )
    parser.add_argument(
        "--russian-arhitecture-root",
        type=Path,
        default=_PROJECT_ROOT / "russian_arhitecture",
        dest="guide_root",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
    )
    parser.add_argument(
        "--image-wait-ms",
        type=int,
        default=30000,
        metavar="MS",
    )
    parser.add_argument(
        "--lang",
        dest="langs",
        nargs="+",
        choices=("en", "ru"),
        default=("en", "ru"),
        metavar="LANG",
    )
    parser.add_argument(
        "--html-only",
        action="store_true",
    )
    args = parser.parse_args()
    guide_root = args.guide_root.resolve()
    out_dir = (
        args.output_dir.resolve()
        if args.output_dir
        else guide_root / "output"
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    places = _places_with_local_images(guide_root)
    missing_slugs = _missing_image_places(guide_root)
    if missing_slugs:
        print(
            "Places missing images ({}): {}".format(
                len(missing_slugs),
                ", ".join(missing_slugs),
            ),
        )
    skipped = len(RUSSIAN_ARHITECTURE_PLACES) - len(places)
    if skipped:
        print(
            "Omitted {} duplicate sidecar place(s) from export "
            "(images on disk; deduplicated).".format(skipped),
        )
    if not places:
        print(
            "No places with local images. Run "
            "scripts/generate_russian_arhitecture_guide.py and "
            "scripts/download_russian_arhitecture_images.py.",
            file=sys.stderr,
        )
        return 2

    stem = PDF_NAME[:-4]
    langs: tuple[str, ...] = tuple(dict.fromkeys(args.langs))
    footer = PDF_FOOTER_PAGE_NUMBERS
    header = "<div style='font-size:9px;width:100%'></div>"
    use_chunked = len(places) > PDF_CHUNK_MAX_PLACES
    for edition in langs:
        html_path = out_dir / "{}_{}.html".format(stem, edition)
        pdf_path = out_dir / "{}_{}.pdf".format(stem, edition)
        narrative_deduper = GuideNarrativeDeduper()
        html_path.write_text(
            _build_html(
                guide_root,
                places,
                edition,
                project_root=_PROJECT_ROOT,
                deduper=narrative_deduper,
            ),
            encoding="utf-8",
        )
        print("Written:", html_path)
        if args.html_only:
            continue
        if use_chunked:
            pdf_deduper = GuideNarrativeDeduper()
            pdf_ok = _pdf_via_playwright_chunked(
                guide_root=guide_root,
                out_dir=out_dir,
                stem=stem,
                edition=edition,
                places=places,
                pdf_path=pdf_path,
                project_root=_PROJECT_ROOT,
                image_wait_timeout_ms=args.image_wait_ms,
                header=header,
                deduper=pdf_deduper,
            )
        else:
            pdf_ok = _pdf_via_playwright(
                html_path,
                pdf_path,
                image_wait_timeout_ms=args.image_wait_ms,
                display_header_footer=True,
                footer_template=footer,
                header_template=header,
                static_site_root=guide_root,
            )
        if pdf_ok:
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
        out_dir / HTML_NAME,
    )
    if not args.html_only:
        shutil.copy2(
            out_dir / "{}_{}.pdf".format(stem, primary),
            out_dir / PDF_NAME,
        )
        print("Primary edition ({}): {}".format(primary, out_dir / PDF_NAME))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
