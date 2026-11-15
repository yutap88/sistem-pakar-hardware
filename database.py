
import sqlite3
import json
from pathlib import Path

# ==========================================
# KONFIGURASI DATABASE
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "hardware_expert.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ==========================================
# INISIALISASI DATABASE
# ==========================================

def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # TABEL GEJALA
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gejala (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kode TEXT UNIQUE NOT NULL,
                nama_gejala TEXT NOT NULL,
                deskripsi TEXT
            )
        """)

        # TABEL KERUSAKAN
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS kerusakan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kode TEXT UNIQUE NOT NULL,
                nama_kerusakan TEXT NOT NULL,
                deskripsi TEXT,
                solusi TEXT
            )
        """)

        # TABEL ATURAN
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS aturan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kode_gejala TEXT NOT NULL,
                kode_kerusakan TEXT NOT NULL,
                bobot_cf REAL NOT NULL,
                FOREIGN KEY (kode_gejala)
                    REFERENCES gejala(kode),
                FOREIGN KEY (kode_kerusakan)
                    REFERENCES kerusakan(kode),
                UNIQUE (kode_gejala, kode_kerusakan),
                CHECK (bobot_cf >= 0 AND bobot_cf <= 1)
            )
        """)

        # TABEL RIWAYAT
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS riwayat (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_pengguna TEXT NOT NULL,
                tanggal DATETIME DEFAULT CURRENT_TIMESTAMP,
                kode_kerusakan TEXT,
                hasil_cf REAL,
                detail_gejala TEXT,
                FOREIGN KEY (kode_kerusakan)
                    REFERENCES kerusakan(kode)
            )
        """)

        # TABEL KONSULTASI (satu baris untuk satu sesi diagnosis)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS konsultasi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_pengguna TEXT NOT NULL,
                tanggal DATETIME DEFAULT CURRENT_TIMESTAMP,
                gejala_json TEXT NOT NULL,
                sumber_migrasi TEXT UNIQUE
            )
        """)

        # TABEL DETAIL KONSULTASI (satu baris untuk satu kandidat kerusakan)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS detail_konsultasi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                konsultasi_id INTEGER NOT NULL,
                kode_kerusakan TEXT NOT NULL,
                hasil_cf REAL NOT NULL,
                hasil_json TEXT NOT NULL,
                legacy_riwayat_id INTEGER UNIQUE,
                FOREIGN KEY (konsultasi_id)
                    REFERENCES konsultasi(id) ON DELETE CASCADE,
                FOREIGN KEY (kode_kerusakan)
                    REFERENCES kerusakan(kode)
            )
        """)

        # ======================================
        # DATA GEJALA
        # ======================================

        data_gejala = [
            ("G01", "Komputer tidak menyala",
             "Komputer tidak merespons saat tombol power ditekan."),

            ("G02", "Kipas tidak berputar",
             "Kipas komputer tidak berputar."),

            ("G03", "Terdengar bunyi beep",
             "Komputer mengeluarkan bunyi beep saat dinyalakan."),

            ("G04", "Layar monitor blank",
             "Monitor tidak menampilkan gambar."),

            ("G05", "Komputer berjalan lambat",
             "Komputer membutuhkan waktu lama menjalankan aplikasi."),

            ("G06", "Hard disk berbunyi klik",
             "Terdengar bunyi klik tidak normal dari hard disk."),

            ("G07", "Komputer cepat panas",
             "Suhu komputer meningkat secara tidak normal."),

            ("G08", "Komputer sering restart sendiri",
             "Komputer restart tanpa perintah."),

            ("G09", "Layar bergaris",
             "Monitor menampilkan garis."),

            ("G10", "USB tidak terdeteksi",
             "Perangkat USB tidak terbaca."),

            ("G11", "No bootable device",
             "Komputer gagal menemukan perangkat booting."),

            ("G12", "Blue screen",
             "Komputer mengalami layar biru atau BSOD."),

            ("G13", "Kipas casing berputar tidak stabil",
             "Kipas casing berputar tidak stabil atau kecepatannya berubah-ubah."),

            # ======================================
            # GEJALA TAMBAHAN
            # Sumber: Data Dari sumber lain.xlsx (sheet Pengumpulan Data)
            # Alfarizi, G. A., & Yunita, D. (2026). Implementasi pendekatan
            # Certainty Factor untuk diagnosa kerusakan komputer berbasis web.
            # ======================================

            ("G14", "Lampu indikator monitor merah",
             "Lampu indikator pada monitor menyala merah."),

            ("G15", "Monitor menampilkan pesan No Signal",
             "Monitor menampilkan pesan \"No Signal\" saat komputer dinyalakan."),

            ("G16", "Layar monitor tampak redup",
             "Cahaya layar monitor berkurang atau tampak redup."),

            ("G17", "Aplikasi sering berhenti atau gagal",
             "Aplikasi keluar sendiri atau gagal dijalankan."),

            ("G18", "Sistem restart sebelum OS sempat dimuat",
             "Komputer restart kembali sebelum sistem operasi selesai dimuat."),

            ("G19", "Komputer tidak bisa dimatikan normal",
             "Proses shutdown tidak berjalan normal dan komputer tetap hidup."),

            ("G20", "Proses loading sistem operasi berhenti di tengah jalan",
             "Proses loading sistem operasi berhenti sebelum selesai."),

            ("G21", "Koneksi jaringan tidak stabil",
             "Koneksi jaringan tidak stabil meskipun sinyal tersedia."),

            ("G22", "Komputer sering mati mendadak",
             "Komputer mati tanpa proses penutupan normal."),

            ("G23", "Komputer sering freeze",
             "Komputer membeku dan tidak merespons input untuk beberapa waktu."),

            ("G24", "Area prosesor terasa sangat panas",
             "Komputer terasa sangat panas di area prosesor."),

            ("G25", "Keyboard tidak berfungsi",
             "Tombol keyboard tidak merespons saat ditekan."),

            ("G26", "Mouse tidak terdeteksi",
             "Mouse tidak terdeteksi oleh sistem."),

            ("G27", "Layar tidak menampilkan menu BIOS",
             "Layar tidak menampilkan menu awal BIOS saat komputer dinyalakan."),

            ("G28", "Muncul notifikasi kesalahan pada BIOS",
             "Tampilan BIOS menampilkan pesan kesalahan."),

            ("G29", "Perangkat keras tidak terdeteksi di BIOS",
             "Perangkat keras tidak terdeteksi pada daftar perangkat di BIOS."),

            ("G30", "Informasi perangkat pada BIOS tidak sesuai",
             "Informasi perangkat yang terbaca BIOS tidak sesuai dengan kondisi sebenarnya."),

            ("G31", "Waktu dan tanggal BIOS sering berubah",
             "Pengaturan waktu dan tanggal BIOS berubah sendiri secara berulang."),

            ("G32", "Perangkat eksternal sering putus-sambung",
             "Perangkat eksternal terputus dan tersambung kembali secara berulang."),

            ("G33", "Peringatan kekurangan memori",
             "Sistem menampilkan peringatan kekurangan memori."),

            ("G34", "Respon input lambat",
             "Sistem lambat merespons input pengguna."),

            ("G35", "Pemeriksaan disk selalu berjalan saat dinyalakan",
             "Proses pemeriksaan disk berjalan setiap kali komputer dinyalakan."),

            ("G36", "Kesalahan saat booting OS dari harddisk",
             "Sistem menampilkan kesalahan saat memuat OS dari harddisk."),

            ("G37", "Booting sangat lama",
             "Proses booting memakan waktu sangat lama."),

            ("G38", "File sering rusak",
             "Berkas pada sistem sering korup atau tidak dapat dibuka."),

            ("G39", "Pesan kesalahan aplikasi berbasis grafis",
             "Aplikasi berbasis grafis menampilkan pesan kesalahan."),

            ("G40", "Performa grafis tidak optimal",
             "Tampilan grafis berjalan tidak optimal atau tersendat."),

            ("G41", "Tampilan grafis pecah saat aplikasi berat",
             "Tampilan grafis pecah atau rusak saat menjalankan aplikasi berat."),

            ("G42", "Sebagian atau seluruh perangkat tidak menyala",
             "Sebagian atau seluruh perangkat komputer tidak mendapat daya.")
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO gejala
            (kode, nama_gejala, deskripsi)
            VALUES (?, ?, ?)
        """, data_gejala)

        # ======================================
        # DATA KERUSAKAN
        # ======================================

        data_kerusakan = [

            ("P01", "Power Supply (PSU) Bermasalah",
             "Gangguan pada komponen pemasok daya listrik komputer.",
             "Periksa kabel power dan konektor. "
             "Periksa PSU menggunakan teknisi dan ganti jika rusak."),

            ("P02", "RAM Bermasalah",
             "Gangguan pada Random Access Memory.",
             "Matikan komputer, periksa dan bersihkan konektor RAM. "
             "Uji RAM dan ganti jika terbukti rusak."),

            ("P03", "Hard Disk atau SSD Bermasalah",
             "Gangguan pada media penyimpanan komputer.",
             "Periksa koneksi penyimpanan dan lakukan pemeriksaan kesehatan "
             "disk. Segera cadangkan data jika terdeteksi kerusakan."),

            ("P04", "VGA atau Kartu Grafis Bermasalah",
             "Gangguan pada komponen pengolah grafis komputer.",
             "Periksa kabel monitor, konektor VGA, dan driver grafis. "
             "Uji kartu grafis jika diperlukan."),

            ("P05", "Sistem Pendingin Bermasalah",
             "Gangguan pada kipas atau sistem pendinginan komputer.",
             "Bersihkan kipas dan ventilasi, periksa kipas pendingin, "
             "serta periksa thermal paste jika diperlukan."),

            ("P06", "Motherboard Bermasalah",
             "Gangguan pada papan utama komputer.",
             "Periksa konektor, port, dan kondisi fisik motherboard. "
             "Lakukan pemeriksaan lebih lanjut oleh teknisi."),

            # ======================================
            # KERUSAKAN TAMBAHAN
            # Sumber: Data Dari sumber lain.xlsx (sheet Pengumpulan Data)
            # Alfarizi, G. A., & Yunita, D. (2026)
            # ======================================

            ("P07", "Monitor Bermasalah",
             "Gangguan pada tampilan atau perangkat monitor.",
             "Periksa kabel dan sumber sinyal monitor, uji monitor pada "
             "perangkat lain, dan ganti kabel atau panel bila rusak."),

            ("P08", "Sistem Operasi Bermasalah",
             "Gangguan pada sistem operasi komputer.",
             "Periksa file sistem, perbarui atau pasang ulang sistem operasi, "
             "dan cadangkan data sebelum melakukan perbaikan."),

            ("P09", "Prosesor Bermasalah",
             "Gangguan pada prosesor komputer.",
             "Pantau suhu prosesor, bersihkan sistem pendingin, ganti thermal "
             "paste, dan bawa ke teknisi bila prosesor rusak."),

            ("P10", "Keyboard Bermasalah",
             "Gangguan pada perangkat keyboard.",
             "Periksa koneksi keyboard, uji pada perangkat lain, bersihkan "
             "konektor, dan ganti keyboard bila tidak berfungsi."),

            ("P11", "Mouse Bermasalah",
             "Gangguan pada perangkat mouse.",
             "Periksa koneksi port atau Bluetooth, ganti baterai bila perlu, "
             "dan uji mouse pada perangkat lain."),

            ("P12", "BIOS atau CMOS Bermasalah",
             "Gangguan pada pengaturan BIOS atau baterai CMOS.",
             "Reset BIOS ke setelan pabrik, ganti baterai CMOS, dan perbarui "
             "firmware BIOS bila tersedia."),

            ("P13", "Driver atau Software Bermasalah",
             "Gangguan pada driver perangkat atau software sistem.",
             "Perbarui atau pasang ulang driver perangkat dan periksa "
             "Device Manager untuk konflik perangkat.")
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO kerusakan
            (kode, nama_kerusakan, deskripsi, solusi)
            VALUES (?, ?, ?, ?)
        """, data_kerusakan)

        # ======================================
        # BASIS ATURAN DAN BOBOT CF
        # ======================================

        # Bobot berikut merupakan bobot awal untuk
        # pengembangan sistem dan perlu divalidasi pakar.

        data_aturan = [

            # P01 - Power Supply
            ("G01", "P01", 0.90),
            ("G02", "P01", 0.75),
            ("G08", "P01", 0.65),

            # P02 - RAM
            ("G03", "P02", 0.85),
            ("G04", "P02", 0.65),
            ("G08", "P02", 0.50),
            ("G12", "P02", 0.80),

            # P03 - Hard Disk / SSD
            ("G05", "P03", 0.65),
            ("G06", "P03", 0.95),
            ("G11", "P03", 0.90),

            # P04 - VGA
            ("G04", "P04", 0.85),
            ("G09", "P04", 0.90),
            ("G12", "P04", 0.50),

            # P05 - Sistem Pendingin
            ("G02", "P05", 0.85),
            ("G07", "P05", 0.95),
            ("G08", "P05", 0.65),
            ("G13", "P05", 0.80),

            # P06 - Motherboard
            ("G01", "P06", 0.70),
            ("G03", "P06", 0.60),
            ("G08", "P06", 0.55),
            ("G10", "P06", 0.70),

            # ======================================
            # ATURAN TAMBAHAN (tanpa menimpa aturan yang sudah ada)
            # Sumber: Data Dari sumber lain.xlsx (sheet Pengumpulan Data)
            # Alfarizi, G. A., & Yunita, D. (2026)
            # ======================================

            # P01 - Power Supply
            ("G42", "P01", 0.90),

            # P02 - RAM
            ("G05", "P02", 0.60),
            ("G33", "P02", 0.80),
            ("G34", "P02", 0.60),

            # P03 - Hard Disk / SSD
            ("G20", "P03", 0.80),
            ("G35", "P03", 0.80),
            ("G36", "P03", 0.80),
            ("G37", "P03", 0.70),
            ("G38", "P03", 0.80),

            # P04 - VGA
            ("G39", "P04", 0.70),
            ("G40", "P04", 0.70),
            ("G41", "P04", 0.80),

            # P05 - Sistem Pendingin
            ("G22", "P05", 0.80),

            # P06 - Motherboard
            ("G27", "P06", 0.70),

            # P07 - Monitor
            ("G04", "P07", 0.80),
            ("G09", "P07", 0.60),
            ("G14", "P07", 0.80),
            ("G15", "P07", 0.80),
            ("G16", "P07", 0.70),

            # P08 - Sistem Operasi
            ("G12", "P08", 0.90),
            ("G17", "P08", 0.60),
            ("G18", "P08", 0.70),
            ("G19", "P08", 0.60),
            ("G20", "P08", 0.70),
            ("G21", "P08", 0.50),

            # P09 - Prosesor
            ("G07", "P09", 0.80),
            ("G12", "P09", 0.90),
            ("G22", "P09", 0.80),
            ("G23", "P09", 0.70),
            ("G24", "P09", 0.80),

            # P10 - Keyboard
            ("G25", "P10", 0.90),

            # P11 - Mouse
            ("G26", "P11", 0.90),

            # P12 - BIOS / CMOS
            ("G03", "P12", 0.80),
            ("G27", "P12", 0.90),
            ("G28", "P12", 0.90),
            ("G29", "P12", 0.90),
            ("G30", "P12", 0.80),
            ("G31", "P12", 0.90),

            # P13 - Driver / Software
            ("G10", "P13", 0.80),
            ("G17", "P13", 0.70),
            ("G32", "P13", 0.70)
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO aturan
            (kode_gejala, kode_kerusakan, bobot_cf)
            VALUES (?, ?, ?)
        """, data_aturan)

        conn.commit()

        # Migrasi aman: salin data riwayat lama tanpa menghapus tabel riwayat.
        migrasi_riwayat_lama(conn)

        print("DATABASE BERHASIL DIINISIALISASI")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


# ==========================================
# MIGRASI RIWAYAT LAMA
# ==========================================

def migrasi_riwayat_lama(conn=None):
    """
    Menyalin riwayat lama ke struktur konsultasi + detail_konsultasi.

    Riwayat lama dikelompokkan berdasarkan nama_pengguna, tanggal,
    dan detail_gejala. Tabel riwayat lama tidak dihapus atau diubah.
    legacy_riwayat_id mencegah satu baris lama dimigrasikan berulang.
    """
    koneksi_dibuat_di_fungsi = conn is None
    if koneksi_dibuat_di_fungsi:
        conn = get_connection()

    try:
        rows = conn.execute("""
            SELECT
                r.id,
                r.nama_pengguna,
                r.tanggal,
                r.kode_kerusakan,
                r.hasil_cf,
                r.detail_gejala
            FROM riwayat r
            LEFT JOIN detail_konsultasi d
                ON d.legacy_riwayat_id = r.id
            WHERE d.id IS NULL
            ORDER BY r.tanggal, r.nama_pengguna, r.detail_gejala, r.id
        """).fetchall()

        kelompok = {}
        for row in rows:
            kunci = (
                row["nama_pengguna"] or "",
                row["tanggal"] or "",
                row["detail_gejala"] or ""
            )
            kelompok.setdefault(kunci, []).append(row)

        for (nama, tanggal, detail_gejala), daftar in kelompok.items():
            sumber = json.dumps(
                [nama, tanggal, detail_gejala],
                ensure_ascii=False
            )

            konsultasi = conn.execute("""
                SELECT id FROM konsultasi WHERE sumber_migrasi = ?
            """, (sumber,)).fetchone()

            if konsultasi:
                konsultasi_id = konsultasi["id"]
            else:
                daftar_kode = [
                    kode.strip()
                    for kode in (detail_gejala or "").split(",")
                    if kode.strip()
                ]
                gejala_json = json.dumps(
                    {kode: 1.0 for kode in daftar_kode},
                    ensure_ascii=False
                )
                cursor = conn.execute("""
                    INSERT INTO konsultasi
                        (nama_pengguna, tanggal, gejala_json, sumber_migrasi)
                    VALUES (?, ?, ?, ?)
                """, (nama, tanggal, gejala_json, sumber))
                konsultasi_id = cursor.lastrowid

            for row in daftar:
                payload = {
                    "kode": row["kode_kerusakan"],
                    "persentase": float(row["hasil_cf"] or 0),
                    "catatan_migrasi": (
                        "Data berasal dari tabel riwayat versi sebelumnya. "
                        "Rincian aturan/CF per gejala tidak tersedia pada data lama."
                    )
                }
                conn.execute("""
                    INSERT OR IGNORE INTO detail_konsultasi
                        (konsultasi_id, kode_kerusakan, hasil_cf,
                         hasil_json, legacy_riwayat_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    konsultasi_id,
                    row["kode_kerusakan"],
                    float(row["hasil_cf"] or 0),
                    json.dumps(payload, ensure_ascii=False),
                    row["id"]
                ))

        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        if koneksi_dibuat_di_fungsi:
            conn.close()
