# Aset Visual Bab III

Nomor gambar, nomor tabel, dan caption akhir ditentukan pengguna saat menyusun laporan. Berkas PlantUML tidak memuat lokasi bab.

| Penempatan dalam Bab III | Aset | Berkas atau isi | Sumber caption |
|---|---|---|---|
| Setelah penjelasan rancangan penelitian | Diagram alur metode penelitian | [alur_penelitian.puml](assets/alur_penelitian.puml) | Diolah peneliti (2026) |
| Setelah uraian environment dan sebelum rincian reward | Diagram satu langkah environment dan pembaruan Q | [alur_langkah_q_learning.puml](assets/alur_langkah_q_learning.puml) | Diolah peneliti (2026) |
| Setelah pengambilan data OSM | Tabel konfigurasi data | Titik start, target 5.000 m, batas valid 4.500--5.500 m, bbox 3.025 m, `network_type=walk`, dan CRS EPSG:32749 | Diolah peneliti (2026) |
| Setelah comfort score | Tabel kebijakan comfort score | Bobot `highway` 0,55, `surface` 0,30, `width` 0,15; prioritas +1, lainnya −1, dan atribut kosong −0,50; skor gabungan tanpa clipping | Diolah peneliti (2026) |
| Setelah definisi state | Tabel scenario state | A `(current_node,)`, B `(current_node, progress_bin)`, C `(current_node, previous_node, progress_bin)` | Diolah peneliti (2026) |
| Setelah hyperparameter | Tabel konfigurasi pelatihan | alpha, gamma, epsilon awal/akhir, batas langkah dan lima seed; total 75K/150K masing-masing dengan epsilon dinamis atau durasi penurunan tetap 50K | Diolah peneliti (2026) |
| Setelah metrik evaluasi | Tabel definisi dan interpretasi metrik | `is_loop`, galat jarak, reward, mean comfort, overlap berbasis jumlah lintasan ruas, return progress, jarak akhir ke start, closing action, dan alasan terminasi | Diolah peneliti (2026) |

## Rumus yang dimasukkan ke Bab III

1. Perhitungan comfort score.
2. Jarak lurus ke start dalam koordinat meter.
3. Reward ruas, penalti access permissive, arah perjalanan, revisit, dan terminal.
4. Pembaruan Q-Learning.
5. Jadwal epsilon linear.
6. Metrik galat jarak, mean comfort berbobot panjang, return progress ratio, overlap ratio, success rate, dan termination rate.

Gunakan persamaan native Word atau gambar rumus yang dirender dengan benar. Jangan memasukkan LaTeX mentah ke dokumen Word.


## Lokasi aset bersama

Semua sumber berada di [assets/](assets/). Sumber rumus terbaru tersedia pada
[rumus_revisi.tex](assets/rumus_revisi.tex). Diagram penyaringan opsional tersedia
pada [penyaringan_aksi.puml](assets/penyaringan_aksi.puml). Ilustrasi jarak lurus
tersedia pada [ilustrasi_jarak_lurus_node_awal.svg](assets/ilustrasi_jarak_lurus_node_awal.svg).

Diagram terdahulu research_method_flow.puml dan qlearning_environment_flow.puml
tetap disimpan di assets/ untuk referensi, tetapi untuk revisi terkini gunakan
dua diagram pengganti pada tabel di atas. Gambar MultiDiGraph tetap dapat memakai
[projected_multidigraph_illustration.puml](assets/projected_multidigraph_illustration.puml).
