# app.py
import streamlit as st
from pathlib import Path
import re
import pickle
from typing import Tuple

# --------- Helpers / Simple Classifier (fallback) ----------
OFFENSIVE_WORDS = {
    "goblok","anjing","bego","tolol","idiot","bodoh","jelek","gk","gk bagus","kntl","asu",
    "kampret","tolol","sange","tai","brengsek","brengsek","kontol","ngentot"
}

def simple_rule_based(text: str) -> int:
    """Return 1 if bullying, 0 if non-bullying using a tiny keyword heuristic."""
    text_low = text.lower()
    # Remove punctuation for matching
    words = re.findall(r"\w+", text_low)
    for w in words:
        if w in OFFENSIVE_WORDS:
            return 1
    # short heuristic: many insulting patterns
    insulting_patterns = ["jelek", "bodoh", "goblok", "kamu tolol", "gk becus", "mampus"]
    for p in insulting_patterns:
        if p in text_low:
            return 1
    return 0

def load_model(model_path: Path, vect_path: Path = None):
    """Load pickled model and optionally vectorizer. Return (model, vectorizer or None)."""
    model = None
    vect = None
    if model_path.exists():
        with open(model_path, "rb") as f:
            model = pickle.load(f)
    if vect_path and vect_path.exists():
        with open(vect_path, "rb") as f:
            vect = pickle.load(f)
    return model, vect

def classify(text: str, mode: str, model_tuple: Tuple = (None, None)) -> Tuple[int, float]:
    """
    Return label (1 bullying / 0 non-bullying) and confidence-like score (0-1).
    If using model mode, model_tuple = (model, vectorizer)
    """
    if mode == "Model" and model_tuple[0] is not None:
        model, vect = model_tuple
        if vect is None:
            # If model expects raw text (rare) - try direct predict_proba if available
            try:
                proba = model.predict_proba([text])[0]
                label = int(proba[1] > 0.5)
                conf = float(proba[label])
                return label, conf
            except Exception:
                # fallback to simple rule
                return simple_rule_based(text), 0.6
        else:
            X = vect.transform([text])
            try:
                proba = model.predict_proba(X)[0]
                label = int(proba[1] > 0.5)
                conf = float(proba[label])
                return label, conf
            except Exception:
                # fallback to model.predict if no predict_proba
                label = int(model.predict(X)[0])
                return label, 0.8
    else:
        lbl = simple_rule_based(text)
        conf = 0.75 if lbl == 1 else 0.85
        return lbl, conf

# --------- Streamlit UI ----------
st.set_page_config(page_title="IG-like Cyberbullying Demo", layout="wide")

# Custom CSS to mimic Instagram-ish layout + colored labels
st.markdown(
    """
    <style>
    /* layout */
    .main { padding: 0 24px 24px 24px; }
    .left, .right { background: #0f0f10; }
    .ig-logo {
        position: fixed; top: 12px; right: 36px; z-index: 9999;
        font-weight:700; color: #ffffff; font-size:18px;
    }
    .comment-box {
        border-radius:10px; padding:12px; margin-bottom:8px;
    }
    .bully {
        background: linear-gradient(90deg,#ffdde1,#ff9a9e);
        border-left:4px solid #ff4b5c;
        color:#3b0b0b;
    }
    .nobully {
        background: linear-gradient(90deg,#cfe9ff,#9ad0ff);
        border-left:4px solid #2f8fff;
        color:#05283a;
    }
    .comment-meta{ font-size:13px; color:#6b6f76; margin-bottom:6px;}
    .comment-text{ font-size:15px; margin-bottom:6px; white-space:pre-wrap; }
    .conf-pill{ font-size:12px; padding:4px 8px; border-radius:999px; background:rgba(0,0,0,0.06); }
    /* center post size */
    .post-img { max-width:720px; width:100%; border-radius:10px; }
    /* hide streamlit default menu button text */
    </style>
    """,
    unsafe_allow_html=True,
)

# IG logo top-right
st.markdown('<div class="ig-logo">Instagram</div>', unsafe_allow_html=True)

# Layout columns: left nav, main feed, right sidebar
left_col, main_col, right_col = st.columns([1, 2.4, 1])

with left_col:
    st.write("")  # left nav mock
    st.markdown("**Home**\n\nSearch\n\nExplore\n\nReels\n\nMessages\n\nNotifications\n\nCreate\n\nDashboard\n\nProfile", unsafe_allow_html=True)

with main_col:
    st.markdown("### ")
    # Stories mock row
    st.markdown("**Stories**")
    cols = st.columns(6)
    for i, c in enumerate(cols):
        with c:
            st.image("https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=200", width=72)

    st.markdown("---")
    # Post area: image and right-side comment panel (we'll render comments under the post)
    st.markdown("""
    <div style="display:flex;gap:16px;align-items:flex-start;">
        <div style="flex:1;">
    """, unsafe_allow_html=True)

    st.image("https://images.unsplash.com/photo-1535016120720-40c646be5580?q=80&w=1200", use_column_width=True, caption="Postingan - contoh")

    st.markdown("</div>", unsafe_allow_html=True)

    # Input form for comment
    st.markdown("### Tulis Komentar")
    with st.form("comment_form", clear_on_submit=True):
        input_comment = st.text_area("Masukkan komentar...", height=80)
        submitted = st.form_submit_button("Kirim & Deteksi")
        st.write("")  # spacing

    # Model upload / selection options
    st.sidebar.markdown("## Pengaturan Detektor")
    mode = st.sidebar.selectbox("Mode Deteksi", ["Rule-based (cepat)", "Model"])
    model_obj = (None, None)
    if mode == "Model":
        st.sidebar.info("Unggah file pickle model (mis. model.pkl) dan vectorizer (vectorizer.pkl jika ada).")
        model_file = st.sidebar.file_uploader("Model (.pkl)", type=["pkl","pickle"])
        vect_file = st.sidebar.file_uploader("Vectorizer (.pkl)", type=["pkl","pickle"])
        if model_file:
            try:
                model = pickle.load(model_file)
                vect = pickle.load(vect_file) if vect_file else None
                model_obj = (model, vect)
                st.sidebar.success("Model berhasil dimuat.")
            except Exception as e:
                st.sidebar.error(f"Gagal memuat model: {e}")
    else:
        st.sidebar.info("Mode rule-based menggunakan kata kunci sederhana untuk deteksi bullying.")

    # Session state for comments
    if "comments" not in st.session_state:
        st.session_state["comments"] = []  # list of dicts: {text,label,conf,author}

    # On submit: classify and append
    if submitted and input_comment and input_comment.strip():
        label, conf = classify(input_comment, "Model" if mode=="Model" else "Rule-based", model_obj)
        # simple author placeholder
        author = "you"
        st.session_state.comments.insert(0, {"text": input_comment.strip(), "label": int(label), "conf": float(conf), "author": author})

    # Render comments panel (mimic right-side overlay style)
    st.markdown("### Komentar")
    for c in st.session_state.comments:
        if c["label"] == 1:
            css_class = "comment-box bully"
            tag = "Bullying"
        else:
            css_class = "comment-box nobully"
            tag = "Non-Bullying"
        comment_html = f"""
        <div class="{css_class}">
            <div class="comment-meta"><strong>{c['author']}</strong> • <span class="conf-pill">{tag} • {c['conf']:.2f}</span></div>
            <div class="comment-text">{st.session_state.get('highlight_prefix','')}{c['text']}</div>
        </div>
        """
        st.markdown(comment_html, unsafe_allow_html=True)

with right_col:
    st.markdown("**va_zulaikha01**  \nEva Julaeha  \n[Switch]")
    st.markdown("---")
    st.markdown("**Suggested for you**")
    for i in range(4):
        st.markdown(f"- user_suggested_{i+1}  • Follow")

# Footer / notes
st.markdown("---")
st.markdown("UI demo ini meniru layout Instagram. Untuk menggunakan model nyata, pilih mode *Model* dan unggah file pickle model beserta vectorizernya (jika ada).")

