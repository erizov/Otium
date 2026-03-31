# -*- coding: utf-8 -*-
"""Rebuild city guide PDFs when the PDF is older than newest file in city/."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

_SKIP_SLUGS = frozenset({"spb", "moscow", "msk"})


def _slug_from_script(path: Path) -> str | None:
    name = path.name
    if not name.startswith("build_") or not name.endswith("_pdf.py"):
        return None
    return name[len("build_") : -len("_pdf.py")]


def _all_build_slugs() -> list[str]:
    scripts = _PROJECT_ROOT / "scripts"
    slugs: list[str] = []
    for path in scripts.glob("build_*_pdf.py"):
        s = _slug_from_script(path)
        if s and s not in _SKIP_SLUGS:
            slugs.append(s)
    return sorted(slugs)


def _newest_mtime_except(root: Path, skip: Path) -> float | None:
    best: float | None = None
    try:
        resolved_skip = skip.resolve()
    except OSError:
        resolved_skip = skip
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if "__pycache__" in path.parts:
            continue
        if path.name.endswith(".pyc"):
            continue
        try:
            if path.resolve() == resolved_skip:
                continue
        except OSError:
            continue
        try:
            m = path.stat().st_mtime
        except OSError:
            continue
        if best is None or m > best:
            best = m
    return best


def _pdf_path(slug: str) -> Path:
    return _PROJECT_ROOT / slug / "output" / "{}_guide.pdf".format(slug)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions only; do not run build scripts.",
    )
    args = parser.parse_args()

    for slug in _all_build_slugs():
        city_root = _PROJECT_ROOT / slug
        pdf = _pdf_path(slug)
        if not city_root.is_dir():
            print("skip (no dir): {}".format(slug), file=sys.stderr)
            continue

        newest = _newest_mtime_except(city_root, pdf)
        try:
            pdf_m = pdf.stat().st_mtime if pdf.is_file() else None
        except OSError:
            pdf_m = None

        stale = pdf_m is None or (
            newest is not None and newest > pdf_m
        )
        if not stale:
            print("ok {}".format(slug))
            continue

        reason = "missing pdf" if pdf_m is None else "newer sources"
        print("rebuild {} ({})".format(slug, reason))
        if args.dry_run:
            continue
        script = _PROJECT_ROOT / "scripts" / "build_{}_pdf.py".format(slug)
        rc = subprocess.run(
            [sys.executable, str(script)],
            cwd=str(_PROJECT_ROOT),
            check=False,
        ).returncode
        if rc != 0:
            print("FAILED {} (exit {})".format(slug, rc), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
