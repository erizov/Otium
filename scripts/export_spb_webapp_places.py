# -*- coding: utf-8 -*-
"""Export SPB osobnjaki registry to spb/data/spb_places_osobnjaki.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from spb.data.osobnjaki import OSOBNJAKI
from spb.data.osobnjaki_image_urls import OSOBNJAKI_IMAGE_DOWNLOADS
from spb.data.osobnjaki_stories import OSOBNJAKI_STORIES


def _download_url(rel: str) -> str:
    name = Path(str(rel).replace("\\", "/")).name
    return str(OSOBNJAKI_IMAGE_DOWNLOADS.get(name) or "").strip()


def _place_dict(idx: int, row: dict[str, Any]) -> dict[str, Any]:
    slug = "spb_osobnjaki_{}".format(idx)
    images = [x for x in row.get("images") or [] if isinstance(x, str)]
    main = images[0] if images else ""
    facts_in = row.get("facts") or []
    facts = [str(f).strip() for f in facts_in if str(f).strip()]
    addr = str(row.get("address") or "").strip()
    name = str(row.get("name") or "").strip()
    out: dict[str, Any] = {
        "slug": slug,
        "category": "osobnjaki",
        "name_ru": name,
        "name_en": str(row.get("name_en") or "").strip(),
        "subtitle_en": addr,
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
    story = str(OSOBNJAKI_STORIES.get(name) or "").strip()
    if story:
        out["stories_ru"] = [story]
    if main:
        out["image_rel_path"] = main
        url = _download_url(main)
        if url:
            out["image_source_url"] = url
    extras = []
    for rel in images[1:5]:
        block = {"image_rel_path": rel}
        url = _download_url(rel)
        if url:
            block["image_source_url"] = url
        extras.append(block)
    if extras:
        out["additional_images"] = extras
    return out


def main() -> int:
    rows = [_place_dict(i, r) for i, r in enumerate(OSOBNJAKI)]
    out_path = _PROJECT_ROOT / "spb" / "data" / "spb_places_osobnjaki.json"
    out_path.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    with_url = sum(1 for r in rows if r.get("image_source_url"))
    print(
        "Written {} osobnjaki ({} with image_source_url) -> {}".format(
            len(rows), with_url, out_path,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
