import streamlit as st
import pickle
import time

# Memuat model dan vectorizer
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('vectorizer.pkl', 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

# Fungsi untuk memproses komentar
def proses_komentar(komentar):
    komentar_tertransformasi = vectorizer.transform([komentar])
    prediksi = model.predict(komentar_tertransformasi)[0]
    return prediksi

# State untuk komentar & status aplikasi
if "komentar_list" not in st.session_state:
    st.session_state.komentar_list = []

if "started" not in st.session_state:
    st.session_state.started = False

# ------------------- SPLASH SCREEN -------------------
def splash_screen():
    st.markdown(
        """
        <style>
        .main {
            background-color: white;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
        .button {
            padding: 12px 28px;
            background-color: #0095f6;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            cursor: pointer;
        }
        .button:hover {
            background-color: #006d9c;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.image("https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png", width=150)
    st.title("Instagram")
    if st.button("Masuk", use_container_width=False):
        st.session_state.started = True
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------- HALAMAN UTAMA -------------------
def main_page():
    # CSS styling
    st.markdown(
        """
        <style>
        body {
            background-color: #fafafa;
        }
        .container {
            display: flex;
            flex-direction: row;
        }
        .sidebar {
            width: 220px;
            height: 100vh;
            border-right: 1px solid #dbdbdb;
            padding: 20px 10px;
            background-color: white;
        }
        .sidebar h1 {
            font-family: 'Arial Black', sans-serif;
            font-size: 24px;
            margin-bottom: 30px;
        }
        .menu-item {
            font-size: 16px;
            padding: 12px 5px;
            cursor: pointer;
        }
        .menu-item:hover {
            background-color: #f2f2f2;
            border-radius: 8px;
        }
        .content {
            flex: 1;
            padding: 20px;
            display: flex;
            justify-content: center;
        }
        .post {
            width: 500px;
            background-color: white;
            border: 1px solid #dbdbdb;
            border-radius: 3px;
            margin-top: 20px;
            padding-bottom: 10px;
        }
        .post-header {
            display: flex;
            align-items: center;
            padding: 10px;
            font-weight: bold;
            border-bottom: 1px solid #eee;
        }
        .comments {
            max-height: 200px;
            overflow-y: scroll;
            padding: 10px;
        }
        .comment {
            margin-bottom: 10px;
            padding: 8px;
            border-radius: 6px;
            font-size: 14px;
        }
        .bullying {
            background-color: #f8d7da;
            color: #721c24;
        }
        .non-bullying {
            background-color: #d4edda;
            color: #155724;
        }
        .post {
            padding: 20px;
            background-color: white;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Struktur utama
    st.markdown('<div class="container">', unsafe_allow_html=True)

    # Sidebar kiri
    st.markdown(
        """
        <div class="sidebar">
            <h1>Instagram</h1>
            <div class="menu-item">🏠 Home</div>
            <div class="menu-item">🔍 Search</div>
            <div class="menu-item">🧭 Explore</div>
            <div class="menu-item">🎥 Reels</div>
            <div class="menu-item">💬 Messages</div>
            <div class="menu-item">🔔 Notifications</div>
            <div class="menu-item">➕ Create</div>
            <div class="menu-item">👤 Profile</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Konten utama (postingan)
    st.markdown('<div class="content">', unsafe_allow_html=True)
    st.markdown('<div class="post">', unsafe_allow_html=True)

    # Header akun
    st.markdown('<div class="post-header">va_zulaikha01</div>', unsafe_allow_html=True)

    # Foto postingan (menggunakan gambar lesti.jpg)
    st.image("lesti.jpg", use_column_width=True, caption="📸 Lesti Kejora")  # Ganti dengan gambar lokal
    st.text("hidup harus selalu disyukuri")

    # Input komentar
    komentar_pengguna = st.text_input("Tambahkan komentar...")

    if st.button("Kirim"):
        if komentar_pengguna.strip():
            hasil = proses_komentar(komentar_pengguna)
            if hasil == "Cyberbullying":
                label = f'🚨 {komentar_pengguna} (Komentar ini terdeteksi sebagai Cyberbullying)'
                st.session_state.komentar_list.append(("bullying", label))
            else:
                label = f'✅ {komentar_pengguna} (Komentar ini Bukan Cyberbullying)'
                st.session_state.komentar_list.append(("non-bullying", label))
        else:
            st.warning("Silakan masukkan komentar terlebih dahulu.")

    # Komentar dengan scroll
    st.markdown('<div class="comments">', unsafe_allow_html=True)
    for jenis, teks in st.session_state.komentar_list:
        st.markdown(f'<div class="comment {jenis}">{teks}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # tutup post
    st.markdown('</div>', unsafe_allow_html=True)  # tutup content
    st.markdown('</div>', unsafe_allow_html=True)  # tutup container

# ------------------- LOGIC -------------------
if not st.session_state.started:
    splash_screen()
else:
    main_page()
