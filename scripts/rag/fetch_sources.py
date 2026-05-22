# -*- coding: utf-8 -*-
"""Fetch Tier-A sources into the local RAG document cache."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.rag.city_map import names_for_slug
from scripts.rag.config import RagPaths
from scripts.rag.config import rag_paths
from scripts.rag.doc_schema import RagDocument
from scripts.rag.doc_schema import doc_to_dict
from scripts.rag.http_cache import fetch_cached
from scripts.city_guide_sources import fact_source_prefixes
from scripts.rebuild_stale_city_guide_pdfs import _discover_slugs

_WIKI_LICENSE = "CC BY-SA"
_WIKIDATA_LICENSE = "CC0"


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _doc_id(*parts: str) -> str:
    raw = "|".join(parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _write_doc(paths: RagPaths, doc: RagDocument) -> None:
    city_dir = paths.docs_dir / doc.city_slug
    city_dir.mkdir(parents=True, exist_ok=True)
    out = city_dir / "{}_{}_{}.json".format(
        doc.source_name,
        doc.language,
        doc.doc_id[:12],
    )
    out.write_text(
        json.dumps(doc_to_dict(doc), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _mw_extract(
    paths: RagPaths,
    *,
    host: str,
    language: str,
    title: str,
    sleep_sec: float,
    force: bool,
) -> tuple[str, str, dict[str, Any]]:
    """
    Return (canonical_url, plaintext, extra).

    Uses MediaWiki API extracts (plaintext).
    """
    api = "https://{}/w/api.php".format(host)
    url = (
        api
        + "?action=query&format=json&redirects=1&prop=extracts|pageprops"
        + "&explaintext=1&exsectionformat=plain&exlimit=1&ppprop=wikibase_item"
        + "&titles={}".format(quote(title))
    )
    resp = fetch_cached(
        url,
        cache_dir=paths.http_cache_dir,
        sleep_sec=sleep_sec,
        force=force,
        timeout_sec=90,
    )
    blob = resp.json()
    pages = (blob.get("query") or {}).get("pages") or {}
    page = next(iter(pages.values()), {}) if pages else {}
    extract = str(page.get("extract") or "").strip()
    page_title = str(page.get("title") or title).strip()
    canonical = "https://{}/wiki/{}".format(host, quote(page_title.replace(" ", "_")))
    pp = page.get("pageprops") or {}
    qid = str(pp.get("wikibase_item") or "").strip()
    extra = {"page_title": page_title, "wikidata_qid": qid}
    return canonical, extract, extra


def _wikidata_entity(
    paths: RagPaths,
    *,
    qid: str,
    sleep_sec: float,
    force: bool,
) -> dict[str, Any] | None:
    if not qid:
        return None
    url = "https://www.wikidata.org/wiki/Special:EntityData/{}.json".format(qid)
    resp = fetch_cached(
        url,
        cache_dir=paths.http_cache_dir,
        sleep_sec=sleep_sec,
        force=force,
        timeout_sec=90,
    )
    if resp.status_code != 200:
        return None
    return resp.json()


def _wikidata_people_born_in(
    paths: RagPaths,
    *,
    qid: str,
    limit: int,
    sleep_sec: float,
    force: bool,
) -> list[dict[str, str]]:
    """
    Return a short list of notable people born in a city (qid).

    Uses Wikidata SPARQL endpoint; results are metadata only.
    """
    if not qid:
        return []
    endpoint = "https://query.wikidata.org/sparql"
    query = (
        "SELECT ?person ?personLabel ?occupationLabel WHERE {"
        "  ?person wdt:P19 wd:%s ."
        "  OPTIONAL { ?person wdt:P106 ?occupation . }"
        "  SERVICE wikibase:label { bd:serviceParam wikibase:language \"en,ru\". }"
        "} LIMIT %d"
    ) % (qid, int(limit))
    url = endpoint + "?format=json&query=" + quote(query, safe="")
    resp = fetch_cached(
        url,
        cache_dir=paths.http_cache_dir,
        sleep_sec=sleep_sec,
        force=force,
        timeout_sec=90,
        headers={
            "Accept": "application/sparql-results+json",
        },
    )
    if resp.status_code != 200:
        return []
    data = resp.json()
    rows: list[dict[str, str]] = []
    for b in (data.get("results") or {}).get("bindings") or []:
        label = str((b.get("personLabel") or {}).get("value") or "").strip()
        occ = str((b.get("occupationLabel") or {}).get("value") or "").strip()
        uri = str((b.get("person") or {}).get("value") or "").strip()
        if not label or not uri:
            continue
        rows.append({"label": label, "occupation": occ, "uri": uri})
    return rows


def _wikidata_facts_text(entity: dict[str, Any], *, qid: str, lang: str) -> str:
    ent = ((entity.get("entities") or {}).get(qid) or {}) if entity else {}
    labels = ent.get("labels") or {}
    label = str(((labels.get(lang) or {}).get("value") or "")).strip()
    if not label:
        label = str(((labels.get("en") or {}).get("value") or "")).strip()
    desc = str((((ent.get("descriptions") or {}).get(lang) or {}).get("value") or "")).strip()
    if not desc:
        desc = str((((ent.get("descriptions") or {}).get("en") or {}).get("value") or "")).strip()
    parts: list[str] = []
    if label:
        parts.append(label)
    if desc:
        parts.append(desc)
    if not parts:
        return ""
    if len(parts) == 1:
        return parts[0]
    return "{} — {}".format(parts[0], parts[1])


def fetch_city(
    paths: RagPaths,
    slug: str,
    *,
    include_wikivoyage: bool,
    force: bool,
    sleep_sec: float,
) -> None:
    names = names_for_slug(slug)

    for lang, host, title in (
        ("en", "en.wikipedia.org", names.name_en),
        ("ru", "ru.wikipedia.org", names.name_ru or names.name_en),
    ):
        url, text, extra = _mw_extract(
            paths,
            host=host,
            language=lang,
            title=title,
            sleep_sec=sleep_sec,
            force=force,
        )
        doc = RagDocument(
            doc_id=_doc_id("wikipedia", lang, slug, url),
            city_slug=slug,
            language=lang,
            source_name="wikipedia",
            source_url=url,
            license=_WIKI_LICENSE,
            retrieved_at_utc=_utc_now(),
            title=extra.get("page_title") or title,
            text=text,
            extra=extra,
        )
        _write_doc(paths, doc)

        qid = str(extra.get("wikidata_qid") or "").strip()
        entity = _wikidata_entity(
            paths,
            qid=qid,
            sleep_sec=sleep_sec,
            force=force,
        )
        if entity:
            people = _wikidata_people_born_in(
                paths,
                qid=qid,
                limit=20,
                sleep_sec=max(sleep_sec, 1.0),
                force=force,
            )
            facts_text = _wikidata_facts_text(entity, qid=qid, lang=lang)
            wd = RagDocument(
                doc_id=_doc_id("wikidata", lang, slug, qid),
                city_slug=slug,
                language=lang,
                source_name="wikidata",
                source_url="https://www.wikidata.org/wiki/{}".format(qid),
                license=_WIKIDATA_LICENSE,
                retrieved_at_utc=_utc_now(),
                title=qid,
                text=facts_text,
                extra={
                    "qid": qid,
                    "people_born_in": people,
                    "entity": entity.get("entities", {}).get(qid, {}),
                },
            )
            _write_doc(paths, wd)

    if include_wikivoyage:
        for lang, host, title in (
            ("en", "en.wikivoyage.org", names.name_en),
            ("ru", "ru.wikivoyage.org", names.name_ru or names.name_en),
        ):
            url, text, extra = _mw_extract(
                paths,
                host=host,
                language=lang,
                title=title,
                sleep_sec=sleep_sec,
                force=force,
            )
            if not text.strip():
                continue
            doc = RagDocument(
                doc_id=_doc_id("wikivoyage", lang, slug, url),
                city_slug=slug,
                language=lang,
                source_name="wikivoyage",
                source_url=url,
                license=_WIKI_LICENSE,
                retrieved_at_utc=_utc_now(),
                title=extra.get("page_title") or title,
                text=text,
                extra=extra,
            )
            _write_doc(paths, doc)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=_PROJECT_ROOT,
        help="Repo root (default: auto).",
    )
    parser.add_argument(
        "--cities",
        nargs="*",
        default=None,
        metavar="SLUG",
        help="City slugs (default: auto-discovered build_*_pdf slugs).",
    )
    parser.add_argument(
        "--include-wikivoyage",
        action="store_true",
        help="Also fetch Wikivoyage pages (EN/RU) when present.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Ignore cache and refetch all URLs.",
    )
    parser.add_argument(
        "--sleep-sec",
        type=float,
        default=0.35,
        help="Sleep between requests (default: 0.35).",
    )
    args = parser.parse_args()
    root = args.project_root.resolve()
    paths = rag_paths(root)
    slugs = (
        sorted(set(args.cities))
        if args.cities
        else _discover_slugs(root)
    )
    if not slugs:
        print("No city slugs found.", file=sys.stderr)
        return 2
    failed: list[tuple[str, str]] = []
    for slug in slugs:
        prefixes = fact_source_prefixes(root, slug)
        if prefixes:
            print("Fetch:", slug, "({} fact domains)".format(len(prefixes)))
        else:
            print("Fetch:", slug)
        try:
            fetch_city(
                paths,
                slug,
                include_wikivoyage=args.include_wikivoyage,
                force=args.force,
                sleep_sec=max(0.0, float(args.sleep_sec)),
            )
        except Exception as exc:
            msg = str(exc)
            print("FAILED {}: {}".format(slug, msg), file=sys.stderr)
            failed.append((slug, msg))
            continue
    if failed:
        print("---", file=sys.stderr)
        print("Fetch finished with failures: {}".format(len(failed)), file=sys.stderr)
        for slug, msg in failed:
            print("  {}: {}".format(slug, msg), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

