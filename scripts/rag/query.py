# -*- coding: utf-8 -*-
"""Query the local RAG index (cosine over hashed embeddings)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

import sys

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.rag.chunk_and_embed import embed_hash
from scripts.rag.config import rag_paths


@dataclass(frozen=True)
class RetrievedChunk:
    score: float
    chunk: dict[str, Any]


_NORM_RE = re.compile(r"[^A-Za-zА-Яа-яЁё0-9]+")


def _norm_key(text: str) -> str:
    s = _NORM_RE.sub(" ", text.lower()).strip()
    return " ".join(s.split())


_INDEX_CACHE: tuple[str, list[dict[str, Any]], np.ndarray, list[str]] | None = None


def _load_index(project_root: Path) -> tuple[list[dict[str, Any]], np.ndarray]:
    paths = rag_paths(project_root)
    meta_path = paths.index_dir / "chunks.jsonl"
    vec_path = paths.index_dir / "vectors.npy"
    if not meta_path.is_file() or not vec_path.is_file():
        return [], np.zeros((0, 0), dtype=np.float32)
    global _INDEX_CACHE
    cache_key = "{}:{}".format(
        int(meta_path.stat().st_mtime),
        int(vec_path.stat().st_mtime),
    )
    if _INDEX_CACHE and _INDEX_CACHE[0] == cache_key:
        return _INDEX_CACHE[1], _INDEX_CACHE[2]

    chunks: list[dict[str, Any]] = []
    blob_keys: list[str] = []
    for line in meta_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        ch = json.loads(line)
        chunks.append(ch)
        blob = "{}\n{}".format(
            str(ch.get("doc_title") or ""),
            str(ch.get("text") or ""),
        )
        blob_keys.append(_norm_key(blob))

    vec = np.load(vec_path)
    _INDEX_CACHE = (cache_key, chunks, vec, blob_keys)
    return chunks, vec


def retrieve(
    project_root: Path,
    *,
    query: str,
    city_slug: str | None = None,
    language: str | None = None,
    place: str | None = None,
    k: int = 8,
    dim: int = 512,
) -> list[RetrievedChunk]:
    chunks, vec = _load_index(project_root)
    if not chunks or vec.size == 0:
        return []
    qv = embed_hash(query, dim=dim)
    scores = vec @ qv  # cosine because vectors are normalized
    idxs = np.argsort(-scores)
    out: list[RetrievedChunk] = []
    place_norm = _norm_key(place or "")
    if place_norm:
        global _INDEX_CACHE
        blob_keys = _INDEX_CACHE[3] if _INDEX_CACHE else []
        # Prefer explicit City -> Place metadata when present (from local ingests).
        place_keys: list[str] = []
        if _INDEX_CACHE:
            place_keys = [_norm_key(str(c.get("place") or "")) for c in _INDEX_CACHE[1]]
        filtered: list[int] = []
        if place_keys:
            for i in idxs:
                if place_norm and place_norm in place_keys[int(i)]:
                    filtered.append(int(i))
        if not filtered:
            for i in idxs:
                if blob_keys and place_norm in blob_keys[int(i)]:
                    filtered.append(int(i))
        idxs = np.array(filtered, dtype=np.int64)
    for i in idxs:
        ch = chunks[int(i)]
        if city_slug and str(ch.get("city_slug")) != city_slug:
            continue
        if language and str(ch.get("language")) != language:
            continue
        out.append(RetrievedChunk(score=float(scores[int(i)]), chunk=ch))
        if len(out) >= k:
            break
    return out

