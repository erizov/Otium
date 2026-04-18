# -*- coding: utf-8 -*-
"""Collect local heraldry / title-strip images for web UI (PDF titul parity)."""

from __future__ import annotations

import importlib
from pathlib import Path

from scripts.city_guide_core import min_bytes_for_filename

_HERALD_IMAGE_SUFFIXES: frozenset[str] = frozenset(
    {".jpg", ".jpeg", ".png", ".svg", ".gif", ".webp"},
)


def _norm_rel(rel: str) -> str:
    return rel.replace("\\", "/").lstrip("/").lower()


def _file_usable(path: Path) -> bool:
    if not path.is_file():
        return False
    try:
        size = path.stat().st_size
    except OSError:
        return False
    return size >= min_bytes_for_filename(path.name)


def _tuples_from_pdf_module(city_slug: str) -> list[tuple[str, str]]:
    """(rel_path, alt) from build_<slug>_pdf title constants, declaration order."""
    mod_name = "scripts.build_{}_pdf".format(city_slug)
    try:
        mod = importlib.import_module(mod_name)
    except ImportError:
        return []
    out: list[tuple[str, str]] = []
    for attr in ("_TITLE_HISTORY_COATS", "_TITLE_SYMBOLS"):
        block = getattr(mod, attr, None)
        if isinstance(block, tuple):
            for item in block:
                if (
                    isinstance(item, tuple)
                    and len(item) == 2
                    and isinstance(item[0], str)
                ):
                    alt = item[1]
                    if isinstance(alt, tuple):
                        alt = "".join(alt)
                    out.append((item[0], str(alt)))
    for coat_attr, flag_attr in (
        ("_HERALD_COAT_REL", "_HERALD_FLAG_REL"),
    ):
        coat = getattr(mod, coat_attr, None)
        flag = getattr(mod, flag_attr, None)
        if isinstance(coat, str) and coat.strip():
            out.append((coat.strip(), "Герб (книжный / официальный)"))
        if isinstance(flag, str) and flag.strip():
            out.append((flag.strip(), "Флаг (книжный / официальный)"))
    return out


def _scan_guide_emblem_files(city_root: Path) -> list[tuple[str, str]]:
    """images/guide_coat* / guide_flag* not already listed in PDF tuples."""
    img_dir = city_root / "images"
    if not img_dir.is_dir():
        return []
    rows: list[tuple[str, str]] = []
    for path in sorted(img_dir.iterdir(), key=lambda p: p.name.lower()):
        if not path.is_file():
            continue
        suf = path.suffix.lower()
        if suf not in _HERALD_IMAGE_SUFFIXES:
            continue
        name_lower = path.name.lower()
        if not (
            name_lower.startswith("guide_coat")
            or name_lower.startswith("guide_flag")
        ):
            continue
        if not _file_usable(path):
            continue
        rel = "images/{}".format(path.name)
        kind = "Герб" if name_lower.startswith("guide_coat") else "Флаг"
        rows.append((rel, "{} ({})".format(kind, path.name)))
    return rows


# Moscow combined guide titul (output/images/), same as
# ``scripts.download_moscow_title_assets._MOSCOW_HERALDRY_URLS``.
MOSCOW_OUTPUT_TITLE_STRIP: tuple[tuple[str, str], ...] = (
    (
        "images/title_msk_russian_empire_lesser.svg",
        "Малый герб Российской империи",
    ),
    (
        "images/title_msk_bolshoi_basrelief_2025.jpg",
        "Барельеф герба на фасаде Большого театра",
    ),
    (
        "images/title_msk_moscow_coat_soviet.svg",
        "Герб Москвы (советский вариант)",
    ),
    (
        "images/title_msk_moscow_coat_empire.jpg",
        "Герб Москвы (Российская империя)",
    ),
)


def collect_moscow_heraldry_from_output(
    project_root: Path,
) -> list[dict[str, str]]:
    """Heraldry strip files under ``output/images/`` (URLs use ``/moscow-media``)."""
    out_root = project_root / "output"
    seen: set[str] = set()
    rows: list[dict[str, str]] = []
    for rel, alt in MOSCOW_OUTPUT_TITLE_STRIP:
        rel_clean = rel.replace("\\", "/").lstrip("/")
        key = _norm_rel(rel_clean)
        if key in seen:
            continue
        path = out_root / rel_clean
        if not _file_usable(path):
            continue
        seen.add(key)
        rows.append(
            {
                "src": "/moscow-media/{}".format(rel_clean),
                "alt": alt,
            },
        )
    return rows


def _scan_title_herald_files(city_root: Path) -> list[tuple[str, str]]:
    """
    Extra ``images/title_*`` files (exclude university titul strips).

    Catches ad-hoc local heraldry files not listed in the PDF builder.
    """
    img_dir = city_root / "images"
    if not img_dir.is_dir():
        return []
    rows: list[tuple[str, str]] = []
    for path in sorted(img_dir.iterdir(), key=lambda p: p.name.lower()):
        if not path.is_file():
            continue
        suf = path.suffix.lower()
        if suf not in _HERALD_IMAGE_SUFFIXES:
            continue
        name_lower = path.name.lower()
        if not name_lower.startswith("title_"):
            continue
        if name_lower.startswith("title_univ"):
            continue
        if not _file_usable(path):
            continue
        rel = "images/{}".format(path.name)
        caption = path.stem.replace("_", " ")
        rows.append((rel, caption))
    return rows


def collect_heraldry_images(project_root: Path, city_slug: str) -> list[dict[str, str]]:
    """
    Ordered heraldry images: PDF builder tuples, then extra title_* scans.

    Moscow uses ``output/images/title_msk_*`` (combined guide titul); URLs are
    ``/moscow-media/…``. Other cities: ``{"src": "/city/<slug>/images/…"}``.
    """
    if city_slug == "moscow":
        moscow_rows = collect_moscow_heraldry_from_output(project_root)
        if moscow_rows:
            return moscow_rows
    city_root = project_root / city_slug
    seen: set[str] = set()
    ordered: list[dict[str, str]] = []

    def add(rel: str, alt: str) -> None:
        rel_clean = rel.replace("\\", "/").lstrip("/")
        key = _norm_rel(rel_clean)
        if key in seen:
            return
        path = city_root / rel_clean
        if not _file_usable(path):
            return
        seen.add(key)
        src = "/city/{}/{}".format(city_slug, rel_clean)
        ordered.append({"src": src, "alt": alt.strip() or rel_clean})

    for rel, alt in _tuples_from_pdf_module(city_slug):
        add(rel, alt)
    for rel, alt in _scan_title_herald_files(city_root):
        add(rel, alt)
    for rel, alt in _scan_guide_emblem_files(city_root):
        add(rel, alt)
    return ordered
