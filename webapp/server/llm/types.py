# -*- coding: utf-8 -*-
"""Shared request/response types for LLM draft generation."""

from __future__ import annotations

from typing import Any, TypedDict


class MoreInformationLink(TypedDict, total=False):
    label: str
    url: str


class DraftBody(TypedDict, total=False):
    description: str
    history: str
    significance: str


class PlaceDraft(TypedDict, total=False):
    facts: list[str]
    stories: list[str]
    suggested_body: DraftBody
    suggested_links: list[MoreInformationLink]
    raw_text: str
    provider: str
    model: str


def coerce_str_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    out: list[str] = []
    for item in value:
        s = str(item).strip()
        if s:
            out.append(s)
    return out


def coerce_links(value: Any) -> list[MoreInformationLink]:
    if not isinstance(value, list):
        return []
    out: list[MoreInformationLink] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        url = str(item.get("url", "")).strip()
        label = str(item.get("label", "")).strip()
        if not url:
            continue
        if not label:
            label = url
        out.append({"label": label, "url": url})
    return out

