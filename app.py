
import streamlit as st
import json
from database import initialize_database, get_connection
from diagnosis import proses_diagnosis

# ==========================================
# KONFIGURASI APLIKASI
# ==========================================

st.set_page_config(
    page_title="Hardware Expert System",
    page_icon="💻",
    layout="wide"
)

initialize_database()

# ==========================================
# NAVY BLUE MODERN THEME
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #F4F7FC;
}

[data-testid="stSidebar"] {
    background-color: #101D36;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.main-title {
    color: #142B4A;
    font-size: 36px;
    font-weight: 800;
}

.subtitle {
    color: #64748B;
    font-size: 16px;
}

div[data-testid="stMetric"] {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
}

div.stButton > button {
    background-color: #142B4A;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 10px 20px;
}

div.stButton > button:hover {
    background-color: #244A75;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# FUNGSI FORMAT PILIHAN
# ==========================================

def format_kerusakan(kode, data):
    for row in data:
        if row["kode"] == kode:
            return f"{row['kode']} - {row['nama_kerusakan']}"
    return kode


def reset_form_diagnosis():
    """Bersihkan hasil dan seluruh input saat pengguna memulai diagnosis baru."""
    st.session_state.pop("hasil_diagnosis", None)
    st.session_state["nama_pengguna_diagnosis"] = ""
    for key in list(st.session_state.keys()):
        if key.startswith("keyakinan_"):
            st.session_state[key] = "Tidak dipilih"


# ==========================================
# SIDEBAR NAVIGASI
# ==========================================

st.sidebar.title("💻 HARDWARE EXPERT")
st.sidebar.caption("Sistem Pakar Diagnosa Komputer")

menu = st.sidebar.radio(
    "MENU NAVIGASI",
    [
        "Dashboard",
        "Diagnosa",
        "Basis Pengetahuan",
        "Data Kerusakan",
        "Riwayat Diagnosis",
        "Pengujian Sistem",
        "Tentang"
    ]
)

st.sidebar.divider()
st.sidebar.caption("Hardware Expert System v1.0")


# ==========================================
# DASHBOARD
# ==========================================

if menu == "Dashboard":

    st.markdown(
        '<h1 class="main-title">Dashboard</h1>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">Selamat datang di Hardware Expert System. '
        'Sistem Pakar Diagnosa Kerusakan Perangkat Keras Komputer.</p>',
        unsafe_allow_html=True
    )

    conn = get_connection()

    total_gejala = conn.execute(
        "SELECT COUNT(*) FROM gejala"
    ).fetchone()[0]

    total_kerusakan = conn.execute(
        "SELECT COUNT(*) FROM kerusakan"
    ).fetchone()[0]

    total_aturan = conn.execute(
        "SELECT COUNT(*) FROM aturan"
    ).fetchone()[0]

    # Hasil diagnosis baru disimpan pada detail_konsultasi, bukan tabel riwayat lama.
    total_hasil_diagnosis = conn.execute(
        "SELECT COUNT(*) FROM detail_konsultasi"
    ).fetchone()[0]

    conn.close()

    st.markdown("### Ringkasan Sistem")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Gejala", total_gejala)

    with col2:
        st.metric("Jenis Kerusakan", total_kerusakan)

    with col3:
        st.metric("Total Aturan", total_aturan)

    with col4:
        st.metric("Total Hasil Diagnosis", total_hasil_diagnosis)

    st.divider()

    st.markdown("### Metode Sistem Pakar")

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            "**🔍 Forward Chaining**\n\n"
            "Metode penalaran menggunakan fakta atau gejala "
            "untuk memperoleh kesimpulan."
        )

    with col2:
        st.info(
            "**📊 Certainty Factor**\n\n"
            "Metode untuk menghitung tingkat keyakinan "
            "terhadap hasil diagnosis kerusakan."
        )

    st.divider()

    st.markdown("### Mulai Pemeriksaan")

    st.write(
        "Pilih menu Diagnosa untuk memulai pemeriksaan "
        "kerusakan perangkat keras komputer."
    )

    if st.button("🔍 Mulai Diagnosis"):
        st.info("Silakan pilih menu Diagnosa pada navigasi.")


# ==========================================
# MENU DIAGNOSA
# ==========================================

elif menu == "Diagnosa":

    st.header("🔍 Diagnosa Kerusakan Hardware")

    st.write(
        "Silakan isi identitas dan pilih gejala "
        "yang dialami perangkat komputer."
    )

    conn = get_connection()

    data_gejala = conn.execute("""
        SELECT kode, nama_gejala, deskripsi
        FROM gejala
        ORDER BY kode
    """).fetchall()

    conn.close()

    with st.form("form_diagnosis"):

        st.subheader("Identitas Pengguna")

        nama_pengguna = st.text_input(
            "Nama Pengguna",
            placeholder="Masukkan nama pengguna",
            key="nama_pengguna_diagnosis"
        )

        st.divider()

        st.subheader("Pilih Gejala Kerusakan")

        st.caption(
            "Pilih gejala yang dialami komputer dan tentukan "
            "tingkat keyakinan Anda terhadap setiap gejala."
        )

        pilihan_keyakinan = {
            "Tidak yakin": 0.2,
            "Kurang yakin": 0.4,
            "Cukup yakin": 0.6,
            "Yakin": 0.8,
            "Sangat yakin": 1.0
        }

        gejala_dipilih = {}

        for gejala in data_gejala:

            st.markdown(
                f"**{gejala['kode']} - {gejala['nama_gejala']}**"
            )

            if gejala["deskripsi"]:
                st.caption(gejala["deskripsi"])

            pilihan = st.selectbox(
                "Tingkat keyakinan",
                options=[
                    "Tidak dipilih",
                    "Tidak yakin",
                    "Kurang yakin",
                    "Cukup yakin",
                    "Yakin",
                    "Sangat yakin"
                ],
                index=0,
                key=f"keyakinan_{gejala['kode']}"
            )

            if pilihan != "Tidak dipilih":
                gejala_dipilih[gejala["kode"]] = (
                    pilihan_keyakinan[pilihan]
                )

            st.divider()

        proses = st.form_submit_button(
            "🔍 Proses Diagnosis",
            use_container_width=True
        )

        if proses:

            # Hapus hasil diagnosis sebelumnya setiap kali formulir dikirim.
            # Hasil lama tidak akan tertinggal jika input baru tidak valid.
            st.session_state.pop("hasil_diagnosis", None)

            if not nama_pengguna.strip():

                st.error("Nama pengguna wajib diisi.")

            elif not gejala_dipilih:

                st.warning("Silakan pilih minimal satu gejala.")

            else:

                try:

                    hasil = proses_diagnosis(gejala_dipilih)

                    if hasil:

                        conn = get_connection()

                        try:

                            # Satu konsultasi untuk satu proses diagnosis.
                            cursor = conn.execute("""
                                INSERT INTO konsultasi (
                                    nama_pengguna,
                                    gejala_json
                                )
                                VALUES (?, ?)
                            """, (
                                nama_pengguna.strip(),
                                json.dumps(gejala_dipilih, ensure_ascii=False)
                            ))
                            konsultasi_id = cursor.lastrowid

                            # Setiap kandidat kerusakan disimpan sebagai detail.
                            for data in hasil:
                                conn.execute("""
                                    INSERT INTO detail_konsultasi (
                                        konsultasi_id,
                                        kode_kerusakan,
                                        hasil_cf,
                                        hasil_json
                                    )
                                    VALUES (?, ?, ?, ?)
                                """, (
                                    konsultasi_id,
                                    data["kode"],
                                    data["persentase"],
                                    json.dumps(data, ensure_ascii=False)
                                ))

                            conn.commit()

                        except Exception:
                            conn.rollback()
                            raise

                        finally:
                            conn.close()

                        st.session_state["hasil_diagnosis"] = {
                            "nama": nama_pengguna.strip(),
                            "gejala": gejala_dipilih,
                            "hasil": hasil
                        }

                        st.success(
                            "Diagnosis berhasil diproses dan "
                            "seluruh hasil berhasil disimpan."
                        )

                    else:

                        st.session_state["hasil_diagnosis"] = {
                            "nama": nama_pengguna.strip(),
                            "gejala": gejala_dipilih,
                            "hasil": []
                        }

                        st.warning(
                            "Tidak ditemukan kerusakan "
                            "berdasarkan gejala yang dipilih."
                        )

                except Exception as e:

                    st.error(
                        f"Terjadi kesalahan saat diagnosis: {e}"
                    )

    # ======================================
    # HASIL DIAGNOSIS
    # ======================================

    if "hasil_diagnosis" in st.session_state:

        hasil_data = st.session_state["hasil_diagnosis"]

        st.divider()

        st.header("📋 Hasil Diagnosis")

        st.write(
            f"**Nama Pengguna:** {hasil_data['nama']}"
        )

        st.write("**Gejala dan tingkat keyakinan yang dipilih:**")

        gejala_hasil = hasil_data["gejala"]

        if isinstance(gejala_hasil, dict):
            for kode, nilai in gejala_hasil.items():
                st.write(f"- {kode}: {nilai:.1f} ({nilai * 100:.0f}%)")
        else:
            # Kompatibilitas dengan hasil diagnosis dari versi aplikasi lama
            for kode in gejala_hasil:
                st.write(f"- {kode}: Keyakinan 1.0 (100%)")

        hasil = hasil_data["hasil"]

        if hasil:
            # Ringkasan penelusuran Forward Chaining.
            with st.expander("🔎 Lihat Proses Penelusuran Forward Chaining", expanded=True):
                st.markdown("**Tahap 1 — Fakta awal**")
                st.write(
                    "Fakta awal merupakan gejala yang dipilih pengguna "
                    "beserta tingkat keyakinannya."
                )
                if isinstance(gejala_hasil, dict):
                    for kode, nilai in gejala_hasil.items():
                        st.write(f"- {kode}: CF pengguna {nilai:.2f}")
                else:
                    for kode in gejala_hasil:
                        st.write(f"- {kode}: CF pengguna 1.00")

                aturan_aktif_unik = {}
                for hasil_item in hasil:
                    for aturan_item in hasil_item.get("aturan_aktif", []):
                        aturan_aktif_unik[aturan_item["id_aturan"]] = aturan_item

                st.markdown("**Tahap 2 — Pencocokan aturan**")
                st.write(
                    f"Sistem memeriksa aturan pada basis pengetahuan dan "
                    f"menemukan {len(aturan_aktif_unik)} aturan aktif "
                    f"yang cocok dengan fakta awal."
                )
                if aturan_aktif_unik:
                    for aturan_item in aturan_aktif_unik.values():
                        st.write(
                            f"- IF {aturan_item['kode_gejala']} "
                            f"THEN {aturan_item.get('kode_kerusakan', '')} "
                            f"| CF pakar: {aturan_item['cf_pakar']:.2f}"
                        )

                st.markdown("**Tahap 3 — Kesimpulan sementara**")
                st.write(
                    "Setiap aturan aktif menghasilkan kandidat kerusakan. "
                    "Kandidat dengan gejala pendukung yang sama kemudian "
                    "dihitung nilai CF gabungannya."
                )
                for nomor_kandidat, kandidat in enumerate(hasil, start=1):
                    st.write(
                        f"{nomor_kandidat}. {kandidat['kode']} — "
                        f"{kandidat['nama']}: {kandidat['persentase']:.2f}%"
                    )

            st.caption(
                "Catatan metode: aturan pada basis pengetahuan saat ini "
                "berbentuk satu gejala menuju satu kerusakan (IF gejala THEN "
                "kerusakan). Sistem melakukan pencocokan fakta awal terhadap "
                "aturan tersebut; belum menggunakan aturan dengan beberapa "
                "gejala sebagai premis AND."
            )

            for nomor, data in enumerate(hasil, start=1):

                st.divider()

                st.subheader(
                    f"{nomor}. {data['nama']}"
                )

                st.write(
                    f"**Kode Kerusakan:** {data['kode']}"
                )

                st.metric(
                    "Tingkat Keyakinan",
                    f"{data['persentase']}%"
                )

                st.progress(
                    max(
                        0.0,
                        min(
                            1.0,
                            float(data["persentase"]) / 100
                        )
                    )
                )

                st.markdown("**Deskripsi Kerusakan:**")

                st.info(data.get("deskripsi") or "-")

                st.markdown("**Solusi Perbaikan:**")

                st.success(data.get("solusi") or "-")

                st.markdown("**Gejala Pendukung:**")

                for kode in data.get("gejala_cocok", []):
                    st.write(f"- {kode}")

                st.markdown("**Rincian Perhitungan Certainty Factor:**")

                for aturan in data.get("aturan_aktif", []):
                    st.write(
                        f"- Aturan ID {aturan['id_aturan']} | "
                        f"{aturan['kode_gejala']}: "
                        f"CF Pengguna = {aturan['cf_pengguna']:.2f}, "
                        f"CF Pakar = {aturan['cf_pakar']:.2f}, "
                        f"CF Evidence = {aturan['cf_evidence']:.4f}"
                    )

        else:

            st.warning(
                "Tidak ditemukan kerusakan berdasarkan gejala."
            )

        st.button(
            "🔄 Diagnosis Baru",
            on_click=reset_form_diagnosis,
            key="tombol_diagnosis_baru"
        )



# ==========================================
# MENU BASIS PENGETAHUAN
# ==========================================

elif menu == "Basis Pengetahuan":

    st.header("📚 Basis Pengetahuan")
    st.write(
        "Kelola data gejala dan aturan yang digunakan "
        "oleh metode Forward Chaining dan Certainty Factor."
    )

    tab_gejala, tab_aturan, tab_relasi = st.tabs(
        ["🩺 Data Gejala", "⚙️ Aturan Diagnosis", "🔗 Peta Aturan"]
    )

    # ======================================
    # TAB DATA GEJALA
    # ======================================

    with tab_gejala:

        conn = get_connection()
        data_gejala_bp = conn.execute("""
            SELECT kode, nama_gejala, deskripsi
            FROM gejala
            ORDER BY kode
        """).fetchall()
        conn.close()

        st.subheader("Daftar Gejala")

        st.metric("Total Gejala", len(data_gejala_bp))

        if data_gejala_bp:
            st.dataframe(
                [
                    {
                        "Kode": row["kode"],
                        "Nama Gejala": row["nama_gejala"],
                        "Deskripsi": row["deskripsi"] or "-"
                    }
                    for row in data_gejala_bp
                ],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Belum ada data gejala.")

        st.divider()
        st.subheader("➕ Tambah Gejala")

        with st.form("form_tambah_gejala"):
            kode_gejala_baru = st.text_input(
                "Kode Gejala", placeholder="Contoh: G13"
            ).strip().upper()
            nama_gejala_baru = st.text_input("Nama Gejala")
            deskripsi_gejala_baru = st.text_area("Deskripsi Gejala")

            tambah_gejala = st.form_submit_button(
                "Simpan Gejala", use_container_width=True
            )

            if tambah_gejala:
                if not kode_gejala_baru or not nama_gejala_baru.strip():
                    st.error("Kode dan nama gejala wajib diisi.")
                else:
                    conn = get_connection()
                    try:
                        conn.execute("""
                            INSERT INTO gejala (kode, nama_gejala, deskripsi)
                            VALUES (?, ?, ?)
                        """, (
                            kode_gejala_baru,
                            nama_gejala_baru.strip(),
                            deskripsi_gejala_baru.strip()
                        ))
                        conn.commit()
                        st.success("Gejala berhasil ditambahkan.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Gagal menambahkan gejala: {e}")
                    finally:
                        conn.close()

        st.divider()
        st.subheader("✏️ Edit Gejala")

        if data_gejala_bp:
            kode_edit_gejala = st.selectbox(
                "Pilih gejala yang akan diedit",
                [row["kode"] for row in data_gejala_bp],
                key="bp_pilih_edit_gejala"
            )
            item_gejala = next(
                row for row in data_gejala_bp
                if row["kode"] == kode_edit_gejala
            )

            with st.form("form_edit_gejala"):
                nama_edit_gejala = st.text_input(
                    "Nama Gejala",
                    value=item_gejala["nama_gejala"]
                )
                deskripsi_edit_gejala = st.text_area(
                    "Deskripsi Gejala",
                    value=item_gejala["deskripsi"] or ""
                )
                simpan_edit_gejala = st.form_submit_button(
                    "Simpan Perubahan", use_container_width=True
                )

                if simpan_edit_gejala:
                    if not nama_edit_gejala.strip():
                        st.error("Nama gejala wajib diisi.")
                    else:
                        conn = get_connection()
                        try:
                            conn.execute("""
                                UPDATE gejala
                                SET nama_gejala = ?, deskripsi = ?
                                WHERE kode = ?
                            """, (
                                nama_edit_gejala.strip(),
                                deskripsi_edit_gejala.strip(),
                                kode_edit_gejala
                            ))
                            conn.commit()
                            st.success("Data gejala berhasil diperbarui.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Gagal memperbarui gejala: {e}")
                        finally:
                            conn.close()

            st.divider()
            st.subheader("🗑️ Hapus Gejala")

            kode_hapus_gejala = st.selectbox(
                "Pilih gejala yang akan dihapus",
                [row["kode"] for row in data_gejala_bp],
                key="bp_pilih_hapus_gejala"
            )
            konfirmasi_hapus_gejala = st.checkbox(
                "Saya yakin ingin menghapus gejala ini.",
                key="bp_konfirmasi_hapus_gejala"
            )

            if st.button(
                "Hapus Gejala",
                key="bp_tombol_hapus_gejala",
                use_container_width=True
            ):
                if not konfirmasi_hapus_gejala:
                    st.warning("Centang konfirmasi terlebih dahulu.")
                else:
                    conn = get_connection()
                    try:
                        jumlah_aturan_gejala = conn.execute("""
                            SELECT COUNT(*) FROM aturan
                            WHERE kode_gejala = ?
                        """, (kode_hapus_gejala,)).fetchone()[0]

                        if jumlah_aturan_gejala > 0:
                            st.error(
                                "Gejala tidak dapat dihapus karena masih "
                                "digunakan dalam aturan diagnosis. Hapus "
                                "atau ubah aturan terkait terlebih dahulu."
                            )
                        else:
                            conn.execute(
                                "DELETE FROM gejala WHERE kode = ?",
                                (kode_hapus_gejala,)
                            )
                            conn.commit()
                            st.success("Gejala berhasil dihapus.")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Gagal menghapus gejala: {e}")
                    finally:
                        conn.close()

    # ======================================
    # TAB ATURAN DIAGNOSIS
    # ======================================

    with tab_aturan:

        conn = get_connection()
        data_aturan_bp = conn.execute("""
            SELECT
                a.id,
                a.kode_gejala,
                g.nama_gejala,
                a.kode_kerusakan,
                k.nama_kerusakan,
                a.bobot_cf
            FROM aturan a
            JOIN gejala g ON g.kode = a.kode_gejala
            JOIN kerusakan k ON k.kode = a.kode_kerusakan
            ORDER BY a.kode_kerusakan, a.kode_gejala
        """).fetchall()

        pilihan_gejala_bp = conn.execute("""
            SELECT kode, nama_gejala FROM gejala ORDER BY kode
        """).fetchall()

        pilihan_kerusakan_bp = conn.execute("""
            SELECT kode, nama_kerusakan FROM kerusakan ORDER BY kode
        """).fetchall()
        conn.close()

        st.subheader("Daftar Aturan Diagnosis")
        st.caption(
            "Setiap aturan pada struktur database saat ini menghubungkan "
            "satu gejala dengan satu jenis kerusakan."
        )

        st.metric("Total Aturan", len(data_aturan_bp))

        if data_aturan_bp:
            st.dataframe(
                [
                    {
                        "ID": row["id"],
                        "Kode Gejala": row["kode_gejala"],
                        "Nama Gejala": row["nama_gejala"],
                        "Kode Kerusakan": row["kode_kerusakan"],
                        "Nama Kerusakan": row["nama_kerusakan"],
                        "Bobot CF Pakar": round(float(row["bobot_cf"]), 2)
                    }
                    for row in data_aturan_bp
                ],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Belum ada aturan diagnosis.")

        st.divider()
        st.subheader("➕ Tambah Aturan")

        if not pilihan_gejala_bp or not pilihan_kerusakan_bp:
            st.warning(
                "Tambahkan minimal satu gejala dan satu jenis kerusakan "
                "sebelum membuat aturan."
            )
        else:
            label_gejala = {
                row["kode"]: f'{row["kode"]} - {row["nama_gejala"]}'
                for row in pilihan_gejala_bp
            }
            label_kerusakan = {
                row["kode"]: f'{row["kode"]} - {row["nama_kerusakan"]}'
                for row in pilihan_kerusakan_bp
            }

            with st.form("form_tambah_aturan"):
                kode_gejala_aturan = st.selectbox(
                    "Pilih Gejala",
                    list(label_gejala.keys()),
                    format_func=lambda x: label_gejala[x]
                )
                kode_kerusakan_aturan = st.selectbox(
                    "Pilih Kerusakan",
                    list(label_kerusakan.keys()),
                    format_func=lambda x: label_kerusakan[x]
                )
                bobot_aturan_baru = st.number_input(
                    "Bobot CF Pakar",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.8,
                    step=0.05,
                    format="%.2f",
                    help="Nilai 0 sampai 1. Isi berdasarkan hasil konsultasi/validasi pakar."
                )
                tambah_aturan = st.form_submit_button(
                    "Simpan Aturan", use_container_width=True
                )

                if tambah_aturan:
                    conn = get_connection()
                    try:
                        conn.execute("""
                            INSERT INTO aturan
                                (kode_gejala, kode_kerusakan, bobot_cf)
                            VALUES (?, ?, ?)
                        """, (
                            kode_gejala_aturan,
                            kode_kerusakan_aturan,
                            bobot_aturan_baru
                        ))
                        conn.commit()
                        st.success("Aturan berhasil ditambahkan.")
                        st.rerun()
                    except Exception as e:
                        st.error(
                            "Gagal menambahkan aturan. Pastikan kombinasi "
                            f"gejala dan kerusakan belum terdaftar. Detail: {e}"
                        )
                    finally:
                        conn.close()

        st.divider()
        st.subheader("✏️ Edit Bobot Aturan")

        if data_aturan_bp:
            pilihan_id_aturan = st.selectbox(
                "Pilih aturan",
                [row["id"] for row in data_aturan_bp],
                format_func=lambda x: next(
                    (
                        f'ID {row["id"]}: {row["kode_gejala"]} → '
                        f'{row["kode_kerusakan"]} (CF {row["bobot_cf"]:.2f})'
                        for row in data_aturan_bp if row["id"] == x
                    ),
                    str(x)
                ),
                key="bp_pilih_edit_aturan"
            )
            item_aturan = next(
                row for row in data_aturan_bp
                if row["id"] == pilihan_id_aturan
            )

            with st.form("form_edit_aturan"):
                st.text_input(
                    "Relasi Gejala",
                    value=f'{item_aturan["kode_gejala"]} - '
                          f'{item_aturan["nama_gejala"]}',
                    disabled=True
                )
                st.text_input(
                    "Relasi Kerusakan",
                    value=f'{item_aturan["kode_kerusakan"]} - '
                          f'{item_aturan["nama_kerusakan"]}',
                    disabled=True
                )
                bobot_edit_aturan = st.number_input(
                    "Bobot CF Pakar",
                    min_value=0.0,
                    max_value=1.0,
                    value=float(item_aturan["bobot_cf"]),
                    step=0.05,
                    format="%.2f"
                )
                simpan_edit_aturan = st.form_submit_button(
                    "Simpan Perubahan", use_container_width=True
                )

                if simpan_edit_aturan:
                    conn = get_connection()
                    try:
                        conn.execute("""
                            UPDATE aturan
                            SET bobot_cf = ?
                            WHERE id = ?
                        """, (bobot_edit_aturan, pilihan_id_aturan))
                        conn.commit()
                        st.success("Bobot aturan berhasil diperbarui.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Gagal memperbarui aturan: {e}")
                    finally:
                        conn.close()

            st.divider()
            st.subheader("🗑️ Hapus Aturan")

            pilihan_hapus_aturan = st.selectbox(
                "Pilih aturan yang akan dihapus",
                [row["id"] for row in data_aturan_bp],
                format_func=lambda x: next(
                    (
                        f'ID {row["id"]}: {row["kode_gejala"]} → '
                        f'{row["kode_kerusakan"]}'
                        for row in data_aturan_bp if row["id"] == x
                    ),
                    str(x)
                ),
                key="bp_pilih_hapus_aturan"
            )

            konfirmasi_hapus_aturan = st.checkbox(
                "Saya yakin ingin menghapus aturan ini.",
                key="bp_konfirmasi_hapus_aturan"
            )

            if st.button(
                "Hapus Aturan",
                key="bp_tombol_hapus_aturan",
                use_container_width=True
            ):
                if not konfirmasi_hapus_aturan:
                    st.warning("Centang konfirmasi terlebih dahulu.")
                else:
                    conn = get_connection()
                    try:
                        conn.execute(
                            "DELETE FROM aturan WHERE id = ?",
                            (pilihan_hapus_aturan,)
                        )
                        conn.commit()
                        st.success("Aturan berhasil dihapus.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Gagal menghapus aturan: {e}")
                    finally:
                        conn.close()

        st.info(
            "Catatan: perubahan bobot akan langsung memengaruhi hasil "
            "diagnosis berikutnya. Pastikan bobot ditetapkan berdasarkan "
            "penilaian pakar dan dokumentasikan sumbernya."
        )

    # ======================================
    # TAB PETA ATURAN
    # ======================================

    with tab_relasi:

        conn = get_connection()
        relasi = conn.execute("""
            SELECT
                a.kode_gejala,
                g.nama_gejala,
                a.kode_kerusakan,
                k.nama_kerusakan,
                a.bobot_cf
            FROM aturan a
            JOIN gejala g ON g.kode = a.kode_gejala
            JOIN kerusakan k ON k.kode = a.kode_kerusakan
            ORDER BY a.kode_gejala, a.kode_kerusakan
        """).fetchall()
        conn.close()

        st.subheader("Pemetaan Gejala ke Kerusakan")
        st.caption(
            "Peta ini memperlihatkan hubungan fakta gejala dengan "
            "kesimpulan kerusakan dalam proses Forward Chaining."
        )

        if relasi:
            for row in relasi:
                st.write(
                    f'**{row["kode_gejala"]} – {row["nama_gejala"]}** '
                    f'→ **{row["kode_kerusakan"]} – '
                    f'{row["nama_kerusakan"]}** '
                    f'(CF pakar: {float(row["bobot_cf"]):.2f})'
                )
        else:
            st.info("Belum ada relasi aturan.")


# ==========================================
# MENU DATA KERUSAKAN (CRUD)
# ==========================================

elif menu == "Data Kerusakan":

    st.header("🖥️ Data Kerusakan Hardware")

    st.write(
        "Pengelolaan basis pengetahuan kerusakan hardware."
    )

    conn = get_connection()

    data = conn.execute("""
        SELECT kode, nama_kerusakan, deskripsi, solusi
        FROM kerusakan
        ORDER BY kode
    """).fetchall()

    total_aturan = conn.execute(
        "SELECT COUNT(*) FROM aturan"
    ).fetchone()[0]

    conn.close()

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Jenis Kerusakan", len(data))

    with col2:
        st.metric("Total Aturan", total_aturan)

    st.divider()

    st.subheader("📋 Daftar Kerusakan")

    if data:

        st.dataframe(
            [
                {
                    "Kode": row["kode"],
                    "Nama Kerusakan": row["nama_kerusakan"],
                    "Deskripsi": row["deskripsi"],
                    "Solusi": row["solusi"]
                }
                for row in data
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("Belum ada data kerusakan.")

    st.divider()

    # ======================================
    # TAMBAH DATA
    # ======================================

    st.subheader("➕ Tambah Data Kerusakan")

    with st.form("form_tambah_kerusakan"):

        kode_baru = st.text_input(
            "Kode Kerusakan",
            placeholder="Contoh: P07"
        ).strip().upper()

        nama_baru = st.text_input(
            "Nama Kerusakan"
        )

        deskripsi_baru = st.text_area(
            "Deskripsi Kerusakan"
        )

        solusi_baru = st.text_area(
            "Solusi Perbaikan"
        )

        tambah = st.form_submit_button(
            "Simpan Data",
            use_container_width=True
        )

        if tambah:

            if not all([
                kode_baru,
                nama_baru.strip(),
                deskripsi_baru.strip(),
                solusi_baru.strip()
            ]):

                st.error("Semua kolom wajib diisi.")

            else:

                conn = get_connection()

                try:

                    conn.execute("""
                        INSERT INTO kerusakan (
                            kode,
                            nama_kerusakan,
                            deskripsi,
                            solusi
                        )
                        VALUES (?, ?, ?, ?)
                    """, (
                        kode_baru,
                        nama_baru.strip(),
                        deskripsi_baru.strip(),
                        solusi_baru.strip()
                    ))

                    conn.commit()

                    st.success(
                        "Data kerusakan berhasil ditambahkan."
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Gagal menyimpan data: {e}"
                    )

                finally:
                    conn.close()

    st.divider()

    # ======================================
    # EDIT DATA
    # ======================================

    st.subheader("✏️ Edit Data Kerusakan")

    conn = get_connection()

    data_edit = conn.execute("""
        SELECT kode, nama_kerusakan, deskripsi, solusi
        FROM kerusakan
        ORDER BY kode
    """).fetchall()

    conn.close()

    if data_edit:

        pilihan_edit = st.selectbox(
            "Pilih Kerusakan",
            [row["kode"] for row in data_edit],
            format_func=lambda x: format_kerusakan(
                x, data_edit
            )
        )

        item = next(
            row for row in data_edit
            if row["kode"] == pilihan_edit
        )

        with st.form("form_edit_kerusakan"):

            st.text_input(
                "Kode Kerusakan",
                value=item["kode"],
                disabled=True
            )

            nama_edit = st.text_input(
                "Nama Kerusakan",
                value=item["nama_kerusakan"]
            )

            deskripsi_edit = st.text_area(
                "Deskripsi Kerusakan",
                value=item["deskripsi"] or ""
            )

            solusi_edit = st.text_area(
                "Solusi Perbaikan",
                value=item["solusi"] or ""
            )

            simpan_edit = st.form_submit_button(
                "Simpan Perubahan",
                use_container_width=True
            )

            if simpan_edit:

                if not all([
                    nama_edit.strip(),
                    deskripsi_edit.strip(),
                    solusi_edit.strip()
                ]):

                    st.error("Semua kolom wajib diisi.")

                else:

                    conn = get_connection()

                    conn.execute("""
                        UPDATE kerusakan
                        SET nama_kerusakan = ?,
                            deskripsi = ?,
                            solusi = ?
                        WHERE kode = ?
                    """, (
                        nama_edit.strip(),
                        deskripsi_edit.strip(),
                        solusi_edit.strip(),
                        pilihan_edit
                    ))

                    conn.commit()
                    conn.close()

                    st.success(
                        "Data kerusakan berhasil diperbarui."
                    )

                    st.rerun()

    st.divider()

    # ======================================
    # HAPUS DATA
    # ======================================

    st.subheader("🗑️ Hapus Data Kerusakan")

    if data_edit:

        pilihan_hapus = st.selectbox(
            "Pilih data yang ingin dihapus",
            [row["kode"] for row in data_edit],
            format_func=lambda x: format_kerusakan(
                x, data_edit
            ),
            key="pilihan_hapus"
        )

        konfirmasi = st.checkbox(
            "Saya yakin ingin menghapus data ini."
        )

        if st.button(
            "Hapus Data",
            use_container_width=True
        ):

            if not konfirmasi:

                st.warning(
                    "Centang konfirmasi terlebih dahulu."
                )

            else:

                conn = get_connection()

                try:

                    jumlah_aturan = conn.execute("""
                        SELECT COUNT(*)
                        FROM aturan
                        WHERE kode_kerusakan = ?
                    """, (pilihan_hapus,)).fetchone()[0]

                    jumlah_riwayat = conn.execute("""
                        SELECT COUNT(*)
                        FROM riwayat
                        WHERE kode_kerusakan = ?
                    """, (pilihan_hapus,)).fetchone()[0]

                    jumlah_detail = conn.execute("""
                        SELECT COUNT(*)
                        FROM detail_konsultasi
                        WHERE kode_kerusakan = ?
                    """, (pilihan_hapus,)).fetchone()[0]

                    if jumlah_aturan > 0 or jumlah_riwayat > 0 or jumlah_detail > 0:

                        st.error(
                            "Data tidak dapat dihapus karena masih digunakan "
                            "oleh aturan atau riwayat konsultasi/diagnosis."
                        )

                    else:

                        conn.execute("""
                            DELETE FROM kerusakan
                            WHERE kode = ?
                        """, (pilihan_hapus,))

                        conn.commit()

                        st.success(
                            "Data kerusakan berhasil dihapus."
                        )

                        st.rerun()

                except Exception as e:

                    st.error(f"Gagal menghapus data: {e}")

                finally:
                    conn.close()


# ==========================================
# MENU RIWAYAT DIAGNOSIS
# ==========================================

elif menu == "Riwayat Diagnosis":

    st.header("📚 Riwayat Diagnosis")
    st.write(
        "Daftar sesi konsultasi dan seluruh kemungkinan kerusakan "
        "yang dihasilkan pada setiap sesi."
    )

    conn = get_connection()
    konsultasi_rows = conn.execute("""
        SELECT
            c.id,
            c.nama_pengguna,
            c.tanggal,
            c.gejala_json,
            COUNT(d.id) AS jumlah_hasil,
            MAX(d.hasil_cf) AS cf_tertinggi
        FROM konsultasi c
        LEFT JOIN detail_konsultasi d
            ON d.konsultasi_id = c.id
        GROUP BY c.id, c.nama_pengguna, c.tanggal, c.gejala_json
        ORDER BY c.id DESC
    """).fetchall()

    detail_rows = conn.execute("""
        SELECT
            d.id,
            d.konsultasi_id,
            d.kode_kerusakan,
            k.nama_kerusakan,
            d.hasil_cf,
            d.hasil_json,
            d.legacy_riwayat_id
        FROM detail_konsultasi d
        LEFT JOIN kerusakan k
            ON k.kode = d.kode_kerusakan
        ORDER BY d.hasil_cf DESC, d.id
    """).fetchall()
    conn.close()

    st.metric("Total Konsultasi", len(konsultasi_rows))
    st.caption(
        "Satu konsultasi dapat memiliki lebih dari satu kemungkinan kerusakan."
    )

    if konsultasi_rows:
        st.dataframe(
            [
                {
                    "ID Konsultasi": row["id"],
                    "Nama Pengguna": row["nama_pengguna"],
                    "Tanggal": row["tanggal"],
                    "Jumlah Hasil": row["jumlah_hasil"],
                    "CF Tertinggi": (
                        f"{float(row['cf_tertinggi']):.2f}%"
                        if row["cf_tertinggi"] is not None else "-"
                    )
                }
                for row in konsultasi_rows
            ],
            use_container_width=True,
            hide_index=True
        )

        st.divider()
        st.subheader("Detail Konsultasi")

        pilihan_konsultasi = st.selectbox(
            "Pilih ID Konsultasi",
            [row["id"] for row in konsultasi_rows],
            format_func=lambda x: next(
                (
                    f"ID {row['id']} — {row['nama_pengguna']} "
                    f"({row['tanggal']})"
                    for row in konsultasi_rows if row["id"] == x
                ),
                str(x)
            )
        )

        konsultasi_terpilih = next(
            row for row in konsultasi_rows
            if row["id"] == pilihan_konsultasi
        )

        st.write(f"**Nama Pengguna:** {konsultasi_terpilih['nama_pengguna']}")
        st.write(f"**Tanggal:** {konsultasi_terpilih['tanggal']}")

        try:
            gejala_riwayat = json.loads(
                konsultasi_terpilih["gejala_json"] or "{}"
            )
        except (TypeError, json.JSONDecodeError):
            gejala_riwayat = {}

        st.markdown("**Gejala yang dipilih:**")
        if gejala_riwayat:
            for kode, nilai in gejala_riwayat.items():
                st.write(f"- {kode}: CF pengguna {float(nilai):.2f}")
        else:
            st.write("- Data gejala tidak tersedia.")

        hasil_konsultasi = [
            row for row in detail_rows
            if row["konsultasi_id"] == pilihan_konsultasi
        ]

        st.markdown("**Hasil diagnosis:**")
        if hasil_konsultasi:
            for nomor, detail in enumerate(hasil_konsultasi, start=1):
                st.markdown(
                    f"**{nomor}. {detail['kode_kerusakan']} — "
                    f"{detail['nama_kerusakan'] or 'Nama tidak tersedia'}**"
                )
                st.metric(
                    "Tingkat Keyakinan",
                    f"{float(detail['hasil_cf']):.2f}%"
                )

                try:
                    payload = json.loads(detail["hasil_json"] or "{}")
                except (TypeError, json.JSONDecodeError):
                    payload = {}

                if payload.get("aturan_aktif"):
                    st.markdown("**Rincian aturan dan CF:**")
                    for aturan_item in payload["aturan_aktif"]:
                        st.write(
                            f"- {aturan_item.get('kode_gejala', '-')}: "
                            f"CF pengguna {float(aturan_item.get('cf_pengguna', 0)):.2f}, "
                            f"CF pakar {float(aturan_item.get('cf_pakar', 0)):.2f}, "
                            f"CF evidence {float(aturan_item.get('cf_evidence', 0)):.4f}"
                        )
                elif payload.get("catatan_migrasi"):
                    st.caption(payload["catatan_migrasi"])

                st.divider()
        else:
            st.info("Konsultasi ini belum memiliki detail hasil diagnosis.")

    else:
        st.info("Belum ada riwayat konsultasi.")


# ==========================================
# MENU PENGUJIAN SISTEM (PEMERIKSAAN OTOMATIS)
# ==========================================

elif menu == "Pengujian Sistem":

    st.header("🧪 Pengujian Sistem")
    st.caption("Pemeriksaan otomatis struktur basis data, aturan, bobot CF, dan mesin diagnosis. Pemeriksaan ini tidak mengubah data.")

    hasil_pemeriksaan = []
    conn_uji = get_connection()
    try:
        tabel_wajib = [
            "gejala", "kerusakan", "aturan",
            "konsultasi", "detail_konsultasi", "riwayat"
        ]
        tabel_ada = {
            row["name"] for row in conn_uji.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
        for nama_tabel in tabel_wajib:
            hasil_pemeriksaan.append({
                "Pengujian": f"Tabel {nama_tabel} tersedia",
                "Hasil": "LULUS" if nama_tabel in tabel_ada else "GAGAL",
                "Keterangan": "Tabel ditemukan" if nama_tabel in tabel_ada else "Tabel tidak ditemukan"
            })

        if all(t in tabel_ada for t in ["gejala", "kerusakan", "aturan"]):
            jumlah_gejala = conn_uji.execute("SELECT COUNT(*) FROM gejala").fetchone()[0]
            jumlah_kerusakan = conn_uji.execute("SELECT COUNT(*) FROM kerusakan").fetchone()[0]
            jumlah_aturan = conn_uji.execute("SELECT COUNT(*) FROM aturan").fetchone()[0]

            hasil_pemeriksaan.extend([
                {"Pengujian": "Data gejala tersedia", "Hasil": "LULUS" if jumlah_gejala > 0 else "GAGAL", "Keterangan": f"{jumlah_gejala} data gejala"},
                {"Pengujian": "Data kerusakan tersedia", "Hasil": "LULUS" if jumlah_kerusakan > 0 else "GAGAL", "Keterangan": f"{jumlah_kerusakan} data kerusakan"},
                {"Pengujian": "Aturan diagnosis tersedia", "Hasil": "LULUS" if jumlah_aturan > 0 else "GAGAL", "Keterangan": f"{jumlah_aturan} aturan"},
            ])

            bobot_invalid = conn_uji.execute(
                "SELECT COUNT(*) FROM aturan WHERE bobot_cf < 0 OR bobot_cf > 1 OR bobot_cf IS NULL"
            ).fetchone()[0]
            hasil_pemeriksaan.append({
                "Pengujian": "Rentang bobot CF 0 sampai 1",
                "Hasil": "LULUS" if bobot_invalid == 0 else "GAGAL",
                "Keterangan": f"{bobot_invalid} aturan memiliki bobot tidak valid"
            })

            aturan_orphan = conn_uji.execute("""
                SELECT COUNT(*) FROM aturan a
                LEFT JOIN gejala g ON g.kode = a.kode_gejala
                LEFT JOIN kerusakan k ON k.kode = a.kode_kerusakan
                WHERE g.kode IS NULL OR k.kode IS NULL
            """).fetchone()[0]
            hasil_pemeriksaan.append({
                "Pengujian": "Relasi aturan terhubung ke gejala dan kerusakan",
                "Hasil": "LULUS" if aturan_orphan == 0 else "GAGAL",
                "Keterangan": f"{aturan_orphan} aturan memiliki relasi yang tidak valid"
            })

            gejala_tanpa_aturan = conn_uji.execute("""
                SELECT COUNT(*) FROM gejala g
                LEFT JOIN aturan a ON a.kode_gejala = g.kode
                WHERE a.id IS NULL
            """).fetchone()[0]
            hasil_pemeriksaan.append({
                "Pengujian": "Setiap gejala memiliki minimal satu aturan",
                "Hasil": "LULUS" if gejala_tanpa_aturan == 0 else "PERLU DITINJAU",
                "Keterangan": f"{gejala_tanpa_aturan} gejala belum memiliki aturan"
            })

            try:
                hasil_contoh = proses_diagnosis({"G06": 1.0})
                p03 = next((x for x in hasil_contoh if x["kode"] == "P03"), None)
                aturan_g06_p03 = conn_uji.execute(
                    "SELECT bobot_cf FROM aturan WHERE kode_gejala='G06' AND kode_kerusakan='P03'"
                ).fetchone()
                if aturan_g06_p03 is None:
                    status_contoh, ket_contoh = "PERLU DITINJAU", "Aturan G06 ke P03 tidak ditemukan"
                elif p03 is None:
                    status_contoh, ket_contoh = "GAGAL", "Mesin diagnosis tidak menghasilkan P03 untuk G06"
                else:
                    nilai_harapan = round(float(aturan_g06_p03[0]) * 100, 2)
                    nilai_aktual = round(float(p03["persentase"]), 2)
                    cocok = nilai_harapan == nilai_aktual
                    status_contoh = "LULUS" if cocok else "GAGAL"
                    ket_contoh = f"Hasil {nilai_aktual:.2f}%; nilai hitung yang diharapkan {nilai_harapan:.2f}%"
            except Exception as exc:
                status_contoh, ket_contoh = "GAGAL", f"Kesalahan mesin diagnosis: {exc}"

            hasil_pemeriksaan.append({
                "Pengujian": "Uji diagnosis contoh G06 dengan CF pengguna 1.0",
                "Hasil": status_contoh,
                "Keterangan": ket_contoh
            })

    except Exception as exc:
        st.error(f"Pemeriksaan tidak dapat diselesaikan: {exc}")
    finally:
        conn_uji.close()

    if hasil_pemeriksaan:
        import pandas as pd
        df_uji = pd.DataFrame(hasil_pemeriksaan)
        total_lulus = int((df_uji["Hasil"] == "LULUS").sum())
        total_gagal = int((df_uji["Hasil"] == "GAGAL").sum())
        total_tinjau = int((df_uji["Hasil"] == "PERLU DITINJAU").sum())
        c1, c2, c3 = st.columns(3)
        c1.metric("Lulus", total_lulus)
        c2.metric("Gagal", total_gagal)
        c3.metric("Perlu ditinjau", total_tinjau)
        st.dataframe(df_uji, use_container_width=True, hide_index=True)
        if total_gagal == 0 and total_tinjau == 0:
            st.success("Seluruh pemeriksaan otomatis pada daftar ini lulus.")
        elif total_gagal > 0:
            st.error("Masih ada pemeriksaan yang gagal. Periksa keterangan pada tabel sebelum aplikasi dinyatakan siap.")
        else:
            st.warning("Ada pemeriksaan yang perlu ditinjau secara manual.")

    st.info("Catatan: hasil LULUS hanya membuktikan fungsi dan konsistensi teknis pada pengujian ini. Hasil ini bukan bukti akurasi diagnosis medis/teknisi dan tidak menggantikan validasi bobot aturan oleh pakar.")


# ==========================================
# MENU TENTANG
# ==========================================

elif menu == "Tentang":

    st.header("ℹ️ Tentang Aplikasi")

    st.markdown("""
    ## 💻 Hardware Expert System

    Aplikasi Sistem Pakar Diagnosa Kerusakan
    Perangkat Keras Komputer berbasis Web.

    ### Metode Sistem

    - Forward Chaining
    - Certainty Factor (CF)

    ### Teknologi

    - Python
    - Streamlit
    - SQLite

    ### Informasi Aplikasi

    Nama: Hardware Expert System

    Versi: 1.0

    Platform: Web Application
    """)
