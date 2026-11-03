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
Ringkasan membaca CSV dari `RESULT_GROUP="reward_revisit_10_overlap_count_20261103"`.
Grup ini menguji penalti revisit -10 dengan overlap_ratio per episode. Hasil -5
tersimpan pada reward_revisit_5_overlap_count_20261103 sebagai pembanding.
Muat ulang notebook dari disk, restart kernel, lalu jalankan cell muat graf
agar core, RESULT_GROUP dan MAX_WORKERS diperbarui.
Hasil lengkap sebelumnya reward_direct_20261103 (60 training) tetap arsip.
Lihat [analisis terbaru](docs/temp/analisis_reward_direct_20261103/ANALISIS.md).
Hasil selesai sebelumnya tetap pada surface_width_3m_20261102;
ubah RESULT_GROUP ke arsip hanya untuk membaca hasilnya, bukan menimpa dengan training baru.
Agent hanya memeriksa artefak dan mengulang evaluasi greedy dari Q-table;
training penelitian dijalankan pengguna. Jangan menjalankan cell training hanya
untuk menampilkan ulang hasil: gunakan pasangan cell tampilan hasil tersimpan.

## Menjalankan seed paralel

Setelah restart kernel, jalankan cell muat graf pada notebook A/B/C. Cell tersebut
menetapkan grup hasil -10 dan:

```python
MAX_WORKERS = 3
```

Empat cell training memakai `max_workers=MAX_WORKERS`. Isi 1 untuk mode berurutan;
3 menjalankan tiga seed bersamaan pada proses terpisah. Dapat dinaikkan jika CPU/
RAM memadai, maksimum efektif lima seed dan jumlah CPU. Konfigurasi terbaru 3 worker.
Tidak perlu menambah asyncio atau menginstal paket. Jalankan satu cell konfigurasi
training dulu; cell tetap menunggu semua seed, sambil mencetak seed yang selesai.

Setiap seed tetap melatih Q-table sendiri dari awal dengan RNG-nya sendiri.
Penggabungan CSV tetap urutan seed 0--4. Grafik/peta dibuat induk setelah seluruh
seed selesai. Hasil penelitian lama tetap tersimpan. Uji titik start memakai tiga seed acak dengan MAX_WORKERS=3. Penambahan worker menambah penggunaan RAM dan tidak menjamin
percepatan linear. Menjalankan ulang cell bukan melanjutkan training sebelumnya.

## Aturan reward yang aktif (3 November 2026)

- Highway satu prioritas: footway/pedestrian/living_street/residential/tertiary.
- Surface prioritas: asphalt/concrete/paving_stones/paved. Width prioritas >=3 m.
- H/S/W: prioritas +1, lainnya -1, kosong 0; width invalid/gabungan 0.
  Gabungan highway/surface minimum. Service tetap legal jika lolos access/mask.
- Reward ruas = (0,55*rH+0,30*rS+0,15*rW)*panjang/100. Tidak ada pengurangan 0,50.
- Permissive -0,10/100 m; access yes/kosong boleh dan tidak memberi penalti.
  Nilai access lainnya ditolak. Arah kedua fase 0,60; revisit -10;
  sukses +100; kelebihan jarak/buntu/batas langkah masing-masing -50.
- Nama legacy comfort_score/mean_comfort menyimpan gabungan tanpa clipping,
  bukan persentase. Rentang mengikuti parameter; perubahan HIGHWAY_OTHER_SCORE
  tidak dipotong lagi di -1. Hasil lama tidak dihitung ulang otomatis.
  Hasil -5: B dan C masing-masing empat konfigurasi lengkap; 35/40 evaluasi
  greedy valid. Audit terbaru: docs/temp/analisis_BC_revisit5_lengkap_20261103/ANALISIS.md.
- Grup aktif A--C reward_revisit_10_overlap_count_20261103:60 training selesai,
  25/60 greedy valid; audit docs/temp/analisis_ABC_revisit10_20261103/ANALISIS.md. Audit B/C -5 tersedia
  pada docs/temp/analisis_BC_revisit5_20261103/ANALISIS.md.
  Pembanding -3 reward_revisit_3_overlap_count_20261103 memiliki empat konfigurasi B.
  Perubahan terbaru hanya besar penalti, tanpa mengubah mask atau reward lainnya.
  Hasil overlap berbasis meter pada reward_direct_overlap_20261103 tetap arsip.
  reward_direct_20261103 memakai penalti revisit -1 dan belum mencatat overlap
  per episode. Arsip surface_width_3m_20261102 memakai reward/skala sebelumnya.
  Keduanya tetap dapat dibaca tanpa training.
- [Analisis terbaru](docs/temp/analisis_reward_direct_20261103/ANALISIS.md),
  [analisis arsip](docs/temp/analisis_surface_width_3m_20261102/ANALISIS.md),
  [rencana validasi/katalog](docs/VERIFIKASI_VALIDASI_DAN_KATALOG.md).

## Menguji titik start lain

Buka [uji_titik_start.ipynb](uji_titik_start.ipynb) dengan kernel proyek.

Reward, mask dan metrik memakai core bersama yang dimuat ulang saat training.
Perubahan core tidak menghitung ulang hasil lama; jalankan training untuk memakai
parameter baru. Muat ulang notebook dari disk dan restart kernel bila kode berubah.
Uji ini tiga seed acak berbeda; MAX_WORKERS=3 menjalankannya secara paralel.
Masing-masing melatih Q-table dari kosong; total default450.000 episode.

1. Isi SEARCH_LAT/SEARCH_LON dan jalankan cell unduh. Setiap eksekusi mengunduh
   graf OSM baru tanpa cache, mengganti graf dan membuang hasil training sebelumnya.
2. Jalankan cell peta: Highway default, Surface pilihan radio, marker Access per
   kategori pilihan overlay (tanpa smoothness). Input/START dan garis snap tetap;
   overlay ruas awal legal tersedia. Tooltip/legenda membantu inspeksi seluruh graf.
3. Atur konfigurasi; default B/150k per seed/horizon50k, tiga seed acak yang dicatat.
4. Jalankan training lalu cell hasil untuk metrik, grafik gabungan, dan tiga peta
   berlabel seed. kelompok_rute yang sama berarti urutan edge identik. CSV tambahan
   perbandingan_rute_seed.csv memudahkan membandingkan ketiganya.
5. Untuk mengulang training pada peta sama, langsung ulangi cell training dan hasil.
   Tidak ada unduhan ulang; hanya hasil training yang diganti. Jika konfigurasi
   diubah, jalankan cell konfigurasi dahulu. Jika titik diubah, ulangi dari unduhan.

Satu folder kerja uji_titik_start/terbaru/ selalu dipakai. Graf, metadata unduhan
serta peta marker ada di induk; hasil training ada pada training/. Tidak perlu
RUN_LABEL baru. Tiga seed acak berubah setiap batch kecuali RANDOM_SEEDS diisi tuple tiga angka
berbeda. Mengulang training menimpa seluruh batch lama, bukan menambah seed.
Alur ini terpisah dari snapshot dan eksperimen lima seed A--C. Folder uji lama
tetap arsip dan tidak dipakai sebagai cache. Unduhan OSM bukan validasi lapangan.


Cell unduh memakai pengaturan server bawaan OSMnx, tanpa penggantian URL atau
User-Agent di notebook. Setelah memperbarui notebook dari disk, muat ulang dan
restart kernel, lalu jalankan dari cell import/koordinat. Jika koneksi masih
menolak atau timeout, unduhan belum berhasil; ulangi setelah layanan/koneksi
pulih. Lanjutkan training setelah unduhan dan pratinjau berhasil.

## Notebook verifikasi manual

**Status 3 November 2026:** seluruh 32 cell kode dijalankan ulang setelah
penyesuaian reward langsung dan expected manual. Kelulusan hanya untuk kasus
yang tertulis; bukan jaminan bebas bug atau validasi lapangan.

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

## Overlap selama training

Satu metrik baru overlap_ratio dicatat setiap episode dan pada evaluasi akhir,
disimpan 0–1. Revisit setelah 2.500 m tetap legal; reward tidak berubah.
Tampilan hasil memiliki section **Grafik Training**, **Grafik Diagnosis**, dan
**Overlap Rute**. Grafik overlap terpisah (grafik_overlap_<scenario>.png): satu
panel seluruh episode tanpa pemisahan berhasil/gagal, dalam persen.
Rasio = (jumlah lintasan - jumlah ruas fisik unik) / jumlah lintasan; tanpa bobot
panjang. Data kosong bukan 0%.
Notebook A--C memiliki section 3.3 untuk rata-rata overlap seluruh seed evaluasi akhir.
Uji titik otomatis memakai pencatatan yang sama melalui core bersama.
Arsip tanpa overlap tetap dapat ditampilkan; riwayat overlap lamanya tidak direka.


## Checkpoint sebelum penalti data kosong (3 November 2026)

Baseline sebelum perubahan missing: gabungan reward ruas tanpa clipping,
metadata direct_signed_unclipped_20261103, uji titik tiga seed acak/tiga worker,
peta/JSON/Q-table per seed dan perbandingan urutan ruas. Core aktif sekarang
HIGHWAY_OTHER_SCORE=-1; missing highway/surface/width masih0. Pengguna menguji
nilai highway sendiri, jangan otomatis menetapkan -2 berdasarkan arsip. Hasil
uji terakhir memakai unclipped/highway-2/missing0 pada seed708740203/773171908/
1087794112; ketiganya loop valid. Hasil tersimpan/naskah TA tidak diubah.

Pengguna meminta commit baseline DAHULU, baru perubahan missing H/S/W ke-0,5.
Pada checkpoint ini penalti data kosong BELUM diterapkan. Tujuannya preferensi
terhadap kelengkapan informasi, bukan menyatakan data kosong berarti jalan
berbahaya. Catatan ini melengkapi riwayat sebelumnya tanpa menggantikannya.
