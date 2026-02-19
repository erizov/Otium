# -*- coding: utf-8 -*-
"""
Build a test page showing all OTIUM emblem variants (A–T).

Usage:
  python scripts/build_emblem_preview.py

Writes output/emblem_variants.html. Open in a browser to compare variants.
"""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

OUTPUT_DIR = _PROJECT_ROOT / "output"

# Original A–E match build_full_guide.py; F–K are Russian/Soviet-inspired.
EMBLEM_VARIANTS = {
    "A": (
        '<svg class="{{class}}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"'
        ' role="img"><title>OTIUM — laurel wreath and Kremlin tower</title>'
        '<circle cx="32" cy="32" r="29" fill="none" stroke="#8b7355" stroke-width="1.2"/>'
        '<circle cx="32" cy="32" r="25" fill="none" stroke="#c9c4b8" stroke-width="0.6"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.8" '
        'd="M20 36 Q20 22 32 18 Q44 22 44 36"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.8" d="M20 36 Q32 42 44 36"/>'
        '<path fill="#2c2a28" d="M29 24 h6 v20 h-6 z"/>'
        '<path fill="#2c2a28" d="M27 24 L32 18 L37 24 L37 26 L27 26 z"/>'
        '<circle fill="#8b7355" cx="32" cy="16" r="1.8"/>'
        "</svg>"
    ),
    "B": (
        '<svg class="{{class}}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"'
        ' role="img"><title>OTIUM — Kremlin tower seal</title>'
        '<circle cx="32" cy="32" r="28" fill="none" stroke="#8b7355" stroke-width="1.5"/>'
        '<path fill="#2c2a28" d="M28 20 h8 v24 h-8 z"/>'
        '<path fill="#2c2a28" d="M26 20 L32 14 L38 20 L38 22 L26 22 z"/>'
        '<circle fill="#8b7355" cx="32" cy="12" r="2.5"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.7" '
        'd="M32 8 L32 6 M28 10 L26 8 M36 10 L38 8"/>'
        "</svg>"
    ),
    "C": (
        '<svg class="{{class}}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"'
        ' role="img"><title>OTIUM — laurel wreath (dignity)</title>'
        '<circle cx="32" cy="32" r="28" fill="none" stroke="#8b7355" stroke-width="1.2"/>'
        '<circle cx="32" cy="32" r="24" fill="none" stroke="#c9c4b8" stroke-width="0.5"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.9" '
        'd="M16 32 Q16 20 32 14 Q48 20 48 32 Q32 44 16 32"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.9" d="M16 32 Q32 42 48 32"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.6" '
        'd="M24 28 Q32 24 40 28 M24 36 Q32 40 40 36"/>'
        "</svg>"
    ),
    "D": (
        '<svg class="{{class}}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"'
        ' role="img"><title>OTIUM — letter O and tower</title>'
        '<circle cx="32" cy="32" r="26" fill="none" stroke="#8b7355" stroke-width="1.2"/>'
        '<text x="32" y="38" font-family="Georgia,serif" font-size="22" font-weight="600" '
        'fill="#2c2a28" text-anchor="middle">O</text>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.6" '
        'd="M32 44 L32 48 M28 46 L32 50 L36 46"/>'
        "</svg>"
    ),
    "E": (
        '<svg class="{{class}}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"'
        ' role="img"><title>OTIUM — shield, tower and laurel</title>'
        '<path fill="none" stroke="#8b7355" stroke-width="1.2" '
        'd="M32 6 L52 18 L52 46 Q52 54 32 58 Q12 54 12 46 L12 18 Z"/>'
        '<path fill="#2c2a28" d="M28 24 h8 v18 h-8 z"/>'
        '<path fill="#2c2a28" d="M26 24 L32 18 L38 24 L38 26 L26 26 z"/>'
        '<circle fill="#8b7355" cx="32" cy="16" r="1.5"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.6" '
        'd="M20 38 Q32 34 44 38 M20 42 Q32 46 44 42"/>'
        "</svg>"
    ),
    # F–K: Russian and Soviet symbol inspiration
    "F": (
        '<svg class="{{class}}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"'
        ' role="img"><title>OTIUM — five-pointed star (Kremlin)</title>'
        '<circle cx="32" cy="32" r="28" fill="none" stroke="#8b7355" stroke-width="1.2"/>'
        '<path fill="#8b7355" d="M32 10 L38 26 L54 26 L42 36 L46 52 L32 42 L18 52 L22 36 '
        'L10 26 L26 26 Z"/>'
        "</svg>"
    ),
    "G": (
        '<svg class="{{class}}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"'
        ' role="img"><title>OTIUM — star and laurel wreath</title>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.9" '
        'd="M18 32 Q18 20 32 14 Q46 20 46 32 Q32 44 18 32"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.9" '
        'd="M18 32 Q32 40 46 32"/>'
        '<path fill="#8b7355" d="M32 12 L35 24 L46 22 L37 30 L39 42 L32 36 L25 42 L27 30 '
        'L18 22 L29 24 Z"/>'
        "</svg>"
    ),
    "H": (
        '<svg class="{{class}}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"'
        ' role="img"><title>OTIUM — sunburst and tower</title>'
        '<path fill="none" stroke="#c9c4b8" stroke-width="0.6" '
        'd="M32 6 L32 12 M32 52 L32 58 M6 32 L12 32 M52 32 L58 32"/>'
        '<path fill="none" stroke="#c9c4b8" stroke-width="0.5" '
        'd="M16 16 L20 20 M48 16 L44 20 M48 48 L44 44 M16 48 L20 44"/>'
        '<path fill="#2c2a28" d="M29 24 h6 v20 h-6 z"/>'
        '<path fill="#2c2a28" d="M27 24 L32 18 L37 24 L37 26 L27 26 z"/>'
        '<circle fill="#8b7355" cx="32" cy="16" r="1.5"/>'
        '<circle cx="32" cy="32" r="28" fill="none" stroke="#8b7355" stroke-width="1"/>'
        "</svg>"
    ),
    "I": (
        '<svg class="{{class}}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"'
        ' role="img"><title>OTIUM — wheat ears (Soviet harvest)</title>'
        '<circle cx="32" cy="32" r="28" fill="none" stroke="#8b7355" stroke-width="1.2"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.8" '
        'd="M20 32 Q24 20 32 18 Q40 20 44 32 M22 34 Q30 24 32 24 Q34 24 42 34"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.7" '
        'd="M26 38 Q32 28 38 38 M28 42 Q32 34 36 42"/>'
        '<path fill="#2c2a28" d="M30 44 h4 v8 h-4 z"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.6" '
        'd="M32 50 L32 56 M28 54 L32 58 L36 54"/>'
        "</svg>"
    ),
    "J": (
        '<svg class="{{class}}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"'
        ' role="img"><title>OTIUM — gear and star (industry)</title>'
        '<circle cx="32" cy="32" r="26" fill="none" stroke="#8b7355" stroke-width="1.2"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.9" '
        'd="M32 8 L32 14 M32 50 L32 56 M8 32 L14 32 M50 32 L56 32"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.9" '
        'd="M14 14 L18 18 M46 14 L42 18 M46 46 L42 42 M14 46 L18 42"/>'
        '<path fill="#8b7355" d="M32 16 L34 22 L40 22 L35 26 L37 32 L32 28 L27 32 L29 26 '
        'L24 22 L30 22 Z"/>'
        "</svg>"
    ),
    "K": (
        '<svg class="{{class}}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"'
        ' role="img"><title>OTIUM — rays and circle (dawn)</title>'
        '<path fill="#8b7355" fill-opacity="0.15" '
        'd="M32 32 L32 4 L36 4 L36 32 L64 32 L64 36 L36 36 L36 64 L32 64 L32 36 L4 36 L4 32 Z"/>'
        '<path fill="#8b7355" fill-opacity="0.12" '
        'd="M32 32 L48 8 L52 12 L36 32 L52 52 L48 56 Z M32 32 L16 8 L12 12 L28 32 L12 52 '
        'L16 56 Z"/>'
        '<circle cx="32" cy="32" r="22" fill="none" stroke="#8b7355" stroke-width="1.2"/>'
        '<circle cx="32" cy="32" r="18" fill="none" stroke="#c9c4b8" stroke-width="0.5"/>'
        '<path fill="#2c2a28" d="M29 26 h6 v14 h-6 z"/>'
        '<path fill="#2c2a28" d="M27 26 L32 20 L37 26 L37 28 L27 28 z"/>'
        '<circle fill="#8b7355" cx="32" cy="20" r="1.2"/>'
        "</svg>"
    ),
    # L–T: International (US, EU, Roma, SPB, MSK), literature, architecture
    "L": (
        '<svg class="{{class}}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"'
        ' role="img"><title>OTIUM — US (stars and stripes)</title>'
        '<circle cx="32" cy="32" r="28" fill="none" stroke="#8b7355" stroke-width="1.2"/>'
        '<path fill="#8b7355" d="M32 10 L34 20 L42 18 L35 24 L38 34 L32 28 L26 34 L29 24 '
        'L22 18 L30 20 Z"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.8" '
        'd="M20 38 L44 38 M20 42 L44 42 M20 46 L44 46 M20 50 L44 50"/>'
        "</svg>"
    ),
    "M": (
        '<svg class="{{class}}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"'
        ' role="img"><title>OTIUM — European (circle of stars)</title>'
        '<circle cx="32" cy="32" r="28" fill="none" stroke="#8b7355" stroke-width="1.2"/>'
        '<circle cx="32" cy="32" r="24" fill="none" stroke="#c9c4b8" stroke-width="0.5"/>'
        '<g fill="#8b7355">'
        '<circle cx="32" cy="14" r="2.2"/>'
        '<circle cx="48" cy="22" r="2.2"/>'
        '<circle cx="50" cy="38" r="2.2"/>'
        '<circle cx="38" cy="52" r="2.2"/>'
        '<circle cx="22" cy="52" r="2.2"/>'
        '<circle cx="14" cy="38" r="2.2"/>'
        '<circle cx="16" cy="22" r="2.2"/>'
        '<circle cx="26" cy="14" r="2.2"/>'
        '<circle cx="32" cy="32" r="2.2"/>'
        '</g>'
        "</svg>"
    ),
    "N": (
        '<svg class="{{class}}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"'
        ' role="img"><title>OTIUM — Roma (laurel and column)</title>'
        '<circle cx="32" cy="32" r="28" fill="none" stroke="#8b7355" stroke-width="1.2"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.9" '
        'd="M16 32 Q16 20 32 14 Q48 20 48 32 Q32 44 16 32"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.9" '
        'd="M16 32 Q32 40 48 32"/>'
        '<path fill="#2c2a28" d="M28 20 h8 v28 h-8 z"/>'
        '<path fill="#8b7355" d="M30 16 h4 v4 h-4 z"/>'
        "</svg>"
    ),
    "O": (
        '<svg class="{{class}}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"'
        ' role="img"><title>OTIUM — SPB (ship spire, anchor)</title>'
        '<circle cx="32" cy="32" r="28" fill="none" stroke="#8b7355" stroke-width="1.2"/>'
        '<path fill="#2c2a28" d="M30 12 L34 12 L34 24 L38 24 L32 32 L26 24 L30 24 Z"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.8" '
        'd="M32 32 L32 44 M24 38 L32 44 L40 38 M24 38 L24 50 L40 50 L40 38"/>'
        '<circle fill="#8b7355" cx="32" cy="46" r="2"/>'
        "</svg>"
    ),
    "P": (
        '<svg class="{{class}}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"'
        ' role="img"><title>OTIUM — MSK (onion dome and tower)</title>'
        '<circle cx="32" cy="32" r="28" fill="none" stroke="#8b7355" stroke-width="1.2"/>'
        '<path fill="#2c2a28" d="M28 28 h8 v18 h-8 z"/>'
        '<path fill="#8b7355" d="M26 26 Q32 14 38 26 Q32 22 26 26"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.6" '
        'd="M32 14 L32 10 M28 16 L26 14 M36 16 L38 14"/>'
        '<circle fill="#8b7355" cx="32" cy="12" r="1.8"/>'
        "</svg>"
    ),
    "Q": (
        '<svg class="{{class}}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"'
        ' role="img"><title>OTIUM — literature (open book)</title>'
        '<circle cx="32" cy="32" r="28" fill="none" stroke="#8b7355" stroke-width="1.2"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="1" '
        'd="M20 24 L20 42 Q32 38 44 42 L44 24 Q32 28 20 24"/>'
        '<path fill="none" stroke="#c9c4b8" stroke-width="0.6" '
        'd="M32 28 L32 38"/>'
        '<path fill="#2c2a28" d="M22 26 L42 26 L42 40 L22 40 Z"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.5" d="M26 30 L38 30"/>'
        "</svg>"
    ),
    "R": (
        '<svg class="{{class}}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"'
        ' role="img"><title>OTIUM — literature (quill and lamp)</title>'
        '<circle cx="32" cy="32" r="28" fill="none" stroke="#8b7355" stroke-width="1.2"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.9" '
        'd="M24 44 Q28 36 32 32 Q36 28 40 44"/>'
        '<path fill="#2c2a28" d="M38 42 L42 46 L40 48 L36 44 Z"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.7" '
        'd="M32 18 L32 26 M28 22 L36 22"/>'
        '<ellipse fill="#8b7355" cx="32" cy="16" rx="4" ry="3"/>'
        '<path fill="none" stroke="#c9c4b8" stroke-width="0.5" '
        'd="M28 14 L36 14 L34 18 L30 18 Z"/>'
        "</svg>"
    ),
    "S": (
        '<svg class="{{class}}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"'
        ' role="img"><title>OTIUM — architecture (column and arch)</title>'
        '<circle cx="32" cy="32" r="28" fill="none" stroke="#8b7355" stroke-width="1.2"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.9" '
        'd="M18 20 L18 48 M46 20 L46 48"/>'
        '<path fill="#2c2a28" d="M16 18 L20 18 L20 50 L16 50 Z"/>'
        '<path fill="#2c2a28" d="M44 18 L48 18 L48 50 L44 50 Z"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.8" '
        'd="M20 24 Q32 14 44 24 M20 44 Q32 34 44 44"/>'
        "</svg>"
    ),
    "T": (
        '<svg class="{{class}}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"'
        ' role="img"><title>OTIUM — architecture (dome and pediment)</title>'
        '<circle cx="32" cy="32" r="28" fill="none" stroke="#8b7355" stroke-width="1.2"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="1" '
        'd="M14 36 Q14 24 32 18 Q50 24 50 36"/>'
        '<path fill="#2c2a28" d="M22 28 h20 v20 h-20 z"/>'
        '<path fill="none" stroke="#8b7355" stroke-width="0.7" '
        'd="M22 28 L32 20 L42 28"/>'
        '<circle fill="#8b7355" cx="32" cy="22" r="2"/>'
        "</svg>"
    ),
}

VARIANT_TITLES = {
    "A": "Laurel wreath and Kremlin tower",
    "B": "Kremlin tower seal",
    "C": "Laurel wreath (dignity)",
    "D": "Letter O and tower",
    "E": "Shield, tower and laurel",
    "F": "Five-pointed star (Kremlin)",
    "G": "Star and laurel wreath",
    "H": "Sunburst and tower",
    "I": "Wheat ears (Soviet harvest)",
    "J": "Gear and star (industry)",
    "K": "Rays and circle (dawn)",
    "L": "US (stars and stripes)",
    "M": "European (circle of stars)",
    "N": "Roma (laurel and column)",
    "O": "SPB (ship spire, anchor)",
    "P": "MSK (onion dome and tower)",
    "Q": "Literature (open book)",
    "R": "Literature (quill and lamp)",
    "S": "Architecture (column and arch)",
    "T": "Architecture (dome and pediment)",
}


def main() -> int:
    """Write output/emblem_variants.html with all emblem variants."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    parts = []
    for key in (
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
        "L", "M", "N", "O", "P", "Q", "R", "S", "T",
    ):
        svg = EMBLEM_VARIANTS[key].replace("{{class}}", "emblem-preview")
        title = VARIANT_TITLES.get(key, "")
        parts.append(
            '<div class="variant">'
            '<span class="label">Variant {}</span>'
            '<span class="desc">{}</span>'
            "{}"
            "</div>"
            .format(key, title, svg)
        )
    body = "\n".join(parts)
    css = (
        "body { font-family: Georgia, serif; background: #f5f2eb; "
        "color: #2c2a28; padding: 2em; max-width: 1000px; margin: 0 auto; }\n"
        "h1 { font-size: 1.4em; margin-bottom: 0.5em; }\n"
        "p.subtitle { color: #6b635b; margin-bottom: 2em; }\n"
        ".grid { display: flex; flex-wrap: wrap; gap: 2.5em; }\n"
        ".variant { text-align: center; min-width: 140px; }\n"
        ".label { display: block; margin-bottom: 0.25em; font-weight: 600; "
        "font-size: 1.1em; }\n"
        ".desc { display: block; margin-bottom: 0.75em; font-size: 0.85em; "
        "color: #6b635b; }\n"
        ".emblem-preview { width: 120px; height: 120px; display: block; "
        "margin: 0 auto; }\n"
    )
    html = (
        "<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'>"
        "<title>OTIUM emblem variants</title><style>{}</style></head>"
        "<body>"
        "<h1>OTIUM emblem variants</h1>"
        "<p class='subtitle'>Test page — A–E original, F–K Russian/Soviet, "
        "L–T international (US, EU, Roma, SPB, MSK), literature, architecture. "
        "Set EMBLEM_CHOICE in scripts/build_full_guide.py to use in guide.</p>"
        "<div class='grid'>{}</div></body></html>"
    ).format(css, body)
    path = OUTPUT_DIR / "emblem_variants.html"
    path.write_text(html, encoding="utf-8")
    print("Written: {}".format(path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
