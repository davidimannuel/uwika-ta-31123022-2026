# Wiki Implementasi Rute Lari Loop 5 KM

Dokumen ini adalah sumber konteks teknis utama proyek. Bacalah sebelum mengubah **analisa.ipynb**, **rute_lari_core.py**, atau notebook scenario A–C. Isinya menjelaskan keputusan implementasi Python, data, environment, reward, training, evaluasi, dan status eksperimen yang sudah disepakati.

Dokumen ini bukan BAB IV skripsi. Untuk naskah TA gunakan dokumen skripsi; wiki ini menyimpan rincian teknis yang terlalu panjang untuk naskah akademik.

## 1. Tujuan dan Status Implementasi

Sistem membentuk rute lari **loop 5.000 m** menggunakan Q-Learning tabular pada graf jalan OpenStreetMap. Rute hanya valid jika agen:

1. kembali ke **node start**; dan
2. total jaraknya berada pada **4.500–5.500 m**.

Kedua syarat tersebut direpresentasikan oleh **is_loop=True**. Node yang berulang tidak membatalkan loop, tetapi dinilai terpisah melalui metrik revisit dan pengulangan edge.

Tujuan agen bukan hanya mencapai jarak. Agen juga diarahkan memilih edge dengan **comfort score** lebih tinggi, yaitu proxy spasial dari atribut OSM: highway, surface, dan width. Comfort score bukan survei persepsi pelari dan bukan skor keamanan aktual.

Status hasil yang tersimpan sekarang:

- **Hasil aktif per 2 November 2026:** `surface_width_3m_20261102` selesai
  dijalankan pengguna; 60 training dan 6.750.000 episode telah diperiksa,
  seluruh 60 evaluasi direproduksi. Lihat bagian 8.2.2 dan
  `docs/temp/analisis_surface_width_3m_20261102/ANALISIS.md`.
- Ringkasan/angka 29 Oktober di bawah adalah riwayat baseline, bukan hasil aktif.

- Scenario state A, B, dan C adalah eksperimen final. Ketiganya memakai action, reward, action mask, dan aturan revisit yang sama; hanya representasi state yang berbeda.
- Hasil evaluasi terbaru harus selalu dibaca dari CSV setelah notebook dijalankan ulang. Evaluasi yang dipakai untuk pelaporan adalah evaluasi greedy, bukan episode training yang masih mengandung eksplorasi.
- Pada eksperimen epsilon dinamis awal, State C sempat menjadi kandidat utama karena menambahkan konteks arah kedatangan melalui `previous_node`. Namun, hasil epsilon decay tetap menunjukkan State B juga dapat membentuk loop secara konsisten; perbandingan final harus memakai hasil A--C dengan konfigurasi epsilon tetap yang sama.
- Terminasi paling sering masih `no_available_action` dan `over_distance`; hasil perlu dibaca bersama closing action available rate.
- Per 29 Oktober 2026, pengguna telah menyelesaikan empat konfigurasi: dinamis 75k/150k dan horizon epsilon 50k pada training 75k/150k, untuk A--C dan lima seed (60 training). Analisis hasil aktif ada pada bagian 8.2.1 dan `docs/temp/analisis_empat_konfigurasi_20261029/ANALISIS.md`. Hasil lama tetap sebagai arsip; agent hanya membaca history dan mengulang evaluasi dari Q-table, tanpa training ulang.

## 2. Struktur Proyek dan Urutan Eksekusi

| Berkas/direktori | Peran | Catatan |
|---|---|---|
| **rute_lari_core.py** | Core tunggal: konfigurasi, download/load OSM, comfort, action, state, environment, Q-Learning, metrik, grafik, dan peta. | Jangan menduplikasi aturan per scenario. |
| **analisa.ipynb** | Memakai download/load OSM dari core, lalu menganalisis data dan membuat peta graf. | Jalankan lebih dahulu. |
| **scenario_A.ipynb** | Training dan evaluasi state A. | Memanggil core bersama. |
| **scenario_B.ipynb** | Training dan evaluasi state B. | Memanggil core bersama. |
| **scenario_C.ipynb** | Training dan evaluasi state C. | Memanggil core bersama. |
| **verifikasi.ipynb** | Verifikasi poin 1–5 melalui core bersama. | Contoh manual, kasus terkontrol, dan snapshot OSM; Python 3.13. |
| **training.ipynb** | Notebook gabungan versi lama. | Jangan gunakan untuk eksperimen baru. |
| **data_osm_5km/graf_jalan_kaki_5km.graphml** | Snapshot graf jalan terproyeksi. | Input utama training. |
| **data_osm_5km/** | Menyimpan GraphML serta peta analisis highway dan comfort. | Artefak analisis. |
| **hasil_bab_4/training_qlearning_5km/** | CSV training/evaluasi, grafik, peta scenario, dan summary. | Artefak eksperimen. |
| **IMPLEMENTASI.md** | Wiki keputusan teknis ini. | Perbarui bila desain berubah. |

Urutan kerja yang benar:

1. Buka proyek dari direktori root agar path relatif berfungsi.
2. Jalankan **analisa.ipynb** dari atas sampai GraphML berhasil disimpan.
3. Buka salah satu **scenario_A.ipynb** sampai **scenario_C.ipynb**. Notebook memuat GraphML dengan fungsi core yang sama; jika GraphML belum ada, fungsi yang sama mengunduh data OSM.
4. Jalankan Scenario A, B, lalu C. Setiap scenario menjalankan lima seed, menampilkan tabel evaluasi greedy per seed, dua berkas grafik (training utama dan diagnosis), serta peta interaktif. Termination rate berada di dalam grafik diagnosis. Data hasil juga disimpan dalam CSV.
5. Jalankan perbandingan akhir A–C.
6. Gunakan CSV hasil sebagai sumber angka untuk BAB IV dan BAB V.

Notebook scenario dapat membuat GraphML bila belum ada, tetapi analisis tetap sebaiknya dijalankan lebih dahulu untuk memeriksa data dan peta.

### 2.1 Pemisahan cell training dan tampilan hasil

Pesan pada cell pemuatan graf hanya menampilkan jumlah seed. Nilai default `EPISODES=10.000` dipakai untuk uji cepat di core dan tidak ditampilkan lagi karena seluruh eksperimen notebook mengirim jumlah episode secara eksplisit.

Setiap konfigurasi eksperimen pada `scenario_A.ipynb`, `scenario_B.ipynb`, dan `scenario_C.ipynb` sekarang memiliki dua cell berurutan:

1. **Cell training** memanggil `run_scenario_experiment(..., display_results=False)`. Cell ini menjalankan lima seed, melakukan evaluasi greedy, lalu menyimpan artefak; tabel, grafik, dan peta tidak ditampilkan agar output training tidak berat.
2. **Cell tampilkan hasil tersimpan** memanggil `display_saved_experiment_results(...)`. Cell ini **tidak melakukan training**. Cell hanya membaca berkas hasil, lalu menampilkan metrik per seed, diagnosis, termination rate, dua grafik PNG, dan peta HTML interaktif.

Pemisahan ini memungkinkan pengguna memuat ulang peta yang gagal tampil, melihat lagi tabel, atau membuat screenshot grafik tanpa menjalankan ulang training yang memakan waktu. Cell ringkasan sensitivitas juga memakai `summarize_saved_experiments(...)`, sehingga membaca CSV yang tersimpan dan tidak lagi bergantung pada variabel `result_*` yang hanya ada di RAM kernel.

Untuk setiap eksperimen baru, folder `hasil_bab_4/training_qlearning_5km/<result_subdir>/` menyimpan:

| Artefak | Isi dan kegunaan |
|---|---|
| `training_history_<scenario>.csv` | Metrik setiap episode untuk lima seed, termasuk reward, epsilon, TD-error, jarak, comfort, dan alasan terminasi. |
| `evaluation_metrics_<scenario>.csv` | Metrik evaluasi greedy per seed yang dipakai sebagai hasil utama. |
| `diagnosis_metrics_<scenario>.csv` dan `termination_rates_*.csv` | Ringkasan diagnosis dan termination rate training maupun evaluasi greedy. |
| `grafik_training_<scenario>.png` dan `grafik_diagnosis_<scenario>.png` | Diagram hasil training yang sudah dirender. |
| `peta_interaktif_scenario_<scenario>.html` | Peta Folium untuk rute representatif. |
| `qtable_scenario_<scenario>_seed_<seed>.pkl` | Q-table tabular hasil training untuk setiap seed. |
| `rute_evaluasi_scenario_<scenario>_seed_<seed>.json` | Urutan node dan action hasil evaluasi greedy untuk setiap seed. Setiap action menyimpan `from_node`, `next_node`, dan `key` agar edge MultiDiGraph dapat dikenali kembali. |
| `metadata_eksperimen_<scenario>.json` | Konfigurasi episode, epsilon decay, seed, seed yang dipilih untuk peta, dan daftar artefak. |

Artefak Q-table, rute JSON, dan metadata dibuat oleh implementasi terbaru. Folder hasil lama yang dibuat sebelum perubahan ini tetap dapat ditampilkan selama CSV, PNG, dan HTML-nya tersedia; namun Q-table tidak dapat dipulihkan dari folder lama tanpa menjalankan ulang training tersebut.

Pada tampilan hasil tersimpan, bagian **Ringkasan Diagnosis Evaluasi: Agregat Lima Seed** memang hanya memiliki satu baris. Baris tersebut bukan hasil satu seed, melainkan ringkasan lima evaluasi greedy: rata-rata `distance_to_start_at_end_m`, rata-rata `return_progress_ratio`, proporsi `closing_action_available`, dan rata-rata jumlah state Q-table. Nilai per seed tetap tersedia pada tabel **Metrik Evaluasi Greedy per Seed** tepat di atasnya.

Sebelum peta ditampilkan, cell juga mencetak seed yang dipakai serta alasan pemilihannya. Informasi ini diambil dari `metadata_eksperimen_<scenario>.json` apabila tersedia. Untuk folder hasil lama tanpa metadata, seed dihitung ulang dari `evaluation_metrics_<scenario>.csv` memakai aturan pemilihan peta yang sama.

Fungsi `display_saved_experiment_results(...)` khusus untuk tampilan dan sengaja tidak mengembalikan nilai, sehingga notebook tidak mencetak dictionary besar setelah peta. Jika data CSV perlu diolah pada cell lain, gunakan `load_saved_experiment_results(...)`. Peta Folium ditampilkan dengan memasukkan HTML tersimpan ke `iframe.srcdoc` melalui JavaScript Jupyter. Cara ini tidak bergantung pada alamat `file://` maupun endpoint `/files/`, yang dapat diblokir atau memakai root berbeda pada JupyterLab desktop.

## 3. Konfigurasi Bersama

| Parameter | Nilai | Makna |
|---|---:|---|
| START_LAT | -7.282187 | Latitude titik start input pengguna. |
| START_LON | 112.709282 | Longitude titik start input pengguna. |
| TARGET_DISTANCE_M | 5.000 m | Target panjang rute loop. |
| DISTANCE_TOLERANCE | 10% | Toleransi target. |
| MIN_DISTANCE_M | 4.500 m | Batas minimum loop valid. |
| MAX_DISTANCE_M | 5.500 m | Batas maksimum loop valid. |
| DOWNLOAD_RADIUS_M | 3.025 m | Setengah lebar bbox unduhan OSM dari start. |

Dasar area unduhan:

- 5.000 m × 1,10 = 5.500 m sebagai batas rute maksimum.
- 5.500 m ÷ 2 = 2.750 m sebagai jarak jalur teoritis terjauh pada loop.
- 2.750 m × 1,10 = 3.025 m setelah buffer 10%.

Karena OSMnx memakai dist_type bbox, 3.025 m adalah setengah lebar area kotak, bukan radius lingkaran. Buffer 10% adalah keputusan desain eksperimen, bukan rumus standar universal.

## 4. Notebook Analisis Data

### 4.1 Tujuan analisa.ipynb

Notebook analisis membangun input bagi environment. Notebook ini tidak melakukan training. Hasilnya adalah graf terproyeksi, analisis struktur/kualitas data, comfort score per edge, dan peta untuk inspeksi manual.

### 4.2 Pengambilan graf OSM

Konsep pemanggilan OSMnx:

    ox.graph_from_point(
        center_point=(START_LAT, START_LON),
        dist=DOWNLOAD_RADIUS_M,
        dist_type="bbox",
        network_type="walk",
        simplify=True,
        retain_all=False,
        truncate_by_edge=True,
    )

Keputusan parameter:

- **network_type walk**: memilih jaringan yang dapat dilalui pejalan kaki/pelari. Parameter ini bukan jaminan kenyamanan atau keamanan.
- **simplify True**: node yang hanya membentuk bentuk geometri jalan dikurangi; simpang, ujung jalan, dan titik keputusan dipertahankan. Hal ini mengurangi state yang tidak bermakna.
- **retain_all False**: memakai komponen weakly connected terbesar dan membuang pulau jaringan kecil.
- **truncate_by_edge True**: membantu mencegah jalan buntu palsu pada tepi bbox.

Sebelum unduhan final, surface ditambahkan ke daftar useful tags way OSMnx. Jika kolom surface belum ada, itu berarti tag belum disimpan oleh konfigurasi OSMnx, bukan berarti OSM tidak memiliki data surface.

### 4.3 Proyeksi koordinat

Graf awal berada pada WGS84, EPSG:4326: x adalah longitude dan y adalah latitude dalam derajat. Setelah itu graf diproyeksikan dengan **ox.project_graph** menjadi CRS lokal EPSG:32749. Pada graf terproyeksi, x dan y memakai meter.

Proyeksi wajib karena environment menghitung jarak lurus memakai **np.hypot(x - x0, y - y0)**. Perhitungan Pythagoras tersebut hanya layak sebagai meter jika koordinat sudah terproyeksi. Untuk peta Folium, koordinat meter ditransformasikan kembali ke WGS84.

Alurnya:

    WGS84 longitude-latitude
        -> project_graph
        -> x-y meter untuk graf dan RL
        -> transform WGS84 untuk Folium

### 4.4 Struktur MultiDiGraph

Graf adalah networkx MultiDiGraph:

- **node**: simpang, ujung ruas, atau titik keputusan; ID-nya adalah ID node OSM.
- **edge u -> v**: perpindahan terarah dari node u ke node v.
- **key**: pembeda edge paralel apabila u dan v sama.
- **osmid**: ID OSM Way atau ruas jalan sumber; bukan ID node.
- atribut edge penting: length, geometry, highway, surface, width, dan oneway.

Secara sederhana, **node** adalah titik pada jaringan jalan, sedangkan **edge** adalah satu ruas/jalur yang menghubungkan dua node. Contohnya, bila agen berada pada node A dan terdapat ruas jalan sepanjang 120 m menuju node B, maka perpindahan `A -> B` melalui ruas tersebut adalah satu edge. Node biasanya mewakili simpang, ujung ruas, atau titik keputusan; edge menyimpan karakter ruas yang benar-benar dilalui, seperti panjang, klasifikasi jalan, permukaan, lebar, dan `comfort_score`.

Pada Q-Learning proyek ini, ketika agen memilih action, agen sebenarnya memilih **satu edge** untuk bergerak dari node saat ini ke node tujuan. Karena graf bertipe MultiDiGraph, dua node yang sama dapat dihubungkan oleh lebih dari satu edge. Oleh sebab itu action tidak cukup ditulis sebagai node tujuan saja, melainkan sebagai pasangan `(next_node, key)`. Nilai `key` membedakan edge paralel yang memiliki asal `u` dan tujuan `v` sama, tetapi dapat mewakili ruas atau atribut yang berbeda.

    Node A -- edge: panjang 120 m, comfort 0,75 --> Node B

Pada contoh tersebut, `Node A` adalah posisi agen sebelum bergerak, edge adalah ruas jalan yang dipilih, dan `Node B` menjadi posisi agen setelah action dijalankan. Reward comfort dan total jarak diperoleh dari atribut edge yang dipilih, bukan dari node tujuan saja.

Snapshot graf yang dipakai saat ini:

| Metrik | Nilai |
|---|---:|
| Jumlah node | 8.027 |
| Jumlah edge directed | 21.374 |
| CRS | EPSG:32749 |
| Weakly connected components | 1 |
| Total panjang edge directed | 1.353.832,10 m |
| Panjang edge rata-rata | 63,34 m |
| Panjang edge median | 46,19 m |
| Tujuan node unik dari start | 3 |

Total panjang edge directed bukan total jalan fisik unik karena arah dua arah dapat tercatat lebih dari sekali.

### 4.5 Analisis yang dipertahankan

Analisis wajib mencakup sampel node/edge; ringkasan struktur; konektivitas; panjang edge; node start; kelengkapan highway, surface, width, smoothness, dan access; distribusi lima atribut; indikator jumlah tujuan node; kombinasi kelengkapan lima atribut analisis; distribusi comfort score; serta peta interaktif.

Kualitas atribut snapshot sekarang:

| Atribut | Ketersediaan edge |
|---|---:|
| highway | 100,00% |
| surface | 67,59% |
| width mentah | 66,77% |
| width valid dalam meter | 66,18% |
| smoothness pada salinan analisis (cache seluruh way asal) | 65,21% |
| access pada GraphML | 3,03% |

Edge dengan data kosong tidak dibuang karena bisa memutus graf. Komponen comfort yang tidak tersedia menggunakan nilai netral.

### 4.6 Integrasi smoothness dan access ke analisis atribut

Klarifikasi akhir pengguna 29 Oktober 2026: kedua atribut harus masuk pada
seluruh elemen analisis atribut yang relevan. Notebook tetap 43 cell, dengan
perubahan pada bagian yang sudah ada; tidak menambahkan eksplorasi tag lain.

Alur data terpadu:

1. Sesudah graf dimuat, `edges_gdf` menjadi salinan analisis. Jika smoothness
   belum ada, cache yang dipilih oleh `SMOOTHNESS_CACHE_PATH` dicocokkan melalui
   osmid setiap edge. Tidak ada unduhan atau penulisan ulang GraphML.
2. Smoothness dimasukkan sebagai nilai edge hanya jika seluruh way asal ditemukan
   dan bertag. Gabungan kategori dipertahankan sebagai list, bukan memilih nilai
   terbaik. `smoothness_status` dan `smoothness_nilai_asal` menyimpan cakupan/
   informasi parsial. Data parsial tidak dihitung sebagai atribut lengkap.
3. `edges_table` dibuat dari tabel analisis ini tanpa memuat ulang dari G, sehingga
   lima atribut tetap konsisten di semua bagian berikutnya.

Bagian yang diperbarui:

- Sampel/daftar kolom edge dengan sumber dan cakupan smoothness.
- Tabel dan diagram kelengkapan highway/surface/width/smoothness/access;
  tabel membedakan kolom graf asli dan sumber data pada salinan analisis.
- Distribusi smoothness/access per edge berdasarkan jumlah dan panjang, sama
  seperti highway/surface. Tabel smoothness juga menampilkan cakupan dan nilai
  tidak dikenal. Access--foot diperiksa pada way asal yang sama.
- Diagram distribusi menjadi enam panel: highway, surface, kualitas width,
  width valid, smoothness, dan access. Panel width valid tetap memakai subset
  width valid; empat distribusi kategori memakai seluruh panjang edge.
- Kombinasi ketersediaan memakai lima atribut; width tetap mensyaratkan parsing
  meter valid. Ketersediaan tag tidak identik dengan validitas atau izin akses.
- Tooltip peta highway/comfort serta contoh tabel comfort memuat smoothness/
  access sebagai informasi tambahan. Warna/rumus comfort tetap tiga komponen lama.

Sumber cache cocok dengan 6.554 way asal unik. Dari 21.374 edge, smoothness
terisi penuh pada 13.938 (65,21%), parsial pada 216, dan tidak terisi pada 7.220.
Access terisi pada 648 edge (3,03%). Seluruh statistik utama memakai edge
directed; jangan mencampurkan denominator way sumber dari analisis sebelumnya.

Seluruh 21 cell kode berisi dieksekusi pada kernel Python 3.13 dan output disimpan.
Pemeriksaan mencakup konsistensi lima atribut, konservasi jumlah/panjang/
persentase pada distribusi dan kombinasi, pemisahan data parsial, tooltip peta,
cache tidak tersedia, serta kesamaan comfort score terhadap core.
Core, GraphML, notebook scenario/verifikasi, dan hasil training tidak diubah.
Analisis HTML/PNG yang memang dihasilkan notebook diperbarui oleh Run All.

### 4.7 Peta interaktif atribut jalan dan akses

Per 30 Oktober 2026, cell peta analisa.ipynb bernama **Peta Interaktif Atribut
Jalan dan Akses**, dengan tampilan berikut:

- Default hanya warna ruas **Highway (jenis jalan)** dan marker START.
- Pilihan **Surface (permukaan jalan)** dan **Smoothness** mengganti warna ruas bergantian;
  Highway, Surface, dan Smoothness menjadi FeatureGroup `overlay=False` pada
  kontrol radio. Tile basemap terpisah dengan `control=False`, sehingga tetap
  terlihat pada ketiga tampilan. Surface ditambahkan pada 2 November 2026.
- Kategori smoothness meliputi kategori tag yang dikenal, gabungan, tidak dikenal,
  kosong, data parsial, serta sumber belum lengkap. Nilai asli dan cakupan tetap
  ada di tooltip. Ini kategori peta, bukan skor/reward baru.
- Surface menampilkan warna material asli (asphalt/paving_stones/concrete dan
  lainnya), gabungan, tidak dikenal, serta kosong. Tooltip menampilkan nilai
  asli dan calculate_surface_score() dari core; warna bukan skor keselamatan.
- Marker access per jenis tersedia sebagai overlay yang awalnya tidak aktif.
  Legenda highway/surface/smoothness mengikuti pilihan warna ruas; legenda access muncul
  jika minimal satu layer marker diaktifkan. Pengaturan memakai event Leaflet.

Kategori marker no merah, destination oranye, permissive biru, yes hijau,
private merah gelap; nilai lain/gabungan ungu. Marker dihitung di tengah geometri
pada CRS meter kemudian diubah ke WGS84. Pasangan edge dua arah dengan node,
key, geometri ternormalisasi, osmid dan access identik berbagi marker; seluruh
identitas edge dicantumkan di popup. Key paralel berbeda tidak digabung.
Marker bukan koordinat pintu/pagar atau keputusan izin pejalan kaki.

Snapshot menghasilkan 324 marker untuk 648 edge: no 12/24, destination 25/50,
permissive 195/390, yes 92/184 (marker/edge). HTML tetap tersimpan pada
`data_osm_5km/peta_graf_highway.html`; output cell notebook juga diperbarui.
Pemeriksaan meliputi default layer, kategori/cakupan, urutan JavaScript dan
pergantian legenda. Uji interaksi Chrome memeriksa radio tema, overlay access,
legenda, dan kembali ke Highway tanpa error JavaScript; tampilan diperiksa visual.

Pengguna membatasi pengembangan berikutnya pada access agar sederhana.
Pengamatan pengguna: sekitar lokasi start banyak ruas permissive.

### 4.8 Blacklist akses aktif (30 Oktober 2026)

`ACCESS_BLACKLIST` berisi no, private, destination, customers, delivery,
agricultural, forestry, military, permit, discouraged. Atas instruksi pengguna,
build_actions() tidak membuat EdgeAction bila satu nilai access termasuk daftar
tersebut. Graf asli/GraphML tidak dihapus atau diubah; hanya daftar action.

Nilai tunggal, huruf besar/kecil, list hasil simplify, string list, dan pemisah
titik koma ditangani. Jika gabungan memuat satu kategori blacklist, seluruh
edge dikeluarkan. Edge paralel lain yang lolos tetap action terpisah. Berlaku
untuk fresh/revisit/closing, eksplorasi, dan greedy pada seluruh A--C.

Ini batasan penelitian yang sengaja ketat terhadap access: foot=yes tidak
membatalkan blacklist. Belum menerapkan seluruh hierarki izin pejalan kaki OSM.
Yes/permissive/kosong tetap dibentuk sebagai action bila panjang positif;
permissive tetap menerima penalti -0,10 per 100 m. Unknown/variable/nilai baru
dan akses bersyarat belum mendapat penyaringan tambahan, sehingga bisa tetap
terbentuk jika tidak mengandung kategori blacklist. Ini bukan jaminan izin
publik atau keterlintasan lapangan. Titik start dan aturan revisit tetap.

Metadata eksperimen menyimpan penanda blacklist aktif, daftar nilai, dan
kebijakan gabungan tanpa override foot. Saat pengaktifan blacklist, grupnya
`reward_access_blacklist_010_20261030`, terpisah dari grup percobaan reward saja
`reward_access_010_20261030` dan baseline `konfigurasi_empat_20261029`. Grup aktif
setelah perubahan surface/width 2 November dijelaskan pada bagian 5.4.
Perbandingan dengan baseline lama kini mencakup reward dan penyaringan akses;
jangan mengatribusikan seluruh perubahan hasil hanya pada koefisien penalti.

## 5. Comfort Score pada Edge

### 5.1 Formula

    comfort_score =
        0,55 × highway_score
      + 0,30 × surface_score
      + 0,15 × width_score

Comfort score berada pada 0–1. Highway mendapat bobot terbesar karena karakter fungsi ruas lebih informatif; surface menunjukkan karakter fisik permukaan; width diberi bobot terkecil karena lebar badan jalan kendaraan belum tentu sama dengan ruang lari yang nyaman.

### 5.2 Kebijakan nilai

| Komponen | Implementasi |
|---|---|
| highway | Prioritas 1: footway/pedestrian/living_street/residential = 1,00; prioritas 2: path/service/unclassified/tertiary/tertiary_link = 0,60; jenis lain/tidak dikenal = 0,20; kosong = 0,50. |
| surface | Satu prioritas: asphalt/concrete/paving_stones/paved = 1,00; nilai terisi lainnya/tidak dikenal = 0,20; kosong = 0,50. |
| width | Lebar valid >=3 m = 1,00; positif <3 m = 0,20; tidak ada kenaikan skor setelah ambang. |
| data tidak terpakai | Highway/surface kosong = 0,50; width kosong/invalid/gabungan = 0,50. Nilai surface terisi di luar prioritas = 0,20. |
| edge gabungan | Bila highway/surface berupa list setelah simplify, dipilih skor minimum secara konservatif. |

Fungsi inti: **is_missing**, **osm_values**, **calculate_highway_score**, **calculate_surface_score**, **parse_width_m**, **width_score**, dan **add_comfort_scores**. Ketiga cell skor analisis memakai fungsi core yang sama dengan A--C.

Comfort score adalah proxy spasial. Jangan menyebutnya sebagai hasil validasi pengalaman pelari tanpa survei atau validasi lapangan.

### 5.3 Riwayat dua prioritas highway (1 November 2026)

Catatan bagian ini merekam pekerjaan 1 November. Contoh W=0,625/C=0,94375
adalah acuan sebelum perubahan width; aturan aktif 2 November ada di 5.2 dan 5.4.

Klarifikasi pengguna: tertiary dan tertiary_link juga masuk Prioritas 2 (0,60),
sebagai alternatif rute lari. Ini preferensi penelitian, bukan jaminan aman.

Variabel keanggotaan HIGHWAY_PRIORITY_1 dan HIGHWAY_PRIORITY_2 dipisahkan dari
HIGHWAY_PRIORITY_1_SCORE=1.00, HIGHWAY_PRIORITY_2_SCORE=0.60,
HIGHWAY_OTHER_SCORE=0.20, dan HIGHWAY_MISSING_SCORE=0.50. Tidak lagi memakai
pemetaan skor per jenis highway yang berbeda-beda. Skor 1 bukan jaminan aman.

calculate_highway_score() membedakan tag kosong dari nilai terisi yang tidak
dikenal. Mendukung list/string list/kapital/spasi/titik koma; gabungan memakai
minimum. Cell highway analisa.ipynb memanggil fungsi core ini, sedangkan helper
surface dan aturan width dipertahankan. Output analisis mulai cell highway
dikosongkan untuk dihitung ulang, tanpa menjalankan ulang peta atau menyimpan
ulang GraphML dalam pekerjaan ini. Atribut skor disusun ulang di memori saat
training memanggil add_comfort_scores(), sehingga snapshot tidak perlu diunduh.

Contoh residential/asphalt/lebar 3 m menghasilkan H=1, S=1, W=0.625, sehingga
C=0.94375. Ruas 100 m memberi reward ruas +0.44375, atau +0.34375 setelah
penalti permissive, sebelum komponen arah/revisit/terminal. Bobot komponen,
penalti akses, blacklist, state, seed, jumlah episode, dan epsilon tidak berubah.

Metadata eksperimen mencatat kelompok, empat skor, dan kebijakan gabungan.
Notebook A--C memakai grup baru highway_dua_prioritas_20261101, terpisah dari
grup sebelumnya reward_access_blacklist_010_20261030. Output lama pada notebook
scenario dikosongkan; artefak hasil lama tetap utuh. Belum ada training baru.
Notebook verifikasi tetap ditunda; acuan numeriknya adalah konfigurasi lama.

### 5.4 Surface satu prioritas dan width 3 m (2 November 2026)

Surface disederhanakan karena kategori dominan pada snapshot adalah paving_stones,
asphalt, dan concrete. SURFACE_PRIORITY berisi asphalt/concrete/paving_stones/paved;
SURFACE_PRIORITY_SCORE=1.00, SURFACE_OTHER_SCORE=0.20, SURFACE_MISSING_SCORE=0.50.
List/string list/titik koma memakai minimum; nilai terisi tak dikenal bukan netral.

Width tidak lagi memakai normalisasi linear 1–5 m. WIDTH_PRIORITY_MIN_M=3.0,
WIDTH_PRIORITY_SCORE=1.00, WIDTH_OTHER_SCORE=0.20, WIDTH_MISSING_SCORE=0.50.
parse_width_m() tetap menerima satu nilai positif dalam meter, termasuk koma
sebagai desimal pada masukan. List, gabungan titik koma, nol/negatif dan format
invalid diberi skor pengganti. Batas 3 m dipilih pengguna untuk mengurangi
preferensi gang sempit; bukan hasil survei, standar kenyamanan atau larangan aksi.
Lebar badan jalan tidak sama dengan ruang bebas bagi pelari.

Residential/asphalt/3 m kini menghasilkan H=1, S=1, W=1, C=1. Ruas 100 m
memberi reward karakter +0,50; bila permissive menjadi +0,40 sebelum komponen
lain. Pada lebar 2 m diperoleh W=0,20, C=0,88 dan reward karakter +0,38.

Snapshot 21.374 edge: width score 1 pada 9.696 edge, 0,20 pada 4.450,
dan 0,50 pada 7.228. Surface score 1 pada 14.392, 0,20 pada 54, 0,50 pada 6.928.
Jumlah action tetap 21.300. Highway, bobot 0,55/0,30/0,15, reward akses,
mask, state, seed, epsilon dan jumlah episode tidak diubah pada revisi ini.
Analisis sudah dijalankan seluruhnya (21 cell kode) dan peta comfort diperbarui;
GraphML tidak ditulis ulang. Notebook verifikasi lama belum disesuaikan.

Metadata hasil mencatat surface_scoring dan width_scoring, selain highway dan
akses. Grup surface_satu_prioritas_20261102 sempat disiapkan tetapi belum ada
hasil saat ambang width diterapkan. Grup final revisi ini adalah
surface_width_3m_20261102, yang kemudian dijalankan pengguna (bagian 8.2.2).

## 6. Implementasi Q-Learning pada Core Bersama

### 6.1 Input dan snapping start

Semua notebook scenario memanggil **load_or_download_graph()** dari `rute_lari_core.py`. Fungsi ini memuat **data_osm_5km/graf_jalan_kaki_5km.graphml**, atau mengunduh serta menyimpannya bila belum ada. Koordinat start latitude-longitude ditransformasi ke CRS graf, kemudian **ox.distance.nearest_nodes** menentukan START_NODE. Ini memastikan agen mulai pada node yang benar-benar ada dalam graf.

Setelah GraphML dimuat, **add_comfort_scores(G)** dipanggil lagi untuk membuat atribut skor tersedia pada memori. Dictionary **NODE_XY** menyimpan koordinat meter semua node.

### 6.2 Action

Satu action adalah objek **EdgeAction** yang menyimpan:

    next_node, key, length_m, comfort_score, data edge

ID action di Q-table adalah **(next_node, key)**. Node saat ini sudah bagian dari state, sehingga action tidak perlu menyimpan current node. Identitas edge lengkap untuk log rute adalah **(current_node, next_node, key)**.

Fungsi **build_actions(G)** membuat ACTIONS_BY_NODE setelah mengecualikan edge yang access-nya mengandung kategori ACCESS_BLACKLIST. Edge paralel yang lolos tetap menjadi action berbeda. Tidak ada pemilihan edge berdasarkan comfort secara paksa; agen mempelajarinya melalui reward dan Q-table.

Contoh, `(u, v, key=0)` dan `(u, v, key=1)` adalah **dua action berbeda** walaupun sama-sama berakhir di node `v`. Q-table menyimpan nilai masing-masing secara terpisah: `Q[state][(v, 0)]` dan `Q[state][(v, 1)]`. Saat eksplorasi, salah satunya dapat dipilih acak; saat eksploitasi, action dengan Q-value terbesar dipilih. Perbedaan panjang, comfort score, atau nilai masa depan dapat membuat Q-value keduanya berbeda. Namun aturan revisit tetap berbasis ID node tujuan `v`: memilih edge dengan key berbeda tetapi menuju `v` yang sudah dikunjungi tetap dianggap revisit.

### 6.3 Scenario state

| Scenario | State | Tujuan |
|---|---|---|
| A | (current_node,) | Baseline: agen hanya tahu posisi node. |
| B | (current_node, progress_bin) | Membedakan keputusan awal dan akhir pada node yang sama. |
| C | (current_node, previous_node, progress_bin) | Menambahkan arah kedatangan. |

Fungsi pembentuk state adalah **build_state(environment, scenario)**. Jangan mengganti istilah ini menjadi encoder.

Kata **bin** berarti *bucket* atau kategori rentang nilai. Pada proyek ini, `progress_bin` tidak menyimpan jarak meter yang persis, melainkan nomor kategori progres jarak. Parameter `PROGRESS_BINS = 16` berarti rentang 0--5.500 m dibagi menjadi **16 kategori**, dengan indeks 0 sampai 15. Angka **15 bukan pilihan parameter terpisah**; ia adalah indeks terakhir karena indeks Python dimulai dari 0: `16 - 1 = 15`.

Nilai 16 dipilih sebagai kompromi desain: cukup rinci untuk membedakan fase awal, tengah, dan akhir rute (sekitar 343,75 m per kategori), tetapi tidak terlalu banyak sehingga kombinasi state `(node, progress_bin)` membuat Q-table menjadi jauh lebih besar dan jarang dikunjungi. Nilai ini bukan rumus standar universal; bila kelak diubah, seluruh Scenario A--C harus dijalankan ulang agar perbandingan tetap adil.

**progress_bin** menghitung jarak yang sudah ditempuh menjadi 16 kategori:

    int(total_distance_m / MAX_DISTANCE_M × 16)

`MAX_DISTANCE_M` bernilai 5.500 m. Maka satu kategori kira-kira mewakili 5.500 ÷ 16 = 343,75 m. `int(...)` membuang bagian desimal, sehingga hasilnya adalah indeks kategori, bukan jarak meter.

| Jarak yang sudah ditempuh | Perhitungan ringkas | progress_bin |
|---:|---:|---:|
| 0 m | int(0 ÷ 5.500 × 16) | 0 |
| 2.750 m | int(2.750 ÷ 5.500 × 16) | 8 |
| 5.000 m | int(5.000 ÷ 5.500 × 16) | 14 |
| 5.500 m | int(5.500 ÷ 5.500 × 16) = 16, lalu dibatasi | 15 |

Hasil akhirnya selalu dibatasi pada 0 sampai 15 melalui `min(PROGRESS_BINS - 1, max(0, raw_bin))`. Batas bawah 0 menjaga nilai tidak negatif; batas atas 15 mencegah indeks 16 atau lebih ketika jarak mencapai/melewati 5.500 m. Karena itu node yang sama dapat menjadi state berbeda saat agen masih awal, pertengahan, atau mendekati batas jarak.

### 6.4 Kondisi environment

Kelas **RunningRouteEnvironment** menyimpan:

    current_node, previous_node, total_distance_m, step_count,
    node_visits, revisit_count, path_nodes, path_actions,
    done, is_loop, termination_reason

**reset()** membuat episode baru: current node kembali ke start, jarak 0, previous node -1, start dihitung telah dikunjungi satu kali, dan riwayat rute dikosongkan.

### 6.5 Action mask dan revisit

Fungsi **available_actions()** membagi edge keluar menjadi tiga kelompok:

1. **fresh_actions**: next node belum dikunjungi.
2. **closing_actions**: next node adalah start dan total jarak baru berada dalam 4.500–5.500 m.
3. **revisit_actions**: next node sudah dikunjungi, revisit diizinkan, jarak sudah minimal 50% dari target, dan node belum dikunjungi dua kali.

Kebijakan yang dipakai:

    jika ada fresh action: fresh_actions + revisit_actions + closing_actions
    jika tidak ada fresh tetapi revisit ada: revisit_actions + closing_actions
    jika fresh dan revisit kosong: closing_actions saja

Dengan urutan ini, sebelum 50% target `revisit_actions` masih kosong sehingga agen hanya melihat fresh dan closing action. Setelah 50% target, revisit yang memenuhi syarat ikut ditawarkan **meskipun fresh action masih ada**. Batas ini sengaja disamakan dengan fase pulang agar agen dapat mempertimbangkan jalur lama tepat ketika reward arah pulang mulai aktif. Ini memberi agen pilihan untuk memakai node lama sebagai jalur pulang, tanpa mengizinkan pengulangan tak terbatas.

Konfigurasi tetap untuk semua scenario:

| Parameter | Nilai |
|---|---:|
| ALLOW_REVISIT | True |
| REVISIT_AFTER_RATIO | 0,50 |
| RETURN_PHASE_RATIO | 0,50 |
| MAX_NODE_VISITS | 2 |

Ini penting: A–C diuji secara adil karena tidak mempunyai environment berbeda.

Kepulangan ke start di luar rentang 4.500--5.500 m dicegah oleh action mask sebelum action dipilih. Fungsi step juga menolak action yang tidak legal. Terminasi aktif hanya success, over_distance, no_available_action, dan step_limit.

Setiap kali `closing_actions` tidak kosong, environment mencatat `closing_action_was_available=True` untuk episode tersebut. Flag ini **tidak** mengubah daftar action, reward, atau policy; ia hanya mencatat bahwa agen pernah memiliki kesempatan legal untuk langsung menutup loop.

### 6.6 Urutan kerja step(action)

Urutan fungsi **step()** harus dipahami sebelum dimodifikasi:

1. Memastikan episode belum selesai.
2. Menghitung action legal dan menolak action yang tidak ada pada action mask.
3. Menyimpan current node, next node, serta jarak lurus sebelum bergerak.
4. Mengubah posisi, total jarak, previous node, riwayat rute, jumlah kunjungan, dan jumlah langkah.
5. Menghitung reward comfort edge dan menambahkan komponen penalti access permissive.
6. Menambahkan penalti jika terjadi revisit ke node selain start.
7. Memeriksa terminal dengan urutan: success, over_distance, step_limit. Kondisi no_available_action ditangani saat tidak ada action legal.
8. Jika belum terminal dan jarak sudah 50% target, menambahkan reward arah pulang.
9. Mengembalikan next state, reward, done, dan info.

is_loop hanya menjadi True apabila action memasuki start dan jarak total valid. termination_reason pada kondisi tersebut adalah success.

## 7. Reward, Policy, dan Pembaruan Q-table

### 7.1 Reward

Reward edge:

    r_edge = (comfort_score − 0,50) × length_m ÷ 100

Per 30 Oktober 2026, terdapat komponen reward akses terpisah:

    r_access = -0,10 × length_m ÷ 100  jika tag access mengandung permissive
    r_access = 0                     untuk nilai lainnya

Konstanta `PERMISSIVE_PENALTY_PER_100M=-0.10` tidak mengubah comfort score,
state, atau daftar action. Ini preferensi mengurangi panjang ruas permissive,
bukan klaim bahwa ruas tersebut dilarang, berpagar, atau tidak aman. Untuk
100 m dengan comfort 0,80, reward ruas +0,30 menjadi +0,20 setelah komponen
akses, sebelum arah/revisit/terminal. Seratus meter permissive menuju start
pada loop valid tetap memperoleh bonus +80, dan akses tetap diperhitungkan.

Nilai dibaca melalui osm_values (huruf kecil/list/string list) dan pemisah
titik koma. Jika edge gabungan mengandung permissive, penalti dikenakan pada
seluruh panjang edge karena panjang bagian per way belum tersedia pada action.
Ini pendekatan konservatif yang harus disebut saat menafsirkan panjang akses.
Komponen access dicatat pada info/train_step dan dicetak saat verbose=True,
termasuk nol pada kasus tanpa action. Metadata eksperimen menyimpan koefisien,
aturan gabungan, serta penanda/daftar/kebijakan blacklist aktif.

Notebook A--C memakai grup `surface_width_3m_20261102`, dengan empat konfigurasi
serta lima seed yang sama. Pengguna menyelesaikan training; hasil pada 8.2.2.
Hasil lama tetap arsip. Jika menguji efek koefisien akses saja, graf/mask/seed
harus sama; hasil lintas perubahan surface/width bukan isolasi koefisien akses.
Notebook verifikasi ditunda dan acuan numeriknya masih konfigurasi lama.

Nilai **0,50** adalah titik netral. Jika comfort edge tepat 0,50, reward edge bernilai 0. Edge di atas 0,50 memberi reward positif; edge di bawah 0,50 memberi reward negatif. Dengan demikian agen tidak hanya mengejar ruas yang panjang, tetapi mengejar ruas panjang yang kualitasnya lebih baik dari netral.

Panjang edge digunakan agar reward merepresentasikan **berapa jauh** agen menikmati atau melewati ruas tersebut. Jika panjang tidak digunakan, edge 10 m dan edge 100 m dengan comfort sama akan memberi reward sama, padahal pengaruhnya terhadap keseluruhan rute berbeda.

Pembagi **100** berarti reward dinyatakan dalam skala per 100 meter. Ini adalah parameter skala, bukan aturan baku matematika. Tujuannya menjaga reward per edge tetap kecil dan sebanding dengan reward terminal seperti bonus sukses `+80` serta penalti `-50`. Tanpa pembagi 100, sebuah edge 100 m dengan comfort 0,80 akan memberi reward `0,30 × 100 = 30`; nilai ini terlalu besar dibanding bonus sukses dan dapat membuat agen lebih mengejar comfort lokal daripada menyelesaikan loop.

Simulasi reward edge dengan comfort 0,80:

| Panjang edge | Perhitungan | Reward edge |
|---:|---|---:|
| 20 m | `(0,80 − 0,50) × 20 ÷ 100` | `+0,06` |
| 50 m | `(0,80 − 0,50) × 50 ÷ 100` | `+0,15` |
| 100 m | `(0,80 − 0,50) × 100 ÷ 100` | `+0,30` |
| 200 m | `(0,80 − 0,50) × 200 ÷ 100` | `+0,60` |

Lima edge masing-masing 20 m dan comfort 0,80 memberi total `5 × 0,06 = +0,30`, sama dengan satu edge 100 m dengan comfort yang sama. Ini alasan utama reward dikalikan panjang: pemecahan satu ruas jalan menjadi banyak edge tidak mengubah total reward secara material.

Pengurangan `0,50` pada rumus comfort adalah **titik netral**, bukan batas nyaman atau tidak nyaman yang berasal dari survei pelari. Karena comfort score berada pada rentang 0--1, pengurangan ini membuat edge dengan skor tepat 0,50 memberi reward nol; skor di atasnya positif dan skor di bawahnya negatif. Tanpa pengurangan tersebut, edge dengan comfort rendah tetap selalu memberi reward positif hanya karena panjangnya bertambah. Contoh edge 100 m dengan comfort 0,35 adalah:

    tanpa titik netral: 0,35 × 100 / 100 = +0,35
    dengan titik netral: (0,35 - 0,50) × 100 / 100 = -0,15

Sebagai ilustrasi skala total, rute 5.000 m dengan comfort rata-rata 0,68 menghasilkan reward comfort sekitar:

    (0,68 - 0,50) × 5.000 / 100 = +9

Nilai `+9` adalah jumlah reward karakter ruas jika mean comfort berbobot panjang tepat 0,68 dan panjang total tepat 5.000 m. Total reward episode masih memasukkan akses, arah, revisit, dan terminal/buntu; return terdiskonto untuk Q juga berbeda dari jumlah reward tanpa diskonto.

Setelah agen menempuh minimal 50% target, atau 2.500 m, diberikan reward arah pulang:

    r_return = 0,40 × (distance_before − distance_after) ÷ 100

distance before dan distance after adalah jarak Euclidean meter terhadap start. Jika agen mendekat ke start, reward arah pulang bernilai positif. Ini hanya shaping signal; bukan jarak rute sebenarnya.

Sebelum 50% target, agen tidak diberi bonus karena menjauh dari start. Namun, bila sebuah action membuatnya mendekati start terlalu awal, diberlakukan penalti ringan:

    r_early_inward = -0,40 × (distance_before − distance_after) ÷ 100

Penalti ini hanya diterapkan jika `distance_after < distance_before` dan fase action dimulai sebelum 2.500 m. Agen tetap boleh memilih action tersebut; aturan ini bukan action mask. Pendekatan ini dipilih agar comfort edge yang tinggi tidak terlalu mudah menarik agen kembali ke area start pada fase awal, tanpa memberi dorongan berlebihan untuk menjauh sampai berisiko `over_distance`.

Contoh: pada jarak rute 1.800 m, agen melewati edge dengan reward comfort `+0,25`, tetapi posisi akhirnya 50 m lebih dekat ke start. Penalti fase awal adalah `-0,40 × 50 ÷ 100 = -0,20`, sehingga total reward action menjadi `+0,05` sebelum komponen lain.

| Parameter | Nilai | Kondisi |
|---|---:|---|
| SUCCESS_BONUS | +80 | Loop valid. |
| OVER_DISTANCE_PENALTY | -50 | Jarak melebihi 5.500 m. |
| NO_ACTION_PENALTY | -45 | Tidak ada action legal. |
| STEP_LIMIT_PENALTY | -40 | Mencapai 220 langkah. |
| REVISIT_PENALTY | -8 | Revisit node selain start. |
| PERMISSIVE_PENALTY_PER_100M | -0,10 | Per 100 meter edge yang mengandung access permissive. |
| OUTWARD_PENALTY_SCALE | 0,40 | Skala penalti bila, sebelum 2.500 m, action membuat agen mendekati start. |

Nilai reward dapat dituning, tetapi setiap perubahan reward harus dievaluasi ulang pada seluruh A–C dengan seed sama.

### 7.1.1 Dasar skala koefisien arah = 0,40

Koefisien `0,40` pada reward arah dan penalti bergerak menuju start terlalu awal bukan nilai standar Q-Learning. Nilai ini adalah konfigurasi yang menentukan seberapa besar perubahan jarak lurus dihargai atau diberi penalti. Untuk perubahan jarak lurus sebesar 100 m, nilai ini menghasilkan:

    0,40 × 100 / 100 = 0,40

Artinya, setelah fase pulang dimulai, bergerak 100 m lebih dekat ke start memberi `+0,40`. Sebelum fase pulang, bergerak 100 m lebih dekat ke start memberi `-0,40`. Nilai ini membuat arah perjalanan menjadi sinyal tambahan yang nyata di samping comfort, tanpa mendekati bonus terminal `+80`.

Koefisien `0,40` **tidak selalu lebih besar** daripada reward comfort. Sebagai contoh, edge 100 m dengan comfort 0,68 memberi `+0,18`, sehingga pada contoh tersebut reward arah 100 m lebih besar. Namun edge 100 m dengan comfort 1,00 memberi `+0,50`, sehingga reward comfort lebih besar. Oleh karena itu, dokumentasi tidak mengklaim bahwa koefisien arah selalu mendominasi comfort; keduanya sengaja digabungkan sebagai sinyal pembelajaran yang berbeda.

### 7.1.2 Dasar skala bonus berhasil = +80

Nilai `+80` bukan nilai standar Q-Learning dan bukan berasal dari data OSM. Nilai ini adalah parameter desain agar keberhasilan loop valid menjadi tujuan utama. Dasar numeriknya dapat dilihat dari batas atas konservatif reward positif non-terminal pada rute valid.

**Batas atas reward comfort.** Comfort score berada pada rentang 0--1, sehingga nilai positif terbesar per 100 m adalah `(1,00 - 0,50) = 0,50`. Rute valid paling panjang adalah 5.500 m. Dengan demikian:

    R_comfort maksimum = 0,50 × 5.500 / 100 = +27,5

**Batas atas reward arah.** Setelah fase pulang, reward arah menjumlahkan perubahan jarak lurus. Bila agen bergerak menjauh, nilai perubahan menjadi negatif dan mengurangi akumulasi reward arah. Karena jarak lurus awal fase pulang secara konservatif tidak dapat melebihi total panjang rute valid 5.500 m, batas atas yang sengaja dibuat longgar adalah:

    R_arah maksimum = 0,40 × 5.500 / 100 = +22

Dengan demikian, batas atas akumulasi reward positif comfort dan arah adalah:

    R_nonterminal maksimum = +27,5 + +22 = +49,5

Bonus keberhasilan memenuhi:

    +80 > +49,5

Dengan bukti batas ini, bonus `+80` lebih besar daripada akumulasi positif comfort dan arah yang mungkin diperoleh pada rute valid. Selisihnya adalah `80 - 49,5 = 30,5`. Pada dua rute yang sama-sama valid, keduanya menerima bonus `+80` yang sama; perbedaan comfort dan arah tetap digunakan untuk membedakan kualitas kedua rute tersebut.

Pernyataan bahwa `+80` "tidak terlalu besar" bukan fakta matematis dan tidak diklaim sebagai nilai optimal. Yang dapat dinyatakan adalah bahwa `+80` menciptakan hierarki reward yang jelas: keberhasilan loop memberi sinyal terminal terbesar, sedangkan comfort dan arah tetap menjadi komponen pembeda. Sensitivitas terhadap nilai bonus hanya dapat dibuktikan melalui eksperimen ulang dengan konfigurasi lain.

### 7.1.3 Dasar penalti terminal dan revisit

Seluruh penalti berikut adalah konfigurasi operasional, bukan nilai standar universal. Nilai dipilih untuk memberi konsekuensi negatif pada hasil yang tidak memenuhi syarat loop, sambil tetap membedakan jenis kegagalan dan tidak melarang revisit sepenuhnya.

| Parameter | Nilai | Dasar penggunaan |
|---|---:|---|
| `OVER_DISTANCE_PENALTY` | -50 | Rute yang melampaui 5.500 m tidak lagi memenuhi batas valid. Nilai ini paling besar di antara penalti kegagalan karena target jarak sudah terlewati. Kontras terminal terhadap sukses adalah `+80 - (-50) = 130`. |
| `NO_ACTION_PENALTY` | -45 | Agen tidak memiliki edge legal untuk melanjutkan rute. Nilainya dekat dengan -50 agar kondisi buntu tetap jelas merupakan kegagalan, tetapi sedikit lebih kecil karena tidak selalu berarti rute telah melewati batas jarak. |
| `STEP_LIMIT_PENALTY` | -40 | Agen belum membentuk loop setelah 220 langkah. Nilainya tetap negatif, tetapi sedikit lebih kecil karena kondisi ini membatasi episode yang terlalu panjang, bukan pelanggaran langsung terhadap batas jarak. |
| `REVISIT_PENALTY` | -8 | Revisit dibutuhkan sebagai opsi pulang setelah 50% target, sehingga tidak dilarang. Penalti ini membuat pengulangan node kurang menarik dibanding memilih edge baru, tetapi tetap memungkinkan agen kembali melalui jaringan yang telah dilalui. |

Untuk `REVISIT_PENALTY = -8`, tidak ada pembuktian bahwa angka tersebut optimal. Dasarnya adalah fungsi perilaku: penalti harus cukup terlihat dibanding reward comfort per edge yang umumnya kecil, agar agen tidak membentuk putaran pendek berulang, tetapi revisit tetap tersedia melalui action mask pada fase pulang. Nilai ini harus dianggap sebagai hyperparameter dan hanya boleh diubah melalui eksperimen terkontrol pada semua scenario serta seed yang sama.

### 7.2 Epsilon-greedy

**choose_action()** memilih action legal secara acak dengan peluang epsilon; selain itu ia memilih Q-value terbesar. Bila nilai Q terbaik seri, salah satu action terbaik dipilih secara acak.

Core menyediakan dua mode jadwal epsilon. Nilai `epsilon_decay_episodes` bersifat **opsional**.

1. Bila nilainya `None`, mode lama dipakai: epsilon turun selama seluruh jumlah episode training (`K = N`).
2. Bila nilainya diisi, misalnya `50.000`, epsilon hanya turun selama 50.000 episode pertama (`K = 50.000`), lalu tetap pada 0,05.

Secara umum nilai epsilon per episode dihitung dengan:

    progress = min(episode ÷ (K − 1), 1)
    epsilon = 0,05 + (1,00 − 0,05) × (1 − progress)

`K` adalah lama fase penurunan epsilon. Evaluasi greedy memakai epsilon 0 agar policy yang diuji tidak mengandung eksplorasi acak.

Satu nilai epsilon dipakai untuk seluruh action di dalam satu episode. Artinya pada episode awal agen sangat sering mengeksplorasi action legal secara acak; seiring episode bertambah, agen makin sering memakai Q-value terbaik yang sudah dipelajari.

Simulasi nilai epsilon pada eksperimen `EPISODES=40.000`:

| Episode (dimulai dari 0) | Epsilon kira-kira | Makna |
|---:|---:|---|
| 0 | 1,000 | Hampir setiap pemilihan action bersifat acak. |
| 10.000 | 0,762 | Eksplorasi masih dominan, tetapi Q-value mulai lebih sering dipakai. |
| 20.000 | 0,525 | Eksplorasi dan eksploitasi seimbang secara kasar. |
| 39.999 | 0,050 | Hanya sekitar 5% peluang action acak. |

Pada akhir fase decay, apabila ada tiga action legal, agen masih memiliki sekitar 5% peluang memilih salah satu action secara acak. Saat evaluasi greedy, epsilon dipaksa menjadi 0 sehingga agen selalu memilih action legal dengan Q-value tertinggi; hasil evaluasi tidak dipengaruhi eksplorasi acak.

#### Seed dan pengacakan yang dapat diulang

Walaupun Q-Learning memerlukan pilihan acak, hasil eksperimen perlu dapat diuji ulang. Karena itu setiap training membuat generator angka acak NumPy dengan:

    rng = np.random.default_rng(seed)

`seed` adalah angka awal pembentuk urutan pseudoacak, bukan nilai yang menghilangkan pengacakan. Generator ini dipakai ketika `choose_action()` memilih action legal secara acak pada eksplorasi epsilon-greedy dan ketika beberapa action memiliki Q-value terbaik yang sama. Dengan graf, kode, konfigurasi, dan seed yang sama, urutan pilihan acak pada training seharusnya sama sehingga hasil dapat direproduksi.

Pengaruh seed terhadap rute terjadi **secara bertahap melalui pemilihan edge**, bukan dengan memilih satu rute lengkap secara langsung. Pada setiap langkah training, generator dipakai dua kali ketika eksplorasi terjadi:

    if rng.random() < epsilon:
        action = actions[int(rng.integers(len(actions)))]

`rng.random()` menentukan apakah agen melakukan eksplorasi. Jika ya, `rng.integers(len(actions))` memilih indeks salah satu action legal. Dalam graf proyek ini, satu action adalah edge spesifik `(next_node, key)`, sehingga pengacakan tersebut benar-benar dapat menentukan ruas jalan berikutnya yang dipilih agen. Action acak pada langkah awal dapat membawa agen ke node berbeda; akibatnya daftar action legal, reward yang diterima, pembaruan Q-value, dan rute pada langkah berikutnya juga dapat berbeda.

Dengan seed yang sama, kedua nilai pseudoacak tersebut muncul dalam urutan yang sama saat training diulang. Karena graf, daftar action legal, dan aturan environment juga sama, agen biasanya memilih edge eksplorasi yang sama dan memperoleh rute hasil training yang sama. Jika seed diubah, urutan eksplorasi dapat berubah; rute akhirnya dapat berbeda, meskipun tidak harus selalu berbeda apabila kebijakan greedy yang dipelajari akhirnya mengarah ke rute dominan yang sama. Ketika agen tidak mengeksplorasi, action dipilih berdasarkan Q-value tertinggi, bukan melalui `rng.integers()`; pengecualian hanya terjadi bila beberapa Q-value tertinggi seri.

Contoh sederhana: training dengan `seed=0` yang dijalankan dua kali akan menerima urutan angka pseudoacak yang sama, sehingga pilihan eksplorasi dan hasilnya dapat sama persis. Training dengan `seed=1` memakai urutan pseudoacak lain sehingga jalur eksplorasinya dapat berbeda. Dengan kata lain, hasil yang sama ketika notebook dijalankan ulang bukan berarti Q-Learning tidak menggunakan pengacakan; pengacakan tersebut sengaja dikendalikan agar dapat direproduksi.

Eksperimen memakai lima seed, yaitu `(0, 1, 2, 3, 4)`. Seed yang berbeda menghasilkan pola eksplorasi berbeda; sebab itu keberhasilan yang muncul pada seluruh seed lebih meyakinkan daripada keberhasilan pada satu seed saja. Evaluasi greedy menggunakan generator terpisah `np.random.default_rng(seed + 100_000)`. Epsilon evaluasi bernilai 0, tetapi generator tersebut masih diperlukan bila terjadi seri Q-value terbaik; offset `100.000` memisahkan urutan acak evaluasi dari urutan acak training.

### 7.3 Rumus update

Blok satu langkah pada `train_q_learning()` dipisahkan menjadi `train_step(environment, q_table, rng, epsilon, action=None, verbose=False)`. Fungsi ini membaca `environment.latest_state`, memilih action, menjalankan transisi, menangani penalti buntu, dan memperbarui Q. Training serta notebook memakai fungsi yang sama. Property `latest_state` memanggil `build_state()` tanpa menyimpan salinan state. `RunningRouteEnvironment.step()` tetap seperti semula; tidak ada class tambahan.

    Q(s, a) = Q(s, a)
            + alpha × [reward + gamma × max Q(s_baru, a_baru) − Q(s, a)]

Nilai masa depan hanya dicari dari action legal pada state berikutnya. Jika episode selesai atau tidak ada action legal, nilai masa depan adalah 0.

## 8. Konfigurasi Training dan Grafik

| Parameter | Nilai | Makna |
|---|---:|---|
| ALPHA | 0,15 | Laju pembaruan Q-value. |
| GAMMA | 0,95 | Bobot reward masa depan. |
| EPSILON_START | 1,00 | Eksplorasi awal. |
| EPSILON_END | 0,05 | Eksplorasi akhir. |
| EPISODES | 10.000 | Default cepat untuk satu kali uji notebook. Eksperimen mengirim jumlah episode secara eksplisit. |
| epsilon_decay_episodes | None atau 50.000 | None mempertahankan jadwal dinamis lama; 50.000 dipakai pada eksperimen durasi training dengan epsilon decay tetap. |
| MAX_STEPS_PER_EPISODE | 220 | Batas langkah per episode. |
| SEEDS | (0, 1, 2, 3, 4) | Lima seed eksperimen. |
| ROLLING_WINDOW | 50 | Ukuran rata-rata bergerak untuk menghaluskan tren grafik. |

Setiap scenario melatih lima Q-table, satu untuk setiap seed. Untuk grafik training, nilai lima seed pada episode yang sama dirata-ratakan terlebih dahulu, kemudian dihaluskan dengan rata-rata bergerak 50 episode. Evaluasi greedy tetap dicatat per seed.

### 8.1 Diagnosis TD-error

Selama training, setiap pembaruan Q menghitung **TD-error** (Temporal Difference error), yaitu selisih antara target nilai Q dan nilai Q lama.

    TD-error = reward + gamma × nilai Q terbaik pada state berikutnya − nilai Q lama

Notebook menyimpan `mean_abs_td_error`, yaitu rata-rata nilai absolut TD-error dari seluruh update Q dalam satu episode. Nilai absolut dipakai agar perubahan naik dan turun tidak saling meniadakan. Grafik diagnosis menampilkan rata-rata bergerak 50 episode dari lima seed.

TD-error yang semakin kecil dan mendatar menunjukkan bahwa nilai Q pada state-action yang **dikunjungi** makin sedikit berubah. Namun, nilai kecil tidak membuktikan rute sudah baik: agen dapat stabil pada policy yang tetap gagal menutup loop. Oleh karena itu, TD-error adalah metrik diagnosis stabilitas pembelajaran, bukan metrik evaluasi utama; tetap baca bersama evaluasi greedy, `is_loop`, jarak akhir ke start, dan peluang closing action tersedia.

Kolom `steps` juga tetap disimpan pada `training_history_{scenario}.csv` sebagai diagnosis internal. Kolom tersebut tidak ditampilkan sebagai grafik utama karena jumlah langkah dipengaruhi panjang edge dan proses simplifikasi graf. Pada target rute 5 km, langkah lebih sedikit tidak selalu berarti rute lebih baik. Indikator yang relevan bila agen benar-benar terlalu banyak melangkah sudah tersedia melalui terminasi `step_limit`.

### 8.2 Rancangan aktif: empat konfigurasi

Per 29 Oktober 2026, setiap notebook A--C menguji dua jumlah episode dengan dua
strategi epsilon. Rumusan masalah nomor 2 mengenai pengaruh representasi state
tetap dipertahankan; state dibandingkan pada kondisi training yang sama.

| Strategi epsilon | Total episode per seed | Horizon penurunan |
|---|---:|---:|
| Dinamis | 75.000 | 75.000 (`epsilon_decay_episodes=None`) |
| Dinamis | 150.000 | 150.000 (`epsilon_decay_episodes=None`) |
| Horizon tetap | 75.000 | 50.000 |
| Horizon tetap | 150.000 | 50.000 |

Training total 50k dan 100k dikeluarkan dari notebook aktif; dinamis 150k ditambahkan.
Setiap konfigurasi melatih ulang seed `(0,1,2,3,4)` dari Q-table kosong. Beban satu
scenario 20 training/2.250.000 episode, total A--C 60 training/6.750.000 episode.
Graf, reward, mask, dan parameter lain tetap sama. Evaluasi akhir greedy (`epsilon=0`).

`RESULT_GROUP="surface_width_3m_20261102"` pada cell pemuatan graf harus sama di
A/B/C. Artefak memakai subfolder `<RESULT_GROUP>/dinamis_<jumlah>_<scenario>` atau
`<RESULT_GROUP>/tetap_50000_episode_<jumlah>_<scenario>` di folder hasil training.
Hasil sebelumnya, termasuk grup lima konfigurasi, tetap disimpan. Untuk menyimpan
run berikutnya terpisah, ubah RESULT_GROUP secara sama di A/B/C.

Cell tampilan hasil tetap terpisah dari training. Ringkasan dinamis dan horizon
50k masing-masing membaca dua titik (75k/150k), sehingga perbandingan strategi
tersedia pada kedua anggaran episode. Output notebook dibersihkan untuk mencegah
hasil lama terbaca sebagai run baru pada saat konfigurasi disiapkan. Pengguna
kemudian menyelesaikan seluruh training; hasilnya dirangkum di bagian berikut.
Jangan mengisi hasil dinamis 150k dari arsip konfigurasi lain.

### 8.2.1 Arsip baseline empat konfigurasi (29 Oktober 2026)

Sumber: `hasil_bab_4/training_qlearning_5km/konfigurasi_empat_20261029/`.
Angka berikut adalah loop valid saat evaluasi greedy final dari lima seed;
bukan proporsi episode training.

| Strategi epsilon | Total episode | A | B | C |
|---|---:|---:|---:|---:|
| Dinamis | 75.000 | 1/5 | 1/5 | 1/5 |
| Dinamis | 150.000 | 0/5 | 0/5 | 4/5 |
| Horizon 50.000 | 75.000 | 0/5 | 5/5 | 3/5 |
| Horizon 50.000 | 150.000 | 0/5 | 5/5 | 5/5 |

Pada horizon 50k total 150k, B memiliki galat rata-rata 104,28 m, skor karakter
ruas 0,762, dan rata-rata 32.208,4 state Q-table; C masing-masing 160,79 m,
0,726, dan 53.903,4. Keduanya 5/5 sukses. C memiliki simpangan baku galat lebih
kecil (46,14 m vs B 88,73 m), sehingga tidak ada klaim B unggul semua metrik.
B 150k horizon 50k merupakan kandidat utama bila prioritasnya loop, galat,
lalu skor ruas. B 75k tetap alternatif anggaran episode lebih kecil (5/5 sukses,
galat 270,32 m). Kandidat ini dipilih dari hasil eksperimen, bukan bukti optimal.

Pengaruh representasi state bergantung konfigurasi epsilon/durasi. C unggul
keberhasilan pada dinamis 150k, sedangkan B mencapai 5/5 lebih awal pada horizon
50k. Rumusan masalah kedua tetap dapat dijawab melalui perbandingan A--C pada
kondisi training sama. A sempat berhasil 1/5 dinamis 75k; jangan menyebutnya
tidak pernah bisa membentuk loop. Hasil lima seed belum menjamin generalisasi.

Pada 10.000 episode training terakhir konfigurasi horizon 50k total 150k,
keberhasilan B 75,26%, C 64,95%, dan A 1,90%. Angka training mengandung eksplorasi
epsilon 0,05 dan tidak sama dengan evaluasi greedy final. Seluruh 35 evaluasi
gagal tidak pernah memiliki closing action legal: 29 over_distance dan 6 buntu.

Pemeriksaan: 6.750.000 baris history lengkap, jadwal epsilon sesuai, 60 evaluasi
greedy dari Q-table tersimpan menghasilkan metrik/node/action yang sama, dan
prefix history 75k identik pada semua 15 pasangan seed horizon 50k. Training
75k/150k tetap dijalankan dari awal secara terpisah; prefix sama karena seed dan
jadwal sama. Dinamis 75k/150k mengubah durasi sekaligus horizon epsilon, sehingga
perbedaannya bukan efek tambahan episode pada jadwal yang tetap.

Laporan lengkap, tabel per seed, diagnosis akhir, grafik tren, dan catatan
pemeriksaan tersedia di `docs/temp/analisis_empat_konfigurasi_20261029/`.
Tidak ada perubahan core, notebook, reward, mask, snapshot, atau hasil mentah.
Pembahasan notebook verifikasi tetap ditunda; analisis hasil ini tidak menambah
kasus verifikasi. Ekspor GPX dan validasi lapangan belum dilakukan.

### 8.2.2 Hasil aktif surface dan width 3 m (2 November 2026)

Sumber: `hasil_bab_4/training_qlearning_5km/surface_width_3m_20261102/`.
Empat konfigurasi A--C, lima seed, 60 training, 6.750.000 baris history.

| Strategi epsilon | Episode per seed | A | B | C |
|---|---:|---:|---:|---:|
| Dinamis | 75.000 | 0/5 | 0/5 | 5/5 |
| Dinamis | 150.000 | 0/5 | 0/5 | 5/5 |
| Horizon 50k | 75.000 | 1/5 | 1/5 | 5/5 |
| Horizon 50k | 150.000 | 0/5 | 5/5 | 5/5 |

C mencapai 5/5 pada setiap konfigurasi teruji; B 5/5 pada horizon 50k total
150k. A berhasil satu seed horizon 50k total 75k, sehingga tidak selalu gagal.
Pada horizon 50k total 150k, galat B 268,47 m vs C 339,91 m; mean comfort B
0,9034 vs C 0,9193; rata-rata Q-state B 28.103,2 vs C 46.671,6. Tidak ada
klaim satu konfigurasi unggul semua metrik atau berlaku di titik awal lain.

Ada 27 loop valid dengan urutan edge berbeda, bukan jaminan rute berbeda secara
geografis. Seluruhnya masih memuat width <3 m, width tak diketahui dan permissive;
preferensi skor tidak menjadi larangan. Gagal: 29 over_distance dan 4 buntu;
semua kegagalan tidak pernah memiliki closing action legal.

History/epsilon/metadata/manifest lengkap. Semua 60 evaluasi direproduksi dari
Q-table tersimpan: metrik cocok, node/action sama persis. Audit tidak menjalankan
training atau mengubah 228 berkas mentah. Ini reproduksi hasil, bukan pengganti
verifikasi notebook atau validasi lapangan.

Laporan dan CSV per seed: `docs/temp/analisis_surface_width_3m_20261102/`.
Skor/reward dari pemetaan lama tidak langsung sebanding. Perbandingan ke grup
highway lama mengubah surface dan width sekaligus, bukan uji satu faktor.

### 8.3 Arsip hasil sebelum rancangan episode final

Bagian 8.4--8.7 di bawah ini memuat hasil lama pada rentang 10k--400k. Hasil tersebut berguna untuk menjelaskan alasan pemisahan jadwal epsilon, tetapi **tidak boleh dipakai sebagai angka atau kesimpulan final BAB IV**. Untuk pelaporan baru, gunakan hasil empat konfigurasi pada RESULT_GROUP aktif setelah pengguna menjalankannya; angka arsip tidak otomatis menjadi hasil baru.

### 8.4 Arsip sensitivitas Scenario B dengan epsilon dinamis

Hasil berikut berasal dari evaluasi greedy lima seed untuk setiap jumlah episode. Ini adalah catatan eksperimen sementara, bukan hasil final BAB IV.

| Episode | Success rate | Galat jarak rata-rata (m) | Reward rata-rata | Comfort rata-rata | Return progress ratio | Closing action rate |
|---:|---:|---:|---:|---:|---:|---:|
| 10.000 | 0,00 | 539,18 | -85,53 | 0,754 | 0,556 | 0,00 |
| 20.000 | 0,00 | 544,32 | -63,99 | 0,768 | 0,489 | 0,00 |
| 30.000 | 0,00 | 415,38 | -101,51 | 0,761 | 0,496 | 0,00 |
| 40.000 | 0,20 | 299,68 | -56,28 | 0,763 | 0,554 | 0,20 |
| 50.000 | 0,00 | 499,36 | -84,11 | 0,761 | 0,316 | 0,00 |

Pada data ini, 40.000 episode merupakan kandidat terbaik sementara: satu dari lima seed membentuk loop valid, galat jarak paling kecil, dan satu seed memiliki closing action legal. Namun, hasil 50.000 episode turun kembali. Dengan lima seed, satu keberhasilan mengubah rate sebesar 20%, sehingga pola tersebut belum cukup untuk klaim stabil atau untuk menyatakan 50.000 episode lebih buruk secara umum. Comfort relatif stabil; hambatan utama adalah agen jarang mencapai kondisi yang menyediakan closing action.

| Grafik | Arti |
|---|---|
| Rata-rata Keberhasilan 50 Episode Terakhir | Proporsi is_loop True dalam 50 episode terakhir. |
| Rata-rata Reward 50 Episode Terakhir | Rata-rata total reward 50 episode terakhir. Reward naik tidak otomatis berarti loop berhasil. |
| Rata-rata Jarak 50 Episode Terakhir | Rata-rata jarak rute 50 episode terakhir; bandingkan dengan target 5 km dan batas valid. |
| Rata-rata Skor Kenyamanan 50 Episode Terakhir | Rata-rata comfort score rute dalam 50 episode terakhir. |
| Jumlah State Q-table | Jumlah state unik yang memiliki entry Q-table. |
| Nilai Epsilon per Episode | Nilai peluang eksplorasi yang ditetapkan dari 1,00 ke 0,05 per episode; bukan rata-rata hasil episode. |
| Rata-rata Nilai Absolut TD-error 50 Episode Terakhir | Rata-rata besarnya selisih target Q dan Q lama pada update yang terjadi. Makin kecil berarti nilai Q yang dikunjungi makin sedikit berubah; bukan jaminan loop berhasil. |

### 8.5 Arsip epsilon decay tetap Scenario C

Hasil berikut berasal dari evaluasi greedy lima seed dengan `epsilon_decay_episodes=50.000`. Semua eksperimen dimulai ulang dari seed yang sama; untuk seed yang sama, urutan pengalaman hingga suatu episode adalah sama pada 50k, 100k, 200k, dan 400k karena jadwal epsilon juga sama. Dengan demikian, titik 100k, 200k, dan 400k dapat dibaca sebagai checkpoint kebijakan setelah tambahan training, bukan sebagai eksperimen dengan durasi eksplorasi berbeda.

| Total episode | Loop valid | Galat jarak rata-rata (m) | Reward rata-rata | Comfort rata-rata | Return progress rata-rata | Closing action tersedia |
|---:|---:|---:|---:|---:|---:|---:|
| 50.000 | 2/5 | 422,31 | 4,00 | 0,705 | 0,615 | 2/5 |
| 100.000 | 5/5 | 267,31 | 87,08 | 0,699 | 0,786 | 5/5 |
| 200.000 | 5/5 | 264,16 | 86,87 | 0,699 | 0,770 | 5/5 |
| 400.000 | 5/5 | 361,90 | 81,71 | 0,670 | 0,750 | 5/5 |

Pada 50.000 episode, fase penurunan epsilon baru selesai sehingga dua seed saja yang membentuk loop. Mulai 100.000 episode, semua seed membentuk loop valid dan keberhasilan itu tetap muncul pada checkpoint 200.000 serta 400.000 episode. Hal ini adalah bukti empiris bahwa Scenario C mulai stabil dalam **keberhasilan menutup loop** setelah tambahan training dengan epsilon rendah.

Namun, 400.000 episode bukan kandidat durasi terbaik hanya karena semua seed tetap sukses. Galat jarak rata-rata naik menjadi 361,90 m dan comfort rata-rata turun menjadi 0,670. Berdasarkan data ini, **100.000 episode** menjadi kandidat durasi final yang lebih hemat: sudah 5/5 sukses dan metrik kualitasnya hampir sama dengan 200.000 episode. Keputusan final tetap perlu dikonfirmasi dengan menjalankan Scenario A, B, dan C pada konfigurasi epsilon tetap serta jumlah episode 100.000 yang sama.

Sebagai diagnosis, rata-rata nilai absolut TD-error pada 50 episode terakhir dari lima seed berturut-turut adalah 1,224 pada 50k; 0,987 pada 100k; 0,915 pada 200k; dan 0,823 pada 400k. Tren tersebut menurun, sehingga nilai Q pada state-action yang dikunjungi makin sedikit berubah. Nilainya belum perlu dipaksa mencapai nol; TD-error dibaca bersama hasil greedy dan bukan sebagai bukti tunggal stabilitas.

### 8.6 Arsip epsilon decay tetap Scenario B

Hasil Scenario B dengan jadwal epsilon yang sama memperlihatkan pola berbeda dari eksperimen epsilon dinamis sebelumnya.

| Total episode | Loop valid | Galat jarak rata-rata (m) | Reward rata-rata | Comfort rata-rata | Return progress rata-rata | Closing action tersedia |
|---:|---:|---:|---:|---:|---:|---:|
| 50.000 | 0/5 | 499,36 | -84,11 | 0,761 | 0,316 | 0/5 |
| 100.000 | 5/5 | 114,43 | 75,64 | 0,759 | 0,743 | 5/5 |
| 200.000 | 5/5 | 309,77 | 77,50 | 0,767 | 0,747 | 5/5 |
| 400.000 | 5/5 | 340,01 | 78,34 | 0,764 | 0,729 | 5/5 |

Pada 50.000 episode, B belum membentuk loop. Namun setelah tambahan training dengan epsilon tetap 0,05, B mencapai 5/5 loop valid mulai 100.000 episode dan keberhasilan itu bertahan hingga 400.000 episode. Hasil ini menunjukkan bahwa kegagalan B pada eksperimen sebelumnya tidak dapat langsung diklaim semata-mata akibat tidak adanya `previous_node`; durasi eksplorasi yang terlalu panjang merupakan faktor yang sangat berpengaruh.

Untuk checkpoint 100.000 episode, B memiliki galat jarak dan comfort rata-rata lebih baik daripada C, sedangkan C memiliki return progress ratio serta reward rata-rata sedikit lebih tinggi. Karena keduanya sama-sama 5/5 sukses, pemilihan state final harus didasarkan pada tujuan prioritas yang dinyatakan secara eksplisit dan tabel evaluasi lengkap, bukan hanya satu metrik. TD-error B pada 50 episode terakhir adalah 1,749 pada 50k; 0,944 pada 100k; 0,622 pada 200k; dan 0,662 pada 400k. TD-error hanya dibandingkan sebagai tren di dalam scenario B, bukan sebagai angka absolut yang langsung diadu dengan C karena state yang dikunjungi berbeda.

### 8.7 Arsip epsilon decay tetap Scenario A

Scenario A memakai state paling sederhana, yaitu hanya `(current_node)`. Pada jadwal epsilon tetap 50.000 episode, A belum membentuk loop valid pada seluruh durasi yang diuji.

| Total episode | Loop valid | Galat jarak rata-rata (m) | Reward rata-rata | Comfort rata-rata | Return progress rata-rata | Jarak akhir ke start rata-rata (m) | Closing action tersedia |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 50.000 | 0/5 | 546,83 | -86,91 | 0,712 | 0,288 | 1.693,25 | 0/5 |
| 100.000 | 0/5 | 567,17 | -98,44 | 0,714 | 0,441 | 1.047,76 | 0/5 |
| 200.000 | 0/5 | 541,94 | -63,12 | 0,722 | 0,275 | 1.976,09 | 0/5 |
| 400.000 | 0/5 | 551,79 | -49,73 | 0,703 | 0,440 | 1.221,46 | 0/5 |

Pada checkpoint 100.000 episode, seluruh seed A berakhir `over_distance`; tidak satu pun pernah memiliki closing action legal pada evaluasi greedy. Tambahan training hingga 400.000 episode tidak mengubah hasil utama tersebut. TD-error pada 50 episode terakhir berada pada 1,327 (50k), 1,463 (100k), 1,406 (200k), dan 1,208 (400k), sementara keberhasilan training pada jendela yang sama tetap sekitar 0--2%. Ini menunjukkan A belum membentuk policy loop yang berhasil.

Jika dibandingkan pada konfigurasi yang sama—100.000 episode dan epsilon decay tetap 50.000—hasilnya adalah: A 0/5 loop, B 5/5 loop, dan C 5/5 loop. Bukti ini mendukung bahwa informasi progres jarak pada state penting untuk membedakan keputusan saat agen masih membangun rute dan saat harus mulai kembali ke titik start. Sementara itu, `previous_node` pada C dapat memengaruhi kecepatan awal dan trade-off metrik, tetapi pada konfigurasi ini bukan syarat mutlak untuk mencapai loop karena B juga berhasil 5/5.

### 8.8 Cara membaca reward training

Grafik reward training adalah akumulasi seluruh reward comfort, reward/penalti arah pulang, penalti revisit, dan reward terminal dalam episode yang dijalankan dengan kebijakan epsilon-greedy. Karena itu reward tidak wajib selalu naik seiring episode.

Sebagai contoh, episode yang buntu cepat dapat menerima `no_available_action = -45`. Episode lain dapat berjalan lebih jauh, menerima beberapa penalti revisit, lalu berakhir `over_distance = -50`; totalnya dapat lebih rendah, misalnya `-80` atau `-90`. Jadi penurunan reward dapat berarti agen makin sering mengambil rute gagal yang lebih panjang dan lebih mahal, bukan semata-mata kualitas model pasti memburuk.

Reward harus dibaca bersama grafik keberhasilan loop, rata-rata jarak, peluang closing action tersedia, serta termination rate. Bila reward menurun tetapi keberhasilan loop dan closing action meningkat, perlu dilihat trade-off-nya. Bila reward menurun sementara success tetap rendah dan `over_distance`/`no_available_action` tinggi, policy belum menemukan pola loop yang baik.

## 9. Evaluasi, Peta, dan Berkas Hasil

### 9.1 Evaluasi greedy

Fungsi **evaluate_greedy()** memakai epsilon 0. Tabel evaluasi utama sengaja dibatasi agar perbandingan Scenario A--C tetap fokus. Setiap baris mewakili satu seed dan hanya memuat metrik berikut.

Setelah training selesai untuk **setiap seed**, Q-table seed tersebut langsung diuji satu kali oleh `evaluate_greedy()`. Dengan lima seed `(0, 1, 2, 3, 4)`, eksperimen selalu menghasilkan lima evaluasi greedy: satu policy hasil training untuk setiap seed. Pada evaluasi ini `epsilon = 0`, sehingga tidak ada pemilihan action untuk eksplorasi acak; agen memilih action legal dengan nilai Q terbesar. `EPSILON_END = 0,05` hanya digunakan selama training. Bila dua atau lebih action memiliki nilai Q sama, pemilihan tie dilakukan dengan generator acak yang diberi seed tetap (`seed + 100000`) agar hasil evaluasi tetap dapat direproduksi.

| Metrik | Arti |
|---|---|
| is_loop | Keberhasilan utama: kembali ke start pada 4.500–5.500 m. |
| total_distance_m | Total jarak edge pada rute dalam meter. |
| absolute_distance_error_m | Selisih absolut dari target 5.000 m. Bukan pengganti is_loop. |
| total_reward | Akumulasi seluruh reward dan penalti dari satu evaluasi greedy. Dibaca bersama is_loop dan termination_reason, bukan sebagai satu-satunya ukuran kualitas rute. |
| mean_comfort | Rata-rata comfort edge berbobot panjang. Nilai mendekati 1 berarti proporsi panjang rute lebih banyak melewati edge berskor comfort tinggi. |
| distance_to_start_at_end_m | Jarak lurus posisi akhir ke start dalam meter. Makin kecil berarti agen setidaknya mendekati start sebelum terminasi. Ini tidak membuktikan loop karena agen dapat dekat start tanpa kembali ke node start. |
| return_progress_ratio | Proporsi langkah pada fase pulang yang mengurangi jarak lurus ke start. Fase pulang dicatat setelah total jarak mencapai 2.500 m. Nilai mendekati 1 berarti arah pulang lebih konsisten; lihat penjelasan dan contoh pada Bagian 9.2.1. |
| closing_action_available | Bernilai True bila selama evaluasi pernah tersedia edge legal langsung menuju start yang akan menghasilkan total jarak 4.500–5.500 m. Ini menunjukkan kesempatan menutup loop, bukan bukti edge tersebut dipilih. |
| termination_reason | Alasan terminal setiap seed: success, over_distance, no_available_action, atau step_limit. |

Tabel evaluasi utama dan berkas `evaluation_metrics_{scenario}.csv` kini langsung menampilkan `closing_action_available` per seed. Nilai tersebut bersumber dari flag internal `closing_action_was_available`; bernilai True bila selama evaluasi tersedia edge legal langsung ke start dengan proyeksi total jarak 4.500–5.500 m. Nilai True berarti kesempatan menutup loop pernah ada, bukan bahwa edge itu pasti dipilih. Sementara itu, `closing_action_available_rate` serta rate semua tipe terminasi adalah **diagnosis training** yang tetap ditampilkan pada grafik diagnosis.

### 9.1.1 Rumus termination rate

Untuk setiap tipe terminasi, rate dihitung dengan rumus berikut.

    termination_rate(tipe) = jumlah episode dengan tipe tersebut ÷ jumlah seluruh episode

Contoh: bila 3.750 dari 12.500 episode training berakhir karena `over_distance`, maka termination rate `over_distance` adalah 3.750 ÷ 12.500 = 0,30 atau 30%. Pada evaluasi greedy, penyebutnya hanya lima karena satu evaluasi dilakukan untuk masing-masing seed.

### 9.1.2 Grafik yang ditampilkan notebook scenario

Workflow `run_scenario_experiment()` telah menjalankan `evaluate_greedy()` untuk setiap Q-table. Hasilnya langsung dimasukkan ke tabel evaluasi utama, termasuk `closing_action_available`; tidak diperlukan cell evaluasi tambahan. Selain tabel evaluasi, notebook menampilkan dua gambar berikut.

1. **Grafik training utama**: keberhasilan loop, reward, jarak, mean comfort, jumlah state Q-table, dan epsilon. Semuanya selain epsilon memakai rata-rata bergerak 50 episode.
2. **Grafik diagnosis training**: rata-rata jarak akhir ke start, return progress ratio, closing action available rate, rata-rata nilai absolut TD-error, dan lima termination rate. Seluruh panel memakai rata-rata bergerak 50 episode dari lima seed; termination rate ditempatkan pada panel yang sama, bukan sebagai gambar tersendiri.

Grafik diagnosis menggunakan data `training_history_{scenario}.csv`, sehingga menunjukkan perubahan selama training, bukan hanya angka akhir. Nilai kosong pada `return_progress_ratio` terjadi bila episode belum pernah mencapai fase kembali, yaitu 50% dari target (2.500 m); rata-rata hanya dihitung dari episode yang memasuki fase tersebut.

Tidak ada baseline Dijkstra. Perbandingan eksperimen hanya A vs B vs C, dengan lingkungan yang sama.

### 9.1.3 Cara membaca kelompok metrik evaluasi

Metrik evaluasi tidak memiliki peran yang sama. `is_loop` adalah keputusan keberhasilan utama untuk satu seed, sedangkan `success_rate_greedy` merangkum berapa dari lima seed yang berhasil. `total_distance_m` dan `absolute_distance_error_m` menjelaskan kedekatan jarak rute terhadap target 5 km, tetapi rute dengan galat kecil tetap gagal apabila tidak kembali ke node start.

`mean_comfort` menjelaskan karakter ruas yang dilalui rute; `total_reward` hanya menjadi indikator pendukung karena nilainya merupakan gabungan reward comfort, arah perjalanan, penalti revisit, dan reward atau penalti terminal. Oleh sebab itu, total reward tidak boleh dipakai sendirian untuk menyatakan sebuah rute lebih baik.

Tiga metrik berikut membantu mendiagnosis kegagalan pulang: `distance_to_start_at_end_m` menunjukkan seberapa jauh posisi akhir dari start, `return_progress_ratio` menunjukkan konsistensi arah pulang setelah fase pulang dimulai, dan `closing_action_available` menunjukkan apakah agen pernah memiliki kesempatan legal untuk langsung menutup loop. Ketiganya tetap metrik pendukung; rute hanya dinyatakan berhasil ketika `is_loop=True`.

`termination_reason` menjelaskan akhir episode. Contohnya, `over_distance` berarti total jarak telah melewati 5.500 m sebelum agen kembali valid ke start, sedangkan `no_available_action` berarti action mask tidak lagi menyediakan edge legal pada state tersebut.

### 9.2 Cara membaca mean_comfort

`mean_comfort` adalah skor comfort keseluruhan rute. Nilainya dihitung sebagai jumlah setiap **comfort edge × panjang edge**, kemudian dibagi total panjang rute. Karena itu edge panjang memberi pengaruh lebih besar daripada edge pendek.

    mean_comfort = jumlah(comfort_edge × panjang_edge) ÷ jumlah(panjang_edge)

Simulasi:

| Edge | Panjang | Comfort |
|---|---:|---:|
| A | 100 m | 0,80 |
| B | 900 m | 0,60 |

Perhitungannya adalah `(100 × 0,80 + 900 × 0,60) ÷ (100 + 900) = 0,62`. Hasil ini berbeda dari rata-rata biasa `(0,80 + 0,60) ÷ 2 = 0,70`, karena rata-rata biasa keliru menganggap edge 100 m dan 900 m sama pentingnya.

Semakin `mean_comfort` mendekati 1, semakin besar bagian panjang rute yang melewati edge dengan comfort score tinggi. Semakin mendekati 0, semakin banyak panjang rute melalui edge dengan skor rendah. Interpretasi ini tetap terbatas pada proxy OSM; nilai 0,90 tidak berarti pelari pasti menilai rute sangat nyaman atau aman.

### 9.2.1 Cara membaca return_progress_ratio

`return_progress_ratio` digunakan untuk menjawab pertanyaan: **setelah agen memasuki fase pulang, seberapa konsisten langkahnya benar-benar mendekati titik awal?** Metrik ini tidak mengukur kenyamanan maupun keberhasilan loop secara langsung. Metrik ini hanya membaca arah gerak relatif terhadap start.

    return_progress_ratio = return_progress_steps ÷ return_phase_steps

Data pembentuknya disimpan oleh environment pada setiap action sebagai berikut.

1. Sebelum action dijalankan, environment menghitung `distance_before`, yaitu jarak lurus dari node saat ini ke start.
2. Setelah action dijalankan, environment menghitung `distance_after`, yaitu jarak lurus dari node tujuan ke start.
3. Bila total jarak rute **setelah action** sudah minimal 2.500 m, action tersebut dihitung sebagai satu `return_phase_steps`.
4. Bila pada action tersebut `distance_after < distance_before`, action juga dihitung sebagai satu `return_progress_steps`.

Dengan demikian, pembilang menghitung jumlah langkah yang mendekati start dan penyebut menghitung seluruh langkah dalam fase pulang. Metrik ini menghitung **jumlah langkah**, bukan besar perubahan jaraknya. Sebuah langkah yang mendekat 2 m dan langkah yang mendekat 100 m sama-sama menambah pembilang satu kali.

Contoh: setelah total jarak mencapai 2.500 m, agen melakukan lima action dengan jarak lurus terhadap start berikut.

| Action fase pulang | `distance_before` | `distance_after` | Mendekati start? |
|---:|---:|---:|---|
| 1 | 500 m | 440 m | Ya |
| 2 | 440 m | 470 m | Tidak |
| 3 | 470 m | 400 m | Ya |
| 4 | 400 m | 410 m | Tidak |
| 5 | 410 m | 350 m | Ya |

Pada contoh tersebut, `return_phase_steps = 5` dan `return_progress_steps = 3`. Maka:

    return_progress_ratio = 3 ÷ 5 = 0,60

Nilai 0,60 berarti 60% action pada fase pulang bergerak mendekati start. Nilai 1,00 berarti seluruh action fase pulang mendekati start, sedangkan nilai 0,00 berarti tidak ada action fase pulang yang mendekati start. Bila episode berakhir sebelum total jarak mencapai 2.500 m, penyebutnya nol sehingga implementasi menyimpan nilai `NaN` atau kosong; nilai ini tidak diperlakukan sebagai nol saat rata-rata grafik dihitung.

Nilai tinggi belum tentu berarti loop valid. Agen dapat selalu bergerak mendekati start tetapi berhenti di node yang dekat dengan start, memilih edge yang salah, atau melewati batas jarak sebelum kembali tepat ke node awal. Karena itu `return_progress_ratio` harus dibaca bersama `is_loop`, `distance_to_start_at_end_m`, `closing_action_available`, dan `termination_reason`.

### 9.3 Peta interaktif

**make_route_map()** menampilkan satu rute representatif dari lima hasil evaluasi greedy (satu hasil untuk setiap seed), bukan dari episode training. Fungsi **select_representative_trial()** menentukan Q-table/seed yang dipakai dengan aturan berikut.

1. Bila ada satu atau lebih `is_loop=True`, pilih hanya dari kelompok loop valid: `absolute_distance_error_m` terkecil, kemudian `mean_comfort` tertinggi, lalu `return_progress_ratio` tertinggi.
2. Bila belum ada loop valid, pilih rute dengan `absolute_distance_error_m` terkecil, kemudian `distance_to_start_at_end_m` terkecil, lalu `mean_comfort` dan `return_progress_ratio` tertinggi. Urutan ini mencegah rute yang berhenti terlalu dini tetapi kebetulan dekat start terpilih sebagai peta. Dalam kondisi ini peta adalah alat diagnosis, bukan contoh rute final yang berhasil.

Notebook mencetak scenario, seed, nilai seluruh metrik utama, dan alasan pemilihan sebelum peta ditampilkan. Karena itu seed pada peta tidak selalu seed 0 dan pengguna dapat memverifikasi alasan rute tersebut dipilih. `revisit_count` tidak digunakan sebagai kriteria pemilihan peta. Peta memakai warna berbeda per kilometer dan memuat marker start KM 0, marker KM 1–5, serta marker finish terpisah.

Jika rute valid loop, marker finish digeser sedikit untuk tampilan agar tidak menumpuk marker start. Posisi logis finish tetap sama dengan start. Peta representatif bukan rata-rata lima seed; peta hanya alat inspeksi rute terbaik menurut aturan prioritas.

### 9.4 Status dan pembaruan hasil

Ringkasan angka di wiki diberi tanggal dan RESULT_GROUP. CSV pada grup terkait tetap sumber utama; angka arsip tidak menjadi hasil terbaru ketika konfigurasi reward, action mask, jumlah episode, atau epsilon berubah. Gunakan `evaluation_metrics_A.csv`, `evaluation_metrics_B.csv`, dan `evaluation_metrics_C.csv` yang dihasilkan dari **satu konfigurasi yang sama** sebagai sumber tabel BAB IV. Untuk eksperimen sensitivitas episode, jangan mencampurkan CSV epsilon dinamis dengan CSV pada folder `sensitivitas_epsilon_tetap_50000_episode_<jumlah>_<scenario>`.

Sebelum membuat tabel perbandingan A--C, pastikan ketiga scenario sudah dijalankan ulang dengan konfigurasi final dan lima seed yang sama. Ringkasan BAB IV hanya memakai `is_loop`, `total_distance_m`, `absolute_distance_error_m`, `total_reward`, `mean_comfort`, `return_progress_ratio`, `distance_to_start_at_end_m`, `closing_action_available`, dan `termination_reason`; `revisit_count` tidak dipakai sebagai metrik evaluasi utama.

## 10. Aturan Modifikasi dan Konteks untuk AI

Saat membuat perubahan:

1. Ubah satu komponen eksperimen pada satu waktu, misalnya reward kembali atau jumlah progress bin.
2. Jangan mengubah reward/action mask bersamaan dengan definisi state jika ingin membandingkan A–C secara adil.
3. Setelah perubahan yang memengaruhi environment, reward, action, atau training, jalankan ulang seluruh A–C dengan lima seed yang sama.
4. Simpan hasil baru pada direktori berbeda atau beri nama konfigurasi agar CSV lama tidak tertimpa tanpa jejak.
5. Perbarui wiki ini jika parameter, rumus reward, action mask, metrik, atau status hasil berubah.
6. Jangan mengklaim sistem berhasil sebelum is_loop True muncul secara konsisten pada evaluasi greedy.
7. Jangan mengklaim comfort score sebagai pengalaman pelari yang tervalidasi tanpa validasi lapangan atau survei.

Ringkasan singkat: proyek menggunakan Q-Learning tabular dari scratch pada graf jalan kaki OSMnx MultiDiGraph terproyeksi meter. Target adalah loop 5 km plus toleransi 10%. Action adalah edge spesifik (next_node, key). State final yang diuji A sampai C berbeda pada informasi posisi, progres, dan arah kedatangan. Revisit tersedia mulai 50% target dengan maksimum dua kunjungan node; fase ini sama dengan awal reward arah pulang. Semua aturan bersama berada di rute_lari_core.py; analisis berada di analisa.ipynb; eksperimen dipisahkan pada scenario_A.ipynb sampai scenario_C.ipynb. Hasil yang dilaporkan selalu berasal dari evaluasi greedy per seed.


## 11. Verifikasi implementasi

**Status 2 November 2026:** uraian angka contoh dan kelulusan di bawah merekam
notebook versi 29 Oktober. Assertion/output belum disesuaikan dengan perubahan
highway, surface, width, reward akses dan blacklist. Jangan menyatakan notebook
lulus pada konfigurasi terbaru; rencana tinjauan ada di dokumen pendamping.

`verifikasi.ipynb` membuat `nx.MultiDiGraph` sintetis dengan CRS EPSG:32749, atribut
node `x`/`y`, serta edge `length`, `highway`, `surface`, `width`, dan `osmid`
sintetis positif (101–104). `core.add_comfort_scores(G)` menghitung skor, lalu
`core.build_actions(G)` membentuk action seperti implementasi utama; dua key
paralel tetap menjadi dua action berbeda. Tidak ada skor yang ditetapkan langsung.

Cell setelah pembentukan graf menggambarkan `G` melalui `nx.draw_networkx()` dan
`nx.draw_networkx_edge_labels()`. Panah memperlihatkan arah, lengkung memisahkan
dua edge paralel, dan label memuat key, panjang, serta skor ruas. Gambar merupakan
skema konektivitas; lengkung bukan geometri jalan sebenarnya.

Notebook memuat dua episode pada lintasan 0 → 1 → 2 → 0,
panjang ruas 1.700 + 1.700 + 1.600 = 5.000 m. Dua action paralel 0 → 1
memiliki skor 0,80625 (residential/asphalt/3 m) dan 0,620625
(service/paving_stones/2 m) agar epsilon-greedy memiliki alternatif.
Koordinat node memakai meter; panjang ruas merupakan input perjalanan tersendiri,
bukan panjang garis lurus. Contoh ini tidak memerlukan snapshot OSM.

Satu cell menjalankan satu `train_step(..., verbose=True)` dan menampilkan state,
action legal/dipilih, jarak, reward langkah, penalti buntu, reward untuk Q, target,
TD-error, serta substitusi lengkap persamaan Q. Dictionary `result` memuat angka
langkah terakhir. Jika buntu sejak awal, `td_error=None` dan Q tidak diperbarui;
jika buntu setelah perpindahan, penalti ditambahkan sebelum update Q.

Epsilon dihitung pada awal episode melalui `epsilon_for_episode()`: dua episode
contoh memakai 1,00 lalu 0,05. Environment di-reset antar-episode; Q-table dan RNG
berlanjut. Untuk mengulang semuanya dari nol, jalankan cell pembuatan environment.
Parameter `action` dapat dipakai untuk memilih manual; `step()` tetap memeriksa
legalitasnya. Jika action diberikan manual, epsilon tidak menentukan action tersebut.

Tidak ada class baru, helper notebook, unduhan, atau ekspor otomatis. Saat training,
`verbose=False`. Pengujian lengkap state/mask, graf, terminasi, reward, dan validasi
lapangan berada di luar contoh manual awal; cakupan poin 2–5 ditambahkan di bagian berikutnya.

Bagian OSM memuat snapshot penelitian lokal dengan loader core setelah pemeriksaan
keberadaan file, lalu `add_comfort_scores()` dan `build_actions()`. Tiga langkah awal
state B, seed 0, episode berindeks 0 ditelusuri satu per cell memakai Q-table/RNG
tersendiri. Epsilon dihitung sekali melalui `epsilon_for_episode(0, 2)`.
Tidak ada unduhan, penulisan GraphML, atau perubahan hasil eksperimen.

Langkah pertama pada snapshot saat ini memilih edge (1720975931, 1720975893, 0),
panjang 157,32164137901165 m, skor 0,759375. Hitungan manual reward sekitar
0,4080530073268113 dan Q baru 0,0612079510990217 dicantumkan dengan angka tetap,
kemudian dibandingkan dengan hasil core dan nilai Q-table. Identitas edge juga
diperiksa; acuan harus ditinjau bila data/konfigurasi contoh diubah. Penelusuran
singkat ini belum merupakan pengujian seluruh graf atau validasi lapangan.

Komponen reward dicatat langsung pada cabang asli `RunningRouteEnvironment.step()`:
`edge`, `access` (ditambahkan 30 Oktober), `direction`, `revisit`, dan `terminal`, disertai aturan arah serta jarak
lurus sebelum/sesudah. `train_step()` menambahkan `no_action` dan menempatkan
rincian pada `result["reward_components"]` serta info. `verbose=True` mencetak
atribut jalan, komponen H/S/W, formula skor, reward ruas, formula arah, kontribusi
revisit/terminasi/buntu, total reward, dan persamaan Q. Cabang dan urutan penjumlahan
reward dipertahankan. Pencatatan ini berlaku pada contoh sintetis dan snapshot OSM;
belum merupakan verifikasi lengkap seluruh aturan reward.


### 11.1 Kasus lanjutan poin 2–5

Seluruh kasus berada langsung di `verifikasi.ipynb`, tanpa helper/class tambahan.
Tidak ada perubahan core, parameter, aturan reward, mask, atau hasil eksperimen.

- Poin 2 memeriksa state A/B/C sepanjang lintasan yang sama, reset/previous node,
  indeks progres pada batas kategori, revisit sebelum/tepat 2.500 m, dua kunjungan,
  dua key paralel, fresh/revisit/closing bersamaan, penolakan aksi ilegal, dan
  pemilihan acak/greedy dari daftar legal. Mask/reward tetap memakai kondisi penuh
  environment; kelulusan bukan jaminan sifat Markov semua representasi state.
- Poin 3 memeriksa seluruh snapshot: CRS meter, koordinat, panjang positif/berhingga,
  geometri eksplisit dan ujungnya (toleransi 0,1 m), serta kecocokan seluruh action
  dengan edge. Akumulasi jarak diuji pada edge paralel berlainan panjang dan jejak OSM.
- Poin 4 memeriksa sukses inklusif 4.500/5.000/5.500 m, closing di luar rentang
  yang ditolak, non-start tepat/melewati 5.500 m, buntu awal/setelah action, batas
  220 langkah nyata, prioritas success/over_distance, serta penolakan setelah done.
- Poin 5 memeriksa skor atribut kosong/gabungan/lebar, hitungan reward ruas/arah,
  fase yang melintasi 2.500 m, revisit, terminal/buntu, dan penjumlahan komponen.
  Analisis lintasan membandingkan total reward dan return dengan diskonto.

Uji stres edge sintetis 100 km berada di luar rentang panjang ruas snapshot.
Reward kegagalan pada contoh ini dapat melebihi contoh loop valid, sehingga klaim
“reward tertinggi selalu hanya untuk sukses” tidak dinyatakan lulus. Ini batas desain,
bukan perubahan aturan atau hasil lapangan. Aritmetika dan analisis dilaporkan terpisah.
Ringkasan notebook menyatakan bagian yang selesai, bukan jaminan sistem bebas bug.


### 11.2 Status tersimpan dan agenda tinjauan ulang

Per 29 Oktober 2026, `verifikasi.ipynb` terdiri dari 47 cell, termasuk 31 cell kode.
Seluruh cell kode berhasil dieksekusi dari kernel Python 3.13 bersih. Poin 1–5
tersedia dengan angka acuan, output per langkah/tabel, dan assertion. Penambahan
poin 2–5 tidak mengubah core, snapshot GraphML, notebook scenario, atau hasil
training. Bukti berada pada output notebook; tidak ada helper/class verifikasi
atau ekspor artefak terpisah.

Pengguna meminta menyimpan konteks ini dan beralih ke pembahasan lain.
**Pengembangan dan pembahasan verifikasi ditunda sampai pengguna meminta
meninjaunya kembali.** Ketersediaan implementasi tidak berarti semua kasus lanjutan
sudah disetujui pengguna, seluruh sistem bebas bug, atau rute telah tervalidasi di lapangan.

Agenda saat ditinjau kembali:

1. Review keterbacaan, acuan manual, dan relevansi kasus poin 2–5 bersama pengguna.
2. Bahas batas desain reward secara terpisah dari ketepatan aritmetika. Dalam uji
   stres edge sintetis 100 km, reward gagal 256,25 melampaui contoh loop sukses
   95,08609245282265. Kasus tersebut di luar rentang panjang ruas snapshot, sehingga
   perlu dibahas relevansinya terhadap penelitian sebelum menyimpulkan atau
   memutuskan perbaikan. Belum ada keputusan atau perubahan aturan reward.
3. Jika nanti reward/tag OSM diubah atas arahan pengguna, tinjau kembali expected
   pada notebook dan kebutuhan eksperimen A–C dengan konfigurasi yang sama.
   Ekspor GPX dan validasi lapangan tetap ditunda sebagai pekerjaan terpisah.

## 12. Kesepakatan verifikasi, validasi, dan katalog rute

Rencana rinci dan status implementasi: [Verifikasi, validasi, dan katalog](docs/VERIFIKASI_VALIDASI_DAN_KATALOG.md).

- Hitung manual Q tetap dipakai pada beberapa kasus representatif; tidak seluruh
  episode. Verifikasi aturan internal berbeda dari evaluasi A--C dan percobaan lapangan.
- Validasi lapangan direncanakan menggunakan Huawei Watch Fit 3/Huawei Health.
  Strava tidak diperlukan. Rute yang diuji dipilih dari hasil berhasil; tidak ada
  kewajiban semua state menghasilkan rute untuk dicoba. GPS pembanding, bukan kebenaran mutlak.
- Tidak tumpang tindih bukan syarat mutlak; aturan revisit yang aktif dipertahankan.
  GPX/navigasi dan aplikasi belum dibuat; rencana ekspor menunggu pemeriksaan rute/akses.
- Pembimbing menyarankan katalog rute: generate/evaluasi/seleksi secara offline,
  simpan kandidat, lalu tampilkan peta/informasinya pada UI. Tidak perlu training
  ketika pengguna membuka aplikasi atau mendukung titik awal bebas.
- Practical implications: membantu perencanaan rute lokal, memberi pertimbangan
  representasi state, dan memperlihatkan keterbatasan OSM dari pengamatan nyata.
  Katalog mendukung pemanfaatan; inti penelitian tetap reward dan pengaruh state.
- Kandidat rujukan aplikasi Q-Learning ada pada referensi.md; belum otomatis masuk
  daftar pustaka naskah. Mayoritas paper mengevaluasi performa, bukan bukti unit test/manual Bellman.
