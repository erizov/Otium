# -*- coding: utf-8 -*-
"""
Shared logic for download_*_yandex.py scripts.

Fetches first N Yandex images per place (full Russian name), saves as
slug_1.jpg .. slug_N.jpg with JPG conversion and Yandex CDN handling.
"""

from __future__ import annotations

import io
import re
import time
import urllib.request
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

MIN_BYTES = 2048
# Use same min size as download_with_dedup when hashing (for forbidden/dup check)
_HASH_MIN_BYTES = 500
IMAGES_PER_PLACE_DEFAULT = 4
YANDEX_AVATARS = "avatars.mds.yandex.net"
REFERER_YANDEX = "https://yandex.ru/"
FOTO_MOS_RU_DOMAIN = "foto.mos.ru"
REFERER_FOTO_MOS = "https://foto.mos.ru/"


def basename_to_slug(basename: str) -> str:
    """name_1.jpg -> name."""
    stem = Path(basename).stem
    return re.sub(r"_\d+$", "", stem) or stem


def get_slug_from_place(place: dict[str, Any]) -> str | None:
    """Return slug from place's first image path."""
    images = place.get("images") or []
    if not images:
        return None
    path = images[0]
    bn = path.split("/")[-1] if "/" in path else path
    return basename_to_slug(bn)


def query_variants_russian(
    name: str,
    city: str = "Москва",
    extra_word: str | None = None,
) -> list[str]:
    """
    Build search query variants for this place only (place name first for
    place-specific results, not generic Moscow images).
    """
    variants = []
    if name:
        variants.append(name.strip())
    if name and city:
        variants.append("{} {}".format(name, city).strip())
    if extra_word and name and extra_word.lower() not in name.lower():
        variants.append("{} {} {}".format(name, extra_word, city).strip())
    return variants


def download_url_to_bytes(
    url: str,
    timeout: int = 20,
    referer: str | None = None,
) -> bytes | None:
    """Download URL and return raw bytes or None."""
    try:
        headers = {"User-Agent": "ExcursionGuide/1.0"}
        if referer:
            headers["Referer"] = referer
        fetch_url = url
        if any(ord(c) >= 128 for c in url):
            from scripts.download_with_dedup import _url_to_ascii
            ascii_url = _url_to_ascii(url)
            if ascii_url is not None:
                fetch_url = ascii_url
        req = urllib.request.Request(fetch_url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            ct = (resp.headers.get("Content-Type") or "").lower()
            if ct and (
                ct.startswith("text/") or "application/json" in ct
            ):
                return None
            return resp.read()
    except Exception:
        return None


def ensure_jpg(data: bytes, out_path: Path, min_bytes: int = MIN_BYTES) -> bool:
    """
    Write image bytes to out_path as JPG.
    Converts from PNG/WebP/other to JPG when possible (PIL supports WebP).
    Returns True if saved successfully.
    """
    if len(data) < min_bytes:
        return False
    try:
        from PIL import Image
        img = Image.open(io.BytesIO(data))
        # Convert WebP, PNG, etc. to RGB then save as JPEG
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        elif img.mode != "RGB":
            img = img.convert("RGB")
        img.save(out_path, "JPEG", quality=88)
        return out_path.exists() and out_path.stat().st_size >= min_bytes
    except Exception:
        # Only write raw bytes if already JPEG; do not write WebP/PNG as .jpg
        if data[:2] == b"\xff\xd8":
            out_path.write_bytes(data)
            return out_path.stat().st_size >= min_bytes
        return False


def get_actual_image_files(
    slug: str,
    images_dir: Path,
    min_bytes: int = MIN_BYTES,
    forbidden_hashes: set[str] | None = None,
) -> list[Path]:
    """
    Get actual image files from filesystem for a slug.
    
    Returns list of Path objects for files matching slug_N.jpg pattern,
    sorted by N (1, 2, 3, ...).
    
    Filters out files that match forbidden hashes if provided.
    """
    if not images_dir.exists():
        return []
    pattern = re.compile(r"^{}_(\d+)\.jpg$".format(re.escape(slug)))
    actual_files: list[tuple[int, Path]] = []
    
    # Import hash function if needed for forbidden check
    image_content_hash = None
    if forbidden_hashes:
        try:
            from scripts.image_utils import image_content_hash
        except ImportError:
            image_content_hash = None
    
    for path in images_dir.iterdir():
        if not path.is_file():
            continue
        match = pattern.match(path.name)
        if match and path.stat().st_size >= min_bytes:
            # Check if file matches forbidden hash
            if forbidden_hashes and image_content_hash:
                file_hash = image_content_hash(path, min_bytes=min_bytes)
                if file_hash and file_hash in forbidden_hashes:
                    continue  # Skip forbidden image
            num = int(match.group(1))
            actual_files.append((num, path))
    # Sort by number and return paths
    actual_files.sort(key=lambda x: x[0])
    return [p for _, p in actual_files]


def update_place_images_from_filesystem(
    place: dict[str, Any],
    images_dir: Path,
    images_subfolder: str,
    min_bytes: int = MIN_BYTES,
) -> bool:
    """
    Update place's images list to match actual filesystem files.
    
    Returns True if images list was updated, False otherwise.
    """
    slug = get_slug_from_place(place)
    if not slug:
        return False
    actual_files = get_actual_image_files(slug, images_dir, min_bytes)
    if not actual_files:
        # No files exist, clear images list
        if place.get("images"):
            place["images"] = []
            return True
        return False
    # Build expected image paths
    expected_images = [
        "images/{}/{}".format(images_subfolder, f.name)
        for f in actual_files
    ]
    # Check if update needed
    current_images = place.get("images") or []
    if current_images == expected_images:
        return False
    # Update images list to match filesystem (priority: actual files)
    place["images"] = expected_images
    return True


def items_missing_images(
    places: list[dict[str, Any]],
    output_dir: Path,
    images_subfolder: str,
    images_per_place: int = IMAGES_PER_PLACE_DEFAULT,
    min_bytes: int = MIN_BYTES,
    verbose: bool = False,
    forbidden_hashes: set[str] | None = None,
) -> list[tuple[dict[str, Any], str]]:
    """
    Return list of (place, slug) for items with fewer than N image files.
    
    PRIORITY: Actual files on disk take precedence over data structure.
    Checks actual filesystem FIRST, then syncs data structure to match.
    Only counts actual files that exist and meet size requirements.
    Filters out files that match forbidden hashes.
    Only skips place if it has exactly images_per_place files on disk.
    """
    images_dir = output_dir / "images" / images_subfolder
    images_dir.mkdir(parents=True, exist_ok=True)
    if verbose:
        print("  Checking directory: {}".format(images_dir))
        if not images_dir.exists():
            print("  WARNING: Directory does not exist!")
        if forbidden_hashes:
            print("  Filtering out {} forbidden image hash(es)".format(
                len(forbidden_hashes)
            ))
    
    result: list[tuple[dict[str, Any], str]] = []
    for place in places:
        # Try to get slug from place (from existing images in data structure)
        slug = get_slug_from_place(place)
        if not slug:
            # If no slug from data structure, we can't check files
            # This shouldn't happen in normal operation, but skip if it does
            if verbose:
                print("  {}: No slug found, skipping".format(
                    place.get("name", "?")
                ))
            continue
        
        # PRIORITY: Check actual files on disk FIRST (excluding forbidden)
        actual_files = get_actual_image_files(
            slug, images_dir, min_bytes, forbidden_hashes
        )
        actual_count = len(actual_files)
        
        # Sync data structure to match actual files (priority: actual files)
        update_place_images_from_filesystem(
            place, images_dir, images_subfolder, min_bytes
        )
        
        # Only skip if we have EXACTLY images_per_place files on disk
        if actual_count == images_per_place:
            if verbose:
                print("  {} (slug: {}): Has {} images on disk, skipping".format(
                    place.get("name", "?"), slug, actual_count
                ))
            continue
        
        # Include in result if not exactly images_per_place files
        if verbose:
            actual_names = [p.name for p in actual_files]
            if actual_count < images_per_place:
                missing_count = images_per_place - actual_count
                print("  {} (slug: {}): {} of {} images on disk (actual: {}), need {} more".format(
                    place.get("name", "?"), slug, actual_count, images_per_place,
                    ", ".join(actual_names) if actual_names else "none",
                    missing_count
                ))
            else:
                print("  {} (slug: {}): {} images on disk (expected {}), will sync".format(
                    place.get("name", "?"), slug, actual_count, images_per_place
                ))
        result.append((place, slug))
    return result


def update_data_file_for_place(
    data_file_path: Path,
    place_name: str,
    slug: str,
    images_subfolder: str,
    actual_image_files: list[Path],
) -> bool:
    """
    Update Python data file to match actual filesystem images.
    
    Finds the place by name and updates its images list to match actual files.
    Returns True if file was updated, False otherwise.
    """
    if not data_file_path.exists():
        return False
    
    content = data_file_path.read_text(encoding="utf-8")
    original_content = content
    
    # Build new images list (just basenames, e.g., ["slug_1.jpg", "slug_2.jpg"])
    image_basenames = sorted([f.name for f in actual_image_files])
    
    # Try to find place by name (handle both dict and function call formats)
    # Pattern 1: Dictionary format: "name": "Place Name", ... "images": [...]
    # Pattern 2: Function format: _m("Place Name", ..., ["img1.jpg", ...], ...)
    
    # Escape place name for regex
    escaped_name = re.escape(place_name)
    
    # Try dictionary format first
    dict_pattern = (
        r'("name"\s*:\s*"{}"[^}}]*?"images"\s*:\s*\[)([^\]]+)(\])'.format(
            escaped_name
        )
    )
    
    def replace_dict_images(match):
        prefix = match.group(1)
        suffix = match.group(3)
        # Build new images list with _img() calls
        img_calls = ", ".join(
            '_img("{}")'.format(bn) for bn in image_basenames
        )
        return prefix + img_calls + suffix
    
    content = re.sub(dict_pattern, replace_dict_images, content, flags=re.DOTALL)
    
    # Try function call format
    func_pattern = (
        r'(_[a-z]+\s*\(\s*"{}"[^)]*?,\s*\[)([^\]]+)(\]\s*,\s*[0-9.]+)'.format(
            escaped_name
        )
    )
    
    def replace_func_images(match):
        prefix = match.group(1)
        suffix = match.group(3)
        # Build new images list (just basenames in list)
        img_list = ", ".join('"{}"'.format(bn) for bn in image_basenames)
        return prefix + img_list + suffix
    
    content = re.sub(func_pattern, replace_func_images, content, flags=re.DOTALL)
    
    if content != original_content:
        data_file_path.write_text(content, encoding="utf-8")
        return True
    return False


def _get_data_file_path(
    images_subfolder: str,
    project_root: Path | None = None,
) -> Path | None:
    """
    Infer data file path from images_subfolder.
    
    Returns Path to data file (e.g., data/museums.py) or None if not found.
    """
    if project_root is None:
        # Try to infer project root from current file location
        project_root = Path(__file__).resolve().parent.parent
    
    # Map images_subfolder to data file name
    # e.g., "moscow_museums" -> "museums.py"
    subfolder_to_file = {
        "moscow_monasteries": "monasteries.py",
        "moscow_places_of_worship": "places_of_worship.py",
        "moscow_parks": "parks.py",
        "moscow_museums": "museums.py",
        "moscow_palaces": "palaces.py",
        "moscow_buildings": "buildings.py",
        "moscow_sculptures": "sculptures.py",
        "moscow_places": "places.py",
        "moscow_squares": "squares.py",
        "moscow_metro": "metro_stations.py",
        "moscow_theaters": "theaters.py",
        "moscow_viewpoints": "viewpoints.py",
        "moscow_bridges": "bridges.py",
        "moscow_markets": "markets.py",
        "moscow_libraries": "libraries.py",
        "moscow_railway_stations": "railway_stations.py",
        "moscow_cemeteries": "cemeteries.py",
        "moscow_landmarks": "landmarks.py",
        "moscow_cafes": "cafes.py",
    }
    
    filename = subfolder_to_file.get(images_subfolder)
    if not filename:
        return None
    
    data_file = project_root / "data" / filename
    return data_file if data_file.exists() else None


def download_yandex_for_guide(
    guide_label: str,
    places: list[dict[str, Any]],
    images_subfolder: str,
    output_dir: Path,
    images_per_place: int = IMAGES_PER_PLACE_DEFAULT,
    dry_run: bool = False,
    city: str = "Москва",
    extra_query_word: str | None = None,
    data_file_path: Path | None = None,
    project_root: Path | None = None,
) -> int:
    """
    For each place missing images, fetch first N from Yandex and save as
    slug_1.jpg .. slug_N.jpg. Returns count of places with at least one
    new image.
    """
    from scripts.yandex_maps_images import (
        get_place_images,
        search_yandex_images,
    )
    try:
        from scripts.download_with_dedup import (
            _load_forbidden_hashes,
            _load_failed_urls,
            _get_existing_hashes,
            _normalize_image_url,
            _yandex_url_variants,
        )
    except ImportError:
        _load_forbidden_hashes = None
        _load_failed_urls = None
        _get_existing_hashes = None
        _normalize_image_url = None
        _yandex_url_variants = None
    try:
        from scripts.image_utils import (
            image_content_hash,
            image_content_hash_from_bytes,
        )
    except ImportError:
        image_content_hash = None
        image_content_hash_from_bytes = None

    # Determine data file path if not provided
    if data_file_path is None:
        data_file_path = _get_data_file_path(images_subfolder, project_root)
    
    images_dir = output_dir / "images" / images_subfolder
    print("Checking images in: {}".format(images_dir))
    if data_file_path:
        print("Data file: {}".format(data_file_path))
    
    # First, sync all places' images lists with actual filesystem (priority: actual files)
    # This ensures data files reflect what's actually on disk
    if not dry_run:
        synced_count = 0
        data_file_updated = False
        for place in places:
            slug = get_slug_from_place(place)
            if not slug:
                continue
            # Load forbidden hashes to filter them out
            forbidden_hashes_sync: set[str] = set()
            if _load_forbidden_hashes and images_dir.exists():
                forbidden_hashes_sync = _load_forbidden_hashes(images_dir)
            
            actual_files = get_actual_image_files(
                slug, images_dir, MIN_BYTES, forbidden_hashes_sync
            )
            # Check if discrepancy exists
            current_images = place.get("images") or []
            expected_images = [
                "images/{}/{}".format(images_subfolder, f.name)
                for f in actual_files
            ]
            if current_images != expected_images:
                # Update in-memory first
                if update_place_images_from_filesystem(
                    place, images_dir, images_subfolder, MIN_BYTES
                ):
                    synced_count += 1
                # Update data file (priority: actual files)
                if data_file_path:
                    place_name = place.get("name", "?")
                    if update_data_file_for_place(
                        data_file_path, place_name, slug,
                        images_subfolder, actual_files
                    ):
                        data_file_updated = True
        if synced_count > 0:
            print("Synced {} place(s) images lists with filesystem.".format(
                synced_count
            ))
        if data_file_updated:
            print("Updated data file to match filesystem.")
    
    # Load forbidden hashes BEFORE checking missing images
    # so we can filter them out when counting existing files
    forbidden_hashes_for_check: set[str] = set()
    if _load_forbidden_hashes and images_dir.exists():
        forbidden_hashes_for_check = _load_forbidden_hashes(images_dir)
    
    missing = items_missing_images(
        places, output_dir, images_subfolder, images_per_place,
        verbose=True, forbidden_hashes=forbidden_hashes_for_check
    )
    if not missing:
        total_places = len(places)
        print("All {} {} already have {} images (checked {} places).".format(
            total_places, guide_label, images_per_place, total_places
        ))
        return 0
    print("Found {} {} with missing images (need {} per place).".format(
        len(missing), guide_label, images_per_place
    ))

    images_dir = output_dir / "images" / images_subfolder
    images_dir.mkdir(parents=True, exist_ok=True)
    forbidden_hashes: set[str] = set()
    used_hashes: set[str] = set()
    failed_urls: set[str] = set()
    if _load_forbidden_hashes and images_dir.exists():
        forbidden_hashes = _load_forbidden_hashes(images_dir)
        if forbidden_hashes:
            print("Loaded {} forbidden image hash(es) from forbidden/".format(
                len(forbidden_hashes)
            ))
    if _load_failed_urls and images_dir.exists():
        failed_urls = _load_failed_urls(images_dir)
        if failed_urls:
            print("Skipping {} previously failed URL(s)".format(len(failed_urls)))
    if _get_existing_hashes and image_content_hash_from_bytes:
        existing = _get_existing_hashes(images_dir, images_root=None)
        used_hashes = set(existing.values())
    count_updated = 0

    # Request more URLs per place so we get place-specific variety (we still save 4)
    _urls_per_place_request = max(images_per_place * 5, 20)
    # Track URLs we've already tried (by URL string) to avoid reusing across places
    tried_urls: set[str] = set()

    for place, slug in missing:
        name = place.get("name", "?")
        print("{}: {} (slug: {})".format(guide_label, name, slug))

        # Build place-specific URL list: try place name FIRST (specific),
        # then add Moscow only if needed
        urls = []
        queries_used = []
        variants = query_variants_russian(name, city, extra_query_word)
        # First pass: try place name ONLY (most specific) from all sources
        place_name_only = name.strip()
        if place_name_only:
            queries_used.append(place_name_only)
            # Try Yandex Maps with place name only
            found = get_place_images(
                place_name_only,
                city="",
                max_images=_urls_per_place_request,
                retry=1,
            )
            for u in found:
                if u not in tried_urls:
                    urls.append(u)
            # Try Yandex Images with place name only
            if len(urls) < _urls_per_place_request:
                found = search_yandex_images(
                    place_name_only,
                    city="",
                    max_images=_urls_per_place_request,
                )
                for u in found:
                    if u not in tried_urls and u not in urls:
                        urls.append(u)
            # Try foto.mos.ru with place name only
            if len(urls) < _urls_per_place_request:
                try:
                    from scripts.foto_mos_ru import search_foto_mos_ru
                    extra = search_foto_mos_ru(
                        place_name_only, max_images=_urls_per_place_request
                    )
                    for u in extra:
                        if u not in tried_urls and u not in urls:
                            urls.append(u)
                except ImportError:
                    pass
        # Second pass: if not enough, try with Moscow added
        if len(urls) < _urls_per_place_request and city:
            place_with_moscow = "{} {}".format(name, city).strip()
            if place_with_moscow not in queries_used:
                queries_used.append(place_with_moscow)
                found = get_place_images(
                    place_with_moscow,
                    city="",
                    max_images=_urls_per_place_request,
                    retry=1,
                )
                for u in found:
                    if u not in tried_urls and u not in urls:
                        urls.append(u)
                if len(urls) < _urls_per_place_request:
                    found = search_yandex_images(
                        place_with_moscow,
                        city="",
                        max_images=_urls_per_place_request,
                    )
                    for u in found:
                        if u not in tried_urls and u not in urls:
                            urls.append(u)
                if len(urls) < _urls_per_place_request:
                    try:
                        from scripts.foto_mos_ru import search_foto_mos_ru
                        extra = search_foto_mos_ru(
                            place_with_moscow, max_images=_urls_per_place_request
                        )
                        for u in extra:
                            if u not in tried_urls and u not in urls:
                                urls.append(u)
                    except ImportError:
                        pass
        # Third pass: try other variants (e.g., with extra_word) if still needed
        if len(urls) < _urls_per_place_request:
            for query in variants:
                if not query or query in queries_used:
                    continue
                queries_used.append(query)
                found = get_place_images(
                    query,
                    city="",
                    max_images=_urls_per_place_request,
                    retry=1,
                )
                for u in found:
                    if u not in tried_urls and u not in urls:
                        urls.append(u)
                if len(urls) >= _urls_per_place_request:
                    break
                found = search_yandex_images(
                    query,
                    city="",
                    max_images=_urls_per_place_request,
                )
                for u in found:
                    if u not in tried_urls and u not in urls:
                        urls.append(u)
                if len(urls) >= _urls_per_place_request:
                    break
                try:
                    from scripts.foto_mos_ru import search_foto_mos_ru
                    extra = search_foto_mos_ru(
                        query, max_images=_urls_per_place_request
                    )
                    for u in extra:
                        if u not in tried_urls and u not in urls:
                            urls.append(u)
                    if len(urls) >= _urls_per_place_request:
                        break
                except ImportError:
                    pass
        if not urls:
            print("  No images found (Yandex, foto.mos.ru).")
            continue

        primary_query = place_name_only if place_name_only else (
            queries_used[0] if queries_used else name
        )
        print("  Search: {!r} first, then {} ({} unique URLs)".format(
            primary_query[:50], "Москва" if len(queries_used) > 1 else "only",
            len(urls)
        ))
        # PRIORITY: Check actual files on disk FIRST before downloading
        # (excluding forbidden images)
        actual_files_before = get_actual_image_files(
            slug, images_dir, MIN_BYTES, forbidden_hashes
        )
        actual_count_before = len(actual_files_before)
        
        # Only skip if we have EXACTLY images_per_place files (not >=)
        if actual_count_before == images_per_place:
            print("  {} (slug: {}): Already has exactly {} images on disk, skipping download".format(
                name, slug, actual_count_before
            ))
            # Still sync data structure to match actual files
            if not dry_run:
                update_place_images_from_filesystem(
                    place, images_dir, images_subfolder, MIN_BYTES
                )
                if data_file_path:
                    actual_files = get_actual_image_files(
                        slug, images_dir, MIN_BYTES, forbidden_hashes
                    )
                    if update_data_file_for_place(
                        data_file_path, name, slug, images_subfolder, actual_files
                    ):
                        print("  Synced data file for {}".format(name))
            continue
        
        # Download missing images: loop until we have exactly images_per_place files
        downloaded = 0
        max_attempts = images_per_place * 10  # Safety limit
        attempts = 0
        reached_target = False
        
        while attempts < max_attempts and not reached_target:
            # PRIORITY: Re-check actual files on disk before each iteration
            # (excluding forbidden images)
            actual_files_current = get_actual_image_files(
                slug, images_dir, MIN_BYTES, forbidden_hashes
            )
            actual_count_current = len(actual_files_current)
            
            # Stop if we have exactly images_per_place files
            if actual_count_current == images_per_place:
                print("  {} (slug: {}): Now has exactly {} images on disk, stopping downloads".format(
                    name, slug, actual_count_current
                ))
                reached_target = True
                break
            
            # Determine which slot number to use (find first missing slot)
            existing_numbers = set()
            for f in actual_files_current:
                match = re.match(r"^{}_(\d+)\.jpg$".format(re.escape(slug)), f.name)
                if match:
                    existing_numbers.add(int(match.group(1)))
            
            # Find first missing slot number (1, 2, 3, 4...)
            slot = None
            for i in range(1, images_per_place + 1):
                if i not in existing_numbers:
                    slot = i
                    break
            
            if slot is None:
                # All slots filled but count doesn't match - this shouldn't happen
                # but if it does, break to avoid infinite loop
                print("  {} (slug: {}): All slots filled but count mismatch, stopping".format(
                    name, slug
                ))
                break
            
            basename = "{}_{}.jpg".format(slug, slot)
            path = images_dir / basename
            
            # Double-check file doesn't exist (race condition protection)
            if path.exists() and path.stat().st_size >= MIN_BYTES:
                attempts += 1
                continue
            if dry_run:
                print("  [dry-run] would save {} <- ...".format(basename))
                downloaded += 1
                continue
            saved_this_slot = False
            for url in urls:
                if url in tried_urls:
                    continue
                if url in failed_urls:
                    continue
                tried_urls.add(url)
                to_try = [url]
                if _normalize_image_url and url:
                    norm = _normalize_image_url(url)
                    if norm and norm not in to_try:
                        to_try.append(norm)
                if _yandex_url_variants and YANDEX_AVATARS in url:
                    to_try = _yandex_url_variants(url)[:5]
                data = None
                for try_url in to_try:
                    if try_url in tried_urls:
                        continue
                    if try_url in failed_urls:
                        continue
                    tried_urls.add(try_url)
                    ref = None
                    if YANDEX_AVATARS in try_url:
                        ref = REFERER_YANDEX
                    elif FOTO_MOS_RU_DOMAIN in try_url:
                        ref = REFERER_FOTO_MOS
                    data = download_url_to_bytes(try_url, referer=ref)
                    if data and len(data) >= MIN_BYTES:
                        break
                if not data:
                    continue
                # Check forbidden BEFORE saving (must have hash from bytes)
                if image_content_hash_from_bytes:
                    new_hash = image_content_hash_from_bytes(
                        data, min_bytes=_HASH_MIN_BYTES
                    )
                    if new_hash and new_hash in forbidden_hashes:
                        print("  Skipped {} (forbidden hash)".format(
                            url[:50] if url else "?"
                        ))
                        continue
                    if new_hash and new_hash in used_hashes:
                        continue
                if not ensure_jpg(data, path):
                    continue
                if image_content_hash and path.exists():
                    h = image_content_hash(path, min_bytes=_HASH_MIN_BYTES)
                    if h:
                        used_hashes.add(h)
                print("  Saved {} (from {})".format(
                    basename, url[:50] if url else "?"
                ))
                downloaded += 1
                saved_this_slot = True
                
                # PRIORITY: Immediately sync data structure with actual files after download
                # Re-check actual files on disk to get current count (excluding forbidden)
                actual_files_now = get_actual_image_files(
                    slug, images_dir, MIN_BYTES, forbidden_hashes
                )
                actual_count_now = len(actual_files_now)
                
                # Update place's images list in memory to match filesystem
                update_place_images_from_filesystem(
                    place, images_dir, images_subfolder, MIN_BYTES
                )
                
                # Update data file immediately after successful download
                if data_file_path and actual_files_now:
                    if update_data_file_for_place(
                        data_file_path, name, slug, images_subfolder, actual_files_now
                    ):
                        print("  Updated data file (now {} images on disk)".format(
                            actual_count_now
                        ))
                
                # Re-check count after save - if we have exactly images_per_place, stop
                if actual_count_now == images_per_place:
                    print("  {} now has exactly {} images on disk, stopping downloads".format(
                        name, actual_count_now
                    ))
                    reached_target = True
                    break  # Exit for url loop, while loop will exit due to flag
                break  # Successfully saved this slot, move to next iteration of while loop
            
            attempts += 1
            if not saved_this_slot and not path.exists():
                print("  Failed to download for {} (forbidden or duplicate)".format(
                    basename
                ))

        # After processing place, PRIORITY: sync images list with actual files on disk
        # (in case files were added/removed manually or from previous runs)
        if not dry_run:
            # Re-check actual files on disk to get final count (excluding forbidden)
            actual_files_final = get_actual_image_files(
                slug, images_dir, MIN_BYTES, forbidden_hashes
            )
            actual_count_final = len(actual_files_final)
            
            # Update place's images list in memory to match actual files
            update_place_images_from_filesystem(
                place, images_dir, images_subfolder, MIN_BYTES
            )
            
            # Final sync: update data file to match actual filesystem (priority: actual files)
            if data_file_path and actual_files_final:
                if update_data_file_for_place(
                    data_file_path, name, slug, images_subfolder, actual_files_final
                ):
                    print("  Final sync: data file updated ({} images on disk)".format(
                        actual_count_final
                    ))
        if downloaded:
            count_updated += 1
        # Delay between places to avoid cached/generic results
        time.sleep(3)

    return count_updated
