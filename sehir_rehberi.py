import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="GeoAI TR - Yapay Zeka Destekli Şehir Rehberi",
    page_icon="🇹🇷",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #FF4B4B; color: white; font-weight: bold; }
    .stButton>button:hover { background-color: #ff3333; color: white; }
    .reportview-container .main .block-container{ padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_location_data():
    locations = [
        {"id": 1, "sehir": "İstanbul", "isim": "Tarihi Yarımada (Ayasofya & Topkapı)", "kategori": "Tarih Sever", "lat": 41.0086, "lon": 28.9802, "surdurulebilirlik": 85, "reels_skor": 95, "yogunluk": "Yoğun", "gizli_görev": "Tarihi yapıların detaylarını incele ve fotoğraf çek!"},
        {"id": 2, "sehir": "İstanbul", "isim": "Karaköy & Galata Sanat Galerileri", "kategori": "Sanat & Kültür", "lat": 41.0256, "lon": 28.9744, "surdurulebilirlik": 90, "reels_skor": 98, "yogunluk": "Orta", "gizli_görev": "Kamondo Merdivenleri'nde estetik bir Reels video geçişi planla!"},
        {"id": 3, "sehir": "İstanbul", "isim": "Belgrad Ormanı Yürüyüş Rotası", "kategori": "Doğa Macaracısı", "lat": 41.1822, "lon": 28.9814, "surdurulebilirlik": 100, "reels_skor": 80, "yogunluk": "Sakin", "gizli_görev": "Yol boyunca gördüğün atıkları geri dönüşüm kutusuna at!"},
        {"id": 4, "sehir": "İstanbul", "isim": "Kadıköy Moda Sahili ve Kafeler", "kategori": "Gurme & Eğlence", "lat": 40.9822, "lon": 29.0270, "surdurulebilirlik": 75, "reels_skor": 92, "yogunluk": "Çok Yoğun", "gizli_görev": "Moda'daki sıfır atık sertifikalı yerel bir işletmeyi ziyaret et!"},
        {"id": 5, "sehir": "Nevşehir", "isim": "Göreme Açık Hava Müzesi", "kategori": "Tarih Sever", "lat": 38.6396, "lon": 34.8288, "surdurulebilirlik": 90, "reels_skor": 99, "yogunluk": "Yoğun", "gizli_görev": "Karanlık Kilise'deki tarihi fresklerin detaylarını rehber levhadan öğren!"},
        {"id": 6, "sehir": "Nevşehir", "isim": "Avanos Çömlek Atölyeleri", "kategori": "Sanat & Kültür", "lat": 38.7154, "lon": 34.8436, "surdurulebilirlik": 95, "reels_skor": 94, "yogunluk": "Orta", "gizli_görev": "Kendi geleneksel çömleğini şekillendirmeyi dene!"},
        {"id": 7, "sehir": "Nevşehir", "isim": "Ihlara Vadisi Trekking", "kategori": "Doğa Macaracısı", "lat": 38.2541, "lon": 34.2982, "surdurulebilirlik": 100, "reels_skor": 91, "yogunluk": "Sakin", "gizli_görev": "Melendiz Çayı kenarında doğanın sesini dinle!"}
    ]
    return pd.DataFrame(locations)

df_locations = load_location_data()

if 'xp' not in st.session_state:
    st.session_state.xp = 0
if 'completed_missions' not in st.session_state:
    st.session_state.completed_missions = []

st.title("🇹🇷 GeoAI - Yapay Zeka Destekli Şehir Rehberi")
st.caption("Kişiliğinize Özel, Sürdürülebilir ve Eğlenceli Gezi Deneyimi")

st.sidebar.header("🎯 Kullanıcı Profili & Skorlar")
st.sidebar.metric(label="🏆 Toplam Gamification XP", value=f"{st.session_state.xp} XP")
st.sidebar.write(f"✅ Tamamlanan Görevler: {len(st.session_state.completed_missions)}")

sehir_secimi = st.sidebar.selectbox("Geziye Başlayacağınız Şehir:", ["İstanbul", "Nevşehir"])

st.header("🧠 1. 'Benim Tarzım' Kişilik Testi")
st.write("Yapay zekanın size en uygun rotayı çizebilmesi için şu hızlı soruları yanıtlayın:")

col1, col2, col3 = st.columns(3)
with col1:
    q1 = st.radio("Bir şehirde sizi en çok ne heyecanlandırır?", ["Antik yapılar ve müzeler", "Modern sanat ve tasarım", "Doğa yürüyüşleri ve temiz hava", "Yerel lezzetler ve gece hayatı"])
with col2:
    q2 = st.radio("Seyahat ederken çevreye duyarlılığınız nasıldır?", ["Toplu taşımayı ve yürümeyi tercih ederim", "Yerel odaklı esnaf alışverişi yaparım", "Plastik kullanımından kaçınırım", "Hepsi benim için çok önemli"])
with col3:
    q3 = st.radio("Sosyal medya için içerik üretmeyi sever misiniz?", ["Harika estetik videolar çekerim", "Anı kalsın diye fotoğraf çekerim", "Sadece gezerim", "Arada sırada paylaşım yaparım"])

kisi_kategorisi = "Tarih Sever"
if "Antik" in q1: kisi_kategorisi = "Tarih Sever"
elif "Sanat" in q1: kisi_kategorisi = "Sanat & Kültür"
elif "Doğa" in q1: kisi_kategorisi = "Doğa Macaracısı"
elif "lezzetler" in q1: kisi_kategorisi = "Gurme & Eğlence"

st.info(f"🤖 **Yapay Zeka Analizi Tamamlandı:** Kişilik Profiliniz **'{kisi_kategorisi}'** olarak belirlendi!")

st.write("---")
st.header("🗺️ 2. Kişiselleştirilmiş Akıllı Rota & Anlık Durum Entegrasyonu")

filtrelenmiş_df = df_locations[(df_locations['sehir'] == sehir_secimi) & (df_locations['kategori'] == kisi_kategorisi)]
if filtrelenmiş_df.empty:
    filtrelenmiş_df = df_locations[df_locations['sehir'] == sehir_secimi]

col_map, col_list = st.columns([2, 1])
with col_list:
    st.subheader("📍 Rota Noktaları")
    for idx, row in filtrelenmiş_df.iterrows():
        yogunluk_renk = "🔴" if row['yogunluk'] == "Çok Yoğun" else ("🟡" if row['yogunluk'] == "Yoğun" else "🟢")
        st.markdown(f"**{row['isim']}**\n* {yogunluk_renk} Anlık Durum: **{row['yogunluk']}**\n* 🍃 Sürdürülebilirlik Puanı: **%{row['surdurulebilirlik']}**\n* 📸 Reels Skoru: **%{row['reels_skor']}**")
        st.write("---")

with col_map:
    st.subheader("🗺️ Canlı İnteraktif Harita")
    merkez_lat = filtrelenmiş_df.iloc[0]['lat']
    merkez_lon = filtrelenmiş_df.iloc[0]['lon']
    m = folium.Map(location=[merkez_lat, merkez_lon], zoom_start=11)
    for idx, row in filtrelenmiş_df.iterrows():
        folium.Marker([row['lat'], row['lon']], popup=row['isim'], tooltip=row['isim'], icon=folium.Icon(color="red")).add_to(m)
    st_folium(m, width=700, height=400, key="main_map")

st.write("---")
st.header("📊 3. Gelişmiş Özellik Analizleri")
tab1, tab2 = st.tabs(["🎥 'Reels Rotası' Trendleri", "🍃 Sürdürülebilir Turizm Skoru"])
with tab1:
    reels_df = df_locations[df_locations['sehir'] == sehir_secimi].sort_values(by="reels_skor", ascending=False)
    fig_reels = px.bar(reels_df, x="isim", y="reels_skor", color="reels_skor", title="Lokasyonların Reels Estetik Skoru", color_continuous_scale="Viridis")
    st.plotly_chart(fig_reels, use_container_width=True)
with tab2:
    ort_skor = df_locations[df_locations['sehir'] == sehir_secimi]['surdurulebilirlik'].mean()
    st.metric("Ortalama Sürdürülebilirlik Puanı", f"%{ort_skor:.1f}")
    fig_pie = px.pie(df_locations[df_locations['sehir'] == sehir_secimi], values="surdurulebilirlik", names="isim", title="Doğa Dostu Lokasyon Dağılımı")
    st.plotly_chart(fig_pie, use_container_width=True)

st.write("---")
st.header("🎮 4. Gamification (Gizli Görev Sistemi)")
aktif_görevler_df = df_locations[df_locations['sehir'] == sehir_secimi]
for idx, r in aktif_görevler_df.iterrows():
    if r['isim'] not in st.session_state.completed_missions:
        col_m_isim, col_m_btn = st.columns([3, 1])
        with col_m_isim:
            st.warning(f"**{r['isim']} Görevi:** {r['gizli_görev']}")
        with col_m_btn:
            if st.button(f"Görevi Tamamladım (+50 XP)", key=f"btn_{r['id']}"):
                st.session_state.xp += 50
                st.session_state.completed_missions.append(r['isim'])
                st.rerun()
    else:
        st.success(f"🎉 Başarılı: **{r['isim']}** görevi tamamlandı! (+50 XP)")