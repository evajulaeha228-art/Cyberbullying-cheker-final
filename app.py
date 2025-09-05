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
    # Transformasi komentar menggunakan vectorizer dan prediksi apakah termasuk bullying atau tidak
    komentar_tertransformasi = vectorizer.transform([komentar])
    prediksi = model.predict(komentar_tertransformasi)[0]
    return prediksi

# Tampilan Splash Screen
def splash_screen():
    st.markdown(
        '''
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
            padding: 15px 30px;
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
        ''',
        unsafe_allow_html=True
    )

    # Logo Instagram
    st.image("https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png", width=200)
    st.title("Instagram")
    st.markdown("##")
    st.markdown("### Welcome to the Cyberbullying Detection System")

    # Tombol Masuk
    if st.button("Masuk", key="login_button", help="Klik untuk masuk"):
        time.sleep(0.5)  # Simulasi loading
        st.experimental_rerun()

# Tampilan Halaman Utama
def main_page():
    st.markdown(
        '''
        <style>
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
        }
        .header img {
            height: 40px;
        }
        .comment-box {
            width: 100%;
            height: 60px;
            padding: 10px;
            margin-top: 20px;
        }
        .comment-section {
            margin-top: 20px;
        }
        .comment {
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 8px;
        }
        .bullying {
            background-color: #f8d7da;
            color: #721c24;
        }
        .non-bullying {
            background-color: #d4edda;
            color: #155724;
        }
        </style>
        ''',
        unsafe_allow_html=True
    )

    # Header Instagram
    col1, col2 = st.columns([1, 9])
    with col1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png", width=40)
    with col2:
        st.markdown("**Instagram**")
    
    # Menampilkan Nama Akun Pengguna
    st.markdown("### Va_Zulaikha01")

    # Postingan
    st.image("https://upload.wikimedia.org/wikipedia/commons/9/95/Instagram_logo_2022.svg", width=300)
    st.text("Sunset at the beach 🌅")

    # Form komentar
    komentar_pengguna = st.text_area("Tulis komentar di sini:")

    # Tombol Deteksi Komentar
    if st.button("Deteksi Komentar"):
        if komentar_pengguna.strip():
            prediksi = proses_komentar(komentar_pengguna)
            if prediksi == "Cyberbullying":
                st.markdown(f'<div class="comment bullying">🚨 Komentar ini terdeteksi sebagai **Cyberbullying**</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="comment non-bullying">✅ Komentar ini **Bukan Cyberbullying**</div>', unsafe_allow_html=True)
        else:
            st.warning("Silakan masukkan komentar terlebih dahulu.")

    # Menampilkan komentar sebelumnya (contoh komentar)
    st.markdown("### Komentar Terbaru")
    st.markdown(f'<div class="comment bullying">🚨 @user: Kamu jelek banget!</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="comment non-bullying">✅ @user2: Apa kabar? Semangat terus ya!</div>', unsafe_allow_html=True)

# Menampilkan Splash Screen atau Halaman Utama
if 'started' not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    splash_screen()
    if st.button("Masuk", key="enter_button"):
        st.session_state.started = True
        st.experimental_rerun()
else:
    main_page()
