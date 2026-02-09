# -*- coding: utf-8 -*-
"""Image hashing for duplicate detection (perceptual hash preferred, SHA256 fallback)."""

from pathlib import Path
from typing import Optional

# Optional: perceptual hash so full-size and thumbnail count as same image
_PERCEPTUAL_AVAILABLE: Optional[bool] = None


def _perceptual_hash_available() -> bool:
    global _PERCEPTUAL_AVAILABLE
    if _PERCEPTUAL_AVAILABLE is not None:
        return _PERCEPTUAL_AVAILABLE
    try:
        import imagehash
        from PIL import Image
        _PERCEPTUAL_AVAILABLE = True
    except ImportError:
        _PERCEPTUAL_AVAILABLE = False
    return _PERCEPTUAL_AVAILABLE


def image_content_hash(path: Path, min_bytes: int = 500) -> str:
    """
    Content-based hash for deduplication.

    Prefers perceptual hash (imagehash phash) so that full-size and
    scaled-down versions of the same image are treated as duplicates.
    Falls back to SHA256 of file bytes if imagehash/PIL unavailable
    (scaled duplicates will not be detected).
    """
    if not path.exists() or not path.is_file():
        return ""
    if path.stat().st_size < min_bytes:
        return ""
    if _perceptual_hash_available():
        try:
            import imagehash
            from PIL import Image
            img = Image.open(path)
            h = imagehash.phash(img)
            return str(h)
        except Exception:
            pass
    # Fallback: SHA256 of file contents
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()
