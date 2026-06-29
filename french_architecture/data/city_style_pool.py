# -*- coding: utf-8 -*-
"""Map style chapters to city-guide place slugs."""

from __future__ import annotations

CITY_STYLE_POOL: dict[str, list[tuple[str, str]]] = {
    "gallo_roman": [("paris", "paris_bois_de_vincennes_lake"), ("paris", "paris_landmark")],
    "romanesque": [("paris", "paris_musee_cluny")],
    "early_gothic": [("paris", "paris_notre_dame_cathedral"), ("paris", "paris_sainte_chapelle"), ("paris", "paris_hotel_de_ville_paris"), ("paris", "paris_conciergerie"), ("paris", "paris_hotel_de_sens")],
    "rayonnant_flamboyant": [],
    "french_renaissance": [("paris", "paris_pont_neuf"), ("paris", "paris_place_des_vosges")],
    "classical_louis_xiii": [("paris", "paris_arc_de_triomphe"), ("paris", "paris_place_de_la_concorde"), ("paris", "paris_hotel_des_invalides"), ("paris", "paris_pantheon_paris"), ("paris", "paris_parc_monceau"), ("paris", "paris_musee_carnavalet")],
    "louis_xiv_classicism": [("paris", "paris_champs_elysees"), ("paris", "paris_jardin_du_luxembourg"), ("paris", "paris_place_vendome")],
    "regency_rococo": [],
    "louis_xv_rococo": [],
    "louis_xvi_neoclassical": [("paris", "paris_pere_lachaise_cemetery")],
    "revolution_empire": [],
    "restoration_july_monarchy": [],
    "second_empire": [("paris", "paris_pont_alexandre_iii")],
    "haussmann": [("paris", "paris_palais_garnier")],
    "belle_epoque": [],
    "art_nouveau": [("paris", "paris_eiffel_tower")],
    "art_deco_interwar": [("paris", "paris_pavillon_de_flore")],
    "modernism_lecorbusier": [("paris", "paris_cite_des_sciences"), ("paris", "paris_institut_du_monde_arabe")],
    "brutalism": [],
    "grands_projets": [("paris", "paris_centre_pompidou")],
    "contemporary": [("paris", "paris_louvre"), ("paris", "paris_pont_des_arts")],
}
