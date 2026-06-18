# -*- coding: utf-8 -*-
"""Per-city Google Fonts for OTIUM PDF/HTML guides (titles vs body)."""

from __future__ import annotations

# (google_fonts_css2_href, title_font_family_css, body_font_family_css)
# Title stack: place names (h3), guide h1, OTIUM logo. Body: prose, lists.
_TYPO: dict[str, tuple[str, str, str]] = {
    "berlin": (
        "https://fonts.googleapis.com/css2?"
        "family=Grenze+Gotisch:wght@400;600&"
        "family=Source+Sans+3:wght@400;600&display=swap",
        "'Grenze Gotisch', serif",
        "'Source Sans 3', sans-serif",
    ),
    "paris": (
        "https://fonts.googleapis.com/css2?"
        "family=Playfair+Display:wght@500;600&"
        "family=Source+Sans+3:wght@400;600&display=swap",
        "'Playfair Display', serif",
        "'Source Sans 3', sans-serif",
    ),
    "rome": (
        "https://fonts.googleapis.com/css2?"
        "family=Cinzel:wght@500;600&"
        "family=Source+Sans+3:wght@400;600&display=swap",
        "'Cinzel', serif",
        "'Source Sans 3', sans-serif",
    ),
    "venice": (
        "https://fonts.googleapis.com/css2?"
        "family=Cinzel:wght@500;600&"
        "family=Source+Sans+3:wght@400;600&display=swap",
        "'Cinzel', serif",
        "'Source Sans 3', sans-serif",
    ),
    "florence": (
        "https://fonts.googleapis.com/css2?"
        "family=Cormorant+Infant:wght@600&"
        "family=Source+Sans+3:wght@400;600&display=swap",
        "'Cormorant Infant', serif",
        "'Source Sans 3', sans-serif",
    ),
    "barcelona": (
        "https://fonts.googleapis.com/css2?"
        "family=Marcellus&"
        "family=Source+Sans+3:wght@400;600&display=swap",
        "'Marcellus', serif",
        "'Source Sans 3', sans-serif",
    ),
    "madrid": (
        "https://fonts.googleapis.com/css2?"
        "family=Marcellus&"
        "family=Source+Sans+3:wght@400;600&display=swap",
        "'Marcellus', serif",
        "'Source Sans 3', sans-serif",
    ),
    "budapest": (
        "https://fonts.googleapis.com/css2?"
        "family=Spectral:wght@500;600&"
        "family=Source+Sans+3:wght@400;600&display=swap",
        "'Spectral', serif",
        "'Source Sans 3', sans-serif",
    ),
    "prague": (
        "https://fonts.googleapis.com/css2?"
        "family=Spectral:wght@500;600&"
        "family=Source+Sans+3:wght@400;600&display=swap",
        "'Spectral', serif",
        "'Source Sans 3', sans-serif",
    ),
    "vienna": (
        "https://fonts.googleapis.com/css2?"
        "family=Vollkorn:wght@500;600&"
        "family=Source+Sans+3:wght@400;600&display=swap",
        "'Vollkorn', serif",
        "'Source Sans 3', sans-serif",
    ),
    "boston": (
        "https://fonts.googleapis.com/css2?"
        "family=Libre+Baskerville:wght@400;700&"
        "family=Source+Sans+3:wght@400;600&display=swap",
        "'Libre Baskerville', serif",
        "'Source Sans 3', sans-serif",
    ),
    "philadelphia": (
        "https://fonts.googleapis.com/css2?"
        "family=Libre+Baskerville:wght@400;700&"
        "family=Source+Sans+3:wght@400;600&display=swap",
        "'Libre Baskerville', serif",
        "'Source Sans 3', sans-serif",
    ),
    "new_york": (
        "https://fonts.googleapis.com/css2?"
        "family=Libre+Baskerville:wght@400;700&"
        "family=Source+Sans+3:wght@400;600&display=swap",
        "'Libre Baskerville', serif",
        "'Source Sans 3', sans-serif",
    ),
    "montreal": (
        "https://fonts.googleapis.com/css2?"
        "family=Cormorant:wght@500;600&"
        "family=Source+Sans+3:wght@400;600&display=swap",
        "'Cormorant', serif",
        "'Source Sans 3', sans-serif",
    ),
    "jerusalem": (
        "https://fonts.googleapis.com/css2?"
        "family=David+Libre:wght@400;500&"
        "family=Rubik:ital,wght@0,400;0,500;0,600&display=swap",
        "'David Libre', serif",
        "'Rubik', sans-serif",
    ),
    "vatican": (
        "https://fonts.googleapis.com/css2?"
        "family=Cinzel:wght@500;600&"
        "family=Source+Sans+3:wght@400;600&display=swap",
        "'Cinzel', serif",
        "'Source Sans 3', sans-serif",
    ),
    "london": (
        "https://fonts.googleapis.com/css2?"
        "family=Libre+Baskerville:wght@400;700&"
        "family=Source+Sans+3:wght@400;600&display=swap",
        "'Libre Baskerville', serif",
        "'Source Sans 3', sans-serif",
    ),
    "amsterdam": (
        "https://fonts.googleapis.com/css2?"
        "family=Spectral:wght@500;600&"
        "family=Source+Sans+3:wght@400;600&display=swap",
        "'Spectral', serif",
        "'Source Sans 3', sans-serif",
    ),
    "istanbul": (
        "https://fonts.googleapis.com/css2?"
        "family=Spectral:wght@500;600&"
        "family=Source+Sans+3:wght@400;600&display=swap",
        "'Spectral', serif",
        "'Source Sans 3', sans-serif",
    ),
    "tokyo": (
        "https://fonts.googleapis.com/css2?"
        "family=Shippori+Mincho:wght@500;600&"
        "family=Noto+Sans+JP:wght@400;500;600&display=swap",
        "'Shippori Mincho', serif",
        "'Noto Sans JP', sans-serif",
    ),
    "dubai": (
        "https://fonts.googleapis.com/css2?"
        "family=Marcellus&"
        "family=Source+Sans+3:wght@400;600&display=swap",
        "'Marcellus', serif",
        "'Source Sans 3', sans-serif",
    ),
    "athens": (
        "https://fonts.googleapis.com/css2?"
        "family=Cinzel:wght@500;600&"
        "family=Source+Sans+3:wght@400;600&display=swap",
        "'Cinzel', serif",
        "'Source Sans 3', sans-serif",
    ),
    "lisbon": (
        "https://fonts.googleapis.com/css2?"
        "family=Playfair+Display:wght@500;600&"
        "family=Source+Sans+3:wght@400;600&display=swap",
        "'Playfair Display', serif",
        "'Source Sans 3', sans-serif",
    ),
    "singapore": (
        "https://fonts.googleapis.com/css2?"
        "family=Source+Serif+4:opsz,wght@8..60,500;600&"
        "family=Source+Sans+3:wght@400;600&display=swap",
        "'Source Serif 4', serif",
        "'Source Sans 3', sans-serif",
    ),
    "bangkok": (
        "https://fonts.googleapis.com/css2?"
        "family=Spectral:wght@500;600&"
        "family=Source+Sans+3:wght@400;600&display=swap",
        "'Spectral', serif",
        "'Source Sans 3', sans-serif",
    ),
    "los_angeles": (
        "https://fonts.googleapis.com/css2?"
        "family=Libre+Baskerville:wght@400;700&"
        "family=Source+Sans+3:wght@400;600&display=swap",
        "'Libre Baskerville', serif",
        "'Source Sans 3', sans-serif",
    ),
    "san_francisco": (
        "https://fonts.googleapis.com/css2?"
        "family=Libre+Baskerville:wght@400;700&"
        "family=Source+Sans+3:wght@400;600&display=swap",
        "'Libre Baskerville', serif",
        "'Source Sans 3', sans-serif",
    ),
    "dublin": (
        "https://fonts.googleapis.com/css2?"
        "family=Libre+Baskerville:wght@400;700&"
        "family=Source+Sans+3:wght@400;600&display=swap",
        "'Libre Baskerville', serif",
        "'Source Sans 3', sans-serif",
    ),
    "copenhagen": (
        "https://fonts.googleapis.com/css2?"
        "family=Vollkorn:wght@500;600&"
        "family=Source+Sans+3:wght@400;600&display=swap",
        "'Vollkorn', serif",
        "'Source Sans 3', sans-serif",
    ),
}

_DEFAULT = (
    "https://fonts.googleapis.com/css2?"
    "family=Cormorant+Garamond:wght@600&"
    "family=Source+Sans+3:wght@400;600&display=swap",
    "'Cormorant Garamond', serif",
    "'Source Sans 3', sans-serif",
)


def guide_pdf_pagination_css(*, toc_h2_extra: str = "") -> str:
    """
    Print/PDF rules: TOC on its own page; title + lead image stay together.
    """
    from scripts.city_guide_place_figures import place_figure_layout_css

    toc_h2 = toc_h2_extra.strip()
    if toc_h2 and not toc_h2.endswith(";"):
        toc_h2 += ";"
    place_fig_css = place_figure_layout_css()
    return """
.guide-toc {{ page-break-before: always; break-before: page;
  page-break-after: always; break-after: page;
  margin: 0; padding: 0.2rem 0 0.45rem; page-break-inside: auto; }}
.guide-toc h2 {{ {toc_h2}
  font-size: 1.28rem; font-weight: 600; margin: 0.4rem 0 0.55rem; }}
.guide-toc ol {{ margin: 0.35rem 0 0.65rem 1.25rem; padding: 0;
  columns: 2; column-gap: 1.5rem; }}
.guide-toc li {{ margin: 0.18rem 0; line-height: 1.35;
  font-size: 0.88rem; break-inside: avoid; }}
.guide-toc a {{ color: #1a5276; text-decoration: underline;
  text-underline-offset: 0.12em; cursor: pointer; }}
.guide-toc a:hover {{ color: #0d3d56; }}
.guide-toc li.toc-item--sub {{ font-size: 0.82rem; margin-left: 0.35rem; }}
.toc-back {{ font-size: 0.78rem; margin: 0 0 0.35rem; text-align: right; }}
.toc-back a {{ color: #1a5276; text-decoration: underline;
  text-underline-offset: 0.12em; cursor: pointer; }}
.toc-back a:hover {{ color: #0d3d56; }}
.place, .historical-reference, .guide-primer, .guide-trip-plans {{
  scroll-margin-top: 1.25rem; }}
.historical-reference h2, .guide-primer h2, .guide-trip-plans h2,
.chapter-head h2, .place-lead h3 {{ position: relative; }}
.guide-toc + .place, .guide-toc + .chapter-head {{
  page-break-before: avoid; break-before: avoid-page; }}
.place-lead {{ page-break-inside: avoid; break-inside: avoid-page;
  page-break-after: auto; }}
.place-lead > h3 {{ page-break-after: avoid; break-after: avoid-page; }}
.place-lead > .place-meta {{ page-break-after: avoid; break-after: avoid-page; }}
{place_fig_css}
""".format(toc_h2=toc_h2, place_fig_css=place_fig_css)


def typography_triple(city_slug: str) -> tuple[str, str, str]:
    """Href and CSS font-family stacks for city slug (snake_case)."""
    return _TYPO.get(city_slug, _DEFAULT)


def guide_inline_css(title_symbols_class: str, city_slug: str) -> str:
    """Inline CSS for Latin-script city guides (not Smolensk/SPB)."""
    _, title, body = typography_triple(city_slug)
    hebrew_sub = ""
    if city_slug == "jerusalem":
        hebrew_sub = (
            ".sub-he {{ font-family: {body}, {title}, sans-serif; "
            "font-style: normal; font-size: 1.02rem; }}\n"
        ).format(body=body, title=title)
    elif city_slug == "tokyo":
        hebrew_sub = (
            ".sub-ja {{ font-family: {body}, {title}, sans-serif; "
            "font-style: normal; font-size: 1.02rem; }}\n"
        ).format(body=body, title=title)
    return """
body {{ font-family: {body}; margin: 2rem;
  color: #1a1a1a; font-size: 11pt; }}
.cover-otium {{ page-break-after: always; min-height: auto;
  padding: 1.15rem 0.85rem 1.35rem; box-sizing: border-box; }}
.otium-logo {{ font-family: {title}; font-size: 2.15rem;
  font-weight: 600; letter-spacing: 0.18em; margin-bottom: 0.85rem; }}
.otiump {{ margin: 0.42rem 0; line-height: 1.42; text-align: justify;
  font-size: 0.95rem; }}
.guide-title {{ page-break-after: auto; margin-bottom: 0.55rem;
  page-break-inside: avoid; }}
.historical-reference {{ margin: 0.75rem 0 1.15rem;
  page-break-inside: auto; }}
.historical-reference h2 {{ font-family: {title}; font-size: 1.28rem;
  font-weight: 600; margin: 0.4rem 0 0.55rem; }}
.guide-primer, .guide-trip-plans {{ margin: 0.85rem 0 1.25rem;
  page-break-inside: auto; }}
.guide-primer h2, .guide-trip-plans h2 {{ font-family: {title};
  font-size: 1.28rem; font-weight: 600; margin: 0.4rem 0 0.55rem; }}
.guide-primer h3, .trip-plan h3 {{ font-family: {title}; font-size: 1.05rem;
  font-weight: 600; margin: 0.85rem 0 0.35rem; color: #333; }}
.trip-plan {{ margin: 0.65rem 0 1rem; page-break-inside: avoid; }}
ol.trip-stops {{ margin: 0.35rem 0 0.5rem 1.25rem; padding: 0;
  line-height: 1.45; font-size: 0.96rem; }}
ol.trip-stops a {{ color: #1a5276; text-decoration: none; }}
ol.trip-stops a:hover {{ text-decoration: underline; }}
.{tclass} {{ margin-bottom: 0.28rem; }}
.title-strip-label {{ font-size: 0.72rem; text-transform: uppercase;
  letter-spacing: 0.08em; color: #555; margin: 0.5rem 0 0.25rem;
  text-align: center; width: 100%; }}
.heraldry-strip {{ display: flex; flex-wrap: wrap; align-items: center;
  justify-content: center; gap: 0.35rem 0.55rem; margin: 0.2rem 0 0.45rem; }}
.heraldry-fig {{ margin: 0; }}
.heraldry-fig img {{ width: auto; display: block; margin: 0 auto;
  border-radius: 2px; }}
.heraldry-coat-book img {{ max-height: 6.25rem; max-width: 7rem;
  object-fit: contain; }}
.heraldry-strip.heraldry-universities {{ gap: 0.2rem 0.35rem;
  margin: 0.12rem 0 0.35rem; align-items: flex-start; }}
.heraldry-coat-hist img {{ max-height: 6.25rem; max-width: 7rem;
  object-fit: contain; }}
.heraldry-flag-book img {{ max-height: 6.25rem; max-width: 7rem;
  object-fit: contain; }}
.heraldry-univ-cell {{ flex: 0 1 5.6rem; max-width: 5.85rem;
  display: flex; flex-direction: column; align-items: stretch; }}
.heraldry-univ-cell--large {{ flex: 0 0 10.5rem; min-width: 10.5rem;
  max-width: 11rem; }}
.heraldry-univ .heraldry-fig {{ width: 100%; margin: 0; }}
.heraldry-univ .heraldry-fig img {{ max-height: 1.2rem; max-width: 100%;
  width: 100%; object-fit: contain; }}
.heraldry-univ .heraldry-fig img.heraldry-univ-img--large {{
  max-height: 2.65rem; width: 100%; height: auto;
  object-fit: contain; }}
.heraldry-univ-img--on-dark {{ background: #1a3a5f; border-radius: 2px;
  padding: 1px 3px; box-sizing: border-box; }}
.heraldry-univ-caption {{ font-size: 0.52rem; line-height: 1.18;
  margin: 0.12rem 0 0; padding: 0 0.06rem; color: #252525;
  text-align: center; font-weight: 500; }}
.heraldry-motto {{ text-align: center; margin: 0.18rem auto;
  width: 100%; }}
.motto-line {{ font-family: {title}; font-size: 1rem;
  margin: 0; color: #333; line-height: 1.35; }}
.guide-title h1.guide-title-main {{ font-family: {title};
  font-size: 2.35rem; margin-bottom: 0.5rem; font-weight: 600; }}
.lead {{ color: #444; font-size: 1.05rem; }}
{pagination}
.place {{ margin-bottom: 2.2rem; page-break-inside: auto; }}
h3 {{ font-family: {title}; font-size: 1.22rem; margin: 1.2rem 0 0.35rem;
  font-weight: 600; }}
h4 {{ font-family: {title}; font-size: 0.95rem; text-transform: uppercase;
  letter-spacing: 0.06em; margin: 1rem 0 0.4rem; color: #333;
  font-weight: 600; }}
.sub-de, .sub-en, .sub-es, .sub-fr, .sub-ca, .sub-it, .sub-hu, .sub-cs, .sub-he,
.sub-ja {{
  color: #555; font-size: 0.95rem; margin: 0 0 0.5rem; font-style: italic; }}
.place-meta {{ font-size: 0.92rem; color: #353535; margin: 0 0 0.75rem;
  line-height: 1.4; }}
img {{ max-width: 100%; height: auto; display: block; border-radius: 4px; }}
.prose, .place-desc p {{ margin: 0.45rem 0; line-height: 1.5;
  text-align: justify; }}
.place-story-block {{ margin: 0.5rem 0 0.75rem 0; }}
.place-story-block .place-story {{ font-style: italic; color: #4a5568; }}
ul.facts, ul.stories {{ margin: 0.3rem 0 0.6rem 1.2rem; padding: 0; }}
ul.facts li, ul.stories li {{ margin: 0.25rem 0; line-height: 1.45; }}
{hebrew_sub}""".format(
        body=body,
        title=title,
        tclass=title_symbols_class,
        hebrew_sub=hebrew_sub,
        pagination=guide_pdf_pagination_css(
            toc_h2_extra="font-family: {0}".format(title),
        ),
    )
