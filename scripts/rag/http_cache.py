# -*- coding: utf-8 -*-
"""Simple filesystem HTTP cache for RAG fetchers."""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests

from scripts.rag.config import DEFAULT_USER_AGENT


@dataclass(frozen=True)
class CachedResponse:
    url: str
    status_code: int
    headers: dict[str, str]
    retrieved_at: float
    body: bytes

    def json(self) -> Any:
        return json.loads(self.body.decode("utf-8"))

    def text(self) -> str:
        return self.body.decode("utf-8", errors="replace")


def _key_for_url(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def _path_for_key(cache_dir: Path, key: str) -> Path:
    return cache_dir / "{}.json".format(key)


def fetch_cached(
    url: str,
    *,
    cache_dir: Path,
    timeout_sec: int = 60,
    sleep_sec: float = 0.0,
    force: bool = False,
    headers: dict[str, str] | None = None,
    retries: int = 2,
    backoff_sec: float = 2.0,
) -> CachedResponse:
    """
    GET a URL with caching.

    Stores JSON envelope: {url, status_code, headers, retrieved_at, body_b64}.
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    key = _key_for_url(url)
    path = _path_for_key(cache_dir, key)
    if path.is_file() and not force:
        blob = json.loads(path.read_text(encoding="utf-8"))
        return CachedResponse(
            url=str(blob["url"]),
            status_code=int(blob["status_code"]),
            headers=dict(blob.get("headers") or {}),
            retrieved_at=float(blob["retrieved_at"]),
            body=bytes.fromhex(str(blob["body_hex"])),
        )
    if sleep_sec > 0:
        time.sleep(sleep_sec)
    merged = {"User-Agent": DEFAULT_USER_AGENT}
    if headers:
        merged.update(headers)
    last_exc: Exception | None = None
    attempt = 0
    while True:
        attempt += 1
        try:
            resp = requests.get(url, headers=merged, timeout=timeout_sec)
            break
        except (requests.Timeout, requests.ConnectionError) as exc:
            last_exc = exc
            if attempt > retries + 1:
                raise
            time.sleep(max(0.0, backoff_sec) * attempt)
    if last_exc:
        # Keep mypy happy; we either broke with resp or raised.
        pass
    cr = CachedResponse(
        url=url,
        status_code=int(resp.status_code),
        headers={k: v for k, v in resp.headers.items()},
        retrieved_at=time.time(),
        body=resp.content,
    )
    path.write_text(
        json.dumps(
            {
                "url": cr.url,
                "status_code": cr.status_code,
                "headers": cr.headers,
                "retrieved_at": cr.retrieved_at,
                "body_hex": cr.body.hex(),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return cr

