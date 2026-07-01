# -*- coding: utf-8 -*-
"""Map style chapters to city-guide place slugs."""

from __future__ import annotations

CITY_STYLE_POOL: dict[str, list[tuple[str, str]]] = {
    "roman_germania": [("berlin", "berlin_pergamon_museum")],
    "romanesque": [],
    "gothic": [("berlin", "berlin_reichstag"), ("berlin", "berlin_cathedral"), ("berlin", "berlin_kaiser_wilhelm_memorial_church"), ("berlin", "berlin_nikolaikirche_berlin"), ("berlin", "berlin_berliner_dom"), ("vienna", "vienna_stephansdom"), ("vienna", "vienna_karlskirche"), ("vienna", "vienna_rathaus_vienna"), ("vienna", "vienna_austrian_parliament"), ("vienna", "vienna_ruprechtskirche_vienna")],
    "renaissance": [("berlin", "berlin_bode_museum"), ("berlin", "berlin_oberbaum_bridge"), ("berlin", "berlin_rotes_rathaus"), ("vienna", "vienna_hofburg_vienna"), ("vienna", "vienna_state_opera")],
    "baroque": [("berlin", "berlin_charlottenburg_palace"), ("berlin", "berlin_humboldt_forum_berlin"), ("vienna", "vienna_schoenbrunn_palace"), ("vienna", "vienna_belvedere_vienna"), ("vienna", "vienna_spanish_riding_school"), ("vienna", "vienna_maria_theresien_denkmal"), ("vienna", "vienna_kunsthistorisches_museum"), ("vienna", "vienna_stephansplatz"), ("vienna", "vienna_ankeruhr_vienna"), ("vienna", "vienna_spanische_hofreitschule_facade")],
    "rococo": [],
    "neoclassicism": [("berlin", "berlin_brandenburg_gate"), ("berlin", "berlin_gendarmenmarkt"), ("berlin", "berlin_potsdamer_platz"), ("berlin", "berlin_victory_column"), ("berlin", "berlin_bellevue_palace"), ("berlin", "berlin_deutsches_historisches_museum"), ("berlin", "berlin_berlinische_galerie"), ("berlin", "berlin_museum_fuer_naturkunde_berlin")],
    "historicism": [],
    "art_nouveau": [("berlin", "berlin_hauptbahnhof"), ("vienna", "vienna_museumsquartier")],
    "modernism": [("berlin", "berlin_alexanderplatz_tv_tower"), ("berlin", "berlin_soviet_memorial_treptow"), ("vienna", "vienna_donauturm"), ("vienna", "vienna_freud_memorial"), ("vienna", "vienna_judenplatz_holocaust_memorial"), ("vienna", "vienna_technisches_museum_wien")],
    "bauhaus": [],
    "expressionism": [],
    "nazi_monumental": [("berlin", "berlin_futurium_berlin"), ("berlin", "berlin_tempelhofer_feld")],
    "postwar_modern": [],
    "brutalism": [],
    "contemporary": [("berlin", "berlin_holocaust_memorial"), ("berlin", "berlin_jewish_museum_berlin"), ("vienna", "vienna_haus_der_musik_wien")],
}
