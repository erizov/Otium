# -*- coding: utf-8 -*-
"""Print Moscow osobnjaki bootstrap status for loop monitoring."""

from __future__ import annotations

import json
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from moscow.data.osobnjaki import IMAGES_SUBFOLDER, OSOBNJAKI, OSOBNJAKI_CORE
from scripts.city_guide_core import MIN_IMAGE_BYTES


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    img_dir = _PROJECT_ROOT / "moscow" / "images" / IMAGES_SUBFOLDER
    img_dir.mkdir(parents=True, exist_ok=True)

    valid: dict[str, int] = {}
    for path in img_dir.glob("*.jpg"):
        if path.stat().st_size >= MIN_IMAGE_BYTES:
            prefix = path.stem.rsplit("_", 1)[0]
            valid[prefix] = valid.get(prefix, 0) + 1

    complete = 0
    partial: list[str] = []
    missing: list[str] = []
    for item in OSOBNJAKI:
        name = item["name"]
        slug_prefix = None
        for img in item["images"]:
            slug_prefix = Path(img).name.rsplit("_", 1)[0]
            break
        count = valid.get(slug_prefix or "", 0)
        if count >= 4:
            complete += 1
        elif count:
            partial.append("{} ({}/4)".format(name, count))
        else:
            missing.append(name)

    places_path = _PROJECT_ROOT / "moscow" / "data" / "moscow_places.json"
    total_json = 0
    osobnjaki_json = 0
    if places_path.is_file():
        rows = json.loads(places_path.read_text(encoding="utf-8"))
        total_json = len(rows)
        osobnjaki_json = sum(
            1 for r in rows if r.get("category") == "osobnjaki"
        )

    batch1_expected = len(OSOBNJAKI_CORE) * 4
    batch2_expected = (len(OSOBNJAKI) - len(OSOBNJAKI_CORE)) * 4
    batch1_complete = 0
    batch2_complete = 0
    for item in OSOBNJAKI_CORE:
        prefix = Path(item["images"][0]).name.rsplit("_", 1)[0]
        if valid.get(prefix, 0) >= 4:
            batch1_complete += 1
    for item in OSOBNJAKI[len(OSOBNJAKI_CORE):]:
        prefix = Path(item["images"][0]).name.rsplit("_", 1)[0]
        if valid.get(prefix, 0) >= 4:
            batch2_complete += 1

    valid_files = sum(valid.values())
    expected = len(OSOBNJAKI) * 4
    print("=== Moscow osobnjaki status ===")
    print("Places in data: {} (batch1 {}, batch2 {})".format(
        len(OSOBNJAKI), len(OSOBNJAKI_CORE), len(OSOBNJAKI) - len(OSOBNJAKI_CORE),
    ))
    print("JSON export: {} osobnjaki / {} total".format(
        osobnjaki_json, total_json,
    ))
    print("Images: {} / {} valid (batch1 {}/{}, batch2 {}/{})".format(
        valid_files,
        expected,
        batch1_complete,
        len(OSOBNJAKI_CORE),
        batch2_complete,
        len(OSOBNJAKI) - len(OSOBNJAKI_CORE),
    ))
    if partial:
        print("Partial ({}): {}".format(len(partial), "; ".join(partial[:5])))
        if len(partial) > 5:
            print("  … +{} more".format(len(partial) - 5))
    if missing:
        print("Not started ({}): {}".format(
            len(missing), "; ".join(missing[:5]),
        ))
        if len(missing) > 5:
            print("  … +{} more".format(len(missing) - 5))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
