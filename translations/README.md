# Translation workflow files

See **[docs/GUIDE_TRANSLATION_BATCH.md](../docs/GUIDE_TRANSLATION_BATCH.md)** for
the full Google Colab workflow.

Quick start:

```powershell
python scripts/export_guide_translation_queue.py --cities chernivtsi
# … translate in Colab …
python scripts/apply_guide_translation_results.py
```

Large generated files (`queue/`, `collab/`, `results/`) are gitignored; keep them
on Drive or locally. Examples are in `examples/`.
