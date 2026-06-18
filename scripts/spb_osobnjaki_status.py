# -*- coding: utf-8 -*-
"""Print SPB osobnjaki bootstrap status."""

from __future__ import annotations

import json
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from spb.data.osobnjaki import IMAGES_SUBFOLDER, OSOBNJAKI, OSOBNJAKI_CORE
from scripts.city_guide_core import MIN_IMAGE_BYTES


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    img_dir = _PROJECT_ROOT / "spb" / "images" / IMAGES_SUBFOLDER
    img_dir.mkdir(parents=True, exist_ok=True)

    valid: dict[str, int] = {}
    for path in img_dir.glob("*.jpg"):
        if path.stat().st_size >= MIN_IMAGE_BYTES:
            prefix = path.stem.rsplit("_", 1)[0]
            valid[prefix] = valid.get(prefix, 0) + 1

    complete = partial = 0
    partial_names: list[str] = []
    missing: list[str] = []
    for item in OSOBNJAKI:
        name = item["name"]
        prefix = Path(item["images"][0]).name.rsplit("_", 1)[0]
        count = valid.get(prefix, 0)
        if count >= 4:
            complete += 1
        elif count:
            partial += 1
            partial_names.append("{} ({}/4)".format(name, count))
        else:
            missing.append(name)

    json_path = _PROJECT_ROOT / "spb" / "data" / "spb_places_osobnjaki.json"
    json_count = 0
    if json_path.is_file():
        json_count = len(json.loads(json_path.read_text(encoding="utf-8")))

    batch2_n = len(OSOBNJAKI) - len(OSOBNJAKI_CORE)
    b1_ok = sum(
        1 for item in OSOBNJAKI_CORE
        if valid.get(Path(item["images"][0]).name.rsplit("_", 1)[0], 0) >= 4
    )
    b2_ok = complete - b1_ok

    print("=== SPB osobnjaki status ===")
    print("Places in data: {} (batch1 {}, batch2 {})".format(
        len(OSOBNJAKI), len(OSOBNJAKI_CORE), batch2_n,
    ))
    print("JSON export: {} osobnjaki".format(json_count))
    print("Images: {} / {} valid (batch1 {}/{}, batch2 {}/{})".format(
        sum(valid.values()),
        len(OSOBNJAKI) * 4,
        b1_ok,
        len(OSOBNJAKI_CORE),
        b2_ok,
        batch2_n,
    ))
    if partial_names:
        print("Partial ({}): {}".format(
            len(partial_names), "; ".join(partial_names[:5]),
        ))
    if missing:
        print("Not started ({}): {}".format(
            len(missing), "; ".join(missing[:5]),
        ))
        if len(missing) > 5:
            print("  … +{} more".format(len(missing) - 5))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
