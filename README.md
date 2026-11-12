# Bike Sharing Data Analysis

## Deskripsi Proyek

Proyek ini bertujuan untuk menganalisis pola penyewaan sepeda berdasarkan waktu, jenis hari, kondisi cuaca, dan musim menggunakan Bike Sharing Dataset. Data yang digunakan terdiri dari data penyewaan per jam (`hour.csv`) dan data penyewaan per hari (`day.csv`) selama periode 2011–2012.

Analisis dilakukan untuk memahami pola permintaan penyewaan sepeda serta mengetahui faktor lingkungan yang memiliki keterkaitan dengan jumlah penyewaan.

## Business Questions

Analisis ini berfokus pada dua pertanyaan bisnis:

1. Bagaimana perbedaan rata-rata jumlah penyewaan sepeda per jam antara hari kerja (_working day_) dan hari non-kerja (_weekend/holiday_) selama periode 2011–2012, serta pada jam berapa permintaan penyewaan mencapai puncaknya?

2. Bagaimana perbedaan rata-rata jumlah penyewaan sepeda berdasarkan kondisi cuaca (_weathersit_) dan musim (_season_) selama periode 2011–2012, serta kondisi mana yang berkaitan dengan tingkat permintaan tertinggi dan terendah?

## Tahapan Analisis

Tahapan yang dilakukan dalam proyek ini meliputi:

1. **Data Gathering**: Mengumpulkan dan membaca dataset penyewaan sepeda.
2. **Data Assessing**: Memeriksa kualitas data, seperti missing values, duplikasi, tipe data, dan konsistensi data.
3. **Data Cleaning**: Memastikan data siap digunakan untuk proses analisis.
4. **Exploratory Data Analysis (EDA)**: Mengeksplorasi pola penyewaan berdasarkan waktu, jenis hari, cuaca, dan musim.
5. **Data Visualization**: Menampilkan hasil analisis dalam bentuk grafik agar pola data lebih mudah dipahami.
6. **Analisis Lanjutan**: Membandingkan rata-rata penyewaan dan menggunakan korelasi Spearman untuk melihat hubungan antara kondisi lingkungan dan jumlah penyewaan.
7. **Conclusion**: Menyusun kesimpulan dan rekomendasi berdasarkan hasil analisis.

## Hasil Analisis

Beberapa hasil utama dari analisis ini adalah:

- Rata-rata penyewaan pada hari kerja sebesar 193,21 penyewaan per jam, sedangkan hari non-kerja sebesar 181,41 penyewaan per jam.
- Puncak penyewaan pada hari kerja terjadi sekitar pukul 17.00, sedangkan pada hari non-kerja sekitar pukul 13.00.
- Kondisi cuaca cerah atau sedikit berawan memiliki rata-rata penyewaan tertinggi di antara kategori cuaca yang tersedia.
- Musim Fall memiliki rata-rata penyewaan tertinggi, sedangkan Spring memiliki rata-rata terendah.
- Korelasi Spearman menunjukkan hubungan positif antara suhu dan jumlah penyewaan sepeda.

## Tools dan Libraries

Proyek ini menggunakan beberapa tools dan library berikut:

- Python 3.13.7
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Streamlit
- Google Colab / Jupyter Notebook

## Struktur Folder

```text
submission/
├── dashboard/
│   └── dashboard.py
├── data/
│   ├── hour.csv
│   └── day.csv
├── Proyek_Analisis_Data.ipynb
├── requirements.txt
├── README.md
└── url.txt
```

## Setup Environment - Anaconda

```bash
conda create --name bike-sharing python=3.13
conda activate bike-sharing
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal

```bash
pip install -r requirements.txt
```

## Cara Menjalankan Dashboard

1. Pastikan Python sudah terinstal.
2. Clone atau download repository proyek ini.
3. Buka terminal pada folder utama proyek.
4. Instal library yang dibutuhkan dengan perintah:

```bash
pip install -r requirements.txt
```

5. Jalankan dashboard menggunakan perintah:

```bash
streamlit run dashboard/dashboard.py
```

6. Dashboard akan terbuka melalui browser pada alamat lokal yang disediakan oleh Streamlit.

## Dashboard

Dashboard dibuat menggunakan Streamlit untuk menampilkan ringkasan data, visualisasi pola penyewaan, serta hasil analisis berdasarkan pertanyaan bisnis.

Link Dashboard: https://bike-sharing-analysis-devi.streamlit.app

## Dataset

Dataset yang digunakan adalah Bike Sharing Dataset yang terdiri dari:

- `hour.csv`: Data penyewaan sepeda berdasarkan jam.
- `day.csv`: Data penyewaan sepeda berdasarkan hari.
