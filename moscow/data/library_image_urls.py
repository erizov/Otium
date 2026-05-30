# -*- coding: utf-8 -*-
"""Image URLs filled by place name (Commons, Pixabay, Pexels, Openverse, Pastvu, etc.). Round-robin fallbacks per slot."""

LIBRARY_IMAGE_DOWNLOADS: dict[str, str] = {
    "dostoevsky_lib_1.jpg": "https://images.pexels.com/photos/5884209/pexels-photo-5884209.jpeg",
    "dostoevsky_lib_2.jpg": "https://img.pastvu.com/d/z/x/u/zxumo325cqiefnvzq1.jpg",
    "dostoevsky_lib_3.jpg": "https://images.pexels.com/photos/135526/pexels-photo-135526.jpeg",
    "dostoevsky_lib_4.jpg": "https://img.pastvu.com/d/8/f/3/8f389b60ef66ec3fa2fbab46e6feaf0b.jpg",
    "inostranka_1.jpg": "https://live.staticflickr.com/628/22338631194_af58dd2c63_b.jpg",
    "inostranka_2.jpg": "https://live.staticflickr.com/608/22935353406_bd9401c887_b.jpg",
    "inostranka_3.jpg": "https://live.staticflickr.com/5658/22542957517_7c4ef32146_b.jpg",
    "inostranka_4.jpg": "https://live.staticflickr.com/5750/22972448721_b5e2dd238f_b.jpg",
    "nekrasov_lib_1.jpg": "https://images.pexels.com/photos/31946792/pexels-photo-31946792.jpeg",
    "nekrasov_lib_2.jpg": "https://images.pexels.com/photos/12570415/pexels-photo-12570415.jpeg",
    "nekrasov_lib_3.jpg": "https://images.pexels.com/photos/3848886/pexels-photo-3848886.jpeg",
    "nekrasov_lib_4.jpg": "https://img.pastvu.com/d/z/x/u/zxumo325cqiefnvzq1.jpg",
    "pashkov_house_1.jpg": "https://live.staticflickr.com/3262/2703384123_0245881404.jpg",
    "pashkov_house_2.jpg": "https://upload.wikimedia.org/wikipedia/commons/8/89/Moscow_-_2025_-_Pashkov_House.jpg",
    "pashkov_house_3.jpg": "https://live.staticflickr.com/957/28245004898_2c5861963d_b.jpg",
    "pashkov_house_4.jpg": "https://upload.wikimedia.org/wikipedia/commons/d/d7/Moscow_-_2025_-_Pashkov%27s_House.jpg",
    "rgb_1.jpg": "https://live.staticflickr.com/7893/31840119247_dcb343a220_b.jpg",
    "rgb_2.jpg": "https://live.staticflickr.com/4240/35255414955_b9a05e8a35_b.jpg",
    "rgb_3.jpg": "https://live.staticflickr.com/2673/4153667882_30cfd799da_b.jpg",
    "rgb_4.jpg": "https://live.staticflickr.com/2564/4128588476_51be8e701c_b.jpg",
    "rgub_1.jpg": "https://upload.wikimedia.org/wikipedia/commons/b/b6/Zal_redkoy_knigi_RGBM.jpg",
    "rgub_2.jpg": "https://avatars.mds.yandex.net/get-altay/15291179/2a0000019897b25262b335aa14a29f15aacc/orig",
    "rgub_3.jpg": "https://upload.wikimedia.org/wikipedia/commons/8/8b/Zal_literatury_na_inostrannyh_yazykah_v_RGBM.jpg",
    "rgub_4.jpg": "https://avatars.mds.yandex.net/get-altay/15291179/2a0000019897b25262b335aa14a29f15aacc/XXXL",
    "turgenev_lib_1.jpg": "https://images.pexels.com/photos/12064/pexels-photo-12064.jpeg",
    "turgenev_lib_2.jpg": "https://images.pexels.com/photos/11738598/pexels-photo-11738598.jpeg",
    "turgenev_lib_3.jpg": "https://img.pastvu.com/d/z/x/u/zxumo325cqiefnvzq1.jpg",
    "turgenev_lib_4.jpg": "https://images.pexels.com/photos/35019674/pexels-photo-35019674.jpeg",
}

LIBRARY_IMAGE_FALLBACKS: dict[str, list[str]] = {
    "dostoevsky_lib_1.jpg": [
        "https://img.pastvu.com/d/z/x/u/zxumo325cqiefnvzq1.jpg",
        "https://images.pexels.com/photos/135526/pexels-photo-135526.jpeg",
        "https://img.pastvu.com/d/8/f/3/8f389b60ef66ec3fa2fbab46e6feaf0b.jpg",
    ],
    "dostoevsky_lib_2.jpg": [
        "https://images.pexels.com/photos/5884209/pexels-photo-5884209.jpeg",
        "https://images.pexels.com/photos/135526/pexels-photo-135526.jpeg",
        "https://img.pastvu.com/d/8/f/3/8f389b60ef66ec3fa2fbab46e6feaf0b.jpg",
    ],
    "dostoevsky_lib_3.jpg": [
        "https://images.pexels.com/photos/5884209/pexels-photo-5884209.jpeg",
        "https://img.pastvu.com/d/z/x/u/zxumo325cqiefnvzq1.jpg",
        "https://img.pastvu.com/d/8/f/3/8f389b60ef66ec3fa2fbab46e6feaf0b.jpg",
    ],
    "dostoevsky_lib_4.jpg": [
        "https://images.pexels.com/photos/5884209/pexels-photo-5884209.jpeg",
        "https://img.pastvu.com/d/z/x/u/zxumo325cqiefnvzq1.jpg",
        "https://images.pexels.com/photos/135526/pexels-photo-135526.jpeg",
    ],
    "nekrasov_lib_1.jpg": [
        "https://images.pexels.com/photos/12570415/pexels-photo-12570415.jpeg",
        "https://images.pexels.com/photos/3848886/pexels-photo-3848886.jpeg",
        "https://img.pastvu.com/d/z/x/u/zxumo325cqiefnvzq1.jpg",
    ],
    "nekrasov_lib_2.jpg": [
        "https://images.pexels.com/photos/31946792/pexels-photo-31946792.jpeg",
        "https://images.pexels.com/photos/3848886/pexels-photo-3848886.jpeg",
        "https://img.pastvu.com/d/z/x/u/zxumo325cqiefnvzq1.jpg",
    ],
    "nekrasov_lib_3.jpg": [
        "https://images.pexels.com/photos/31946792/pexels-photo-31946792.jpeg",
        "https://images.pexels.com/photos/12570415/pexels-photo-12570415.jpeg",
        "https://img.pastvu.com/d/z/x/u/zxumo325cqiefnvzq1.jpg",
    ],
    "nekrasov_lib_4.jpg": [
        "https://images.pexels.com/photos/31946792/pexels-photo-31946792.jpeg",
        "https://images.pexels.com/photos/12570415/pexels-photo-12570415.jpeg",
        "https://images.pexels.com/photos/3848886/pexels-photo-3848886.jpeg",
    ],
    "turgenev_lib_1.jpg": [
        "https://images.pexels.com/photos/11738598/pexels-photo-11738598.jpeg",
        "https://img.pastvu.com/d/z/x/u/zxumo325cqiefnvzq1.jpg",
        "https://images.pexels.com/photos/35019674/pexels-photo-35019674.jpeg",
    ],
    "turgenev_lib_2.jpg": [
        "https://images.pexels.com/photos/12064/pexels-photo-12064.jpeg",
        "https://img.pastvu.com/d/z/x/u/zxumo325cqiefnvzq1.jpg",
        "https://images.pexels.com/photos/35019674/pexels-photo-35019674.jpeg",
    ],
    "turgenev_lib_3.jpg": [
        "https://images.pexels.com/photos/12064/pexels-photo-12064.jpeg",
        "https://images.pexels.com/photos/11738598/pexels-photo-11738598.jpeg",
        "https://images.pexels.com/photos/35019674/pexels-photo-35019674.jpeg",
    ],
    "turgenev_lib_4.jpg": [
        "https://images.pexels.com/photos/12064/pexels-photo-12064.jpeg",
        "https://images.pexels.com/photos/11738598/pexels-photo-11738598.jpeg",
        "https://img.pastvu.com/d/z/x/u/zxumo325cqiefnvzq1.jpg",
    ],
}

