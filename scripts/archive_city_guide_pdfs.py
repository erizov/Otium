# -*- coding: utf-8 -*-
"""Timestamped backups of city guide PDFs before rebuild (keep N distinct)."""

from __future__ import annotations

import hashlib
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

_ARCHIVE_SUFFIX_RE = re.compile(
    r"^(.+)_(\d{8}_\d{6}(?:_\d{6})?)\.pdf$",
    re.IGNORECASE,
)
_HASH_CHUNK = 65536


def _is_archive_name(name: str) -> bool:
    return bool(_ARCHIVE_SUFFIX_RE.match(name))


def guide_pdf_stems(slug: str) -> list[str]:
    """Live PDF name stems for a city (without ``.pdf``)."""
    base = "{}_guide".format(slug)
    return [base, "{}_en".format(base), "{}_ru".format(base)]


def guide_pdf_paths(output_dir: Path, slug: str) -> list[Path]:
    """Live guide PDFs in a city output folder (not timestamped archives)."""
    return [
        output_dir / "{}.pdf".format(stem)
        for stem in guide_pdf_stems(slug)
        if (output_dir / "{}.pdf".format(stem)).is_file()
        and not _is_archive_name((output_dir / "{}.pdf".format(stem)).name)
    ]


def _file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(_HASH_CHUNK), b""):
            digest.update(block)
    return digest.hexdigest()


def _list_archives(directory: Path, base_stem: str) -> list[Path]:
    archives: list[Path] = []
    for path in directory.glob("{}_*.pdf".format(base_stem)):
        if not path.is_file():
            continue
        match = _ARCHIVE_SUFFIX_RE.match(path.name)
        if match and match.group(1) == base_stem:
            archives.append(path)
    return archives


def _duplicate_archive_paths(archives: list[Path]) -> list[Path]:
    """Older timestamped copies whose bytes match a newer archive."""
    to_delete: list[Path] = []
    seen: dict[str, Path] = {}
    for path in sorted(
        archives,
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    ):
        try:
            digest = _file_hash(path)
        except OSError:
            continue
        if digest in seen:
            to_delete.append(path)
        else:
            seen[digest] = path
    return to_delete


def _prune_archives(directory: Path, base_stem: str, *, keep: int) -> None:
    archives = _list_archives(directory, base_stem)
    for dup in _duplicate_archive_paths(archives):
        try:
            dup.unlink()
        except OSError:
            pass
    archives = _list_archives(directory, base_stem)
    archives.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    for old in archives[keep:]:
        try:
            old.unlink()
        except OSError:
            pass


def _matches_existing_archive(pdf: Path, archives: list[Path]) -> bool:
    try:
        source_hash = _file_hash(pdf)
    except OSError:
        return False
    for arch in archives:
        try:
            if _file_hash(arch) == source_hash:
                return True
        except OSError:
            continue
    return False


def archive_guide_pdf(
    pdf: Path,
    *,
    keep: int = 3,
    now: datetime | None = None,
) -> Path | None:
    """
    Copy ``pdf`` to ``{stem}_{YYYYMMDD_HHMMSS}.pdf`` and keep ``keep`` archives.

    Skips the copy when an existing archive already has identical bytes.
    Returns the new archive path, or None if skipped or ``pdf`` is missing.
    """
    if not pdf.is_file() or _is_archive_name(pdf.name):
        return None
    archives = _list_archives(pdf.parent, pdf.stem)
    if _matches_existing_archive(pdf, archives):
        _prune_archives(pdf.parent, pdf.stem, keep=keep)
        return None
    if now is None:
        now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y%m%d_%H%M%S_%f")
    dest = pdf.with_name("{}_{}.pdf".format(pdf.stem, stamp))
    shutil.copy2(pdf, dest)
    _prune_archives(pdf.parent, pdf.stem, keep=keep)
    return dest


def archive_city_output_pdfs(
    project_root: Path,
    slug: str,
    *,
    keep: int = 3,
    final_guides: bool = True,
) -> list[Path]:
    """Archive live PDFs under ``<slug>/output/`` and optionally ``final_guides/``."""
    created: list[Path] = []
    out_dir = project_root / slug / "output"
    if out_dir.is_dir():
        for pdf in guide_pdf_paths(out_dir, slug):
            arch = archive_guide_pdf(pdf, keep=keep)
            if arch:
                created.append(arch)
    if final_guides:
        fg = project_root / "final_guides"
        if fg.is_dir():
            for pdf in guide_pdf_paths(fg, slug):
                arch = archive_guide_pdf(pdf, keep=keep)
                if arch:
                    created.append(arch)
    return created


def cleanup_city_archives(
    project_root: Path,
    slug: str,
    *,
    keep: int = 3,
    final_guides: bool = True,
) -> None:
    """Drop duplicate timestamped PDFs; keep ``keep`` newest distinct per stem."""
    dirs: list[Path] = []
    out_dir = project_root / slug / "output"
    if out_dir.is_dir():
        dirs.append(out_dir)
    if final_guides:
        fg = project_root / "final_guides"
        if fg.is_dir():
            dirs.append(fg)
    for directory in dirs:
        for stem in guide_pdf_stems(slug):
            _prune_archives(directory, stem, keep=keep)


def cleanup_all_city_archives(
    project_root: Path,
    slugs: list[str] | None = None,
    *,
    keep: int = 3,
    final_guides: bool = True,
) -> None:
    """Prune timestamped archives for every city (or ``slugs`` only)."""
    if slugs is None:
        slugs = sorted(
            p.parent.parent.name
            for p in project_root.glob("*/output/*_guide*.pdf")
        )
    for slug in slugs:
        cleanup_city_archives(
            project_root,
            slug,
            keep=keep,
            final_guides=final_guides,
        )


def main() -> int:
    import argparse
    import sys

    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=root,
    )
    parser.add_argument(
        "--keep",
        type=int,
        default=3,
        metavar="N",
        help="Keep N distinct timestamped archives per PDF stem (default 3).",
    )
    parser.add_argument(
        "--cities",
        nargs="*",
        metavar="SLUG",
        default=None,
        help="City slugs to clean (default: all with guide PDFs).",
    )
    parser.add_argument(
        "--no-final-guides",
        action="store_true",
        help="Only prune under <city>/output/, not final_guides/.",
    )
    args = parser.parse_args()
    cleanup_all_city_archives(
        args.project_root.resolve(),
        args.cities,
        keep=args.keep,
        final_guides=not args.no_final_guides,
    )
    print(
        "Pruned duplicate timestamped PDFs (keep={} distinct per stem).".format(
            args.keep,
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
