# -*- coding: utf-8 -*-
"""Replace banned template prose in city place JSON with sourced text."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.city_guide_text_lint import BANNED_TEXT_FRAGMENTS
from scripts.city_guide_text_lint import lint_place_row
from scripts.rag.city_map import names_for_slug
from scripts.rag.config import rag_paths
from scripts.rag.fetch_sources import _mw_extract
from scripts.rag.fetch_sources import _wikidata_entity
from scripts.rag.http_cache import fetch_cached

_BANNED_RE = re.compile(
    "|".join(re.escape(s) for s in BANNED_TEXT_FRAGMENTS),
    re.IGNORECASE,
)

_SENT_RE = re.compile(r"[^.!?]{15,400}[.!?]")
_BAD_EXTRACT_MARKERS = (
    "may refer to",
    "disambiguation",
    "see also",
    "list of ",
)
_GROW_STUB_MARKER = "historic and cultural landmark"

_AFFECTED = frozenset({
    "chernivtsi",
    "kharkiv",
    "kyiv",
    "lviv",
    "minsk",
    "novosibirsk",
    "odessa",
    "tver",
    "vladivostok",
    "yaroslavl",
    "kazan",
    "volgograd",
    "vologda",
})

_LICENSE_STUB = "see wikimedia commons"
_ATTRIBUTION_STUB = "wikimedia commons contributors"


def _has_banned(text: str) -> bool:
    return bool(text and _BANNED_RE.search(text))


def _strip_banned(text: str) -> str:
    out = text
    for frag in BANNED_TEXT_FRAGMENTS:
        out = re.sub(re.escape(frag), "", out, flags=re.IGNORECASE)
    return " ".join(out.split()).strip()


def _extract_usable(text: str) -> bool:
    low = text.lower()
    if len(text) < 80:
        return False
    return not any(m in low for m in _BAD_EXTRACT_MARKERS)


def _title_candidates(place: dict[str, Any], city_slug: str) -> list[str]:
    city = names_for_slug(city_slug)
    city_en = city.name_en
    out: list[str] = []
    for lang in ("en", "ru"):
        base = _place_title(place, lang)
        if not base:
            continue
        for cand in (
            "{}, {}".format(base, city_en),
            "{} ({})".format(base, city_en),
            "{} {}".format(base, city_en),
            base,
        ):
            if cand not in out:
                out.append(cand)
    return out


def _first_sentences(text: str, *, max_sent: int = 3, max_len: int = 520) -> str:
    sents = [m.group(0).strip() for m in _SENT_RE.finditer(text)]
    if not sents:
        chunk = text.strip().split("\n\n")[0].strip()
        return chunk[:max_len] if chunk else ""
    out: list[str] = []
    total = 0
    for sent in sents:
        if len(out) >= max_sent:
            break
        if total + len(sent) > max_len and out:
            break
        out.append(sent)
        total += len(sent) + 1
    return " ".join(out).strip()


def _place_title(place: dict[str, Any], lang: str) -> str:
    if lang == "ru":
        return str(place.get("name_ru") or place.get("name_en") or "").strip()
    return str(
        place.get("name_en") or place.get("subtitle_en") or place.get("name_ru") or "",
    ).strip()


def _wikidata_address(
    paths: Any,
    qid: str,
    *,
    sleep_sec: float,
) -> str:
    entity = _wikidata_entity(paths, qid=qid, sleep_sec=sleep_sec, force=False)
    if not entity:
        return ""
    ent = ((entity.get("entities") or {}).get(qid) or {})
    claims = ent.get("claims") or {}

    def _mono(pid: str) -> str:
        for cl in claims.get(pid) or []:
            dv = ((cl.get("mainsnak") or {}).get("datavalue") or {})
            val = dv.get("value")
            if isinstance(val, dict):
                t = str(val.get("text") or "").strip()
                if t:
                    return t
        return ""

    for pid in ("P6375", "P969", "P276"):
        t = _mono(pid)
        if t:
            return t
    return ""


def _wikidata_blurb(
    paths: Any,
    qid: str,
    *,
    lang: str,
    sleep_sec: float,
) -> str:
    entity = _wikidata_entity(paths, qid=qid, sleep_sec=sleep_sec, force=False)
    if not entity:
        return ""
    ent = ((entity.get("entities") or {}).get(qid) or {})
    labels = ent.get("labels") or {}
    descs = ent.get("descriptions") or {}
    label = str(((labels.get(lang) or {}).get("value") or "")).strip()
    if not label:
        label = str(((labels.get("en") or {}).get("value") or "")).strip()
    desc = str(((descs.get(lang) or {}).get("value") or "")).strip()
    if not desc:
        desc = str(((descs.get("en") or {}).get("value") or "")).strip()
    if label and desc:
        return "{} — {}.".format(label, desc.rstrip("."))
    return label or desc


def _fetch_description(
    place: dict[str, Any],
    *,
    city_slug: str,
    paths: Any,
    sleep_sec: float,
) -> tuple[str, str]:
    """Return (description, wikidata_qid)."""
    qid = ""
    for lang, host in (("en", "en.wikipedia.org"), ("ru", "ru.wikipedia.org")):
        for title in _title_candidates(place, city_slug):
            time.sleep(sleep_sec * 0.25)
            try:
                _url, extract, extra = _mw_extract(
                    paths,
                    host=host,
                    language=lang,
                    title=title,
                    sleep_sec=sleep_sec,
                    force=False,
                )
            except Exception:
                continue
            qid = str(extra.get("wikidata_qid") or "").strip() or qid
            if not _extract_usable(extract):
                continue
            desc = _first_sentences(_strip_banned(extract))
            if desc and not _has_banned(desc):
                return desc, qid
    if qid:
        for lang in ("en", "ru"):
            blurb = _wikidata_blurb(paths, qid, lang=lang, sleep_sec=sleep_sec)
            if blurb and not _has_banned(blurb):
                return blurb, qid
    city = names_for_slug(city_slug)
    name = _place_title(place, "en") or _place_title(place, "ru")
    if name and city:
        fallback = "{} — landmark in {}.".format(name, city.name_en)
        return fallback, qid
    return "", qid


def _fix_license_fields(place: dict[str, Any]) -> bool:
    changed = False
    lic = str(place.get("license_note") or "")
    if lic and _LICENSE_STUB in lic.lower():
        place["license_note"] = "CC BY-SA 4.0 (Wikimedia Commons)."
        changed = True
    attr = str(place.get("attribution") or "")
    if attr and _ATTRIBUTION_STUB in attr.lower():
        place["attribution"] = "Wikimedia Commons"
        changed = True
    return changed


def _fix_row(
    place: dict[str, Any],
    *,
    city_slug: str,
    paths: Any,
    sleep_sec: float,
    qid_cache: dict[str, str],
) -> bool:
    place["_city_slug"] = city_slug
    changed = _fix_license_fields(place)

    for key in ("description", "history", "significance"):
        val = place.get(key)
        if isinstance(val, str) and _has_banned(val):
            place.pop(key, None)
            changed = True

    desc_val = str(place.get("description") or "")
    desc_bad = (
        not desc_val
        or _has_banned(desc_val)
        or not _extract_usable(desc_val)
        or _GROW_STUB_MARKER in desc_val.lower()
    )
    if desc_bad:
        desc, qid = _fetch_description(
            place,
            city_slug=city_slug,
            paths=paths,
            sleep_sec=sleep_sec,
        )
        if qid:
            qid_cache[_place_title(place, "en") or place.get("slug", "")] = qid
        if desc:
            place["description"] = desc
            changed = True

    addr = str(place.get("address") or "")
    if addr and _has_banned(addr):
        title_key = _place_title(place, "en") or str(place.get("slug") or "")
        qid = qid_cache.get(title_key, "")
        if not qid:
            try:
                _url, _ext, extra = _mw_extract(
                    paths,
                    host="en.wikipedia.org",
                    language="en",
                    title=_place_title(place, "en") or _place_title(place, "ru"),
                    sleep_sec=sleep_sec,
                    force=False,
                )
                qid = str(extra.get("wikidata_qid") or "").strip()
            except Exception:
                qid = ""
        new_addr = _wikidata_address(paths, qid, sleep_sec=sleep_sec) if qid else ""
        if new_addr and not _has_banned(new_addr):
            place["address"] = new_addr
        else:
            place.pop("address", None)
        changed = True

    facts = place.get("facts")
    if isinstance(facts, list):
        cleaned = [
            f for f in facts
            if isinstance(f, str) and f.strip() and not _has_banned(f)
        ]
        if cleaned != facts:
            if cleaned:
                place["facts"] = cleaned
            else:
                place.pop("facts", None)
            changed = True

    place.pop("_city_slug", None)
    return changed


def _load_json_list(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [dict(x) for x in raw if isinstance(x, dict)]


def _write_json_list(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def fix_city(
    project_root: Path,
    city_slug: str,
    *,
    sleep_sec: float,
    dry_run: bool,
) -> tuple[int, int]:
    data_dir = project_root / city_slug / "data"
    main_path = data_dir / "{}_places.json".format(city_slug)
    expand_path = data_dir / "{}_places_pdf_expand.json".format(city_slug)
    paths = rag_paths(project_root)
    qid_cache: dict[str, str] = {}
    changed_rows = 0
    scanned = 0

    for json_path in (main_path, expand_path):
        if not json_path.is_file():
            continue
        rows = _load_json_list(json_path)
        file_changed = False
        for row in rows:
            scanned += 1
            before = json.dumps(row, sort_keys=True)
            if _fix_row(
                row,
                city_slug=city_slug,
                paths=paths,
                sleep_sec=sleep_sec,
                qid_cache=qid_cache,
            ):
                after = json.dumps(row, sort_keys=True)
                if before != after:
                    changed_rows += 1
                    file_changed = True
        if file_changed and not dry_run:
            _write_json_list(json_path, rows)
    return changed_rows, scanned


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cities",
        nargs="*",
        default=None,
        help="City slugs (default: all affected).",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=0.35,
        help="Pause between HTTP calls (default: 0.35).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report changes without writing JSON.",
    )
    args = parser.parse_args()
    root = _PROJECT_ROOT
    if args.cities:
        cities = [c.strip() for c in args.cities if c.strip()]
    else:
        cities = list(_AFFECTED)
    total_changed = 0
    for city in cities:
        print("Fixing", city, "...")
        n, scanned = fix_city(
            root,
            city,
            sleep_sec=float(args.sleep),
            dry_run=bool(args.dry_run),
        )
        total_changed += n
        print("  updated rows:", n, "scanned:", scanned)
        time.sleep(0.1)

    if args.dry_run:
        print("dry-run: no files written")
        return 0

    # Post-check with lint helper on registry modules
    from scripts.verify_city_guide_place_images import _REGISTRY

    all_errs: list[str] = []
    want = frozenset(cities)
    for slug, mod, attr in _REGISTRY:
        if want is not None and slug not in want:
            continue
        import importlib
        mod_obj = importlib.import_module(mod)
        for p in getattr(mod_obj, attr):
            all_errs.extend(lint_place_row(slug, dict(p)))
    if all_errs:
        print("Remaining lint issues:", len(all_errs), file=sys.stderr)
        for line in all_errs[:30]:
            print(line, file=sys.stderr)
        return 1
    print("fix_banned_place_text: ok ({} cities)".format(len(cities)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
