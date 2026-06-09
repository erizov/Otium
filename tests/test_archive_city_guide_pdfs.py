# -*- coding: utf-8 -*-
"""Tests for timestamped city-guide PDF archiving."""

from __future__ import annotations

from pathlib import Path

from scripts.archive_city_guide_pdfs import (
    _duplicate_archive_paths,
    _prune_archives,
    archive_guide_pdf,
)


def test_skip_identical_archive(tmp_path: Path) -> None:
    live = tmp_path / "smolensk_guide.pdf"
    live.write_bytes(b"%PDF-1.4 same content")
    first = archive_guide_pdf(live, keep=3)
    assert first is not None
    second = archive_guide_pdf(live, keep=3)
    assert second is None
    archives = list(tmp_path.glob("smolensk_guide_*.pdf"))
    assert len(archives) == 1


def test_prune_keeps_three_distinct_versions(tmp_path: Path) -> None:
    live = tmp_path / "smolensk_guide.pdf"
    for idx in range(5):
        live.write_bytes("%PDF version {}".format(idx).encode())
        archive_guide_pdf(live, keep=3)
    archives = sorted(tmp_path.glob("smolensk_guide_*.pdf"))
    assert len(archives) == 3
    bodies = {path.read_bytes() for path in archives}
    assert len(bodies) == 3


def test_dedupe_identical_timestamped_copies(tmp_path: Path) -> None:
    payload = b"%PDF duplicate bytes"
    older = tmp_path / "smolensk_guide_20260101_120000.pdf"
    newer = tmp_path / "smolensk_guide_20260201_120000.pdf"
    older.write_bytes(payload)
    newer.write_bytes(payload)
    dupes = _duplicate_archive_paths([older, newer])
    assert older in dupes
    assert newer not in dupes
    _prune_archives(tmp_path, "smolensk_guide", keep=3)
    assert not older.is_file()
    assert newer.is_file()
