# 📡 Prediksi Lokasi Rektorat – Streamlit App

Aplikasi Streamlit ini memprediksi **lantai** tempat Anda berada di Gedung Rektorat Kampus Sindangsari dengan memanfaatkan:
1. **Snapshot Wi-Fi** (BSSID, signal, dan frekuensi).
2. **Koordinat GPS** (latitude & longitude).
3. Model **SVM** terlatih (`svm_model.pkl`).

Aplikasi kini mendukung **tiga** metode input:

| Metode | Deskripsi |
| ------ | --------- |
| **Otomatis (Wi-Fi Snapshot)** | Ambil data Wi-Fi & lokasi secara langsung dari laptop/PC Anda. |
| **Manual** | Masukkan nilai fitur satu per satu di antarmuka. |
| **Upload CSV** | Unggah file `.csv` berisi deretan nilai RSSI/fitur. Cocok untuk batch prediksi. |

---

## ✨ Fitur Utama
- **Validasi “semua nol”**  
  Jika semua fitur bernilai `0`, aplikasi menampilkan pesan:  
  > *Pastikan berada di Rektorat Sindangsari. Jika sudah di sana, silakan coba pindah lokasi.*
- **Prediksi Multi-baris (CSV)**  
  Satu file bisa berisi banyak baris; hasil ditampilkan per baris.
- **Skalasi Fitur Otomatis**  
  Menggunakan `StandardScaler` yang telah di-fit pada dataset pelatihan.
- **Tampilan Ringkas**  
  Menggunakan ikon dan emoji agar antarmuka lebih ramah pengguna.

---

## 🛠️ Persyaratan

| Komponen | Versi Minimum |
|----------|---------------|
| Python   | 3.9 |
| Streamlit| 1.33 |
| scikit-learn | 1.4 |
| pandas   | 2.2 |
| numpy    | 1.26 |
| joblib   | 1.4 |
| pywifi   | 1.3 |
| Windows  | 10/11 (untuk PowerShell + pywifi) |

> **Catatan:** Pada Linux/macOS Anda dapat menjalankan mode **Upload CSV** dan **Manual**, tetapi snapshot Wi-Fi & GPS otomatis mungkin memerlukan penyesuaian skrip.

---

## 🚀 Instalasi

```bash
# 1. Klon repositori
git clone https://github.com/username/rektorat-lantai-prediksi.git
cd rektorat-lantai-prediksi

# 2. Buat dan aktifkan virtualenv (opsional tapi disarankan)
python -m venv venv
source venv/Scripts/activate   # Windows: venv\Scripts\activate

# 3. Instal dependensi
pip install -r requirements.txt
```

File **`requirements.txt`** minimal:

```
streamlit
scikit-learn
pandas
numpy
pywifi
joblib
```

---

## 🏃 Menjalankan Aplikasi

```bash
streamlit run main.py
```

Kemudian buka browser di `http://localhost:8501`.

---

## 📑 Format CSV

- **Tanpa header.**
- **Satu baris** mewakili **satu snapshot**.
- Jika CSV hanya satu baris, baris tersebut akan otomatis di-transpos (kolom → fitur).
- Setiap nilai harus urut sesuai urutan **`feature_names`** pada `dataset_model_per_lantai.csv`.

Contoh baris (dipotong):

```
-100.0,-100.0,-81.0,-80.0,-50.0,-84.0, ... , -79.0,-79.0,-76.0
```

---

## 🧐 Troubleshooting

| Masalah | Solusi |
|---------|--------|
| **Error: gagal mendeteksi jaringan atau lokasi** | Pastikan Wi-Fi dan lokasi (GPS) aktif. Jalankan Terminal/PowerShell sebagai Administrator. |
| **Pesan “Pastikan berada di Rektorat Sindangsari…” padahal sudah di lokasi** | Coba **pindah beberapa meter** atau ulangi scan; sinyal Wi-Fi dapat terhalang. |
| **Jumlah kolom CSV ≠ jumlah fitur** | Periksa file CSV, pastikan jumlah nilai sama dengan banyaknya fitur di `feature_names`. |

---
