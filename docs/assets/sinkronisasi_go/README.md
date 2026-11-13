# Aset penyelarasan laporan dengan implementasi Go

Acuan: 12 profil di workdirs/training/output/training pada proyek Go, selesai 11 November 2026. Konfigurasi bersama dan sumber angka tercatat di sumber_dan_ringkasan.json. Ini hasil pengujian dalam batas penelitian, bukan validasi lapangan atau penetapan parameter optimal.

## Pemakaian

- Kode PlantUML tidak memuat nomor bab atau gambar. Render dengan PlantUML; diagram aktivitas memakai orientasi vertikal bawaan, tanpa directive yang mengubahnya menjadi diagram kelas.
- rumus_go.tex menyimpan sumber rumus. Persamaan pada Word panduan juga berupa Equation yang dapat diedit. Sesuaikan nomor persamaan melalui field Word pada naskah utama.
- tabel/ memuat seluruh tabel panduan dalam urutan kemunculannya, sebagai CSV terpisah. evaluasi_per_seed.csv memuat seluruh 60 hasil agar hasil gagal tidak hilang dalam ringkasan.
- Atribut/skor dihitung ulang lewat command analyze Go pada salinan snapshot dan YAML di /private/tmp; output proyek Go tidak ditimpa. Penyebut kelengkapan atribut dan statistik skor adalah semua 58.020 edge terarah, bukan hanya edge yang lolos akses. Width terisi berarti dapat diolah menjadi satu nilai positif dalam meter.
- Gambar PNG untuk Word, SVG untuk ekspor vektor. Label membedakan warna dan pola garis/arsir agar tetap terbaca dalam cetak hitam putih. Tidak ada peta dasar daring atau unduhan baru.
- Grafik training merangkum seluruh lima seed dalam blok 1.000 episode. Grafik overlap terpisah, mencakup semua episode, tanpa pemisahan berhasil/gagal. Ringkasan 10.000 episode terakhir dihitung per seed dan dirata-ratakan dengan bobot sama.
- Rerata galat/skor/overlap rute valid dalam ringkasan_profil.csv hanya memakai loop berhasil; kolom valid menyatakan ukuran sampelnya. all_error_mean_m dan all_q_states_mean memakai seluruh lima seed. Tidak ada imputasi nol untuk profil tanpa rute valid.
- Total langkah adalah jumlah kolom steps pada history seluruh seed, bukan jumlah episode. Pemeriksaan membaca 13.500.000 baris, tanpa training atau replay Q-table baru.
- buat_gambar.py memakai Python/Pandas/Matplotlib yang sudah tersedia di environment analisis Go. CSV yang dibaca disimpan bersama script. Gambar peta membutuhkan snapshot asli pada source_project sebagaimana direkam di JSON; snapshot tidak diduplikasi ke aset ini.

## Batas interpretasi

Pusat snapshot (-7.282187,112.709282) berbeda dari masukan start (-7.281518,112.710178). Data snapshot bertanggal 5 November 2026; training memakai node311432306. Perubahan titik start tidak disebut sebagai download baru. Hasil checkpoint lain dan workdir testing tidak dicampurkan.

Rute berhasil menurut graf belum menjadi rute tervalidasi. Overlap menghitung segmen, bukan meter. Ukuran Q-table adalah jumlah entri state yang tercatat, bukan pembuktian seluruh ruang state sudah dipelajari.

Diagram PlantUML diperiksa struktur sumbernya; rendering PlantUML belum dijalankan lokal. Gambar jarak_langsung_dan_lintasan memakai prefix40 langkah dari B horizon100k total300k seed1; angka contoh ada pada contoh_jarak.json.
