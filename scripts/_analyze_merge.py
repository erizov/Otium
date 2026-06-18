# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path

from scripts.city_guide_core import (
    dedupe_pdf_sidecar_places,
    place_has_pdf_image,
    places_for_pdf,
)

moscow = Path("moscow")
places = json.loads(
    Path("moscow/data/moscow_places.json").read_text(encoding="utf-8"),
)
pdf_slugs = {p["slug"] for p in places_for_pdf(moscow, places, city_slug="moscow")}
html = Path("moscow/output/moscow_guide.html").read_text(encoding="utf-8")
unified = set(re.findall(r'<section class="place" id="([^"]+)"', html))
missing = json.loads(
    Path("moscow/data/moscow_pdf_missing_from_unified.json").read_text(
        encoding="utf-8",
    ),
)["missing"]
dedup_slugs = {
    p["slug"] for p in dedupe_pdf_sidecar_places(places, city_slug="moscow")
}

no_img = []
dedup_removed = []
eligible_not_in_html = []
for m in missing:
    slug = m["slug"]
    p = next(x for x in places if x["slug"] == slug)
    if not place_has_pdf_image(moscow, p):
        no_img.append(slug)
        continue
    if slug not in dedup_slugs:
        dedup_removed.append(slug)
        continue
    if slug in pdf_slugs and slug not in unified:
        eligible_not_in_html.append(slug)

print("no_img", len(no_img))
print("dedup_removed", len(dedup_removed))
print("eligible_not_in_html", len(eligible_not_in_html), eligible_not_in_html)
