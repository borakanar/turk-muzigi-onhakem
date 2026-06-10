
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Türk Müziği Ön Hakemlik Sistemi")

st.title("🎓 Türk Müziği Akademik Ön Hakemlik Sistemi")

try:
    df = pd.read_excel("Turk_Muzigi_Tez_Veritabani_Taslagi.xlsx")
except:
    df = pd.DataFrame()

menu = st.sidebar.selectbox(
    "Menü",
    ["Tez Arama","Araştırma Önerisi","Hakem Raporu"]
)

if "rapor" not in st.session_state:
    st.session_state.rapor = None

if menu == "Tez Arama":
    st.header("Tez Arama")
    q = st.text_input("Anahtar kelime")
    if not df.empty and q:
        sonuc = df[df["Başlık"].astype(str).str.contains(q, case=False, na=False)]
        st.dataframe(sonuc)

elif menu == "Araştırma Önerisi":
    st.header("Araştırma Önerisi")
    baslik = st.text_input("Başlık")
    problem = st.text_area("Problem")
    amac = st.text_area("Amaç")
    yontem = st.selectbox("Yöntem",
                          ["Doküman İncelemesi","Betimsel Analiz","Karma Yöntem","Deneysel"])

    if st.button("Değerlendir"):
        tematik = 75
        yontem_p = 90 if yontem == "Doküman İncelemesi" else 70
        bosluk = 85
        genel = round((tematik*0.35)+(yontem_p*0.35)+(bosluk*0.30))

        st.session_state.rapor = {
            "Tematik": tematik,
            "Yöntem": yontem_p,
            "Boşluk": bosluk,
            "Genel": genel,
            "Yorum": f"{baslik} başlıklı çalışma ön değerlendirmede olumlu bulunmuştur."
        }

        st.success("Rapor oluşturuldu.")

elif menu == "Hakem Raporu":
    st.header("Ön Hakem Raporu")
    if st.session_state.rapor:
        r = st.session_state.rapor
        st.metric("Tematik Benzerlik", r["Tematik"])
        st.metric("Yöntem Uygunluğu", r["Yöntem"])
        st.metric("Araştırma Boşluğu", r["Boşluk"])
        st.metric("Genel Puan", r["Genel"])
        st.info(r["Yorum"])
    else:
        st.warning("Önce değerlendirme yapınız.")
