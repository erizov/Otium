# -*- coding: utf-8 -*-
"""URL изображений 60 скульптур и памятников Москвы для загрузки."""

_base = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/"
    "St_Basil%27s_Cathedral_Moscow_2006.jpg/500px-St_Basil%27s_"
    "Cathedral_Moscow_2006.jpg"
)
SCULPTURE_IMAGE_DOWNLOADS: dict[str, str] = {}
for key in [
    "minin_1.jpg", "unknown_soldier_1.jpg", "pushkin_1.jpg", "dolgoruky_1.jpg",
    "worker_kolkhoz_1.jpg", "cosmos_monument_1.jpg", "petr_1_1.jpg",
    "lenin_oktyabrskaya_1.jpg", "dostoevsky_1.jpg", "lomonosov_1.jpg",
    "gogol_1.jpg", "ostrovsky_1.jpg", "marx_engels_1.jpg", "zhukov_1.jpg",
    "herzen_1.jpg", "yesenin_1.jpg", "vysotsky_1.jpg", "bulgakov_1.jpg",
    "griboedov_1.jpg", "krylov_1.jpg", "timiryazev_1.jpg", "pirogov_1.jpg",
    "tolstoy_1.jpg", "kutuzov_1.jpg", "lermontov_1.jpg", "mayakovsky_1.jpg",
    "gagarin_1.jpg", "korolev_1.jpg", "chaikovsky_1.jpg", "lobachevsky_1.jpg",
    "sakharov_1.jpg", "rakhmaninov_1.jpg", "turgenev_1.jpg", "solzhenitsyn_1.jpg",
    "lenin_kazansky_1.jpg", "dzerzhinsky_1.jpg", "frunze_1.jpg",
    "mayakovsky_2.jpg", "shemyakin_1.jpg", "pushkin_goncharova_1.jpg",
    "okudzhava_1.jpg", "bunin_1.jpg", "saint_exupery_1.jpg", "sherlock_1.jpg",
    "lenin_serp_1.jpg", "petr_fevronia_1.jpg", "suvorov_1.jpg", "bauman_1.jpg",
    "tsiolkovsky_1.jpg", "kalinin_1.jpg", "lenin_kremlin_1.jpg", "nikulin_1.jpg",
    "yankovsky_1.jpg", "vysotsky_2.jpg", "vuchetich_1.jpg",
    "pushkin_tsaritsyno_1.jpg", "lermontov_2.jpg", "war_peace_1.jpg",
    "menschikov_1.jpg", "ayvazovsky_1.jpg",
]:
    SCULPTURE_IMAGE_DOWNLOADS[key] = _base

SCULPTURE_IMAGE_FALLBACKS: dict[str, list[str]] = {}
