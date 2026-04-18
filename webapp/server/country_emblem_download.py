# -*- coding: utf-8 -*-
"""Download country emblem SVGs into webapp static (best-effort)."""

from __future__ import annotations

import logging
from pathlib import Path

import requests

logger = logging.getLogger(__name__)

_USER_AGENT = (
    "ExcursionGuideEditor/0.1 "
    "(local dev; contact: none; uses Wikimedia Commons API)"
)

# Wikimedia Commons file titles (SVG preferred). Best-effort for UI badges.
_COMMONS_TITLE_BY_CODE: dict[str, str] = {
    "ru": "File:Coat of Arms of the Russian Federation.svg",
    "de": "File:Coat_of_arms_of_Germany.svg",
    "fr": "File:Coat_of_arms_of_the_French_Republic.svg",
    "it": "File:Emblem_of_Italy.svg",
    "es": "File:Coat_of_Arms_of_Spain.svg",
    "cz": "File:Coat_of_arms_of_the_Czech_Republic.svg",
    "hu": "File:Coat_of_arms_of_Hungary.svg",
    "at": "File:Austria_Bundesadler.svg",
    "us": "File:Greater_coat_of_arms_of_the_United_States.svg",
    "ca": "File:Royal_Coat_of_arms_of_Canada.svg",
    "il": "File:Emblem_of_Israel.svg",
    "va": "File:Coat of arms of the Holy See.svg",
    "gb": "File:Royal Coat of Arms of the United Kingdom.svg",
    "nl": "File:State coat of arms of the Netherlands.svg",
    "tr": "File:National emblem of Turkey.svg",
    "jp": "File:Imperial Seal of Japan.svg",
    "ae": "File:Emblem of the United Arab Emirates.svg",
    "gr": "File:Coat of arms of Greece.svg",
    "pt": "File:Coat of arms of Portugal.svg",
    "sg": "File:Coat of arms of Singapore.svg",
    "th": "File:Garuda Emblem of Thailand.svg",
    "ie": "File:Coat of arms of Ireland.svg",
    "dk": "File:National coat of arms of Denmark.svg",
}


def ensure_country_emblem_svg(static_root: Path, country_code: str) -> bool:
    """
    If `static/emblems/<code>.svg` is missing, try to download from Commons.

    Returns True if the file exists after the call (already there or saved).
    """
    code = country_code.strip().lower()
    if not code:
        return False
    dest = static_root / "emblems" / f"{code}.svg"
    if dest.is_file() and not is_placeholder_emblem(dest):
        return True
    title = _COMMONS_TITLE_BY_CODE.get(code)
    if not title:
        return False
    url = _commons_file_url(title)
    if not url:
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        res = requests.get(
            url,
            timeout=30,
            headers={"User-Agent": _USER_AGENT},
        )
        res.raise_for_status()
    except Exception as exc:
        logger.warning("Country emblem download failed (%s): %s", code, exc)
        return False
    try:
        dest.write_bytes(res.content)
    except OSError as exc:
        logger.warning("Country emblem write failed (%s): %s", code, exc)
        return False
    return dest.is_file()


def _commons_file_url(title: str) -> str | None:
    api = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "imageinfo",
        "iiprop": "url",
    }
    try:
        res = requests.get(
            api,
            params=params,
            timeout=20,
            headers={"User-Agent": _USER_AGENT},
        )
        res.raise_for_status()
        data = res.json()
    except Exception as exc:
        logger.warning("Commons API error for %s: %s", title, exc)
        return None
    if data.get("error"):
        logger.warning(
            "Commons API returned error for %s: %s",
            title,
            data.get("error"),
        )
        return None
    pages = (data.get("query") or {}).get("pages") or {}
    for _pid, page in pages.items():
        if page.get("missing"):
            continue
        infos = page.get("imageinfo") or []
        if not infos:
            continue
        url = infos[0].get("url")
        if isinstance(url, str) and url.startswith("http"):
            return url
    normalized = (data.get("query") or {}).get("normalized") or []
    for item in normalized:
        to_title = item.get("to")
        if isinstance(to_title, str) and to_title:
            return _commons_file_url(to_title)
    return None


def is_placeholder_emblem(path: Path) -> bool:
    try:
        head = path.read_text(encoding="utf-8", errors="ignore")[:800]
    except OSError:
        return False
    return "excursion-webapp-placeholder" in head
