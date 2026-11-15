import unittest
from diagnosis import hitung_cf_kombinasi, proses_diagnosis


class TestDiagnosis(unittest.TestCase):
    def test_gejala_kosong(self):
        self.assertEqual(proses_diagnosis([]), [])
        self.assertEqual(proses_diagnosis({}), [])
        self.assertEqual(proses_diagnosis(None), [])

    def test_g06_menghasilkan_p03_95_persen(self):
        hasil = proses_diagnosis(["G06"])
        p03 = next((item for item in hasil if item["kode"] == "P03"), None)
        self.assertIsNotNone(p03)
        self.assertAlmostEqual(p03["persentase"], 95.0, places=2)

    def test_cf_pengguna_dikalikan_cf_pakar(self):
        hasil = proses_diagnosis({"G06": 0.8})
        p03 = next(item for item in hasil if item["kode"] == "P03")
        self.assertAlmostEqual(p03["persentase"], 76.0, places=2)

    def test_kombinasi_cf(self):
        self.assertAlmostEqual(hitung_cf_kombinasi([0.5, 0.5]), 0.75, places=6)

    def test_g13_menghasilkan_p05(self):
        hasil = proses_diagnosis(["G13"])
        p05 = next((item for item in hasil if item["kode"] == "P05"), None)
        self.assertIsNotNone(p05)
        self.assertAlmostEqual(p05["persentase"], 80.0, places=2)

    def test_cf_nol_ditolak(self):
        with self.assertRaises(ValueError):
            proses_diagnosis({"G01": 0})

    def test_cf_negatif_ditolak(self):
        with self.assertRaises(ValueError):
            proses_diagnosis({"G01": -0.5})

    def test_cf_di_atas_satu_ditolak(self):
        with self.assertRaises(ValueError):
            proses_diagnosis({"G01": 1.1})

    def test_cf_nan_ditolak(self):
        with self.assertRaises(ValueError):
            proses_diagnosis({"G01": float("nan")})

    def test_cf_bukan_angka_ditolak(self):
        with self.assertRaises(ValueError):
            proses_diagnosis({"G01": "yakin sekali"})

    def test_kode_gejala_tidak_dikenal_ditolak(self):
        with self.assertRaises(ValueError):
            proses_diagnosis(["G99"])

    def test_input_tipe_tidak_didukung(self):
        with self.assertRaises(TypeError):
            proses_diagnosis("G01")


if __name__ == "__main__":
    unittest.main(verbosity=2)
