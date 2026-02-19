# -*- coding: utf-8 -*-
"""Image URLs filled by place name (Commons, Pixabay, Pexels, Openverse, Pastvu, etc.). Round-robin fallbacks per slot."""

MARKET_IMAGE_DOWNLOADS: dict[str, str] = {
    "danilovsky_1.jpg": "https://upload.wikimedia.org/wikipedia/commons/a/af/Danilovskiy_market_%282015%29_by_shakko_04.JPG",
    "danilovsky_2.jpg": "https://upload.wikimedia.org/wikipedia/commons/7/7c/Moskow_danilovsky_market_construction3.JPG",
    "danilovsky_3.jpg": "https://upload.wikimedia.org/wikipedia/commons/d/d2/Moskow_danilovsky_market_construction4.JPG",
    "danilovsky_4.jpg": "https://live.staticflickr.com/65535/49011128672_a1916ce643_b.jpg",
    "depo_1.jpg": "https://live.staticflickr.com/8616/16767837905_43ab05674e_b.jpg",
    "depo_2.jpg": "https://upload.wikimedia.org/wikipedia/commons/b/b8/%D0%90-%D0%A7%D0%A12-549%2C_%D0%B4%D0%B5%D0%BF%D0%BE_%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0-%D0%9F%D0%B0%D1%81%D1%81%D0%B0%D0%B6%D0%B8%D1%80%D1%81%D0%BA%D0%B0%D1%8F-%D0%9A%D1%83%D1%80%D1%81%D0%BA%D0%B0%D1%8F.jpg",
    "depo_3.jpg": "https://live.staticflickr.com/7588/16147913983_c74b2b3c33_b.jpg",
    "depo_4.jpg": "https://upload.wikimedia.org/wikipedia/commons/f/f2/%D0%A7%D0%A17-319%2C_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%2C_%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%2C_%D0%B4%D0%B5%D0%BF%D0%BE_%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0-%D0%9F%D0%B0%D1%81%D1%81%D0%B0%D0%B6%D0%B8%D1%80%D1%81%D0%BA%D0%B0%D1%8F-%D0%9A%D1%83%D1%80%D1%81%D0%BA%D0%B0%D1%8F_%28Trainpix_150291%29.jpg",
    "dorogomilovsky_1.jpg": "https://upload.wikimedia.org/wikipedia/commons/b/b1/%D0%94%D0%BE%D1%80%D0%BE%D0%B3%D0%BE%D0%BC%D0%B8%D0%BB%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9_%D1%80%D1%8B%D0%BD%D0%BE%D0%BA.jpg",
    "dorogomilovsky_2.jpg": "https://upload.wikimedia.org/wikipedia/commons/9/9a/%D0%92%D0%B8%D0%B4_%D1%81%D0%B8%D1%82%D0%B8_%D1%81_%D0%B4%D0%BE%D1%80%D0%BE%D0%B3%D0%BE_%D0%BC%D0%B8%D0%BB%D0%BE_%D0%B2_%D0%BA%D0%BE%D0%B3%D0%BE_%D1%80%D1%8B%D0%BD%D0%BA%D0%B0.jpg",
    "dorogomilovsky_3.jpg": "https://upload.wikimedia.org/wikipedia/commons/b/b1/%D0%94%D0%BE%D1%80%D0%BE%D0%B3%D0%BE%D0%BC%D0%B8%D0%BB%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9_%D1%80%D1%8B%D0%BD%D0%BE%D0%BA.jpg",
    "dorogomilovsky_4.jpg": "https://images.pexels.com/photos/31946770/pexels-photo-31946770.jpeg",
    "eliseevsky_1.jpg": "https://upload.wikimedia.org/wikipedia/commons/7/71/Moscow%2C_Tverskaya_st._14_-_Eliseevskiy_shop_%282013%29_by_shakko_01.jpg",
    "eliseevsky_2.jpg": "https://live.staticflickr.com/8143/7462109274_460653889d_b.jpg",
    "eliseevsky_3.jpg": "https://live.staticflickr.com/2489/3702341364_d056cdaa68_b.jpg",
    "eliseevsky_4.jpg": "https://live.staticflickr.com/6020/5919283043_f660d6bc65_b.jpg",
    "gum_1.jpg": "https://live.staticflickr.com/8642/16631554715_e4bf4879e6_b.jpg",
    "gum_2.jpg": "https://live.staticflickr.com/7621/16221733464_b92d705c81.jpg",
    "gum_3.jpg": "https://live.staticflickr.com/8120/8647162819_d067495f2c.jpg",
    "gum_4.jpg": "https://live.staticflickr.com/4106/5132527603_14b25d7efb_b.jpg",
    "patriarch_market_1.jpg": "https://images.pexels.com/photos/16849575/pexels-photo-16849575.jpeg",
    "patriarch_market_2.jpg": "https://images.pexels.com/photos/31810194/pexels-photo-31810194.jpeg",
    "patriarch_market_3.jpg": "https://images.pexels.com/photos/31946770/pexels-photo-31946770.jpeg",
    "patriarch_market_4.jpg": "https://images.pexels.com/photos/5357794/pexels-photo-5357794.jpeg",
    "preobrazhensky_1.jpg": "https://upload.wikimedia.org/wikipedia/commons/8/8b/%D0%9F%D1%80%D0%B5%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D1%81%D0%BA%D0%B8%D0%B9_%D1%80%D1%8B%D0%BD%D0%BE%D0%BA_%28%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%29_23.jpg",
    "preobrazhensky_2.jpg": "https://upload.wikimedia.org/wikipedia/commons/d/d7/%D0%9F%D1%80%D0%B5%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D1%81%D0%BA%D0%B8%D0%B9_%D1%80%D1%8B%D0%BD%D0%BE%D0%BA_%28%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%29_33.jpg",
    "preobrazhensky_3.jpg": "https://upload.wikimedia.org/wikipedia/commons/4/4d/%D0%9F%D1%80%D0%B5%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D1%81%D0%BA%D0%B8%D0%B9_%D1%80%D1%8B%D0%BD%D0%BE%D0%BA_%28%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%29_37.jpg",
    "preobrazhensky_4.jpg": "https://upload.wikimedia.org/wikipedia/commons/a/a7/%D0%9F%D1%80%D0%B5%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D1%81%D0%BA%D0%B8%D0%B9_%D1%80%D1%8B%D0%BD%D0%BE%D0%BA_%28%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%29_20.jpg",
    "rizhsky_1.jpg": "https://live.staticflickr.com/7816/46584257544_2bc8f0bf30_b.jpg",
    "rizhsky_2.jpg": "https://live.staticflickr.com/723/22521353498_4377b9b252_b.jpg",
    "rizhsky_3.jpg": "https://live.staticflickr.com/754/22316930784_d1362f6f4b_b.jpg",
    "rizhsky_4.jpg": "https://live.staticflickr.com/5646/22318512253_c032dc7d86_b.jpg",
    "tsum_1.jpg": "https://live.staticflickr.com/166/338467448_725ccd34b7_b.jpg",
    "tsum_2.jpg": "https://live.staticflickr.com/8660/16642814586_cbba08679e_b.jpg",
    "tsum_3.jpg": "https://live.staticflickr.com/5676/23588625626_470210ae37_b.jpg",
    "tsum_4.jpg": "https://upload.wikimedia.org/wikipedia/commons/1/1e/%D0%A6%D1%83%D0%BC-%D1%82%D0%BE%D1%80%D0%B5%D0%B7.jpg",
    "vremya_1.jpg": "https://images.pexels.com/photos/31946792/pexels-photo-31946792.jpeg",
    "vremya_2.jpg": "https://images.pexels.com/photos/16443021/pexels-photo-16443021.jpeg",
    "vremya_3.jpg": "https://images.pexels.com/photos/14100378/pexels-photo-14100378.jpeg",
    "vremya_4.jpg": "https://img.pastvu.com/d/z/x/u/zxumo325cqiefnvzq1.jpg",
}

MARKET_IMAGE_FALLBACKS: dict[str, list[str]] = {
    "dorogomilovsky_1.jpg": [
        "https://images.pexels.com/photos/1846014/pexels-photo-1846014.jpeg",
        "https://images.pexels.com/photos/31946770/pexels-photo-31946770.jpeg",
    ],
    "dorogomilovsky_2.jpg": [
        "https://images.pexels.com/photos/34392806/pexels-photo-34392806.jpeg",
        "https://upload.wikimedia.org/wikipedia/commons/b/b1/%D0%94%D0%BE%D1%80%D0%BE%D0%B3%D0%BE%D0%BC%D0%B8%D0%BB%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9_%D1%80%D1%8B%D0%BD%D0%BE%D0%BA.jpg",
        "https://images.pexels.com/photos/31946770/pexels-photo-31946770.jpeg",
    ],
    "dorogomilovsky_3.jpg": [
        "https://images.pexels.com/photos/34392806/pexels-photo-34392806.jpeg",
        "https://images.pexels.com/photos/1846014/pexels-photo-1846014.jpeg",
        "https://images.pexels.com/photos/31946770/pexels-photo-31946770.jpeg",
    ],
    "dorogomilovsky_4.jpg": [
        "https://images.pexels.com/photos/34392806/pexels-photo-34392806.jpeg",
        "https://images.pexels.com/photos/1846014/pexels-photo-1846014.jpeg",
        "https://upload.wikimedia.org/wikipedia/commons/b/b1/%D0%94%D0%BE%D1%80%D0%BE%D0%B3%D0%BE%D0%BC%D0%B8%D0%BB%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9_%D1%80%D1%8B%D0%BD%D0%BE%D0%BA.jpg",
    ],
    "patriarch_market_1.jpg": [
        "https://images.pexels.com/photos/31810194/pexels-photo-31810194.jpeg",
        "https://images.pexels.com/photos/31946770/pexels-photo-31946770.jpeg",
        "https://images.pexels.com/photos/5357794/pexels-photo-5357794.jpeg",
    ],
    "patriarch_market_2.jpg": [
        "https://images.pexels.com/photos/16849575/pexels-photo-16849575.jpeg",
        "https://images.pexels.com/photos/31946770/pexels-photo-31946770.jpeg",
        "https://images.pexels.com/photos/5357794/pexels-photo-5357794.jpeg",
    ],
    "patriarch_market_3.jpg": [
        "https://images.pexels.com/photos/16849575/pexels-photo-16849575.jpeg",
        "https://images.pexels.com/photos/31810194/pexels-photo-31810194.jpeg",
        "https://images.pexels.com/photos/5357794/pexels-photo-5357794.jpeg",
    ],
    "patriarch_market_4.jpg": [
        "https://images.pexels.com/photos/16849575/pexels-photo-16849575.jpeg",
        "https://images.pexels.com/photos/31810194/pexels-photo-31810194.jpeg",
        "https://images.pexels.com/photos/31946770/pexels-photo-31946770.jpeg",
    ],
    "vremya_1.jpg": [
        "https://images.pexels.com/photos/16443021/pexels-photo-16443021.jpeg",
        "https://images.pexels.com/photos/14100378/pexels-photo-14100378.jpeg",
        "https://img.pastvu.com/d/z/x/u/zxumo325cqiefnvzq1.jpg",
    ],
    "vremya_2.jpg": [
        "https://images.pexels.com/photos/31946792/pexels-photo-31946792.jpeg",
        "https://images.pexels.com/photos/14100378/pexels-photo-14100378.jpeg",
        "https://img.pastvu.com/d/z/x/u/zxumo325cqiefnvzq1.jpg",
    ],
    "vremya_3.jpg": [
        "https://images.pexels.com/photos/31946792/pexels-photo-31946792.jpeg",
        "https://images.pexels.com/photos/16443021/pexels-photo-16443021.jpeg",
        "https://img.pastvu.com/d/z/x/u/zxumo325cqiefnvzq1.jpg",
    ],
    "vremya_4.jpg": [
        "https://images.pexels.com/photos/31946792/pexels-photo-31946792.jpeg",
        "https://images.pexels.com/photos/16443021/pexels-photo-16443021.jpeg",
        "https://images.pexels.com/photos/14100378/pexels-photo-14100378.jpeg",
    ],
}

