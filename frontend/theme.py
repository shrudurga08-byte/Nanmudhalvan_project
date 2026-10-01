"""LegalEase Streamlit theme. Same look as the HTML version (style.css):
dark surfaces, blue-violet accent, gold eyebrow, serif headings."""
import streamlit as st

_CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Source+Serif+4:wght@600;700&display=swap');

:root {
  --bg: #0a0c10;
  --bg-elevated: #12151c;
  --panel: #161a22;
  --panel-2: #1c212b;
  --border: #262c38;
  --border-soft: #1e232d;
  --text: #f3f4f7;
  --text-dim: #b7bec9;
  --muted: #7c8494;
  --accent: #5b8cff;
  --accent-2: #7c5bff;
  --gold: #d4af5f;
  --danger: #ff5c6a;
  --danger-soft: rgba(255, 92, 106, 0.12);
  --success: #34c98d;
  --success-soft: rgba(52, 201, 141, 0.12);
  --shadow-md: 0 10px 30px rgba(0, 0, 0, 0.4);
  --shadow-lift: 0 14px 40px rgba(91, 140, 255, 0.18);
}

html, body, .stApp, .stMarkdown, .stButton button, .stDownloadButton button,
input, textarea, label, [data-testid="stWidgetLabel"] {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

.stApp {
  background:
    radial-gradient(1100px 560px at 12% -8%, rgba(91, 140, 255, 0.10), transparent 60%),
    radial-gradient(900px 500px at 105% 5%, rgba(124, 91, 255, 0.07), transparent 55%),
    var(--bg);
  color: var(--text);
}

/* Clean chrome */
[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"], [data-testid="stDecoration"], #MainMenu, footer { display: none !important; }

.block-container, [data-testid="stMainBlockContainer"] {
  max-width: 820px;
  padding: 2.6rem 1.5rem 5rem;
}

/* ---------------- Hero ---------------- */
.le-hero { text-align: center; margin: 0 0 2.2rem; }
.le-eyebrow {
  display: inline-block; font-size: 11px; font-weight: 700;
  letter-spacing: 0.14em; color: var(--gold); margin-bottom: 16px;
}
.le-hero h1 {
  font-family: 'Source Serif 4', serif;
  font-size: 2.15rem !important; line-height: 1.25; font-weight: 700;
  margin: 0 0 14px; padding: 0; letter-spacing: -0.01em;
  background: linear-gradient(180deg, #ffffff 30%, #c7cede 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.le-hero-sub {
  color: var(--text-dim); font-size: 15px; max-width: 500px;
  margin: 0 auto 22px; line-height: 1.6;
}
.le-tags { display: flex; justify-content: center; gap: 8px; flex-wrap: wrap; }
.le-tag {
  font-size: 12px; font-weight: 600; padding: 6px 13px; border-radius: 999px;
  background: var(--panel); border: 1px solid var(--border); color: var(--text-dim);
}

/* ---------------- Cards ---------------- */
.st-key-form_card, .st-key-result_card, .st-key-export_card {
  background: linear-gradient(180deg, var(--panel) 0%, var(--panel-2) 100%);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1.8rem 1.8rem 1.5rem;
  margin-bottom: 1.6rem;
  box-shadow: var(--shadow-md);
}
.le-card-title { font-size: 17px; font-weight: 700; color: var(--text); margin: 0 0 4px; }
.le-card-sub { font-size: 13px; color: var(--muted); margin: 0 0 1.3rem; }

.le-badge {
  display: inline-flex; align-items: center; gap: 6px; padding: 6px 13px;
  border-radius: 999px; font-size: 12px; font-weight: 600;
  background: var(--success-soft); color: var(--success);
  border: 1px solid rgba(52, 201, 141, 0.25); margin-bottom: 1rem;
}

/* ---------------- Inputs ---------------- */
[data-testid="stWidgetLabel"] p {
  color: var(--text-dim); font-size: 12.5px; font-weight: 600; letter-spacing: 0.01em;
}
div[data-baseweb="input"], div[data-baseweb="textarea"] {
  background: var(--bg-elevated) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  transition: border-color .15s ease, box-shadow .15s ease;
}
div[data-baseweb="input"] > div, div[data-baseweb="base-input"] { background: transparent !important; }
div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea {
  color: var(--text) !important; font-size: 14px;
}
div[data-baseweb="input"]:focus-within, div[data-baseweb="textarea"]:focus-within {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(91, 140, 255, 0.14) !important;
}
::placeholder { color: #4a5160 !important; opacity: 1; }

/* ---------------- Buttons ---------------- */
.stButton > button, .stDownloadButton > button {
  background: var(--panel-2); color: var(--text);
  border: 1px solid var(--border); border-radius: 8px;
  padding: 0.6rem 1.1rem; font-weight: 600; letter-spacing: 0.01em;
  transition: transform .06s ease, border-color .15s ease, background .15s ease;
}
.stButton > button p, .stDownloadButton > button p { color: inherit; }
.stButton > button:hover, .stDownloadButton > button:hover {
  border-color: #3a4152; background: #20252f; color: var(--text);
}
.stDownloadButton > button:hover { border-color: var(--accent); color: var(--accent); }
.stButton > button:active, .stDownloadButton > button:active { transform: translateY(1px); }

.stButton > button[kind="primary"], button[data-testid="stBaseButton-primary"] {
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 100%);
  border-color: transparent; color: #fff;
  box-shadow: var(--shadow-lift);
  padding: 0.85rem 1.4rem; font-size: 0.95rem;
}
.stButton > button[kind="primary"]:hover, button[data-testid="stBaseButton-primary"]:hover {
  filter: brightness(1.08); border-color: transparent; color: #fff;
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 100%);
}

/* ---------------- Tabs ---------------- */
[data-baseweb="tab-list"] { gap: 0.4rem; }
button[data-baseweb="tab"] { background: transparent; color: var(--muted); font-weight: 600; }
button[data-baseweb="tab"][aria-selected="true"] { color: var(--text); }
[data-baseweb="tab-highlight"] { background: var(--accent) !important; }
[data-baseweb="tab-border"] { background: var(--border-soft) !important; }

/* ---------------- Preview ---------------- */
.le-preview {
  background: var(--bg-elevated); border: 1px solid var(--border);
  border-radius: 11px; padding: 22px 24px; max-height: 440px; overflow-y: auto;
  line-height: 1.68; font-size: 14px; color: var(--text-dim);
}
.le-preview h4 {
  margin: 20px 0 6px; color: var(--text); font-family: 'Source Serif 4', serif;
  font-size: 15px; font-weight: 700; padding-bottom: 6px;
  border-bottom: 1px solid var(--border-soft);
}
.le-preview h4:first-child { margin-top: 0; }
.le-preview p { margin: 8px 0; }
.le-export-label {
  font-size: 12px; font-weight: 600; color: var(--muted); text-transform: uppercase;
  letter-spacing: 0.06em; margin: 1.3rem 0 0.4rem; padding-top: 1.1rem;
  border-top: 1px solid var(--border-soft);
}

[data-testid="stAlert"] { border-radius: 10px; }

/* ---------------- Sidebar ---------------- */
[data-testid="stSidebar"] {
  background: var(--bg-elevated);
  border-right: 1px solid var(--border-soft);
}
.le-brand { display: flex; align-items: center; gap: 10px; margin: 0.4rem 0 1.8rem; }
.le-brand-icon {
  width: 34px; height: 34px; display: grid; place-items: center; border-radius: 9px;
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  color: #fff; font-size: 18px; box-shadow: 0 4px 14px rgba(91, 140, 255, 0.35);
}
.le-brand-name { font-family: 'Source Serif 4', serif; font-weight: 700; font-size: 18px; color: var(--text); }
.le-side-title {
  font-size: 11px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.09em; color: var(--muted); margin: 0 0 12px 4px;
}
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] { gap: 0.25rem; }
[data-testid="stSidebar"] .stButton > button {
  background: transparent; border: 1px solid transparent; color: var(--text-dim);
  font-weight: 500; font-size: 0.82rem; padding: 0.5rem 0.7rem; box-shadow: none;
}
[data-testid="stSidebar"] .stButton > button > div { justify-content: flex-start; width: 100%; }
[data-testid="stSidebar"] .stButton > button:hover {
  background: var(--panel); border-color: var(--border); color: var(--text);
}
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] > div:last-child .stButton > button > div {
  justify-content: center;
}
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] > div:last-child .stButton > button:hover {
  background: var(--danger-soft); border-color: transparent; color: var(--danger);
}
.le-status {
  margin-top: 1.4rem; padding-top: 1rem; border-top: 1px solid var(--border-soft);
  font-size: 12px; color: var(--muted); display: flex; align-items: center; gap: 7px;
}
.le-dot { width: 7px; height: 7px; border-radius: 50%; display: inline-block; }
.le-dot-on { background: var(--success); box-shadow: 0 0 0 3px var(--success-soft); }
.le-dot-off { background: var(--danger); box-shadow: 0 0 0 3px var(--danger-soft); }

.le-note { text-align: center; color: var(--muted); font-size: 12px; margin-top: 0.5rem; }

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 8px; }
::-webkit-scrollbar-track { background: transparent; }
"""


def apply_theme() -> None:
    st.markdown(f"<style>{_CSS}</style>", unsafe_allow_html=True)


def hero() -> None:
    st.markdown(
        '<div class="le-hero">'
        '<span class="le-eyebrow">AI-POWERED &middot; LEGAL DRAFTING</span>'
        "<h1>Draft precise legal documents<br/>in seconds, not hours.</h1>"
        '<p class="le-hero-sub">Enter the parties, terms and date. LegalEase structures a '
        "complete, formally worded document you can edit and export instantly.</p>"
        '<div class="le-tags"><span class="le-tag">Contracts</span><span class="le-tag">NDAs</span>'
        '<span class="le-tag">Lease Agreements</span><span class="le-tag">Offer Letters</span></div>'
        "</div>",
        unsafe_allow_html=True,
    )


def section_heading(title: str, sub: str = "") -> None:
    st.markdown(
        f'<div class="le-card-title">{title}</div><div class="le-card-sub">{sub}</div>',
        unsafe_allow_html=True,
    )


def status_badge(text: str) -> None:
    st.markdown(f'<div class="le-badge">&#10003; {text}</div>', unsafe_allow_html=True)


def sidebar_brand() -> None:
    st.markdown(
        '<div class="le-brand"><span class="le-brand-icon">&#9878;</span>'
        '<span class="le-brand-name">LegalEase</span></div>'
        '<div class="le-side-title">Document Library</div>',
        unsafe_allow_html=True,
    )


def sidebar_status(online: bool) -> None:
    dot = "le-dot-on" if online else "le-dot-off"
    label = "API connected" if online else "API offline"
    st.markdown(
        f'<div class="le-status"><span class="le-dot {dot}"></span>{label}</div>',
        unsafe_allow_html=True,
    )


def preview_box(inner_html: str) -> None:
    st.markdown(f'<div class="le-preview">{inner_html}</div>', unsafe_allow_html=True)


def export_label() -> None:
    st.markdown('<div class="le-export-label">Export as</div>', unsafe_allow_html=True)


def disclaimer() -> None:
    st.markdown(
        '<div class="le-note">LegalEase is an AI drafting aid, not legal advice. '
        "Have a qualified professional review any document before use.</div>",
        unsafe_allow_html=True,
    )