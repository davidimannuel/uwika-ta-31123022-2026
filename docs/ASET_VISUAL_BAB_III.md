# Aset Visual Bab III

Nomor gambar, nomor tabel, dan caption akhir ditentukan pengguna saat menyusun laporan. Berkas PlantUML tidak memuat lokasi bab.

| Penempatan dalam Bab III | Aset | Berkas atau isi | Sumber caption |
|---|---|---|---|
| Setelah penjelasan rancangan penelitian | Diagram alur metode penelitian | `research_method_flow.puml` | Diolah peneliti (2026) |
| Setelah uraian environment dan sebelum rincian reward | Diagram alur satu episode environment | `qlearning_environment_flow.puml` | Diolah peneliti (2026) |
| Setelah pengambilan data OSM | Tabel konfigurasi data | Titik start, target 5.000 m, batas valid 4.500--5.500 m, bbox 3.025 m, `network_type=walk`, dan CRS EPSG:32749 | Diolah peneliti (2026) |
| Setelah comfort score | Tabel kebijakan comfort score | Bobot `highway` 0,55, `surface` 0,30, `width` 0,15; serta aturan nilai kosong 0,50 | Diolah peneliti (2026) |
| Setelah definisi state | Tabel scenario state | A `(current_node)`, B `(current_node, progress_bin)`, C `(current_node, previous_node, progress_bin)` | Diolah peneliti (2026) |
| Setelah hyperparameter | Tabel konfigurasi pelatihan | alpha, gamma, epsilon awal/akhir, batas langkah, seed, dan episode sensitivitas | Diolah peneliti (2026) |
| Setelah metrik evaluasi | Tabel definisi dan interpretasi metrik | `is_loop`, galat jarak, reward, mean comfort, return progress, jarak akhir ke start, closing action, dan alasan terminasi | Diolah peneliti (2026) |

## Rumus yang dimasukkan ke Bab III

1. Perhitungan comfort score.
2. Jarak lurus ke start dalam koordinat meter.
3. Reward comfort edge, penalti arah fase awal, dan reward arah pulang.
4. Pembaruan Q-Learning.
5. Jadwal epsilon linear.
6. Metrik galat jarak, mean comfort berbobot panjang, return progress ratio, success rate, dan termination rate.

Gunakan persamaan native Word atau gambar rumus yang dirender dengan benar. Jangan memasukkan LaTeX mentah ke dokumen Word.
