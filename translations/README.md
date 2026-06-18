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

---

## City guide images (2-image PDF rule)

PDFs show **1 photo** when only one exists on disk, **2 photos** when two or
more exist (capped at 2). Download policy: **max 2 images per place** for
registry cities; **Moscow and SPB** place downloads are frozen (use on-disk only).

Regenerate this table:

```powershell
python scripts/stats_city_guide_images_per_place.py
```

Snapshot **2026-06-14** (primary + `additional_images` on disk, PDF cap 2):

| City | Places | 0 img | 1 img | 2 img |
|------|--------|-------|-------|-------|
| amsterdam | 31 | 0 | 31 | 0 |
| athens | 29 | 0 | 29 | 0 |
| bangkok | 32 | 0 | 32 | 0 |
| barcelona | 33 | 0 | 33 | 0 |
| berlin | 38 | 0 | 38 | 0 |
| boston | 28 | 0 | 28 | 0 |
| budapest | 33 | 0 | 33 | 0 |
| chernivtsi | 33 | 0 | 33 | 0 |
| copenhagen | 29 | 0 | 29 | 0 |
| dubai | 34 | 0 | 34 | 0 |
| dublin | 21 | 0 | 21 | 0 |
| florence | 37 | 0 | 37 | 0 |
| istanbul | 33 | 0 | 33 | 0 |
| jerusalem | 33 | 0 | 33 | 0 |
| kazan | 29 | 0 | 29 | 0 |
| kharkiv | 29 | 0 | 29 | 0 |
| kyiv | 30 | 0 | 30 | 0 |
| lisbon | 28 | 0 | 28 | 0 |
| london | 26 | 0 | 26 | 0 |
| los_angeles | 30 | 0 | 30 | 0 |
| lviv | 30 | 0 | 30 | 0 |
| madrid | 33 | 0 | 33 | 0 |
| minsk | 34 | 0 | 34 | 0 |
| montreal | 39 | 0 | 39 | 0 |
| **moscow** | **500** | **119** | **60** | **321** |
| new_york | 35 | 0 | 35 | 0 |
| novosibirsk | 28 | 0 | 28 | 0 |
| odessa | 25 | 0 | 25 | 0 |
| paris | 38 | 0 | 38 | 0 |
| philadelphia | 27 | 0 | 27 | 0 |
| prague | 37 | 0 | 37 | 0 |
| rome | 40 | 0 | 40 | 0 |
| san_francisco | 26 | 0 | 26 | 0 |
| singapore | 27 | 0 | 27 | 0 |
| smolensk | 68 | 0 | 3 | 64 |
| **spb** | **354** | **0** | **304** | **50** |
| tokyo | 30 | 0 | 30 | 0 |
| tver | 31 | 0 | 31 | 0 |
| vatican | 27 | 0 | 27 | 0 |
| venice | 35 | 0 | 35 | 0 |
| vienna | 33 | 0 | 33 | 0 |
| vladivostok | 25 | 0 | 25 | 0 |
| volgograd | 25 | 0 | 25 | 0 |
| vologda | 22 | 0 | 22 | 0 |
| yaroslavl | 26 | 0 | 26 | 0 |
| **TOTAL** | **2211** | **119** | **1656** | **435** |

**Totals (PDF-eligible, excl. `suppress_images_for_pdf`):** 2,210 places — **1
image** 1,656 (74.9%), **2 images** 435 (19.7%), **0 images** 119 (5.4%, all
Moscow).

Most registry cities still have only the primary image; **SPB** 2-image rows are
mostly osobnjaki sidecar (50); **Smolensk** already has 64 places at 2 images.

### Rebuild after translation or new downloads

Run from repo root. **Translate first** (Colab batch), then rebuild PDFs
**without Ollama** (`CITY_GUIDE_NO_TRANSLATE=1` is set by the rebuild script).

```powershell
# 1) Optional: fill missing EN/RU text before rebuild
python scripts/export_guide_translation_queue.py
# … Colab: en_to_ru / ru_to_en → translations/results/*.jsonl …
python scripts/apply_guide_translation_results.py

# 2) Download missing images (max 2/place; skips moscow/spb)
python scripts/download_missing_registry_images.py

# 3) Preview stale guides
python scripts/rebuild_stale_city_guide_pdfs.py --dry-run

# 4) Rebuild stale PDFs only (no live translation)
python scripts/rebuild_stale_city_guide_pdfs.py

# Or: force rebuild every city (after image-policy change)
python scripts/rebuild_stale_city_guide_pdfs.py --force-all
```

One-shot download + force rebuild (2-image layout):

```powershell
python scripts/rebuild_all_guides_two_images.py
```

Large guides that timed out on Playwright: rebuild single cities with a longer
image wait (no Ollama):

```powershell
$env:CITY_GUIDE_NO_TRANSLATE = "1"
python scripts/build_spb_pdf.py --image-wait-ms 180000
```

See also **[docs/REBUILD_ALL_CITY_GUIDES.md](../docs/REBUILD_ALL_CITY_GUIDES.md)**
and **[docs/GUIDE_TRANSLATION_BATCH.md](../docs/GUIDE_TRANSLATION_BATCH.md)**.
