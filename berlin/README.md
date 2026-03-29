# Berlin guide (OTIUM model)

Flat `images/<slug>.jpg`, JSON registry, whitelist. **Raster images are
committed** for reproducible CI and offline builds.

## Build

From the repository root:

```bash
python scripts/download_berlin_images.py
python scripts/validate_berlin_sources.py
python scripts/build_berlin_pdf.py
python scripts/build_berlin_pdf.py --html-only
```

PDF under `berlin/output/*.pdf` is gitignored.

See `docs/BERLIN_GUIDE.md`.
