# -*- coding: utf-8 -*-
"""
Download images with per-download duplicate checking.

Downloads images one by one, checking after each download if it's a duplicate
of any existing file in the folder. Ensures each item gets exactly 4 distinct
images before proceeding.
"""

from __future__ import annotations

import shutil
import sys
import time
import urllib.request
from pathlib import Path
from typing import Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.image_utils import image_content_hash
from scripts.slug_item_map import basename_to_slug

MIN_IMAGE_BYTES = 500

# Basenames to skip downloading (forbidden images)
FORBIDDEN_BASENAMES: frozenset[str] = frozenset({
    "znamensky_4.jpg",
    "marfo_mariinsky_1.jpg",
})

# Hashes of forbidden images (skip any download matching these).
# Loaded from forbidden/ subfolder at runtime and merged with this set.
# Add known-bad hashes here for faster skip without scanning forbidden/.
FORBIDDEN_IMAGE_HASHES: frozenset[str] = frozenset()

FORBIDDEN_SUBDIR_NAME = "forbidden"

# Placeholder or non-image URLs to skip
_SKIP_URL_PREFIXES = ("https://example.com/", "http://example.com/", "https://yandex.ru/clck/")
_YANDEX_AVATARS = "avatars.mds.yandex.net"


def _normalize_image_url(url: str) -> str | None:
    """
    Return a downloadable image URL, or None if not usable.
    Fixes Yandex template URLs (e.g. .../%s or .../%).
    """
    if not url or not url.strip():
        return None
    url = url.strip()
    if any(url.startswith(p) for p in _SKIP_URL_PREFIXES):
        return None
    if url.startswith("//"):
        url = "https:" + url
    if _YANDEX_AVATARS in url:
        # Yandex template: replace %s or trailing /% with /orig
        if "%s" in url:
            url = url.replace("%s", "orig")
        if url.rstrip("/").endswith("/%"):
            url = url.rstrip("/").rstrip("%") + "orig"
        if "/%" in url:
            url = url.replace("/%", "/orig")
    if not url.startswith("http"):
        return None
    # Skip non-image resources
    if ".js" in url or "/jclck/" in url:
        return None
    return url


def _yandex_url_variants(url: str) -> list[str]:
    """
    For a Yandex avatars URL, return a list of URLs to try (different sizes).
    """
    if _YANDEX_AVATARS not in url:
        return [url]
    normalized = _normalize_image_url(url)
    if not normalized:
        return []
    # Same URL may support size suffix; try alternates as fallbacks
    variants = [normalized]
    if "/get-altay/" in normalized or "/get-vh/" in normalized:
        base = normalized
        for size in ("XXXL", "L_height", "M_height", "orig"):
            if size in base:
                continue
            if base.endswith("orig"):
                alt = base[:-4] + size
            else:
                alt = base.rstrip("/") + "/" + size
            if alt != base and alt not in variants:
                variants.append(alt)
    return variants[:5]  # Cap so we don't try too many


def _load_forbidden_hashes(images_dir: Path) -> set[str]:
    """
    Load content hashes of all images in images_dir/forbidden/.
    Used to skip downloads that match known-bad images (fast check).
    """
    forbidden_dir = images_dir / FORBIDDEN_SUBDIR_NAME
    out: set[str] = set()
    if not forbidden_dir.exists() or not forbidden_dir.is_dir():
        return out
    for path in forbidden_dir.iterdir():
        if not path.is_file():
            continue
        if path.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
            continue
        if path.stat().st_size < MIN_IMAGE_BYTES:
            continue
        h = image_content_hash(path, min_bytes=MIN_IMAGE_BYTES)
        if h:
            out.add(h)
    return out


def _get_existing_hashes(images_dir: Path, images_root: Optional[Path] = None) -> dict[str, str]:
    """
    Get content hash for all existing image files in directory and all subdirs.

    If images_root is provided, scans all subdirectories in images_root.
    Skips the forbidden/ subfolder. Returns: {filename: hash, ...}
    """
    existing: dict[str, str] = {}

    def _scan_dir(directory: Path) -> None:
        if not directory.exists():
            return
        for path in directory.iterdir():
            if path.is_dir():
                if path.name == FORBIDDEN_SUBDIR_NAME:
                    continue
                continue
            if path.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
                continue
            if path.stat().st_size < MIN_IMAGE_BYTES:
                continue
            h = image_content_hash(path, min_bytes=MIN_IMAGE_BYTES)
            if h:
                existing[path.name] = h

    # If images_root provided, scan all subdirs (each guide subdir)
    if images_root and images_root.exists():
        for subdir in images_root.iterdir():
            if not subdir.is_dir() or subdir.name == FORBIDDEN_SUBDIR_NAME:
                continue
            _scan_dir(subdir)
    _scan_dir(images_dir)
    return existing


def _is_duplicate(
    new_path: Path,
    existing_hashes: dict[str, str],
    images_dir: Path,
) -> Optional[str]:
    """
    Check if newly downloaded file is duplicate of any existing file.

    Returns: existing filename if duplicate, None otherwise.
    """
    if not new_path.exists() or new_path.stat().st_size < MIN_IMAGE_BYTES:
        return None
    new_hash = image_content_hash(new_path, min_bytes=MIN_IMAGE_BYTES)
    if not new_hash:
        return None
    for existing_name, existing_hash in existing_hashes.items():
        if existing_hash == new_hash:
            return existing_name
    return None


def _validate_uniqueness(
    path: Path,
    existing_hashes: dict[str, str],
    current_basename: str,
) -> tuple[bool, Optional[str]]:
    """
    Validate that the image at path is unique.

    Returns (True, None) if unique, (False, existing_name) if duplicate.
    """
    if not path.exists() or path.stat().st_size < MIN_IMAGE_BYTES:
        return False, None
    h = image_content_hash(path, min_bytes=MIN_IMAGE_BYTES)
    if not h:
        return False, None
    for existing_name, existing_hash in existing_hashes.items():
        if existing_name == current_basename:
            continue
        if existing_hash == h:
            return False, existing_name
    return True, None


def download_images_with_dedup(
    images_dir: Path,
    image_downloads: dict[str, str],
    image_fallbacks: dict[str, list[str]],
    banned: frozenset[str],
    items: list[dict],
    max_attempts_per_item: int = 20,
    images_root: Optional[Path] = None,
    forbidden_basenames: Optional[frozenset[str]] = None,
    use_ai_identify: bool = False,
    guide_name: str = "",
    force_overwrite: bool = False,
) -> dict[str, int]:
    """
    Download images with per-download duplicate checking.

    By default existing image files are not overwritten. Use force_overwrite
    to replace duplicates or re-download. For each item, up to 4 distinct
    images; after each download, validates uniqueness.

    Args:
        images_dir: Directory to save images
        image_downloads: {basename: url, ...}
        image_fallbacks: {basename: [url, ...], ...}
        banned: Set of banned basenames
        items: List of item dicts with 'name' and 'images' keys
        max_attempts_per_item: Max URLs to try per item
        images_root: If set, check hashes in all subdirs
        forbidden_basenames: Basenames to skip (e.g. znamensky_4.jpg).
        use_ai_identify: If True, use AI to check image matches item.
        guide_name: Guide name for AI context (e.g. monasteries).
        force_overwrite: If True, replace existing duplicates; default False.

    Returns:
        {item_name: count_of_distinct_images_downloaded, ...}
    """
    images_dir.mkdir(parents=True, exist_ok=True)
    forbidden_dir = images_dir / FORBIDDEN_SUBDIR_NAME
    forbidden_dir.mkdir(parents=True, exist_ok=True)
    if forbidden_basenames is None:
        forbidden_basenames = FORBIDDEN_BASENAMES
    # Load forbidden hashes from forbidden/ subfolder + constant (fast skip)
    forbidden_hashes = _load_forbidden_hashes(images_dir) | set(FORBIDDEN_IMAGE_HASHES)
    existing_hashes = _get_existing_hashes(images_dir, images_root=images_root)

    # Build item -> list of image basenames mapping
    from scripts.validate_images_per_item import _basename

    item_to_basenames: dict[str, list[str]] = {}
    basename_to_item: dict[str, str] = {}
    for item in items:
        name = item.get("name", "?")
        images = item.get("images") or []
        basenames = [_basename(img) for img in images]
        item_to_basenames[name] = basenames
        for bn in basenames:
            basename_to_item[bn] = name

    results: dict[str, int] = {}
    downloaded_count = 0

    # Process each item to get 4 distinct images
    for item in items:
        item_name = item.get("name", "?")
        basenames = item_to_basenames.get(item_name, [])

        # Filter to only _1, _2, _3, _4 images (standard format)
        # Sort to ensure _1, _2, _3, _4 order
        standard_basenames = sorted([
            bn for bn in basenames
            if bn.endswith("_1.jpg") or bn.endswith("_2.jpg") or
            bn.endswith("_3.jpg") or bn.endswith("_4.jpg")
        ])
        if len(standard_basenames) < 4:
            # Need exactly 4 images in standard format
            print(
                "  Warning: {} has only {} standard format images, "
                "need 4".format(item_name, len(standard_basenames)),
            )

        distinct_count = 0

        # Process exactly 4 basenames (_1, _2, _3, _4)
        if len(standard_basenames) < 4:
            results[item_name] = distinct_count
            continue

        for basename in standard_basenames[:4]:
            if distinct_count >= 4:
                break
            if basename in banned or basename in forbidden_basenames:
                if basename in forbidden_basenames:
                    path = images_dir / basename
                    if path.exists() and path.is_file():
                        dest = forbidden_dir / basename
                        if dest != path:
                            shutil.move(str(path), str(dest))
                            print(
                                "  Moved to forbidden: {} (skipping)".format(
                                    basename,
                                ),
                            )
                        else:
                            print("  Skipping forbidden image: {}".format(basename))
                    else:
                        print("  Skipping forbidden image: {}".format(basename))
                continue

            path = images_dir / basename
            attempts_for_this_basename = 0
            # Refresh hash list to include any files downloaded for previous items
            existing_hashes = _get_existing_hashes(images_dir, images_root=images_root)
            
            # If file already exists and is valid, check if distinct
            if path.exists() and path.stat().st_size >= MIN_IMAGE_BYTES:
                this_hash = image_content_hash(path, min_bytes=MIN_IMAGE_BYTES)
                if not this_hash:
                    # Invalid file: only replace if force_overwrite
                    if force_overwrite:
                        path.unlink()
                    else:
                        continue
                else:
                    # Check against ALL existing files (no duplicates allowed)
                    is_dup = False
                    dup_of_name: Optional[str] = None
                    for existing_name, existing_hash in existing_hashes.items():
                        if existing_name == basename:
                            continue
                        if existing_hash == this_hash:
                            is_dup = True
                            dup_of_name = existing_name
                            break

                    if is_dup and dup_of_name:
                        if force_overwrite:
                            print(
                                "  Existing file {} is duplicate of {}, "
                                "replacing".format(basename, dup_of_name),
                            )
                            path.unlink()
                            if basename in existing_hashes:
                                del existing_hashes[basename]
                        else:
                            print(
                                "  Existing file {} is duplicate of {} "
                                "(skip; use --force-overwrite to replace)".format(
                                    basename, dup_of_name,
                                ),
                            )
                            continue

                    if not is_dup:
                        # File is distinct, count it
                        distinct_count += 1
                        if basename not in existing_hashes:
                            existing_hashes[basename] = this_hash
                        continue

            # Try to download (either missing file or duplicate that was deleted)
            # Refresh existing_hashes to include all files currently in folder
            existing_hashes = _get_existing_hashes(images_dir, images_root=images_root)
            
            raw_urls = [image_downloads.get(basename)] + list(
                image_fallbacks.get(basename, []),
            )
            urls_to_try = []
            seen: set[str] = set()
            for u in raw_urls:
                if not u:
                    continue
                norm = _normalize_image_url(u)
                if not norm or norm in seen:
                    continue
                if _YANDEX_AVATARS in norm:
                    for variant in _yandex_url_variants(u):
                        v = _normalize_image_url(variant) or variant
                        if v not in seen:
                            urls_to_try.append(v)
                            seen.add(v)
                else:
                    urls_to_try.append(norm)
                    seen.add(norm)
            urls_to_try = urls_to_try[:20]

            downloaded_this_slot = False
            for url in urls_to_try:
                attempts_for_this_basename += 1
                if attempts_for_this_basename > 20:  # Max URLs per basename
                    break
                try:
                    req = urllib.request.Request(
                        url,
                        headers={"User-Agent": "ExcursionGuide/1.0"},
                    )
                    with urllib.request.urlopen(req, timeout=15) as resp:
                        data = resp.read()
                    if len(data) < MIN_IMAGE_BYTES:
                        continue

                    # Write to temp file first
                    temp_path = images_dir / (basename + ".tmp")
                    temp_path.write_bytes(data)

                    # Validate uniqueness before accepting
                    current_hashes = _get_existing_hashes(
                        images_dir, images_root=images_root,
                    )
                    new_hash = image_content_hash(temp_path, min_bytes=MIN_IMAGE_BYTES)
                    if new_hash:
                        if new_hash in forbidden_hashes:
                            dest = forbidden_dir / "rejected_{}_{}.jpg".format(
                                path.stem, new_hash[:8],
                            )
                            try:
                                shutil.copy2(str(temp_path), str(dest))
                            except OSError:
                                pass
                            temp_path.unlink()
                            print(
                                "  Skipped (forbidden hash): {}, trying next URL".format(
                                    basename,
                                ),
                            )
                            time.sleep(0.2)
                            continue
                        is_unique, dup_of = _validate_uniqueness(
                            temp_path, current_hashes, basename,
                        )
                        if not is_unique and dup_of:
                            print(
                                "  Validation failed (duplicate, same as {}), "
                                "trying next URL".format(dup_of),
                            )
                            temp_path.unlink()
                            time.sleep(0.2)
                            continue

                    # Optional: AI image identification
                    if use_ai_identify:
                        try:
                            from scripts.image_identify import image_matches_item
                            if not image_matches_item(
                                temp_path, item_name,
                                guide_context=guide_name or "place",
                            ):
                                print(
                                    "  AI: image does not match '{}', "
                                    "trying next URL".format(item_name),
                                )
                                temp_path.unlink()
                                time.sleep(0.2)
                                continue
                        except Exception as e:
                            print(
                                "  AI check failed ({}), accepting image.".format(e),
                                file=sys.stderr,
                            )

                    # Accept: rename temp to final
                    temp_path.rename(path)
                    # Validate again after save (ensure still unique)
                    current_hashes = _get_existing_hashes(
                        images_dir, images_root=images_root,
                    )
                    ok, dup_of = _validate_uniqueness(path, current_hashes, basename)
                    if not ok and dup_of:
                        print(
                            "  Validation failed after save (duplicate of {}), "
                            "trying next URL".format(dup_of),
                        )
                        path.unlink()
                        if basename in existing_hashes:
                            del existing_hashes[basename]
                        time.sleep(0.2)
                        continue

                    final_hash = image_content_hash(path, min_bytes=MIN_IMAGE_BYTES)
                    if final_hash:
                        existing_hashes[basename] = final_hash
                    distinct_count += 1
                    downloaded_count += 1
                    downloaded_this_slot = True
                    print(
                        "  Downloaded distinct image: {} ({}/4 for {})".format(
                            basename, distinct_count, item_name,
                        ),
                    )
                    time.sleep(0.3)
                    break
                except Exception as e:
                    temp_path = images_dir / (basename + ".tmp")
                    if temp_path.exists():
                        temp_path.unlink()
                    continue

            # If we couldn't download a distinct image for this slot, skip it
            if not downloaded_this_slot and not path.exists():
                print(
                    "  Warning: Could not download distinct image for {} "
                    "({} URLs tried)".format(basename, len(urls_to_try)),
                )

        results[item_name] = distinct_count

    print(
        "\nDownload summary: {} distinct images downloaded across {} items".format(
            downloaded_count, len(results),
        ),
    )
    return results


def validate_item_images_format(
    items: list[dict],
    images_dir: Path,
    guide_name: str = "guide",
) -> tuple[bool, list[str]]:
    """
    Validate that each item has exactly 4 images in format name_1, name_2, name_3, name_4.

    Checks forbidden folder every time: files whose hash is in forbidden/ (or
    FORBIDDEN_IMAGE_HASHES) are treated as missing. Images are distinct, no duplicates.

    Returns: (is_valid, list_of_errors)
    """
    from scripts.validate_images_per_item import _basename

    forbidden_hashes = _load_forbidden_hashes(images_dir) | set(FORBIDDEN_IMAGE_HASHES)
    errors: list[str] = []

    for i, item in enumerate(items, 1):
        name = item.get("name", "?")
        images = item.get("images") or []
        basenames = [_basename(img) for img in images]

        # Filter to standard format (_1, _2, _3, _4) and sort
        standard_basenames = sorted([
            bn for bn in basenames
            if bn.endswith("_1.jpg") or bn.endswith("_2.jpg") or
            bn.endswith("_3.jpg") or bn.endswith("_4.jpg")
        ])

        if len(standard_basenames) != 4:
            errors.append(
                "{} item {} ({!r}): expected exactly 4 images in format "
                "name_1.jpg, name_2.jpg, name_3.jpg, name_4.jpg, got {}: {}".format(
                    guide_name, i, name, len(standard_basenames),
                    standard_basenames,
                ),
            )
            continue

        # Verify format: must have _1, _2, _3, _4
        expected_suffixes = {"_1.jpg", "_2.jpg", "_3.jpg", "_4.jpg"}
        actual_suffixes = {bn[-6:] for bn in standard_basenames}
        if actual_suffixes != expected_suffixes:
            errors.append(
                "{} item {} ({!r}): missing required suffixes. "
                "Expected: {}, Got: {}".format(
                    guide_name, i, name, sorted(expected_suffixes),
                    sorted(actual_suffixes),
                ),
            )
            continue

        # Check all 4 files exist (and are not in forbidden folder by hash)
        missing = []
        for bn in standard_basenames:
            path = images_dir / bn
            if not path.exists() or path.stat().st_size < MIN_IMAGE_BYTES:
                missing.append(bn)
                continue
            h = image_content_hash(path, min_bytes=MIN_IMAGE_BYTES)
            if h and h in forbidden_hashes:
                missing.append(bn)
        if missing:
            errors.append(
                "{} item {} ({!r}): missing files: {}".format(
                    guide_name, i, name, missing,
                ),
            )
            continue

        # Check all 4 are distinct (different content hash)
        # Also check against all other items in the guide
        hashes = []
        all_other_hashes: set[str] = set()
        
        # Collect hashes from all other items first
        for j, other_item in enumerate(items, 1):
            if j == i:
                continue
            other_images = other_item.get("images") or []
            other_basenames = [_basename(img) for img in other_images]
            other_standard = sorted([
                bn for bn in other_basenames
                if bn.endswith("_1.jpg") or bn.endswith("_2.jpg") or
                bn.endswith("_3.jpg") or bn.endswith("_4.jpg")
            ])
            for other_bn in other_standard:
                other_path = images_dir / other_bn
                if not other_path.exists():
                    continue
                other_h = image_content_hash(
                    other_path, min_bytes=MIN_IMAGE_BYTES,
                )
                if other_h and other_h not in forbidden_hashes:
                    all_other_hashes.add(other_h)
        
        for bn in standard_basenames:
            path = images_dir / bn
            h = image_content_hash(path, min_bytes=MIN_IMAGE_BYTES)
            if not h:
                errors.append(
                    "{} item {} ({!r}): could not hash {}".format(
                        guide_name, i, name, bn,
                    ),
                )
                break
            hashes.append(h)
            
            # Check if this image is duplicate of another item
            if h in all_other_hashes:
                errors.append(
                    "{} item {} ({!r}): image {} is duplicate of another item".format(
                        guide_name, i, name, bn,
                    ),
                )

        if len(hashes) == 4 and len(set(hashes)) < 4:
            errors.append(
                "{} item {} ({!r}): duplicate images within item (need 4 "
                "distinct images per item)".format(guide_name, i, name),
            )

    return len(errors) == 0, errors
