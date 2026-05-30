# -*- coding: utf-8 -*-
"""E2E test guide: 5 items, 4 images each, maps. Used by tests/test_e2e_workflow.py."""

IMAGES_SUBFOLDER = "test_e2e"


def _img(name: str) -> str:
    return "images/{}/{}".format(IMAGES_SUBFOLDER, name)


TEST_E2E_PLACES = [
    {
        "name": "Test Place A",
        "address": "Test St 1",
        "style": "test",
        "highlights": ["H1"],
        "featured": True,
        "history": "Test history A.",
        "significance": "Test significance.",
        "facts": ["Fact 1"],
        "images": [
            _img("place_a_1.jpg"),
            _img("place_a_2.jpg"),
            _img("place_a_3.jpg"),
            _img("place_a_4.jpg"),
        ],
        "map_url": "",
        "lat": 55.7558,
        "lon": 37.6173,
    },
    {
        "name": "Test Place B",
        "address": "Test St 2",
        "style": "test",
        "highlights": ["H2"],
        "featured": False,
        "history": "Test history B.",
        "significance": "Test significance.",
        "facts": ["Fact 2"],
        "images": [
            _img("place_b_1.jpg"),
            _img("place_b_2.jpg"),
            _img("place_b_3.jpg"),
            _img("place_b_4.jpg"),
        ],
        "map_url": "",
        "lat": 55.7560,
        "lon": 37.6175,
    },
    {
        "name": "Test Place C",
        "address": "Test St 3",
        "style": "test",
        "highlights": ["H3"],
        "featured": False,
        "history": "Test history C.",
        "significance": "Test significance.",
        "facts": ["Fact 3"],
        "images": [
            _img("place_c_1.jpg"),
            _img("place_c_2.jpg"),
            _img("place_c_3.jpg"),
            _img("place_c_4.jpg"),
        ],
        "map_url": "",
        "lat": 55.7562,
        "lon": 37.6177,
    },
    {
        "name": "Test Place D",
        "address": "Test St 4",
        "style": "test",
        "highlights": ["H4"],
        "featured": False,
        "history": "Test history D.",
        "significance": "Test significance.",
        "facts": ["Fact 4"],
        "images": [
            _img("place_d_1.jpg"),
            _img("place_d_2.jpg"),
            _img("place_d_3.jpg"),
            _img("place_d_4.jpg"),
        ],
        "map_url": "",
        "lat": 55.7564,
        "lon": 37.6179,
    },
    {
        "name": "Test Place E",
        "address": "Test St 5",
        "style": "test",
        "highlights": ["H5"],
        "featured": False,
        "history": "Test history E.",
        "significance": "Test significance.",
        "facts": ["Fact 5"],
        "images": [
            _img("place_e_1.jpg"),
            _img("place_e_2.jpg"),
            _img("place_e_3.jpg"),
            _img("place_e_4.jpg"),
        ],
        "map_url": "",
        "lat": 55.7566,
        "lon": 37.6181,
    },
]
