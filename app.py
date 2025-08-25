import streamlit as st

st.set_page_config(page_title="Deteksi Cyberbullying IG", layout="centered")

# Judul
st.markdown(
    """
    <h2 style='text-align:center; font-family:sans-serif;'>📷 Instagram - Deteksi Cyberbullying</h2>
    """,
    unsafe_allow_html=True
)

# Tampilkan postingan
st.image("postingan.jpg", use_column_width=True, caption="Postingan")

# Inisialisasi session state untuk menyimpan komentar
if "komentar_list" not in st.session_state:
    st.session_state.komentar_list = []

# Form komentar
with st.form("komentar_form", clear_on_submit=True):
    komentar = st.text_input("Tulis komentar...")
    submitted = st.form_submit_button("Kirim")

    if submitted and komentar:
        # Rule sederhana klasifikasi
        if any(kata in komentar.lower() for kata in ["bodoh", "jelek", "goblok", "hina"]):
            label = "Cyberbullying"
        else:
            label = "Bukan Cyberbullying"

        # Simpan ke session
        st.session_state.komentar_list.append((komentar, label))

# Tampilkan komentar
st.markdown("---")
st.subheader("💬 Komentar")

if st.session_state.komentar_list:
    for komentar, label in reversed(st.session_state.komentar_list):
        if label == "Cyberbullying":
            warna = "red"
        else:
            warna = "green"

        st.markdown(
            f"""
            <div style="padding:8px; border-bottom:1px solid #ddd;">
                <span style="font-size:16px;">{komentar}</span><br>
                <span style="color:{warna}; font-weight:bold;">{label}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.info("Belum ada komentar. Jadilah yang pertama!")
