# -*- coding: utf-8 -*-
"""Load per-city fact-source allowlists from SOURCES_WHITELIST.md."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.city_guide_standard_whitelist import load_prefixes_from_markdown
from scripts.city_guide_standard_whitelist import whitelist_path_for_city

_DOMAINS_PATH = Path(__file__).resolve().parent.parent / "data" / "city_official_domains.json"


def official_domains_for_city(city_slug: str) -> tuple[str, ...]:
    """Tier B domains from data/city_official_domains.json."""
    if not _DOMAINS_PATH.is_file():
        return ()
    raw = json.loads(_DOMAINS_PATH.read_text(encoding="utf-8"))
    urls = raw.get(city_slug) if isinstance(raw, dict) else None
    if not isinstance(urls, list):
        return ()
    return tuple(str(u).strip() for u in urls if str(u).strip())


def fact_source_prefixes(project_root: Path, city_slug: str) -> tuple[str, ...]:
    """
    HTTPS prefixes allowed for factual ingestion (RAG Tier B).

    Merges markdown whitelist Facts section with city_official_domains.json.
    """
    path = whitelist_path_for_city(project_root, city_slug)
    found: set[str] = set(official_domains_for_city(city_slug))
    if path.is_file():
        text = path.read_text(encoding="utf-8")
        in_facts = False
        for line in text.splitlines():
            s = line.strip()
            if s.lower().startswith("## facts"):
                in_facts = True
                continue
            if s.startswith("## ") and in_facts:
                break
            if in_facts and s.startswith("- https://"):
                found.add(s[2:].strip())
        for p in load_prefixes_from_markdown(path):
            if "wikipedia" not in p and "wikidata" not in p and "commons" not in p:
                found.add(p)
    return tuple(sorted(found, key=len, reverse=True))
