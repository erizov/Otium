# Budapest guide (OTIUM model)

Flat `images/<slug>.jpg`, JSON registry, whitelist, and scripts in `scripts/`.

Raster images under `budapest/images/` are **committed** for reproducible
builds without re-downloading from Commons.

## Build

From the repository root:

```bash
python scripts/download_budapest_images.py
python scripts/validate_budapest_sources.py
python scripts/build_budapest_pdf.py
```

HTML only (no Playwright PDF), e.g. for CI:

```bash
python scripts/build_budapest_pdf.py --html-only
```

PDF output is ignored by git (`budapest/output/*.pdf`).

See `docs/BUDAPEST_GUIDE.md` for structure and conventions.
