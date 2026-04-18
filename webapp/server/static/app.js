/* global window, document, fetch */

function el(id) {
  return document.getElementById(id);
}

function normalizeText(s) {
  return (s || "").toString().toLowerCase().trim();
}

function placeName(place) {
  return (
    place.name_ru ||
    place.name_en ||
    place.name ||
    place.slug ||
    "Untitled"
  ).toString();
}

function placeSubtitle(place) {
  return (
    place.subtitle_en ||
    place.subtitle_de ||
    place.subtitle_hu ||
    place.subtitle_es ||
    place.subtitle_it ||
    place.subtitle_fr ||
    ""
  ).toString();
}

function renderProse(place) {
  const parts = [];
  if (place.description) {
    parts.push(`<h3>Description</h3><div>${escapeHtml(place.description)}</div>`);
  }
  if (place.facts && place.facts.length) {
    parts.push(`<h3>Facts</h3><ul>${place.facts
      .map((x) => `<li>${escapeHtml(x)}</li>`)
      .join("")}</ul>`);
  }
  if (place.stories && place.stories.length) {
    parts.push(`<h3>Stories</h3><ul>${place.stories
      .map((x) => `<li>${escapeHtml(x)}</li>`)
      .join("")}</ul>`);
  }
  if (place.history) {
    parts.push(`<h3>History</h3><div>${escapeHtml(place.history)}</div>`);
  }
  if (place.significance) {
    parts.push(`<h3>Significance</h3><div>${escapeHtml(place.significance)}</div>`);
  }
  if (place.more_information && place.more_information.length) {
    const lis = place.more_information
      .map((x) => {
        const label = (x.label || x.url || "").toString();
        const url = (x.url || "").toString();
        if (!url) return "";
        return `<li><a href="${escapeAttr(url)}" target="_blank" rel="noreferrer noopener">${escapeHtml(label)}</a></li>`;
      })
      .filter(Boolean)
      .join("");
    if (lis) parts.push(`<h3>More information</h3><ul>${lis}</ul>`);
  }
  if (!parts.length) return `<div class="muted">No content yet.</div>`;
  return parts.join("");
}

function escapeHtml(s) {
  const t = (s || "").toString();
  return t
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function escapeAttr(s) {
  return escapeHtml(s).replaceAll("'", "&#39;");
}

function splitLines(s) {
  return (s || "")
    .toString()
    .split(/\r?\n/)
    .map((x) => x.trim())
    .filter(Boolean);
}

function joinLines(items) {
  return (items || []).join("\n");
}

async function jsonGet(url) {
  const res = await fetch(url);
  if (!res.ok) {
    let detail = "";
    try {
      const data = await res.json();
      detail = data.detail || data.error || JSON.stringify(data);
    } catch {
      try {
        detail = await res.text();
      } catch {
        detail = "";
      }
    }
    const msg = detail ? `HTTP ${res.status}: ${detail}` : `HTTP ${res.status}`;
    throw new Error(msg);
  }
  return await res.json();
}

async function jsonPost(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body || {}),
  });
  if (!res.ok) {
    let detail = "";
    try {
      const data = await res.json();
      detail = data.detail || data.error || JSON.stringify(data);
    } catch {
      try {
        detail = await res.text();
      } catch {
        detail = "";
      }
    }
    const msg = detail ? `HTTP ${res.status}: ${detail}` : `HTTP ${res.status}`;
    throw new Error(msg);
  }
  return await res.json();
}

const APPEARANCE_LS_KEY = "excursionEditorAppearance";
const APPEARANCE_VERSION = 1;
const EMPTY_FONT_STYLESHEET = "data:text/css,body{}";

let appearancePresets = null;

function loadSavedAppearance() {
  try {
    const raw = localStorage.getItem(APPEARANCE_LS_KEY);
    if (!raw) return null;
    const o = JSON.parse(raw);
    if (o.v !== APPEARANCE_VERSION) return null;
    return {
      palette: o.palette || "flag",
      fontProfile: o.fontProfile || "city_default",
      scale: o.scale != null ? String(o.scale) : "1",
    };
  } catch {
    return null;
  }
}

function persistAppearance(cur) {
  localStorage.setItem(
    APPEARANCE_LS_KEY,
    JSON.stringify({
      v: APPEARANCE_VERSION,
      palette: cur.palette,
      fontProfile: cur.fontProfile,
      scale: cur.scale,
    })
  );
}

function readAppearanceFromForm() {
  const p = document.querySelector(
    'input[name="appearancePalette"]:checked'
  );
  const f = document.querySelector('input[name="appearanceFont"]:checked');
  const s = document.querySelector('input[name="appearanceScale"]:checked');
  return {
    palette: (p && p.value) || "flag",
    fontProfile: (f && f.value) || "city_default",
    scale: (s && s.value) || "1",
  };
}

function setAppearanceFormValues(cur) {
  const names = [
    ["appearancePalette", cur.palette],
    ["appearanceFont", cur.fontProfile],
    ["appearanceScale", cur.scale],
  ];
  names.forEach(([name, val]) => {
    const elRadio = document.querySelector(
      `input[name="${name}"][value="${val}"]`
    );
    if (elRadio) elRadio.checked = true;
  });
}

function applyThemeColors(paletteId) {
  if (!appearancePresets) return;
  const root = document.documentElement;
  if (paletteId === "paper") {
    root.setAttribute("data-palette", "paper");
  } else {
    root.removeAttribute("data-palette");
  }
  let theme;
  if (paletteId === "flag") {
    theme = appearancePresets.flag_theme;
  } else if (paletteId === "neutral") {
    theme = appearancePresets.palettes.neutral;
  } else {
    theme = appearancePresets.palettes.paper;
  }
  root.style.setProperty("--bg", theme.bg_base);
  root.style.setProperty("--flag-a", theme.flag_a);
  root.style.setProperty("--flag-b", theme.flag_b);
  root.style.setProperty("--flag-c", theme.flag_c);
  root.style.setProperty("--accent", theme.accent);
  root.style.setProperty("--accent-2", theme.accent_2);
}

function applyFontProfile(profileId) {
  if (!appearancePresets) return;
  const profs = appearancePresets.font_profiles || [];
  const p = profs.find((x) => x.id === profileId);
  if (!p) return;
  const root = document.documentElement;
  root.style.setProperty("--city-title-font", p.title_font_family);
  root.style.setProperty("--city-body-font", p.body_font_family);
  const link = document.getElementById("editor-fonts-link");
  if (link) {
    if (p.google_fonts_href) {
      link.href = p.google_fonts_href;
    } else {
      link.href = EMPTY_FONT_STYLESHEET;
    }
  }
}

function applyScale(scaleStr) {
  document.documentElement.style.setProperty(
    "--editor-scale",
    scaleStr || "1"
  );
}

function refreshAppearanceFromForm() {
  const cur = readAppearanceFromForm();
  applyThemeColors(cur.palette);
  applyFontProfile(cur.fontProfile);
  applyScale(cur.scale);
  persistAppearance(cur);
}

async function initAppearance() {
  appearancePresets = await jsonGet(
    `/api/${encodeURIComponent(state.city)}/editor-presets`
  );
  const defaults = {
    palette: "flag",
    fontProfile: "city_default",
    scale: "1",
  };
  const saved = loadSavedAppearance();
  const cur = saved
    ? {
        palette: saved.palette,
        fontProfile: saved.fontProfile,
        scale: saved.scale,
      }
    : defaults;
  setAppearanceFormValues(cur);
  applyThemeColors(cur.palette);
  applyFontProfile(cur.fontProfile);
  applyScale(cur.scale);

  ["appearancePalette", "appearanceFont", "appearanceScale"].forEach(
    (name) => {
      document.querySelectorAll(`input[name="${name}"]`).forEach((inp) => {
        inp.addEventListener("change", () => refreshAppearanceFromForm());
      });
    }
  );
  const resetBtn = document.getElementById("appearanceResetBtn");
  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      localStorage.removeItem(APPEARANCE_LS_KEY);
      setAppearanceFormValues(defaults);
      applyThemeColors(defaults.palette);
      applyFontProfile(defaults.fontProfile);
      applyScale(defaults.scale);
      persistAppearance(defaults);
    });
  }
}

let state = {
  city: window.__CITY__ || "smolensk",
  places: [],
  place: null,
  providers: [],
  ollamaModels: [],
  openaiModels: [],
  bestOllama: null,
  bestOpenai: null,
};

function setStatus(text, kind) {
  const s = el("applyStatus");
  if (!s) return;
  s.textContent = text || "";
  s.className = `status ${kind === "bad" ? "" : "muted"}`;
}

function renderDraft(draft) {
  const facts = (draft.facts || []).slice(0, 30);
  const stories = (draft.stories || []).slice(0, 30);
  const body = draft.suggested_body || {};
  const links = (draft.suggested_links || []).slice(0, 20);

  const fLis = facts.length
    ? `<ul>${facts.map((x) => `<li>${escapeHtml(x)}</li>`).join("")}</ul>`
    : `<div class="muted">No facts returned.</div>`;
  const sLis = stories.length
    ? `<ul>${stories.map((x) => `<li>${escapeHtml(x)}</li>`).join("")}</ul>`
    : `<div class="muted">No stories returned.</div>`;

  const bodyBits = [];
  if (body.description)
    bodyBits.push(
      `<div class="pill good">description</div><div class="muted">${escapeHtml(
        body.description
      )}</div>`
    );
  if (body.history)
    bodyBits.push(
      `<div class="pill good">history</div><div class="muted">${escapeHtml(
        body.history
      )}</div>`
    );
  if (body.significance)
    bodyBits.push(
      `<div class="pill good">significance</div><div class="muted">${escapeHtml(
        body.significance
      )}</div>`
    );

  const linksLis = links.length
    ? `<ul>${links
        .map((l) => {
          const label = (l.label || l.url || "").toString();
          const url = (l.url || "").toString();
          if (!url) return "";
          return `<li><a href="${escapeAttr(
            url
          )}" target="_blank" rel="noreferrer noopener">${escapeHtml(
            label
          )}</a></li>`;
        })
        .filter(Boolean)
        .join("")}</ul>`
    : `<div class="muted">No links returned.</div>`;

  return `
    <div class="row">
      <div class="pill">provider: ${escapeHtml(draft.provider || "")}</div>
      <div class="pill">model: ${escapeHtml(draft.model || "")}</div>
    </div>
    <div class="row" style="margin-top:10px">
      <div class="grow">
        <div class="pill good">Facts</div>
        ${fLis}
      </div>
      <div class="grow">
        <div class="pill">Stories</div>
        ${sLis}
      </div>
    </div>
    <div style="margin-top:10px">
      <div class="pill">Suggested body</div>
      ${bodyBits.length ? bodyBits.join("<div style='height:10px'></div>") : `<div class="muted">No body suggestions.</div>`}
    </div>
    <div style="margin-top:10px">
      <div class="pill">Suggested links</div>
      ${linksLis}
    </div>
  `;
}

function renderPlaceList(filterText) {
  const list = el("placeList");
  const q = normalizeText(filterText);
  const items = state.places.filter((p) => {
    if (!q) return true;
    return (
      normalizeText(placeName(p)).includes(q) ||
      normalizeText(p.slug).includes(q) ||
      normalizeText(placeSubtitle(p)).includes(q)
    );
  });

  list.innerHTML = items
    .map((p) => {
      const active = state.place && state.place.slug === p.slug ? "active" : "";
      const meta = [p.category, p.slug].filter(Boolean).join(" · ");
      return `<div class="place-item ${active}" data-slug="${escapeAttr(
        p.slug || ""
      )}">
        <div class="name">${escapeHtml(placeName(p))}</div>
        <div class="meta">${escapeHtml(meta)}</div>
      </div>`;
    })
    .join("");

  list.querySelectorAll(".place-item").forEach((node) => {
    node.addEventListener("click", () => {
      const slug = node.getAttribute("data-slug");
      selectPlace(slug);
    });
  });
}

function renderPlace(place) {
  el("placeTitle").textContent = placeName(place);
  el("placeSubtitle").textContent = placeSubtitle(place);

  const imgWrap = el("placeImages");
  const images = [];
  if (place.image_url) images.push({ url: place.image_url, kind: "main" });
  const extras = place.additional_images || [];
  extras.forEach((x, idx) => {
    if (x && x.image_url) images.push({ url: x.image_url, kind: "extra", idx });
  });

  imgWrap.innerHTML = images
    .slice(0, 5)
    .map((img) => {
      const btn =
        img.kind === "extra"
          ? `<button data-del="${img.idx}" title="Remove image">×</button>`
          : "";
      return `<div class="place-image">
        ${btn}
        <img src="${escapeAttr(img.url)}" loading="lazy" alt="${escapeAttr(
          placeName(place)
        )}" />
      </div>`;
    })
    .join("");

  imgWrap.querySelectorAll("button[data-del]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const idx = parseInt(btn.getAttribute("data-del"), 10);
      await deleteExtraImage(idx);
    });
  });

  if (images.length < 5) {
    const addBtn = document.createElement("button");
    addBtn.className = "button";
    addBtn.textContent = "Add image…";
    addBtn.addEventListener("click", () => addExtraImage());
    imgWrap.appendChild(addBtn);
  }

  el("currentContent").innerHTML = renderProse(place);

  el("descEdit").value = place.description || "";
  el("historyEdit").value = place.history || "";
  el("sigEdit").value = place.significance || "";
  el("factsEdit").value = joinLines(place.facts || []);
  el("storiesEdit").value = joinLines(place.stories || []);
  const links = (place.more_information || []).map((x) => {
    const label = (x.label || "").toString().trim();
    const url = (x.url || "").toString().trim();
    if (!url) return "";
    return `${label} | ${url}`.trim();
  });
  el("linksEdit").value = joinLines(links.filter(Boolean));

  el("draftArea").innerHTML = `<div class="pill">No draft yet.</div>`;
}

async function deleteExtraImage(idx) {
  if (!state.place) return;
  const extras = (state.place.additional_images || []).filter(
    (x) => x && x.image_rel_path
  );
  const editor = extras
    .map((x) => ({
      image_rel_path: x.image_rel_path,
      image_source_url: x.image_source_url || "",
    }))
    .filter((x) => x.image_rel_path);
  editor.splice(idx, 1);
  await jsonPost(`/api/${state.city}/places/${state.place.slug}/apply`, {
    editor_images: editor,
  });
  await loadPlaces();
  selectPlace(state.place.slug);
}

async function addExtraImage() {
  if (!state.place) return;
  const rel = (
    window.prompt("Image rel path (e.g. images/foo.jpg)") || ""
  ).trim();
  if (!rel) return;
  const src = (window.prompt("Image source URL (optional)") || "").trim();
  const existing = (state.place.additional_images || []).filter(
    (x) => x && x.image_rel_path
  );
  const editor = existing
    .map((x) => ({
      image_rel_path: x.image_rel_path,
      image_source_url: x.image_source_url || "",
    }))
    .filter((x) => x.image_rel_path);
  if (editor.length >= 4) {
    window.alert("Max 5 images total (1 main + 4 extra).");
    return;
  }
  editor.push({ image_rel_path: rel, image_source_url: src });
  await jsonPost(`/api/${state.city}/places/${state.place.slug}/apply`, {
    editor_images: editor,
  });
  await loadPlaces();
  selectPlace(state.place.slug);
}

function selectPlace(slug) {
  const place = state.places.find((p) => p.slug === slug) || state.places[0];
  state.place = place;
  renderPlaceList(el("search").value);
  renderPlace(place);
  setStatus("", "ok");
}

async function loadProviders() {
  const data = await jsonGet("/api/llm/providers").catch(() => null);
  state.providers = (data && data.providers) || [];
  const haveOllama = state.providers.some((p) => p && p.id === "ollama");
  const haveOpenai = state.providers.some((p) => p && p.id === "openai");
  if (!haveOllama) {
    state.providers.unshift({ id: "ollama", label: "Ollama (local)", enabled: true });
  }
  if (!haveOpenai) {
    state.providers.push({ id: "openai", label: "OpenAI", enabled: false });
  }
  const sel = el("providerSelect");
  sel.innerHTML = state.providers
    .map((p) => {
      const label = p.enabled
        ? (p.label || p.id)
        : `${p.label || p.id} (set OPENAI_API_KEY)`;
      return `<option value="${escapeAttr(p.id)}">${escapeHtml(label)}</option>`;
    })
    .join("");
}

function setModelOptions(models, bestName) {
  const sel = el("modelSelect");
  const opts = (models || []).map((m) => {
    const name = m.name || m;
    return `<option value="${escapeAttr(name)}">${escapeHtml(name)}</option>`;
  });
  opts.push(`<option value="__custom__">Custom…</option>`);
  sel.innerHTML = opts.join("");
  if (bestName) sel.value = bestName;
}

async function loadModelsForProvider(providerId) {
  if (providerId === "openai") {
    const openai = await jsonGet("/api/llm/openai/models").catch(() => null);
    state.openaiModels =
      (openai && openai.models) || [
        { name: "gpt-4.1" },
        { name: "gpt-4.1-mini" },
        { name: "gpt-4o" },
        { name: "gpt-4o-mini" },
      ];
    state.bestOpenai = (openai && openai.best) || "gpt-4.1-mini";
    setModelOptions(state.openaiModels, state.bestOpenai);
    return;
  }

  const ollama = await jsonGet("/api/llm/ollama/models").catch(() => null);
  state.ollamaModels = (ollama && ollama.models) || [];
  state.bestOllama = (ollama && ollama.best) || null;
  setModelOptions(state.ollamaModels, state.bestOllama);
  if (ollama && ollama.error) {
    el("draftArea").innerHTML = `<div class="pill bad">${escapeHtml(
      ollama.error
    )}</div>`;
  }
}

async function generateDraft() {
  if (!state.place) return;
  const provider = el("providerSelect").value;
  let model = el("modelSelect").value;
  if (model === "__custom__") {
    model = window.prompt("Enter model name") || "";
  }
  el("draftArea").innerHTML = `<div class="pill">Generating…</div>`;
  try {
    const draft = await jsonPost("/api/llm/draft", {
      city_slug: state.city,
      slug: state.place.slug,
      provider,
      model,
    });
    el("draftArea").innerHTML = renderDraft(draft);

    const body = draft.suggested_body || {};
    if (body.description && !el("descEdit").value.trim())
      el("descEdit").value = body.description;
    if (body.history && !el("historyEdit").value.trim())
      el("historyEdit").value = body.history;
    if (body.significance && !el("sigEdit").value.trim())
      el("sigEdit").value = body.significance;
    if (draft.facts && draft.facts.length && !el("factsEdit").value.trim())
      el("factsEdit").value = joinLines(draft.facts);
    if (draft.stories && draft.stories.length && !el("storiesEdit").value.trim())
      el("storiesEdit").value = joinLines(draft.stories);
    if (
      draft.suggested_links &&
      draft.suggested_links.length &&
      !el("linksEdit").value.trim()
    ) {
      el("linksEdit").value = joinLines(
        draft.suggested_links.map((l) => `${l.label} | ${l.url}`)
      );
    }
  } catch (err) {
    el("draftArea").innerHTML = `<div class="pill bad">Failed: ${escapeHtml(
      err.message || err.toString()
    )}</div>`;
  }
}

async function loadPlaces() {
  const data = await jsonGet(`/api/${state.city}/places`);
  state.places = data.places || [];
  renderPlaceList("");
  selectPlace((state.places[0] || {}).slug);
}

function getModeValue(name) {
  const nodes = document.querySelectorAll(`input[name="${name}"]`);
  for (const n of nodes) {
    if (n.checked) return n.value;
  }
  return "replace";
}

function applyMode(current, incoming, mode) {
  const a = (current || "").toString().trim();
  const b = (incoming || "").toString().trim();
  if (!b) return a;
  if (mode === "append" && a) return `${a}\n\n${b}`;
  return b;
}

function parseLinks(lines) {
  return lines
    .map((line) => {
      const parts = line.split("|").map((x) => x.trim());
      if (parts.length === 1) {
        const url = parts[0];
        return url ? { label: url, url } : null;
      }
      const label = parts[0];
      const url = parts.slice(1).join(" | ").trim();
      return url ? { label: label || url, url } : null;
    })
    .filter(Boolean);
}

async function applyEdits() {
  if (!state.place) return;
  const slug = state.place.slug;
  const patch = {};

  const descMode = getModeValue("descMode");
  const historyMode = getModeValue("historyMode");
  const sigMode = getModeValue("sigMode");

  patch.description = applyMode(
    state.place.description,
    el("descEdit").value,
    descMode
  );
  patch.history = applyMode(
    state.place.history,
    el("historyEdit").value,
    historyMode
  );
  patch.significance = applyMode(
    state.place.significance,
    el("sigEdit").value,
    sigMode
  );
  patch.facts = splitLines(el("factsEdit").value);
  patch.stories = splitLines(el("storiesEdit").value);
  patch.more_information = parseLinks(splitLines(el("linksEdit").value));

  setStatus("Applying…", "ok");
  try {
    await jsonPost(`/api/${state.city}/places/${slug}/apply`, patch);
    await loadPlaces();
    selectPlace(slug);
    setStatus("Saved to overlay JSON.", "ok");
  } catch (err) {
    setStatus(`Failed: ${err.message || err}`, "bad");
  }
}

async function init() {
  await initAppearance();

  el("citySelect").addEventListener("change", () => {
    const city = el("citySelect").value;
    window.location.href = `/${encodeURIComponent(city)}`;
  });

  el("search").addEventListener("input", () => {
    renderPlaceList(el("search").value);
  });

  el("applyBtn").addEventListener("click", () => {
    applyEdits();
  });

  el("providerSelect").addEventListener("change", async () => {
    await loadModelsForProvider(el("providerSelect").value);
  });

  el("generateBtn").addEventListener("click", () => {
    generateDraft();
  });

  const buildBtn = el("buildPdfBtn");
  if (buildBtn) {
    buildBtn.addEventListener("click", () => {
      buildPdf();
    });
  }

  await loadProviders();
  await loadModelsForProvider(el("providerSelect").value);
  await loadPlaces();
}

async function buildPdf() {
  const st = el("buildPdfStatus");
  if (st) st.textContent = "Starting build…";
  try {
    await jsonPost(`/api/${state.city}/build_pdf`, {});
  } catch (err) {
    if (st) st.textContent = `Failed to start: ${err.message || err}`;
    return;
  }
  const started = Date.now();
  while (Date.now() - started < 1000 * 60 * 20) {
    await new Promise((r) => setTimeout(r, 1200));
    let data = null;
    try {
      data = await jsonGet(`/api/${state.city}/build_pdf/status`);
    } catch (err) {
      if (st) st.textContent = `Status error: ${err.message || err}`;
      continue;
    }
    const job = (data && data.job) || {};
    if (job.status === "running") {
      if (st) st.textContent = "Building…";
      continue;
    }
    if (job.status === "success") {
      if (st) st.textContent = "Build OK.";
      return;
    }
    if (job.status === "failed") {
      const reason = (job.stderr || job.reason || "Unknown failure").toString();
      if (st) st.textContent = `Build failed: ${reason.slice(0, 300)}`;
      return;
    }
    if (st) st.textContent = "Idle.";
    return;
  }
  if (st) st.textContent = "Build timed out.";
}

init().catch((err) => {
  document.body.innerHTML = `<pre>${escapeHtml(err.stack || err.toString())}</pre>`;
});

