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

from scripts.guide_loader import GUIDES, load_places


def _place_dict(guide: str, idx: int, row: dict[str, Any]) -> dict[str, Any]:
    slug = "moscow_{}_{}".format(guide, idx)
    raw_imgs = row.get("images") or []
    images = [x for x in raw_imgs if isinstance(x, str) and x.strip()]
    main = images[0] if images else ""
    extras = [{"image_rel_path": u} for u in images[1:5]]
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
    out: dict[str, Any] = {
        "slug": slug,
        "category": guide,
        "name_ru": str(row.get("name") or "").strip(),
        "name_en": "",
        "subtitle_en": subtitle,
        "history": str(row.get("history") or "").strip(),
        "significance": str(row.get("significance") or "").strip(),
        "facts": facts,
        "architecture_style": str(row.get("style") or "").strip(),
        "address": addr,
    }
    if main:
        out["image_rel_path"] = main
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
    for guide in GUIDES:
        rows = load_places(guide)
        for i, row in enumerate(rows):
            if isinstance(row, dict):
                out_rows.append(_place_dict(guide, i, row))
    city_dir = _PROJECT_ROOT / "moscow" / "data"
    city_dir.mkdir(parents=True, exist_ok=True)
    dest = city_dir / "moscow_places.json"
    dest.write_text(
        json.dumps(out_rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("Written {} places -> {}".format(len(out_rows), dest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
