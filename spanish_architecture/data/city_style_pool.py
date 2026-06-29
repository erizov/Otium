# -*- coding: utf-8 -*-
"""Map style chapters to city-guide place slugs."""

from __future__ import annotations

CITY_STYLE_POOL: dict[str, list[tuple[str, str]]] = {
    "roman_hispania": [("madrid", "madrid_almudena_cathedral"), ("madrid", "madrid_cybeles_palace_madrid"), ("barcelona", "barcelona_santa_maria_del_mar"), ("lisbon", "lisbon_carmo_convent"), ("lisbon", "lisbon_miradouro_senhora_monte"), ("lisbon", "lisbon_se_cathedral")],
    "visigothic": [],
    "islamic_iberia": [("madrid", "madrid_atocha"), ("madrid", "madrid_las_ventas"), ("barcelona", "barcelona_palau_guell"), ("barcelona", "barcelona_llotja_de_la_mar_barcelona"), ("lisbon", "lisbon_sao_jorge_castle"), ("lisbon", "lisbon_campo_pequeno")],
    "mudejar": [("madrid", "madrid_plaza_de_espana_madrid")],
    "romanesque": [("madrid", "madrid_santiago_bernabeu")],
    "catalan_gothic": [("barcelona", "barcelona_santa_maria_del_pi"), ("lisbon", "lisbon_padrao_descobrimentos")],
    "isabelline_gothic": [],
    "manuelin": [("lisbon", "lisbon_tower_belem"), ("lisbon", "lisbon_jeronimos_monastery"), ("lisbon", "lisbon_palacio_belem")],
    "plateresque": [],
    "herrerian": [("madrid", "madrid_fountain_cibeles")],
    "spanish_baroque": [],
    "churrigueresque": [],
    "portuguese_baroque": [("lisbon", "lisbon_rossio")],
    "neoclassicism": [("madrid", "madrid_museo_del_prado"), ("madrid", "madrid_royal_palace_madrid"), ("madrid", "madrid_puerta_de_alcala"), ("madrid", "madrid_gran_via_madrid"), ("madrid", "madrid_plaza_de_oriente"), ("madrid", "madrid_sorolla_museum"), ("madrid", "madrid_museo_cerralbo"), ("madrid", "madrid_zarzuela_theatre"), ("madrid", "madrid_plaza_de_cibeles_fountain"), ("barcelona", "barcelona_columbus_monument"), ("barcelona", "barcelona_arc_de_triomf"), ("barcelona", "barcelona_mnac_palau_nacional"), ("lisbon", "lisbon_estrela_basilica")],
    "eclectic_historicism": [("madrid", "madrid_puerta_del_sol"), ("barcelona", "barcelona_cathedral"), ("barcelona", "barcelona_barceloneta_beach"), ("barcelona", "barcelona_parc_de_la_ciutadella"), ("barcelona", "barcelona_placa_catalunya"), ("barcelona", "barcelona_sagrat_cor_tibidabo"), ("barcelona", "barcelona_basilica_de_la_merce"), ("barcelona", "barcelona_parc_del_laberint")],
    "catalan_modernisme": [("barcelona", "barcelona_sagrada_familia"), ("barcelona", "barcelona_park_guell"), ("barcelona", "barcelona_casa_batllo"), ("barcelona", "barcelona_casa_mila"), ("barcelona", "barcelona_palau_de_la_musica")],
    "portuguese_art_nouveau": [],
    "rationalist_interwar": [],
    "franco_estado_novo": [],
    "postwar_modern": [("madrid", "madrid_edificio_metropolis")],
    "contemporary": [("madrid", "madrid_museo_thyssen"), ("madrid", "madrid_museo_reina_sofia"), ("madrid", "madrid_caixaforum_madrid"), ("barcelona", "barcelona_torre_glories"), ("barcelona", "barcelona_hotel_w_barcelona"), ("lisbon", "lisbon_maat")],
}
