# One-shot rebuild: all city guides

Use this checklist to refresh **images**, **validate sources**, and **build HTML/PDF**
for every per-city guide in the repo. Run commands from the repository root
(`Excursion/`). Requires Python 3, `pip install -r requirements.txt`, and for PDF
output: `playwright install chromium`.

**Editorial policy** (facts, omitting unsourced fields): see
[City guides README — Editorial policy](CITY_GUIDES_README.md#editorial-policy-facts-and-sources).

---

## All cities (17)

| City folder | Download images | Validate sources | Build HTML + PDF |
|-------------|-----------------|------------------|------------------|
| `barcelona/` | `python scripts/download_barcelona_images.py` | `python scripts/validate_barcelona_sources.py` | `python scripts/build_barcelona_pdf.py` |
| `berlin/` | `python scripts/download_berlin_images.py` | `python scripts/validate_berlin_sources.py` | `python scripts/build_berlin_pdf.py` |
| `boston/` | `python scripts/download_boston_images.py` | `python scripts/validate_boston_sources.py` | `python scripts/build_boston_pdf.py` |
| `budapest/` | `python scripts/download_budapest_images.py` | `python scripts/validate_budapest_sources.py` | `python scripts/build_budapest_pdf.py` |
| `florence/` | `python scripts/download_florence_images.py` | `python scripts/validate_florence_sources.py` | `python scripts/build_florence_pdf.py` |
| `jerusalem/` | `python scripts/download_jerusalem_images.py` | `python scripts/validate_jerusalem_sources.py` | `python scripts/build_jerusalem_pdf.py` |
| `madrid/` | `python scripts/download_madrid_images.py` | `python scripts/validate_madrid_sources.py` | `python scripts/build_madrid_pdf.py` |
| `montreal/` | `python scripts/download_montreal_images.py` | `python scripts/validate_montreal_sources.py` | `python scripts/build_montreal_pdf.py` |
| `new_york/` | `python scripts/download_new_york_images.py` | `python scripts/validate_new_york_sources.py` | `python scripts/build_new_york_pdf.py` |
| `paris/` | `python scripts/download_paris_images.py` | `python scripts/validate_paris_sources.py` | `python scripts/build_paris_pdf.py` |
| `philadelphia/` | `python scripts/download_philadelphia_images.py` | `python scripts/validate_philadelphia_sources.py` | `python scripts/build_philadelphia_pdf.py` |
| `prague/` | `python scripts/download_prague_images.py` | `python scripts/validate_prague_sources.py` | `python scripts/build_prague_pdf.py` |
| `rome/` | `python scripts/download_rome_images.py` | `python scripts/validate_rome_sources.py` | `python scripts/build_rome_pdf.py` |
| `smolensk/` | `python scripts/download_smolensk_images.py` | `python scripts/validate_smolensk_sources.py` | `python scripts/build_smolensk_pdf.py` |
| `spb/` | `python scripts/download_spb_images.py` | `python scripts/validate_spb_sources.py` | `python scripts/build_spb_pdf.py` |
| `venice/` | `python scripts/download_venice_images.py` | `python scripts/validate_venice_sources.py` | `python scripts/build_venice_pdf.py` |
| `vienna/` | `python scripts/download_vienna_images.py` | `python scripts/validate_vienna_sources.py` | `python scripts/build_vienna_pdf.py` |

**Optional:** HTML only (no PDF) where supported, e.g.
`python scripts/build_budapest_pdf.py --html-only` (see each script’s `--help`).

**Registry stats table** (place counts, missing fields):  
`python scripts/report_city_guide_stats.py --write`

---

## Copy-paste: sequential (PowerShell / bash)

Run download → validate → build per city, or chain the three commands for one city
before moving to the next.

**Example: Smolensk only**

```bash
python scripts/download_smolensk_images.py
python scripts/validate_smolensk_sources.py
python scripts/build_smolensk_pdf.py
```

**Example: loop all (bash) — adjust if a script fails**

```bash
for city in barcelona berlin boston budapest florence jerusalem madrid montreal new_york paris philadelphia prague rome smolensk spb venice vienna; do
  python scripts/download_${city}_images.py || exit 1
  python scripts/validate_${city}_sources.py || exit 1
  python scripts/build_${city}_pdf.py || exit 1
done
```

On Windows PowerShell, run the three commands per city from the table or use a
small script that calls `python scripts/download_<city>_images.py` etc.

---

## Outputs

| City | Typical output folder |
|------|------------------------|
| Most Latin/Cyrillic guides | `<city>/output/<city>_guide.html` and `.pdf` |
| SPB | `spb/output/` (see `spb/README.md`) |

Smolensk: `smolensk/output/smolensk_guide.html`, `smolensk_guide.pdf`.

---

## Full prompt for an AI assistant (one-shot)

You can paste the block below into a Cursor chat to rebuild every guide after
data or JSON changes:

```text
From the Excursion repo root, for each city in:
barcelona, berlin, boston, budapest, florence, jerusalem, madrid, montreal,
new_york, paris, philadelphia, prague, rome, smolensk, spb, venice, vienna:

1. Run: python scripts/download_<city>_images.py
2. Run: python scripts/validate_<city>_sources.py (fix any whitelist/source issues)
3. Run: python scripts/build_<city>_pdf.py

Then run: python scripts/report_city_guide_stats.py --write
and commit docs/CITY_GUIDES_README.md if the stats table changed.

Follow docs/CITY_GUIDES_README.md editorial policy for facts.
Use each city’s README for path flags and --html-only if PDF is not needed.
```
