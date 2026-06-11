# -*- coding: utf-8 -*-

"""Moscow title-page heraldry: historical coats, city symbols, universities."""



from __future__ import annotations



from html import escape

from pathlib import Path



from scripts.city_guide_core import smallest_same_stem_image_rel

from scripts.city_guide_historical_reference_ru import (

    HERALDRY_CHAPTER_LABEL_EN,

    HERALDRY_CHAPTER_LABEL_RU,

)

from scripts.moscow_title_assets_data import (

    moscow_history_coats,

    moscow_universities,

)





def _fig_if_exists(root: Path, rel: str, alt: str, extra_class: str) -> str:

    resolved = smallest_same_stem_image_rel(root, rel)

    if not resolved:

        return ""

    src = "../{}".format(resolved.lstrip("/").replace("\\", "/"))

    return (

        '<figure class="heraldry-fig {}" title="{}">'

        '<img src="{}" alt="{}"/>'

        "</figure>".format(

            extra_class,

            escape(alt),

            escape(src),

            escape(alt),

        )

    )



_HERALD_COAT_REL = "images/guide_coat_of_arms.svg"

_HERALD_FLAG_REL = "images/guide_flag.svg"





def _univ_fig_if_exists(

    root: Path,

    rel: str,

    alt: str,

    *,

    dark_bg: bool = False,

    large_logo: bool = False,

) -> str:

    path = root / rel.replace("\\", "/")

    if not path.is_file():

        return ""

    src = "../{}".format(rel.lstrip("/").replace("\\", "/"))

    img_class = "heraldry-univ-img"

    if dark_bg:

        img_class += " heraldry-univ-img--on-dark"

    if large_logo:

        img_class += " heraldry-univ-img--large"

    cell_class = "heraldry-univ-cell"
    if large_logo:
        cell_class += " heraldry-univ-cell--large"

    return (

        '<div class="{}">'

        '<figure class="heraldry-fig heraldry-univ" title="{}">'

        '<img class="{}" src="{}" alt="{}"/>'

        '<figcaption class="heraldry-univ-caption">{}</figcaption>'

        "</figure></div>"

    ).format(

        cell_class,

        escape(alt),

        img_class,

        escape(src),

        escape(alt),

        escape(alt),

    )





def moscow_heraldry_html(

    root: Path,

    title_symbols_class: str,

    edition: str,

) -> str:

    """Three title strips after OTIUM (historical, official, universities)."""

    if edition == "ru":

        aria = "Гербы, флаг и вузы Москвы"

        motto = "Столица Российской Федерации"

        official_lbl = "Символика города (нынешний герб и флаг)"

        univ_lbl = "Ведущие вузы Москвы"

        coat_alt = "Герб Москвы"

        flag_alt = "Флаг Москвы"

        herald_label = HERALDRY_CHAPTER_LABEL_RU

    else:

        aria = "Coats of arms, flag, and universities of Moscow"

        motto = "Capital of the Russian Federation"

        official_lbl = "City symbols (current coat of arms and flag)"

        univ_lbl = "Major universities of Moscow"

        coat_alt = "Coat of arms of Moscow"

        flag_alt = "Flag of Moscow"

        herald_label = HERALDRY_CHAPTER_LABEL_EN



    chunks: list[str] = [

        '<div class="{}" aria-label="{}">'.format(

            title_symbols_class,

            escape(aria),

        ),

        '<p class="title-strip-label">{}</p>'.format(escape(herald_label)),

        '<div class="heraldry-strip heraldry-history">',

    ]

    for rel, alt in moscow_history_coats(edition):

        fig = _fig_if_exists(root, rel, alt, "heraldry-coat-hist")

        if fig:

            chunks.append(fig)

    chunks.append("</div>")

    chunks.append(

        '<div class="heraldry-motto">'

        '<p class="motto-line">{}</p>'

        "</div>".format(escape(motto))

    )

    chunks.append(

        '<p class="title-strip-label">{}</p>'.format(escape(official_lbl))

    )

    chunks.append('<div class="heraldry-strip heraldry-official">')

    coat_candidates = (

        _HERALD_COAT_REL,

        "images/title_msk_moscow_coat_soviet.svg",

    )

    for rel in coat_candidates:

        fig = _fig_if_exists(root, rel, coat_alt, "heraldry-coat-book")

        if fig:

            chunks.append(fig)

            break

    flag_fig = _fig_if_exists(

        root,

        _HERALD_FLAG_REL,

        flag_alt,

        "heraldry-flag-book",

    )

    if flag_fig:

        chunks.append(flag_fig)

    chunks.append("</div>")

    chunks.append(

        '<p class="title-strip-label">{}</p>'.format(escape(univ_lbl))

    )

    chunks.append('<div class="heraldry-strip heraldry-universities">')

    for rel, alt, dark_bg, large_logo in moscow_universities(edition):

        fig = _univ_fig_if_exists(
            root,
            rel,
            alt,
            dark_bg=dark_bg,
            large_logo=large_logo,
        )

        if fig:

            chunks.append(fig)

    chunks.append("</div></div>")

    return "\n".join(chunks)

