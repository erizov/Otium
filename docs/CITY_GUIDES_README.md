# City guides (Excursion repo)

OTIUM-style **per-city** guides live in their own folder: JSON registry, flat
`images/<slug>.jpg`, `docs/SOURCES_WHITELIST.md`, and three scripts in
`scripts/` named after the city slug (`prague`, `budapest`, `berlin`, `paris`,
`rome`, `barcelona`, `smolensk`, …).

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

Merged registries (`*places.json` + detail JSON where applicable). **Images** = raster/SVG files under `<city>/images/` (recursive). Columns **no year** through **no sig.** count places where that field is missing or placeholder-only (`—`, `-`, `n/a`, …), using `is_substantive_text()` in `scripts/city_guide_core.py`. **no facts** means no substantive `facts` list item.

Refresh: `python scripts/report_city_guide_stats.py --write`

| City | Places | Images | no year | no style | no addr | no desc | no facts | no history | no sig. |
|------|-------:|-------:|--------:|---------:|--------:|---------:|----------:|-----------:|---------:|
| `barcelona` | 32 | 34 | 32 | 12 | 12 | 12 | 12 | 12 | 12 |
| `berlin` | 35 | 37 | 35 | 15 | 15 | 15 | 15 | 15 | 15 |
| `boston` | 29 | 31 | 29 | 29 | 29 | 29 | 29 | 29 | 29 |
| `budapest` | 30 | 32 | 30 | 10 | 10 | 10 | 10 | 10 | 10 |
| `florence` | 33 | 35 | 33 | 33 | 33 | 33 | 33 | 33 | 33 |
| `jerusalem` | 22 | 24 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `madrid` | 32 | 34 | 32 | 12 | 12 | 12 | 12 | 12 | 12 |
| `montreal` | 37 | 39 | 37 | 37 | 37 | 37 | 37 | 37 | 37 |
| `new_york` | 36 | 38 | 36 | 36 | 36 | 36 | 36 | 36 | 36 |
| `paris` | 34 | 36 | 34 | 13 | 13 | 13 | 13 | 13 | 13 |
| `philadelphia` | 29 | 31 | 29 | 0 | 0 | 29 | 0 | 0 | 0 |
| `prague` | 33 | 35 | 33 | 13 | 13 | 13 | 13 | 13 | 13 |
| `rome` | 35 | 37 | 35 | 15 | 15 | 15 | 15 | 15 | 15 |
| `smolensk` | 50 | 116 | 19 | 3 | 0 | 0 | 0 | 0 | 0 |
| `spb` | 313 | 354 | 249 | 249 | 249 | 249 | 249 | 249 | 249 |
| `venice` | 34 | 36 | 34 | 34 | 34 | 34 | 34 | 34 | 34 |
| `vienna` | 32 | 34 | 32 | 0 | 0 | 32 | 0 | 0 | 0 |
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
