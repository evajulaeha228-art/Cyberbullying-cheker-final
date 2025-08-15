import streamlit as st
import pickle

# Load model dan vectorizer
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# Judul aplikasi
st.title("Deteksi Cyberbullying di Komentar Instagram")
st.write("Masukkan komentar untuk mendeteksi apakah termasuk cyberbullying atau bukan.")

# Input teks dari user
komentar = st.text_area("Masukkan komentar:")

# Tombol prediksi
if st.button("Deteksi"):
    if komentar.strip() == "":
        st.warning("Silakan masukkan komentar terlebih dahulu.")
    else:
        # Ubah komentar menjadi vektor
        vektor = vectorizer.transform([komentar])
        prediksi = model.predict(vektor)[0]

        # Tampilkan hasil
        if prediksi == "Cyberbullying":
            st.error("🚨 Komentar terdeteksi sebagai **Cyberbullying**")
        else:
            st.success("✅ Komentar **Bukan Cyberbullying**")
