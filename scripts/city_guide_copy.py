# -*- coding: utf-8 -*-
"""Resilient copy for guide HTML/PDF artifacts (Windows file locks)."""

from __future__ import annotations

import os
import shutil
import sys
import time
from pathlib import Path

# Windows: sharing violation / memory-mapped file (PDF viewer, Explorer preview).
_WIN_FILE_LOCKED = frozenset({13, 32, 1224})

_PATCHED = False
_REAL_COPY2 = shutil.copy2


def install_guide_copy_patch() -> None:
    """Replace shutil.copy2 for guide PDF/HTML copies (batch-safe on Windows)."""
    global _PATCHED, _REAL_COPY2
    if _PATCHED:
        return
    import shutil as _shutil

    _REAL_COPY2 = _shutil.copy2

    def copy2(src, dst, *args, **kwargs):
        s = Path(src)
        d = Path(dst)
        if s.is_file() and s.suffix.lower() in (".pdf", ".html"):
            if copy_guide_artifact(s, d):
                return dst
            if d.suffix.lower() == ".pdf":
                print(
                    "Warning: left primary PDF unchanged; edition file: "
                    "{}".format(s),
                    file=sys.stderr,
                )
                return dst
            return _REAL_COPY2(src, dst, *args, **kwargs)
        return _REAL_COPY2(src, dst, *args, **kwargs)

    _shutil.copy2 = copy2
    copy2._guide_copy_patch = True  # type: ignore[attr-defined]
    _PATCHED = True


def _is_windows_file_lock_error(exc: OSError) -> bool:
    winerr = getattr(exc, "winerror", None)
    if winerr in _WIN_FILE_LOCKED:
        return True
    return exc.errno in _WIN_FILE_LOCKED


def copy_guide_artifact(
    src: Path,
    dest: Path,
    *,
    retries: int = 10,
    delay_sec: float = 0.45,
) -> bool:
    """
    Copy a built guide HTML/PDF, retrying when the destination is locked.

    Uses a temp file + replace so partially open targets on Windows are less
    likely to break batch rebuilds (WinError 32 / 1224).
    """
    src_p = src.resolve()
    dest_p = dest.resolve()
    if not src_p.is_file():
        return False
    dest_p.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest_p.with_name(dest_p.name + ".tmp-copy")
    last_err: OSError | None = None
    for attempt in range(max(1, retries)):
        try:
            _REAL_COPY2(src_p, tmp)
            os.replace(str(tmp), str(dest_p))
            return True
        except OSError as exc:
            last_err = exc
            if tmp.is_file():
                tmp.unlink(missing_ok=True)
            if not _is_windows_file_lock_error(exc) and attempt == 0:
                raise
            if attempt + 1 < retries:
                time.sleep(delay_sec * (attempt + 1))
    if last_err is not None:
        print(
            "Warning: could not update {} (file may be open in a viewer): "
            "{}".format(dest_p, last_err),
            file=sys.stderr,
        )
    return False
