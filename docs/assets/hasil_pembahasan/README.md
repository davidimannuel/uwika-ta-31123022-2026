# Aset hasil dan pembahasan penelitian rute lari

Aset pendamping draf Bab IV tertanggal 4 November 2026. Berkas Word untuk
penyalinan berada di `docs/temp/revisi_bab_4_20261104/`. Folder ini menyimpan
gambar, data tabel, dan kode pembuatannya secara permanen.

## Sumber hasil

Seluruh hasil berasal dari
`hasil_bab_4/training_qlearning_5km/reward_missing_05_20261103/`:
3 skenario, 4 konfigurasi, dan 5 seed per konfigurasi, yaitu 60 pelatihan
dengan 6.750.000 episode serta 60 rute evaluasi akhir. Konfigurasi meliputi
75.000 dan 150.000 episode, masing-masing dengan penurunan epsilon dinamis
atau penurunan selama 50.000 episode awal. Evaluasi akhir menggunakan epsilon 0.

Graf yang digunakan adalah `data_osm_5km/graf_jalan_kaki_5km.graphml`.
Daftar berkas sumber dan sidik SHA256 graf tersedia di [sumber_data.json](sumber_data.json).
Pembuatan paket ini membaca hasil yang sudah tersimpan, tanpa melatih ulang atau
mengunduh peta. Bagian verifikasi dan validasi tidak disusun dalam paket ini.

## Gambar dalam draf

Nomor di bawah merupakan usulan; sesuaikan caption dan penomoran otomatis Word
ketika memindahkan gambar ke naskah utama. Setiap PNG juga tersedia dalam SVG.

| Usulan | Berkas PNG | Isi |
|---|---|---|
| 4.1 | [jaringan_jalan_wilayah_studi.png](jaringan_jalan_wilayah_studi.png) | Jaringan jalan dan titik awal. |
| 4.2 | [kelengkapan_atribut_jalan.png](kelengkapan_atribut_jalan.png) | Ketersediaan highway, surface, width yang valid, dan access. |
| 4.3 | [distribusi_skor_karakter_ruas.png](distribusi_skor_karakter_ruas.png) | Sebaran skor gabungan pada edge graf. |
| 4.4 | [perbandingan_keberhasilan_evaluasi.png](perbandingan_keberhasilan_evaluasi.png) | Jumlah loop valid dari lima seed per konfigurasi. |
| 4.5 | [perkembangan_keberhasilan_pelatihan.png](perkembangan_keberhasilan_pelatihan.png) | Keberhasilan selama pelatihan. |
| 4.6 | [perkembangan_pengulangan_ruas.png](perkembangan_pengulangan_ruas.png) | Pengulangan ruas selama seluruh episode pelatihan. |
| 4.7 | [rute_loop_contoh.png](rute_loop_contoh.png) | Skenario C, 75.000 episode, penurunan tetap 50.000, seed 0. |
| 4.8 | [rute_gagal_contoh.png](rute_gagal_contoh.png) | Skenario A, 75.000 episode dinamis, seed 1. |

Gambar opsional `perbandingan_rute_state_a`, `perbandingan_rute_state_b`, dan
`perbandingan_rute_state_c` membandingkan jarak serta pengulangan per seed.
Gambar ini tidak wajib ditambahkan bila mengulang informasi tabel.

Peta dibuat dari geometri graf, dengan koordinat relatif dalam kilometer dari
titik awal. Sumber jaringan adalah OpenStreetMap contributors, proyeksi
EPSG:32749. Peta tidak memperlihatkan hasil penelusuran lapangan.

## Tabel dan definisi data

| Berkas | Isi |
|---|---|
| [hasil_evaluasi_lengkap.csv](hasil_evaluasi_lengkap.csv) | 60 rute evaluasi, metrik, alasan berhenti, dan komposisi atribut ruas. |
| [ringkasan_hasil.csv](ringkasan_hasil.csv) | 12 konfigurasi skenario, rata-rata, simpangan baku sampel, dan jumlah loop. |
| [ringkasan_terstruktur.json](ringkasan_terstruktur.json) | Ringkasan yang sama beserta hitungan alasan berhenti. |
| [data_grafik_pelatihan.csv](data_grafik_pelatihan.csv) | Titik garis yang ditampilkan pada grafik pelatihan. |
| [data_atribut_dan_skor.csv](data_atribut_dan_skor.csv) | Atribut, skor, dan status akses seluruh 21.374 edge terarah. |
| [statistik_graf.json](statistik_graf.json) | Jumlah node/edge, kelengkapan atribut, akses, dan statistik skor. |
| `rute_loop_contoh.json` dan `rute_gagal_contoh.json` | Lintasan dua rute yang digambar. |

Rata-rata evaluasi dihitung dari seluruh lima seed, termasuk yang gagal,
kecuali jika teks secara khusus menyebut rute valid. Jarak dan galat dinyatakan
dalam meter. `mean_comfort` adalah skor ruas rata-rata yang dibobot menurut
panjang perjalanan; nilainya bukan persentase kenyamanan atau keamanan.
`overlap_ratio` adalah jumlah lintasan ulang dibagi seluruh lintasan ruas.
Penggunaan ruas fisik yang sama dengan arah berlawanan tetap dihitung sebagai
pengulangan. Kalikan rasio dengan 100 untuk menampilkannya dalam persen.
Kunjungan ulang simpang tidak selalu berarti mengulang ruas.

Untuk kurva pelatihan, metrik dirata-ratakan antar-lima seed pada episode yang
sama, kemudian diperhalus dengan rata-rata bergerak 50 episode. Grafik
menampilkan episode pertama, setiap 500 episode, dan episode terakhir.
Episode berhasil dan gagal sama-sama disertakan. Penyederhanaan tampilan ini
tidak mengubah hitungan keberhasilan pada 10.000 episode terakhir di tabel:
angka tersebut dihitung dari seluruh episode dalam rentang itu, yaitu 50.000
episode dari lima seed per konfigurasi.

## Membuat ulang aset

Jalankan dari root proyek menggunakan dependency proyek yang sudah tersedia:

```bash
uv run python docs/assets/hasil_pembahasan/buat_aset_hasil.py
```

Perintah menimpa gambar dan tabel pada folder ini, tanpa menimpa hasil pelatihan
atau graf. Untuk mencoba di folder lain:

```bash
uv run python docs/assets/hasil_pembahasan/buat_aset_hasil.py --output-dir /tmp/aset_bab4
```

Kode ini dikhususkan untuk kelompok hasil yang disebutkan di atas. Aturan skor
dibaca dari fungsi murni pada core aktif, sedangkan hasil rute dibaca dari
kelompok eksperimen tersimpan. Jangan menjalankannya setelah mengubah aturan
reward lalu menganggap seluruh hasil tetap mewakili aturan yang baru. Untuk
angka pelatihan dan evaluasi baru, perbarui sumber serta pembahasan secara
bersamaan.

Paket ZIP berisi aset, tabel, petunjuk, dan kode, tanpa naskah Word atau hasil
render pemeriksaan halaman. Tidak ada perubahan dependency proyek dalam
penyusunan paket ini.
