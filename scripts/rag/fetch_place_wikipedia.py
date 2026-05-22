# -*- coding: utf-8 -*-
"""Fetch per-place Wikipedia pages into the local RAG cache.

This fills the gap between city-level sources (city overview pages) and the
guide's per-place fields.

It is conservative:
- only fetches pages for places that are missing content fields
- stores provenance in RAG docs (never in PDF-facing fields)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote


_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.rag.city_map import names_for_slug
from scripts.rag.config import rag_paths
from scripts.rag.doc_schema import doc_to_dict
from scripts.rag.doc_schema import RagDocument
from scripts.rag.http_cache import fetch_cached
from webapp.server.city_store import load_city_places


def _utc_now() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _place_title(place: dict[str, Any], lang: str) -> str:
    if lang == "ru":
        return str(place.get("name_ru") or "").strip()
    return str(place.get("name_en") or place.get("subtitle_en") or "").strip()


def _needs_any_field(place: dict[str, Any]) -> bool:
    for k in ("description", "history", "significance"):
        if not str(place.get(k) or "").strip():
            return True
    facts = place.get("facts")
    if not isinstance(facts, list) or not facts:
        return True
    return False


def _wikipedia_extract(host: str, title: str) -> tuple[str, str]:
    """
    Return (final_url, plain_text_extract).

    Uses MediaWiki API with redirects enabled.
    """
    api = f"https://{host}/w/api.php"
    url = (
        api
        + "?action=query&format=json&redirects=1&prop=extracts&explaintext=1"
        + "&exsectionformat=plain&titles="
        + quote(title)
    )
    paths = rag_paths(_PROJECT_ROOT)
    res = fetch_cached(url, cache_dir=paths.http_cache_dir)
    data = json.loads(res.body.decode("utf-8", errors="replace"))
    pages = (((data or {}).get("query") or {}).get("pages") or {})
    page = None
    for _, p in pages.items():
        if isinstance(p, dict):
            page = p
            break
    if not page:
        return url, ""
    if "missing" in page:
        return url, ""
    text = str(page.get("extract") or "").strip()
    # Best-effort canonical page URL.
    page_title = str(page.get("title") or title).replace(" ", "_")
    final = f"https://{host}/wiki/{quote(page_title)}"
    return final, text


def fetch_city_places(
    project_root: Path,
    *,
    city_slug: str,
    lang: str,
    max_places: int | None,
) -> int:
    if lang not in {"ru", "en"}:
        raise ValueError("lang must be ru or en")
    places = load_city_places(project_root, city_slug)
    if not places:
        return 0
    host = "ru.wikipedia.org" if lang == "ru" else "en.wikipedia.org"
    paths = rag_paths(project_root)
    written = 0
    scanned = 0
    for place in places:
        if max_places is not None and scanned >= max_places:
            break
        scanned += 1
        if not _needs_any_field(place):
            continue
        title = _place_title(place, lang)
        if not title:
            continue
        # Skip very generic titles.
        if len(title) < 3:
            continue

        final_url, extract = _wikipedia_extract(host, title)
        if not extract or len(extract) < 200:
            continue

        doc_id = _sha256(final_url + "\n" + city_slug + "\n" + lang)
        doc = RagDocument(
            doc_id=doc_id,
            city_slug=city_slug,
            language=lang,
            source_name="wikipedia",
            source_url=final_url,
            license="CC BY-SA (see Wikipedia page)",
            retrieved_at_utc=_utc_now(),
            title=title,
            text=extract,
            extra={
                "city_hint": getattr(names_for_slug(city_slug), f"name_{lang}") or "",
                "place": title,
                "kind": "place_page",
            },
        )
        out_dir = paths.docs_dir / city_slug / title[:80].replace("/", "_")
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"wikipedia_place_{lang}_{doc_id[:12]}.json"
        out_path.write_text(
            json.dumps(doc_to_dict(doc), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        written += 1
    print(f"Fetched place pages: {written} (scanned {scanned})")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=None)
    parser.add_argument("--city", required=True)
    parser.add_argument("--lang", choices=("ru", "en"), default="ru")
    parser.add_argument("--max-places", type=int, default=200)
    args = parser.parse_args()
    root = (
        args.project_root.resolve()
        if args.project_root
        else Path(__file__).resolve().parent.parent.parent
    )
    max_places = int(args.max_places) if args.max_places else None
    return fetch_city_places(
        root,
        city_slug=str(args.city).strip(),
        lang=str(args.lang),
        max_places=max_places,
    )


if __name__ == "__main__":
    raise SystemExit(main())

