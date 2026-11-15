# Rancang Bangun Sistem Pakar Diagnosa Kerusakan Perangkat Keras Komputer
**Berbasis Web Menggunakan Metode Certainty Factor dan Forward Chaining**

Repositori ini berisi *source code* aplikasi sistem pakar yang dibuat untuk memenuhi tugas mata kuliah **Sistem Pakar**.

## 👥 Disusun Oleh:
* Yayat Supriyatna (2026310051)
* Yuta Pratama (2025310045)
* Jujun (2021310104)
* Leliana Eka Fauziah (2020310091)

**Program Studi Teknik Informatika**
**Fakultas Informatika dan Desain**
**Universitas Bina Insani - Bekasi**

---

## 🚀 Tentang Proyek
Sistem pakar (Expert System) ini dikembangkan menggunakan Python untuk membantu menganalisis dan mendiagnosis masalah pada perangkat keras (hardware) komputer. Aplikasi ini bekerja dengan mencocokkan gejala-gejala kerusakan yang dialami untuk menemukan kemungkinan sumber masalah dan memberikan solusi perbaikan komponen fisik.

## 📂 Struktur Proyek
* `app.py` - File eksekusi utama aplikasi (Streamlit).
* `diagnosis.py` - Modul pemrosesan logika sistem pakar.
* `database.py` - Modul pengelolaan koneksi dan operasi database.
* `hardware_expert.db` - Database SQLite yang menyimpan pengetahuan sistem pakar.
* `test_diagnosis.py` - Pengujian otomatis (*unit testing*) untuk modul diagnosis.
* `requirements.txt` - Daftar dependensi/library Python yang dibutuhkan aplikasi.

## 🗄️ Database
Database menggunakan **SQLite** (`hardware_expert.db`), dibuat otomatis saat aplikasi pertama dijalankan.

| Tabel | Fungsi |
|---|---|
| `gejala` | Daftar gejala kerusakan (`kode`, `nama_gejala`, `deskripsi`) |
| `kerusakan` | Daftar jenis kerusakan + solusi (`kode`, `nama_kerusakan`, `deskripsi`, `solusi`) |
| `aturan` | Relasi gejala ↔ kerusakan beserta bobot CF (`kode_gejala`, `kode_kerusakan`, `bobot_cf`) |
| `riwayat` | Riwayat diagnosis lama (`nama_pengguna`, `tanggal`, `kode_kerusakan`, `hasil_cf`, `detail_gejala`) |
| `konsultasi` | Sesi konsultasi pengguna (`nama_pengguna`, `tanggal`, `gejala_json`) |
| `detail_konsultasi` | Hasil per kerusakan per sesi (`konsultasi_id`, `kode_kerusakan`, `hasil_cf`, `hasil_json`) |

## 🛠️ Cara Menjalankan Aplikasi
1. Pastikan **Python 3.10+** terinstal.
2. *Clone* repositori:
   ```bash
   git clone https://github.com/yutap88/sistem-pakar-hardware.git
   cd sistem-pakar-hardware
   ```
3. Buat & aktifkan virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # Linux/Mac
   ```
4. Instal dependensi:
   ```bash
   pip install -r requirements.txt
   ```
5. Jalankan aplikasi:
   ```bash
   streamlit run app.py
   ```
6. Buka browser di **http://localhost:8501** — aplikasi sudah hidup dan siap dipakai.

## ✅ Jalankan Test
```bash
python test_diagnosis.py
```
