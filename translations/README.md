# Translation workflow files

See **[docs/GUIDE_TRANSLATION_BATCH.md](../docs/GUIDE_TRANSLATION_BATCH.md)** for
EN↔RU batch translation.

**EN narrative fill (missing English place text):**

```powershell
python scripts/export_en_narrative_fill_queue.py --split-by-city
# Upload translations/collab/en_narrative_fill_colab.ipynb to Google Colab
# + en_narrative_fill.json (or en_narrative_fill_moscow.json)
python scripts/apply_en_narrative_fill_results.py --dry-run
python scripts/apply_en_narrative_fill_results.py
```

Quick start (translation):

```powershell
python scripts/export_guide_translation_queue.py --cities chernivtsi
# … translate in Colab …
python scripts/apply_guide_translation_results.py
```

Large generated files (`queue/`, `collab/`, `results/`) are gitignored; keep them
on Drive or locally. Examples are in `examples/`.
