# -*- coding: utf-8 -*-
"""Copy french_architecture scaffold into a new national guide module."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = "french_architecture"

_MODULE_CONST: dict[str, str] = {
    "german_architecture": "GERMAN",
    "english_architecture": "ENGLISH",
    "american_architecture": "AMERICAN",
}

_MODULE_TITLE: dict[str, tuple[str, str]] = {
    "german_architecture": ("Немецкая архитектура", "German Architecture"),
    "english_architecture": ("Английская архитектура", "English Architecture"),
    "american_architecture": (
        "Американская архитектура (обе Америки)",
        "American Architecture (Both Continents)",
    ),
}

_SKIP_COPY = frozenset({
    "data/french_architecture_places.json",
    "data/city_style_pool.py",
    "data/city_places_index.py",
    "data/image_reuse.py",
    "data/style_catalog.py",
    "data/style_examples_seeds.py",
    "data/style_targets.py",
    "data/french_architecture_historical_reference_en.txt",
    "data/french_architecture_historical_reference_ru.txt",
    "output/french_architecture_guide.html",
    "output/french_architecture_guide_en.html",
    "output/french_architecture_guide_ru.html",
})


def _patch_text(module: str, text: str) -> str:
    const = _MODULE_CONST[module]
    out = text.replace("french_architecture", module)
    out = out.replace("FRENCH_ARCHITECTURE_PLACES", "{}_ARCHITECTURE_PLACES".format(const))
    return out


def bootstrap(module: str) -> Path:
    if module not in _MODULE_CONST:
        raise KeyError("Unknown module {!r}".format(module))
    src_root = ROOT / TEMPLATE
    dst_root = ROOT / module
    if not src_root.is_dir():
        raise FileNotFoundError(src_root)

    for path in src_root.rglob("*"):
        rel = path.relative_to(src_root).as_posix()
        if rel in _SKIP_COPY:
            continue
        if path.is_dir():
            continue
        if rel.startswith("images/styles/") and path.suffix == ".jpg":
            continue
        dst = dst_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix in {".py", ".md", ".txt"}:
            dst.write_text(
                _patch_text(module, path.read_text(encoding="utf-8")),
                encoding="utf-8",
            )
        else:
            shutil.copy2(path, dst)

    data = dst_root / "data"
    (data / "{}_places.json".format(module)).write_text("[]\n", encoding="utf-8")

    reg = data / "places_registry.py"
    reg.write_text(
        '''# -*- coding: utf-8 -*-
"""Architecture guide place registry."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict, cast

from scripts.city_guide_registry_common import load_pdf_expand_rows


class CityPlace(TypedDict, total=False):
    slug: str
    category: str
    name_ru: str
    subtitle_en: str
    image_rel_path: str
    image_source_url: str
    additional_images: list[dict[str, str]]
    description: str
    history: str
    significance: str
    facts: list[str]


def _load_places() -> list[CityPlace]:
    path = Path(__file__).with_name("{module}_places.json")
    data_dir = Path(__file__).parent
    raw: list[dict] = json.loads(path.read_text(encoding="utf-8"))
    raw.extend(load_pdf_expand_rows(data_dir, "{module}"))
    return cast(list[CityPlace], raw)


{const}_ARCHITECTURE_PLACES: list[CityPlace] = _load_places()
'''.format(module=module, const=_MODULE_CONST[module]),
        encoding="utf-8",
    )

    title_ru, title_en = _MODULE_TITLE[module]
    readme = dst_root / "README.md"
    readme.write_text(
        "# {}\n\n"
        "Chronological architecture guide. Pipeline:\n\n"
        "```bash\n"
        "python scripts/generate_architecture_guide.py --module {module}\n"
        "python scripts/resolve_architecture_guide_images.py "
        "--module {module} --commons-only\n"
        "python scripts/filter_architecture_guide_commons_only.py "
        "--module {module}\n"
        "python scripts/build_architecture_guide_pdf.py "
        "--module {module} --lang ru en\n"
        "```\n".format(title_en, module=module),
        encoding="utf-8",
    )

    wl = dst_root / "docs" / "SOURCES_WHITELIST.md"
    wl.write_text(
        "# Allowed sources — {}\n\n"
        "## Images (Commons only)\n\n"
        "- https://upload.wikimedia.org/\n"
        "- https://commons.wikimedia.org/\n\n"
        "## Facts\n\n"
        "- https://www.wikidata.org/\n"
        "- https://en.wikipedia.org/\n"
        "- https://ru.wikipedia.org/\n".format(title_en),
        encoding="utf-8",
    )

    (dst_root / "images" / "styles").mkdir(parents=True, exist_ok=True)
    (dst_root / "output").mkdir(parents=True, exist_ok=True)
    return dst_root


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("modules", nargs="+", choices=sorted(_MODULE_CONST))
    args = parser.parse_args()
    for mod in args.modules:
        print("Bootstrapped", bootstrap(mod))


if __name__ == "__main__":
    main()
