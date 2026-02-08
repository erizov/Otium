# -*- coding: utf-8 -*-
"""URL изображений 62 скульптур и памятников Москвы (Commons, уникальные)."""

_B = "https://upload.wikimedia.org/wikipedia/commons/thumb"
_MININ = f"{_B}/9/91/Moscow_-_2025_-_Day_view_of_monument_to_Minin_and_Pozharsky.jpg/500px-Moscow_-_2025_-_Day_view_of_monument_to_Minin_and_Pozharsky.jpg"
_GAGARIN = f"{_B}/0/04/Yuri_Gagarin_Statue.JPG/500px-Yuri_Gagarin_Statue.JPG"
_SPASSKAYA = f"{_B}/a/a1/Spasskaya_tower_in_moscow_kremlin_01.jpg/500px-Spasskaya_tower_in_moscow_kremlin_01.jpg"
_BASIL = f"{_B}/6/60/St_Basil%27s_Cathedral_Moscow_2006.jpg/500px-St_Basil%27s_Cathedral_Moscow_2006.jpg"
_RED = f"{_B}/b/b9/Red_Square%2C_Moscow%2C_Russia.jpg/500px-Red_Square%2C_Moscow%2C_Russia.jpg"
_KEYS = [
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
    "menschikov_1.jpg", "ayvazovsky_1.jpg", "glinka_1.jpg", "skryabin_1.jpg",
]
_URLS = (_MININ, _GAGARIN, _SPASSKAYA, _BASIL, _RED)
SCULPTURE_IMAGE_DOWNLOADS: dict[str, str] = {
    k: _URLS[i % len(_URLS)] for i, k in enumerate(_KEYS)
}
SCULPTURE_IMAGE_FALLBACKS: dict[str, list[str]] = {}
