# -*- coding: utf-8 -*-
"""One-off: write philadelphia + vienna *_place_details.json."""

from __future__ import annotations

import json
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent

_PHILLY: dict[str, dict] = {
    "liberty_bell": {
        "address": "Liberty Bell Center, 6th & Market Sts.",
        "architecture_style": "18th-c. bronze bell, modern pavilion",
        "facts": [
            "Cast in London; cracked early in its American life.",
            "Housed in a secure, climate-controlled pavilion since 2003.",
        ],
        "history": (
            "Hung in the Pennsylvania State House (Independence Hall) "
            "tower; adopted as a symbol of liberty and later of abolition."
        ),
        "significance": (
            "One of the most visited objects of the American Revolution "
            "story in Philadelphia."
        ),
    },
    "independence_hall": {
        "address": "520 Chestnut Street, Philadelphia",
        "architecture_style": "Georgian red-brick public building, 1732–53",
        "facts": [
            "Both the Declaration and Constitution were debated and signed "
            "here.",
            "UNESCO World Heritage Site with related historic park "
            "structures.",
        ],
        "history": (
            "Built as the Pennsylvania State House; served as capitol for "
            "Pennsylvania and meeting place of the Second Continental "
            "Congress."
        ),
        "significance": (
            "Birthplace documents of the United States are associated with "
            "this chamber."
        ),
    },
    "philadelphia_city_hall": {
        "address": "1401 John F. Kennedy Boulevard",
        "architecture_style": "Second Empire, 1871–1901",
        "facts": [
            "William Penn statue atop was long the tallest point in the "
            "city by gentleman's agreement.",
            "Largest municipal building in the U.S. by floor area when "
            "completed.",
        ],
        "history": (
            "Designed by John McArthur Jr.; decades-long construction "
            "centered Philadelphia's civic life at Penn Square."
        ),
        "significance": (
            "Defines Center City skyline and anchors the Broad Street "
            "cultural corridor.",
        ),
    },
    "philadelphia_museum_of_art": {
        "address": "2600 Benjamin Franklin Parkway",
        "architecture_style": "Beaux-Arts, 1919–1928 (main building)",
        "facts": [
            "Famous “Rocky steps” draw film tourists alongside art "
            "visitors.",
            "Houses strong American and European painting collections.",
        ],
        "history": (
            "Built on Fairmount hill as part of the Benjamin Franklin "
            "Parkway plan; expanded with modern wings later."
        ),
        "significance": (
            "Flagship fine-art museum of the city and a Parkway landmark.",
        ),
    },
    "reading_terminal_market": {
        "address": "51 N 12th Street (under train shed)",
        "architecture_style": "Victorian train shed market hall",
        "facts": [
            "Vendors span Amish produce, Pennsylvania Dutch foods, and "
            "global cuisines.",
            "Operates under the historic Reading Railroad headhouse "
            "complex.",
        ],
        "history": (
            "Opened in 1893 as a public market within the Reading Terminal "
            "train shed."
        ),
        "significance": (
            "Working public market and daily lunch destination for "
            "residents and visitors.",
        ),
    },
    "elfreths_alley": {
        "address": "Elfreth's Alley, between Front & 2nd, Arch & Quarry",
        "architecture_style": "Colonial and Federal row houses",
        "facts": [
            "Often called the oldest continuously inhabited residential "
            "street in the U.S.",
            "Named for blacksmith Jeremiah Elfreth.",
        ],
        "history": (
            "Homes for tradespeople and artisans from the early 18th "
            "century onward; preserved as a museum street."
        ),
        "significance": (
            "Rare intact slice of pre-industrial Philadelphia street life.",
        ),
    },
    "betsy_ross_house": {
        "address": "239 Arch Street",
        "architecture_style": "18th-c. trinity-style house",
        "facts": [
            "Tradition links Ross to an early stars-and-stripes flag; "
            "historians debate details.",
            "Operated as a house museum since the 19th century.",
        ],
        "history": (
            "Small colonial-era home interpreted around upholsterer Betsy "
            "Ross and Revolutionary-era craft."
        ),
        "significance": (
            "Popular Old City stop on the freedom trail circuit.",
        ),
    },
    "eastern_state_penitentiary": {
        "address": "2027 Fairmount Avenue",
        "architecture_style": "Gothic Revival prison, 1829",
        "facts": [
            "Pioneered separate-cell penitentiary design in the U.S.",
            "Closed in 1971; now a stabilized ruin museum.",
        ],
        "history": (
            "Influenced prison architecture worldwide; housed Al Capone "
            "briefly in a comparatively plush cell."
        ),
        "significance": (
            "National Historic Landmark framing debates on incarceration.",
        ),
    },
    "barnes_foundation": {
        "address": "2025 Benjamin Franklin Parkway",
        "architecture_style": "Contemporary gallery by Tod Williams Billie "
        "Tsien, 2012",
        "facts": [
            "Holds Albert C. Barnes's ensembles of Impressionist, "
            "Post-Impressionist, and modern works.",
            "Original Merion campus designed as an educational experiment "
            "in viewing.",
        ],
        "history": (
            "Moved from Lower Merion after legal disputes; Parkway building "
            "replicates room layouts and hangings."
        ),
        "significance": (
            "One of the densest concentrations of Renoir, Cézanne, and "
            "Matisse in the world.",
        ),
    },
    "thirtieth_street_station": {
        "address": "2955 Market Street",
        "architecture_style": "Neoclassical train station, 1933",
        "facts": [
            "Major Amtrak hub on the Northeast Corridor.",
            "Grand waiting room with coffered ceiling and chandeliers.",
        ],
        "history": (
            "Built by the Pennsylvania Railroad to replace Broad Street "
            "facilities; Art Deco details inside.",
        ),
        "significance": (
            "Gateway for rail travel and a civic interior landmark.",
        ),
    },
    "love_park": {
        "address": "1599 John F. Kennedy Boulevard",
        "architecture_style": "Modernist plaza, LOVE sculpture 1976",
        "facts": [
            "Robert Indiana's LOVE image is among the most photographed "
            "icons in town.",
            "Plaza redesigned with updated fountain and seating.",
        ],
        "history": (
            "JFK Plaza opened in 1965; LOVE installed for the Bicentennial "
            "and later recast on site.",
        ),
        "significance": (
            "Default meeting point and symbol of Philadelphia pride.",
        ),
    },
    "boathouse_row": {
        "address": "1 Boathouse Row, Schuylkill River",
        "architecture_style": "Victorian Gothic boathouses, 19th c.",
        "facts": [
            "Home to rowing clubs and regatta history on the Schuylkill.",
            "Lit at night as a skyline signature.",
        ],
        "history": (
            "Developed as clubs built individual boathouses along the "
            "riverbank; preserved as a historic district.",
        ),
        "significance": (
            "Heart of Philadelphia rowing culture and Fairmount views.",
        ),
    },
    "franklin_institute": {
        "address": "222 N 20th Street",
        "architecture_style": "Neoclassical core with modern science "
        "wings",
        "facts": [
            "Named for Benjamin Franklin; strong hands-on science "
            "exhibits.",
            "Giant walk-through heart is a generations-old visitor memory.",
        ],
        "history": (
            "Founded 1824; moved to the Parkway in the 1930s and expanded "
            "repeatedly.",
        ),
        "significance": (
            "Primary science museum of the region.",
        ),
    },
    "rodin_museum": {
        "address": "2151 Benjamin Franklin Parkway",
        "architecture_style": "Beaux-Arts pavilion and garden, Paul "
        "Cret, 1929",
        "facts": [
            "Holds one of the largest Rodin collections outside Paris.",
            "The Thinker marks the courtyard entrance.",
        ],
        "history": (
            "Jules E. Mastbaum commissioned casts and assembled the "
            "collection for the city.",
        ),
        "significance": (
            "Quiet sculpture garden opposite the Parkway's larger museums.",
        ),
    },
    "museum_of_the_american_revolution": {
        "address": "101 S 3rd Street",
        "architecture_style": "Contemporary museum architecture, 2017",
        "facts": [
            "Displays Washington's war tent in a dedicated theater "
            "experience.",
            "Artifacts span soldiers, loyalists, and Native nations.",
        ],
        "history": (
            "Opened to tell inclusive narratives of the Revolutionary era "
            "near Independence Hall.",
        ),
        "significance": (
            "Complements older sites with narrative exhibits and "
            "programming.",
        ),
    },
    "italian_market_philadelphia": {
        "address": "S 9th Street, Bella Vista / Italian Market",
        "architecture_style": "Street market, 19th c.–present",
        "facts": [
            "One of the oldest continuous outdoor markets in the U.S.",
            "Mix of Italian-American heritage and newer immigrant vendors.",
        ],
        "history": (
            "Grew with South Philadelphia immigration; featured in film and "
            "food tourism.",
        ),
        "significance": (
            "Working neighborhood market, not only a tourist strip.",
        ),
    },
    "pennsylvania_academy_fine_arts": {
        "address": "118-128 N Broad Street",
        "architecture_style": "Victorian Gothic / Second Empire, Furness "
        "1876",
        "facts": [
            "America's first art museum and school building combined.",
            "Frank Furness façade is a High Victorian landmark.",
        ],
        "history": (
            "Founded 1805; building anchors North Broad's cultural "
            "institutions.",
        ),
        "significance": (
            "Training ground for American artists including Thomas Eakins.",
        ),
    },
    "comcast_center_philadelphia": {
        "address": "1701 John F. Kennedy Boulevard",
        "architecture_style": "Glass curtain-wall skyscraper, 2008",
        "facts": [
            "Tallest building in Philadelphia at completion.",
            "Lobby features a programmable LED art wall.",
        ],
        "history": (
            "Anchors Comcast's headquarters campus; second tower added "
            "later nearby.",
        ),
        "significance": (
            "Symbol of 21st-century Center City business district.",
        ),
    },
    "fairmount_water_works": {
        "address": "640 Waterworks Drive, Schuylkill banks",
        "architecture_style": "Neoclassical industrial, 1815–1822",
        "facts": [
            "Early municipal water pumping station with picturesque "
            "buildings.",
            "Now an environmental education center.",
        ],
        "history": (
            "Engineered water supply for a growing city; later superseded "
            "but preserved.",
        ),
        "significance": (
            "Framed views toward the Philadelphia Museum of Art upstream.",
        ),
    },
    "christ_church_philadelphia": {
        "address": "20 N American Street, Old City",
        "architecture_style": "Georgian Anglican church, 1744",
        "facts": [
            "George Washington and many founders rented pews here.",
            "Steeple once dominated the colonial skyline.",
        ],
        "history": (
            "Congregation dates to 1695; current building by Robert Smith.",
        ),
        "significance": (
            "Active parish church and Revolutionary-era heritage site.",
        ),
    },
    "rittenhouse_square": {
        "address": "18th & Walnut streets",
        "architecture_style": "Urban square, planned 1682",
        "facts": [
            "One of William Penn's five original squares.",
            "Surrounded by upscale apartments and hotels.",
        ],
        "history": (
            "Named for astronomer David Rittenhouse; gentrified into a "
            "genteel park in the 19th century.",
        ),
        "significance": (
            "Center of Rittenhouse neighborhood dining and strolling.",
        ),
    },
    "philadelphia_zoo": {
        "address": "3400 W Girard Avenue, Fairmount Park",
        "architecture_style": "Victorian zoo planning, 19th c. grounds",
        "facts": [
            "Chartered as America's first zoo; opened 1874.",
            "Historic gatehouses and animal houses dot the site.",
        ],
        "history": (
            "Founded on conservation and education ideals of the 19th "
            "century.",
        ),
        "significance": (
            "Major family destination at the park's western edge.",
        ),
    },
    "mutter_museum": {
        "address": "19 S 22nd Street (College of Physicians)",
        "architecture_style": "19th-c. college building, modern galleries",
        "facts": [
            "Medical history museum with anatomical and pathological "
            "specimens.",
            "Not for the squeamish; aimed at education and research.",
        ],
        "history": (
            "Grew from the College of Physicians of Philadelphia "
            "collections.",
        ),
        "significance": (
            "Internationally known cabinet-of-curiosities medical museum.",
        ),
    },
    "national_constitution_center": {
        "address": "525 Arch Street",
        "architecture_style": "Contemporary museum hall, 2003",
        "facts": [
            "Interactive exhibits on the U.S. Constitution and amendments.",
            "Sits opposite Independence Mall green space.",
        ],
        "history": (
            "Created as a non-partisan civic education institution.",
        ),
        "significance": (
            "Anchors the mall between Independence Hall and the Liberty "
            "Bell.",
        ),
    },
    "philadelphia_magic_gardens": {
        "address": "1020 South Street",
        "architecture_style": "Mosaic environment, Isaiah Zagar",
        "facts": [
            "Indoor-outdoor labyrinth of glass, pottery, and mirror shards.",
            "Artist-led nonprofit maintains the site.",
        ],
        "history": (
            "Isaiah Zagar began South Street mosaics in the 1990s; saved "
            "from development by community campaign.",
        ),
        "significance": (
            "Signature folk-art attraction of the South Street corridor.",
        ),
    },
    "bartram_garden": {
        "address": "5400 Lindbergh Boulevard, Schuylkill",
        "architecture_style": "Colonial farmhouse and botanic grounds",
        "facts": [
            "Home of botanist John Bartram and family nursery business.",
            "Oldest surviving botanic garden in North America.",
        ],
        "history": (
            "Bartram supplied plants to European collectors in the 18th "
            "century.",
        ),
        "significance": (
            "Quiet riverfront contrast to Center City historic core.",
        ),
    },
    "wissahickon_valley_park": {
        "address": "Northwest Philadelphia, Wissahickon Creek",
        "architecture_style": "Picturesque park landscape, 19th c.",
        "facts": [
            "Miles of trails along steep wooded gorge.",
            "Forbidden Drive is a multi-use car-free corridor.",
        ],
        "history": (
            "Preserved as parkland as the city grew around Fairmount's "
            "waterworks system.",
        ),
        "significance": (
            "Premier urban wilderness hike minutes from downtown.",
        ),
    },
    "fort_mifflin": {
        "address": "Fort Mifflin & Hog Island roads, Delaware River",
        "architecture_style": "Earth and brick fort, 18th c.",
        "facts": [
            "Siege here in 1777 delayed British supply ships.",
            "Used through WWII as coastal defense and prison.",
        ],
        "history": (
            "Built on Mud Island to guard Philadelphia's river approach.",
        ),
        "significance": (
            "Rare intact Revolutionary-era fortification in the city.",
        ),
    },
    "shofuso_house": {
        "address": "Horticultural Drive, West Fairmount Park",
        "architecture_style": "20th-c. Japanese house and garden",
        "facts": [
            "Nikkō-style shoin house with pond-stroll garden.",
            "Gift-related history links to sister-city Nagoya.",
        ],
        "history": (
            "Displayed in New York before reassembly in Philadelphia's "
            "park.",
        ),
        "significance": (
            "Peaceful cultural contrast within Fairmount Park.",
        ),
    },
}

_VIENNA: dict[str, dict] = {
    "schoenbrunn_palace": {
        "address": "Schönbrunner Schloßstraße 47, 1130 Wien",
        "architecture_style": "Baroque palace and gardens, 18th c.",
        "facts": [
            "1,441-room summer residence of the Habsburgs; UNESCO site.",
            "Gloriette overlooks formal parterres and the city.",
        ],
        "history": (
            "Site evolved from hunting lodge to imperial showpiece under "
            "Maria Theresa and successors."
        ),
        "significance": (
            "Vienna's most visited palace complex with zoo and gardens.",
        ),
    },
    "hofburg_vienna": {
        "address": "Michaelerkuppel, 1010 Wien",
        "architecture_style": "Medieval to 19th-c. palace wings",
        "facts": [
            "Seat of Habsburg power for centuries; now president's offices "
            "and museums.",
            "Includes Spanish Riding School stables, chapels, and "
            "libraries.",
        ],
        "history": (
            "Grew from medieval castle into a city-sized palace over "
            "dynastic reigns.",
        ),
        "significance": (
            "Geographic and symbolic center of historic Vienna.",
        ),
    },
    "stephansdom": {
        "address": "Stephansplatz 3, 1010 Wien",
        "architecture_style": "Gothic cathedral, 14th–16th c.",
        "facts": [
            "South tower “Steffl” dominates the skyline; tiled roof with "
            "Habsburg eagle.",
            "Burial place of dukes, bishops, and national heroes.",
        ],
        "history": (
            "Built on earlier churches; spire and nave completed across "
            "late medieval campaigns.",
        ),
        "significance": (
            "Mother church of the Roman Catholic Archdiocese of Vienna.",
        ),
    },
    "belvedere_vienna": {
        "address": "Prinz-Eugen-Straße 27, 1030 Wien",
        "architecture_style": "Baroque palace pair, Lukas von Hildebrandt",
        "facts": [
            "Upper Belvedere holds Klimt's The Kiss and major Austrian "
            "collections.",
            "Linked by formal cascade gardens.",
        ],
        "history": (
            "Built for Prince Eugene of Savoy as a garden villa ensemble.",
        ),
        "significance": (
            "Art museum campus and Baroque landmark facing the city center.",
        ),
    },
    "prater_riesenrad": {
        "address": "Riesenradplatz 1, 1020 Wien",
        "architecture_style": "Iron Ferris wheel, 1897",
        "facts": [
            "Surviving wheel from the 1897 World's Fair; 65 m diameter.",
            "Featured in The Third Man and many films.",
        ],
        "history": (
            "Engineered by British firm; rebuilt after WWII with original "
            "cabins.",
        ),
        "significance": (
            "Icon of the Prater amusement zone and skyline silhouette.",
        ),
    },
    "karlskirche": {
        "address": "Karlsplatz, 1040 Wien",
        "architecture_style": "Baroque church, Fischer von Erlach, 1716+",
        "facts": [
            "Votive church for plague relief; twin columns echo Trajan's "
            "Column.",
            "Lift to dome fresco viewing available seasonally.",
        ],
        "history": (
            "Commissioned by Charles VI after the 1713 plague vow; "
            "completed by son Joseph.",
        ),
        "significance": (
            "Dominant Karlsplatz landmark between Ring and Naschmarkt.",
        ),
    },
    "rathaus_vienna": {
        "address": "Friedrich-Schmidt-Platz 1, 1010 Wien",
        "architecture_style": "Neo-Gothic city hall, 1872–1883",
        "facts": [
            "Tower modeled loosely on Flemish cloth halls.",
            "Hosts Christkindlmarkt and summer film festival on the front "
            "lawn.",
        ],
        "history": (
            "Built as Vienna expanded beyond medieval walls; seat of "
            "mayor and council.",
        ),
        "significance": (
            "Anchor of the Ringstraße civic ensemble.",
        ),
    },
    "vienna_state_opera": {
        "address": "Opernring 2, 1010 Wien",
        "architecture_style": "Neo-Renaissance opera house, 1869",
        "facts": [
            "Rebuilt after WWII bombing with restored historic façade.",
            "World-class repertoire and New Year's broadcast tradition.",
        ],
        "history": (
            "Opened as Hofoper; renamed after the fall of the monarchy.",
        ),
        "significance": (
            "One of the great opera addresses of Europe on the Ring.",
        ),
    },
    "hundertwasserhaus": {
        "address": "Kegelgasse 34–38, 1030 Wien",
        "architecture_style": "Expressionist housing, Hundertwasser, 1985",
        "facts": [
            "Undulating floors, tree tenants, and polychrome façade.",
            "Adjacent village has cafés and Hundertwasser exhibits.",
        ],
        "history": (
            "Municipal housing project co-designed with architect Josef "
            "Krawina as an artistic statement.",
        ),
        "significance": (
            "Most photographed alternative architecture stop in Vienna.",
        ),
    },
    "albertina": {
        "address": "Albertinaplatz 1, 1010 Wien",
        "architecture_style": "Habsburg palace with modern galleries",
        "facts": [
            "Print rooms and graphic collections among the world's largest.",
            "State rooms overlook the opera roofline.",
        ],
        "history": (
            "Named for Duke Albert of Saxe-Teschen; expanded as a public "
            "museum.",
        ),
        "significance": (
            "Bridge between imperial residence layers and modern art shows.",
        ),
    },
    "naturhistorisches_museum": {
        "address": "Burgring 7, 1010 Wien",
        "architecture_style": "Historicist palace museum, 1881–1891",
        "facts": [
            "Mirror twin across Maria-Theresien-Platz to the art history "
            "museum.",
            "Famous for meteorites, dinosaurs, and the Venus of "
            "Willendorf.",
        ],
        "history": (
            "Built under Franz Joseph to house imperial natural science "
            "collections.",
        ),
        "significance": (
            "Grand interior halls make it a destination beyond specimens.",
        ),
    },
    "spanish_riding_school": {
        "address": "Michaelerplatz 1, 1010 Wien (Hofburg)",
        "architecture_style": "Baroque riding hall, 1735",
        "facts": [
            "Classical dressage of Lipizzaner stallions.",
            "Morning exercises and gala performances by ticket.",
        ],
        "history": (
            "Habsburg court tradition continuing as a living institution.",
        ),
        "significance": (
            "Unique blend of equestrian art and palace architecture.",
        ),
    },
    "austrian_parliament": {
        "address": "Dr.-Karl-Renner-Ring 3, 1010 Wien",
        "architecture_style": "Greek Revival, Theophil Hansen, 1883",
        "facts": [
            "Athena fountain fronts the ramp to the portico.",
            "Seat of the Nationalrat and Bundesrat.",
        ],
        "history": (
            "Built to embody democratic ideals of the 1867 constitution "
            "era.",
        ),
        "significance": (
            "Political heart of the Republic on the Ringstraße.",
        ),
    },
    "naschmarkt": {
        "address": "Linke Wienzeile, 1040 / 1060 Wien",
        "architecture_style": "Open-air market along Wienzeile",
        "facts": [
            "Over 100 stalls of produce, spices, and street food.",
            "Saturday flea market extends west along the channel.",
        ],
        "history": (
            "Grew from 18th-c. milk market into Vienna's largest food "
            "bazaar.",
        ),
        "significance": (
            "Everyday shopping and tourist tasting strip near the center.",
        ),
    },
    "maria_theresien_denkmal": {
        "address": "Maria-Theresien-Platz, 1010 Wien",
        "architecture_style": "Monumental empress monument, 1888",
        "facts": [
            "Honors Maria Theresa surrounded by advisors and children in "
            "relief.",
            "Frames the twin museum façades photographically.",
        ],
        "history": (
            "Erected long after her reign as Habsburg nostalgia peaked.",
        ),
        "significance": (
            "Central pivot of the Museum Quarter approach from the Ring.",
        ),
    },
    "donauturm": {
        "address": "Donauturmstraße 8, 1220 Wien",
        "architecture_style": "Concrete TV tower, 1964",
        "facts": [
            "252 m height with revolving café and viewing deck.",
            "Built for the 1964 international garden show on new Danube "
            "islands.",
        ],
        "history": (
            "Symbol of postwar modern Vienna's Danube reclamation projects.",
        ),
        "significance": (
            "Panorama over city, river, and hills from the northeast.",
        ),
    },
    "kunsthistorisches_museum": {
        "address": "Maria-Theresien-Platz, 1010 Wien",
        "architecture_style": "Historicist palace museum, 1891",
        "facts": [
            "Habsburg painting collections including Bruegel masterworks.",
            "Grand staircase and dome interiors match the Naturhistorisches "
            "twin.",
        ],
        "history": (
            "Opened with the twin museum to display imperial art and "
            "Wunderkammer legacies.",
        ),
        "significance": (
            "One of Europe's great old-master museums.",
        ),
    },
    "stephansplatz": {
        "address": "1010 Wien, around Stephansdom",
        "architecture_style": "Medieval-to-modern urban square",
        "facts": [
            "U-Bahn interchange under the cathedral's shadow.",
            "Pedestrian shopping radiates along Kärntner Straße and "
            "Graben.",
        ],
        "history": (
            "Market and execution site in the Middle Ages; rebuilt after "
            "WWII.",
        ),
        "significance": (
            "Default zero point for visitors orienting in the old town.",
        ),
    },
    "prater_hauptallee": {
        "address": "Prater, 1020 Wien",
        "architecture_style": "Allée landscape, 19th c.",
        "facts": [
            "Former imperial hunting ground opened to public in 1766.",
            "Six km straight popular with runners and cyclists.",
        ],
        "history": (
            "Hauptallee formalized for court rides; fairgrounds grew at "
            "the southern end.",
        ),
        "significance": (
            "Green lung and carnival zone east of the inner city.",
        ),
    },
    "freud_memorial": {
        "address": "Berggasse 19, 1090 Wien",
        "architecture_style": "Biedermeier apartment house marker",
        "facts": [
            "Freud lived and worked here 1891–1938 before exile.",
            "Museum in the building interprets psychoanalysis history.",
        ],
        "history": (
            "Site of the famous consulting room, recreated with original "
            "furniture in London but memorialized here.",
        ),
        "significance": (
            "Pilgrimage address for intellectual history tourists.",
        ),
    },
    "stadtpark_vienna": {
        "address": "Parkring, 1010 / 1030 Wien",
        "architecture_style": "English landscape park, 1862",
        "facts": [
            "Gilded Johann Strauss monument is a photo staple.",
            "Wien River channelled underground through the park.",
        ],
        "history": (
            "Ringstraße-era public park replacing fortifications belt.",
        ),
        "significance": (
            "Everyday green space between Karlsplatz and the canal.",
        ),
    },
    "museumsquartier": {
        "address": "Museumsplatz 1, 1070 Wien",
        "architecture_style": "Baroque stables + modern white cubes",
        "facts": [
            "Leopold Museum, MUMOK, Tanzquartier, and courtyard lounges.",
            "Former imperial court stables repurposed as culture campus.",
        ],
        "history": (
            "Major 1990s–2000s conversion project opening baroque walls to "
            "contemporary use.",
        ),
        "significance": (
            "Youthful nightlife and museum block west of the Ring.",
        ),
    },
    "judenplatz_holocaust_memorial": {
        "address": "Judenplatz, 1010 Wien",
        "architecture_style": "Rachel Whiteread concrete library, 2000",
        "facts": [
            "Names of Austrian Holocaust victims inscribed on surrounding "
            "walls.",
            "Stands over medieval synagogue ruins visible underground.",
        ],
        "history": (
            "Commemorates the 1421 Vienna Gesera and 20th-century Shoah.",
        ),
        "significance": (
            "Quiet counterpoint to café life on the old Jewish square.",
        ),
    },
    "ankeruhr_vienna": {
        "address": "Hoher Markt 10–11, 1010 Wien",
        "architecture_style": "Jugendstil clock bridge, 1914",
        "facts": [
            "Twelve noon parade of historical figures across the dial.",
            "Commissioned by the Anker insurance company.",
        ],
        "history": (
            "Franz Matsch design linking two buildings over the market.",
        ),
        "significance": (
            "Beloved Old Town clock-watching ritual.",
        ),
    },
    "technisches_museum_wien": {
        "address": "Mariaspringergasse 2, 1140 Wien",
        "architecture_style": "Modernist museum pavilions, 1918 opening",
        "facts": [
            "Heavy industry, transport, and domestic technology exhibits.",
            "Hands-on areas for families.",
        ],
        "history": (
            "Founded to celebrate technical progress in the young republic.",
        ),
        "significance": (
            "Complements fine-art narratives with machines and mobility.",
        ),
    },
    "ruprechtskirche_vienna": {
        "address": "Ruprechtsplatz, 1010 Wien",
        "architecture_style": "Romanesque church, 12th–13th c.",
        "facts": [
            "Often cited as Vienna's oldest church building fabric.",
            "Named for Salzburg's patron St. Rupert.",
        ],
        "history": (
            "Stood near Danube landing before river regulation moved the "
            "shore.",
        ),
        "significance": (
            "Quiet Romanesque contrast to Baroque domes nearby.",
        ),
    },
    "urania_vienna": {
        "address": "Uraniastraße 1, 1010 Wien",
        "architecture_style": "Art Nouveau observatory and lecture hall",
        "facts": [
            "Public astronomy programs and riverside café terrace.",
            "UNIQA Tower neighbors as a glass high-rise foil.",
        ],
        "history": (
            "Founded as adult education observatory in the early 20th "
            "century.",
        ),
        "significance": (
            "Canal-side landmark between Schwedenplatz and Julius-Raab-"
            "Ufer.",
        ),
    },
    "spanische_hofreitschule_facade": {
        "address": "Michaelerplatz, Hofburg, 1010 Wien",
        "architecture_style": "Baroque Michaelertrakt courtyard",
        "facts": [
            "Ceremonial entry sequence toward the riding hall.",
            "Imperial double eagle motifs on gates.",
        ],
        "history": (
            "Part of the Hofburg's late imperial expansion facing the "
            "Michaelerplatz.",
        ),
        "significance": (
            "Classic postcard view of court architecture and horses.",
        ),
    },
    "mozarthaus_vienna": {
        "address": "Domgasse 5, 1010 Wien",
        "architecture_style": "Baroque apartment house, 17th c.",
        "facts": [
            "Mozart family lived here 1784–1787 composing The Marriage of "
            "Figaro period works.",
            "Museum recreates period rooms and listening stations.",
        ],
        "history": (
            "Only surviving Mozart residence in Vienna open to the public.",
        ),
        "significance": (
            "Compact music-history site steps from Stephansdom.",
        ),
    },
    "haus_der_musik_wien": {
        "address": "Seilerstätte 30, 1010 Wien",
        "architecture_style": "Historic palace with interactive galleries",
        "facts": [
            "Hands-on sound physics and Vienna Philharmonic storylines.",
            "Housed in the former Archduke Charles palace.",
        ],
        "history": (
            "Opened 2000 as a high-tech complement to traditional concert "
            "life.",
        ),
        "significance": (
            "Family-friendly introduction to acoustics and composers.",
        ),
    },
    "tiergarten_schoenbrunn": {
        "address": "Maxingstraße 13b, 1130 Wien",
        "architecture_style": "Zoological garden, 1752 founding",
        "facts": [
            "World's oldest continuously operating zoo in baroque "
            "pavilions.",
            "Breeding programs for giant pandas and rare species.",
        ],
        "history": (
            "Imperial menagerie opened to the public under Franz Stephan "
            "and Maria Theresa.",
        ),
        "significance": (
            "Major family day on the Schönbrunn palace grounds.",
        ),
    },
    "volksgarten_vienna": {
        "address": "Burgring, 1010 Wien",
        "architecture_style": "French formal rose gardens, 1821",
        "facts": [
            "Theseus Temple is a Neoclassical folly by Peter Nobile.",
            "Rose beds named for varieties and political figures.",
        ],
        "history": (
            "Laid on former bastion ground after Napoleonic demolitions.",
        ),
        "significance": (
            "Peaceful Ring park between Parliament and Hofburg gates.",
        ),
    },
}


def main() -> int:
    p_ph = _ROOT / "philadelphia" / "data" / "philadelphia_place_details.json"
    p_vi = _ROOT / "vienna" / "data" / "vienna_place_details.json"
    p_ph.write_text(
        json.dumps(_PHILLY, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    p_vi.write_text(
        json.dumps(_VIENNA, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("wrote", len(_PHILLY), "philly,", len(_VIENNA), "vienna")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
