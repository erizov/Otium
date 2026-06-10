# -*- coding: utf-8 -*-
"""Proximity-optimized walking routes from places already in a city guide."""

from __future__ import annotations

import json
import math
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence
from urllib.parse import quote

from scripts.city_guide_front_matter import place_prominence_score
from scripts.city_guide_naming import is_pdf_filler_slug
from scripts.city_guide_narrative import place_heading_plain
from scripts.rag.city_map import names_for_slug
from scripts.rag.config import rag_paths

STOPS_ONE_DAY = 6
STOPS_PER_THREE_DAY = 5
THREE_DAY_KEYS: tuple[str, ...] = ("3d1", "3d2", "3d3")

_SENTINEL = object()

_CITY_CENTER_CACHE: dict[str, tuple[float, float]] = {}
_MAX_CITY_DISTANCE_KM = 40.0


def _city_center(city_slug: str) -> tuple[float, float] | None:
    if city_slug in _CITY_CENTER_CACHE:
        return _CITY_CENTER_CACHE[city_slug]
    names = names_for_slug(city_slug)
    queries = [
        "{}, Russia".format(names.name_en),
        names.name_en,
    ]
    if names.name_ru:
        queries.insert(0, "{}, Russia".format(names.name_ru))
    for query in queries:
        coords = _nominatim_coordinates(query, sleep_sec=0.35, city_center=None)
        if coords:
            _CITY_CENTER_CACHE[city_slug] = coords
            return coords
    return None


def _near_city(
    lat: float,
    lon: float,
    center: tuple[float, float],
    *,
    max_km: float = _MAX_CITY_DISTANCE_KM,
) -> bool:
    return haversine_km(lat, lon, center[0], center[1]) <= max_km


@dataclass(frozen=True)
class _Point:
    slug: str
    lat: float
    lon: float
    prominence: int


def route_coords_cache_path(project_root: Path, city_slug: str) -> Path:
    slug = city_slug.strip().lower()
    return project_root / slug / "data" / "{}_route_coords.json".format(slug)


def load_route_coords_cache(project_root: Path, city_slug: str) -> dict[str, dict]:
    path = route_coords_cache_path(project_root, city_slug)
    if not path.is_file():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        return {}
    out: dict[str, dict] = {}
    for slug, block in raw.items():
        if not isinstance(slug, str) or not isinstance(block, dict):
            continue
        lat, lon = block.get("lat"), block.get("lon")
        if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
            out[slug] = {"lat": float(lat), "lon": float(lon)}
    return out


def save_route_coords_cache(
    project_root: Path,
    city_slug: str,
    cache: Mapping[str, Mapping[str, float]],
) -> Path:
    path = route_coords_cache_path(project_root, city_slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(dict(cache), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in kilometres."""
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    )
    return 2 * r * math.asin(min(1.0, math.sqrt(a)))


def _valid_coord(lat: Any, lon: Any) -> tuple[float, float] | None:
    if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
        return None
    if not (-90.0 <= float(lat) <= 90.0 and -180.0 <= float(lon) <= 180.0):
        return None
    if float(lat) == 0.0 and float(lon) == 0.0:
        return None
    return float(lat), float(lon)


def _place_title_candidates(place: Mapping[str, Any], city_slug: str) -> list[str]:
    city = names_for_slug(city_slug)
    city_en = city.name_en
    city_ru = city.name_ru or city_en
    out: list[str] = []

    def add(base: str) -> None:
        base = base.strip()
        if not base or base in out:
            return
        for cand in (
            "{}, {}".format(base, city_en),
            "{} ({})".format(base, city_en),
            "{}, {}, Russia".format(base, city_en),
            "{}, {}".format(base, city_ru),
            base,
        ):
            if cand not in out:
                out.append(cand)

    add(str(place.get("name_en") or place.get("subtitle_en") or ""))
    add(str(place.get("name_ru") or place.get("name") or ""))
    return out


def _mw_coordinates(
    host: str,
    title: str,
    *,
    sleep_sec: float = 0.2,
) -> tuple[float, float] | None:
    if os.environ.get("CITY_GUIDE_NO_GEOCODE", "").strip().lower() in {
        "1",
        "true",
        "yes",
    }:
        return None
    from scripts.rag.http_cache import fetch_cached

    paths = rag_paths()
    api = "https://{}/w/api.php".format(host)
    url = (
        api
        + "?action=query&format=json&redirects=1"
        + "&prop=coordinates|pageprops&ppprop=wikibase_item"
        + "&titles={}".format(quote(title))
    )
    try:
        resp = fetch_cached(
            url,
            cache_dir=paths.http_cache_dir,
            sleep_sec=sleep_sec,
            timeout_sec=60,
        )
        blob = resp.json()
    except (OSError, ValueError, KeyError):
        return None
    pages = (blob.get("query") or {}).get("pages") or {}
    page = next(iter(pages.values()), {}) if pages else {}
    coords = page.get("coordinates") or []
    if coords:
        block = coords[0] if isinstance(coords[0], dict) else {}
        direct = _valid_coord(block.get("lat"), block.get("lon"))
        if direct:
            return direct
    pp = page.get("pageprops") or {}
    qid = str(pp.get("wikibase_item") or "").strip()
    if qid:
        wd = _wikidata_coordinates(qid, sleep_sec=sleep_sec)
        if wd:
            return wd
    return None


def _wikidata_coordinates(
    qid: str,
    *,
    sleep_sec: float = 0.2,
) -> tuple[float, float] | None:
    from scripts.rag.fetch_sources import _wikidata_entity

    entity = _wikidata_entity(
        rag_paths(),
        qid=qid,
        sleep_sec=sleep_sec,
        force=False,
    )
    if not entity:
        return None
    ent = ((entity.get("entities") or {}).get(qid) or {})
    claims = ent.get("claims") or {}
    for cl in claims.get("P625") or []:
        dv = ((cl.get("mainsnak") or {}).get("datavalue") or {})
        val = dv.get("value")
        if isinstance(val, dict):
            return _valid_coord(val.get("latitude"), val.get("longitude"))
    return None


def _nominatim_coordinates(
    query: str,
    *,
    sleep_sec: float = 0.35,
    city_center: tuple[float, float] | None = _SENTINEL,
    limit: int = 5,
) -> tuple[float, float] | None:
    if os.environ.get("CITY_GUIDE_NO_GEOCODE", "").strip().lower() in {
        "1",
        "true",
        "yes",
    }:
        return None
    from scripts.rag.config import DEFAULT_USER_AGENT
    from scripts.rag.http_cache import fetch_cached

    url = (
        "https://nominatim.openstreetmap.org/search?q="
        + quote(query)
        + "&format=json&limit={}".format(max(1, limit))
    )
    headers = {"User-Agent": DEFAULT_USER_AGENT}
    best: tuple[float, float] | None = None
    best_dist = float("inf")
    for force in (False, True):
        try:
            resp = fetch_cached(
                url,
                cache_dir=rag_paths().http_cache_dir,
                sleep_sec=sleep_sec,
                timeout_sec=60,
                headers=headers,
                force=force,
            )
            rows = resp.json()
        except (OSError, ValueError, KeyError):
            continue
        if not isinstance(rows, list):
            continue
        for row in rows:
            if not isinstance(row, dict):
                continue
            coords = _valid_coord(row.get("lat"), row.get("lon"))
            if not coords:
                continue
            if city_center is None:
                return coords
            if city_center is _SENTINEL:
                continue
            dist = haversine_km(coords[0], coords[1], city_center[0], city_center[1])
            if dist < best_dist:
                best_dist = dist
                best = coords
    if best is not None and best_dist <= _MAX_CITY_DISTANCE_KM:
        return best
    return None


def _wikipedia_search_title(query: str, *, sleep_sec: float = 0.2) -> str | None:
    from scripts.rag.http_cache import fetch_cached

    url = (
        "https://en.wikipedia.org/w/api.php?action=opensearch"
        + "&search={}&limit=1&namespace=0&format=json".format(quote(query))
    )
    try:
        resp = fetch_cached(
            url,
            cache_dir=rag_paths().http_cache_dir,
            sleep_sec=sleep_sec,
            timeout_sec=60,
        )
        blob = resp.json()
    except (OSError, ValueError, KeyError, IndexError):
        return None
    if not isinstance(blob, list) or len(blob) < 2:
        return None
    titles = blob[1]
    if isinstance(titles, list) and titles:
        return str(titles[0]).strip() or None
    return None


def resolve_place_coordinates(
    place: Mapping[str, Any],
    city_slug: str,
    cache: dict[str, dict],
    *,
    write_cache: bool = False,
    project_root: Path | None = None,
    allow_geocode: bool = True,
) -> tuple[float, float] | None:
    slug = str(place.get("slug") or "").strip()
    if not slug:
        return None
    hit = cache.get(slug)
    if hit:
        cached = _valid_coord(hit.get("lat"), hit.get("lon"))
        if cached:
            if allow_geocode:
                center = _city_center(city_slug)
                if center is None or _near_city(cached[0], cached[1], center):
                    return cached
            else:
                return cached

    direct = _valid_coord(place.get("lat"), place.get("lon"))
    if direct:
        if allow_geocode:
            center = _city_center(city_slug)
            if center is None or _near_city(direct[0], direct[1], center):
                cache[slug] = {"lat": direct[0], "lon": direct[1]}
                if write_cache and project_root is not None:
                    save_route_coords_cache(project_root, city_slug, cache)
                return direct
        else:
            return direct

    if not allow_geocode:
        return None

    center = _city_center(city_slug)
    candidates = _place_title_candidates(place, city_slug)

    for query in candidates:
        coords = _nominatim_coordinates(query, city_center=center)
        if coords:
            cache[slug] = {"lat": coords[0], "lon": coords[1]}
            if write_cache and project_root is not None:
                save_route_coords_cache(project_root, city_slug, cache)
            return coords

    for host in ("en.wikipedia.org", "ru.wikipedia.org"):
        for title in candidates:
            coords = _mw_coordinates(host, title)
            if coords:
                cache[slug] = {"lat": coords[0], "lon": coords[1]}
                if write_cache and project_root is not None:
                    save_route_coords_cache(project_root, city_slug, cache)
                return coords

    if candidates:
        search_title = _wikipedia_search_title(candidates[0])
        if search_title:
            coords = _mw_coordinates("en.wikipedia.org", search_title)
            if coords:
                cache[slug] = {"lat": coords[0], "lon": coords[1]}
                if write_cache and project_root is not None:
                    save_route_coords_cache(project_root, city_slug, cache)
                return coords

    return None


def _to_points(
    places: Sequence[Mapping[str, Any]],
    edition: str,
    city_slug: str,
    cache: dict[str, dict],
    *,
    project_root: Path | None,
    write_cache: bool,
    allow_geocode: bool,
) -> list[_Point]:
    out: list[_Point] = []
    for place in places:
        slug = str(place.get("slug") or "")
        if not slug or is_pdf_filler_slug(slug):
            continue
        score = place_prominence_score(place, edition)
        if score < 0:
            continue
        coords = resolve_place_coordinates(
            place,
            city_slug,
            cache,
            write_cache=write_cache,
            project_root=project_root,
            allow_geocode=allow_geocode,
        )
        if not coords:
            continue
        lat, lon = coords
        out.append(_Point(slug=slug, lat=lat, lon=lon, prominence=score))
    return out


def nearest_neighbor_route(
    points: Sequence[_Point],
    *,
    limit: int,
    start_slug: str | None = None,
) -> list[_Point]:
    """Greedy nearest-neighbour walk, starting from the seed place."""
    if not points or limit <= 0:
        return []
    pool = list(points)
    if start_slug:
        seed_idx = next(
            (i for i, p in enumerate(pool) if p.slug == start_slug),
            0,
        )
    else:
        seed_idx = max(range(len(pool)), key=lambda i: pool[i].prominence)
    route: list[_Point] = [pool.pop(seed_idx)]
    while pool and len(route) < limit:
        last = route[-1]
        nxt_idx = min(
            range(len(pool)),
            key=lambda i: haversine_km(last.lat, last.lon, pool[i].lat, pool[i].lon),
        )
        route.append(pool.pop(nxt_idx))
    return route


def _k_means(
    points: Sequence[_Point],
    k: int,
    *,
    max_iter: int = 24,
) -> list[list[_Point]]:
    if k <= 0 or not points:
        return []
    if len(points) <= k:
        return [[p] for p in points] + [[] for _ in range(k - len(points))]

    ordered = sorted(points, key=lambda p: (-p.prominence, p.slug))
    step = max(1, len(ordered) // k)
    centroids = [ordered[i * step] for i in range(k)]
    clusters: list[list[_Point]] = [[] for _ in range(k)]

    for _ in range(max_iter):
        clusters = [[] for _ in range(k)]
        for pt in points:
            idx = min(
                range(k),
                key=lambda i: haversine_km(
                    pt.lat,
                    pt.lon,
                    centroids[i].lat,
                    centroids[i].lon,
                ),
            )
            clusters[idx].append(pt)
        moved = False
        for i in range(k):
            if not clusters[i]:
                continue
            lat = sum(p.lat for p in clusters[i]) / len(clusters[i])
            lon = sum(p.lon for p in clusters[i]) / len(clusters[i])
            if abs(lat - centroids[i].lat) > 1e-6 or abs(lon - centroids[i].lon) > 1e-6:
                moved = True
            centroids[i] = _Point(
                slug=centroids[i].slug,
                lat=lat,
                lon=lon,
                prominence=centroids[i].prominence,
            )
        if not moved:
            break

    clusters = [c for c in clusters if c]
    clusters.sort(
        key=lambda cluster: (
            -max(p.prominence for p in cluster),
            min(p.slug for p in cluster),
        ),
    )
    return clusters


def _default_minutes(prominence: int) -> int:
    if prominence >= 10:
        return 75
    if prominence >= 6:
        return 60
    return 45


def _stop_dict(point: _Point) -> dict[str, Any]:
    return {
        "slug": point.slug,
        "minutes": _default_minutes(point.prominence),
    }


def _prominence_fallback_route(
    places: Sequence[Mapping[str, Any]],
    edition: str,
    *,
    limit: int,
) -> list[dict[str, Any]]:
    ranked = sorted(
        (
            p
            for p in places
            if not is_pdf_filler_slug(str(p.get("slug") or ""))
            and place_prominence_score(p, edition) >= 0
        ),
        key=lambda p: (
            -place_prominence_score(p, edition),
            str(p.get("slug") or ""),
        ),
    )
    out: list[dict[str, Any]] = []
    for place in ranked[:limit]:
        slug = str(place.get("slug") or "")
        score = place_prominence_score(place, edition)
        out.append({"slug": slug, "minutes": _default_minutes(score)})
    return out


def _fill_stops(
    stops: list[dict[str, Any]],
    places: Sequence[Mapping[str, Any]],
    edition: str,
    *,
    limit: int,
    exclude: set[str] | None = None,
) -> list[dict[str, Any]]:
    blocked = set(exclude or ())
    used = {str(s.get("slug") or "") for s in stops} | blocked
    merged = [s for s in stops if str(s.get("slug") or "") not in blocked]
    for stop in _prominence_fallback_route(places, edition, limit=limit * 3):
        slug = str(stop.get("slug") or "")
        if not slug or slug in used:
            continue
        merged.append(stop)
        used.add(slug)
        if len(merged) >= limit:
            break
    return merged[:limit]


def build_proximity_itineraries(
    places: Sequence[Mapping[str, Any]],
    city_slug: str,
    edition: str,
    *,
    project_root: Path | None = None,
    write_cache: bool = False,
    allow_geocode: bool = False,
) -> dict[str, dict[str, Any]]:
    """
    Build ``1d`` and ``3d1``/``3d2``/``3d3`` plans from guide places.

    Uses nearest-neighbour ordering when coordinates are available; falls
    back to prominence order otherwise.
    """
    cache: dict[str, dict] = {}
    if project_root is not None:
        cache = load_route_coords_cache(project_root, city_slug)

    points = _to_points(
        places,
        edition,
        city_slug,
        cache,
        project_root=project_root,
        write_cache=write_cache,
        allow_geocode=allow_geocode,
    )

    titles_en = {
        "1d": "One day",
        "3d1": "Three days — day 1",
        "3d2": "Three days — day 2",
        "3d3": "Three days — day 3",
    }
    titles_ru = {
        "1d": "Один день",
        "3d1": "Три дня — день 1",
        "3d2": "Три дня — день 2",
        "3d3": "Три дня — день 3",
    }
    intros_en = {
        "1d": (
            "A compact loop linking the strongest cards in this guide, "
            "ordered to minimise backtracking on foot."
        ),
        "3d1": "Day 1 — central cluster.",
        "3d2": "Day 2 — next neighbourhood group.",
        "3d3": "Day 3 — remaining highlights nearby.",
    }
    intros_ru = {
        "1d": (
            "Компактный маршрут по главным точкам путеводителя с "
            "минимальным возвратом назад пешком."
        ),
        "3d1": "День 1 — центральный кластер.",
        "3d2": "День 2 — следующая группа районов.",
        "3d3": "День 3 — оставшиеся близкие объекты.",
    }
    titles = titles_ru if edition == "ru" else titles_en
    intros = intros_ru if edition == "ru" else intros_en

    out: dict[str, dict[str, Any]] = {}
    used_slugs: set[str] = set()

    if len(points) >= 2:
        one_day = nearest_neighbor_route(points, limit=STOPS_ONE_DAY)
        if one_day:
            stops = _fill_stops(
                [_stop_dict(p) for p in one_day],
                places,
                edition,
                limit=STOPS_ONE_DAY,
            )
            used_slugs.update(str(s.get("slug") or "") for s in stops)
            out["1d"] = {
                "title": titles["1d"],
                "intro": intros["1d"],
                "stops": stops,
            }

        clusters = _k_means(points, len(THREE_DAY_KEYS))
        for key, cluster in zip(THREE_DAY_KEYS, clusters):
            if not cluster:
                continue
            seed = max(cluster, key=lambda p: p.prominence).slug
            day_route = nearest_neighbor_route(
                cluster,
                limit=STOPS_PER_THREE_DAY,
                start_slug=seed,
            )
            if day_route:
                stops = _fill_stops(
                    [_stop_dict(p) for p in day_route],
                    places,
                    edition,
                    limit=STOPS_PER_THREE_DAY,
                    exclude=used_slugs,
                )
                used_slugs.update(str(s.get("slug") or "") for s in stops)
                out[key] = {
                    "title": titles[key],
                    "intro": intros[key],
                    "stops": stops,
                }
        if len(out) < len(THREE_DAY_KEYS) + int("1d" in out):
            pool = _prominence_fallback_route(
                places,
                edition,
                limit=STOPS_PER_THREE_DAY * len(THREE_DAY_KEYS) * 2,
            )
            for idx, key in enumerate(THREE_DAY_KEYS):
                if key in out:
                    continue
                chunk = [
                    s
                    for s in pool
                    if str(s.get("slug") or "") not in used_slugs
                ][:STOPS_PER_THREE_DAY]
                if chunk:
                    used_slugs.update(str(s.get("slug") or "") for s in chunk)
                    out[key] = {
                        "title": titles[key],
                        "intro": intros[key],
                        "stops": chunk,
                    }
    else:
        one_day = _prominence_fallback_route(
            places,
            edition,
            limit=STOPS_ONE_DAY,
        )
        if one_day:
            used_slugs.update(str(s.get("slug") or "") for s in one_day)
            out["1d"] = {
                "title": titles["1d"],
                "intro": intros["1d"],
                "stops": one_day,
            }
        pool = [
            s
            for s in _prominence_fallback_route(
                places,
                edition,
                limit=STOPS_PER_THREE_DAY * len(THREE_DAY_KEYS) * 2,
            )
            if str(s.get("slug") or "") not in used_slugs
        ]
        for key in THREE_DAY_KEYS:
            chunk = pool[:STOPS_PER_THREE_DAY]
            if not chunk:
                break
            pool = pool[STOPS_PER_THREE_DAY:]
            used_slugs.update(str(s.get("slug") or "") for s in chunk)
            out[key] = {
                "title": titles[key],
                "intro": intros[key],
                "stops": chunk,
            }

    return out


def proximity_itineraries_for_edition(
    places: Sequence[Mapping[str, Any]],
    city_slug: str,
    edition: str,
    *,
    project_root: Path | None,
) -> dict[str, Any]:
    """Edition block for ``itineraries`` front-matter JSON shape."""
    return build_proximity_itineraries(
        places,
        city_slug,
        edition,
        project_root=project_root,
        write_cache=False,
        allow_geocode=False,
    )
