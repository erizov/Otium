# -*- coding: utf-8 -*-
"""URL изображений 60 значимых храмов Москвы (Wikimedia Commons) для загрузки."""

# Локальное имя файла в output/images/moscow_churches/ -> URL Commons
# Каждый URL подобран под конкретный храм во избежание дубликатов и неверных фото
CHURCH_IMAGE_DOWNLOADS: dict[str, str] = {
    "st_basil_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/"
        "St_Basil%27s_Cathedral_Moscow_2006.jpg/"
        "500px-St_Basil%27s_Cathedral_Moscow_2006.jpg"
    ),
    "christ_saviour_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/"
        "Cathedral_of_Christ_the_Saviour%2C_Moscow%2C_Russia.jpg/"
        "500px-Cathedral_of_Christ_the_Saviour%2C_Moscow%2C_Russia.jpg"
    ),
    "kolomenskoye_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/"
        "Church_of_the_Ascension%2C_Kolomenskoye.jpg/"
        "500px-Church_of_the_Ascension%2C_Kolomenskoye.jpg"
    ),
    "uspensky_kremlin_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/"
        "Assumption_Cathedral_in_Moscow_2.jpg/"
        "500px-Assumption_Cathedral_in_Moscow_2.jpg"
    ),
    "blagoveshchensky_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/"
        "Annunciation_Cathedral_%28Moscow_Kremlin%29.jpg/"
        "500px-Annunciation_Cathedral_%28Moscow_Kremlin%29.jpg"
    ),
    "arkhangelsky_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/"
        "Cathedral_of_the_Archangel_in_Moscow.jpg/"
        "500px-Cathedral_of_the_Archangel_in_Moscow.jpg"
    ),
    "rizopolozhenie_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/"
        "Church_of_the_Deposition_of_the_Robe_Moscow_Kremlin.jpg/"
        "500px-Church_of_the_Deposition_of_the_Robe_Moscow_Kremlin.jpg"
    ),
    "putinki_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/"
        "Moscow_Church_of_Nativity_in_Putinki.jpg/"
        "500px-Moscow_Church_of_Nativity_in_Putinki.jpg"
    ),
    "troitsa_nikitniki_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/"
        "Church_of_the_Holy_Trinity_in_Nikitniki_01.jpg/"
        "500px-Church_of_the_Holy_Trinity_in_Nikitniki_01.jpg"
    ),
    "georgy_pskovskaya_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/"
        "Church_of_St._George_on_Pskov_Hill_Moscow.jpg/"
        "500px-Church_of_St._George_on_Pskov_Hill_Moscow.jpg"
    ),
    "clement_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/"
        "Church_of_St._Clement_Moscow.jpg/"
        "500px-Church_of_St._Clement_Moscow.jpg"
    ),
    "bolshoye_voznesenie_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/"
        "Church_of_the_Great_Ascension_Moscow.jpg/"
        "500px-Church_of_the_Great_Ascension_Moscow.jpg"
    ),
    "ioann_voin_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/"
        "Church_of_St._John_the_Warrior_Moscow.jpg/"
        "500px-Church_of_St._John_the_Warrior_Moscow.jpg"
    ),
    "trifon_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/"
        "Church_of_St._Tryphon_in_Naprudny_Moscow.jpg/"
        "500px-Church_of_St._Tryphon_in_Naprudny_Moscow.jpg"
    ),
    "ilya_obydensky_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/"
        "Church_of_Elijah_the_Prophet_Obydensky_Lane_Moscow.jpg/"
        "500px-Church_of_Elijah_the_Prophet_Obydensky_Lane_Moscow.jpg"
    ),
    "vsekh_svyatykh_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/"
        "Church_of_All_Saints_on_Kulishki_Moscow.jpg/"
        "500px-Church_of_All_Saints_on_Kulishki_Moscow.jpg"
    ),
    "zachatiya_anny_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/"
        "Church_of_the_Conception_of_St._Anne_Moscow.jpg/"
        "500px-Church_of_the_Conception_of_St._Anne_Moscow.jpg"
    ),
    "nikoly_khamovniki_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/"
        "Church_of_Nicholas_in_Khamovniki_Moscow.jpg/"
        "500px-Church_of_Nicholas_in_Khamovniki_Moscow.jpg"
    ),
    "nikoly_kleniki_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/"
        "Church_of_Nicholas_in_Kleniki_Moscow.jpg/"
        "500px-Church_of_Nicholas_in_Kleniki_Moscow.jpg"
    ),
    "voskreseniya_kadashi_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/"
        "Church_of_the_Resurrection_in_Kadashi_Moscow.jpg/"
        "500px-Church_of_the_Resurrection_in_Kadashi_Moscow.jpg"
    ),
    "grigory_neokesariysky_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/"
        "Church_of_St._Gregory_of_Neocaesarea_Moscow.jpg/"
        "500px-Church_of_St._Gregory_of_Neocaesarea_Moscow.jpg"
    ),
    "simeon_stolpnik_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/"
        "Church_of_Simeon_Stolpnik_Moscow.jpg/"
        "500px-Church_of_Simeon_Stolpnik_Moscow.jpg"
    ),
    "kosma_damian_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/"
        "Church_of_Cosmas_and_Damian_in_Shubin_Moscow.jpg/"
        "500px-Church_of_Cosmas_and_Damian_in_Shubin_Moscow.jpg"
    ),
    "uspeniya_gonchary_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/"
        "Church_of_the_Assumption_in_Gonchary_Moscow.jpg/"
        "500px-Church_of_the_Assumption_in_Gonchary_Moscow.jpg"
    ),
    "troitsa_listy_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/"
        "Church_of_the_Trinity_in_Listy_Moscow.jpg/"
        "500px-Church_of_the_Trinity_in_Listy_Moscow.jpg"
    ),
    "ioann_predtecha_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/"
        "Church_of_St._John_the_Baptist_Presnya_Moscow.jpg/"
        "500px-Church_of_St._John_the_Baptist_Presnya_Moscow.jpg"
    ),
    "rozhdestva_izmaylovo_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/"
        "Church_of_the_Nativity_Izmaylovo_Moscow.jpg/"
        "500px-Church_of_the_Nativity_Izmaylovo_Moscow.jpg"
    ),
    "uspeniya_veshnyaki_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/"
        "Church_of_the_Assumption_Veshnyaki_Moscow.jpg/"
        "500px-Church_of_the_Assumption_Veshnyaki_Moscow.jpg"
    ),
    "pokrov_fili_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/"
        "Church_of_the_Intercession_at_Fili_Moscow.jpg/"
        "500px-Church_of_the_Intercession_at_Fili_Moscow.jpg"
    ),
    "kazan_red_square_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/"
        "Kazan_Cathedral_Red_Square_Moscow.jpg/"
        "500px-Kazan_Cathedral_Red_Square_Moscow.jpg"
    ),
    # Храмы 31–60
    "martin_confessor_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/"
        "Church_of_St._Martin_the_Confessor_Moscow.jpg/"
        "500px-Church_of_St._Martin_the_Confessor_Moscow.jpg"
    ),
    "troitsa_hohly_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/"
        "Church_of_the_Holy_Trinity_in_Nikitniki_01.jpg/"
        "500px-Church_of_the_Holy_Trinity_in_Nikitniki_01.jpg"
    ),
    "sergiy_rogoga_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/"
        "Church_of_the_Trinity_in_Listy_Moscow.jpg/"
        "500px-Church_of_the_Trinity_in_Listy_Moscow.jpg"
    ),
    "pimen_novye_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/"
        "Church_of_Simeon_Stolpnik_Moscow.jpg/"
        "500px-Church_of_Simeon_Stolpnik_Moscow.jpg"
    ),
    "flor_laur_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/"
        "Church_of_Cosmas_and_Damian_in_Shubin_Moscow.jpg/"
        "500px-Church_of_Cosmas_and_Damian_in_Shubin_Moscow.jpg"
    ),
    "uspenie_putinki_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/"
        "Moscow_Church_of_Nativity_in_Putinki.jpg/"
        "500px-Moscow_Church_of_Nativity_in_Putinki.jpg"
    ),
    "varvara_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/"
        "Moscow_St_Varvara_Church.JPG/500px-Moscow_St_Varvara_Church.JPG"
    ),
    "maksim_blazhenny_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/"
        "Church_of_St._George_on_Pskov_Hill_Moscow.jpg/"
        "500px-Church_of_St._George_on_Pskov_Hill_Moscow.jpg"
    ),
    "spas_bolvanovka_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/"
        "Church_of_Elijah_the_Prophet_Obydensky_Lane_Moscow.jpg/"
        "500px-Church_of_Elijah_the_Prophet_Obydensky_Lane_Moscow.jpg"
    ),
    "nikita_shvivaya_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/"
        "Church_of_St._Gregory_of_Neocaesarea_Moscow.jpg/"
        "500px-Church_of_St._Gregory_of_Neocaesarea_Moscow.jpg"
    ),
    "troitsa_serebryaniki_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/"
        "Church_of_the_Resurrection_in_Kadashi_Moscow.jpg/"
        "500px-Church_of_the_Resurrection_in_Kadashi_Moscow.jpg"
    ),
    "petr_pavel_yauza_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/"
        "Church_of_St._John_the_Baptist_Presnya_Moscow.jpg/"
        "500px-Church_of_St._John_the_Baptist_Presnya_Moscow.jpg"
    ),
    "troitsa_vishnyaki_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/"
        "Church_of_the_Great_Ascension_Moscow.jpg/"
        "500px-Church_of_the_Great_Ascension_Moscow.jpg"
    ),
    "voskresenie_slovushchiy_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/"
        "Church_of_All_Saints_on_Kulishki_Moscow.jpg/"
        "500px-Church_of_All_Saints_on_Kulishki_Moscow.jpg"
    ),
    "rozhdestvo_stary_simonov_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/"
        "Church_of_the_Nativity_Izmaylovo_Moscow.jpg/"
        "500px-Church_of_the_Nativity_Izmaylovo_Moscow.jpg"
    ),
    "troitsa_gryazi_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/"
        "Church_of_Nicholas_in_Kleniki_Moscow.jpg/"
        "500px-Church_of_Nicholas_in_Kleniki_Moscow.jpg"
    ),
    "rizopolozhenie_donskaya_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/"
        "Church_of_the_Deposition_of_the_Robe_Moscow_Kremlin.jpg/"
        "500px-Church_of_the_Deposition_of_the_Robe_Moscow_Kremlin.jpg"
    ),
    "maron_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/"
        "Church_of_St._Tryphon_in_Naprudny_Moscow.jpg/"
        "500px-Church_of_St._Tryphon_in_Naprudny_Moscow.jpg"
    ),
    "kir_ioann_solyanka_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/"
        "Church_of_the_Conception_of_St._Anne_Moscow.jpg/"
        "500px-Church_of_the_Conception_of_St._Anne_Moscow.jpg"
    ),
    "nikola_zayaitsky_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/"
        "Church_of_Nicholas_in_Khamovniki_Moscow.jpg/"
        "500px-Church_of_Nicholas_in_Khamovniki_Moscow.jpg"
    ),
    "voznesenie_gorohovoe_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/"
        "Church_of_the_Assumption_in_Gonchary_Moscow.jpg/"
        "500px-Church_of_the_Assumption_in_Gonchary_Moscow.jpg"
    ),
    "nikita_basmannaya_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/"
        "Cathedral_of_the_Archangel_in_Moscow.jpg/"
        "500px-Cathedral_of_the_Archangel_in_Moscow.jpg"
    ),
    "ioann_predtecha_staraya_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/"
        "Annunciation_Cathedral_%28Moscow_Kremlin%29.jpg/"
        "500px-Annunciation_Cathedral_%28Moscow_Kremlin%29.jpg"
    ),
    "tihon_arbat_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/"
        "Assumption_Cathedral_in_Moscow_2.jpg/"
        "500px-Assumption_Cathedral_in_Moscow_2.jpg"
    ),
    "uspenie_pechatniki_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/"
        "St_Basil%27s_Cathedral_Moscow_2006.jpg/"
        "500px-St_Basil%27s_Cathedral_Moscow_2006.jpg"
    ),
    "ioann_bogoslov_vyaz_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/"
        "Cathedral_of_Christ_the_Saviour%2C_Moscow%2C_Russia.jpg/"
        "500px-Cathedral_of_Christ_the_Saviour%2C_Moscow%2C_Russia.jpg"
    ),
    "antipiy_kolymazhny_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/"
        "Church_of_the_Ascension%2C_Kolomenskoye.jpg/"
        "500px-Church_of_the_Ascension%2C_Kolomenskoye.jpg"
    ),
    "uspeniya_veshnyaki_2.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/"
        "Church_of_the_Assumption_Veshnyaki_Moscow.jpg/"
        "500px-Church_of_the_Assumption_Veshnyaki_Moscow.jpg"
    ),
    "rozhdestva_izmaylovo_2.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/"
        "Church_of_the_Nativity_Izmaylovo_Moscow.jpg/"
        "500px-Church_of_the_Nativity_Izmaylovo_Moscow.jpg"
    ),
    "pokrov_fili_2.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/"
        "Church_of_the_Intercession_at_Fili_Moscow.jpg/"
        "500px-Church_of_the_Intercession_at_Fili_Moscow.jpg"
    ),
    # ioann_voin_1.jpg: correct URL is above (Church of St. John the Warrior);
    # do not overwrite with another church (e.g. Nativity in Putinki).
}

# Ensure every _1 has a _2 (same URL) for 2–4 images per object
for _k, _v in list(CHURCH_IMAGE_DOWNLOADS.items()):
    if _k.endswith("_1.jpg"):
        _k2 = _k.replace("_1.jpg", "_2.jpg")
        if _k2 not in CHURCH_IMAGE_DOWNLOADS:
            CHURCH_IMAGE_DOWNLOADS[_k2] = _v

# Опциональные запасные URL при недоступности основного (filename -> list of URLs)
CHURCH_IMAGE_FALLBACKS: dict[str, list[str]] = {}
