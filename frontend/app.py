import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import requests
import streamlit as st

from ai_core.generator import format_docx, format_html_preview, format_pdf, sanitize_text
from config import API_URL
from theme import (
    apply_theme, disclaimer, hero, preview_box,
    section_heading, sidebar_brand, sidebar_status, status_badge,
)

st.set_page_config(page_title="LegalEase | AI Legal Document Generator",
                   page_icon="⚖️", layout="centered")
apply_theme()

for key, default in {
    "generated_text": "", "doc_id": None, "doc_type": "", "terms": "",
    "show_edit": False, "doc_version": 0, "just_generated": False,
}.items():
    st.session_state.setdefault(key, default)


def api(method: str, path: str, **kw):
    return requests.request(method, f"{API_URL}{path}", timeout=120, **kw)


def load_document(doc_id: int):
    r = api("GET", f"/documents/{doc_id}")
    if r.ok:
        d = r.json()
        st.session_state.update(
            generated_text=d["document"], doc_id=d["id"], doc_type=d["document_type"],
            terms=d["terms"], show_edit=False, just_generated=False,
            doc_version=st.session_state.doc_version + 1,
        )


# ---------------------------------------------------------------- sidebar
with st.sidebar:
    sidebar_brand()
    online = True
    try:
        docs = api("GET", "/documents").json()
        if not docs:
            st.caption("Nothing saved yet.")
        for d in docs:
            c1, c2 = st.columns([5, 1])
            label = f"{d['document_type']} ({d['created_at'][:10]})"
            if c1.button(label, key=f"load_{d['id']}", use_container_width=True):
                load_document(d["id"])
                st.rerun()
            if c2.button("🗑", key=f"del_{d['id']}"):
                api("DELETE", f"/documents/{d['id']}")
                if st.session_state.doc_id == d["id"]:
                    st.session_state.generated_text = ""
                    st.session_state.doc_id = None
                st.rerun()
    except requests.RequestException:
        online = False
        st.warning("Backend not reachable.")
    sidebar_status(online)

# ---------------------------------------------------------------- header
hero()

# ---------------------------------------------------------------- inputs
with st.container(key="form_card"):
    section_heading("1. Describe your document",
                    "Fill in the essentials. The AI handles the legal structure.")

    document_type = st.text_input(
        "Document Type  (e.g. Agreement, Contract, NDA)",
        placeholder="Freelance Work Contract")

    col_parties, col_date = st.columns([1.4, 1])
    parties = col_parties.text_area(
        "Parties Involved", height=110,
        placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)")
    dates = col_date.text_input("Effective Date", placeholder="April 15, 2025")

    terms = st.text_area(
        "Terms & Conditions  (use semicolons to separate clauses)", height=130,
        placeholder="Payment within 7 days of invoice; Confidentiality must be maintained; "
                    "Either party may terminate with 15 days notice")

    if st.button("✨ Generate Document", type="primary", use_container_width=True):
        if not (document_type.strip() and parties.strip() and dates.strip()):
            st.error("Please fill in Document Type, Parties Involved and Effective Date.")
        else:
            try:
                with st.spinner("Generating with Gemini..."):
                    r = api("POST", "/generate", json={
                        "document_type": document_type, "parties": parties,
                        "terms": terms, "dates": dates,
                    })
                if r.ok:
                    data = r.json()
                    st.session_state.update(
                        generated_text=sanitize_text(data["document"]), doc_id=data["id"],
                        doc_type=document_type, terms=terms, show_edit=False,
                        just_generated=True,
                        doc_version=st.session_state.doc_version + 1,
                    )
                else:
                    st.error(r.json().get("detail", r.text))
            except requests.RequestException as e:
                st.error(f"Could not reach the backend at {API_URL}: {e}")

# ---------------------------------------------------------------- output
if not st.session_state.generated_text:
    st.info("Click 'Generate Document' to start")
else:
    with st.container(key="result_card"):
        section_heading("2. Review & edit",
                        "Preview the draft and edit it if needed.")
        if st.session_state.just_generated:
            status_badge("Generated successfully")

        tab_preview, tab_edit = st.tabs(["📄 Preview", "✏️ Edit"])

        # Edit tab is filled first so the preview always shows the latest text.
        with tab_edit:
            st.session_state.generated_text = st.text_area(
                "Edit document below", value=st.session_state.generated_text, height=350,
                key=f"editor_{st.session_state.doc_version}",
                label_visibility="collapsed",
            )
            if st.session_state.doc_id and st.button("💾 Save changes"):
                r = api("PUT", f"/documents/{st.session_state.doc_id}",
                        json={"content": st.session_state.generated_text})
                if r.ok:
                    st.success("Saved.")
                else:
                    st.error("Could not save.")

        with tab_preview:
            preview_box(format_html_preview(st.session_state.generated_text))

# ---------------------------------------------------------------- export (always visible)
text = st.session_state.generated_text
doc_type = st.session_state.doc_type or "Legal Document"
tterms = st.session_state.terms
fname = re.sub(r"[^a-z0-9]+", "_", doc_type.lower()).strip("_") or "document"
has_doc = bool(text)


def build(fn):
    """Build an export file; return (bytes, error) so one failure never hides the others."""
    if not has_doc:
        return b"", None
    try:
        return fn(text, doc_type, tterms), None
    except Exception as e:  # noqa: BLE001
        return b"", e


docx_bytes, docx_err = build(format_docx)
pdf_bytes, pdf_err = build(format_pdf)

with st.container(key="export_card"):
    section_heading("3. Export",
                    "Download your document as TXT, DOCX or PDF." if has_doc
                    else "Generate or open a document to enable downloads.")
    d1, d2, d3 = st.columns(3)
    d1.download_button("📄 TXT", data=text or "", file_name=f"{fname}.txt",
                       mime="text/plain", use_container_width=True, disabled=not has_doc)
    d2.download_button(
        "📝 DOCX", data=docx_bytes, file_name=f"{fname}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True, disabled=(not has_doc) or docx_err is not None)
    d3.download_button("📕 PDF", data=pdf_bytes, file_name=f"{fname}.pdf",
                       mime="application/pdf", use_container_width=True,
                       disabled=(not has_doc) or pdf_err is not None)
    if docx_err is not None:
        st.warning(f"DOCX export failed: {docx_err}")
    if pdf_err is not None:
        st.warning(f"PDF export failed: {pdf_err}")

disclaimer()