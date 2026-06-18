# -*- coding: utf-8 -*-
"""Export Moscow guide registries to moscow/data/moscow_places.json for the UI."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.guide_loader import GUIDES, load_guide_with_downloads, load_stories
from scripts.merge_moscow_guide_stories import classify_story_edition


def _download_url(rel: str, downloads: dict[str, str]) -> str:
    name = Path(str(rel).replace("\\", "/")).name
    return str(downloads.get(name) or "").strip()


def _image_extra(rel: str, downloads: dict[str, str]) -> dict[str, str]:
    out: dict[str, str] = {"image_rel_path": rel}
    url = _download_url(rel, downloads)
    if url:
        out["image_source_url"] = url
    return out


def _place_dict(
    guide: str,
    idx: int,
    row: dict[str, Any],
    downloads: dict[str, str],
) -> dict[str, Any]:
    slug = "moscow_{}_{}".format(guide, idx)
    raw_imgs = row.get("images") or []
    images = [x for x in raw_imgs if isinstance(x, str) and x.strip()]
    main = images[0] if images else ""
    extras = [_image_extra(u, downloads) for u in images[1:5]]
    facts_in = row.get("facts") or []
    if isinstance(facts_in, list):
        facts = [str(f).strip() for f in facts_in if str(f).strip()]
    else:
        facts = []
    highlights = row.get("highlights") or []
    hi_txt = ""
    if isinstance(highlights, list) and highlights:
        hi_txt = " · ".join(str(x) for x in highlights[:12])
    addr = str(row.get("address") or "").strip()
    subtitle = addr if addr else hi_txt
    name = str(row.get("name") or "").strip()
    out: dict[str, Any] = {
        "slug": slug,
        "category": guide,
        "name_ru": name,
        "name_en": str(row.get("name_en") or "").strip(),
        "subtitle_en": subtitle,
        "history": str(row.get("history") or "").strip(),
        "significance": str(row.get("significance") or "").strip(),
        "facts": facts,
        "architecture_style": str(row.get("style") or "").strip(),
        "address": addr,
    }
    for base in ("history", "significance"):
        en_val = str(row.get("{}_en".format(base)) or "").strip()
        if en_val:
            out["{}_en".format(base)] = en_val
    story = str(load_stories(guide).get(name) or "").strip()
    if story:
        if classify_story_edition(story) == "ru":
            out["stories_ru"] = [story]
        else:
            out["stories_en"] = [story]
    if main:
        out["image_rel_path"] = main
        main_url = _download_url(main, downloads)
        if main_url:
            out["image_source_url"] = main_url
    if extras:
        out["additional_images"] = extras
    lat = row.get("lat")
    lon = row.get("lon")
    if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
        out["lat"] = float(lat)
        out["lon"] = float(lon)
    return out


def main() -> int:
    out_rows: list[dict[str, Any]] = []
    with_urls = 0
    for guide in GUIDES:
        rows, downloads = load_guide_with_downloads(guide)
        for i, row in enumerate(rows):
            if isinstance(row, dict):
                place = _place_dict(guide, i, row, downloads)
                if place.get("image_source_url"):
                    with_urls += 1
                out_rows.append(place)
    city_dir = _PROJECT_ROOT / "moscow" / "data"
    city_dir.mkdir(parents=True, exist_ok=True)
    dest = city_dir / "moscow_places.json"
    dest.write_text(
        json.dumps(out_rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        "Written {} places ({} with image_source_url) -> {}".format(
            len(out_rows),
            with_urls,
            dest,
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
