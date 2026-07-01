# -*- coding: utf-8 -*-
"""Write style catalogs and seed files for DE / EN / AM architecture guides."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.architecture_module_seed_data import MODULE_STYLES

HISTORICAL_TEXTS: dict[str, tuple[str, str]] = {
    "german_architecture": (
        "От римских ворот Трира и кёльнской готики до Баухауса, "
        "бетонных послевоенных кварталов и Эльбфилармонии немецкая "
        "архитектура соединяет инженерную точность с политическими "
        "переломами эпох.\n\n"
        "Романские соборы Рейна, дворцы абсолютизма и неоклассика "
        "Шинкеля задали образ государства; югендстиль и экспрессионизм "
        "отразили модерн начала XX века. После разрушений 1945 года "
        "модернизм, брутализм и современные музеи сформировали облик "
        "объединённой Германии.\n\n"
        "Путеводитель построен по хронологическим главам; в каждой — "
        "только памятники с подтверждёнными изображениями Wikimedia Commons.",
        "From Trier's Roman gates and Cologne Gothic to the Bauhaus, "
        "post-war concrete quarters and the Elbphilharmonie, German "
        "architecture links engineering precision with the political "
        "turning points of each era.\n\n"
        "Rhenish Romanesque cathedrals, absolutist palaces and Schinkel's "
        "Neoclassicism shaped the image of the state; Jugendstil and "
        "Expressionism reflected early modernity. After 1945, modernism, "
        "Brutalism and contemporary museums formed the face of reunified "
        "Germany.\n\n"
        "This guide follows chronological chapters with landmarks backed "
        "by Wikimedia Commons images only.",
    ),
    "english_architecture": (
        "От римских бань Бата и норманнского Дарема до палладианских "
        "террас, викторианского парламента и стеклянного Шарда английская "
        "архитектура задаёт ритм Британии и её колониального наследия.\n\n"
        "Готика, тюдоровские особняки и классика Кристофера Рена сменились "
        "георгианскими квадратами и индустриальной готикой Викторианской "
        "эпохи. Модернизм, брутализм и высокотехнологичные башни XXI века "
        "продолжают лондонский диалог о публичном пространстве.\n\n"
        "Каждая глава содержит примеры с изображениями только из Commons.",
        "From Bath's Roman baths and Norman Durham to Palladian terraces, "
        "Victorian Parliament and the glass Shard, English architecture "
        "sets the rhythm of Britain and its colonial legacy.\n\n"
        "Gothic, Tudor mansions and Wren's classicism gave way to Georgian "
        "squares and Victorian industrial Gothic. Modernism, Brutalism and "
        "high-tech towers continue London's dialogue on public space.\n\n"
        "Each chapter lists examples with Wikimedia Commons images only.",
    ),
    "american_architecture": (
        "От испанских миссий и федерального Капитолия до небоскрёбов "
        "Чикагской школы, прерийных домов Райта и бетонной Бразилии — "
        "архитектура обеих Америк отражает миграцию стилей и масштаб "
        "континента.\n\n"
        "Колониальные формы, греческое возрождение и бо-ар сформировали "
        "образ молодых республик; ар-деко Манхэттена и латиноамериканский "
        "барокко показали региональные варианты. Послевоенный модернизм, "
        "брутализм и постмодерн подготовили музеи и башни XXI века от "
        "Мехико до Монреаля.\n\n"
        "В путеводитель включены только объекты с изображениями Commons.",
        "From Spanish missions and the Federal Capitol to Chicago School "
        "skyscrapers, Wright's Prairie houses and concrete Brasília, the "
        "architecture of both Americas reflects migrating styles and "
        "continental scale.\n\n"
        "Colonial forms, Greek Revival and Beaux-Arts shaped young "
        "republics; Manhattan Art Deco and Latin American Baroque showed "
        "regional variants. Post-war modernism, Brutalism and postmodern "
        "museums and towers from Mexico City to Montreal define the 21st "
        "century.\n\n"
        "Only landmarks with Wikimedia Commons images are included.",
    ),
}


def _write_style_catalog(module: str, styles: dict[str, Any]) -> None:
    lines = [
        "# -*- coding: utf-8 -*-",
        '"""Architectural styles — chronological chapters."""',
        "",
        "from __future__ import annotations",
        "",
        "from typing import Any",
        "",
        "STYLE_META: dict[str, tuple[str, str, str, str]] = {",
    ]
    order: list[str] = []
    for key, (meta, _examples) in styles.items():
        order.append(key)
        lines.append(
            '    "{key}": (\n'
            '        "{ru}",\n'
            '        "{en}",\n'
            '        "{ir}",\n'
            '        "{ie}",\n'
            "    ),".format(
                key=key,
                ru=meta[0].replace('"', '\\"'),
                en=meta[1].replace('"', '\\"'),
                ir=meta[2].replace('"', '\\"'),
                ie=meta[3].replace('"', '\\"'),
            ),
        )
    lines.append("}")
    lines.append("")
    lines.append(
        "from {}.data.style_examples_seeds import STYLE_EXAMPLES".format(module),
    )
    lines.append("")
    lines.append("STYLE_ORDER: tuple[str, ...] = (")
    for key in order:
        lines.append('    "{}",'.format(key))
    lines.append(")")
    lines.append("")
    lines.append("if set(STYLE_ORDER) != set(STYLE_META):")
    lines.append("    raise RuntimeError('STYLE_ORDER / STYLE_META mismatch')")
    lines.append("")
    path = ROOT / module / "data" / "style_catalog.py"
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_seeds(module: str, styles: dict[str, Any]) -> None:
    lines = [
        "# -*- coding: utf-8 -*-",
        '"""Curated seed examples with bilingual text."""',
        "",
        "from __future__ import annotations",
        "",
        "from typing import Any",
        "",
        "",
        "def _ex(",
        "    suffix: str,",
        "    name_ru: str,",
        "    name_en: str,",
        "    *,",
        '    year: str = "",',
        '    city_ru: str = "",',
        '    city_en: str = "",',
        '    history_ru: str = "",',
        '    history_en: str = "",',
        '    significance_ru: str = "",',
        '    significance_en: str = "",',
        '    commons_url: str = "",',
        ") -> dict[str, Any]:",
        "    return {",
        '        "suffix": suffix,',
        '        "name_ru": name_ru,',
        '        "name_en": name_en,',
        '        "year": year,',
        '        "city_ru": city_ru,',
        '        "city_en": city_en,',
        '        "history_ru": history_ru,',
        '        "history_en": history_en,',
        '        "significance_ru": significance_ru,',
        '        "significance_en": significance_en,',
        '        "commons_url": commons_url,',
        "    }",
        "",
        "",
        "STYLE_EXAMPLES: dict[str, list[dict[str, Any]]] = {",
    ]
    for key, (_meta, examples) in styles.items():
        lines.append('    "{}": ['.format(key))
        for ex in examples:
            suffix, ru, en, year, city_ru, city_en, hr, he, url = ex
            lines.append(
                "        _ex({!r}, {!r}, {!r}, year={!r}, city_ru={!r}, "
                "city_en={!r}, history_ru={!r}, history_en={!r}, "
                "commons_url={!r}),".format(
                    suffix, ru, en, year, city_ru, city_en, hr, he, url,
                ),
            )
        lines.append("    ],")
    lines.append("}")
    lines.append("")
    path = ROOT / module / "data" / "style_examples_seeds.py"
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_targets(module: str, styles: dict[str, Any]) -> None:
    keys = list(styles.keys())
    lines = [
        "# -*- coding: utf-8 -*-",
        '"""Per-style example counts for the architecture guide."""',
        "",
        "from __future__ import annotations",
        "",
        "from {}.data.style_catalog import STYLE_ORDER".format(module),
        "",
        "",
        "def style_example_target(style_key: str) -> int:",
        '    """Return how many examples a style chapter should list."""',
        "    # Commons-only guides: aim for 4, accept fewer after filtering.",
        "    return 4",
        "",
    ]
    path = ROOT / module / "data" / "style_targets.py"
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_historical(module: str) -> None:
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


def write_module_catalogs(module: str) -> None:
    styles = MODULE_STYLES[module]
    _write_style_catalog(module, styles)
    _write_seeds(module, styles)
    _write_targets(module, styles)
    _write_historical(module)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "modules",
        nargs="*",
        default=sorted(MODULE_STYLES),
    )
    args = parser.parse_args()
    for mod in args.modules:
        write_module_catalogs(mod)
        print("Wrote catalogs for", mod)


if __name__ == "__main__":
    main()
