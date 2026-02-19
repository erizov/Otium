# -*- coding: utf-8 -*-
"""
Simple script to list places without any images.

Checks all guides and outputs places that have zero image files
(excluding maps). Outputs to console and optionally to a file.

Usage:
  python scripts/list_no_images.py                    # Print to console
  python scripts/list_no_images.py --output report.txt  # Save to file
  python scripts/list_no_images.py --guide monasteries  # Single guide only
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.guide_loader import GUIDES, GUIDE_TO_SUBDIR, load_places

OUTPUT_DIR = _PROJECT_ROOT / "output"


def _basename(rel_path: str) -> str:
    """From 'images/moscow_monasteries/foo_1.jpg' or 'foo_1.jpg' -> 'foo_1.jpg'."""
    return rel_path.replace("\\", "/").split("/")[-1]


def _has_any_image(place: dict[str, Any], img_dir: Path) -> bool:
    """Check if place has at least one image file (map not counted)."""
    images = place.get("images") or []
    return any((img_dir / _basename(p)).is_file() for p in images)


def main() -> int:
    """List places without any images."""
    parser = argparse.ArgumentParser(
        description="List places without any image files",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output file path (default: print to console)",
    )
    parser.add_argument(
        "--guide",
        type=str,
        default=None,
        choices=list(GUIDES) + [None],
        help="Check single guide only (default: all guides)",
    )
    args = parser.parse_args()

    guides_to_check = [args.guide] if args.guide else GUIDES
    places_without: list[tuple[str, str]] = []  # (guide, place_name)

    for guide in guides_to_check:
        if guide == "test_e2e":
            continue
        try:
            places = load_places(guide)
        except Exception as e:
            print("Skip {}: {}.".format(guide, e), file=sys.stderr)
            continue
        subdir = GUIDE_TO_SUBDIR.get(guide)
        if not subdir:
            continue
        img_dir = OUTPUT_DIR / "images" / subdir
        for place in places:
            name = place.get("name") or "?"
            if not _has_any_image(place, img_dir):
                places_without.append((guide, name))

    # Build output
    lines: list[str] = []
    if args.guide:
        lines.append("Places without images in '{}':".format(args.guide))
    else:
        lines.append("Places without any images (all guides):")
    lines.append("=" * 60)
    lines.append("")

    if not places_without:
        lines.append("All places have at least one image.")
    else:
        if args.guide:
            for _, name in places_without:
                lines.append("  - {}".format(name))
        else:
            # Group by guide
            by_guide: dict[str, list[str]] = {}
            for guide, name in places_without:
                if guide not in by_guide:
                    by_guide[guide] = []
                by_guide[guide].append(name)

            for guide in sorted(by_guide.keys()):
                lines.append("{} ({}):".format(guide, len(by_guide[guide])))
                for name in sorted(by_guide[guide]):
                    lines.append("  - {}".format(name))
                lines.append("")

        lines.append("")
        lines.append("Total: {} place(s) without images".format(len(places_without)))

    output_text = "\n".join(lines)

    if args.output:
        out_path = Path(args.output)
        out_path.write_text(output_text, encoding="utf-8")
        print("Written: {}".format(out_path))
    else:
        print(output_text)

    return 0 if places_without else 1


if __name__ == "__main__":
    sys.exit(main())
