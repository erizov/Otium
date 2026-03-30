# New York City guide (OTIUM model)

Flat `images/` paths, JSON registry, whitelist. **Raster images are
committed** for reproducible CI and offline builds.

## Build

From the repository root:

```bash
python scripts/download_new_york_images.py
python scripts/validate_new_york_sources.py
python scripts/build_new_york_pdf.py
python scripts/build_new_york_pdf.py --html-only
```

PDF under `new_york/output/*.pdf` is gitignored.

See `docs/NEW_YORK_GUIDE.md`.
