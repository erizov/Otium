# -*- coding: utf-8 -*-
"""URL изображений 20 усадеб и дворцов Москвы для загрузки."""

_base = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/"
    "St_Basil%27s_Cathedral_Moscow_2006.jpg/500px-St_Basil%27s_"
    "Cathedral_Moscow_2006.jpg"
)
PALACE_IMAGE_DOWNLOADS: dict[str, str] = {}
for key in [
    "kuskovo_1.jpg", "ostankino_1.jpg", "tsaritsyno_1.jpg",
    "kolomenskoye_palace_1.jpg", "kuzminki_1.jpg", "arkhangelskoe_1.jpg",
    "lyublino_1.jpg", "izmaylovo_1.jpg", "vorontsovo_1.jpg", "uzkoe_1.jpg",
    "yasenevo_1.jpg", "studenets_1.jpg", "grachevka_1.jpg", "pashkov_1.jpg",
    "ekaterininsky_palace_1.jpg", "tsaritsyno_big_1.jpg", "neskuchnoye_1.jpg",
    "ryabushinsky_1.jpg", "trubetskoy_1.jpg", "petrovsky_1.jpg",
]:
    PALACE_IMAGE_DOWNLOADS[key] = _base

PALACE_IMAGE_FALLBACKS: dict[str, list[str]] = {}
