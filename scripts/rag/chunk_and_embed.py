# -*- coding: utf-8 -*-
"""Chunk RAG documents and build a lightweight local embeddings index."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.rag.config import rag_paths

_WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё0-9][A-Za-zА-Яа-яЁё0-9'’\\-]+")


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    doc_id: str
    city_slug: str
    language: str
    source_name: str
    source_url: str
    license: str
    doc_title: str
    place: str
    section_hint: str
    text: str


def _iter_doc_files(docs_dir: Path) -> list[Path]:
    if not docs_dir.is_dir():
        return []
    out: list[Path] = []
    for p in sorted(docs_dir.rglob("*.json")):
        if p.is_file():
            out.append(p)
    return out


def _load_doc(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _estimate_tokens(text: str) -> int:
    # Rough heuristic: 1 token ~= 4 chars for Latin/Cyrillic prose.
    return max(1, int(math.ceil(len(text) / 4.0)))


def _split_paragraphs(text: str) -> list[str]:
    chunks = [t.strip() for t in text.split("\n\n") if t.strip()]
    return chunks


def chunk_document(
    doc: dict[str, Any],
    *,
    target_tokens: int,
    overlap_tokens: int,
) -> list[Chunk]:
    text = str(doc.get("text") or "").strip()
    if not text:
        return []
    paras = _split_paragraphs(text)
    buf: list[str] = []
    out: list[Chunk] = []
    buf_tokens = 0
    idx = 0

    def flush() -> None:
        nonlocal idx
        if not buf:
            return
        joined = "\n\n".join(buf).strip()
        if not joined:
            return
        idx += 1
        cid = "{}:{}".format(str(doc.get("doc_id") or "doc"), idx)
        out.append(
            Chunk(
                chunk_id=cid,
                doc_id=str(doc.get("doc_id") or ""),
                city_slug=str(doc.get("city_slug") or ""),
                language=str(doc.get("language") or ""),
                source_name=str(doc.get("source_name") or ""),
                source_url=str(doc.get("source_url") or ""),
                license=str(doc.get("license") or ""),
                doc_title=str(doc.get("title") or ""),
                place=str((doc.get("extra") or {}).get("place") or "city_overview"),
                section_hint=str(doc.get("source_name") or ""),
                text=joined,
            )
        )

    for p in paras:
        pt = _estimate_tokens(p)
        if buf_tokens + pt > target_tokens and buf:
            flush()
            # overlap tail
            if overlap_tokens > 0:
                tail: list[str] = []
                t_tokens = 0
                for prev in reversed(buf):
                    tt = _estimate_tokens(prev)
                    if t_tokens + tt > overlap_tokens:
                        break
                    tail.append(prev)
                    t_tokens += tt
                buf = list(reversed(tail))
                buf_tokens = t_tokens
            else:
                buf = []
                buf_tokens = 0
        buf.append(p)
        buf_tokens += pt
    flush()
    return out


def embed_hash(text: str, *, dim: int = 512) -> np.ndarray:
    """
    Deterministic, lightweight “embedding” via hashed token projections.

    This is not a semantic SOTA model, but it is local-only, fast, and
    sufficient to build an index and size accounting without external services.
    """
    v = np.zeros((dim,), dtype=np.float32)
    toks = _WORD_RE.findall(text.lower())
    if not toks:
        return v
    for t in toks:
        h = hash(t)
        idx = h % dim
        sign = 1.0 if (h & 1) else -1.0
        v[idx] += sign
    norm = float(np.linalg.norm(v))
    if norm > 0:
        v /= norm
    return v


def build_index(
    *,
    project_root: Path,
    target_tokens: int,
    overlap_tokens: int,
    dim: int,
) -> tuple[list[Chunk], np.ndarray]:
    paths = rag_paths(project_root)
    docs = _iter_doc_files(paths.docs_dir)
    chunks: list[Chunk] = []
    for dp in docs:
        doc = _load_doc(dp)
        chunks.extend(
            chunk_document(
                doc,
                target_tokens=target_tokens,
                overlap_tokens=overlap_tokens,
            )
        )
    if not chunks:
        return [], np.zeros((0, dim), dtype=np.float32)
    mat = np.zeros((len(chunks), dim), dtype=np.float32)
    for i, ch in enumerate(chunks):
        mat[i] = embed_hash(ch.text, dim=dim)
    return chunks, mat


def _write_index(
    project_root: Path,
    *,
    chunks: list[Chunk],
    vectors: np.ndarray,
) -> None:
    paths = rag_paths(project_root)
    paths.index_dir.mkdir(parents=True, exist_ok=True)
    meta_path = paths.index_dir / "chunks.jsonl"
    vec_path = paths.index_dir / "vectors.npy"
    meta_path.write_text(
        "".join(
            json.dumps(
                {
                    "chunk_id": c.chunk_id,
                    "doc_id": c.doc_id,
                    "city_slug": c.city_slug,
                    "language": c.language,
                    "source_name": c.source_name,
                    "source_url": c.source_url,
                    "license": c.license,
                    "doc_title": c.doc_title,
                    "place": c.place,
                    "section_hint": c.section_hint,
                    "text": c.text,
                },
                ensure_ascii=False,
            )
            + "\n"
            for c in chunks
        ),
        encoding="utf-8",
    )
    np.save(vec_path, vectors)


def _size_report(project_root: Path) -> dict[str, Any]:
    paths = rag_paths(project_root)
    docs = _iter_doc_files(paths.docs_dir)
    doc_bytes = sum(p.stat().st_size for p in docs)
    idx_meta = paths.index_dir / "chunks.jsonl"
    idx_vec = paths.index_dir / "vectors.npy"
    meta_bytes = idx_meta.stat().st_size if idx_meta.is_file() else 0
    vec_bytes = idx_vec.stat().st_size if idx_vec.is_file() else 0
    return {
        "docs_files": len(docs),
        "docs_bytes": doc_bytes,
        "index_meta_bytes": meta_bytes,
        "index_vec_bytes": vec_bytes,
        "total_bytes": doc_bytes + meta_bytes + vec_bytes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help="Repo root (default: auto).",
    )
    parser.add_argument("--target-tokens", type=int, default=800)
    parser.add_argument("--overlap-tokens", type=int, default=120)
    parser.add_argument("--dim", type=int, default=512)
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Print current cached sizes; do not rebuild index.",
    )
    args = parser.parse_args()
    root = (
        args.project_root.resolve()
        if args.project_root
        else Path(__file__).resolve().parent.parent.parent
    )
    if args.report_only:
        print(json.dumps(_size_report(root), ensure_ascii=False, indent=2))
        return 0
    chunks, vec = build_index(
        project_root=root,
        target_tokens=int(args.target_tokens),
        overlap_tokens=int(args.overlap_tokens),
        dim=int(args.dim),
    )
    if not chunks:
        print(
            "No RAG documents found. Run scripts/rag/fetch_sources.py first.",
            file=sys.stderr,
        )
        return 2
    _write_index(root, chunks=chunks, vectors=vec)
    print(json.dumps(_size_report(root), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

