# -*- coding: utf-8 -*-
"""Scan built guide HTML for TOC vs body anchor mismatches."""
from __future__ import annotations

import re
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

_FRONT_MATTER_IDS = frozenset(
    {
        "guide-toc",
        "guide-historical",
        "guide-primer",
        "guide-trips",
        "guide-universities",
        "guide-modern-smolensk",
        "guide-welcome-closing",
    },
)


def _toc_block(html: str) -> str | None:
    match = re.search(
        r'<nav class="guide-toc".*?</nav>',
        html,
        flags=re.DOTALL,
    )
    return match.group(0) if match else None


def _anchors_in_toc(toc_html: str) -> list[str]:
    return re.findall(r'href="#([^"]+)"', toc_html)


def _section_ids(html: str) -> set[str]:
    ids: set[str] = set()
    for match in re.finditer(
        r'<section[^>]+id="([^"]+)"',
        html,
    ):
        ids.add(match.group(1))
    for match in re.finditer(
        r'<div[^>]+class="[^"]*chapter-head[^"]*"[^>]+id="([^"]+)"',
        html,
    ):
        ids.add(match.group(1))
    return ids


def check_guide_html(path: Path) -> dict[str, object] | None:
    html = path.read_text(encoding="utf-8")
    toc = _toc_block(html)
    if not toc:
        return None
    toc_links = _anchors_in_toc(toc)
    body_ids = _section_ids(html)
    toc_set = set(toc_links)
    missing_targets = [a for a in toc_links if a not in body_ids]
    place_body = {
        i
        for i in body_ids
        if i not in _FRONT_MATTER_IDS and not i.startswith("cat-")
    }
    missing_from_toc = sorted(place_body - toc_set)
    label_mismatches: list[tuple[str, str, str]] = []
    for anchor in toc_links:
        if anchor in _FRONT_MATTER_IDS or anchor.startswith("cat-"):
            continue
        label_match = re.search(
            r'href="#{}"[^>]*>([^<]+)</a>'.format(re.escape(anchor)),
            toc,
        )
        if not label_match:
            continue
        toc_label = label_match.group(1)
        heading = re.search(
            r'id="{}"[^>]*>.*?<h3[^>]*>([^<]+)</h3>'.format(
                re.escape(anchor),
            ),
            html,
            flags=re.DOTALL,
        )
        if heading and heading.group(1) != toc_label:
            label_mismatches.append(
                (anchor, toc_label, heading.group(1)),
            )
    return {
        "path": path,
        "missing_targets": missing_targets,
        "missing_from_toc": missing_from_toc,
        "label_mismatches": label_mismatches,
    }


def main() -> int:
    bad: list[dict[str, object]] = []
    for path in sorted(_PROJECT_ROOT.glob("*/output/*_guide*.html")):
        if path.name.endswith("_guide.html"):
            continue
        result = check_guide_html(path)
        if not result:
            continue
        if (
            result["missing_targets"]
            or result["missing_from_toc"]
            or result["label_mismatches"]
        ):
            bad.append(result)
    for row in bad:
        path = row["path"]
        city = path.parent.parent.name
        edition = path.stem.split("_")[-1]
        print("{} ({}):".format(city, edition))
        if row["missing_targets"]:
            print("  TOC links without section:", row["missing_targets"][:8])
        if row["missing_from_toc"]:
            print("  sections missing from TOC:", row["missing_from_toc"][:8])
        for anchor, toc_l, body_l in row["label_mismatches"][:5]:
            print(
                "  label mismatch {}: TOC={!r} body={!r}".format(
                    anchor,
                    toc_l,
                    body_l,
                ),
            )
    print("guides with TOC drift:", len(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
