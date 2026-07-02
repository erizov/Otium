# -*- coding: utf-8 -*-
"""Add Art Nouveau chapter (5 places) to English architecture guide."""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

PLACES = ROOT / "english_architecture" / "data" / "english_architecture_places.json"
EXPAND = (
    ROOT
    / "english_architecture"
    / "data"
    / "english_architecture_places_pdf_expand.json"
)
GUIDE = ROOT / "english_architecture"
OVERRIDES = GUIDE / "data" / "image_overrides.py"

_STYLE_RU = "Ар-нуво (1890-е — 1914)"
_STYLE_EN = "Art Nouveau (1890s–1914)"
_LICENSE = "See Wikimedia Commons file page for license."
_ATTRIBUTION = "Wikimedia Commons contributors"

HARRODS_IMAGE = (
    "https://i.pinimg.com/originals/d5/e7/c0/"
    "d5e7c01cffd89f1d8d177280ec4325d4.jpg"
)


def _normalize_name(name: str) -> str:
    text = name.lower().strip()
    text = text.replace("’", "'").replace("`", "'")
    text = re.sub(r"[^a-zа-яё0-9]+", " ", text, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", text).strip()


NEW_ROWS: list[dict[str, Any]] = [
    {
        "slug": "art_nouveau_queens_cross_church",
        "category": "art_nouveau",
        "name_ru": "Церковь Куинз-кросс",
        "name_en": "Queen's Cross Church",
        "subtitle_en": "Queen's Cross Church, Glasgow",
        "image_rel_path": "images/styles/art_nouveau_queens_cross_church.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/d/dc/"
            "Queens_Cross_Church07a.jpg"
        ),
        "year_built": "1898–1899",
        "address": "Гарскьюб-роуд, 870, Глазго G20 7EL",
        "address_en": "870 Garscube Road, Glasgow G20 7EL",
        "description": (
            "Единственная построенная церковь Чарльза Ренни Макинтоша; "
            "шпиль и асимметричный силуэт."
        ),
        "description_ru": (
            "Единственная построенная церковь Чарльза Ренни Макинтоша; "
            "шпиль и асимметричный силуэт."
        ),
        "description_en": (
            "The only church built by Charles Rennie Mackintosh; "
            "tower and asymmetrical silhouette."
        ),
    },
    {
        "slug": "art_nouveau_royal_arcade_norwich",
        "category": "art_nouveau",
        "name_ru": "Королевская аркада",
        "name_en": "Royal Arcade",
        "subtitle_en": "Royal Arcade, Norwich",
        "image_rel_path": "images/styles/art_nouveau_royal_arcade_norwich.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/d/dd/"
            "Royal_Arcade%2C_Norwich%2C_Inglaterra%2C_2022-11-19%2C_DD_32.jpg"
        ),
        "year_built": "1899",
        "address": "Джентльменс-уок, 28, Норвич NR2 1ND",
        "address_en": "28 Gentleman's Walk, Norwich NR2 1ND",
        "description": (
            "Крытая торговая галерея Джорджа Скиппера с "
            "витражами и керамикой."
        ),
        "description_ru": (
            "Крытая торговая галерея Джорджа Скиппера с "
            "витражами и керамикой."
        ),
        "description_en": (
            "George Skipper's glazed shopping arcade with "
            "stained glass and ceramics."
        ),
    },
    {
        "slug": "art_nouveau_everards_printing",
        "category": "art_nouveau",
        "name_ru": "Типография Эверарда",
        "name_en": "Everard's Printing Works",
        "subtitle_en": "Everard's Printing Works, Bristol",
        "image_rel_path": "images/styles/art_nouveau_everards_printing.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/4/47/"
            "Everard%27s_Printing_Works%2C_Bristol.jpg"
        ),
        "year_built": "1900–1901",
        "address": "Брод-стрит, 38, Бристоль BS1 2HG",
        "address_en": "38 Broad Street, Bristol BS1 2HG",
        "description": (
            "Фасад из цветной керамики Уильяма Джеймса Нитби "
            "для пивоварни Эверарда."
        ),
        "description_ru": (
            "Фасад из цветной керамики Уильяма Джеймса Нитби "
            "для пивоварни Эверарда."
        ),
        "description_en": (
            "William James Neatby's polychrome ceramic façade "
            "for Everard's brewery."
        ),
    },
    {
        "slug": "art_nouveau_turkey_cafe",
        "category": "art_nouveau",
        "name_ru": "Кафе «Индюк»",
        "name_en": "The Turkey Café",
        "subtitle_en": "The Turkey Café, Leicester",
        "image_rel_path": "images/styles/art_nouveau_turkey_cafe.jpg",
        "image_source_url": (
            "https://upload.wikimedia.org/wikipedia/commons/7/75/"
            "The_Turkey_Cafe%2C_Granby_Street_%E2%80%93_4_-_geograph.org.uk_"
            "-_8127111.jpg"
        ),
        "year_built": "1901",
        "address": "Гранби-стрит, 24, Лестер LE1 1DA",
        "address_en": "24 Granby Street, Leicester LE1 1DA",
        "description": (
            "Декоративный фасад кафе с мотивами индейки; "
            "реконструкция Артура Уонсома."
        ),
        "description_ru": (
            "Декоративный фасад кафе с мотивами индейки; "
            "реконструкция Артура Уонсома."
        ),
        "description_en": (
            "Ornamental café front with turkey motifs; "
            "restored by Arthur Wakerley."
        ),
    },
    {
        "slug": "art_nouveau_harrods_food_hall",
        "category": "art_nouveau",
        "name_ru": "Продовольственный зал Harrods",
        "name_en": "Harrods Food Hall",
        "subtitle_en": "Harrods Food Hall, London",
        "image_rel_path": "images/styles/art_nouveau_harrods_food_hall.jpg",
        "image_source_url": HARRODS_IMAGE,
        "year_built": "1901–1902",
        "address": "Бромптон-роуд, 87–135, Лондон SW1X 7XL",
        "address_en": "87–135 Brompton Road, London SW1X 7XL",
        "description": (
            "Кафе и продовольственные отделы с плиткой ар-нуво "
            "в универмаге Harrods."
        ),
        "description_ru": (
            "Кафе и продовольственные отделы с плиткой ар-нуво "
            "в универмаге Harrods."
        ),
        "description_en": (
            "Cafés and food halls with Art Nouveau tiling "
            "in Harrods department store."
        ),
    },
]

_DEDUP_NAME_KEYS: frozenset[str] = frozenset({
    norm
    for row in NEW_ROWS
    for norm in (
        _normalize_name(str(row.get("name_en") or "")),
        _normalize_name(str(row.get("name_ru") or "")),
    )
    if norm
})


def _finalize(row: dict[str, Any]) -> dict[str, Any]:
    year = str(row.get("year_built") or "")
    city_ru = str(row.get("address") or "").split(",")[-1].strip()
    city_en = str(row.get("address_en") or "").split(",")[-1].strip()
    out = dict(row)
    out.setdefault("license_note", _LICENSE)
    out.setdefault("attribution", _ATTRIBUTION)
    out.setdefault("architecture_style", _STYLE_RU)
    out.setdefault("architecture_style_en", _STYLE_EN)
    out.setdefault("history", out.get("description", ""))
    out.setdefault("history_ru", out.get("description_ru", ""))
    out.setdefault("history_en", out.get("description_en", ""))
    out.setdefault("significance", "")
    out.setdefault("significance_ru", "")
    out.setdefault("significance_en", "")
    out["facts"] = ["Период: {}.".format(year), "Город: {}.".format(city_ru)]
    out["facts_ru"] = out["facts"]
    out["facts_en"] = [
        "Period: {}.".format(year),
        "City: {}.".format(city_en),
    ]
    return out


def _is_duplicate_row(row: dict[str, Any]) -> bool:
    slug = str(row.get("slug") or "")
    if slug.startswith("art_nouveau_"):
        return False
    keys = {
        _normalize_name(str(row.get("name_en") or "")),
        _normalize_name(str(row.get("name_ru") or "")),
    }
    keys.discard("")
    return bool(keys & _DEDUP_NAME_KEYS)


def _merge_image_overrides(slugs_urls: dict[str, str]) -> None:
    text = OVERRIDES.read_text(encoding="utf-8")
    for slug, url in sorted(slugs_urls.items()):
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


def _download(rows: list[dict[str, Any]]) -> None:
    from scripts.city_guide_jerusalem_style_images import (
        _candidate_urls,
        _download_place_image,
    )

    for row in rows:
        slug = str(row.get("slug") or "")
        url = str(row.get("image_source_url") or "").strip()
        dest = GUIDE / str(row["image_rel_path"])
        if dest.is_file():
            dest.unlink(missing_ok=True)
        ordered = _candidate_urls(url, 1280)
        ok, _err = _download_place_image(
            ordered,
            dest,
            timeout_sec=60,
            retries_429=5,
            pause_429_sec=50.0,
        )
        print("  {} -> {}".format(slug, "ok" if ok else "fail"))
        time.sleep(18.0)


def _insert_chapter_rows(places: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen = {str(r.get("slug") or "") for r in places}
    to_add = [
        _finalize(row)
        for row in NEW_ROWS
        if str(row["slug"]) not in seen
    ]
    if not to_add:
        return places
    insert_at = next(
        (
            i
            for i, row in enumerate(places)
            if str(row.get("category") or "") == "art_deco"
        ),
        len(places),
    )
    return places[:insert_at] + to_add + places[insert_at:]


def main() -> int:
    places: list[dict[str, Any]] = json.loads(
        PLACES.read_text(encoding="utf-8"),
    )
    expand: list[dict[str, Any]] = json.loads(
        EXPAND.read_text(encoding="utf-8"),
    )

    before_expand = len(expand)
    expand = [r for r in expand if not _is_duplicate_row(r)]
    removed_expand = before_expand - len(expand)

    places = _insert_chapter_rows(places)
    PLACES.write_text(
        json.dumps(places, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    EXPAND.write_text(
        json.dumps(expand, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    added = [
        r for r in places
        if str(r.get("slug") or "").startswith("art_nouveau_")
    ]
    slug_urls = {
        str(r["slug"]): str(r["image_source_url"] or "")
        for r in added
        if r.get("image_source_url")
    }
    if slug_urls:
        _merge_image_overrides(slug_urls)

    print("Downloading {} images...".format(len(added)))
    _download(added)
    if removed_expand:
        print("Removed {} duplicate expand row(s)".format(removed_expand))
    print("Art Nouveau chapter: {} place(s)".format(len(added)))
    for row in added:
        print("  + {} ({})".format(row["name_en"], row["slug"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
