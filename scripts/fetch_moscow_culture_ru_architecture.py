# -*- coding: utf-8 -*-
"""
Fetch Moscow architecture institutes from culture.ru (api-next atlas).

Catalog page: https://www.culture.ru/architecture/institutes/location-moskva

Output: moscow/data/moscow_culture_ru_catalog.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

_API_URL = (
    "https://www.culture.ru/api-next/atlas/institutes"
    "?statuses%5B0%5D=published&rubricPaths%5B0%5D=566"
    "&limit=140&location=moskva"
)
_PAGE_BASE = "https://www.culture.ru/architecture/institutes/"


def _norm_name(value: str) -> str:
    s = value.strip().lower().replace("ё", "е")
    s = re.sub(r"[^a-zа-я0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _thumb_url(thumb: dict[str, Any] | None) -> str:
    if not thumb:
        return ""
    public_id = str(thumb.get("publicId") or "").strip()
    if not public_id:
        return ""
    return "https://cdn.culture.ru/c/{}.800x600.jpg".format(public_id)


def _fetch_catalog() -> list[dict[str, Any]]:
    req = urllib.request.Request(
        _API_URL,
        headers={
            "User-Agent": "ExcursionGuide/1.0 (Moscow guide; culture.ru catalog)",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        raw = json.loads(resp.read().decode("utf-8"))
    if not isinstance(raw, list):
        raise ValueError("Unexpected API response (expected JSON array)")
    rows: list[dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        title = str(item.get("title") or "").strip()
        slug = str(item.get("name") or "").strip()
        if not title or not slug:
            continue
        loc = item.get("location") or {}
        coords = loc.get("coordinates") if isinstance(loc, dict) else None
        lon = lat = None
        if isinstance(coords, list) and len(coords) >= 2:
            lon, lat = float(coords[0]), float(coords[1])
        rows.append(
            {
                "culture_ru_id": item.get("_id"),
                "name_ru": title,
                "name_norm": _norm_name(title),
                "page_url": urllib.parse.urljoin(_PAGE_BASE, slug),
                "image_source_url": _thumb_url(item.get("thumbnailFile")),
                "address": str(item.get("address") or "").strip(),
                "lat": lat,
                "lon": lon,
            },
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=_PROJECT_ROOT / "moscow" / "data" / "moscow_culture_ru_catalog.json",
    )
    args = parser.parse_args()
    print("Fetching culture.ru Moscow architecture catalog …", file=sys.stderr)
    rows = _fetch_catalog()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    with_img = sum(1 for r in rows if r.get("image_source_url"))
    print("Written {} rows ({} with images) -> {}".format(
        len(rows),
        with_img,
        args.out,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
