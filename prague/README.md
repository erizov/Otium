# Prague guide (OTIUM model)

Flat `images/<slug>.jpg`, JSON registry, whitelist, and scripts in `scripts/`.

Raster images under `prague/images/` are **committed** for reproducible builds
(like Budapest and Berlin).

## Build

From the repository root:

```bash
python scripts/download_prague_images.py
python scripts/validate_prague_sources.py
python scripts/build_prague_pdf.py
```

HTML only (no Playwright PDF), e.g. for CI:

```bash
python scripts/build_prague_pdf.py --html-only
```

PDF output is ignored by git (`prague/output/*.pdf`); keep PDFs local or in releases.

See `docs/PRAGUE_GUIDE.md` for structure and conventions.
