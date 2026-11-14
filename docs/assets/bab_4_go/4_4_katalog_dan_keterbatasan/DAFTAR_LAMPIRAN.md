# Bahan gambar untuk penerapan katalog dan keterbatasan

Susunan aktif adalah **4.4.3 Penerapan Katalog Rute Lari** dan
**4.4.4 Keterbatasan Penelitian**. Tidak ada lagi4.5 Penerapan Katalog tersendiri.
Gunakan Word terbaru di docs/temp/bab_4_4_katalog_keterbatasan_go_20261114/.
Salin mulai halaman2. Ganti placeholder tepat di antara paragraf yang tersedia.

## Tiga gambar yang perlu dimasukkan ke4.4.3

| Berkas yang disarankan | Isi dan posisi | Usulan judul gambar |
|---|---|---|
| halaman_utama_katalog.png | Daftar rute dan area peta setelah satu rute dipilih. Letakkan setelah uraian antarmuka katalog. | Tampilan halaman utama katalog rute lari |
| peta_depan_gang_toko9.png | Seluruh lintasan depan gang sebelah Toko9. Letakkan setelah paragraf yang menjelaskan rute dan panjang5.151,87m. | Peta rute dari titik awal depan gang sebelah Toko 9 |
| peta_depan_wk.png | Seluruh lintasan depan Universitas Wijaya Kusuma. Letakkan setelah paragraf rute dan panjang5.527,50m. | Peta rute dari titik awal depan Universitas Wijaya Kusuma |

Sumber screenshot:

- [Halaman utama katalog](https://davidimannuel.github.io/go-running-route-q-learning/)
- [Peta depan gang sebelah Toko9](https://davidimannuel.github.io/go-running-route-q-learning/routes/depan-gang-sebelah-toko9/index.html)
- [Peta depan Universitas Wijaya Kusuma](https://davidimannuel.github.io/go-running-route-q-learning/routes/depan-wk/index.html)

Simpan screenshot asli di folder aset yang sama dengan panduan ini.
Screenshot belum tersedia; Word menggunakan tiga placeholder teks, bukan gambar
contoh yang dibuat-buat. Halaman utama boleh tetap memperlihatkan ketiga rute.
Tidak diperlukan peta detail Indomaret untuk dua contoh yang dipilih.

## Cara memasang

1. Pilih rute pada halaman utama agar daftar dan area peta dapat terlihat bersama.
2. Untuk peta detail, tampilkan seluruh lintasan, START/akhir, nama jalan yang
   terbaca dan atribusi peta; atur panel agar tidak menutupi lintasan.
3. Gunakan tampilan/ukuran konsisten untuk kedua peta. Simpan gambar asli,
   jangan hanya salinan yang sudah diperkecil di Word.
4. Ganti teks `[PLACEHOLDER ...]` dengan gambar. Caption tetap di bawah gambar.
5. Sesuaikan nomor gambar dengan naskah. Lebar maksimal14cm mengikuti margin;
   pastikan label pada ukuran cetak tidak lebih kecil8pt. Jika terlalu kecil,
   atur ulang tampilan screenshot atau ukuran gambar.

## Apa yang tidak perlu ditambahkan di sini

Ketiga gambar digunakan langsung pada isi4.4.3; tidak wajib diduplikasi pada
Lampiran akhir laporan.4.4.4 cukup uraian keterbatasan, tanpa tabel, gambar,
rumus, diagram PlantUML atau Mermaid baru.

Rekaman lintasan GPS/Huawei Health, foto kondisi/hambatan, catatan penyimpangan,
tanggal/waktu dan perbandingan jarak digunakan pada bagian validasi lapangan.
Bukti tersebut belum diberikan. Jangan memakai screenshot rencana katalog
sebagai pengganti rekaman perjalanan nyata.

## Bukti sumber yang disimpan untuk penelusuran

- katalog_rute_tercatat.json: daftar tiga rute dari sumber Go.
- konfigurasi_tiga_rute.json: konfigurasi B300k/penurunan100k dan start berbeda.
- kebutuhan_gambar.csv: sumber/posisi/caption/status setiap gambar.
- sumber_dan_penempatan.json: sumber, hash, lingkup dan pemeriksaan Word.

JSON/CSV tersebut tidak wajib dicetak sebagai tabel atau Lampiran akhir.
Pengguna menyatakan Toko9 dan Universitas Wijaya Kusuma sudah dicoba,
sedangkan Indomaret belum. Hasil percobaan belum disimpulkan dan metadata
field_validation pada Go tidak diubah oleh pekerjaan naskah ini.
