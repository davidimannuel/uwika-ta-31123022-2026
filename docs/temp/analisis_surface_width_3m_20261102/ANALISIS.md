# Analisis training surface dan width 3 m

Tanggal pemeriksaan: 2 November 2026 (Asia/Jakarta).
Sumber tunggal: `hasil_bab_4/training_qlearning_5km/surface_width_3m_20261102/`.
Training dijalankan pengguna. Pemeriksaan ini membaca artefak dan mengulang evaluasi
greedy; tidak menjalankan training, mengubah core/notebook, atau menimpa hasil mentah.

## Konfigurasi yang diperiksa

- State A: `(current_node,)`; B: `(current_node, progress_bin)`;
  C: `(current_node, previous_node, progress_bin)`.
- Empat konfigurasi: dinamis 75k/150k; horizon epsilon 50k pada total 75k/150k.
- Lima seed 0–4, masing-masing dimulai dari Q-table kosong; total 60 training.
- Highway: prioritas 1 = 1,00; prioritas 2 = 0,60; lainnya = 0,20; kosong = 0,50.
  Prioritas 2 mencakup tertiary/tertiary_link.
- Surface: asphalt/concrete/paving_stones/paved = 1,00; lainnya = 0,20;
  kosong = 0,50; gabungan minimum.
- Width: valid >=3 m = 1,00; positif <3 m = 0,20;
  kosong/invalid/gabungan = 0,50. Batas 3 m merupakan preferensi penelitian.
- Bobot H/S/W tetap 0,55/0,30/0,15. Penalti permissive -0,10 per 100 m;
  blacklist akses aktif. Target 5.000 m, toleransi 4.500–5.500 m.
- Evaluasi akhir epsilon 0; epsilon minimum training 0,05.

## Keberhasilan evaluasi greedy

| Strategi epsilon | Episode per seed | A | B | C |
|---|---:|---:|---:|---:|
| Dinamis | 75.000 | 0/5 | 0/5 | 5/5 |
| Dinamis | 150.000 | 0/5 | 0/5 | 5/5 |
| Horizon 50k | 75.000 | 1/5 | 1/5 | 5/5 |
| Horizon 50k | 150.000 | 0/5 | 5/5 | 5/5 |

Pembilang adalah jumlah Q-table/seed dengan loop valid pada evaluasi akhir,
bukan proporsi episode training. C mencapai 5/5 pada setiap konfigurasi yang
diuji; ini belum membuktikan keberhasilan pada semua seed atau titik awal.
B mencapai 5/5 pada horizon 50k total 150k. A berhasil satu seed pada horizon
50k total 75k, sehingga pernyataan bahwa A tidak pernah bisa membentuk loop salah.

## Perbandingan metrik

| Epsilon | Episode | State | Loop | Galat semua seed (m) | Galat loop valid (m) | Skor ruas loop valid | Rata-rata state Q |
|---|---:|---|---:|---:|---:|---:|---:|
| Dinamis | 75.000 | A | 0/5 | 575,94 | — | — | 4.287,0 |
| Dinamis | 75.000 | B | 0/5 | 499,70 | — | — | 25.996,2 |
| Dinamis | 75.000 | C | 5/5 | 331,46 | 331,46 | 0,9271 | 45.109,8 |
| Dinamis | 150.000 | A | 0/5 | 499,28 | — | — | 4.812,2 |
| Dinamis | 150.000 | B | 0/5 | 495,75 | — | — | 30.498,4 |
| Dinamis | 150.000 | C | 5/5 | 394,17 | 394,17 | 0,9291 | 52.099,2 |
| Horizon 50k | 75.000 | A | 1/5 | 483,03 | 211,51 | 0,9056 | 4.754,2 |
| Horizon 50k | 75.000 | B | 1/5 | 441,76 | 135,64 | 0,9285 | 25.475,0 |
| Horizon 50k | 75.000 | C | 5/5 | 334,17 | 334,17 | 0,9251 | 43.899,0 |
| Horizon 50k | 150.000 | A | 0/5 | 569,14 | — | — | 5.415,0 |
| Horizon 50k | 150.000 | B | 5/5 | 268,47 | 268,47 | 0,9034 | 28.103,2 |
| Horizon 50k | 150.000 | C | 5/5 | 339,91 | 339,91 | 0,9193 | 46.671,6 |

Galat semua seed mencakup perjalanan gagal, sehingga tidak dapat dibaca sendiri
sebagai kualitas rute. Kolom loop valid hanya dihitung pada seed sukses;
perbandingan dengan satu seed sukses memiliki dasar berbeda dari lima seed sukses.
Mean comfort tetap skor menurut aturan atribut penelitian, bukan skor survei.

Pada horizon 50k total 150k, B dan C sama-sama 5/5. B lebih dekat ke 5 km
(galat rata-rata 268,47 m vs C 339,91 m) serta memiliki lebih sedikit state Q
(28.103,2 vs 46.671,6). C memiliki skor ruas rata-rata lebih tinggi
(0,9193 vs 0,9034). Tidak ada satu konfigurasi yang unggul pada seluruh metrik.
C dinamis 75k sudah mencapai 5/5 pada anggaran episode lebih kecil; belum perlu
menetapkan atau menghapus konfigurasi hanya berdasarkan ringkasan ini.

## Diagnosis dan kandidat rute

- Total 27 evaluasi valid dan 33 gagal.
- Gagal: 29 over_distance dan 4 no_available_action; tidak ada kegagalan
  yang pernah memiliki closing action legal pada episode evaluasinya.
- Semua 27 lintasan valid berbeda secara urutan edge `(u,v,key)`. Ini belum
  mengukur kemiripan geografis; rute berbeda masih mungkin berbagi sebagian besar ruas.
- Seluruh 27 rute valid mengandung ruas berlebar <3 m, lebar tidak diketahui,
  dan permissive. Batas width dan penalti akses merupakan preferensi lunak,
  bukan larangan atau bukti rute telah layak digunakan di lapangan.
- Panjang rute valid 4.500,17–5.211,51 m.
- Kandidat dengan galat terkecil pada grup ini: state B, horizon 50k total
  150k, seed 1, panjang 4.945,95 m,
  galat 54,05 m, skor ruas 0,9408.
  Rute ini mencakup 613,40 m ruas dengan lebar valid <3 m,
  315,96 m lebar tidak diketahui, dan
  1.254,82 m edge yang mengandung permissive.
  Panjang permissive mengikuti seluruh edge gabungan, bukan pembagian per way.
  Ini kandidat untuk diperiksa, bukan rekomendasi yang sudah divalidasi.

## Pemeriksaan artefak

- Dua belas folder konfigurasi, 60 CSV-row evaluasi, 60 Q-table dan 60 rute JSON tersedia.
- Seluruh berkas yang disebut pada manifest metadata tersedia.
- Sebanyak 6.750.000 baris history lengkap; setiap seed memiliki urutan episode
  1 sampai batas training, tanpa nomor episode hilang/berulang.
- Epsilon di seluruh history sesuai durasi/horizon metadata.
- Metadata seluruh folder sesuai kelompok highway, surface, ambang width 3 m,
  penalti permissive, dan blacklist aktif pada core saat pemeriksaan.
- Seluruh 60 evaluasi diulang dari Q-table tersimpan: metrik cocok dalam toleransi
  numerik, urutan node dan action cocok persis dengan rute JSON.
- Panjang setiap rute cocok dengan jumlah panjang edge snapshot; tidak terdapat
  edge blacklist pada lintasan. Diagnosis jumlah state Q cocok dengan Q-table.
- Sebanyak 228 berkas hasil mentah tidak berubah selama audit.

Kelulusan pemeriksaan ini menunjukkan konsistensi artefak dan reproduksi evaluasi,
bukan pembuktian seluruh kode bebas bug, optimalitas, atau validasi lapangan.

## Batas perbandingan dengan grup lama

Angka terbaru tidak boleh digabung dengan `konfigurasi_empat_20261029` atau
`highway_dua_prioritas_20261101`. Skala surface/width berubah, sehingga kenaikan
mean comfort atau total reward lintas grup tidak otomatis berarti rute lebih baik.
Perbandingan ke grup highway lama mencakup perubahan surface dan width sekaligus;
ke baseline lebih lama juga mencakup perubahan akses/highway. Pengaruh satu
komponen belum terisolasi melalui eksperimen perubahan tunggal.

## Berkas pendamping dan kelanjutan

- `evaluasi_per_seed.csv`: metrik 60 seed, identitas rute, panjang permissive,
  ruas <3 m, dan lebar tak diketahui.
- `ringkasan_konfigurasi.csv`: ringkasan 12 kombinasi dan keberhasilan training
  pada 10.000 episode terakhir per seed, terpisah dari greedy.
- `audit.json`: rincian pemeriksaan dan ringkasan terstruktur.

Selanjutnya pengguna dapat meninjau hasil ini, melanjutkan pembahasan reward,
kemudian menyesuaikan acuan `verifikasi.ipynb`. Rencana lapangan, GPX, dan katalog
belum diimplementasikan. Lihat `docs/VERIFIKASI_VALIDASI_DAN_KATALOG.md`.
