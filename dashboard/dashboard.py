
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# KONFIGURASI DASHBOARD
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# MEMBACA DATASET
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

df_hour = pd.read_csv(DATA_DIR / "hour.csv")
df_day = pd.read_csv(DATA_DIR / "day.csv")

df_hour["dteday"] = pd.to_datetime(df_hour["dteday"])
df_day["dteday"] = pd.to_datetime(df_day["dteday"])

# MENGUBAH KODE KATEGORI MENJADI LABEL
season_labels = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}

weather_labels = {
    1: "Clear / Few Clouds",
    2: "Mist / Cloudy",
    3: "Light Rain / Snow",
    4: "Heavy Rain / Snow"
}

df_day["season_label"] = df_day["season"].map(season_labels)
df_day["weather_label"] = df_day["weathersit"].map(weather_labels)

# SIDEBAR FILTER
st.sidebar.title("Filter Dashboard")

min_date = df_day["dteday"].min().date()
max_date = df_day["dteday"].max().date()

selected_dates = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# MEMASTIKAN RENTANG TANGGAL VALID
if isinstance(selected_dates, (tuple, list)):
    if len(selected_dates) == 2:
        start_date, end_date = selected_dates
    elif len(selected_dates) == 1:
        start_date = selected_dates[0]
        end_date = selected_dates[0]
    else:
        start_date = min_date
        end_date = max_date
else:
    start_date = selected_dates
    end_date = selected_dates

# FILTER DATA
df_hour_filtered = df_hour[
    (df_hour["dteday"].dt.date >= start_date) &
    (df_hour["dteday"].dt.date <= end_date)
].copy()

df_day_filtered = df_day[
    (df_day["dteday"].dt.date >= start_date) &
    (df_day["dteday"].dt.date <= end_date)
].copy()

# JUDUL DASHBOARD
st.title("🚲 Bike Sharing Analysis Dashboard")

st.markdown(
    "Dashboard ini menyajikan analisis pola penyewaan sepeda "
    "berdasarkan waktu, jenis hari, kondisi cuaca, dan musim "
    "selama periode 2011–2012."
)

st.divider()

# RINGKASAN DATA
st.subheader("Ringkasan Penyewaan Sepeda")

total_rentals = df_day_filtered["cnt"].sum()
average_rentals = df_day_filtered["cnt"].mean()
total_days = len(df_day_filtered)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Penyewaan",
    f"{total_rentals:,.0f}"
)

col2.metric(
    "Rata-rata Penyewaan per Hari",
    f"{average_rentals:,.2f}" if total_days > 0 else "-"
)

col3.metric(
    "Jumlah Hari",
    f"{total_days:,}"
)

st.divider()

# ==================================================
# PERTANYAAN BISNIS 1
# ==================================================

st.header("1. Pola Penyewaan Berdasarkan Waktu dan Jenis Hari")

st.markdown(
    "Bagaimana perbedaan rata-rata jumlah penyewaan sepeda "
    "antara hari kerja dan hari non-kerja, serta kapan "
    "permintaan penyewaan mencapai puncaknya?"
)

# RATA-RATA PENYEWAAN BERDASARKAN JENIS HARI
workingday_analysis = (
    df_hour_filtered.groupby("workingday")["cnt"]
    .mean()
    .reset_index()
)

workingday_analysis["jenis_hari"] = workingday_analysis[
    "workingday"
].map({
    0: "Hari Non-Kerja",
    1: "Hari Kerja"
})

fig1 = px.bar(
    workingday_analysis,
    x="jenis_hari",
    y="cnt",
    color="jenis_hari",
    text_auto=".2f",
    title="Rata-rata Penyewaan Berdasarkan Jenis Hari",
    labels={
        "jenis_hari": "Jenis Hari",
        "cnt": "Rata-rata Penyewaan per Jam"
    }
)

fig1.update_layout(showlegend=False)

# RATA-RATA PENYEWAAN BERDASARKAN JAM
hourly_analysis = (
    df_hour_filtered.groupby(["hr", "workingday"])["cnt"]
    .mean()
    .reset_index()
)

hourly_analysis["jenis_hari"] = hourly_analysis[
    "workingday"
].map({
    0: "Hari Non-Kerja",
    1: "Hari Kerja"
})

fig2 = px.line(
    hourly_analysis,
    x="hr",
    y="cnt",
    color="jenis_hari",
    markers=True,
    title="Pola Penyewaan Sepeda Berdasarkan Jam",
    labels={
        "hr": "Jam",
        "cnt": "Rata-rata Penyewaan per Jam",
        "jenis_hari": "Jenis Hari"
    }
)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)

# INSIGHT PERTANYAAN 1 (DINAMIS)
st.subheader("Insight Pertanyaan 1")

if df_hour_filtered.empty:
    st.info(
        "Tidak ada data penyewaan pada rentang tanggal yang dipilih."
    )
else:
    insight_q1 = []

    # RATA-RATA PENYEWAAN BERDASARKAN JENIS HARI
    for _, row in workingday_analysis.iterrows():
        insight_q1.append(
            f"Rata-rata penyewaan pada {row['jenis_hari'].lower()} "
            f"adalah {row['cnt']:.2f} penyewaan per jam."
        )

    # JAM PUNCAK SETIAP JENIS HARI
    if not hourly_analysis.empty:
        peak_indices = hourly_analysis.groupby(
            "workingday"
        )["cnt"].idxmax()

        peak_hours = hourly_analysis.loc[peak_indices]

        for _, row in peak_hours.iterrows():
            jenis_hari = (
                "hari kerja"
                if row["workingday"] == 1
                else "hari non-kerja"
            )

            insight_q1.append(
                f"Puncak penyewaan pada {jenis_hari} terjadi pukul "
                f"{int(row['hr']):02d}.00 dengan rata-rata "
                f"{row['cnt']:.2f} penyewaan."
            )

    st.info(" ".join(insight_q1))

st.divider()

# ==================================================
# PERTANYAAN BISNIS 2
# ==================================================

st.header("2. Pola Penyewaan Berdasarkan Cuaca dan Musim")

st.markdown(
    "Bagaimana perbedaan rata-rata jumlah penyewaan sepeda "
    "berdasarkan kondisi cuaca dan musim?"
)

# RATA-RATA PENYEWAAN BERDASARKAN CUACA
weather_analysis = (
    df_day_filtered.groupby("weather_label")["cnt"]
    .mean()
    .reset_index()
)

weather_order = [
    "Clear / Few Clouds",
    "Mist / Cloudy",
    "Light Rain / Snow",
    "Heavy Rain / Snow"
]

weather_analysis["weather_label"] = pd.Categorical(
    weather_analysis["weather_label"],
    categories=weather_order,
    ordered=True
)

weather_analysis = weather_analysis.sort_values("weather_label")

fig3 = px.bar(
    weather_analysis,
    x="weather_label",
    y="cnt",
    text_auto=".2f",
    title="Rata-rata Penyewaan Berdasarkan Kondisi Cuaca",
    labels={
        "weather_label": "Kondisi Cuaca",
        "cnt": "Rata-rata Penyewaan per Hari"
    }
)

# RATA-RATA PENYEWAAN BERDASARKAN MUSIM
season_analysis = (
    df_day_filtered.groupby("season_label")["cnt"]
    .mean()
    .reindex(["Spring", "Summer", "Fall", "Winter"])
    .reset_index()
)

fig4 = px.bar(
    season_analysis,
    x="season_label",
    y="cnt",
    text_auto=".2f",
    title="Rata-rata Penyewaan Berdasarkan Musim",
    labels={
        "season_label": "Musim",
        "cnt": "Rata-rata Penyewaan per Hari"
    }
)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.plotly_chart(fig4, use_container_width=True)

# INSIGHT PERTANYAAN 2 (DINAMIS)
st.subheader("Insight Pertanyaan 2")

if df_day_filtered.empty:
    st.info(
        "Tidak ada data penyewaan pada rentang tanggal yang dipilih."
    )
else:
    insight_q2 = []

    # CUACA DENGAN RATA-RATA TERTINGGI DAN TERENDAH
    weather_available = weather_analysis.dropna(
        subset=["cnt"]
    )

    if not weather_available.empty:
        weather_high = weather_available.loc[
            weather_available["cnt"].idxmax()
        ]

        weather_low = weather_available.loc[
            weather_available["cnt"].idxmin()
        ]

        insight_q2.append(
            f"Rata-rata penyewaan tertinggi berdasarkan cuaca "
            f"terdapat pada {weather_high['weather_label']} "
            f"({weather_high['cnt']:,.2f} penyewaan per hari), "
            f"sedangkan terendah terdapat pada "
            f"{weather_low['weather_label']} "
            f"({weather_low['cnt']:,.2f} penyewaan per hari)."
        )

    # MUSIM DENGAN RATA-RATA TERTINGGI DAN TERENDAH
    season_available = season_analysis.dropna(
        subset=["cnt"]
    )

    if not season_available.empty:
        season_high = season_available.loc[
            season_available["cnt"].idxmax()
        ]

        season_low = season_available.loc[
            season_available["cnt"].idxmin()
        ]

        insight_q2.append(
            f"Berdasarkan musim, rata-rata penyewaan tertinggi "
            f"terjadi pada musim {season_high['season_label']} "
            f"({season_high['cnt']:,.2f} penyewaan per hari), "
            f"sedangkan terendah terjadi pada musim "
            f"{season_low['season_label']} "
            f"({season_low['cnt']:,.2f} penyewaan per hari)."
        )

    st.info(" ".join(insight_q2))

st.divider()

# ==================================================
# ANALISIS KORELASI SPEARMAN
# ==================================================

st.header("3. Hubungan Kondisi Lingkungan dengan Penyewaan")

if len(df_day_filtered) >= 2:

    correlation_data = df_day_filtered[
        ["temp", "atemp", "hum", "windspeed", "cnt"]
    ].corr(method="spearman")

    correlation_result = (
        correlation_data["cnt"]
        .drop("cnt")
        .dropna()
        .sort_values(ascending=False)
        .reset_index()
    )

    correlation_result.columns = [
        "Variabel",
        "Korelasi Spearman"
    ]

    if not correlation_result.empty:

        fig5 = px.bar(
            correlation_result,
            x="Variabel",
            y="Korelasi Spearman",
            text_auto=".3f",
            title="Korelasi Spearman terhadap Jumlah Penyewaan",
            labels={
                "Variabel": "Variabel Lingkungan",
                "Korelasi Spearman": "Koefisien Korelasi"
            }
        )

        st.plotly_chart(
            fig5,
            use_container_width=True
        )

    else:
        st.info(
            "Korelasi belum dapat dihitung karena data pada "
            "rentang tanggal ini tidak memiliki variasi yang cukup."
        )

else:
    st.info(
        "Korelasi belum dapat dihitung. Pilih rentang tanggal "
        "yang mencakup minimal dua hari."
    )

st.caption(
    "Catatan: Korelasi menunjukkan hubungan antarvariabel, "
    "bukan hubungan sebab-akibat."
)

# FOOTER
st.divider()

st.caption(
    "Bike Sharing Data Analysis | Dataset periode 2011–2012"
)
