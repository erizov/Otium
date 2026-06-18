# -*- coding: utf-8 -*-
"""
Fill missing Moscow guide images from Moscow_Complete_Guide HTML/PDF.

For buildings, palaces, and places_of_worship: copy on-disk files referenced
in the Complete HTML, or extract embedded photos from the Complete PDF.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html import unescape
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_core import (
    MIN_IMAGE_BYTES,
    place_has_pdf_image,
    smallest_same_stem_image_rel,
)

TARGET_CATEGORIES = frozenset({
    "buildings",
    "palaces",
    "places_of_worship",
})

CHAPTER_TO_CATEGORY: dict[int, str] = {
    1: "monasteries",
    2: "places_of_worship",
    3: "parks",
    4: "museums",
    5: "palaces",
    6: "buildings",
}

CHAPTER_IDS = frozenset({
    ch for ch, cat in CHAPTER_TO_CATEGORY.items() if cat in TARGET_CATEGORIES
})

_SECTION_RE = re.compile(
    r'<section class="monastery" id="ch-(\d+)-p\d+"[^>]*>'
    r"(.*?)</section>",
    re.DOTALL,
)
_TITLE_RE = re.compile(
    r'<h2 class="monastery-title">(.*?)</h2>',
    re.DOTALL,
)
_TAG_RE = re.compile(r"<[^>]+>")
_IMG_RE = re.compile(
    r'<img[^>]+src="([^"]+)"[^>]*class="monastery-img"',
    re.IGNORECASE,
)


def _norm(name: str) -> str:
    s = unescape(name or "").strip().lower()
    s = re.sub(r"^\d+\.\s*", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.replace("ё", "е")


def _strip_title(html_title: str) -> str:
    text = _TAG_RE.sub("", html_title)
    text = unescape(text).strip()
    text = re.sub(r"^\d+\.\s*", "", text)
    return text.strip()


def _parse_complete_sections(html_path: Path) -> dict[str, list[str]]:
    """Map normalized title -> local image rel paths from Complete HTML."""
    text = html_path.read_text(encoding="utf-8")
    out: dict[str, list[str]] = {}
    for m in _SECTION_RE.finditer(text):
        ch = int(m.group(1))
        if ch not in CHAPTER_IDS:
            continue
        body = m.group(2)
        tm = _TITLE_RE.search(body)
        if not tm:
            continue
        title = _strip_title(tm.group(1))
        imgs: list[str] = []
        row = body.split('<div class="images-row">', 1)
        if len(row) > 1:
            chunk = row[1].split("</div>", 1)[0]
            for src in _IMG_RE.findall(chunk):
                src = unescape(src).strip()
                if src.startswith("images/") and not src.startswith("http"):
                    imgs.append(src.replace("\\", "/"))
        if title:
            out[_norm(title)] = imgs
    return out


def _load_json_places() -> list[dict[str, Any]]:
    path = _PROJECT_ROOT / "moscow" / "data" / "moscow_places.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _missing_rels(root: Path, place: dict[str, Any]) -> list[str]:
    rels: list[str] = []
    main = str(place.get("image_rel_path") or "").strip()
    if main and not smallest_same_stem_image_rel(root, main):
        rels.append(main)
    for extra in place.get("additional_images") or []:
        er = str(extra.get("image_rel_path") or "").strip()
        if er and not smallest_same_stem_image_rel(root, er):
            rels.append(er)
    return rels


def _copy_file(root: Path, src_rel: str, dest_rel: str) -> bool:
    src = root / src_rel.replace("\\", "/")
    if not src.is_file() or src.stat().st_size < MIN_IMAGE_BYTES:
        return False
    dest = root / dest_rel.replace("\\", "/")
    if dest.is_file() and dest.stat().st_size >= MIN_IMAGE_BYTES:
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(src.read_bytes())
    return True


def _is_map_image(width: int, height: int, size: int) -> bool:
    if size < MIN_IMAGE_BYTES:
        return True
    if width <= 0 or height <= 0:
        return size < 8000
    ratio = width / float(height)
    return ratio > 2.8 or (width < 200 and height < 200)


def _build_pdf_index(doc: Any) -> tuple[list[str], dict[int, list[tuple[int, bytes, str]]]]:
    """Page normalized text + per-page photo candidates (size, bytes, ext)."""
    page_text: list[str] = []
    page_images: dict[int, list[tuple[int, bytes, str]]] = {}
    seen_xref: set[int] = set()
    for i in range(len(doc)):
        page_text.append(_norm(doc[i].get_text()))
        imgs: list[tuple[int, bytes, str]] = []
        for info in doc[i].get_images(full=True):
            xref = int(info[0])
            if xref in seen_xref:
                continue
            seen_xref.add(xref)
            try:
                extracted = doc.extract_image(xref)
            except Exception:
                continue
            data = extracted.get("image") or b""
            ext = str(extracted.get("ext") or "jpg").lower()
            w = int(extracted.get("width") or info[2] or 0)
            h = int(extracted.get("height") or info[3] or 0)
            if _is_map_image(w, h, len(data)):
                continue
            if len(data) < MIN_IMAGE_BYTES:
                continue
            imgs.append((len(data), data, ext))
        imgs.sort(key=lambda t: t[0], reverse=True)
        page_images[i] = [(d, e) for _, d, e in imgs]
    return page_text, page_images


def _pages_for_title(page_text: list[str], title_norm: str) -> list[int]:
    short = title_norm[: min(28, len(title_norm))]
    hits: list[int] = []
    for i, pt in enumerate(page_text):
        if title_norm in pt or (len(short) >= 12 and short in pt):
            hits.append(i)
    if not hits:
        return []
    extended = sorted(set(hits + [p + 1 for p in hits if p + 1 < len(page_text)]))
    return extended


def _pdf_images_for_pages(
    page_nums: list[int],
    page_images: dict[int, list[tuple[bytes, str]]],
) -> list[tuple[bytes, str]]:
    out: list[tuple[bytes, str]] = []
    seen_sizes: set[int] = set()
    for pn in page_nums:
        for data, ext in page_images.get(pn, []):
            sig = len(data)
            if sig in seen_sizes:
                continue
            seen_sizes.add(sig)
            out.append((data, ext))
    return out


def _write_image(dest: Path, data: bytes, ext: str, rel: str) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    suffix = Path(rel).suffix.lower().lstrip(".")
    if suffix in ("jpg", "jpeg", "png", "webp", "gif"):
        dest.write_bytes(data)
        return dest.stat().st_size >= MIN_IMAGE_BYTES
    out = dest.with_suffix("." + ext)
    out.write_bytes(data)
    return out.stat().st_size >= MIN_IMAGE_BYTES


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--html",
        type=Path,
        default=_PROJECT_ROOT / "moscow" / "output" / "Moscow_Complete_Guide.html",
    )
    parser.add_argument(
        "--pdf",
        type=Path,
        default=None,
    )
    parser.add_argument(
        "--moscow-root",
        type=Path,
        default=_PROJECT_ROOT / "moscow",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
    )
    args = parser.parse_args()

    root = args.moscow_root.resolve()
    html_path = args.html.resolve()
    pdf_path = args.pdf
    if pdf_path is None:
        for name in ("Moscow_Complete_Guide.pdf", "Moscow_Complete.pdf"):
            candidate = root / "output" / name
            if candidate.is_file():
                pdf_path = candidate
                break
    if pdf_path is None or not pdf_path.is_file():
        print("Complete PDF not found.", file=sys.stderr)
        return 2
    pdf_path = pdf_path.resolve()

    if not html_path.is_file():
        print("Complete HTML not found:", html_path, file=sys.stderr)
        return 2

    import fitz

    print("Parsing Complete HTML...", flush=True)
    complete_imgs = _parse_complete_sections(html_path)
    places = _load_json_places()
    targets = [
        p for p in places
        if str(p.get("category") or "") in TARGET_CATEGORIES
        and _missing_rels(root, p)
    ]
    print("Places needing images:", len(targets), flush=True)
    print("Opening PDF index (one pass)...", flush=True)
    doc = fitz.open(str(pdf_path))
    page_text, page_images = _build_pdf_index(doc)
    doc.close()
    print("PDF pages indexed:", len(page_text), flush=True)

    stats = {
        "places_checked": 0,
        "rels_needed": 0,
        "copied_from_disk": 0,
        "extracted_pdf": 0,
        "still_missing": 0,
    }
    details: list[dict[str, str]] = []

    for place in targets:
        title_norm = _norm(str(place.get("name_ru") or ""))
        missing = _missing_rels(root, place)
        if not missing:
            continue
        stats["places_checked"] += 1
        stats["rels_needed"] += len(missing)
        html_paths = complete_imgs.get(title_norm, [])
        pdf_images = _pdf_images_for_pages(
            _pages_for_title(page_text, title_norm),
            page_images,
        )
        pdf_idx = 0

        for dest_rel in missing:
            filled = False
            for src_rel in html_paths:
                if _copy_file(root, src_rel, dest_rel):
                    stats["copied_from_disk"] += 1
                    details.append({
                        "action": "copy",
                        "place": str(place.get("name_ru") or ""),
                        "dest": dest_rel,
                        "src": src_rel,
                    })
                    filled = True
                    break
            if filled:
                continue
            if pdf_idx < len(pdf_images):
                data, ext = pdf_images[pdf_idx]
                pdf_idx += 1
                dest = root / dest_rel.replace("\\", "/")
                if args.dry_run:
                    stats["extracted_pdf"] += 1
                    filled = True
                elif _write_image(dest, data, ext, dest_rel):
                    stats["extracted_pdf"] += 1
                    details.append({
                        "action": "pdf",
                        "place": str(place.get("name_ru") or ""),
                        "dest": dest_rel,
                    })
                    filled = True
            if not filled:
                stats["still_missing"] += 1
                details.append({
                    "action": "missing",
                    "place": str(place.get("name_ru") or ""),
                    "dest": dest_rel,
                })

    report = {
        "pdf": str(pdf_path),
        "html": str(html_path),
        "stats": stats,
        "details": details,
    }
    report_path = root / "data" / "moscow_complete_image_fill.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("=== Moscow Complete image fill ===")
    for key, val in stats.items():
        print("  {}: {}".format(key, val))
    print("Report:", report_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
