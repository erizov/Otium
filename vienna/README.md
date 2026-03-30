# Vienna guide (OTIUM model)

Flat `images/` paths, JSON registry, whitelist. **Raster images are
committed** for reproducible CI and offline builds.

## Build

From the repository root:

```bash
python scripts/download_vienna_images.py
python scripts/validate_vienna_sources.py
python scripts/build_vienna_pdf.py
python scripts/build_vienna_pdf.py --html-only
```

PDF under `vienna/output/*.pdf` is gitignored.

See `docs/VIENNA_GUIDE.md`.
