# -*- coding: utf-8 -*-
"""Explicit image URLs for guide places."""

from __future__ import annotations

from typing import Any

IMAGE_URL_OVERRIDES: dict[str, tuple[str, str | None]] = {
    "norman_sicilian_cefalu": (
        "https://upload.wikimedia.org/wikipedia/commons/a/a5/"
        "Cefalu_Cathedral_exterior_BW_2012-10-11_12-13-18.jpg",
        None,
    ),
    "mannerism_cappella_pauline": (
        "https://upload.wikimedia.org/wikipedia/commons/6/64/"
        "Dome_of_Cappella_Paolina_in_Santa_Maria_Maggiore_%28Rome%29.jpg",
        None,
    ),
    "mannerism_orvieto_well": (
        "https://upload.wikimedia.org/wikipedia/commons/9/9c/"
        "Pozzo_di_San_Patrizio_Oriveto.JPG",
        None,
    ),
    "mannerism_palazzo_binder": (
        "https://upload.wikimedia.org/wikipedia/commons/1/19/"
        "Palazzo_bindi-sergardi_01.JPG",
        None,
    ),
    "mannerism_santa_maria_novella": (
        "https://upload.wikimedia.org/wikipedia/commons/b/bc/"
        "Plaza_de_Santa_Mar%C3%ADa_Novella%2C_Florencia%2C_Italia%2C_"
        "2022-09-19%2C_DD_44.jpg",
        None,
    ),
    "palladian_venetian_venice_arsenale_2": (
        "https://upload.wikimedia.org/wikipedia/commons/2/28/"
        "Arsenale_%28Venice%29_-_The_Lion_of_Venice_on_the_pediment_"
        "of_the_arsenal.jpg",
        None,
    ),
    "baroque_rome_villa_borghese_2": (
        "https://upload.wikimedia.org/wikipedia/commons/f/f5/"
        "Templo_de_Asclepio%2C_Villa_Borghese%2C_Roma%2C_Italia%2C_"
        "2022-09-14%2C_DD_12.jpg",
        None,
    ),
    "sicilian_baroque_duomo_modica": (
        "https://upload.wikimedia.org/wikipedia/commons/a/aa/"
        "Cathedral_of_San_Giorgio_Modica%2C_Duomo_di_San_Giorgio%2C_"
        "Sicily_Sicilia_Italy_in_1992.jpg",
        None,
    ),
    "neoclassicism_florence_mercato_centrale_2": (
        "https://upload.wikimedia.org/wikipedia/commons/a/ab/"
        "Via_dell%27ariento%2C_mercato_centrale_01.jpg",
        None,
    ),
    "neoclassicism_florence_piazza_massimo_azeglio_2": (
        "https://upload.wikimedia.org/wikipedia/commons/6/6c/"
        "Firenze_-_Florence_-_Piazza_Massimo_d%27Azeglio_-_View_South.jpg",
        None,
    ),
    "romantic_eclectic_stazione_milano": (
        "https://upload.wikimedia.org/wikipedia/commons/6/60/"
        "Upper_front_facade_of_Milano_Stazione_Centrale.jpg",
        None,
    ),
    "romantic_eclectic_galleria_umberto": (
        "https://upload.wikimedia.org/wikipedia/commons/f/fa/"
        "Galleria_Umberto_I_Naples_n01.jpg",
        None,
    ),
    "liberty_villino_idale": (
        "https://upload.wikimedia.org/wikipedia/commons/e/ec/"
        "9028_-_Milano%2C_C.so_Venezia_-_Giuseppe_Sommaruga%2C_Pal."
        "_Castiglioni_%281904%29_-_Foto_Giovanni_Dall%27Orto_22-Apr-2007.jpg",
        None,
    ),
    "liberty_palazzo_exhibition": (
        "https://upload.wikimedia.org/wikipedia/commons/a/a7/"
        "Palazzo_delle_Esposizioni_%28Rome%29.jpg",
        None,
    ),
    "liberty_casa_fiorita": (
        "https://upload.wikimedia.org/wikipedia/commons/7/7d/"
        "Torino_Casa_Fenoglio-Lafleur.jpg",
        None,
    ),
    "rationalism_palazzo_justice": (
        "https://upload.wikimedia.org/wikipedia/commons/e/e9/"
        "Il_Palazzo_di_Giustizia_di_Milano%2C_sede_del_Tribunale%2C_"
        "opera_di_Marcello_Piacentini.jpg",
        None,
    ),
    "fascist_rationalism_mattatoio": (
        "https://upload.wikimedia.org/wikipedia/commons/0/08/"
        "Mattatoio_Testaccio_%28Rome%29_10.jpg",
        None,
    ),
    "fascist_rationalism_eur": (
        "https://upload.wikimedia.org/wikipedia/commons/2/22/"
        "EUR_Piazza_Guglielmo_Marconi.jpg",
        None,
    ),
    "postwar_modern_pirelli": (
        "https://upload.wikimedia.org/wikipedia/commons/f/f4/"
        "Mi-Milano-1959-Grattacielo-Pirelli-01.jpg",
        None,
    ),
    "brutalism_san_giovanni_bosco": (
        "https://upload.wikimedia.org/wikipedia/commons/5/51/"
        "Chiesa_di_San_Giovanni_Bosco_%28Torino%29_%281%29.jpg",
        None,
    ),
    "brutalism_university_cagliari": (
        "https://upload.wikimedia.org/wikipedia/commons/7/7f/"
        "Biblioteca_Facolt%C3%A0_di_Ingegneria%2C_Universit%C3%A0_"
        "degli_studi_di_Cagliari.jpg",
        None,
    ),
    "brutalism_church_longarone": (
        "https://upload.wikimedia.org/wikipedia/commons/9/91/"
        "Longarone_%28BL%29_-_chiesa_di_Santa_Maria_Immacolata.jpg",
        None,
    ),
    "postwar_modern_church_autostrada": (
        "https://upload.wikimedia.org/wikipedia/commons/4/42/"
        "Chiesa_dell%27Autostrada_del_Sole%2C_vista_dall%27autostrada.jpg",
        None,
    ),
    "brutalism_church_autostrada_brut": (
        "https://upload.wikimedia.org/wikipedia/commons/2/2f/"
        "Chiesa_dell%27Autostrada_del_Sole%2C_vista_dal_ponte.jpg",
        None,
    ),
    "postmodern_tendenza_museum_modena": (
        "https://upload.wikimedia.org/wikipedia/commons/c/cc/"
        "Palazzo_Santa_Margherita%2C_Modena.jpg",
        None,
    ),
    "contemporary_venice_giardini_biennale_2": (
        "https://upload.wikimedia.org/wikipedia/commons/4/41/"
        "Venezia_-_Giardini_della_Biennale%2C_padiglione_italiano_-_"
        "Foto_di_Paolo_Steffan.jpg",
        None,
    ),
    "liberty_villa_necchi": (
        "https://upload.wikimedia.org/wikipedia/commons/c/c0/"
        "Villa_Necchi%2C_Milan%2C_Italy.jpg",
        None,
    ),
    "liberty_stazione_napoli": (
        "https://upload.wikimedia.org/wikipedia/commons/1/15/"
        "Napoli_staz_Garibaldi.jpg",
        None,
    ),
    "brutalism_church_resistenza": (
        "https://upload.wikimedia.org/wikipedia/commons/0/00/"
        "WLM-IT_Monumento_Resistenza%2C_Cuneo.jpg",
        None,
    ),
    "postmodern_tendenza_celtic": (
        "https://upload.wikimedia.org/wikipedia/commons/2/27/"
        "N_cubed%2C_by_Tom_de_Paor.jpg",
        None,
    ),
    "contemporary_snfcc": (
        "https://upload.wikimedia.org/wikipedia/commons/0/08/"
        "Roma_-_MAXXI_-_Museo_nazionale_delle_arti_del_XXI_secolo_-_Curve.jpeg",
        None,
    ),
    "postmodern_tendenza_palazzo_italia": (
        "https://upload.wikimedia.org/wikipedia/commons/9/9b/"
        "Italia_Expo_2015.JPG",
        None,
    ),
    "contemporary_porta_nuova": (
        "https://upload.wikimedia.org/wikipedia/commons/1/12/"
        "Milan_skyline_skyscrapers_of_Porta_Nuova_business_district.jpg",
        None,
    ),
    "contemporary_citylife": (
        "https://upload.wikimedia.org/wikipedia/commons/9/9f/"
        "Hadid_Generali_Tower_and_CityLife_Milano_Residental_Complex.jpg",
        None,
    ),
    "postmodern_tendenza_church_resurrection": (
        "https://upload.wikimedia.org/wikipedia/commons/c/cc/"
        "Fonte_battesimale_-_.chiesa_del_Santo_Volto%2C_Turin.jpg",
        None,
    ),
    "high_renaissance_st_peters": (
        "https://upload.wikimedia.org/wikipedia/commons/f/f5/"
        "Basilica_di_San_Pietro_in_Vaticano_September_2015-1a.jpg",
        None,
    ),
    "romantic_eclectic_altare_patria": (
        "https://upload.wikimedia.org/wikipedia/commons/1/1d/"
        "Vittoriano_Altare_della_Patria_2013-09-16.jpg",
        None,
    ),
    "brutalism_convento_annunciata": (
        "https://upload.wikimedia.org/wikipedia/commons/d/d2/"
        "Milan_foggy_panorama_with_Velasca_Tower.jpg",
        None,
    ),
}
PRIMARY_IMAGE_REUSE: dict[str, tuple[str, str]] = {}
SECOND_IMAGE_REUSE: dict[str, tuple[str, str]] = {}


def apply_image_url_overrides(place: dict[str, Any]) -> dict[str, Any]:
    slug = str(place.get("slug") or "")
    override = IMAGE_URL_OVERRIDES.get(slug)
    if not override:
        return place
    primary, secondary = override
    merged = dict(place)
    merged["image_source_url"] = primary
    if secondary:
        merged["additional_images"] = [{
            "image_source_url": secondary,
        }]
    else:
        merged.pop("additional_images", None)
    return merged
