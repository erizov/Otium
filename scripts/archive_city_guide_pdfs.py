# -*- coding: utf-8 -*-
"""Timestamped backups of city guide PDFs before rebuild (keep N newest)."""

from __future__ import annotations

import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

_ARCHIVE_SUFFIX_RE = re.compile(r"^(.+)_(\d{8}_\d{6})\.pdf$", re.IGNORECASE)


def _is_archive_name(name: str) -> bool:
    return bool(_ARCHIVE_SUFFIX_RE.match(name))


def guide_pdf_paths(output_dir: Path, slug: str) -> list[Path]:
    """Live guide PDFs in a city output folder (not timestamped archives)."""
    stem = "{}_guide".format(slug)
    candidates = (
        output_dir / "{}.pdf".format(stem),
        output_dir / "{}_en.pdf".format(stem),
        output_dir / "{}_ru.pdf".format(stem),
    )
    return [p for p in candidates if p.is_file() and not _is_archive_name(p.name)]


def _prune_archives(directory: Path, base_stem: str, *, keep: int) -> None:
    archives: list[Path] = []
    for path in directory.glob("{}_*.pdf".format(base_stem)):
        if not path.is_file():
            continue
        match = _ARCHIVE_SUFFIX_RE.match(path.name)
        if match and match.group(1) == base_stem:
            archives.append(path)
    archives.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    for old in archives[keep:]:
        try:
            old.unlink()
        except OSError:
            pass


def archive_guide_pdf(
    pdf: Path,
    *,
    keep: int = 2,
    now: datetime | None = None,
) -> Path | None:
    """
    Copy ``pdf`` to ``{stem}_{YYYYMMDD_HHMMSS}.pdf`` and keep ``keep`` archives.

    Returns the new archive path, or None if ``pdf`` is missing.
    """
    if not pdf.is_file() or _is_archive_name(pdf.name):
        return None
    if now is None:
        now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y%m%d_%H%M%S")
    dest = pdf.with_name("{}_{}.pdf".format(pdf.stem, stamp))
    shutil.copy2(pdf, dest)
    _prune_archives(pdf.parent, pdf.stem, keep=keep)
    return dest


def archive_city_output_pdfs(
    project_root: Path,
    slug: str,
    *,
    keep: int = 2,
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
