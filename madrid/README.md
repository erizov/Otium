# Madrid guide (OTIUM model)

Flat `images/<slug>.jpg`, JSON registry, whitelist. **Raster images are
committed** for reproducible CI and offline builds.

## Build

From the repository root:

```bash
python scripts/download_madrid_images.py
python scripts/validate_madrid_sources.py
python scripts/build_madrid_pdf.py
python scripts/build_madrid_pdf.py --html-only
```

PDF under `madrid/output/*.pdf` is gitignored.

See `docs/MADRID_GUIDE.md`.
