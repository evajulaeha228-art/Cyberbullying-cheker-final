import streamlit as st
import pickle

# ================= LOAD MODEL =================
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)
with open('vectorizer.pkl', 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

def proses_komentar(komentar):
    komentar_tertransformasi = vectorizer.transform([komentar])
    prediksi = model.predict(komentar_tertransformasi)[0]
    return prediksi

# ================= SESSION STATE =================
if "komentar_list" not in st.session_state:
    st.session_state.komentar_list = []
if "started" not in st.session_state:
    st.session_state.started = False
if "likes" not in st.session_state:
    st.session_state.likes = 0

# ================= SPLASH SCREEN =================
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
    st.markdown("### Welcome to the Cyberbullying Detection System")

    if st.button("Masuk"):
        st.session_state.started = True

    st.markdown('</div>', unsafe_allow_html=True)

# ================= MAIN PAGE =================
def main_page():
    col1, col2 = st.columns([1, 2])

    # Sidebar kiri
    with col1:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 8px;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" width="30">
                <h2 style="margin:0;">Instagram</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("---")
        st.markdown("🏠 Home")
        st.markdown("🔍 Search")
        st.markdown("🧭 Explore")
        st.markdown("🎥 Reels")
        st.markdown("💬 Messages")
        st.markdown("🔔 Notifications")
        st.markdown("➕ Create")
        st.markdown("👤 Profile")

    # Konten utama
    with col2:
        st.markdown("### va_zulaikha01")
        st.image("lesti.jpg", use_container_width=True)

        colA, colB, colC, colD = st.columns([1,1,1,5])
        with colA:
            if st.button("❤️ Like"):
                st.session_state.likes += 1
        with colB:
            st.write("💬")
        with colC:
            st.write("📤")
        with colD:
            st.write("🔖")

        st.markdown(f"**{st.session_state.likes} suka**")

        komentar_pengguna = st.text_input("Tambahkan komentar...")
        if st.button("Kirim 📤"):
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

        st.markdown("#### Komentar")
        st.markdown(
            """
            <style>
            .scroll-box {
                max-height: 250px;
                overflow-y: auto;
                padding: 10px;
                border: 1px solid #dbdbdb;
                border-radius: 6px;
                background-color: #fafafa;
            }
            .bullying {
                background-color: #f8d7da;
                color: #721c24;
                padding: 5px;
                margin-bottom: 5px;
                border-radius: 4px;
            }
            .non-bullying {
                background-color: #d4edda;
                color: #155724;
                padding: 5px;
                margin-bottom: 5px;
                border-radius: 4px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        komentar_html = '<div class="scroll-box">'
        for jenis, teks in st.session_state.komentar_list:
            komentar_html += f'<div class="{jenis}">{teks}</div>'
        komentar_html += '</div>'
        st.markdown(komentar_html, unsafe_allow_html=True)

# ================= LOGIC =================
if not st.session_state.started:
    splash_screen()
else:
    main_page()
