# -*- coding: utf-8 -*-
"""
Core utilities: exceptions, logging, validation.

Single module for cross-cutting concerns (DRY, SOLID).
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any, Optional


class ExcursionError(Exception):
    """Base exception for Excursion project."""

    pass


class GuideError(ExcursionError):
    """Invalid guide config or data."""

    pass


class DownloadError(ExcursionError):
    """Image download failed."""

    pass


class ValidationError(ExcursionError):
    """Data or file validation failed."""

    pass


def setup_logging(
    level: int = logging.INFO,
    stream: Any = None,
) -> logging.Logger:
    """Configure project logging. Returns root logger."""
    stream = stream or sys.stderr
    fmt = logging.Formatter("%(levelname)s: %(message)s")
    h = logging.StreamHandler(stream)
    h.setFormatter(fmt)
    root = logging.getLogger("excursion")
    root.handlers.clear()
    root.addHandler(h)
    root.setLevel(level)
    return root


def validate_place(place: dict[str, Any]) -> None:
    """Validate place dict has required keys. Raises ValidationError."""
    required = {"name", "address", "images", "lat", "lon"}
    missing = required - set(place.keys())
    if missing:
        raise ValidationError(
            "Place missing keys {}: {!r}".format(missing, place.get("name", "?")),
        )
    if not isinstance(place.get("images"), list):
        raise ValidationError("Place images must be list: {!r}".format(place.get("name")))
    lat, lon = place.get("lat"), place.get("lon")
    if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
        raise ValidationError(
            "Place lat/lon must be numbers: {!r}".format(place.get("name")),
        )


def ensure_utf8_console() -> None:
    """Fix Windows console for Cyrillic output."""
    if sys.platform != "win32":
        return
    import io
    for name, stream in [("stdout", sys.stdout), ("stderr", sys.stderr)]:
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except (AttributeError, OSError):
                pass
        elif hasattr(stream, "buffer"):
            try:
                wrapper = io.TextIOWrapper(
                    stream.buffer, encoding="utf-8", errors="replace",
                )
                setattr(sys, name, wrapper)
            except (AttributeError, OSError):
                pass


def project_root() -> Path:
    """Return project root directory."""
    return Path(__file__).resolve().parent.parent


def load_env() -> None:
    """Load .env file if python-dotenv available."""
    try:
        from dotenv import load_dotenv
        load_dotenv(project_root() / ".env")
    except ImportError:
        pass


def validate_image_slots(
    place: dict[str, Any],
    slug: str,
) -> list[str]:
    """
    Validate place has all 4 image slots (_1.._4) and map coordinates.
    Returns list of errors (empty if valid).
    """
    errors: list[str] = []
    name = place.get("name", "?")
    images = place.get("images", [])
    basenames = [
        img.split("/")[-1] if "/" in img else img for img in images
    ]
    standard = [
        bn for bn in basenames
        if bn.endswith("_1.jpg") or bn.endswith("_2.jpg") or
        bn.endswith("_3.jpg") or bn.endswith("_4.jpg")
    ]

    expected = [
        "{}_1.jpg".format(slug),
        "{}_2.jpg".format(slug),
        "{}_3.jpg".format(slug),
        "{}_4.jpg".format(slug),
    ]
    missing = [e for e in expected if e not in basenames]
    if missing:
        errors.append(
            "{}: missing image slots: {}".format(name, missing),
        )

    # Check map
    lat, lon = place.get("lat"), place.get("lon")
    if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
        errors.append(
            "{}: invalid map coordinates (lat/lon)".format(name),
        )
    elif not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        errors.append(
            "{}: map coordinates out of range: {}, {}".format(name, lat, lon),
        )

    return errors


def save_checkpoint(
    checkpoint_file: Path,
    data: dict[str, Any],
) -> None:
    """Save checkpoint data for resume capability."""
    import json
    try:
        checkpoint_file.parent.mkdir(parents=True, exist_ok=True)
        checkpoint_file.write_text(
            json.dumps(data, indent=2), encoding="utf-8",
        )
    except OSError as e:
        logging.getLogger("excursion").warning(
            "Failed to save checkpoint {}: {}".format(checkpoint_file, e),
        )


def load_checkpoint(
    checkpoint_file: Path,
) -> Optional[dict[str, Any]]:
    """Load checkpoint data. Returns None if not found or invalid."""
    import json
    if not checkpoint_file.exists():
        return None
    try:
        return json.loads(checkpoint_file.read_text(encoding="utf-8"))
    except Exception:
        return None
