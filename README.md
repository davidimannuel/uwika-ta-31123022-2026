# Development TA Rute Lari

Proyek menggunakan Python 3.13, uv, dan JupyterLab. Gunakan notebook untuk kode dan eksperimen, serta terminal terintegrasi JupyterLab untuk mengelola dependensi.

## Berkas environment

| Berkas | Fungsi | Masuk Git |
|---|---|---|
| `pyproject.toml` | Dependensi langsung dan batas versi Python | Ya |
| `uv.lock` | Versi pasti paket yang dipilih uv | Ya |
| `.python-version` | Versi Python pilihan proyek | Ya |
| `.venv/` | Environment lokal | Tidak |

Konfigurasi saat panduan ini ditulis memakai `.python-version` bernilai `3.13`, sedangkan `requires-python = ">=3.13"` masih mengizinkan versi mayor/minor Python yang lebih baru. Untuk membatasi dukungan hanya pada seri 3.13, ubah batas menjadi `">=3.13,<3.14"`, lalu perbarui lockfile secara sengaja. Pin `3.13` belum mengunci versi patch; catat versi lengkap yang digunakan untuk eksperimen.

Dependensi kode tercatat dalam `project.dependencies`. `jupyterlab` dan `ipykernel` berada dalam grup `dev`, yang dipasang secara default oleh uv. Setup awal sudah tersedia; tidak perlu mengulang `uv init`.

## Memulai sesi

Dari terminal sistem:

```bash
cd /Users/david/widya_kartika/uwika-ta-31123022-2026
uv sync --locked
uv run --locked jupyter lab
```

Tidak perlu mengaktifkan `.venv` secara manual. Pilih kernel **TA Rute Lari (Python 3.13)** di notebook. Jika belum tersedia, jalankan sekali dari terminal proyek:

```bash
uv run --locked python -m ipykernel install --sys-prefix --name ta-rute-lari --display-name "TA Rute Lari (Python 3.13)"
```

Periksa melalui cell notebook:

```python
import sys
from pathlib import Path

print("Python:", sys.version)
print("Executable:", sys.executable)
print("Environment:", sys.prefix)
print("Folder kerja:", Path.cwd())
```

Python harus 3.13.x dan environment menunjuk ke `.venv` proyek. Buka notebook utama dari folder yang memuat `rute_lari_core.py`. Notebook dalam subfolder dapat memerlukan pengaturan path import tersendiri.

Terminal JupyterLab dan kernel notebook memiliki folder kerja masing-masing. Perintah `cd` di terminal tidak mengubah folder kerja notebook.

## Menambah paket dari JupyterLab

1. Simpan notebook dan hasil penting. Selesaikan atau hentikan training yang aktif.
2. Buka **File → New → Terminal** di JupyterLab.
3. Masuk ke folder utama proyek:

```bash
cd /Users/david/widya_kartika/uwika-ta-31123022-2026
```

4. Jalankan salah satu perintah berikut sesuai kebutuhan. Ganti placeholder dengan nama paket yang benar:

```bash
# Paket yang digunakan kode proyek:
uv add nama-paket

# Alat pengembangan:
uv add --dev nama-alat
```

5. Periksa perubahan `pyproject.toml` dan `uv.lock`:

```bash
 git diff -- pyproject.toml uv.lock
```

6. Restart kernel melalui **Kernel → Restart Kernel**, lalu jalankan ulang cell import dan persiapan. Jalankan cell training hanya bila diperlukan.

Restart menghapus variabel di RAM. Bila perubahan menyentuh JupyterLab, ipykernel, atau dependensi server, simpan pekerjaan dan hentikan kernel serta server terlebih dahulu; jalankan perubahan dari terminal sistem, lalu buka kembali JupyterLab.

### Alternatif dari cell sementara

Setelah memastikan folder kerja benar dan uv tersedia:

```python
!uv add nama-paket
```

Hapus cell instalasi setelah digunakan, atau ubah menjadi catatan Markdown. Run All pada notebook eksperimen sebaiknya tidak mengubah dependensi.

Hindari `%pip install`, `!pip install`, dan `uv pip install` untuk mengelola dependensi proyek: ketiganya tidak otomatis mencatat perubahan dalam `pyproject.toml` dan `uv.lock`. Gunakan `uv add`. Lihat [panduan uv dan Jupyter](https://docs.astral.sh/uv/guides/integration/jupyter/).

## Menghapus dan memperbarui paket

Lakukan saat tidak ada training aktif. Nama paket berikut adalah placeholder:

```bash
uv remove nama-paket
uv remove --dev nama-alat
```

Untuk upgrade yang disengaja:

```bash
uv lock --upgrade-package nama-paket
uv sync --locked
```

Tinjau diff lockfile dan uji kode yang terdampak. Dependensi terkait dapat ikut berubah. Hindari upgrade seluruh environment di tengah rangkaian eksperimen yang akan dibandingkan. Lihat [pengelolaan dependensi uv](https://docs.astral.sh/uv/concepts/projects/dependencies/).

## Mengubah kode dan menjalankan notebook

- Simpan fungsi bersama di `rute_lari_core.py`; notebook memanggil modul tersebut.
- Setelah mengubah core, restart kernel dan jalankan ulang import serta persiapan. Memuat ulang modul saja belum tentu mengganti objek environment atau model yang sudah dibuat.
- Simpan hasil sebelum restart; variabel RAM akan hilang.
- Periksa cell sebelum Run All karena notebook scenario memuat training panjang.
- Uji perubahan dengan eksekusi kecil sebelum training penuh.
- Gunakan cell pembacaan hasil tersimpan untuk melihat kembali tabel, grafik, dan peta tanpa training ulang.
- Simpan hasil baru ke folder berbeda bila konfigurasi berubah.
- Catat konfigurasi, seed, snapshot graf, commit kode, versi lengkap Python, dan lockfile yang dipakai untuk hasil yang akan dilaporkan.

## Empat konfigurasi eksperimen A–C

Setiap notebook A/B/C memakai dinamis 75.000/150.000 episode serta horizon epsilon
50.000 pada training 75.000/150.000 episode. Semua konfigurasi menggunakan lima
seed dan dimulai dari Q-table kosong. Training total 50.000/100.000 tidak lagi ada
pada notebook aktif. Evaluasi akhirnya greedy (`epsilon=0`).

Jalankan cell pemuatan graf, lalu pasangan training/tampilan hasil sesuai urutan.
Kedua ringkasan membaca CSV dari `RESULT_GROUP="surface_width_3m_20261102"`.
Grup ini sudah dijalankan pengguna dan diperiksa pada 2 November 2026. Hasil
sebelumnya tetap tersimpan; gunakan nama baru yang sama di A/B/C untuk eksperimen
berikutnya agar tidak menimpa hasil.
Agent hanya memeriksa artefak dan mengulang evaluasi greedy dari Q-table;
training penelitian dijalankan pengguna. Jangan menjalankan cell training hanya
untuk menampilkan ulang hasil: gunakan pasangan cell tampilan hasil tersimpan.

## Aturan skor yang aktif

- Highway: dua prioritas 1,00/0,60; lainnya 0,20; kosong 0,50.
- Surface: asphalt/concrete/paving_stones/paved = 1,00; lainnya 0,20; kosong 0,50.
- Width: >=3 m = 1,00; positif <3 m = 0,20; kosong/invalid/gabungan = 0,50.
- Bobot H/S/W tetap 0,55/0,30/0,15. Permissive mendapat -0,10 per 100 m;
  kategori ACCESS_BLACKLIST dikeluarkan dari action. Ruas <3 m tidak dilarang.
- Ketiga komponen skor analisis memakai fungsi core bersama. Peta atribut memiliki
  radio Highway/Surface/Smoothness dan overlay marker access; Highway default.
- Laporan terbaru: [Analisis hasil](docs/temp/analisis_surface_width_3m_20261102/ANALISIS.md).
  Rencana lanjutan: [Verifikasi, validasi, dan katalog](docs/VERIFIKASI_VALIDASI_DAN_KATALOG.md).

## Notebook verifikasi manual

**Status 2 November 2026:** penjelasan berikut merekam notebook yang tersedia,
tetapi acuan angka/assertion masih aturan lama. Jangan menganggap output lama
sebagai verifikasi konfigurasi terbaru. Tinjauan ulang ditunda sampai diminta;
perlu menyesuaikan highway/surface/width, akses dan blacklist terlebih dahulu.

Buka `verifikasi.ipynb` dari root proyek dengan kernel **TA Rute Lari (Python 3.13)**.
Notebook membuat graf sintetis `nx.MultiDiGraph` dengan highway/surface/width,
menghitung skor melalui `core.add_comfort_scores(G)`, membentuk action lewat
`core.build_actions(G)`, lalu menjalankan satu `train_step()` per cell.
Cell berikutnya menampilkan graf melalui fungsi gambar bawaan NetworkX, termasuk
ruas paralel, panah arah, dan label key/panjang/skor.
Fungsi yang sama dipakai `train_q_learning()`; `verbose=True` mencetak state, action,
komponen H/S/W, formula skor, reward ruas/arah/revisit/terminasi/buntu, total reward,
serta persamaan Q dengan angka dan hasilnya. Komponen dicatat saat perhitungan asli
dijalankan di core. `env.latest_state` membaca state terbaru.

Contoh memuat dua episode, masing-masing tiga langkah. Epsilon dihitung melalui
`epsilon_for_episode()` pada awal episode: 1,00 lalu 0,05. Saat reset episode,
Q-table dan generator acak diteruskan. Cell pembuatan environment memulai ulang semuanya.
Input Q awal dapat diisi langsung pada `q_table`; action tertentu dapat dipaksa lewat
parameter `action`, sehingga pemilihan action tersebut tidak dipengaruhi epsilon.

Bagian berikutnya memakai snapshot OSM lokal untuk tiga langkah awal satu episode,
dengan Q-table/RNG sendiri dan satu contoh hitungan manual Q. GraphML wajib
tersedia; jika belum ada, notebook berhenti sebelum loader agar tidak mengunduh.

Bagian lanjutan menguji poin 2–5: state/action mask, integritas graf dan jarak,
terminasi, serta skor/komponen reward. Acuan ditulis pada cell agar bisa diperiksa
manual; assertion menghentikan eksekusi jika hasil tidak cocok. Setelah acuan
angka disesuaikan, gunakan **Restart Kernel and Run All** untuk mengeksekusi
seluruh bagian secara berurutan.

Analisis reward terpisah menyertakan stres edge sintetis 100 km yang melampaui rentang
data penelitian. Counterexample tersebut membatasi klaim reward global, bukan hasil
rute nyata atau perubahan aturan. Tidak ada helper, class tambahan, unduhan, atau
ekspor otomatis. Bukti tersimpan pada output notebook; verifikasi bukan validasi lapangan.

## Menyimpan pekerjaan ke Git

Simpan notebook, lalu periksa dari terminal proyek:

```bash
git status --short
git diff --stat
git diff -- pyproject.toml uv.lock .python-version
```

Stage berkas yang telah diperiksa. Contoh perubahan panduan dan environment:

```bash
git add README.md pyproject.toml uv.lock .python-version
git diff --cached --stat
git commit -m "Document uv and JupyterLab workflow"
```

Tambahkan kode dan notebook yang diubah secara eksplisit bila termasuk dalam pekerjaan yang sama. `.venv/`, `__pycache__/`, dan `.ipynb_checkpoints/` sudah diabaikan `.gitignore`.

Folder `data_osm_5km/`, `hasil_bab_4/`, dan `docs/temp/` juga diabaikan oleh konfigurasi Git saat ini. Cadangkan snapshot graf dan hasil penting secara terpisah. Commit kode tidak mencadangkan berkas yang diabaikan; lockfile tidak menyimpan data OSM atau hasil training.

## Pemulihan masalah

| Masalah | Tindakan |
|---|---|
| `ModuleNotFoundError` | Periksa kernel dan `sys.executable` sebelum menambah paket. |
| Perubahan core belum terlihat | Simpan hasil, restart kernel, dan buat ulang objek. |
| uv tidak ditemukan | Gunakan terminal sistem tempat uv tersedia. |
| Paket terpasang melalui pip | Simpan pekerjaan dan hentikan kernel/server; deklarasikan paket yang diperlukan dengan `uv add`, lalu jalankan `uv sync --locked`. |
| Lockfile tidak sesuai | Periksa diff; bila perubahan deklarasi disengaja, jalankan `uv lock`, tinjau hasil, lalu `uv sync --locked`. |
| Snapshot graf hilang | Pulihkan cadangan; unduhan baru dapat menghasilkan graf berbeda. |

`uv sync --locked` menyelaraskan environment dengan lockfile dan menghapus paket tambahan yang tidak dideklarasikan, tanpa memperbarui lockfile. Jangan menyunting `uv.lock` secara manual. Lihat [locking dan syncing uv](https://docs.astral.sh/uv/concepts/projects/sync/).

## Rutinitas singkat

- Mulai: sync → buka JupyterLab → pilih kernel → periksa environment.
- Development: edit → simpan → restart bila diperlukan → uji kecil.
- Dependensi: terminal JupyterLab → uv add/remove → periksa diff → restart kernel.
- Selesai: simpan notebook dan hasil → periksa Git → commit → cadangkan data eksperimen.
