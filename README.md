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
* `app.py` - File eksekusi utama aplikasi.
* `diagnosis.py` - Modul pemrosesan logika sistem pakar.
* `database.py` - Modul pengelolaan koneksi dan operasi database.
* `hardware_expert.db` - Database SQLite yang menyimpan pengetahuan sistem pakar.
* `test_diagnosis.py` - Pengujian otomatis (*unit testing*) untuk modul diagnosis.
* `requirements.txt` - Daftar dependensi/library Python yang dibutuhkan aplikasi.

## 🛠️ Cara Menjalankan Aplikasi
1. Pastikan **Python** telah terinstal di perangkat Anda.
2. *Clone* repositori ini ke komputer lokal Anda:
   ```bash
   git clone [https://github.com/yutap88/sistem-pakar-hardware.git](https://github.com/yutap88/sistem-pakar-hardware.git)
