# -*- coding: utf-8 -*-
"""Grow small city-guide PDFs into a target size band using new place rows.

After builds, measures ``<slug>/output/<slug>_guide.pdf``. When the file is
below ``--min-mb``, appends unique ``places_of_worship`` / ``landmarks`` /
``museums`` rows with Commons JPEGs (no ``license_note`` / ``attribution``),
downloads images, rebuilds, and stops when the PDF lies in
(``--min-mb``, ``--max-mb``).

Jerusalem-style JSON (mostly ``name_en``) is updated in-place with a
``.bak`` backup. SPB / Smolensk append to optional sidecar JSON files merged
by their registries.

Requires network (Commons API), Playwright builds, and per-city download
scripts under ``scripts/download_<slug>_images.py``.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_naming import filler_place_slug
from scripts.city_guide_naming import image_rel_path_for_slug
from scripts.city_guide_naming import pdf_expand_sidecar_filename
from scripts.expand_guides_commons_batch import (  # noqa: E402
    _SEARCH_SLEEP_SEC,
    _search_first_jpeg_url,
)

_PRIMARY_GUIDE_NAME = re.compile(r"^[a-z0-9_]+_guide\.pdf$")
_BYTES_PER_MB = 1024 * 1024


def _display_city(slug: str) -> str:
    return slug.replace("_", " ").title()


def _primary_pdf_path(project_root: Path, slug: str) -> Path:
    return project_root / slug / "output" / "{}_guide.pdf".format(slug)


def _places_main_json(project_root: Path, slug: str) -> Path | None:
    p = project_root / slug / "data" / "{}_places.json".format(slug)
    return p if p.is_file() else None


def _uses_name_en_primary(rows: list[dict]) -> bool:
    """True when guide rows follow Jerusalem-style ``name_en`` cards."""
    if not rows:
        return False
    n_en = sum(1 for r in rows if (str(r.get("name_en", "")).strip()))
    return n_en >= max(1, len(rows) // 5)


def _existing_keys(rows: list[dict]) -> tuple[set[str], set[str]]:
    slugs: set[str] = set()
    names: set[str] = set()
    for r in rows:
        s = str(r.get("slug", "")).strip()
        if s:
            slugs.add(s)
        for k in ("name_en", "name_ru"):
            v = str(r.get(k, "")).strip().lower()
            if v:
                names.add(v)
    return slugs, names


def _next_filler_index(
    used_slugs: set[str],
    city_slug: str,
    category: str,
) -> int:
    """Stable per-category counter (01, 02, …)."""
    prefix = "{}_filler_{}_".format(city_slug, category)
    nn = 0
    for s in used_slugs:
        if s.startswith(prefix):
            tail = s[len(prefix) :]
            if tail.isdigit():
                nn = max(nn, int(tail))
    return nn + 1


def _queries_for_slug(slug: str, display: str) -> list[tuple[str, str]]:
    """(category, commons search phrase)."""
    if slug == "spb":
        base = "Санкт-Петербург"
        return [
            ("places_of_worship", base + " собор"),
            ("places_of_worship", base + " храм"),
            ("landmarks", base + " музей"),
            ("museums", base + " музей изобразительных"),
        ]
    if slug == "smolensk":
        b = "Смоленск"
        return [
            ("places_of_worship", b + " церковь"),
            ("places_of_worship", b + " собор"),
            ("landmarks", b + " памятник"),
        ]
    return [
        ("places_of_worship", display + " cathedral"),
        ("places_of_worship", display + " church"),
        ("places_of_worship", display + " mosque"),
        ("landmarks", display + " historic square"),
        ("museums", display + " museum"),
        ("landmarks", display + " palace"),
    ]


def _new_place_row(
    *,
    slug: str,
    place_slug: str,
    category: str,
    title: str,
    image_url: str,
    use_ru_names: bool,
    description: str | None,
    commons_query: str,
) -> dict[str, Any]:
    """Build one JSON row; no license / attribution keys (PDF stays clean)."""
    rel_img = image_rel_path_for_slug(place_slug)
    if use_ru_names:
        row: dict[str, Any] = {
            "slug": place_slug,
            "category": category,
            "name_ru": title[:120],
            "subtitle_en": _display_city(slug) + " · " + category.replace(
                "_",
                " ",
            ),
            "image_source_url": image_url,
            "image_rel_path": rel_img,
            "expand_commons_query": commons_query,
        }
        if description:
            row["description"] = description
        return row
    row = {
        "slug": place_slug,
        "category": category,
        "name_en": title[:120],
        "subtitle_en": title[:120],
        "image_source_url": image_url,
        "image_rel_path": rel_img,
        "expand_commons_query": commons_query,
    }
    if description:
        row["description"] = description
    return row


def _rag_description_for_title(
    *,
    project_root: Path,
    city_slug: str,
    title: str,
) -> str | None:
    """
    Get a short description snippet from the local RAG index.

    If RAG is not built or nothing relevant is found, return None.
    """
    try:
        from scripts.rag.query import retrieve  # local-only import
    except Exception:
        return None
    hits = retrieve(
        project_root,
        query="{} {}".format(title, city_slug.replace("_", " ")),
        city_slug=city_slug,
        language="en",
        k=3,
    )
    for h in hits:
        t = str(h.chunk.get("text") or "").strip()
        if not t:
            continue
        # Use first paragraph / sentence-like chunk as description.
        first = t.split("\n\n", 1)[0].strip()
        if first:
            return first[:450]
    return None


def _commons_row_for_query(
    slug: str,
    category: str,
    query: str,
    *,
    project_root: Path,
    use_ru_names: bool,
    used_slugs: set[str],
    used_names: set[str],
) -> dict[str, Any] | None:
    url, title = _search_first_jpeg_url(query)
    time.sleep(_SEARCH_SLEEP_SEC)
    if not url or not title:
        return None
    clean_title = title
    if clean_title.lower().startswith("file:"):
        clean_title = clean_title[5:].strip()
    low = clean_title.strip().lower()
    if low in used_names:
        return None
    nn = _next_filler_index(used_slugs, slug, category)
    ps = filler_place_slug(slug, category, nn)
    if ps in used_slugs:
        return None
    desc = _rag_description_for_title(
        project_root=project_root,
        city_slug=slug,
        title=clean_title,
    )
    return _new_place_row(
        slug=slug,
        place_slug=ps,
        category=category,
        title=clean_title,
        image_url=url,
        use_ru_names=use_ru_names,
        description=desc,
        commons_query=query,
    )


def _append_sidecar(
    project_root: Path,
    slug: str,
    new_rows: list[dict],
    *,
    dry_run: bool,
) -> None:
    if dry_run or not new_rows:
        return
    filename = pdf_expand_sidecar_filename(slug)
    path = project_root / slug / "data" / filename
    prev: list[dict] = []
    if path.is_file():
        prev = json.loads(path.read_text(encoding="utf-8"))
    bak = path.with_suffix(path.suffix + ".bak")
    if path.is_file():
        shutil.copy2(path, bak)
    merged = prev + new_rows
    path.write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _run_download(project_root: Path, slug: str) -> int:
    script = project_root / "scripts" / "download_{}_images.py".format(slug)
    if not script.is_file():
        print("No download script for {}.".format(slug), file=sys.stderr)
        return 1
    proc = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(project_root),
        check=False,
    )
    return int(proc.returncode)


def _run_build(project_root: Path, slug: str) -> int:
    script = project_root / "scripts" / "build_{}_pdf.py".format(slug)
    if not script.is_file():
        return 1
    proc = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(project_root),
        check=False,
    )
    return int(proc.returncode)


def _pdf_mb(path: Path) -> float | None:
    if not path.is_file():
        return None
    return path.stat().st_size / float(_BYTES_PER_MB)


def _collect_batch(
    slug: str,
    display: str,
    queries: list[tuple[str, str]],
    *,
    project_root: Path,
    used_slugs: set[str],
    used_names: set[str],
    use_ru_names: bool,
    batch_size: int,
) -> list[dict]:
    out: list[dict] = []
    for cat, q in queries:
        if len(out) >= batch_size:
            break
        row = _commons_row_for_query(
            slug,
            cat,
            q,
            project_root=project_root,
            use_ru_names=use_ru_names,
            used_slugs=used_slugs,
            used_names=used_names,
        )
        if row is None:
            continue
        out.append(row)
        used_slugs.add(str(row["slug"]))
        nm = str(row.get("name_en") or row.get("name_ru", "")).lower()
        if nm:
            used_names.add(nm)
    return out


def _merge_sidecar_used(
    project_root: Path,
    slug: str,
    used_slugs: set[str],
    used_names: set[str],
) -> None:
    from scripts.city_guide_registry_common import load_pdf_expand_rows

    data_dir = project_root / slug / "data"
    for r in load_pdf_expand_rows(data_dir, slug):
        s = str(r.get("slug", "")).strip()
        if s:
            used_slugs.add(s)
        for k in ("name_en", "name_ru"):
            v = str(r.get(k, "")).strip().lower()
            if v:
                used_names.add(v)


def _restore_json_backup(path: Path) -> None:
    bak = path.with_suffix(path.suffix + ".bak")
    if bak.is_file():
        shutil.copy2(bak, path)


def expand_one_slug(
    project_root: Path,
    slug: str,
    *,
    min_mb: float,
    max_mb: float,
    batch_size: int,
    max_batches: int,
    dry_run: bool,
) -> int:
    pdf = _primary_pdf_path(project_root, slug)
    main = _places_main_json(project_root, slug)
    if main is None:
        print("skip {}: no places json".format(slug), file=sys.stderr)
        return 0
    rows = json.loads(main.read_text(encoding="utf-8"))
    use_ru = slug in ("spb", "smolensk") or not _uses_name_en_primary(rows)
    if use_ru and slug not in ("spb", "smolensk"):
        print("skip {}: expects name_ru cards".format(slug), file=sys.stderr)
        return 0

    before = _pdf_mb(pdf)
    if before is None:
        print("skip {}: no PDF yet".format(slug), file=sys.stderr)
        return 0
    if before >= min_mb and before <= max_mb:
        print("{}: {:.2f} MB (already in band)".format(slug, before))
        return 0
    if before > max_mb:
        print(
            "{}: {:.2f} MB (above max; skip)".format(slug, before),
            file=sys.stderr,
        )
        return 0

    print("{}: {:.2f} MB -> expanding".format(slug, before))
    used_slugs, used_names = _existing_keys(rows)
    _merge_sidecar_used(project_root, slug, used_slugs, used_names)
    queries = _queries_for_slug(slug, _display_city(slug))
    batches = 0
    sidecar_path = (
        project_root / slug / "data" / pdf_expand_sidecar_filename(slug)
    )

    while batches < max_batches:
        mb = _pdf_mb(pdf)
        if mb is not None and mb >= min_mb and mb <= max_mb:
            print("{}: done at {:.2f} MB".format(slug, mb))
            return 0
        if mb is not None and mb > max_mb:
            print(
                "{}: overshoot {:.2f} MB; restoring last backup".format(slug, mb),
                file=sys.stderr,
            )
            if not dry_run:
                _restore_json_backup(sidecar_path)
                _run_build(project_root, slug)
            return 1

        new_batch = _collect_batch(
            slug,
            _display_city(slug),
            queries,
            project_root=project_root,
            used_slugs=used_slugs,
            used_names=used_names,
            use_ru_names=use_ru,
            batch_size=batch_size,
        )
        if not new_batch:
            print(
                "{}: no more Commons rows (stop at {:.2f} MB)".format(
                    slug,
                    mb or -1.0,
                ),
                file=sys.stderr,
            )
            return 1

        _append_sidecar(project_root, slug, new_batch, dry_run=dry_run)

        batches += 1
        if dry_run:
            print(
                "dry-run {}: would add {} place(s)".format(
                    slug,
                    len(new_batch),
                ),
            )
            return 0

        if _run_download(project_root, slug) != 0:
            return 1
        if _run_build(project_root, slug) != 0:
            return 1

    print("{}: max batches reached".format(slug), file=sys.stderr)
    return 1


def _audit(project_root: Path, *, min_mb: float) -> None:
    fg = project_root / "final_guides"
    if not fg.is_dir():
        print("No final_guides/", file=sys.stderr)
        return
    small: list[tuple[str, float]] = []
    for path in sorted(fg.glob("*_guide.pdf")):
        if not _PRIMARY_GUIDE_NAME.match(path.name):
            continue
        mb = path.stat().st_size / float(_BYTES_PER_MB)
        slug = path.name[: -len("_guide.pdf")]
        if mb < min_mb:
            small.append((slug, mb))
        print("{:24s} {:6.2f} MB".format(path.name, mb))
    print("--- below {:.1f} MB: {}".format(min_mb, len(small)))
    for slug, mb in small:
        print("  {}  {:.2f}".format(slug, mb))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=_PROJECT_ROOT,
        help="Repository root.",
    )
    parser.add_argument("--min-mb", type=float, default=15.0)
    parser.add_argument("--max-mb", type=float, default=20.0)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--max-batches", type=int, default=40)
    parser.add_argument(
        "--slugs",
        nargs="*",
        default=None,
        metavar="SLUG",
        help="Limit to these slugs (default: all small primary PDFs).",
    )
    parser.add_argument(
        "--audit-only",
        action="store_true",
        help="List primary *_guide.pdf sizes in final_guides/ and exit.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not write JSON, download, or build.",
    )
    args = parser.parse_args()
    root = args.project_root.resolve()

    if args.audit_only:
        _audit(root, min_mb=args.min_mb)
        return 0

    targets: list[str]
    if args.slugs:
        targets = sorted(set(args.slugs))
    else:
        fg = root / "final_guides"
        targets = []
        if fg.is_dir():
            for path in sorted(fg.glob("*_guide.pdf")):
                if not _PRIMARY_GUIDE_NAME.match(path.name):
                    continue
                mb = path.stat().st_size / float(_BYTES_PER_MB)
                if mb < args.min_mb:
                    targets.append(path.name[: -len("_guide.pdf")])

    if not targets:
        print("No slugs to expand (none below min size).")
        return 0

    failed = 0
    for slug in targets:
        rc = expand_one_slug(
            root,
            slug,
            min_mb=args.min_mb,
            max_mb=args.max_mb,
            batch_size=args.batch_size,
            max_batches=args.max_batches,
            dry_run=args.dry_run,
        )
        if rc != 0:
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
