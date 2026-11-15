import math
from database import get_connection


def hitung_cf_kombinasi(nilai_cf):
    """Menggabungkan bukti CF positif untuk hipotesis kerusakan yang sama."""
    if not nilai_cf:
        return 0.0

    nilai_valid = []
    for nilai in nilai_cf:
        try:
            cf = float(nilai)
        except (TypeError, ValueError):
            raise ValueError("Nilai CF kombinasi harus berupa angka.")
        if not math.isfinite(cf) or not 0.0 <= cf <= 1.0:
            raise ValueError("Nilai CF kombinasi harus berada pada rentang 0 sampai 1.")
        nilai_valid.append(cf)

    cf_hasil = nilai_valid[0]
    for cf_selanjutnya in nilai_valid[1:]:
        cf_hasil = cf_hasil + cf_selanjutnya * (1.0 - cf_hasil)

    return min(1.0, max(0.0, cf_hasil))


def _normalisasi_gejala(gejala_dipilih):
    """Validasi dan normalisasi input menjadi {kode_gejala: CF_pengguna}."""
    if gejala_dipilih is None:
        return {}

    if isinstance(gejala_dipilih, dict):
        fakta_awal = {}
        for kode, nilai in gejala_dipilih.items():
            kode_normal = str(kode).strip().upper()
            if not kode_normal:
                raise ValueError("Kode gejala tidak boleh kosong.")
            try:
                nilai_normal = float(nilai)
            except (TypeError, ValueError):
                raise ValueError(f"Nilai keyakinan untuk {kode_normal} harus berupa angka.")
            if not math.isfinite(nilai_normal) or not 0.0 < nilai_normal <= 1.0:
                raise ValueError(
                    f"Nilai keyakinan untuk {kode_normal} harus lebih dari 0 dan maksimal 1."
                )
            fakta_awal[kode_normal] = nilai_normal
        return fakta_awal

    if isinstance(gejala_dipilih, (list, tuple, set)):
        fakta_awal = {}
        for kode in gejala_dipilih:
            kode_normal = str(kode).strip().upper()
            if not kode_normal:
                raise ValueError("Kode gejala tidak boleh kosong.")
            fakta_awal[kode_normal] = 1.0
        return fakta_awal

    raise TypeError("Input gejala harus berupa dictionary atau daftar kode gejala.")


def proses_diagnosis(gejala_dipilih):
    """
    Mesin inferensi satu tahap Forward Chaining dan Certainty Factor.

    Struktur aturan: satu gejala (fakta) -> satu jenis kerusakan (kesimpulan).
    CF Evidence = CF Pengguna x CF Pakar.
    Beberapa bukti positif untuk kerusakan yang sama digabungkan dengan
    CFcombine = CF1 + CF2 * (1 - CF1).
    """
    fakta_awal = _normalisasi_gejala(gejala_dipilih)
    if not fakta_awal:
        return []

    conn = get_connection()
    try:
        kode_valid = {
            row["kode"] for row in conn.execute("SELECT kode FROM gejala").fetchall()
        }
        kode_tidak_valid = sorted(set(fakta_awal) - kode_valid)
        if kode_tidak_valid:
            raise ValueError("Kode gejala tidak ditemukan: " + ", ".join(kode_tidak_valid))

        aturan_database = conn.execute("""
            SELECT a.id, a.kode_gejala, a.kode_kerusakan, a.bobot_cf,
                   g.nama_gejala, k.nama_kerusakan, k.deskripsi, k.solusi
            FROM aturan a
            JOIN gejala g ON g.kode = a.kode_gejala
            JOIN kerusakan k ON k.kode = a.kode_kerusakan
            ORDER BY a.id
        """).fetchall()

        hasil = {}
        jumlah_aturan_aktif = 0

        # Forward Chaining: fakta awal dicocokkan dengan anteseden setiap aturan.
        for aturan in aturan_database:
            kode_gejala = aturan["kode_gejala"]
            if kode_gejala not in fakta_awal:
                continue

            jumlah_aturan_aktif += 1
            kode_kerusakan = aturan["kode_kerusakan"]
            cf_pengguna = fakta_awal[kode_gejala]
            cf_pakar = float(aturan["bobot_cf"])
            cf_evidence = cf_pengguna * cf_pakar

            if kode_kerusakan not in hasil:
                hasil[kode_kerusakan] = {
                    "kode": kode_kerusakan,
                    "nama": aturan["nama_kerusakan"],
                    "deskripsi": aturan["deskripsi"],
                    "solusi": aturan["solusi"],
                    "nilai_cf": [],
                    "gejala_cocok": [],
                    "aturan_aktif": []
                }

            item = hasil[kode_kerusakan]
            item["nilai_cf"].append(cf_evidence)
            item["gejala_cocok"].append(kode_gejala)
            item["aturan_aktif"].append({
                "id_aturan": aturan["id"],
                "kode_gejala": kode_gejala,
                "nama_gejala": aturan["nama_gejala"],
                "kode_kerusakan": kode_kerusakan,
                "nama_kerusakan": aturan["nama_kerusakan"],
                "cf_pengguna": cf_pengguna,
                "cf_pakar": cf_pakar,
                "cf_evidence": round(cf_evidence, 4)
            })

        hasil_akhir = []
        for data in hasil.values():
            cf_gabungan = hitung_cf_kombinasi(data.pop("nilai_cf"))
            data["persentase"] = round(cf_gabungan * 100, 2)
            data["fakta_awal"] = [
                {"kode": kode, "cf_pengguna": nilai}
                for kode, nilai in fakta_awal.items()
            ]
            data["total_aturan_diperiksa"] = len(aturan_database)
            data["total_aturan_aktif"] = jumlah_aturan_aktif
            hasil_akhir.append(data)

        hasil_akhir.sort(key=lambda item: item["persentase"], reverse=True)
        return hasil_akhir
    finally:
        conn.close()
