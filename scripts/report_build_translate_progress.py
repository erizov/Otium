# -*- coding: utf-8 -*-
"""Print translation/build progress for long Ollama guide runs."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent
LOG = _SCRIPT_DIR / "build_all_pdfs_translate_log.txt"
SMOKE_LOG = _SCRIPT_DIR / "barcelona_ru_smoke.log"
CACHE = _PROJECT_ROOT / ".cache" / "city_guide_translate.json"


def _cache_count() -> int:
    if not CACHE.is_file():
        return 0
    try:
        data = json.loads(CACHE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return 0
    return len(data) if isinstance(data, dict) else 0


def _log_tail(path: Path, n: int = 8) -> list[str]:
    if not path.is_file():
        return []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return lines[-n:]


def _last_city_progress(lines: list[str]) -> str:
    for line in reversed(lines):
        m = re.search(r"\[(\d+)/(\d+)\]\s+Building\s+(\S+)", line)
        if m:
            return "city {}/{}: {}".format(m.group(1), m.group(2), m.group(3))
    return "no city marker yet"


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    cache_n = _cache_count()
    smoke = _log_tail(SMOKE_LOG)
    build = _log_tail(LOG)
    print("=== guide build progress {} ===".format(now))
    print("translation cache entries: {}".format(cache_n))
    if smoke:
        print("barcelona smoke: {}".format(smoke[-1][:120]))
    else:
        print("barcelona smoke: not started or no log yet")
    if build:
        print("full build: {}".format(_last_city_progress(build)))
        print("last log lines:")
        for line in build:
            print("  " + line[:160])
    else:
        print("full build: waiting (log empty)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
