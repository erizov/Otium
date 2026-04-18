# -*- coding: utf-8 -*-
"""Merge scripts/city_place_extensions.json into each city *_places.json."""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_EXTENSIONS_PATH = Path(__file__).resolve().parent / "city_place_extensions.json"
_USER_AGENT = "ExcursionGuide/1.0 (extend_new_city_guides_to_12.py)"
# Per-city target for *this* merge-only script (extensions file caps near 12).
# Use ``scripts/grow_city_guides_to_25.py`` to reach 25+ with Commons search.
_MIN_MERGE_TARGET = 12

if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

_CITIES: tuple[str, ...] = (
    "amsterdam",
    "athens",
    "bangkok",
    "copenhagen",
    "dubai",
    "dublin",
    "istanbul",
    "lisbon",
    "london",
    "los_angeles",
    "san_francisco",
    "singapore",
    "tokyo",
    "vatican",
)


def _batch_commons_urls(
    titles: list[str],
    *,
    pause_sec: float,
) -> dict[str, str]:
    """Map commons filename -> upload URL (batched MediaWiki query)."""
    if not titles:
        return {}
    pipe = "|".join(
        ("File:" + t) if not t.startswith("File:") else t
        for t in titles
    )
    q = urllib.parse.urlencode(
        {
            "action": "query",
            "titles": pipe,
            "prop": "imageinfo",
            "iiprop": "url",
            "format": "json",
        },
    )
    url = "https://commons.wikimedia.org/w/api.php?" + q
    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    wait = 6.0
    data: dict[str, Any] | None = None
    for attempt in range(12):
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            print(
                "  429 batch: sleep {:.0f}s ({}/12)".format(wait, attempt + 1),
                file=sys.stderr,
            )
            time.sleep(wait)
            wait = min(wait * 1.5, 180.0)
    if data is None:
        raise SystemExit("Commons batch query failed (rate limit)")
    by_title: dict[str, str] = {}
    for page in data["query"]["pages"].values():
        t = page.get("title", "")
        if t.startswith("File:"):
            t = t[5:]
        if "imageinfo" not in page:
            continue
        by_title[t] = str(page["imageinfo"][0]["url"])
    out: dict[str, str] = {}
    for want in titles:
        if want in by_title:
            out[want] = by_title[want]
            continue
        low = want.casefold()
        hit = None
        for got, u in by_title.items():
            if got.casefold() == low:
                hit = u
                break
        if hit is None:
            raise SystemExit(
                "Missing imageinfo for {!r} (got {!r})".format(
                    want,
                    sorted(by_title),
                ),
            )
        out[want] = hit
    time.sleep(max(0.0, pause_sec))
    return out


def _finalize_row(
    partial: dict[str, Any],
    *,
    url_map: dict[str, str],
) -> dict[str, Any]:
    slug = partial["slug"]
    cf = partial.get("commons_file")
    cached = partial.get("image_source_url")
    if cached:
        src = str(cached)
    elif cf:
        src = url_map.get(cf)
    else:
        src = None
    if not src:
        raise SystemExit(
            "Missing image URL for {} (commons_file={!r})".format(slug, cf),
        )
    row = {k: v for k, v in partial.items() if k not in ("commons_file",)}
    row["image_source_url"] = src
    row["image_rel_path"] = "images/{}.jpg".format(slug)
    row["license_note"] = "See Wikimedia Commons file page for license."
    row["attribution"] = "Wikimedia Commons contributors"
    return row


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Append extension places from city_place_extensions.json.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=6,
        help="titles per Commons API batch (default 6)",
    )
    parser.add_argument(
        "--batch-pause-sec",
        type=float,
        default=4.0,
        help="sleep after each successful batch (default 4)",
    )
    args = parser.parse_args()

    ext: dict[str, list[dict[str, Any]]] = json.loads(
        _EXTENSIONS_PATH.read_text(encoding="utf-8"),
    )

    needed_files: list[str] = []
    work: list[tuple[str, Path, list[dict[str, Any]], list[dict[str, Any]]]] = []
    for slug in _CITIES:
        path = _PROJECT_ROOT / slug / "data" / "{}_places.json".format(slug)
        rows = json.loads(path.read_text(encoding="utf-8"))
        if len(rows) >= _MIN_MERGE_TARGET:
            print(slug, "skip (already", len(rows), "places)")
            continue
        extras = ext.get(slug)
        if not extras:
            raise SystemExit("No extensions defined for {}".format(slug))
        for raw in extras:
            cf = raw.get("commons_file")
            if cf and cf not in needed_files:
                needed_files.append(cf)
        work.append((slug, path, rows, extras))

    url_map: dict[str, str] = {}
    for i in range(0, len(needed_files), args.batch_size):
        batch = needed_files[i : i + args.batch_size]
        url_map.update(
            _batch_commons_urls(batch, pause_sec=args.batch_pause_sec),
        )

    for slug, path, rows, extras in work:
        have = {r["slug"] for r in rows}
        for raw in extras:
            fin = _finalize_row(dict(raw), url_map=url_map)
            if fin["slug"] in have:
                continue
            rows.append(fin)
            have.add(fin["slug"])
        if len(rows) < _MIN_MERGE_TARGET:
            raise SystemExit(
                "{} still has only {} places (need {})".format(
                    slug, len(rows), _MIN_MERGE_TARGET,
                ),
            )
        path.write_text(
            json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(slug, "->", len(rows), "places")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
