# -*- coding: utf-8 -*-
import re
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from russian_architecture.data.style_catalog import STYLE_ORDER

html = Path("russian_architecture/output/russian_architecture_guide_ru.html").read_text(
    encoding="utf-8",
)
toc_part = html.split("</nav>")[0]
toc_cats = re.findall(r'href="#(cat-[^"]+)"', toc_part)
body_cats = re.findall(r'id="(cat-[^"]+)"', html)
for s in STYLE_ORDER:
    anchor = "cat-" + s.replace("_", "-")
    if anchor not in toc_cats or anchor not in body_cats:
        print(s, "toc", anchor in toc_cats, "body", anchor in body_cats)
