# -*- coding: utf-8 -*-
"""Image URLs for E2E test guide. Uses Wikimedia Commons (stable, no key)."""

# Different Commons images to avoid duplicates
_COMMONS = "https://upload.wikimedia.org/wikipedia/commons/thumb"
_URLS = [
    "{}/0/0f/Moscow_State_University_edit1.jpg/320px-"
    "Moscow_State_University_edit1.jpg".format(_COMMONS),
    "{}/5/5a/Red_Square_2013-05-09.jpg/320px-Red_Square_2013-05-09.jpg".format(
        _COMMONS,
    ),
    "{}/4/4a/Spasskaya_Tower_in_2013.jpg/320px-Spasskaya_Tower_in_2013.jpg".format(
        _COMMONS,
    ),
    "{}/e/ef/Moscow_State_University_edit2.jpg/320px-"
    "Moscow_State_University_edit2.jpg".format(_COMMONS),
]

TEST_E2E_IMAGE_DOWNLOADS: dict[str, str] = {}
TEST_E2E_IMAGE_FALLBACKS: dict[str, list[str]] = {}

for pi, place in enumerate(("place_a", "place_b", "place_c", "place_d", "place_e")):
    for i in range(1, 5):
        bn = "{}_{}.jpg".format(place, i)
        TEST_E2E_IMAGE_DOWNLOADS[bn] = _URLS[(pi * 4 + i - 1) % len(_URLS)]
        TEST_E2E_IMAGE_FALLBACKS[bn] = []
