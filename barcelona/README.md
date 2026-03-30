# Barcelona guide (OTIUM model)

Flat `images/<slug>.jpg`, JSON registry, whitelist. **Raster images are
committed** for reproducible CI and offline builds.

## Build

From the repository root:

```bash
python scripts/download_barcelona_images.py
python scripts/validate_barcelona_sources.py
python scripts/build_barcelona_pdf.py
python scripts/build_barcelona_pdf.py --html-only
```

PDF under `barcelona/output/*.pdf` is gitignored.

See `docs/BARCELONA_GUIDE.md`.
