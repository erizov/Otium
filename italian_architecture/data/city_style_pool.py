# -*- coding: utf-8 -*-
"""Map style chapters to city-guide place slugs."""

from __future__ import annotations

CITY_STYLE_POOL: dict[str, list[tuple[str, str]]] = {
    "etruscan_roman": [("rome", "rome_colosseum"), ("rome", "rome_roman_forum"), ("rome", "rome_pantheon"), ("rome", "rome_castel_sant_angelo"), ("rome", "rome_piazza_navona"), ("rome", "rome_capitoline_hill"), ("rome", "rome_trajan_column"), ("rome", "rome_baths_of_caracalla"), ("rome", "rome_ponte_sant_angelo"), ("rome", "rome_bocca_della_verita"), ("rome", "rome_pyramid_of_cestius"), ("rome", "rome_arch_of_constantine"), ("rome", "rome_ara_pacis_museum"), ("rome", "rome_largo_torre_argentina"), ("rome", "rome_via_appia"), ("rome", "rome_piazza_del_popolo"), ("rome", "rome_campo_de_fiori"), ("rome", "rome_basilica_san_paolo_fuori"), ("rome", "rome_mausoleum_of_augustus"), ("rome", "rome_jewish_ghetto_portico_octavia"), ("rome", "rome_testaccio_monte"), ("rome", "rome_basilica_san_clemente"), ("rome", "rome_piazza_del_campidoglio"), ("rome", "rome_palatine_hill"), ("rome", "rome_circus_maximus"), ("rome", "rome_theatre_of_marcellus"), ("rome", "rome_piazza_venezia"), ("rome", "rome_baths_of_diocletian"), ("rome", "rome_catacombs_san_callisto"), ("florence", "florence_ponte_vecchio"), ("florence", "florence_piazzale_michelangelo"), ("florence", "florence_santo_spirito"), ("florence", "florence_san_miniato_al_monte"), ("venice", "venice_ponte_accademia"), ("venice", "venice_campo_san_polo")],
    "early_christian": [("rome", "rome_santa_maria_trastevere"), ("rome", "rome_basilica_santa_maria_maggiore"), ("rome", "rome_san_giovanni_in_laterano"), ("florence", "florence_santa_croce"), ("venice", "venice_piazza_san_marco"), ("venice", "venice_basilica_san_marco"), ("venice", "venice_campanile_san_marco"), ("venice", "venice_san_zaccaria_venice"), ("venice", "venice_santa_maria_dei_miracoli")],
    "romanesque": [],
    "norman_sicilian": [],
    "gothic": [("florence", "florence_duomo"), ("florence", "florence_santa_maria_novella"), ("florence", "florence_orsanmichele"), ("florence", "florence_baptistery"), ("florence", "florence_torre_arnolfo_palazzo_vecchio"), ("venice", "venice_grand_canal"), ("venice", "venice_st_marks_clocktower"), ("venice", "venice_ca_doro"), ("venice", "venice_scuola_grande_san_rocco"), ("venice", "venice_campo_santa_margherita"), ("venice", "venice_san_francesco_della_vigna")],
    "early_renaissance": [("rome", "rome_villa_farnesina"), ("rome", "rome_quirinal_palace"), ("florence", "florence_uffizi"), ("florence", "florence_palazzo_vecchio"), ("florence", "florence_san_lorenzo"), ("florence", "florence_palazzo_pitti"), ("florence", "florence_boboli_gardens"), ("florence", "florence_galleria_accademia"), ("florence", "florence_palazzo_strozzi"), ("florence", "florence_piazza_della_signoria"), ("florence", "florence_museo_galileo"), ("florence", "florence_ponte_santa_trinita"), ("florence", "florence_palazzo_medici_riccardi"), ("florence", "florence_bargello_museum"), ("florence", "florence_casa_buonarroti"), ("florence", "florence_san_marco_museum_florence"), ("florence", "florence_santa_maria_del_carmine"), ("florence", "florence_ognissanti_florence"), ("florence", "florence_basilica_annunziata"), ("florence", "florence_stibbert_museum"), ("florence", "florence_fountain_neptune_florence"), ("venice", "venice_rialto_bridge"), ("venice", "venice_santa_maria_della_salute"), ("venice", "venice_peggy_guggenheim_collection"), ("venice", "venice_burano"), ("venice", "venice_scala_contarini_del_bovolo"), ("venice", "venice_arsenale_gate_land")],
    "high_renaissance": [],
    "mannerism": [],
    "palladian_venetian": [("venice", "venice_doges_palace"), ("venice", "venice_bridge_of_sighs"), ("venice", "venice_biblioteca_marciana"), ("venice", "venice_jewish_museum_venice"), ("venice", "venice_murano"), ("venice", "venice_arsenale"), ("venice", "venice_lido_di_venezia"), ("venice", "venice_san_giorgio_maggiore"), ("venice", "venice_gallerie_accademia"), ("venice", "venice_ca_rezzonico"), ("venice", "venice_santa_maria_formosa"), ("venice", "venice_canton")],
    "baroque": [("rome", "rome_st_peters_basilica"), ("rome", "rome_trevi_fountain"), ("rome", "rome_spanish_steps"), ("rome", "rome_villa_borghese"), ("rome", "rome_palazzo_barberini"), ("rome", "rome_capuchin_crypt_rome"), ("rome", "rome_villa_sciarra"), ("rome", "rome_santa_maria_sopra_minerva"), ("rome", "rome_galleria_borghese")],
    "sicilian_baroque": [],
    "rococo_late_baroque": [],
    "neoclassicism": [("rome", "rome_vittoriano"), ("florence", "florence_mercato_centrale"), ("florence", "florence_piazza_massimo_azeglio"), ("florence", "florence_tuscany_hall_opera"), ("venice", "venice_teatro_la_fenice")],
    "romantic_eclectic": [],
    "liberty": [],
    "rationalism": [],
    "fascist_rationalism": [],
    "postwar_modern": [],
    "brutalism": [],
    "postmodern_tendenza": [],
    "contemporary": [("venice", "venice_giardini_biennale"), ("venice", "venice_punta_della_dogana")],
}
