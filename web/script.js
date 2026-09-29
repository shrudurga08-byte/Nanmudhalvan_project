const API_URL = "http://localhost:8000"; // change if backend runs elsewhere

const el = (id) => document.getElementById(id);
const state = { docId: null, docType: "", terms: "", generatedText: "", editing: false };

function showToast(message, type = "") {
  const toast = el("toast");
  toast.textContent = message;
  toast.className = `toast ${type}`;
  setTimeout(() => toast.classList.add("hidden"), 3500);
}

function slugify(text) {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/^_+|_+$/g, "") || "document";
}

function sanitizeText(text) {
  if (!text) return "";
  const replacements = { "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"', "\u2013": "-", "\u2014": "-", "\u2026": "...", "\u2022": "-", "\u00a0": " " };
  let out = text;
  for (const [oldC, newC] of Object.entries(replacements)) out = out.split(oldC).join(newC);
  out = out.replace(/\*\*(.*?)\*\*/g, "$1").replace(/^\s*#{1,6}\s*/gm, "").replace(/^\s*\*\s+/gm, "- ").replace(/`/g, "");
  return out.trim();
}

function isHeading(line) {
  const s = line.trim();
  if (!s || s.length > 80) return false;
  return /^\d+\.\s+[^.]{2,80}:?$/.test(s) || s.endsWith(":") || (s === s.toUpperCase() && /[A-Z]/.test(s) && s.length > 3);
}
function isBullet(line) { const s = line.trim(); return s.startsWith("- ") || s.startsWith("* "); }
function escapeHtml(str) { const div = document.createElement("div"); div.textContent = str; return div.innerHTML; }

function renderPreview(text) {
  const lines = sanitizeText(text).split("\n");
  let html = "";
  for (const raw of lines) {
    const line = raw.trim();
    if (!line) continue;
    if (isBullet(line)) html += `<p style="margin:2px 0 2px 20px">&bull; ${escapeHtml(line.slice(2))}</p>`;
    else if (isHeading(line)) html += `<h4>${escapeHtml(line)}</h4>`;
    else html += `<p>${escapeHtml(line)}</p>`;
  }
  return html;
}

async function api(method, path, body) {
  const res = await fetch(`${API_URL}${path}`, {
    method,
    headers: body ? { "Content-Type": "application/json" } : undefined,
    body: body ? JSON.stringify(body) : undefined,
  });
  let data = null;
  try { data = await res.json(); } catch (_) {}
  if (!res.ok) throw new Error((data && data.detail) || res.statusText);
  return data;
}

async function loadDocumentList() {
  const list = el("doc-list");
  try {
    const docs = await api("GET", "/documents");
    if (!docs.length) { list.innerHTML = `<p class="muted">Nothing saved yet.</p>`; return; }
    list.innerHTML = "";
    docs.forEach((d) => {
      const row = document.createElement("div");
      row.className = "doc-item";
      const openBtn = document.createElement("button");
      openBtn.className = "doc-btn";
      openBtn.textContent = `${d.document_type} (${d.created_at.slice(0, 10)})`;
      openBtn.onclick = () => loadDocument(d.id);
      const delBtn = document.createElement("button");
      delBtn.className = "del-btn";
      delBtn.textContent = "🗑";
      delBtn.onclick = async (e) => {
        e.stopPropagation();
        await api("DELETE", `/documents/${d.id}`);
        if (state.docId === d.id) resetResult();
        loadDocumentList();
      };
      row.append(openBtn, delBtn);
      list.appendChild(row);
    });
  } catch (e) {
    list.innerHTML = `<p class="muted">Backend not reachable.</p>`;
  }
}

async function loadDocument(id) {
  try {
    const d = await api("GET", `/documents/${id}`);
    Object.assign(state, { docId: d.id, docType: d.document_type, terms: d.terms, generatedText: d.document, editing: false });
    renderResult();
  } catch (e) { showToast(e.message, "error"); }
}

function resetResult() {
  state.docId = null;
  state.generatedText = "";
  el("resultSection").classList.add("hidden");
}

el("generateBtn").addEventListener("click", async () => {
  const documentType = el("documentType").value.trim();
  const parties = el("parties").value.trim();
  const terms = el("terms").value.trim();
  const dates = el("effectiveDate").value.trim();
  const errorEl = el("formError");

  if (!documentType || !parties || !dates) {
    errorEl.textContent = "Please fill in Document Type, Parties Involved and Effective Date.";
    errorEl.classList.remove("hidden");
    return;
  }
  errorEl.classList.add("hidden");

  const btn = el("generateBtn");
  btn.disabled = true;
  btn.textContent = "Generating with Gemini...";
  try {
    const data = await api("POST", "/generate", { document_type: documentType, parties, terms, dates });
    Object.assign(state, { docId: data.id, docType: documentType, terms, generatedText: sanitizeText(data.document), editing: false });
    renderResult(true);
    loadDocumentList();
  } catch (e) {
    errorEl.textContent = e.message;
    errorEl.classList.remove("hidden");
  } finally {
    btn.disabled = false;
    btn.textContent = "Generate Document";
  }
});

function renderResult(justGenerated = false) {
  el("resultSection").classList.remove("hidden");
  el("statusBadge").classList.toggle("hidden", !justGenerated);
  el("editorWrap").classList.add("hidden");
  el("saveBtn").classList.add("hidden");
  el("editor").value = state.generatedText;
  el("preview").innerHTML = renderPreview(state.generatedText);
}

el("editToggleBtn").addEventListener("click", () => {
  state.editing = !state.editing;
  el("editorWrap").classList.toggle("hidden", !state.editing);
  el("saveBtn").classList.toggle("hidden", !state.editing || !state.docId);
  if (state.editing) el("editor").value = state.generatedText;
});

el("editor").addEventListener("input", (e) => {
  state.generatedText = e.target.value;
  el("preview").innerHTML = renderPreview(state.generatedText);
});

el("saveBtn").addEventListener("click", async () => {
  if (!state.docId) return;
  try {
    await api("PUT", `/documents/${state.docId}`, { content: state.generatedText });
    showToast("Saved.", "success");
  } catch (e) { showToast(e.message, "error"); }
});

function triggerDownload(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = filename;
  document.body.appendChild(a); a.click(); a.remove();
  URL.revokeObjectURL(url);
}

el("downloadTxt").addEventListener("click", () => {
  triggerDownload(new Blob([state.generatedText], { type: "text/plain" }), `${slugify(state.docType || "document")}.txt`);
});
el("downloadDocx").addEventListener("click", () => downloadFormatted("docx"));
el("downloadPdf").addEventListener("click", () => downloadFormatted("pdf"));

async function downloadFormatted(kind) {
  if (!state.docId) { showToast("Generate a document first.", "error"); return; }
  try {
    const res = await fetch(`${API_URL}/documents/${state.docId}/export/${kind}`);
    if (!res.ok) throw new Error(`Export failed (${res.status})`);
    const blob = await res.blob();
    triggerDownload(blob, `${slugify(state.docType || "document")}.${kind}`);
  } catch (e) { showToast(e.message, "error"); }
}

loadDocumentList();