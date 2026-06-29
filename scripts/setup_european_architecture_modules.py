# -*- coding: utf-8 -*-
"""Setup support files and populate city pools for European architecture guides."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent

CITY_PLACES_INDEX_TEMPLATE = '''# -*- coding: utf-8 -*-
"""Load city guide places that have local images."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

MIN_IMAGE_BYTES = 500

_CITY_ROOTS = {cities}


def _local_additional_images(
    project_root: Path,
    city: str,
    row: dict[str, Any],
) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for extra in row.get("additional_images") or []:
        if len(out) >= 1:
            break
        if not isinstance(extra, dict):
            continue
        rel = str(extra.get("image_rel_path") or "").strip()
        if not rel:
            continue
        path = project_root / city / rel
        if not path.is_file() or path.stat().st_size < MIN_IMAGE_BYTES:
            continue
        out.append({{
            "image_rel_path": rel,
            "image_source_url": str(extra.get("image_source_url") or ""),
        }})
    return out


def load_city_index(project_root: Path) -> dict[str, dict[str, Any]]:
    """Map ``city:slug`` -> place row with ``city`` and ``image_rel_path``."""
    index: dict[str, dict[str, Any]] = {{}}
    for city in _CITY_ROOTS:
        data_dir = project_root / city / "data"
        if not data_dir.is_dir():
            continue
        for path in sorted(data_dir.glob("*places*.json")):
            try:
                rows = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            if not isinstance(rows, list):
                continue
            for row in rows:
                if not isinstance(row, dict):
                    continue
                slug = str(row.get("slug") or "").strip()
                rel = str(row.get("image_rel_path") or "").strip()
                if not slug or not rel:
                    continue
                img = project_root / city / rel
                if not img.is_file() or img.stat().st_size < MIN_IMAGE_BYTES:
                    continue
                key = "{{}}:{{}}".format(city, slug)
                index[key] = {{
                    "city": city,
                    "slug": slug,
                    "name_ru": str(row.get("name_ru") or ""),
                    "name_en": str(
                        row.get("subtitle_en") or row.get("name_en") or "",
                    ),
                    "image_rel_path": rel,
                    "image_source_url": str(
                        row.get("image_source_url") or "",
                    ),
                    "history_ru": str(
                        row.get("history_ru") or row.get("history") or "",
                    ),
                    "history_en": str(
                        row.get("history_en") or row.get("history") or "",
                    ),
                    "significance_ru": str(
                        row.get("significance_ru")
                        or row.get("significance")
                        or "",
                    ),
                    "significance_en": str(
                        row.get("significance_en")
                        or row.get("significance")
                        or "",
                    ),
                    "year_built": str(row.get("year_built") or ""),
                    "architecture_style": str(
                        row.get("architecture_style") or "",
                    ),
                    "address": str(row.get("address") or ""),
                    "additional_images": _local_additional_images(
                        project_root,
                        city,
                        row,
                    ),
                }}
    return index
'''

IMAGE_REUSE_TEMPLATE = '''# -*- coding: utf-8 -*-
"""Primary + second image copy for the architecture guide."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from {pkg}.data.guide_image_policy import SINGLE_IMAGE_SLUGS

MIN_IMAGE_BYTES = 500
MAX_IMAGES_PER_PLACE = 2


def extra_image_rel(place_slug: str) -> str:
    return "images/styles/{{}}_2.jpg".format(place_slug)


def has_local_image(guide_root: Path, rel: str) -> bool:
    path = guide_root / rel
    return path.is_file() and path.stat().st_size >= MIN_IMAGE_BYTES


def copy_city_image(
    project_root: Path,
    guide_root: Path,
    city: str,
    src_rel: str,
    dest_rel: str,
) -> bool:
    src = project_root / city / src_rel
    dest = guide_root / dest_rel
    if not src.is_file() or src.stat().st_size < MIN_IMAGE_BYTES:
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.is_file() and dest.stat().st_size >= MIN_IMAGE_BYTES:
        return True
    shutil.copy2(src, dest)
    return dest.is_file() and dest.stat().st_size >= MIN_IMAGE_BYTES


def city_additional_sources(
    city_row: dict[str, Any],
    project_root: Path,
) -> list[dict[str, str]]:
    city = str(city_row.get("city") or "")
    out: list[dict[str, str]] = []
    for extra in city_row.get("additional_images") or []:
        if len(out) >= MAX_IMAGES_PER_PLACE - 1:
            break
        if not isinstance(extra, dict):
            continue
        rel = str(extra.get("image_rel_path") or "").strip()
        if not rel:
            continue
        path = project_root / city / rel
        if path.is_file() and path.stat().st_size >= MIN_IMAGE_BYTES:
            out.append({{
                "src_rel": rel,
                "image_source_url": str(
                    extra.get("image_source_url") or "",
                ),
            }})
    return out


def attach_additional_image_rows(
    row: dict[str, Any],
    city_row: dict[str, Any] | None,
    project_root: Path,
) -> None:
    if not city_row:
        return
    slug = str(row.get("slug") or "").strip()
    if not slug or slug in SINGLE_IMAGE_SLUGS:
        return
    from {pkg}.data.image_overrides import IMAGE_URL_OVERRIDES

    if slug in IMAGE_URL_OVERRIDES:
        return
    sources = city_additional_sources(city_row, project_root)
    if not sources:
        return
    src = sources[0]
    row["additional_images"] = [{{
        "image_rel_path": extra_image_rel(slug),
        "image_source_url": src["image_source_url"],
        "_src_city": str(city_row["city"]),
        "_src_rel": src["src_rel"],
    }}]


def link_additional_images(
    project_root: Path,
    guide_root: Path,
    row: dict[str, Any],
) -> int:
    slug = str(row.get("slug") or "").strip()
    if not slug:
        return 0
    linked = 0
    extras = row.get("additional_images")
    if not isinstance(extras, list):
        extras = []
    for extra in extras:
        if not isinstance(extra, dict):
            continue
        dest_rel = str(extra.get("image_rel_path") or extra_image_rel(slug))
        if has_local_image(guide_root, dest_rel):
            linked += 1
            continue
        city = str(extra.get("_src_city") or "").strip()
        src_rel = str(extra.get("_src_rel") or "").strip()
        if city and src_rel and copy_city_image(
            project_root,
            guide_root,
            city,
            src_rel,
            dest_rel,
        ):
            linked += 1
        break
    return linked


def attach_from_city_ref(
    row: dict[str, Any],
    city_index: dict[str, dict[str, Any]],
    project_root: Path,
) -> None:
    city_ref = str(row.get("_city_ref") or "").strip()
    if not city_ref:
        return
    attach_additional_image_rows(
        row,
        city_index.get(city_ref),
        project_root,
    )


def prune_missing_additional_images(
    guide_root: Path,
    row: dict[str, Any],
) -> None:
    extras = row.get("additional_images")
    if not isinstance(extras, list):
        return
    kept: list[dict[str, Any]] = []
    for extra in extras:
        if not isinstance(extra, dict):
            continue
        rel = str(extra.get("image_rel_path") or "").strip()
        if rel and has_local_image(guide_root, rel):
            kept.append(extra)
    if kept:
        row["additional_images"] = kept
    else:
        row.pop("additional_images", None)


def strip_internal_image_keys(row: dict[str, Any]) -> None:
    for extra in row.get("additional_images") or []:
        if isinstance(extra, dict):
            extra.pop("_src_city", None)
            extra.pop("_src_rel", None)
    row.pop("_city_ref", None)
    row.pop("_reuse_from", None)
'''

WHITELIST_TEMPLATE = '''# -*- coding: utf-8 -*-
"""Image source URL checks for {pkg}."""

from __future__ import annotations

from pathlib import Path

from scripts.city_guide_standard_whitelist import clear_whitelist_cache
from scripts.city_guide_standard_whitelist import url_is_whitelisted

__all__ = [
    "clear_whitelist_cache",
    "default_whitelist_path",
    "url_is_whitelisted",
]


def default_whitelist_path() -> Path:
    return Path(__file__).resolve().parent / "docs" / "SOURCES_WHITELIST.md"
'''

BANNED_IMAGES = '''# -*- coding: utf-8 -*-
"""Image URLs and local paths that must not be used in the guide."""

from __future__ import annotations

BANNED_IMAGE_URL_FRAGMENTS: tuple[str, ...] = ()
BANNED_LOCAL_IMAGE_RELS: tuple[str, ...] = ()


def url_is_banned(url: str) -> bool:
    low = str(url or "").strip().lower()
    if not low:
        return False
    return any(frag.lower() in low for frag in BANNED_IMAGE_URL_FRAGMENTS)


def local_rel_is_banned(rel: str) -> bool:
    norm = str(rel or "").replace("\\\\", "/").strip().lower()
    if not norm:
        return False
    return any(b.lower() in norm for b in BANNED_LOCAL_IMAGE_RELS)
'''

# (style_key, keywords) — matched against architecture_style + name + slug
ITALIAN_KEYWORDS: dict[str, tuple[str, ...]] = {
    "etruscan_roman": (
        "roman", "ancient", "colosseum", "pantheon", "forum", "hadrian",
        "mausoleum", "baths", "amphitheatre", "amphitheater", "etruscan",
    ),
    "early_christian": (
        "early christian", "byzantine", "basilica", "ravenna", "mosaic",
    ),
    "romanesque": ("romanesque", "medieval basilica"),
    "norman_sicilian": ("sicily", "norman", "palermo", "cefalu", "monreale"),
    "gothic": ("gothic", "duomo", "cathedral"),
    "early_renaissance": (
        "early renaissance", "renaissance", "medici", "brunelleschi",
    ),
    "high_renaissance": (
        "high renaissance", "bramante", "st peter", "vatican",
    ),
    "mannerism": ("mannerist", "mannerism", "giulio romano"),
    "palladian_venetian": (
        "palladian", "palladio", "venetian", "doge", "rialto",
    ),
    "baroque": ("baroque", "borromini", "bernini", "jesuit"),
    "sicilian_baroque": ("sicilian baroque", "noto", "catania baroque"),
    "rococo_late_baroque": ("rococo", "late baroque", "turin"),
    "neoclassicism": ("neoclassic", "neo-classic", "canova"),
    "romantic_eclectic": ("eclectic", "historicist", "romantic"),
    "liberty": ("liberty", "art nouveau", "stile liberty", "galleria"),
    "rationalism": ("rationalist", "rationalism", "piacentini"),
    "fascist_rationalism": ("eur", "fascist", "mussolini", "razionalismo"),
    "postwar_modern": ("post-war", "postwar", "neorealism", "velasca"),
    "brutalism": ("brutalist", "brutalism", "concrete"),
    "postmodern_tendenza": ("postmodern", "tendenza", "graves"),
    "contemporary": (
        "contemporary", "modern", "21st", "zaha", "piano", "maxxi",
    ),
}

FRENCH_KEYWORDS: dict[str, tuple[str, ...]] = {
    "gallo_roman": ("gallo-roman", "roman", "nimes", "arles", "lyon roman"),
    "romanesque": ("romanesque", "cluny", "vezelay"),
    "early_gothic": ("early gothic", "notre-dame", "saint-denis", "gothic"),
    "rayonnant_flamboyant": (
        "rayonnant", "flamboyant", "sainte-chapelle",
    ),
    "french_renaissance": ("renaissance", "chambord", "loire", "valois"),
    "classical_louis_xiii": ("louis xiii", "classical", "mansart"),
    "louis_xiv_classicism": (
        "louis xiv", "versailles", "le vau", "hardouin",
    ),
    "regency_rococo": ("regency", "régence", "rococo"),
    "louis_xv_rococo": ("louis xv", "rococo", "hôtel particulier"),
    "louis_xvi_neoclassical": ("louis xvi", "neoclassic", "concorde"),
    "revolution_empire": ("empire", "triumphal", "arc de triomphe"),
    "restoration_july_monarchy": ("restoration", "july monarchy", "1830"),
    "second_empire": ("second empire", "napoleon iii", "opera garnier"),
    "haussmann": ("haussmann", "boulevard", "opera"),
    "belle_epoque": ("belle époque", "belle epoque", "grand palais"),
    "art_nouveau": ("art nouveau", "guimard", "metro"),
    "art_deco_interwar": ("art deco", "palais de tokyo", "interwar"),
    "modernism_lecorbusier": (
        "le corbusier", "corbusier", "savoye", "modernist",
    ),
    "brutalism": ("brutalist", "brutalism"),
    "grands_projets": (
        "pompidou", "grands projets", "postmodern", "mitterrand",
    ),
    "contemporary": ("contemporary", "pyramid", "louvre", "21st"),
}

SPANISH_KEYWORDS: dict[str, tuple[str, ...]] = {
    "roman_hispania": ("roman", "segovia", "merida", "tarragona"),
    "visigothic": ("visigoth", "san juan de baños"),
    "islamic_iberia": (
        "islamic", "moorish", "al-andalus", "mezquita", "alhambra",
        "cordoba", "granada",
    ),
    "mudejar": ("mudejar", "mudéjar", "toledo mudejar"),
    "romanesque": ("romanesque", "santiago", "jacques"),
    "catalan_gothic": ("catalan gothic", "barcelona gothic", "santa maria"),
    "isabelline_gothic": ("isabelline", "san juan de los reyes"),
    "manuelin": ("manuelin", "manueline", "belém", "belem", "jerónimos"),
    "plateresque": ("plateresque", "plateresco"),
    "herrerian": ("herrerian", "escorial", "herrera"),
    "spanish_baroque": ("spanish baroque", "solomonic", "granada baroque"),
    "churrigueresque": ("churrigueresque", "salamanca"),
    "portuguese_baroque": (
        "portuguese baroque", "bom jesus", "mafra", "lisbon baroque",
    ),
    "neoclassicism": ("neoclassic", "prado", "puerta de alcalá"),
    "eclectic_historicism": ("eclectic", "historicist", "19th"),
    "catalan_modernisme": (
        "modernisme", "gaudi", "gaudí", "sagrada", "modernista",
    ),
    "portuguese_art_nouveau": (
        "arte nova", "art nouveau portugal", "porto art nouveau",
    ),
    "rationalist_interwar": ("rationalist", "gcp", "interwar"),
    "franco_estado_novo": ("franco", "estado novo", "valle de los caidos"),
    "postwar_modern": ("post-war", "postwar", "torres blancas"),
    "contemporary": (
        "contemporary", "guggenheim", "maat", "calatrava", "21st",
    ),
}

MODULE_KEYWORDS: dict[str, dict[str, tuple[str, ...]]] = {
    "italian_architecture": ITALIAN_KEYWORDS,
    "french_architecture": FRENCH_KEYWORDS,
    "spanish_architecture": SPANISH_KEYWORDS,
}

MODULE_CITIES: dict[str, tuple[str, ...]] = {
    "italian_architecture": ("rome", "florence", "venice"),
    "french_architecture": ("paris",),
    "spanish_architecture": ("madrid", "barcelona", "lisbon"),
}


def _score_style(text: str, keywords: tuple[str, ...]) -> int:
    low = text.lower()
    return sum(1 for kw in keywords if kw in low)


def _load_city_places(
    project_root: Path,
    cities: tuple[str, ...],
) -> list[tuple[str, str, dict[str, Any]]]:
    out: list[tuple[str, str, dict[str, Any]]] = []
    for city in cities:
        data_dir = project_root / city / "data"
        if not data_dir.is_dir():
            continue
        for path in sorted(data_dir.glob("*places*.json")):
            try:
                rows = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            if not isinstance(rows, list):
                continue
            for row in rows:
                if not isinstance(row, dict):
                    continue
                slug = str(row.get("slug") or "").strip()
                rel = str(row.get("image_rel_path") or "").strip()
                if not slug or not rel:
                    continue
                img = project_root / city / rel
                if not img.is_file() or img.stat().st_size < 500:
                    continue
                out.append((city, slug, row))
    return out


def _best_style(
    row: dict[str, Any],
    keywords_map: dict[str, tuple[str, ...]],
) -> str | None:
    blob = " ".join(
        str(row.get(k) or "")
        for k in (
            "architecture_style",
            "name_ru",
            "subtitle_en",
            "name_en",
            "slug",
            "description",
            "history",
        )
    )
    best_key = None
    best_score = 0
    for key, kws in keywords_map.items():
        if not kws:
            continue
        score = _score_style(blob, kws)
        if score > best_score:
            best_score = score
            best_key = key
    return best_key if best_score > 0 else None


def populate_pools(module: str) -> dict[str, list[tuple[str, str]]]:
    cities = MODULE_CITIES[module]
    kws = MODULE_KEYWORDS[module]
    pool: dict[str, list[tuple[str, str]]] = {
        k: [] for k in kws
    }
    seen: set[tuple[str, str]] = set()
    for city, slug, row in _load_city_places(ROOT, cities):
        style = _best_style(row, kws)
        if not style:
            continue
        entry = (city, slug)
        if entry in seen:
            continue
        seen.add(entry)
        pool[style].append(entry)
    return pool


def write_city_style_pool(module: str, pool: dict[str, list]) -> None:
    path = ROOT / module / "data" / "city_style_pool.py"
    lines = [
        "# -*- coding: utf-8 -*-",
        '"""Map style chapters to city-guide place slugs."""',
        "",
        "from __future__ import annotations",
        "",
        "CITY_STYLE_POOL: dict[str, list[tuple[str, str]]] = {",
    ]
    for key, entries in pool.items():
        if entries:
            inner = ", ".join(
                '("{c}", "{s}")'.format(c=c, s=s) for c, s in entries
            )
            lines.append('    "{}": [{}],'.format(key, inner))
        else:
            lines.append('    "{}": [],'.format(key))
    lines.append("}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_support_files(module: str, cities: tuple[str, ...]) -> None:
    pkg = module
    data = ROOT / module / "data"
    (data / "city_places_index.py").write_text(
        CITY_PLACES_INDEX_TEMPLATE.format(cities=repr(cities)),
        encoding="utf-8",
    )
    (data / "image_reuse.py").write_text(
        IMAGE_REUSE_TEMPLATE.format(pkg=pkg),
        encoding="utf-8",
    )
    (ROOT / module / "whitelist.py").write_text(
        WHITELIST_TEMPLATE.format(pkg=pkg),
        encoding="utf-8",
    )
    (data / "banned_images.py").write_text(BANNED_IMAGES, encoding="utf-8")


HISTORICAL_TEXTS: dict[str, tuple[str, str]] = {
    "italian_architecture": (
        "От античных форумов Рима и мозаик Равенны до стеклянных башен "
        "Милана и Рима XXI века итальянская архитектура задаёт европейские "
        "ориентиры на каждом витке истории.\n\n"
        "Римская Империя оставила арки, амфитеатры и инженерию бетона; "
        "раннехристианские базилики и византийские мотивы подготовили "
        "средневековье. Романские аббатства и итальянская готика с её "
        "полихромным мрамором сменились Возрождением Флоренции и Рима — "
        "от Брунеллески до Браманте и Микеланджело.\n\n"
        "Барокко Бернини и Борромини, сицилийское барокко после 1693 года "
        "и неоклассика эпохи Наполеона сформировали облик городов. "
        "Стили Либерти, рационализм и архитектура фашистской эпохи "
        "отразили модерн и политику XX века; послевоенный модернизм, "
        "брутализм и постмодернизм Tendenza подготовили современную сцену "
        "музеев и городских вмешательств.\n\n"
        "Путеводитель выстроен по хронологическим главам: в каждой — "
        "знаковые памятники с кратким контекстом и именами мастеров.",
        "From Rome's ancient forums and Ravenna's mosaics to Milan's and "
        "Rome's glass towers of the 21st century, Italian architecture has "
        "set European benchmarks at every turn of history.\n\n"
        "The Roman Empire left arches, amphitheatres and concrete "
        "engineering; early Christian basilicas and Byzantine motifs "
        "prepared the Middle Ages. Romanesque abbeys and Italian Gothic "
        "with its polychrome marble gave way to the Renaissance of "
        "Florence and Rome—from Brunelleschi to Bramante and Michelangelo.\n\n"
        "The Baroque of Bernini and Borromini, Sicilian Baroque after "
        "1693 and Napoleonic Neoclassicism shaped cities. Stile Liberty, "
        "Rationalism and Fascist-era architecture reflected modernity and "
        "politics; post-war modernism, Brutalism and Tendenza postmodernism "
        "prepared today's museums and urban interventions.\n\n"
        "This guide follows chronological chapters; each lists landmark "
        "monuments with brief context and architect names.",
    ),
    "french_architecture": (
        "От галло-римских театров и романских аббатств до пирамид Лувра "
        "и небоскрёбов Дефанса французская архитектура соединяет "
        "государственный идеал с изобретательностью формы.\n\n"
        "Готика Иль-де-Франс, замки Луары и классицизм Людовика XIV "
        "создали язык абсолютной монархии; рококо и неоклассика "
        "подготовили революцию и ампир. Османизация Парижа, Вторая "
        "империя и Прекрасная эпоха задали ритм бульваров и парадных "
        "фасадов.\n\n"
        "Ар-нуво Гимара, ар-деко и модернизм Ле Корбюсье изменили "
        "жилую ячейку и образ города. Великие проекты 1980-х и "
        "современные культурные центры вписывают Францию в глобальный "
        "диалог об устойчивости и публичном пространстве.\n\n"
        "Каждая глава путеводителя посвящена одному стилю и содержит "
        "типовые примеры с историческим комментарием.",
        "From Gallo-Roman theatres and Romanesque abbeys to the Louvre "
        "Pyramid and La Défense towers, French architecture links state "
        "ideals with formal invention.\n\n"
        "Île-de-France Gothic, Loire châteaux and Louis XIV classicism "
        "created the language of absolute monarchy; Rococo and "
        "Neoclassicism led to Revolution and Empire. Haussmann's Paris, "
        "the Second Empire and the Belle Époque set the rhythm of "
        "boulevards and ceremonial façades.\n\n"
        "Guimard's Art Nouveau, Art Deco and Le Corbusier's modernism "
        "changed the dwelling unit and the image of the city. Grands "
        "Projets of the 1980s and contemporary cultural centres place "
        "France in the global dialogue on sustainability and public "
        "space.\n\n"
        "Each chapter covers one style with representative examples "
        "and historical commentary.",
    ),
    "spanish_architecture": (
        "Иберийская архитектура — синтез римского наследия, исламского "
        "Аль-Андалуса, христианских королевств и португальской "
        "морской империи, от Сеговии до Лиссабона.\n\n"
        "Римская Испания и вестготские храмы сменились мечетями Кордовы "
        "и дворцами Альгамбры; мудéjar соединил исламский орнамент с "
        "христианскими объёмами. Каталонская и изабеллинская готика, "
        "мануэлино и платереско отразили эпоху открытий; эскориальский "
        "стиль Эрреры и чурригереско задали барочный пыл Испании.\n\n"
        "Каталонский модернизм Гауди и португальское ар-нуво, "
        "рационализм межвоенного периода и монументализм диктатур "
        "XX века подготовили послевоенную модернизацию и современные "
        "музеи вроде Гуггенхайма в Бильбао.\n\n"
        "Путеводитель охватывает Испанию и Португалию по хронологическим "
        "главам с примерами зданий и краткими справками.",
        "Iberian architecture blends Roman heritage, Islamic Al-Andalus, "
        "Christian kingdoms and Portugal's maritime empire—from Segovia "
        "to Lisbon.\n\n"
        "Roman Hispania and Visigothic churches gave way to Córdoba's "
        "mosques and the Alhambra; Mudéjar joined Islamic ornament with "
        "Christian volumes. Catalan and Isabelline Gothic, Manueline and "
        "Plateresque reflected the Age of Discovery; Herrera's Escorial "
        "and Churrigueresque set Spain's Baroque fervour.\n\n"
        "Gaudí's Catalan Modernisme and Portuguese Art Nouveau, interwar "
        "Rationalism and dictatorship monumentalism prepared post-war "
        "modernization and contemporary museums such as the Guggenheim "
        "Bilbao.\n\n"
        "This guide covers Spain and Portugal in chronological chapters "
        "with building examples and brief notes.",
    ),
}


def write_historical_texts(module: str) -> None:
    ru, en = HISTORICAL_TEXTS[module]
    data = ROOT / module / "data"
    (data / "{}_historical_reference_ru.txt".format(module)).write_text(
        ru + "\n",
        encoding="utf-8",
    )
    (data / "{}_historical_reference_en.txt".format(module)).write_text(
        en + "\n",
        encoding="utf-8",
    )


def main() -> None:
    for module, cities in MODULE_CITIES.items():
        write_support_files(module, cities)
        pool = populate_pools(module)
        write_city_style_pool(module, pool)
        write_historical_texts(module)
        total = sum(len(v) for v in pool.values())
        print("{}: {} pool entries".format(module, total))


if __name__ == "__main__":
    main()
