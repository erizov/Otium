# -*- coding: utf-8 -*-
from __future__ import annotations

"""Count JPG files in each output/images subfolder (excluding forbidden)."""

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

OUTPUT_IMAGES_DIR = _PROJECT_ROOT / "output" / "images"
FORBIDDEN_SUBDIR = "forbidden"


def count_jpgs_in_folder(folder: Path) -> int:
    """Count .jpg and .jpeg files in folder."""
    count = 0
    if not folder.exists() or not folder.is_dir():
        return 0
    for path in folder.iterdir():
        if not path.is_file():
            continue
        if path.suffix.lower() in (".jpg", ".jpeg"):
            count += 1
    return count


def main() -> int:
    """Print JPG counts per subfolder."""
    if not OUTPUT_IMAGES_DIR.exists():
        print("Output images directory not found: {}".format(OUTPUT_IMAGES_DIR))
        return 1

    results: list[tuple[str, int]] = []
    total = 0

    for subfolder in sorted(OUTPUT_IMAGES_DIR.iterdir()):
        if not subfolder.is_dir():
            continue
        if subfolder.name == FORBIDDEN_SUBDIR:
            continue
        count = count_jpgs_in_folder(subfolder)
        results.append((subfolder.name, count))
        total += count

    if not results:
        print("No subfolders found in {}".format(OUTPUT_IMAGES_DIR))
        return 0

    print("JPG files per subfolder (excluding forbidden/):")
    print("-" * 50)
    for name, count in results:
        print("  {:40s} {:6d}".format(name, count))
    print("-" * 50)
    print("  {:40s} {:6d}".format("TOTAL", total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
