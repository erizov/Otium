# Optimized PDF/HTML guides

Optimized guides **drop places without images** and use **3 photos + 1 map per place** in a **2×2 grid** (smaller PDF/HTML).

## Naming

| Output type | Full | Optimized |
|-------------|------|-----------|
| Single guide HTML | `{guide}_guide.html` | `{guide}_guide_opt.html` |
| Single guide PDF  | `{guide}_guide.pdf`  | `{guide}_guide_opt.pdf`  |
| Combined Moscow HTML | `Moscow_Complete_Guide.html` | `Moscow_Complete_Guide_opt.html` |
| Combined Moscow PDF  | `Moscow_Complete_Guide.pdf`  | `Moscow_Complete_Guide_opt.pdf`  |

## Behavior

- **Places:** Only places that have **at least one** valid image on disk are included.
- **Per place:** Up to **3 images** plus **1 map**, laid out in a **2×2 grid** (row1: photo1, photo2; row2: photo3, map).
- **Output:** `*_guide_opt.html` and `*_guide_opt.pdf` (full guides keep `*_guide.html` / `*_guide.pdf`).

## Commands to generate optimized PDF guides

**Single guide (e.g. parks)** — build from existing images only (no download):

```bash
python scripts/build_pdf.py --guide parks --optimized --build-with-available
```

Output: `output/parks_guide_opt.html`, `output/parks_guide_opt.pdf`.

**Single guide with download** (download missing images, then build optimized):

```bash
python scripts/build_pdf.py --guide parks --optimized --build-with-available
```
(Omitting `--build-only` runs download first, then builds optimized HTML/PDF.)

**All single guides optimized** — build optimized PDF/HTML for every guide from existing images:

```bash
python scripts/build_pdf.py --all-guides --optimized --build-only --build-with-available
```

Output: `output/<guide>_guide_opt.html` and `output/<guide>_guide_opt.pdf` for each guide.

**Combined Moscow guide (optimized)** — one PDF with all topics, only places that have images, 3 photos + map per place:

```bash
python scripts/build_full_guide.py --optimized
```

Output: `output/Moscow_Complete_Guide_opt.html`, `output/Moscow_Complete_Guide_opt.pdf`.

This runs `build_pdf.py --all-guides --optimized --build-only --build-with-available` first to generate each `*_guide_opt.html`, then assembles and chunk-renders the combined PDF.

**Combined Moscow guide with image download then optimized build:**

```bash
python scripts/build_full_guide.py --download-images --optimized
```

**Full (non-optimized) combined guide** (all places, 4 images per place):

```bash
python scripts/build_full_guide.py
```

Output: `output/Moscow_Complete_Guide.html`, `output/Moscow_Complete_Guide.pdf`.
