# Philadelphia guide (OTIUM model)

Flat `images/` paths, JSON registry, whitelist. **Raster images are
committed** for reproducible CI and offline builds.

## Build

From the repository root:

```bash
python scripts/download_philadelphia_images.py
python scripts/validate_philadelphia_sources.py
python scripts/build_philadelphia_pdf.py
python scripts/build_philadelphia_pdf.py --html-only
```

PDF under `philadelphia/output/*.pdf` is gitignored.

See `docs/PHILADELPHIA_GUIDE.md`.
