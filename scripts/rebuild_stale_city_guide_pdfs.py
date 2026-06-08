# -*- coding: utf-8 -*-
"""Rebuild per-city guide PDFs when inputs are newer than the output PDF.

Compares modification time of city text/images against existing PDFs:

- ``<slug>/data/*.json`` (places + sidecars)
- ``<slug>/images/**`` (jpg, png, webp, svg, …)
- ``<slug>/docs/SOURCES_WHITELIST.md``
- ``scripts/build_<slug>_pdf.py``
- ``scripts/city_guide_historical_reference_ru.py`` (shared historical chapter)

Output targets: ``*_guide_en.pdf``, ``*_guide_ru.pdf``, and/or legacy
``*_guide.pdf`` — rebuild when **any** target is missing or older than inputs.

Requires Playwright + Chromium for full PDF builds (same as manual build).
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.archive_city_guide_pdfs import archive_city_output_pdfs


def _project_root() -> Path:
    return _PROJECT_ROOT


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
        for pattern in ("*.jpg", "*.jpeg", "*.png", "*.webp", "*.svg", "*.gif"):
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
            "scripts/city_guide_narrative.py",
            "scripts/build_pdf.py",
        ):
            p = project_root / rel
            if p.is_file():
                paths.append(p)
    return paths


def _extra_stale_input_paths(project_root: Path) -> list[Path]:
    """Shared modules that affect guide text/layout beyond per-city data."""
    rels = (
        "scripts/city_guide_historical_reference_ru.py",
        "scripts/city_guide_core.py",
        "scripts/city_guide_naming.py",
        "scripts/city_guide_narrative.py",
        "scripts/city_guide_front_matter.py",
    )
    out: list[Path] = []
    for rel in rels:
        p = project_root / rel
        if p.is_file():
            out.append(p)
    return out


def merged_input_paths(
    project_root: Path,
    slug: str,
    *,
    include_shared: bool,
) -> list[Path]:
    paths = _input_paths(project_root, slug, include_shared=include_shared)
    paths.extend(_extra_stale_input_paths(project_root))
    data_dir = project_root / slug / "data"
    if data_dir.is_dir():
        paths.extend(
            p for p in data_dir.glob("*registry*.py") if p.is_file()
        )
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


def stale_pdf_targets(output_dir: Path, slug: str) -> list[Path]:
    """PDF paths that must be fresh together for a full rebuild."""
    base = output_dir / "{}_guide.pdf".format(slug)
    en = output_dir / "{}_guide_en.pdf".format(slug)
    ru = output_dir / "{}_guide_ru.pdf".format(slug)
    if en.is_file() or ru.is_file():
        targets = [p for p in (en, ru, base) if p.is_file()]
        return targets if targets else [en, ru]
    return [base]


def needs_rebuild(
    project_root: Path,
    slug: str,
    *,
    include_shared: bool,
) -> tuple[bool, str]:
    """True when any target PDF is missing or older than newest input."""
    out_dir = project_root / slug / "output"
    targets = stale_pdf_targets(out_dir, slug)
    inputs = merged_input_paths(
        project_root,
        slug,
        include_shared=include_shared,
    )
    if not inputs:
        return False, "no tracked inputs"
    newest = _max_mtime(inputs)
    if newest is None:
        return False, "no readable inputs"
    for pdf in targets:
        if not pdf.is_file():
            return True, "missing {}".format(pdf.name)
    oldest = min(p.stat().st_mtime for p in targets)
    if newest > oldest:
        return True, "inputs newer than PDF(s)"
    return False, "up to date"


def _run_build(
    project_root: Path,
    slug: str,
    *,
    html_only: bool = False,
    allow_translate: bool = False,
) -> int:
    script = project_root / "scripts" / "build_{}_pdf.py".format(slug)
    cmd = [sys.executable, str(script)]
    if html_only:
        cmd.append("--html-only")
    env = None
    if not allow_translate:
        env = dict(os.environ)
        env["CITY_GUIDE_NO_TRANSLATE"] = "1"
    proc = subprocess.run(
        cmd,
        cwd=str(project_root),
        check=False,
        env=env,
    )
    return int(proc.returncode)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
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
        "--html-only",
        action="store_true",
        help="Pass --html-only to each city builder (no Playwright PDF).",
    )
    parser.add_argument(
        "--include-shared",
        action="store_true",
        help=(
            "Also treat shared Jerusalem-style / narrative modules as "
            "inputs (typography, PDF helpers)."
        ),
    )
    parser.add_argument(
        "--with-translate",
        action="store_true",
        help=(
            "Allow cross-edition live translation during PDF/HTML build "
            "(may call Ollama/OpenAI). Default: disabled."
        ),
    )
    parser.add_argument(
        "--archive-keep",
        type=int,
        default=2,
        metavar="N",
        help=(
            "Before each rebuild, copy live PDFs to timestamped names "
            "and keep N archives per file (default 2). Use 0 to skip."
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
        need, reason = needs_rebuild(
            root,
            slug,
            include_shared=args.include_shared,
        )
        status = "STALE" if need else "ok"
        print("{}: {} ({})".format(slug, status, reason))
        if need:
            stale.append(slug)

    if args.dry_run:
        print(
            "Dry run: {} stale, {} up to date.".format(
                len(stale),
                len(slugs) - len(stale),
            ),
        )
        return 0

    failed = 0
    for slug in stale:
        if args.archive_keep > 0 and not args.html_only:
            archived = archive_city_output_pdfs(
                root,
                slug,
                keep=args.archive_keep,
            )
            if archived:
                print(
                    "Archived {} PDF(s) for {}.".format(len(archived), slug),
                )
        print("Rebuilding {} ...".format(slug))
        code = _run_build(
            root,
            slug,
            html_only=args.html_only,
            allow_translate=args.with_translate,
        )
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
