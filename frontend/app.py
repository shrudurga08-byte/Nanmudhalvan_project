import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import requests
import streamlit as st

from ai_core.generator import format_docx, format_html_preview, format_pdf, sanitize_text
from config import API_URL, LOGO_PATH

st.set_page_config(page_title="LegalEase", layout="centered")

for key, default in {
    "generated_text": "", "doc_id": None, "doc_type": "", "terms": "",
    "show_edit": False, "doc_version": 0,
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
            terms=d["terms"], show_edit=False,
            doc_version=st.session_state.doc_version + 1,
        )


# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.subheader("Saved documents")
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
        st.warning("Backend not reachable.")

# ---------------------------------------------------------------- header
_, mid, _ = st.columns([1, 2, 1])
with mid:
    if Path(LOGO_PATH).exists():
        st.image(str(LOGO_PATH), use_container_width=True)
st.markdown("<h2 style='text-align:center;'>AI Legal Document Generator</h2>",
            unsafe_allow_html=True)

# ---------------------------------------------------------------- inputs
document_type = st.text_input("Document Type (Ex: Agreement, Contract, NDA)")
parties = st.text_area("Parties Involved")
terms = st.text_area("Terms & Conditions (Use semicolons for bullet points)")
dates = st.text_input("Effective Date")

if st.button("Generate Document"):
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
                    doc_version=st.session_state.doc_version + 1,
                )
                st.success("Document Generated Successfully!")
            else:
                st.error(r.json().get("detail", r.text))
        except requests.RequestException as e:
            st.error(f"Could not reach the backend at {API_URL}: {e}")

# ---------------------------------------------------------------- output
if not st.session_state.generated_text:
    st.info("Click 'Generate Document' to start")
else:
    if st.button("✏️ Click to Edit Document"):
        st.session_state.show_edit = not st.session_state.show_edit

    if st.session_state.show_edit:
        st.session_state.generated_text = st.text_area(
            "Edit Document Below:", value=st.session_state.generated_text, height=350,
            key=f"editor_{st.session_state.doc_version}",
        )
        if st.session_state.doc_id and st.button("💾 Save changes"):
            r = api("PUT", f"/documents/{st.session_state.doc_id}",
                    json={"content": st.session_state.generated_text})
            st.success("Saved.") if r.ok else st.error("Could not save.")

    text = st.session_state.generated_text
    styled = format_html_preview(text)
    st.markdown(
        "<div style='background:#0e1117;border:1px solid #2b2f3a;border-radius:8px;"
        f"padding:16px;max-height:420px;overflow-y:auto;color:#ddd'>{styled}</div>",
        unsafe_allow_html=True,
    )

    doc_type = st.session_state.doc_type or "Legal Document"
    tterms = st.session_state.terms
    fname = re.sub(r"[^a-z0-9]+", "_", doc_type.lower()).strip("_") or "document"

    st.download_button("📄 Download as .TXT", data=text, file_name=f"{fname}.txt",
                       mime="text/plain")
    st.download_button(
        "📝 Download as .DOCX", data=format_docx(text, doc_type, tterms),
        file_name=f"{fname}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    st.download_button("📕 Download as .PDF", data=format_pdf(text, doc_type, tterms),
                       file_name=f"{fname}.pdf", mime="application/pdf")