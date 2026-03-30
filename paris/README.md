# Paris guide (OTIUM model)

Flat `images/<slug>.jpg`, JSON registry, whitelist. **Raster images are
committed** for reproducible CI and offline builds.

## Build

From the repository root:

```bash
python scripts/download_paris_images.py
python scripts/validate_paris_sources.py
python scripts/build_paris_pdf.py
python scripts/build_paris_pdf.py --html-only
```

PDF under `paris/output/*.pdf` is gitignored.

See `docs/PARIS_GUIDE.md`.
