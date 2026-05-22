# -*- coding: utf-8 -*-
"""Lint image_rel_path, on-disk files, slug prefix, and size caps."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_core import min_bytes_for_filename
from scripts.city_guide_image_optimize import CITY_GUIDE_IMAGE_WARN_BYTES
from scripts.city_guide_image_optimize import CITY_GUIDE_IMAGE_WARN_SIDE_PX
from scripts.city_guide_image_optimize import raster_dimensions
from scripts.city_guide_naming import LEGACY_UNPREFIXED_CITIES
from scripts.city_guide_naming import is_pdf_filler_slug
from scripts.verify_city_guide_place_images import _REGISTRY

_HERALDRY_STEMS = frozenset({
    "guide_coat_of_arms",
    "guide_flag",
})


def _load_places(module_name: str, attr: str) -> list[dict]:
    mod = importlib.import_module(module_name)
    raw = getattr(mod, attr)
    return [dict(p) for p in raw]


def lint_city(
    city_slug: str,
    module_name: str,
    attr: str,
    *,
    strict_prefix: bool,
    warn_size: bool,
) -> list[str]:
    errs: list[str] = []
    root = _PROJECT_ROOT / city_slug
    try:
        places = _load_places(module_name, attr)
    except Exception as exc:
        return ["{}: load failed: {}".format(city_slug, exc)]
    for p in places:
        if p.get("suppress_images_for_pdf"):
            continue
        slug = str(p.get("slug") or "").strip()
        rel = str(p.get("image_rel_path") or "").strip()
        name = p.get("name_en", p.get("name_ru", slug))
        if not rel:
            errs.append("{} {!r}: missing image_rel_path".format(city_slug, name))
            continue
        rel_norm = rel.replace("\\", "/").lstrip("/")
        stem = Path(rel_norm).stem
        if (
            strict_prefix
            and city_slug not in LEGACY_UNPREFIXED_CITIES
            and not is_pdf_filler_slug(slug)
            and stem not in _HERALDRY_STEMS
            and not slug.startswith(city_slug + "_")
        ):
            errs.append(
                "{} {!r}: slug {!r} should start with {!r}_".format(
                    city_slug, name, slug, city_slug,
                ),
            )
        flat_slug_image = (
            "/" not in rel_norm
            and rel_norm.startswith("images/")
            and stem == slug
        )
        if (
            slug
            and stem != slug
            and stem not in _HERALDRY_STEMS
            and not is_pdf_filler_slug(slug)
            and flat_slug_image
        ):
            errs.append(
                "{} {!r}: stem {!r} != slug {!r}".format(
                    city_slug, name, stem, slug,
                ),
            )
        path = (root / rel_norm).resolve()
        if not path.is_file():
            from scripts.city_guide_core import smallest_same_stem_image_rel

            alt = smallest_same_stem_image_rel(root, rel_norm)
            if alt and (root / alt).is_file():
                errs.append(
                    "{} {!r}: image_rel_path should be {} (found alternate)".format(
                        city_slug,
                        name,
                        alt,
                    ),
                )
            else:
                errs.append(
                    "{} {!r}: missing file {}".format(city_slug, name, rel_norm),
                )
            continue
        try:
            sz = path.stat().st_size
        except OSError:
            errs.append("{} {!r}: cannot stat {}".format(city_slug, name, rel))
            continue
        if sz < min_bytes_for_filename(path.name):
            errs.append("{} {!r}: file too small {}".format(city_slug, name, rel))
        if warn_size and path.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
            if sz > CITY_GUIDE_IMAGE_WARN_BYTES:
                errs.append(
                    "{} {!r}: raster > {} KiB ({})".format(
                        city_slug,
                        name,
                        CITY_GUIDE_IMAGE_WARN_BYTES // 1024,
                        rel_norm,
                    ),
                )
            dims = raster_dimensions(path)
            if dims and max(dims) > CITY_GUIDE_IMAGE_WARN_SIDE_PX:
                errs.append(
                    "{} {!r}: longest side {} > {} px".format(
                        city_slug,
                        name,
                        max(dims),
                        CITY_GUIDE_IMAGE_WARN_SIDE_PX,
                    ),
                )
    return errs


_BLOCKING_MARKERS = (
    "missing file",
    "missing image_rel_path",
    "file too small",
    "cannot stat",
    "should start with",
    "stem ",
    "image_rel_path should be",
)


def lint_city_blocking_errors(
    city_slug: str,
    module_name: str,
    attr: str,
    *,
    strict_prefix: bool = True,
) -> list[str]:
    """Non-size lint issues that should block guide HTML/PDF builds."""
    return [
        line
        for line in lint_city(
            city_slug,
            module_name,
            attr,
            strict_prefix=strict_prefix,
            warn_size=False,
        )
        if any(marker in line for marker in _BLOCKING_MARKERS)
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cities", nargs="*", default=None, metavar="SLUG")
    parser.add_argument(
        "--strict-prefix",
        action="store_true",
        default=True,
        help="Require {city}_ slug prefix (default on).",
    )
    parser.add_argument(
        "--no-strict-prefix",
        action="store_true",
        help="Allow legacy unprefixed slugs.",
    )
    parser.add_argument(
        "--warn-size",
        action="store_true",
        default=True,
        help="Warn when raster exceeds 400 KiB or 2048px (default on).",
    )
    parser.add_argument(
        "--fail-on-warn",
        action="store_true",
        help="Treat size warnings as errors.",
    )
    args = parser.parse_args()
    strict = args.strict_prefix and not args.no_strict_prefix
    targets = _REGISTRY
    if args.cities:
        want = frozenset(args.cities)
        targets = tuple(t for t in _REGISTRY if t[0] in want)
    all_errs: list[str] = []
    for slug, mod, attr in targets:
        all_errs.extend(
            lint_city(
                slug,
                mod,
                attr,
                strict_prefix=strict,
                warn_size=args.warn_size,
            ),
        )
    for line in all_errs:
        print(line, file=sys.stderr)
    is_error = bool(all_errs)
    if all_errs:
        print("lint_image_paths: {} issue(s)".format(len(all_errs)), file=sys.stderr)
    else:
        print("lint_image_paths: ok ({} cities)".format(len(targets)))
    if is_error and not args.fail_on_warn:
        only_soft = all(
            "KiB" in e
            or "longest side" in e
            or "should be images/" in e
            for e in all_errs
        )
        if only_soft:
            return 0
    return 1 if is_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
