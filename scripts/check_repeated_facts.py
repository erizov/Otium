# -*- coding: utf-8 -*-
"""
Поиск повторяющихся фактов внутри одного объекта во всех главах.

Смотрит на поля history / significance / highlights / facts / story (если есть)
и ищет дубли по «очевидным» шаблонам: совпадающие или почти совпадающие фразы
в разных секциях одного и того же места.

Запуск:
    python scripts/check_repeated_facts.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.core import ensure_utf8_console  # noqa: E402
from scripts.guide_loader import GUIDES, load_places  # noqa: E402


def _normalize_text(text: str) -> str:
    """Грубая нормализация для сравнения «почти одинаковых» фактов."""
    s = text.strip().lower()
    # Убираем кавычки/точки в конце и прочий шум.
    s = re.sub(r"[«»\"“”]", "", s)
    s = re.sub(r"\s+", " ", s)
    s = s.rstrip(".;:,!")

    # Схлопываем типичные синонимы/формулировки.
    replacements = {
        r"объект всемирного наследия юнеско": "unesco",
        r"объект юнеско": "unesco",
        r"юнеско": "unesco",
        r"в списке всемирного наследия": "unesco",
        r"в списке юнеско": "unesco",
        r"включен в список юнеско": "unesco",
        r"входит в список юнеско": "unesco",
        r"входит в состав музея-заповедника коломенское": "kolomenskoe",
        r"памятник м\.?\s*а\.?\s*булгакову": "bulgakov_monument",
        r"памятник булгакову": "bulgakov_monument",
        r"патриаршие пруды": "patriarch_ponds",
    }
    for pattern, repl in replacements.items():
        s = re.sub(pattern, repl, s)

    # Убираем годы вида «— 2007 год», «(1994)» и подобные.
    s = re.sub(r"\b(1[89]\d{2}|20\d{2})\b", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _split_sentences(block: str) -> list[str]:
    """Разбивает длинный текст на короткие фразы для сравнения."""
    # Первое приближение: делим по точкам/точкам с переносом.
    parts = re.split(r"[.!?]\s+", block.strip())
    return [p.strip() for p in parts if p.strip()]


def _collect_fragments(place: dict[str, Any]) -> list[tuple[str, str]]:
    """Возвращает список (section, fragment_text) для одного места."""
    out: list[tuple[str, str]] = []

    history = place.get("history") or ""
    if history:
        for sent in _split_sentences(history):
            out.append(("history", sent))

    significance = place.get("significance") or ""
    if significance:
        for sent in _split_sentences(significance):
            out.append(("significance", sent))

    highlights = place.get("highlights") or []
    for h in highlights:
        if h:
            out.append(("highlights", str(h)))

    facts = place.get("facts") or []
    for f in facts:
        if f:
            out.append(("facts", str(f)))

    # story используется только у некоторых гидов, но поддержим, если есть.
    story = place.get("story") or ""
    if story:
        for sent in _split_sentences(story):
            out.append(("story", sent))

    return out


def find_repeats_for_place(place: dict[str, Any]) -> list[str]:
    """Ищет повторы внутри одного объекта, возвращает список описаний проблем."""
    frags = _collect_fragments(place)
    if len(frags) <= 1:
        return []

    normalized: list[tuple[str, str, str]] = []
    for section, text in frags:
        norm = _normalize_text(text)
        if not norm:
            continue
        normalized.append((section, text, norm))

    issues: list[str] = []

    # Сравниваем каждую пару фрагментов.
    for i in range(len(normalized)):
        sec_i, text_i, norm_i = normalized[i]
        for j in range(i + 1, len(normalized)):
            sec_j, text_j, norm_j = normalized[j]
            if sec_i == sec_j:
                continue

            if norm_i == norm_j:
                issues.append(
                    "  - дублируется между {} и {}: {!r} / {!r}".format(
                        sec_i, sec_j, text_i, text_j,
                    ),
                )
                continue

            # «Почти дубликат»: короткая строка входит в длинную.
            short, long_, sec_short, sec_long, txt_short, txt_long = (
                (norm_i, norm_j, sec_i, sec_j, text_i, text_j)
                if len(norm_i) <= len(norm_j)
                else (norm_j, norm_i, sec_j, sec_i, text_j, text_i)
            )
            if len(short) >= 10 and short in long_:
                issues.append(
                    "  - почти повтор между {} и {}: {!r} ⊂ {!r}".format(
                        sec_short, sec_long, txt_short, txt_long,
                    ),
                )

    return issues


def main() -> int:
    ensure_utf8_console()
    any_issues = False
    for guide in GUIDES:
        try:
            places = load_places(guide)
        except Exception as exc:  # pragma: no cover - диагностическое
            print("Ошибка загрузки {}: {}.".format(guide, exc), file=sys.stderr)
            continue

        for idx, place in enumerate(places, 1):
            name = place.get("name") or "?"
            repeats = find_repeats_for_place(place)
            if not repeats:
                continue
            if not any_issues:
                print("Найдены повторы по фактам/формулировкам:\n")
                any_issues = True
            print("{} #{:02d}: {}".format(guide, idx, name))
            for line in repeats:
                print(line)
            print()

    if not any_issues:
        print("Повторов между историями/значением/фактами внутри объектов не найдено.")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

