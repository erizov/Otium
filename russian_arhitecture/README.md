# Russian Architecture guide

Thirty architectural styles (chronological chapters) with 2–3 landmark
examples each. PDF uses SPB-style category chapters (one chapter per style).

```bash
python scripts/generate_russian_arhitecture_guide.py
python scripts/resolve_russian_arhitecture_images.py --copy-only
python scripts/resolve_russian_arhitecture_images.py --commons-delay 3
python scripts/build_russian_arhitecture_pdf.py --lang ru en
```

Data: `data/style_catalog.py`, `data/russian_arhitecture_places.json`.
Images: `images/styles/` (reused from city guides when possible).
