# -*- coding: utf-8 -*-
"""Tests for trusted official/tourism image host parsing."""

from __future__ import annotations

from pathlib import Path

from scripts.city_guide_trusted_image_sources import trusted_image_hosts


def test_trusted_hosts_skip_facts_only(tmp_path: Path) -> None:
    md = tmp_path / "SOURCES_WHITELIST.md"
    md.write_text(
        "\n".join([
            "## Images",
            "- https://upload.wikimedia.org/",
            "## Facts",
            "- https://www.unesco.org/",
            "- https://en.wikipedia.org/",
            "- https://www.visitberlin.de/",
            "- https://www.museuminsel.berlin/",
        ]),
        encoding="utf-8",
    )
    hosts = trusted_image_hosts(md)
    assert "www.visitberlin.de" in hosts
    assert "www.museuminsel.berlin" in hosts
    assert "www.unesco.org" not in hosts
    assert "en.wikipedia.org" not in hosts
