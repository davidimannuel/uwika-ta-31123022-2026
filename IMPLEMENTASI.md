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

- Scenario state A, B, dan C adalah eksperimen final. Ketiganya memakai action, reward, action mask, dan aturan revisit yang sama; hanya representasi state yang berbeda.
- Scenario C telah menghasilkan satu loop valid dari lima evaluasi greedy pada konfigurasi saat ini.
- State C adalah kandidat utama karena menambahkan konteks arah kedatangan melalui `previous_node`.
- Terminasi paling sering masih `no_available_action` dan `over_distance`; hasil perlu dibaca bersama closing action available rate.

## 2. Struktur Proyek dan Urutan Eksekusi

| Berkas/direktori | Peran | Catatan |
|---|---|---|
| **rute_lari_core.py** | Core tunggal: konfigurasi, download/load OSM, comfort, action, state, environment, Q-Learning, metrik, grafik, dan peta. | Jangan menduplikasi aturan per scenario. |
| **analisa.ipynb** | Memakai download/load OSM dari core, lalu menganalisis data dan membuat peta graf. | Jalankan lebih dahulu. |
| **scenario_A.ipynb** | Training dan evaluasi state A. | Memanggil core bersama. |
| **scenario_B.ipynb** | Training dan evaluasi state B. | Memanggil core bersama. |
| **scenario_C.ipynb** | Training dan evaluasi state C. | Memanggil core bersama. |
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

Analisis wajib mencakup sampel node/edge; ringkasan struktur; konektivitas; panjang edge; node start; kelengkapan highway, surface, dan width; distribusi tiga atribut; indikator jumlah tujuan node; kombinasi kelengkapan atribut comfort; distribusi comfort score; serta peta interaktif.

Kualitas atribut snapshot sekarang:

| Atribut | Ketersediaan edge |
|---|---:|
| highway | 100,00% |
| surface | 67,59% |
| width mentah | 66,77% |
| width valid dalam meter | 66,18% |

Edge dengan data kosong tidak dibuang karena bisa memutus graf. Komponen comfort yang tidak tersedia menggunakan nilai netral.

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
| highway | footway/pedestrian 0,95; path 0,85; living_street 0,80; residential 0,75; service 0,60; unclassified 0,55; tertiary 0,45; secondary/track 0,35; primary 0,20; trunk/steps 0,10. |
| surface | asphalt 1,00; concrete/paved 0,90; paving_stones 0,75; sett 0,65; compacted 0,55; fine_gravel 0,45; gravel 0,30; dirt 0,25; ground/unpaved 0,20. |
| width | 1 m bernilai 0,25; 5 m atau lebih 1,00; nilai di antaranya dinormalisasi linear. |
| data kosong | surface dan width kosong, invalid, atau multiple bernilai 0,50. |
| edge gabungan | Bila highway/surface berupa list setelah simplify, dipilih skor minimum secara konservatif. |

Fungsi inti di training notebook: **is_missing**, **osm_values**, **parse_width_m**, **conservative_score**, **width_score**, dan **add_comfort_scores**.

Comfort score adalah proxy spasial. Jangan menyebutnya sebagai hasil validasi pengalaman pelari tanpa survei atau validasi lapangan.

## 6. Implementasi Q-Learning pada Core Bersama

### 6.1 Input dan snapping start

Semua notebook scenario memanggil **load_or_download_graph()** dari `rute_lari_core.py`. Fungsi ini memuat **data_osm_5km/graf_jalan_kaki_5km.graphml**, atau mengunduh serta menyimpannya bila belum ada. Koordinat start latitude-longitude ditransformasi ke CRS graf, kemudian **ox.distance.nearest_nodes** menentukan START_NODE. Ini memastikan agen mulai pada node yang benar-benar ada dalam graf.

Setelah GraphML dimuat, **add_comfort_scores(G)** dipanggil lagi untuk membuat atribut skor tersedia pada memori. Dictionary **NODE_XY** menyimpan koordinat meter semua node.

### 6.2 Action

Satu action adalah objek **EdgeAction** yang menyimpan:

    next_node, key, length_m, comfort_score, data edge

ID action di Q-table adalah **(next_node, key)**. Node saat ini sudah bagian dari state, sehingga action tidak perlu menyimpan current node. Identitas edge lengkap untuk log rute adalah **(current_node, next_node, key)**.

Fungsi **build_actions(G)** membuat ACTIONS_BY_NODE. Semua edge paralel dipertahankan sebagai action yang berbeda. Tidak ada pemilihan edge berdasarkan comfort secara paksa; agen harus mempelajarinya melalui reward dan Q-table.

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

Kondisi early_return tetap ada dalam step sebagai penjagaan, tetapi action mask normal tidak menawarkan edge ke start sebelum jarak valid. Jadi early_return biasanya tidak muncul kecuali action mask atau pemanggilan step diubah.

Setiap kali `closing_actions` tidak kosong, environment mencatat `closing_action_was_available=True` untuk episode tersebut. Flag ini **tidak** mengubah daftar action, reward, atau policy; ia hanya mencatat bahwa agen pernah memiliki kesempatan legal untuk langsung menutup loop.

### 6.6 Urutan kerja step(action)

Urutan fungsi **step()** harus dipahami sebelum dimodifikasi:

1. Memastikan episode belum selesai.
2. Menghitung action legal dan menolak action yang tidak ada pada action mask.
3. Menyimpan current node, next node, serta jarak lurus sebelum bergerak.
4. Mengubah posisi, total jarak, previous node, riwayat rute, jumlah kunjungan, dan jumlah langkah.
5. Menghitung reward comfort edge.
6. Menambahkan penalti jika terjadi revisit ke node selain start.
7. Memeriksa terminal dengan urutan: success, early_return, over_distance, step_limit.
8. Jika belum terminal dan jarak sudah 50% target, menambahkan reward arah pulang.
9. Mengembalikan next state, reward, done, dan info.

is_loop hanya menjadi True apabila action memasuki start dan jarak total valid. termination_reason pada kondisi tersebut adalah success.

## 7. Reward, Policy, dan Pembaruan Q-table

### 7.1 Reward

Reward edge:

    r_edge = (comfort_score − 0,50) × length_m ÷ 100

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
| EARLY_RETURN_PENALTY | -45 | Kembali ke start di luar jarak valid. |
| STEP_LIMIT_PENALTY | -40 | Mencapai 220 langkah. |
| REVISIT_PENALTY | -8 | Revisit node selain start. |
| OUTWARD_PENALTY_SCALE | 0,40 | Skala penalti bila, sebelum 2.500 m, action membuat agen mendekati start. |

Nilai reward dapat dituning, tetapi setiap perubahan reward harus dievaluasi ulang pada seluruh A–C dengan seed sama.

### 7.2 Epsilon-greedy

**choose_action()** memilih action legal secara acak dengan peluang epsilon; selain itu ia memilih Q-value terbesar. Bila nilai Q terbaik seri, salah satu action terbaik dipilih secara acak.

Schedule epsilon:

    epsilon = 0,05 + (1,00 − 0,05) × (1 − episode ÷ 2.499)

Epsilon turun linear dari 1,00 ke 0,05 selama 2.500 episode. Evaluasi greedy memakai epsilon 0 agar policy yang diuji tidak mengandung eksplorasi acak.

Satu nilai epsilon dipakai untuk seluruh action di dalam satu episode. Artinya pada episode awal agen sangat sering mengeksplorasi action legal secara acak; seiring episode bertambah, agen makin sering memakai Q-value terbaik yang sudah dipelajari.

Simulasi schedule epsilon saat `EPISODES=2.500`:

| Episode (dimulai dari 0) | Epsilon kira-kira | Makna |
|---:|---:|---|
| 0 | 1,000 | Hampir setiap pemilihan action bersifat acak. |
| 500 | 0,810 | Sekitar 81% peluang eksplorasi, 19% memilih Q-value terbaik. |
| 1.250 | 0,525 | Eksplorasi dan pemanfaatan policy relatif seimbang. |
| 2.000 | 0,240 | Agen lebih sering mengikuti Q-value terbaik. |
| 2.499 | 0,050 | Hanya sekitar 5% peluang action acak. |

Contoh pada episode 2.000: apabila ada tiga action legal, agen memiliki sekitar 24% peluang memilih salah satu action secara acak dan sekitar 76% peluang memilih action dengan Q-value tertinggi. Saat evaluasi greedy, epsilon dipaksa menjadi 0 sehingga agen selalu memilih action legal dengan Q-value tertinggi; hasil evaluasi tidak dipengaruhi eksplorasi acak.

### 7.3 Rumus update

    Q(s, a) = Q(s, a)
            + alpha × [reward + gamma × max Q(s_baru, a_baru) − Q(s, a)]

Nilai masa depan hanya dicari dari action legal pada state berikutnya. Jika episode selesai atau tidak ada action legal, nilai masa depan adalah 0.

## 8. Konfigurasi Training dan Enam Grafik

| Parameter | Nilai | Makna |
|---|---:|---|
| ALPHA | 0,15 | Laju pembaruan Q-value. |
| GAMMA | 0,95 | Bobot reward masa depan. |
| EPSILON_START | 1,00 | Eksplorasi awal. |
| EPSILON_END | 0,05 | Eksplorasi akhir. |
| EPISODES | 2.500 | Episode per seed per scenario. |
| MAX_STEPS_PER_EPISODE | 220 | Batas langkah per episode. |
| SEEDS | (0, 1, 2, 3, 4) | Lima seed eksperimen. |
| ROLLING_WINDOW | 50 | Ukuran rata-rata bergerak untuk menghaluskan tren grafik. |

Setiap scenario melatih lima Q-table, satu untuk setiap seed. Training history digabung, tetapi evaluasi greedy tetap dicatat per seed.

| Grafik | Arti |
|---|---|
| Rata-rata Keberhasilan 50 Episode Terakhir | Proporsi is_loop True dalam 50 episode terakhir. |
| Rata-rata Reward 50 Episode Terakhir | Rata-rata total reward 50 episode terakhir. Reward naik tidak otomatis berarti loop berhasil. |
| Rata-rata Jarak 50 Episode Terakhir | Rata-rata jarak rute 50 episode terakhir; bandingkan dengan target 5 km dan batas valid. |
| Rata-rata Skor Kenyamanan 50 Episode Terakhir | Rata-rata comfort score rute dalam 50 episode terakhir. |
| Jumlah State Q-table | Jumlah state unik yang memiliki entry Q-table. |
| Nilai Epsilon per Episode | Nilai peluang eksplorasi yang ditetapkan dari 1,00 ke 0,05 per episode; bukan rata-rata hasil episode. |

## 9. Evaluasi, Peta, dan Berkas Hasil

### 9.1 Evaluasi greedy

Fungsi **evaluate_greedy()** memakai epsilon 0. Tabel evaluasi utama sengaja dibatasi agar perbandingan Scenario A--C tetap fokus. Setiap baris mewakili satu seed dan hanya memuat metrik berikut.

| Metrik | Arti |
|---|---|
| is_loop | Keberhasilan utama: kembali ke start pada 4.500–5.500 m. |
| total_distance_m | Total jarak edge pada rute dalam meter. |
| absolute_distance_error_m | Selisih absolut dari target 5.000 m. Bukan pengganti is_loop. |
| total_reward | Akumulasi seluruh reward dan penalti dari satu evaluasi greedy. Dibaca bersama is_loop dan termination_reason, bukan sebagai satu-satunya ukuran kualitas rute. |
| mean_comfort | Rata-rata comfort edge berbobot panjang. |
| distance_to_start_at_end_m | Jarak lurus posisi akhir ke start dalam meter. Makin kecil berarti agen setidaknya mendekati start sebelum terminasi. |
| return_progress_ratio | Proporsi langkah setelah 2.500 m yang mengurangi jarak lurus ke start. Nilai mendekati 1 berarti arah pulang lebih konsisten. |
| termination_reason | Alasan terminal setiap seed: success, over_distance, no_available_action, early_return, atau step_limit. |

`closing_action_available_rate` dan rate semua tipe terminasi adalah **diagnosis training**, bukan metrik pembanding utama. Metrik tersebut tetap ditampilkan dalam grafik diagnosis untuk menjelaskan mengapa suatu scenario berhasil atau gagal, tetapi tidak dimasukkan ke tabel evaluasi per seed maupun berkas `evaluation_metrics_{scenario}.csv`.

### 9.1.1 Rumus termination rate

Untuk setiap tipe terminasi, rate dihitung dengan rumus berikut.

    termination_rate(tipe) = jumlah episode dengan tipe tersebut ÷ jumlah seluruh episode

Contoh: bila 3.750 dari 12.500 episode training berakhir karena `over_distance`, maka termination rate `over_distance` adalah 3.750 ÷ 12.500 = 0,30 atau 30%. Pada evaluasi greedy, penyebutnya hanya lima karena satu evaluasi dilakukan untuk masing-masing seed.

### 9.1.2 Grafik yang ditampilkan notebook scenario

Notebook menampilkan tabel evaluasi greedy dalam format vertikal agar setiap metrik utama mudah dibandingkan antar-seed. Berkas `evaluation_metrics_{scenario}.csv` memakai kolom yang sama dengan tabel tersebut. Selain tabel evaluasi, notebook menampilkan dua gambar berikut.

1. **Grafik training utama**: keberhasilan loop, reward, jarak, mean comfort, jumlah state Q-table, dan epsilon. Semuanya selain epsilon memakai rata-rata bergerak 50 episode.
2. **Grafik diagnosis training**: rata-rata jarak akhir ke start, return progress ratio, closing action available rate, dan lima termination rate. Seluruh panel memakai rata-rata bergerak 50 episode dari lima seed; termination rate ditempatkan pada panel yang sama, bukan sebagai gambar tersendiri.

Grafik diagnosis menggunakan data `training_history_{scenario}.csv`, sehingga menunjukkan perubahan selama training, bukan hanya angka akhir. Nilai kosong pada `return_progress_ratio` terjadi bila episode belum pernah mencapai fase kembali, yaitu 50% dari target (2.500 m); rata-rata hanya dihitung dari episode yang memasuki fase tersebut.

Tidak ada baseline Dijkstra. Perbandingan eksperimen hanya A vs B vs C, dengan lingkungan yang sama.

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

### 9.3 Peta interaktif

**make_route_map()** menampilkan satu rute representatif dari lima hasil evaluasi greedy (satu hasil untuk setiap seed), bukan dari episode training. Fungsi **select_representative_trial()** menentukan Q-table/seed yang dipakai dengan aturan berikut.

1. Bila ada satu atau lebih `is_loop=True`, pilih hanya dari kelompok loop valid: `absolute_distance_error_m` terkecil, kemudian `mean_comfort` tertinggi, lalu `return_progress_ratio` tertinggi.
2. Bila belum ada loop valid, pilih rute dengan `absolute_distance_error_m` terkecil, kemudian `distance_to_start_at_end_m` terkecil, lalu `mean_comfort` dan `return_progress_ratio` tertinggi. Urutan ini mencegah rute yang berhenti terlalu dini tetapi kebetulan dekat start terpilih sebagai peta. Dalam kondisi ini peta adalah alat diagnosis, bukan contoh rute final yang berhasil.

Notebook mencetak scenario, seed, nilai seluruh metrik utama, dan alasan pemilihan sebelum peta ditampilkan. Karena itu seed pada peta tidak selalu seed 0 dan pengguna dapat memverifikasi alasan rute tersebut dipilih. `revisit_count` tidak digunakan sebagai kriteria pemilihan peta. Peta memakai warna berbeda per kilometer dan memuat marker start KM 0, marker KM 1–5, serta marker finish terpisah.

Jika rute valid loop, marker finish digeser sedikit untuk tampilan agar tidak menumpuk marker start. Posisi logis finish tetap sama dengan start. Peta representatif bukan rata-rata lima seed; peta hanya alat inspeksi rute terbaik menurut aturan prioritas.

### 9.4 Hasil sekarang

| State | Loop rate | Jarak rata-rata | Galat absolut rata-rata | Comfort rata-rata | Revisit rata-rata |
|---|---:|---:|---:|---:|---:|
| A | 0,00 | 3,769 km | 1.440,42 m | 0,707 | 4,20 |
| B | 0,00 | 4,657 km | 718,51 m | 0,726 | 5,80 |
| C | 0,20 | 5,122 km | 341,00 m | 0,717 | 4,60 |

Tabel hasil harus diperbarui setiap kali konfigurasi berubah. Pada konfigurasi saat ini, C menghasilkan satu loop valid dari lima evaluasi greedy; hasil tersebut masih awal dan perlu diuji ulang dengan seed yang sama bila parameter kembali diubah.

## 10. Aturan Modifikasi dan Konteks untuk AI

Saat membuat perubahan:

1. Ubah satu komponen eksperimen pada satu waktu, misalnya reward kembali atau jumlah progress bin.
2. Jangan mengubah reward/action mask bersamaan dengan definisi state jika ingin membandingkan A–C secara adil.
3. Setelah perubahan yang memengaruhi environment, reward, action, atau training, jalankan ulang seluruh A–C dengan lima seed yang sama.
4. Simpan hasil baru pada direktori berbeda atau beri nama konfigurasi agar CSV lama tidak tertimpa tanpa jejak.
5. Perbarui wiki ini jika parameter, rumus reward, action mask, metrik, atau status hasil berubah.
6. Jangan mengklaim sistem berhasil sebelum is_loop True muncul secara konsisten pada evaluasi greedy.
7. Jangan mengklaim comfort score sebagai pengalaman pelari yang tervalidasi tanpa validasi lapangan atau survei.

Ringkasan singkat: proyek menggunakan Q-Learning tabular dari scratch pada graf jalan kaki OSMnx MultiDiGraph terproyeksi meter. Target adalah loop 5 km plus toleransi 10%. Action adalah edge spesifik (next_node, key). State final yang diuji A sampai C berbeda pada informasi posisi, progres, dan arah kedatangan. Revisit tersedia mulai 50% target dengan maksimum dua kunjungan node; fase ini sama dengan awal reward arah pulang. Semua aturan bersama berada di rute_lari_core.py; analisis berada di analisa.ipynb; eksperimen dipisahkan pada scenario_A.ipynb sampai scenario_C.ipynb. Konfigurasi saat ini telah menghasilkan loop valid pada salah satu evaluasi greedy C.
