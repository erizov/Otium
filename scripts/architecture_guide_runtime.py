# -*- coding: utf-8 -*-
"""Dynamic imports for architecture guide scripts."""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from scripts.architecture_guide_image_common import MIN_IMAGE_BYTES
from scripts.architecture_guide_image_common import copy_city_image
from scripts.architecture_guide_image_common import extra_image_rel
from scripts.architecture_guide_image_common import has_local_image
from scripts.architecture_guide_image_common import link_additional_images
from scripts.architecture_guide_image_common import make_attach_additional_image_rows
from scripts.architecture_guide_image_common import make_attach_from_city_ref
from scripts.architecture_guide_image_common import make_load_city_index
from scripts.architecture_guide_image_common import prune_missing_additional_images
from scripts.architecture_guide_image_common import strip_internal_image_keys
from scripts.architecture_guide_modules import ArchitectureGuideModule
from scripts.architecture_guide_modules import module_config


def _import_optional(name: str) -> Any | None:
    try:
        return importlib.import_module(name)
    except ImportError:
        return None


def _noop_url_is_banned(url: str) -> bool:
    return False


def _noop_local_rel_is_banned(rel: str) -> bool:
    return False


def _default_whitelist_path(slug: str) -> Path:
    return (
        Path(__file__).resolve().parent.parent
        / slug
        / "docs"
        / "SOURCES_WHITELIST.md"
    )


@dataclass
class ArchitectureGuideParts:
    cfg: ArchitectureGuideModule
    STYLE_ORDER: tuple[str, ...]
    STYLE_META: dict[str, tuple[str, str, str, str]]
    STYLE_EXAMPLES: dict[str, list[dict[str, Any]]]
    style_example_target: Any
    pool_for_style: Any
    is_catalog_suffix_excluded: Any
    is_slug_excluded: Any
    dedupe_places_by_ru_title: Any
    apply_narrative_overrides: Any
    apply_image_url_overrides: Any
    strip_extra_images: Any
    load_city_index: Any
    attach_from_city_ref: Any
    link_additional_images: Any
    prune_missing_additional_images: Any
    strip_internal_image_keys: Any
    SINGLE_IMAGE_SLUGS: frozenset[str]
    IMAGE_URL_OVERRIDES: dict[str, Any]
    PRIMARY_IMAGE_REUSE: dict[str, Any]
    SECOND_IMAGE_REUSE: dict[str, Any]
    url_is_whitelisted: Any
    default_whitelist_path: Callable[[], Path]
    local_rel_is_banned: Any
    url_is_banned: Any
    MIN_IMAGE_BYTES: int
    extra_image_rel: Callable[[str], str]
    has_local_image: Callable[[Path, str], bool]
    copy_city_image: Callable[..., bool]
    attach_additional_image_rows: Callable[
        [dict[str, Any], dict[str, Any] | None, Path],
        None,
    ]


def load_parts(slug: str) -> ArchitectureGuideParts:
    cfg = module_config(slug)
    pkg = cfg.slug
    sc = importlib.import_module("{}.data.style_catalog".format(pkg))
    st = importlib.import_module("{}.data.style_targets".format(pkg))
    ge = importlib.import_module("{}.data.guide_exclusions".format(pkg))
    gd = importlib.import_module("{}.data.guide_dedupe".format(pkg))
    pn = importlib.import_module("{}.data.place_narratives".format(pkg))
    io = importlib.import_module("{}.data.image_overrides".format(pkg))
    gp = importlib.import_module("{}.data.guide_image_policy".format(pkg))

    ci_mod = _import_optional("{}.data.city_places_index".format(pkg))
    if ci_mod is not None:
        load_city_index = ci_mod.load_city_index
    else:
        load_city_index = make_load_city_index(cfg.city_roots)

    ir_mod = _import_optional("{}.data.image_reuse".format(pkg))
    attach_additional = make_attach_additional_image_rows(
        gp.SINGLE_IMAGE_SLUGS,
        io.IMAGE_URL_OVERRIDES,
    )
    if ir_mod is not None:
        attach_from_city_ref_fn = ir_mod.attach_from_city_ref
        link_additional = ir_mod.link_additional_images
        prune_additional = ir_mod.prune_missing_additional_images
        strip_internal = ir_mod.strip_internal_image_keys
        attach_additional = ir_mod.attach_additional_image_rows
    else:
        attach_from_city_ref_fn = make_attach_from_city_ref(attach_additional)
        link_additional = link_additional_images
        prune_additional = prune_missing_additional_images
        strip_internal = strip_internal_image_keys

    wl_mod = _import_optional("{}.whitelist".format(pkg))
    if wl_mod is not None:
        url_is_whitelisted = wl_mod.url_is_whitelisted
        default_whitelist = wl_mod.default_whitelist_path
    else:
        from scripts.city_guide_standard_whitelist import url_is_whitelisted

        default_whitelist = lambda: _default_whitelist_path(pkg)  # noqa: E731

    bi_mod = _import_optional("{}.data.banned_images".format(pkg))
    if bi_mod is not None:
        local_rel_is_banned = bi_mod.local_rel_is_banned
        url_is_banned = bi_mod.url_is_banned
    else:
        local_rel_is_banned = _noop_local_rel_is_banned
        url_is_banned = _noop_url_is_banned

    return ArchitectureGuideParts(
        cfg=cfg,
        STYLE_ORDER=sc.STYLE_ORDER,
        STYLE_META=sc.STYLE_META,
        STYLE_EXAMPLES=sc.STYLE_EXAMPLES,
        style_example_target=st.style_example_target,
        pool_for_style=ge.pool_for_style,
        is_catalog_suffix_excluded=ge.is_catalog_suffix_excluded,
        is_slug_excluded=ge.is_slug_excluded,
        dedupe_places_by_ru_title=gd.dedupe_places_by_ru_title,
        apply_narrative_overrides=pn.apply_narrative_overrides,
        apply_image_url_overrides=io.apply_image_url_overrides,
        strip_extra_images=gp.strip_extra_images,
        load_city_index=load_city_index,
        attach_from_city_ref=attach_from_city_ref_fn,
        link_additional_images=link_additional,
        prune_missing_additional_images=prune_additional,
        strip_internal_image_keys=strip_internal,
        SINGLE_IMAGE_SLUGS=gp.SINGLE_IMAGE_SLUGS,
        IMAGE_URL_OVERRIDES=io.IMAGE_URL_OVERRIDES,
        PRIMARY_IMAGE_REUSE=getattr(io, "PRIMARY_IMAGE_REUSE", {}),
        SECOND_IMAGE_REUSE=getattr(io, "SECOND_IMAGE_REUSE", {}),
        url_is_whitelisted=url_is_whitelisted,
        default_whitelist_path=default_whitelist,
        local_rel_is_banned=local_rel_is_banned,
        url_is_banned=url_is_banned,
        MIN_IMAGE_BYTES=MIN_IMAGE_BYTES,
        extra_image_rel=extra_image_rel,
        has_local_image=has_local_image,
        copy_city_image=copy_city_image,
        attach_additional_image_rows=attach_additional,
    )
