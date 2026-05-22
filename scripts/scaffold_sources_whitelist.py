# -*- coding: utf-8 -*-
"""Generate or refresh per-city SOURCES_WHITELIST.md from shared template."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_DOMAINS_PATH = _PROJECT_ROOT / "data" / "city_official_domains.json"

_WIKI_IMAGE = """## Images (validated by validate_<city>_sources.py)

- https://upload.wikimedia.org/
- https://commons.wikimedia.org/
"""

_FACTS_HEADER = """
## Facts (editors / RAG fetch_sources allowlist)

Use for dates, names, and history — not for long verbatim copy.
"""

_DENY = """
## Do not use for facts

- TripAdvisor, Pinterest, random blogs, unattributed social posts
- Stock photo sites for factual claims (images only if ever whitelisted)
"""


def _load_domains() -> dict[str, list[str]]:
    if not _DOMAINS_PATH.is_file():
        return {}
    raw = json.loads(_DOMAINS_PATH.read_text(encoding="utf-8"))
    out: dict[str, list[str]] = {}
    for key, val in raw.items():
        if isinstance(val, list):
            out[str(key)] = [str(u).strip() for u in val if str(u).strip()]
    return out


def render_whitelist(city_slug: str, official: list[str]) -> str:
    lines = [
        "# Allowed sources — {}".format(city_slug.replace("_", " ").title()),
        "",
        _WIKI_IMAGE.replace("<city>", city_slug),
    ]
    lines.append(_FACTS_HEADER.strip())
    lines.append("")
    lines.append("- https://www.unesco.org/")
    lines.append("- https://www.wikidata.org/")
    lines.append("- https://en.wikipedia.org/")
    lines.append("- https://ru.wikipedia.org/")
    for url in official:
        lines.append("- {}".format(url))
    lines.append(_DENY.strip())
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cities",
        nargs="*",
        default=None,
        metavar="SLUG",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing SOURCES_WHITELIST.md.",
    )
    args = parser.parse_args()
    domains = _load_domains()
    cities = sorted(domains.keys())
    if args.cities:
        cities = [c for c in cities if c in set(args.cities)]
    written = 0
    for slug in cities:
        path = _PROJECT_ROOT / slug / "docs" / "SOURCES_WHITELIST.md"
        if path.is_file() and not args.force:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            render_whitelist(slug, domains.get(slug, [])),
            encoding="utf-8",
        )
        written += 1
        print("wrote", path.relative_to(_PROJECT_ROOT))
    print("Updated {} whitelist file(s).".format(written))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
