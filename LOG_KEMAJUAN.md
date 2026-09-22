# Log Kemajuan Implementasi

Dokumen ini adalah handover singkat untuk sesi berikutnya atau agent lain. Detail teknis lengkap berada pada `IMPLEMENTASI.md`.

## Status terakhir

- Proyek: Q-Learning tabular untuk membentuk rute lari loop 5 km pada graf jalan OpenStreetMap.
- Rute valid: kembali ke node start pada total jarak 4.500--5.500 m (`is_loop=True`).
- State yang aktif dan dibandingkan: A = `(current_node,)`, B = `(current_node, progress_bin)`, C = `(current_node, previous_node, progress_bin)`.
- Scenario D telah dihapus; revisit bukan bagian state. Revisit tetap merupakan aturan environment yang sama untuk seluruh A--C.
- Evaluasi utama adalah **greedy** (`epsilon=0`) sekali untuk setiap Q-table/seed. `EPSILON_END=0,05` hanya berlaku saat training.
- Rancangan eksperimen episode yang disepakati tetapi belum dijalankan ulang: (a) epsilon dinamis pada 30k, 40k, 50k, dan 75k; (b) horizon epsilon tetap 50k pada 50k, 75k, 100k, dan 150k. Keduanya dijalankan pada A, B, C dan lima seed yang sama.
- Hasil lama hingga 400k disimpan sebagai bukti awal: B dan C pernah mencapai 5/5 loop pada 100k dengan horizon epsilon tetap 50k, sedangkan A tetap 0/5. Hasil itu tidak menjadi angka final sampai rangkaian baru selesai dijalankan.

## Keputusan implementasi yang penting

- Action adalah edge spesifik `(next_node, key)`. Jika terdapat beberapa edge paralel dari `u` ke `v`, masing-masing `key` adalah action berbeda.
- Riwayat revisit saat ini memeriksa node tujuan yang pernah dikunjungi, bukan ID edge.
- Revisit diizinkan setelah 50% target (2.500 m), maksimum dua kunjungan node, dan setiap revisit mendapat penalti.
- Fase pulang dimulai pada 50% target. Sebelum fase ini, agen diberi penalti ringan jika action membuatnya lebih dekat ke start; sesudah fase ini, agen memperoleh reward bila makin dekat ke start.
- Comfort score edge memakai highway, surface, dan width; comfort adalah proxy berbasis OSM, bukan hasil survei pelari atau skor keamanan.
- `closing_action_available=True` berarti selama evaluasi tersedia action legal langsung ke start yang menghasilkan total jarak 4.500--5.500 m. Flag ini adalah diagnosis kesempatan menutup loop, bukan jaminan loop berhasil.

## Perubahan kode pada sesi terakhir

- `rute_lari_core.py` mendukung `run_scenario_experiment(..., episodes=..., result_subdir=...)`.
- `rute_lari_core.py` kini juga mendukung `epsilon_decay_episodes`. Bila nilainya `None`, epsilon tetap turun mengikuti total episode seperti eksperimen lama. Bila diisi `50_000`, epsilon turun hanya selama 50.000 episode pertama lalu tetap 0,05.
- Jumlah episode default adalah 10.000 untuk percobaan cepat. Nilai eksplisit dipakai pada eksperimen perbandingan.
- `train_q_learning(..., episodes=..., epsilon_decay_episodes=...)` mendukung jadwal epsilon dinamis maupun tetap.
- Output eksperimen dapat ditulis ke `result_subdir`, sehingga CSV, grafik, dan peta tidak tertimpa oleh konfigurasi episode lain.
- `scenario_A.ipynb`, `scenario_B.ipynb`, dan `scenario_C.ipynb` tidak lagi memiliki cell training default yang redundan. Masing-masing menyediakan cell epsilon dinamis 30k, 40k, 50k, 75k serta cell horizon epsilon tetap 50k, 75k, 100k, 150k; tiap kelompok memiliki tabel dan empat grafik ringkasan.
- Setiap cell eksperimen melakukan `importlib.reload(rute_lari_core)` untuk menghindari kernel memakai versi core lama.
- Masing-masing notebook A--C sekarang memiliki dua kelompok eksperimen: 30k, 40k, 50k, 75k dengan epsilon dinamis, serta 50k, 75k, 100k, 150k dengan horizon epsilon tetap 50k. Artefak kelompok kedua memakai folder `sensitivitas_epsilon_tetap_50000_episode_<jumlah>_<scenario>`.

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

1. Jalankan ulang epsilon dinamis pada 30k, 40k, 50k, dan 75k untuk A, B, dan C. Laporan BAB IV hanya menjadikannya alasan metodologis, bukan pembandingan durasi final.
2. Jalankan horizon epsilon tetap 50k pada 50k, 75k, 100k, dan 150k untuk A, B, dan C. Rangkaian ini menjadi basis hasil akhir BAB IV.
3. Bandingkan A--C dengan jumlah episode sama, evaluasi greedy, serta grafik TD-error. Jangan mencampurkan hasil epsilon dinamis dan horizon tetap sebagai satu rangkaian.
4. Tentukan state kandidat dari keberhasilan loop terlebih dahulu, lalu galat jarak dan comfort sebagai pembeda. Return progress dan reward dibaca sebagai metrik pendukung.
5. Lima seed cukup untuk eksperimen saat ini, tetapi pembahasan BAB IV harus menyebutnya sebagai stabilitas empiris pada lima seed, bukan klaim generalisasi.

## Berkas utama

- `rute_lari_core.py`: satu-satunya core environment dan Q-Learning.
- `analisa.ipynb`: analisis data OSM.
- `scenario_A.ipynb`, `scenario_B.ipynb`, `scenario_C.ipynb`: eksperimen state dan sensitivitas episode.
- `IMPLEMENTASI.md`: wiki teknis lengkap.
- `hasil_bab_4/training_qlearning_5km/`: artefak CSV, grafik, dan peta hasil running.
