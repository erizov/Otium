# Boston guide (OTIUM model)

Flat `images/` paths, JSON registry, whitelist. **Raster images are
committed** for reproducible CI and offline builds.

## Build

From the repository root:

```bash
python scripts/download_boston_images.py
python scripts/validate_boston_sources.py
python scripts/build_boston_pdf.py
python scripts/build_boston_pdf.py --html-only
```

PDF under `boston/output/*.pdf` is gitignored.

See `docs/BOSTON_GUIDE.md`.
