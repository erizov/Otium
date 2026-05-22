# -*- coding: utf-8 -*-
"""Save editor uploads with canonical paths and raster optimization."""

from __future__ import annotations

import re
from io import BytesIO
from pathlib import Path
from typing import Any

from scripts.city_guide_image_optimize import optimize_raster_image_if_large
from scripts.city_guide_naming import image_rel_path_for_slug

_RASTER_EXT = frozenset({".jpg", ".jpeg", ".png", ".webp", ".gif"})


def primary_image_rel_path(place_slug: str) -> str:
    return image_rel_path_for_slug(place_slug.strip())


def additional_image_rel_path(place_slug: str, seq: int) -> str:
    """
    Additional slots use ``images/{slug}_02.jpg`` … ``_05`` (max four extras).

    ``seq`` is 2–5 inclusive.
    """
    if seq < 2 or seq > 5:
        raise ValueError("additional seq must be 2..5")
    return "images/{}_{:02d}.jpg".format(place_slug.strip(), seq)


def next_additional_rel_path(
    city_root: Path,
    place_slug: str,
    existing: list[dict[str, Any]],
) -> str | None:
    """Pick the first free canonical additional path (or unused slot on disk)."""
    used = {
        Path(str(it.get("image_rel_path") or "")).stem
        for it in existing
        if isinstance(it, dict) and it.get("image_rel_path")
    }
    for seq in range(2, 6):
        rel = additional_image_rel_path(place_slug, seq)
        stem = Path(rel).stem
        if stem in used:
            continue
        if not (city_root / rel).is_file():
            return rel
    return None


def _write_as_jpeg(dest: Path, data: bytes) -> None:
    from PIL import Image

    dest.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(BytesIO(data)) as im:
        im.load()
        if im.mode in ("RGBA", "P"):
            bg = Image.new("RGB", im.size, (255, 255, 255))
            rgba = im.convert("RGBA") if im.mode == "P" else im
            bg.paste(rgba, mask=rgba.split()[3])
            rgb = bg
        else:
            rgb = im.convert("RGB")
        rgb.save(dest, format="JPEG", quality=88, optimize=True)


def save_uploaded_image(
    city_root: Path,
    rel_path: str,
    data: bytes,
    *,
    optimize: bool = True,
) -> str:
    """
    Write bytes to ``city_root / rel_path`` (always ``.jpg``), then optimize.

    Returns normalized ``rel_path`` using forward slashes.
    """
    rel = rel_path.replace("\\", "/").lstrip("/")
    if not rel.lower().startswith("images/"):
        raise ValueError("image_rel_path must start with images/")
    if Path(rel).suffix.lower() not in (".jpg", ".jpeg"):
        raise ValueError("image_rel_path must end with .jpg")
    dest = city_root / rel
    _write_as_jpeg(dest, data)
    if optimize:
        optimize_raster_image_if_large(dest, verbose=False)
    return rel


def optimize_image_at_rel(city_root: Path, rel_path: str) -> bool:
    """Optimize an existing on-disk raster if present."""
    rel = rel_path.replace("\\", "/").lstrip("/")
    dest = city_root / rel
    if not dest.is_file():
        return False
    if dest.suffix.lower() not in _RASTER_EXT:
        return False
    return optimize_raster_image_if_large(dest, verbose=False)


def normalize_rel_path(rel: str, city_slug: str, place_slug: str) -> str:
    """
    Map user-entered paths to canonical ``images/{slug}.jpg`` when possible.

    Accepts legacy ``images/foo.jpg`` when ``foo`` equals place slug stem.
    """
    rel_clean = rel.replace("\\", "/").lstrip("/")
    if not rel_clean.startswith("images/"):
        rel_clean = "images/" + rel_clean.lstrip("/")
    stem = Path(rel_clean).stem
    slug = place_slug.strip()
    if stem == slug or stem == slug.replace(city_slug + "_", "", 1):
        return primary_image_rel_path(slug)
    m = re.match(r"^images/(.+)_(\d{2})\.jpe?g$", rel_clean, re.I)
    if m and m.group(1) == slug:
        return additional_image_rel_path(slug, int(m.group(2)))
    if not rel_clean.lower().endswith(".jpg"):
        rel_clean = str(Path(rel_clean).with_suffix(".jpg")).replace("\\", "/")
    return rel_clean


def finalize_image_fields_in_patch(
    city_root: Path,
    city_slug: str,
    place_slug: str,
    patch: dict[str, Any],
) -> dict[str, Any]:
    """
    Normalize image paths in a place patch and optimize any existing files.
    """
    out = dict(patch)
    if "image_rel_path" in out and out["image_rel_path"]:
        rel = normalize_rel_path(str(out["image_rel_path"]), city_slug, place_slug)
        out["image_rel_path"] = rel
        optimize_image_at_rel(city_root, rel)
    editor = out.get("editor_images")
    if isinstance(editor, list):
        norm: list[dict[str, str]] = []
        for it in editor:
            if not isinstance(it, dict):
                continue
            rel = str(it.get("image_rel_path") or "").strip()
            if not rel:
                continue
            rel = normalize_rel_path(rel, city_slug, place_slug)
            optimize_image_at_rel(city_root, rel)
            norm.append(
                {
                    "image_rel_path": rel,
                    "image_source_url": str(
                        it.get("image_source_url") or "",
                    ).strip(),
                },
            )
        out["editor_images"] = norm[:4]
    return out
