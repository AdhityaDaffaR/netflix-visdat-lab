import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. KONFIGURASI HALAMAN & CUSTOM CSS (NETFLIX THEME)
# ==========================================
st.set_page_config(
    page_title="Netflix Dashboard",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS untuk tema Gelap/Merah ala Netflix
st.markdown("""
<style>
    .stApp {
        background-color: #141414;
        color: #ffffff;
    }
    .sidebar .stSidebar {
        background-color: #000000;
    }
    h1, h2, h3 {
        color: #E50914 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎬 Netflix Content Analysis Dashboard")
st.markdown("Dashboard interaktif untuk menganalisis katalog film dan serial TV Netflix.")

# ==========================================
# 2. MEMUAT DATASET
# ==========================================
@st.cache_data
def load_data():
    # Pastikan file 'netflix_titles.csv' berada satu folder dengan file python ini
    df = pd.read_csv('netflix_titles.csv')
    return df

# Penanganan error jika file CSV belum dimasukkan ke folder
try:
    df_netflix = load_data()
except FileNotFoundError:
    st.error("⚠️ File 'netflix_titles.csv' tidak ditemukan di dalam folder proyek! Silakan masukkan file dataset tersebut terlebih dahulu.")
    # Membuat data dummy agar aplikasi tetap bisa berjalan untuk uji coba modul
    df_netflix = pd.DataFrame({
        'type': ['Movie', 'TV Show', 'Movie', 'Movie', 'TV Show'],
        'release_year': [2018, 2019, 2020, 2020, 2021],
        'rating': ['PG-13', 'TV-MA', 'R', 'PG', 'TV-14'],
        'country': ['United States', 'India', 'United States', 'United Kingdom', 'Japan'],
        'duration': ['90 min', '1 Season', '120 min', '95 min', '2 Seasons']
    })

# ==========================================
# 3. SIDEBAR FILTER INTERAKTIF
# ==========================================
st.sidebar.header("🔍 Filter Dashboard")

# Filter Tipe Konten (Movie / TV Show)
selected_type = st.sidebar.selectbox(
    "Pilih Tipe Konten:",
    options=['All'] + list(df_netflix['type'].unique())
)

# Filter Rentang Tahun Rilis
min_year = int(df_netflix['release_year'].min()) if not df_netflix.empty else 2000
max_year = int(df_netflix['release_year'].max()) if not df_netflix.empty else 2024

year_range = st.sidebar.slider(
    "Rentang Tahun Rilis:",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# Terapkan Filter ke DataFrame
filtered_df = df_netflix.copy()
if selected_type != 'All':
    filtered_df = filtered_df[filtered_df['type'] == selected_type]

filtered_df = filtered_df[
    (filtered_df['release_year'] >= year_range[0]) & 
    (filtered_df['release_year'] <= year_range[1])
]

# Tampilkan metrik ringkas di sidebar
st.sidebar.markdown(f"**Total Data Ditampilkan:** {len(filtered_df)} baris")

# ==========================================
# 4. VISUALISASI DATA (PIE CHART & LINE CHART)
# ==========================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Proporsi Tipe Konten")
    type_counts = filtered_df['type'].value_counts()
    
    # Plot Matplotlib (Pie Chart)
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.pie(
        type_counts.values, 
        labels=type_counts.index, 
        autopct='%1.1f%%', 
        colors=['#E50914', '#221f1f'], 
        startangle=90,
        textprops={'color': 'white'}
    )
    ax1.axis('equal')
    st.pyplot(fig1)

with col2:
    st.subheader("2. Tren Rilis Konten per Tahun")
    
    if not filtered_df.empty:
        trend_data = filtered_df.groupby(['release_year', 'type']).size().reset_index(name='count')
        
        fig2 = plt.figure(figsize=(6, 4))
        sns.lineplot(
            data=trend_data, 
            x='release_year', 
            y='count', 
            hue='type', 
            palette=['#E50914', '#ffffff'],
            linewidth=2.5
        )
        plt.title('Grafik Tren Rilis Netflix', color='white')
        plt.xlabel('Tahun Rilis', color='white')
        plt.ylabel('Jumlah Konten', color='white')
        plt.gca().set_facecolor('#141414')
        fig2.patch.set_facecolor('#141414')
        plt.tick_colors = 'white'
        st.pyplot(fig2)
    else:
        st.warning("Tidak ada data untuk rentang tahun yang dipilih.")

# ==========================================
# 5. TABEL DATA MENTAH (INTERAKTIF)
# ==========================================
st.divider()
st.subheader("📋 Dataset Netflix (Filtered)")
st.dataframe(filtered_df, use_container_width=True)