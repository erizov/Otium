# -*- coding: utf-8 -*-
"""Run every scripts/build_<slug>_pdf.py for cities with data/<slug>_places.json."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _discover_slugs(project_root: Path) -> list[str]:
    scripts_dir = project_root / "scripts"
    out: list[str] = []
    for path in sorted(scripts_dir.glob("build_*_pdf.py")):
        stem = path.stem
        if not stem.startswith("build_") or not stem.endswith("_pdf"):
            continue
        slug = stem[len("build_") : -len("_pdf")]
        if not slug:
            continue
        places = project_root / slug / "data" / "{}_places.json".format(slug)
        if places.is_file():
            out.append(slug)
    return out


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    slugs = _discover_slugs(root)
    if not slugs:
        print("No cities with data/<slug>_places.json found.", file=sys.stderr)
        return 2
    failed: list[tuple[str, int]] = []
    for i, slug in enumerate(slugs, start=1):
        script = root / "scripts" / "build_{}_pdf.py".format(slug)
        print(
            "[{}/{}] Building {} ...".format(i, len(slugs), slug),
            flush=True,
        )
        proc = subprocess.run(
            [sys.executable, str(script)],
            cwd=str(root),
            check=False,
        )
        if proc.returncode != 0:
            failed.append((slug, int(proc.returncode)))
    print(
        "Done: {} ok, {} failed.".format(
            len(slugs) - len(failed),
            len(failed),
        ),
        flush=True,
    )
    if failed:
        for slug, code in failed:
            print("  FAIL {} exit {}".format(slug, code), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
