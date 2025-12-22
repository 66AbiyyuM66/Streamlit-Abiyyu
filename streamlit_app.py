import streamlit as st

st.set_page_config(page_title="Biodata Abiyyu", layout="centered")

st.title("👤 Biodata Diri")

st.write("""
**Nama** : Abiyyu  
**Umur** : 20 tahun  
""")

st.subheader("Tentang Saya")
st.write("""
Saya adalah individu yang memiliki ketertarikan dalam bidang teknologi dan analisis.
Saya terbiasa mengerjakan tugas akademik, proyek kecil, serta pemecahan masalah secara
mandiri maupun berkelompok. Saya memiliki motivasi untuk terus belajar hal baru dan
meningkatkan kemampuan diri.
""")

st.subheader("Pengalaman Singkat")
st.write("""
Saya pernah terlibat dalam berbagai aktivitas yang menuntut ketelitian dan tanggung jawab,
seperti pengolahan data sederhana, pembuatan laporan, dan penggunaan tools berbasis Python.
Pengalaman tersebut membantu saya mengembangkan pola pikir sistematis, manajemen waktu,
serta kemampuan bekerja di bawah tekanan.
""")

st.subheader("Keahlian Dasar")
st.write("""
- Python dasar  
- Analisis data sederhana  
- Pembuatan laporan  
- Kerja tim dan komunikasi  
""")

st.markdown("---")
st.caption("Website biodata sederhana menggunakan Streamlit")
