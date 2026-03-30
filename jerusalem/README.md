# Jerusalem guide (OTIUM model)

Flat `images/` paths, JSON registry, whitelist. **Raster images are
committed** for reproducible CI and offline builds.

## Build

From the repository root:

```bash
python scripts/download_jerusalem_images.py
python scripts/validate_jerusalem_sources.py
python scripts/build_jerusalem_pdf.py
python scripts/build_jerusalem_pdf.py --html-only
```

PDF under `jerusalem/output/*.pdf` is gitignored.
