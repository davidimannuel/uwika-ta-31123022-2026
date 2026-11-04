# Log Kemajuan Implementasi

Dokumen ini adalah handover singkat untuk sesi berikutnya atau agent lain. Detail teknis lengkap berada pada `IMPLEMENTASI.md`.

## Status terakhir

- Penalti aktif -10; MAX_WORKERS=3. A–C seluruh12 konfigurasi lengkap (60
  training/6.750.000 episode). Evaluasi greedy25/60 valid: A3, B11, C11.
- Seluruh60 evaluasi direproduksi; metrik/path/overlap cocok. Detail audit di bawah.
- -10 mengurangi overlap tetapi B/C turun35/40 pada -5 ke22/40. Jangan menaikkan
  penalti lagi dahulu; kode tetap -10 sesuai instruksi terakhir, bukan otomatis revert.
- Grup reward_revisit_10_overlap_count_20261103. Tidak ada training/unduhan oleh
  agent pada audit ini. Hasil -5/-3/-1 tetap arsip pembanding.


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

## Penalti -10 dan tiga worker (3 November 2026)

- Konstanta core -5 ke -10, seluruh notebook A--C MAX_WORKERS=3 dan grup baru.
  Output lama notebook dibersihkan; hasil mentah -5/-3 tidak ditimpa.
- Verifikasi literal diperbarui -10, contoh total +1+0,60-10=-8,40; 32 cell
  dijalankan ulang dan lulus pada kernel bersih. Uji Jupyter tiga worker/lima seed
  cocok mode berurutan dan metadata -10/workers3. Tidak ada dependensi baru.
- Dokumentasi aktif disinkronkan, audit pada
  docs/temp/verifikasi_revisit10_workers3_20261103/. Tanpa training penelitian,
  unduhan atau perubahan naskah TA. Reload notebook dari disk dan restart kernel
  sebelum training agar grup hasil dan MAX_WORKERS di kernel ikut berubah.

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

## Penalti -5 dan training seed paralel (3 November 2026)

- Pengguna meminta -5 serta percepatan antar-seed. Core berubah -3 ke -5,
  komponen reward lain/mask/state/epsilon/seed/Q tetap. A--C pindah grup
  reward_revisit_5_overlap_count_20261103 dan output lama dibersihkan. Hasil
  -3 dan seluruh arsip mentah tidak ditimpa; training penelitian -5 belum ada.
- max_workers ditambahkan ke run_scenario_experiment, default 1. Notebook
  A--C MAX_WORKERS=2, memakai multiprocessing spawn; Q/environment/RNG mandiri.
  Worker training/evaluasi saja, induk menyimpan hasil/plot. Urutan akhir seeds
  masukan tetap, meskipun penyelesaian task tidak berurutan. Parameter runtime
  induk disalin ke worker; data graf induk dipakai kembali pada environment hasil.
- Verifikasi 32 cell lulus: penalti literal -5, contoh total -3,40. Uji sintetis
  18 kombinasi cocok core sebelum paralel (penalti disamakan -5); parity hasil
  lengkap dua epsilon/seed tidak berurutan, A/B/C, snapshot runtime, error worker
  dan validasi worker lulus. OSM nyata (35 episode/dua seed) Q/history/metrik/rute
  identik 1 vs 2 proses. Uji dari kernel Jupyter bersih dengan reload modul lulus.
- README/AGENTS/IMPLEMENTASI dan rencana verifikasi disinkronkan. Tanpa dependensi
  baru, training penelitian, unduhan atau perubahan naskah TA. Kecepatan training
  penuh belum diukur; RAM bertambah. Audit docs/temp/verifikasi_revisit5_paralel_20261103/.

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

## Eksperimen penalti revisit -3 (3 November 2026)

- Pengguna menyetujui -3 menggantikan -1 per kunjungan ulang node non-start.
  Hanya konstanta reward yang berubah; mask, komponen reward lain, Q, seed,
  epsilon dan empat konfigurasi tetap. Berlaku pada core bersama A/B/C dan uji titik.
- A--C disiapkan pada RESULT_GROUP=reward_revisit_3_overlap_count_20261103.
  Output lama notebook dibersihkan; folder -1 reward_direct_overlap_count_20261103
  serta seluruh artefak penelitian lama tetap sebagai pembanding, tidak ditimpa.
- Expected literal verifikasi diperbarui: ruas +1, arah +0,60, revisit -3,
  total -1,40. Seluruh 32 cell kode verifikasi lulus pada kernel bersih.
  Core dibandingkan dengan salinan sebelum perubahan: hanya konstanta -1 ke -3.
  Sumber cell training/seed/episode tetap; 1.982 berkas hasil lama tidak berubah.
- Tidak menjalankan training penelitian atau unduhan. Eksperimen -3 belum punya
  hasil; angka audit di bawah adalah reward lama -1. Restart kernel dan jalankan
  cell muat graf sebelum training agar core dan RESULT_GROUP yang baru terbaca.
- Node revisit berbeda dari overlap ruas fisik. Nilai -3 adalah asumsi awal untuk
  mengurangi preferensi revisit, bukan jaminan overlap turun atau nilai optimal.

## Pengamatan empat konfigurasi B dengan overlap hitungan (3 November 2026)

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

## Pengamatan B epsilon dinamis dengan overlap hitungan (3 November 2026)

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

## Sinkronisasi penjelasan identitas ruas overlap (3 November 2026)

- IMPLEMENTASI memuat asal fungsi Shapely, nilai WKB/hex, alasan normalisasi,
  penanganan geometri absen serta contoh edge paralel nyata. AGENTS mencatat
  keputusan agar sesi selanjutnya konsisten. Shapely sudah dependensi sejak uv,
  bukan instalasi baru. pyproject/uv.lock tidak berubah.
- physical_road_id untuk pengamatan dipisahkan dari ID action (next_node,key).
  Identitas sama pada bentuk persis sama termasuk arah balik, meskipun key beda;
  bentuk berbeda tetap dipisah. Fallback garis endpoint memiliki keterbatasan
  untuk paralel yang geometry-nya tidak tersedia, dijelaskan secara eksplisit.
- Rumus aktif hitungan (N_total-N_unik)/N_total; satu grafik seluruh episode.
  Contoh B arsip: 12/45=26,67%; angka 26,43% di laporan lama berbasis meter.
- Pengguna memilih mencoba B terlebih dahulu. Hasil training count belum dianalisis
  dalam pekerjaan dokumentasi ini. Core, notebook, reward, mask dan hasil tidak
  diubah; tidak ada training atau pengunduhan baru.

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

## Analisis hasil reward langsung A--C (3 November 2026)

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

## Peta atribut pada pratinjau uji titik (3 November 2026)

- Pengguna meminta peta marker start menjadi seperti Peta Interaktif Atribut Jalan
  dan Akses, tanpa smoothness. Cell peta uji titik kini radio Highway/Surface,
  overlay Access per kategori dan legenda dinamis. Highway default; overlay akses
  serta ruas awal legal awalnya tidak aktif. Input biru/START hijau/snap tetap.
- Seluruh graf tampil termasuk access non-whitelist. Tooltip memuat atribut/reward
  dasar, marker midpoint pada CRS meter; arah identik digabung, key paralel terpisah.
  Popup memuat identitas/whitelist; marker bukan posisi pasti pagar.
- Hanya notebook uji titik dan dokumentasi berubah. Core/reward/mask/seed/A--C/
  analisis/verifikasi/koordinat/unduh dan training tidak diubah. Peta membaca G,
  menimpa HTML seperti sebelumnya; tidak mengunduh atau menjalankan training.
- Pemeriksaan lulus: schema/sintaks notebook; cell selain peta/deskripsinya
  identik; graf sintetis menguji atribut kosong/gabungan/unknown, midpoint,
  whitelist, deduplikasi dua arah dan key paralel. Core/analisa/verifikasi identik.
- Graf uji lokal 8.284 node/22.136 edge berhasil dipetakan ke kedua tema.
  Access: destination 27 marker/54 edge, no 12/24, permissive 198/396, yes 93/186.
  Browser Chrome menguji radio, overlay akses/ruas legal dan legenda dinamis,
  START tetap ada, tidak ada smoothness atau error JavaScript. Screenshot diperiksa.
  Tidak ada unduhan graf/training baru; GraphML lokal tetap identik.

## Reward langsung diterapkan ke seluruh notebook rute (3 November 2026)

- Permintaan pengguna mengaktifkan implementasi seluruh kesepakatan ke notebook.
  HIGHWAY_PRIORITY satu kelompok footway/pedestrian/living_street/residential/
  tertiary; H/S/W +1/-1/0; width >=3 m; bobot tetap 0,55/0,30/0,15.
- Core reward ruas langsung B*L/100, tanpa pengurangan 0,50 dan clip 0--1.
  Gabungan bertanda -1..1. Nama legacy comfort_score/mean_comfort tetap dengan
  makna baru; metadata versi/formula/bobot/rentang menjelaskan perubahan.
- Akses/mask/state/epsilon/seed/Q tetap. Arah 0,60, revisit -1, sukses +100,
  gagal -50 seperti keputusan sebelumnya. Graf sumber dan hasil lama tidak ditimpa.
- Analisis histogram/peta memuat negatif/netral/positif dan memakai perhitungan
  gabungan core; 21 cell kode dijalankan ulang. Verifikasi expected diperbarui
  independen, termasuk access, manual Q nonnol/terminal; 31 cell kode lulus.
- A--C menyiapkan RESULT_GROUP=reward_direct_20261103 dan membersihkan output
  arsip dari notebook. Empat konfigurasi/lima seed tetap; belum training panjang.
- Uji titik reload core dan skor G sebelum training tanpa unduh/load graf ulang.
  Koordinat pengguna/overwrite terbaru tetap. Notebook basic Q/RNG adalah contoh
  umum terpisah, tidak memiliki reward rute sehingga tidak diubah reward toy-nya.
- Pengujian lulus: 27 kombinasi H/S/W dan 17 variasi tag/batas; 21.300 action
  utama identik dengan sebelum perubahan. A/B/C diuji dua episode per lima seed
  pada graf sintetis di /private/tmp, termasuk rute dengan mean_comfort=-1 dan
  grafik/tampilan hasil. Metadata baru benar; loader tetap membaca arsip lima seed.
- Uji titik dua kali training satu seed mengganti hasil lama tanpa unduh/load
  graf ulang, termasuk setelah core reload. Snapshot utama byte-identik.
  Tidak ada training penelitian atau unduhan live baru untuk perubahan ini.

## Bonus sukses +100 dan penalti gagal seragam -50 (3 November 2026)

- Pengguna meminta menerapkan bonus sukses +100 dan satu penalti gagal -50.
  SUCCESS_BONUS 80 -> 100, NO_ACTION_PENALTY -45 -> -50,
  STEP_LIMIT_PENALTY -40 -> -50; OVER_DISTANCE_PENALTY tetap -50.
- Rumus komponen, urutan terminasi, mask, fase, revisit -1, arah 0,60, akses,
  state, epsilon dan seed tetap. Metadata baru mencatat terminal_rewards.
- H/S/W langsung +1/-1/0 dan satu prioritas highway masih belum diterapkan.
  Tidak mengubah data/graf/notebook/hasil lama atau menjalankan training penelitian.
  Komponen utama reward sudah dibahas; integrasi rancangan langsung belum selesai.
- Dasar skala terminal di wiki dibedakan dari kode aktif: bonus dua kali reward
  ruas ideal 5 km dan kegagalan satu kali mengacu rancangan langsung, bukan hasil
  optimasi; kode aktif masih skor 0--1 dan titik netral 0,50.
- Pemeriksaan 60 kasus A--C/akses lulus: sukses inklusif 4.500/5.500 m, sukses
  pada langkah 220, prioritas over_distance atas step_limit, batas 5.500 m di
  non-start belum over_distance, buntu sebelum/sesudah langkah, penalti sekali
  dan terminal tanpa bootstrap Q. Metadata dari dua episode sintetis tersimpan
  di /private/tmp terverifikasi. AST memastikan hanya konstanta/metadata berubah.

## Penalti revisit -1 (3 November 2026)

- Pengguna meminta menerapkan usulan penalti revisit -1 per kejadian, menggantikan
  -8. Perubahan hanya konstanta REVISIT_PENALTY dan pencatatan revisit_penalty pada
  metadata run baru. Arah tetap 0,60 pada kedua fase; terminal tidak diubah.
- Aturan kunjungan tetap: sebelum 2.500 m dilarang, setelahnya maksimum dua
  kunjungan per node. Penalti berlaku pada node non-start; closing loop ke start
  tetap dikecualikan. Penalti tidak dikalikan panjang ruas.
- H/S/W langsung +1/-1/0 dan satu prioritas highway masih rancangan chat,
  belum diterapkan. Kode aktif tetap skor 0--1 dan pengurangan 0,50.
- Tidak mengubah notebook/graf/hasil lama atau menjalankan training penelitian.
  Notebook verifikasi masih ditunda. Pemeriksaan 36 kasus A--C/akses lulus:
  penalti pada revisit termasuk key paralel, node baru/start tanpa penalti,
  larangan sebelum 2.500 m dan setelah dua kunjungan, serta hitungan Q.
  Metadata dari dua episode sintetis terverifikasi di /private/tmp. AST hanya
  berubah pada konstanta dan field metadata, bukan algoritma atau mask.

## Koefisien arah 0,60 pada kedua fase (3 November 2026)

- Pengguna meminta implementasi 0,60 juga untuk penalti arah fase awal, setelah
  menyetujui 0,60 fase pulang. RETURN_REWARD_SCALE dan OUTWARD_PENALTY_SCALE
  diubah dari 0,40 ke 0,60; rumus/cabang/ambang 2.500 m tetap.
- Metadata run baru mencatat dua koefisien dan rasio fase pada direction_reward.
  Tidak menulis ulang graf/hasil lama atau menjalankan training penelitian.
- Kesepakatan H/S/W reward langsung +1/-1/0 dan satu prioritas highway belum
  diterapkan. Kode masih skor 0--1, bobot 0,55/0,30/0,15 dan pengurangan 0,50.
  Akses tetap permissive -0,10 per 100 m. Revisit/terminal dibahas berikutnya.
- Dokumentasi membedakan status kode dan rancangan serta memperbarui analisis
  skala arah; angka desain tidak diklaim optimal atau menjamin semua sukses
  lebih tinggi dari seluruh kegagalan. Notebook verifikasi tetap ditunda.
- Pemeriksaan lulus: 54 kombinasi A--C/akses/fase/terminal, termasuk ruas yang
  melintasi ambang 2.500 m, arah tidak ditambahkan pada terminal langsung, dan
  hitungan Q dengan next Q nonnol. Metadata 0,60/0,60/0,50 terverifikasi dari
  run sintetis dua episode pada /private/tmp. Analisis AST memastikan perubahan
  kode hanya dua konstanta dan metadata; source notebook serta graf tetap.

## Uji titik selalu menimpa, training tidak mengunduh ulang (2 November 2026)

- Pengguna menolak FileExistsError pada percobaan uji titik. Kebijakan proteksi
  RUN_LABEL/hasil lama pada entri sebelumnya digantikan oleh alur ini.
- Satu folder tetap uji_titik_start/terbaru/: cell unduh selalu bypass GraphML/
  cache HTTP dan menimpa graf/metadata. Setelah sukses, hasil training lama
  dibuang; cell peta memperbarui marker/HTML. Nama run dan mode cache dihapus.
- Mengulang cell training memakai G dalam memori, tanpa unduhan/load graf.
  Hanya training/ dibersihkan agar file seed/konfigurasi lama tidak tertinggal;
  graf, metadata graf dan peta marker tetap. Setiap training dari Q-table kosong,
  satu seed acak aktual dicatat; angka seed tetap bisa diisi untuk pengulangan.
- Perubahan input/radius/konfigurasi dan kegagalan unduhan membatalkan konteks
  terkait; hasil titik lama tidak boleh tampil sebagai hasil titik baru.
- Koordinat pengguna dipertahankan. Core, A--C, verifikasi, graf utama dan hasil
  penelitian tidak diubah. Folder uji lama tetap, tidak digunakan sebagai cache.
  Tidak menjalankan unduhan live atau training panjang untuk perubahan workflow.
- Pemeriksaan lulus: tiga permintaan unduh baru terkontrol, empat training pendek
  masing-masing dua episode, timpa seed/konfigurasi tanpa sisa file, metadata,
  tampilan tanpa training, marker titik baru, penghapusan hasil graf lama dan
  kegagalan unduhan yang tidak memakai konteks lama. Training ulang tidak
  memanggil unduh/load graf; graf/metadata/peta marker byte dan mtime tetap.
  Core, source A--C/verifikasi serta snapshot utama tetap; Jupyter dapat menyimpan
  metadata/output notebook A--C yang terbuka selama pemeriksaan.
  Seluruh artefak pemeriksaan ada di /private/tmp, bukan hasil penelitian.

## Koreksi: service hanya turun skor (2 November 2026)

- Pengguna mengklarifikasi bahwa exclude berarti keluar dari HIGHWAY_PRIORITY_2,
  bukan melarang action. Service kini HIGHWAY_OTHER_SCORE=0,20, termasuk pada
  aturan minimum gabungan. Empat anggota prioritas kedua lain tetap 0,60.
- Seluruh tambahan filter highway/metadata larangan dibatalkan. build_actions,
  aturan mask, Q/state/epsilon/seed tetap seperti sebelum salah tafsir. Whitelist
  access dan penalti permissive yang sudah disetujui tetap berlaku.
- Notebook A--C, RESULT_GROUP dan output dikembalikan utuh dari salinan sebelum
  salah tafsir. Uji titik/verifikasi/graf/hasil mentah tidak diubah. Grup baru tidak
  dipilih otomatis. Untuk training ulang gunakan grup baru agar arsip lama aman.
- Hasil lama memakai service 0,60; bukan hasil reward service 0,20. Analisis hanya
  diperbarui keterangannya; output lama belum dihitung ulang. Tidak ada training
  penelitian baru yang dijalankan agent.
- Pemeriksaan lulus: service tunggal/gabungan bernilai 0,20, enam kasus reward/Q/
  closing pada A--C dan pemilihan eksplorasi/greedy tetap menerima service.
  Action persis kembali seperti sebelum salah tafsir: 21.300 pada graf utama,
  22.058 pada graf uji. Seluruh fungsi/class core kembali identik; hanya anggota
  prioritas highway berubah. Notebook/grup/output A--C pulih byte-identik.

## Whitelist access menggantikan blacklist (2 November 2026)

- Pengguna meminta daftar izin yang lebih singkat. ACCESS_WHITELIST hanya
  yes/permissive; tag kosong tetap diizinkan. Nilai terisi lain/tidak dikenal
  ditolak. Pada gabungan seluruh komponen harus diizinkan, tanpa override foot.
- ACCESS_BLACKLIST dihapus dari core; metadata run baru merekam whitelist,
  kebijakan tag kosong dan aturan gabungan. Penalti permissive -0,10 per 100 m,
  skor H/S/W, state, Q, epsilon, seed dan notebook A--C tetap.
- Snapshot utama tetap 21.300 action dan graf uji terbaru tetap 22.058 action,
  identik dengan filter lama karena kategori yang muncul hanya kosong/yes/
  permissive/destination/no. Nilai unknown/variable/lain pada lokasi baru kini
  dikeluarkan; tidak mengklaim semua graf atau data masa depan ekuivalen.
- Grup/hasil training lama tidak diubah; metadata blacklist lama tetap historis.
  Tidak mengganti RESULT_GROUP A--C untuk perubahan yang tidak mengubah action
  pada snapshot ini. Notebook analisis hanya disesuaikan keterangannya.
- Pemeriksaan lulus: 40 variasi tag, edge paralel, action manual ilegal,
  closing, metadata whitelist dan enam kasus reward/bootstrap Q legal pada A--C.
  Dua graf dibandingkan sampai identitas action: tidak ada action yang berubah.
  Algoritma, seed, notebook A--C/verifikasi/uji titik dan graf utama tidak berubah
  pada revisi ini. Uji pendek hanya di /private/tmp; tidak ada training penelitian baru.

## Koreksi uji titik: unduhan baru dan satu training acak (2 November 2026)

- Pengguna meminta uji lokasi memakai unduhan map baru dan tidak dipaksakan lima
  seed. Versi snapshot-only di catatan berikut adalah riwayat yang digantikan.
- Notebook kini DOWNLOAD_NEW_GRAPH=True: unduh walk graph sekitar koordinat
  pengguna dengan bbox radius default 3.025 m, force_download dan use_cache=False.
  File graf baru/metadata unduhan disimpan per nama titik/RUN_LABEL; bukan graf utama.
- Satu training dengan RANDOM_SEED=None -> secrets.randbits(32), dicetak dan
  disimpan. Seeds lima run tetap khusus A--C. Default B 150k/horizon 50k tetap;
  koordinat yang sudah diubah pengguna di notebook dipertahankan.
- Core loader menerima pusat/path/radius/cache khusus dengan default lama tetap.
  run_scenario_experiment menerima seeds opsional; None tetap lima seed penelitian.
  Tampilan diagnosis menghitung jumlah seed aktual, tidak hardcode lima.
- Reload graf run memakai metadata pusat/radius/hash. Graf run dengan hasil tidak
  ditimpa; cell hasil dapat dibuka tanpa training. Algoritma reward/Q/mask tetap.
- Pemeriksaan terkontrol lulus: loader pusat khusus/bypass/reload/pemulihan cache,
  default snapshot lama, satu seed acak tercatat, metadata/display satu run,
  perlindungan hasil/graf, mismatch koordinat, default lima seed dan invalid seed.
  Training uji pendek dua episode per seed hanya di /private/tmp.
- Unduhan OSM langsung berhasil pada koordinat pengguna (-7.281521,112.710178),
  tanpa cache HTTP: 8,284 node dan 22,136 edge terarah. Graf/metadatanya di
  hasil_bab_4/training_qlearning_5km/uji_titik_start/titik_01/uji_01/.
  Cell unduhan dan peta memiliki output; cell training produksi tetap belum
  dijalankan. Pemeriksaan terkontrol tidak dipakai sebagai pengganti bukti live.
- Tidak ada training panjang pada lokasi baru yang dijalankan agent.

## Notebook uji titik start (2 November 2026)

- Permintaan pengguna: notebook khusus untuk mencari start dari lat/long,
  menampilkan marker, lalu training dan menampilkan metrik serta peta rute.
- Dibuat uji_titik_start.ipynb (14 cell). Default contoh dari note.txt,
  node terdekat 1720975893 dengan pergeseran 40,08 m. Marker input dan node START
  dibedakan; ruas awal legal memakai aturan core.
- Snapshot lokal tetap; tidak mengubah start core/A--C atau mengunduh area baru.
  Titik di luar cakupan/snap >100 m default/tanpa action legal dicegah training.
- Default B 150k horizon 50k, lima seed. C 75k dinamis disediakan sebagai alternatif
  melalui parameter. Hasil terpisah menurut nama titik/node/konfigurasi/RUN_LABEL;
  file hasil lama tidak ditimpa. Metadata input/node/hash graf/core disimpan.
- Tampilan hasil memakai helper core tanpa training. Koordinat atau konfigurasi
  berubah perlu cell pencarian/peta/konfigurasi diulang.
- Semua cell pencarian dan peta telah dieksekusi; cell training produksi belum.
  Uji alur dua episode satu seed dilakukan pada /private/tmp saja. Pencocokan,
  artefak/metadata, display tanpa training, penjagaan overwrite/stale input,
  cakupan/snap/koordinat invalid/node buntu lulus. Core, A--C, verifikasi dan
  GraphML tidak berubah. Tidak ada training penelitian baru yang dijalankan agent.
- Dokumentasi konteks/README diperbarui; belum ada commit baru untuk notebook ini.

## Sinkronisasi desain dan hasil terbaru (2 November 2026)

- Surface satu prioritas: asphalt/concrete/paving_stones/paved = 1,00;
  lainnya/tidak dikenal = 0,20; kosong = 0,50; gabungan minimum.
- Width ambang 3 m: >=3 m = 1,00; positif <3 m = 0,20;
  kosong/invalid/gabungan = 0,50. Normalisasi linear dihapus. Ini preferensi,
  bukan larangan ruas sempit atau standar kenyamanan lari.
- Highway dua prioritas, bobot H/S/W 0,55/0,30/0,15, akses -0,10 per 100 m,
  blacklist, mask, state, episode, epsilon dan seed tetap. Semua skor analisis
  memakai core. Peta atribut kini memiliki tema Surface dengan warna material,
  tooltip skor dan legenda yang berganti. Analisis/peta comfort sudah dijalankan ulang.
- Pemeriksaan saat implementasi: surface 24 variasi tag + 36 langkah reward/Q;
  width 31 variasi/batas + 36 langkah reward/Q; A--C, seluruh 21.374 edge,
  21.300 action tetap, GraphML tidak berubah. Ini bukan revisi verifikasi.ipynb.
- Pengguna menjalankan grup final surface_width_3m_20261102; seluruh metadata,
  manifest, 6.750.000 baris history dan epsilon cocok. Semua 60 evaluasi dari
  Q-table direproduksi dengan metrik/node/action yang sama; tidak training ulang.

| Strategi epsilon | Episode per seed | A | B | C |
|---|---:|---:|---:|---:|
| Dinamis | 75.000 | 0/5 | 0/5 | 5/5 |
| Dinamis | 150.000 | 0/5 | 0/5 | 5/5 |
| Horizon 50k | 75.000 | 1/5 | 1/5 | 5/5 |
| Horizon 50k | 150.000 | 0/5 | 5/5 | 5/5 |

- Total 27 loop valid dan 33 gagal (29 over_distance, 4 buntu). Semua kegagalan
  tidak pernah memiliki closing action legal. Ke-27 urutan edge valid berbeda,
  tetapi kemiripan geografis belum dianalisis. Semua masih mengandung ruas <3 m,
  width kosong dan permissive; belum ada validasi lapangan.
- Horizon 50k total 150k: B galat 268,47 m, skor 0,9034, Q-state 28.103,2;
  C galat 339,91 m, skor 0,9193, Q-state 46.671,6. C 5/5 pada semua konfigurasi;
  A sempat 1/5, sehingga tidak selalu gagal. Lima seed bukan jaminan generalisasi.
- Laporan/CSV/audit: docs/temp/analisis_surface_width_3m_20261102/.
- Kesepakatan verifikasi/validasi/practical implications/katalog disimpan pada
  docs/VERIFIKASI_VALIDASI_DAN_KATALOG.md; kandidat 26 sumber di referensi.md.
- Hitung manual tetap beberapa contoh representatif. Notebook verifikasi lama
  belum disesuaikan; pekerjaan lanjutan ditunda sampai pengguna meminta.
- Pembimbing menyarankan katalog rute tersimpan, bukan training melalui app.
  Field check memakai Huawei Watch Fit 3/Huawei Health; tidak wajib Strava.
  GPX, navigasi, aplikasi, katalog khusus dan pemeriksaan lapangan belum dibuat.
- Tidak mengubah core/notebook, data, atau 228 berkas training dalam sesi audit ini;
  dokumen TA utama tidak diedit. Angka/grup lama tetap sebagai arsip.

## Tertiary masuk Prioritas 2 (1 November 2026)

- Pengguna menilai tertiary masih dapat dipertimbangkan untuk rute lari.
  Tertiary dan tertiary_link dipindahkan ke HIGHWAY_PRIORITY_2, skor 0,60,
  berlaku pada seluruh A--C dan analisis melalui fungsi core bersama.
- Grup highway_dua_prioritas_20261101 belum memiliki hasil, sehingga namanya
  tetap. Tidak ada hasil training yang ditimpa atau training baru dijalankan.
- Pemeriksaan skor tunggal/gabungan/kosong serta enam langkah reward dan Q
  (dua jenis highway x A--C) lulus; git diff --check juga lulus.
- Penjelasan analisis/AGENTS/IMPLEMENTASI diselaraskan. Bobot, akses/blacklist,
  state dan parameter training tetap. Acuan verifikasi lama tetap ditunda.

## Dua prioritas highway diterapkan pada A--C (1 November 2026)

- Pengguna menyetujui priority 1 = 1,00 (footway, pedestrian, living_street,
  residential), priority 2 = 0,60 (path, service, unclassified), jenis lain
  termasuk tidak dikenal = 0,20, tag kosong = 0,50; gabungan memakai minimum.
- HIGHWAY_PRIORITY_1/2 dan empat konstanta skor berada di core. Fungsi
  calculate_highway_score() dipakai add_comfort_scores() untuk seluruh A--C.
- Cell highway/penjelasan analisa.ipynb memakai fungsi core yang sama, tanpa
  pemetaan skor terpisah. Helper surface dipertahankan. Output analisis dari
  cell highway ke bawah dikosongkan agar tidak menampilkan skor lama.
- Grup scenario menjadi highway_dua_prioritas_20261101; hasil lama tetap.
  Metadata menyimpan kelompok/skor/kebijakan gabungan. Notebook scenario
  dikosongkan outputnya. Tidak menjalankan training penelitian atau unduhan.
- Bobot comfort, surface/width, reward akses -0,10, blacklist aktif, state,
  seed, epsilon, jumlah episode dan start tetap. GraphML/verifikasi tidak diubah.
- Pemeriksaan lulus: 32 kasus tag/gabungan/kosong, 30 langkah reward/Q A--C,
  delapan cell analisis yang relevan, serta metadata A--C melalui dua episode
  sintetis per scenario (artefak hanya /private/tmp). Seluruh 21.374 edge cocok
  antara analisis dan core; surface/width tidak berubah, 21.300 action sama.
  Skor snapshot: 1,00 pada 14.174 edge; 0,60 pada 2.748; 0,20 pada 4.452.
  Hash GraphML tetap; sintaks notebook dan git diff --check lulus.

## Blacklist access aktif pada pilihan action (30 Oktober 2026)

- Pengguna meminta access yang masuk blacklist tidak dijadikan pilihan.
- build_actions() melewati edge bila salah satu nilai access masuk
  ACCESS_BLACKLIST. Mendukung kapital/spasi/list/string list/titik koma.
- Berlaku untuk semua A--C, fresh/revisit/closing, eksplorasi dan greedy.
  Edge paralel yang lolos tetap tersedia. Graf asli tidak diubah.
- Tidak memakai override foot: seluruh kategori blacklist dikeluarkan sebagai
  batasan penelitian yang diminta. Unknown/nilai baru/bersyarat di luar daftar
  belum ditangani lebih lanjut. Yes/kosong/permissive tetap dapat menjadi action.
- Penalti permissive tetap -0,10 per 100 m. Metadata menyimpan blacklist aktif,
  daftar kategori, dan kebijakannya. Tidak ada training penelitian dijalankan.
- Grup A--C menjadi reward_access_blacklist_010_20261030 agar tidak menimpa
  percobaan reward saja jika sudah dijalankan. Konfigurasi episode/epsilon/seed
  tetap. Perbedaan dengan baseline lama melibatkan reward serta pilihan action.
- Pemeriksaan lulus: 72 variasi tag, edge paralel, pemilihan eksplorasi/greedy,
  penolakan action manual, buntu/closing, dan Q berikutnya yang legal pada A--C.
  Snapshot mengecualikan 74 edge (destination 50, no 24), menyisakan 21.300
  action; tiga action keluar start tetap. Hash GraphML tidak berubah.
  Metadata/alur simpan diuji dengan satu seed dua episode graf sintetis,
  seluruh artefak uji hanya di /private/tmp; bukan training penelitian.
- Notebook analisis/verifikasi, GraphML, serta artefak hasil lama tidak diubah.

## Reward permissive -0,10 per 100 meter (30 Oktober 2026)

- Pengguna meminta mencoba penalti -0,10. Konstanta pada core adalah
  PERMISSIVE_PENALTY_PER_100M=-0.10; kontribusi dikalikan panjang edge/100.
- Komponen access dipisahkan dari comfort, tercatat pada step/train_step dan
  verbose termasuk persamaan total Q. Berlaku pula pada langkah terminal.
- Nilai gabungan yang mengandung permissive dikenai penalti seluruh panjang
  edge; ini pendekatan konservatif, bukan panjang pasti bagian way permissive.
- Blacklist tetap konfigurasi belum aktif. State, mask, comfort, parameter,
  start, dan snapshot graf tetap. Perubahan perilaku hanya komponen reward.
- Notebook A--C dipindah ke RESULT_GROUP=reward_access_010_20261030 agar hasil
  lama tidak tertimpa; empat konfigurasi dan lima seed tetap. Output notebook
  dikosongkan. Tidak ada training panjang atau hasil eksperimen baru.
- Metadata eksperimen berikutnya mencatat koefisien/aturan gabungan/blacklist.
- Pemeriksaan lulus: 105 kasus dibanding baseline (15 variasi tag x 7 kondisi),
  skala panjang, buntu tanpa action, verbose dan update Q; tiga action keluar
  start snapshot OSM tetap legal dengan selisih reward tepat sesuai panjang.
  Alur penyimpanan/metadata juga lulus pada graf sintetis satu seed dua episode,
  seluruh output uji berada di /private/tmp; bukan hasil eksperimen penelitian.
- Notebook verifikasi tetap ditunda/tidak diedit; acuan hitungan OSM lama
  perlu disesuaikan saat pengguna meminta melanjutkannya.

## Pemisahan variabel blacklist akses (30 Oktober 2026)

- Pengguna menyepakati destination dikeluarkan dan meminta variabel blacklist
  tersendiri sebelum membahas reward untuk kategori yang tersisa.
- `ACCESS_BLACKLIST` ditambahkan pada core sebagai frozenset sepuluh kategori:
  no, private, destination, customers, delivery, agricultural, forestry,
  military, permit, discouraged. Konstanta belum diterapkan pada penyaringan.
- Tidak ada perubahan fungsi core, graf, notebook, reward/mask, atau training.
  Reward yes/permissive/kosong dan aturan foot/nilai ambigu masih dibahas.
- Pemeriksaan sintaks dan AST memastikan satu-satunya perubahan kode adalah
  penambahan konstanta. Dokumentasi konteks diselaraskan.

## Pilihan layer Highway/Smoothness dan fokus access (30 Oktober 2026)

- Pengguna meminta smoothness sebagai pilihan layer pada peta yang sama;
  deskripsi/judul kini **Peta Interaktif Atribut Jalan dan Akses**.
- Highway aktif default. Smoothness bergantian melalui pilihan radio, bukan
  menumpuk warna. Marker access tersedia per kategori tetapi awalnya nonaktif.
  Basemap tetap tampil; legenda mengikuti tema dan status overlay access.
- Smoothness parsial/kosong/tidak dikenal/gabungan dibedakan pada peta; nilai
  asli dan cakupannya tetap pada tooltip. Tidak ada skor/reward tambahan.
- Cell peta berhasil dieksekusi. Default/cakupan/JavaScript diperiksa; interaksi
  nyata di Chrome lulus (tema, marker access, legenda, kembali ke Highway),
  tanpa error JavaScript. Screenshot diperiksa; output notebook/HTML diperbarui.
- Fokus berikutnya hanya access agar tidak menambah kompleksitas. Pengguna
  mengamati banyak permissive sekitar start; jenis akses dan pemilihan lokasi
  akan dibahas nanti. Reward/mask/graf/start/training belum diubah.

## Marker access pada peta jenis jalan (30 Oktober 2026)

- Pengguna meminta marker per jenis access pada peta highway analisa.ipynb.
  Cell peta/penjelasannya diperbarui; cell analisis lain tetap sama.
- Marker di tengah geometri meter, per kategori warna/ikon, layer toggle, legenda,
  dan popup rincian ruas/way/edge. Edge dua arah identik berbagi marker tanpa
  menggabungkan key paralel berbeda; bukan penanda lokasi pasti pintu/pagar.
- Hasil: 324 marker mewakili 648 edge (no 12/24, destination 25/50,
  permissive 195/390, yes 92/184). Output notebook dan HTML peta diperbarui.
- Cell diuji dengan persiapan notebook; jumlah/warna/layer/lokasi/cakupan HTML
  sesuai, termasuk access kosong/nilai lain. Graf/core/reward/training tetap.

## Integrasi smoothness/access ke seluruh analisis atribut (29 Oktober 2026)

- Pengguna menjelaskan kedua atribut harus masuk di tabel/diagram kelengkapan
  dan seluruh bagian analisis atribut terkait, bukan dua tambahan terpisah.
- Notebook 43 cell kini memakai satu tabel analisis lima atribut: highway,
  surface, width, smoothness, access. Sampel/kolom, kelengkapan, distribusi,
  diagram enam panel, kombinasi, serta tooltip peta sudah diselaraskan.
- Smoothness dari cache hanya dipakai untuk edge bila semua way asal ditemukan
  dan bertag; list kategori tetap dipertahankan. Nilai parsial/status tersimpan
  terpisah pada tabel analisis. Seluruh statistik utama memakai edge directed.
- Smoothness lengkap 13.938 edge (65,21%), parsial 216; access terisi 648 (3,03%).
  Cache cocok dengan 6.554 way asal unik. Tidak ada penambahan ke G/GraphML.
- Seluruh 21 cell kode berisi berjalan pada Python 3.13 dan output disimpan.
  Pemeriksaan konservasi jumlah/panjang/persentase, sumber/parsial, tooltip,
  cache hilang, dan kesamaan comfort score dengan core lulus. Diagram diperiksa visual.
- Reward/rumus/bobot/mask/core, GraphML, scenario A--C/verifikasi, dan hasil
  training tetap sama. Kandidat tag lain belum ditambahkan.

## Analisis hasil empat konfigurasi (29 Oktober 2026)

- Pengguna telah menjalankan semua A/B/C × empat konfigurasi × lima seed.
  Agent tidak melakukan training ulang. Sumber tunggal: grup konfigurasi_empat_20261029.
- Keberhasilan greedy A/B/C: dinamis 75k = 1/1/1 dari lima;
  dinamis 150k = 0/0/4; horizon 50k total 75k = 0/5/3;
  horizon 50k total 150k = 0/5/5.
- B 150k horizon 50k kandidat utama pada kriteria loop, galat, lalu karakter
  ruas: 5/5 sukses, galat rata-rata 104,28 m, skor ruas 0,762. C pada kondisi
  sama 5/5, galat 160,79 m, skor 0,726; C penyebaran galat lebih kecil.
  B 75k tetap alternatif anggaran lebih kecil dengan 5/5, galat 270,32 m.
- A berhasil sekali pada dinamis 75k; jangan menyatakan tidak pernah bisa.
  Pengaruh state bergantung epsilon/durasi; rumusan masalah tidak berubah.
- Seluruh metadata/artefak, urutan seed/episode dan jadwal epsilon sesuai.
  Agent mengevaluasi ulang 60 Q-table; seluruh metrik dan rute identik.
  Prefix 75k horizon 50k identik pada 15 pasangan seed durasi 75k/150k.
- Seluruh 35 kegagalan evaluasi tidak memiliki closing action tersedia:
  29 over_distance, 6 no_available_action, tanpa step_limit.
- Analisis lengkap beserta CSV/grafik/pemeriksaan disimpan pada
  `docs/temp/analisis_empat_konfigurasi_20261029/ANALISIS.md`.
  Lima seed belum membuktikan generalisasi atau optimalitas; belum validasi lapangan.
- Core, snapshot, notebook, dan artefak mentah tidak diubah; verifikasi/reward/
  GPX tetap ditunda. Ringkasan hasil lama di bawah merupakan arsip dan tidak
  menggantikan hasil empat konfigurasi yang baru diperiksa.

## Empat konfigurasi berpasangan (29 Oktober 2026)

- Pengguna menyepakati dinamis 75k/150k dan horizon epsilon 50k pada 75k/150k.
  Total 50k dan 100k dihapus dari notebook aktif; dinamis 150k ditambahkan.
- A/B/C tetap dipertahankan, lima seed per konfigurasi. Rumusan masalah tidak diubah.
  Jumlahnya 60 training/6.750.000 episode untuk seluruh scenario.
- Cell training/tampilan dan kedua ringkasan disesuaikan. Hasil baru memakai
  RESULT_GROUP `konfigurasi_empat_20261029`; seluruh hasil sebelumnya tetap disimpan.
- Agent belum menjalankan training panjang; pengguna akan menjalankan dan melihat
  hasil. Core dan notebook verifikasi yang sedang ditunda tidak diubah.
- Pemeriksaan nbformat/sintaks dan uji alur A/B/C lulus: tepat empat training,
  empat pasangan tampilan, dan dua ringkasan berisi titik 75k/150k. Grafik diuji
  dengan data uji di memori, tanpa hasil riset baru. Horizon epsilon dikonfirmasi
  memakai fungsi produksi. Tidak ada training panjang yang dijalankan.

## Penyederhanaan menjadi lima konfigurasi (29 Oktober 2026)

- Notebook A--C kini memiliki lima cell training: 50k bersama, 75k dinamis,
  dan 75k/100k/150k dengan horizon epsilon 50k. Training 30k/40k dan duplikat 50k dihapus.
- Acuan 50k dipakai kedua ringkasan; cell tampilan hasil tetap terpisah dari training.
  Seluruh output lama notebook dibersihkan untuk menghindari hasil tertukar.
- Hasil run berikutnya memakai RESULT_GROUP `konfigurasi_lima_20261029`, terpisah
  dari artefak lama. Gunakan nama grup yang sama di A/B/C.
- Agent tidak menjalankan training panjang. Pengguna akan menjalankan notebook
  untuk melihat hasil; core dan verifikasi yang sedang ditunda tidak diubah.
- Pemeriksaan: nbformat/sintaks seluruh cell A/B/C valid; uji alur dengan training
  pengganti memastikan tepat lima konfigurasi dan lima pasangan tampilan. Dua
  ringkasan/grafik diuji memakai CSV arsip sebagai referensi sementara, tanpa
  menulis hasil baru. Acuan 50k terbukti berasal dari satu folder pada kedua ringkasan.

## Sinkronisasi konteks dan penundaan verifikasi (29 Oktober 2026)

- AGENTS.md dan IMPLEMENTASI.md diselaraskan dengan notebook 47 cell/31 cell kode
  yang telah dijalankan, cakupan poin 1–5, batas klaim, dan catatan stres reward.
- Pengguna akan membahas topik lain dan ingin meninjau verifikasi lagi nanti.
  Jangan melanjutkan kasus baru atau perubahan reward sampai diminta.
- Agenda tinjauan: review kasus lanjutan, relevansi stres 100 km terhadap data,
  serta keputusan reward/tag OSM bila diperlukan. Belum ada keputusan perubahan.
- Sinkronisasi ini hanya mengubah dokumentasi, bukan core atau notebook.

## Verifikasi lanjutan poin 2–5 (29 Oktober 2026)

- Notebook dilengkapi state A/B/C dan batas progres, action mask/revisit/closing,
  integritas snapshot/identitas edge/jarak, empat terminasi dan prioritasnya,
  serta hitungan manual skor dan seluruh komponen reward.
- Semua kasus memakai core yang sama dengan graf MultiDiGraph; tidak ada helper
  atau class baru. Core, snapshot, notebook scenario, dan hasil eksperimen tidak diubah.
- Analisis perilaku dibedakan dari kelulusan aritmetika. Stres edge sintetis 100 km
  memberi reward gagal lebih tinggi dari contoh sukses; jaminan reward global
  tidak dinyatakan lulus. Kasus ini di luar rentang panjang ruas snapshot OSM.
- Hasil: seluruh 31 cell kode selesai dari kernel Python 3.13 bersih. State/mask,
  integritas seluruh snapshot, jarak, terminasi, dan aritmetika reward sesuai acuan.
  Stres memberi reward 256,25 dibanding contoh sukses 95,08609; ini catatan desain.
  Hash core, snapshot, dan notebook scenario tidak berubah.
- Output disimpan pada notebook. Reward/tag OSM, GPX, dan validasi lapangan tidak diubah.

## Penelusuran asal skor dan reward (29 Oktober 2026)

- Graf sintetis diisi highway/surface/width dan diproses lewat add_comfort_scores(),
  lalu build_actions(). Skor dua edge paralel sekarang 0,80625 dan 0,620625.
- step() mencatat kontribusi ruas, arah, revisit, dan terminasi pada perhitungan asli;
  train_step() menambahkan penalti buntu. Verbose mencetak asal skor, formula dan
  penjumlahan reward sebelum persamaan Q, juga pada bagian OSM.
- Aturan, koefisien, mask, dan state tidak diubah. Contoh manual sintetis disesuaikan
  karena input jalan menggantikan skor langsung. Acuan Q OSM tetap sama.
- Hasil: seluruh cell notebook selesai pada kernel bersih; komponen menjumlah ke
  reward aktual, termasuk arah/revisit/terminasi/buntu. Pada 72 kombinasi dengan
  input sama, Q-table, history, dan evaluasi identik dengan sebelum pencatatan.
  Snapshot GraphML dan notebook scenario tetap tidak berubah.

## Verifikasi Q pada snapshot OSM (29 Oktober 2026)

- Ditambahkan bagian OSM pada `verifikasi.ipynb`: snapshot lokal → skor core →
  `build_actions()` → environment state B → tiga `train_step()` dengan verbose.
- Q-table/RNG terpisah dari contoh sintetis; epsilon tetap selama episode dan
  dihitung melalui `epsilon_for_episode()`. Tidak ada unduhan atau penyimpanan GraphML.
- Langkah pertama dibandingkan dengan hitungan manual berangka tetap dan Q-table.
  Ini penelusuran awal episode, bukan evaluasi loop atau validasi kondisi jalan.
- Hasil: seluruh 23 cell selesai pada kernel bersih; hitungan manual Q sesuai
  dengan core dan Q-table. Hash snapshot/core/scenario tidak berubah, dan
  keluaran langkah sintetis tetap sama.
- Core, notebook scenario, dan hasil eksperimen tidak diubah.

## Ekstraksi langkah training (29 Oktober 2026)

- Dengan persetujuan pengguna, blok tiap langkah dipindahkan ke `train_step()`;
  `train_q_learning()` dan notebook memanggil fungsi yang sama. Tidak ada class baru.
- Ditambahkan property `RunningRouteEnvironment.latest_state`, berbasis `build_state()`.
  Logika `step()`, reward, mask, state, parameter, dan format return training tetap sama.
- `verifikasi.ipynb` menelusuri dua episode × tiga langkah, satu pemanggilan per cell.
  Epsilon dihitung per episode menggunakan `epsilon_for_episode()`, dari 1,00 ke 0,05.
  Q-table/RNG dipertahankan antar-episode. Verbose mencetak persamaan Q lengkap.
- Hasil: semua cell notebook berjalan pada kernel Python 3.13 bersih. Sebanyak
  72 kombinasi uji terkontrol mempertahankan Q-table, history, dan evaluasi secara identik.
  Kasus buntu, maksimum Q negatif, action ilegal, reset/latest_state, dan verbose lulus.
- Input notebook disesuaikan menjadi graf sintetis `nx.MultiDiGraph` (3 node,
  4 edge) dan `core.build_actions(G)`, termasuk dua key paralel. Skor masih
  diisi manual untuk fokus Q-value. Core tidak diubah pada penyesuaian graf ini.
- ID `osmid` graf contoh diubah menjadi positif, 101–104, sesuai permintaan pengguna.
- Ditambahkan cell gambar graf memakai fungsi bawaan NetworkX, termasuk arah,
  dua ruas paralel, serta label key/panjang/skor. Core dan perhitungan tidak diubah.
- Reward/tag OSM, GPX, dan kelompok verifikasi lain tetap ditunda.

## Pemulihan core (29 Oktober 2026)

- Atas permintaan pengguna, `QValueUpdater` dihapus dan blok perhitungan Q pada
  `train_q_learning()` dikembalikan seperti semula. Core identik dengan versi
  sebelum seluruh perubahan verifikasi, sesuai baseline Git yang telah diperiksa.
- Pengguna ingin memeriksa kode terlebih dahulu. Belum ada penambahan latest state
  atau perubahan `step()`; notebook tidak diubah dan cell Q-nya masih perlu disesuaikan.

## Penyederhanaan verifikasi (29 Oktober 2026)

- Implementasi verifikasi lama beserta helper, callback, dan keluaran run lama
  telah dihapus atas permintaan pengguna.
- Notebook disederhanakan lagi menjadi satu contoh: buat `RunningRouteEnvironment`,
  pilih action manual, panggil `step()`, lalu cetak hasilnya. Data 0 → 1 → 2
  dipakai untuk menjalankan langkah 0 → 1 sepanjang 100 m.
- Setelah langkah, panggil `QValueUpdater` dari core dan cetak `last_update`.
  Reward contoh 0,3 dan Q awal nol menghasilkan Q baru 0,045, sesuai hitungan manual.
- Pada revisi notebook ini tidak ada perubahan core, reward, mask, state, atau parameter.
  Pemeriksaan migrasi core sebelumnya mempertahankan hasil pada 36 kombinasi.
- Poin verifikasi lainnya, penyesuaian reward/tag OSM, dan GPX ditunda.
  Dokumen TA utama dan notebook scenario tidak diedit.

## Pembaruan terminasi environment

- Terminasi aktif hanya `success`, `over_distance`, `no_available_action`, dan `step_limit`.
- Cabang terminasi kepulangan di luar rentang valid, konstanta penaltinya, serta label dan warna grafik terkait telah dihapus. Action mask tetap hanya menawarkan edge ke start jika menghasilkan total jarak 4.500--5.500 m; `step()` tetap menolak action yang tidak legal.
- Output notebook dan artefak eksperimen lama merupakan hasil tersimpan. Baris terminasi lama yang bernilai nol dan legenda grafik lama dapat tetap terlihat pada arsip tersebut; tabel dan grafik yang dibuat dari core terbaru memakai empat terminasi aktif.

## Pembaruan penyimpanan dan tampilan hasil

- `run_scenario_experiment` kini memiliki parameter `display_results`. Notebook scenario mengirim `False` agar cell training hanya menyimpan hasil, tidak memaksa tampilan tabel, grafik, dan peta.
- Setelah setiap cell training, tersedia cell baru yang memanggil `display_saved_experiment_results`. Cell tersebut memuat ulang CSV, grafik PNG, dan peta HTML tanpa menjalankan Q-Learning.
- Eksperimen baru menyimpan lebih lengkap: CSV riwayat dan evaluasi, grafik, peta, metadata JSON, Q-table `.pkl` per seed, serta jejak rute evaluasi greedy `.json` per seed.
- Ringkasan sensitivitas pada notebook A--C sekarang membaca CSV melalui `summarize_saved_experiments`, sehingga dapat dijalankan kembali setelah kernel di-restart.

## Keputusan implementasi yang penting

- Action adalah edge spesifik `(next_node, key)`. Jika terdapat beberapa edge paralel dari `u` ke `v`, masing-masing `key` adalah action berbeda.
- Riwayat revisit saat ini memeriksa node tujuan yang pernah dikunjungi, bukan ID edge.
- Revisit diizinkan setelah 50% target (2.500 m), maksimum dua kunjungan node, dan setiap revisit mendapat penalti.
- Fase pulang dimulai pada 50% target. Sebelum fase ini, agen diberi penalti ringan jika action membuatnya lebih dekat ke start; sesudah fase ini, agen memperoleh reward bila makin dekat ke start.
- Comfort score edge memakai highway, surface, dan width; comfort adalah proxy berbasis OSM, bukan hasil survei pelari atau skor keamanan.
- `closing_action_available=True` berarti selama evaluasi tersedia action legal langsung ke start yang menghasilkan total jarak 4.500--5.500 m. Flag ini adalah diagnosis kesempatan menutup loop, bukan jaminan loop berhasil.
- Dasar skala reward telah dilengkapi pada `IMPLEMENTASI.md`: titik netral comfort `0,50`, normalisasi per 100 m, simulasi koefisien arah `0,40`, batas atas konservatif reward non-terminal `+49,5`, dasar bonus sukses `+80`, serta fungsi setiap penalti terminal dan revisit. Nilai-nilai tersebut tetap diposisikan sebagai konfigurasi operasional, bukan standar universal atau nilai optimal yang telah terbukti.

## Perubahan kode pada sesi terakhir

- `rute_lari_core.py` mendukung `run_scenario_experiment(..., episodes=..., result_subdir=...)`.
- `rute_lari_core.py` kini juga mendukung `epsilon_decay_episodes`. Bila nilainya `None`, epsilon tetap turun mengikuti total episode seperti eksperimen lama. Bila diisi `50_000`, epsilon turun hanya selama 50.000 episode pertama lalu tetap 0,05.
- Jumlah episode default adalah 10.000 untuk percobaan cepat. Nilai eksplisit dipakai pada eksperimen perbandingan.
- `train_q_learning(..., episodes=..., epsilon_decay_episodes=...)` mendukung jadwal epsilon dinamis maupun tetap.
- Output eksperimen dapat ditulis ke `result_subdir`, sehingga CSV, grafik, dan peta tidak tertimpa oleh konfigurasi episode lain.
- Pada rancangan sebelum 29 Oktober 2026, notebook A--C menyediakan delapan konfigurasi. Rancangan aktif sekarang empat konfigurasi; daftar di atas menggantikan rancangan sebelumnya.
- Setiap cell eksperimen melakukan `importlib.reload(rute_lari_core)` untuk menghindari kernel memakai versi core lama.
- Artefak delapan konfigurasi sebelumnya di folder sensitivitas tetap menjadi arsip; notebook aktif kini memakai RESULT_GROUP terpisah untuk empat konfigurasi.

## Arsip hasil sensitivitas sebelumnya: Scenario B

Semua angka dari evaluasi greedy lima seed:

| Episode | Success rate | Galat jarak rata-rata (m) | Reward rata-rata | Comfort rata-rata | Return progress | Closing action rate |
|---:|---:|---:|---:|---:|---:|---:|
| 10.000 | 0,00 | 539,18 | -85,53 | 0,754 | 0,556 | 0,00 |
| 20.000 | 0,00 | 544,32 | -63,99 | 0,768 | 0,489 | 0,00 |
| 30.000 | 0,00 | 415,38 | -101,51 | 0,761 | 0,496 | 0,00 |
| 40.000 | 0,20 | 299,68 | -56,28 | 0,763 | 0,554 | 0,20 |
| 50.000 | 0,00 | 499,36 | -84,11 | 0,761 | 0,316 | 0,00 |

Interpretasi:

- 40k adalah kandidat terbaik sementara untuk B, tetapi hanya 1/5 seed sukses.
- 50k belum membaik; tambahan episode tidak otomatis meningkatkan hasil karena epsilon-greedy terus melakukan eksplorasi dan hasil lima seed masih sangat sensitif terhadap satu seed.
- Comfort stabil di sekitar 0,75--0,77. Masalah utamanya bukan pemilihan comfort, melainkan jarangnya kondisi `closing_action_available`.
- Belum boleh menyatakan model atau jumlah episode telah stabil.

## Cara membaca summary sensitivitas notebook

Sumbu X adalah jumlah episode. Semua grafik memakai agregasi lima evaluasi greedy:

1. `success_rate_greedy`: proporsi seed yang membentuk loop valid; indikator utama.
2. `mean_distance_error_m`: rata-rata selisih absolut terhadap 5.000 m; lebih kecil lebih baik, tetapi tetap harus dibaca bersama `is_loop`.
3. `mean_return_progress_ratio`: konsistensi langkah mendekati start setelah 2.500 m; makin dekat 1 makin baik.
4. `closing_action_available_rate`: proporsi seed yang pernah memiliki edge legal untuk langsung kembali ke start pada rentang valid.

Tabel juga memuat `mean_total_reward` dan `mean_comfort`. Reward bukan indikator utama karena penalti terminal dapat membuatnya turun; comfort harus dibaca sebagai proxy OSM.

## Langkah berikutnya yang disepakati

1. Tinjau dan pindahkan naskah, tabel, serta aset dari `docs/temp/BAB_4_DRAFT.md` ke dokumen utama BAB IV.
2. Bandingkan A--C dengan jumlah episode sama, evaluasi greedy, serta grafik TD-error. Jangan mencampurkan hasil epsilon dinamis dan horizon tetap sebagai satu rangkaian.
3. Tetapkan Scenario B fixed 75k sebagai kandidat sementara berdasarkan urutan prioritas: loop valid, galat jarak, lalu comfort. Return progress dan reward dibaca sebagai metrik pendukung.
4. Lima seed cukup untuk eksperimen saat ini, tetapi pembahasan BAB IV harus menyebutnya sebagai stabilitas empiris pada lima seed, bukan klaim generalisasi.

## Berkas utama

- `rute_lari_core.py`: satu-satunya core environment dan Q-Learning.
- `analisa.ipynb`: analisis data OSM.
- `scenario_A.ipynb`, `scenario_B.ipynb`, `scenario_C.ipynb`: eksperimen state dan sensitivitas episode.
- `IMPLEMENTASI.md`: wiki teknis lengkap.
- `hasil_bab_4/training_qlearning_5km/`: artefak CSV, grafik, dan peta hasil running.
- `docs/temp/BAB_4_DRAFT.docx`: draf Word mandiri BAB IV yang memuat naskah, tabel, dan visualisasi hasil final sementara; telah dirender untuk pemeriksaan tata letak sebelum dipindahkan ke dokumen skripsi utama.
- `docs/temp/BAB_4_5_DAFTAR_PUSTAKA_DRAFT.docx`: draf Word gabungan BAB IV, BAB V, dan daftar pustaka yang telah dirender serta diperiksa tata letaknya. BAB V menyimpulkan hasil fixed decay 75k secara terbatas pada lima seed dan memuat saran penelitian lanjutan.
- `referensi.md`: daftar referensi final telah diseragamkan dengan draf BAB IV--V. Saat merevisi BAB I--III, sitasi OpenStreetMap Wiki perlu menggunakan `n.d.-a`, `n.d.-b`, dan `n.d.-c` agar konsisten dengan daftar pustaka.

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


### Lokasi permanen lampiran naskah pada 4 November 2026

Atas permintaan pengguna, sumber diagram PlantUML, rumus, petunjuk dan ZIP
dipindahkan dari folder revisi sementara ke docs/assets/. Salinan hasil
ekstraksi ZIP yang identik digabung setelah pemeriksaan byte. Word panduan revisi
tetap di docs/temp/revisi_bab_1_3_20261104/. Word panduan dan naskah utama tidak
diubah; rujukan Word memakai nama berkas lampiran sehingga tetap sesuai.
Lampiran naskah berikutnya juga harus disimpan di docs/ di luar folder temp.


### Perapian aset bersama pada 4 November 2026

Aset lama di root docs/ dan lampiran terbaru kini disatukan di docs/assets/.
Folder docs/aset_naskah/ tidak digunakan lagi. Seluruh sumber PlantUML, SVG dan
rumus dipertahankan byte-nya; tidak menghapus diagram terdahulu. README folder
assets membedakan aset revisi terkini dan diagram terdahulu. Panduan visual
Bab II/III menunjuk lokasi baru. PDF panduan kampus, dokumen Word, notebook,
core, graf dan hasil eksperimen tetap. ZIP lampiran diperbarui agar petunjuknya
menunjuk folder baru. Word sementara tetap di docs/temp/.


## Bahan penyusunan Bab IV pada 4 November 2026

Atas permintaan pengguna, fokus penulisan beralih ke hasil dan pembahasan,
tanpa menyusun bagian verifikasi atau validasi. Naskah utama dibaca ulang;
struktur dipertahankan sejauh memungkinkan. Judul Rancangan Eksperimen kedua
diusulkan menjadi Hasil Pelatihan dan Evaluasi. Isi lama yang memakai hasil
dan konfigurasi terdahulu diganti melalui bahan Word sementara, bukan diedit
langsung pada TA.

Word: docs/temp/revisi_bab_4_20261104/REVISI_BAB_4_HASIL_DAN_PEMBAHASAN.docx.
Aset permanen: docs/assets/hasil_pembahasan/ (README, PNG/SVG, CSV/JSON,
buat_aset_hasil.py, dan ZIP). Draf memuat karakteristik graf, kelengkapan
atribut, aturan skor, empat konfigurasi, tabel seluruh lima seed A–C,
perbandingan state dan epsilon, pengulangan ruas, alasan berhenti, dua contoh
rute, pemanfaatan hasil, serta batas kesimpulan. Bahasa ditujukan kepada
pembaca laporan, bukan riwayat perubahan implementasi. Seluruh 32 halaman
Word dirender dan ditinjau; 60 baris tabel per seed dicocokkan ke CSV.

Sumber tunggal hasil utama: reward_missing_05_20261103, lengkap 60 training,
6.750.000 episode, dan 60 evaluasi tersimpan. Loop A/B/C: dinamis75K 0/0/1;
dinamis150K 0/3/1; tetap50K-total75K 0/2/5; tetap50K-total150K 2/4/5.
37 evaluasi gagal terdiri dari 29 melebihi jarak dan 8 tanpa pilihan ruas.
Seluruh rute gagal tidak pernah memiliki pilihan penutup loop legal pada
langkah yang dikunjungi; ini tidak berarti graf tidak mempunyai loop valid.
C tetap75K menghasilkan 5/5 loop, galat rata-rata 141,57 m dan pengulangan
1,15%, tetapi tidak dinyatakan optimal secara umum. B dinamis150K 3/5 lebih
tinggi daripada C 1/5. Tidak mengklaim C selalu unggul atau 50K optimal.

Grafik pelatihan merata-ratakan lima seed per episode lalu menggunakan
rata-rata bergerak 50 episode, ditampilkan tiap 500 episode. Tabel 10.000
episode terakhir memakai seluruh baris pada rentang itu. Pengulangan tetap
berbasis jumlah lintasan, mencakup seluruh episode. Sampel rute berhasil:
C tetap75K seed0, panjang 5.052,51 m, pengulangan 0%. Sampel gagal: A dinamis75K
seed1, panjang 4.985,77 m tetapi posisi akhir masih 2.886,66 m dari start.

Dokumen revisi sebelumnya belum tentu seluruhnya diterapkan pengguna;
pemeriksaan konsistensi antarbab ditunda sampai penyalinan selesai. Naskah TA
utama, core, notebook, graf, metadata dan hasil training tidak diubah.
Tidak menjalankan training, mengunduh peta, atau mengubah dependency proyek.
Kode aset dapat dijalankan ulang dengan uv melalui lingkungan proyek;
runtime plot sementara untuk penyusunan berada di /private/tmp saja.
