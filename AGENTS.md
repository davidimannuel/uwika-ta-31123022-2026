# Konteks Agent Proyek TA Rute Lari

Dokumen ini adalah orientasi singkat untuk agent yang bekerja di proyek ini. Sebelum mengubah kode, notebook, atau naskah, baca juga `IMPLEMENTASI.md` sebagai sumber teknis utama dan `LOG_KEMAJUAN.md` untuk status eksperimen terakhir.

## Tujuan penelitian

Membangun dan mengevaluasi Q-Learning tabular untuk membentuk **rute lari loop 5 km** berbasis graf jalan OpenStreetMap di Dukuh Kupang, Surabaya.

Rute hanya valid bila:

1. kembali ke node start; dan
2. total jarak berada pada 4.500--5.500 meter.

Keberhasilan tersebut direpresentasikan oleh `is_loop=True`. Comfort score adalah proxy berbasis atribut OSM `highway`, `surface`, dan `width`; jangan menyebutnya sebagai persepsi pelari, keamanan aktual, atau hasil survei.

## Berkas utama

| Berkas | Peran |
|---|---|
| `rute_lari_core.py` | Satu-satunya core: data OSM, graf, comfort, environment, Q-Learning, metrik, grafik, dan peta. |
| `analisa.ipynb` | Analisis snapshot OSM dan graf. |
| `scenario_A.ipynb` | Eksperimen state A. |
| `scenario_B.ipynb` | Eksperimen state B. |
| `scenario_C.ipynb` | Eksperimen state C. |
| `verifikasi.ipynb` | Verifikasi poin 1–5: Q, state/mask, graf, terminasi, dan reward. |
| `IMPLEMENTASI.md` | Wiki implementasi dan keputusan teknis lengkap. |
| `LOG_KEMAJUAN.md` | Handover hasil dan pekerjaan terakhir. |
| `referensi.md` | Daftar sumber, format sitasi, tautan, dan pemakaian referensi pada naskah TA. |
| `docs/PANDUAN-TA-SKRIPSI-LENGKAP.pdf` | Panduan penulisan TA/skripsi; rujukan sistematika dan ketentuan penulisan naskah. |
| `docs/` | Kode PlantUML dan panduan aset visual untuk naskah TA. |
| `hasil_bab_4/training_qlearning_5km/` | CSV, grafik, peta, dan artefak eksperimen. |

`training.ipynb` adalah versi lama; jangan dipakai untuk eksperimen baru.

## Desain yang sudah disepakati

- Graf: OSMnx `MultiDiGraph` terarah, terproyeksi meter (`EPSG:32749`).
- Target: 5.000 m, toleransi 10%, area unduh bbox 3.025 m.
- Action Q-Learning: edge spesifik `(next_node, key)`. Edge paralel dengan `u` dan `v` sama tetapi `key` berbeda adalah action berbeda.
- Revisit diperiksa berdasarkan node tujuan, bukan edge. Revisit diizinkan mulai 50% target dan maksimum dua kunjungan node.
- State yang dibandingkan:
  - A: `(current_node,)`
  - B: `(current_node, progress_bin)`
  - C: `(current_node, previous_node, progress_bin)`
- Scenario D telah dihapus dan tidak boleh dihidupkan kembali tanpa persetujuan pengguna.
- Skor highway per 1 November 2026: HIGHWAY_PRIORITY_1 berisi footway,
  pedestrian, living_street, residential (1,00); HIGHWAY_PRIORITY_2 berisi
  path, service, unclassified, tertiary, tertiary_link (0,60). Nilai lain/tidak dikenal
  0,20; tag kosong 0,50. Gabungan memakai minimum. calculate_highway_score()
  pada core dipakai oleh add_comfort_scores() dan cell highway analisa.ipynb.
  Bobot 0,55/0,30/0,15, reward akses, blacklist, state dan epsilon tetap.
- Surface per 2 November 2026: SURFACE_PRIORITY berisi asphalt, concrete,
  paving_stones, paved (1,00); nilai terisi lainnya/tidak dikenal 0,20;
  kosong 0,50; gabungan minimum. calculate_surface_score() dipakai analisis/core.
- Width per 2 November 2026: WIDTH_PRIORITY_MIN_M=3.0; valid >=3 m bernilai
  1,00, positif <3 m 0,20, kosong/invalid/gabungan 0,50. Tidak ada normalisasi
  linear. width_score() dipakai analisis dan A--C. Ini preferensi reward;
  ruas <3 m tetap legal jika lolos mask, bukan standar kenyamanan/keamanan.
- `progress_bin` memakai 16 bin pada rentang 0--5.500 m.
- Evaluasi final setiap seed adalah greedy, yaitu `epsilon=0`. Epsilon minimum 0,05 hanya berlaku selama training.

## Aturan eksperimen

1. Jangan menduplikasi environment atau Q-Learning di notebook. Ubah aturan bersama hanya di `rute_lari_core.py`.
2. Jangan mengubah reward, action mask, state, dan hyperparameter sekaligus bila hasil akan dibandingkan. Ubah satu faktor per eksperimen.
3. Perbandingan A--C yang final wajib memakai jumlah episode, seed, graf, reward, dan action mask yang sama.
4. Default `EPISODES=10_000` hanya untuk uji cepat. Notebook A--C memakai empat konfigurasi: dinamis 75k/150k serta horizon epsilon 50k pada training 75k/150k. Tidak ada training total 50k atau 100k pada notebook aktif. Notebook aktif memakai `RESULT_GROUP="surface_width_3m_20261102"` yang sama pada A/B/C; grup `konfigurasi_empat_20261029` menyimpan hasil baseline lama.
5. Setiap jumlah episode melatih ulang lima seed `(0,1,2,3,4)` dari awal. Hasil 150k bukan kelanjutan Q-table hasil 75k.
6. Jangan mengklaim sistem stabil atau siap digunakan hanya dari satu loop valid atau lima seed. Laporkan keterbatasan secara eksplisit.
7. Jangan memasukkan metode atau rencana yang belum diimplementasikan ke dokumentasi TA.

## Metrik yang dipakai

Metrik utama per evaluasi greedy: `is_loop`, `total_distance_m`, `absolute_distance_error_m`, `total_reward`, `mean_comfort`, `return_progress_ratio`, `distance_to_start_at_end_m`, `closing_action_available`, dan `termination_reason`.

Interpretasi penting:

- `closing_action_available=True` berarti selama episode tersedia edge legal langsung ke start pada jarak total valid. Ini adalah kesempatan menutup loop, bukan jaminan agen memilihnya.
- `return_progress_ratio` mengukur proporsi langkah setelah 2.500 m yang mengurangi jarak lurus ke start.
- Reward training tidak wajib naik; baca bersama keberhasilan loop, jarak, closing action, dan termination rate.
- `mean_comfort` mendekati 1 berarti secara berbobot panjang rute melewati edge dengan comfort score relatif tinggi.

## Status eksperimen terakhir

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
  Tidak ada action blacklist. Validasi lapangan belum dilakukan.
- Hasil `konfigurasi_empat_20261029` dan `highway_dua_prioritas_20261101`
  tetap arsip. Jangan memakai angka/skor lama sebagai hasil grup terbaru;
  skor/reward lintas pemetaan tidak langsung sebanding atau mengisolasi satu faktor.
- Verifikasi notebook tetap ditunda. Output/assertion lama belum disesuaikan
  dengan highway, surface, width, akses dan blacklist terbaru. Pemeriksaan kecil
  saat implementasi serta replay hasil tidak menggantikan revisi notebook itu.

## Praktik kerja dan dokumentasi

- Jangan mengubah dokumen TA utama `.docx` secara langsung. Berikan umpan balik
  di chat; buat Word sementara hanya jika diminta, agar pengguna menyalin manual.

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
  Analisis sudah dijalankan ulang setelah perubahan 2 November. GraphML tetap;
  notebook verifikasi belum disesuaikan. Hasil training terbaru ada di atas.

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
  Per 30 Oktober 2026, kategori pengecualian dipisahkan ke `ACCESS_BLACKLIST`
  pada core: no, private, destination, customers, delivery, agricultural,
  forestry, military, permit, discouraged. Destination disepakati dikeluarkan.
  Blacklist kini aktif pada build_actions(): satu nilai terlarang mengeluarkan
  seluruh edge dari action, termasuk gabungan/list/titik koma dan edge ke start.
  Foot=yes tidak mengesampingkan blacklist, sesuai batasan ketat penelitian.
  Nilai di luar blacklist/kosong/bersyarat belum disaring lebih lanjut.
  Reward permissive aktif per 30 Oktober 2026: `PERMISSIVE_PENALTY_PER_100M=-0.10`
  dikalikan panjang edge/100, sebagai komponen access terpisah. Yes/kosong tidak
  mendapat tambahan reward akses. Gabungan yang mengandung permissive memakai
  seluruh panjang edge sebagai pendekatan konservatif; ini bukan pemetaan pagar.
  Grup aktif `surface_width_3m_20261102`; grup highway lama/reward saja dan
  baseline lama tetap arsip. Perbandingan ke baseline lama mencakup akses,
  blacklist dan pemetaan highway/surface/width, bukan isolasi koefisien penalti.
  Start tetap.

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

**Per 2 November 2026:** output/assertion di notebook masih memakai acuan lama;
kelulusan eksekusi 29 Oktober di bawah adalah riwayat, bukan status lulus terbaru.

**Status 29 Oktober 2026:** implementasi notebook poin 1–5 tersedia (47 cell,
31 cell kode); seluruh cell kode telah dijalankan pada kernel Python 3.13 bersih.
Ini hasil kasus yang ditulis, bukan jaminan bebas bug atau validasi lapangan.
**Pembahasan ditunda atas permintaan pengguna untuk beralih ke topik lain.**
Jangan menambah kasus, merombak notebook, atau menyesuaikan reward secara mandiri;
lanjutkan ketika pengguna meminta meninjau kembali verifikasi.

- Gunakan `train_step()` dari core untuk satu langkah training, termasuk update Q.
  `train_q_learning()` memakai fungsi yang sama; jangan menduplikasi rumus di notebook.
- `RunningRouteEnvironment.latest_state` adalah property yang membaca `build_state()`.
  `step()` tetap mengurus environment. Tidak ada class QValueUpdater atau helper baru.
- Buat graf verifikasi sintetis sebagai `nx.MultiDiGraph`; gunakan `build_actions()`
  dari core untuk membentuk action. Isi highway/surface/width, lalu gunakan
  add_comfort_scores(); jangan menetapkan skor sintetis langsung pada notebook ini.
- `verifikasi.ipynb` menjalankan satu langkah per cell, dua episode pada data sintetis.
  Epsilon dihitung memakai `epsilon_for_episode()` per episode, bukan per langkah.
  Reset environment mempertahankan Q-table dan RNG; action manual mengabaikan epsilon.
- Komponen reward dicatat pada cabang perhitungan asli di step(), bukan dihitung
  ulang untuk tampilan. train_step menambahkan komponen penalti buntu.
- `verbose=True` mencetak atribut/skor, komponen reward, dan persamaan Q aktual;
  default training tidak mencetak.
- Bagian OSM memuat snapshot lokal tanpa unduhan, menjalankan tiga langkah awal,
  dan membandingkan satu Q dengan hitungan manual berangka tetap. Q-table/RNG
  terpisah dari contoh sintetis; acuan ditinjau bila snapshot/konfigurasi berubah.
- Poin 2–5 berisi kasus terkontrol dan acuan eksplisit pada cell notebook: state/mask,
  graf/jarak, terminasi, dan reward. Gunakan MultiDiGraph serta fungsi core yang sama.
- Pisahkan kelulusan aritmetika dari analisis perilaku reward. Counterexample edge
  sintetis 100 km menunjukkan batas jaminan global; bukan data/rute nyata.
- Tidak ada helper/class terpisah, perubahan core, unduhan, atau eksperimen panjang
  untuk penambahan poin 2–5. Output disimpan pada notebook.

Saat verifikasi ditinjau kembali:

1. Review kasus dan output notebook bersama pengguna; implementasi tersedia, tetapi
   seluruh kasus lanjutan belum dinyatakan selesai direview pengguna.
2. Tinjau relevansi uji stres edge 100 km terhadap rentang data penelitian. Reward
   stres gagal 256,25 melebihi contoh loop sukses sekitar 95,08609; aritmetika
   sesuai, tetapi jaminan reward global tidak dinyatakan lulus. Ini belum menjadi
   keputusan mengubah reward; pisahkan analisis terbatas dataset dan klaim umum.
3. Jika pengguna memutuskan perubahan reward/tag OSM, tinjau expected manual dan
   rencana eksperimen A–C yang adil sebelum menjalankan ulang. GPX dan validasi
   lapangan tetap agenda terpisah; jangan menuliskannya sebagai pekerjaan selesai.
