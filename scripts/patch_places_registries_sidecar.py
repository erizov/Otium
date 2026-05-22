# -*- coding: utf-8 -*-
"""Inject PDF expand sidecar merge into places_registry.py loaders."""

from __future__ import annotations

from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_MARKER = "load_pdf_expand_rows"
_INSERT_TMPL = (
    "    raw.extend(load_pdf_expand_rows(Path(__file__).parent, \"{slug}\"))\n"
)
_IMPORT_LINES = (
    "from scripts.city_guide_registry_common import load_pdf_expand_rows\n"
)


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if _MARKER in text:
        return False
    slug = path.parent.parent.name
    needle = '    raw: list[dict] = json.loads(path.read_text(encoding="utf-8"))\n'
    if needle not in text:
        return False
    text = text.replace(
        needle,
        needle + _INSERT_TMPL.format(slug=slug),
        1,
    )
    if _IMPORT_LINES.strip() not in text:
        anchor = "from typing import"
        if anchor in text:
            text = text.replace(anchor, _IMPORT_LINES + anchor, 1)
        else:
            text = _IMPORT_LINES + text
    path.write_text(text, encoding="utf-8")
    return True


def main() -> int:
    changed = 0
    for path in sorted(_ROOT.glob("*/data/places_registry.py")):
        if patch_file(path):
            changed += 1
            print("patched", path.relative_to(_ROOT))
    print("Patched {} registry file(s).".format(changed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
