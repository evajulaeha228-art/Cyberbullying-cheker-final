import streamlit as st
import pickle

# Load model & vectorizer
@st.cache_resource
def load_model():
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    return model, vectorizer

model, vectorizer = load_model()

# CSS Instagram Style
st.markdown("""
    <style>
    .insta-card {
        max-width: 500px;
        margin: auto;
        border: 1px solid #dbdbdb;
        border-radius: 12px;
        background: white;
        font-family: Arial, sans-serif;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .header {
        display: flex;
        align-items: center;
        padding: 10px;
    }
    .profile-pic {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 10px;
        background: #ddd;
    }
    .username {
        font-weight: bold;
    }
    .photo {
        width: 100%;
        border-top: 1px solid #eee;
        border-bottom: 1px solid #eee;
    }
    .actions {
        padding: 10px;
        font-size: 20px;
    }
    .comment-box {
        padding: 5px 10px;
        font-size: 15px;
    }
    .blur {
        color: transparent;
        text-shadow: 0 0 8px rgba(0,0,0,0.5);
        user-select: none;
    }
    </style>
""", unsafe_allow_html=True)

# Inisialisasi session state untuk daftar komentar
if "comments" not in st.session_state:
    st.session_state.comments = []

if "show_comment" not in st.session_state:
    st.session_state.show_comment = {}

# Judul Aplikasi
st.title("📸 Instagram Cyberbullying Detector")

# Upload Foto
foto = st.file_uploader("Upload foto postingan", type=["jpg", "jpeg", "png"])

# Input komentar
komentar = st.text_input("Tulis komentar...")

if st.button("Kirim Komentar"):
    if komentar.strip() != "":
        # Prediksi komentar
        vektor = vectorizer.transform([komentar])
        prediksi = model.predict(vektor)[0]

        # Simpan ke daftar komentar
        st.session_state.comments.append({
            "user": "user123",
            "text": komentar,
            "label": prediksi
        })
    else:
        st.warning("Komentar tidak boleh kosong!")

# --- Tampilan Postingan Instagram ---
st.markdown('<div class="insta-card">', unsafe_allow_html=True)

# Header Postingan
st.markdown("""
    <div class="header">
        <div class="profile-pic"></div>
        <div class="username">user_ig</div>
    </div>
""", unsafe_allow_html=True)

# Foto Postingan
if foto:
    st.image(foto, use_column_width=True)
else:
    st.image("https://via.placeholder.com/500x300.png?text=Foto+Instagram", use_column_width=True)

# Actions ❤️ 🔁 💬
st.markdown("""
    <div class="actions">
        ❤️  🔁  💬
    </div>
""", unsafe_allow_html=True)

# Daftar komentar
st.write("### Komentar:")

for i, c in enumerate(st.session_state.comments):
    komentar_tampil = c["text"]

    if c["label"] == "Cyberbullying" and not st.session_state.show_comment.get(i, False):
        komentar_tampil = f"<span class='blur'>{komentar_tampil}</span>"

    st.markdown(f"""
        <div class="comment-box">
            <b>{c['user']}</b>: {komentar_tampil} <br>
            <span style="font-size:12px; color:{'red' if c['label']=='Cyberbullying' else 'green'};">
                {'🚨 Cyberbullying' if c['label']=='Cyberbullying' else '✅ Aman'}
            </span>
        </div>
    """, unsafe_allow_html=True)

    # Tombol tampilkan komentar asli kalau terdeteksi cyberbullying
    if c["label"] == "Cyberbullying" and not st.session_state.show_comment.get(i, False):
        if st.button(f"Tampilkan komentar asli #{i}"):
            st.session_state.show_comment[i] = True
            st.experimental_rerun()

st.markdown('</div>', unsafe_allow_html=True)

