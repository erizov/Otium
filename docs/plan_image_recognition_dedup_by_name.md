# Plan: Improve Image Recognition and Deduplication by Item Name

## Current behaviour

- **Image assignment**: Each guide item has a list of image filenames (e.g. `red_square_1.jpg`). These map to URLs in `*_image_urls.py` (e.g. `PLACE_IMAGE_DOWNLOADS`). Filenames are effectively slugs derived from item names (e.g. «Красная площадь» → `red_square`).
- **Deduplication**: `workflow_build_guides.py` runs cross-guide dedup by **content hash** (perceptual hash or SHA256). For each group of identical images, the file from the **highest-priority guide** is kept; all other paths are **overwritten** with that file so each guide still has its expected filenames.
- **Gap**: Dedup ignores **item name** and **filename/slug**. So `red_square_1.jpg` in `moscow_places` can be overwritten with the same bytes as `ostankino_1.jpg` from `moscow_palaces` if they hash the same. The result is the wrong visual for the item name (e.g. Red Square showing a palace). There is no check that the image content or source URL matches the item name.

## Goals

1. **Name–image consistency**: Ensure the image shown for an item is appropriate for that item’s name (no wrong attribution after dedup or in source URLs).
2. **Name-aware deduplication**: When resolving duplicate content hashes, take into account item name / slug so we don’t replace an image for item A with an image that “belongs” to item B.
3. **Recognition and validation**: Optionally validate that URLs or downloaded images match the intended item (by slug/name), and improve future URL choice or dedup rules using item names.

## Proposed improvements

### 1. Name-aware dedup (high impact, no new deps)

**Idea**: When grouping by content hash, we have `(guide, path)` per file. Each path has a basename like `red_square_1.jpg` → slug `red_square`. Use slug as a proxy for “item name”.

- **Rule**: When choosing which file to keep as canonical for a given hash, prefer the one whose **slug appears in the same guide’s item list** (e.g. places has an item with images containing `red_square_*.jpg`). If only one file in the group has a slug that matches an item in its guide, keep that one; otherwise fall back to current guide priority.
- **Refinement**: When **replacing** a file, if the **target** path’s slug (e.g. `red_square_1`) and the **canonical** path’s slug (e.g. `ostankino_1`) differ, **do not overwrite**: leave the lower-priority file as-is and log “same content, different items — skipped replace”. That way we only replace when it’s the same logical item (same slug) or when we explicitly allow cross-item replacement. Build may then show “duplicate” bytes in two files; we can later add a second pass that fills missing or duplicate slots from a pool, or accept two copies for different items.
- **Data**: Each guide’s items and their `images` lists are in `data/<guide>.py`. The workflow (or a small helper) can load “for guide G, set of slugs that appear in any item’s images” and pass that into `cross_guide_dedup`.

**Files to change**: `scripts/workflow_build_guides.py` (and/or `scripts/image_utils.py`), optionally `scripts/dedup_by_priority.py` if we want a standalone dedup script that respects names.

### 2. Slug–item mapping and validation (medium impact)

**Idea**: Derive a single source of truth: “slug → item name (and guide)”.

- **Build a map**: When loading guides, build `(guide, slug) → item_name` (e.g. `("places", "red_square") → "Красная площадь"`). Use the same slug logic as today (e.g. from image basename: strip `_N.jpg` to get slug).
- **Use in dedup**: In name-aware dedup, use this map to compare “canonical file’s item name” vs “replaced file’s item name”. Only overwrite if same slug or same item name (e.g. same place in two guides) or by explicit rule.
- **Validation script**: Add `scripts/validate_image_item_names.py` (or extend `validate_images_per_item.py`): for each image file in `output/images/<subdir>`, check that (guide, slug) exists in the map and that the item has that image in its list. Optionally in the future: call an image-tagging or CLIP API to check that the image content is consistent with the item name (e.g. “Red Square” vs “palace”); start as a manual or optional check.

**Files**: New or extended validation script; `scripts/workflow_build_guides.py` (or shared module in `scripts/`) to build slug→item map from `data/*.py`.

### 3. URL assignment and “recognition” at source (medium/long term)

**Idea**: Reduce wrong images at the source so dedup has fewer bad cases.

- **Naming convention**: Enforce that DOWNLOADS keys are always `{slug}_{1..4}.jpg` (or similar) and that slug is derived from the same item name used in the guide (e.g. from `places.py`). Document this in README and in `cursor_prompt.md` so new items get correct slugs.
- **Optional checks when editing data**: A small script or CI check: for each (guide, slug) in DOWNLOADS, verify that an item in that guide has that slug in its `images` list; otherwise warn “orphan image key” or “missing image for item”.
- **Future**: If we have Commons/Wikidata URLs, we could check that the URL’s title or metadata mentions the place name (or a known alias). That would be a lightweight “recognition” step before download.

### 4. Optional: content–name consistency (lower priority, new deps)

**Idea**: After download (or after dedup), check that image **content** is not clearly wrong for the item name.

- **Options**: (a) Offline: run a small classifier or CLIP-style model (e.g. “Red Square” vs “palace”) and flag mismatches; (b) use a third-party API that returns tags or scene labels and compare to item name. This is heavier and optional; name-aware dedup and slug validation already reduce most misattribution.

## Implementation order

1. **Slug–item map**: Add a small function (or script) that loads all guides and returns `(guide, slug) → item_name` (and optionally “slug set per guide”). Use the same basename→slug rule as in build (e.g. `red_square_1.jpg` → `red_square`).
2. **Name-aware dedup**: In `cross_guide_dedup`, load the slug–item map; when deciding to overwrite, compare canonical vs target slug (and optionally item names). If they differ, skip overwrite and log. Optionally prefer as canonical the file whose (guide, slug) exists in the map.
3. **Validation**: Extend or add validation so every image file in `output/images/*` is checked against the slug–item map and the item’s `images` list; fail or warn if a file’s slug is not tied to any item or if an item is missing an image.
4. **Docs and conventions**: Document slug rules and “one URL per object” in README; add a note in `cursor_prompt.md` for future data edits.
5. **Optional**: Content–name consistency (CLIP/API) only if needed after 1–4.

## Success criteria

- After workflow run, no file is overwritten by a different item’s image (different slug) when we could avoid it.
- Validation ensures every image filename is tied to an item and every item has the expected number of images (existing strict/default rules).
- New or updated guides follow slug-from-item-name and one-URL-per-object so that name-aware dedup and validation stay effective.

---

## Implementation steps (done)

1. **Slug–item map** — **scripts/slug_item_map.py**
   - `basename_to_slug(basename)`: strip extension and trailing `_N` (e.g. `red_square_1.jpg` → `red_square`).
   - `get_slug_to_item_name(project_root)`: load all guides, return `(guide, slug) -> item_name`.
   - `get_slugs_per_guide(project_root)`: `guide -> set(slugs)` for that guide.

2. **Name-aware dedup** — **scripts/workflow_build_guides.py** `cross_guide_dedup()`
   - For each duplicate group, compute `keep_slug` and `path_slug` from basenames.
   - If `keep_slug != path_slug`: skip overwrite, log “Same content, different items — skipped replace”.
   - If same slug: replace as before (same logical item).

3. **Validation** — **scripts/validate_images_per_item.py**
   - `--check-slugs`: scan `output/images/<subdir>`, for each file get `(guide, slug)` from subdir name and basename; ensure `(guide, slug)` is in the slug–item map; report errors otherwise.
   - `SUBDIR_TO_GUIDE` added for subdir → guide mapping.

4. **Docs** — **README.md**
   - New subsection “Имена файлов изображений и дедупликация по имени объекта”: slug rules, one URL per object, name-aware dedup behaviour, `--check-slugs` usage.
