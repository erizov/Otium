# -*- coding: utf-8 -*-
"""Resolve images for Russian Architecture guide from city guides + Commons."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import time
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from russian_arhitecture.data.style_catalog import (  # noqa: E402
    STYLE_EXAMPLES,
    STYLE_ORDER,
)
from scripts.city_guide_commons_fetch import (  # noqa: E402
    commons_file_upload_url,
    commons_search_raster_title_for_city,
)
from scripts.city_guide_jerusalem_style_images import (  # noqa: E402
    _candidate_urls,
    _download_place_image,
)

MIN_IMAGE_BYTES = 500
_CITY_ROOTS = (
    "moscow",
    "spb",
    "kyiv",
    "novosibirsk",
    "vladimir",
    "pskov",
    "novgorod",
)

# (city_folder, place_slug) for reliable reuse
_EXPLICIT: dict[str, tuple[str, str]] = {
    "ancient_rus_kyiv_sophia": ("kyiv", "kyiv_saint_sophia"),
    "moscow_fifteenth_sixteenth_kremlin_dormition": (
        "moscow",
        "moscow_places_of_worship_4",
    ),
    "moscow_fifteenth_sixteenth_kremlin_archangel": (
        "moscow",
        "moscow_places_of_worship_5",
    ),
    "tent_roof_st_basil": ("moscow", "moscow_places_of_worship_1"),
    "tent_roof_ascension_kolomenskoye": (
        "moscow",
        "moscow_places_of_worship_2",
    ),
    "naryshkin_baroque_intercession_fili": (
        "moscow",
        "moscow_places_of_worship_28",
    ),
    "elizabethan_baroque_winter_palace": ("spb", "winter_palace"),
    "mature_classicism_tauride_palace": ("spb", "tauride_palace"),
    "empire_isaac_cathedral": ("spb", "isaac_cathedral"),
    "pseudo_russian_savior_on_blood": ("spb", "savior_on_blood"),
    "russo_byzantine_christ_savior": ("moscow", "moscow_places_of_worship_0"),
    "russo_byzantine_armoury": ("moscow", "moscow_museums_3"),
    "eclecticism_historical_museum": ("moscow", "moscow_museums_0"),
    "eclecticism_polytechnic_museum": ("moscow", "moscow_museums_5"),
    "art_nouveau_ryabushinsky_mansion": ("moscow", "moscow_palaces_17"),
    "regional_soviet_luzhniki_stadium": ("moscow", "moscow_landmarks_8"),
    "neo_russian_feodorovsky_cathedral": (
        "spb",
        "spb_feodorovsky_cathedral_spb",
    ),
    "petrine_baroque_peter_paul_cathedral": ("spb", "peter_paul_fortress"),
    "pseudo_russian_gum": ("moscow", "moscow_buildings_1"),
    "neo_russian_yaroslavsky_station": ("moscow", "moscow_railway_stations_0"),
    "art_nouveau_vitebsky_station": ("spb", "vitebsky_station"),
    "neoclassicism_early20_kyivsky_station": (
        "moscow",
        "moscow_railway_stations_3",
    ),
    "avant_garde_narkomfin": ("moscow", "moscow_osobnjaki_24"),
    "stalinist_msu_main_building": ("moscow", "moscow_landmarks_2"),
    "stalinist_vdnh_main_pavilion": ("moscow", "moscow_parks_1"),
    "soviet_modernism_ostankino_tower": ("moscow", "moscow_landmarks_1"),
    "regional_soviet_novosibirsk_opera": (
        "novosibirsk",
        "novosibirsk_opera_ballet",
    ),
    "contemporary_moscow_city": ("moscow", "moscow_landmarks_0"),
    "contemporary_zaryadye_park": ("moscow", "moscow_landmarks_4"),
    "elizabethan_baroque_smolny_cathedral": ("spb", "smolny_cathedral"),
    "mature_classicism_admiralty": ("spb", "admiralty_spb"),
    "mature_classicism_kazan_cathedral_spb": ("spb", "kazan_cathedral"),
    "art_nouveau_singer_house": ("spb", "singer_house"),
}


def _norm_name(text: str) -> str:
    s = text.lower().strip()
    s = re.sub(r"[^\w\s]", " ", s, flags=re.UNICODE)
    return re.sub(r"\s+", " ", s).strip()


def _load_city_index(project_root: Path) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for city in _CITY_ROOTS:
        data_dir = project_root / city / "data"
        if not data_dir.is_dir():
            continue
        for path in sorted(data_dir.glob("*places*.json")):
            try:
                rows = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            if not isinstance(rows, list):
                continue
            for row in rows:
                if not isinstance(row, dict):
                    continue
                slug = str(row.get("slug") or "").strip()
                if not slug:
                    continue
                index["{}:{}".format(city, slug)] = {
                    "city": city,
                    "slug": slug,
                    "name_ru": str(row.get("name_ru") or ""),
                    "name_norm": _norm_name(str(row.get("name_ru") or "")),
                    "image_rel_path": str(row.get("image_rel_path") or ""),
                    "image_source_url": str(row.get("image_source_url") or ""),
                }
    return index


def _wikimedia_url(url: str) -> str:
    u = (url or "").strip()
    if "upload.wikimedia.org" in u.lower():
        return u
    return ""


def _copy_city_image(
    project_root: Path,
    guide_root: Path,
    city: str,
    rel: str,
    dest_rel: str,
) -> bool:
    src = project_root / city / rel
    dest = guide_root / dest_rel
    if not src.is_file() or src.stat().st_size < MIN_IMAGE_BYTES:
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.is_file() and dest.stat().st_size >= MIN_IMAGE_BYTES:
        return True
    shutil.copy2(src, dest)
    return dest.is_file() and dest.stat().st_size >= MIN_IMAGE_BYTES


def _match_by_name(
    name_ru: str,
    index: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    target = _norm_name(name_ru)
    if not target:
        return None
    best: dict[str, Any] | None = None
    best_len = 0
    for row in index.values():
        cand = row["name_norm"]
        if not cand:
            continue
        if target in cand or cand in target:
            overlap = min(len(target), len(cand))
            if overlap > best_len:
                best = row
                best_len = overlap
    return best


def _download_commons(
    guide_root: Path,
    row: dict[str, Any],
    url: str,
) -> bool:
    rel = str(row.get("image_rel_path") or "")
    if not rel or not url:
        return False
    dest = guide_root / rel
    urls = _candidate_urls(url, 500, thumbs_only=True)
    ok, _err = _download_place_image(
        urls,
        dest,
        timeout_sec=60,
        retries_429=4,
        pause_429_sec=30.0,
    )
    return ok


def _commons_url_for_query(query: str, city_hint: str) -> str:
    title = commons_search_raster_title_for_city(
        query,
        city_hint or "moscow",
        srlimit=8,
    )
    if not title:
        return ""
    url = commons_file_upload_url(title)
    return url or ""


def resolve_images(
    project_root: Path,
    *,
    commons_delay: float = 1.5,
    copy_only: bool = False,
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    from scripts.generate_russian_arhitecture_guide import (  # noqa: E402
        _place_row,
        _slug,
        _image_rel,
    )

    guide_root = project_root / "russian_arhitecture"
    index = _load_city_index(project_root)
    stats = {
        "copied_city": 0,
        "commons_ok": 0,
        "already": 0,
        "missing": 0,
    }
    rows: list[dict[str, Any]] = []

    for style_key in STYLE_ORDER:
        for ex in STYLE_EXAMPLES.get(style_key, []):
            row = _place_row(style_key, ex)
            slug = row["slug"]
            dest_rel = row["image_rel_path"]
            dest = guide_root / dest_rel
            if dest.is_file() and dest.stat().st_size >= MIN_IMAGE_BYTES:
                stats["already"] += 1
                rows.append(row)
                continue

            resolved_url = ""
            copied = False
            hint = _EXPLICIT.get(slug)
            if hint:
                city, place_slug = hint
                src_row = index.get("{}:{}".format(city, place_slug))
                if src_row:
                    rel = src_row["image_rel_path"]
                    if rel and _copy_city_image(
                        project_root,
                        guide_root,
                        city,
                        rel,
                        dest_rel,
                    ):
                        copied = True
                        stats["copied_city"] += 1
                        resolved_url = _wikimedia_url(src_row["image_source_url"])
            if not copied:
                reuse = str(ex.get("reuse_from") or "").strip()
                if reuse and "/" in reuse:
                    city = reuse.split("/", 1)[0]
                    rel = reuse.split("/", 1)[1]
                    if _copy_city_image(
                        project_root,
                        guide_root,
                        city,
                        rel,
                        dest_rel,
                    ):
                        copied = True
                        stats["copied_city"] += 1
            if not copied:
                match = _match_by_name(str(ex.get("name_ru") or ""), index)
                if match and match["image_rel_path"]:
                    if _copy_city_image(
                        project_root,
                        guide_root,
                        match["city"],
                        match["image_rel_path"],
                        dest_rel,
                    ):
                        copied = True
                        stats["copied_city"] += 1
                        resolved_url = _wikimedia_url(match["image_source_url"])

            if not copied and not copy_only:
                city_hint = str(ex.get("city_en") or ex.get("city_ru") or "")
                if "Petersburg" in city_hint or "Петербург" in city_hint:
                    slug_city = "spb"
                elif "Kyiv" in city_hint or "Киев" in city_hint:
                    slug_city = "kyiv"
                elif "Novosibirsk" in city_hint:
                    slug_city = "novosibirsk"
                else:
                    slug_city = "moscow"
                query = str(ex.get("name_en") or ex.get("name_ru") or "")
                resolved_url = _commons_url_for_query(query, slug_city)
                if resolved_url:
                    row["image_source_url"] = resolved_url
                    if _download_commons(guide_root, row, resolved_url):
                        stats["commons_ok"] += 1
                        copied = True
                    time.sleep(commons_delay)

            if resolved_url:
                row["image_source_url"] = resolved_url
            if copied or (dest.is_file() and dest.stat().st_size >= MIN_IMAGE_BYTES):
                rows.append(row)
            else:
                stats["missing"] += 1
                rows.append(row)

    return rows, stats


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Resolve Russian Architecture images (city reuse + Commons).",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=_PROJECT_ROOT,
    )
    parser.add_argument(
        "--commons-delay",
        type=float,
        default=1.5,
    )
    parser.add_argument(
        "--copy-only",
        action="store_true",
        help="Only copy from city guides; skip Commons API",
    )
    args = parser.parse_args()
    rows, stats = resolve_images(
        args.project_root,
        commons_delay=args.commons_delay,
        copy_only=args.copy_only,
    )
    out = (
        args.project_root
        / "russian_arhitecture"
        / "data"
        / "russian_arhitecture_places.json"
    )
    out.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("Wrote {} places".format(len(rows)))
    print(
        "Images: already={}, copied_city={}, commons_ok={}, missing={}".format(
            stats["already"],
            stats["copied_city"],
            stats["commons_ok"],
            stats["missing"],
        ),
    )
    return 0 if stats["missing"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
