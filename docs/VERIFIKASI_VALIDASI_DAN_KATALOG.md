# Kesepakatan verifikasi, validasi, dan katalog rute

Disinkronkan pada 2 November 2026. Dokumen ini menyimpan hasil diskusi dan batas
pekerjaan untuk dilanjutkan nanti. Rencana di sini belum menjadi implementasi
atau hasil validasi. Dokumen TA utama tidak diubah langsung; pengguna memindahkan
materi dari chat atau Word sementara secara manual.

## Status saat ini

| Bagian | Status |
|---|---|
| Core bersama, train_step, latest_state, pencatatan komponen reward | Tersedia |
| Highway dua prioritas, surface satu prioritas, width ambang 3 m | Aktif di core dan analisis |
| Penalti permissive dan blacklist akses | Aktif |
| Training surface_width_3m_20261102 | Selesai dijalankan pengguna; 60 training/6.750.000 episode diperiksa |
| Replay evaluasi dari Q-table | 60/60 cocok dengan metrik dan lintasan tersimpan |
| verifikasi.ipynb poin 1–5 | Implementasi lama tersedia; acuan/output belum disesuaikan dengan skor/akses terbaru |
| Pemeriksaan dan rekaman lapangan | Direncanakan, belum dilaksanakan |
| Ekspor GPX/navigasi | Ditunda |
| Aplikasi katalog rute | Disepakati sebagai bentuk pemanfaatan; belum dibuat |

Hasil terbaru dan keterbatasannya: [laporan training](temp/analisis_surface_width_3m_20261102/ANALISIS.md).
Rincian aturan aktif: [IMPLEMENTASI.md](../IMPLEMENTASI.md).

## Tiga lapisan bukti

| Lapisan | Pertanyaan | Bukti yang disiapkan |
|---|---|---|
| Verifikasi implementasi | Apakah program sesuai rancangan? | Hitungan manual, nilai harapan independen, assertion, jejak state/action/reward/Q |
| Evaluasi eksperimen | Bagaimana pengaruh representasi state? | Perbandingan A–C pada graf/reward/mask/seed/episode/epsilon yang sama; hasil greedy per seed |
| Validasi lapangan | Apakah rute terpilih dapat diikuti pada kondisi nyata? | Jejak aktivitas, catatan akses/hambatan dan perbandingan terhadap rute hasil sistem |

Kelulusan sejumlah kasus tidak membuktikan seluruh kode bebas bug. Bukti
konvergensi teoretis bukan bukti implementasi benar. Keberhasilan greedy juga
belum membuktikan keamanan aktual, kenyamanan menurut pelari, atau generalisasi
ke titik awal lain. Pengulangan evaluasi deterministik pada model/start yang sama
tidak menjadi training seed independen baru.

## Verifikasi yang akan ditinjau kembali

Gunakan core bersama. Tidak perlu class QValueUpdater, framework pengujian baru,
atau penulisan ulang algoritma khusus di notebook. Graf sintetis dibuat sebagai
nx.MultiDiGraph dengan struktur node/edge seperti OSMnx, atribut OSM sintetis,
ID positif, add_comfort_scores(), lalu build_actions(). Graf nyata memakai
snapshot lokal; tidak perlu mengunduh ulang untuk tiap pengujian.

| Poin | Kasus penting | Cara pemeriksaan |
|---|---|---|
| Q-value | Transisi nonterminal dengan Q berikutnya tidak nol; reward akses; terminal tanpa bootstrap | Tulis Q lama, alpha, gamma, reward, max Q legal, target dan Q baru; cocokkan dengan train_step |
| State dan action mask | A/B/C, bin progres, previous_node, reset, edge paralel, blacklist akses, closing dan revisit | Nilai harapan eksplisit dan jejak satu langkah per cell; eksplorasi, greedy dan bootstrap harus memakai action legal |
| Graf dan akumulasi jarak | Identitas (u,v,key), koordinat/proyeksi, panjang edge dan lintasan | Graf sintetis untuk hasil yang diketahui; snapshot OSM untuk integrasi/struktur nyata |
| Terminasi | Success inklusif 4.500–5.500 m, overshoot, buntu, batas langkah, tidak menerima langkah setelah done | Kondisi batas terkontrol beserta alasan terminasi; early_return sudah dihapus |
| Reward | H/S/W, permissive, arah, revisit, terminal/buntu dan jumlah komponen | Hitungan komponen independen serta contoh lintasan sukses/gagal; aritmetika dipisahkan dari analisis perilaku |

Hitung manual tetap dipakai pada beberapa transisi representatif, bukan seluruh
training atau semua langkah setiap episode. Sertakan contoh terminal agar tidak
mengambil nilai Q lanjutan setelah episode selesai. Bandingkan bilangan desimal
dengan toleransi numerik yang wajar; bukan kesamaan teks angka yang dibulatkan.
Expected value tidak boleh hanya diproduksi oleh fungsi yang sedang diuji.

State harus hanya memuat komponen definisi skenario. Environment tetap menyimpan
jarak/riwayat untuk transisi, reward, terminasi dan mask bersama; penggunaan kondisi
penuh oleh aturan tersebut bukan otomatis kebocoran informasi ke struktur state.
Aturan bantuan yang sama harus dinyatakan untuk semua A–C. Representasi state
ringkas tidak otomatis memenuhi seluruh sifat Markov; jangan mengklaim assertion
state membuktikan kelengkapan informasinya.

Tidak perlu menganggap reward seluruh rute sukses selalu lebih tinggi daripada
semua kegagalan. Periksa potensi perilaku menyimpang dan hubungkan return dengan
keberhasilan tugas. Uji stres edge 100 km pada notebook lama berada di luar
rentang snapshot; tinjau relevansinya, jangan menyatakannya sebagai ruas nyata.

Acuan notebook perlu diperbarui untuk highway, surface, width, penalti permissive,
blacklist serta jumlah action yang berubah. Output lulus 29 Oktober hanya berlaku
untuk konfigurasi saat itu. Pemeriksaan kecil implementasi terbaru dan replay
hasil training tidak berarti notebook tersebut sudah direvisi atau lulus sekarang.

## Validasi lapangan

- Pengguna ingin mencoba sendiri rute yang benar-benar dihasilkan. Ambil kandidat
  dari evaluasi berhasil, kemungkinan B/C; state gagal tetap dilaporkan dalam eksperimen.
- Gunakan Huawei Watch Fit 3 dan Huawei Health untuk merekam bentuk lintasan,
  jarak, dan aktivitas. Huawei Health saja cukup; Strava bukan kebutuhan wajib.
- Catat identitas rute, asal skenario/konfigurasi/seed, waktu pemeriksaan, kesesuaian
  lintasan, hambatan seperti pagar/jalan tertutup, dan penyimpangan yang terpaksa diambil.
- Jika rute aktual berubah karena hambatan, simpan perbedaannya; jangan menyatakan
  bahwa lintasan yang dimodifikasi identik dengan rute yang divalidasi.
- Panjang dari penjumlahan edge graf dan GPS dibandingkan dengan memperhitungkan
  ketidakpastian GPS/geometri. Huawei bukan alat ukur jarak mutlak benar.
- Jumlah sampel, batas deviasi yang diterima dan format bukti akhir belum ditetapkan.
  Jangan memasukkan angka toleransi GPS baru tanpa dibahas.
- Tidak tumpang tindih adalah contoh dari penguji, bukan syarat mutlak penelitian.
  Pengguna mempertahankan aturan revisit sekarang agar agen tidak terlalu dibatasi.

Access=permissive bukan sinonim pagar tertutup. Width >=3 m juga bukan jaminan
ruang bebas pelari. Semua 27 loop valid terbaru masih memuat ruas <3 m, width
kosong dan permissive; pemeriksaan peta/lapangan tetap diperlukan. Hasil lapangan
berlaku pada rute dan kondisi/waktu yang diperiksa.

GPX untuk membantu mengikuti jalur telah dibahas, tetapi implementasinya ditunda
sampai kandidat rute dan kebijakan akses dinilai. Dukungan navigasi perangkat juga
belum dipastikan; jangan menjanjikan impor/navigasi GPX pada jam tanpa pemeriksaan.

## Practical implications

Manfaat penelitian yang akan dibahas berdasarkan bukti:

1. Membantu perencanaan kandidat rute lari lokal sekitar 5 km yang kembali ke titik
   awal dan mempertimbangkan karakter ruas jalan.
2. Memberi pertimbangan bagi pengembang tentang informasi state, keberhasilan,
   dan ukuran Q-table berdasarkan konfigurasi yang diuji.
3. Memperlihatkan kegunaan dan keterbatasan data OSM melalui kecocokan graf dengan
   kondisi aktual, terutama akses dan hambatan yang belum tercatat.

Tidak mengklaim penghematan waktu, kenyamanan, atau keamanan pengguna tanpa
pengukuran yang relevan. Perbandingan skor karakter berbasis OSM tidak sama
dengan hasil survei persepsi. Praktikal implikasi tidak mensyaratkan dukungan
semua titik awal. Rumusan masalah tetap berfokus pada reward serta pengaruh
representasi state; strategi epsilon merupakan faktor eksperimen pendamping.

## Bentuk aplikasi: katalog rute

Pembimbing menyarankan menghasilkan beberapa rute lebih dahulu, menyimpan hasil
terpilih, lalu menyediakan UI untuk melihatnya. Kesepakatan alurnya:

Training offline -> kandidat rute -> evaluasi dan seleksi -> simpan -> tampilkan
melalui aplikasi. Pengguna melihat daftar, memilih rute, lalu melihat peta,
titik awal/akhir, panjang, dan status pemeriksaan lapangan.

Tidak perlu melatih agen saat aplikasi dibuka atau menerima titik awal bebas.
Training pada satu start tidak otomatis berhasil untuk start lain. Framework UI
belum ditetapkan; Streamlit hanya pernah disebut sebagai kemungkinan.

Data calon katalog: ID/nama rute, urutan edge dan geometri, start/panjang,
skenario/konfigurasi/seed, status/tanggal pemeriksaan dan catatan hambatan.
Artefak rute JSON eksperimen sudah tersedia sebagai sumber, tetapi penyimpanan
katalog khusus dan UI belum dibuat.

Pilih rute valid; kegagalan tetap tercantum pada laporan eksperimen. Tidak perlu
memaksakan jumlah tertentu atau mengambil rute dari setiap state. Tinjau
kemiripan geografis, bukan hanya perbedaan ID atau urutan edge. Dua puluh tujuh
lintasan valid terbaru berbeda persis secara urutan, tetapi belum tentu menjadi
27 pilihan katalog yang cukup berbeda secara penggunaan.

Katalog adalah bentuk pemanfaatan. Hasil utama penelitian tetap perancangan
reward dan evaluasi pengaruh representasi state, sesuai rumusan masalah.

## Referensi dan langkah berikutnya

[Kandidat rujukan](../referensi.md#kandidat-referensi-verifikasi-dan-evaluasi-q-learning-2-november-2026)
memuat sumber yang dibahas. Banyak paper melaporkan evaluasi performa tanpa
menjelaskan unit test atau hitung manual; jangan mengatribusikan metode yang
sebenarnya tidak dilaporkan. DQN/MLP/varian dua pemain harus dibedakan dari Q-table.

Pada sesi berikutnya, lanjutkan dari hasil terbaru yang sudah tersimpan. Tinjau
reward bila pengguna meminta, sesuaikan verifikasi setelah desain ditetapkan,
lalu rencanakan seleksi kandidat, pemeriksaan lapangan, ekspor dan katalog secara
bertahap. Dokumen ini tidak menjalankan pekerjaan lanjutan tersebut otomatis.
