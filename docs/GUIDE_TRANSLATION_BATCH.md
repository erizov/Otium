# Batch translation for city guides (Google Colab)

Translate **EN ↔ RU** place text **before** PDF rebuild so guides do not call
Ollama at build time. Workflow:

1. **Export** strings that need translation from repo JSON.
2. **Translate** in Google Colab (two arrays: EN→RU and RU→EN).
3. **Apply** results back into guide data.
4. **Audit** and **rebuild PDFs** (translation disabled during rebuild).

See also: [CITY_GUIDES_README.md](CITY_GUIDES_README.md),
[REBUILD_ALL_CITY_GUIDES.md](REBUILD_ALL_CITY_GUIDES.md).

---

## What gets translated

A row is queued when:

- The **target** edition has no usable narrative in JSON (`place_edition_needs_fill`), and
- The **source** edition has usable text in the opposite language.

Fields:

| Field | EN source keys | RU target keys |
|-------|----------------|----------------|
| Name | `name_en`, `name` | `name_ru` |
| Description | `description_en`, `description` | `description_ru` |
| History | `history_en`, `history` | `history_ru` |
| Significance | `significance_en`, `significance` | `significance_ru` |
| Facts | `facts[]` (per item) | `facts_ru[]` |

Reverse keys for **RU → EN**.

**Not queued:** landmark boilerplate (`— landmark in City.`), empty stubs, rows
with no opposite-language source (use `fill_sparse_guide_narratives.py` instead).

---

## Where files live (large queues)

Use **`translations/`** at the repo root. Prefer **JSON Lines** (`.jsonl`), not
pipe-separated `.txt`.

| File | Size | Purpose |
|------|------|---------|
| `translations/queue/queue.jsonl` | Large | Full jobs (id, city, slug, target_key, source_text, …). **Keep in repo or Drive** — required for apply. |
| `translations/collab/en_to_ru.json` | Large | Colab input: `[{"id","text"}, …]` |
| `translations/collab/ru_to_en.json` | Large | Colab input |
| `translations/collab/en_to_ru.jsonl` | Large | Same as JSON, one object per line (streaming) |
| `translations/collab/ru_to_en.jsonl` | Large | Same |
| `translations/results/en_to_ru_results.jsonl` | Large | Colab output |
| `translations/results/ru_to_en_results.jsonl` | Large | Colab output |
| `translations/meta.json` | Small | Counts and timestamp |

### Why not pipe `|` or Excel for the main queue?

- **Pipe-separated text** breaks on `|`, newlines, and quotes inside guide prose.
- **Excel (.xlsx)** is fine for a **small sample** (100 rows) to spot-check, but
  awkward for 5k+ cells and multiline paragraphs.
- **JSON / JSONL** is safe for multiline strings and is what export/apply use.

**If the repo is huge:** use `--split-by-city` and upload one city at a time to
Colab (`translations/collab/by_city/chernivtsi_en_to_ru.json`).

**Git:** large `translations/queue/*.jsonl` and `collab/*.json` are gitignored;
copy them via Google Drive or zip. Commit only `meta.json` and `examples/`.

---

## Step 1 — Export (on your PC)

From repo root:

```powershell
# Preview counts (fast audit)
python scripts/audit_guide_edition_gaps.py --cities chernivtsi

# Build translation queue + Colab arrays
python scripts/export_guide_translation_queue.py --cities chernivtsi

# All cities (large — use Drive)
python scripts/export_guide_translation_queue.py

# Per-city files for Colab upload limits
python scripts/export_guide_translation_queue.py --split-by-city --cities prague vologda
```

Example `translations/meta.json`:

```json
{
  "generated_at": "2026-06-02T12:00:00+00:00",
  "cities": ["chernivtsi"],
  "job_count": 84,
  "en_to_ru_count": 52,
  "ru_to_en_count": 32
}
```

Example line in `translations/queue/queue.jsonl`:

```json
{"id": "chernivtsi/chernivtsi_university/description/en-ru", "city": "chernivtsi", "source_file": "chernivtsi/data/chernivtsi_places.json", "slug": "chernivtsi_university", "field": "description", "src_lang": "en", "dst_lang": "ru", "source_text": "Chernivtsi University Residence is a palaces in Chernivtsi.", "target_key": "description_ru", "kind": "prose"}
```

Example Colab input row in `translations/collab/en_to_ru.json`:

```json
{"id": "chernivtsi/chernivtsi_university/description/en-ru", "text": "Chernivtsi University Residence is a palaces in Chernivtsi."}
```

---

## Step 2 — Google Colab

### 2.1 Upload

Upload to Colab (or mount Google Drive):

- `translations/collab/en_to_ru.json` (or `.jsonl`)
- `translations/collab/ru_to_en.json`
- Optionally `translations/queue/queue.jsonl` (for reference only)

For one city only:

- `translations/collab/by_city/chernivtsi_en_to_ru.json`
- `translations/collab/by_city/chernivtsi_ru_to_en.json`

### 2.2 Translate (example pattern)

Use any model/API you trust (Gemini, OpenAI, etc.). Keep **`id`** unchanged;
only fill **`translated`**.

```python
import json
from pathlib import Path

def load_array(path):
    p = Path(path)
    if p.suffix == ".jsonl":
        return [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]
    return json.loads(p.read_text(encoding="utf-8"))

SYSTEM_EN_RU = (
    "Translate city-guide text from English to Russian. "
    "Guidebook tone. Keep dates and proper names. Do not add facts. "
    "Output only the translation, plain text."
)
SYSTEM_RU_EN = (
    "Переведи текст путеводителя с русского на английский. "
    "Тон путеводителя. Сохрани даты и имена. Не добавляй фактов. "
    "Выведи только перевод, plain text."
)

def translate_batch(rows, system_prompt, translate_fn, chunk=40):
    out = []
    for i in range(0, len(rows), chunk):
        block = rows[i : i + chunk]
        for row in block:
            text = translate_fn(row["text"], system_prompt)
            out.append({"id": row["id"], "translated": text})
    return out

# translate_fn = your API call
en_to_ru = load_array("en_to_ru.json")
ru_to_en = load_array("ru_to_en.json")

en_to_ru_results = translate_batch(en_to_ru, SYSTEM_EN_RU, translate_fn)
ru_to_en_results = translate_batch(ru_to_en, SYSTEM_RU_EN, translate_fn)

Path("en_to_ru_results.jsonl").write_text(
    "\n".join(json.dumps(r, ensure_ascii=False) for r in en_to_ru_results),
    encoding="utf-8",
)
Path("ru_to_en_results.jsonl").write_text(
    "\n".join(json.dumps(r, ensure_ascii=False) for r in ru_to_en_results),
    encoding="utf-8",
)
```

### 2.3 Download

Download from Colab:

- `en_to_ru_results.jsonl`
- `ru_to_en_results.jsonl`

Copy into the repo:

```text
translations/results/en_to_ru_results.jsonl
translations/results/ru_to_en_results.jsonl
```

Result line format:

```json
{"id": "chernivtsi/chernivtsi_university/description/en-ru", "translated": "Резиденция Черновицкого университета — дворец в Черновцах."}
```

---

## Step 3 — Apply (on your PC)

Default: write into **overlay** (safe review), same as the web editor:

```powershell
python scripts/apply_guide_translation_results.py --dry-run
python scripts/apply_guide_translation_results.py
```

This updates:

```text
<city>/data/<city>_place_details_more.json
```

slug → `{ "description_ru": "...", "facts_ru": ["...", "..."] }`

To write **directly** into `*_places.json` (bulk, harder to revert):

```powershell
python scripts/apply_guide_translation_results.py --write-places
```

Merge overlay into main JSON when satisfied (manual edit or your own merge script).

---

## Step 4 — Verify and rebuild PDFs

```powershell
python scripts/audit_guide_edition_gaps.py --cities chernivtsi
python scripts/rebuild_stale_city_guide_pdfs.py --cities chernivtsi
```

`rebuild_stale_city_guide_pdfs.py` sets **`CITY_GUIDE_NO_TRANSLATE=1`** by default
(no Ollama during PDF). Use `--with-translate` only if you intentionally want
live fallback.

---

## Where EN/RU text is stored for PDF builds

| Layer | Path | Used by PDF |
|-------|------|-------------|
| Main registry | `<city>/data/<city>_places.json` | Yes |
| PDF expand | `<city>/data/<city>_places_pdf_expand.json` | Yes |
| Overlay | `<city>/data/<city>_place_details_more.json` | Yes (merged) |
| Translation queue | `translations/queue/queue.jsonl` | No (workflow only) |
| Colab results | `translations/results/*.jsonl` | No (apply once) |
| Runtime cache | `.cache/city_guide_translate.json` | Fallback only; do not rely on it |

**Convention after apply:**

- RU PDF reads: `description_ru`, `history_ru`, `significance_ru`, `facts_ru`, `name_ru`
- EN PDF reads: `description_en` / `description`, `history_en` / `history`, …

---

## Optional: small Excel sample

For human review of **names only** (not full queue):

```powershell
python scripts/export_guide_translation_queue.py --cities vologda
```

In Colab, load `en_to_ru.json` with pandas, filter `kind == "name"`, export 50
rows to `sample_names.xlsx`, translate manually, then merge back into
`en_to_ru_results.jsonl` by `id`.

---

## Troubleshooting

| Issue | Action |
|-------|--------|
| `need EN->RU` still high after apply | Overlay not merged into places; re-run audit; check `target_key` in queue |
| Colab timeout | Use `--split-by-city`; smaller `chunk` in translate loop |
| Wrong language in PDF | `text_for_edition` rejected text; fix translation or encoding |
| PDF still calls Ollama | Rebuild without `--with-translate`; ensure JSON has `*_ru` / `*_en` fields |

---

## Scripts reference

| Script | Role |
|--------|------|
| `scripts/export_guide_translation_queue.py` | Build queue + Colab JSON/JSONL |
| `scripts/apply_guide_translation_results.py` | Merge results into overlay or places |
| `scripts/guide_translation_queue.py` | Shared queue logic |
| `scripts/audit_guide_edition_gaps.py` | Count gaps (`need EN->RU`, `need RU->EN`) |
| `scripts/fill_sparse_guide_narratives.py` | LLM fill when **no** opposite text |
| `scripts/rebuild_stale_city_guide_pdfs.py` | PDF rebuild (no translate by default) |
