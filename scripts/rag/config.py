# -*- coding: utf-8 -*-
"""RAG configuration and common paths (local-only)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RagPaths:
    """Filesystem layout for local caches and indices."""

    project_root: Path

    @property
    def cache_root(self) -> Path:
        return self.project_root / ".rag_cache"

    @property
    def http_cache_dir(self) -> Path:
        return self.cache_root / "http"

    @property
    def docs_dir(self) -> Path:
        return self.cache_root / "docs"

    @property
    def index_dir(self) -> Path:
        return self.cache_root / "index"

    @property
    def outputs_dir(self) -> Path:
        return self.project_root / "rag_outputs"


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def rag_paths(root: Path | None = None) -> RagPaths:
    return RagPaths(project_root=(root or project_root()).resolve())


DEFAULT_USER_AGENT = (
    "ExcursionCityRAG/0.1 (local-only city guide RAG; "
    "contact: see repo README)"
)

