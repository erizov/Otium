# -*- coding: utf-8 -*-
"""GigaChat API client (OAuth + chat completions)."""

from __future__ import annotations

import json
import logging
import os
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from typing import Any

logger = logging.getLogger(__name__)

_OAUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
_CHAT_URL = (
    "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
)
_DEFAULT_SCOPE = "GIGACHAT_API_PERS"
_TOKEN_TTL_SEC = 25 * 60

_token_cache: dict[str, Any] = {"value": "", "expires_at": 0.0}


def _ssl_context() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def _load_credentials() -> str:
    key = os.environ.get("GIGA_AUTH_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "GIGA_AUTH_KEY is not set (add it to .env at project root).",
        )
    return key


def get_gigachat_access_token(*, force_refresh: bool = False) -> str:
    """Return a cached OAuth access token (refreshed every ~25 minutes)."""
    now = time.time()
    if (
        not force_refresh
        and _token_cache["value"]
        and now < float(_token_cache["expires_at"])
    ):
        return str(_token_cache["value"])

    credentials = _load_credentials()
    body = urllib.parse.urlencode({"scope": _DEFAULT_SCOPE}).encode("utf-8")
    req = urllib.request.Request(
        _OAUTH_URL,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": str(uuid.uuid4()),
            "Authorization": "Basic {}".format(credentials),
        },
    )
    try:
        with urllib.request.urlopen(
            req, context=_ssl_context(), timeout=90,
        ) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            "GigaChat OAuth failed ({}): {}".format(exc.code, detail),
        ) from exc

    token = str(raw.get("access_token") or "").strip()
    if not token:
        raise RuntimeError("GigaChat OAuth: empty access_token in response")
    _token_cache["value"] = token
    _token_cache["expires_at"] = now + _TOKEN_TTL_SEC
    return token


def ask_gigachat(question: str, model: str = "GigaChat") -> str:
    """
    Send one user message to GigaChat and return assistant text.

    Uses ``GIGA_AUTH_KEY`` from the environment (Base64 client credentials).
    """
    token = get_gigachat_access_token()
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": question}],
        "temperature": 0.7,
        "max_tokens": 512,
        "stream": False,
    }

    def _post(bearer: str) -> dict[str, Any]:
        inner = urllib.request.Request(
            _CHAT_URL,
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers={
                "Authorization": "Bearer {}".format(bearer),
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )
        with urllib.request.urlopen(
            inner, context=_ssl_context(), timeout=120,
        ) as resp:
            return json.loads(resp.read().decode("utf-8"))

    try:
        raw = _post(token)
    except urllib.error.HTTPError as exc:
        if exc.code == 401:
            token = get_gigachat_access_token(force_refresh=True)
            try:
                raw = _post(token)
            except urllib.error.HTTPError as exc2:
                detail = exc2.read().decode("utf-8", errors="replace")
                return "Ошибка {}: {}".format(exc2.code, detail)
        else:
            detail = exc.read().decode("utf-8", errors="replace")
            return "Ошибка {}: {}".format(exc.code, detail)

    choices = raw.get("choices") or []
    if not choices:
        return "Ошибка: пустой ответ GigaChat"
    message = choices[0].get("message") or {}
    content = message.get("content")
    if isinstance(content, str):
        return content.strip()
    return "Ошибка: нет текста в ответе GigaChat"
