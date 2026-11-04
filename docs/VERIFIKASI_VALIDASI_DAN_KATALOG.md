# Kesepakatan verifikasi, validasi, dan katalog rute

Disinkronkan pada 2 November 2026. Dokumen ini menyimpan hasil diskusi dan batas
pekerjaan untuk dilanjutkan nanti. Rencana di sini belum menjadi implementasi
atau hasil validasi. Dokumen TA utama tidak diubah langsung; pengguna memindahkan
materi dari chat atau Word sementara secara manual.

## Status saat ini

| Bagian | Status |
|---|---|
| Core bersama, train_step, latest_state, pencatatan komponen reward | Tersedia |
| Highway/surface satu prioritas, width ambang 3 m; H/S/W +1/-1/0 | Aktif di core dan analisis |
| Penalti permissive dan whitelist akses | Aktif |
| Service | Reward dasar highway -1; tetap legal jika lolos access/mask |
| Training reward_direct_20261103 | Selesai: 60 training/6.750.000 episode; 60 evaluasi direproduksi |
| Arsip surface_width_3m_20261102 | Selesai dijalankan pengguna; 60 training/6.750.000 episode diperiksa |
| Replay evaluasi dari Q-table | 60/60 cocok dengan metrik dan lintasan tersimpan |
| uji_titik_start.ipynb | Unduh graf sekitar koordinat baru dan satu training acak tercatat; training panjang belum dijalankan agent |
| verifikasi.ipynb poin 1–5 | 32 cell kode dijalankan ulang, termasuk contoh overlap 20%, pada 3 November |
| Pemeriksaan dan rekaman lapangan | Direncanakan, belum dilaksanakan |
| Ekspor GPX/navigasi | Ditunda |
| Aplikasi katalog rute | Disepakati sebagai bentuk pemanfaatan; belum dibuat |

Hasil terbaru dan keterbatasannya: [analisis reward langsung](temp/analisis_reward_direct_20261103/ANALISIS.md). Arsip reward sebelumnya: [analisis surface/width](temp/analisis_surface_width_3m_20261102/ANALISIS.md).
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
| State dan action mask | A/B/C, bin progres, previous_node, reset, edge paralel, whitelist akses, closing dan revisit | Nilai harapan eksplisit dan jejak satu langkah per cell; eksplorasi, greedy dan bootstrap harus memakai action legal |
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

Acuan notebook sudah diperbarui untuk reward langsung 3 November dan dijalankan
ulang. Kelulusan kode tetap berbeda dari evaluasi eksperimen atau review lapangan.
Hasil training baru belum tersedia; hasil lama tetap menurut konfigurasi arsip.

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

Kandidat konfigurasi yang disarankan untuk sumber awal: B/150k/horizon 50k,
dengan C/75k/dinamis sebagai tambahan. Pemilihan rute tetap berdasarkan hasil,
kemiripan dan pemeriksaan lapangan, bukan mengambil semua seed secara otomatis.
Notebook [uji titik start](../uji_titik_start.ipynb) menyediakan pencarian start
lain dengan unduhan graf baru dan satu training acak memakai core bersama; tidak berarti
Q-table lama telah bisa digeneralisasikan ke start bebas.

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

## Pencatatan overlap aktif (3 November 2026)

Pengguna memilih satu metrik overlap_ratio untuk setiap episode training dan
evaluasi akhir. Implementasi core sudah aktif, section grafik overlap terpisah.
Tidak ada perubahan reward/aturan revisit. A--C menargetkan grup baru
reward_direct_overlap_count_20261103; hasil berbasis meter tetap pada grup lama.
Hasil lengkap sebelumnya dan validasi lapangan tetap dibedakan.

Klarifikasi terakhir: overlap_ratio berdasarkan jumlah lintasan ruas,
bukan meter. Grafik hanya seluruh episode, tanpa penyaringan berhasil/gagal.
Contoh verifikasi 1/5=20% memakai ruas dengan panjang berbeda untuk memastikan
bobot panjang tidak masuk perhitungan. Reward dan aturan tetap.


## Eksperimen penalti revisit -3 (3 November 2026)

Pengguna menyetujui perubahan penalti node revisit dari -1 menjadi -3. Core bersama
berlaku untuk A/B/C dan uji titik start; mask dan komponen reward lain tetap.
Grup berikutnya reward_revisit_3_overlap_count_20261103 belum dilatih. Pembanding
-1 reward_direct_overlap_count_20261103 tetap disimpan. Verifikasi memakai
expected literal -3 dan total -1,40 pada contoh ruas/arah pulang 100 m.
Bandingkan keberhasilan loop dan overlap_ratio pada graf/seed/konfigurasi sama.
Penalti node juga berlaku bila persimpangan lama dicapai melalui ruas baru;
tidak identik dengan penalti pengulangan ruas, dan tidak menjamin overlap hilang.


## Pembaruan penalti -5 dan eksekusi paralel (3 November 2026)

Penalti node revisit aktif -5. Expected manual contoh 100 m ideal, mendekat
100 m pada fase pulang, nonterminal/tanpa akses: +1+0,60-5=-3,40. Seluruh 32 cell
verifikasi lulus. Mode paralel hanya menjalankan seed independen bersamaan;
Q-learning setiap seed tidak berubah. Parity Q/history/metrik/rute diuji pada
graf sintetis dan snapshot OSM, serta pemanggilan dari kernel Jupyter bersih.
A--C memakai MAX_WORKERS=2, core default 1; uji titik satu seed tetap satu proses.
Hasil -5 belum dilatih, grup baru reward_revisit_5_overlap_count_20261103.
Hasil -3 tetap pembanding; tidak ada validasi lapangan atau pengukuran kecepatan
training penuh pada perubahan ini. Rincian IMPLEMENTASI bagian 2.2, audit pada
docs/temp/verifikasi_revisit5_paralel_20261103/.


## Parameter terbaru -10 dan tiga worker (3 November 2026)

Pengguna meminta penalti node revisit -10 dan MAX_WORKERS=3 untuk A--C. Expected
contoh ruas ideal 100 m/mendekat 100 m pada fase pulang menjadi +1+0,60-10=-8,40.
Seluruh 32 cell verifikasi lulus pada kernel bersih. Uji lima seed melalui
Jupyter menunjukkan Q/history/metrik/rute identik 1 vs 3 worker; metadata baru
merekam -10 dan tiga proses. Grup reward_revisit_10_overlap_count_20261103 belum
dilatih. Hasil -5 tetap arsip pembanding; belum ada hasil atau validasi lapangan
untuk parameter -10. Audit: docs/temp/verifikasi_revisit10_workers3_20261103/.


## Audit hasil -10 lengkap (3 November 2026)

A--C selesai60 training/6.750.000 episode;25/60 evaluasi greedy valid. Seluruh60
Q-table dievaluasi ulang, metrik/path cocok, overlap dihitung ulang independen.
Ini audit kode/hasil eksperimen, bukan validasi lapangan. B/C35/40 pada -5 turun
ke22/40 pada -10. Sembilan loop valid overlap0%, tetapi sebelas rute gagal juga
overlap0%; tetap gunakan syarat kembali ke start pada4.500--5.500m. Laporan
lengkap: docs/temp/analisis_ABC_revisit10_20261103/ANALISIS.md.


## Audit missing -0,5 lengkap (4 November 2026)

Semua12konfigurasi kini berada pada reward_missing_05_20261103 termasuk B yang
sudah dilatih ulang.60training/6.750.000history; seluruh60greedy direproduksi,
metrik/path dan overlap geometri cocok. Metadata sama: missing-0,5/highwayother-1,
tanpa clipping/revisit-10/lima seed/tiga worker.240file sumber dan graf tetap.
Loop A/B/C: dinamis75K0/0/1; dinamis150K0/3/1; horizon50K total75K0/2/5;
horizon50K total150K2/4/5. Total23/60: A2,B9,C12.37gagal=29overdistance+8buntu,
semua tidak pernah memiliki closing action legal. C horizon75K kandidat:5/5,
galat141,57m/overlap1,15%; C horizon150K5/5 tetapi galat276,57m/overlap1,22%.
B dinamis150K3/5 melampaui C1/5; jangan mengklaim C selalu unggul/optimal.
Seluruh23loop utama tanpa service tetapi masih permissive/data kosong. Uji titik
lain terpisah3/3loop,2rute masih memakai637,15m service. Bukti lapangan/UI belum
ditinjau.32cell verifikasi tersimpan tanpa error. Bahan eksperimen cukup untuk
mulai BabIV; lanjutkan pembahasan state/epsilon/seed/kegagalan, sinkronisasi naskah,
validasi lapangan dan katalog. Naskah lama masih skor0-1/netral0,50/hasil30-75K;
Word tidak diubah. Tanpa training/unduhan baru atau perubahan raw data.
Laporan/CSV/grafik: docs/temp/analisis_missing_05_20261104/ANALISIS.md.
