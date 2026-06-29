# -*- coding: utf-8 -*-
"""Explicit image URLs for guide places."""

from __future__ import annotations

from typing import Any

IMAGE_URL_OVERRIDES: dict[str, tuple[str, str | None]] = {
    "catalan_gothic_manresa": (
        "https://upload.wikimedia.org/wikipedia/commons/d/d4/"
        "PM_146709n_E_Manresa.jpg",
        None,
    ),
    "roman_hispania_bridge_alcantara": (
        "https://upload.wikimedia.org/wikipedia/commons/1/14/"
        "Puente_de_Alc%C3%A1ntara%2C_C%C3%A1ceres_Province%2C_Spain."
        "_Pic_02.jpg",
        None,
    ),
    "roman_hispania_italica": (
        "https://upload.wikimedia.org/wikipedia/commons/3/33/"
        "Anfiteatro_de_las_ruinas_romanas_de_It%C3%A1lica%2C_Santiponce"
        "%2C_Sevilla%2C_Espa%C3%B1a%2C_2015-12-06%2C_DD_34-45_PAN_HDR.JPG",
        None,
    ),
    "visigothic_vega_del_mar": (
        "https://upload.wikimedia.org/wikipedia/commons/2/2a/"
        "Bas%C3%ADlica_Paleocristiana_de_Vega_del_Mar.JPG",
        None,
    ),
    "visigothic_santa_lucia": (
        "https://upload.wikimedia.org/wikipedia/commons/e/e4/"
        "Santa_Luc%C3%ADa_de_El_Trampal.jpg",
        None,
    ),
    "islamic_iberia_alhambra": (
        "https://upload.wikimedia.org/wikipedia/commons/c/cf/"
        "Alhambra_evening_panorama_Mirador_San_Nicolas_sRGB-1.jpg",
        None,
    ),
    "islamic_iberia_comares": (
        "https://upload.wikimedia.org/wikipedia/commons/c/cb/"
        "Alhambra_Comares_Hall_%28R_Prazeres%29_DSCF6579.jpg",
        None,
    ),
    "islamic_iberia_medina_azahara": (
        "https://upload.wikimedia.org/wikipedia/commons/1/19/"
        "Sal%C3%B3n_Rico_-_Medina_Azahara%2C_C%C3%B3rdoba_%282%29.jpg",
        None,
    ),
    "islamic_iberia_mezquita_cordoba": (
        "https://upload.wikimedia.org/wikipedia/commons/4/4a/"
        "Mezquita_cordoba_arco_interior.jpg",
        None,
    ),
    "islamic_iberia_torre_del_oro": (
        "https://upload.wikimedia.org/wikipedia/commons/4/4a/"
        "Gold_Tower_Guadalquivir_Seville_Tower_Arabic.jpg",
        None,
    ),
    "mudejar_teruel_towers": (
        "https://upload.wikimedia.org/wikipedia/commons/b/b9/"
        "Iglesia_de_San_Mart%C3%ADn%2C_Teruel._Torre.jpg",
        None,
    ),
    "romanesque_san_isidoro": (
        "https://upload.wikimedia.org/wikipedia/commons/8/88/"
        "Igrexa_de_San_Isidoro_de_Le%C3%B3n._Praza_de_San_Isidoro."
        "_Espa%C3%B1a-18.jpg",
        None,
    ),
    "romanesque_santo_domingo_silos": (
        "https://upload.wikimedia.org/wikipedia/commons/d/d7/"
        "Monasterio_de_Santo_Domingo_de_Silos_%28Burgos%29._Entrada.jpg",
        None,
    ),
    "romanesque_santiago": (
        "https://upload.wikimedia.org/wikipedia/commons/4/45/"
        "2025_Facade_towers_of_the_Cathedral_of_Santiago_from_the_"
        "Garden_of_the_Speaking_Stones._Galicia.jpg",
        None,
    ),
    "catalan_gothic_llotja_mar": (
        "https://upload.wikimedia.org/wikipedia/commons/f/fa/"
        "Recreation_of_1st_daguerreotype_in_Spain_-1839-_casa_Xifre_"
        "and_Llotja_de_Mar_-Barcelona.jpg",
        None,
    ),
    "catalan_gothic_santa_maria_mar": (
        "https://upload.wikimedia.org/wikipedia/commons/b/ba/"
        "Main_facade_-_Bas%C3%ADlica_de_Santa_Maria_del_Mar_-_"
        "Barcelona_2014.jpg",
        None,
    ),
    "catalan_gothic_barcelona_cathedral": (
        "https://upload.wikimedia.org/wikipedia/commons/3/3e/"
        "Catedral_de_la_Santa_Cruz_y_Santa_Eulalia_--_2019_--_"
        "Barcelona%2C_Espa%C3%B1a.jpg",
        None,
    ),
    "catalan_gothic_girona_cathedral": (
        "https://upload.wikimedia.org/wikipedia/commons/9/97/"
        "Cathedral_of_Girona_%282%29.jpg",
        None,
    ),
    "isabelline_gothic_san_gregorio": (
        "https://upload.wikimedia.org/wikipedia/commons/d/da/"
        "Valladolid_-_Colegio_de_San_Gregorio%2C_portada_15.jpg",
        None,
    ),
    "isabelline_gothic_san_pablo_valladolid": (
        "https://upload.wikimedia.org/wikipedia/commons/4/4e/"
        "Valladolid_-_San_Pablo_20200221a.jpg",
        None,
    ),
    "manuelin_evora_manueline": (
        "https://upload.wikimedia.org/wikipedia/commons/9/9b/"
        "Castelo_de_%C3%89vora.jpg",
        None,
    ),
    "manuelin_porto_silva": (
        "https://upload.wikimedia.org/wikipedia/commons/d/d8/"
        "South_fa%C3%A7ade_of_Igreja_de_S%C3%A3o_Francisco_%28Porto%29.jpg",
        None,
    ),
    "herrerian_villa_magna": (
        "https://upload.wikimedia.org/wikipedia/commons/b/b0/"
        "Valladolid_-_Museo_Patio_Herreriano_de_Arte_Contempor%C3%A1neo_"
        "Espa%C3%B1ol_30.jpg",
        None,
    ),
    "spanish_baroque_tavera": (
        "https://upload.wikimedia.org/wikipedia/commons/6/68/"
        "Toledo_-_Palacio_de_Tavera_-_Fachada.JPG",
        None,
    ),
    "portuguese_baroque_clerigos": (
        "https://upload.wikimedia.org/wikipedia/commons/c/cf/"
        "Exterior_view_of_Igreja_dos_Cl%C3%A9rigos_10.jpg",
        None,
    ),
    "portuguese_baroque_raio": (
        "https://upload.wikimedia.org/wikipedia/commons/b/be/"
        "Main_facade_of_Pal%C3%A1cio_do_Raio_02-cropped.jpg",
        None,
    ),
    "neoclassicism_royal_palace": (
        "https://upload.wikimedia.org/wikipedia/commons/d/da/"
        "Royal_Palace_of_Madrid_east_facade_1.jpg",
        None,
    ),
    "neoclassicism_puerta_alcala": (
        "https://upload.wikimedia.org/wikipedia/commons/c/c6/"
        "Puerta_de_Alcal%C3%A1_-_2008.jpg",
        None,
    ),
    "eclectic_historicism_metropolis": (
        "https://upload.wikimedia.org/wikipedia/commons/e/ec/"
        "Edificio_Metr%C3%B3polis%2C_calle_de_Alcal%C3%A1%2C_Madrid%2C_"
        "Espa%C3%B1a%2C_2017-05-18%2C_DD_08.jpg",
        None,
    ),
    "eclectic_historicism_palacio_cristal": (
        "https://upload.wikimedia.org/wikipedia/commons/a/a5/"
        "Palacio_de_Cristal_-_01.jpg",
        None,
    ),
    "catalan_modernisme_casa_punxes": (
        "https://upload.wikimedia.org/wikipedia/commons/8/87/"
        "Casa_de_les_Punxes_-_001.jpg",
        None,
    ),
    "catalan_modernisme_sagrada_familia": (
        "https://upload.wikimedia.org/wikipedia/commons/0/08/"
        "Sagrada_Familia_March_2015-14a.jpg",
        None,
    ),
    "portuguese_art_nouveau_palacio_sereias": (
        "https://upload.wikimedia.org/wikipedia/commons/8/8f/"
        "Pal%C3%A1cio_Foz_2012.jpg",
        None,
    ),
    "portuguese_art_nouveau_serralves_early": (
        "https://upload.wikimedia.org/wikipedia/commons/4/42/"
        "Casa_de_Serralves_4.jpg",
        None,
    ),
    "rationalist_interwar_casa_junceda": (
        "https://upload.wikimedia.org/wikipedia/commons/c/c7/"
        "12_Dispensari_antitubercul%C3%B3s%2C_pati.jpg",
        None,
    ),
    "rationalist_interwar_casa_flores": (
        "https://upload.wikimedia.org/wikipedia/commons/9/9e/"
        "Madrilgo_Casa_de_las_Flores%2C_Secundino_Zuazo%2C_1930-32.jpg",
        None,
    ),
    "rationalist_interwar_club_union": (
        "https://upload.wikimedia.org/wikipedia/commons/0/07/"
        "La_Uni%C3%B3n_y_el_F%C3%A9nix_Espa%C3%B1ol_building_and_Church_"
        "of_the_Calatravas.jpg",
        None,
    ),
    "postwar_modern_benidorm": (
        "https://upload.wikimedia.org/wikipedia/commons/d/da/"
        "Intempo_and_Sunset_Drive_from_Ermita_de_la_Virgen_del_Mar%2C_"
        "Benidorm%2C_Alicante%2C_Spain%2C_2024_January_-_2.jpg",
        None,
    ),
    "contemporary_w_barcelona": (
        "https://upload.wikimedia.org/wikipedia/commons/a/a3/"
        "Barcelona_-_Rambla_del_Mar_-_View_SE_on_%22The_Sail%22%2C_"
        "Architect_Ricardo_Bofill%27s_%27Taller_de_Arquitectura_W_"
        "Barcelona_Hotel%27_of_2009.jpg",
        None,
    ),
    # Break duplicate image hashes (same bytes, different places).
    "herrerian_segovia_bridge": (
        "https://upload.wikimedia.org/wikipedia/commons/d/d2/"
        "Viaducto_de_Segovia.jpg",
        None,
    ),
    "manuelin_jeronimos": (
        "https://upload.wikimedia.org/wikipedia/commons/4/40/"
        "Cloister_of_the_Jer%C3%B3nimos_Monastery_in_Bel%C3%A9m%2C_"
        "Lisbon%2C_20250604_1313_9204.jpg",
        None,
    ),
    "plateresque_casa_consistorial": (
        "https://upload.wikimedia.org/wikipedia/commons/e/e0/"
        "Plaza_Mayor_-_Casa_Consistorial_%28Salamanca%29.jpg",
        None,
    ),
    "herrerian_moncloa": (
        "https://upload.wikimedia.org/wikipedia/commons/f/f9/"
        "Palacio_de_la_Moncloa_%28Madrid%29_01.jpg",
        None,
    ),
    "rationalist_interwar_telefonica": (
        "https://upload.wikimedia.org/wikipedia/commons/9/9f/"
        "Telef%C3%B3nica_-_Gran_V%C3%ADa_28_-_Madrid.jpg",
        None,
    ),
    "contemporary_caixaforum": (
        "https://upload.wikimedia.org/wikipedia/commons/9/97/"
        "Plaza_-_CaixaForum_Madrid_01.jpg",
        None,
    ),
    "contemporary_forum_barcelona": (
        "https://upload.wikimedia.org/wikipedia/commons/e/e2/"
        "Edifici_F%C3%B2rum_Barcelona_Catalonia.jpg",
        None,
    ),
    "visigothic_santa_comba": (
        "https://upload.wikimedia.org/wikipedia/commons/b/b2/"
        "Church_of_Santa_Comba_de_Bande._2011.jpg",
        None,
    ),
    "churrigueresque_valladolid_univ": (
        "https://upload.wikimedia.org/wikipedia/commons/1/16/"
        "Universidad_de_Valladolid._Fachada.jpg",
        None,
    ),
    "portuguese_art_nouveau_medeiros_almeida": (
        "https://upload.wikimedia.org/wikipedia/commons/b/b7/"
        "Casa_Museu_Ant%C3%B3nio_Medeiros_e_Almeida.jpg",
        None,
    ),
    "franco_estado_novo_ministerio_aire": (
        "https://upload.wikimedia.org/wikipedia/commons/2/20/"
        "Ministerio_del_Aire_%28Madrid%29_01.jpg",
        None,
    ),
    "postwar_modern_chamartin": (
        "https://upload.wikimedia.org/wikipedia/commons/c/cd/"
        "Madrid_chamartin.jpg",
        None,
    ),
    "contemporary_city_arts": (
        "https://upload.wikimedia.org/wikipedia/commons/d/d6/"
        "Museo_Pr%C3%ADncipe_Felipe%2C_Ciudad_de_las_Artes_y_las_Ciencias%2C_"
        "Valencia%2C_Espa%C3%B1a%2C_2014-06-29%2C_DD_59.JPG",
        None,
    ),
    "contemporary_ciudad_cultura": (
        "https://upload.wikimedia.org/wikipedia/commons/1/18/"
        "2011-08-17_Cidade_da_Cultura._Santiago_de_Compostela-C16.jpg",
        None,
    ),
    "islamic_iberia_banos_magdalena": (
        "https://upload.wikimedia.org/wikipedia/commons/d/d8/"
        "Ba%C3%B1os_califales_-_C%C3%B3rdoba.jpg",
        None,
    ),
    "visigothic_san_juan_banos": (
        "https://upload.wikimedia.org/wikipedia/commons/3/3a/"
        "San_Juan_de_Ba%C3%B1os.jpg",
        None,
    ),
    "portuguese_baroque_queluz": (
        "https://upload.wikimedia.org/wikipedia/commons/a/af/"
        "Pal%C3%A1cio_Nacional_de_Queluz_DSC04937_-_QUELUZ_%2832558819844%29.jpg",
        None,
    ),
    "portuguese_baroque_mercy_porto": (
        "https://upload.wikimedia.org/wikipedia/commons/7/78/"
        "Igreja_da_Miseric%C3%B3rdia_do_Porto.jpg",
        None,
    ),
    "neoclassicism_prado": (
        "https://upload.wikimedia.org/wikipedia/commons/0/04/"
        "East_facade_of_the_Cas%C3%B3n_del_Buen_Retiro%2C_Museo_del_Prado%2C_"
        "Madrid.jpg",
        None,
    ),
    "neoclassicism_teatro_real": (
        "https://upload.wikimedia.org/wikipedia/commons/0/0e/"
        "Teatro_Real_de_Madrid_-_02.jpg",
        None,
    ),
    "catalan_modernisme_casa_mila": (
        "https://upload.wikimedia.org/wikipedia/commons/5/55/"
        "Barcelona_-_Passeig_de_Gr%C3%A0cia_-_Casa_Mil%C3%A0_-_View_up_close_"
        "to_the_fa%C3%A7ade.jpg",
        None,
    ),
    "catalan_modernisme_park_guell": (
        "https://upload.wikimedia.org/wikipedia/commons/c/cb/"
        "Park_G%C3%BCell_02.jpg",
        None,
    ),
    "franco_estado_novo_valle_caidos": (
        "https://upload.wikimedia.org/wikipedia/commons/6/6e/"
        "SPA-2014-San_Lorenzo_de_El_Escorial-Valley_of_the_Fallen_%28Valle_de_"
        "los_Ca%C3%ADdos%29.jpg",
        None,
    ),
    "postwar_modern_barceloneta_hotels": (
        "https://upload.wikimedia.org/wikipedia/commons/6/6f/"
        "Promenade_and_beach%2C_Platja_de_la_Barceloneta%2C_Barcelona%2C_"
        "2015.jpg",
        None,
    ),
    "contemporary_congress_madrid": (
        "https://upload.wikimedia.org/wikipedia/commons/d/db/"
        "Palacio_de_Congresos_y_Exposiciones_%28Madrid%29_01.jpg",
        None,
    ),
    "contemporary_maat": (
        "https://upload.wikimedia.org/wikipedia/commons/a/a5/"
        "Building_of_the_Museum_of_Art%2C_Architecture_and_Technology_in_"
        "Lisbon%2C_20250604_2006_9600.jpg",
        None,
    ),
    "mudejar_aljaferia_mudejar": (
        "https://upload.wikimedia.org/wikipedia/commons/c/c7/"
        "Palacio_de_la_Aljafer%C3%ADa.jpg",
        None,
    ),
    "plateresque_salamanca_univ": (
        "https://upload.wikimedia.org/wikipedia/commons/f/f8/"
        "Salamanca_016.jpg",
        None,
    ),
    "churrigueresque_cartuja_sacristy": (
        "https://upload.wikimedia.org/wikipedia/commons/f/ff/"
        "Fachada_del_Monasterio_de_la_Cartuja_de_Granada.jpg",
        None,
    ),
    "catalan_modernisme_bellesguard": (
        "https://upload.wikimedia.org/wikipedia/commons/a/a3/"
        "Barcelona_-_Carrer_de_Bellesguard_-_View_NNE_on_Entrance_Gate_to_"
        "Torre_de_Bellesguard_%28Casa_Figueras%29_1900-09_by_Antoni_Gaud%C3%AD.jpg",
        None,
    ),
    "catalan_modernisme_casa_vicens": (
        "https://upload.wikimedia.org/wikipedia/commons/9/9c/"
        "Barcelona%2C_casa_Vicens_%28Antoni_Gaud%C3%AD%29_balc%C3%B3n.jpg",
        None,
    ),
    "mudejar_san_martin_toledo": (
        "https://lh5.googleusercontent.com/p/"
        "AF1QipOCEPTOnMNFcIJ7VlVorSX1s47UFAsPI6FTX-MR=w800-h1020-k-no",
        None,
    ),
    "romanesque_jaca": (
        "https://upload.wikimedia.org/wikipedia/commons/8/86/"
        "Jaca%2C_Catedral_de_San_Pedro-PM_32162.jpg",
        None,
    ),
    "neoclassicism_lisbon_academy": (
        "https://upload.wikimedia.org/wikipedia/commons/b/b6/"
        "Largo-da-Academia-das-Belas-artes-1918-Escola-Superior-de-Belas-"
        "Artes-de-Lisboa-fachada.jpg",
        None,
    ),
    "rationalist_interwar_nautical_club": (
        "https://upload.wikimedia.org/wikipedia/commons/1/1b/"
        "Reial_Club_Mar%C3%ADtim_de_Barcelona.jpg",
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
