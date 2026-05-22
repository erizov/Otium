# -*- coding: utf-8 -*-
"""Unified raster image optimization for all city guides."""

from __future__ import annotations

import argparse
import sys
from io import BytesIO
from pathlib import Path

from PIL import Image

# Default cap for guide PDF embedding (bytes).
CITY_GUIDE_IMAGE_MAX_BYTES = 350 * 1024
CITY_GUIDE_IMAGE_MAX_SIDE_PX = 1600
CITY_GUIDE_IMAGE_WARN_BYTES = 400 * 1024
CITY_GUIDE_IMAGE_WARN_SIDE_PX = 2048

_RASTER_EXT = frozenset({".jpg", ".jpeg", ".png", ".webp"})
_SKIP_EXT = frozenset({".svg", ".gif"})


def _fit_max_side(im: Image.Image, max_side: int) -> Image.Image:
    w, h = im.size
    m = max(w, h)
    if m <= max_side:
        return im
    scale = max_side / m
    nw = max(1, int(round(w * scale)))
    nh = max(1, int(round(h * scale)))
    return im.resize((nw, nh), Image.Resampling.LANCZOS)


def _as_rgb_white_bg(im: Image.Image) -> Image.Image:
    if im.mode == "RGB":
        return im
    if im.mode == "RGBA":
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[3])
        return bg
    if im.mode == "P":
        return _as_rgb_white_bg(im.convert("RGBA"))
    return im.convert("RGB")


def _bytes_jpeg(im: Image.Image, max_side: int, quality: int) -> bytes:
    work = _fit_max_side(im, max_side)
    rgb = _as_rgb_white_bg(work)
    buf = BytesIO()
    rgb.save(
        buf,
        format="JPEG",
        quality=quality,
        optimize=True,
        subsampling=1,
    )
    return buf.getvalue()


def _bytes_webp(im: Image.Image, max_side: int, quality: int) -> bytes:
    work = _fit_max_side(im, max_side)
    buf = BytesIO()
    if work.mode in ("RGBA", "P"):
        rgba = work.convert("RGBA") if work.mode == "P" else work
        rgba.save(buf, format="WEBP", quality=quality, method=6)
    else:
        rgb = work.convert("RGB")
        rgb.save(buf, format="WEBP", quality=quality, method=6)
    return buf.getvalue()


def _bytes_png(im: Image.Image, max_side: int) -> bytes:
    work = _fit_max_side(im, max_side)
    buf = BytesIO()
    work.save(buf, format="PNG", optimize=True, compress_level=9)
    return buf.getvalue()


def _max_side_steps(im: Image.Image) -> list[int]:
    orig = max(im.size)
    out: list[int] = [orig]
    cap = CITY_GUIDE_IMAGE_MAX_SIDE_PX
    for s in (
        3072, 2560, 2048, 1920, 1600, 1400, 1280, 1140, 1024, 900, 800,
        720, 640, 560, 480,
    ):
        if s > cap:
            continue
        if s < orig and s not in out:
            out.append(s)
    if cap < orig and cap not in out:
        out.append(cap)
    return out


def _atomic_replace(path: Path, data: bytes) -> None:
    tmp = path.with_name(path.name + ".tmp-opt")
    try:
        tmp.write_bytes(data)
        tmp.replace(path)
    except OSError:
        if tmp.is_file():
            tmp.unlink(missing_ok=True)
        raise


def _encode_under_cap(
    im: Image.Image,
    ext: str,
    max_bytes: int,
) -> bytes | None:
    if ext in (".jpg", ".jpeg"):
        qualities = list(range(90, 49, -4))
        for side in _max_side_steps(im):
            for q in qualities:
                blob = _bytes_jpeg(im, side, q)
                if len(blob) <= max_bytes:
                    return blob
        return None
    if ext == ".webp":
        qualities = list(range(88, 47, -4))
        for side in _max_side_steps(im):
            for q in qualities:
                blob = _bytes_webp(im, side, q)
                if len(blob) <= max_bytes:
                    return blob
        return None
    if ext == ".png":
        for side in _max_side_steps(im):
            blob = _bytes_png(im, side)
            if len(blob) <= max_bytes:
                return blob
        return None
    return None


def optimize_raster_image_if_large(
    path: Path,
    *,
    max_bytes: int | None = None,
    max_side: int | None = None,
    verbose: bool = False,
) -> bool:
    """
    Re-save raster files over max_bytes or max_side until under caps.

    Returns True when the file was rewritten.
    """
    if max_bytes is None:
        max_bytes = CITY_GUIDE_IMAGE_MAX_BYTES
    if max_side is None:
        max_side = CITY_GUIDE_IMAGE_MAX_SIDE_PX
    if not path.is_file():
        return False
    ext = path.suffix.lower()
    if ext in _SKIP_EXT or ext not in _RASTER_EXT:
        return False
    try:
        size0 = path.stat().st_size
    except OSError:
        return False
    try:
        with Image.open(path) as im:
            im.load()
            if getattr(im, "is_animated", False):
                return False
            needs_side = max(im.size) > max_side
            if size0 <= max_bytes and not needs_side:
                return False
            if needs_side:
                if ext in (".jpg", ".jpeg"):
                    blob = _bytes_jpeg(im, max_side, 85)
                elif ext == ".webp":
                    blob = _bytes_webp(im, max_side, 85)
                elif ext == ".png":
                    blob = _bytes_png(im, max_side)
                else:
                    blob = None
            else:
                blob = _encode_under_cap(im, ext, max_bytes)
    except OSError:
        return False
    if blob is None:
        return False
    if not needs_side and len(blob) >= size0:
        return False
    if needs_side:
        try:
            with Image.open(BytesIO(blob)) as check:
                check.load()
                if max(check.size) >= max(im.size):
                    return False
        except OSError:
            return False
    elif len(blob) >= size0:
        return False
    try:
        _atomic_replace(path, blob)
    except OSError:
        return False
    if verbose:
        print(
            "optimized {}  {} -> {} B".format(
                path.as_posix(), size0, len(blob),
            ),
            file=sys.stderr,
        )
    return True


def raster_dimensions(path: Path) -> tuple[int, int] | None:
    """Return (width, height) for a raster file, or None."""
    if path.suffix.lower() not in _RASTER_EXT:
        return None
    try:
        with Image.open(path) as im:
            return im.size
    except OSError:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Shrink city-guide raster images over a size cap.",
    )
    parser.add_argument(
        "--images-dir",
        type=Path,
        required=True,
        help="Directory to scan.",
    )
    parser.add_argument(
        "--max-kib",
        type=int,
        default=CITY_GUIDE_IMAGE_MAX_BYTES // 1024,
        metavar="N",
        help="Max file size in KiB before optimizing.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only list paths over the cap.",
    )
    args = parser.parse_args()
    cap = max(1, args.max_kib) * 1024
    root = args.images_dir.resolve()
    if not root.is_dir():
        print("Not a directory: {}".format(root), file=sys.stderr)
        return 1
    changed = 0
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in _RASTER_EXT:
            continue
        try:
            sz = path.stat().st_size
        except OSError:
            continue
        if sz <= cap:
            continue
        if args.dry_run:
            print("{}  {} B".format(path.relative_to(root), sz))
            continue
        if optimize_raster_image_if_large(path, max_bytes=cap, verbose=True):
            changed += 1
    if args.dry_run:
        print("dry-run: listed files over {} KiB".format(args.max_kib))
    else:
        print("Rewrote {} file(s).".format(changed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
