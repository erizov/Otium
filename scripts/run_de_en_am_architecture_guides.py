# -*- coding: utf-8 -*-
"""Build German, English, and American architecture guides."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULES = (
    "german_architecture",
    "english_architecture",
    "american_architecture",
)
PY = sys.executable


def _run(cmd: list[str], *, check: bool = True) -> int:
    print("+", " ".join(cmd), flush=True)
    result = subprocess.run(cmd, cwd=ROOT, check=False)
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode,
            cmd,
        )
    return int(result.returncode or 0)


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skip-setup",
        action="store_true",
        help="Skip bootstrap, pool setup, and catalog writes.",
    )
    parser.add_argument(
        "--allow-alt-sources",
        action="store_true",
        help="Allow Flickr / Openverse / Geograph (not Commons-only).",
    )
    parser.add_argument(
        "--modules",
        nargs="*",
        default=list(MODULES),
    )
    args = parser.parse_args()

    if not args.skip_setup:
        _run([
            PY,
            "scripts/bootstrap_architecture_module.py",
            *args.modules,
        ])
        _run([PY, "scripts/setup_european_architecture_modules.py"])
        _run([
            PY,
            "scripts/write_architecture_module_catalogs.py",
            *args.modules,
        ])

    summary: dict[str, dict[str, int]] = {}
    for mod in args.modules:
        _run([
            PY,
            "scripts/generate_architecture_guide.py",
            "--module",
            mod,
            "--no-link-images",
        ])
        resolve_cmd = [
            PY,
            "scripts/resolve_architecture_guide_images.py",
            "--module",
            mod,
            "--commons-delay",
            "3.5",
            "--commons-api-gap",
            "4.5",
            "--pause-429",
            "55",
        ]
        if not args.allow_alt_sources:
            resolve_cmd.append("--commons-only")
        _run(resolve_cmd, check=False)
        _run([
            PY,
            "scripts/filter_architecture_guide_commons_only.py",
            "--module",
            mod,
        ])
        _run([
            PY,
            "scripts/build_architecture_guide_pdf.py",
            "--module",
            mod,
            "--lang",
            "ru",
            "en",
        ])
        places_path = ROOT / mod / "data" / "{}_places.json".format(mod)
        rows = json.loads(places_path.read_text(encoding="utf-8"))
        missing_path = ROOT / mod / "data" / "missing_but_wanted.json"
        missing = json.loads(missing_path.read_text(encoding="utf-8"))
        summary[mod] = {
            "success": len(rows),
            "failed": len(missing),
            "attempted": len(rows) + len(missing),
        }

    report_path = ROOT / "translations" / "meta" / "de_en_am_architecture_build.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("\n=== Summary ===")
    for mod, stats in summary.items():
        print(
            "{}: success={} failed={} attempted={}".format(
                mod,
                stats["success"],
                stats["failed"],
                stats["attempted"],
            ),
        )
    print("Report:", report_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
