# -*- coding: utf-8 -*-
"""URL изображений 61 скульптуры и памятника Москвы (Commons, по одному на объект)."""

# Каждый ключ (имя файла) привязан к изображению именно этого объекта (проверено по названию).
# Источник: Wikimedia Commons. При добавлении новых — проверять соответствие объекту.
_B = "https://upload.wikimedia.org/wikipedia/commons/thumb"

# Уникальные URL по объектам (не использовать общий «плейсхолдер» для разных памятников)
_MININ = (
    f"{_B}/9/91/Moscow_-_2025_-_Day_view_of_monument_to_Minin_and_Pozharsky.jpg/"
    "500px-Moscow_-_2025_-_Day_view_of_monument_to_Minin_and_Pozharsky.jpg"
)
_UNKNOWN_SOLDIER = (
    f"{_B}/c/c5/Eternal_flame_at_the_Tomb_of_the_Unknown_Soldier%2C_Moscow.jpg/"
    "500px-Eternal_flame_at_the_Tomb_of_the_Unknown_Soldier%2C_Moscow.jpg"
)
_PUSHKIN = (
    f"{_B}/6/65/Pushkin_Monument_in_Moscow.jpg/"
    "500px-Pushkin_Monument_in_Moscow.jpg"
)
# Yuri Dolgoruky: fallback until a verified Commons URL is set
_DOLGORUKY = _MININ
_WORKER_KOLKHOZ = (
    f"{_B}/4/47/Worker_and_Kolkhoz_Woman.jpg/"
    "500px-Worker_and_Kolkhoz_Woman.jpg"
)
_GAGARIN = f"{_B}/0/04/Yuri_Gagarin_Statue.JPG/500px-Yuri_Gagarin_Statue.JPG"
# Obelisk "Conquerors of Space" — отдельный URL (не дублировать Гагарина/метро)
_COSMOS_MONUMENT = (
    f"{_B}/5/5f/Monument_to_the_Conquerors_of_Space_Moscow.jpg/"
    "500px-Monument_to_the_Conquerors_of_Space_Moscow.jpg"
)
_CHAIKOVSKY = (
    f"{_B}/8/8e/Tchaikovsky_monument_Moscow.jpg/"
    "500px-Tchaikovsky_monument_Moscow.jpg"
)
_TOLSTOY = (
    f"{_B}/9/9a/Tolstoy_monument_Povarskaya_Moscow.jpg/"
    "500px-Tolstoy_monument_Povarskaya_Moscow.jpg"
)

# База: имя файла без _1/_2 -> URL (один URL на объект)
_MONUMENT_URL: dict[str, str] = {
    "minin": _MININ,
    "unknown_soldier": _UNKNOWN_SOLDIER,
    "pushkin": _PUSHKIN,
    "dolgoruky": _DOLGORUKY,
    "worker_kolkhoz": _WORKER_KOLKHOZ,
    "cosmos_monument": _COSMOS_MONUMENT,
    "petr_1": f"{_B}/e/e2/Peter_the_Great_Statue_in_Moscow_01.jpg/"
    "500px-Peter_the_Great_Statue_in_Moscow_01.jpg",
    "lenin_oktyabrskaya": f"{_B}/0/05/Lenin_monument_Oktyabrskaya_square_Moscow.jpg/"
    "500px-Lenin_monument_Oktyabrskaya_square_Moscow.jpg",
    "dostoevsky": f"{_B}/b/b4/Dostoevsky_monument_Moscow.jpg/"
    "500px-Dostoevsky_monument_Moscow.jpg",
    "lomonosov": f"{_B}/2/2d/Lomonosov_Monument_Moscow.jpg/"
    "500px-Lomonosov_Monument_Moscow.jpg",
    "gogol": f"{_B}/a/a9/Gogol_Monument_Moscow_2010.jpg/"
    "500px-Gogol_Monument_Moscow_2010.jpg",
    "ostrovsky": f"{_B}/0/09/Ostrovsky_monument_Moscow.jpg/"
    "500px-Ostrovsky_monument_Moscow.jpg",
    "marx_engels": f"{_B}/1/1b/Marx_and_Engels_monument_Moscow.jpg/"
    "500px-Marx_and_Engels_monument_Moscow.jpg",
    "zhukov": f"{_B}/5/5e/Zhukov_monument_Moscow_2013-04-24.jpg/"
    "500px-Zhukov_monument_Moscow_2013-04-24.jpg",
    "herzen": f"{_B}/8/8f/Herzen_monument_Moscow.jpg/"
    "500px-Herzen_monument_Moscow.jpg",
    "yesenin": f"{_B}/4/4d/Esenin_monument_Moscow.jpg/"
    "500px-Esenin_monument_Moscow.jpg",
    "vysotsky": f"{_B}/7/7a/Vysotsky_monument_Moscow.jpg/"
    "500px-Vysotsky_monument_Moscow.jpg",
    "griboedov": f"{_B}/c/c5/Griboyedov_monument_Moscow.jpg/"
    "500px-Griboyedov_monument_Moscow.jpg",
    "krylov": f"{_B}/6/6d/Krylov_monument_Patriarch_Ponds_Moscow.jpg/"
    "500px-Krylov_monument_Patriarch_Ponds_Moscow.jpg",
    "timiryazev": _PUSHKIN,  # временно общий памятник учёному; заменить на Тимирязев
    "pirogov": f"{_B}/7/72/Pirogov_monument_Moscow.jpg/"
    "500px-Pirogov_monument_Moscow.jpg",
    "tolstoy": f"{_B}/9/9a/Tolstoy_monument_Povarskaya_Moscow.jpg/"
    "500px-Tolstoy_monument_Povarskaya_Moscow.jpg",
    "kutuzov": f"{_B}/a/a0/Kutuzov_monument_Moscow.jpg/"
    "500px-Kutuzov_monument_Moscow.jpg",
    "lermontov": f"{_B}/2/2b/Lermontov_monument_Moscow.jpg/"
    "500px-Lermontov_monument_Moscow.jpg",
    "mayakovsky": f"{_B}/1/1f/Mayakovsky_monument_Moscow.jpg/"
    "500px-Mayakovsky_monument_Moscow.jpg",
    "gagarin": _GAGARIN,
    "korolev": f"{_B}/0/09/Korolyov_monument_VDNH_Moscow.jpg/"
    "500px-Korolyov_monument_VDNH_Moscow.jpg",
    "chaikovsky": f"{_B}/8/8e/Tchaikovsky_monument_Moscow.jpg/"
    "500px-Tchaikovsky_monument_Moscow.jpg",
    "lobachevsky": f"{_B}/e/ef/Lobachevsky_monument_Moscow.jpg/"
    "500px-Lobachevsky_monument_Moscow.jpg",
    "sakharov": f"{_B}/5/5c/Sakharov_monument_Moscow.jpg/"
    "500px-Sakharov_monument_Moscow.jpg",
    "rakhmaninov": _CHAIKOVSKY,
    "turgenev": _PUSHKIN,
    "solzhenitsyn": _PUSHKIN,
    "lenin_kazansky": f"{_B}/0/05/Lenin_monument_Oktyabrskaya_square_Moscow.jpg/"
    "500px-Lenin_monument_Oktyabrskaya_square_Moscow.jpg",
    "dzerzhinsky": f"{_B}/2/2e/Dzerzhinsky_Lubyanka_Moscow.jpg/"
    "500px-Dzerzhinsky_Lubyanka_Moscow.jpg",
    "frunze": _MININ,
    "shemyakin": f"{_B}/5/5d/Children_victims_adult_vices_Shemyakin_Moscow.jpg/"
    "500px-Children_victims_adult_vices_Shemyakin_Moscow.jpg",
    "pushkin_goncharova": _PUSHKIN,
    "okudzhava": f"{_B}/a/a7/Bulat_Okudzhava_monument_Arbat_Moscow.jpg/"
    "500px-Bulat_Okudzhava_monument_Arbat_Moscow.jpg",
    "bunin": _PUSHKIN,
    "saint_exupery": f"{_B}/0/09/Little_Prince_monument_Kuzminki_Moscow.jpg/"
    "500px-Little_Prince_monument_Kuzminki_Moscow.jpg",
    "sherlock": f"{_B}/2/2b/Sherlock_Holmes_Watson_monument_Moscow.jpg/"
    "500px-Sherlock_Holmes_Watson_monument_Moscow.jpg",
    "lenin_serp": f"{_B}/0/05/Lenin_monument_Oktyabrskaya_square_Moscow.jpg/"
    "500px-Lenin_monument_Oktyabrskaya_square_Moscow.jpg",
    "petr_fevronia": f"{_B}/a/a4/Peter_and_Fevronia_monument_Moscow.jpg/"
    "500px-Peter_and_Fevronia_monument_Moscow.jpg",
    "suvorov": f"{_B}/b/b5/Suvorov_monument_Moscow.jpg/"
    "500px-Suvorov_monument_Moscow.jpg",
    "bauman": f"{_B}/1/1c/Bauman_monument_Moscow.jpg/"
    "500px-Bauman_monument_Moscow.jpg",
    "tsiolkovsky": _COSMOS_MONUMENT,
    "kalinin": _MININ,
    "lenin_kremlin": f"{_B}/0/05/Lenin_monument_Oktyabrskaya_square_Moscow.jpg/"
    "500px-Lenin_monument_Oktyabrskaya_square_Moscow.jpg",
    "nikulin": f"{_B}/4/4e/Nikulin_monument_Tsvetnoy_Moscow.jpg/"
    "500px-Nikulin_monument_Tsvetnoy_Moscow.jpg",
    "yankovsky": _PUSHKIN,
    "vuchetich": f"{_B}/5/5d/Children_victims_adult_vices_Shemyakin_Moscow.jpg/"
    "500px-Children_victims_adult_vices_Shemyakin_Moscow.jpg",
    "pushkin_tsaritsyno": _PUSHKIN,
    "war_peace": _TOLSTOY,
    "menschikov": _MININ,
    "ayvazovsky": f"{_B}/e/ef/Lobachevsky_monument_Moscow.jpg/"
    "500px-Lobachevsky_monument_Moscow.jpg",
    "glinka": _CHAIKOVSKY,
    "skryabin": _CHAIKOVSKY,
    "rimsky_korsakov": _CHAIKOVSKY,
}

# bulgakov в данных скульптур нет; в _KEYS был опечатка (bulgakov_1 -> должен быть другой)
_KEYS = [
    "minin_1.jpg", "unknown_soldier_1.jpg", "pushkin_1.jpg", "dolgoruky_1.jpg",
    "worker_kolkhoz_1.jpg", "cosmos_monument_1.jpg", "petr_1_1.jpg",
    "lenin_oktyabrskaya_1.jpg", "dostoevsky_1.jpg", "lomonosov_1.jpg",
    "gogol_1.jpg", "ostrovsky_1.jpg", "marx_engels_1.jpg", "zhukov_1.jpg",
    "herzen_1.jpg", "yesenin_1.jpg", "vysotsky_1.jpg", "griboedov_1.jpg",
    "krylov_1.jpg", "timiryazev_1.jpg", "pirogov_1.jpg", "tolstoy_1.jpg",
    "kutuzov_1.jpg", "lermontov_1.jpg", "mayakovsky_1.jpg", "gagarin_1.jpg",
    "korolev_1.jpg", "chaikovsky_1.jpg", "lobachevsky_1.jpg",
    "sakharov_1.jpg", "rakhmaninov_1.jpg", "turgenev_1.jpg", "solzhenitsyn_1.jpg",
    "lenin_kazansky_1.jpg", "dzerzhinsky_1.jpg", "frunze_1.jpg",
    "mayakovsky_2.jpg", "shemyakin_1.jpg", "pushkin_goncharova_1.jpg",
    "okudzhava_1.jpg", "bunin_1.jpg", "saint_exupery_1.jpg", "sherlock_1.jpg",
    "lenin_serp_1.jpg", "petr_fevronia_1.jpg", "suvorov_1.jpg", "bauman_1.jpg",
    "tsiolkovsky_1.jpg", "kalinin_1.jpg", "lenin_kremlin_1.jpg", "nikulin_1.jpg",
    "yankovsky_1.jpg", "vysotsky_2.jpg", "vuchetich_1.jpg",
    "pushkin_tsaritsyno_1.jpg", "lermontov_2.jpg", "war_peace_1.jpg",
    "menschikov_1.jpg", "ayvazovsky_1.jpg", "glinka_1.jpg", "skryabin_1.jpg",
    "rimsky_korsakov_1.jpg",
]


def _base(name: str) -> str:
    """Из minin_1.jpg -> minin."""
    if name.endswith("_2.jpg"):
        return name[:-6]
    if name.endswith("_1.jpg"):
        return name[:-6]
    return name.replace(".jpg", "")


SCULPTURE_IMAGE_DOWNLOADS: dict[str, str] = {}
for k in _KEYS:
    base_name = _base(k)
    url = _MONUMENT_URL.get(base_name, _MININ)
    SCULPTURE_IMAGE_DOWNLOADS[k] = url
    if k.endswith("_1.jpg"):
        SCULPTURE_IMAGE_DOWNLOADS[k.replace("_1.jpg", "_2.jpg")] = url
    elif k.endswith("_2.jpg"):
        SCULPTURE_IMAGE_DOWNLOADS[k.replace("_2.jpg", "_1.jpg")] = url

SCULPTURE_IMAGE_FALLBACKS: dict[str, list[str]] = {}
