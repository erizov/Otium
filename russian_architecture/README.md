# Russian Architecture guide

Thirty architectural styles (chronological chapters) with 2–3 landmark
examples each. PDF uses SPB-style category chapters (one chapter per style).

```bash
python scripts/generate_russian_architecture_guide.py
python scripts/resolve_russian_architecture_images.py --copy-only
python scripts/resolve_russian_architecture_images.py --commons-delay 3
python scripts/build_russian_architecture_pdf.py --lang ru en
```

Data: `data/style_catalog.py`, `data/russian_architecture_places.json`.
Images: `images/styles/` (reused from city guides when possible).
