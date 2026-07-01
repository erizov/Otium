# English Architecture

Chronological architecture guide. Pipeline:

```bash
python scripts/generate_architecture_guide.py --module english_architecture
python scripts/resolve_architecture_guide_images.py --module english_architecture --commons-only
python scripts/filter_architecture_guide_commons_only.py --module english_architecture
python scripts/build_architecture_guide_pdf.py --module english_architecture --lang ru en
```
