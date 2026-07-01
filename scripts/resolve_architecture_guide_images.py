# -*- coding: utf-8 -*-
"""Resolve images for architecture guides from city guides + Commons."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_commons_fetch import (  # noqa: E402
    commons_file_upload_url,
    commons_search_raster_title_for_city,
    configure_commons_api_throttle,
)
from scripts.city_guide_jerusalem_style_images import (  # noqa: E402
    _candidate_urls,
    _download_place_image,
)
from scripts.city_guide_second_image_sources import (  # noqa: E402
    discover_extended_second_image_urls,
)
from scripts.architecture_guide_modules import MODULES  # noqa: E402
from scripts.architecture_guide_runtime import ArchitectureGuideParts  # noqa: E402
from scripts.architecture_guide_runtime import load_parts  # noqa: E402

_RUSSIAN_EXPLICIT: dict[str, tuple[str, str]] = {
    "ancient_rus_kyiv_sophia": ("kyiv", "kyiv_saint_sophia"),
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
    "neo_russian_yaroslavsky_station": ("moscow", "moscow_railway_stations_0"),
    "art_nouveau_vitebsky_station": ("spb", "vitebsky_station"),
    "neoclassicism_early20_kyivsky_station": (
        "moscow",
        "moscow_railway_stations_3",
    ),
    "avant_garde_narkomfin": ("moscow", "moscow_osobnjaki_24"),
    "stalinist_msu_main_building": ("moscow", "moscow_landmarks_2"),
    "stalinist_vdnh_main_pavilion": ("moscow", "moscow_parks_1"),
    "regional_soviet_novosibirsk_opera": (
        "novosibirsk",
        "novosibirsk_opera_ballet",
    ),
    "contemporary_zaryadye_park": ("moscow", "moscow_landmarks_4"),
    "elizabethan_baroque_smolny_cathedral": ("spb", "smolny_cathedral"),
    "mature_classicism_admiralty": ("spb", "admiralty_spb"),
    "mature_classicism_kazan_cathedral_spb": ("spb", "kazan_cathedral"),
    "art_nouveau_singer_house": ("spb", "singer_house"),
}

_OVERRIDE_MIN_PX = 1200


def _prefer_width(parts: ArchitectureGuideParts) -> int:
    return int(getattr(parts.cfg, "image_prefer_width", 1280) or 1280)


def _explicit_map(parts: ArchitectureGuideParts) -> dict[str, tuple[str, str]]:
    if parts.cfg.slug == "russian_architecture":
        return _RUSSIAN_EXPLICIT
    return {}


def _norm_name(text: str) -> str:
    s = text.lower().strip()
    s = re.sub(r"[^\w\s]", " ", s, flags=re.UNICODE)
    return re.sub(r"\s+", " ", s).strip()


def _resolve_index(
    parts: ArchitectureGuideParts,
    project_root: Path,
) -> dict[str, dict[str, Any]]:
    index = parts.load_city_index(project_root)
    for row in index.values():
        row["name_norm"] = _norm_name(str(row.get("name_ru") or ""))
    return index


def _wikimedia_url(url: str) -> str:
    u = (url or "").strip()
    if "upload.wikimedia.org" in u.lower():
        return u
    return ""


def _is_usable_url(url: str) -> bool:
    u = (url or "").strip()
    if not u.startswith("https://"):
        return False
    if "%s" in u or u.endswith("%"):
        return False
    return True


def _city_slug_from_row(
    parts: ArchitectureGuideParts,
    row: dict[str, Any],
) -> str:
    city_hint = str(row.get("address_en") or row.get("address") or "")
    low = city_hint.lower()
    for city in parts.cfg.city_roots:
        if city.replace("_", " ") in low or city in low:
            return city
    if "Petersburg" in city_hint or "Петербург" in city_hint:
        return "spb"
    if "Kyiv" in city_hint or "Киев" in city_hint or "Київ" in city_hint:
        return "kyiv"
    if "Novosibirsk" in city_hint or "Новосибирск" in city_hint:
        return "novosibirsk"
    if parts.cfg.city_roots:
        return parts.cfg.city_roots[0]
    return "moscow"


def _search_query(row: dict[str, Any]) -> str:
    return str(row.get("subtitle_en") or row.get("name_ru") or "").strip()


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


def _clear_banned_dest(
    parts: ArchitectureGuideParts,
    guide_root: Path,
    dest_rel: str,
) -> bool:
    if not parts.has_local_image(guide_root, dest_rel):
        return False
    if not parts.local_rel_is_banned(dest_rel):
        return True
    try:
        (guide_root / dest_rel).unlink(missing_ok=True)
    except OSError:
        pass
    return False


def _city_image_usable(
    parts: ArchitectureGuideParts,
    city_row: dict[str, Any],
) -> bool:
    url = str(city_row.get("image_source_url") or "")
    rel = str(city_row.get("image_rel_path") or "")
    if parts.url_is_banned(url):
        return False
    if parts.local_rel_is_banned(rel):
        return False
    return True


def _download_commons(
    parts: ArchitectureGuideParts,
    guide_root: Path,
    row: dict[str, Any],
    url: str,
    *,
    retries_429: int = 4,
    pause_429_sec: float = 30.0,
    thumbs_only: bool = True,
    prefer_width: int | None = None,
) -> bool:
    rel = str(row.get("image_rel_path") or "")
    if not rel or not url:
        return False
    dest = guide_root / rel
    urls: list[str] = []
    if prefer_width:
        urls.extend(
            _candidate_urls(url, prefer_width, thumbs_only=True),
        )
    width = 500 if thumbs_only else None
    urls.extend(_candidate_urls(url, width, thumbs_only=thumbs_only))
    seen: set[str] = set()
    ordered: list[str] = []
    for candidate in urls:
        if candidate not in seen:
            seen.add(candidate)
            ordered.append(candidate)
    ok, _err = _download_place_image(
        ordered,
        dest,
        timeout_sec=60,
        retries_429=retries_429,
        pause_429_sec=pause_429_sec,
    )
    return ok


def _candidate_image_urls(
    parts: ArchitectureGuideParts,
    row: dict[str, Any],
    *,
    slug_city: str,
    whitelist_path: Path,
) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []

    def _add(url: str) -> None:
        u = url.strip()
        if not _is_usable_url(u) or u in seen or parts.url_is_banned(u):
            return
        seen.add(u)
        out.append(u)

    catalog_url = str(row.get("image_source_url") or "").strip()
    if _is_usable_url(catalog_url):
        _add(catalog_url)

    query = _search_query(row)
    if query:
        from scripts.city_guide_trusted_image_sources import (
            wikipedia_lead_image_urls,
        )

        for lang in ("en", "ru"):
            for u in wikipedia_lead_image_urls(query, lang=lang, max_urls=2):
                _add(u)
        city_en = slug_city.replace("_", " ").title()
        for u in discover_extended_second_image_urls(
            row,
            slug_city,
            "{} {}".format(query, city_en).strip(),
            whitelist_path=whitelist_path,
            url_is_whitelisted=parts.url_is_whitelisted,
            exclude_url=catalog_url,
            max_per_source=2,
            skip_pixabay=True,
            skip_pexels=True,
        ):
            _add(u)
    return out


def _download_first_url(
    parts: ArchitectureGuideParts,
    guide_root: Path,
    row: dict[str, Any],
    urls: list[str],
    *,
    retries_429: int,
    pause_429_sec: float,
) -> str:
    for url in urls:
        if _download_commons(
            parts,
            guide_root,
            row,
            url,
            retries_429=retries_429,
            pause_429_sec=pause_429_sec,
            thumbs_only=False,
            prefer_width=_prefer_width(parts),
        ):
            return url
    return ""


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


def _download_to_rel(
    parts: ArchitectureGuideParts,
    guide_root: Path,
    dest_rel: str,
    url: str,
    *,
    retries_429: int,
    pause_429_sec: float,
    thumbs_only: bool = True,
) -> bool:
    return _download_commons(
        parts,
        guide_root,
        {"image_rel_path": dest_rel},
        url,
        retries_429=retries_429,
        pause_429_sec=pause_429_sec,
        thumbs_only=thumbs_only,
    )


def _resolve_second_image(
    parts: ArchitectureGuideParts,
    project_root: Path,
    guide_root: Path,
    row: dict[str, Any],
    index: dict[str, dict[str, Any]],
    *,
    copy_only: bool,
    commons_delay: float,
    retries_429: int,
    pause_429_sec: float,
    whitelist_path: Path,
    stats: dict[str, int],
    city_row: dict[str, Any] | None = None,
) -> None:
    slug = str(row.get("slug") or "").strip()
    if not slug:
        return
    if slug in parts.SINGLE_IMAGE_SLUGS:
        row.pop("additional_images", None)
        return
    dest_rel = parts.extra_image_rel(slug)
    if slug in parts.IMAGE_URL_OVERRIDES:
        override = parts.IMAGE_URL_OVERRIDES[slug][1]
        if override:
            if _download_to_rel(
                parts,
                guide_root,
                dest_rel,
                override,
                retries_429=retries_429,
                pause_429_sec=pause_429_sec,
                thumbs_only=False,
            ):
                row["additional_images"] = [{
                    "image_rel_path": dest_rel,
                    "image_source_url": override,
                }]
                stats["second_downloaded"] += 1
                return
            reuse = parts.SECOND_IMAGE_REUSE.get(slug)
            if reuse:
                city, rel = reuse
                if parts.copy_city_image(
                    project_root,
                    guide_root,
                    city,
                    rel,
                    dest_rel,
                ):
                    row["additional_images"] = [{
                        "image_rel_path": dest_rel,
                        "image_source_url": str(
                            row.get("image_source_url") or "",
                        ),
                    }]
                    stats["second_copied"] += 1
                    return
            return
        row.pop("additional_images", None)
        return
    if parts.has_local_image(guide_root, dest_rel):
        return

    if city_row:
        parts.attach_additional_image_rows(row, city_row, project_root)
    else:
        parts.attach_from_city_ref(row, index, project_root)
    if parts.link_additional_images(project_root, guide_root, row):
        stats["second_copied"] += 1
        return

    if copy_only:
        return

    primary_url = str(row.get("image_source_url") or "").strip()
    slug_city = _city_slug_from_row(parts, row)
    for url in _candidate_image_urls(
        parts,
        row,
        slug_city=slug_city,
        whitelist_path=whitelist_path,
    ):
        if url == primary_url:
            continue
        if _download_to_rel(
            parts,
            guide_root,
            dest_rel,
            url,
            retries_429=retries_429,
            pause_429_sec=pause_429_sec,
        ):
            row["additional_images"] = [{
                "image_rel_path": dest_rel,
                "image_source_url": url,
            }]
            stats["second_downloaded"] += 1
            time.sleep(commons_delay)
            return

    query = _search_query(row)
    alt_url = _commons_url_for_query(
        "{} view".format(query).strip(),
        slug_city,
    )
    if alt_url and alt_url != primary_url and _download_to_rel(
        parts,
        guide_root,
        dest_rel,
        alt_url,
        retries_429=retries_429,
        pause_429_sec=pause_429_sec,
    ):
        row["additional_images"] = [{
            "image_rel_path": dest_rel,
            "image_source_url": alt_url,
        }]
        stats["second_commons"] += 1
        time.sleep(commons_delay)


def _clear_local_images_for_override(
    parts: ArchitectureGuideParts,
    guide_root: Path,
    row: dict[str, Any],
) -> None:
    slug = str(row.get("slug") or "")
    if slug not in parts.IMAGE_URL_OVERRIDES:
        return
    rel = str(row.get("image_rel_path") or "")
    if rel:
        try:
            (guide_root / rel).unlink(missing_ok=True)
        except OSError:
            pass
    second = guide_root / parts.extra_image_rel(slug)
    try:
        second.unlink(missing_ok=True)
    except OSError:
        pass


def _override_primary_too_small(
    parts: ArchitectureGuideParts,
    guide_root: Path,
    dest_rel: str,
) -> bool:
    path = guide_root / dest_rel
    if not path.is_file():
        return False
    try:
        from PIL import Image

        with Image.open(path) as im:
            w, h = im.size
        return max(w, h) < _prefer_width(parts)
    except OSError:
        return False


def _commons_only_urls(
    parts: ArchitectureGuideParts,
    row: dict[str, Any],
    slug_city: str,
) -> list[str]:
    """Collect only Wikimedia Commons URLs for a place."""
    seen: set[str] = set()
    out: list[str] = []

    def _add(url: str) -> None:
        u = _wikimedia_url(url) or (
            url.strip()
            if "upload.wikimedia.org" in url.lower()
            else ""
        )
        if not _is_usable_url(u) or u in seen or parts.url_is_banned(u):
            return
        seen.add(u)
        out.append(u)

    catalog_url = str(row.get("image_source_url") or "").strip()
    if catalog_url:
        _add(catalog_url)
    if out:
        return out
    query = _search_query(row)
    if query:
        found = _commons_url_for_query(query, slug_city)
        if found:
            _add(found)
    return out


def resolve_images(
    project_root: Path,
    parts: ArchitectureGuideParts,
    *,
    commons_delay: float = 4.0,
    copy_only: bool = False,
    commons_only: bool = False,
    retries_429: int = 5,
    pause_429_sec: float = 45.0,
    commons_api_gap: float = 2.5,
    upscale_all: bool = False,
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    from scripts.generate_architecture_guide import generate_places

    configure_commons_api_throttle(
        min_gap_sec=commons_api_gap,
        retries_429=retries_429,
        pause_429_sec=pause_429_sec,
    )
    guide_root = project_root / parts.cfg.slug
    whitelist_path = parts.default_whitelist_path()
    explicit = _explicit_map(parts)
    index = _resolve_index(parts, project_root)
    stats = {
        "copied_city": 0,
        "catalog_url": 0,
        "alt_source": 0,
        "commons_ok": 0,
        "already": 0,
        "missing": 0,
        "second_copied": 0,
        "second_downloaded": 0,
        "second_commons": 0,
        "commons_attempted": 0,
        "commons_failed": 0,
    }
    rows, _gen_stats = generate_places(project_root, parts, link_images=False)

    if upscale_all:
        for row in rows:
            rel = str(row.get("image_rel_path") or "")
            if not rel:
                continue
            try:
                (guide_root / rel).unlink(missing_ok=True)
            except OSError:
                pass

    for row in rows:
        row = parts.apply_image_url_overrides(row)
        slug = str(row.get("slug") or "")
        if slug in parts.IMAGE_URL_OVERRIDES:
            _clear_local_images_for_override(parts, guide_root, row)
        dest_rel = str(row["image_rel_path"])
        dest = guide_root / dest_rel
        primary_ok = parts.has_local_image(guide_root, dest_rel)
        if primary_ok and parts.local_rel_is_banned(dest_rel):
            try:
                dest.unlink(missing_ok=True)
            except OSError:
                pass
            primary_ok = False
        if (
            slug in parts.IMAGE_URL_OVERRIDES
            and primary_ok
            and _override_primary_too_small(parts, guide_root, dest_rel)
        ):
            try:
                dest.unlink(missing_ok=True)
            except OSError:
                pass
            primary_ok = False
        resolved_url = ""
        copied = primary_ok
        city_row: dict[str, Any] | None = None
        hint = explicit.get(slug)
        city_ref = str(row.get("_city_ref") or "").strip()
        if city_ref and ":" in city_ref:
            hint = tuple(city_ref.split(":", 1))  # type: ignore[assignment]

        if primary_ok:
            stats["already"] += 1
        else:
            url_override = slug in parts.IMAGE_URL_OVERRIDES
            if url_override:
                reuse = parts.PRIMARY_IMAGE_REUSE.get(slug)
                if reuse:
                    city, rel = reuse
                    if parts.copy_city_image(
                        project_root,
                        guide_root,
                        city,
                        rel,
                        dest_rel,
                    ):
                        resolved_url = str(row.get("image_source_url") or "")
                        copied = True
                        stats["copied_city"] += 1
                if not copied:
                    catalog_url = str(
                        row.get("image_source_url") or "",
                    ).strip()
                    if catalog_url and _download_commons(
                        parts,
                        guide_root,
                        row,
                        catalog_url,
                        retries_429=retries_429,
                        pause_429_sec=pause_429_sec,
                        thumbs_only=False,
                        prefer_width=_prefer_width(parts),
                    ):
                        resolved_url = catalog_url
                        copied = True
                        stats["catalog_url"] += 1
                        time.sleep(commons_delay)
            elif hint:
                city, place_slug = hint
                city_row = index.get("{}:{}".format(city, place_slug))
                if city_row and _city_image_usable(parts, city_row):
                    rel = str(city_row.get("image_rel_path") or "")
                    city_url = str(city_row.get("image_source_url") or "")
                    if not commons_only or _wikimedia_url(city_url):
                        if rel and parts.copy_city_image(
                            project_root,
                            guide_root,
                            city,
                            rel,
                            dest_rel,
                        ):
                            if _clear_banned_dest(parts, guide_root, dest_rel):
                                copied = True
                                stats["copied_city"] += 1
                                resolved_url = _wikimedia_url(city_url)
                            else:
                                copied = False
            if not copied and not url_override and not commons_only:
                reuse = str(row.get("_reuse_from") or "").strip()
                if reuse and "/" in reuse:
                    city = reuse.split("/", 1)[0]
                    rel = reuse.split("/", 1)[1]
                    if parts.copy_city_image(
                        project_root,
                        guide_root,
                        city,
                        rel,
                        dest_rel,
                    ):
                        if _clear_banned_dest(parts, guide_root, dest_rel):
                            copied = True
                            stats["copied_city"] += 1
                        else:
                            copied = False
            if not copied and not url_override:
                match = _match_by_name(str(row.get("name_ru") or ""), index)
                if match and match.get("image_rel_path") and _city_image_usable(
                    parts,
                    match,
                ):
                    match_url = str(match.get("image_source_url") or "")
                    if commons_only and not _wikimedia_url(match_url):
                        match = None
                if match and match.get("image_rel_path") and _city_image_usable(
                    parts,
                    match,
                ):
                    city_row = match
                    if parts.copy_city_image(
                        project_root,
                        guide_root,
                        str(match["city"]),
                        str(match["image_rel_path"]),
                        dest_rel,
                    ):
                        if _clear_banned_dest(parts, guide_root, dest_rel):
                            copied = True
                            stats["copied_city"] += 1
                            resolved_url = _wikimedia_url(
                                str(match.get("image_source_url") or ""),
                            )
                        else:
                            copied = False

            if not copied and not copy_only:
                slug_city = _city_slug_from_row(parts, row)
                if commons_only:
                    alt_urls = _commons_only_urls(parts, row, slug_city)
                    stats["commons_attempted"] += 1
                else:
                    catalog_url = str(row.get("image_source_url") or "").strip()
                    alt_urls = _candidate_image_urls(
                        parts,
                        row,
                        slug_city=slug_city,
                        whitelist_path=whitelist_path,
                    )
                if alt_urls:
                    got = _download_first_url(
                        parts,
                        guide_root,
                        row,
                        alt_urls,
                        retries_429=retries_429,
                        pause_429_sec=pause_429_sec,
                    )
                    if got:
                        resolved_url = got
                        copied = True
                        if commons_only:
                            stats["commons_ok"] += 1
                        elif got == str(row.get("image_source_url") or "").strip():
                            stats["catalog_url"] += 1
                        else:
                            stats["alt_source"] += 1
                    elif commons_only:
                        stats["commons_failed"] += 1
                    time.sleep(commons_delay)

                if not copied and not commons_only:
                    query = _search_query(row)
                    resolved_url = _commons_url_for_query(query, slug_city)
                    if resolved_url:
                        row["image_source_url"] = resolved_url
                        if _download_commons(
                            parts,
                            guide_root,
                            row,
                            resolved_url,
                            retries_429=retries_429,
                            pause_429_sec=pause_429_sec,
                            thumbs_only=False,
                            prefer_width=_prefer_width(parts),
                        ):
                            stats["commons_ok"] += 1
                            copied = True
                        time.sleep(commons_delay)

        if resolved_url:
            row["image_source_url"] = resolved_url
        if not city_row and hint:
            city_row = index.get("{}:{}".format(hint[0], hint[1]))
        if not city_row and city_ref:
            city_row = index.get(city_ref)
        if not parts.cfg.single_image_only:
            _resolve_second_image(
                parts,
                project_root,
                guide_root,
                row,
                index,
                copy_only=copy_only,
                commons_delay=commons_delay,
                retries_429=retries_429,
                pause_429_sec=pause_429_sec,
                whitelist_path=whitelist_path,
                stats=stats,
                city_row=city_row,
            )
        parts.prune_missing_additional_images(guide_root, row)
        row = parts.strip_extra_images(row)
        parts.strip_internal_image_keys(row)
        if not parts.has_local_image(guide_root, dest_rel):
            stats["missing"] += 1

    return rows, stats


def _add_module_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--module",
        choices=tuple(MODULES.keys()),
        required=True,
        help="Architecture guide package (e.g. russian_architecture).",
    )


def _run(
    mod: str,
    project_root: Path,
    *,
    commons_delay: float,
    copy_only: bool,
    commons_only: bool,
    retries_429: int,
    pause_429_sec: float,
    commons_api_gap: float,
    upscale_all: bool = False,
) -> int:
    parts = load_parts(mod)
    rows, stats = resolve_images(
        project_root,
        parts,
        commons_delay=commons_delay,
        copy_only=copy_only,
        commons_only=commons_only,
        retries_429=retries_429,
        pause_429_sec=pause_429_sec,
        commons_api_gap=commons_api_gap,
        upscale_all=upscale_all,
    )
    out = (
        project_root
        / parts.cfg.slug
        / "data"
        / parts.cfg.places_json
    )
    out.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("Wrote {} places".format(len(rows)))
    print(
        "Images: already={}, copied_city={}, catalog_url={}, "
        "alt_source={}, commons_ok={}, missing={}, "
        "commons_attempted={}, commons_failed={}, "
        "second_copied={}, second_downloaded={}, second_commons={}".format(
            stats["already"],
            stats["copied_city"],
            stats["catalog_url"],
            stats["alt_source"],
            stats["commons_ok"],
            stats["missing"],
            stats.get("commons_attempted", 0),
            stats.get("commons_failed", 0),
            stats["second_copied"],
            stats["second_downloaded"],
            stats["second_commons"],
        ),
    )
    return 0 if stats["missing"] == 0 or commons_only else 1


def main(module: str | None = None) -> int:
    if module is not None:
        return _run(
            module,
            _PROJECT_ROOT,
            commons_delay=4.0,
            copy_only=False,
            retries_429=5,
            pause_429_sec=45.0,
            commons_api_gap=2.5,
        )
    parser = argparse.ArgumentParser(
        description="Resolve architecture guide images (city reuse + Commons).",
    )
    _add_module_argument(parser)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=_PROJECT_ROOT,
    )
    parser.add_argument(
        "--commons-delay",
        type=float,
        default=4.0,
        help="Pause between remote image attempts (default 4.0s).",
    )
    parser.add_argument(
        "--commons-api-gap",
        type=float,
        default=2.5,
        help="Min gap between Commons API calls (default 2.5s).",
    )
    parser.add_argument(
        "--retries-429",
        type=int,
        default=5,
        help="429 retries per download / Commons API call (default 5).",
    )
    parser.add_argument(
        "--pause-429",
        type=float,
        default=45.0,
        help="Base sleep after HTTP 429 (default 45s).",
    )
    parser.add_argument(
        "--commons-only",
        action="store_true",
        help="Use only Wikimedia Commons URLs (no Wikipedia/Pixabay/etc.)",
    )
    parser.add_argument(
        "--copy-only",
        action="store_true",
        help="Only copy from city guides; skip remote downloads",
    )
    parser.add_argument(
        "--upscale-all",
        action="store_true",
        help="Delete existing images and re-fetch at module prefer width",
    )
    args = parser.parse_args()
    return _run(
        args.module,
        args.project_root,
        commons_delay=args.commons_delay,
        copy_only=args.copy_only,
        commons_only=args.commons_only,
        retries_429=args.retries_429,
        pause_429_sec=args.pause_429,
        commons_api_gap=args.commons_api_gap,
        upscale_all=args.upscale_all,
    )


if __name__ == "__main__":
    raise SystemExit(main())
