# -*- coding: utf-8 -*-
"""Rebuild stale city-guide PDFs, then copy them into final_guides/."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.archive_city_guide_pdfs import archive_city_output_pdfs
from scripts.city_guide_core import copy_built_guide_pdf_to_final_guides
from scripts.rebuild_stale_city_guide_pdfs import (
    _input_paths,
    _max_mtime,
    _run_build,
    merged_input_paths,
    needs_rebuild,
    stale_pdf_targets,
)


def _extra_stale_input_paths(project_root: Path) -> list[Path]:
    """Shared modules that affect guide text/layout beyond per-city data."""
    rels = (
        "scripts/city_guide_historical_reference_ru.py",
        "scripts/city_guide_front_matter.py",
    )
    out: list[Path] = []
    for rel in rels:
        p = project_root / rel
        if p.is_file():
            out.append(p)
    return out


def _merged_input_paths(
    project_root: Path,
    slug: str,
    *,
    include_shared: bool,
) -> list[Path]:
    return merged_input_paths(
        project_root,
        slug,
        include_shared=include_shared,
    )


def _stale_check_targets(
    output_dir: Path,
    slug: str,
    scope: str,
) -> list[Path]:
    """PDF paths that must be fresh together for this deploy scope."""
    all_targets = stale_pdf_targets(output_dir, slug)
    base = output_dir / "{}_guide.pdf".format(slug)
    en = output_dir / "{}_guide_en.pdf".format(slug)
    ru = output_dir / "{}_guide_ru.pdf".format(slug)
    if scope == "en":
        return [en] if en.is_file() else [en]
    if scope == "ru":
        return [ru] if ru.is_file() else [ru]
    return all_targets


def _needs_rebuild_for_targets(
    project_root: Path,
    slug: str,
    scope: str,
    *,
    include_shared: bool,
) -> tuple[bool, str]:
    """True when any target PDF is missing or older than newest input."""
    out_dir = project_root / slug / "output"
    targets = _stale_check_targets(out_dir, slug, scope)
    inputs = _merged_input_paths(
        project_root,
        slug,
        include_shared=include_shared,
    )
    newest = _max_mtime(inputs)
    if newest is None:
        return False, "no tracked inputs"
    for pdf in targets:
        if not pdf.is_file():
            return True, "missing {}".format(pdf.name)
    oldest = min(p.stat().st_mtime for p in targets if p.is_file())
    if newest > oldest:
        return True, "inputs newer than output PDF(s)"
    return False, "up to date"


def _builder_script(project_root: Path, slug: str) -> Path | None:
    script = project_root / "scripts" / "build_{}_pdf.py".format(slug)
    if script.is_file():
        return script
    return None


def _guide_pdf_paths(output_dir: Path, slug: str, scope: str) -> list[Path]:
    """Return existing PDF paths for one city output dir and deploy scope."""
    base = output_dir / "{}_guide.pdf".format(slug)
    en = output_dir / "{}_guide_en.pdf".format(slug)
    ru = output_dir / "{}_guide_ru.pdf".format(slug)
    if scope == "en":
        return [en] if en.is_file() else []
    if scope == "ru":
        return [ru] if ru.is_file() else []
    out: list[Path] = []
    if en.is_file():
        out.append(en)
    if ru.is_file():
        out.append(ru)
    if base.is_file():
        out.append(base)
    return out


def run_deploy(
    project_root: Path,
    scope: str,
    *,
    dry_run: bool = False,
    no_build: bool = False,
    include_shared: bool = False,
    archive_keep: int = 3,
    allow_translate: bool = False,
) -> int:
    """
    Rebuild stale guides, then copy into project_root/final_guides.

    Staleness uses the same inputs as rebuild_stale_city_guide_pdfs
    (city data JSON, images, whitelist, builder) plus
    city_guide_historical_reference_ru.py. For dual-language cities
    (``*_guide_en.pdf`` or ``*_guide_ru.pdf`` present), all three outputs
    (en, ru, primary) must exist and be newer than inputs when scope is
    ``all``.
    """
    if scope not in ("all", "en", "ru"):
        print("Invalid scope: {!r} (use all, en, ru).".format(scope), file=sys.stderr)
        return 2
    root = project_root.resolve()
    build_failures = 0
    rebuilt = 0
    skipped_no_builder = 0
    failed_slugs: set[str] = set()

    if not no_build:
        for out_dir in sorted(root.glob("*/output")):
            if not out_dir.is_dir():
                continue
            slug = out_dir.parent.name
            builder = _builder_script(root, slug)
            if builder is None:
                skipped_no_builder += 1
                continue
            need, reason = _needs_rebuild_for_targets(
                root,
                slug,
                scope,
                include_shared=include_shared,
            )
            if not need:
                continue
            print("{}: rebuild ({})".format(slug, reason))
            if dry_run:
                rebuilt += 1
                continue
            if archive_keep > 0:
                archived = archive_city_output_pdfs(
                    root,
                    slug,
                    keep=archive_keep,
                )
                if archived:
                    print(
                        "  archived {} PDF(s).".format(len(archived)),
                    )
            code = _run_build(
                root,
                slug,
                allow_translate=allow_translate,
            )
            if code != 0:
                print(
                    "Build failed for {} (exit {}).".format(slug, code),
                    file=sys.stderr,
                )
                build_failures += 1
                failed_slugs.add(slug)
                continue
            rebuilt += 1

    if dry_run and not no_build:
        print(
            "Dry run: {} slug(s) would rebuild; {} without builder script.".format(
                rebuilt,
                skipped_no_builder,
            ),
        )

    if build_failures:
        print(
            "Skipping copy for failed slug(s): {}.".format(
                ", ".join(sorted(failed_slugs)),
            ),
            file=sys.stderr,
        )

    copied = 0
    if not dry_run:
        for out_dir in sorted(root.glob("*/output")):
            if not out_dir.is_dir():
                continue
            slug = out_dir.parent.name
            if slug in failed_slugs:
                continue
            for pdf in _guide_pdf_paths(out_dir, slug, scope):
                copy_built_guide_pdf_to_final_guides(root, pdf)
                copied += 1
        print(
            "Deploy {}: rebuilt {}, copied {} PDF(s) to final_guides/.".format(
                scope,
                rebuilt,
                copied,
            ),
        )
    else:
        would_copy = 0
        for out_dir in sorted(root.glob("*/output")):
            if not out_dir.is_dir():
                continue
            slug = out_dir.parent.name
            would_copy += len(_guide_pdf_paths(out_dir, slug, scope))
        print(
            "Dry run: would copy {} PDF(s) for scope {!r}.".format(
                would_copy,
                scope,
            ),
        )
    return 1 if build_failures else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Rebuild per-city guide PDFs when inputs are newer than outputs, "
            "then copy from <slug>/output/ into final_guides/."
        ),
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help="Repository root (default: parent of scripts/).",
    )
    parser.add_argument(
        "--lang",
        dest="scope",
        choices=("all", "en", "ru"),
        default="all",
        metavar="SCOPE",
        help="Which PDFs to refresh and copy: all editions, en only, or ru.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show stale slugs; do not build or copy.",
    )
    parser.add_argument(
        "--with-translate",
        action="store_true",
        help=(
            "Allow EN↔RU translation during PDF/HTML build "
            "(uses cache, Ollama, or OpenAI)."
        ),
    )
    parser.add_argument(
        "--no-build",
        action="store_true",
        help="Copy only; skip staleness rebuild (not recommended).",
    )
    parser.add_argument(
        "--include-shared",
        action="store_true",
        help=(
            "Treat shared Jerusalem-style modules as inputs (same as "
            "rebuild_stale_city_guide_pdfs --include-shared)."
        ),
    )
    parser.add_argument(
        "--archive-keep",
        type=int,
        default=3,
        metavar="N",
        help="Keep N distinct timestamped PDF backups per file (0=off).",
    )
    args = parser.parse_args(argv)
    root = (
        args.project_root.resolve()
        if args.project_root
        else _PROJECT_ROOT
    )
    return run_deploy(
        root,
        args.scope,
        dry_run=args.dry_run,
        no_build=args.no_build,
        include_shared=args.include_shared,
        archive_keep=args.archive_keep,
        allow_translate=args.with_translate,
    )


if __name__ == "__main__":
    raise SystemExit(main())
