# -*- coding: utf-8 -*-
"""
Workflow: backup, download images, cross-guide deduplication, then build guides.

1. Backup: copy output/<guide>_guide.{html,pdf} to output/backup/ with
   rotation; keep only 3 backups per guide (_1, _2, _3; newest is _1).
2. Download: for each guide run build_pdf.py --guide <name> --download-only
   (downloads images into output/images/<subdir>, validates map URLs).
3. Deduplicate: scan all output/images/*; group files by content hash
   (perceptual hash); for each group with files from multiple guides, keep
   the file from the highest-priority guide and delete the others.
4. Build: run build_pdf.py --guide <name> for each guide (writes HTML/PDF).

Usage: python scripts/workflow_build_guides.py
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent
BACKUP_DIR_NAME = "backup"
MAX_BACKUPS_PER_GUIDE = 3
MIN_IMAGE_BYTES = 500

# Subdir name (under output/images/) -> guide key for priority
SUBDIR_TO_GUIDE = {
    "moscow_monasteries": "monastery",
    "moscow_places_of_worship": "places_of_worship",
    "moscow_parks": "park",
    "moscow_museums": "museum",
    "moscow_palaces": "palace",
    "moscow_buildings": "building",
    "moscow_sculptures": "sculpture",
    "moscow_places": "place",
    "moscow_metro": "metro",
}

# Highest (0) to lowest (8)
GUIDE_PRIORITY = {
    "monastery": 0,
    "places_of_worship": 1,
    "palace": 2,
    "building": 3,
    "park": 4,
    "museum": 5,
    "metro": 6,
    "place": 7,
    "sculpture": 8,
}

GUIDES = [
    "monasteries",
    "places_of_worship",
    "parks",
    "museums",
    "palaces",
    "buildings",
    "sculptures",
    "places",
    "metro",
]


def _rotate_backup(backup_dir: Path, guide: str, ext: str) -> None:
    """
    Rotate backups for one guide and extension: current output file
    is copied to backup/<guide>_guide_1<ext>; previous _1 -> _2, _2 -> _3;
    _3 is removed. Keeps at most MAX_BACKUPS_PER_GUIDE.
    """
    output_dir = _PROJECT_ROOT / "output"
    base = "{}_guide".format(guide)
    src = output_dir / (base + ext)
    if not src.exists():
        return
    backup_dir.mkdir(parents=True, exist_ok=True)
    # Shift from oldest to newest so we don't overwrite before reading
    oldest = backup_dir / (base + "_{}".format(MAX_BACKUPS_PER_GUIDE) + ext)
    if oldest.exists():
        oldest.unlink()
    for i in range(MAX_BACKUPS_PER_GUIDE - 1, 0, -1):
        prev = backup_dir / (base + "_{}".format(i) + ext)
        next_path = backup_dir / (base + "_{}".format(i + 1) + ext)
        if prev.exists():
            shutil.copy2(prev, next_path)
    dest1 = backup_dir / (base + "_1" + ext)
    shutil.copy2(src, dest1)


def backup_guides(output_dir: Path, backup_dir: Path) -> None:
    """Backup existing guide HTML and PDF; keep 3 per guide."""
    for guide in GUIDES:
        for ext in [".html", ".pdf"]:
            src = output_dir / ("{}_guide".format(guide) + ext)
            if src.exists():
                _rotate_backup(backup_dir, guide, ext)
                print("Backed up {}_guide{}".format(guide, ext))


def download_all_guides() -> int:
    """Run build_pdf.py --guide <name> --download-only for each guide."""
    python = sys.executable
    build_script = _SCRIPT_DIR / "build_pdf.py"
    if not build_script.is_file():
        print("Error: build_pdf.py not found.", file=sys.stderr)
        return 1
    failed: list[str] = []
    for guide in GUIDES:
        print("\n--- Downloading images for guide: {} ---".format(guide))
        ret = subprocess.call(
            [python, str(build_script), "--guide", guide, "--download-only"],
            cwd=str(_PROJECT_ROOT),
        )
        if ret != 0:
            failed.append(guide)
    if failed:
        print(
            "Download failed for: {}.".format(", ".join(failed)),
            file=sys.stderr,
        )
        return 1
    print("\nAll guide images downloaded.")
    return 0


def cross_guide_dedup(images_root: Path) -> int:
    """
    Find duplicate images across guides by content hash. Keep the file from
    the highest-priority guide as canonical; for every other path with the
    same hash, overwrite only if the target has the same slug (same logical
    item). If canonical and target slugs differ, skip replace and log.
    Returns number of files replaced.
    """
    if str(_PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(_PROJECT_ROOT))
    from scripts.image_utils import image_content_hash
    from scripts.slug_item_map import basename_to_slug

    hash_to_entries: dict[str, list[tuple[str, Path]]] = {}
    if not images_root.exists():
        return 0
    for subdir_path in images_root.iterdir():
        if not subdir_path.is_dir():
            continue
        guide = SUBDIR_TO_GUIDE.get(subdir_path.name)
        if guide is None:
            continue
        for path in subdir_path.iterdir():
            if not path.is_file():
                continue
            if path.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
                continue
            if path.stat().st_size < MIN_IMAGE_BYTES:
                continue
            h = image_content_hash(path, min_bytes=MIN_IMAGE_BYTES)
            if not h:
                continue
            if h not in hash_to_entries:
                hash_to_entries[h] = []
            hash_to_entries[h].append((guide, path))
    replaced = 0
    for h, entries in hash_to_entries.items():
        if len(entries) <= 1:
            continue
        # Sort by priority (lower number = keep first as canonical)
        entries.sort(key=lambda x: (GUIDE_PRIORITY.get(x[0], 99), x[1].name))
        keep_guide, keep_path = entries[0]
        keep_slug = basename_to_slug(keep_path.name)
        for guide, path in entries[1:]:
            path_slug = basename_to_slug(path.name)
            if keep_slug != path_slug:
                print(
                    "  Same content, different items — skipped replace: "
                    "{} ({} from {}) vs {} ({} from {})".format(
                        path.name, path_slug, guide,
                        keep_path.name, keep_slug, keep_guide,
                    ),
                )
                continue
            try:
                shutil.copy2(keep_path, path)
                replaced += 1
                print(
                    "  Replaced duplicate ({}): {} (with {} from {})".format(
                        h[:12], path.name, keep_path.name, keep_guide,
                    ),
                )
            except OSError as e:
                print(
                    "  Warning: could not replace {}: {}".format(path, e),
                    file=sys.stderr,
                )
    return replaced


def validate_images(output_dir: Path) -> int:
    """
    Run validate_images_per_item.py: every item must have 4 images with
    distinct DOWNLOADS. Returns 0 if validation passes.
    """
    python = sys.executable
    val_script = _SCRIPT_DIR / "validate_images_per_item.py"
    if not val_script.is_file():
        print("Error: validate_images_per_item.py not found.", file=sys.stderr)
        return 1
    ret = subprocess.call(
        [python, str(val_script)],
        cwd=str(_PROJECT_ROOT),
    )
    return ret


def build_all(output_dir: Path) -> int:
    """Run build_pdf.py for each guide. Returns 0 on success."""
    python = sys.executable
    build_script = _SCRIPT_DIR / "build_pdf.py"
    if not build_script.is_file():
        print("Error: build_pdf.py not found.", file=sys.stderr)
        return 1
    failed: list[str] = []
    for guide in GUIDES:
        print("\n--- Building guide: {} ---".format(guide))
        ret = subprocess.call(
            [python, str(build_script), "--guide", guide],
            cwd=str(_PROJECT_ROOT),
        )
        if ret != 0:
            failed.append(guide)
    if failed:
        print(
            "\nFailed guides: {}.".format(", ".join(failed)),
            file=sys.stderr,
        )
        return 1
    print("\nAll guides built successfully.")
    return 0


def main() -> int:
    output_dir = _PROJECT_ROOT / "output"
    output_dir.mkdir(exist_ok=True)
    backup_dir = output_dir / BACKUP_DIR_NAME
    images_root = output_dir / "images"

    print("Step 1: Backing up existing guides (keep {} per guide)...".format(
        MAX_BACKUPS_PER_GUIDE,
    ))
    backup_guides(output_dir, backup_dir)

    print("\nStep 2: Downloading images for all guides...")
    if download_all_guides() != 0:
        return 1

    print("\nStep 3: Cross-guide deduplication (by content hash)...")
    replaced = cross_guide_dedup(images_root)
    if replaced:
        print("  Replaced {} duplicate image(s) with canonical copy.".format(
            replaced,
        ))
    else:
        print("  No cross-guide duplicate images found.")

    print("\nStep 4: Validate 4 images per item (no empty, no duplicate URLs)...")
    skip_val = os.environ.get("SKIP_IMAGE_VALIDATION", "").strip().lower()
    if skip_val in ("1", "true", "yes"):
        print("  Skipped (SKIP_IMAGE_VALIDATION is set).")
    elif validate_images(output_dir) != 0:
        print(
            "Validation failed. Fix data/*.py and data/*_image_urls.py so "
            "every item has exactly 4 images with distinct DOWNLOADS. Set "
            "SKIP_IMAGE_VALIDATION=1 to build PDFs anyway (e.g. 2 images per "
            "item until expansion is done).",
            file=sys.stderr,
        )
        return 1

    print("\nStep 5: Building all guides...")
    return build_all(output_dir)


if __name__ == "__main__":
    sys.exit(main())
