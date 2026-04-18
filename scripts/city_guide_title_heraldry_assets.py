# -*- coding: utf-8 -*-
"""Title-strip heraldry: Commons filenames, alt text, and API search fallbacks."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TypeAlias

from scripts.city_guide_commons_fetch import commons_search_first_image_url

_FileStems: TypeAlias = tuple[str, ...]

# (local_rel, commons_file_stems, alt_en, commons_search_fallback)
HeraldPair: TypeAlias = tuple[str, _FileStems, str, str]

HERALDRY_BY_SLUG: dict[str, tuple[HeraldPair, HeraldPair]] = {
    "amsterdam": (
        (
            "images/guide_coat_of_arms.svg",
            ("Coat_of_arms_of_Amsterdam.svg",),
            "Coat of arms of Amsterdam",
            "Amsterdam coat of arms official svg",
        ),
        (
            "images/guide_flag.svg",
            ("Flag_of_Amsterdam.svg",),
            "Flag of Amsterdam",
            "Amsterdam city flag svg",
        ),
    ),
    "athens": (
        (
            "images/guide_coat_of_arms.svg",
            (),
            "Coat of arms of Athens",
            "Athens municipality coat of arms svg",
        ),
        (
            "images/guide_flag.svg",
            (),
            "Flag of Athens",
            "Athens Greece city flag svg",
        ),
    ),
    "bangkok": (
        (
            "images/guide_coat_of_arms.svg",
            (),
            "Seal of Bangkok",
            "Bangkok Metropolitan Administration seal svg",
        ),
        (
            "images/guide_flag.svg",
            ("Flag_of_Bangkok.svg",),
            "Flag of Bangkok",
            "Bangkok city flag svg",
        ),
    ),
    "chernivtsi": (
        (
            "images/guide_coat_of_arms.svg",
            ("Coat_of_arms_of_Chernivtsi.svg",),
            "Coat of arms of Chernivtsi",
            "Chernivtsi coat of arms svg",
        ),
        (
            "images/guide_flag.svg",
            (),
            "Flag of Chernivtsi",
            "Chernivtsi city flag svg",
        ),
    ),
    "copenhagen": (
        (
            "images/guide_coat_of_arms.svg",
            (),
            "Coat of arms of Copenhagen",
            "Copenhagen coat of arms svg",
        ),
        (
            "images/guide_flag.svg",
            (),
            "Flag of Copenhagen",
            "Copenhagen city flag svg",
        ),
    ),
    "dubai": (
        (
            "images/guide_coat_of_arms.svg",
            ("Coat_of_arms_of_Dubai.svg",),
            "Coat of arms of Dubai",
            "Dubai coat of arms svg",
        ),
        (
            "images/guide_flag.svg",
            ("Flag_of_Dubai.svg",),
            "Flag of Dubai",
            "Dubai flag svg",
        ),
    ),
    "dublin": (
        (
            "images/guide_coat_of_arms.svg",
            (),
            "Coat of arms of Dublin",
            "Dublin city coat of arms svg",
        ),
        (
            "images/guide_flag.svg",
            (),
            "Flag of Dublin",
            "Dublin city flag svg",
        ),
    ),
    "istanbul": (
        (
            "images/guide_coat_of_arms.svg",
            (),
            "Emblem of Istanbul",
            "Istanbul Metropolitan Municipality emblem svg",
        ),
        (
            "images/guide_flag.svg",
            (),
            "Flag of Istanbul",
            "Istanbul city flag svg",
        ),
    ),
    "kazan": (
        (
            "images/guide_coat_of_arms.svg",
            (),
            "Coat of arms of Kazan",
            "Kazan coat of arms svg",
        ),
        (
            "images/guide_flag.svg",
            ("Flag_of_Kazan.svg",),
            "Flag of Kazan",
            "Kazan city flag svg",
        ),
    ),
    "kharkiv": (
        (
            "images/guide_coat_of_arms.svg",
            (),
            "Coat of arms of Kharkiv",
            "Kharkiv coat of arms svg",
        ),
        (
            "images/guide_flag.svg",
            ("Flag_of_Kharkiv.svg", "Flag_of_Kharkiv_Oblast.svg"),
            "Flag of Kharkiv",
            "Kharkiv city flag svg",
        ),
    ),
    "kyiv": (
        (
            "images/guide_coat_of_arms.svg",
            (
                "COA_of_Kyiv_Kurovskyi.svg",
                "Coat_of_arms_of_Kiev.svg",
            ),
            "Coat of arms of Kyiv",
            "Kyiv coat of arms svg",
        ),
        (
            "images/guide_flag.svg",
            ("Flag_of_Kyiv_Kurovskyi.svg",),
            "Flag of Kyiv",
            "Kyiv city flag svg",
        ),
    ),
    "lisbon": (
        (
            "images/guide_coat_of_arms.svg",
            (),
            "Coat of arms of Lisbon",
            "Lisbon coat of arms svg",
        ),
        (
            "images/guide_flag.svg",
            (),
            "Flag of Lisbon",
            "Lisbon city flag svg",
        ),
    ),
    "london": (
        (
            "images/guide_coat_of_arms.svg",
            (),
            "Coat of arms of the City of London",
            "City of London coat of arms svg",
        ),
        (
            "images/guide_flag.svg",
            (),
            "Flag of the City of London",
            "City of London flag svg",
        ),
    ),
    "los_angeles": (
        (
            "images/guide_coat_of_arms.svg",
            (),
            "Seal of Los Angeles",
            "Los Angeles city seal svg",
        ),
        (
            "images/guide_flag.svg",
            ("Flag_of_Los_Angeles,_California.svg",),
            "Flag of Los Angeles",
            "Los Angeles city flag svg",
        ),
    ),
    "lviv": (
        (
            "images/guide_coat_of_arms.svg",
            (),
            "Coat of arms of Lviv",
            "Lviv coat of arms svg",
        ),
        (
            "images/guide_flag.svg",
            ("Flag_of_Lviv.svg",),
            "Flag of Lviv",
            "Lviv city flag svg",
        ),
    ),
    "minsk": (
        (
            "images/guide_coat_of_arms.svg",
            ("Coat_of_arms_of_Minsk.svg",),
            "Coat of arms of Minsk",
            "Minsk coat of arms svg",
        ),
        (
            "images/guide_flag.svg",
            ("Flag_of_Minsk.svg",),
            "Flag of Minsk",
            "Minsk city flag svg",
        ),
    ),
    "novosibirsk": (
        (
            "images/guide_coat_of_arms.svg",
            (),
            "Coat of arms of Novosibirsk",
            "Novosibirsk coat of arms svg",
        ),
        (
            "images/guide_flag.svg",
            ("Flag_of_Novosibirsk.svg",),
            "Flag of Novosibirsk",
            "Novosibirsk city flag svg",
        ),
    ),
    "odessa": (
        (
            "images/guide_coat_of_arms.svg",
            (),
            "Coat of arms of Odesa",
            "Odesa coat of arms svg",
        ),
        (
            "images/guide_flag.svg",
            (),
            "Flag of Odesa",
            "Odesa city flag svg",
        ),
    ),
    "san_francisco": (
        (
            "images/guide_coat_of_arms.svg",
            (),
            "Seal of San Francisco",
            "San Francisco city seal svg",
        ),
        (
            "images/guide_flag.svg",
            ("Flag_of_San_Francisco,_California.svg",),
            "Flag of San Francisco",
            "San Francisco city flag svg",
        ),
    ),
    "singapore": (
        (
            "images/guide_coat_of_arms.svg",
            (),
            "Coat of arms of Singapore",
            "Singapore coat of arms state crest svg",
        ),
        (
            "images/guide_flag.svg",
            ("Flag_of_Singapore.svg",),
            "Flag of Singapore",
            "Singapore flag svg",
        ),
    ),
    "tokyo": (
        (
            "images/guide_coat_of_arms.svg",
            (),
            "Emblem of Tokyo",
            "Tokyo metropolis symbol svg",
        ),
        (
            "images/guide_flag.svg",
            ("Flag_of_Tokyo_Metropolis.svg",),
            "Flag of Tokyo Metropolis",
            "Tokyo metropolis flag svg",
        ),
    ),
    "tver": (
        (
            "images/guide_coat_of_arms.svg",
            (),
            "Coat of arms of Tver",
            "Tver coat of arms svg",
        ),
        (
            "images/guide_flag.svg",
            (),
            "Flag of Tver",
            "Tver city flag svg",
        ),
    ),
    "volgograd": (
        (
            "images/guide_coat_of_arms.svg",
            (),
            "Coat of arms of Volgograd",
            "Volgograd coat of arms svg",
        ),
        (
            "images/guide_flag.svg",
            (),
            "Flag of Volgograd",
            "Volgograd city flag svg",
        ),
    ),
    "vladivostok": (
        (
            "images/guide_coat_of_arms.svg",
            (),
            "Coat of arms of Vladivostok",
            "Vladivostok coat of arms svg",
        ),
        (
            "images/guide_flag.svg",
            (),
            "Flag of Vladivostok",
            "Vladivostok city flag svg",
        ),
    ),
    "vologda": (
        (
            "images/guide_coat_of_arms.svg",
            (),
            "Coat of arms of Vologda",
            "Vologda coat of arms svg",
        ),
        (
            "images/guide_flag.svg",
            ("Flag_of_Vologda_Oblast.svg", "Flag_of_Vologda.svg"),
            "Flag of Vologda",
            "Vologda city flag svg",
        ),
    ),
    "yaroslavl": (
        (
            "images/guide_coat_of_arms.svg",
            (),
            "Coat of arms of Yaroslavl",
            "Yaroslavl coat of arms svg",
        ),
        (
            "images/guide_flag.svg",
            (),
            "Flag of Yaroslavl",
            "Yaroslavl city flag svg",
        ),
    ),
}


def _fp(stem: str) -> str:
    return "https://commons.wikimedia.org/wiki/Special:FilePath/{}".format(
        stem,
    )


def heraldry_url_candidates(
    _rel: str,
    stems: _FileStems,
    _alt: str,
    search_fallback: str,
) -> list[str]:
    """Ordered HTTPS URLs to try (FilePath; search only if no stems)."""
    out: list[str] = [_fp(s) for s in stems]
    q = search_fallback.strip()
    if not out and q:
        found = commons_search_first_image_url(q)
        if found:
            out.append(found)
    return out


def title_page_asset_specs_for_slug(
    city_slug: str,
) -> tuple[tuple[str, list[str]], ...]:
    """Pairs (rel_path, url_candidates) for image download."""
    pair = HERALDRY_BY_SLUG.get(city_slug)
    if not pair:
        return ()
    coat, flag = pair
    return (
        (coat[0], heraldry_url_candidates(*coat)),
        (flag[0], heraldry_url_candidates(*flag)),
    )


def title_symbols_for_slug(
    city_slug: str,
) -> tuple[tuple[str, str], ...]:
    """(rel, alt) tuples for HTML/PDF title strip."""
    pair = HERALDRY_BY_SLUG.get(city_slug)
    if not pair:
        return (
            ("images/guide_coat_of_arms.svg", "City emblem"),
            ("images/guide_flag.svg", "Flag"),
        )
    coat, flag = pair
    return ((coat[0], coat[2]), (flag[0], flag[2]))


def title_page_assets_for_download_arg(
    city_slug: str,
) -> tuple[tuple[str, str | Sequence[str]], ...]:
    """Shape expected by ``download_jerusalem_style_images`` title_page_assets."""
    specs = title_page_asset_specs_for_slug(city_slug)
    if not specs:
        return ()
    out: list[tuple[str, str | Sequence[str]]] = []
    for rel, urls in specs:
        if not urls:
            continue
        if len(urls) == 1:
            out.append((rel, urls[0]))
        else:
            out.append((rel, tuple(urls)))
    return tuple(out)


def heraldry_slugs() -> tuple[str, ...]:
    return tuple(sorted(HERALDRY_BY_SLUG.keys()))
