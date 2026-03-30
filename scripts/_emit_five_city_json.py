# -*- coding: utf-8 -*-
"""One-off: write vienna/boston/philadelphia/new_york/montreal places JSON."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
L = (
    "See Wikimedia Commons file page for license."
)
A = "Wikimedia Commons contributors"


def jwrite(rel: str, rows: list[dict]) -> None:
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    vienna = [
        {"slug": "schoenbrunn_palace", "category": "palaces",
         "name_en": "Schönbrunn Palace", "subtitle_de": "Schloss Schönbrunn",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/b/bb/"
             "Schonbrunn_Palace_-_Vienna.jpg"),
         "image_rel_path": "images/schoenbrunn_palace.jpg",
         "license_note": L, "attribution": A},
        {"slug": "hofburg_vienna", "category": "palaces",
         "name_en": "Hofburg", "subtitle_de": "Hofburg — Neue Burg",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/c/c6/"
             "Wien_-_Hofburg_-_Neue_Burg_-_Panorama_-_2018-08-22.jpg"),
         "image_rel_path": "images/hofburg_vienna.jpg",
         "license_note": L, "attribution": A},
        {"slug": "stephansdom", "category": "places_of_worship",
         "name_en": "St. Stephen's Cathedral",
         "subtitle_de": "Stephansdom",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/c/cd/"
             "Austria-00154_-_St._Stephen%27s_Cathedral_%28Stephansdom%29"
             "_%289097202854%29.jpg"),
         "image_rel_path": "images/stephansdom.jpg",
         "license_note": L, "attribution": A},
        {"slug": "belvedere_vienna", "category": "palaces",
         "name_en": "Belvedere", "subtitle_de": "Oberes Belvedere",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/a/a6/"
             "Oberes_Belvedere_Wien.jpg"),
         "image_rel_path": "images/belvedere_vienna.jpg",
         "license_note": L, "attribution": A},
        {"slug": "prater_riesenrad", "category": "landmarks",
         "name_en": "Wiener Riesenrad",
         "subtitle_de": "Riesenrad, Prater",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/d/d5/"
             "Wien%2C_Prater%2C_Riesenrad_--_2018_--_3161.jpg"),
         "image_rel_path": "images/prater_riesenrad.jpg",
         "license_note": L, "attribution": A},
        {"slug": "karlskirche", "category": "places_of_worship",
         "name_en": "Karlskirche",
         "subtitle_de": "Karlskirche, Karlsplatz",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/4/4e/"
             "Karlskirche%2C_Vienna_%2850661791653%29.jpg"),
         "image_rel_path": "images/karlskirche.jpg",
         "license_note": L, "attribution": A},
        {"slug": "rathaus_vienna", "category": "landmarks",
         "name_en": "Vienna City Hall", "subtitle_de": "Rathaus",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/4/4c/"
             "Rathaus%2C_Vienna_%288337511536%29.jpg"),
         "image_rel_path": "images/rathaus_vienna.jpg",
         "license_note": L, "attribution": A},
        {"slug": "vienna_state_opera", "category": "theaters",
         "name_en": "Vienna State Opera",
         "subtitle_de": "Wiener Staatsoper",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/5/59/"
             "Wien_-_Staatsoper_%282%29.JPG"),
         "image_rel_path": "images/vienna_state_opera.JPG",
         "license_note": L, "attribution": A},
        {"slug": "hundertwasserhaus", "category": "landmarks",
         "name_en": "Hundertwasserhaus",
         "subtitle_de": "Hundertwasserhaus Wien",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/8/80/"
             "Hundertwasserhaus_Wien_2019.jpg"),
         "image_rel_path": "images/hundertwasserhaus.jpg",
         "license_note": L, "attribution": A},
        {"slug": "albertina", "category": "museums",
         "name_en": "Albertina",
         "subtitle_de": "Albertina Museum",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/a/a3/"
             "Albertina_Wien_evening.jpg"),
         "image_rel_path": "images/albertina.jpg",
         "license_note": L, "attribution": A},
        {"slug": "naturhistorisches_museum", "category": "museums",
         "name_en": "Natural History Museum",
         "subtitle_de": "Naturhistorisches Museum Wien",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/6/6c/"
             "Naturhistorisches_Museum_Wien_%28by_Pudelek%29.jpg"),
         "image_rel_path": "images/naturhistorisches_museum.jpg",
         "license_note": L, "attribution": A},
        {"slug": "spanish_riding_school", "category": "misc",
         "name_en": "Spanish Riding School",
         "subtitle_de": "Spanische Hofreitschule",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/9/9e/"
             "Spanische_Hofreitschule_Vienna_entrance_Hofburg.jpg"),
         "image_rel_path": "images/spanish_riding_school.jpg",
         "license_note": L, "attribution": A},
        {"slug": "austrian_parliament", "category": "landmarks",
         "name_en": "Austrian Parliament",
         "subtitle_de": "Parlament",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/b/bf/"
             "Parlament_Wien-DSC_0238w.jpg"),
         "image_rel_path": "images/austrian_parliament.jpg",
         "license_note": L, "attribution": A},
        {"slug": "naschmarkt", "category": "markets",
         "name_en": "Naschmarkt",
         "subtitle_de": "Wiener Naschmarkt",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/9/99/"
             "Wien_-_Naschmarkt.jpg"),
         "image_rel_path": "images/naschmarkt.jpg",
         "license_note": L, "attribution": A},
        {"slug": "maria_theresien_denkmal", "category": "sculptures",
         "name_en": "Maria Theresa Memorial",
         "subtitle_de": "Maria-Theresien-Denkmal",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/f/ff/"
             "Wien%2C_Maria-Theresien-Denkmal_--_2018_--_3046.jpg"),
         "image_rel_path": "images/maria_theresien_denkmal.jpg",
         "license_note": L, "attribution": A},
        {"slug": "donauturm", "category": "viewpoints",
         "name_en": "Danube Tower", "subtitle_de": "Donauturm",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/0/08/"
             "Donauturm_Wien.jpg"),
         "image_rel_path": "images/donauturm.jpg",
         "license_note": L, "attribution": A},
        {"slug": "kunsthistorisches_museum", "category": "museums",
         "name_en": "Kunsthistorisches Museum",
         "subtitle_de": "KHM, Maria-Theresien-Platz",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/8/8f/"
             "Vienna_-_View_of_Maria_Theresien-Platz_and_the_"
             "Kunsthistorisches_Museum_-_6291.jpg"),
         "image_rel_path": "images/kunsthistorisches_museum.jpg",
         "license_note": L, "attribution": A},
        {"slug": "stephansplatz", "category": "squares",
         "name_en": "Stephansplatz",
         "subtitle_de": "Stephansplatz, Innere Stadt",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/c/c0/"
             "Austria-Vienna-Stephansplatz-Panorama.png"),
         "image_rel_path": "images/stephansplatz_vienna.png",
         "license_note": L, "attribution": A},
        {"slug": "prater_hauptallee", "category": "parks",
         "name_en": "Prater Hauptallee",
         "subtitle_de": "Hauptallee, Wiener Prater",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/d/d3/"
             "Hauptallee_Prater_Wien_2022-08-09_06.jpg"),
         "image_rel_path": "images/prater_hauptallee.jpg",
         "license_note": L, "attribution": A},
        {"slug": "freud_memorial", "category": "sculptures",
         "name_en": "Sigmund Freud Memorial",
         "subtitle_de": "Freud-Denkmal, Freud Park",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/7/72/"
             "Freud_Denkmal_Freud-Park.jpg"),
         "image_rel_path": "images/freud_memorial.jpg",
         "license_note": L, "attribution": A},
    ]

    boston = [
        {"slug": "massachusetts_state_house", "category": "landmarks",
         "name_en": "Massachusetts State House",
         "subtitle_en": "Beacon Hill",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/c/c8/"
             "Massachusetts_State_House_2022.jpg"),
         "image_rel_path": "images/massachusetts_state_house.jpg",
         "license_note": L, "attribution": A},
        {"slug": "faneuil_hall", "category": "landmarks",
         "name_en": "Faneuil Hall",
         "subtitle_en": "Marketplace and meeting hall",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/b/b6/"
             "Faneuil_Hall_Boston_Massachusetts.JPG"),
         "image_rel_path": "images/faneuil_hall.JPG",
         "license_note": L, "attribution": A},
        {"slug": "old_north_church", "category": "places_of_worship",
         "name_en": "Old North Church",
         "subtitle_en": "Christ Church, North End",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/5/51/"
             "Old_North_Church_%286001949500%29.jpg"),
         "image_rel_path": "images/old_north_church.jpg",
         "license_note": L, "attribution": A},
        {"slug": "boston_public_library_mckim", "category": "libraries",
         "name_en": "Boston Public Library, McKim Building",
         "subtitle_en": "Copley Square",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/b/b0/"
             "Boston_Public_Library%2C_McKim_Building_%282019%29.jpg"),
         "image_rel_path": "images/boston_public_library_mckim.jpg",
         "license_note": L, "attribution": A},
        {"slug": "trinity_church_copley", "category": "places_of_worship",
         "name_en": "Trinity Church",
         "subtitle_en": "Richardson, Copley Square",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/a/ab/"
             "Trinity_Church%2C_Copley_Square%2C_Boston_MA_"
             "%2850986785927%29.jpg"),
         "image_rel_path": "images/trinity_church_copley.jpg",
         "license_note": L, "attribution": A},
        {"slug": "fenway_park", "category": "misc",
         "name_en": "Fenway Park",
         "subtitle_en": "Home of the Red Sox",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/a/ad/"
             "Outside_Fenway_Park_in_Boston.jpg"),
         "image_rel_path": "images/fenway_park.jpg",
         "license_note": L, "attribution": A},
        {"slug": "bunker_hill_monument", "category": "landmarks",
         "name_en": "Bunker Hill Monument",
         "subtitle_en": "Charlestown",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/b/bc/"
             "Bunker_Hill_Monument_%2836276p%29.jpg"),
         "image_rel_path": "images/bunker_hill_monument.jpg",
         "license_note": L, "attribution": A},
        {"slug": "uss_constitution", "category": "misc",
         "name_en": "USS Constitution",
         "subtitle_en": "Charlestown Navy Yard",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/0/0f/"
             "USS_Constitution%2C_Boston%2C_2024-12-15_"
             "%2854208864939%29.jpg"),
         "image_rel_path": "images/uss_constitution.jpg",
         "license_note": L, "attribution": A},
        {"slug": "quincy_market", "category": "markets",
         "name_en": "Quincy Market",
         "subtitle_en": "Faneuil Hall Marketplace",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/b/ba/"
             "Quincy_Market_-_Boston%2C_MA.jpg"),
         "image_rel_path": "images/quincy_market.jpg",
         "license_note": L, "attribution": A},
        {"slug": "boston_common", "category": "parks",
         "name_en": "Boston Common",
         "subtitle_en": "Public park",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/f/fb/"
             "Boston_Common_November_2016_panorama.jpg"),
         "image_rel_path": "images/boston_common.jpg",
         "license_note": L, "attribution": A},
        {"slug": "widener_library", "category": "libraries",
         "name_en": "Widener Library",
         "subtitle_en": "Harvard Yard, Cambridge",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/3/31/"
             "Widener_Library_steps%2C_Harvard_Yard%2C_Cambridge%2C_"
             "Massachusetts%2C_US_%28PPL3-Altered%29_julesvernex2.jpg"),
         "image_rel_path": "images/widener_library.jpg",
         "license_note": L, "attribution": A},
        {"slug": "mit_great_dome", "category": "landmarks",
         "name_en": "MIT Great Dome",
         "subtitle_en": "Cambridge",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/6/6a/"
             "Great_Dome%2C_Massachusetts_Institute_of_Technology%2C_"
             "Aug_2019.jpg"),
         "image_rel_path": "images/mit_great_dome.jpg",
         "license_note": L, "attribution": A},
        {"slug": "charles_river_esplanade", "category": "parks",
         "name_en": "Charles River Esplanade",
         "subtitle_en": "Charles River reservation",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/9/9e/"
             "Charles_River_Esplanade_Boston_May_2018_panorama.jpg"),
         "image_rel_path": "images/charles_river_esplanade.jpg",
         "license_note": L, "attribution": A},
        {"slug": "jfk_presidential_library", "category": "museums",
         "name_en": "John F. Kennedy Presidential Library",
         "subtitle_en": "Columbia Point",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/0/00/"
             "John_F._Kennedy_Presidential_Library_%287207868142%29.jpg"),
         "image_rel_path": "images/jfk_presidential_library.jpg",
         "license_note": L, "attribution": A},
        {"slug": "isabella_stewart_gardner_museum", "category": "museums",
         "name_en": "Isabella Stewart Gardner Museum",
         "subtitle_en": "Fenway–Kenmore",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/6/69/"
             "Isabella_Stewart_Gardner_Museum_New_Wing.jpg"),
         "image_rel_path": "images/isabella_stewart_gardner_museum.jpg",
         "license_note": L, "attribution": A},
        {"slug": "museum_of_fine_arts_boston", "category": "museums",
         "name_en": "Museum of Fine Arts, Boston",
         "subtitle_en": "Huntington Avenue",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/b/b3/"
             "MFA%2C_Boston%2C_MASS.JPG"),
         "image_rel_path": "images/museum_of_fine_arts_boston.JPG",
         "license_note": L, "attribution": A},
        {"slug": "newbury_street", "category": "misc",
         "name_en": "Newbury Street",
         "subtitle_en": "Back Bay",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/7/73/"
             "USA-Boston-Newbury_Street0.jpg"),
         "image_rel_path": "images/newbury_street.jpg",
         "license_note": L, "attribution": A},
        {"slug": "boston_tea_party_museum", "category": "museums",
         "name_en": "Boston Tea Party Ships & Museum",
         "subtitle_en": "Congress Street Bridge",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/e/e4/"
             "Griffin_Wharf.JPG"),
         "image_rel_path": "images/boston_tea_party_museum.JPG",
         "license_note": L, "attribution": A},
        {"slug": "paul_revere_house", "category": "misc",
         "name_en": "Paul Revere House",
         "subtitle_en": "North Square",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/d/dc/"
             "Paul_Revere%27s_House_Freedom_Trail_Boston.JPG"),
         "image_rel_path": "images/paul_revere_house.JPG",
         "license_note": L, "attribution": A},
        {"slug": "boston_public_garden", "category": "parks",
         "name_en": "Boston Public Garden",
         "subtitle_en": "Adjacent to Boston Common",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/9/9e/"
             "Boston_Public_Garden_May_2018_010.jpg"),
         "image_rel_path": "images/boston_public_garden.jpg",
         "license_note": L, "attribution": A},
    ]

    philadelphia = [
        {"slug": "liberty_bell", "category": "landmarks",
         "name_en": "Liberty Bell",
         "subtitle_en": "Independence National Historical Park",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/3/3e/"
             "Liberty_Bell%2C_Aug_2019.jpg"),
         "image_rel_path": "images/liberty_bell.jpg",
         "license_note": L, "attribution": A},
        {"slug": "independence_hall", "category": "landmarks",
         "name_en": "Independence Hall",
         "subtitle_en": "Chestnut Street",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/9/9f/"
             "Exterior_of_the_Independence_Hall%2C_Aug_2019.jpg"),
         "image_rel_path": "images/independence_hall.jpg",
         "license_note": L, "attribution": A},
        {"slug": "philadelphia_city_hall", "category": "landmarks",
         "name_en": "Philadelphia City Hall",
         "subtitle_en": "Center City",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/b/b3/"
             "Philadelphia_city_hall.jpg"),
         "image_rel_path": "images/philadelphia_city_hall.jpg",
         "license_note": L, "attribution": A},
        {"slug": "philadelphia_museum_of_art", "category": "museums",
         "name_en": "Philadelphia Museum of Art",
         "subtitle_en": "Benjamin Franklin Parkway",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/9/93/"
             "Philadelphia_Museum_of_Art%2C_main_building.jpg"),
         "image_rel_path": "images/philadelphia_museum_of_art.jpg",
         "license_note": L, "attribution": A},
        {"slug": "reading_terminal_market", "category": "markets",
         "name_en": "Reading Terminal Market",
         "subtitle_en": "12th Street",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/a/a4/"
             "Reading_Terminal_Market_1.jpg"),
         "image_rel_path": "images/reading_terminal_market.jpg",
         "license_note": L, "attribution": A},
        {"slug": "elfreths_alley", "category": "misc",
         "name_en": "Elfreth's Alley",
         "subtitle_en": "Old City",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/4/4b/"
             "Elfreths_Alley.jpg"),
         "image_rel_path": "images/elfreths_alley.jpg",
         "license_note": L, "attribution": A},
        {"slug": "betsy_ross_house", "category": "misc",
         "name_en": "Betsy Ross House",
         "subtitle_en": "Arch Street",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/6/60/"
             "Betsy_Ross_House%2C_Philadelphia%2C_PA.JPG"),
         "image_rel_path": "images/betsy_ross_house.JPG",
         "license_note": L, "attribution": A},
        {"slug": "eastern_state_penitentiary", "category": "misc",
         "name_en": "Eastern State Penitentiary",
         "subtitle_en": "Fairmount Avenue",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/1/1a/"
             "Philadelphia%27s_Eastern_State_Penitentiary%2C_main_gate.jpg"),
         "image_rel_path": "images/eastern_state_penitentiary.jpg",
         "license_note": L, "attribution": A},
        {"slug": "barnes_foundation", "category": "museums",
         "name_en": "Barnes Foundation",
         "subtitle_en": "Benjamin Franklin Parkway",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/f/f8/"
             "The_Barnes_Foundation_in_Philadelphia_%28by_MyWikiBiz%29.jpg"),
         "image_rel_path": "images/barnes_foundation.jpg",
         "license_note": L, "attribution": A},
        {"slug": "thirtieth_street_station", "category": "railway_stations",
         "name_en": "William H. Gray III 30th Street Station",
         "subtitle_en": "Amtrak hub",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/1/12/"
             "Philly_30th_St._Station.jpg"),
         "image_rel_path": "images/thirtieth_street_station.jpg",
         "license_note": L, "attribution": A},
        {"slug": "love_park", "category": "squares",
         "name_en": "Love Park",
         "subtitle_en": "John F. Kennedy Plaza",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/6/6b/"
             "Love_Park_Philadelphia_2025.jpg"),
         "image_rel_path": "images/love_park.jpg",
         "license_note": L, "attribution": A},
        {"slug": "boathouse_row", "category": "landmarks",
         "name_en": "Boathouse Row",
         "subtitle_en": "Schuylkill River",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/8/87/"
             "Boathouse_Row_-_Oct_2024.jpg"),
         "image_rel_path": "images/boathouse_row.jpg",
         "license_note": L, "attribution": A},
        {"slug": "franklin_institute", "category": "museums",
         "name_en": "The Franklin Institute",
         "subtitle_en": "Science museum",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/e/e5/"
             "Philadelphia_October_2017_10_%28The_Franklin_Institute%29.jpg"),
         "image_rel_path": "images/franklin_institute.jpg",
         "license_note": L, "attribution": A},
        {"slug": "rodin_museum", "category": "museums",
         "name_en": "Rodin Museum",
         "subtitle_en": "Benjamin Franklin Parkway",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/0/0f/"
             "Rodin_Museum_entrance_in_Philadelphia%2C_Pennsylvania.jpg"),
         "image_rel_path": "images/rodin_museum.jpg",
         "license_note": L, "attribution": A},
        {"slug": "museum_of_the_american_revolution", "category": "museums",
         "name_en": "Museum of the American Revolution",
         "subtitle_en": "Old City",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/c/cc/"
             "Museum_of_the_American_Revolution.jpg"),
         "image_rel_path": "images/museum_of_the_american_revolution.jpg",
         "license_note": L, "attribution": A},
        {"slug": "italian_market_philadelphia", "category": "markets",
         "name_en": "Italian Market",
         "subtitle_en": "South 9th Street",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/4/4e/"
             "ItalianMarketPhiladelphia.jpg"),
         "image_rel_path": "images/italian_market_philadelphia.jpg",
         "license_note": L, "attribution": A},
        {"slug": "pennsylvania_academy_fine_arts", "category": "museums",
         "name_en": "Pennsylvania Academy of the Fine Arts",
         "subtitle_en": "Broad Street",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/a/ab/"
             "Pennsylvania_Academy_of_the_Fine_Arts_building.jpg"),
         "image_rel_path": "images/pennsylvania_academy_fine_arts.jpg",
         "license_note": L, "attribution": A},
        {"slug": "comcast_center_philadelphia", "category": "landmarks",
         "name_en": "Comcast Center",
         "subtitle_en": "Center City",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/4/49/"
             "Center_City_-_Comcast_Center_%2853587020610%29.jpg"),
         "image_rel_path": "images/comcast_center_philadelphia.jpg",
         "license_note": L, "attribution": A},
        {"slug": "fairmount_water_works", "category": "landmarks",
         "name_en": "Fairmount Water Works",
         "subtitle_en": "Schuylkill banks",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/c/cd/"
             "Fairmount_Water_Works_at_dusk.jpg"),
         "image_rel_path": "images/fairmount_water_works.jpg",
         "license_note": L, "attribution": A},
        {"slug": "christ_church_philadelphia", "category": "places_of_worship",
         "name_en": "Christ Church",
         "subtitle_en": "2nd Street, Old City",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/3/3b/"
             "Christ_Church_from_2nd_Street.jpg"),
         "image_rel_path": "images/christ_church_philadelphia.jpg",
         "license_note": L, "attribution": A},
    ]

    new_york = [
        {"slug": "statue_of_liberty", "category": "landmarks",
         "name_en": "Statue of Liberty",
         "subtitle_en": "Liberty Island",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/d/d3/"
             "Statue_of_Liberty%2C_NY.jpg"),
         "image_rel_path": "images/statue_of_liberty.jpg",
         "license_note": L, "attribution": A},
        {"slug": "brooklyn_bridge", "category": "bridges",
         "name_en": "Brooklyn Bridge",
         "subtitle_en": "East River",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/0/00/"
             "Brooklyn_Bridge_Manhattan.jpg"),
         "image_rel_path": "images/brooklyn_bridge.jpg",
         "license_note": L, "attribution": A},
        {"slug": "empire_state_building", "category": "landmarks",
         "name_en": "Empire State Building",
         "subtitle_en": "Midtown Manhattan",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/4/45/"
             "Empire_State_Building_pano.jpg"),
         "image_rel_path": "images/empire_state_building.jpg",
         "license_note": L, "attribution": A},
        {"slug": "times_square", "category": "squares",
         "name_en": "Times Square",
         "subtitle_en": "Broadway and 7th Avenue",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/0/0c/"
             "Times_Square%2C_New_York_City%2C_20231006_1916_2338.jpg"),
         "image_rel_path": "images/times_square.jpg",
         "license_note": L, "attribution": A},
        {"slug": "bethesda_terrace", "category": "parks",
         "name_en": "Bethesda Terrace and Fountain",
         "subtitle_en": "Central Park",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/9/93/"
             "Bethesda_Fountain_Central_Park_Manhattan_NYC.jpg"),
         "image_rel_path": "images/bethesda_terrace.jpg",
         "license_note": L, "attribution": A},
        {"slug": "metropolitan_museum_of_art", "category": "museums",
         "name_en": "The Metropolitan Museum of Art",
         "subtitle_en": "Fifth Avenue",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/7/70/"
             "Metropolitan_Museum_of_Art_entrance_NYC.JPG"),
         "image_rel_path": "images/metropolitan_museum_of_art.JPG",
         "license_note": L, "attribution": A},
        {"slug": "grand_central_terminal", "category": "railway_stations",
         "name_en": "Grand Central Terminal",
         "subtitle_en": "Midtown Manhattan",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/0/08/"
             "Grand_Central_Terminal_facade.jpg"),
         "image_rel_path": "images/grand_central_terminal.jpg",
         "license_note": L, "attribution": A},
        {"slug": "flatiron_building", "category": "landmarks",
         "name_en": "Flatiron Building",
         "subtitle_en": "Fifth Avenue at Broadway",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/d/da/"
             "New_York_City_%28New_York%2C_USA%29%2C_Empire_State_"
             "Building%2C_Blick_auf_Flatiron_Building_--_2012_--_6459.jpg"),
         "image_rel_path": "images/flatiron_building.jpg",
         "license_note": L, "attribution": A},
        {"slug": "high_line", "category": "parks",
         "name_en": "High Line", "subtitle_en": "Elevated park",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/e/eb/"
             "High_Line_New_York_August_2013.jpg"),
         "image_rel_path": "images/high_line.jpg",
         "license_note": L, "attribution": A},
        {"slug": "nine_eleven_memorial", "category": "misc",
         "name_en": "National September 11 Memorial",
         "subtitle_en": "World Trade Center site",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/2/2c/"
             "National_September_11_Memorial_-_Reflecting_pool_-_"
             "2013-09-14_-_DSC00359.jpg"),
         "image_rel_path": "images/nine_eleven_memorial.jpg",
         "license_note": L, "attribution": A},
        {"slug": "rockefeller_center", "category": "landmarks",
         "name_en": "Rockefeller Center",
         "subtitle_en": "Midtown",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/8/89/"
             "New_York_City_%28New_York%2C_USA%29%2C_Rockefeller_"
             "Center_--_2012_--_6413.jpg"),
         "image_rel_path": "images/rockefeller_center.jpg",
         "license_note": L, "attribution": A},
        {"slug": "chrysler_building", "category": "landmarks",
         "name_en": "Chrysler Building",
         "subtitle_en": "Art Deco skyscraper",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/d/d6/"
             "View_of_Chrysler_Building_from_Empire_State_Building%2C_"
             "New_York_City%2C_20231001_1510_1364.jpg"),
         "image_rel_path": "images/chrysler_building.jpg",
         "license_note": L, "attribution": A},
        {"slug": "washington_square_arch", "category": "landmarks",
         "name_en": "Washington Square Arch",
         "subtitle_en": "Greenwich Village",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/c/c0/"
             "Washington_Square_Arch_September_2022.jpg"),
         "image_rel_path": "images/washington_square_arch.jpg",
         "license_note": L, "attribution": A},
        {"slug": "saint_patricks_cathedral", "category": "places_of_worship",
         "name_en": "St. Patrick's Cathedral",
         "subtitle_en": "Fifth Avenue",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/8/86/"
             "Spires_of_St_Patricks_Cathedral_Rising_Above_Fifth_Avenue"
             "_2019-09-30_18-19.jpg"),
         "image_rel_path": "images/saint_patricks_cathedral.jpg",
         "license_note": L, "attribution": A},
        {"slug": "one_world_trade_center", "category": "landmarks",
         "name_en": "One World Trade Center",
         "subtitle_en": "Lower Manhattan",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/c/c2/"
             "One_World_Trade_Center_%26_7_World_Trade_Center.jpg"),
         "image_rel_path": "images/one_world_trade_center.jpg",
         "license_note": L, "attribution": A},
        {"slug": "the_vessel", "category": "misc",
         "name_en": "The Vessel",
         "subtitle_en": "Hudson Yards",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/9/9a/"
             "Vessel_in_Hudson_Yards%2C_2021-10-02.jpg"),
         "image_rel_path": "images/the_vessel.jpg",
         "license_note": L, "attribution": A},
        {"slug": "ny_public_library_main", "category": "libraries",
         "name_en": "New York Public Library (Main Branch)",
         "subtitle_en": "Stephen A. Schwarzman Building",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/8/86/"
             "New_York_City%2C_Midtown_Manhattan%2C_New_York_Public_"
             "Library%2C_Stephen_A._Schwarzman_Building%2C_1897-1911._"
             "5th_Avenue_%282011%29.jpg"),
         "image_rel_path": "images/ny_public_library_main.jpg",
         "license_note": L, "attribution": A},
        {"slug": "american_museum_natural_history", "category": "museums",
         "name_en": "American Museum of Natural History",
         "subtitle_en": "Upper West Side",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/6/64/"
             "Facade_of_the_American_museum_of_natural_history_NYC_%282%29"
             ".jpg"),
         "image_rel_path": "images/american_museum_natural_history.jpg",
         "license_note": L, "attribution": A},
        {"slug": "guggenheim_museum", "category": "museums",
         "name_en": "Solomon R. Guggenheim Museum",
         "subtitle_en": "Upper East Side",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/d/d2/"
             "Solomon_R._Guggenheim_Museum_New_York_City.jpg"),
         "image_rel_path": "images/guggenheim_museum.jpg",
         "license_note": L, "attribution": A},
        {"slug": "ellis_island_immigration_museum", "category": "museums",
         "name_en": "Ellis Island National Museum of Immigration",
         "subtitle_en": "Upper New York Bay",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/9/9c/"
             "Ellis_Island_Immigration_Museum.jpg"),
         "image_rel_path": "images/ellis_island_immigration_museum.jpg",
         "license_note": L, "attribution": A},
    ]

    montreal = [
        {"slug": "notre_dame_montreal", "category": "places_of_worship",
         "name_en": "Notre-Dame Basilica of Montreal",
         "subtitle_fr": "Basilique Notre-Dame de Montréal",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/d/d0/"
             "Exterior_of_Notre-Dame_de_Montr%C3%A9al_Basilica.jpg"),
         "image_rel_path": "images/notre_dame_montreal.jpg",
         "license_note": L, "attribution": A},
        {"slug": "old_port_montreal", "category": "misc",
         "name_en": "Old Port of Montreal",
         "subtitle_fr": "Vieux-Port de Montréal",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/d/de/"
             "Vieux-Port_de_Montreal_72.jpg"),
         "image_rel_path": "images/old_port_montreal.jpg",
         "license_note": L, "attribution": A},
        {"slug": "mount_royal_lookout", "category": "viewpoints",
         "name_en": "Mount Royal lookout",
         "subtitle_fr": "Belvédère du Mont-Royal",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/6/6c/"
             "Mount_Royal_Montreal_Lookout.jpg"),
         "image_rel_path": "images/mount_royal_lookout.jpg",
         "license_note": L, "attribution": A},
        {"slug": "montreal_biosphere", "category": "museums",
         "name_en": "Biosphere Environment Museum",
         "subtitle_fr": "Biosphère de Montréal",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/8/8c/"
             "Biosph%C3%A8re_Montr%C3%A9al.jpg"),
         "image_rel_path": "images/montreal_biosphere.jpg",
         "license_note": L, "attribution": A},
        {"slug": "olympic_stadium_montreal", "category": "landmarks",
         "name_en": "Olympic Stadium",
         "subtitle_fr": "Stade olympique",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/1/14/"
             "Montreal-Olympic-Stadium-May-2024.jpg"),
         "image_rel_path": "images/olympic_stadium_montreal.jpg",
         "license_note": L, "attribution": A},
        {"slug": "jean_talon_market", "category": "markets",
         "name_en": "Jean-Talon Market",
         "subtitle_fr": "Marché Jean-Talon",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/2/21/"
             "March%C3%A9_Jean-Talon_6.jpg"),
         "image_rel_path": "images/jean_talon_market.jpg",
         "license_note": L, "attribution": A},
        {"slug": "mcgill_campus", "category": "misc",
         "name_en": "McGill University",
         "subtitle_fr": "Campus du centre-ville",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/c/c0/"
             "McGill_University_downtown_campus_31.JPG"),
         "image_rel_path": "images/mcgill_campus.JPG",
         "license_note": L, "attribution": A},
        {"slug": "saint_joseph_oratory", "category": "places_of_worship",
         "name_en": "Saint Joseph's Oratory",
         "subtitle_fr": "Oratoire Saint-Joseph",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/6/69/"
             "Oratoire_Saint-Joseph_du_Mont-Royal_-_Montreal.jpg"),
         "image_rel_path": "images/saint_joseph_oratory.jpg",
         "license_note": L, "attribution": A},
        {"slug": "place_jacques_cartier", "category": "squares",
         "name_en": "Place Jacques-Cartier",
         "subtitle_fr": "Vieux-Montréal",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/4/4c/"
             "Place_Jacques-Cartier%2C_Vieux-Montr%C3%A9al%2C_Montreal%2C_"
             "Quebec_%2830068046525%29.jpg"),
         "image_rel_path": "images/place_jacques_cartier.jpg",
         "license_note": L, "attribution": A},
        {"slug": "montreal_museum_fine_arts", "category": "museums",
         "name_en": "Montreal Museum of Fine Arts",
         "subtitle_fr": "Musée des beaux-arts de Montréal",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/4/42/"
             "Montreal_Museum_of_Fine_Arts.jpg"),
         "image_rel_path": "images/montreal_museum_fine_arts.jpg",
         "license_note": L, "attribution": A},
        {"slug": "jacques_cartier_bridge", "category": "bridges",
         "name_en": "Jacques Cartier Bridge",
         "subtitle_fr": "Pont Jacques-Cartier",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/4/4f/"
             "Jacques_Cartier_Bridge_in_Montreal%2C_Qu%C3%A9bec.jpg"),
         "image_rel_path": "images/jacques_cartier_bridge.jpg",
         "license_note": L, "attribution": A},
        {"slug": "montreal_city_hall", "category": "landmarks",
         "name_en": "Montreal City Hall",
         "subtitle_fr": "Hôtel de Ville de Montréal",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/7/7f/"
             "H%C3%B4tel_de_Ville_de_Montr%C3%A9al%2C_juin_2024.jpg"),
         "image_rel_path": "images/montreal_city_hall.jpg",
         "license_note": L, "attribution": A},
        {"slug": "underground_city_montreal", "category": "misc",
         "name_en": "Underground City (RESO)",
         "subtitle_fr": "Ville souterraine",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/7/7a/"
             "Montreal_Underground_City_IMG_5762.JPG"),
         "image_rel_path": "images/underground_city_montreal.JPG",
         "license_note": L, "attribution": A},
        {"slug": "habitat_67", "category": "landmarks",
         "name_en": "Habitat 67",
         "subtitle_fr": "Habitations sur le fleuve",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/f/fe/"
             "Habitat_67_2019_dllu_01.jpg"),
         "image_rel_path": "images/habitat_67.jpg",
         "license_note": L, "attribution": A},
        {"slug": "clock_tower_old_port", "category": "landmarks",
         "name_en": "Montreal Clock Tower",
         "subtitle_fr": "Tour de l'horloge, Vieux-Port",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/b/be/"
             "Clock_Tower%2C_Old_Port%2C_Montreal_2021.jpg"),
         "image_rel_path": "images/clock_tower_old_port.jpg",
         "license_note": L, "attribution": A},
        {"slug": "parc_jean_drapeau", "category": "parks",
         "name_en": "Parc Jean-Drapeau",
         "subtitle_fr": "Îles de Sainte-Hélène et Notre-Dame",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/e/e2/"
             "Parc_Jean-Drapeau_Montr%C3%A9al.jpg"),
         "image_rel_path": "images/parc_jean_drapeau.jpg",
         "license_note": L, "attribution": A},
        {"slug": "parc_jeanne_mance", "category": "parks",
         "name_en": "Jeanne-Mance Park",
         "subtitle_fr": "Parc Jeanne-Mance",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/b/b8/"
             "Parc_Jeanne-Mance_22.JPG"),
         "image_rel_path": "images/parc_jeanne_mance.JPG",
         "license_note": L, "attribution": A},
        {"slug": "square_saint_louis", "category": "squares",
         "name_en": "Square Saint-Louis",
         "subtitle_fr": "Le Plateau-Mont-Royal",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/f/fe/"
             "Montreal_Square_Saint-Louis.jpg"),
         "image_rel_path": "images/square_saint_louis.jpg",
         "license_note": L, "attribution": A},
        {"slug": "marche_bonsecours", "category": "markets",
         "name_en": "Bonsecours Market",
         "subtitle_fr": "Marché Bonsecours",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/b/b4/"
             "March%C3%A9_Bonsecours_in_Old_Montreal.jpg"),
         "image_rel_path": "images/marche_bonsecours.jpg",
         "license_note": L, "attribution": A},
        {"slug": "montreal_botanical_garden", "category": "parks",
         "name_en": "Montreal Botanical Garden",
         "subtitle_fr": "Jardin botanique de Montréal",
         "image_source_url": (
             "https://upload.wikimedia.org/wikipedia/commons/e/ec/"
             "Montreal_Botanical_Garden_April_2017_005.jpg"),
         "image_rel_path": "images/montreal_botanical_garden.jpg",
         "license_note": L, "attribution": A},
    ]

    jwrite("vienna/data/vienna_places.json", vienna)
    jwrite("boston/data/boston_places.json", boston)
    jwrite("philadelphia/data/philadelphia_places.json", philadelphia)
    jwrite("new_york/data/new_york_places.json", new_york)
    jwrite("montreal/data/montreal_places.json", montreal)
    for city in (
        "vienna", "boston", "philadelphia", "new_york", "montreal",
    ):
        p = ROOT / city / "data" / f"{city}_place_details.json"
        if not p.is_file():
            p.write_text("{}\n", encoding="utf-8")


if __name__ == "__main__":
    main()
