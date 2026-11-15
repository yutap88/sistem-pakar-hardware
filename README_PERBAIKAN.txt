HARDWARE EXPERT SYSTEM - PAKET PERBAIKAN KODE

Isi paket:
- app.py              : aplikasi Streamlit yang telah dikoreksi
- database.py         : skema dan seed database, termasuk G13 dan aturan G13 -> P05
- diagnosis.py        : mesin Forward Chaining + Certainty Factor dengan validasi input ketat
- test_diagnosis.py   : 12 pengujian otomatis
- requirements.txt    : dependensi aplikasi Streamlit

CARA MEMASANG DI WINDOWS
1. Tutup aplikasi Streamlit yang sedang berjalan (Ctrl+C di terminal).
2. Backup file hardware_expert.db terlebih dahulu. Jangan hapus database lama.
3. Salin kelima file di atas ke folder D:\SISTEM_PAKAR_HARDWARE.
4. Pilih Replace jika Windows menanyakan penggantian app.py, database.py,
   diagnosis.py, test_diagnosis.py, dan requirements.txt.
5. Jangan mengganti atau menghapus hardware_expert.db.
6. Jalankan di terminal VS Code:
   pip install -r requirements.txt
   python -c "from database import initialize_database; initialize_database()"
   python -m unittest -v test_diagnosis
   streamlit run app.py

CATATAN DATABASE
- database.py menggunakan INSERT OR IGNORE untuk seed. Menambahkan G13 dan
  aturan G13 -> P05 (CF awal 0.80) tidak menghapus riwayat atau data yang sudah ada.
- Jika G13 atau aturannya sudah ada, seed tidak membuat duplikat dan tidak
  menimpa nilai yang sebelumnya dimasukkan melalui aplikasi.
- Simpan backup hardware_expert.db sebelum update.

HASIL PEMERIKSAAN PAKET
- Semua file Python lolos pemeriksaan sintaks.
- 12 pengujian otomatis diagnosis lulus pada database uji baru.
- Pengujian ini tidak membuktikan akurasi diagnosis dunia nyata atau validasi
  bobot CF oleh teknisi/pakar.

CATATAN TAILWIND DAN CLOUDFLARE
Paket ini masih merupakan versi Streamlit. Tailwind CSS tidak dapat langsung
menggantikan tampilan Streamlit seperti pada aplikasi React/Vite biasa.
Untuk Tailwind + Cloudflare, tahap berikutnya adalah migrasi frontend ke
React + Vite + Tailwind, backend API Python (FastAPI di Cloudflare Workers),
dan penyimpanan Cloudflare D1. Jangan mengunggah file SQLite lokal sebagai
penyimpanan produksi di Cloudflare Workers.
