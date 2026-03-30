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
}

_DEFAULT = (
    "https://fonts.googleapis.com/css2?"
    "family=Cormorant+Garamond:wght@600&"
    "family=Source+Sans+3:wght@400;600&display=swap",
    "'Cormorant Garamond', serif",
    "'Source Sans 3', sans-serif",
)


def typography_triple(city_slug: str) -> tuple[str, str, str]:
    """Href and CSS font-family stacks for city slug (snake_case)."""
    return _TYPO.get(city_slug, _DEFAULT)


def guide_inline_css(title_symbols_class: str, city_slug: str) -> str:
    """Inline CSS for Latin-script city guides (not Smolensk/SPB)."""
    _, title, body = typography_triple(city_slug)
    return """
body {{ font-family: {body}; margin: 2rem;
  color: #1a1a1a; font-size: 11pt; }}
.cover-otium {{ page-break-after: always; min-height: auto;
  padding: 1.15rem 0.85rem 1.35rem; box-sizing: border-box; }}
.otium-logo {{ font-family: {title}; font-size: 2.15rem;
  font-weight: 600; letter-spacing: 0.18em; margin-bottom: 0.85rem; }}
.otiump {{ margin: 0.42rem 0; line-height: 1.42; text-align: justify;
  max-width: 38rem; font-size: 0.95rem; }}
.guide-title {{ page-break-after: auto; margin-bottom: 0.55rem;
  page-break-inside: avoid; }}
.{tclass} {{ margin-bottom: 0.28rem; }}
.title-strip-label {{ font-size: 0.72rem; text-transform: uppercase;
  letter-spacing: 0.08em; color: #555; margin: 0.5rem 0 0.25rem;
  text-align: center; width: 100%; }}
.heraldry-strip {{ display: flex; flex-wrap: wrap; align-items: center;
  justify-content: center; gap: 0.35rem 0.55rem; margin: 0.2rem 0 0.45rem; }}
.heraldry-fig {{ margin: 0; }}
.heraldry-fig img {{ width: auto; display: block; margin: 0 auto;
  border-radius: 2px; }}
.heraldry-coat-book img {{ max-height: 3.35rem; object-fit: contain; }}
.guide-title h1.guide-title-main {{ font-family: {title};
  font-size: 2.35rem; margin-bottom: 0.5rem; font-weight: 600; }}
.lead {{ color: #444; font-size: 1.05rem; }}
.place {{ margin-bottom: 2.2rem; page-break-inside: auto; }}
h3 {{ font-family: {title}; font-size: 1.22rem; margin: 1.2rem 0 0.35rem;
  font-weight: 600; }}
h4 {{ font-family: {title}; font-size: 0.95rem; text-transform: uppercase;
  letter-spacing: 0.06em; margin: 1rem 0 0.4rem; color: #333;
  font-weight: 600; }}
.sub-de, .sub-en, .sub-es, .sub-fr, .sub-ca, .sub-it, .sub-hu, .sub-cs {{
  color: #555; font-size: 0.95rem; margin: 0 0 0.5rem; font-style: italic; }}
.place-meta {{ font-size: 0.92rem; color: #353535; margin: 0 0 0.75rem;
  line-height: 1.4; }}
.place-fig {{ margin: 0.5rem 0 1rem; }}
img {{ max-width: 100%; height: auto; display: block; border-radius: 4px; }}
.prose, .place-desc p {{ margin: 0.45rem 0; line-height: 1.5;
  text-align: justify; }}
ul.facts, ul.stories {{ margin: 0.3rem 0 0.6rem 1.2rem; padding: 0; }}
ul.facts li, ul.stories li {{ margin: 0.25rem 0; line-height: 1.45; }}
""".format(
        body=body,
        title=title,
        tclass=title_symbols_class,
    )
