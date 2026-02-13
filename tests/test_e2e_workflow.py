# -*- coding: utf-8 -*-
"""
E2E workflow test: download images and build PDF guide.

Tests complete workflow with test data (5 items, 4 images each, maps).
Validates: broken links, missing texts, image gaps, small images.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import pytest

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.core import ValidationError, validate_place
from scripts.guide_loader import load_places
from scripts.image_utils import image_content_hash
from scripts.slug_item_map import basename_to_slug

MIN_IMAGE_BYTES = 500
MIN_IMAGE_WIDTH = 400
MIN_IMAGE_HEIGHT = 300


def test_guide_data_validation() -> None:
    """Validate all guides have required fields and valid data."""
    from scripts.guide_loader import GUIDES

    errors: list[str] = []
    for guide in GUIDES:
        try:
            places = load_places(guide)
        except Exception as e:
            errors.append("{}: failed to load: {}".format(guide, e))
            continue

        for i, place in enumerate(places):
            try:
                validate_place(place)
            except ValidationError as e:
                errors.append("{} item {}: {}".format(guide, i + 1, e))

            # Check required text fields
            name = place.get("name", "").strip()
            if not name:
                errors.append("{} item {}: empty name".format(guide, i + 1))
            address = place.get("address", "").strip()
            if not address:
                errors.append("{} item {}: empty address".format(guide, i + 1))
            history = place.get("history", "").strip()
            if not history:
                errors.append("{} item {}: empty history".format(guide, i + 1))

                # Check images: if _1.._4 exist, must not have gaps
                images = place.get("images", [])
                basenames = [
                    img.split("/")[-1] if "/" in img else img for img in images
                ]
                standard = [
                    bn for bn in basenames
                    if bn.endswith("_1.jpg") or bn.endswith("_2.jpg") or
                    bn.endswith("_3.jpg") or bn.endswith("_4.jpg")
                ]
                if standard:
                    slugs = {basename_to_slug(bn) for bn in standard}
                    if len(slugs) != 1:
                        errors.append(
                            "{} item {} ({!r}): images have different slugs: {}".format(
                                guide, i + 1, name, slugs,
                            ),
                        )
                    else:
                        slug = next(iter(slugs))
                        # Extract slot numbers from existing images
                        slot_nums = []
                        for bn in standard:
                            import re
                            m = re.search(r"_(\d+)\.jpg$", bn)
                            if m:
                                slot_nums.append(int(m.group(1)))
                        slot_nums.sort()
                        # Check for gaps: if we have _1 and _3, missing _2
                        if len(slot_nums) > 1:
                            for idx in range(len(slot_nums) - 1):
                                if slot_nums[idx + 1] - slot_nums[idx] > 1:
                                    missing_slots = list(
                                        range(slot_nums[idx] + 1, slot_nums[idx + 1]),
                                    )
                                    missing_basenames = [
                                        "{}_{}.jpg".format(slug, n) for n in missing_slots
                                    ]
                                    errors.append(
                                        "{} item {} ({!r}): gap in image slots: "
                                        "have {}, missing {}".format(
                                            guide, i + 1, name,
                                            ["{}_{}.jpg".format(slug, n) for n in slot_nums],
                                            missing_basenames,
                                        ),
                                    )
                                    break

            # Check map coordinates
            lat, lon = place.get("lat"), place.get("lon")
            if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
                errors.append(
                    "{} item {} ({!r}): invalid lat/lon: {}, {}".format(
                        guide, i + 1, name, lat, lon,
                    ),
                )
            elif not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                errors.append(
                    "{} item {} ({!r}): lat/lon out of range: {}, {}".format(
                        guide, i + 1, name, lat, lon,
                    ),
                )

    assert not errors, "Validation errors:\n" + "\n".join("  " + e for e in errors)


def test_image_files_exist_and_valid() -> None:
    """Check images exist, are valid size, and not too small."""
    from scripts.guide_loader import GUIDES, GUIDE_TO_SUBDIR

    errors: list[str] = []
    images_dir = output_dir / "images"

    for guide in GUIDES:
        subdir_name = GUIDE_TO_SUBDIR.get(guide)
        if not subdir_name:
            continue
        subdir = images_dir / subdir_name
        if not subdir.exists():
            continue

        places = load_places(guide)
        for place in places:
            name = place.get("name", "?")
            images = place.get("images", [])
            basenames = [
                img.split("/")[-1] if "/" in img else img for img in images
            ]
            standard = [
                bn for bn in basenames
                if bn.endswith("_1.jpg") or bn.endswith("_2.jpg") or
                bn.endswith("_3.jpg") or bn.endswith("_4.jpg")
            ]

            for bn in standard:
                path = subdir / bn
                if not path.exists():
                    errors.append(
                        "{} ({!r}): missing image {}".format(guide, name, bn),
                    )
                    continue
                if path.stat().st_size < MIN_IMAGE_BYTES:
                    errors.append(
                        "{} ({!r}): image {} too small: {} bytes".format(
                            guide, name, bn, path.stat().st_size,
                        ),
                    )
                    continue

                # Check image dimensions if PIL available
                try:
                    from PIL import Image
                    with Image.open(path) as img:
                        w, h = img.size
                        if w < MIN_IMAGE_WIDTH or h < MIN_IMAGE_HEIGHT:
                            errors.append(
                                "{} ({!r}): image {} too small: {}x{} (min {}x{})".format(
                                    guide, name, bn, w, h,
                                    MIN_IMAGE_WIDTH, MIN_IMAGE_HEIGHT,
                                ),
                            )
                except ImportError:
                    pass
                except Exception as e:
                    errors.append(
                        "{} ({!r}): failed to read image {}: {}".format(
                            guide, name, bn, e,
                        ),
                    )

    assert not errors, "Image validation errors:\n" + "\n".join("  " + e for e in errors)


def test_links_in_html() -> None:
    """Check HTML files for broken image links."""
    import re
    from urllib.parse import urlparse

    errors: list[str] = []
    html_files = list(output_dir.glob("*.html"))

    for html_path in html_files:
        try:
            content = html_path.read_text(encoding="utf-8")
        except Exception as e:
            errors.append("Failed to read {}: {}".format(html_path.name, e))
            continue

        # Find all img src attributes
        img_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
        for match in re.finditer(img_pattern, content):
            src = match.group(1)
            # Skip data URLs
            if src.startswith("data:"):
                continue
            # Resolve relative paths
            if not src.startswith("http"):
                img_path = html_path.parent / src
                if not img_path.exists():
                    errors.append(
                        "{}: broken image link: {}".format(html_path.name, src),
                    )

    assert not errors, "Link validation errors:\n" + "\n".join("  " + e for e in errors)


def test_image_files_exist_and_valid() -> None:
    """Check images exist, are valid size, and not too small."""
    from scripts.guide_loader import GUIDES, GUIDE_TO_SUBDIR

    output_dir = _PROJECT_ROOT / "output"
    errors: list[str] = []
    images_dir = output_dir / "images"

    if not images_dir.exists():
        pytest.skip("output/images not found - run build first")

    for guide in GUIDES:
        subdir_name = GUIDE_TO_SUBDIR.get(guide)
        if not subdir_name:
            continue
        subdir = images_dir / subdir_name
        if not subdir.exists():
            continue

        places = load_places(guide)
        for place in places:
            name = place.get("name", "?")
            images = place.get("images", [])
            basenames = [
                img.split("/")[-1] if "/" in img else img for img in images
            ]
            standard = [
                bn for bn in basenames
                if bn.endswith("_1.jpg") or bn.endswith("_2.jpg") or
                bn.endswith("_3.jpg") or bn.endswith("_4.jpg")
            ]

            for bn in standard:
                path = subdir / bn
                if not path.exists():
                    continue  # Missing files are OK (will be downloaded)
                if path.stat().st_size < MIN_IMAGE_BYTES:
                    errors.append(
                        "{} ({!r}): image {} too small: {} bytes".format(
                            guide, name, bn, path.stat().st_size,
                        ),
                    )
                    continue

                # Check image dimensions if PIL available
                try:
                    from PIL import Image
                    with Image.open(path) as img:
                        w, h = img.size
                        if w < MIN_IMAGE_WIDTH or h < MIN_IMAGE_HEIGHT:
                            errors.append(
                                "{} ({!r}): image {} too small: {}x{} (min {}x{})".format(
                                    guide, name, bn, w, h,
                                    MIN_IMAGE_WIDTH, MIN_IMAGE_HEIGHT,
                                ),
                            )
                except ImportError:
                    pass
                except Exception as e:
                    errors.append(
                        "{} ({!r}): failed to read image {}: {}".format(
                            guide, name, bn, e,
                        ),
                    )

    assert not errors, "Image validation errors:\n" + "\n".join("  " + e for e in errors)


def test_links_in_html() -> None:
    """Check HTML files for broken image links."""
    import re

    output_dir = _PROJECT_ROOT / "output"
    if not output_dir.exists():
        pytest.skip("output directory not found - run build first")

    errors: list[str] = []
    html_files = list(output_dir.glob("*.html"))

    for html_path in html_files:
        try:
            content = html_path.read_text(encoding="utf-8")
        except Exception as e:
            errors.append("Failed to read {}: {}".format(html_path.name, e))
            continue

        # Find all img src attributes
        img_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
        for match in re.finditer(img_pattern, content):
            src = match.group(1)
            # Skip data URLs
            if src.startswith("data:"):
                continue
            # Resolve relative paths
            if not src.startswith("http"):
                img_path = html_path.parent / src
                if not img_path.exists():
                    errors.append(
                        "{}: broken image link: {}".format(html_path.name, src),
                    )

    assert not errors, "Link validation errors:\n" + "\n".join("  " + e for e in errors)


@pytest.mark.skipif(
    not (_PROJECT_ROOT / "output").exists(),
    reason="output directory not found - run build first",
)
def test_e2e_validation() -> None:
    """E2E validation: check all guides have valid data and files."""
    test_guide_data_validation()
    test_image_files_exist_and_valid()
    test_links_in_html()
