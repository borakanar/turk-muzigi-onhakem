import streamlit as st
import pandas as pd

st.set_page_config(page_title="Türk Müziği Ön Hakemlik Sistemi", layout="wide")

@st.cache_data
def load_data():
    return pd.read_excel("Turk_Muzigi_Tez_Veritabani_AnahtarKelime_Yontem.xlsx")

df = load_data()

st.title("🎓 Türk Müziği Akademik Ön Hakemlik Sistemi")

menu = st.sidebar.radio(
    "Menü",
    [
        "Tez Veritabanı",
        "Araştırma Önerisi",
        "Ön Hakem Raporu"
    ]
)

if "rapor" not in st.session_state:
    st.session_state.rapor = None

# --------------------------------------------------
# TEZ VERİTABANI
# --------------------------------------------------

if menu == "Tez Veritabanı":

    st.header("📚 Tez Veritabanı")

    yil_listesi = sorted(df["Yıl"].dropna().unique())

    secilen_yil = st.selectbox(
        "Yıl Seç",
        ["Tümü"] + list(yil_listesi)
    )

    arama = st.text_input("Başlık veya Anahtar Kelime Ara")

    filtre = df.copy()

    if secilen_yil != "Tümü":
        filtre = filtre[filtre["Yıl"] == secilen_yil]

    if arama:
        filtre = filtre[
            filtre.astype(str)
            .apply(lambda x: x.str.contains(arama, case=False, na=False))
            .any(axis=1)
        ]

    st.write(f"Toplam Kayıt: {len(filtre)}")
    st.dataframe(filtre, use_container_width=True)

# --------------------------------------------------
# ARAŞTIRMA ÖNERİSİ
# --------------------------------------------------

elif menu == "Araştırma Önerisi":

    st.header("📝 Araştırma Önerisi")

    baslik = st.text_input("Araştırma Başlığı")

    problem = st.text_area("Problem Durumu")

    amac = st.text_area("Araştırmanın Amacı")

    yontem = st.selectbox(
        "Önerilen Yöntem",
        [
            "Doküman İncelemesi",
            "Betimsel Analiz",
            "Analitik İnceleme",
            "Tarihsel Araştırma",
            "Karma Yöntem"
        ]
    )

    if st.button("Ön Değerlendirme Yap"):

        benzer = 0

        if baslik:

            for row in df["Başlık"].astype(str):

                kelimeler = baslik.lower().split()

                for k in kelimeler:

                    if k in row.lower():
                        benzer += 1
                        break

        tematik = min(100, benzer * 10)

        yontem_puan = 80

        bosluk = max(20, 100 - tematik)

        genel = round(
            (tematik * 0.35)
            + (yontem_puan * 0.35)
            + (bosluk * 0.30)
        )

        yorum = f"""
Araştırma önerisi veri tabanındaki çalışmalarla karşılaştırılmıştır.

Benzer tez sayısı: {benzer}

Tematik benzerlik puanı: {tematik}

Yöntem uygunluğu puanı: {yontem_puan}

Araştırma boşluğu puanı: {bosluk}
"""

        st.session_state.rapor = {
            "tematik": tematik,
            "yontem": yontem_puan,
            "bosluk": bosluk,
            "genel": genel,
            "yorum": yorum
        }

        st.success("Ön hakem raporu oluşturuldu.")

# --------------------------------------------------
# RAPOR
# --------------------------------------------------

elif menu == "Ön Hakem Raporu":

    st.header("📋 Ön Hakem Raporu")

    if st.session_state.rapor:

        r = st.session_state.rapor

        st.metric("Tematik Benzerlik", r["tematik"])
        st.metric("Yöntem Uygunluğu", r["yontem"])
        st.metric("Araştırma Boşluğu", r["bosluk"])
        st.metric("Genel Puan", r["genel"])

        st.subheader("Hakem Yorumu")
        st.write(r["yorum"])

    else:
        st.warning("Önce araştırma önerisini değerlendiriniz.")
