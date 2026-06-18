# -*- coding: utf-8 -*-
"""Merged place narrative (description + facts + history + significance)."""

from __future__ import annotations

import re
from html import escape
from typing import Any, Mapping

from scripts.city_guide_core import is_substantive_text
from scripts.city_guide_naming import (
    clean_wikimedia_display_title,
    filler_display_title,
    is_pdf_filler_slug,
    looks_like_slug_title,
    title_from_pdf_filler_slug,
    title_from_place_slug,
)
from scripts.city_guide_translate import (
    EditionTranslator,
    get_edition_translator,
    opposite_edition,
    translate_for_edition,
)

_CYRILLIC_RE = re.compile(r"[\u0400-\u04FF]")
_SENTENCE_SPLIT_RE = re.compile(
    r"(?<=[.!?…])(?<![A-ZА-ЯЁ]\.)\s+(?=[\"«(A-ZА-ЯЁ0-9])",
)
_NEUTRAL_META_RE = re.compile(r"^[\d\s\u2013\-–—.,/()+]+$")
_SYNTHETIC_RU_STORY_RE = re.compile(
    r"место, которое стоит увидеть в контексте",
    re.IGNORECASE,
)
_SYNTHETIC_EN_STORY_RE = re.compile(
    r"^A notable (?:Moscow|Saint Petersburg) .+, part of the city's .+\.",
    re.IGNORECASE,
)


def is_synthetic_tourist_story(text: str) -> bool:
    """True for auto-generated category filler, not curated place stories."""
    s = str(text).strip()
    if not s:
        return False
    if _SYNTHETIC_RU_STORY_RE.search(s):
        return True
    if _SYNTHETIC_EN_STORY_RE.match(s):
        return True
    if s.startswith("Заметный объект Санкт-Петербурга в контексте"):
        return True
    if "Его история связана с" in s and _SYNTHETIC_RU_STORY_RE.search(s):
        return True
    return False
_LANDMARK_STUB_RE = re.compile(
    r"^.+\s[—–-]\slandmark in [^.]+\.?\s*$",
    re.IGNORECASE,
)
_EN_LANDMARK_TAIL_RE = re.compile(
    r"^(?:a\s+)?(?:notable\s+|historic(?:al)?(?:\s+and\s+cultural)?\s+)?"
    r"landmark in [^.]+\.?\s*$",
    re.IGNORECASE,
)
_HISTORIC_LANDMARK_SENTENCE_RE = re.compile(
    r"^.+\s+is\s+a\s+historic(?:al)?(?:\s+and\s+cultural)?\s+landmark\s+in\s+"
    r"[^.]+\.?\s*$",
    re.IGNORECASE,
)
_LANDMARK_STUB_RU_RE = re.compile(
    r"^.+\s[—–-]\s*(?:знаковая\s+)?достопримечательность(?:\s+в\s+|\s+)[^.]+\.?\s*$",
    re.IGNORECASE,
)
_RU_LANDMARK_TAIL_RE = re.compile(
    r"^(?:знаковая\s+)?достопримечательность(?:\s+в\s+|\s+)[^.]+\.?\s*$",
    re.IGNORECASE,
)


def polish_display_title(text: str) -> str:
    from scripts.city_guide_naming import clean_place_display_title

    return clean_place_display_title(str(text).strip())


def is_ru_landmark_stub(text: str) -> bool:
    s = str(text).strip()
    if not s:
        return False
    if _LANDMARK_STUB_RU_RE.match(s):
        return True
    parts = re.split(r"\s[—–-]\s", s, maxsplit=1)
    if len(parts) == 2 and _RU_LANDMARK_TAIL_RE.match(parts[1].strip()):
        return True
    return bool(_RU_LANDMARK_TAIL_RE.match(s))


def is_landmark_boilerplate(text: str) -> bool:
    """Grow-script / translate filler — never show in guides."""
    return (
        is_landmark_stub(text)
        or is_ru_landmark_stub(text)
        or is_reference_boilerplate(text)
    )


_GENERIC_FACT_STUBS = frozenset(
    {
        "check opening hours and ticketing on official sites before travel.",
        "crowds peak on weekends and public holidays.",
    },
)

_PIXABAY_REF_RE = re.compile(
    r"Reference image context:\s*https?://\S+",
    re.IGNORECASE,
)
_PHOTO_TAGS_RE = re.compile(r"Photo tags:", re.IGNORECASE)
_PUBLIC_ARCHIVE_RE = re.compile(
    r"Public photo archives",
    re.IGNORECASE,
)
_WORTH_A_STOP_RE = re.compile(
    r"^Worth a stop when exploring .+\.\s*$",
    re.IGNORECASE,
)
_MINIMAL_CATEGORY_RE = re.compile(
    r"^.+ is a [a-z ]+ in .+\.\s*$",
    re.IGNORECASE,
)
_URL_RE = re.compile(r"https?://\S+")
_GUIDE_ILLUSTRATION_RE = re.compile(
    r"Иллюстрации в гиде[^.]*\.?\s*",
    re.IGNORECASE,
)
_ILLUSTRATION_META_RE = re.compile(
    r"[;.]?\s*на иллюстрации[^.]*\.?\s*",
    re.IGNORECASE,
)
_ILLUSTRATION_META_START_RE = re.compile(
    r"^На иллюстрации[^.]*\.?\s*",
    re.IGNORECASE,
)
_GUIDE_EXTRA_FRAME_RE = re.compile(
    r"[;.]?\s*Дополнительн(?:ый кадр|ые кадры)(?: в гиде)?[^.]*\.?\s*",
    re.IGNORECASE,
)
_GUIDE_EXTRA_FRAME_START_RE = re.compile(
    r"^Дополнительн(?:ый кадр|ые кадры)(?: в гиде)?[^.]*\.?\s*",
    re.IGNORECASE,
)
_GUIDE_AMONG_ILLUSTRATIONS_RE = re.compile(
    r"Среди иллюстраций в гиде[^.]*\.?\s*",
    re.IGNORECASE,
)
_GUIDE_ON_PHOTO_RE = re.compile(
    r"На фото в гиде[^.]*\.?\s*",
    re.IGNORECASE,
)
_GUIDE_PHOTO_RE = re.compile(
    r"Фото в гиде[^.]*\.?\s*",
    re.IGNORECASE,
)
_GUIDE_ILLUSTRATION_SINGULAR_RE = re.compile(
    r"Иллюстрация в гиде[^.]*\.?\s*",
    re.IGNORECASE,
)
_GUIDE_IN_GUIDE_INLINE_RE = re.compile(
    r";\s*в гиде[^.]*\.?\s*",
    re.IGNORECASE,
)
_GUIDE_IN_GUIDE_START_RE = re.compile(
    r"^в гиде[^.]*\.?\s*",
    re.IGNORECASE,
)
_COMMONS_PAREN_RE = re.compile(
    r"\s*\([^)]*\bCommons\b[^)]*\)",
    re.IGNORECASE,
)
_NA_COMMONS_INLINE_RE = re.compile(
    r";\s*на Commons[^.]*\.?\s*",
    re.IGNORECASE,
)
_NA_COMMONS_START_RE = re.compile(
    r"^На Commons[^.]*\.?\s*",
    re.IGNORECASE,
)
_ILLUSTRATION_DASH_START_RE = re.compile(
    r"^Иллюстрация —[^.]*\.?\s*",
    re.IGNORECASE,
)
_WIKIMEDIA_COMMONS_START_RE = re.compile(
    r"^(?:Кадр|Три кадра|Главный кадр)[^.]*\bCommons\b[^.]*\.?\s*",
    re.IGNORECASE,
)
_WIKIMEDIA_COMMONS_INLINE_RE = re.compile(
    r"[;,]\s*на Wikimedia Commons[^.]*\.?\s*",
    re.IGNORECASE,
)


def clean_pixabay_artifacts(text: str) -> str:
    """Strip Pixabay filler phrases and URLs from guide prose."""
    s = str(text).strip()
    if not s:
        return s
    s = _GUIDE_AMONG_ILLUSTRATIONS_RE.sub("", s)
    s = _GUIDE_ON_PHOTO_RE.sub("", s)
    s = _GUIDE_PHOTO_RE.sub("", s)
    s = _GUIDE_ILLUSTRATION_SINGULAR_RE.sub("", s)
    s = _GUIDE_ILLUSTRATION_RE.sub("", s)
    s = _GUIDE_EXTRA_FRAME_RE.sub("", s)
    s = _GUIDE_EXTRA_FRAME_START_RE.sub("", s)
    s = _ILLUSTRATION_META_RE.sub("", s)
    s = _ILLUSTRATION_META_START_RE.sub("", s)
    s = _GUIDE_IN_GUIDE_INLINE_RE.sub("", s)
    s = _GUIDE_IN_GUIDE_START_RE.sub("", s)
    s = _COMMONS_PAREN_RE.sub("", s)
    s = _NA_COMMONS_INLINE_RE.sub("", s)
    s = _NA_COMMONS_START_RE.sub("", s)
    s = _ILLUSTRATION_DASH_START_RE.sub("", s)
    s = _WIKIMEDIA_COMMONS_START_RE.sub("", s)
    s = _WIKIMEDIA_COMMONS_INLINE_RE.sub("", s)
    s = _PIXABAY_REF_RE.sub("", s)
    s = re.sub(
        r"Photo tags:[^.]*\.?\s*",
        "",
        s,
        flags=re.IGNORECASE,
    )
    s = re.sub(
        r"Public photo archives[^.]*\.?\s*",
        "",
        s,
        flags=re.IGNORECASE,
    )
    s = _URL_RE.sub("", s)
    s = re.sub(r"\s+", " ", s).strip(" .")
    return s


_REFERENCE_BOOK_RE = re.compile(
    r"Крижевская|"
    r"блогерами|"
    r"Текст предоставлен издательством|"
    r"li\s*res\.ru|litres\.ru|"
    r"ISBN\s*[\d\-Xx]+|"
    r"формат\s+PDF\s+A4|"
    r"Эксмо;\s*Москва|"
    r"BEST\s+OF\s+RUSSIA|"
    r"Ins\s*a?gram\s+собрал",
    re.IGNORECASE,
)
_OCR_TOC_RE = re.compile(
    r"Содержание\s+Вступление\s+\d+|"
    r"\d+\s+МАР[ШW]РУТ|"
    r"Донской\s+пр-д,\s*д\.\s*9\s+Центросоюз|"
    r"отдел\s+рукописей\s+РГБ",
    re.IGNORECASE,
)
_PDF_PAGE_TOC_RE = re.compile(r"\b\d{3}\s+[А-ЯЁA-Z]")


def is_reference_boilerplate(text: str) -> bool:
    """OCR/book-catalog filler from PDF sidecar imports — not place prose."""
    s = str(text).strip()
    if len(s) < 80:
        return False
    if _REFERENCE_BOOK_RE.search(s):
        return True
    if _OCR_TOC_RE.search(s):
        return True
    if "Москва изнутри" in s and "ISBN" in s.upper():
        return True
    if s.count("©") >= 2:
        return True
    if len(_PDF_PAGE_TOC_RE.findall(s)) >= 4:
        return True
    return False


def is_pixabay_stub(text: str) -> bool:
    """True for Pixabay tag/url filler or minimal category one-liners."""
    s = str(text).strip()
    if not s:
        return False
    if _WORTH_A_STOP_RE.match(s):
        return True
    if _PUBLIC_ARCHIVE_RE.search(s):
        return True
    if _PIXABAY_REF_RE.search(s):
        return True
    cleaned = clean_pixabay_artifacts(s)
    if not cleaned:
        return True
    if _PHOTO_TAGS_RE.search(s):
        if len(cleaned) < 40:
            return True
        if _MINIMAL_CATEGORY_RE.match(cleaned) and len(cleaned) < 100:
            return True
        return False
    if _MINIMAL_CATEGORY_RE.match(s) and len(s) < 100:
        return True
    return False


def has_cyrillic(text: str) -> bool:
    return bool(_CYRILLIC_RE.search(text))


def _cyrillic_letter_ratio(text: str) -> float:
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0
    cyr = sum(1 for c in letters if "\u0400" <= c <= "\u04FF")
    return cyr / len(letters)


_LEADING_LATIN_RE = re.compile(r'^[\s*"«(\[]*[A-Za-z]')


def is_landmark_stub(text: str) -> bool:
    """True for grow/fix fallback lines like ``Foo — landmark in City.``"""
    s = str(text).strip()
    if not s:
        return False
    if _LANDMARK_STUB_RE.match(s):
        return True
    if _HISTORIC_LANDMARK_SENTENCE_RE.match(s):
        return True
    parts = re.split(r"\s[—–-]\s", s, maxsplit=1)
    if len(parts) == 2 and _EN_LANDMARK_TAIL_RE.match(parts[1].strip()):
        return True
    return bool(_EN_LANDMARK_TAIL_RE.match(s))


def is_generic_fact(text: str) -> bool:
    return str(text).strip().lower() in _GENERIC_FACT_STUBS


def is_usable_narrative_text(text: str) -> bool:
    if not is_substantive_text(text):
        return False
    if is_landmark_boilerplate(text):
        return False
    if is_generic_fact(text):
        return False
    if is_pixabay_stub(text):
        return False
    return True


def text_for_edition(text: str, edition: str) -> bool:
    """True when *text* belongs in an en or ru PDF body/meta line."""
    s = str(text).strip()
    if not is_substantive_text(s):
        return False
    if is_landmark_boilerplate(s):
        return False
    if _NEUTRAL_META_RE.fullmatch(s):
        return True
    if edition == "ru":
        if not has_cyrillic(s):
            return False
        ratio = _cyrillic_letter_ratio(s)
        if _LEADING_LATIN_RE.match(s) and ratio < 0.55:
            return False
        return ratio >= 0.35
    return not has_cyrillic(s)


def _edition_field_keys(edition: str, base: str) -> tuple[str, ...]:
    if edition == "ru":
        return (f"{base}_ru", base)
    return (f"{base}_en", base)


def _cross_edition_field_keys(edition: str, base: str) -> tuple[str, ...]:
    alt = opposite_edition(edition)
    if alt == "ru":
        return (f"{base}_ru", base)
    return (f"{base}_en", base)


def pick_text_field(
    place: Mapping[str, Any],
    edition: str,
    base: str,
    *,
    translator: EditionTranslator | None = None,
) -> str | None:
    for key in _edition_field_keys(edition, base):
        raw = place.get(key)
        if raw is None:
            continue
        text = str(raw).strip()
        if text_for_edition(text, edition):
            return text
    tr = (
        translator
        if translator is not None
        else get_edition_translator()
    )
    if tr is None:
        return None
    for key in _cross_edition_field_keys(edition, base):
        raw = place.get(key)
        if raw is None:
            continue
        text = str(raw).strip()
        if not is_substantive_text(text):
            continue
        translated = translate_for_edition(
            text,
            edition,
            kind="prose",
            translator=tr,
        )
        if translated:
            return translated
    return None


def pick_list_items(
    place: Mapping[str, Any],
    edition: str,
    base: str,
    *,
    translator: EditionTranslator | None = None,
) -> list[str]:
    for key in _edition_field_keys(edition, base):
        raw = place.get(key)
        if not isinstance(raw, list):
            continue
        out = [
            str(item).strip()
            for item in raw
            if text_for_edition(str(item).strip(), edition)
        ]
        if out:
            return out
    tr = (
        translator
        if translator is not None
        else get_edition_translator()
    )
    if tr is None:
        return []
    for key in _cross_edition_field_keys(edition, base):
        raw = place.get(key)
        if not isinstance(raw, list):
            continue
        out: list[str] = []
        for item in raw:
            text = str(item).strip()
            if not is_substantive_text(text):
                continue
            translated = translate_for_edition(
                text,
                edition,
                kind="prose",
                translator=tr,
            )
            if translated:
                out.append(translated)
        if out:
            return out
    return []


def normalize_sentence_key(sentence: str) -> str:
    s = sentence.strip().lower()
    s = re.sub(r"[^\w\s\u0400-\u04ff]", " ", s, flags=re.UNICODE)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _normalize_heading_key(text: str) -> str:
    return normalize_sentence_key(clean_wikimedia_display_title(text))


def split_sentences(text: str) -> list[str]:
    text = str(text).strip()
    if not text:
        return []
    parts = _SENTENCE_SPLIT_RE.split(text)
    out: list[str] = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if part[-1] not in ".!?…":
            part = part + "."
        out.append(part)
    return out


class GuideNarrativeDeduper:
    """Drop duplicate sentences across one guide edition."""

    def __init__(self) -> None:
        self._seen: set[str] = set()

    def accept(
        self,
        sentence: str,
        *,
        dedupe_key: str | None = None,
    ) -> bool:
        key = normalize_sentence_key(dedupe_key or sentence)
        if len(key) < 12:
            return True
        if key in self._seen:
            return False
        self._seen.add(key)
        return True


def _paragraph_blocks_from_text(text: str) -> list[list[str]]:
    blocks: list[list[str]] = []
    for para in str(text).split("\n\n"):
        para = para.strip()
        if not is_substantive_text(para):
            continue
        sents = split_sentences(para)
        if sents:
            blocks.append(sents)
    return blocks


def _field_text_variants(
    place: Mapping[str, Any],
    base: str,
) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for key in (f"{base}_en", base, f"{base}_ru"):
        raw = place.get(key)
        if raw is None or isinstance(raw, list):
            continue
        text = str(raw).strip()
        if not is_substantive_text(text) or text in seen:
            continue
        seen.add(text)
        out.append(text)
    return out


def _list_field_variants(
    place: Mapping[str, Any],
    base: str,
) -> list[list[str]]:
    seen: set[tuple[str, ...]] = set()
    out: list[list[str]] = []
    for key in (f"{base}_en", base, f"{base}_ru"):
        raw = place.get(key)
        if not isinstance(raw, list):
            continue
        items = [
            str(item).strip()
            for item in raw
            if is_substantive_text(str(item).strip())
        ]
        if not items:
            continue
        sig = tuple(items)
        if sig in seen:
            continue
        seen.add(sig)
        out.append(items)
    return out


def _render_text_for_edition(
    raw: str,
    edition: str,
    *,
    translator: EditionTranslator | None,
) -> str | None:
    text = str(raw).strip()
    if is_landmark_boilerplate(text):
        return None
    if text_for_edition(text, edition):
        return text
    tr = translator if translator is not None else get_edition_translator()
    if tr is None:
        return None
    translated = translate_for_edition(
        text,
        edition,
        kind="prose",
        translator=tr,
    )
    if translated and is_landmark_boilerplate(translated):
        return None
    return translated


def _collect_text_field_sentence_pairs(
    place: Mapping[str, Any],
    edition: str,
    base: str,
) -> list[tuple[str, str]]:
    """Merge EN/RU source fields; dedupe keys follow English when available."""
    tr = get_edition_translator()
    pairs: list[tuple[str, str]] = []
    seen_keys: set[str] = set()
    for raw in _field_text_variants(place, base):
        display = _render_text_for_edition(raw, edition, translator=tr)
        if not display:
            continue
        disp_sents = split_sentences(display)
        if text_for_edition(raw, "en"):
            key_sents = split_sentences(raw)
            for idx, sent in enumerate(disp_sents):
                if not is_usable_narrative_text(sent):
                    continue
                key = key_sents[min(idx, len(key_sents) - 1)]
                nk = normalize_sentence_key(key)
                if nk in seen_keys:
                    continue
                seen_keys.add(nk)
                pairs.append((sent, key))
        else:
            for sent in disp_sents:
                if not is_usable_narrative_text(sent):
                    continue
                nk = normalize_sentence_key(sent)
                if nk in seen_keys:
                    continue
                seen_keys.add(nk)
                pairs.append((sent, sent))
    return pairs


def _collect_list_field_sentence_pairs(
    place: Mapping[str, Any],
    edition: str,
    base: str,
) -> list[tuple[str, str]]:
    tr = get_edition_translator()
    pairs: list[tuple[str, str]] = []
    seen_keys: set[str] = set()
    for items in _list_field_variants(place, base):
        for raw in items:
            if not is_usable_narrative_text(raw):
                continue
            display = _render_text_for_edition(raw, edition, translator=tr)
            if not display or not is_usable_narrative_text(display):
                continue
            key = raw if text_for_edition(raw, "en") else display
            for sent in split_sentences(display):
                if not is_usable_narrative_text(sent):
                    continue
                nk = normalize_sentence_key(key)
                if nk in seen_keys:
                    continue
                seen_keys.add(nk)
                pairs.append((sent, key))
    return pairs


def _segment_sentences(
    place: Mapping[str, Any],
    edition: str,
) -> tuple[list[str], list[str]]:
    """
    Return (overview, context) sentence lists.

    overview = description + facts; context = history + significance.
    """
    overview: list[str] = []
    context: list[str] = []

    for sent, _key in _collect_text_field_sentence_pairs(
        place, edition, "description",
    ):
        overview.append(sent)

    for sent, _key in _collect_list_field_sentence_pairs(
        place, edition, "facts",
    ):
        overview.append(sent)

    for sent, _key in _collect_text_field_sentence_pairs(
        place, edition, "history",
    ):
        context.append(sent)

    for sent, _key in _collect_text_field_sentence_pairs(
        place, edition, "significance",
    ):
        context.append(sent)

    return overview, context


def _fallback_narrative_paragraph(
    place: Mapping[str, Any],
    edition: str,
) -> str | None:
    """Last resort only for non-boilerplate description fields."""
    for key in _edition_field_keys(edition, "description"):
        raw = place.get(key)
        if raw is None:
            continue
        text = str(raw).strip()
        if (
            text_for_edition(text, edition)
            and is_usable_narrative_text(text)
        ):
            return text
    tr = get_edition_translator()
    if tr is None:
        return None
    for key in _cross_edition_field_keys(edition, "description"):
        raw = place.get(key)
        if raw is None:
            continue
        text = str(raw).strip()
        if not is_substantive_text(text) or is_landmark_boilerplate(text):
            continue
        translated = translate_for_edition(
            text,
            edition,
            kind="prose",
            translator=tr,
        )
        if translated and is_usable_narrative_text(translated):
            return translated
    return None


def _dedupe_sentence_pairs(
    pairs: list[tuple[str, str]],
    deduper: GuideNarrativeDeduper,
) -> list[str]:
    out: list[str] = []
    for sentence, key in pairs:
        if deduper.accept(sentence, dedupe_key=key):
            out.append(sentence)
    return out


def _dedupe_sentences(
    sentences: list[str],
    deduper: GuideNarrativeDeduper,
) -> list[str]:
    out: list[str] = []
    for sentence in sentences:
        if deduper.accept(sentence):
            out.append(sentence)
    return out


def group_into_paragraphs(
    overview: list[str],
    context: list[str],
) -> list[str]:
    """
    Merge into one or two prose paragraphs (never more).

    Two paragraphs when there is enough sourced material in both parts.
    """
    combined = overview + context
    if not combined:
        return []
    if not context:
        return [" ".join(overview)]
    if not overview:
        if len(context) <= 3 or sum(len(s) for s in context) < 420:
            return [" ".join(context)]
        mid = (len(context) + 1) // 2
        return [
            " ".join(context[:mid]),
            " ".join(context[mid:]),
        ]
    total = len(combined)
    if total <= 4:
        return [" ".join(combined)]
    return [" ".join(overview), " ".join(context)]


def narrative_sentence_blocks(
    place: Mapping[str, Any],
    edition: str,
) -> list[list[str]]:
    """Ordered sentence groups: overview (desc+facts), then context (hist+sig)."""
    overview, context = _segment_sentences(place, edition)
    blocks: list[list[str]] = []
    if overview:
        blocks.append(overview)
    if context:
        blocks.append(context)
    return blocks


def merge_narrative_html(
    place: Mapping[str, Any],
    edition: str,
    deduper: GuideNarrativeDeduper | None = None,
) -> str:
    """Title-less merged narrative as ``<div class=\"place-desc\">`` HTML."""
    dedupe = deduper or GuideNarrativeDeduper()
    overview_pairs: list[tuple[str, str]] = []
    context_pairs: list[tuple[str, str]] = []
    overview_pairs.extend(
        _collect_text_field_sentence_pairs(place, edition, "description"),
    )
    overview_pairs.extend(
        _collect_list_field_sentence_pairs(place, edition, "facts"),
    )
    context_pairs.extend(
        _collect_text_field_sentence_pairs(place, edition, "history"),
    )
    context_pairs.extend(
        _collect_text_field_sentence_pairs(place, edition, "significance"),
    )
    overview = _dedupe_sentence_pairs(overview_pairs, dedupe)
    context = _dedupe_sentence_pairs(context_pairs, dedupe)
    paragraphs = group_into_paragraphs(overview, context)
    if not paragraphs:
        if (overview_pairs or context_pairs) and not overview and not context:
            return ""
        fallback = _fallback_narrative_paragraph(place, edition)
        if fallback:
            paragraphs = [fallback]
    if not paragraphs:
        return ""
    inner = "\n".join(
        '<p class="prose">{}</p>'.format(escape(p)) for p in paragraphs
    )
    return '<div class="place-desc">{}</div>'.format(inner)


def filter_stories(place: Mapping[str, Any], edition: str) -> list[str]:
    items = pick_list_items(place, edition, "stories")
    kept = [
        str(st).strip()
        for st in items
        if str(st).strip() and not is_synthetic_tourist_story(str(st))
    ]
    return kept


def _extract_english_lead(text: str) -> str:
    """First English clause from a mixed RU/EN Wikipedia snippet."""
    from scripts.fetch_place_stories import MIN_STORY_CHARS

    s = str(text).strip()
    if not s:
        return ""
    if text_for_edition(s, "en"):
        return s
    for marker in ("(Russian:", "(Russian", "(рус.", "(Рус."):
        idx = s.find(marker)
        if idx >= MIN_STORY_CHARS:
            lead = s[:idx].strip().rstrip("(").strip()
            if text_for_edition(lead, "en"):
                return lead
    parts = re.split(r"\s[—–-]\s", s, maxsplit=1)
    if len(parts) == 2 and text_for_edition(parts[0], "en"):
        return parts[0].strip()
    return ""


def _tourist_story_fallback(
    place: Mapping[str, Any],
    edition: str,
) -> str:
    """
    Short tourist-style note when no curated ``stories_*`` list exists.

    Uses the first sentence of history / significance for this edition.
    """
    from scripts.fetch_place_stories import MAX_STORY_CHARS, MIN_STORY_CHARS

    chunks: list[str] = []
    for base in ("history", "significance", "description"):
        text = pick_text_field(place, edition, base)
        if text:
            chunks.append(text)
    if not chunks:
        alt = opposite_edition(edition)
        alt_items = pick_list_items(place, alt, "stories")
        if alt_items:
            tr = get_edition_translator()
            if tr is not None:
                translated = translate_for_edition(
                    alt_items[0],
                    edition,
                    kind="prose",
                    translator=tr,
                )
                if translated:
                    chunks.append(translated)
            elif edition == "en":
                lead = _extract_english_lead(alt_items[0])
                if lead:
                    chunks.append(lead)
        if not chunks:
            alt_raw = place.get("stories_ru" if alt == "ru" else "stories_en")
            if isinstance(alt_raw, list) and alt_raw:
                if edition == "en":
                    lead = _extract_english_lead(str(alt_raw[0]))
                    if lead:
                        chunks.append(lead)
    if not chunks and edition == "en":
        bits: list[str] = []
        year = str(place.get("year_built") or "").strip()
        if year and year.isdigit():
            bits.append("Dating from {}.".format(year))
        for key in ("subtitle_en", "address", "architecture_style"):
            text = str(place.get(key) or "").strip()
            if text_for_edition(text, "en"):
                bits.append(text.rstrip(".") + ".")
        cat = str(place.get("category") or "").replace("_", " ")
        if cat and text_for_edition(cat, "en"):
            bits.append("A notable Moscow {}.".format(cat))
        if bits:
            chunks.append(" ".join(bits))
    if not chunks:
        return ""
    combined = " ".join(chunks).strip()
    parts = _SENTENCE_SPLIT_RE.split(combined)
    out: list[str] = []
    for part in parts:
        sentence = part.strip()
        if not is_substantive_text(sentence):
            continue
        if not text_for_edition(sentence, edition):
            continue
        out.append(sentence)
        if len(" ".join(out)) >= MIN_STORY_CHARS:
            break
    snippet = " ".join(out).strip()
    if len(snippet) < MIN_STORY_CHARS:
        return ""
    if len(snippet) > MAX_STORY_CHARS:
        snippet = snippet[: MAX_STORY_CHARS - 3].rsplit(" ", 1)[0] + "..."
    return snippet


def subtitle_html_for_edition(place: Mapping[str, Any], edition: str) -> str:
    if edition == "ru":
        key = "subtitle_ru"
        cls = "sub-ru"
    else:
        key = "subtitle_en"
        cls = "sub-en"
    raw = place.get(key)
    if not is_substantive_text(str(raw or "")):
        return ""
    text = polish_display_title(str(raw).strip())
    if not text_for_edition(text, edition):
        return ""
    heading = place_heading_plain(place, edition)
    if _normalize_heading_key(text) == _normalize_heading_key(heading):
        return ""
    return '<p class="{}">{}</p>'.format(cls, escape(text))


def place_heading_plain(
    place: Mapping[str, Any],
    edition: str,
    *,
    translator: EditionTranslator | None = None,
) -> str:
    """Primary h3 title in the requested edition language."""
    slug = str(place.get("slug") or "place")
    if is_pdf_filler_slug(slug):
        filler = filler_display_title(dict(place))
        if filler:
            return filler

    if edition == "ru":
        keys = ("name_ru", "name")
        alt_keys = ("name_en", "subtitle_en", "name")
    else:
        keys = ("name_en", "subtitle_en", "name")
        alt_keys = ("name_ru", "name")
    plain = pick_first_text(place, edition, keys)
    if plain:
        if looks_like_slug_title(plain):
            return title_from_place_slug(plain)
        return polish_display_title(plain)
    tr = (
        translator
        if translator is not None
        else get_edition_translator()
    )
    if tr is not None:
        for key in alt_keys:
            raw = place.get(key)
            if raw is None:
                continue
            text = str(raw).strip()
            if not is_substantive_text(text):
                continue
            translated = translate_for_edition(
                text,
                edition,
                kind="name",
                translator=tr,
            )
            if translated:
                return polish_display_title(translated)
    if is_pdf_filler_slug(slug):
        return title_from_pdf_filler_slug(slug)
    if "_" in slug:
        return title_from_place_slug(slug)
    return slug


def pick_first_text(
    place: Mapping[str, Any],
    edition: str,
    keys: tuple[str, ...],
) -> str | None:
    for key in keys:
        raw = place.get(key)
        if raw is None:
            continue
        text = str(raw).strip()
        if text_for_edition(text, edition):
            return polish_display_title(text)
    return None


def place_meta_line(
    place: Mapping[str, Any],
    edition: str,
    labels: dict[str, str],
) -> str | None:
    from scripts.city_guide_place_meta import (
        meta_labels,
        pick_location_label,
        pick_metro_line,
        pick_street_address,
        pick_visit_hours,
        place_category,
    )

    parts: list[str] = []
    cat = place_category(dict(place))
    meta = meta_labels(edition)
    line = pick_metro_line(dict(place))
    if cat == "metro" and line:
        parts.append("{} {}".format(meta["metro_line"], line))
    location = pick_location_label(dict(place))
    if location:
        parts.append("{} {}".format(meta["location"], location))
    address = pick_street_address(dict(place))
    if address:
        parts.append("{} {}".format(meta["address"], address))
    hours = pick_visit_hours(dict(place), edition)
    if hours:
        parts.append("{} {}".format(meta["visit_hours"], hours))
    style = pick_text_field(place, edition, "architecture_style")
    if style:
        parts.append("{} {}".format(labels["style"], style))
    year = pick_text_field(place, edition, "year_built")
    if year:
        parts.append("{} {}".format(labels["period"], year))
    if not parts:
        return None
    return " | ".join(parts)
