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
`paris/`, `rome/`, `venice/`, `florence/`, `barcelona/`, `madrid/`.
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

Expansion plan (more place ideas): `docs/CITY_GUIDES_EXPANSION_PLAN.md`.
