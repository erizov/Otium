# -*- coding: utf-8 -*-
"""Patch English guide images (exteriors) and UK-localized addresses."""

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
    "roman_britain_fishbourne": (
        "https://upload.wikimedia.org/wikipedia/commons/7/75/"
        "Fishbourne_palace_north_wing.JPG"
    ),
    "palladian_wren_greenwich": (
        "https://upload.wikimedia.org/wikipedia/commons/b/b0/"
        "Royal_Naval_College_Greenwich_view_from_the_Thames.jpg"
    ),
    "regency_regent_street": (
        "https://upload.wikimedia.org/wikipedia/commons/8/80/"
        "Regent_Street_2011-04-25.jpg"
    ),
    "arts_crafts_red_house": (
        "https://upload.wikimedia.org/wikipedia/commons/0/03/"
        "The_Red_House%2C_Bexleyheath.JPG"
    ),
    "arts_crafts_blackwell": (
        "https://upload.wikimedia.org/wikipedia/commons/e/ec/"
        "Bowness-on-Windermere%2C_Blackwell%2C_the_Arts_and_Crafts_House_"
        "-_geograph.org.uk_-_7612905.jpg"
    ),
    "edwardian_lloyds_register": (
        "https://upload.wikimedia.org/wikipedia/commons/5/5e/"
        "Lloyd%27s_register.JPG"
    ),
    "art_deco_daily_telegraph": (
        "https://upload.wikimedia.org/wikipedia/commons/1/12/"
        "Fleet_Street%2C_former_Daily_Telegraph_headquarters_"
        "-_geograph.org.uk_-_2244211.jpg"
    ),
    "brutalism_alexandra_road": (
        "https://upload.wikimedia.org/wikipedia/commons/3/33/"
        "Alexander_and_Ainsworth_Estate%2C_London._Fujifilm.jpg"
    ),
    "brutalism_clifton_cathedral": (
        "https://upload.wikimedia.org/wikipedia/commons/3/31/"
        "Clifton_Cathedral_-_PXL_20260331_133707156.jpg"
    ),
    "art_deco_willesden_synagogue": (
        "https://upload.wikimedia.org/wikipedia/commons/c/ce/"
        "Synagogue_on_Parkside%2C_Willesden_-_geograph.org.uk_-_62124.jpg"
    ),
    "tudor_st_james_piccadilly": (
        "https://upload.wikimedia.org/wikipedia/commons/5/50/"
        "London_-_Piccadilly_-_St._James%27s_Church_-_Piccadilly_Market_"
        "-_ICE_Fisheye.jpg"
    ),
    "georgian_bath_abbey": (
        "https://upload.wikimedia.org/wikipedia/commons/9/97/"
        "Bath_Abbey_Exterior%2C_Somerset%2C_UK_-_Diliff.jpg"
    ),
    "georgian_bevis_marks_synagogue": (
        "https://upload.wikimedia.org/wikipedia/commons/2/22/"
        "Bevis_Marks_Synagogue_05.JPG"
    ),
}

REMOVE_SLUGS = frozenset({"georgian_boston_old_north"})

# address_ru, address_en — UK conventions
ADDRESSES: dict[str, tuple[str, str]] = {
    "roman_britain_fishbourne": (
        "Солтхилл-роуд, Фишборн, PO19 3QR",
        "Salthill Road, Fishbourne, PO19 3QR",
    ),
    "palladian_wren_greenwich": (
        "Кинг-Уильям-уок, Гринвич, Лондон SE10 9NN",
        "King William Walk, Greenwich, London SE10 9NN",
    ),
    "regency_regent_street": (
        "Риджент-стрит, Лондон W1",
        "Regent Street, London W1",
    ),
    "arts_crafts_red_house": (
        "Ред-Хаус-лейн, Бекслихит, Лондон DA6 8JF",
        "Red House Lane, Bexleyheath, London DA6 8JF",
    ),
    "arts_crafts_blackwell": (
        "Боунесс-он-Уиндермир, Камбрия LA23 3JT",
        "Bowness-on-Windermere, Cumbria LA23 3JT",
    ),
    "edwardian_lloyds_register": (
        "Фенчёрч-стрит, 71, Лондон EC3M 4BS",
        "71 Fenchurch Street, London EC3M 4BS",
    ),
    "art_deco_daily_telegraph": (
        "Флит-стрит, 135–141, Лондон EC4A 2BU",
        "135–141 Fleet Street, London EC4A 2BU",
    ),
    "brutalism_alexandra_road": (
        "Александра-роуд, Лондон NW8 0DH",
        "Alexandra Road, London NW8 0DH",
    ),
    "brutalism_clifton_cathedral": (
        "Клифтон-парк, Бристоль BS8 3BX",
        "Clifton Park, Bristol BS8 3BX",
    ),
    "art_deco_willesden_synagogue": (
        "Парксайд, Уиллсден, Лондон NW2 5RX",
        "Parkside, Willesden, London NW2 5RX",
    ),
    "tudor_st_james_piccadilly": (
        "Пикадилли, Лондон W1J 9LL",
        "Piccadilly, London W1J 9LL",
    ),
    "georgian_bath_abbey": (
        "Бат-Эбби Чёрчярд, Бат BA1 1LT",
        "Bath Abbey Churchyard, Bath BA1 1LT",
    ),
    "georgian_bevis_marks_synagogue": (
        "Бевис Маркс, Лондон EC3A 7LH",
        "Bevis Marks, London EC3A 7LH",
    ),
}


def _patch_row(row: dict[str, Any]) -> dict[str, Any]:
    slug = str(row.get("slug") or "")
    if slug in REMOVE_SLUGS:
        return row
    url = IMAGE_PATCHES.get(slug)
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
    for slug in sorted(IMAGE_PATCHES):
        row = by_slug.get(slug)
        if not row:
            continue
        url = IMAGE_PATCHES[slug]
        dest = GUIDE / str(row["image_rel_path"])
        if dest.is_file():
            dest.unlink(missing_ok=True)
        ok = _download_url(url, dest)
        print("  {} -> {}".format(slug, "ok" if ok else "fail"))
        time.sleep(18.0)


def _merge_image_overrides() -> None:
    text = OVERRIDES.read_text(encoding="utf-8")
    if "IMAGE_URL_OVERRIDES: dict" in text and not text.strip().endswith("}"):
        pass
    lines = [
        "# -*- coding: utf-8 -*-",
        '"""Explicit image URLs for guide places."""',
        "",
        "from __future__ import annotations",
        "",
        "from typing import Any",
        "",
        "IMAGE_URL_OVERRIDES: dict[str, tuple[str, str | None]] = {",
    ]
    for slug in sorted(IMAGE_PATCHES):
        lines.append('    "{}": ('.format(slug))
        lines.append('        "{}",'.format(IMAGE_PATCHES[slug]))
        lines.append("        None,")
        lines.append("    ),")
    lines.extend([
        "}",
        "PRIMARY_IMAGE_REUSE: dict[str, tuple[str, str]] = {}",
        "SECOND_IMAGE_REUSE: dict[str, tuple[str, str]] = {}",
        "",
        "",
        "def apply_image_url_overrides(place: dict[str, Any]) -> dict[str, Any]:",
        '    slug = str(place.get("slug") or "")',
        "    override = IMAGE_URL_OVERRIDES.get(slug)",
        "    if not override:",
        "        return place",
        "    primary, secondary = override",
        "    merged = dict(place)",
        '    merged["image_source_url"] = primary',
        "    if secondary:",
        '        merged["additional_images"] = [{',
        '            "image_source_url": secondary,',
        "        }]",
        "    else:",
        '        merged.pop("additional_images", None)',
        "    return merged",
        "",
    ])
    OVERRIDES.write_text("\n".join(lines), encoding="utf-8")


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
    expand = [
        _patch_row(r)
        for r in expand
        if str(r.get("slug") or "") not in REMOVE_SLUGS
    ]
    EXPAND.write_text(
        json.dumps(expand, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    old_img = GUIDE / "images/styles/georgian_boston_old_north.jpg"
    if old_img.is_file():
        old_img.unlink(missing_ok=True)

    _merge_image_overrides()

    by_slug = {str(r.get("slug") or ""): r for r in places + expand}
    print("Downloading images...")
    _download_images(by_slug)
    print(
        "Patched {} images, {} addresses, removed {}".format(
            len(IMAGE_PATCHES),
            len(ADDRESSES),
            len(REMOVE_SLUGS),
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
