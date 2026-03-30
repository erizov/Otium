# Florence guide (OTIUM model)

Flat `images/` paths, JSON registry, whitelist. **Raster images are
committed** for reproducible CI and offline builds.

## Build

From the repository root:

```bash
python scripts/download_florence_images.py
python scripts/validate_florence_sources.py
python scripts/build_florence_pdf.py
python scripts/build_florence_pdf.py --html-only
```

PDF under `florence/output/*.pdf` is gitignored.
