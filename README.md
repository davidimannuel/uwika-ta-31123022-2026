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
