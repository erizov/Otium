# City guides (Excursion repo)

OTIUM-style **per-city** guides live in their own folder: JSON registry, flat
`images/<slug>.jpg`, `docs/SOURCES_WHITELIST.md`, and three scripts in
`scripts/` named after the city slug (`prague`, `budapest`, `berlin`, `paris`,
`rome`, `barcelona`, `smolensk`, …).

**Rebuild every city in one workflow:** [REBUILD_ALL_CITY_GUIDES.md](REBUILD_ALL_CITY_GUIDES.md).

---

## Local web editor (LLM-assisted)

The repo includes a lightweight local web app to browse a city guide and persist
edits into an overlay detail file.

- **Persistent edits**: written to `<city>/data/<city>_place_details_more.json`
  (auto-merged by existing `*_place_details*.json` logic).
- **LLM draft**:
  - Default: **Ollama (local)**, with model list shown in UI and strongest model
    auto-selected.
  - Optional: **OpenAI** appears as the last provider choice when
    `OPENAI_API_KEY` is set.

### Run

From repo root:

```powershell
pip install -r requirements.txt
powershell -ExecutionPolicy Bypass -File scripts/webapp_start.ps1 [-BindHost 127.0.0.1] [-Port 8000]
```

Open `http://127.0.0.1:8000/<city>` (example: `/smolensk`) and use **Apply** to
save edits.

Stop:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/webapp_stop.ps1
```

### Extend to another city

Any city folder that contains `data/<city>_places.json` will automatically show
up in the UI’s City dropdown (no code changes needed).

## Editorial policy (facts and sources)

Applies to **all** per-city guides (JSON registries, detail files, and any prose
that ships in HTML/PDF).

- **Do not invent or imply facts.** Statements in `description`, `history`,
  `significance`, `facts`, `stories`, and meta fields (`year_built`,
  `architecture_style`, `address` when used as a factual claim) must come from
  **valid sources** (e.g. cited reference, museum or official site, reputable
  reference work with a stable link, or `docs/SOURCES_WHITELIST.md`-compliant
  image metadata). If it cannot be verified, **omit** it.
- **Omit empty sections.** If there is no reliable information for a field, leave
  the key **absent** or use a single placeholder token (`—`, `-`, etc.) only
  where tooling expects a stub; see `is_substantive_text()` in
  `scripts/city_guide_core.py`. Do **not** pad with generic filler.
- **Skip `year_built`, `architecture_style`, `history`, and `significance`**
  when sources do not supply them. Builders omit empty blocks; meta lines omit
  missing parts.

---

## Example: Budapest

From the **repository root** (`Excursion/`):

```bash
# 1) Refresh images from Commons (optional if rasters are already in git)
python scripts/download_budapest_images.py

# 2) Check every image_source_url against the city whitelist
python scripts/validate_budapest_sources.py

# 3) HTML + PDF (needs Playwright + Chromium for PDF)
python scripts/build_budapest_pdf.py

# HTML only (no PDF) — same inputs; good for CI or quick checks
python scripts/build_budapest_pdf.py --html-only
```

**Custom paths** (defaults: `budapest/` and `budapest/output/`):

```bash
python scripts/download_budapest_images.py --budapest-root path/to/budapest
python scripts/build_budapest_pdf.py --budapest-root path/to/budapest --output-dir path/to/out
```

**Outputs:** `budapest/output/budapest_guide.html`; PDF is written beside it but
`budapest/output/*.pdf` is gitignored (large binaries).

More detail: `budapest/README.md`, `docs/BUDAPEST_GUIDE.md`.

---

## Typography (PDF / HTML)

European and US Latin guides load **Google Fonts** in
`scripts/city_guide_typography.py`. **Title faces** (OTIUM logo, guide `h1`,
each place `h3`) evoke the region; **body** stays **Source Sans 3** for
readability. **Smolensk** and **SPB** keep their own stylesheets (e.g. Ponomar /
Cormorant for Cyrillic).

| City slug | Title font (headings) |
|-----------|------------------------|
| `berlin` | Grenze Gotisch |
| `paris` | Playfair Display |
| `rome`, `venice` | Cinzel |
| `florence` | Cormorant Infant |
| `barcelona`, `madrid` | Marcellus |
| `budapest`, `prague` | Spectral |
| `vienna` | Vollkorn |
| `boston`, `philadelphia`, `new_york` | Libre Baskerville |
| `montreal` | Cormorant |
| `jerusalem` | David Libre (titles) · Rubik (body, Hebrew subtitles) |

<!-- city-guide-stats -->
## Registry statistics

Merged registries (`*places.json` + detail JSON where applicable). **Images** = raster/SVG files under `<city>/images/` (recursive). **obj/place** = average count of substantive list items per place (facts + stories + additional_images). Columns **no year** through **no sig.** count places where that field is missing or placeholder-only (`—`, `-`, `n/a`, …), using `is_substantive_text()` in `scripts/city_guide_core.py`. **no facts** means no substantive `facts` list item.

Refresh: `python scripts/report_city_guide_stats.py --write`

| City | Places | Images | obj/place | no year | no style | no addr | no desc | no facts | no history | no sig. |
|------|-------:|-------:|----------:|--------:|---------:|--------:|---------:|----------:|-----------:|---------:|
| `barcelona` | 33 | 34 | 1.2 | 33 | 13 | 13 | 13 | 13 | 13 | 13 |
| `berlin` | 36 | 37 | 1.1 | 36 | 16 | 16 | 16 | 16 | 16 | 16 |
| `boston` | 30 | 31 | 1.9 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| `budapest` | 31 | 32 | 1.3 | 31 | 11 | 11 | 11 | 11 | 11 | 11 |
| `florence` | 34 | 35 | 1.9 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| `jerusalem` | 23 | 24 | 1.9 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| `madrid` | 33 | 34 | 1.2 | 33 | 13 | 13 | 13 | 13 | 13 | 13 |
| `montreal` | 38 | 39 | 1.9 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| `new_york` | 37 | 38 | 1.9 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| `paris` | 35 | 36 | 1.2 | 35 | 14 | 14 | 14 | 14 | 14 | 14 |
| `philadelphia` | 30 | 31 | 1.9 | 30 | 1 | 1 | 30 | 1 | 1 | 1 |
| `prague` | 34 | 35 | 1.2 | 34 | 14 | 14 | 14 | 14 | 14 | 14 |
| `rome` | 36 | 37 | 1.1 | 36 | 16 | 16 | 16 | 16 | 16 | 16 |
| `smolensk` | 51 | 116 | 2.1 | 19 | 4 | 1 | 1 | 1 | 1 | 1 |
| `spb` | 314 | 354 | 0.5 | 250 | 250 | 250 | 250 | 250 | 250 | 250 |
| `venice` | 35 | 36 | 1.9 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| `vienna` | 33 | 34 | 1.9 | 33 | 1 | 1 | 33 | 1 | 1 | 1 |
<!-- /city-guide-stats -->

---

## Using another city

Replace the slug in script names and flags:

| Step | Pattern |
|------|---------|
| Download | `python scripts/download_<city>_images.py` |
| Validate | `python scripts/validate_<city>_sources.py` |
| Build | `python scripts/build_<city>_pdf.py [--html-only]` |

**Root directory flags** (examples):

- `download_prague_images.py --prague-root …`
- `download_smolensk_images.py --smolensk-root …`
- `build_smolensk_pdf.py --smolensk-root … --output-dir …`

**Cities in this repo:** `smolensk/`, `spb/` (e.g. `download_spb_images.py`,
`validate_spb_sources.py`, `build_spb_pdf.py`), `prague/`, `budapest/`, `berlin/`,
`paris/`, `rome/`, `venice/`, `florence/`, `jerusalem/`, `barcelona/`, `madrid/`.
**Berlin** (same command pattern as Budapest): `download_berlin_images.py`,
`validate_berlin_sources.py`, `build_berlin_pdf.py` (`--berlin-root`).
**Paris:** `download_paris_images.py`, `validate_paris_sources.py`,
`build_paris_pdf.py` (`--paris-root`).
**Rome:** `download_rome_images.py`, `validate_rome_sources.py`,
`build_rome_pdf.py` (`--rome-root`).
**Barcelona:** `download_barcelona_images.py`, `validate_barcelona_sources.py`,
`build_barcelona_pdf.py` (`--barcelona-root`).
**Madrid:** `download_madrid_images.py`, `validate_madrid_sources.py`,
`build_madrid_pdf.py` (`--madrid-root`).

**Venice** (`venice/`): `download_venice_images.py`, `validate_venice_sources.py`,
`build_venice_pdf.py` (`--venice-root`). See `venice/README.md`.

**Florence** (`florence/`): `download_florence_images.py`,
`validate_florence_sources.py`, `build_florence_pdf.py` (`--florence-root`).
See `florence/README.md`.

**Montreal** (`montreal/`): `download_montreal_images.py`,
`validate_montreal_sources.py`, `build_montreal_pdf.py` (`--montreal-root`).

**Jerusalem** (`jerusalem/`): `download_jerusalem_images.py`,
`validate_jerusalem_sources.py`, `build_jerusalem_pdf.py` (`--jerusalem-root`).
See `jerusalem/README.md`.

Expansion plan (more place ideas): `docs/CITY_GUIDES_EXPANSION_PLAN.md`.
