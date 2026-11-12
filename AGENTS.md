# Konteks Agent Proyek TA Rute Lari

## Kandidat validasi lapangan — 12 November 2026

Pengguna menetapkan tiga rute dari tiga titik awal berbeda, seluruhnya memakai
B horizon100k-total300k. Katalog Go lokal: depan-gang-sebelah-toko9
(seed13916397716709765191,5151,87m), depan-indomaret-dkb
(seed16261264761017114444,5298,84m), depan-wk
(seed9988407548480542851,5527,50m). Ketiganya masih field_validation=not_recorded;
ini kandidat untuk diperiksa, bukan hasil validasi atau pengganti60run eksperimen.
Catat rekaman lintasan/loop, jarak GPS vs graf, akses/hambatan dan penyimpangan;
temuan gagal tetap dilaporkan. Hasil terbatas pada tiga rute/kondisi pemeriksaan.
Config testing kini hanya B horizon100k-total300k dengan lima seed acak. Katalog
menyimpan config/metadata sumber sehingga tidak berubah saat testing titik lain.
Katalog lokal tiga rute belum berarti versi publik sudah diperbarui; perlu push
serta deployment. Checkpoint Go:3af6b27; tes/vet/build dan integritas tiga rute
lulus. Naskah/DOCX utama dan revisi bab sesi lain tidak diubah.

## Ekspor HTML langsung — 12 November 2026

`cli export --workdir ... [--profile ...]` kini memperbarui HTML asli, bukan
membuat output/site. Tanpa profile: analisis dan seluruh profil tersimpan;
dengan profile: hanya peta/report profil terpilih. CSV/Q/metadata/config tetap,
tanpa training/unduhan. Navigasi memakai indeks CLI serve; advanced Q di lokasi
hasil yang sama. Manifest pembaruan output/export.json schema2. Site lama
terverifikasi dibersihkan; file tambahan/symlink/manifest tidak cocok ditolak.
web-catalog dan deployment terpisah. Rincian command pada README Go.

## Katalog publik aktif — 12 November 2026

[Katalog rute lari](https://davidimannuel.github.io/go-running-route-q-learning/) sudah dapat dibuka; indeks publik
menampilkan satu rute, depan-gang-sebelah-toko9, dari hasil training tersimpan.
Source Pages=GitHub Actions; push perubahan web-catalog pada main memicu deploy.
Command add/rm/clear hanya lokal sampai perubahan di-commit/push. field_validation
tetap not_recorded; bukan bukti validasi lapangan atau hasil eksperimen baru.
Catatan belum deploy/katalog kosong di bawah adalah riwayat sebelum publikasi.

## Riwayat checkpoint CLI dan katalog Go — 12 November 2026

Command run, catalog add/rm/clear dan panel peta responsif sudah diimplementasikan.
Setelah reset, pengguna menambahkan kembali satu rute lokal:
`depan-gang-sebelah-toko9`, seed12226258565145578727, profil
b-horizon-100000-total-300000, jarak tersimpan5337,56m. Angka ini contoh katalog,
bukan pengganti hasil eksperimen60run. field_validation=not_recorded.
Katalog saat checkpoint sudah berisi satu rute, menggantikan status kosong di
catatan reset. Checkpoint tercatat pada Go ee2ddb9 dan dokumentasi6768c16;
pengguna kemudian push dan berhasil deployment pada URL publik di atas.
Go test/race CLI/vet/build lulus. Perubahan parameter testing dan output notebook
pengguna dipisahkan; revisi bab/aset/DOCX sesi lain tidak masuk checkpoint ini.

## Command gabungan Go — 12 November 2026

`cli run --workdir ... [--profile ...] [--force] [--debug]` menyiapkan snapshot
sesuai query config, lalu analyze dan train berurutan. Cache tetap dipakai kecuali
force; config/profil diperiksa sebelum download. Gagal/batal menghentikan tahap
berikutnya, hasil tahap sebelumnya tetap tersimpan. Tidak menjalankan notebook,
export atau catalog. Implementasi diuji dengan fixture, tanpa unduh/training
penelitian atau perubahan parameter/hasil/DOCX. Command lengkap di README Go.

Panel HTML rute/analisis sudah mendukung Minimize/Show details; HP/landscape
pendek mulai ringkas, isi dapat digulir maksimal55dvh. Pilihan seed/KM/layer
tetap tersimpan. Menu layer rute ringkas dan zoom di kiri bawah pada layar kecil.
Diuji browser320/390portrait,844landscape,1280desktop; Go test/vet/build lulus.
Hanya template diperbarui; HTML hasil lama belum diregenerasi, tanpa training.
Pratinjau awal terpisah di /tmp. Pengguna kemudian menambahkan satu rute
katalog dan memublikasikannya; indeks publik telah diperiksa12November.

## Katalog Go — 12 November 2026

`cli catalog rm [--dir web-catalog] [--debug] <id>` menghapus SATU rute pilihan
dan memperbarui indeks/manifest; flag sebelum ID. Rute lain/hasil training tetap.
Tanpa prompt tambahan; ID tidak ditemukan gagal tanpa perubahan. Lock/staging
sama dengan add/clear. Tes fixture meliputi rute lain tetap, sumber utuh, rute
terakhir, input invalid, pembatalan dan lock. Tidak menjalankan rm pada rute nyata.

`cli catalog clear [--dir web-catalog] [--debug]` sudah tersedia dan dijalankan
atas permintaan pengguna; saat reset katalog dikosongkan sebelum diisi kembali.
Membuat ulang
index/catalog.json/.nojekyll/routes walau berkas terhapus sebagian. Semua pilihan
katalog dihapus tanpa prompt tambahan; download/analisis/training tetap. Lock
bersama add, staging sebelum penggantian, tolak symlink/file di luar struktur
katalog. Jangan hapus isi katalog manual. Reset bersifat lokal; status publik
terbaru ada di bagian atas, bukan status kosong pada riwayat reset.

`cli catalog add --workdir ... --profile ... --seed ...` sudah diimplementasikan;
prompt hanya ID dan deskripsi. Memakai hasil/metadata tersimpan, satu seed loop
valid, tanpa training/unduhan/config katalog khusus. `web-catalog/` selalu mode
standard lengkap tanpa Q-values, menambah rute tanpa menimpa ID lama. Workflow
GitHub Pages sudah dipublikasikan pada URL di atas. Saat implementasi awal katalog kosong;
pengguna kemudian menambahkan satu rute lokal. Contoh awal memakai fixture
sintetis di /tmp. Pengguna memilih seed sendiri.
Alur katalog: ubah koordinat config → cli run → periksa hasil/pilih seed →
catalog add → periksa katalog → commit/push untuk publikasi. Catalog add hanya
membuat HTML/detail/metadata dari hasil tersimpan, tanpa download/analyze/train
ulang dan tanpa perlu cli export dahulu. Tambahkan seed sebelum hasil sumber
ditimpa percobaan berikutnya. Config/hasil ilmiah/DOCX tidak berubah; rincian
command ada pada README Go.

Pembaruan presentasi Go 11 November: `export.map_mode` standard untuk testing,
advanced untuk training (default advanced). Command `cli export --workdir ...`
awalnya membuat `output/site/`; sejak 12 November memperbarui HTML asli dari
HTML/metadata tersimpan, tanpa training atau perubahan data penelitian. Standard menyertakan fitur/graf lengkap tanpa inspeksi
Q-values; advanced Q memakai hasil asli dan server lokal. Navigasi seed memiliki
tombol kiri/kanan, nilai uint64 utuh dan sumber seed dari metadata. Pengguna akan
generate sendiri saat pembaruan11November. Status deployment kini aktif,
sedangkan alur output/site lama diganti oleh pembaruan HTML langsung. Detail
dan command ada pada README Go/IMPLEMENTASI; angka penelitian tetap.

## Acuan aktif: Go — sinkronisasi 9 November 2026, batch 22.18 WIB

Kode aktif berada di `/Users/david/development/go-running-route-q-learning`.
Repositori ini untuk naskah, aset dan dokumentasi; Python di bawah adalah riwayat.
Baca AGENTS/README Go sebelum perubahan. Sinkronkan Markdown yang sudah ada,
tanpa dokumen tambahan. Naskah Word utama hanya diedit pengguna.

Config terkini: loop 5.000 m dengan toleransi 20% (4.000–6.000 m), graf mentah dua
arah/Haversine, 25 bin pada 0–6.000 m, 500 langkah, alpha 0,15/gamma 0,95, seed 0–4,
150k/300k episode dan epsilon dinamis/horizon 100k. Outward 0, return 1,20,
revisit −10; highway priority +1/secondary +0,5/other −10/missing −2, bobot H/S/W
0,55/0,30/0,15. Access kosong/yes/permissive diperiksa pada way dan kedua
endpoint; barrier saja tidak melarang. Start training 311432306, input
−7.281518/112.710178. Jangan mengubah pilihan start/parameter pengguna otomatis.

Penalti baru `distance_error_penalty_per_100m=-5`: koefisien dikali
`abs(jarak_akhir - 5000)/100`, sekali pada seluruh terminasi; nonterminal 0.
Over_distance dan mask closing tetap. Nol/omitted menonaktifkan komponen.
Batch 22.18 WIB sudah memakai penalti ini: **22/60 valid (A 2 B 15 C 5)**,
18 loop berada di 4.500–5.500 m. B horizon 300k 5/5, galat 161,29 m pada 5 loop.
Checkpoint 21.50 tanpa penalti:23/60 dan 13 loop pada rentang tersebut. Hasil
campuran, belum bukti perbaikan menyeluruh atau konfigurasi final disepakati.
Hasil 31/60 tanggal 7 November dan aturan Python 10% adalah checkpoint historis.

Rincian, batas interpretasi dan sumber ada pada bagian Go `IMPLEMENTASI.md`
dan status atas `LOG_KEMAJUAN.md`. Artefak analisis masih lama: analysis.json
9 November 16.58, ringkasan notebook 21.03 (B/C saja), audit 7 November. Perbarui
dari hasil tersimpan sebelum dipakai untuk Bab IV; jangan otomatis training ulang.
Fokus berikutnya penyelarasan Bab I–IV; verifikasi/validasi ditunda sesuai permintaan.
Skor preferensi dan keberhasilan graf tidak membuktikan kelayakan lapangan.
Aturan praktik kerja/naskah di bawah tetap berlaku; desain/hasil Python adalah arsip.

## Tujuan penelitian

Membangun dan mengevaluasi Q-Learning tabular untuk membentuk **rute lari loop 5 km** berbasis graf jalan OpenStreetMap di Dukuh Kupang, Surabaya.

Rute hanya valid bila:

1. kembali ke node start; dan
2. total jarak berada pada 4.000–6.000 meter untuk konfigurasi Go aktif (toleransi 20%; arsip sebelumnya 10%).

Keberhasilan tersebut direpresentasikan oleh `is_loop=True`. Nama legacy comfort_score kini menyimpan gabungan reward dasar highway/surface/width tanpa pembatasan rentang. Ini preferensi penelitian, bukan persepsi pelari, keamanan aktual atau hasil survei.

## Berkas repositori naskah dan riwayat Python

| Berkas | Peran |
|---|---|
| `rute_lari_core.py` | Core Python historis; core aktif berada di proyek Go. |
| `analisa.ipynb` | Analisis snapshot OSM dan graf. |
| `scenario_A.ipynb` | Eksperimen state A. |
| `scenario_B.ipynb` | Eksperimen state B. |
| `scenario_C.ipynb` | Eksperimen state C. |
| `verifikasi.ipynb` | Verifikasi poin 1–5: Q, state/mask, graf, terminasi, dan reward. |
| `uji_titik_start.ipynb` | Unduh graf OSM di sekitar lat/long pilihan, pratinjau start, tiga seed acak dan hasil per seed. |
| `IMPLEMENTASI.md` | Wiki implementasi dan keputusan teknis lengkap. |
| `LOG_KEMAJUAN.md` | Handover hasil dan pekerjaan terakhir. |
| `referensi.md` | Daftar sumber, format sitasi, tautan, dan pemakaian referensi pada naskah TA. |
| `docs/PANDUAN-TA-SKRIPSI-LENGKAP.pdf` | Panduan penulisan TA/skripsi; rujukan sistematika dan ketentuan penulisan naskah. |
| `docs/` | Kode PlantUML dan panduan aset visual untuk naskah TA. |
| `hasil_bab_4/training_qlearning_5km/` | CSV, grafik, peta, dan artefak eksperimen. |

`training.ipynb` adalah versi lama; jangan dipakai untuk eksperimen baru.

## Riwayat desain Python (hingga 4 November 2026)

- Graf: OSMnx `MultiDiGraph` terarah, terproyeksi meter (`EPSG:32749`).
- Target: 5.000 m, toleransi 10%, area unduh bbox 3.025 m.
- Action Q-Learning: edge spesifik `(next_node, key)`. Edge paralel dengan `u` dan `v` sama tetapi `key` berbeda adalah action berbeda.
- Revisit diperiksa berdasarkan node tujuan, bukan edge. Revisit diizinkan mulai 50% target dan maksimum dua kunjungan node.
- State yang dibandingkan:
  - A: `(current_node,)`
  - B: `(current_node, progress_bin)`
  - C: `(current_node, previous_node, progress_bin)`
- Scenario D telah dihapus dan tidak boleh dihidupkan kembali tanpa persetujuan pengguna.
- Reward dasar H/S/W aktif per 3 November: prioritas +1, lainnya/tidak dikenal -1,
  kosong -0,5; width invalid/gabungan -0,5. Tidak ada pengurangan titik netral 0,50.
- HIGHWAY_PRIORITY satu kelompok: footway, pedestrian, living_street, residential,
  tertiary. Service/path/unclassified/tertiary_link di luar prioritas, bukan dilarang.
- SURFACE_PRIORITY: asphalt/concrete/paving_stones/paved. Width valid >=3 m +1,
  positif <3 m -1. Ini preferensi, bukan standar kenyamanan/keamanan.
- Gabungan highway/surface minimum; seluruh fungsi pemetaan ada di core.
  Bobot highway/surface/width tetap 0,55/0,30/0,15. Reward ruas = gabungan*L/100.
- Nama atribut/method legacy comfort_score, *_score, add_comfort_scores dan
  mean_comfort dipertahankan. Gabungan tidak di-clip; rentang mengikuti parameter.
  Jangan mencampur skor baru dengan angka 0--1 arsip.
- ACCESS_WHITELIST={yes,permissive}; kosong boleh. Semua nilai gabungan harus
  masuk whitelist, foot=yes tidak override. Permissive -0,10 per 100 m;
  yes/kosong 0. Pemetaan reward tidak mengubah legalitas service atau mask.
- `progress_bin` memakai 16 bin pada rentang 0--5.500 m.
- Evaluasi final setiap seed adalah greedy, yaitu `epsilon=0`. Epsilon minimum 0,05 hanya berlaku selama training.

## Reward aktif 3 November 2026

- Seluruh rancangan yang disepakati SUDAH diterapkan ke core dan notebook rute:
  H/S/W default +1/-1/-0,5, satu prioritas highway, bobot lama, akses -0,10, arah 0,60
  kedua fase, revisit -10, sukses +100 dan seluruh kegagalan -50.
- Fase, mask, state, epsilon, seed dan rumus Q tetap. Arah tidak ditambah pada
  terminal langsung; buntu ditambahkan sekali. Closing ke start bebas penalti revisit.
- Metadata baru reward_scheme=direct_signed_unclipped_missing_05_20261103,
  formula/bobot/rentang skor,
  pemetaan atribut, arah/revisit/terminal/akses. Arsip metadata lama tidak diubah.
- Hasil selesai A--C reward_direct_20261103: 60 training/60 evaluasi direproduksi.
  Hasil reward_revisit_10_overlap_count_20261103 lengkap A--C: 60 training,
  25/60 greedy valid; penalti -10, overlap_ratio per episode. Grup reward_direct_overlap_count_20261103
  adalah pembanding -1; empat konfigurasi/lima seed tetap.
- Analisis 21 cell kode dan verifikasi 32 cell kode telah dijalankan ulang pada
  kernel bersih/snapshot lokal. Histogram/peta mencakup -1..1; hitungan manual
  serta expected verifikasi diubah independen, termasuk akses dan next Q nonnol.
- Uji titik memuat ulang core dan skor G sebelum training tanpa unduh/load graf
  ulang. Overwrite satu folder terbaru tetap. Koordinat pengguna dipertahankan.
- basic_q_learning dan eksperimen RNG adalah contoh umum terpisah; tidak memiliki
  reward rute lari sehingga reward toy-nya tidak dipaksa mengikuti atribut OSM.
- Verifikasi lulus kasus yang ditulis, bukan jaminan bebas bug atau validasi lapangan.
  Training panjang, GPX dan katalog belum dikerjakan oleh agent.

## Uji titik awal lain

- Koreksi terbaru 2 November: uji titik adalah percobaan yang selalu ditimpa.
  Tidak ada POINT_NAME/RUN_LABEL/DOWNLOAD_NEW_GRAPH atau mode cache pada notebook.
- Cell unduh selalu force_download=True/use_cache=False di sekitar input, bbox
  default 3.025 m. Graf/metadata mengganti uji_titik_start/terbaru/. Setelah berhasil,
  folder training/ lama dibuang; cell peta membuat marker/HTML terbaru.
- Cell training saja memakai G yang sudah dimuat, tanpa unduh/load graf ulang.
  Hanya subfolder uji_titik_start/terbaru/training/ dibersihkan dan ditulis ulang,
  termasuk Q-table seed lama. Graf/metadata graf/peta marker tetap.
- Perubahan koordinat/radius wajib diikuti cell unduh dan peta. Konteks lama
  dibatalkan saat unduhan dimulai; training/hasil menolak titik atau konfigurasi
  yang belum diperbarui. Hasil dianggap selesai setelah semua artefak tersimpan.
- Tiga training per percobaan. RANDOM_SEEDS=None memilih tiga seed acak berbeda
  saat training; semuanya dicetak/disimpan. Tuple tiga angka untuk pengulangan.
- Default B/150k per seed/horizon 50k/MAX_WORKERS=3; C/75k/dinamis alternatif.
  Tidak mengubah SEEDS global. A--C tetap lima seed dan snapshot utama.
- Peta uji titik 3 November memakai radio Highway (default)/Surface dan overlay
  marker Access per kategori, tanpa smoothness. Legenda dinamis; marker di tengah
  geometri meter, dua arah identik digabung tetapi key paralel tetap terpisah.
  Tooltip memuat atribut/reward dasar; seluruh graf ditampilkan untuk inspeksi
  termasuk access yang tidak lolos whitelist. Overlay ruas awal legal default mati.
- Marker input biru, START hijau, garis snap dan ruas awal legal; snap >100 m
  default/tanpa action awal mencegah training. Metadata mencatat lokasi/graf/core/
  unduhan/seed. Rute gagal tetap dilaporkan, bukan dimasukkan katalog otomatis.
- Folder lama bernama titik/run tetap arsip, tidak dimuat oleh alur terbaru.
  Graf/core/notebook A--C tidak diubah pada revisi perilaku overwrite ini.
- Unduhan live sebelumnya pada koordinat pengguna berhasil: 8.284 node dan
  22.136 edge. Ini riwayat unduhan, bukan hasil baru atau validasi lapangan.
  Pemeriksaan ulang alur dilakukan terkontrol; training panjang dijalankan pengguna.

## Aturan eksperimen

1. Pada arsip Python, environment dan Q-Learning bersama berada di `rute_lari_core.py`. Pengembangan aktif memakai package Go; jangan mengubah Python untuk menyesuaikan eksperimen Go.
2. Jangan mengubah reward, action mask, state, dan hyperparameter sekaligus bila hasil akan dibandingkan. Ubah satu faktor per eksperimen.
3. Perbandingan A--C yang final wajib memakai jumlah episode, seed, graf, reward, dan action mask yang sama.
4. Default `EPISODES=10_000` hanya untuk uji cepat. Notebook A--C memakai empat konfigurasi: dinamis 75k/150k serta horizon epsilon 50k pada training 75k/150k. Tidak ada training total 50k atau 100k pada notebook aktif. Notebook aktif kini memakai `RESULT_GROUP="reward_missing_05_20261103"`;
   grup sebelumnya `reward_revisit_10_overlap_count_20261103` yang sama pada A/B/C (A--C lengkap 25/60 greedy valid; pembanding -5 B/C lengkap 35/40 valid tetap arsip); reward_direct_20261103 adalah arsip selesai; `surface_width_3m_20261102` adalah arsip selesai; grup `konfigurasi_empat_20261029` menyimpan hasil baseline lama.
5. Khusus eksperimen pembanding A--C, setiap jumlah episode melatih ulang lima seed `(0,1,2,3,4)` dari awal. Hasil 150k bukan kelanjutan Q-table hasil 75k.
6. Jangan mengklaim sistem stabil atau siap digunakan hanya dari satu loop valid atau lima seed. Laporkan keterbatasan secara eksplisit.
7. Jangan memasukkan metode atau rencana yang belum diimplementasikan ke dokumentasi TA.

## Metrik yang dipakai

Metrik utama per evaluasi greedy: `is_loop`, `total_distance_m`, `absolute_distance_error_m`, `total_reward`, `mean_comfort`, `overlap_ratio`, `return_progress_ratio`, `distance_to_start_at_end_m`, `closing_action_available`, dan `termination_reason`.

Interpretasi penting:

- `closing_action_available=True` berarti selama episode tersedia edge legal langsung ke start pada jarak total valid. Ini adalah kesempatan menutup loop, bukan jaminan agen memilihnya.
- `return_progress_ratio` mengukur proporsi langkah setelah 2.500 m yang mengurangi jarak lurus ke start.
- Reward training tidak wajib naik; baca bersama keberhasilan loop, jarak, closing action, dan termination rate.
- mean_comfort kini rata-rata berbobot panjang skor preferensi tanpa pembatasan rentang; tinggi berarti banyak kontribusi positif menurut aturan. Ini bukan persentase kenyamanan.

## Status eksperimen terakhir

Penalti aktif -10 pada reward_revisit_10_overlap_count_20261103; A--C lengkap,
60 training/6.750.000 episode dan25/60 greedy valid. Seluruh60 direproduksi.
Grup -5 tetap arsip: B/C lengkap 35/40 greedy valid; grup -3 juga dipertahankan.
A--C memakai MAX_WORKERS=3 di cell muat graf; core default max_workers=1 dan
uji titik kini tiga seed acak dengan MAX_WORKERS=3. Paralel memakai multiprocessing spawn,
Q/environment/RNG per seed mandiri, hasil akhir urutan seed masukan. Worker tidak
menulis artefak; induk menyimpan tiap seed selesai. Jangan paralelkan langkah
atau berbagi Q-table antar-seed. Parameter induk disalin ke worker. Verifikasi
32 cell lulus (-10, total contoh -8,40); Jupyter 3 worker/lima seed diuji, uji sintetis/OSM/Jupyter menunjukkan
kesamaan persis mode berurutan/paralel pada kasus yang diuji. Ini bukan benchmark
training penuh atau jaminan percepatan linear. Rincian IMPLEMENTASI bagian 2.2.

Riwayat sebelum eksperimen -5:
Seluruh empat konfigurasi B pada grup count sudah diamati; ringkasan ada pada
bagian terakhir dokumen. A/C count belum tersedia saat audit ini. Angka seluruh A--C berikut tetap baseline lengkap sebelumnya.


Pengguna menyelesaikan reward_direct_20261103: 12 folder/60 training dan
6.750.000 episode. Greedy A/B/C dari lima seed: dinamis 75K=0/5/5,
dinamis 150K=0/5/5, horizon 50K total 75K=2/5/5, total 150K=1/5/5.
B/C masing-masing 20/20 valid; ini berlaku pada snapshot/start/seed teruji.

B horizon 50K total 150K memiliki galat rata-rata terkecil dan skor ruas tertinggi
di antara konfigurasi B/C: 289,82 m/0,9356/Q-state 15.779,0; C pada konfigurasi
sama 321,18 m/0,9255/37.710,2. B horizon total 75K sudah 5/5, dengan
321,74 m/0,9285/15.106,8 Q-state. Horizon lebih kecil galatnya untuk B,
sedangkan dinamis lebih kecil untuk C pada kedua durasi. Jangan menyebut horizon
syarat mutlak keberhasilan B atau tambahan previous_node selalu lebih baik.

Ada 43 loop valid, hanya 33 urutan edge unik. Seluruhnya 4.509,00--4.915,66 m,
di bawah 5.000 m tetapi sah toleransi. Reward tidak memiliki komponen khusus
untuk memperkecil galat absolut ke 5.000 m. Semua loop masih permissive,
width <3 m/unknown dan revisit; 30 menggunakan ruas nonprioritas/negatif.
Ini legal desain. Gagal 17 seluruhnya A: 12 over_distance dan 5 buntu, semuanya
tidak pernah memiliki closing action legal. A bukan selalu gagal.

Keberhasilan 10K episode training terakhir B/C: dinamis 75K 66,19%/54,35%;
dinamis 150K 81,55%/76,06%; horizon total 75K 84,83%/79,63%; horizon total
150K 87,11%/80,73%. Training bereksplorasi, evaluasi akhir greedy epsilon=0.
Perbedaan rate bukan bukti konvergensi umum atau efek state saja.

Seluruh metadata/history/epsilon diperiksa; 60 evaluasi direproduksi dari
Q-table, metrik serta node/action cocok. Core/GraphML dan 228 berkas input tetap.
Agent tidak menjalankan training baru/unduhan atau mengubah kode/notebook/mask.
Kandidat katalog B horizon total 150K; total 75K layak bila jumlah episode
menjadi pertimbangan. B seed 0 pada keduanya identik: 4.915,66 m, galat 84,34 m,
skor 0,9644 dan 14 revisit. Pemeriksaan peta/akses dan validasi lapangan tetap perlu.
Laporan/CSV/grafik: docs/temp/analisis_reward_direct_20261103/.
Skor/reward arsip lama tidak dibandingkan langsung; banyak komponen berubah.

Angka 2 November berikut adalah arsip reward lama, bukan hasil aktif.

- Per 2 November 2026 pengguna menyelesaikan seluruh empat konfigurasi
  A--C pada grup `surface_width_3m_20261102`: 60 training, 6.750.000 episode.
- Keberhasilan greedy A/B/C dari lima seed: dinamis 75k = 0/0/5;
  dinamis 150k = 0/0/5; horizon 50k total 75k = 1/1/5;
  horizon 50k total 150k = 0/5/5. Jangan menyebut A selalu gagal.
- Horizon 50k total 150k: B galat 268,47 m, skor ruas 0,9034,
  Q-state rata-rata 28.103,2; C galat 339,91 m, skor 0,9193, Q-state 46.671,6.
  B/C sama-sama 5/5; tidak ada klaim unggul pada semua metrik atau generalisasi.
- Laporan: `docs/temp/analisis_surface_width_3m_20261102/ANALISIS.md`.
  Seluruh history/epsilon/metadata diperiksa dan 60 evaluasi direproduksi dari
  Q-table: metrik, node dan action cocok; tidak menjalankan training baru.
- Ada 27 loop valid dengan urutan edge berbeda, tetapi kemiripan geografis belum
  dinilai. Semuanya masih memuat ruas <3 m, width kosong, dan permissive.
  Seluruh action lolos kebijakan akses saat pelatihan. Validasi lapangan belum dilakukan.
- Hasil `konfigurasi_empat_20261029` dan `highway_dua_prioritas_20261101`
  tetap arsip. Jangan memakai angka/skor lama sebagai hasil grup terbaru;
  skor/reward lintas pemetaan tidak langsung sebanding atau mengisolasi satu faktor.
- Pada 3 November verifikasi sudah disesuaikan dan dijalankan ulang atas permintaan
  pengguna untuk semua notebook. Hasil training di atas tetap konfigurasi lama;
  jangan mereproduksi angka arsip dengan reward terbaru lalu mengklaim sama.

## Praktik kerja dan dokumentasi

- Word revisi merupakan usulan. Pengguna tidak menerapkan semua revisi Bab I–III;
  jangan menganggap seluruh saran sudah ada dalam naskah utama. Pemeriksaan
  konsistensi akhir harus membaca kembali naskah yang benar-benar disimpan.
- Gunakan bahasa naskah yang mudah dimengerti pembaca dan dosen. Jelaskan
  arti variabel, istilah, serta angka sebelum menarik kesimpulan. Hindari
  riwayat perubahan kode atau kalimat internal seperti “skor tidak dikurangi
  0,5” sebagai penjelasan metode; nyatakan aturan dan maknanya langsung.
- Fokus penulisan saat ini adalah Bab IV tanpa bagian verifikasi dan validasi.
  Kedua bagian tersebut ditunda sampai pengguna melanjutkannya secara khusus.

- Jangan mengubah dokumen TA utama `.docx` secara langsung. Berikan umpan balik
  di chat; buat Word sementara hanya jika diminta, agar pengguna menyalin manual.

- Simpan lampiran yang akan dipakai dalam naskah, seperti kode diagram,
  gambar, tabel terpisah, dan sumber rumus, secara permanen di `docs/`
  (folder bersama: `docs/assets/`). Jangan menyimpannya di
  `docs/temp/`; folder temp digunakan untuk Word panduan revisi atau bahan kerja
  sementara. Ini preferensi pengguna yang berlaku untuk pekerjaan berikutnya.

- Gunakan `docs/PANDUAN-TA-SKRIPSI-LENGKAP.pdf` sebagai rujukan saat meninjau atau menyusun naskah TA. Baca bagian yang relevan sebelum memberikan saran mengenai sistematika, format penulisan, dan sitasi.
- Gunakan komentar kode berbahasa Indonesia yang menjelaskan alasan, terutama pada reward, action mask, dan state.
- Setelah perubahan desain atau hasil penting, sinkronkan `IMPLEMENTASI.md` dan `LOG_KEMAJUAN.md`.
- Setelah memakai sumber baru dalam naskah TA, sinkronkan `referensi.md`; jangan memakai angka atau klaim dari sumber yang belum dicatat di sana.
- Saat mengubah notebook, pastikan cell dapat dijalankan sebagai kode dan tidak bergantung pada cell lama yang sudah dihapus. Cell eksperimen memuat ulang `rute_lari_core` untuk menghindari versi module lama pada kernel.
- Untuk angka Bab IV dan Bab V, gunakan CSV hasil dari satu konfigurasi final yang sama, bukan angka lama yang tersimpan di dokumen `.docx`.
- Prioritaskan penjelasan dalam bahasa Indonesia dan fokus pada isi/metodologi sebelum format penulisan.
- Pada setiap revisi subbab TA, periksa pula apakah tabel, gambar, atau rumus diperlukan untuk memperjelas relasi yang penting. Tambahkan hanya bila memberi nilai penjelasan; simpan kode PlantUML yang relevan di `docs/` agar pengguna dapat merendernya sendiri.
- Utamakan diagram PlantUML yang tidak melebar. Untuk diagram dengan beberapa node atau tahap, gunakan orientasi vertikal (`top to bottom direction`) kecuali orientasi horizontal tetap jelas dan muat nyaman pada lebar halaman laporan.
- Kode dan nama berkas PlantUML harus netral: jangan menyertakan nomor gambar, nomor bab, atau caption. Pengguna menentukan penempatan, nomor, dan caption saat menyusun laporan.


## Analisis lima atribut OSM

- Klarifikasi pengguna 29 Oktober 2026: highway, surface, width, smoothness,
  dan access harus terintegrasi pada seluruh analisis atribut yang relevan,
  bukan hanya ditambahkan sebagai dua bagian terpisah.
- `analisa.ipynb` memakai satu tabel edge untuk sampel, tabel/diagram kelengkapan,
  distribusi, diagram distribusi enam panel, kombinasi ketersediaan lima atribut,
  dan tooltip peta yang sudah ada. Tidak ada analisis kandidat tag lain.
- Smoothness yang belum ada di GraphML dibaca dari cache snapshot dan ditambahkan
  hanya pada salinan tabel. Nilai dipakai untuk satu edge bila seluruh way asal
  ditemukan dan bertag; data parsial disimpan pada kolom nilai asal/status.
- Snapshot saat ini: 13.938 edge smoothness lengkap (65,21%), 216 parsial;
  access terisi pada 648 edge (3,03%). Semua persentase utama memakai edge,
  bukan mencampurkan jumlah way sumber dengan edge. Tabel access--foot tetap
  memakai way yang sama sebagai pemeriksaan pendamping izin.
- Notebook 43 cell sudah dijalankan seluruhnya pada Python 3.13; output tersimpan.
  Skor tetap highway/surface/width; versi terakhir analisis memakai core bersama.
  Pada 3 November analisis/verifikasi dijalankan ulang untuk reward langsung.
  GraphML tetap. Hasil training arsip dan status grup baru dijelaskan di atas.

- Pembaruan 30 Oktober 2026: peta graf berdasarkan highway pada analisa.ipynb
  memiliki marker access berwarna/ikon per kategori, layer per jenis dan legenda.
  Marker berada di tengah geometri ruas pada CRS meter lalu diproyeksikan WGS84;
  edge dua arah identik berbagi satu marker, key paralel berbeda tetap terpisah.
  Popup memuat tag/nama/way/edge. Ini visualisasi tag, bukan keputusan izin akses.

- Klarifikasi lanjutan 30 Oktober 2026: bagian peta bernama **Peta Interaktif
  Atribut Jalan dan Akses**. Highway aktif secara default; Surface (ditambahkan
  2 November) dan Smoothness dipilih bergantian melalui radio layer. Warna Surface
  adalah material asli, dengan skor core pada tooltip. Marker access per jenis
  awalnya tidak aktif.
  Legenda mengikuti tema ruas dan status marker yang aktif; basemap tetap tampil.
- Fokus pengembangan berikutnya adalah access agar tidak menambah kompleksitas.
  Smoothness hanya dipakai dalam analisis/visualisasi, belum menjadi reward.
  Per 2 November 2026 blacklist diganti whitelist pada build_actions():
  hanya yes/permissive dan tag kosong yang lolos; nilai baru/unknown ditolak.
  List/string list/titik koma diizinkan hanya jika seluruh nilai terisi termasuk
  whitelist. Foot=yes tidak mengesampingkan nilai access di luar daftar.
  Reward permissive tetap PERMISSIVE_PENALTY_PER_100M=-0.10 dikalikan panjang/100;
  yes/kosong mendapat komponen akses nol. Gabungan permissive memakai seluruh
  panjang edge sebagai pendekatan konservatif, bukan pemetaan pagar.
- Pada snapshot utama whitelist dan blacklist lama memberi 21.300 action identik;
  graf uji unduhan terbaru 22.058 action identik. Notebook/grup A--C, seed,
  skor dan hasil tersimpan tidak diubah dalam revisi whitelist. Metadata lama
  tetap merekam kebijakan saat training. Metadata run baru menyimpan whitelist,
  izin tag kosong dan aturan gabungan. Data lokasi lain dapat memiliki perubahan
  action jika mengandung nilai di luar whitelist; jangan menganggap semua graf ekuivalen.
- Kesetaraan action berlaku pada penggantian whitelist; reward langsung 3 November
  mengubah reward. Grup reward_direct_20261103 selesai dilatih dan diaudit;
  surface_width_3m_20261102 tetap arsip yang tidak ditimpa.
  Perbandingan dengan baseline lama tetap melibatkan beberapa perubahan desain,
  bukan isolasi penalti akses. Start penelitian tetap.

## Kesepakatan verifikasi, validasi, dan pemanfaatan

- Rincian ada pada `docs/VERIFIKASI_VALIDASI_DAN_KATALOG.md`.
- Hitungan manual Q tetap diperlukan sebagai beberapa contoh representatif,
  bukan seluruh episode: transisi nonterminal dengan next Q tidak nol,
  komponen akses, dan terminal tanpa bootstrap. Angka harapan harus independen.
- Verifikasi state/mask/graf/jarak/terminasi/reward memakai core yang sama,
  graf sintetis MultiDiGraph dan sampel snapshot nyata. Legalitas harus konsisten
  pada eksplorasi, greedy dan bootstrap. Sifat Markov bukan dijamin oleh assertion.
- Evaluasi eksperimen (A--C matched settings) berbeda dari verifikasi kode dan
  validasi lapangan. Rute gagal tetap dilaporkan, tidak dimasukkan katalog.
- Validasi lapangan direncanakan pada rute berhasil, kemungkinan B/C, dengan
  Huawei Watch Fit 3/Huawei Health. Strava tidak diperlukan. Rekaman GPS adalah
  pembanding dengan ketidakpastian, bukan jarak mutlak benar.
- Tidak tumpang tindih bukan syarat mutlak: aturan revisit sekarang tetap.
- GPX/navigasi ditunda sampai rute/akses dinilai; belum ada implementasi ekspor.
- Pembimbing menyarankan UI berupa katalog beberapa rute yang dihasilkan,
  diseleksi, dan disimpan sebelumnya. Tidak perlu training saat pengguna membuka
  app atau dukungan titik awal bebas. Ini rencana, belum aplikasi/katalog siap pakai.
- Practical implications: bantuan perencanaan rute lokal, pertimbangan pemilihan
  representasi state, dan bukti keterbatasan OSM dari pemeriksaan lapangan.
  Rumusan masalah kedua tetap pengaruh representasi state; epsilon faktor eksperimen.

## Verifikasi implementasi

Per 3 November: 49 cell/32 cell kode dijalankan ulang pada kernel bersih memakai
reward langsung. Lima poin sesuai expected: manual Q sintetis/OSM, state/mask,
graf/jarak, terminasi dan reward. Expected ditulis independen; tidak diturunkan
langsung dari fungsi yang diuji. Perbandingan numerik memakai toleransi kecil.

- train_step/core.step yang sama dipakai training dan verifikasi. Tidak ada class
  QValueUpdater/helper framework baru. latest_state tetap property build_state.
- Dua episode sintetis MultiDiGraph dengan atribut jalan dan build_actions;
  epsilon per episode, Q-table/RNG diteruskan ketika reset.
- Sampel OSM lokal tiga langkah; contoh manual pertama memuat penalti permissive.
  Next Q legal nonnol dan terminal tanpa bootstrap juga diuji eksplisit.
- Mask access, revisit, closing, key paralel; jarak/progres/reset serta batas
  4.500/5.500/220 langkah diperiksa. Ini tidak membuktikan sifat Markov.
- Gabungan skor -1..1, angka reward fase/akses/revisit/terminal dan penjumlahannya
  diperiksa. Uji stres edge 100 km tetap terpisah dari data nyata dan menunjukkan
  tidak ada jaminan semua kegagalan memberi reward lebih rendah dari semua sukses.
- Kelulusan eksekusi bukan tanda seluruh kasus selesai direview pengguna; tinjau
  relevansi uji stres/validasi lapangan saat pengguna meminta. Jangan menambah
  aturan atau menjalankan training panjang secara mandiri.


## Pengukuran overlap dalam satu rute (3 November 2026)

Riwayat tahap awal: overlap dihitung terpisah atas 60 rute evaluasi tersimpan.
Keputusan lanjutan pengguna menyederhanakan menjadi satu kolom overlap_ratio dan
meminta pencatatan tiap episode. Implementasi aktif sudah mencatatnya pada core
serta section grafik terpisah; lihat bagian Pencatatan overlap selama training.
Angka di bawah tetap hasil postprocessing grup reward_direct_20261103.

Identitas ruas berdasarkan geometri tanpa membedakan arah; ruas paralel berbeda
geometri tetap terpisah, persimpangan satu titik tidak dihitung. Panjang memakai
edge.length agar konsisten dengan jarak lama. Pada 60 rute ini union geometri
memastikan tidak ada overlap parsial tambahan. Tanpa geometry memakai garis node,
sesuai representasi graf. Data lain dengan overlap parsial perlu perluasan metode.

Semua 43 loop valid overlap, rentang 5,94--26,43%. Rata-rata B/C: dinamis
75K 17,28%/15,67%; dinamis 150K 18,57%/19,21%; horizon total 75K
19,41%/10,90%; horizon total 150K 20,19%/15,89%. Semua B/C lima loop valid.
A hanya dua/satu loop pada horizon, jadi tidak dibandingkan rate overlap saja.

B horizon seed 0 (75K/150K identik): panjang 4.915,66 m, ruas unik 3.616,22 m,
pengulangan 1.299,45 m/26,43%, 12 lintasan ulang, 14 revisit node.
Seluruh pengulangan contoh ini reverse; unique_edge_ratio terarah tetap 1,00.
B terbaik rata-rata galat/skor belum tentu terbaik overlap. C horizon total 75K
paling rendah overlap di B/C: 505,78 m/10,90%, tetapi galat 365,27 m/skor 0,9149.
Belum ada ambang overlap, perubahan pemilihan katalog, reward atau aturan revisit.

Laporan: docs/temp/analisis_reward_direct_20261103/OVERLAP.md, CSV per seed/
ringkasan/ruas berulang, grafik dan peta contoh berwarna merah. Sembilan kasus
kecil dan identitas jarak lulus; 228 berkas hasil mentah/GraphML tetap. Browser
peta contoh: 33 ruas fisik unik, 12 ruas berulang, toggle lulus tanpa error JS;
screenshot diperiksa. Menghitung hanya evaluasi akhir, bukan jutaan episode.


## Pencatatan overlap selama training (3 November 2026)

Definisi aktif yang disepakati pengguna adalah hitungan lintasan ruas:
overlap_ratio = (N_total - N_unik) / N_total. N_total adalah jumlah lintasan edge,
N_unik adalah jumlah ruas fisik unik tanpa membedakan arah. Panjang dalam meter
tidak menjadi bobot. Satu ruas dilalui tiga kali berarti dua lintasan ulang.
Geometri ter-normalisasi menjadi identitas ruas; paralel berbeda geometri tetap
terpisah. Identitas dipersiapkan sekali pada build_actions. Tanpa lintasan, nilai
NaN/null; hanya satu kolom overlap_ratio (0--1) disimpan tiap episode/evaluasi/JSON.

Grafik overlap tetap section tersendiri, tetapi hanya SATU PANEL untuk SELURUH
EPISODE, tanpa pemisahan atau penyaringan berhasil/gagal. Kurva persen memakai
jendela 50 episode dan rata-rata observasi antar-seed. Section 3.3 notebook A--C
juga memakai seluruh seed evaluasi; agregat bernama mean_overlap_ratio.
Metadata basis=physical_road_traversal_count dengan rumus hitungan, bukan panjang.
Reward, mask (revisit >=2.500 m), state, epsilon, seed dan pemilihan peta tetap.

Target training A--C sekarang reward_direct_overlap_count_20261103. Pengguna sudah
memiliki hasil pada reward_direct_overlap_20261103 yang berbasis meter, sehingga
folder itu dipertahankan. Jangan mencampur persentase berbasis meter dan hitungan.
Hasil reward_direct_20261103 tetap arsip tanpa pencatatan overlap tiap episode.
Muat ulang notebook dan jalankan cell muat graf untuk memperbarui RESULT_GROUP
sebelum training. Uji titik tetap memakai overwrite training terbaru melalui core
bersama, tanpa unduhan ulang bila hanya training diulang. Koordinat tetap.

Pengujian lulus: 180 episode sintetis A--C/dua seed menghasilkan Q-table dan semua
metrik selain overlap identik terhadap versi sebelumnya; 60 rute arsip cocok
hitungan lintasan audit independen. Contoh lima lintasan/empat ruas unik menghasilkan
20%, meskipun ruas ulang 1.500 m dari total 5.000 m (metode meter akan 30%).
Grafik diuji tanpa kolom is_loop, satu panel, rata-rata semua observasi. Alur simpan/
baca/tampil A/B/C satu seed dan label arsip meter lulus. Verifikasi kernel bersih
49 cell/32 code lulus; gambar diperiksa visual. 290 berkas hasil lama serta graf,
analisa dan dependensi tidak diubah. Tidak ada training penelitian/unduhan baru.


### Klarifikasi identitas ruas overlap (3 November 2026)

- Shapely sudah ada sejak setup uv (pyproject.toml, 9fd76a0, 9 Oktober 2026);
  tidak diinstal khusus untuk overlap. normalize() method, wkb properti bytes.
- physical_road_id = geometry.normalize().wkb hanya untuk menghitung ruas unik.
  Action agen tetap (next_node,key). Geometri sama termasuk arah balik digabung,
  geometri berbeda dipisah; key berbeda dengan geometri sama tetap satu ruas
  pada metrik. Jika geometry absen, garis endpoint dapat menyamakan paralel
  yang endpoint-nya sama. Rincian/contoh/rujukan ada pada akhir IMPLEMENTASI.md.
- Rumus aktif hitungan lintasan, bukan meter; satu grafik seluruh episode.
  B arsip seed 0: 12/45=26,67% (meter lama 26,43%, jangan dicampur).
- Pengguna memilih B lebih dahulu sebagai referensi. Sinkronisasi ini hanya
  dokumentasi; tidak mengubah core/notebook/dependensi atau menjalankan training.


### Pengamatan B epsilon dinamis dengan overlap hitungan (3 November 2026)

Pengguna menyelesaikan B dinamis 75K dan 150K pada grup
reward_direct_overlap_count_20261103: 10 training/lima seed per konfigurasi,
1.125.000 baris history. Metadata basis count, episode/epsilon dan artefak lengkap.
Seluruh 10 evaluasi Q-table direproduksi; metrik/path sesuai dan count diperiksa
langsung dari geometri. Rute akhir serta metrik lama sama dengan arsip reward
langsung pada seed/konfigurasi yang sama. Tidak ada training baru oleh agent.

| Ukuran | 75K | 150K |
|---|---:|---:|
| Loop greedy | 5/5 | 5/5 |
| Overlap greedy rata-rata | 12,98% | 15,35% |
| Galat rata-rata | 399,63 m | 340,90 m |
| Skor ruas rata-rata | 0,9125 | 0,9247 |
| Rata-rata Q-state | 15.446,4 | 17.439,4 |
| Overlap seluruh episode, 10K terakhir | 11,97% | 12,82% |
| Keberhasilan training, 10K terakhir | 66,19% | 81,55% |

150K lebih dekat ke target rata-rata 58,72 m dan skor lebih tinggi, tetapi overlap
bertambah 2,37 poin persentase. Tidak unggul semua metrik. Kurva seluruh episode
naik dari sekitar 0,4% menjadi 12--13%; awal training rata-rata jarak hanya ~1 km,
sering belum mencapai izin revisit 2.500 m. Overlap rendah di awal bukan bukti
rute lebih baik. Overlap belum menjadi reward. Tidak membuat grafik yang memisah
berhasil/gagal. Epsilon rata-rata 10K terakhir berbeda (~0,1133 vs ~0,0817), jadi
jangan mengisolasi efek jumlah episode dari perbedaan fase eksplorasi itu.

Overlap greedy per seed 75K: 13,95%;20,93%;10%;10%;10%.
150K: 13,95%;11,63%;18,60%;18,60%;13,95%. Seed 1 membaik, lainnya tidak seragam.
75K tiga urutan edge unik (seed 2/3/4 sama), 150K empat (seed 0/4 sama).
Seluruh loop masih <5.000 m tetapi sah toleransi. Ini pengamatan B satu start/
snapshot, bukan hasil A--C lengkap atau validasi lapangan. Pembanding berikutnya
sesuai rancangan adalah B horizon 50K, tanpa mengubah reward dahulu.

Laporan/CSV/grafik: docs/temp/analisis_B_dinamis_overlap_count_20261103/ANALISIS.md.
Tidak mengubah core/notebook/reward/mask atau hasil mentah; hanya laporan dan
konteks markdown disinkronkan. Hasil count lain belum ditinjau pada audit ini.


### Pengamatan empat konfigurasi B dengan overlap hitungan (3 November 2026)

Lengkap pada grup reward_direct_overlap_count_20261103: empat konfigurasi B,
20 training/lima seed per konfigurasi, 2.250.000 baris history. A/C belum tersedia
pada grup ini saat pemeriksaan. Seluruh metadata/episode/epsilon/artifact lengkap;
20 evaluasi Q-table direproduksi dan count diverifikasi. Nilai/rute akhir cocok
arsip reward_direct_20261103 untuk konfigurasi/seed sama. 80 berkas sumber tetap.

| Konfigurasi | Loop | Galat rata-rata | Overlap rata-rata | Skor ruas |
|---|---:|---:|---:|---:|
| Dinamis 75K | 5/5 | 399,63 m | 12,98% | 0,9125 |
| Dinamis 150K | 5/5 | 340,90 m | 15,35% | 0,9247 |
| Horizon 50K total 75K | 5/5 | 321,74 m | 15,05% | 0,9285 |
| Horizon 50K total 150K | 5/5 | 289,82 m | 17,43% | 0,9356 |

Saran praktis sementara B horizon total 75K: mean galat/overlap/skor lebih baik
sedikit dari dinamis 150K dengan setengah episode. Horizon 150K lebih baik galat/
skor, tetapi dibanding horizon 75K hanya memperbaiki galat 31,92 m sambil menambah
overlap 2,38 poin dan dua kali episode. Dinamis 75K paling rendah mean overlap.
Tidak satu konfigurasi unggul semua ukuran; selisih deskriptif pada lima seed,
bukan klaim signifikansi/generalitas. Semua konfigurasi tetap untuk laporan.

Training seluruh episode pada 10K akhir: overlap 11,97/12,82/13,75/14,21%;
keberhasilan 66,19/81,55/84,83/87,11% pada urutan konfigurasi tabel. Horizon
memiliki epsilon 0,05; dynamic window masih berbeda epsilon. Tidak menyimpulkan
konvergensi formal dari kurva mendatar atau bahwa overlap harus turun.

Pemilihan peta saat ini berdasarkan galat, tidak mempertimbangkan overlap.
Pada dua konfigurasi horizon, seed 0 terpilih: 4.915,66 m tetapi overlap 26,67%,
tertinggi di seed masing-masing. Kandidat kompromi yang dapat diperiksa:
- Dinamis 75K seed 0: 4.685,49 m / overlap 13,95% / skor 0,9255; identik
  dinamis 150K seed 0/4 serta horizon 150K seed 1/4.
- Horizon 75K seed 2: 4.614,91 m / overlap 11,36% / skor 0,9411.
20 hasil hanya 13 urutan edge unik; belum jaminan 13 rute geografis berbeda.

Belum mengubah reward/mask atau memilih kandidat katalog final. Periksa beberapa
rute/pagar/akses aktual dahulu. Untuk rumusan masalah kedua tetap pakai A--C
setelan sama; overlap akhir arsip A/C bisa dihitung ulang tanpa training, tetapi
tren overlap tiap episode A/C memerlukan pencatatan baru. Jangan menambah episode
atau faktor baru hanya untuk mengejar overlap rendah tanpa tujuan yang disepakati.

Laporan/CSV/grafik: docs/temp/analisis_B_empat_konfigurasi_overlap_count_20261103/ANALISIS.md.
Hanya laporan/dokumentasi diperbarui, tanpa training/unduhan/ubah kode atau
hasil mentah. Ini hasil B lokal, bukan validasi lapangan atau hasil lengkap A--C count.


## Pengamatan B dinamis 75K: reward lama, langsung -1 dan -3 (3 November 2026)

Pengguna sudah menjalankan B dinamis 75K pada reward_revisit_3_overlap_count_20261103.
375.000 history lengkap, lima seed; sepuluh evaluasi -1/-3 diulang dan cocok
metrik serta node/action. Episode/seed/epsilon ketiga versi cocok persis.

| Versi | Loop 10K terakhir per seed, agregat lima seed | Loop greedy | Overlap greedy |
|---|---:|---:|---:|
| surface_width_3m_20261102: netral 0,50, revisit -8 | 0,116% | 0/5 | Tidak dihitung pada audit ini |
| reward_direct_overlap_count_20261103: revisit -1 | 66,19% | 5/5 | 12,98% |
| reward_revisit_3_overlap_count_20261103: revisit -3 | 51,66% | 5/5 | 6,70% |

Reward lama/banyak faktor berubah: revisit -8 ke -1/-3, arah 0,40 ke 0,60,
bonus 80 ke 100, pemetaan/rumus reward ruas. Jangan menyimpulkan penghapusan
netral 0,50 sendiri penyebab peningkatan. Versi lama greedy tidak pernah punya
closing action; kedua baru 5/5 pernah tersedia dan berhasil. -1 ke -3 hanya
mengubah penalti: tradeoff training loop turun 14,53 poin tetapi overlap greedy
turun 6,28 poin; galat greedy rata-rata turun 399,63 ke 351,03 m.
B dinamis 150K -3 juga memiliki artefak tetapi belum ditinjau dalam audit ini.
Tidak mengubah kode/notebook/hasil mentah, training atau unduhan.
Laporan: docs/temp/analisis_B75_perbandingan_reward_20261103/ANALISIS.md.



## Pengamatan B dinamis 75K dan 150K, penalti -3 (3 November 2026)

Dua durasi -3 selesai lima seed. Dibanding -1 pada durasi/seed/epsilon sama:

| Episode | Loop greedy -1/-3 | Overlap greedy -1 -> -3 | Loop 10K akhir -1 -> -3 |
|---|---:|---:|---:|
| 75K | 5/5 dan 5/5 | 12,98% -> 6,70% | 66,19% -> 51,66% |
| 150K | 5/5 dan 5/5 | 15,35% -> 6,94% | 81,55% -> 78,77% |

Seluruh sepuluh pasangan seed/durasi menurun overlap-nya. -3 sudah berpengaruh
cukup besar secara deskriptif; tidak menyimpulkan optimalitas atau signifikansi.
150K -3 mean galat 296,65 m (lama -1 340,90 m), skor ruas 0,9172 (lama 0,9247).
Peta 150K -3 seed 0: 4.808,07 m, overlap 2/47=4,26%, node revisit 5. Dua ruas
berulang bernama Dukuh Kupang Barat XVI/XVII; belum terbukti wajib atau minimal.
Sepuluh evaluasi 150K direproduksi; metrik/path cocok. Audit 75K sebelumnya cocok.
Saran -5 hanya eksperimen lanjutan bila diinginkan, belum diterapkan; core tetap -3.
Tidak mengubah kode/notebook/hasil mentah atau menjalankan training/unduhan.
Laporan: docs/temp/analisis_B_dinamis_revisit3_20261103/ANALISIS.md.



## Kemiripan seed B dinamis 75K -3 (3 November 2026)

Urutan edge diperiksa: hanya seed 1/2 identik (4.604,73 m, overlap 4,65%, 43
langkah); seed 3 berbeda (5.117,60 m, 3,77%, 53 langkah). Seed 0 juga berbeda
meskipun panjang dekat. Q-table 1/2 berbeda (17.116/17.213 state); nilai Q action
terpilih berbeda pada 42/43 langkah tetapi action terbaik sama, tanpa seri Q
terbaik pada seluruh 43 langkah keduanya. Evaluasi greedy tidak mengeksplorasi.
Seed berbeda bukan tujuan keragaman antar-rute; revisit mengatur satu episode.
Versi -3 memiliki empat urutan unik/5 loop, -1 tiga/5 loop (seed 2/3/4 identik),
versi lama netral lima urutan berbeda tetapi 0/5 loop. Bukan bukti optimalitas atau
konvergensi global. Core/reward/mask/evaluasi tetap; tidak ada training/unduhan.
Laporan: docs/temp/analisis_kemiripan_seed_B75_20261103/ANALISIS.md.



## Reward, epsilon dan state: pembanding terbaru 75K -3 (3 November 2026)

C dinamis 75K dan B horizon 50K total 75K sudah tersedia. Pada reward -3 sama:
B dinamis loop 5/5, galat 351,03 m, overlap 6,70%; B horizon loop 5/5,
galat 195,68 m, overlap 7,33%; C dinamis loop 5/5, galat 290,92 m, overlap
4,74%. Seluruh 15 evaluasi direproduksi, metrik/path cocok. Ini hasil lokal lima
seed, bukan superioritas umum atau signifikansi. Training 10K akhir masing-masing
51,66%/77,58%/52,95%, tetapi epsilon B horizon lebih rendah saat pengukuran.
Rekomendasi pembahasan: perbandingan A/B/C tetap inti rumusan masalah state;
dua epsilon tetap berguna sebagai konfigurasi pendukung walau loop sudah 5/5.
B sukses tidak membuat C redundan. Insentif reward lama-baru berubah bersama;
jangan menyebut penghapusan netral 0,50 sebagai penyebab tunggal. Rancangan,
core, notebook dan hasil mentah tidak diubah; tanpa training/unduhan baru.
Laporan: docs/temp/analisis_reward_epsilon_state_20261103/ANALISIS.md.



## Seluruh empat konfigurasi B penalti -3 selesai (3 November 2026)

Grup reward_revisit_3_overlap_count_20261103: 20 training/2.250.000 episode,
semua 20 greedy valid. Dinamis 75K/150K overlap 6,70%/6,94%; horizon 50K total
75K/150K 7,33%/8,12%. Pembanding -1 berturut-turut 12,98/15,35/15,05/17,43%.
Training loop 10K akhir -3: 51,66/78,77/77,58/82,20%. Seluruh parameter metadata
selain penalti/pemilihan peta cocok, seed/episode/epsilon antarversi cocok persis.
Lima evaluasi horizon total 150K direproduksi, metrik/path cocok; konfigurasi
lain sudah direproduksi sebelumnya. Saran -5 sebagai eksperimen lanjutan tetap
belum diterapkan. Core masih -3. Hasil hanya lokal lima seed/start penelitian.
Peta horizon150K memilih seed 1 overlap 12,24%; seed 3 hanya 1,96%, karena peta
dipilih menurut galat jarak, bukan overlap. Jangan menyamakan peta dengan mean.
Laporan: docs/temp/analisis_B_empat_konfigurasi_revisit3_20261103/ANALISIS.md.
Tidak mengubah kode/notebook/hasil mentah atau menjalankan training/unduhan.

## Audit awal B/C penalti -5, sebelum konfigurasi C terakhir selesai (3 November 2026)

B lengkap empat konfigurasi; C lengkap tiga. C horizon 50K total 150K belum punya
metadata/history/evaluasi akhir (saat laporan disimpan 4/5 rute seed ada).
35 training/3.750.000 history, 30/35 greedy valid; seluruh 35 direproduksi dengan
metrik/path cocok dan overlap geometri diverifikasi, 140 berkas sumber tetap.

| Konfigurasi | Loop B/C | Overlap B/C |
|---|---:|---:|
| Dinamis 75K | 1/5 dan 4/5 | 6,92% / 4,13% |
| Dinamis 150K | 5/5 dan 5/5 | 5,24% / 3,07% |
| Horizon 50K total 75K | 5/5 dan 5/5 | 3,37% / 3,69% |
| Horizon 50K total 150K | B 5/5; C belum final | B 5,58%; C belum final |

Overlap mean seluruh seed, termasuk gagal; jangan menyebut overlap rendah pada
rute gagal sebagai keberhasilan. B dinamis75 gagal empat over_distance; C dinamis75
satu buntu. Semua gagal tidak pernah punya closing action. -5 dibanding -3
mengurangi overlap tiga konfigurasi B tetapi menurunkan greedy B dinamis75 dari
5/5 ke 1/5 dan C dinamis75 dari 5/5 ke 4/5. Jangan menaikkan penalti lagi dulu.
C horizon75 seed3 adalah kandidat: 4.860,94 m, overlap0%, galat139,06m, revisit1;
belum validasi lapangan. C dinamis150 menggunakan sekitar2,2x Q-state B, overlap
lebih kecil dan galat hampir sama. Dua epsilon dan state tetap pembanding relevan.
Tidak mengubah kode/notebook/hasil mentah atau menjalankan training/unduhan.
Laporan: docs/temp/analisis_BC_revisit5_20261103/ANALISIS.md.


## Audit lengkap B/C penalti -5 (3 November 2026)

Kini delapan konfigurasi B/C lengkap: 40 training/4.500.000 episode, 35/40 greedy
valid (B16/20, C19/20). Seluruh 40 direproduksi; metrik/path cocok dan overlap
geometri independen cocok. Seed/episode/epsilon/parameter B-C konsisten; 160
berkas sumber tetap. Audit awal tujuh konfigurasi tetap riwayat.

| Konfigurasi | Loop B/C | Overlap B/C | Galat B/C |
|---|---:|---:|---:|
| Dinamis75K | 1/5 dan 4/5 | 6,92% / 4,13% | 473,55 / 287,57 m |
| Dinamis150K | 5/5 dan 5/5 | 5,24% / 3,07% | 302,74 / 304,64 m |
| Horizon50K total75K | 5/5 dan 5/5 | 3,37% / 3,69% | 357,69 / 301,80 m |
| Horizon50K total150K | 5/5 dan 5/5 | 5,58% / 3,16% | 212,43 / 344,99 m |

Mean seluruh lima seed, termasuk gagal. Kegagalan hanya dinamis75: B empat
over_distance, C satu buntu, semua tidak pernah punya closing action. Dibanding
-3, -5 menekan overlap tiga konfigurasi B tetapi menurunkan loop dinamis75.
Jangan menaikkan penalti lagi dulu. Dua epsilon dan perbandingan state masih
berguna; tidak ada konfigurasi unggul semua ukuran. C dinamis150 Q-state sekitar
2,2x B; ini bukan pengukuran rasio RAM/waktu. Semua angka deskriptif lima seed.
Ada lima loop overlap0%; kandidat C horizon75 seed3 4.860,94m/galat139,06m,
node revisit1. Periksa peta/lapangan sebelum katalog. Tidak ada validasi lapangan.
Laporan terbaru: docs/temp/analisis_BC_revisit5_lengkap_20261103/ANALISIS.md.
Tanpa perubahan kode/notebook/hasil mentah, training penelitian atau unduhan.


## Pembaruan eksperimen -10, tiga worker (3 November 2026)

Pengguna secara eksplisit meminta -10 dan MAX_WORKERS=3 meski audit -5 sebelumnya
menyarankan menahan penalti. Ikuti permintaan terbaru; jangan mengembalikan -5
secara otomatis. Grup A--C reward_revisit_10_overlap_count_20261103 belum dilatih.
Core hanya berubah konstanta -5 ke -10; logika worker, Q, mask, state dan epsilon
tetap. Uji titik satu seed mengikuti penalti core, tetap satu proses. Verifikasi
32 cell lulus; uji Jupyter membuktikan Q/history/metrik/rute identik 1 vs 3 worker
pada lima seed sintetis. Reload notebook dari disk dan restart kernel sebelum
training agar grup hasil dan jumlah worker diperbarui. Semua hasil lama tetap.


## Audit lengkap A–C penalti -10 (3 November 2026)

12 konfigurasi/60 training/6.750.000 episode lengkap. Seluruh60 evaluasi Q-table
cocok metrik/path, overlap geometri independen cocok, metadata -10/3worker,
seed/episode/epsilon/artefak diperiksa. 240 berkas sumber tetap. Greedy25/60 valid:
A3/20, B11/20, C11/20. Selesai training berbeda dari keberhasilan evaluasi.

| Konfigurasi | Loop A/B/C | Overlap A/B/C |
|---|---:|---:|
| Dinamis75K | 0/5, 0/5, 2/5 | 5,12%, 5,46%, 4,67% |
| Dinamis150K | 1/5, 4/5, 3/5 | 3,31%, 0,82%, 0,86% |
| Horizon50K total75K | 0/5, 2/5, 3/5 | 4,17%, 0,71%, 0,74% |
| Horizon50K total150K | 2/5, 5/5, 3/5 | 1,43%, 2,42%, 1,13% |

Overlap mean seluruh lima seed termasuk gagal. B/C turun35/40 pada -5 ke22/40
pada -10; menekan overlap dengan biaya keberhasilan. Satu-satunya5/5 adalah B
horizon150K (galat252,25m, overlap2,42%, skor0,9339). Kegagalan32 over_distance,
3 buntu, semuanya tidak pernah punya closing action legal. Sebelas gagal punya
overlap0%, jadi overlap tidak menggantikan syarat loop. Sembilan valid overlap0%.
C horizon75 seed4 kandidat4.913,09m/galat86,91m/overlap0%; B horizon150 seed1
5.092,78m/galat92,78m/overlap3,28%. Belum validasi lapangan atau pilihan final.
Rekomendasi jangan naikkan penalti lagi; simpan -10 untuk sensitivitas. Kode tetap
-10/3worker, tanpa perubahan otomatis. Parameter reward final A–C harus sama.
Laporan: docs/temp/analisis_ABC_revisit10_20261103/ANALISIS.md.
Tanpa perubahan kode/notebook/hasil mentah, training penelitian atau unduhan.

## Audit sinkronisasi uji titik start (3 November 2026)

uji_titik_start.ipynb sudah memakai core bersama: reward -10/mask/Q/epsilon/
overlap count. Default B150K/horizon50K, satu seed acak dicatat dan satu proses;
ini sengaja berbeda dari lima seed/tiga worker A--C. Kode notebook/koordinat tidak
diubah. Hasil uji terakhir yang tersimpan saat audit masih penalti -1, sehingga
perlu training ulang untuk hasil parameter terbaru; bukan kode yang tertinggal.

Uji cell asli dengan graf sintetis/folder sementara lulus: force download/no-cache
arguments, preview Highway/Surface/Access, metadata -10/seed/worker/overlap, display,
retraining tanpa unduh, overwrite training saja, penolakan koordinat lama serta
invalidasi hasil setelah unduh baru. 2.583 berkas penelitian tetap. Tidak ada
unduhan nyata atau training penelitian, hanya enam episode per uji singkat.
Audit: docs/temp/audit_uji_start_sync_20261103/AUDIT.md.


## Koneksi Overpass uji titik (3 November 2026)

Atas permintaan pengguna, pengaturan server alternatif di-revert. Notebook
kembali memanggil core.load_or_download_graph() langsung tanpa OVERPASS_URL,
perubahan ox.settings.overpass_url atau User-Agent khusus. Server mengikuti
bawaan OSMnx (https://overpass-api.de/api pada versi terpasang). Muat ulang
notebook dari disk dan restart kernel sebelum menjalankan ulang dari awal.

Force download/use_cache=False, pembatalan konteks saat gagal, koordinat/radius,
reward dan konfigurasi training tetap. Core, notebook A--C dan hasil penelitian
tidak diubah. Sumber cell koneksi kembali sama dengan sebelum percobaan endpoint
alternatif; sintaks seluruh cell diperiksa. Tidak menguji unduhan jaringan atau
menjalankan training. Probe/kontrol koneksi sebelumnya tetap riwayat pada
docs/temp/audit_overpass_connection_20261103/AUDIT.md; bukan bukti layanan pulih.

## Uji titik: tiga seed acak (3 November 2026)

Atas permintaan pengguna untuk memeriksa rute yang selalu sama, notebook uji titik
kini menjalankan tiga training mandiri per batch. RANDOM_SEEDS=None membuat tiga
seed acak berbeda melalui SystemRandom.sample(range(2**32), 3), dicetak/disimpan.
Tuple tiga integer berbeda boleh diisi untuk mengulang. Default B/150.000 episode
PER SEED/horizon50.000; total450.000 episode. MAX_WORKERS=3 memakai core spawn
bersama, bisa diisi1 untuk berurutan. A--C tetap lima seed0--4 tanpa perubahan.

Graf/titik/reward/mask/state/Q/epsilon tetap sama antar-seed. Training memakai G
memori, tidak mengunduh atau memuat ulang graf. Folder training/ dibersihkan SEKALI
per batch, lalu menampung ketiga Q-table, JSON rute, CSV metrik/grafik gabungan,
dan peta_scenario_{scenario}_seed_{seed}.html. Metadata titik memuat semua seed dan
nama peta. Cell hasil membaca hasil tersimpan, menampilkan SEMUA peta per seed;
peta perwakilan core tetap disimpan tetapi tidak dipakai sebagai satu-satunya
peta uji. perbandingan_rute_seed.csv memberi kelompok_rute berdasarkan urutan
tepat (from_node,next_node,key). Kelompok sama berarti urutan identik; jumlah
unik mencakup rute gagal. Ini bukan metrik persentase kemiripan geografis.

Dua batch sintetis @3seed x6episode diuji memakai cell asli dan3 worker spawn:
metadata/Q/JSON/peta per seed lengkap, hasil tanpa training, grup sama/berbeda,
overwrite training saja, konfigurasi/titik lama ditolak, training ulang tanpa
HTTP. Core dan notebook A--C cocok hash;2.584 file hasil penelitian tetap utuh.
Belum menjalankan training penuh tiga seed atau unduhan jaringan; kelulusan uji
ini bukan hasil variasi rute pada titik pengguna atau bukti konvergensi.
Audit: docs/temp/audit_uji_tiga_seed_20261103/AUDIT.md.

## Diagnosis service dan atribut kosong (3 November 2026)

Pengguna mencoba HIGHWAY_OTHER_SCORE=-2. Metadata uji tiga seed1279940429,
2839352981,2590398777 mencatat -2; ketiganya loop valid tetapi melewati tiga edge
way432851197 sepanjang637,15m. Q-table tersimpan pada keputusan masuk service
seed1279940429: Q(service)=35,1552; residential terbaik25,5148. Ini estimasi hasil
belajar, bukan bukti optimalitas. Replay memakai pemetaan metadata -2 cocok reward
akhir seluruh seed. Kontribusi ruas service -6,3715, arah +2,5214, gabungan -3,8501;
akses/revisit/terminal pada ketiga edge nol. Bonus sukses +100 pada akhir rute.

Detail penting yang perlu dipertahankan dalam pembahasan: add_comfort_scores
memakai np.clip(gabungan,-1,1). Highway -2 dengan surface/width kosong memberi
raw -1,10 tetapi skor akhir -1. Memberi skor -1 juga untuk atribut kosong tidak
menurunkan skor way tersebut lagi; uji counterfactual di memori membuktikannya.
Jangan menyarankan menurunkan skor lebih jauh tanpa mempertimbangkan clipping.
Data legal22.058edge: highway kosong0, surface kosong7.460, width tidak valid/
kosong7.856. Data kosong bukan bukti bahaya jalan; penalti ketidaklengkapan akan
mempengaruhi banyak alternatif. Tidak menerapkan penalti baru atau mengubah kode.

Saat audit, core di disk memiliki HIGHWAY_OTHER_SCORE=-1 dan hash berbeda dari
training -2; jangan menganggap file aktif identik konfigurasi hasil tersimpan.
Seluruh hasil/graf tetap. Tidak menjalankan training/unduhan. Audit rinci:
docs/temp/diagnosis_service_missing_20261103/audit.json.

## Comfort score tanpa pembatasan (3 November 2026)

Permintaan pengguna diterapkan: add_comfort_scores menyimpan float(gabungan)
langsung tanpa np.clip. Formula dan bobot H/S/W tetap0,55/0,30/0,15; parameter
pemetaan termasuk HIGHWAY_OTHER_SCORE tidak diubah oleh agent. Pengguna akan
mencoba nilai highway sendiri. Tidak menerapkan penalti untuk atribut kosong.

Rentang kini mengikuti nilai komponen, tidak dipaksa -1..1. Skor -1,10/-1,55
atau +1,55 diteruskan apa adanya ke action/reward dan mean_comfort. Nama API dan
atribut legacy tetap. Metadata baru reward_scheme=direct_signed_unclipped_20261103,
comfort_score_range=null (tidak ada batas tetap), comfort_score_clipped=false,
comfort_score_policy=weighted_sum_without_clipping. Metadata/hasil lama tetap.

analisa.ipynb memeriksa rumus gabungan alih-alih batas tetap; histogram interval
0,10 mengikuti min/max data termasuk kasus semua skor sama. Peta memakai kategori
ujung terbuka agar skor di luar rentang lama tidak salah label. Deskripsi dan
tooltip notebook A--C/uji/verifikasi disinkronkan. Hanya cell kode skor/distribusi/
peta analisis dan label pratinjau uji berubah; konfigurasi/koordinat/seed/worker/
reward lain/mask/Q/unduhan tetap. Output pada cell kode yang diedit dibersihkan.

Uji terkontrol: nilai di bawah -1 dan di atas +1, propagasi ke reward, metadata,
histogram dan kategori peta lulus. Regresi60episode sintetis A--C/dua seed pada
nilai default menghasilkan Q/history identik sebelum/sesudah. Satu eksperimen
sintetis tiga episode memeriksa metadata; tidak ada training panjang/unduhan.
Graf serta semua hasil tersimpan tetap (lihat audit). Hasil training lama tidak
dihitung ulang otomatis. Untuk uji titik, simpan perubahan core lalu jalankan
cell training/hasil; reload core dan rescore G sudah otomatis, tanpa unduh ulang.
Perubahan source notebook/label perlu muat ulang dari disk. Verifikasi manual
masih memuat expected untuk nilai default; penyesuaian parameter eksperimen
memerlukan peninjauan angka manual, bukan menganggap contoh lama berlaku.
Audit: docs/temp/audit_comfort_unclipped_20261103/AUDIT.md.


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


## Penalti data kosong -0,5 setelah checkpoint (3 November 2026)

Baseline telah di-commit sebagai70b1a08 SEBELUM perubahan missing. Sesudahnya,
HIGHWAY_MISSING_SCORE, SURFACE_MISSING_SCORE dan WIDTH_MISSING_SCORE menjadi-0,5.
HIGHWAY_OTHER_SCORE tetap sesuai file sebelum perubahan (saat itu-1); pengguna
mengujinya sendiri. Kategori terisi yang tidak dikenal tetap OTHER; width kosong,
invalid, tidak positif atau gabungan memakai missing-0,5. Tidak ada blacklist
service/TPU atau perubahan access. Ini preferensi kelengkapan informasi, bukan
kesimpulan bahwa tag kosong berarti jalan berbahaya. Tujuannya percobaan;
belum membuktikan penurunan penggunaan service pada hasil training pengguna.

Formula/bobot tetap0,55/0,30/0,15 dan tanpa clipping. Contoh semua atribut kosong
memberi B=-0,5; service default-1 dengan surface/width kosong B=-0,775; highway-2
pada kondisi sama memberi B=-1,325. Reward ruas tetap B*panjang/100. Metadata baru
reward_scheme=direct_signed_unclipped_missing_05_20261103; pemetaan H/S/W merekam
missing-0,5. Reward akses/arah/revisit/terminal, state, mask, Q, episode/epsilon,
seed/worker dan koordinat tidak diubah. Core bersama menerapkan aturan ke semua
notebook. A--C memakai grup baru reward_missing_05_20261103 untuk melindungi arsip;
uji titik tetap menimpa batch training terbaru tanpa mengunduh ulang G.

Notebook verifikasi:32cell kode lulus pada kernel bersih, expected literal untuk
kasus kosong/invalid/gabungan disesuaikan, termasuk empat contoh atribut parsial.
Pemeriksaan tambahan: missing semua memberi reward ruas-0,5 per100m dan Q pertama
-0,075 (alpha0,15, bootstrap0); highway-2 memberi-1,325 tanpa clipping. Semua
parameter modul selain tiga konstanta missing identik sebelum/sesudah.2.599file
hasil/graf tetap utuh. Tidak menjalankan training panjang/unduhan. Output analisis
skor lama dibersihkan agar tidak menjadi bukti aturan baru; jalankan ulang analisis
untuk tampilan terbaru. Notebook verifikasi menyimpan output kernel yang lulus.

Perubahan missing ini BELUM di-commit (terpisah dari baseline sesuai urutan
permintaan). Untuk mencoba, muat ulang notebook dari disk dan jalankan konfigurasi
agar grup baru terbaca. Uji titik dengan G yang sudah dimuat cukup konfigurasi,
training dan hasil. Gunakan tuple tiga seed yang sama untuk membandingkan reward.
Audit: docs/temp/audit_missing_reward_20261103/AUDIT.md.


## Koreksi grup hasil B agar sama dengan A/C (3 November 2026)

Pengguna meminta menyamakan folder lalu akan training ulang. RESULT_GROUP pada
cell muat graf scenario_B.ipynb dikoreksi dari reward_revisit_10_overlap_count_20261103
ke reward_missing_05_20261103, sama dengan A/C. Empat cell training, empat cell
hasil dan ringkasan memakai variabel yang sama. Output/nomor eksekusi B dibersihkan
agar hasil dari folder lama tidak tampak sebagai hasil grup baru. Deskripsi aktif
A/B/C juga diperjelas karena sebelumnya masih menyebut grup -10 di beberapa bagian.
Core/reward/parameter/seed/worker/koordinat tetap; tidak memindah, menghapus atau
menyalin artefak training. Hasil B missing-0,5 yang terlanjur tersimpan di folder
lama tetap di sana. Pengguna akan menjalankan ulang B ke folder baru; agent tidak
melatih ulang. Sebelum training, muat ulang notebook dari disk dan WAJIB jalankan
cell muat graf/config agar variabel RESULT_GROUP pada kernel diperbarui; pastikan
output Grup hasil: reward_missing_05_20261103. A/C tidak perlu training ulang hanya
karena koreksi nama grup B. Penilaian Bab IV menyeluruh dilanjutkan setelah hasil
training yang hendak dipakai pengguna tersedia pada grup yang konsisten.


## Audit missing -0,5 lengkap (4 November 2026)

Semua12konfigurasi kini berada pada reward_missing_05_20261103 termasuk B yang
sudah dilatih ulang.60training/6.750.000history; seluruh60greedy direproduksi,
metrik/path dan overlap geometri cocok. Metadata sama: missing-0,5/highwayother-1,
tanpa clipping/revisit-10/lima seed/tiga worker.240file sumber dan graf tetap.
Loop A/B/C: dinamis75K0/0/1; dinamis150K0/3/1; horizon50K total75K0/2/5;
horizon50K total150K2/4/5. Total23/60: A2,B9,C12.37gagal=29overdistance+8buntu,
semua tidak pernah memiliki closing action legal. C horizon75K kandidat:5/5,
galat141,57m/overlap1,15%; C horizon150K5/5 tetapi galat276,57m/overlap1,22%.
B dinamis150K3/5 melampaui C1/5; jangan mengklaim C selalu unggul/optimal.
Seluruh23loop utama tanpa service tetapi masih permissive/data kosong. Uji titik
lain terpisah3/3loop,2rute masih memakai637,15m service. Bukti lapangan/UI belum
ditinjau.32cell verifikasi tersimpan tanpa error. Bahan eksperimen cukup untuk
mulai BabIV; lanjutkan pembahasan state/epsilon/seed/kegagalan, sinkronisasi naskah,
validasi lapangan dan katalog. Naskah lama masih skor0-1/netral0,50/hasil30-75K;
Word tidak diubah. Tanpa training/unduhan baru atau perubahan raw data.
Laporan/CSV/grafik: docs/temp/analisis_missing_05_20261104/ANALISIS.md.


## Bahan revisi naskah Bab I sampai III pada 4 November 2026

Pemeriksaan naskah utama terhadap core aktif dan panduan kampus menghasilkan
docs/temp/revisi_bab_1_3_20261104/REVISI_BAB_1_3_TERBARU.docx; lampiran kode
PlantUML, sumber rumus, dan ZIP disimpan permanen di docs/assets/. Panduan berisi lokasi penggantian, alasan, teks siap
salin, tabel skor/akses/reward/konfigurasi/metrik, dan koreksi alat yang berulang.
Rumusan masalah dan tujuan tetap. Empat konfigurasi 75K/150K dinamis dan horizon
50K tetap menjadi acuan, dengan lima seed per konfigurasi pada A–C.

Dokumen mengikuti implementasi yang telah dilatih: missing -0,5, revisit -10,
skor langsung tanpa clipping, akses whitelist yes/permissive/kosong, arah 0,60,
sukses +100 dan kegagalan -50. Diskusi pelonggaran missing/revisit belum menjadi
keputusan perubahan; panduan memberi catatan untuk ditinjau sebelum disalin.
Bagian verifikasi dan penulisan ulang Bab IV belum disusun dalam paket ini.
Naskah TA utama, core, notebook, graf dan hasil training tidak diubah.
