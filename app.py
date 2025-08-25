# app.py
# Streamlit app: Instagram-like UI + comment input + classification + persistent storage
# Usage:
#   pip install streamlit scikit-learn joblib
#   streamlit run app.py
#
# Notes:
# - If you have a trained sklearn Pipeline (vectorizer + estimator), save it as model.joblib or model.pkl
#   and place it next to this app, or upload via the "Upload model" widget in the UI.
# - Comments stored in comments.json

import streamlit as st
from datetime import datetime
import uuid
import json
import os
from pathlib import Path

# Optional: try to import joblib for model loading
try:
    import joblib
except Exception:
    joblib = None

# ---------------------------
# Configuration & utilities
# ---------------------------
COMMENTS_FILE = Path(__file__).with_name("comments.json")

st.set_page_config(page_title="Prototype Deteksi Cyberbullying (Mirip Instagram)", layout="wide")

def load_comments():
    if COMMENTS_FILE.exists():
        try:
            return json.loads(COMMENTS_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []

def save_comments(comments):
    COMMENTS_FILE.write_text(json.dumps(comments, ensure_ascii=False, indent=2), encoding="utf-8")

# Simple fallback classifier (rule-based)
BULLY_KEYWORDS = [
    "bodoh", "jelek", "bego", "goblok", "k*t", "tolol", "banci", "m*ntap", "goblok", "b*dak",
    "goblok", "stupid", "idiot", "hate", "worthless", "fuck"
]
def fallback_classify(text: str) -> str:
    t = text.lower()
    for k in BULLY_KEYWORDS:
        if k in t:
            return "Cyberbullying"
    return "Bukan Cyberbullying"

# Load model if exists in working directory (model.joblib or model.pkl)
def try_load_model_from_path():
    model_paths = ["model.joblib", "model.pkl"]
    for mp in model_paths:
        p = Path(mp)
        if p.exists():
            if joblib:
                try:
                    mdl = joblib.load(str(p))
                    return mdl
                except Exception as e:
                    st.warning(f"Gagal memuat model dari {mp}: {e}")
            else:
                st.warning("joblib tidak tersedia; install joblib untuk memuat model tersimpan.")
    return None

# Classify wrapper: tries model.predict, else fallback
def classify_text(text: str, model):
    if model is None:
        return fallback_classify(text)
    # If model is a pipeline or has predict, try to call it
    try:
        # handle case where model.predict returns array of labels
        pred = model.predict([text])
        if isinstance(pred, (list, tuple)) or hasattr(pred, "__len__"):
            return str(pred[0])
        else:
            return str(pred)
    except Exception as e:
        # Some models require transform, or predict_proba -> thresholding, etc.
        # If model has predict_proba, we try threshold 0.5 on positive class
        try:
            if hasattr(model, "predict_proba"):
                probs = model.predict_proba([text])
                # take highest probability label if classes_ present
                if hasattr(model, "classes_"):
                    classes = model.classes_
                    idx = probs[0].argmax()
                    return str(classes[idx])
                else:
                    return str(probs[0])
        except Exception:
            pass
        # as fallback, use rule-based
        st.info("Model error saat klasifikasi, menggunakan fallback rules.")
        return fallback_classify(text)

# ---------------------------
# App UI
# ---------------------------

# Sidebar: model loading & info
with st.sidebar:
    st.title("Pengaturan")
    st.markdown("**Model deteksi**")
    model_file_uploaded = st.file_uploader("Upload model (.joblib / .pkl) (opsional)", type=["joblib","pkl"])
    st.write("Atau letakkan file `model.joblib` / `model.pkl` di folder aplikasi untuk dimuat otomatis.")
    st.markdown("---")
    st.info("Jika tidak ada model, aplikasi menggunakan aturan kata kunci sederhana (demo).")
    st.markdown("**Instruksi singkat**:\n- Ketik komentar di kolom kanan bawah lalu klik *Post*.\n- Komentar akan diklasifikasikan & disimpan ke `comments.json`.")
    st.markdown("---")
    st.write("Debug")
    st.write(f"comments.json ada: {COMMENTS_FILE.exists()}")
    st.write("Session state keys:")
    st.write(list(st.session_state.keys()))

# Try load model from disk first
if "loaded_model" not in st.session_state:
    st.session_state.loaded_model = try_load_model_from_path()

# If user uploaded model via widget, load it into memory (and optionally save to disk)
if model_file_uploaded is not None:
    try:
        if joblib:
            # save uploaded bytes to temporary file and load
            tmp_path = Path("uploaded_model.joblib")
            tmp_path.write_bytes(model_file_uploaded.getvalue())
            loaded = joblib.load(str(tmp_path))
            st.session_state.loaded_model = loaded
            st.success("Model berhasil diunggah dan dimuat ke memori.")
        else:
            st.error("joblib tidak terpasang: jalankan 'pip install joblib' untuk memuat model.")
    except Exception as e:
        st.error(f"Gagal memuat model: {e}")

model = st.session_state.get("loaded_model", None)

# Page header
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("<h1 style='margin:0'>Prototype - Deteksi Cyberbullying</h1>", unsafe_allow_html=True)
with col2:
    st.markdown("<div style='text-align:right;color:#666'>Mirip Tampilan Instagram — Untuk Skripsi</div>", unsafe_allow_html=True)

st.markdown("---")

# Main layout: left = image/ post, right = comments & input
left_col, right_col = st.columns([2, 1])

# Ensure in session: toggles for showing blurred comments
if "show_comment" not in st.session_state:
    st.session_state.show_comment = {}

# Load existing comments
comments = load_comments()

# Helper to add comment
def add_comment(user, text, label):
    global comments
    new = {
        "id": str(uuid.uuid4()),
        "user": user,
        "text": text,
        "label": label,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    comments.append(new)
    save_comments(comments)
    # ensure toggle state exists
    st.session_state.show_comment[new["id"]] = False

# Left column: post display
with left_col:
    # top-of-post header like IG
    st.markdown("""
    <div style="display:flex;align-items:center;padding:8px 0;">
      <div style="width:46px;height:46px;border-radius:50%;background:linear-gradient(135deg,#f09433,#e6683c,#dc2743,#cc2366,#bc1888);color:white;display:flex;align-items:center;justify-content:center;font-weight:700;">EJ</div>
      <div style="margin-left:10px">
        <div style="font-weight:700">eva_julaeha</div>
        <div style="font-size:12px;color:#8e8e8e">Jakarta · {date}</div>
      </div>
    </div>
    """.format(date=datetime.now().strftime("%d %b %Y")), unsafe_allow_html=True)

    # post image area
    st.markdown(
        """
        <div style="border:1px solid #dbdbdb;border-radius:6px;overflow:hidden;">
            <img src="https://picsum.photos/900/600?random=7" style="width:100%;height:auto;display:block;">
            <div style="padding:12px;">
                <div style="font-weight:600;">Caption contoh: Menikmati sore di taman 🌿</div>
                <div style="color:#8e8e8e;margin-top:6px">780,496 likes · 1 day ago</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("##")

    # Optionally show model summary
    if model is not None:
        st.success("Model terpasang dan siap digunakan.")
        try:
            summary = ""
            if hasattr(model, "classes_"):
                summary += f"Classes: {list(model.classes_)}  "
            if hasattr(model, "__class__"):
                summary += f"Type: {model.__class__.__name__}"
            st.write(summary)
        except Exception:
            pass
    else:
        st.warning("Tidak ditemukan model. Aplikasi memakai rule-based fallback.")

# Right column: comments list and input
with right_col:
    st.markdown("<div style='font-size:18px;font-weight:700'>Comments</div>", unsafe_allow_html=True)

    # display comments on the right - newest first
    if comments:
        for c in reversed(comments):
            cid = c["id"]
            label = c.get("label", "Tidak diketahui")
            is_bully = (str(label).lower().find("cyber") != -1) or (str(label).lower().find("bully") != -1)
            show = st.session_state.show_comment.get(cid, False)

            # comment header (user + badge)
            badge_color = "#ffeef0" if is_bully else "#ecfdf5"
            badge_text_color = "#c00" if is_bully else "#065f46"
            st.markdown(
                f"""
                <div style="display:flex;align-items:flex-start;padding:8px 0;border-bottom:1px solid #f2f2f2">
                  <div style="width:40px;height:40px;border-radius:50%;background:#ddd;display:flex;align-items:center;justify-content:center;font-weight:700;margin-right:8px">U</div>
                  <div style="flex:1">
                    <div style="font-weight:700">{c['user']} <span style="display:inline-block;padding:3px 8px;border-radius:12px;background:{badge_color};color:{badge_text_color};font-size:12px;margin-left:8px">{label}</span></div>
                    <div style="margin-top:6px">
                        {"<span style='filter: blur(3px);'>"+c['text']+"</span>" if is_bully and not show else c['text']}
                        {"&nbsp;<button style='border:none;background:#fff;color:#0a66ff;padding:2px 6px;border-radius:6px;margin-left:6px' disabled> </button>"}
                    </div>
                    <div style="font-size:11px;color:#8e8e8e;margin-top:6px">{c['time']}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
            # Provide toggle button to show/hide the blurred text
            if is_bully:
                key = f"toggle_{cid}"
                if st.button("Tampilkan / Sembunyikan", key=key):
                    st.session_state.show_comment[cid] = not st.session_state.show_comment.get(cid, False)
    else:
        st.info("Belum ada komentar. Jadilah yang pertama!")

    st.markdown("---")
    st.markdown("**Tambah komentar**")
    with st.form(key="comment_form", clear_on_submit=True):
        user = st.text_input("Nama (opsional)", value="user_demo")
        comment_text = st.text_input("Tulis komentar...", value="")
        submit = st.form_submit_button("Post")
        if submit:
            if not comment_text.strip():
                st.warning("Komentar kosong!")
            else:
                # classify
                label = classify_text(comment_text.strip(), model)
                add_comment(user if user.strip() else "user_demo", comment_text.strip(), label)
                st.success(f"Komentar dipost — label: {label}")
                # reload comments variable
                comments = load_comments()
                # scroll-ish: rerun to show latest
                st.experimental_rerun()

# Footer note
st.markdown("---")
st.markdown("<div style='color:#666;font-size:13px'>Catatan: Ini prototype untuk keperluan penelitian — tidak terintegrasi langsung dengan API resmi Instagram.</div>", unsafe_allow_html=True)
