# Venice guide (OTIUM model)

Flat `images/` paths, JSON registry, whitelist. **Raster images are
committed** for reproducible CI and offline builds.

## Build

From the repository root:

```bash
python scripts/download_venice_images.py
python scripts/validate_venice_sources.py
python scripts/build_venice_pdf.py
python scripts/build_venice_pdf.py --html-only
```

PDF under `venice/output/*.pdf` is gitignored.
