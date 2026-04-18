# Vatican City guide

## Refresh images

From the repository root:

```bash
python scripts/download_vatican_images.py
python scripts/validate_vatican_sources.py
```

## Build HTML / PDF

```bash
python scripts/build_vatican_pdf.py --html-only
python scripts/build_vatican_pdf.py
```

PDF under `vatican/output/*.pdf` is gitignored.
