# -*- coding: utf-8 -*-

from __future__ import annotations

import re
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from smolensk.data.places_registry import SMOLENSK_PLACES  # noqa: E402

_FLAT_IMAGE = re.compile(r"^images/[a-z0-9_]+\.jpe?g$", re.IGNORECASE)


def test_smolensk_places_count_48() -> None:
    assert len(SMOLENSK_PLACES) == 48


def test_each_place_has_required_image_fields() -> None:
    for p in SMOLENSK_PLACES:
        assert p.get("slug")
        assert p.get("category")
        assert p.get("name_ru")
        rel = p.get("image_rel_path")
        assert rel
        assert _FLAT_IMAGE.match(rel.replace("\\", "/")), rel
        inner = rel.replace("images/", "").replace("\\", "/")
        assert "/" not in inner
        assert p.get("image_source_url")
        for ex in p.get("additional_images") or []:
            er = ex.get("image_rel_path")
            assert er
            assert _FLAT_IMAGE.match(er.replace("\\", "/")), er
            assert ex.get("image_source_url")


def test_merged_text_details_sample() -> None:
    mus = next(p for p in SMOLENSK_PLACES if p.get("slug") == "historical_museum")
    assert mus.get("description")
    assert mus.get("history")
    assert mus.get("significance")
    assert mus.get("facts")


def test_victory_square_has_extra_images() -> None:
    vs = next(p for p in SMOLENSK_PLACES if p.get("slug") == "victory_square")
    extra = vs.get("additional_images") or []
    assert len(extra) == 2


def test_tram_removed() -> None:
    slugs = {p.get("slug") for p in SMOLENSK_PLACES}
    assert "tram_incline" not in slugs
