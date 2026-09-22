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
| `IMPLEMENTASI.md` | Wiki implementasi dan keputusan teknis lengkap. |
| `LOG_KEMAJUAN.md` | Handover hasil dan pekerjaan terakhir. |
| `referensi.md` | Daftar sumber, format sitasi, tautan, dan pemakaian referensi pada naskah TA. |
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
- `progress_bin` memakai 16 bin pada rentang 0--5.500 m.
- Evaluasi final setiap seed adalah greedy, yaitu `epsilon=0`. Epsilon minimum 0,05 hanya berlaku selama training.

## Aturan eksperimen

1. Jangan menduplikasi environment atau Q-Learning di notebook. Ubah aturan bersama hanya di `rute_lari_core.py`.
2. Jangan mengubah reward, action mask, state, dan hyperparameter sekaligus bila hasil akan dibandingkan. Ubah satu faktor per eksperimen.
3. Perbandingan A--C yang final wajib memakai jumlah episode, seed, graf, reward, dan action mask yang sama.
4. Default `EPISODES=10_000` hanya untuk uji cepat. Notebook A--C menyediakan dua rangkaian eksplisit: epsilon dinamis pada 30k, 40k, 50k, dan 75k episode; serta horizon epsilon tetap 50k pada 50k, 75k, 100k, dan 150k episode. Setiap hasil disimpan pada subfolder sendiri.
5. Setiap jumlah episode melatih ulang lima seed `(0,1,2,3,4)` dari awal. Hasil 50k bukan kelanjutan hasil 40k.
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

- Sensitivitas jumlah episode sedang dijalankan.
- Scenario B (lima seed) pada 10k, 20k, 30k, 40k, dan 50k episode memiliki success rate berturut-turut 0%, 0%, 0%, 20%, dan 0%.
- Pada B, 40k adalah kandidat sementara terbaik, tetapi hasil belum stabil. Comfort relatif stabil; hambatan utama adalah jarangnya `closing_action_available`.
- Jangan menyimpulkan bahwa 50k lebih buruk atau episode lebih banyak selalu lebih baik dari hasil lima seed saja.

## Praktik kerja dan dokumentasi

- Gunakan komentar kode berbahasa Indonesia yang menjelaskan alasan, terutama pada reward, action mask, dan state.
- Setelah perubahan desain atau hasil penting, sinkronkan `IMPLEMENTASI.md` dan `LOG_KEMAJUAN.md`.
- Setelah memakai sumber baru dalam naskah TA, sinkronkan `referensi.md`; jangan memakai angka atau klaim dari sumber yang belum dicatat di sana.
- Saat mengubah notebook, pastikan cell dapat dijalankan sebagai kode dan tidak bergantung pada cell lama yang sudah dihapus. Cell eksperimen memuat ulang `rute_lari_core` untuk menghindari versi module lama pada kernel.
- Untuk angka Bab IV dan Bab V, gunakan CSV hasil dari satu konfigurasi final yang sama, bukan angka lama yang tersimpan di dokumen `.docx`.
- Prioritaskan penjelasan dalam bahasa Indonesia dan fokus pada isi/metodologi sebelum format penulisan.
- Pada setiap revisi subbab TA, periksa pula apakah tabel, gambar, atau rumus diperlukan untuk memperjelas relasi yang penting. Tambahkan hanya bila memberi nilai penjelasan; simpan kode PlantUML yang relevan di `docs/` agar pengguna dapat merendernya sendiri.
- Utamakan diagram PlantUML yang tidak melebar. Untuk diagram dengan beberapa node atau tahap, gunakan orientasi vertikal (`top to bottom direction`) kecuali orientasi horizontal tetap jelas dan muat nyaman pada lebar halaman laporan.
- Kode dan nama berkas PlantUML harus netral: jangan menyertakan nomor gambar, nomor bab, atau caption. Pengguna menentukan penempatan, nomor, dan caption saat menyusun laporan.
