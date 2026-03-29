# Budapest city guide

Same layout as `prague/` and `smolensk/`: `budapest/data/*.json`,
`budapest/images/`, `budapest/output/`, `budapest/docs/SOURCES_WHITELIST.md`.

- **Card language:** English (`name_en`) with Hungarian subtitle (`subtitle_hu`).
- **Title:** coat of arms and flag from Commons (`download_budapest_images.py`).
- **Raster images** under `budapest/images/` are **committed** so CI can build
  HTML without re-downloading (see `budapest/README.md`).
- **Scripts:** `download_budapest_images.py`, `validate_budapest_sources.py`,
  `build_budapest_pdf.py` (`--html-only` skips PDF).
