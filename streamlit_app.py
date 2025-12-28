import streamlit as st
import pandas as pd

# Title 
st.title("Pemerograman Dasar Menggunakan Bahasa Python")

# Header
st.header("Belajar Membuat Web Dengan Streamlit dan Bahasa Python")

st.divider()
# Subheader
st.subheader("""Abiyyu Muflih Kurnia 4232401041""")

st.divider()


# Code
st.code("""def kelas():
        prit("RPE Pagi 3B")
""")

st.write("")

# Text untuk membuat Paragraf
st.text("HALLO!!! Perkenalkan saya Abiyyu Muflih Kurnia saya berumur 20 tahun, saya sekarang" \
" sedang berkuliah di Politeknik Negeri Batam, dengan jurusan Teknik Elektro, Prodi D4 " \
"Teknologi Rekayasa Pembangkit Energi, dengan kelas B, ini adalah Web analisis menggunakan library " \
"Streamlit dan menggunakan bahasa pemerograman Python ")

st.write("")
st.write("")

# Text
st.text("Ini adalah table untuk analisis")
abyy = pd.DataFrame({
"Team" : ["Celtics", "Lakers", "Warriors", "Bulls", "Spurs"], "Juara" : [18, 17, 7, 6, 5]
})

st.table(data=abyy)

st.write("")
st.write("")

# Chart
st.subheader("Grafik 5 Team NBA Dengan Juara Terbanyak")
st.bar_chart(abyy.set_index("Team"))

st.divider()

# Rating
sentiment_mapping = ["one", "two", "three", "four", "five"]
selected = st.feedback("stars")
if selected is not None:
    st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")

# Caption
st.caption("Copyright (c) 2025")



