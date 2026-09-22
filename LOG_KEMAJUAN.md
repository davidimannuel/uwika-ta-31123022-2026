# Log Kemajuan Implementasi

Dokumen ini adalah handover singkat untuk sesi berikutnya atau agent lain. Detail teknis lengkap berada pada `IMPLEMENTASI.md`.

## Status terakhir

- Proyek: Q-Learning tabular untuk membentuk rute lari loop 5 km pada graf jalan OpenStreetMap.
- Rute valid: kembali ke node start pada total jarak 4.500--5.500 m (`is_loop=True`).
- State yang aktif dan dibandingkan: A = `(current_node,)`, B = `(current_node, progress_bin)`, C = `(current_node, previous_node, progress_bin)`.
- Scenario D telah dihapus; revisit bukan bagian state. Revisit tetap merupakan aturan environment yang sama untuk seluruh A--C.
- Evaluasi utama adalah **greedy** (`epsilon=0`) sekali untuk setiap Q-table/seed. `EPSILON_END=0,05` hanya berlaku saat training.
- Hasil terbaru epsilon decay tetap 50.000 pada Scenario C: 50k menghasilkan 2/5 loop valid; 100k, 200k, dan 400k masing-masing menghasilkan 5/5 loop valid. Pada 400k, galat jarak rata-rata dan comfort memburuk dibanding 100k/200k walaupun success rate tetap 100%.
- Scenario B pada epsilon decay tetap: 50k menghasilkan 0/5 loop; 100k, 200k, dan 400k masing-masing menghasilkan 5/5 loop. Pada 100k, B memiliki galat jarak rata-rata 114,43 m dan comfort 0,759; C pada 100k memiliki galat 267,31 m dan comfort 0,699, tetapi return progress dan reward C lebih tinggi. Jangan lagi menyimpulkan bahwa C pasti lebih unggul hanya dari hasil epsilon dinamis lama.

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
- `scenario_A.ipynb`, `scenario_B.ipynb`, dan `scenario_C.ipynb` tidak lagi memiliki cell training default yang redundan. Masing-masing menyediakan cell 10k, 20k, 30k, 40k, dan 50k episode, plus tabel dan empat grafik ringkasan.
- Setiap cell eksperimen melakukan `importlib.reload(rute_lari_core)` untuk menghindari kernel memakai versi core lama.
- Masing-masing notebook A--C sekarang memiliki dua kelompok eksperimen: 10k--50k dengan epsilon dinamis, serta 50k, 100k, 200k, dan 400k dengan epsilon decay tetap 50k. Artefak kelompok kedua memakai folder `sensitivitas_epsilon_tetap_50000_episode_<jumlah>_<scenario>`.

## Hasil sensitivitas episode yang sudah tersedia: Scenario B

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

## Langkah berikutnya yang disarankan

1. Scenario B dan C telah menunjukkan 100k sebagai kandidat durasi final: keduanya 5/5 loop valid. B lebih dekat ke target dan memiliki comfort lebih tinggi pada checkpoint ini; C memiliki return progress serta reward lebih tinggi. Pilih prioritas metrik sebelum menentukan state kandidat utama.
2. Jalankan Scenario A pada **100.000 episode dengan epsilon_decay_episodes=50.000**. Hasil B dan C 100k yang sudah ada dapat menjadi kelompok pembanding jika tidak ada konfigurasi lain yang berubah.
3. Bandingkan A--C memakai evaluasi greedy dan grafik TD-error; jangan membandingkan hasil epsilon dinamis dengan epsilon tetap sebagai satu rangkaian yang sama.
4. Tentukan kesimpulan perbandingan state hanya dari satu jumlah episode final yang sama untuk A--C.
5. Untuk klaim stabil yang lebih kuat, lima seed masih terbatas. Setelah konfigurasi dikunci, evaluasi ulang dengan lebih banyak seed (misalnya 10 atau 20) dan gunakan success rate serta sebaran metrik per seed.
6. Jika closing action tetap jarang pada scenario lain, catat sebagai masalah yang perlu dibahas dan diuji secara terpisah. Jangan mengubah environment sebelum rancangan eksperimennya disepakati.

## Berkas utama

- `rute_lari_core.py`: satu-satunya core environment dan Q-Learning.
- `analisa.ipynb`: analisis data OSM.
- `scenario_A.ipynb`, `scenario_B.ipynb`, `scenario_C.ipynb`: eksperimen state dan sensitivitas episode.
- `IMPLEMENTASI.md`: wiki teknis lengkap.
- `hasil_bab_4/training_qlearning_5km/`: artefak CSV, grafik, dan peta hasil running.
