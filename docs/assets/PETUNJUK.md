# Lampiran revisi Bab I sampai III

Berkas diagram dan rumus disimpan permanen di `docs/assets/`.
Word panduan penyalinan tetap berada di
`docs/temp/revisi_bab_1_3_20261104/REVISI_BAB_1_3_TERBARU.docx`.
Dokumen utama TA tidak diubah. Berkas aset tidak bergantung pada folder temp;
simpan dan perbarui sumber diagram serta rumus di folder permanen ini.

## Diagram

- `alur_penelitian.puml`: ganti diagram pada Alur Penelitian.
- `alur_langkah_q_learning.puml`: ganti diagram langkah environment/pelatihan.
- `penyaringan_aksi.puml`: pendamping opsional; uraian dan tabel pada DOCX sudah cukup.

Render menggunakan PlantUML, misalnya plugin/editor PlantUML yang biasa dipakai.
Ekspor SVG agar gambar tetap tajam saat diperbesar di Word. PNG beresolusi tinggi
juga dapat dipakai. Sumber berbentuk activity diagram vertikal, tanpa perintah
`top to bottom direction` yang sebelumnya membuat parser menganggap diagram class.

Kode tidak memuat nomor bab atau nomor gambar. Letakkan caption di bawah gambar
dengan penomoran otomatis Word. Diagram langkah menampilkan satu langkah,
bukan satu episode penuh. Pengulangan langkah dijelaskan pada teks metode.
Sumber telah ditelaah secara struktural; hasil render PlantUML belum dihasilkan
dalam paket ini. Gunakan versi PlantUML yang mendukung sintaks activity standar.

## Persamaan

Persamaan utama dalam DOCX adalah objek matematika Word yang dapat diedit.
Salin dari DOCX agar tidak perlu mengetik ulang. `rumus_revisi.tex` menyediakan
sumber cadangan. Baris yang diawali `%` merupakan komentar dan tidak ikut ditempel.
Untuk sumber LaTeX, masukkan satu persamaan ke area Equation Word dengan mode
LaTeX bila tersedia, lalu ubah ke tampilan Professional. Dukungan `cases` dapat
berbeda menurut versi Word; rumus arah pada DOCX disediakan sebagai persamaan
terpisah dengan penjelasan kondisi sehingga tidak bergantung pada dukungan itu.

Nomor persamaan sengaja tidak dipasang permanen. Setelah menyalin, gunakan nomor
bab yang benar, perbarui urutan caption dan rujukan silang. Persamaan ditempatkan
1,5 cm dari kiri teks dengan nomor di batas kanan sesuai panduan kampus.

## Dasar konfigurasi

Pemetaan aktif: prioritas +1, lainnya -1, missing -0,5; bobot 0,55/0,30/0,15;
akses permissive -0,10 per 100 m; arah 0,60; revisit -10; sukses +100; gagal -50.
Missing -0,5 dan revisit -10 mengikuti eksperimen aktif, bukan penetapan keputusan
baru setelah diskusi terakhir. Tidak ada revisi kode, training, atau unduhan graf.

Materi verifikasi, hasil Bab IV, dan validasi lapangan tidak disusun dalam paket ini.
