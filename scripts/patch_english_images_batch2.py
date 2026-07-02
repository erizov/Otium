# -*- coding: utf-8 -*-
"""Patch English guide images (batch 2) — user-selected + fresh exteriors."""

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

PLACES = ROOT / "english_architecture" / "data" / "english_architecture_places.json"
EXPAND = (
    ROOT
    / "english_architecture"
    / "data"
    / "english_architecture_places_pdf_expand.json"
)
GUIDE = ROOT / "english_architecture"
OVERRIDES = GUIDE / "data" / "image_overrides.py"

IMAGE_PATCHES: dict[str, str] = {
    "english_gothic_salisbury": (
        "https://upload.wikimedia.org/wikipedia/commons/1/1c/"
        "Salisbury_Cathedral%2C_Cathedral_Close%2C_Wiltshire.jpg"
    ),
    "tudor_st_james_piccadilly": (
        "https://upload.wikimedia.org/wikipedia/commons/a/ac/"
        "St_James_Church_Piccadilly_1.jpg"
    ),
    "georgian_bath_royal_crescent": (
        "https://upload.wikimedia.org/wikipedia/commons/4/45/"
        "Royal_Crescent%2C_Bath.jpg"
    ),
    "georgian_bath_circus": (
        "https://wikiway.com/upload/hl-photo/3e3/2ed/bat_5.jpg"
    ),
    "regency_regent_street": (
        "https://www.malls.ru/upload/iblock/0cd/"
        "Depositphotos_26296747_l_2015.jpg"
    ),
    "brutalism_national_theatre": (
        "https://upload.wikimedia.org/wikipedia/commons/7/73/"
        "National_Theatre_London.jpg"
    ),
    "brutalism_alexandra_road": (
        "https://i.ytimg.com/vi/qDNwgbJBHko/maxresdefault.jpg"
    ),
}

# Local-file fallback when primary host is unreachable (metadata URL unchanged).
IMAGE_DOWNLOAD_FALLBACKS: dict[str, str] = {
    "brutalism_alexandra_road": (
        "https://upload.wikimedia.org/wikipedia/commons/e/ee/"
        "Alexandra_Estate_view_facing_east_from_west_side.jpg"
    ),
}

PATCH_ALIASES: dict[str, str] = {
    "english_gothic_salisbury_cathedral": "english_gothic_salisbury",
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
    if not url:
        return row
    out = dict(row)
    out["image_source_url"] = url
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
        if not ok:
            fallback = IMAGE_DOWNLOAD_FALLBACKS.get(slug)
            if fallback:
                print(
                    "  {} primary failed; trying fallback".format(slug),
                    file=sys.stderr,
                )
                ok = _download_url(fallback, dest)
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
