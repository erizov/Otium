# -*- coding: utf-8 -*-
"""Extended style chapter intros (3–10 lines, RU/EN)."""

from __future__ import annotations

# style_key -> list of paragraphs (each 1–3 sentences)
STYLE_INTRO_PARAS: dict[str, tuple[list[str], list[str]]] = {
    "ancient_rus": (
        [
            "Каменное зодчество Киевской Руси складывалось на стыке "
            "византийской традиции и местных мастерских. Крестово-купольный "
            "храм, мозаика и фреска определяют облик древнейших сохранившихся "
            "памятников.",
            "Стены храмов массивны, притворы компактны, купола часто "
            "опираются на паруса. В интерьере важны икона и мозаичный "
            "образ — архитектура служит богослужению и власти.",
            "Киев, Новгород и Владимир — главные центры; отсюда "
            "распространяются приёмы, которые позже разовьёт московское "
            "зодчество.",
        ],
        [
            "Stone architecture of Kyivan Rus grew at the intersection "
            "of Byzantine tradition and local workshops. The cross-in-square "
            "church, mosaic and fresco define the earliest surviving monuments.",
            "Walls are massive, narthexes compact, domes often rest on "
            "pendentives. Interior image and mosaic matter as much as "
            "structure — architecture serves liturgy and princely power.",
            "Kyiv, Novgorod and Vladimir are the main centres; techniques "
            "spread from here to later Muscovite building.",
        ],
    ),
    "novgorod_school": (
        [
            "Новгородская школа отличается пониженными барабанами, "
            "асимметричными фасадами и выразительной кирпичной кладкой. "
            "Храмы тесно связаны с городской площадью и торговыми путями.",
            "Мастера экономят камень, но усиливают декор кирпичом — "
            "зубцы, пояски, вложенные арки. Фрески часто сохраняются "
            "лучше, чем в других регионах.",
            "Стиль расцветает в XII–XV веках и влияет на поздние "
            "псковские и московские приёмы.",
        ],
        [
            "The Novgorod school is known for low drums, asymmetrical "
            "façades and ornamental brickwork. Churches relate closely "
            "to the market square and trade routes.",
            "Builders save stone but enrich surfaces with brick — "
            "dentils, cornices, recessed arches. Frescoes often survive "
            "remarkably well.",
            "The style flourishes in the 12th–15th centuries and "
            "influences later Pskov and Moscow work.",
        ],
    ),
    "pskov_school": (
        [
            "Псковские храмы лаконичны по объёму, но богаты колокольнями "
            "и звонницами у крепостных стен. Композиция часто привязана "
            "к оборонительному контексту.",
            "«Восьмёрки» барабанов и кокошники перекликаются с "
            "новгородской традицией, но фасады ещё сдержаннее.",
            "Псковская школа важна для понимания северо-западного "
            "варианта древнерусского зодчества XIV–XVI веков.",
        ],
        [
            "Pskov churches are compact in volume yet rich in belfries "
            "and wall bell towers. Composition is often tied to "
            "fortification.",
            "Octagonal drums and kokoshniks echo Novgorod, but façades "
            "are even more restrained.",
            "The Pskov school is key to the north-western branch of "
            "medieval Rus architecture in the 14th–16th centuries.",
        ],
    ),
    "moscow_fifteenth_sixteenth": (
        [
            "Московское зодчество XV–XVI веков соединяет русскую "
            "купольную композицию с итальянскими порталами и "
            "кирпично-белокаменной техникой.",
            "Кремлёвские соборы задают канон для всей страны; "
            "мастера Фиораванти и Алевиз вводят классические "
            "пропорции в православный храм.",
            "К этому же времени относятся первые шатровые эксперименты "
            "и рост декоративности фасадов.",
        ],
        [
            "Muscovite architecture of the 15th–16th centuries joins "
            "Russian dome composition with Italian portals and "
            "brick-and-limestone technique.",
            "Kremlin cathedrals set a canon for the realm; masters "
            "such as Fioravanti and Aloisio bring classical proportion "
            "into Orthodox churches.",
            "The same era sees early tent-roof experiments and "
            "richer façade ornament.",
        ],
    ),
    "tent_roof": (
        [
            "Шатровый стиль — смелый эксперимент московских зодчих "
            "середины XVI века: храм без внутренних опор, с высоким "
            "шатром вместо купола.",
            "Собор Василия Блаженного — символ эпохи; каждая глава — "
            "отдельная капелла на общем подклетe.",
            "Шатры подчёркивают вертикаль и праздничность, связаны "
            "с победами Ивана Грозного и идеей «небесного города».",
        ],
        [
            "The tent-roof style is a bold mid-16th-century Moscow "
            "experiment: churches without interior pillars, with a "
            "tall tent instead of a dome.",
            "Saint Basil's Cathedral is the era's symbol; each tower "
            "is a separate chapel on a shared basement.",
            "Tents stress verticality and festivity, linked to Ivan "
            "the Terrible's victories and the idea of a heavenly city.",
        ],
    ),
    "uzorochye": (
        [
            "Русское узорочье XVII века — пышный декор из кокошников, "
            "поясков и наличников в эпоху Смуты и первых Романовых.",
            "Храмы и терема украшают как ювелирные изделия; "
            "композиция остаётся традиционной, но фасад превращается "
            "в орнаментальное полотно.",
            "Узорочье предвосхищает нарышкинское барокко и сохраняет "
            "связь с московским княжеским прошлым.",
        ],
        [
            "Muscovite ornamental architecture of the 17th century "
            "layers kokoshniks, cornices and window surrounds in the "
            "Time of Troubles and early Romanov era.",
            "Churches and terem chambers are jewelled with ornament; "
            "planning stays traditional while the façade becomes a "
            "textile of pattern.",
            "Uzorochye anticipates Naryshkin Baroque and keeps ties "
            "to princely Moscow.",
        ],
    ),
    "naryshkin_baroque": (
        [
            "Нарышкинское барокко — московское «барокко под куполом»: "
            "вертикальные ярусы кокошников и белокаменная резьба "
            "конца XVII века.",
            "Храмы выглядят лёгкими и стремительными, хотя построены "
            "из кирпича и белого камня.",
            "Стиль связывает узорочье с петровской модернизацией "
            "и влияет на ранние барочные ансамбли.",
        ],
        [
            "Naryshkin Baroque is Moscow 'baroque under the dome': "
            "vertical kokoshnik tiers and white-stone carving of the "
            "late 17th century.",
            "Churches appear light and soaring though built of brick "
            "and limestone.",
            "The style bridges ornamental Muscovy and Petrine "
            "modernisation.",
        ],
    ),
    "petrine_baroque": (
        [
            "Петровское барокко формирует облик новой столицы на Неве: "
            "сетка каналов, крепость, собор и дворцы северного барокко.",
            "Трезини и Леблон закладывают «регулярный город» — "
            "архитектура служит имперской идее просвещения.",
            "Петербург становится витриной Европы, но с собственным "
            "масштабом и климатическими приёмами.",
        ],
        [
            "Petrine Baroque shapes the new capital on the Neva: "
            "canal grid, fortress, cathedral and Northern Baroque palaces.",
            "Trezzini and Le Blond lay out the 'regular city' — "
            "architecture serves an imperial project of reform.",
            "Petersburg becomes a showcase of Europe with its own "
            "scale and climate strategies.",
        ],
    ),
    "elizabethan_baroque": (
        [
            "Елизаветинское барокко — роскошь дворцов Растрелли: "
            "изогнутые фасады, золото и праздничная пластика "
            "середины XVIII века.",
            "Зимний и Екатерининский дворцы, Смольный собор — "
            "образцы театральной архитектуры.",
            "Стиль демонстрирует могущество империи перед эпохой "
            "строгого классицизма.",
        ],
        [
            "Elizabethan Baroque is Rastrelli's palace luxury: curved "
            "façades, gilding and festive wall plasticity of the "
            "mid-18th century.",
            "The Winter and Catherine Palaces, Smolny Cathedral — "
            "models of theatrical architecture.",
            "The style displays imperial power before the age of "
            "strict Neoclassicism.",
        ],
    ),
    "early_classicism": (
        [
            "Ранний русский классицизм второй половины XVIII века "
            "опирается на античные ордера и строгую симметрию.",
            "Дворцы и соборы-ротонды Екатерининской эпохи строят "
            "итальянские и русские мастера академии.",
            "Классицизм постепенно вытесняет барочную пышность, "
            "подготавливая зрелый петербургский ансамбль.",
        ],
        [
            "Early Russian Neoclassicism of the late 18th century "
            "relies on antique orders and strict symmetry.",
            "Catherine-era palaces and rotunda churches are built "
            "by Italian and Russian academy masters.",
            "Neoclassicism gradually replaces Baroque splendour "
            "and prepares mature Petersburg ensembles.",
        ],
    ),
    "mature_classicism": (
        [
            "Зрелый русский классицизм создаёт монументальные ансамбли "
            "столицы: Адмиралтейство, стрелка Васильевского острова, "
            "дворцовые площади.",
            "Кваренги, Захаров, Росси и Томон формируют единый "
            "городской силуэт с колоннадами и ротондами.",
            "Классицизм становится государственным языком архитектуры "
            "на рубеже XVIII–XIX веков.",
        ],
        [
            "Mature Russian Neoclassicism creates monumental capital "
            "ensembles: the Admiralty, Vasilyevsky Spit, palace squares.",
            "Quarenghi, Zakharov, Rossi and Thomon shape a unified "
            "skyline of colonnades and rotundas.",
            "Neoclassicism becomes the state language of architecture "
            "around 1800.",
        ],
    ),
    "empire": (
        [
            "Русский ампир первой трети XIX века выражает торжество "
            "империи после Отечественной войны 1812 года.",
            "Колоннады, триумфальные мотивы и парадные оси связывают "
            "архитектуру с армией и монархией.",
            "Монферран, Стасов и Росси создают соборы, дворцы и "
            "магистрали нового масштаба.",
        ],
        [
            "Russian Empire style of the early 19th century expresses "
            "imperial triumph after the war of 1812.",
            "Colonnades, triumphal motifs and ceremonial axes tie "
            "architecture to army and monarchy.",
            "Montferrand, Stasov and Rossi create cathedrals, palaces "
            "and avenues of a new scale.",
        ],
    ),
    "russo_byzantine": (
        [
            "Русско-византийский стиль середины XIX века — ответ "
            "на поиск национального и православного облика империи.",
            "Константин Тон систематизирует типовые проекты храмов "
            "и общественных зданий.",
            "Купола, аркатурные пояса и симметрия сочетаются "
            "с государственным заказом на массовое строительство.",
        ],
        [
            "Russo-Byzantine architecture of the mid-19th century "
            "answers a search for national Orthodox form.",
            "Konstantin Thon codifies standard church and civic "
            "designs.",
            "Domes, arcaded friezes and symmetry meet state demand "
            "for large-scale construction.",
        ],
    ),
    "eclecticism": (
        [
            "Эклектика второй половины XIX века свободно смешивает "
            "романские, византийские и ренессансные мотивы.",
            "Музеи, вокзалы и особняки демонстрируют богатство "
            "города и заказчиков.",
            "Архитекторы цитируют историю, не следуя одному "
            "строгому канону.",
        ],
        [
            "Late 19th-century eclecticism freely mixes Romanesque, "
            "Byzantine and Renaissance motifs.",
            "Museums, stations and mansions display urban and "
            "client wealth.",
            "Architects quote history without obeying a single strict "
            "canon.",
        ],
    ),
    "pseudo_russian": (
        [
            "Псевдорусский стиль романтически обращается к допетровской "
            "традиции в общественных и торговых зданиях.",
            "Килевидные крыши, башенки и ярусы напоминают terem, "
            "но выполнены в кирпиче и металле XIX века.",
            "Стиль популярен у меценатов, ищущих «русский» образ "
            "без церковного канона.",
        ],
        [
            "Pseudo-Russian style romantically revives pre-Petrine "
            "tradition in public and commercial buildings.",
            "Gabled roofs, turrets and tiers echo terem forms in "
            "19th-century brick and iron.",
            "Patrons favour a 'Russian' image outside church canon.",
        ],
    ),
    "neo_russian": (
        [
            "Неорусский стиль на рубеже XIX–XX веков сочетает "
            "народные мотивы с модерном и майоликой.",
            "Вокзалы, галереи и особняки получают сказочный силуэт.",
            "Архитектура поддерживает идею национального возрождения "
            "в Серебряный век.",
        ],
        [
            "Neo-Russian style at the turn of the 20th century "
            "combines folk motifs with Art Nouveau and majolica.",
            "Stations, galleries and mansions gain fairy-tale "
            "silhouettes.",
            "Architecture backs national revival in the Silver Age.",
        ],
    ),
    "art_nouveau": (
        [
            "Модерн приносит плавные линии, растительный орнамент "
            "и новые материалы — сталь, стекло, кованый металл.",
            "Особняки Шехтеля и Кекушева превращают улицу "
            "в скульптурный пейзаж.",
            "Стиль отражает космополитичную Москву и Петербург "
            "до Первой мировой войны.",
        ],
        [
            "Art Nouveau brings flowing lines, plant ornament and "
            "new materials — steel, glass, wrought iron.",
            "Mansions by Schechtel and Kekushev turn streets into "
            "sculptural landscapes.",
            "The style mirrors cosmopolitan Moscow and Petersburg "
            "before the First World War.",
        ],
    ),
    "neoclassicism_early20": (
        [
            "Неоклассицизм начала XX века возвращает античные формы "
            "в банках, вокзалах и доходных домах.",
            "Строгие портики и симметрия успокаивают город после "
            "эклектики и модерна.",
            "Мастера Фомин, Щуко и Жолтовский готовят почву "
            "для советской монументальности.",
        ],
        [
            "Early 20th-century Neoclassicism returns antique forms "
            "to banks, stations and apartment houses.",
            "Strict porticos and symmetry calm the city after "
            "eclecticism and Art Nouveau.",
            "Fomin, Shchuko and Zholtovsky prepare ground for "
            "Soviet monumentality.",
        ],
    ),
    "avant_garde": (
        [
            "Авангард 1920–1930-х годов радикально переосмысливает "
            "форму, конструкцию и функцию здания.",
            "Башни Шухова, павильоны Мельникова и экспериментальные "
            "жилые ячейки демонстрируют инженерную смелость.",
            "Архитектура участвует в революционном проекте "
            "нового быта.",
        ],
        [
            "Avant-garde architecture of the 1920s–30s radically "
            "rethinks form, structure and function.",
            "Shukhov's towers, Melnikov's pavilions and experimental "
            "housing show engineering daring.",
            "Architecture joins the revolutionary project of a "
            "new everyday life.",
        ],
    ),
    "constructivism": (
        [
            "Конструктивизм ставит конструкцию и функцию выше "
            "декора; доминируют стекло, бетон и экспериментальная "
            "планировка.",
            "Клубы, жилые комплексы и общественные здания "
            "проектируют братья Веснины и Гинзбург; Илья Голосов — "
            "ЗИЛ и клуб им. Русакова — динамичные конструктивистские "
            "объёмы.",
            "Стиль отражает утопию коллективного труда и "
            "индустриализации страны.",
        ],
        [
            "Constructivism privileges structure and function over "
            "decoration; glass, concrete and experimental planning "
            "dominate.",
            "Clubs, housing and public buildings are designed by "
            "the Vesnin brothers and Ginzburg; Ilya Golosov's ZIL "
            "Palace of Culture and Rusakov Club are dynamic "
            "Constructivist volumes.",
            "The style reflects the utopia of collective labour "
            "and industrialisation.",
        ],
    ),
    "stalinist": (
        [
            "Сталинская архитектура 1930–1950-х — монументальный "
            "«советский ампир»: высотки, парадные магистрали, "
            "дворцы метро.",
            "Классические ордера возвращаются как символ победы "
            "и государственной мощи.",
            "Город задумывается как театр власти и "
            "представительства.",
        ],
        [
            "Stalinist architecture of the 1930s–50s is monumental "
            "'Soviet Empire': skyscrapers, parade avenues, metro "
            "palaces.",
            "Classical orders return as symbols of victory and "
            "state power.",
            "The city is conceived as a theatre of authority.",
        ],
    ),
    "panel_housing": (
        [
            "Типовое панельное домостроение массово решает жилищную "
            "проблему после войны и урбанизации.",
            "Серии «хрущёвок» и последующие микрорайоны формируют "
            "облик советского пригорода.",
            "Архитектура здесь — прежде всего индустриальный "
            "процесс, а не индивидуальный авторский замысел.",
        ],
        [
            "Industrial panel housing massively addresses post-war "
            "and urbanisation needs.",
            "Khrushchevka series and later micro-districts shape "
            "the Soviet suburb.",
            "Architecture here is primarily industrial process "
            "rather than individual authorship.",
        ],
    ),
    "soviet_modernism": (
        [
            "Советский модернизм 1960–1980-х предпочитает лаконичные "
            "объёмы, инженерные конструкции и функциональные залы.",
            "Дворцы культуры, спортивные комплексы и телебашни "
            "демонстрируют технический оптимизм.",
            "Стиль соседствует с брутализмом и региональными "
            "вариациями.",
        ],
        [
            "Soviet modernism of the 1960s–80s favours concise "
            "volumes, engineering and functional halls.",
            "Palaces of culture, sports complexes and TV towers "
            "show technical optimism.",
            "The style neighbours Brutalism and regional variants.",
        ],
    ),
    "stalinist_neoclassicism": (
        [
            "Сталинский неоклассицизм накладывает ордер и симметрию "
            "на советские ведомства, жилые дома и вокзалы.",
            "Фасады торжественны, материалы представительны — "
            "мрамор, бронза, лепнина.",
            "Стиль сглаживает переход от конструктивизма "
            "к имперской парадности.",
        ],
        [
            "Stalinist Neoclassicism applies order and symmetry to "
            "Soviet ministries, housing and stations.",
            "Façades are ceremonial; materials prestigious — marble, "
            "bronze, stucco.",
            "The style bridges Constructivism and imperial ceremony.",
        ],
    ),
    "art_deco": (
        [
            "Ар-деко 1920–1930-х сочетает геометрический декор "
            "и парадную представительность театров и кинотеатров.",
            "Здания подчёркивают зрелище и массовый досуг "
            "раннего социализма.",
            "Стиль перекликается с неоклассикой и конструктивизмом.",
        ],
        [
            "1920s–30s Art Deco combines geometric décor and "
            "ceremonial theatres and cinemas.",
            "Buildings stress spectacle and mass leisure of "
            "early socialism.",
            "The style overlaps Neoclassicism and Constructivism.",
        ],
    ),
    "post_constructivism": (
        [
            "Постконструктивизм 1930-х — переходный язык: строгие "
            "фасады, вертикальные пилоны, остатки авангарда.",
            "Здания сочетают рациональную сетку окон с "
            "неоклассическими деталями.",
            "Период готовит официальный стиль высокой сталинской "
            "эпохи.",
        ],
        [
            "1930s post-constructivism is a transitional language: "
            "austere façades, vertical pylons, avant-garde traces.",
            "Buildings mix rational window grids with Neoclassical "
            "details.",
            "The period prepares the official style of High Stalinism.",
        ],
    ),
    "regional_soviet": (
        [
            "Региональное советское зодчество создаёт крупные "
            "спортивные и культурные комплексы в столицах "
            "союзных республик.",
            "Масштаб и инженерия демонстрируют модернизацию "
            "всего СССР.",
            "Проекты адаптируют модернизм к местному климату "
            "и контексту.",
        ],
        [
            "Regional Soviet architecture builds large sports and "
            "culture complexes in union-republic capitals.",
            "Scale and engineering display modernisation across "
            "the USSR.",
            "Projects adapt modernism to local climate and context.",
        ],
    ),
    "brutalism": (
        [
            "Брутализм 1960–1970-х открывает бетон и конструкцию "
            "как главный декор общественных зданий.",
            "Массивные консоли и выразительные каркасы "
            "подчёркивают инженерную логику.",
            "Стиль поляризует, но даёт узнаваемые памятники "
            "науки и культуры.",
        ],
        [
            "1960s–70s Brutalism exposes concrete and structure as "
            "the main ornament of public buildings.",
            "Massive cantilevers and expressive frames stress "
            "engineering logic.",
            "Polarising yet memorable for science and culture.",
        ],
    ),
    "soviet_neoclassicism_revival": (
        [
            "Послевоенное возрождение неоклассицизма восстанавливает "
            "исторические ансамбли и парадные магистрали.",
            "Архитекторы соединяют реставрацию с новым "
            "представительским строительством.",
            "Центры Москвы и Ленинграда получают единый "
            "торжественный облик.",
        ],
        [
            "Post-war neoclassical revival restores historic "
            "ensembles and ceremonial avenues.",
            "Architects combine restoration with new representative "
            "construction.",
            "Centres of Moscow and Leningrad gain a unified "
            "ceremonial appearance.",
        ],
    ),
    "postmodernism": (
        [
            "Постмодернизм конца XX века иронично цитирует "
            "исторические формы в коммерческих и общественных "
            "проектах.",
            "Колонны, арки и фронтоны возвращаются как знак, "
            "а не как канон.",
            "Стиль отражает кризис модернистской уверенности.",
        ],
        [
            "Late 20th-century postmodernism ironically quotes "
            "historical forms in commercial and public work.",
            "Columns, arches and pediments return as signs, "
            "not canon.",
            "The style reflects crisis of modernist confidence.",
        ],
    ),
    "neo_eclectic": (
        [
            "Неоэклектика 1990–2010-х свободно смешивает стили "
            "в постсоветской застройке и реконструкции.",
            "Новые кварталы цитируют классику, модерн и ар-деко "
            "для комфорта и статуса.",
            "Архитектура часто следует рыночному спросу, "
            "а не единой школе.",
        ],
        [
            "1990s–2010s neo-eclecticism freely mixes styles in "
            "post-Soviet construction and reconstruction.",
            "New quarters quote classicism, Art Nouveau and Art Deco "
            "for comfort and status.",
            "Architecture often follows market demand rather than "
            "a single school.",
        ],
    ),
    "contemporary": (
        [
            "Современная архитектура 2000-х — международные башни, "
            "набережные и ландшафтные общественные пространства.",
            "Стекло и сталь формируют новый силуэт Москвы, "
            "Казани, Санкт-Петербурга.",
            "Проекты балансируют между глобальными трендами "
            "и локальным контекстом.",
        ],
        [
            "Contemporary architecture since the 2000s brings "
            "international towers, embankments and landscape public "
            "realm.",
            "Glass and steel shape new skylines in Moscow, Kazan "
            "and Saint Petersburg.",
            "Projects balance global trends and local context.",
        ],
    ),
}


def style_intro_paragraphs(cat: str, edition: str) -> list[str]:
    """Return 3–10 intro paragraphs for a style chapter."""
    block = STYLE_INTRO_PARAS.get(cat)
    if not block:
        return []
    paras = block[0] if edition == "ru" else block[1]
    return list(paras)
