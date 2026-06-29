# -*- coding: utf-8 -*-
"""Image URLs and local paths that must not be used in the guide."""

from __future__ import annotations

BANNED_IMAGE_URL_FRAGMENTS: tuple[str, ...] = ()
BANNED_LOCAL_IMAGE_RELS: tuple[str, ...] = ()


def url_is_banned(url: str) -> bool:
    low = str(url or "").strip().lower()
    if not low:
        return False
    return any(frag.lower() in low for frag in BANNED_IMAGE_URL_FRAGMENTS)


def local_rel_is_banned(rel: str) -> bool:
    norm = str(rel or "").replace("\\", "/").strip().lower()
    if not norm:
        return False
    return any(b.lower() in norm for b in BANNED_LOCAL_IMAGE_RELS)
