# -*- coding: utf-8 -*-
"""Write Markdown inventory of per-city guide PDFs and optional output/ PDFs."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_OUT = _PROJECT_ROOT / "docs" / "CITY_GUIDE_PDF_INVENTORY.md"

_IMAGE_EXT = frozenset({
    ".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg", ".bmp", ".tif", ".tiff",
})


def _human_size(num_bytes: int) -> str:
    if num_bytes < 1024:
        return "{} B".format(num_bytes)
    n = float(num_bytes)
    for unit in ("KB", "MB", "GB", "TB"):
        if n < 1024.0 or unit == "TB":
            return "{:.2f} {}".format(n, unit)
        n /= 1024.0
    return "{:.2f} TB".format(n / 1024.0)


def _fmt_utc(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime(
        "%Y-%m-%d %H:%M UTC",
    )


def _iter_image_files(img_dir: Path) -> list[Path]:
    if not img_dir.is_dir():
        return []
    out: list[Path] = []
    for path in img_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in _IMAGE_EXT:
            out.append(path)
    return out


def _city_pdf_path(output_dir: Path, city_slug: str) -> Path | None:
    primary = output_dir / "{}_guide.pdf".format(city_slug)
    if primary.is_file():
        return primary
    cands = list(output_dir.glob("*.pdf"))
    if not cands:
        return None
    return max(cands, key=lambda p: p.stat().st_mtime)


def _collect_city_rows(root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for out_dir in sorted(root.glob("*/output")):
        city = out_dir.parent.name
        pdf = _city_pdf_path(out_dir, city)
        if pdf is None:
            continue
        st = pdf.stat()
        pdf_mtime = st.st_mtime
        pdf_size = st.st_size
        places_path = root / city / "data" / "{}_places.json".format(city)
        n_places: int | None = None
        if places_path.is_file():
            try:
                data = json.loads(places_path.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    n_places = len(data)
            except (OSError, ValueError, json.JSONDecodeError):
                n_places = None
        img_paths = _iter_image_files(root / city / "images")
        img_bytes = sum(p.stat().st_size for p in img_paths)
        html_path = out_dir / "{}_guide.html".format(city)
        mtimes = [pdf_mtime]
        if html_path.is_file():
            mtimes.append(html_path.stat().st_mtime)
        for p in img_paths:
            mtimes.append(p.stat().st_mtime)
        last_mod = max(mtimes)
        rows.append(
            {
                "slug": city,
                "display": city.replace("_", " ").title(),
                "pdf_rel": pdf.relative_to(root).as_posix(),
                "pdf_size": pdf_size,
                "pdf_mtime": pdf_mtime,
                "last_mod": last_mod,
                "n_places": n_places,
                "img_count": len(img_paths),
                "img_bytes": img_bytes,
                "total_bytes": pdf_size + img_bytes,
            },
        )
    rows.sort(key=lambda r: r["last_mod"], reverse=True)
    return rows


def _collect_output_pdf_rows(root: Path) -> list[dict[str, Any]]:
    out_root = root / "output"
    if not out_root.is_dir():
        return []
    rows: list[dict[str, Any]] = []
    for pdf in sorted(out_root.rglob("*.pdf")):
        if not pdf.is_file():
            continue
        st = pdf.stat()
        rows.append(
            {
                "rel": pdf.relative_to(root).as_posix(),
                "size": st.st_size,
                "mtime": st.st_mtime,
            },
        )
    rows.sort(key=lambda r: r["mtime"], reverse=True)
    return rows


def _markdown_city_table(rows: list[dict[str, Any]]) -> str:
    lines = [
        "| City | Guide PDF (path) | PDF size | PDF modified (UTC) | "
        "Last change — city assets (UTC) | Places | Images | "
        "Images total | PDF + images |",
        "|------|------------------|----------|----------------------|"
        "----------------------------------|--------|--------|"
        "--------------|----------------|",
    ]
    for r in rows:
        lines.append(
            "| {display} | `{pdf_rel}` | {pdf_sz} | {pdf_m} | {lm} | "
            "{np} | {ic} | {ib} | {tb} |".format(
                display=r["display"],
                pdf_rel=r["pdf_rel"],
                pdf_sz=_human_size(r["pdf_size"]),
                pdf_m=_fmt_utc(r["pdf_mtime"]),
                lm=_fmt_utc(r["last_mod"]),
                np="—" if r["n_places"] is None else str(r["n_places"]),
                ic=str(r["img_count"]),
                ib=_human_size(r["img_bytes"]),
                tb=_human_size(r["total_bytes"]),
            ),
        )
    return "\n".join(lines) + "\n"


def _markdown_output_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No files under `output/`._\n"
    lines = [
        "| Path | Size | Modified (UTC) |",
        "|------|------|------------------|",
    ]
    for r in rows:
        lines.append(
            "| `{rel}` | {sz} | {mt} |".format(
                rel=r["rel"],
                sz=_human_size(r["size"]),
                mt=_fmt_utc(r["mtime"]),
            ),
        )
    total = sum(r["size"] for r in rows)
    lines.append("")
    lines.append(
        "**Subtotal:** {} PDF(s), {} combined.".format(
            len(rows),
            _human_size(total),
        ),
    )
    lines.append("")
    return "\n".join(lines)


def build_markdown(
    *,
    root: Path,
    include_output: bool,
) -> str:
    city_rows = _collect_city_rows(root)
    sum_pdf = sum(r["pdf_size"] for r in city_rows)
    sum_img = sum(r["img_bytes"] for r in city_rows)
    sum_all = sum(r["total_bytes"] for r in city_rows)
    out_rows = _collect_output_pdf_rows(root) if include_output else []
    out_total = sum(r["size"] for r in out_rows)

    parts: list[str] = [
        "# City guide PDF inventory\n",
        "Generated by `scripts/report_city_pdf_inventory.py`. "
        "**Last change** per city = newest of guide PDF, "
        "`*_guide.html`, and all files under `<city>/images/` "
        "(recursive; common raster and SVG extensions).\n",
        "## Per-city guides\n",
        _markdown_city_table(city_rows),
        "### Roll-up (per-city folders only)\n",
        "| Metric | Value |",
        "|--------|-------|",
        "| Cities with `{{slug}}/output/*_guide.pdf` | {} |".format(
            len(city_rows),
        ),
        "| All guide PDFs | {} |".format(_human_size(sum_pdf)),
        "| All `images/` | {} |".format(_human_size(sum_img)),
        "| PDF + images | {} |".format(_human_size(sum_all)),
        "",
    ]
    if include_output:
        parts.extend(
            [
                "## Other PDFs under `output/`\n",
                "Moscow theme guides, backups, `fullpdf/`, `optpdf/`, etc. "
                "(not tied to `<city>/output/` city folders).\n",
                _markdown_output_table(out_rows),
                "| Metric | Value |",
                "|--------|-------|",
                "| PDF files under `output/` | {} |".format(len(out_rows)),
                "| Combined size | {} |".format(_human_size(out_total)),
                "",
            ],
        )
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="write to docs/CITY_GUIDE_PDF_INVENTORY.md (default path)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="write markdown to this path (implies write; overrides --write)",
    )
    parser.add_argument(
        "--no-output-tree",
        action="store_true",
        help="omit the `output/` PDF listing (only per-city guides)",
    )
    args = parser.parse_args()
    include_output = not args.no_output_tree
    text = build_markdown(
        root=_PROJECT_ROOT,
        include_output=include_output,
    )
    out_path = args.out
    if out_path is None and args.write:
        out_path = _DEFAULT_OUT
    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
        print("Wrote", out_path, file=sys.stderr)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
