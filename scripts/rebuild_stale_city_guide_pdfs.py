# -*- coding: utf-8 -*-
"""Rebuild per-city guide PDFs when inputs are newer than the output PDF.

Typical inputs: ``<slug>/data/*.json``, ``<slug>/images/**`` (common raster
and SVG extensions), ``<slug>/docs/SOURCES_WHITELIST.md``, and
``scripts/build_<slug>_pdf.py``. Compares the latest modification time among
those files to ``<slug>/output/<slug>_guide.pdf`` (Playwright build).

Requires the same environment as a manual PDF build (``playwright`` + Chromium).
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


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


def _input_paths(
    project_root: Path,
    slug: str,
    *,
    include_shared: bool,
) -> list[Path]:
    city_root = project_root / slug
    paths: list[Path] = []
    data_dir = city_root / "data"
    if data_dir.is_dir():
        paths.extend(p for p in data_dir.glob("*.json") if p.is_file())
    img_dir = city_root / "images"
    if img_dir.is_dir():
        for pattern in ("*.jpg", "*.jpeg", "*.png", "*.webp", "*.svg"):
            paths.extend(p for p in img_dir.rglob(pattern) if p.is_file())
    wl = city_root / "docs" / "SOURCES_WHITELIST.md"
    if wl.is_file():
        paths.append(wl)
    builder = project_root / "scripts" / "build_{}_pdf.py".format(slug)
    if builder.is_file():
        paths.append(builder)
    if include_shared:
        for rel in (
            "scripts/city_guide_typography.py",
            "scripts/city_guide_jerusalem_style_pdf.py",
            "scripts/city_guide_jerusalem_style_images.py",
            "scripts/build_pdf.py",
        ):
            p = project_root / rel
            if p.is_file():
                paths.append(p)
    return paths


def _max_mtime(paths: list[Path]) -> float | None:
    best: float | None = None
    for p in paths:
        try:
            mt = p.stat().st_mtime
        except OSError:
            continue
        if best is None or mt > best:
            best = mt
    return best


def _pdf_path(project_root: Path, slug: str) -> Path:
    return project_root / slug / "output" / "{}_guide.pdf".format(slug)


def _needs_rebuild(
    project_root: Path,
    slug: str,
    *,
    include_shared: bool,
) -> tuple[bool, str]:
    pdf = _pdf_path(project_root, slug)
    inputs = _input_paths(project_root, slug, include_shared=include_shared)
    if not inputs:
        return False, "no tracked inputs"
    newest = _max_mtime(inputs)
    if newest is None:
        return False, "no readable inputs"
    if not pdf.is_file():
        return True, "PDF missing"
    try:
        pdf_mt = pdf.stat().st_mtime
    except OSError as exc:
        return True, "PDF stat failed: {}".format(exc)
    if newest > pdf_mt:
        return True, "inputs newer than PDF"
    return False, "up to date"


def _run_build(project_root: Path, slug: str) -> int:
    script = project_root / "scripts" / "build_{}_pdf.py".format(slug)
    cmd = [sys.executable, str(script)]
    proc = subprocess.run(
        cmd,
        cwd=str(project_root),
        check=False,
    )
    return int(proc.returncode)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Rebuild city guide PDFs when data/images/whitelist/builder "
            "are newer than output PDF."
        ),
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help="Repository root (default: parent of scripts/).",
    )
    parser.add_argument(
        "--cities",
        nargs="*",
        metavar="SLUG",
        default=None,
        help=(
            "City slugs to check (default: all with "
            "scripts/build_<slug>_pdf.py and data/<slug>_places.json)."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print stale/fresh status only; do not run builders.",
    )
    parser.add_argument(
        "--include-shared",
        action="store_true",
        help=(
            "Also treat shared Jerusalem-style modules as inputs "
            "(typography, PDF helpers, Playwright wrapper)."
        ),
    )
    args = parser.parse_args()
    root = (
        args.project_root.resolve()
        if args.project_root
        else _project_root()
    )
    if args.cities:
        slugs = sorted(set(args.cities))
    else:
        slugs = _discover_slugs(root)

    if not slugs:
        print("No matching city slugs found.", file=sys.stderr)
        return 2

    stale: list[str] = []
    for slug in slugs:
        need, reason = _needs_rebuild(
            root,
            slug,
            include_shared=args.include_shared,
        )
        status = "STALE" if need else "ok"
        print("{}: {} ({})".format(slug, status, reason))
        if need:
            stale.append(slug)

    if args.dry_run:
        print("Dry run: {} stale, {} up to date.".format(
            len(stale),
            len(slugs) - len(stale),
        ))
        return 0

    failed = 0
    for slug in stale:
        print("Rebuilding {} ...".format(slug))
        code = _run_build(root, slug)
        if code != 0:
            print(
                "Build failed for {} (exit {}).".format(slug, code),
                file=sys.stderr,
            )
            failed += 1
    if failed:
        return 1
    if stale:
        print("Rebuilt {} guide(s).".format(len(stale)))
    else:
        print("Nothing to rebuild.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
