# Log Kemajuan Implementasi

Dokumen ini adalah handover singkat untuk sesi berikutnya atau agent lain. Detail teknis lengkap berada pada `IMPLEMENTASI.md`.

## Status terakhir

- Proyek: Q-Learning tabular untuk membentuk rute lari loop 5 km pada graf jalan OpenStreetMap.
- Rute valid: kembali ke node start pada total jarak 4.500--5.500 m (`is_loop=True`).
- State yang aktif dan dibandingkan: A = `(current_node,)`, B = `(current_node, progress_bin)`, C = `(current_node, previous_node, progress_bin)`.
- Scenario D telah dihapus; revisit bukan bagian state. Revisit tetap merupakan aturan environment yang sama untuk seluruh A--C.
- Evaluasi utama adalah **greedy** (`epsilon=0`) sekali untuk setiap Q-table/seed. `EPSILON_END=0,05` hanya berlaku saat training.
- Hasil aktif per 2 November 2026: `surface_width_3m_20261102`, empat konfigurasi
  dinamis 75k/150k dan horizon 50k total 75k/150k; A/B/C dan lima seed.
  Seluruh 60 training/6.750.000 episode selesai dijalankan pengguna dan diperiksa.
  Baseline `konfigurasi_empat_20261029` tetap arsip.
- Hasil rancangan sebelumnya tetap disimpan sebagai arsip. Baca angka dari CSV grup
  yang dibahas; hasil lama tidak mewakili rangkaian empat konfigurasi baru.
- Paket draf BAB IV tersedia pada `docs/temp/`: naskah sementara, manifest aset, ringkasan CSV, gambar analisis graf, grafik sensitivitas, grafik training/diagnosis B-C 75k, serta peta interaktif B-C 75k.

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
