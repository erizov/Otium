# Rome guide (OTIUM model)

Flat `images/<slug>.jpg`, JSON registry, whitelist. **Raster images are
committed** for reproducible CI and offline builds.

## Build

From the repository root:

```bash
python scripts/download_rome_images.py
python scripts/validate_rome_sources.py
python scripts/build_rome_pdf.py
python scripts/build_rome_pdf.py --html-only
```

PDF under `rome/output/*.pdf` is gitignored.

See `docs/ROME_GUIDE.md`.
