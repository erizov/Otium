# RAG sources policy (city guides)

This repo can build a **local-only** Retrieval Augmented Generation (RAG)
knowledge base for city guides. The RAG corpus is used to draft and verify
guide text (history, architecture, facts, significance, famous persons, etc.).

## Core principles

- **Legality first.** Only download and store content that is allowed by the
  source’s license/ToS and `robots.txt`.
- **Provenance is mandatory.** Every downloaded document/chunk must retain:
  - **`source_url`** (canonical URL)
  - **`source_name`** (e.g. `wikipedia`, `wikidata`, `wikivoyage`, `unesco`)
  - **`license`** (string, e.g. `CC BY-SA 4.0`, `Public Domain`, `Unknown`)
  - **`retrieved_at`** (UTC timestamp)
- **No sources in PDFs.** The generated city guide PDFs must not contain
  “sources”, “Commons”, “Wikipedia”, attribution lines, or license notes in
  the rendered text. Provenance is stored in **RAG metadata** only.
- **Do not invent facts.** City-guide editorial rules still apply
  (see `docs/CITY_GUIDES_README.md`, “Editorial policy”).

## Allowed source tiers (default)

### Tier A (automatable, broad coverage)

- **Wikipedia (EN/RU)** — city pages and selected linked pages.
  - License: CC BY-SA (varies by language edition; treat as CC BY-SA).
  - Retrieval: MediaWiki API (extracts) or REST endpoints.
- **Wikidata** — factual triples + selected query results (e.g. UNESCO ID,
  coordinates, founding date).
  - License: CC0.
  - Retrieval: Wikidata API + SPARQL endpoint.
- **Wikivoyage (EN/RU, when available)** — travel structure / districts /
  “see” lists (used as signals, not as factual authority).

### Tier B (official / institutional, per-domain allowlist)

- **UNESCO World Heritage** pages.
- **Official tourism boards / museum sites / municipal portals** when:
  - access is allowed by ToS + robots
  - pages are stable and linkable
  - the domain is added to an allowlist

### Tier C (books / long-form)

- **Project Gutenberg** (EN, public domain).
- **Internet Archive / Open Library** only when a specific item is legally
  downloadable and storable under its access mode (often *not*).
- National library PD scans (case-by-case).

## What we store locally

RAG cache and index are **local artifacts** and must remain out of git:

- `.rag_cache/http/…` — raw HTTP payload cache (for reproducibility)
- `.rag_cache/docs/<city>/…` — normalized documents
- `.rag_cache/index/…` — chunk metadata + vectors

## How we avoid sources in PDFs

- City-guide builders do not render source metadata fields.
- Any **auto-generated** place rows must omit `license_note` and `attribution`
  fields unless explicitly needed for another process.
- Any RAG exporter must write provenance into **side metadata files** only
  (JSON/JSONL), never into fields that flow into PDFs (`description`, `facts`,
  `history`, `significance`, `subtitle_*`, meta lines, etc.).

## Required User-Agent and rate limiting

All RAG fetchers must set a descriptive **User-Agent** and apply per-host
rate limits (especially Wikimedia and Wikidata SPARQL).

## Per-city allowlists (facts / Tier B)

Official and institutional domains for each city live in
`<city>/docs/SOURCES_WHITELIST.md` (generated from `data/city_official_domains.json`):

```powershell
python scripts/scaffold_sources_whitelist.py --force
```

`scripts/rag/fetch_sources.py` reads the **Facts** section prefixes when ingesting
optional HTTP pages. Image URL validation still uses the same file via
`scripts/city_guide_standard_whitelist.py`.

**Refresh cadence (recommended):** quarterly per active city —
`fetch_sources.py`, `fetch_place_wikipedia.py`, `chunk_and_embed.py`,
`rebuild_index.py`, then `export_place_fields.py` (review before `--apply`).

## Editorial lint

```powershell
python scripts/city_guide_text_lint.py
python scripts/lint_image_paths.py
```
