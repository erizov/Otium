# -*- coding: utf-8 -*-
"""Image URLs for osobnjaki batch 2 (culture.ru + Commons)."""

_CDN = "https://cdn.culture.ru/c/{}.800x600.jpg"
_NARKOMFIN = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/"
    "Moscow_Narkomfin_6891.jpg/1280px-Moscow_Narkomfin_6891.jpg"
)
_RYAB_BANK = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/"
    "Schechtel%2C_Birzhevaya_Square%2C_Ryabushinsky_Bank.jpg/1280px-"
    "Schechtel%2C_Birzhevaya_Square%2C_Ryabushinsky_Bank.jpg"
)
_SPIR36 = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/"
    "Moscow%2C_Spiridonovka_36.jpg/1280px-Moscow%2C_Spiridonovka_36.jpg"
)


def _four(prefix: str, url: str) -> dict[str, str]:
    return {
        "{}_1.jpg".format(prefix): url,
        "{}_2.jpg".format(prefix): url,
        "{}_3.jpg".format(prefix): url,
        "{}_4.jpg".format(prefix): url,
    }


OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS: dict[str, str] = {}
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(
    _four("politkatorzh", _CDN.format("271918"))
)
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(
    _four("palibin", _CDN.format("264732"))
)
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(
    _four("izvestia_dom", _CDN.format("264902"))
)
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(
    _four("dynamo_dom", _CDN.format("264903"))
)
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(_four("narkomfin", _NARKOMFIN))
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(
    _four("dom_knigi", _CDN.format("266201"))
)
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(
    _four("smirnov_tversk", (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/"
        "Smirnov%27s_house_%28Tverskoy_Boulevard%29.jpg/1280px-"
        "Smirnov%27s_house_%28Tverskoy_Boulevard%29.jpg"
    ))
)
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(
    _four("schechtel_house", (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/"
        "Schechtel%27s_mansion_in_Moscow.jpg/1280px-"
        "Schechtel%27s_mansion_in_Moscow.jpg"
    ))
)
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(
    _four("utro_rossii", (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/"
        "Utro_Rossii_building_Moscow.jpg/1280px-"
        "Utro_Rossii_building_Moscow.jpg"
    ))
)
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(
    _four("snegirev", (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/"
        "Snegirev_House_Plyushchikha.jpg/1280px-"
        "Snegirev_House_Plyushchikha.jpg"
    ))
)
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(
    _four("morozova_varvara", (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/"
        "Morozova_House_Myasnitskaya.jpg/1280px-"
        "Morozova_House_Myasnitskaya.jpg"
    ))
)
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(
    _four("khludov", _CDN.format("264917"))
)
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(
    _four("kekushev_ost", (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/"
        "Kekushev_apartment_house_Ostozhenka.jpg/1280px-"
        "Kekushev_apartment_house_Ostozhenka.jpg"
    ))
)
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(
    _four("shchapov", _CDN.format("264320"))
)
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(
    _four("korobkov", _CDN.format("264283"))
)
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(
    _four("mamontov", _CDN.format("264435"))
)
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(
    _four("golitsyn", _CDN.format("264916"))
)
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(
    _four("tsvetkov", (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/"
        "Tsvetkov_House_Prechistenskaya.jpg/1280px-"
        "Tsvetkov_House_Prechistenskaya.jpg"
    ))
)
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(
    _four("vtorov", _CDN.format("264317"))
)
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(
    _four("prokofiev_bg", _CDN.format("264889"))
)
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(
    _four("bakhrushin", _CDN.format("264732"))
)
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(
    _four("lunin", _CDN.format("264268"))
)
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(
    _four("nashchokin", _CDN.format("264283"))
)
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(_four("ryabushinsky_bank", _RYAB_BANK))
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(_four("spiridonovka_36", _SPIR36))
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(
    _four("dolgorukov", (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/"
        "House_of_the_Unions_Moscow.jpg/1280px-"
        "House_of_the_Unions_Moscow.jpg"
    ))
)
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(
    _four("sollogub", _CDN.format("264435"))
)
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(
    _four("pushkin_museum_house", (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/"
        "Pushkin_Museum_main_building_Moscow.jpg/1280px-"
        "Pushkin_Museum_main_building_Moscow.jpg"
    ))
)
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(
    _four("botkin", _CDN.format("264324"))
)
OSOBNJAKI_BATCH2_IMAGE_DOWNLOADS.update(
    _four("mazepin", _CDN.format("266315"))
)
