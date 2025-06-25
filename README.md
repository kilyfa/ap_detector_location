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

## 🗂️ Struktur Proyek
