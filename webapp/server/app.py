# -*- coding: utf-8 -*-
"""FastAPI app: browse and edit city guides locally."""

from __future__ import annotations

import os
import subprocess
import threading
import time
from pathlib import Path
from typing import Any

from fastapi import Body
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from webapp.server.city_store import (
    apply_place_patch,
    cities_ui_order,
    city_paths,
    discover_cities,
    load_city_places,
)
from webapp.server.city_fonts import fonts_for_city
from webapp.server.city_emblems import emblems_for_city
from webapp.server.city_theme import CityTheme
from webapp.server.city_theme import theme_for_city
from webapp.server.llm import ollama_client
from webapp.server.llm import openai_client
from webapp.server.llm.types import PlaceDraft
from webapp.server.llm.types import coerce_links
from webapp.server.llm.types import coerce_str_list

from scripts.city_guide_heraldry_images import collect_heraldry_images
from scripts.city_guide_historical_reference_ru import (
    HERALDRY_CHAPTER_LABEL_RU,
    HISTORICAL_SECTION_TITLE_RU,
    reference_text_ru_for_any_city,
)
from scripts.guide_editor_presets import NEUTRAL_PALETTE
from scripts.guide_editor_presets import PAPER_PALETTE
from scripts.guide_editor_presets import static_font_profiles

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _theme_css_dict(theme: CityTheme) -> dict[str, str]:
    fc = theme.flag_c
    return {
        "bg_base": theme.bg_base,
        "flag_a": theme.flag_a,
        "flag_b": theme.flag_b,
        "flag_c": fc if fc else "transparent",
        "accent": theme.accent,
        "accent_2": theme.accent_2,
    }


def _city_dropdown_label(slug: str) -> str:
    """Label for <option> text; value stays the repo directory slug."""
    cleaned = slug.replace("-", "_").strip("_")
    if not cleaned:
        return slug
    parts = [p.capitalize() for p in cleaned.split("_") if p]
    return " ".join(parts) if parts else slug


templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
templates.env.filters["city_dropdown_label"] = _city_dropdown_label

app = FastAPI(title="Excursion Guide Editor", version="0.1.0")

app.mount(
    "/static",
    StaticFiles(directory=str(Path(__file__).parent / "static")),
    name="static",
)

_output_dir = PROJECT_ROOT / "output"
if _output_dir.is_dir():
    app.mount(
        "/moscow-media",
        StaticFiles(directory=str(_output_dir)),
        name="moscow-media",
    )


@app.get("/", include_in_schema=False)
def home() -> RedirectResponse:
    cities = discover_cities(PROJECT_ROOT)
    default = "moscow" if "moscow" in cities else "smolensk"
    return RedirectResponse(url="/{}".format(default), status_code=307)


@app.get("/api/cities")
def api_cities() -> dict[str, Any]:
    return {"cities": cities_ui_order(PROJECT_ROOT)}


@app.get("/api/{city_slug}/editor-presets")
def api_editor_presets(city_slug: str) -> dict[str, Any]:
    cities = discover_cities(PROJECT_ROOT)
    if city_slug not in cities:
        raise HTTPException(status_code=404, detail="Unknown city")
    fonts = fonts_for_city(city_slug)
    theme = theme_for_city(city_slug)
    city_default = {
        "id": "city_default",
        "label": "City default",
        "google_fonts_href": fonts.google_fonts_href,
        "title_font_family": fonts.title_font_family,
        "body_font_family": fonts.body_font_family,
    }
    return {
        "version": 1,
        "city_slug": city_slug,
        "flag_theme": _theme_css_dict(theme),
        "palettes": {
            "flag": None,
            "neutral": dict(NEUTRAL_PALETTE),
            "paper": dict(PAPER_PALETTE),
        },
        "font_profiles": [city_default] + static_font_profiles(),
    }


@app.get("/{city_slug}", response_class=HTMLResponse, include_in_schema=False)
def city_page(request: Request, city_slug: str) -> HTMLResponse:
    cities = discover_cities(PROJECT_ROOT)
    if city_slug not in cities:
        raise HTTPException(status_code=404, detail="Unknown city")
    fonts = fonts_for_city(city_slug)
    theme = theme_for_city(city_slug)
    emblems = emblems_for_city(PROJECT_ROOT, city_slug)
    return templates.TemplateResponse(
        "city.html",
        {
            "request": request,
            "city_slug": city_slug,
            "cities": cities_ui_order(PROJECT_ROOT),
            "fonts": fonts,
            "theme": theme,
            "emblems": emblems,
        },
    )


@app.get("/api/{city_slug}/guide-sections")
def api_guide_sections(city_slug: str) -> dict[str, Any]:
    """Heraldry assets + Russian historical blurb (same sources as PDF titul)."""
    cities = discover_cities(PROJECT_ROOT)
    if city_slug not in cities:
        raise HTTPException(status_code=404, detail="Unknown city")
    heraldry_images = collect_heraldry_images(PROJECT_ROOT, city_slug)
    if not heraldry_images:
        emblems = emblems_for_city(PROJECT_ROOT, city_slug)
        if emblems.city_emblem_url:
            heraldry_images.append(
                {
                    "src": emblems.city_emblem_url,
                    "alt": "Герб (guide_coat_of_arms)",
                }
            )
        if emblems.city_flag_url:
            heraldry_images.append(
                {
                    "src": emblems.city_flag_url,
                    "alt": "Флаг (guide_flag)",
                }
            )
    body = reference_text_ru_for_any_city(city_slug)
    paras = [p.strip() for p in body.split("\n\n") if p.strip()]
    return {
        "heraldry_title": HERALDRY_CHAPTER_LABEL_RU,
        "heraldry_images": heraldry_images,
        "history_title": HISTORICAL_SECTION_TITLE_RU,
        "history_paragraphs": paras,
    }


@app.get("/api/{city_slug}/places")
def api_places(city_slug: str) -> dict[str, Any]:
    cities = discover_cities(PROJECT_ROOT)
    if city_slug not in cities:
        raise HTTPException(status_code=404, detail="Unknown city")
    places = load_city_places(PROJECT_ROOT, city_slug)
    paths = city_paths(PROJECT_ROOT, city_slug)
    if city_slug == "moscow":
        media_base = "/moscow-media"
        images_root = str(PROJECT_ROOT / "output")
    else:
        media_base = "/city/{}".format(city_slug)
        images_root = str(paths.images_dir)
    for p in places:
        rel = str(p.get("image_rel_path") or "").replace("\\", "/").lstrip("/")
        if rel:
            p["image_url"] = "{}/{}".format(media_base, rel)
        extra = p.get("additional_images") or []
        if isinstance(extra, list):
            for it in extra:
                if not isinstance(it, dict):
                    continue
                r2 = (
                    str(it.get("image_rel_path") or "")
                    .replace("\\", "/")
                    .lstrip("/")
                )
                if r2:
                    it["image_url"] = "{}/{}".format(media_base, r2)
    return {
        "city": city_slug,
        "places": places,
        "images_root": images_root,
    }


@app.post("/api/{city_slug}/places/{slug}/apply")
def api_apply_patch(
    city_slug: str,
    slug: str,
    patch: dict[str, Any] = Body(...),
) -> dict[str, Any]:
    cities = discover_cities(PROJECT_ROOT)
    if city_slug not in cities:
        raise HTTPException(status_code=404, detail="Unknown city")
    if not slug:
        raise HTTPException(status_code=400, detail="Missing slug")
    overlay = apply_place_patch(PROJECT_ROOT, city_slug, slug, patch)
    return {"ok": True, "overlay": overlay.get(slug, {})}


def _mount_city_static() -> None:
    """
    Mount each city root under `/city/<slug>/` for images and other assets.

    We mount the whole city directory so `image_rel_path` like `images/foo.jpg`
    works without special-casing.
    """
    for city in discover_cities(PROJECT_ROOT):
        root = PROJECT_ROOT / city
        if not root.is_dir():
            continue
        app.mount(f"/city/{city}", StaticFiles(directory=str(root)), name=f"city-{city}")


_mount_city_static()

_PDF_JOBS_LOCK = threading.Lock()
_PDF_JOBS: dict[str, dict[str, Any]] = {}


@app.get("/api/llm/providers")
def api_llm_providers() -> dict[str, Any]:
    openai_enabled = bool(os.getenv("OPENAI_API_KEY"))
    return {
        "providers": [
            {"id": "ollama", "label": "Ollama (local)", "enabled": True},
            {"id": "openai", "label": "OpenAI", "enabled": openai_enabled},
        ]
    }


def _build_pdf_worker(city_slug: str) -> None:
    started = time.time()
    with _PDF_JOBS_LOCK:
        _PDF_JOBS[city_slug] = {"status": "running", "started_at": started}
    script = PROJECT_ROOT / "scripts" / f"build_{city_slug}_pdf.py"
    if not script.is_file():
        with _PDF_JOBS_LOCK:
            _PDF_JOBS[city_slug] = {
                "status": "failed",
                "reason": f"Missing script: {script}",
                "started_at": started,
                "finished_at": time.time(),
            }
        return
    cmd = ["python", str(script), "--html-only"]
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=60 * 20,
            check=False,
        )
    except Exception as exc:
        with _PDF_JOBS_LOCK:
            _PDF_JOBS[city_slug] = {
                "status": "failed",
                "reason": str(exc),
                "started_at": started,
                "finished_at": time.time(),
            }
        return
    ok = proc.returncode == 0
    with _PDF_JOBS_LOCK:
        _PDF_JOBS[city_slug] = {
            "status": "success" if ok else "failed",
            "returncode": proc.returncode,
            "stdout": (proc.stdout or "")[-8000:],
            "stderr": (proc.stderr or "")[-8000:],
            "started_at": started,
            "finished_at": time.time(),
        }


@app.post("/api/{city_slug}/build_pdf")
def api_build_pdf(city_slug: str) -> dict[str, Any]:
    cities = discover_cities(PROJECT_ROOT)
    if city_slug not in cities:
        raise HTTPException(status_code=404, detail="Unknown city")
    with _PDF_JOBS_LOCK:
        existing = _PDF_JOBS.get(city_slug)
        if existing and existing.get("status") == "running":
            return {"ok": True, "job": existing}
    t = threading.Thread(target=_build_pdf_worker, args=(city_slug,), daemon=True)
    t.start()
    return {"ok": True, "job": {"status": "running"}}


@app.get("/api/{city_slug}/build_pdf/status")
def api_build_pdf_status(city_slug: str) -> dict[str, Any]:
    with _PDF_JOBS_LOCK:
        job = _PDF_JOBS.get(city_slug) or {"status": "idle"}
    return {"ok": True, "job": job}


@app.get("/api/llm/ollama/models")
def api_ollama_models() -> dict[str, Any]:
    try:
        models = ollama_client.list_models()
    except Exception as exc:
        return {
            "models": [],
            "best": None,
            "error": f"Ollama unavailable: {exc}",
        }
    return {
        "models": [{"name": m.name, "score": m.score} for m in models],
        "best": ollama_client.best_model_name(models),
    }


@app.get("/api/llm/openai/models")
def api_openai_models() -> dict[str, Any]:
    enabled = bool(os.getenv("OPENAI_API_KEY"))
    # Conservative defaults; UI can also accept custom model names.
    return {
        "enabled": enabled,
        "models": [
            {"name": "gpt-4.1"},
            {"name": "gpt-4.1-mini"},
            {"name": "gpt-4o"},
            {"name": "gpt-4o-mini"},
        ],
        "best": "gpt-4.1-mini",
    }


def _find_place(city_slug: str, slug: str) -> dict[str, Any]:
    places = load_city_places(PROJECT_ROOT, city_slug)
    for p in places:
        if p.get("slug") == slug:
            return p
    raise HTTPException(status_code=404, detail="Unknown place slug")


def _draft_prompt(place: dict[str, Any]) -> list[dict[str, str]]:
    name = str(place.get("name_ru") or place.get("name_en") or place.get("slug") or "")
    subtitle = (
        str(place.get("subtitle_en") or "")
        or str(place.get("subtitle_de") or "")
        or str(place.get("subtitle_hu") or "")
    )
    context_bits: list[str] = []
    for key in ("address", "year_built", "architecture_style"):
        val = str(place.get(key) or "").strip()
        if val:
            context_bits.append(f"{key}: {val}")
    context = "\n".join(context_bits).strip()
    user = (
        "Tell me more about this place.\n\n"
        f"Place name: {name}\n"
        f"Subtitle: {subtitle}\n"
        f"{context}\n\n"
        "Separate facts from stories.\n"
        "Return JSON with this shape:\n"
        "{\n"
        '  \"facts\": [\"...\"],\n'
        '  \"stories\": [\"...\"],\n'
        '  \"suggested_body\": {\n'
        '    \"description\": \"...\",\n'
        '    \"history\": \"...\",\n'
        '    \"significance\": \"...\"\n'
        "  },\n"
        '  \"suggested_links\": [{\"label\": \"...\", \"url\": \"...\"}]\n'
        "}\n\n"
        "If you are unsure about a claim, put it under stories (not facts) or omit it."
    )
    return [
        {
            "role": "system",
            "content": (
                "You are helping edit a city guide. Avoid inventing facts. "
                "Keep facts short and verifiable. Stories can be folklore/legends."
            ),
        },
        {"role": "user", "content": user},
    ]


@app.post("/api/llm/draft")
def api_llm_draft(payload: dict[str, Any] = Body(...)) -> PlaceDraft:
    city_slug = str(payload.get("city_slug") or "").strip()
    slug = str(payload.get("slug") or "").strip()
    provider = str(payload.get("provider") or "ollama").strip()
    model = str(payload.get("model") or "").strip()
    if not city_slug or city_slug not in discover_cities(PROJECT_ROOT):
        raise HTTPException(status_code=404, detail="Unknown city")
    if not slug:
        raise HTTPException(status_code=400, detail="Missing slug")

    place = _find_place(city_slug, slug)
    messages = _draft_prompt(place)

    parsed: dict[str, Any] | None = None
    raw_text = ""
    if provider == "ollama":
        if not model:
            models = ollama_client.list_models()
            model = ollama_client.best_model_name(models) or ""
        if not model:
            raise HTTPException(status_code=503, detail="No Ollama models found")
        try:
            parsed, raw_text = ollama_client.chat_json(model=model, messages=messages)
        except Exception as exc:
            raise HTTPException(status_code=503, detail=f"Ollama error: {exc}")
    elif provider == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            raise HTTPException(status_code=403, detail="OPENAI_API_KEY not set")
        if not model:
            model = "gpt-4.1-mini"
        try:
            parsed, raw_text = openai_client.chat_json(model=model, messages=messages)
        except Exception as exc:
            raise HTTPException(status_code=503, detail=f"OpenAI error: {exc}")
    else:
        raise HTTPException(status_code=400, detail="Unknown provider")

    facts = coerce_str_list((parsed or {}).get("facts"))
    stories = coerce_str_list((parsed or {}).get("stories"))
    body = (parsed or {}).get("suggested_body")
    if not isinstance(body, dict):
        body = {}
    suggested_body: dict[str, str] = {}
    for k in ("description", "history", "significance"):
        v = str(body.get(k, "")).strip()
        if v:
            suggested_body[k] = v
    links = coerce_links((parsed or {}).get("suggested_links"))
    return {
        "facts": facts,
        "stories": stories,
        "suggested_body": suggested_body,
        "suggested_links": links,
        "raw_text": raw_text,
        "provider": provider,
        "model": model,
    }

