# -*- coding: utf-8 -*-
"""Patch German guide images (batch 2) — user-selected + fresh exteriors."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.city_guide_jerusalem_style_images import (  # noqa: E402
    _candidate_urls,
    _download_place_image,
)

PLACES = ROOT / "german_architecture" / "data" / "german_architecture_places.json"
EXPAND = (
    ROOT
    / "german_architecture"
    / "data"
    / "german_architecture_places_pdf_expand.json"
)
GUIDE = ROOT / "german_architecture"
OVERRIDES = GUIDE / "data" / "image_overrides.py"

IMAGE_PATCHES: dict[str, str] = {
    "roman_germania_porta_nigra": (
        "https://upload.wikimedia.org/wikipedia/commons/6/6a/"
        "Porta_Nigra_bei_Nacht.jpg"
    ),
    "romanesque_worms": (
        "https://upload.wikimedia.org/wikipedia/commons/0/00/"
        "Worms-Dom_St_Peter-22-2007-gje.jpg"
    ),
    "romanesque_speyer": (
        "https://upload.wikimedia.org/wikipedia/commons/0/03/"
        "Speyer_Dom_Luft.jpg"
    ),
    "romanesque_mainz": (
        "https://upload.wikimedia.org/wikipedia/commons/7/79/"
        "Mainz_Cathedral_-_Mainz%2C_Germany_-_panoramio.jpg"
    ),
    "gothic_ulm_minster": (
        "https://upload.wikimedia.org/wikipedia/commons/7/71/"
        "Ulm-Minster-0160.jpg"
    ),
    "renaissance_heidelberg": (
        "https://upload.wikimedia.org/wikipedia/commons/5/51/"
        "Heidelberg_Schloss.jpg"
    ),
    "rococo_wieskirche": (
        "https://upload.wikimedia.org/wikipedia/commons/8/87/"
        "Steingaden%2C_Wieskirche_002.jpg"
    ),
    "rococo_zwinger": (
        "https://irecommend.ru/sites/default/files/imagecache/"
        "copyright1/user-images/1294913/Rn6iY1ZjT76JAqmVwT2KWA.jpg"
    ),
    "neoclassicism_walhalla": (
        "https://upload.wikimedia.org/wikipedia/commons/b/b0/"
        "Walhalla-Memorial_01.jpg"
    ),
    "historicism_vienna_votivkirche": (
        "https://upload.wikimedia.org/wikipedia/commons/0/05/"
        "Votivkirche_bei_Nacht_sl1.jpg"
    ),
    "nazi_monumental_tempelhof": (
        "https://upload.wikimedia.org/wikipedia/commons/4/45/"
        "TempelhofExterior.jpg"
    ),
    "postwar_modern_berlin_phil": (
        "https://upload.wikimedia.org/wikipedia/commons/6/65/"
        "Berliner_Philharmonie.jpg"
    ),
    "postwar_modern_hansaviertel": (
        "https://upload.wikimedia.org/wikipedia/commons/7/73/"
        "Interbau_Berlin-Hansaviertel_with_snow_2025-02-14_03.jpg"
    ),
}

PATCH_ALIASES: dict[str, str] = {
    "romanesque_worms_cathedral": "romanesque_worms",
    "romanesque_speyer_cathedral": "romanesque_speyer",
    "romanesque_mainz_cathedral": "romanesque_mainz",
}

ADDRESSES: dict[str, tuple[str, str]] = {
    "historicism_vienna_votivkirche": (
        "Рузвельтплац, 8, 1090 Вена",
        "Rooseveltplatz 8, 1090 Vienna",
    ),
}


def _effective_url(slug: str) -> str | None:
    if slug in IMAGE_PATCHES:
        return IMAGE_PATCHES[slug]
    base = PATCH_ALIASES.get(slug)
    if base:
        return IMAGE_PATCHES.get(base)
    return None


def _patch_row(row: dict[str, Any]) -> dict[str, Any]:
    slug = str(row.get("slug") or "")
    url = _effective_url(slug)
    addr = ADDRESSES.get(slug)
    if not url and not addr:
        return row
    out = dict(row)
    if url:
        out["image_source_url"] = url
    if addr:
        out["address"], out["address_en"] = addr
    return out


def _download_url(url: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    ordered = _candidate_urls(url, 1280)
    ok, _err = _download_place_image(
        ordered,
        dest,
        timeout_sec=60,
        retries_429=5,
        pause_429_sec=50.0,
    )
    return bool(ok and dest.is_file())


def _download_images(by_slug: dict[str, dict[str, Any]]) -> None:
    slugs = sorted(set(IMAGE_PATCHES) | set(PATCH_ALIASES))
    for slug in slugs:
        row = by_slug.get(slug)
        if not row:
            continue
        url = _effective_url(slug)
        if not url:
            continue
        dest = GUIDE / str(row["image_rel_path"])
        if dest.is_file():
            dest.unlink(missing_ok=True)
        ok = _download_url(url, dest)
        print("  {} -> {}".format(slug, "ok" if ok else "fail"))
        time.sleep(20.0)


def _merge_image_overrides() -> None:
    text = OVERRIDES.read_text(encoding="utf-8")
    for slug in sorted(set(IMAGE_PATCHES) | set(PATCH_ALIASES)):
        url = _effective_url(slug)
        if not url:
            continue
        needle = '"{}": ('.format(slug)
        block = (
            '    "{}": (\n'
            '        "{}",\n'
            "        None,\n"
            "    ),"
        ).format(slug, url)
        if needle in text:
            start = text.index(needle)
            end = text.index("),", start) + 2
            text = text[:start] + block + text[end:]
        else:
            insert_at = text.index("IMAGE_URL_OVERRIDES:")
            brace = text.index("{", insert_at)
            text = text[: brace + 1] + "\n" + block + text[brace + 1 :]
    OVERRIDES.write_text(text, encoding="utf-8")


def main() -> int:
    places: list[dict[str, Any]] = json.loads(
        PLACES.read_text(encoding="utf-8"),
    )
    places = [_patch_row(r) for r in places]
    PLACES.write_text(
        json.dumps(places, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    expand: list[dict[str, Any]] = json.loads(
        EXPAND.read_text(encoding="utf-8"),
    )
    expand = [_patch_row(r) for r in expand]
    EXPAND.write_text(
        json.dumps(expand, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    _merge_image_overrides()

    by_slug = {str(r.get("slug") or ""): r for r in places + expand}
    print("Downloading images...")
    _download_images(by_slug)
    print("Patched {} image URLs".format(len(IMAGE_PATCHES)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
