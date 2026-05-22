# -*- coding: utf-8 -*-
"""Convenience: fetch → chunk+embed → (optional) translate enrich → rebuild."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help="Repo root (default: auto).",
    )
    parser.add_argument(
        "--cities",
        nargs="*",
        default=None,
        metavar="SLUG",
        help="Limit to city slugs (default: all discovered).",
    )
    parser.add_argument(
        "--include-wikivoyage",
        action="store_true",
        help="Fetch Wikivoyage too.",
    )
    parser.add_argument(
        "--translate-city",
        default=None,
        metavar="SLUG",
        help="Run translate enrichment for one city (optional).",
    )
    args = parser.parse_args()
    root = args.project_root.resolve() if args.project_root else _project_root()

    cmd = [sys.executable, str(root / "scripts" / "rag" / "fetch_sources.py")]
    if args.cities:
        cmd.extend(["--cities"] + list(args.cities))
    if args.include_wikivoyage:
        cmd.append("--include-wikivoyage")
    rc = subprocess.run(cmd, cwd=str(root), check=False).returncode
    if rc != 0:
        return int(rc)

    rc = subprocess.run(
        [sys.executable, str(root / "scripts" / "rag" / "chunk_and_embed.py")],
        cwd=str(root),
        check=False,
    ).returncode
    if rc != 0:
        return int(rc)

    if args.translate_city:
        rc = subprocess.run(
            [
                sys.executable,
                str(root / "scripts" / "rag" / "translate_enrich.py"),
                "--city",
                str(args.translate_city),
            ],
            cwd=str(root),
            check=False,
        ).returncode
        if rc != 0:
            return int(rc)
        rc = subprocess.run(
            [sys.executable, str(root / "scripts" / "rag" / "chunk_and_embed.py")],
            cwd=str(root),
            check=False,
        ).returncode
        if rc != 0:
            return int(rc)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

