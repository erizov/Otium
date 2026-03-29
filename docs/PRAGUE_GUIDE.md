# Prague city guide

Follows the same layout as `smolensk/`: `prague/data/*.json`, `prague/images/`,
`prague/output/`, `prague/docs/SOURCES_WHITELIST.md`.

- **Card language:** English (`name_en`) with optional Czech subtitle (`subtitle_cs`).
- **Scripts:** `download_prague_images.py`, `validate_prague_sources.py`,
  `build_prague_pdf.py` (`--html-only` skips PDF).
- **Shared helpers:** `scripts/city_guide_core.py` (minimum image size and
  same-stem file resolution) — also used by `build_smolensk_pdf.py`.

Title page uses coat of arms and flag from Wikimedia Commons when present under
`prague/images/`.

**Images in git:** Prague rasters are usually fetched locally or in CI; from
**Budapest onward** raster files under `*/images/` are committed for
reproducibility (see `budapest/README.md`).
