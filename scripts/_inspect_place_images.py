# -*- coding: utf-8 -*-
import json
from pathlib import Path

from scripts.city_guide_core import MIN_IMAGE_BYTES

names = [
    "Гостиница «Ленинградская»",
    "Государственная Дума",
    "«Яр»",
    "Церковь Рождества Христова в Измайлове",
    "Здание МИД",
    "Дом Союзов (Колонный зал)",
    "ВДНХ",
    "Буддийский храм Тубден Шеддублинг",
    "Театр Российской армии",
    "Церковь Георгия Победоносца на Псковской горке",
    "Церковь Никиты Мученика на Швивой горке",
    "Церковь Спаса на Болвановке",
    "Москва-Сити",
]
rows = json.loads(
    Path("moscow/data/moscow_places.json").read_text(encoding="utf-8"),
)
moscow = Path("moscow")
for n in names:
    p = next(x for x in rows if x.get("name_ru") == n)
    slug = p["slug"]
    rel = p.get("image_rel_path", "")
    path = moscow / rel.replace("images/", "images/")
    ok = path.is_file() and path.stat().st_size >= MIN_IMAGE_BYTES
    print("===", n, slug, "===")
    print("primary:", rel, ok, path.stat().st_size if path.is_file() else 0)
    print("url:", (p.get("image_source_url") or "")[:80])
    for i, a in enumerate(p.get("additional_images") or []):
        ar = a.get("image_rel_path", "")
        ap = moscow / ar.replace("images/", "images/")
        aok = ap.is_file() and ap.stat().st_size >= MIN_IMAGE_BYTES
        print(f"  add{i}:", ar, aok, ap.stat().st_size if ap.is_file() else 0)
        print(f"       url:", (a.get("image_source_url") or "")[:80])
