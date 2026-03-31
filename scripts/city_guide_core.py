# -*- coding: utf-8 -*-
"""Shared helpers for per-city guide builds (Smolensk-style PDF/HTML)."""

from __future__ import annotations

from pathlib import Path

MIN_IMAGE_BYTES = 500
_MIN_VECTOR_BYTES = 32

# Lone filler tokens in JSON/detail merges — omit section if only this.
_PLACEHOLDER_TOKENS: frozenset[str] = frozenset({
    "—",
    "–",
    "-",
    "…",
    "...",
    "n/a",
    "na",
    "n.a.",
    "tbd",
    "tbc",
})


def is_substantive_text(value: str | None) -> bool:
    """
    True when value is non-empty and not a single placeholder token.

    Used so Facts / History / Significance (and meta lines) stay hidden
    when source data only contains an em dash or similar stub.
    """
    if value is None:
        return False
    s = str(value).strip()
    if not s:
        return False
    if s in _PLACEHOLDER_TOKENS:
        return False
    if s.lower() in _PLACEHOLDER_TOKENS:
        return False
    return True


def min_bytes_for_filename(filename: str) -> int:
    """Raster images need a size floor; tiny SVG/GIF are still valid."""
    suf = Path(filename).suffix.lower()
    if suf in (".svg", ".gif"):
        return _MIN_VECTOR_BYTES
    return MIN_IMAGE_BYTES


def smallest_same_stem_image_rel(root: Path, rel: str) -> str | None:
    """
    Among files sharing the same stem (foo.jpg, foo.webp, …), pick the
    smallest by bytes that is still >= MIN_IMAGE_BYTES.
    """
    rel_clean = rel.replace("\\", "/").lstrip("/")
    base = root / rel_clean
    parent = base.parent
    stem = base.stem
    if not parent.is_dir():
        return None
    sized: list[tuple[Path, int]] = []
    try:
        for path in parent.iterdir():
            if not path.is_file() or path.stem != stem:
                continue
            size = path.stat().st_size
            if size >= min_bytes_for_filename(path.name):
                sized.append((path, size))
    except OSError:
        return None
    if not sized:
        return None
    best = min(sized, key=lambda t: t[1])[0]
    try:
        return best.relative_to(root.resolve()).as_posix()
    except ValueError:
        return None
