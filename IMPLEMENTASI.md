# Wiki Implementasi Rute Lari Loop 5 KM

Dokumen ini menyimpan konteks implementasi dan keputusan teknis penelitian. Acuan aktif untuk pengembangan kode dan hasil TA adalah proyek Go pada bagian berikut. Rincian Python di bagian sesudahnya dipertahankan sebagai riwayat; jangan memakainya untuk menggantikan konfigurasi Go terbaru.

Dokumen ini bukan BAB IV skripsi. Untuk naskah TA gunakan dokumen skripsi; wiki ini menyimpan rincian teknis yang terlalu panjang untuk naskah akademik.

## Kandidat validasi lapangan — 12 November 2026

Pengguna menetapkan tiga rute dari tiga titik awal berbeda, seluruhnya memakai
B horizon100k-total300k. Katalog Go lokal: depan-gang-sebelah-toko9
(seed13916397716709765191,5151,87m), depan-indomaret-dkb
(seed16261264761017114444,5298,84m), depan-uwika
(seed9988407548480542851,5527,50m). Ketiganya masih field_validation=not_recorded;
ini kandidat untuk diperiksa, bukan hasil validasi atau pengganti60run eksperimen.
Catat rekaman lintasan/loop, jarak GPS vs graf, akses/hambatan dan penyimpangan;
temuan gagal tetap dilaporkan. Hasil terbatas pada tiga rute/kondisi pemeriksaan.
Config testing kini hanya B horizon100k-total300k dengan lima seed acak. Katalog
menyimpan config/metadata sumber sehingga tidak berubah saat testing titik lain.
Katalog lokal tiga rute belum berarti versi publik sudah diperbarui; perlu push
serta deployment. Checkpoint Go:3af6b27; tes/vet/build dan integritas tiga rute
lulus. Naskah/DOCX utama dan revisi bab sesi lain tidak diubah.

## Katalog publik aktif — 12 November 2026

[Katalog rute lari](https://davidimannuel.github.io/go-running-route-q-learning/) sudah dipublikasikan melalui GitHub
Pages. Pemeriksaan browser12November menemukan indeks dengan satu rute pilihan,
depan-gang-sebelah-toko9. Source memakai GitHub Actions dan workflow
.github/workflows/catalog-pages.yml, mengunggah hanya web-catalog. Perubahan lokal
add/rm/clear baru terlihat publik setelah commit/push dan deployment berhasil.
Run awal gagal Get Pages site failed/404 ketika Pages belum aktif; setelah Source
GitHub Actions dipilih dan workflow dijalankan ulang, pengguna menyatakan berhasil
dan indeks publik dapat dibuka. field_validation=not_recorded tetap berlaku.
Tidak menjalankan training/analisis baru, mengubah hasil ilmiah, atau DOCX.

## Riwayat checkpoint katalog dan CLI Go — 12 November 2026

Cakupan checkpoint: workflow run (download → analyze → train), katalog
add/rm/clear, situs statis/Pages, panel rute/analisis Minimize/Show details, serta
README/AGENTS/bantuan CLI. Go test/race CLI/vet/build lulus pada kode checkpoint.
Tidak mengubah core RL atau menjalankan unduhan/training penelitian.

Status lokal terbaru: setelah clear, pengguna menambahkan kembali rute
`depan-gang-sebelah-toko9`, profil b-horizon-100000-total-300000,
seed12226258565145578727, jarak5337,56m dari metadata tersimpan. web-catalog berisi
satu rute standard lengkap; bukan katalog kosong lagi. field_validation masih
not_recorded. Rute pilihan adalah contoh pemanfaatan terpisah dari60evaluasi
penelitian; tidak mengganti angka Bab IV. Situs/workflow disertakan pada checkpoint
Go pada ee2ddb9 dan dokumentasi6768c16. Pengguna kemudian push/deploy.
Perubahan koordinat testing, output notebook dan revisi
naskah/aset sesi lain tetap dipisahkan dari commit pekerjaan CLI/katalog ini.

## Command gabungan download, analyze, train — 12 November 2026

Pada repo Go, jalankan `go run ./cmd/cli run --workdir workdirs/testing` atau
`--workdir workdirs/training` dari root repo Go. Untuk satu profil tambahkan
`--profile b-horizon-100000-total-300000`. Download selalu dijalankan untuk
menyiapkan osm.json berdasarkan koordinat/radius config sekarang; cache memakai
query yang sesuai. `--force` meminta data baru ke Overpass, `--debug` menambah log.
Tidak ada opsi snapshot pada command gabungan. Config dan profil divalidasi dahulu.

Urutan download → analyze → train berhenti pada kegagalan/pembatalan pertama.
Hasil tahap sebelumnya tetap tersimpan; bukan transaksi seluruh output. Profil
lain yang tidak dipilih tetap ada sesuai aturan train. Gunakan output_dir berbeda
untuk mempertahankan percobaan sebelumnya, periksa metadata ketika lokasi berubah,
dan jangan mengedit config saat proses berjalan. Notebook, export dan catalog
tetap command/alur terpisah. Tidak ada parameter RL atau data penelitian diubah
untuk fitur ini; pengujian memakai snapshot sintetis dan fetcher lokal.

## Penambahan rute pilihan ke web-catalog — 12 November 2026

Penghapusan SATU rute: `go run ./cmd/cli catalog rm <id>`. Folder lain memakai
`catalog rm --dir <folder> <id>`; flag mendahului ID. Tanpa workdir/seed/prompt
tambahan. Folder rute pilihan dibuang di staging, entri manifest dihapus dan
indeks diperbarui bersama. Rute lain serta hasil sumber tetap utuh; rute terakhir
menyisakan katalog kosong. ID tidak ditemukan tidak mengubah katalog. Memakai
validasi folder dan lock yang sama dengan add/clear. Clear tetap untuk reset
SELURUH katalog atau memulihkan struktur yang terhapus sebagian. Tes lokal
memakai fixture; tidak menghapus rute nyata pada penambahan command rm ini.

Untuk mengosongkan seluruh katalog: `go run ./cmd/cli catalog clear` dari root
repo Go, opsional `--dir <folder>`/`--debug`. Tidak memerlukan workdir atau seed.
Command langsung menghapus seluruh pilihan, membuat ulang index.html, manifest
routes=[] standard, .nojekyll dan routes/ kosong. Memulihkan katalog yang manifest
atau map-nya terhapus sebagian. Folder di luar struktur katalog/symlink ditolak;
lock sama dengan add, indeks kosong dibuat di staging sebelum publikasi lokal.
Hasil download/analisis/training tetap. User meminta reset dan sudah dijalankan
12November; katalog sempat kosong, kemudian pengguna menambahkan satu rute
dan melakukan publikasi. Clear berikutnya tetap hanya lokal sampai push/deploy.
Hindari menghapus folder rute/manifest secara manual.

Command Go `catalog add --workdir <folder> --profile <nama> --seed <seed>`
meminta **Route ID** dan **Route description**, tanpa nama/koordinat/config
katalog khusus. Workdir sekarang hanya menentukan output_dir; graf, lokasi,
reward, rute dan konfigurasi training dibaca dari HTML/metadata hasil tersimpan.
Seed harus ada dan berhasil membentuk loop sesuai batas jarak metadata. Identitas
skenario/seed/graf/start, metrik evaluasi dan kontinuitas/jarak loop diperiksa
sebelum publikasi lokal; ini bukan pengujian kelayakan lapangan.

Alur pemakaian: ubah koordinat config → jalankan cli run → periksa peta/metrik
dan pilih seed → catalog add → periksa katalog → commit/push untuk publikasi.
Catalog add hanya membuat ulang presentasi seed pilihan dari hasil tersimpan;
tidak menjalankan download, analyze atau train, dan tidak membutuhkan cli export
terlebih dahulu. Tambahkan rute pilihan sebelum hasil sumber ditimpa percobaan
lokasi berikutnya. Command add sendiri tidak melakukan commit/push/deployment.

Pembaruan tampilan12November: panel rute/analisis mempunyai Minimize/Show details.
Layar kecil/landscape pendek mulai ringkas, saat terbuka maksimal55%tinggi
viewport dan dapat digulir. Kontrol tetap terpasang sehingga seed/KM/layer tidak
reset; padding fit/popup mengikuti ukuran panel. Menu layer rute ringkas pada HP,
zoom di kiri bawah, tinggi map mengikuti viewport dinamis. Browser diuji pada
320/390portrait,844landscape dan1280desktop tanpa overflow horizontal atau error
console. Go test/vet/build lulus. HTML hasil nyata belum diregenerasi; pratinjau
menggunakan salinan rute katalog di /tmp, tanpa perubahan hasil/metadata/training.

Keluaran `web-catalog/`: index.html, catalog.json, .nojekyll dan
routes/<id>/{index.html,details.html,metadata.json}. Selalu mode standard,
walaupun sumber advanced. Satu seed pilihan, graf/layer/atribut/reward lengkap,
tanpa Q-values/request backend. Metadata sumber tetap dan ditambah identitas
katalog, mode, tanggal, status field_validation=not_recorded serta hash HTML.
Tabel detail hanya menampilkan seed pilihan; batch asal tetap dalam JSON lengkap.
ID lama meminta input lain. Penambahan menyalin katalog lama ke staging,
memperbarui indeks dan menerbitkan seluruh paket; lock mencegah penulisan ganda.
Tidak menyalin snapshot/CSV/Q atau mengubah hasil asli.

Workflow .github/workflows/catalog-pages.yml pada repo Go mengunggah hanya
web-catalog ke GitHub Pages setelah push main/perubahan folder terkait atau
dispatch manual. Pengguna perlu memilih Pages source=GitHub Actions. Tautan
relatif mendukung subfolder repositori; Leaflet dan tile OSM dimuat HTTPS di
browser, attribution/referrer dipertahankan. Katalog awalnya kosong; sekarang
sudah berisi satu rute dan dapat dibuka melalui URL publik di atas.
Uji sintetis Go/race/vet/build lulus; preview browser
berhasil pada subfolder tanpa backend Go. Tidak menjalankan training/unduhan
atau menambahkan hasil nyata ke katalog secara otomatis. Dokumen TA tetap.

## Pembaruan HTML hasil Go — 12 November 2026

`export.map_mode` mengatur presentasi: testing memakai `standard`, training
`advanced`; bila dihilangkan, default advanced. Standard mempertahankan graf,
seluruh seed/metrik, layer comfort/access/node, popup atribut/reward, per-KM,
arah dan overlap; hanya inspeksi Q-values yang tidak disertakan. Advanced memakai
endpoint Q lokal. Leaflet/CDN dan tile OSM tetap eksternal; seluruh graf tertanam
sehingga mode standard belum mengurangi ukuran HTML secara berarti.

Command `go run ./cmd/cli export --workdir workdirs/testing` (atau training)
kini memperbarui HTML pada lokasi asli: road-analysis.html/analysis.html serta
training/<profil>/routes.html/report.html. Opsi --profile hanya memperbarui profil
terpilih; profil lain dan analisis tetap. Tanpa opsi, seluruh hasil tersimpan
ikut diperbarui. All results kembali ke indeks CLI serve, bukan katalog salinan.

Data diambil dari payload HTML/metadata tersimpan; YAML hanya menentukan output
dan mode presentasi. Tidak training/unduhan atau mengubah CSV, Q-table, snapshot,
config maupun metadata eksperimen. Analisis lama mempertahankan skor/tanggalnya.
output/export.json schema2 mencatat pembaruan terakhir dan hash HTML sebelum
pembaruan. Mode advanced memakai Q-table dari direktori hasil yang sama.

Semua HTML disiapkan dahulu; kegagalan publikasi/pembatalan memulihkan file lama,
tanpa jaminan transaksi tahan crash. Jangan bersamaan dengan train/analyze pada
workdir yang sama. Folder site lama dibersihkan hanya jika manifest schema1 dan
struktur hasil ekspor cocok; file tambahan/symlink/manifest asing ditolak tanpa
perubahan. web-catalog/deployment tetap terpisah. Alur ini menggantikan paket
output/site versi11November agar tidak muncul dua versi HTML hasil yang sama.

Navigasi seed memakai tombol kiri/kanan, nomor run, seed uint64 lengkap sebagai
teks dan penjelasan sumber tetap/acak dari metadata. Tautan profil/seed tersimpan
di URL; representative tetap memakai pemeringkatan semula. Advanced membaca
Q dari hasil pada direktori yang sama melalui CLI server.
Pengujian memakai fixture sintetis dan browser; tes Go, vet, build lulus. Hasil
pengguna belum diekspor ulang, diunggah atau dilatih ulang. Ini fasilitas
publikasi/inspeksi, belum keputusan seleksi katalog atau validasi lapangan.

## Acuan implementasi Go — sinkronisasi 9 November 2026

### Lokasi, sumber dan status

Kode aktif: `/Users/david/development/go-running-route-q-learning`.
Repositori TA ini menyimpan naskah, aset dan Markdown progres; kode/notebook
Python tetap riwayat. Naskah utama hanya diedit pengguna. Sinkronisasi ini
membaca chat **“Jawab pertanyaan umum”**, lalu mencocokkan sumber Go, YAML,
metadata dan CSV evaluasi terbaru. Tidak mengubah kode, config, notebook,
snapshot, hasil training atau DOCX; tidak menjalankan training/unduhan.

Sumber parameter: `workdirs/training/config.yaml` dan `workdirs/testing/config.yaml`
di proyek Go. Sumber hasil adalah `output/training-run.json` dan
`output/training/<profil>/{metadata.json, history.csv, evaluation.csv}`;
Q-table/trace berada pada `seed-<seed>/{qtable.csv, evaluation-steps.csv}`.
Gunakan metadata saat training, karena YAML dapat berubah setelahnya.
Pengguna masih mencoba parameter; batch terbaru belum otomatis menjadi pilihan
final naskah. Ringkasan berikut menggantikan acuan 31/60 tanggal 7 November.

### Konfigurasi aktif dan aturan yang dipakai

| Komponen | Implementasi Go terbaru |
|---|---|
| Target dan validitas | Kembali ke start dan panjang 4.000–6.000 m; target 5.000 m, toleransi 20% |
| Graf | Segmen OSM mentah dua arah, parallel edge dipertahankan; tanpa simplifikasi, seleksi komponen atau truncation setara OSMnx |
| Jarak | Haversine per segmen dan ke start, radius bumi 6.371.009 m; tidak memakai proyeksi UTM |
| State | A=current; B=current+progress bin; C=current+previous+progress bin |
| Progres | 25 bin pada 0–6.000 m, lebar 240 m; reset previous=−1 |
| Training | A/B/C × dinamis 150k/300k dan horizon 100k-total 150k/300k;12 profil/60 run/13.500.000 episode |
| Epsilon | Linear 1→0,05 sepanjang total episode atau mencapai 0,05 pada 100k lalu tetap; evaluasi greedy 0 |
| Parameter | alpha 0,15; gamma 0,95; max_steps 500; seed 0–4; max_workers 5; Q/RNG mandiri tiap seed, mulai dari kosong |
| Revisit | Diizinkan setelah 2.500 m, maksimum 2 kunjungan node; penalti −10 selain closing ke start |
| Highway | footway/pedestrian/living_street/residential/tertiary:+1; secondary:+0,5; other termasuk service:−10; kosong:−2 |
| Surface/width | Surface asphalt/concrete/paving_stones/paved:+1; width valid>=3 m:+1; lainnya −1, kosong/width invalid −0,5 |
| Reward ruas | Bobot H/S/W 0,55/0,30/0,15; gabungan tanpa clipping dikali panjang/100; bukan ukuran keamanan/kenyamanan lapangan |
| Arah | Outward 0; return 1,20 setelah 50% target; Haversine dan prioritas terminal tetap; bukan bonus langsung menjauh |
| Reward lain | Permissive way −0,10/100 m; sukses +100; over_distance/buntu/batas langkah −50; galat jarak akhir −5/100 m |
| Akses | Kosong/yes/permissive pada way, source dan destination; scalar ternormalisasi, tanpa split/list/override foot; barrier saja tidak melarang |
| Action | `(next_node, key)`; terurut numerik, key paralel tetap berbeda; mask legal bersama untuk eksplorasi/greedy/bootstrap |
| Overlap | `(jumlah lintasan−jumlah ruas fisik unik)/jumlah lintasan`; identitas endpoint tanpa arah; bukan persentase panjang |

Start training aktif `311432306`, input `-7.281518, 112.710178`.
Snapshot 26.345 node/58.020 edge, SHA-256:
`f0a5885db46c2f9cd962674aaeaa82f7d5c69579d5ba5d80641f727b6e20f964`.
Node mentah mencakup pembentuk geometri, bukan seluruhnya persimpangan.
Service tetap dapat dipilih bila lolos akses; skor negatif tidak menghapus action.
Filter akses endpoint sudah diterapkan; temuan gerbang/no pada 31 loop 7 November
adalah riwayat sebelum filter, bukan deskripsi semua hasil terbaru.

### Penalti galat jarak akhir yang sudah diimplementasikan

Pengguna memilih mempertahankan terminasi over_distance dan mask closing.
Penalti tambahan mengikuti:

```text
reward_distance_error = distance_error_penalty_per_100m
                        * abs(total_distance_m - target_distance_m) / 100
```

Koefisien aktif −5. Panjang 4.800 m maupun 5.200 m mendapat −10;5.050 m mendapat −2,5;
tepat 5.000 m mendapat 0. Kekurangan maupun kelebihan dihitung proporsional,
tanpa pembulatan per blok 100 m. Komponen diterapkan **sekali di akhir episode**,
pada sukses, over_distance, batas langkah atau buntu, termasuk buntu awal.
Langkah nonterminal 0; tidak menghukum kekurangan jarak pada setiap langkah.
Pada buntu setelah bergerak, komponen masuk StopPenalty sekali sebelum Bellman.
Terminal tidak bootstrap; bonus sukses dan penalti gagal lama tetap berlaku.
Episode buntu pada 1.000 m, misalnya, mendapat tambahan −200 dari komponen ini.

Nilai `0` atau field yang dihilangkan menonaktifkannya, tanpa mengubah hasil
tersimpan. RewardConfig default 0 menjaga metadata lama. Untuk kebijakan hasil
belajar dengan nilai berbeda, training harus dimulai lagi dari Q-table kosong;
perubahan YAML saja tidak menulis ulang Q atau evaluasi lama.

Sumber: `internal/qlearning/{reward.go, environment.go, agent.go}`,
`internal/analysis/training_csv.go`, dan `cmd/cli/train.go`. Trace mencatat
`reward_distance_error`; popup rute menampilkan Distance error penalty.
Metadata merekam rumus, aplikasi, zero_disables dan
`reward_scheme=configurable_signed_unclipped_distance_error_v2` saat aktif.

### Hasil terbaru: batch 9 November 22.18 WIB

Seluruh 12 profil konsisten pada snapshot/start/reward/environment/seed/akses.
Evaluasi akhir 22/60 valid, terdiri dari A 2/20, B 15/20, C 5/20:

| Konfigurasi | A, dari 5 | B, dari 5 | C, dari 5 |
|---|---:|---:|---:|
| Dinamis 150k | 0 | 0 | 0 |
| Dinamis 300k | 1 | 5 | 1 |
| Horizon 100k, total 150k | 0 | 5 | 2 |
| Horizon 100k, total 300k | 1 | 5 | 2 |

Gagal 31 over_distance dan 7 buntu. Dari 22 loop, 18 berada dalam 4.500–5.500 m;
ini pengelompokan jarak hasil toleransi 20%, bukan eksperimen toleransi 10%.
B horizon 300k 5/5, galat rata-rata 161,29 m, mean_comfort 0,9093 dan overlap 0,71%
pada 5 loop; lima seed tersebut menghasilkan 4 urutan edge unik. Lima keberhasilan
belum membuktikan optimalitas, stabilitas umum atau kelayakan lapangan.

Checkpoint 21.50 tanpa penalti jarak tercatat 23/60 (A 3/B 16/C 4),13 loop dalam
rentang 4.500–5.500 m. Setelah −5:22/60 dan 18 loop pada rentang tersebut. B horizon 300k
naik 4/5→5/5, tetapi B dinamis 150k turun 4/5→0/5. Efeknya campuran; rerata galat
subset berhasil perlu menyebut n dan tidak membuktikan perbaikan menyeluruh.
Angka pembanding berasal dari audit checkpoint sesi sumber dan README Go;
sinkronisasi ini tidak melatih ulang atau mengulang seluruh audit history/Q.

Testing terakhir 22.21 WIB memakai titik `-7.281885, 112.711476`, start 311431485,
snapshot/seed acak berbeda. Dua profil B 300k menghasilkan 6/10 valid: dinamis 1/5,
horizon 5/5; total 3.000.000 episode. Jangan menggabungkannya dengan 60 run training
atau mengaitkan selisih dari checkpoint testing lama hanya pada penalti jarak.

### Kesiapan artefak dan pembahasan naskah

- `analysis.json` training masih 9 November 16.58 WIB, highway.other −1/missing −0,5;
  config terbaru −10/−2. CSV/peta analisis tersebut belum mencerminkan scoring baru.
- `analysis/training/last_window_summary.csv` masih 21.03 WIB dan hanya B/C;
  bukan ringkasan batch 22.18 yang memuat A/B/C.
- `analysis/final-experiment-audit.json` masih 7 November. Audit lama tidak boleh
  digunakan sebagai bukti batch baru atau diklaim mencakup penalti jarak.
- Perbarui analyze dan notebook analisis **dari snapshot/hasil tersimpan** sebelum
  mengutip tabel/grafik; tidak memerlukan training ulang. Sinkronisasi Markdown
  ini tidak menjalankan keduanya atau mengubah artefak penelitian.
- Draf TA masih memerlukan penyelarasan terhadap Go/Haversine/graf mentah,
  25 bin, 20%, 500 langkah dan reward baru, seperti hasil tinjauan pada sesi sumber.
  Naskah Word tidak diedit. Fokus Bab IV hasil/pembahasan; verifikasi/validasi
  tetap ditunda sampai pengguna meminta.
- Bandingkan A/B/C pada konfigurasi yang sama, bedakan history eksploratif dan
  evaluasi greedy, serta nyatakan n untuk rerata rute berhasil. Episode sama
  belum berarti jumlah langkah/pengalaman sama. Tidak ada keputusan menambah
  episode khusus C, mengganti reward otomatis atau memasukkan Dijkstra.

Rincian berikut menyimpan checkpoint historis; tidak menggantikan config dan
hasil terbaru di atas.

### Riwayat checkpoint 7 November dan audit awal 9 November

Checkpoint historis7 November:12 profil/60 training/13.500.000 episode. Greedy31/60 valid.

| Konfigurasi | A, dari5 | B, dari5 | C, dari5 |
|---|---:|---:|---:|
| Dinamis150k | 0 | 5 | 0 |
| Dinamis300k | 1 | 5 | 3 |
| Horizon100k, total150k | 0 | 3 | 4 |
| Horizon100k, total300k | 0 | 5 | 5 |

B dinamis150k kandidat awal katalog berdasarkan eksperimen ini:5/5 loop,
galat rata-rata208,41m dan overlap2,23%. Kelayakan lapangan belum dibuktikan.
Seluruh29 evaluasi gagal tanpa closing action legal:25 over_distance dan4 buntu.
Tidak ada step_limit; maksimum langkah training pada audit tersimpan353.

Episode sama membandingkan hasil pada jumlah percobaan yang ditetapkan, bukan
kemampuan maksimum atau jumlah pengalaman yang pasti sama. Panjang episode
berbeda; total langkah history dapat menjadi pelengkap analisis tanpa training
baru. State lebih kaya dapat membutuhkan lebih banyak pengalaman, tetapi tidak
ada keputusan menambah episode khusus C. Pengaruh horizon tidak seragam antarstate.
Pisahkan keberhasilan episode training yang masih bereksplorasi dari evaluasi
akhir greedy. Lima seed/satu start tidak membuktikan optimalitas atau generalisasi.
Skor ruas adalah preferensi penelitian, bukan ukuran keamanan aktual.

### Riwayat temuan akses node sebelum filter endpoint

Pada versi ketika audit awal dilakukan, `internal/qlearning/action.go` hanya
menyaring `edge.Access`; tag node belum diperiksa.
`internal/osm/graph.go` menyalin atribut way ke edge dan mempertahankan tag node
pada graf. Artinya ruas yang diizinkan dapat tetap melewati node gerbang dengan
akses terlarang dalam snapshot.

Pemeriksaan silang31 rute valid dengan `osm.json` pada9 November menemukan:
semua31 rute melewati setidaknya satu node `access=no`; total19 node berbeda,
berupa gate/sliding_gate/swing_gate, tanpa tag foot eksplisit pada node tersebut.
Contoh B dinamis150k seed0, step3 menuju node9645488764: ruas residential,
access=permissive, tetapi node tujuan barrier=gate/access=no. Koordinat node
−7,2815751/112,708849. Node ini muncul pada20 rute valid.

Ini bukti keterbatasan pemodelan akses saat ini, bukan bukti gerbang pasti tertutup
sekarang atau penetapan status hukum lokasi. Jangan menyamakan keberhasilan loop
pada graf dengan kelayakan lapangan. Usulan: bahas pembatasan eksplisit akses node
terlebih dahulu; jangan melarang semua barrier tanpa membedakan jenis dan akses.
Saat audit pagi tersebut belum ada perubahan mask/reward atau training ulang.
Filter way dan kedua endpoint kemudian diterapkan pada9 November; hasil terbaru
di atas sudah memakai `edge_and_endpoint_whitelist_v1`.
Jika kebijakan diubah nanti, pertahankan hasil lama sebagai baseline dan hasil
baru sebagai eksperimen terpisah, jangan mengedit metadata hasil lama.
Rujukan tag: https://wiki.openstreetmap.org/wiki/Key:access dan
https://wiki.openstreetmap.org/wiki/Key:barrier.

Pengujian9 November: `go test -count=1 ./...` seluruh paket lulus setelah dijalankan
dengan izin server HTTP localhost; percobaan sandbox awal terhambat bind port,
bukan kegagalan logika. `go vet ./...` dan `go build -buildvcs=false ./...` lulus.
Tidak mengubah kode Go, konfigurasi, snapshot, hasil training, atau naskah TA.

## Riwayat implementasi Python — hingga 4 November 2026

Bagian berikut dipertahankan sebagai arsip. Parameter dan hasilnya tidak menjadi
acuan implementasi Go atau angka naskah terbaru.

## 1. Tujuan dan Status Implementasi

Sistem membentuk rute lari **loop 5.000 m** menggunakan Q-Learning tabular pada graf jalan OpenStreetMap. Rute hanya valid jika agen:

1. kembali ke **node start**; dan
2. total jaraknya berada pada **4.500–5.500 m**.

Kedua syarat tersebut direpresentasikan oleh **is_loop=True**. Node yang berulang tidak membatalkan loop, tetapi dinilai terpisah melalui metrik revisit dan pengulangan edge.

Tujuan agen bukan hanya mencapai jarak. Agen juga diarahkan memilih edge dengan **comfort score** lebih tinggi, yaitu proxy spasial dari atribut OSM: highway, surface, dan width. Comfort score bukan survei persepsi pelari dan bukan skor keamanan aktual; nama legacy ini kini menyimpan preferensi bertanda tanpa pembatasan rentang.

Status hasil yang tersimpan sekarang:

- **Hasil aktif per 3 November 2026:** `reward_revisit_10_overlap_count_20261103`
  lengkap A--C,60 training/6.750.000 episode,25/60 greedy valid. Seluruh60
  direproduksi; lihat `docs/temp/analisis_ABC_revisit10_20261103/ANALISIS.md`.
- `reward_direct_20261103` adalah arsip sebelumnya (bagian8.2.3).
- `surface_width_3m_20261102` adalah arsip reward lama (bagian 8.2.2).
- Ringkasan/angka 29 Oktober di bawah adalah riwayat baseline, bukan hasil aktif.

- Scenario state A, B, dan C adalah eksperimen final. Ketiganya memakai action, reward, action mask, dan aturan revisit yang sama; hanya representasi state yang berbeda.
- Hasil evaluasi terbaru harus selalu dibaca dari CSV setelah notebook dijalankan ulang. Evaluasi yang dipakai untuk pelaporan adalah evaluasi greedy, bukan episode training yang masih mengandung eksplorasi.
- Pada eksperimen epsilon dinamis awal, State C sempat menjadi kandidat utama karena menambahkan konteks arah kedatangan melalui `previous_node`. Namun, hasil epsilon decay tetap menunjukkan State B juga dapat membentuk loop secara konsisten; perbandingan final harus memakai hasil A--C dengan konfigurasi epsilon tetap yang sama.
- Terminasi paling sering masih `no_available_action` dan `over_distance`; hasil perlu dibaca bersama closing action available rate.
- Per 29 Oktober 2026, pengguna telah menyelesaikan empat konfigurasi: dinamis 75k/150k dan horizon epsilon 50k pada training 75k/150k, untuk A--C dan lima seed (60 training). Analisis baseline ada pada bagian 8.2.1 dan `docs/temp/analisis_empat_konfigurasi_20261029/ANALISIS.md`. Hasil lama tetap sebagai arsip; agent hanya membaca history dan mengulang evaluasi dari Q-table, tanpa training ulang.

### 1.1 Reward langsung aktif 3 November 2026

Seluruh kesepakatan reward diterapkan ke core dan notebook rute lari: H/S/W
+1/-1/0, satu prioritas highway termasuk tertiary, bobot 0,55/0,30/0,15, tanpa
pengurangan 0,50. Akses permissive -0,10 per 100 m; arah 0,60 kedua fase;
revisit -10; sukses +100; tiga kegagalan -50. Fase/mask/state/epsilon/seed/Q tetap.

Grup aktif reward_revisit_10_overlap_count_20261103 lengkap A--C:60 training,
25/60 evaluasi valid dan seluruh60 direproduksi. Pengguna
meminta penalti -10 menggantikan -5 dan MAX_WORKERS=3 pada A--C. Grup -5 tetap
arsip lengkap B/C (35/40 greedy valid). Komponen reward lain/Q/mask/state/epsilon
serta implementasi paralel tetap. Verifikasi 32 cell lulus dengan expected
literal -10 dan total -8,40. Uji Jupyter tiga worker/lima seed menghasilkan
Q/history/metrik/rute identik dengan mode berurutan pada kasus sintetis.

### 1.2 Pencatatan overlap aktif

Grup aktif reward_revisit_10_overlap_count_20261103 lengkap A--C; audit terbaru
ada di bagian akhir dokumen.
Grup -5 lengkap B/C tetap pembanding; angka audit di bagian akhir adalah riwayat
-5. Definisi overlap, kolom tiap episode/evaluasi dan grafik tidak berubah.

## 2. Struktur Proyek dan Urutan Eksekusi

| Berkas/direktori | Peran | Catatan |
|---|---|---|
| **rute_lari_core.py** | Core tunggal: konfigurasi, download/load OSM, comfort, action, state, environment, Q-Learning, metrik, grafik, dan peta. | Jangan menduplikasi aturan per scenario. |
| **analisa.ipynb** | Memakai download/load OSM dari core, lalu menganalisis data dan membuat peta graf. | Jalankan lebih dahulu. |
| **scenario_A.ipynb** | Training dan evaluasi state A. | Memanggil core bersama. |
| **scenario_B.ipynb** | Training dan evaluasi state B. | Memanggil core bersama. |
| **scenario_C.ipynb** | Training dan evaluasi state C. | Memanggil core bersama. |
| **verifikasi.ipynb** | Verifikasi poin 1–5 melalui core bersama. | Contoh manual, kasus terkontrol, dan snapshot OSM; Python 3.13. |
| **uji_titik_start.ipynb** | Unduh graf baru sekitar koordinat dan jalankan tiga seed acak. | Default B 150k horizon 50k; graf, seed, dan hasil tersimpan terpisah. |
| **training.ipynb** | Notebook gabungan versi lama. | Jangan gunakan untuk eksperimen baru. |
| **data_osm_5km/graf_jalan_kaki_5km.graphml** | Snapshot graf jalan terproyeksi. | Input utama training. |
| **data_osm_5km/** | Menyimpan GraphML serta peta analisis highway dan comfort. | Artefak analisis. |
| **hasil_bab_4/training_qlearning_5km/** | CSV training/evaluasi, grafik, peta scenario, dan summary. | Artefak eksperimen. |
| **IMPLEMENTASI.md** | Wiki keputusan teknis ini. | Perbarui bila desain berubah. |

Urutan kerja yang benar:

1. Buka proyek dari direktori root agar path relatif berfungsi.
2. Jalankan **analisa.ipynb** dari atas sampai GraphML berhasil disimpan.
3. Buka salah satu **scenario_A.ipynb** sampai **scenario_C.ipynb**. Notebook memuat GraphML dengan fungsi core yang sama; jika GraphML belum ada, fungsi yang sama mengunduh data OSM.
4. Jalankan Scenario A, B, lalu C. Setiap scenario menjalankan lima seed, menampilkan tabel evaluasi greedy per seed, tiga berkas grafik (training utama, diagnosis, overlap), serta peta interaktif. Termination rate berada di dalam grafik diagnosis. Data hasil juga disimpan dalam CSV.
5. Jalankan perbandingan akhir A–C.
6. Gunakan CSV hasil sebagai sumber angka untuk BAB IV dan BAB V.

Notebook scenario dapat membuat GraphML bila belum ada, tetapi analisis tetap sebaiknya dijalankan lebih dahulu untuk memeriksa data dan peta.

### 2.1 Pemisahan cell training dan tampilan hasil

Pesan pada cell pemuatan graf hanya menampilkan jumlah seed. Nilai default `EPISODES=10.000` dipakai untuk uji cepat di core dan tidak ditampilkan lagi karena seluruh eksperimen notebook mengirim jumlah episode secara eksplisit.

Setiap konfigurasi eksperimen pada `scenario_A.ipynb`, `scenario_B.ipynb`, dan `scenario_C.ipynb` sekarang memiliki dua cell berurutan:

1. **Cell training** memanggil `run_scenario_experiment(..., display_results=False)`. Cell ini menjalankan lima seed, melakukan evaluasi greedy, lalu menyimpan artefak; tabel, grafik, dan peta tidak ditampilkan agar output training tidak berat.
2. **Cell tampilkan hasil tersimpan** memanggil `display_saved_experiment_results(...)`. Cell ini **tidak melakukan training**. Cell hanya membaca berkas hasil, lalu menampilkan metrik per seed, diagnosis, termination rate, tiga grafik PNG pada section terpisah, dan peta HTML interaktif.

Pemisahan ini memungkinkan pengguna memuat ulang peta yang gagal tampil, melihat lagi tabel, atau membuat screenshot grafik tanpa menjalankan ulang training yang memakan waktu. Cell ringkasan sensitivitas juga memakai `summarize_saved_experiments(...)`, sehingga membaca CSV yang tersimpan dan tidak lagi bergantung pada variabel `result_*` yang hanya ada di RAM kernel.

Untuk setiap eksperimen baru, folder `hasil_bab_4/training_qlearning_5km/<result_subdir>/` menyimpan:

| Artefak | Isi dan kegunaan |
|---|---|
| `training_history_<scenario>.csv` | Metrik setiap episode untuk lima seed, termasuk reward, epsilon, TD-error, jarak, comfort, dan alasan terminasi. |
| `evaluation_metrics_<scenario>.csv` | Metrik evaluasi greedy per seed yang dipakai sebagai hasil utama. |
| `diagnosis_metrics_<scenario>.csv` dan `termination_rates_*.csv` | Ringkasan diagnosis dan termination rate training maupun evaluasi greedy. |
| `grafik_training_<scenario>.png`, `grafik_diagnosis_<scenario>.png`, `grafik_overlap_<scenario>.png` | Tiga bagian grafik; overlap terpisah. |
| `peta_interaktif_scenario_<scenario>.html` | Peta Folium untuk rute representatif. |
| `qtable_scenario_<scenario>_seed_<seed>.pkl` | Q-table tabular hasil training untuk setiap seed. |
| `rute_evaluasi_scenario_<scenario>_seed_<seed>.json` | Urutan node dan action hasil evaluasi greedy untuk setiap seed. Setiap action menyimpan `from_node`, `next_node`, dan `key` agar edge MultiDiGraph dapat dikenali kembali. |
| `metadata_eksperimen_<scenario>.json` | Konfigurasi episode, epsilon decay, seed, seed yang dipilih untuk peta, dan daftar artefak. |

Artefak Q-table, rute JSON, dan metadata dibuat oleh implementasi terbaru. Folder hasil lama yang dibuat sebelum perubahan ini tetap dapat ditampilkan selama CSV, PNG, dan HTML-nya tersedia; namun Q-table tidak dapat dipulihkan dari folder lama tanpa menjalankan ulang training tersebut.

Pada tampilan hasil tersimpan, bagian **Ringkasan Diagnosis Evaluasi: Agregat Lima Seed** memang hanya memiliki satu baris. Baris tersebut bukan hasil satu seed, melainkan ringkasan lima evaluasi greedy: rata-rata `distance_to_start_at_end_m`, rata-rata `return_progress_ratio`, proporsi `closing_action_available`, dan rata-rata jumlah state Q-table. Nilai per seed tetap tersedia pada tabel **Metrik Evaluasi Greedy per Seed** tepat di atasnya.

Sebelum peta ditampilkan, cell juga mencetak seed yang dipakai serta alasan pemilihannya. Informasi ini diambil dari `metadata_eksperimen_<scenario>.json` apabila tersedia. Untuk folder hasil lama tanpa metadata, seed dihitung ulang dari `evaluation_metrics_<scenario>.csv` memakai aturan pemilihan peta yang sama.

Fungsi `display_saved_experiment_results(...)` khusus untuk tampilan dan sengaja tidak mengembalikan nilai, sehingga notebook tidak mencetak dictionary besar setelah peta. Jika data CSV perlu diolah pada cell lain, gunakan `load_saved_experiment_results(...)`. Peta Folium ditampilkan dengan memasukkan HTML tersimpan ke `iframe.srcdoc` melalui JavaScript Jupyter. Cara ini tidak bergantung pada alamat `file://` maupun endpoint `/files/`, yang dapat diblokir atau memakai root berbeda pada JupyterLab desktop.

### 2.2 Training seed paralel

`run_scenario_experiment(..., max_workers=1)` tetap berurutan untuk kompatibilitas.
Notebook A--C memakai `MAX_WORKERS=3` di cell muat graf, kemudian meneruskan
`max_workers=MAX_WORKERS` pada empat cell training. Nilai 1 berurutan; nilai >1
memakai multiprocessing Pool dengan start method spawn yang sesuai macOS/Jupyter.
Jumlah proses efektif dibatasi jumlah seed dan CPU. Tidak ada dependensi baru.

Setiap task memanggil train_q_learning lalu evaluate_greedy yang sama. Setiap seed
memiliki RNG, environment dan Q-table sendiri; episode/langkah di dalam seed tetap
berurutan. Snapshot parameter training/reward dari induk dipasang ke proses spawn.
Graf dibangun induk dan data action/koordinat dikirim ke worker, tanpa unduh baru.
Proses induk menerima seed sesuai urutan selesai dan menyimpan Q/rute JSON-nya.
CSV, grafik, peta dan metadata digabung setelah semua seed selesai. Hasil akhir
history/evaluasi/trials diurutkan kembali menurut seeds masukan. Referensi graf
environment yang diterima disamakan ke data induk agar tidak menahan salinan
seluruh graf per trial. Workers tidak menulis ke folder eksperimen.

Cell Jupyter tetap menunggu seluruh seed selesai; percepatan berasal dari beberapa
seed berjalan bersamaan. Tambahan proses memerlukan RAM dan biaya mulai/transfer
data; jangan mengklaim 2 proses pasti 2 kali lebih cepat. Konfigurasi terbaru 3 worker sesuai permintaan pengguna; jalankan satu
konfigurasi training dulu. Uji titik kini tiga seed acak dengan MAX_WORKERS=3,
tanpa mengubah SEEDS global. Menambah worker tidak mempercepat satu seed.

Metadata execution menyimpan mode, max_workers_requested, workers, start_method,
dan result_order=input_seed_order. Jika terjadi error/interupsi, Pool context
menghentikan workers; Q/rute seed yang sudah selesai mungkin tersimpan, tetapi
ringkasan lengkap baru tersedia setelah seluruh seed selesai. Ini bukan fitur
resume: menjalankan ulang cell memulai seed dari Q-table kosong.

Uji 3 November: 18 kombinasi A/B/C, seed dan epsilon cocok dengan core sebelum
paralelisasi setelah penalti disamakan -5; dua jadwal B menghasilkan Q/history/
metrik/rute identik berurutan vs 2 proses, termasuk seeds tidak berurutan. Snapshot
parameter runtime, error worker, validasi jumlah worker dan seluruh state diuji.
Graf OSM nyata diuji 35 episode per seed (dua seed), hasil kedua mode identik.
Kernel Jupyter bersih berhasil memanggil 2 proses setelah reload modul. Verifikasi
32 cell lulus. Ini uji implementasi, bukan training penelitian atau benchmark.
Audit: docs/temp/verifikasi_revisit5_paralel_20261103/.

## 3. Konfigurasi Bersama

| Parameter | Nilai | Makna |
|---|---:|---|
| START_LAT | -7.282187 | Latitude titik start input pengguna. |
| START_LON | 112.709282 | Longitude titik start input pengguna. |
| TARGET_DISTANCE_M | 5.000 m | Target panjang rute loop. |
| DISTANCE_TOLERANCE | 10% | Toleransi target. |
| MIN_DISTANCE_M | 4.500 m | Batas minimum loop valid. |
| MAX_DISTANCE_M | 5.500 m | Batas maksimum loop valid. |
| DOWNLOAD_RADIUS_M | 3.025 m | Setengah lebar bbox unduhan OSM dari start. |

Dasar area unduhan:

- 5.000 m × 1,10 = 5.500 m sebagai batas rute maksimum.
- 5.500 m ÷ 2 = 2.750 m sebagai jarak jalur teoritis terjauh pada loop.
- 2.750 m × 1,10 = 3.025 m setelah buffer 10%.

Karena OSMnx memakai dist_type bbox, 3.025 m adalah setengah lebar area kotak, bukan radius lingkaran. Buffer 10% adalah keputusan desain eksperimen, bukan rumus standar universal.

## 4. Notebook Analisis Data

### 4.1 Tujuan analisa.ipynb

Notebook analisis membangun input bagi environment. Notebook ini tidak melakukan training. Hasilnya adalah graf terproyeksi, analisis struktur/kualitas data, comfort score per edge, dan peta untuk inspeksi manual.

### 4.2 Pengambilan graf OSM

Konsep pemanggilan OSMnx:

    ox.graph_from_point(
        center_point=(START_LAT, START_LON),
        dist=DOWNLOAD_RADIUS_M,
        dist_type="bbox",
        network_type="walk",
        simplify=True,
        retain_all=False,
        truncate_by_edge=True,
    )

Keputusan parameter:

- **network_type walk**: memilih jaringan yang dapat dilalui pejalan kaki/pelari. Parameter ini bukan jaminan kenyamanan atau keamanan.
- **simplify True**: node yang hanya membentuk bentuk geometri jalan dikurangi; simpang, ujung jalan, dan titik keputusan dipertahankan. Hal ini mengurangi state yang tidak bermakna.
- **retain_all False**: memakai komponen weakly connected terbesar dan membuang pulau jaringan kecil.
- **truncate_by_edge True**: membantu mencegah jalan buntu palsu pada tepi bbox.

Sebelum unduhan final, surface ditambahkan ke daftar useful tags way OSMnx. Jika kolom surface belum ada, itu berarti tag belum disimpan oleh konfigurasi OSMnx, bukan berarti OSM tidak memiliki data surface.

### 4.3 Proyeksi koordinat

Graf awal berada pada WGS84, EPSG:4326: x adalah longitude dan y adalah latitude dalam derajat. Setelah itu graf diproyeksikan dengan **ox.project_graph** menjadi CRS lokal EPSG:32749. Pada graf terproyeksi, x dan y memakai meter.

Proyeksi wajib karena environment menghitung jarak lurus memakai **np.hypot(x - x0, y - y0)**. Perhitungan Pythagoras tersebut hanya layak sebagai meter jika koordinat sudah terproyeksi. Untuk peta Folium, koordinat meter ditransformasikan kembali ke WGS84.

Alurnya:

    WGS84 longitude-latitude
        -> project_graph
        -> x-y meter untuk graf dan RL
        -> transform WGS84 untuk Folium

### 4.4 Struktur MultiDiGraph

Graf adalah networkx MultiDiGraph:

- **node**: simpang, ujung ruas, atau titik keputusan; ID-nya adalah ID node OSM.
- **edge u -> v**: perpindahan terarah dari node u ke node v.
- **key**: pembeda edge paralel apabila u dan v sama.
- **osmid**: ID OSM Way atau ruas jalan sumber; bukan ID node.
- atribut edge penting: length, geometry, highway, surface, width, dan oneway.

Secara sederhana, **node** adalah titik pada jaringan jalan, sedangkan **edge** adalah satu ruas/jalur yang menghubungkan dua node. Contohnya, bila agen berada pada node A dan terdapat ruas jalan sepanjang 120 m menuju node B, maka perpindahan `A -> B` melalui ruas tersebut adalah satu edge. Node biasanya mewakili simpang, ujung ruas, atau titik keputusan; edge menyimpan karakter ruas yang benar-benar dilalui, seperti panjang, klasifikasi jalan, permukaan, lebar, dan `comfort_score`.

Pada Q-Learning proyek ini, ketika agen memilih action, agen sebenarnya memilih **satu edge** untuk bergerak dari node saat ini ke node tujuan. Karena graf bertipe MultiDiGraph, dua node yang sama dapat dihubungkan oleh lebih dari satu edge. Oleh sebab itu action tidak cukup ditulis sebagai node tujuan saja, melainkan sebagai pasangan `(next_node, key)`. Nilai `key` membedakan edge paralel yang memiliki asal `u` dan tujuan `v` sama, tetapi dapat mewakili ruas atau atribut yang berbeda.

    Node A -- edge: panjang 120 m, comfort 0,75 --> Node B

Pada contoh tersebut, `Node A` adalah posisi agen sebelum bergerak, edge adalah ruas jalan yang dipilih, dan `Node B` menjadi posisi agen setelah action dijalankan. Reward comfort dan total jarak diperoleh dari atribut edge yang dipilih, bukan dari node tujuan saja.

Snapshot graf yang dipakai saat ini:

| Metrik | Nilai |
|---|---:|
| Jumlah node | 8.027 |
| Jumlah edge directed | 21.374 |
| CRS | EPSG:32749 |
| Weakly connected components | 1 |
| Total panjang edge directed | 1.353.832,10 m |
| Panjang edge rata-rata | 63,34 m |
| Panjang edge median | 46,19 m |
| Tujuan node unik dari start | 3 |

Total panjang edge directed bukan total jalan fisik unik karena arah dua arah dapat tercatat lebih dari sekali.

### 4.5 Analisis yang dipertahankan

Analisis wajib mencakup sampel node/edge; ringkasan struktur; konektivitas; panjang edge; node start; kelengkapan highway, surface, width, smoothness, dan access; distribusi lima atribut; indikator jumlah tujuan node; kombinasi kelengkapan lima atribut analisis; distribusi comfort score; serta peta interaktif.

Kualitas atribut snapshot sekarang:

| Atribut | Ketersediaan edge |
|---|---:|
| highway | 100,00% |
| surface | 67,59% |
| width mentah | 66,77% |
| width valid dalam meter | 66,18% |
| smoothness pada salinan analisis (cache seluruh way asal) | 65,21% |
| access pada GraphML | 3,03% |

Edge dengan data kosong tidak dibuang karena bisa memutus graf. Komponen comfort yang tidak tersedia menggunakan nilai netral.

### 4.6 Integrasi smoothness dan access ke analisis atribut

Klarifikasi akhir pengguna 29 Oktober 2026: kedua atribut harus masuk pada
seluruh elemen analisis atribut yang relevan. Notebook tetap 43 cell, dengan
perubahan pada bagian yang sudah ada; tidak menambahkan eksplorasi tag lain.

Alur data terpadu:

1. Sesudah graf dimuat, `edges_gdf` menjadi salinan analisis. Jika smoothness
   belum ada, cache yang dipilih oleh `SMOOTHNESS_CACHE_PATH` dicocokkan melalui
   osmid setiap edge. Tidak ada unduhan atau penulisan ulang GraphML.
2. Smoothness dimasukkan sebagai nilai edge hanya jika seluruh way asal ditemukan
   dan bertag. Gabungan kategori dipertahankan sebagai list, bukan memilih nilai
   terbaik. `smoothness_status` dan `smoothness_nilai_asal` menyimpan cakupan/
   informasi parsial. Data parsial tidak dihitung sebagai atribut lengkap.
3. `edges_table` dibuat dari tabel analisis ini tanpa memuat ulang dari G, sehingga
   lima atribut tetap konsisten di semua bagian berikutnya.

Bagian yang diperbarui:

- Sampel/daftar kolom edge dengan sumber dan cakupan smoothness.
- Tabel dan diagram kelengkapan highway/surface/width/smoothness/access;
  tabel membedakan kolom graf asli dan sumber data pada salinan analisis.
- Distribusi smoothness/access per edge berdasarkan jumlah dan panjang, sama
  seperti highway/surface. Tabel smoothness juga menampilkan cakupan dan nilai
  tidak dikenal. Access--foot diperiksa pada way asal yang sama.
- Diagram distribusi menjadi enam panel: highway, surface, kualitas width,
  width valid, smoothness, dan access. Panel width valid tetap memakai subset
  width valid; empat distribusi kategori memakai seluruh panjang edge.
- Kombinasi ketersediaan memakai lima atribut; width tetap mensyaratkan parsing
  meter valid. Ketersediaan tag tidak identik dengan validitas atau izin akses.
- Tooltip peta highway/comfort serta contoh tabel comfort memuat smoothness/
  access sebagai informasi tambahan. Warna/rumus comfort tetap tiga komponen lama.

Sumber cache cocok dengan 6.554 way asal unik. Dari 21.374 edge, smoothness
terisi penuh pada 13.938 (65,21%), parsial pada 216, dan tidak terisi pada 7.220.
Access terisi pada 648 edge (3,03%). Seluruh statistik utama memakai edge
directed; jangan mencampurkan denominator way sumber dari analisis sebelumnya.

Seluruh 21 cell kode berisi dieksekusi pada kernel Python 3.13 dan output disimpan.
Pemeriksaan mencakup konsistensi lima atribut, konservasi jumlah/panjang/
persentase pada distribusi dan kombinasi, pemisahan data parsial, tooltip peta,
cache tidak tersedia, serta kesamaan comfort score terhadap core.
Core, GraphML, notebook scenario/verifikasi, dan hasil training tidak diubah.
Analisis HTML/PNG yang memang dihasilkan notebook diperbarui oleh Run All.

### 4.7 Peta interaktif atribut jalan dan akses

Per 30 Oktober 2026, cell peta analisa.ipynb bernama **Peta Interaktif Atribut
Jalan dan Akses**, dengan tampilan berikut:

- Default hanya warna ruas **Highway (jenis jalan)** dan marker START.
- Pilihan **Surface (permukaan jalan)** dan **Smoothness** mengganti warna ruas bergantian;
  Highway, Surface, dan Smoothness menjadi FeatureGroup `overlay=False` pada
  kontrol radio. Tile basemap terpisah dengan `control=False`, sehingga tetap
  terlihat pada ketiga tampilan. Surface ditambahkan pada 2 November 2026.
- Kategori smoothness meliputi kategori tag yang dikenal, gabungan, tidak dikenal,
  kosong, data parsial, serta sumber belum lengkap. Nilai asli dan cakupan tetap
  ada di tooltip. Ini kategori peta, bukan skor/reward baru.
- Surface menampilkan warna material asli (asphalt/paving_stones/concrete dan
  lainnya), gabungan, tidak dikenal, serta kosong. Tooltip menampilkan nilai
  asli dan calculate_surface_score() dari core; warna bukan skor keselamatan.
- Marker access per jenis tersedia sebagai overlay yang awalnya tidak aktif.
  Legenda highway/surface/smoothness mengikuti pilihan warna ruas; legenda access muncul
  jika minimal satu layer marker diaktifkan. Pengaturan memakai event Leaflet.

Kategori marker no merah, destination oranye, permissive biru, yes hijau,
private merah gelap; nilai lain/gabungan ungu. Marker dihitung di tengah geometri
pada CRS meter kemudian diubah ke WGS84. Pasangan edge dua arah dengan node,
key, geometri ternormalisasi, osmid dan access identik berbagi marker; seluruh
identitas edge dicantumkan di popup. Key paralel berbeda tidak digabung.
Marker bukan koordinat pintu/pagar atau keputusan izin pejalan kaki.

Snapshot menghasilkan 324 marker untuk 648 edge: no 12/24, destination 25/50,
permissive 195/390, yes 92/184 (marker/edge). HTML tetap tersimpan pada
`data_osm_5km/peta_graf_highway.html`; output cell notebook juga diperbarui.
Pemeriksaan meliputi default layer, kategori/cakupan, urutan JavaScript dan
pergantian legenda. Uji interaksi Chrome memeriksa radio tema, overlay access,
legenda, dan kembali ke Highway tanpa error JavaScript; tampilan diperiksa visual.

Pengguna membatasi pengembangan berikutnya pada access agar sederhana.
Pengamatan pengguna: sekitar lokasi start banyak ruas permissive.

### 4.8 Whitelist akses aktif (2 November 2026)

Blacklist sepuluh nilai yang dibuat 30 Oktober diganti daftar izin singkat:

    ACCESS_WHITELIST = frozenset({"yes", "permissive"})

| Kondisi access | Perlakuan |
|---|---|
| yes | Dibentuk menjadi action; reward akses nol |
| permissive | Dibentuk menjadi action; penalti -0,10 per 100 m |
| Kosong/tidak tersedia | Tetap dibentuk menjadi action; reward akses nol |
| Nilai terisi lainnya, termasuk tidak dikenal | Tidak dibentuk menjadi action |
| Gabungan/list/string list/titik koma | Semua nilai terisi harus masuk whitelist |

build_actions() memakai access_values.issubset(ACCESS_WHITELIST). Himpunan kosong
lolos untuk mempertahankan ruas tanpa tag. Satu komponen non-whitelist cukup
menolak seluruh edge, termasuk closing ke start. Edge paralel lain tetap tersedia.
Huruf besar/kecil dan spasi dinormalisasi oleh osm_values(). Foot=yes tidak
mengganti kebijakan access. Atribut conditional terpisah dan hierarki izin lengkap
OSM belum ditafsirkan; tag kosong bukan bukti izin publik atau keterlintasan aktual.

Penalti permissive tidak berubah dan tetap berlaku pada seluruh panjang edge
jika gabungan memuat permissive. Skor H/S/W, Q-update, state, epsilon dan seed
juga tetap. Filter ini digunakan bersama untuk A--C dan notebook uji titik.

Pada snapshot penelitian ada tag kosong/yes/permissive/destination/no; whitelist
baru menghasilkan 21.300 action identik dengan blacklist sebelumnya. Graf uji
terbaru menghasilkan 22.058 action identik. Tidak ada perubahan notebook A--C,
RESULT_GROUP, file graf atau hasil training. Metadata hasil lama tidak ditulis
ulang: blacklist merupakan kebijakan pada saat training tersebut. Jika graf baru
memuat unknown/variable/nilai lain, whitelist lebih ketat; kesetaraan tidak
berlaku otomatis untuk semua lokasi atau pembaruan OSM.

Metadata run berikutnya mencatat access_whitelist_applied, access_whitelist_values,
access_missing_allowed=True dan access_whitelist_policy=
all_values_whitelisted_no_foot_override. Field blacklist tidak lagi ditulis pada
run baru. Loader tampilan tetap dapat membaca metadata hasil lama.

### 4.9 Koreksi skor highway service (2 November 2026)

Pengguna mengklarifikasi bahwa service hanya dikeluarkan dari HIGHWAY_PRIORITY_2,
bukan dari daftar action. Service mengikuti HIGHWAY_OTHER_SCORE=0,20; gabungan
memakai minimum seperti sebelumnya. Prioritas kedua tersisa path, unclassified,
tertiary dan tertiary_link, seluruhnya 0,60. Tidak ada filter highway tambahan.
Build_actions, whitelist access, mask, Q, state, epsilon dan seed kembali persis
seperti sebelum salah tafsir. Ruas service tetap bisa dilalui/menutup loop jika
lolos aturan access, jarak dan kunjungan biasa.

Larangan action service dan perubahan grup/output A--C sebelumnya dibatalkan.
Notebook A--C dikembalikan utuh termasuk hasil tampilannya; hasil tersebut memakai
skor service lama 0,60, bukan hasil reward terbaru. Grup baru tidak dipilih otomatis.
Jika melatih ulang, gunakan grup baru yang sama di A--C untuk menjaga artefak lama.
Uji titik tetap mengikuti core; restart kernel dan ulangi pencarian/peta sebelum
training. Uji titik memakai satu folder terbaru yang selalu ditimpa.
Metadata highway_scoring yang sudah ada otomatis mencatat service di luar prioritas;
tidak ada metadata pengecualian highway baru. Data/graf/hasil lama tetap utuh.

Contoh service/asphalt/width 3 m: H=0,20, S=1,00, W=1,00 menghasilkan C=0,56.
Reward edge per 100 m = +0,06; jika permissive, komponen akses -0,10 sehingga
jumlah kedua komponen -0,04 sebelum komponen arah, revisit atau terminal.
Skor rendah mengurangi preferensi, tidak menjamin ruas tersebut tak dipilih.
Analisis hanya diperbarui keterangannya; output skor lama belum dijalankan ulang.
Notebook verifikasi tetap ditunda dan acuan numeriknya perlu disesuaikan nanti.

## 5. Comfort Score pada Edge

### 5.1 Formula

    B = 0,55*r_H + 0,30*r_S + 0,15*r_W
    R_ruas = B * panjang_meter / 100

Nilai default komponen +1/-1/-0,5; gabungan B disimpan tanpa clipping. Rentang
mengikuti parameter komponen dan bobot. Tidak ada pengurangan titik netral 0,50; nilai kosong dikenai penalti-0,5. Nama atribut comfort_score, highway_score, surface_score,
width_score dan API add_comfort_scores dipertahankan agar notebook/loader tetap
kompatibel, tetapi makna dan rentang angka berubah. Metadata versi baru menandai
reward_scheme=direct_signed_unclipped_missing_05_20261103, comfort_score_range=null dan
comfort_score_clipped=false. Metadata arsip lama tidak diubah.

### 5.2 Kebijakan nilai

| Komponen | +1 | -1 | -0,5 |
|---|---|---|---|
| Highway | footway/pedestrian/living_street/residential/tertiary | Nilai terisi lainnya/tidak dikenal, termasuk service/path/unclassified/tertiary_link | Kosong |
| Surface | asphalt/concrete/paving_stones/paved | Nilai terisi lainnya/tidak dikenal | Kosong |
| Width | Nilai valid >=3 m | Positif <3 m | Kosong/invalid/gabungan |

Highway/surface gabungan minimum; width menerima satu angka positif dalam meter,
koma desimal dikenali. Semua penghitungan terpusat di core, termasuk analisis.
Nilai ini preferensi desain, bukan standar keamanan/kenyamanan. Highway nonprioritas
serta ruas sempit tetap menjadi action bila lolos aturan access/mask.

Bagian 5.3--5.4 di bawah menyimpan riwayat pemetaan, bukan kebijakan aktif.

### 5.3 Riwayat dua prioritas highway (1 November 2026)

Catatan bagian ini merekam pekerjaan 1 November. Contoh W=0,625/C=0,94375
adalah acuan sebelum perubahan width; aturan aktif 2 November ada di 5.2 dan 5.4.

Klarifikasi pengguna: tertiary dan tertiary_link juga masuk Prioritas 2 (0,60),
sebagai alternatif rute lari. Ini preferensi penelitian, bukan jaminan aman.

Variabel keanggotaan HIGHWAY_PRIORITY_1 dan HIGHWAY_PRIORITY_2 dipisahkan dari
HIGHWAY_PRIORITY_1_SCORE=1.00, HIGHWAY_PRIORITY_2_SCORE=0.60,
HIGHWAY_OTHER_SCORE=0.20, dan HIGHWAY_MISSING_SCORE=0.50. Tidak lagi memakai
pemetaan skor per jenis highway yang berbeda-beda. Skor 1 bukan jaminan aman.

calculate_highway_score() membedakan tag kosong dari nilai terisi yang tidak
dikenal. Mendukung list/string list/kapital/spasi/titik koma; gabungan memakai
minimum. Cell highway analisa.ipynb memanggil fungsi core ini, sedangkan helper
surface dan aturan width dipertahankan. Output analisis mulai cell highway
dikosongkan untuk dihitung ulang, tanpa menjalankan ulang peta atau menyimpan
ulang GraphML dalam pekerjaan ini. Atribut skor disusun ulang di memori saat
training memanggil add_comfort_scores(), sehingga snapshot tidak perlu diunduh.

Contoh residential/asphalt/lebar 3 m menghasilkan H=1, S=1, W=0.625, sehingga
C=0.94375. Ruas 100 m memberi reward ruas +0.44375, atau +0.34375 setelah
penalti permissive, sebelum komponen arah/revisit/terminal. Bobot komponen,
penalti akses, blacklist, state, seed, jumlah episode, dan epsilon tidak berubah.

Metadata eksperimen mencatat kelompok, empat skor, dan kebijakan gabungan.
Notebook A--C memakai grup baru highway_dua_prioritas_20261101, terpisah dari
grup sebelumnya reward_access_blacklist_010_20261030. Output lama pada notebook
scenario dikosongkan; artefak hasil lama tetap utuh. Belum ada training baru.
Notebook verifikasi tetap ditunda; acuan numeriknya adalah konfigurasi lama.

### 5.4 Riwayat surface satu prioritas dan width 3 m (2 November 2026)

Surface disederhanakan karena kategori dominan pada snapshot adalah paving_stones,
asphalt, dan concrete. SURFACE_PRIORITY berisi asphalt/concrete/paving_stones/paved;
SURFACE_PRIORITY_SCORE=1.00, SURFACE_OTHER_SCORE=0.20, SURFACE_MISSING_SCORE=0.50.
List/string list/titik koma memakai minimum; nilai terisi tak dikenal bukan netral.

Width tidak lagi memakai normalisasi linear 1–5 m. WIDTH_PRIORITY_MIN_M=3.0,
WIDTH_PRIORITY_SCORE=1.00, WIDTH_OTHER_SCORE=0.20, WIDTH_MISSING_SCORE=0.50.
parse_width_m() tetap menerima satu nilai positif dalam meter, termasuk koma
sebagai desimal pada masukan. List, gabungan titik koma, nol/negatif dan format
invalid diberi skor pengganti. Batas 3 m dipilih pengguna untuk mengurangi
preferensi gang sempit; bukan hasil survei, standar kenyamanan atau larangan aksi.
Lebar badan jalan tidak sama dengan ruang bebas bagi pelari.

Residential/asphalt/3 m kini menghasilkan H=1, S=1, W=1, C=1. Ruas 100 m
memberi reward karakter +0,50; bila permissive menjadi +0,40 sebelum komponen
lain. Pada lebar 2 m diperoleh W=0,20, C=0,88 dan reward karakter +0,38.

Snapshot 21.374 edge: width score 1 pada 9.696 edge, 0,20 pada 4.450,
dan 0,50 pada 7.228. Surface score 1 pada 14.392, 0,20 pada 54, 0,50 pada 6.928.
Jumlah action tetap 21.300. Highway, bobot 0,55/0,30/0,15, reward akses,
mask, state, seed, epsilon dan jumlah episode tidak diubah pada revisi ini.
Analisis sudah dijalankan seluruhnya (21 cell kode) dan peta comfort diperbarui;
GraphML tidak ditulis ulang. Notebook verifikasi lama belum disesuaikan.

Metadata hasil mencatat surface_scoring dan width_scoring, selain highway dan
akses. Grup surface_satu_prioritas_20261102 sempat disiapkan tetapi belum ada
hasil saat ambang width diterapkan. Grup final revisi ini adalah
surface_width_3m_20261102, yang kemudian dijalankan pengguna (bagian 8.2.2).

## 6. Implementasi Q-Learning pada Core Bersama

### 6.1 Input dan snapping start

Semua notebook scenario memanggil **load_or_download_graph()** dari `rute_lari_core.py`. Fungsi ini memuat **data_osm_5km/graf_jalan_kaki_5km.graphml**, atau mengunduh serta menyimpannya bila belum ada. Koordinat start latitude-longitude ditransformasi ke CRS graf, kemudian **ox.distance.nearest_nodes** menentukan START_NODE. Ini memastikan agen mulai pada node yang benar-benar ada dalam graf.

Setelah GraphML dimuat, **add_comfort_scores(G)** dipanggil lagi untuk membuat atribut skor tersedia pada memori. Dictionary **NODE_XY** menyimpan koordinat meter semua node.

### 6.1.1 Notebook uji titik start (2 November 2026)

Notebook khusus percobaan koordinat baru memakai satu folder kerja tetap:
hasil_bab_4/training_qlearning_5km/uji_titik_start/terbaru/.
Tidak ada RUN_LABEL/POINT_NAME atau opsi memuat cache pada notebook terbaru.
Koordinat yang telah diisi pengguna dipertahankan.

1. Cell unduh selalu memanggil load_or_download_graph(force_download=True,
   center_point=input, graph_path=path khusus, use_cache=False). GraphML dan cache
   HTTP dilewati. Graf/metadata unduhan ditimpa; hasil training/ dan peta marker
   lama di folder terbaru dibuang setelah unduhan berhasil.
2. Cell peta membuat marker input biru/START hijau dan garis snap. Radio Highway
   default/Surface mengganti warna seluruh graf; overlay marker Access tersedia
   per kategori (default mati), tanpa smoothness. Legenda mengikuti pilihan.
   Ruas awal legal overlay default mati agar tidak menutupi warna highway.
   Tooltip memuat H/S/W/access/panjang dan reward dasar. Marker tengah ruas
   dihitung pada CRS meter; dua arah identik digabung, key paralel tetap terpisah.
   Popup menunjukkan tag dan status whitelist, bukan lokasi pagar. Graf lengkap
   termasuk ruas yang ditolak tetap tampil untuk inspeksi. HTML tetap ditimpa pada
   peta_titik_start.html. Tidak ada unduhan tambahan; hanya memakai G dalam memori.
3. Cell training memakai graf G dalam memori tanpa mengunduh/memuat ulang.
   Folder training/ selalu dibersihkan dan ditimpa. Q-table dimulai dari kosong;
   hasil seed/konfigurasi lama tidak bercampur. File graf, metadata_graf.json dan
   peta_titik_start.html di folder induk tidak berubah ketika training diulang.
4. Cell hasil menampilkan metrik/grafik/peta dari training terakhir tanpa melatih.
   Setelah training ulang, jalankan cell hasil untuk memperbarui tampilannya.

Default B/150000 episode per seed/horizon epsilon50000; alternatif C/75000/None.
RANDOM_SEEDS=None memilih tiga seed acak berbeda tiap batch. Tuple tiga angka
dapat diisi untuk mengulang. MAX_WORKERS=3 memakai proses mandiri core. Metadata
titik ditulis setelah seluruh hasil/peta per seed selesai, memuat input/start/snap,
hash graf/core, metadata graf, konfigurasi dan tiga seed. Cell hasil membandingkan
urutan edge serta menampilkan semua peta. Rincian revisi tiga seed pada akhir dokumen.

Konteks pencarian/peta/konfigurasi/training dibatalkan saat unduhan dimulai.
Unduhan gagal tidak membolehkan training/peta lama dipakai untuk titik baru.
Koordinat atau radius berubah harus diikuti unduhan/peta; konfigurasi berubah
harus diikuti cell konfigurasi/training. Hasil lama tidak ditampilkan sebagai
hasil titik/konfigurasi baru. Snap default >100 m dan tidak ada action awal legal
masih mencegah training. Tidak ada FileExistsError untuk hasil yang sudah ada.

Pengaturan ini hanya notebook uji titik. Core, seed A--C, graf utama dan artefak
penelitian tetap. Folder uji titik/run lama tidak dibaca atau dihapus oleh revisi.
File graf tersimpan merupakan rekaman masukan; cell unduh tidak memakainya sebagai
cache. Tile basemap tetap mengikuti layanan peta/browser, berbeda dari unduhan graf.

Unduhan live sebelumnya pada input -7.281521,112.710178 berhasil tanpa cache HTTP:
8.284 node dan 22.136 edge. Ini riwayat, bukan unduhan baru pada revisi overwrite.
Alur overwrite diuji terkontrol memakai graf sintetis dan training singkat pada
folder sementara. Training panjang serta validasi lapangan belum dijalankan agent.

### 6.2 Action

Satu action adalah objek **EdgeAction** yang menyimpan:

    next_node, key, length_m, comfort_score, data edge

ID action di Q-table adalah **(next_node, key)**. Node saat ini sudah bagian dari state, sehingga action tidak perlu menyimpan current node. Identitas edge lengkap untuk log rute adalah **(current_node, next_node, key)**.

Fungsi **build_actions(G)** membuat ACTIONS_BY_NODE hanya untuk edge yang semua nilai access terisinya masuk ACCESS_WHITELIST, atau tag access-nya kosong. Edge paralel yang lolos tetap menjadi action berbeda. Tidak ada pemilihan edge berdasarkan comfort secara paksa; agen mempelajarinya melalui reward dan Q-table.

Contoh, `(u, v, key=0)` dan `(u, v, key=1)` adalah **dua action berbeda** walaupun sama-sama berakhir di node `v`. Q-table menyimpan nilai masing-masing secara terpisah: `Q[state][(v, 0)]` dan `Q[state][(v, 1)]`. Saat eksplorasi, salah satunya dapat dipilih acak; saat eksploitasi, action dengan Q-value terbesar dipilih. Perbedaan panjang, comfort score, atau nilai masa depan dapat membuat Q-value keduanya berbeda. Namun aturan revisit tetap berbasis ID node tujuan `v`: memilih edge dengan key berbeda tetapi menuju `v` yang sudah dikunjungi tetap dianggap revisit.

### 6.3 Scenario state

| Scenario | State | Tujuan |
|---|---|---|
| A | (current_node,) | Baseline: agen hanya tahu posisi node. |
| B | (current_node, progress_bin) | Membedakan keputusan awal dan akhir pada node yang sama. |
| C | (current_node, previous_node, progress_bin) | Menambahkan arah kedatangan. |

Fungsi pembentuk state adalah **build_state(environment, scenario)**. Jangan mengganti istilah ini menjadi encoder.

Kata **bin** berarti *bucket* atau kategori rentang nilai. Pada proyek ini, `progress_bin` tidak menyimpan jarak meter yang persis, melainkan nomor kategori progres jarak. Parameter `PROGRESS_BINS = 16` berarti rentang 0--5.500 m dibagi menjadi **16 kategori**, dengan indeks 0 sampai 15. Angka **15 bukan pilihan parameter terpisah**; ia adalah indeks terakhir karena indeks Python dimulai dari 0: `16 - 1 = 15`.

Nilai 16 dipilih sebagai kompromi desain: cukup rinci untuk membedakan fase awal, tengah, dan akhir rute (sekitar 343,75 m per kategori), tetapi tidak terlalu banyak sehingga kombinasi state `(node, progress_bin)` membuat Q-table menjadi jauh lebih besar dan jarang dikunjungi. Nilai ini bukan rumus standar universal; bila kelak diubah, seluruh Scenario A--C harus dijalankan ulang agar perbandingan tetap adil.

**progress_bin** menghitung jarak yang sudah ditempuh menjadi 16 kategori:

    int(total_distance_m / MAX_DISTANCE_M × 16)

`MAX_DISTANCE_M` bernilai 5.500 m. Maka satu kategori kira-kira mewakili 5.500 ÷ 16 = 343,75 m. `int(...)` membuang bagian desimal, sehingga hasilnya adalah indeks kategori, bukan jarak meter.

| Jarak yang sudah ditempuh | Perhitungan ringkas | progress_bin |
|---:|---:|---:|
| 0 m | int(0 ÷ 5.500 × 16) | 0 |
| 2.750 m | int(2.750 ÷ 5.500 × 16) | 8 |
| 5.000 m | int(5.000 ÷ 5.500 × 16) | 14 |
| 5.500 m | int(5.500 ÷ 5.500 × 16) = 16, lalu dibatasi | 15 |

Hasil akhirnya selalu dibatasi pada 0 sampai 15 melalui `min(PROGRESS_BINS - 1, max(0, raw_bin))`. Batas bawah 0 menjaga nilai tidak negatif; batas atas 15 mencegah indeks 16 atau lebih ketika jarak mencapai/melewati 5.500 m. Karena itu node yang sama dapat menjadi state berbeda saat agen masih awal, pertengahan, atau mendekati batas jarak.

### 6.4 Kondisi environment

Kelas **RunningRouteEnvironment** menyimpan:

    current_node, previous_node, total_distance_m, step_count,
    node_visits, revisit_count, path_nodes, path_actions,
    done, is_loop, termination_reason

**reset()** membuat episode baru: current node kembali ke start, jarak 0, previous node -1, start dihitung telah dikunjungi satu kali, dan riwayat rute dikosongkan.

### 6.5 Action mask dan revisit

Fungsi **available_actions()** membagi edge keluar menjadi tiga kelompok:

1. **fresh_actions**: next node belum dikunjungi.
2. **closing_actions**: next node adalah start dan total jarak baru berada dalam 4.500–5.500 m.
3. **revisit_actions**: next node sudah dikunjungi, revisit diizinkan, jarak sudah minimal 50% dari target, dan node belum dikunjungi dua kali.

Kebijakan yang dipakai:

    jika ada fresh action: fresh_actions + revisit_actions + closing_actions
    jika tidak ada fresh tetapi revisit ada: revisit_actions + closing_actions
    jika fresh dan revisit kosong: closing_actions saja

Dengan urutan ini, sebelum 50% target `revisit_actions` masih kosong sehingga agen hanya melihat fresh dan closing action. Setelah 50% target, revisit yang memenuhi syarat ikut ditawarkan **meskipun fresh action masih ada**. Batas ini sengaja disamakan dengan fase pulang agar agen dapat mempertimbangkan jalur lama tepat ketika reward arah pulang mulai aktif. Ini memberi agen pilihan untuk memakai node lama sebagai jalur pulang, tanpa mengizinkan pengulangan tak terbatas.

Konfigurasi tetap untuk semua scenario:

| Parameter | Nilai |
|---|---:|
| ALLOW_REVISIT | True |
| REVISIT_AFTER_RATIO | 0,50 |
| RETURN_PHASE_RATIO | 0,50 |
| MAX_NODE_VISITS | 2 |

Ini penting: A–C diuji secara adil karena tidak mempunyai environment berbeda.

Kepulangan ke start di luar rentang 4.500--5.500 m dicegah oleh action mask sebelum action dipilih. Fungsi step juga menolak action yang tidak legal. Terminasi aktif hanya success, over_distance, no_available_action, dan step_limit.

Setiap kali `closing_actions` tidak kosong, environment mencatat `closing_action_was_available=True` untuk episode tersebut. Flag ini **tidak** mengubah daftar action, reward, atau policy; ia hanya mencatat bahwa agen pernah memiliki kesempatan legal untuk langsung menutup loop.

### 6.6 Urutan kerja step(action)

Urutan fungsi **step()** harus dipahami sebelum dimodifikasi:

1. Memastikan episode belum selesai.
2. Menghitung action legal dan menolak action yang tidak ada pada action mask.
3. Menyimpan current node, next node, serta jarak lurus sebelum bergerak.
4. Mengubah posisi, total jarak, previous node, riwayat rute, jumlah kunjungan, dan jumlah langkah.
5. Menghitung reward comfort edge dan menambahkan komponen penalti access permissive.
6. Menambahkan penalti jika terjadi revisit ke node selain start.
7. Memeriksa terminal dengan urutan: success, over_distance, step_limit. Kondisi no_available_action ditangani saat tidak ada action legal.
8. Jika belum terminal dan jarak sudah 50% target, menambahkan reward arah pulang.
9. Mengembalikan next state, reward, done, dan info.

is_loop hanya menjadi True apabila action memasuki start dan jarak total valid. termination_reason pada kondisi tersebut adalah success.

## 7. Reward, Policy, dan Pembaruan Q-table

### 7.1 Reward

    R = R_ruas + R_akses + R_arah + R_revisit + R_terminal + R_buntu

| Komponen | Aturan |
|---|---|
| Ruas | (0,55*rH+0,30*rS+0,15*rW)*L/100 |
| Akses | permissive -0,10*L/100; yes/kosong 0 |
| Arah awal | Sebelum langkah <2.500 m dan mendekat: -0,60*(d_before-d_after)/100 |
| Arah pulang | Jika cabang awal tidak berlaku, setelah langkah >=2.500 m: +0,60*(d_before-d_after)/100 |
| Revisit | -10 per kunjungan ulang node non-start yang masih legal |
| Sukses | +100, kembali ke start pada 4.500--5.500 m |
| Kelebihan jarak/buntu/batas langkah | Masing-masing -50 |

L adalah panjang ruas; d jarak lurus ke start. Ruas gabungan yang memuat
permissive dikenai penalti sepanjang edge. Action access di luar whitelist tidak
pernah ditawarkan, bukan hanya diberi penalti. Tidak ada reward smoothness.

Urutan terminal: sukses, over_distance, step_limit, lalu arah. Terminal langsung
tidak menambah arah; kembali ke start bebas penalti revisit. Jika setelah langkah
masih berjalan tetapi tidak ada action, train_step menambahkan -50 sekali dan
bootstrap Q nol. Buntu sejak awal memberi -50 tanpa perpindahan/update Q.
Ruas melintasi 2.500 m memeriksa penalti fase awal dahulu. Ambang dan mask tetap.

Metadata baru merekam formula/bobot/rentang, prioritas H/S/W, direction_reward,
revisit_penalty, terminal_rewards, whitelist dan penalti permissive. Metadata/CSV/
Q-table lama tidak ditulis ulang. Hasil beda versi reward tidak langsung sebanding.

### 7.1.1 Dasar skala koefisien arah = 0,60

Koefisien kedua fase dipilih 0,60 agar sederhana dan memberi pengaruh arah yang
cukup terlihat. Perubahan jarak lurus 100 m berkontribusi +/-0,60; 50 m +/-0,30.
Reward ruas maksimum 100 m adalah +1. Jadi pada perpindahan lurus penuh pengaruh
arah 60% dari kontribusi ruas maksimum. Ini analisis skala, bukan bukti optimal.

### 7.1.2 Dasar skala bonus berhasil = +100

Reward ruas ideal pada target 5 km = 1*5.000/100 = 50. Bonus dipilih dua kali
nilai itu, yaitu +100. Faktor dua merupakan asumsi desain untuk menekankan tujuan
loop, bukan ketentuan Q-Learning. Pada panjang maksimum valid 5.500 m, batas ruas
55. Jika perubahan jarak lurus tidak melebihi panjang ruas, batas kontribusi arah
positif yang longgar 0,60*5.500/100 = 33. Jumlah batas 88 di bawah bonus 100,
namun ini bukan jaminan urutan return semua sukses/gagal. Kegagalan bisa melewati
batas jarak dan gamma=0,95 memberi pengaruh waktu penerimaan bonus.

### 7.1.3 Dasar penalti terminal dan revisit

Semua kegagalan diberi -50 karena sama-sama tidak memenuhi tugas; tidak ada dasar
kuat untuk membedakan -50/-45/-40. Skala -50 setara reward ruas ideal 5 km.
Penalti ditambahkan ke reward perjalanan, sehingga total gagal tidak wajib negatif.
Revisit -10 setara reward ruas ideal 1.000 m. Pengguna memilih nilai ini agar
kunjungan ulang kurang menarik, sambil tetap diizinkan untuk pulang. Contoh
100 m seluruh prioritas, mendekat 100 m pada fase pulang dan revisit legal:
+1+0,60-10 = -8,40 sebelum akses/terminal; pada -5 totalnya -3,40,
pada -3 totalnya -1,40 dan
pada -1 totalnya +0,60.
Ini asumsi desain yang akan diuji, bukan nilai optimal atau jaminan overlap turun.
Revisit dihitung berdasarkan node, sedangkan overlap berdasarkan ruas fisik;
mengunjungi persimpangan lama melalui ruas baru tetap terkena penalti revisit.
Aturan action mask, ambang 2.500 m dan maksimum dua kunjungan tidak berubah.

Nilai ini konfigurasi awal yang disepakati, belum hasil optimasi. Penilaian akhirnya
berdasarkan keberhasilan, jarak, karakter ruas dan perilaku, bukan total reward saja.

### 7.2 Epsilon-greedy

**choose_action()** memilih action legal secara acak dengan peluang epsilon; selain itu ia memilih Q-value terbesar. Bila nilai Q terbaik seri, salah satu action terbaik dipilih secara acak.

Core menyediakan dua mode jadwal epsilon. Nilai `epsilon_decay_episodes` bersifat **opsional**.

1. Bila nilainya `None`, mode lama dipakai: epsilon turun selama seluruh jumlah episode training (`K = N`).
2. Bila nilainya diisi, misalnya `50.000`, epsilon hanya turun selama 50.000 episode pertama (`K = 50.000`), lalu tetap pada 0,05.

Secara umum nilai epsilon per episode dihitung dengan:

    progress = min(episode ÷ (K − 1), 1)
    epsilon = 0,05 + (1,00 − 0,05) × (1 − progress)

`K` adalah lama fase penurunan epsilon. Evaluasi greedy memakai epsilon 0 agar policy yang diuji tidak mengandung eksplorasi acak.

Satu nilai epsilon dipakai untuk seluruh action di dalam satu episode. Artinya pada episode awal agen sangat sering mengeksplorasi action legal secara acak; seiring episode bertambah, agen makin sering memakai Q-value terbaik yang sudah dipelajari.

Simulasi nilai epsilon pada eksperimen `EPISODES=40.000`:

| Episode (dimulai dari 0) | Epsilon kira-kira | Makna |
|---:|---:|---|
| 0 | 1,000 | Hampir setiap pemilihan action bersifat acak. |
| 10.000 | 0,762 | Eksplorasi masih dominan, tetapi Q-value mulai lebih sering dipakai. |
| 20.000 | 0,525 | Eksplorasi dan eksploitasi seimbang secara kasar. |
| 39.999 | 0,050 | Hanya sekitar 5% peluang action acak. |

Pada akhir fase decay, apabila ada tiga action legal, agen masih memiliki sekitar 5% peluang memilih salah satu action secara acak. Saat evaluasi greedy, epsilon dipaksa menjadi 0 sehingga agen selalu memilih action legal dengan Q-value tertinggi; hasil evaluasi tidak dipengaruhi eksplorasi acak.

#### Seed dan pengacakan yang dapat diulang

Walaupun Q-Learning memerlukan pilihan acak, hasil eksperimen perlu dapat diuji ulang. Karena itu setiap training membuat generator angka acak NumPy dengan:

    rng = np.random.default_rng(seed)

`seed` adalah angka awal pembentuk urutan pseudoacak, bukan nilai yang menghilangkan pengacakan. Generator ini dipakai ketika `choose_action()` memilih action legal secara acak pada eksplorasi epsilon-greedy dan ketika beberapa action memiliki Q-value terbaik yang sama. Dengan graf, kode, konfigurasi, dan seed yang sama, urutan pilihan acak pada training seharusnya sama sehingga hasil dapat direproduksi.

Pengaruh seed terhadap rute terjadi **secara bertahap melalui pemilihan edge**, bukan dengan memilih satu rute lengkap secara langsung. Pada setiap langkah training, generator dipakai dua kali ketika eksplorasi terjadi:

    if rng.random() < epsilon:
        action = actions[int(rng.integers(len(actions)))]

`rng.random()` menentukan apakah agen melakukan eksplorasi. Jika ya, `rng.integers(len(actions))` memilih indeks salah satu action legal. Dalam graf proyek ini, satu action adalah edge spesifik `(next_node, key)`, sehingga pengacakan tersebut benar-benar dapat menentukan ruas jalan berikutnya yang dipilih agen. Action acak pada langkah awal dapat membawa agen ke node berbeda; akibatnya daftar action legal, reward yang diterima, pembaruan Q-value, dan rute pada langkah berikutnya juga dapat berbeda.

Dengan seed yang sama, kedua nilai pseudoacak tersebut muncul dalam urutan yang sama saat training diulang. Karena graf, daftar action legal, dan aturan environment juga sama, agen biasanya memilih edge eksplorasi yang sama dan memperoleh rute hasil training yang sama. Jika seed diubah, urutan eksplorasi dapat berubah; rute akhirnya dapat berbeda, meskipun tidak harus selalu berbeda apabila kebijakan greedy yang dipelajari akhirnya mengarah ke rute dominan yang sama. Ketika agen tidak mengeksplorasi, action dipilih berdasarkan Q-value tertinggi, bukan melalui `rng.integers()`; pengecualian hanya terjadi bila beberapa Q-value tertinggi seri.

Contoh sederhana: training dengan `seed=0` yang dijalankan dua kali akan menerima urutan angka pseudoacak yang sama, sehingga pilihan eksplorasi dan hasilnya dapat sama persis. Training dengan `seed=1` memakai urutan pseudoacak lain sehingga jalur eksplorasinya dapat berbeda. Dengan kata lain, hasil yang sama ketika notebook dijalankan ulang bukan berarti Q-Learning tidak menggunakan pengacakan; pengacakan tersebut sengaja dikendalikan agar dapat direproduksi.

Eksperimen memakai lima seed, yaitu `(0, 1, 2, 3, 4)`. Seed yang berbeda menghasilkan pola eksplorasi berbeda; sebab itu keberhasilan yang muncul pada seluruh seed lebih meyakinkan daripada keberhasilan pada satu seed saja. Evaluasi greedy menggunakan generator terpisah `np.random.default_rng(seed + 100_000)`. Epsilon evaluasi bernilai 0, tetapi generator tersebut masih diperlukan bila terjadi seri Q-value terbaik; offset `100.000` memisahkan urutan acak evaluasi dari urutan acak training.

### 7.3 Rumus update

Blok satu langkah pada `train_q_learning()` dipisahkan menjadi `train_step(environment, q_table, rng, epsilon, action=None, verbose=False)`. Fungsi ini membaca `environment.latest_state`, memilih action, menjalankan transisi, menangani penalti buntu, dan memperbarui Q. Training serta notebook memakai fungsi yang sama. Property `latest_state` memanggil `build_state()` tanpa menyimpan salinan state. `RunningRouteEnvironment.step()` tetap seperti semula; tidak ada class tambahan.

    Q(s, a) = Q(s, a)
            + alpha × [reward + gamma × max Q(s_baru, a_baru) − Q(s, a)]

Nilai masa depan hanya dicari dari action legal pada state berikutnya. Jika episode selesai atau tidak ada action legal, nilai masa depan adalah 0.

## 8. Konfigurasi Training dan Grafik

| Parameter | Nilai | Makna |
|---|---:|---|
| ALPHA | 0,15 | Laju pembaruan Q-value. |
| GAMMA | 0,95 | Bobot reward masa depan. |
| EPSILON_START | 1,00 | Eksplorasi awal. |
| EPSILON_END | 0,05 | Eksplorasi akhir. |
| EPISODES | 10.000 | Default cepat untuk satu kali uji notebook. Eksperimen mengirim jumlah episode secara eksplisit. |
| epsilon_decay_episodes | None atau 50.000 | None mempertahankan jadwal dinamis lama; 50.000 dipakai pada eksperimen durasi training dengan epsilon decay tetap. |
| MAX_STEPS_PER_EPISODE | 220 | Batas langkah per episode. |
| SEEDS | (0, 1, 2, 3, 4) | Lima seed eksperimen. |
| ROLLING_WINDOW | 50 | Ukuran rata-rata bergerak untuk menghaluskan tren grafik. |

Setiap scenario melatih lima Q-table, satu untuk setiap seed. Untuk grafik training, nilai lima seed pada episode yang sama dirata-ratakan terlebih dahulu, kemudian dihaluskan dengan rata-rata bergerak 50 episode. Evaluasi greedy tetap dicatat per seed.

### 8.1 Diagnosis TD-error

Selama training, setiap pembaruan Q menghitung **TD-error** (Temporal Difference error), yaitu selisih antara target nilai Q dan nilai Q lama.

    TD-error = reward + gamma × nilai Q terbaik pada state berikutnya − nilai Q lama

Notebook menyimpan `mean_abs_td_error`, yaitu rata-rata nilai absolut TD-error dari seluruh update Q dalam satu episode. Nilai absolut dipakai agar perubahan naik dan turun tidak saling meniadakan. Grafik diagnosis menampilkan rata-rata bergerak 50 episode dari lima seed.

TD-error yang semakin kecil dan mendatar menunjukkan bahwa nilai Q pada state-action yang **dikunjungi** makin sedikit berubah. Namun, nilai kecil tidak membuktikan rute sudah baik: agen dapat stabil pada policy yang tetap gagal menutup loop. Oleh karena itu, TD-error adalah metrik diagnosis stabilitas pembelajaran, bukan metrik evaluasi utama; tetap baca bersama evaluasi greedy, `is_loop`, jarak akhir ke start, dan peluang closing action tersedia.

Kolom `steps` juga tetap disimpan pada `training_history_{scenario}.csv` sebagai diagnosis internal. Kolom tersebut tidak ditampilkan sebagai grafik utama karena jumlah langkah dipengaruhi panjang edge dan proses simplifikasi graf. Pada target rute 5 km, langkah lebih sedikit tidak selalu berarti rute lebih baik. Indikator yang relevan bila agen benar-benar terlalu banyak melangkah sudah tersedia melalui terminasi `step_limit`.

### 8.2 Rancangan aktif: empat konfigurasi

Per 29 Oktober 2026, setiap notebook A--C menguji dua jumlah episode dengan dua
strategi epsilon. Rumusan masalah nomor 2 mengenai pengaruh representasi state
tetap dipertahankan; state dibandingkan pada kondisi training yang sama.

| Strategi epsilon | Total episode per seed | Horizon penurunan |
|---|---:|---:|
| Dinamis | 75.000 | 75.000 (`epsilon_decay_episodes=None`) |
| Dinamis | 150.000 | 150.000 (`epsilon_decay_episodes=None`) |
| Horizon tetap | 75.000 | 50.000 |
| Horizon tetap | 150.000 | 50.000 |

Training total 50k dan 100k dikeluarkan dari notebook aktif; dinamis 150k ditambahkan.
Setiap konfigurasi melatih ulang seed `(0,1,2,3,4)` dari Q-table kosong. Beban satu
scenario 20 training/2.250.000 episode, total A--C 60 training/6.750.000 episode.
Graf, reward, mask, dan parameter lain tetap sama. Evaluasi akhir greedy (`epsilon=0`).

`RESULT_GROUP="reward_revisit_10_overlap_count_20261103"` pada cell pemuatan graf harus sama di
A/B/C. Artefak memakai subfolder `<RESULT_GROUP>/dinamis_<jumlah>_<scenario>` atau
`<RESULT_GROUP>/tetap_50000_episode_<jumlah>_<scenario>` di folder hasil training.
Hasil sebelumnya, termasuk grup lima konfigurasi, tetap disimpan. Untuk menyimpan
run berikutnya terpisah, ubah RESULT_GROUP secara sama di A/B/C.

Cell tampilan hasil tetap terpisah dari training. Ringkasan dinamis dan horizon
50k masing-masing membaca dua titik (75k/150k), sehingga perbandingan strategi
tersedia pada kedua anggaran episode. Output notebook dibersihkan untuk mencegah
hasil lama terbaca sebagai run baru pada saat konfigurasi disiapkan. Pengguna
kemudian menyelesaikan seluruh training; hasilnya dirangkum di bagian berikut.
Jangan mengisi hasil dinamis 150k dari arsip konfigurasi lain.

### 8.2.1 Arsip baseline empat konfigurasi (29 Oktober 2026)

Sumber: `hasil_bab_4/training_qlearning_5km/konfigurasi_empat_20261029/`.
Angka berikut adalah loop valid saat evaluasi greedy final dari lima seed;
bukan proporsi episode training.

| Strategi epsilon | Total episode | A | B | C |
|---|---:|---:|---:|---:|
| Dinamis | 75.000 | 1/5 | 1/5 | 1/5 |
| Dinamis | 150.000 | 0/5 | 0/5 | 4/5 |
| Horizon 50.000 | 75.000 | 0/5 | 5/5 | 3/5 |
| Horizon 50.000 | 150.000 | 0/5 | 5/5 | 5/5 |

Pada horizon 50k total 150k, B memiliki galat rata-rata 104,28 m, skor karakter
ruas 0,762, dan rata-rata 32.208,4 state Q-table; C masing-masing 160,79 m,
0,726, dan 53.903,4. Keduanya 5/5 sukses. C memiliki simpangan baku galat lebih
kecil (46,14 m vs B 88,73 m), sehingga tidak ada klaim B unggul semua metrik.
B 150k horizon 50k merupakan kandidat utama bila prioritasnya loop, galat,
lalu skor ruas. B 75k tetap alternatif anggaran episode lebih kecil (5/5 sukses,
galat 270,32 m). Kandidat ini dipilih dari hasil eksperimen, bukan bukti optimal.

Pengaruh representasi state bergantung konfigurasi epsilon/durasi. C unggul
keberhasilan pada dinamis 150k, sedangkan B mencapai 5/5 lebih awal pada horizon
50k. Rumusan masalah kedua tetap dapat dijawab melalui perbandingan A--C pada
kondisi training sama. A sempat berhasil 1/5 dinamis 75k; jangan menyebutnya
tidak pernah bisa membentuk loop. Hasil lima seed belum menjamin generalisasi.

Pada 10.000 episode training terakhir konfigurasi horizon 50k total 150k,
keberhasilan B 75,26%, C 64,95%, dan A 1,90%. Angka training mengandung eksplorasi
epsilon 0,05 dan tidak sama dengan evaluasi greedy final. Seluruh 35 evaluasi
gagal tidak pernah memiliki closing action legal: 29 over_distance dan 6 buntu.

Pemeriksaan: 6.750.000 baris history lengkap, jadwal epsilon sesuai, 60 evaluasi
greedy dari Q-table tersimpan menghasilkan metrik/node/action yang sama, dan
prefix history 75k identik pada semua 15 pasangan seed horizon 50k. Training
75k/150k tetap dijalankan dari awal secara terpisah; prefix sama karena seed dan
jadwal sama. Dinamis 75k/150k mengubah durasi sekaligus horizon epsilon, sehingga
perbedaannya bukan efek tambahan episode pada jadwal yang tetap.

Laporan lengkap, tabel per seed, diagnosis akhir, grafik tren, dan catatan
pemeriksaan tersedia di `docs/temp/analisis_empat_konfigurasi_20261029/`.
Tidak ada perubahan core, notebook, reward, mask, snapshot, atau hasil mentah.
Pembahasan notebook verifikasi tetap ditunda; analisis hasil ini tidak menambah
kasus verifikasi. Ekspor GPX dan validasi lapangan belum dilakukan.

### 8.2.2 Arsip surface dan width 3 m (2 November 2026)

Sumber: `hasil_bab_4/training_qlearning_5km/surface_width_3m_20261102/`.
Empat konfigurasi A--C, lima seed, 60 training, 6.750.000 baris history.

| Strategi epsilon | Episode per seed | A | B | C |
|---|---:|---:|---:|---:|
| Dinamis | 75.000 | 0/5 | 0/5 | 5/5 |
| Dinamis | 150.000 | 0/5 | 0/5 | 5/5 |
| Horizon 50k | 75.000 | 1/5 | 1/5 | 5/5 |
| Horizon 50k | 150.000 | 0/5 | 5/5 | 5/5 |

C mencapai 5/5 pada setiap konfigurasi teruji; B 5/5 pada horizon 50k total
150k. A berhasil satu seed horizon 50k total 75k, sehingga tidak selalu gagal.
Pada horizon 50k total 150k, galat B 268,47 m vs C 339,91 m; mean comfort B
0,9034 vs C 0,9193; rata-rata Q-state B 28.103,2 vs C 46.671,6. Tidak ada
klaim satu konfigurasi unggul semua metrik atau berlaku di titik awal lain.

Ada 27 loop valid dengan urutan edge berbeda, bukan jaminan rute berbeda secara
geografis. Seluruhnya masih memuat width <3 m, width tak diketahui dan permissive;
preferensi skor tidak menjadi larangan. Gagal: 29 over_distance dan 4 buntu;
semua kegagalan tidak pernah memiliki closing action legal.

History/epsilon/metadata/manifest lengkap. Semua 60 evaluasi direproduksi dari
Q-table tersimpan: metrik cocok, node/action sama persis. Audit tidak menjalankan
training atau mengubah 228 berkas mentah. Ini reproduksi hasil, bukan pengganti
verifikasi notebook atau validasi lapangan.

Laporan dan CSV per seed: `docs/temp/analisis_surface_width_3m_20261102/`.
Skor/reward dari pemetaan lama tidak langsung sebanding. Perbandingan ke grup
highway lama mengubah surface dan width sekaligus, bukan uji satu faktor.

### 8.2.3 Hasil aktif reward langsung (3 November 2026)

Pengguna menyelesaikan reward_direct_20261103: 12 folder/60 training dan
6.750.000 episode. Greedy A/B/C dari lima seed: dinamis 75K=0/5/5,
dinamis 150K=0/5/5, horizon 50K total 75K=2/5/5, total 150K=1/5/5.
B/C masing-masing 20/20 valid; ini berlaku pada snapshot/start/seed teruji.

B horizon 50K total 150K memiliki galat rata-rata terkecil dan skor ruas tertinggi
di antara konfigurasi B/C: 289,82 m/0,9356/Q-state 15.779,0; C pada konfigurasi
sama 321,18 m/0,9255/37.710,2. B horizon total 75K sudah 5/5, dengan
321,74 m/0,9285/15.106,8 Q-state. Horizon lebih kecil galatnya untuk B,
sedangkan dinamis lebih kecil untuk C pada kedua durasi. Jangan menyebut horizon
syarat mutlak keberhasilan B atau tambahan previous_node selalu lebih baik.

Ada 43 loop valid, hanya 33 urutan edge unik. Seluruhnya 4.509,00--4.915,66 m,
di bawah 5.000 m tetapi sah toleransi. Reward tidak memiliki komponen khusus
untuk memperkecil galat absolut ke 5.000 m. Semua loop masih permissive,
width <3 m/unknown dan revisit; 30 menggunakan ruas nonprioritas/negatif.
Ini legal desain. Gagal 17 seluruhnya A: 12 over_distance dan 5 buntu, semuanya
tidak pernah memiliki closing action legal. A bukan selalu gagal.

Keberhasilan 10K episode training terakhir B/C: dinamis 75K 66,19%/54,35%;
dinamis 150K 81,55%/76,06%; horizon total 75K 84,83%/79,63%; horizon total
150K 87,11%/80,73%. Training bereksplorasi, evaluasi akhir greedy epsilon=0.
Perbedaan rate bukan bukti konvergensi umum atau efek state saja.

Seluruh metadata/history/epsilon diperiksa; 60 evaluasi direproduksi dari
Q-table, metrik serta node/action cocok. Core/GraphML dan 228 berkas input tetap.
Agent tidak menjalankan training baru/unduhan atau mengubah kode/notebook/mask.
Kandidat katalog B horizon total 150K; total 75K layak bila jumlah episode
menjadi pertimbangan. B seed 0 pada keduanya identik: 4.915,66 m, galat 84,34 m,
skor 0,9644 dan 14 revisit. Pemeriksaan peta/akses dan validasi lapangan tetap perlu.
Laporan/CSV/grafik: docs/temp/analisis_reward_direct_20261103/.
Skor/reward arsip lama tidak dibandingkan langsung; banyak komponen berubah.

### 8.2.4 Pengamatan B epsilon dinamis dengan overlap hitungan (3 November 2026)

Pengguna menyelesaikan B dinamis 75K dan 150K pada grup
reward_direct_overlap_count_20261103: 10 training/lima seed per konfigurasi,
1.125.000 baris history. Metadata basis count, episode/epsilon dan artefak lengkap.
Seluruh 10 evaluasi Q-table direproduksi; metrik/path sesuai dan count diperiksa
langsung dari geometri. Rute akhir serta metrik lama sama dengan arsip reward
langsung pada seed/konfigurasi yang sama. Tidak ada training baru oleh agent.

| Ukuran | 75K | 150K |
|---|---:|---:|
| Loop greedy | 5/5 | 5/5 |
| Overlap greedy rata-rata | 12,98% | 15,35% |
| Galat rata-rata | 399,63 m | 340,90 m |
| Skor ruas rata-rata | 0,9125 | 0,9247 |
| Rata-rata Q-state | 15.446,4 | 17.439,4 |
| Overlap seluruh episode, 10K terakhir | 11,97% | 12,82% |
| Keberhasilan training, 10K terakhir | 66,19% | 81,55% |

150K lebih dekat ke target rata-rata 58,72 m dan skor lebih tinggi, tetapi overlap
bertambah 2,37 poin persentase. Tidak unggul semua metrik. Kurva seluruh episode
naik dari sekitar 0,4% menjadi 12--13%; awal training rata-rata jarak hanya ~1 km,
sering belum mencapai izin revisit 2.500 m. Overlap rendah di awal bukan bukti
rute lebih baik. Overlap belum menjadi reward. Tidak membuat grafik yang memisah
berhasil/gagal. Epsilon rata-rata 10K terakhir berbeda (~0,1133 vs ~0,0817), jadi
jangan mengisolasi efek jumlah episode dari perbedaan fase eksplorasi itu.

Overlap greedy per seed 75K: 13,95%;20,93%;10%;10%;10%.
150K: 13,95%;11,63%;18,60%;18,60%;13,95%. Seed 1 membaik, lainnya tidak seragam.
75K tiga urutan edge unik (seed 2/3/4 sama), 150K empat (seed 0/4 sama).
Seluruh loop masih <5.000 m tetapi sah toleransi. Ini pengamatan B satu start/
snapshot, bukan hasil A--C lengkap atau validasi lapangan. Pembanding berikutnya
sesuai rancangan adalah B horizon 50K, tanpa mengubah reward dahulu.

Laporan/CSV/grafik: docs/temp/analisis_B_dinamis_overlap_count_20261103/ANALISIS.md.
Tidak mengubah core/notebook/reward/mask atau hasil mentah; hanya laporan dan
konteks markdown disinkronkan. Hasil count lain belum ditinjau pada audit ini.

### 8.2.5 Pengamatan empat konfigurasi B dengan overlap hitungan (3 November 2026)

Lengkap pada grup reward_direct_overlap_count_20261103: empat konfigurasi B,
20 training/lima seed per konfigurasi, 2.250.000 baris history. A/C belum tersedia
pada grup ini saat pemeriksaan. Seluruh metadata/episode/epsilon/artifact lengkap;
20 evaluasi Q-table direproduksi dan count diverifikasi. Nilai/rute akhir cocok
arsip reward_direct_20261103 untuk konfigurasi/seed sama. 80 berkas sumber tetap.

| Konfigurasi | Loop | Galat rata-rata | Overlap rata-rata | Skor ruas |
|---|---:|---:|---:|---:|
| Dinamis 75K | 5/5 | 399,63 m | 12,98% | 0,9125 |
| Dinamis 150K | 5/5 | 340,90 m | 15,35% | 0,9247 |
| Horizon 50K total 75K | 5/5 | 321,74 m | 15,05% | 0,9285 |
| Horizon 50K total 150K | 5/5 | 289,82 m | 17,43% | 0,9356 |

Saran praktis sementara B horizon total 75K: mean galat/overlap/skor lebih baik
sedikit dari dinamis 150K dengan setengah episode. Horizon 150K lebih baik galat/
skor, tetapi dibanding horizon 75K hanya memperbaiki galat 31,92 m sambil menambah
overlap 2,38 poin dan dua kali episode. Dinamis 75K paling rendah mean overlap.
Tidak satu konfigurasi unggul semua ukuran; selisih deskriptif pada lima seed,
bukan klaim signifikansi/generalitas. Semua konfigurasi tetap untuk laporan.

Training seluruh episode pada 10K akhir: overlap 11,97/12,82/13,75/14,21%;
keberhasilan 66,19/81,55/84,83/87,11% pada urutan konfigurasi tabel. Horizon
memiliki epsilon 0,05; dynamic window masih berbeda epsilon. Tidak menyimpulkan
konvergensi formal dari kurva mendatar atau bahwa overlap harus turun.

Pemilihan peta saat ini berdasarkan galat, tidak mempertimbangkan overlap.
Pada dua konfigurasi horizon, seed 0 terpilih: 4.915,66 m tetapi overlap 26,67%,
tertinggi di seed masing-masing. Kandidat kompromi yang dapat diperiksa:
- Dinamis 75K seed 0: 4.685,49 m / overlap 13,95% / skor 0,9255; identik
  dinamis 150K seed 0/4 serta horizon 150K seed 1/4.
- Horizon 75K seed 2: 4.614,91 m / overlap 11,36% / skor 0,9411.
20 hasil hanya 13 urutan edge unik; belum jaminan 13 rute geografis berbeda.

Belum mengubah reward/mask atau memilih kandidat katalog final. Periksa beberapa
rute/pagar/akses aktual dahulu. Untuk rumusan masalah kedua tetap pakai A--C
setelan sama; overlap akhir arsip A/C bisa dihitung ulang tanpa training, tetapi
tren overlap tiap episode A/C memerlukan pencatatan baru. Jangan menambah episode
atau faktor baru hanya untuk mengejar overlap rendah tanpa tujuan yang disepakati.

Laporan/CSV/grafik: docs/temp/analisis_B_empat_konfigurasi_overlap_count_20261103/ANALISIS.md.
Hanya laporan/dokumentasi diperbarui, tanpa training/unduhan/ubah kode atau
hasil mentah. Ini hasil B lokal, bukan validasi lapangan atau hasil lengkap A--C count.

### 8.3 Arsip hasil sebelum rancangan episode final

Bagian 8.4--8.7 di bawah ini memuat hasil lama pada rentang 10k--400k. Hasil tersebut berguna untuk menjelaskan alasan pemisahan jadwal epsilon, tetapi **tidak boleh dipakai sebagai angka atau kesimpulan final BAB IV**. Untuk pelaporan baru, gunakan hasil empat konfigurasi pada RESULT_GROUP aktif setelah pengguna menjalankannya; angka arsip tidak otomatis menjadi hasil baru.

### 8.4 Arsip sensitivitas Scenario B dengan epsilon dinamis

Hasil berikut berasal dari evaluasi greedy lima seed untuk setiap jumlah episode. Ini adalah catatan eksperimen sementara, bukan hasil final BAB IV.

| Episode | Success rate | Galat jarak rata-rata (m) | Reward rata-rata | Comfort rata-rata | Return progress ratio | Closing action rate |
|---:|---:|---:|---:|---:|---:|---:|
| 10.000 | 0,00 | 539,18 | -85,53 | 0,754 | 0,556 | 0,00 |
| 20.000 | 0,00 | 544,32 | -63,99 | 0,768 | 0,489 | 0,00 |
| 30.000 | 0,00 | 415,38 | -101,51 | 0,761 | 0,496 | 0,00 |
| 40.000 | 0,20 | 299,68 | -56,28 | 0,763 | 0,554 | 0,20 |
| 50.000 | 0,00 | 499,36 | -84,11 | 0,761 | 0,316 | 0,00 |

Pada data ini, 40.000 episode merupakan kandidat terbaik sementara: satu dari lima seed membentuk loop valid, galat jarak paling kecil, dan satu seed memiliki closing action legal. Namun, hasil 50.000 episode turun kembali. Dengan lima seed, satu keberhasilan mengubah rate sebesar 20%, sehingga pola tersebut belum cukup untuk klaim stabil atau untuk menyatakan 50.000 episode lebih buruk secara umum. Comfort relatif stabil; hambatan utama adalah agen jarang mencapai kondisi yang menyediakan closing action.

| Grafik | Arti |
|---|---|
| Rata-rata Keberhasilan 50 Episode Terakhir | Proporsi is_loop True dalam 50 episode terakhir. |
| Rata-rata Reward 50 Episode Terakhir | Rata-rata total reward 50 episode terakhir. Reward naik tidak otomatis berarti loop berhasil. |
| Rata-rata Jarak 50 Episode Terakhir | Rata-rata jarak rute 50 episode terakhir; bandingkan dengan target 5 km dan batas valid. |
| Rata-rata Skor Kenyamanan 50 Episode Terakhir | Rata-rata comfort score rute dalam 50 episode terakhir. |
| Jumlah State Q-table | Jumlah state unik yang memiliki entry Q-table. |
| Nilai Epsilon per Episode | Nilai peluang eksplorasi yang ditetapkan dari 1,00 ke 0,05 per episode; bukan rata-rata hasil episode. |
| Rata-rata Nilai Absolut TD-error 50 Episode Terakhir | Rata-rata besarnya selisih target Q dan Q lama pada update yang terjadi. Makin kecil berarti nilai Q yang dikunjungi makin sedikit berubah; bukan jaminan loop berhasil. |

### 8.5 Arsip epsilon decay tetap Scenario C

Hasil berikut berasal dari evaluasi greedy lima seed dengan `epsilon_decay_episodes=50.000`. Semua eksperimen dimulai ulang dari seed yang sama; untuk seed yang sama, urutan pengalaman hingga suatu episode adalah sama pada 50k, 100k, 200k, dan 400k karena jadwal epsilon juga sama. Dengan demikian, titik 100k, 200k, dan 400k dapat dibaca sebagai checkpoint kebijakan setelah tambahan training, bukan sebagai eksperimen dengan durasi eksplorasi berbeda.

| Total episode | Loop valid | Galat jarak rata-rata (m) | Reward rata-rata | Comfort rata-rata | Return progress rata-rata | Closing action tersedia |
|---:|---:|---:|---:|---:|---:|---:|
| 50.000 | 2/5 | 422,31 | 4,00 | 0,705 | 0,615 | 2/5 |
| 100.000 | 5/5 | 267,31 | 87,08 | 0,699 | 0,786 | 5/5 |
| 200.000 | 5/5 | 264,16 | 86,87 | 0,699 | 0,770 | 5/5 |
| 400.000 | 5/5 | 361,90 | 81,71 | 0,670 | 0,750 | 5/5 |

Pada 50.000 episode, fase penurunan epsilon baru selesai sehingga dua seed saja yang membentuk loop. Mulai 100.000 episode, semua seed membentuk loop valid dan keberhasilan itu tetap muncul pada checkpoint 200.000 serta 400.000 episode. Hal ini adalah bukti empiris bahwa Scenario C mulai stabil dalam **keberhasilan menutup loop** setelah tambahan training dengan epsilon rendah.

Namun, 400.000 episode bukan kandidat durasi terbaik hanya karena semua seed tetap sukses. Galat jarak rata-rata naik menjadi 361,90 m dan comfort rata-rata turun menjadi 0,670. Berdasarkan data ini, **100.000 episode** menjadi kandidat durasi final yang lebih hemat: sudah 5/5 sukses dan metrik kualitasnya hampir sama dengan 200.000 episode. Keputusan final tetap perlu dikonfirmasi dengan menjalankan Scenario A, B, dan C pada konfigurasi epsilon tetap serta jumlah episode 100.000 yang sama.

Sebagai diagnosis, rata-rata nilai absolut TD-error pada 50 episode terakhir dari lima seed berturut-turut adalah 1,224 pada 50k; 0,987 pada 100k; 0,915 pada 200k; dan 0,823 pada 400k. Tren tersebut menurun, sehingga nilai Q pada state-action yang dikunjungi makin sedikit berubah. Nilainya belum perlu dipaksa mencapai nol; TD-error dibaca bersama hasil greedy dan bukan sebagai bukti tunggal stabilitas.

### 8.6 Arsip epsilon decay tetap Scenario B

Hasil Scenario B dengan jadwal epsilon yang sama memperlihatkan pola berbeda dari eksperimen epsilon dinamis sebelumnya.

| Total episode | Loop valid | Galat jarak rata-rata (m) | Reward rata-rata | Comfort rata-rata | Return progress rata-rata | Closing action tersedia |
|---:|---:|---:|---:|---:|---:|---:|
| 50.000 | 0/5 | 499,36 | -84,11 | 0,761 | 0,316 | 0/5 |
| 100.000 | 5/5 | 114,43 | 75,64 | 0,759 | 0,743 | 5/5 |
| 200.000 | 5/5 | 309,77 | 77,50 | 0,767 | 0,747 | 5/5 |
| 400.000 | 5/5 | 340,01 | 78,34 | 0,764 | 0,729 | 5/5 |

Pada 50.000 episode, B belum membentuk loop. Namun setelah tambahan training dengan epsilon tetap 0,05, B mencapai 5/5 loop valid mulai 100.000 episode dan keberhasilan itu bertahan hingga 400.000 episode. Hasil ini menunjukkan bahwa kegagalan B pada eksperimen sebelumnya tidak dapat langsung diklaim semata-mata akibat tidak adanya `previous_node`; durasi eksplorasi yang terlalu panjang merupakan faktor yang sangat berpengaruh.

Untuk checkpoint 100.000 episode, B memiliki galat jarak dan comfort rata-rata lebih baik daripada C, sedangkan C memiliki return progress ratio serta reward rata-rata sedikit lebih tinggi. Karena keduanya sama-sama 5/5 sukses, pemilihan state final harus didasarkan pada tujuan prioritas yang dinyatakan secara eksplisit dan tabel evaluasi lengkap, bukan hanya satu metrik. TD-error B pada 50 episode terakhir adalah 1,749 pada 50k; 0,944 pada 100k; 0,622 pada 200k; dan 0,662 pada 400k. TD-error hanya dibandingkan sebagai tren di dalam scenario B, bukan sebagai angka absolut yang langsung diadu dengan C karena state yang dikunjungi berbeda.

### 8.7 Arsip epsilon decay tetap Scenario A

Scenario A memakai state paling sederhana, yaitu hanya `(current_node)`. Pada jadwal epsilon tetap 50.000 episode, A belum membentuk loop valid pada seluruh durasi yang diuji.

| Total episode | Loop valid | Galat jarak rata-rata (m) | Reward rata-rata | Comfort rata-rata | Return progress rata-rata | Jarak akhir ke start rata-rata (m) | Closing action tersedia |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 50.000 | 0/5 | 546,83 | -86,91 | 0,712 | 0,288 | 1.693,25 | 0/5 |
| 100.000 | 0/5 | 567,17 | -98,44 | 0,714 | 0,441 | 1.047,76 | 0/5 |
| 200.000 | 0/5 | 541,94 | -63,12 | 0,722 | 0,275 | 1.976,09 | 0/5 |
| 400.000 | 0/5 | 551,79 | -49,73 | 0,703 | 0,440 | 1.221,46 | 0/5 |

Pada checkpoint 100.000 episode, seluruh seed A berakhir `over_distance`; tidak satu pun pernah memiliki closing action legal pada evaluasi greedy. Tambahan training hingga 400.000 episode tidak mengubah hasil utama tersebut. TD-error pada 50 episode terakhir berada pada 1,327 (50k), 1,463 (100k), 1,406 (200k), dan 1,208 (400k), sementara keberhasilan training pada jendela yang sama tetap sekitar 0--2%. Ini menunjukkan A belum membentuk policy loop yang berhasil.

Jika dibandingkan pada konfigurasi yang sama—100.000 episode dan epsilon decay tetap 50.000—hasilnya adalah: A 0/5 loop, B 5/5 loop, dan C 5/5 loop. Bukti ini mendukung bahwa informasi progres jarak pada state penting untuk membedakan keputusan saat agen masih membangun rute dan saat harus mulai kembali ke titik start. Sementara itu, `previous_node` pada C dapat memengaruhi kecepatan awal dan trade-off metrik, tetapi pada konfigurasi ini bukan syarat mutlak untuk mencapai loop karena B juga berhasil 5/5.

### 8.8 Cara membaca reward training

Grafik reward training adalah akumulasi seluruh reward comfort, reward/penalti arah pulang, penalti revisit, dan reward terminal dalam episode yang dijalankan dengan kebijakan epsilon-greedy. Karena itu reward tidak wajib selalu naik seiring episode.

Sebagai contoh, episode yang buntu cepat dapat menerima `no_available_action = -45`. Episode lain dapat berjalan lebih jauh, menerima beberapa penalti revisit, lalu berakhir `over_distance = -50`; totalnya dapat lebih rendah, misalnya `-80` atau `-90`. Jadi penurunan reward dapat berarti agen makin sering mengambil rute gagal yang lebih panjang dan lebih mahal, bukan semata-mata kualitas model pasti memburuk.

Reward harus dibaca bersama grafik keberhasilan loop, rata-rata jarak, peluang closing action tersedia, serta termination rate. Bila reward menurun tetapi keberhasilan loop dan closing action meningkat, perlu dilihat trade-off-nya. Bila reward menurun sementara success tetap rendah dan `over_distance`/`no_available_action` tinggi, policy belum menemukan pola loop yang baik.

## 9. Evaluasi, Peta, dan Berkas Hasil

### 9.1 Evaluasi greedy

Fungsi **evaluate_greedy()** memakai epsilon 0. Tabel evaluasi utama sengaja dibatasi agar perbandingan Scenario A--C tetap fokus. Setiap baris mewakili satu seed dan hanya memuat metrik berikut.

Setelah training selesai untuk **setiap seed**, Q-table seed tersebut langsung diuji satu kali oleh `evaluate_greedy()`. Dengan lima seed `(0, 1, 2, 3, 4)`, eksperimen selalu menghasilkan lima evaluasi greedy: satu policy hasil training untuk setiap seed. Pada evaluasi ini `epsilon = 0`, sehingga tidak ada pemilihan action untuk eksplorasi acak; agen memilih action legal dengan nilai Q terbesar. `EPSILON_END = 0,05` hanya digunakan selama training. Bila dua atau lebih action memiliki nilai Q sama, pemilihan tie dilakukan dengan generator acak yang diberi seed tetap (`seed + 100000`) agar hasil evaluasi tetap dapat direproduksi.

| Metrik | Arti |
|---|---|
| is_loop | Keberhasilan utama: kembali ke start pada 4.500–5.500 m. |
| total_distance_m | Total jarak edge pada rute dalam meter. |
| absolute_distance_error_m | Selisih absolut dari target 5.000 m. Bukan pengganti is_loop. |
| total_reward | Akumulasi seluruh reward dan penalti dari satu evaluasi greedy. Dibaca bersama is_loop dan termination_reason, bukan sebagai satu-satunya ukuran kualitas rute. |
| mean_comfort | Rata-rata comfort edge berbobot panjang. Nilai mendekati 1 berarti proporsi panjang rute lebih banyak melewati edge berskor comfort tinggi. |
| distance_to_start_at_end_m | Jarak lurus posisi akhir ke start dalam meter. Makin kecil berarti agen setidaknya mendekati start sebelum terminasi. Ini tidak membuktikan loop karena agen dapat dekat start tanpa kembali ke node start. |
| return_progress_ratio | Proporsi langkah pada fase pulang yang mengurangi jarak lurus ke start. Fase pulang dicatat setelah total jarak mencapai 2.500 m. Nilai mendekati 1 berarti arah pulang lebih konsisten; lihat penjelasan dan contoh pada Bagian 9.2.1. |
| closing_action_available | Bernilai True bila selama evaluasi pernah tersedia edge legal langsung menuju start yang akan menghasilkan total jarak 4.500–5.500 m. Ini menunjukkan kesempatan menutup loop, bukan bukti edge tersebut dipilih. |
| termination_reason | Alasan terminal setiap seed: success, over_distance, no_available_action, atau step_limit. |

Tabel evaluasi utama dan berkas `evaluation_metrics_{scenario}.csv` kini langsung menampilkan `closing_action_available` per seed. Nilai tersebut bersumber dari flag internal `closing_action_was_available`; bernilai True bila selama evaluasi tersedia edge legal langsung ke start dengan proyeksi total jarak 4.500–5.500 m. Nilai True berarti kesempatan menutup loop pernah ada, bukan bahwa edge itu pasti dipilih. Sementara itu, `closing_action_available_rate` serta rate semua tipe terminasi adalah **diagnosis training** yang tetap ditampilkan pada grafik diagnosis.

### 9.1.1 Rumus termination rate

Untuk setiap tipe terminasi, rate dihitung dengan rumus berikut.

    termination_rate(tipe) = jumlah episode dengan tipe tersebut ÷ jumlah seluruh episode

Contoh: bila 3.750 dari 12.500 episode training berakhir karena `over_distance`, maka termination rate `over_distance` adalah 3.750 ÷ 12.500 = 0,30 atau 30%. Pada evaluasi greedy, penyebutnya hanya lima karena satu evaluasi dilakukan untuk masing-masing seed.

### 9.1.2 Grafik yang ditampilkan notebook scenario

Workflow `run_scenario_experiment()` telah menjalankan `evaluate_greedy()` untuk setiap Q-table. Hasilnya langsung dimasukkan ke tabel evaluasi utama, termasuk `closing_action_available`; tidak diperlukan cell evaluasi tambahan. Selain tabel evaluasi, notebook menampilkan grafik training, diagnosis dan overlap pada section terpisah.

1. **Grafik training utama**: keberhasilan loop, reward, jarak, mean comfort, jumlah state Q-table, dan epsilon. Semuanya selain epsilon memakai rata-rata bergerak 50 episode.
2. **Grafik diagnosis training**: rata-rata jarak akhir ke start, return progress ratio, closing action available rate, rata-rata nilai absolut TD-error, dan lima termination rate. Seluruh panel memakai rata-rata bergerak 50 episode dari lima seed; termination rate ditempatkan pada panel yang sama, bukan sebagai gambar tersendiri.

Grafik diagnosis menggunakan data `training_history_{scenario}.csv`, sehingga menunjukkan perubahan selama training, bukan hanya angka akhir. Nilai kosong pada `return_progress_ratio` terjadi bila episode belum pernah mencapai fase kembali, yaitu 50% dari target (2.500 m); rata-rata hanya dihitung dari episode yang memasuki fase tersebut.

Tidak ada baseline Dijkstra. Perbandingan eksperimen hanya A vs B vs C, dengan lingkungan yang sama.

### 9.1.3 Cara membaca kelompok metrik evaluasi

Metrik evaluasi tidak memiliki peran yang sama. `is_loop` adalah keputusan keberhasilan utama untuk satu seed, sedangkan `success_rate_greedy` merangkum berapa dari lima seed yang berhasil. `total_distance_m` dan `absolute_distance_error_m` menjelaskan kedekatan jarak rute terhadap target 5 km, tetapi rute dengan galat kecil tetap gagal apabila tidak kembali ke node start.

`mean_comfort` menjelaskan karakter ruas yang dilalui rute; `total_reward` hanya menjadi indikator pendukung karena nilainya merupakan gabungan reward comfort, arah perjalanan, penalti revisit, dan reward atau penalti terminal. Oleh sebab itu, total reward tidak boleh dipakai sendirian untuk menyatakan sebuah rute lebih baik.

Tiga metrik berikut membantu mendiagnosis kegagalan pulang: `distance_to_start_at_end_m` menunjukkan seberapa jauh posisi akhir dari start, `return_progress_ratio` menunjukkan konsistensi arah pulang setelah fase pulang dimulai, dan `closing_action_available` menunjukkan apakah agen pernah memiliki kesempatan legal untuk langsung menutup loop. Ketiganya tetap metrik pendukung; rute hanya dinyatakan berhasil ketika `is_loop=True`.

`termination_reason` menjelaskan akhir episode. Contohnya, `over_distance` berarti total jarak telah melewati 5.500 m sebelum agen kembali valid ke start, sedangkan `no_available_action` berarti action mask tidak lagi menyediakan edge legal pada state tersebut.

### 9.2 Cara membaca mean_comfort

Nama kolom dipertahankan untuk kompatibilitas artefak. Pada reward langsung,
mean_comfort = sum(B_edge*panjang)/sum(panjang), tanpa batas rentang tetap.
Nilai lebih besar menunjukkan kontribusi preferensi H/S/W lebih positif menurut
aturan penelitian. Nilai 0 dapat berasal dari data kosong atau keseimbangan
kontribusi, bukan persepsi kenyamanan sedang. Ini bukan persentase dan tidak
mengukur keamanan aktual. Arsip sebelum direct_signed_20261103 memakai skala
0--1; jangan membandingkan angkanya langsung dengan versi baru.

### 9.2.1 Cara membaca return_progress_ratio

`return_progress_ratio` digunakan untuk menjawab pertanyaan: **setelah agen memasuki fase pulang, seberapa konsisten langkahnya benar-benar mendekati titik awal?** Metrik ini tidak mengukur kenyamanan maupun keberhasilan loop secara langsung. Metrik ini hanya membaca arah gerak relatif terhadap start.

    return_progress_ratio = return_progress_steps ÷ return_phase_steps

Data pembentuknya disimpan oleh environment pada setiap action sebagai berikut.

1. Sebelum action dijalankan, environment menghitung `distance_before`, yaitu jarak lurus dari node saat ini ke start.
2. Setelah action dijalankan, environment menghitung `distance_after`, yaitu jarak lurus dari node tujuan ke start.
3. Bila total jarak rute **setelah action** sudah minimal 2.500 m, action tersebut dihitung sebagai satu `return_phase_steps`.
4. Bila pada action tersebut `distance_after < distance_before`, action juga dihitung sebagai satu `return_progress_steps`.

Dengan demikian, pembilang menghitung jumlah langkah yang mendekati start dan penyebut menghitung seluruh langkah dalam fase pulang. Metrik ini menghitung **jumlah langkah**, bukan besar perubahan jaraknya. Sebuah langkah yang mendekat 2 m dan langkah yang mendekat 100 m sama-sama menambah pembilang satu kali.

Contoh: setelah total jarak mencapai 2.500 m, agen melakukan lima action dengan jarak lurus terhadap start berikut.

| Action fase pulang | `distance_before` | `distance_after` | Mendekati start? |
|---:|---:|---:|---|
| 1 | 500 m | 440 m | Ya |
| 2 | 440 m | 470 m | Tidak |
| 3 | 470 m | 400 m | Ya |
| 4 | 400 m | 410 m | Tidak |
| 5 | 410 m | 350 m | Ya |

Pada contoh tersebut, `return_phase_steps = 5` dan `return_progress_steps = 3`. Maka:

    return_progress_ratio = 3 ÷ 5 = 0,60

Nilai 0,60 berarti 60% action pada fase pulang bergerak mendekati start. Nilai 1,00 berarti seluruh action fase pulang mendekati start, sedangkan nilai 0,00 berarti tidak ada action fase pulang yang mendekati start. Bila episode berakhir sebelum total jarak mencapai 2.500 m, penyebutnya nol sehingga implementasi menyimpan nilai `NaN` atau kosong; nilai ini tidak diperlakukan sebagai nol saat rata-rata grafik dihitung.

Nilai tinggi belum tentu berarti loop valid. Agen dapat selalu bergerak mendekati start tetapi berhenti di node yang dekat dengan start, memilih edge yang salah, atau melewati batas jarak sebelum kembali tepat ke node awal. Karena itu `return_progress_ratio` harus dibaca bersama `is_loop`, `distance_to_start_at_end_m`, `closing_action_available`, dan `termination_reason`.

### 9.3 Peta interaktif

**make_route_map()** menampilkan satu rute representatif dari lima hasil evaluasi greedy (satu hasil untuk setiap seed), bukan dari episode training. Fungsi **select_representative_trial()** menentukan Q-table/seed yang dipakai dengan aturan berikut.

1. Bila ada satu atau lebih `is_loop=True`, pilih hanya dari kelompok loop valid: `absolute_distance_error_m` terkecil, kemudian `mean_comfort` tertinggi, lalu `return_progress_ratio` tertinggi.
2. Bila belum ada loop valid, pilih rute dengan `absolute_distance_error_m` terkecil, kemudian `distance_to_start_at_end_m` terkecil, lalu `mean_comfort` dan `return_progress_ratio` tertinggi. Urutan ini mencegah rute yang berhenti terlalu dini tetapi kebetulan dekat start terpilih sebagai peta. Dalam kondisi ini peta adalah alat diagnosis, bukan contoh rute final yang berhasil.

Notebook mencetak scenario, seed, nilai seluruh metrik utama, dan alasan pemilihan sebelum peta ditampilkan. Karena itu seed pada peta tidak selalu seed 0 dan pengguna dapat memverifikasi alasan rute tersebut dipilih. `revisit_count` tidak digunakan sebagai kriteria pemilihan peta. Peta memakai warna berbeda per kilometer dan memuat marker start KM 0, marker KM 1–5, serta marker finish terpisah.

Jika rute valid loop, marker finish digeser sedikit untuk tampilan agar tidak menumpuk marker start. Posisi logis finish tetap sama dengan start. Peta representatif bukan rata-rata lima seed; peta hanya alat inspeksi rute terbaik menurut aturan prioritas.

### 9.4 Status dan pembaruan hasil

Ringkasan angka di wiki diberi tanggal dan RESULT_GROUP. CSV pada grup terkait tetap sumber utama; angka arsip tidak menjadi hasil terbaru ketika konfigurasi reward, action mask, jumlah episode, atau epsilon berubah. Gunakan `evaluation_metrics_A.csv`, `evaluation_metrics_B.csv`, dan `evaluation_metrics_C.csv` yang dihasilkan dari **satu konfigurasi yang sama** sebagai sumber tabel BAB IV. Untuk eksperimen sensitivitas episode, jangan mencampurkan CSV epsilon dinamis dengan CSV pada folder `sensitivitas_epsilon_tetap_50000_episode_<jumlah>_<scenario>`.

Sebelum membuat tabel perbandingan A--C, pastikan ketiga scenario sudah dijalankan ulang dengan konfigurasi final dan lima seed yang sama. Ringkasan BAB IV hanya memakai `is_loop`, `total_distance_m`, `absolute_distance_error_m`, `total_reward`, `mean_comfort`, `return_progress_ratio`, `distance_to_start_at_end_m`, `closing_action_available`, dan `termination_reason`; `revisit_count` tidak dipakai sebagai metrik evaluasi utama.

## 10. Aturan Modifikasi dan Konteks untuk AI

Saat membuat perubahan:

1. Ubah satu komponen eksperimen pada satu waktu, misalnya reward kembali atau jumlah progress bin.
2. Jangan mengubah reward/action mask bersamaan dengan definisi state jika ingin membandingkan A–C secara adil.
3. Setelah perubahan yang memengaruhi environment, reward, action, atau training, jalankan ulang seluruh A–C dengan lima seed yang sama.
4. Simpan hasil baru pada direktori berbeda atau beri nama konfigurasi agar CSV lama tidak tertimpa tanpa jejak.
5. Perbarui wiki ini jika parameter, rumus reward, action mask, metrik, atau status hasil berubah.
6. Jangan mengklaim sistem berhasil sebelum is_loop True muncul secara konsisten pada evaluasi greedy.
7. Jangan mengklaim comfort score sebagai pengalaman pelari yang tervalidasi tanpa validasi lapangan atau survei.

Ringkasan singkat: proyek menggunakan Q-Learning tabular dari scratch pada graf jalan kaki OSMnx MultiDiGraph terproyeksi meter. Target adalah loop 5 km plus toleransi 10%. Action adalah edge spesifik (next_node, key). State final yang diuji A sampai C berbeda pada informasi posisi, progres, dan arah kedatangan. Revisit tersedia mulai 50% target dengan maksimum dua kunjungan node; fase ini sama dengan awal reward arah pulang. Semua aturan bersama berada di rute_lari_core.py; analisis berada di analisa.ipynb; eksperimen dipisahkan pada scenario_A.ipynb sampai scenario_C.ipynb. Hasil yang dilaporkan selalu berasal dari evaluasi greedy per seed.


## 11. Verifikasi implementasi

Per 3 November verifikasi.ipynb disesuaikan dan 32 cell kode (49 cell total)
dijalankan ulang pada kernel Python bersih. Semua lima poin sesuai expected:

1. Dua episode sintetis MultiDiGraph melalui train_step, tiga langkah OSM lokal,
   hitungan manual angka tetap, next Q legal nonnol, terminal tanpa bootstrap.
2. State A/B/C, progres/reset/previous_node, mask fresh/revisit/closing, key paralel,
   penolakan action ilegal, greedy/eksplorasi legal serta whitelist access.
3. CRS/koordinat/geometri/panjang dan akumulasi; 21.374 edge snapshot, 21.300 action
   legal setelah 74 edge access ditolak. Bukan semua edge dijadikan action.
4. Sukses inklusif 4.500/5.500, overshoot, buntu sebelum/sesudah langkah, 220 langkah
   serta prioritas terminal. Tidak ada early_return atau penalti gagal ganda.
5. Nilai literal H/S/W bertanda, gabungan, akses, fase, revisit, terminal serta jumlah
   komponen. Uji stres 100 km tetap membantah jaminan reward global, bukan rute nyata.

Expected independen dari fungsi reward yang diuji; toleransi numerik kecil. Manual
OSM pertama: residential/paving_stones/4 m memberi B=1, access permissive,
L=157,32164137901165 m, R=0,9*L/100=1,415894772411105 dan Q baru
0,15*R=0,212384215861666. Snapshot berubah memerlukan tinjauan acuan manual.

Seluruh komponen dicatat saat dihitung pada core, tidak dihitung ulang khusus
untuk tampilan. Tidak ada QValueUpdater/framework baru. Kelulusan hanya bukti
kasus yang ditulis, bukan jaminan bebas bug, konvergensi, sifat Markov atau
validasi lapangan. Review pengguna terhadap seluruh kasus tidak dianggap selesai
otomatis. Tidak menjalankan training penelitian, unduhan atau menulis ulang GraphML.

## 12. Kesepakatan verifikasi, validasi, dan katalog rute

Rencana rinci dan status implementasi: [Verifikasi, validasi, dan katalog](docs/VERIFIKASI_VALIDASI_DAN_KATALOG.md).

- Hitung manual Q tetap dipakai pada beberapa kasus representatif; tidak seluruh
  episode. Verifikasi aturan internal berbeda dari evaluasi A--C dan percobaan lapangan.
- Validasi lapangan direncanakan menggunakan Huawei Watch Fit 3/Huawei Health.
  Strava tidak diperlukan. Rute yang diuji dipilih dari hasil berhasil; tidak ada
  kewajiban semua state menghasilkan rute untuk dicoba. GPS pembanding, bukan kebenaran mutlak.
- Tidak tumpang tindih bukan syarat mutlak; aturan revisit yang aktif dipertahankan.
  GPX/navigasi dan aplikasi belum dibuat; rencana ekspor menunggu pemeriksaan rute/akses.
- Pembimbing menyarankan katalog rute: generate/evaluasi/seleksi secara offline,
  simpan kandidat, lalu tampilkan peta/informasinya pada UI. Tidak perlu training
  ketika pengguna membuka aplikasi atau mendukung titik awal bebas.
- Practical implications: membantu perencanaan rute lokal, memberi pertimbangan
  representasi state, dan memperlihatkan keterbatasan OSM dari pengamatan nyata.
  Katalog mendukung pemanfaatan; inti penelitian tetap reward dan pengaruh state.
- Kandidat rujukan aplikasi Q-Learning ada pada referensi.md; belum otomatis masuk
  daftar pustaka naskah. Mayoritas paper mengevaluasi performa, bukan bukti unit test/manual Bellman.


## Pengukuran overlap dalam satu rute (3 November 2026)

Riwayat tahap awal: overlap dihitung terpisah atas 60 rute evaluasi tersimpan.
Keputusan lanjutan pengguna menyederhanakan menjadi satu kolom overlap_ratio dan
meminta pencatatan tiap episode. Implementasi aktif sudah mencatatnya pada core
serta section grafik terpisah; lihat bagian Pencatatan overlap selama training.
Angka di bawah tetap hasil postprocessing grup reward_direct_20261103.

Identitas ruas berdasarkan geometri tanpa membedakan arah; ruas paralel berbeda
geometri tetap terpisah, persimpangan satu titik tidak dihitung. Panjang memakai
edge.length agar konsisten dengan jarak lama. Pada 60 rute ini union geometri
memastikan tidak ada overlap parsial tambahan. Tanpa geometry memakai garis node,
sesuai representasi graf. Data lain dengan overlap parsial perlu perluasan metode.

Semua 43 loop valid overlap, rentang 5,94--26,43%. Rata-rata B/C: dinamis
75K 17,28%/15,67%; dinamis 150K 18,57%/19,21%; horizon total 75K
19,41%/10,90%; horizon total 150K 20,19%/15,89%. Semua B/C lima loop valid.
A hanya dua/satu loop pada horizon, jadi tidak dibandingkan rate overlap saja.

B horizon seed 0 (75K/150K identik): panjang 4.915,66 m, ruas unik 3.616,22 m,
pengulangan 1.299,45 m/26,43%, 12 lintasan ulang, 14 revisit node.
Seluruh pengulangan contoh ini reverse; unique_edge_ratio terarah tetap 1,00.
B terbaik rata-rata galat/skor belum tentu terbaik overlap. C horizon total 75K
paling rendah overlap di B/C: 505,78 m/10,90%, tetapi galat 365,27 m/skor 0,9149.
Belum ada ambang overlap, perubahan pemilihan katalog, reward atau aturan revisit.

Laporan: docs/temp/analisis_reward_direct_20261103/OVERLAP.md, CSV per seed/
ringkasan/ruas berulang, grafik dan peta contoh berwarna merah. Sembilan kasus
kecil dan identitas jarak lulus; 228 berkas hasil mentah/GraphML tetap. Browser
peta contoh: 33 ruas fisik unik, 12 ruas berulang, toggle lulus tanpa error JS;
screenshot diperiksa. Menghitung hanya evaluasi akhir, bukan jutaan episode.


## Pencatatan overlap selama training (3 November 2026)

Definisi aktif yang disepakati pengguna adalah hitungan lintasan ruas:
overlap_ratio = (N_total - N_unik) / N_total. N_total adalah jumlah lintasan edge,
N_unik adalah jumlah ruas fisik unik tanpa membedakan arah. Panjang dalam meter
tidak menjadi bobot. Satu ruas dilalui tiga kali berarti dua lintasan ulang.
Geometri ter-normalisasi menjadi identitas ruas; paralel berbeda geometri tetap
terpisah. Identitas dipersiapkan sekali pada build_actions. Tanpa lintasan, nilai
NaN/null; hanya satu kolom overlap_ratio (0--1) disimpan tiap episode/evaluasi/JSON.

Grafik overlap tetap section tersendiri, tetapi hanya SATU PANEL untuk SELURUH
EPISODE, tanpa pemisahan atau penyaringan berhasil/gagal. Kurva persen memakai
jendela 50 episode dan rata-rata observasi antar-seed. Section 3.3 notebook A--C
juga memakai seluruh seed evaluasi; agregat bernama mean_overlap_ratio.
Metadata basis=physical_road_traversal_count dengan rumus hitungan, bukan panjang.
Reward, mask (revisit >=2.500 m), state, epsilon, seed dan pemilihan peta tetap.

Target training A--C sekarang reward_direct_overlap_count_20261103. Pengguna sudah
memiliki hasil pada reward_direct_overlap_20261103 yang berbasis meter, sehingga
folder itu dipertahankan. Jangan mencampur persentase berbasis meter dan hitungan.
Hasil reward_direct_20261103 tetap arsip tanpa pencatatan overlap tiap episode.
Muat ulang notebook dan jalankan cell muat graf untuk memperbarui RESULT_GROUP
sebelum training. Uji titik tetap memakai overwrite training terbaru melalui core
bersama, tanpa unduhan ulang bila hanya training diulang. Koordinat tetap.

Pengujian lulus: 180 episode sintetis A--C/dua seed menghasilkan Q-table dan semua
metrik selain overlap identik terhadap versi sebelumnya; 60 rute arsip cocok
hitungan lintasan audit independen. Contoh lima lintasan/empat ruas unik menghasilkan
20%, meskipun ruas ulang 1.500 m dari total 5.000 m (metode meter akan 30%).
Grafik diuji tanpa kolom is_loop, satu panel, rata-rata semua observasi. Alur simpan/
baca/tampil A/B/C satu seed dan label arsip meter lulus. Verifikasi kernel bersih
49 cell/32 code lulus; gambar diperiksa visual. 290 berkas hasil lama serta graf,
analisa dan dependensi tidak diubah. Tidak ada training penelitian/unduhan baru.


### Identitas ruas untuk overlap dan asal fungsi Shapely

Perhitungan aktif hanya menggunakan jumlah lintasan: `(N_total - N_unik) / N_total`.
Geometri dipakai untuk mengenali ruas yang sama, bukan untuk memberi bobot meter.
`physical_road_id` adalah identitas pengamatan pada EdgeAction; identitas action
Q-Learning tetap `(next_node, key)`. Perbedaan ini penting pada MultiDiGraph.

Alur implementasi:

1. `build_actions()` membentuk action legal dan mengisi `action.physical_road_id`
   lewat `_physical_road_identity()`, sekali saat action dibentuk.
2. Jika geometri tersedia, identitasnya `geometry.normalize().wkb`.
   `normalize()` adalah method Shapely yang menata koordinat secara konsisten;
   `.wkb` adalah properti (tanpa tanda kurung) yang menghasilkan `bytes`, yaitu
   representasi Well-Known Binary. Ini representasi bentuk, bukan ID way OSM.
3. Geometri garis yang sama dengan urutan terbalik menghasilkan identitas sama
   setelah normalisasi. Dua edge paralel dengan geometri berbeda tetap berbeda.
   Key berbeda dengan geometri persis sama digabung sebagai satu ruas untuk
   metrik overlap; keduanya tetap action berbeda untuk agen.
4. Bila atribut geometry tidak tersedia, kode mencoba garis lurus
   antar-koordinat node. Jika tidak ada geometri valid/koordinat pada graf uji,
   fallback adalah `(min(u,v), max(u,v), str(key))`. Pada dua edge yang sama-sama
   tidak menyimpan geometry dan memiliki endpoint sama, fallback garis lurus
   dapat menyamakan identitasnya meskipun key berbeda. Pembedaan bergantung pada
   representasi geometri yang tersedia; tidak menggunakan buffer atau kedekatan.
5. Setelah episode selesai, `route_metrics()` memasukkan seluruh physical_road_id
   pada `environment.path_actions` ke set. Ukuran set menjadi N_unik; panjang
   path_actions menjadi N_total. Tanpa lintasan menghasilkan NaN/null.
6. Metrik dikumpulkan ke history setiap episode; CSV history ditulis ketika
   eksperimen menyimpan hasil. Evaluasi greedy akhir memakai route_metrics yang
   sama. Grafik adalah satu panel seluruh episode, rata-rata jendela 50 episode
   antar-seed, tanpa pemisahan berhasil/gagal. Metadata menyatakan basis hitungan.

Contoh dari snapshot utama: pasangan node 5575519685 -> 1720976331 memiliki
key 0 sepanjang 64,51 m dengan dua titik koordinat (garis node karena geometry
absen), dan key 1 sepanjang 203,12 m dengan 15 titik koordinat. Identitasnya
berbeda karena geometri berbeda; perbedaan panjang bukan syarat identitasnya.

Pada Jalan Dukuh Kupang Timur XX, edge (1720906005, 1720906028, 0) memiliki
identitas WKB sepanjang 73 byte. Identitas arah balik cocok. Nilainya dapat
diperiksa pada graf utama dengan:

```python
geometry = G.edges[1720906005, 1720906028, 0]["geometry"]
print(geometry)
print(geometry.normalize())
print(geometry.normalize().wkb)        # bytes yang dipakai sebagai identitas
print(geometry.normalize().wkb.hex())  # tampilan hex dari nilai yang sama
```

Untuk rute B horizon 50K total 150K seed 0 pada arsip reward_direct_20261103:
45 lintasan, 33 ruas fisik unik, sehingga metrik hitungan = 12/45 = 26,67%.
Angka 26,43% pada laporan OVERLAP.md lama adalah rasio berbasis meter. Jangan
menyamakan kedua definisi atau mengubah makna kolom arsip secara diam-diam.

Shapely sudah tercantum sebagai dependensi pada pyproject.toml sejak setup uv
(commit 9fd76a0, 9 Oktober 2026); versi yang diperiksa 2.2.0. Tidak ada instalasi
paket baru atau perubahan lockfile untuk fitur overlap. Library ini sudah
menyediakan LineString, normalize dan WKB yang dipakai di atas.
Rujukan teknis: [normalisasi Shapely](https://shapely.readthedocs.io/en/stable/reference/shapely.normalize.html)
dan [representasi WKB](https://shapely.readthedocs.io/en/stable/reference/shapely.to_wkb.html).

Pengguna memilih menjalankan Scenario B terlebih dahulu sebagai referensi pada
reward_direct_overlap_count_20261103. Hasil training tersebut belum dianalisis
pada sinkronisasi penjelasan ini. Tidak ada perubahan kode atau training baru.


## Pengamatan B dinamis 75K: reward lama, langsung -1 dan -3 (3 November 2026)

Pengguna sudah menjalankan B dinamis 75K pada reward_revisit_3_overlap_count_20261103.
375.000 history lengkap, lima seed; sepuluh evaluasi -1/-3 diulang dan cocok
metrik serta node/action. Episode/seed/epsilon ketiga versi cocok persis.

| Versi | Loop 10K terakhir per seed, agregat lima seed | Loop greedy | Overlap greedy |
|---|---:|---:|---:|
| surface_width_3m_20261102: netral 0,50, revisit -8 | 0,116% | 0/5 | Tidak dihitung pada audit ini |
| reward_direct_overlap_count_20261103: revisit -1 | 66,19% | 5/5 | 12,98% |
| reward_revisit_3_overlap_count_20261103: revisit -3 | 51,66% | 5/5 | 6,70% |

Reward lama/banyak faktor berubah: revisit -8 ke -1/-3, arah 0,40 ke 0,60,
bonus 80 ke 100, pemetaan/rumus reward ruas. Jangan menyimpulkan penghapusan
netral 0,50 sendiri penyebab peningkatan. Versi lama greedy tidak pernah punya
closing action; kedua baru 5/5 pernah tersedia dan berhasil. -1 ke -3 hanya
mengubah penalti: tradeoff training loop turun 14,53 poin tetapi overlap greedy
turun 6,28 poin; galat greedy rata-rata turun 399,63 ke 351,03 m.
B dinamis 150K -3 juga memiliki artefak tetapi belum ditinjau dalam audit ini.
Tidak mengubah kode/notebook/hasil mentah, training atau unduhan.
Laporan: docs/temp/analisis_B75_perbandingan_reward_20261103/ANALISIS.md.



## Pengamatan B dinamis 75K dan 150K, penalti -3 (3 November 2026)

Dua durasi -3 selesai lima seed. Dibanding -1 pada durasi/seed/epsilon sama:

| Episode | Loop greedy -1/-3 | Overlap greedy -1 -> -3 | Loop 10K akhir -1 -> -3 |
|---|---:|---:|---:|
| 75K | 5/5 dan 5/5 | 12,98% -> 6,70% | 66,19% -> 51,66% |
| 150K | 5/5 dan 5/5 | 15,35% -> 6,94% | 81,55% -> 78,77% |

Seluruh sepuluh pasangan seed/durasi menurun overlap-nya. -3 sudah berpengaruh
cukup besar secara deskriptif; tidak menyimpulkan optimalitas atau signifikansi.
150K -3 mean galat 296,65 m (lama -1 340,90 m), skor ruas 0,9172 (lama 0,9247).
Peta 150K -3 seed 0: 4.808,07 m, overlap 2/47=4,26%, node revisit 5. Dua ruas
berulang bernama Dukuh Kupang Barat XVI/XVII; belum terbukti wajib atau minimal.
Sepuluh evaluasi 150K direproduksi; metrik/path cocok. Audit 75K sebelumnya cocok.
Saran -5 hanya eksperimen lanjutan bila diinginkan, belum diterapkan; core tetap -3.
Tidak mengubah kode/notebook/hasil mentah atau menjalankan training/unduhan.
Laporan: docs/temp/analisis_B_dinamis_revisit3_20261103/ANALISIS.md.



## Kemiripan seed B dinamis 75K -3 (3 November 2026)

Urutan edge diperiksa: hanya seed 1/2 identik (4.604,73 m, overlap 4,65%, 43
langkah); seed 3 berbeda (5.117,60 m, 3,77%, 53 langkah). Seed 0 juga berbeda
meskipun panjang dekat. Q-table 1/2 berbeda (17.116/17.213 state); nilai Q action
terpilih berbeda pada 42/43 langkah tetapi action terbaik sama, tanpa seri Q
terbaik pada seluruh 43 langkah keduanya. Evaluasi greedy tidak mengeksplorasi.
Seed berbeda bukan tujuan keragaman antar-rute; revisit mengatur satu episode.
Versi -3 memiliki empat urutan unik/5 loop, -1 tiga/5 loop (seed 2/3/4 identik),
versi lama netral lima urutan berbeda tetapi 0/5 loop. Bukan bukti optimalitas atau
konvergensi global. Core/reward/mask/evaluasi tetap; tidak ada training/unduhan.
Laporan: docs/temp/analisis_kemiripan_seed_B75_20261103/ANALISIS.md.



## Reward, epsilon dan state: pembanding terbaru 75K -3 (3 November 2026)

C dinamis 75K dan B horizon 50K total 75K sudah tersedia. Pada reward -3 sama:
B dinamis loop 5/5, galat 351,03 m, overlap 6,70%; B horizon loop 5/5,
galat 195,68 m, overlap 7,33%; C dinamis loop 5/5, galat 290,92 m, overlap
4,74%. Seluruh 15 evaluasi direproduksi, metrik/path cocok. Ini hasil lokal lima
seed, bukan superioritas umum atau signifikansi. Training 10K akhir masing-masing
51,66%/77,58%/52,95%, tetapi epsilon B horizon lebih rendah saat pengukuran.
Rekomendasi pembahasan: perbandingan A/B/C tetap inti rumusan masalah state;
dua epsilon tetap berguna sebagai konfigurasi pendukung walau loop sudah 5/5.
B sukses tidak membuat C redundan. Insentif reward lama-baru berubah bersama;
jangan menyebut penghapusan netral 0,50 sebagai penyebab tunggal. Rancangan,
core, notebook dan hasil mentah tidak diubah; tanpa training/unduhan baru.
Laporan: docs/temp/analisis_reward_epsilon_state_20261103/ANALISIS.md.



## Seluruh empat konfigurasi B penalti -3 selesai (3 November 2026)

Grup reward_revisit_3_overlap_count_20261103: 20 training/2.250.000 episode,
semua 20 greedy valid. Dinamis 75K/150K overlap 6,70%/6,94%; horizon 50K total
75K/150K 7,33%/8,12%. Pembanding -1 berturut-turut 12,98/15,35/15,05/17,43%.
Training loop 10K akhir -3: 51,66/78,77/77,58/82,20%. Seluruh parameter metadata
selain penalti/pemilihan peta cocok, seed/episode/epsilon antarversi cocok persis.
Lima evaluasi horizon total 150K direproduksi, metrik/path cocok; konfigurasi
lain sudah direproduksi sebelumnya. Saran -5 sebagai eksperimen lanjutan tetap
belum diterapkan. Core masih -3. Hasil hanya lokal lima seed/start penelitian.
Peta horizon150K memilih seed 1 overlap 12,24%; seed 3 hanya 1,96%, karena peta
dipilih menurut galat jarak, bukan overlap. Jangan menyamakan peta dengan mean.
Laporan: docs/temp/analisis_B_empat_konfigurasi_revisit3_20261103/ANALISIS.md.
Tidak mengubah kode/notebook/hasil mentah atau menjalankan training/unduhan.

## Audit awal B/C penalti -5, sebelum konfigurasi C terakhir selesai (3 November 2026)

B lengkap empat konfigurasi; C lengkap tiga. C horizon 50K total 150K belum punya
metadata/history/evaluasi akhir (saat laporan disimpan 4/5 rute seed ada).
35 training/3.750.000 history, 30/35 greedy valid; seluruh 35 direproduksi dengan
metrik/path cocok dan overlap geometri diverifikasi, 140 berkas sumber tetap.

| Konfigurasi | Loop B/C | Overlap B/C |
|---|---:|---:|
| Dinamis 75K | 1/5 dan 4/5 | 6,92% / 4,13% |
| Dinamis 150K | 5/5 dan 5/5 | 5,24% / 3,07% |
| Horizon 50K total 75K | 5/5 dan 5/5 | 3,37% / 3,69% |
| Horizon 50K total 150K | B 5/5; C belum final | B 5,58%; C belum final |

Overlap mean seluruh seed, termasuk gagal; jangan menyebut overlap rendah pada
rute gagal sebagai keberhasilan. B dinamis75 gagal empat over_distance; C dinamis75
satu buntu. Semua gagal tidak pernah punya closing action. -5 dibanding -3
mengurangi overlap tiga konfigurasi B tetapi menurunkan greedy B dinamis75 dari
5/5 ke 1/5 dan C dinamis75 dari 5/5 ke 4/5. Jangan menaikkan penalti lagi dulu.
C horizon75 seed3 adalah kandidat: 4.860,94 m, overlap0%, galat139,06m, revisit1;
belum validasi lapangan. C dinamis150 menggunakan sekitar2,2x Q-state B, overlap
lebih kecil dan galat hampir sama. Dua epsilon dan state tetap pembanding relevan.
Tidak mengubah kode/notebook/hasil mentah atau menjalankan training/unduhan.
Laporan: docs/temp/analisis_BC_revisit5_20261103/ANALISIS.md.


## Audit lengkap B/C penalti -5 (3 November 2026)

Kini delapan konfigurasi B/C lengkap: 40 training/4.500.000 episode, 35/40 greedy
valid (B16/20, C19/20). Seluruh 40 direproduksi; metrik/path cocok dan overlap
geometri independen cocok. Seed/episode/epsilon/parameter B-C konsisten; 160
berkas sumber tetap. Audit awal tujuh konfigurasi tetap riwayat.

| Konfigurasi | Loop B/C | Overlap B/C | Galat B/C |
|---|---:|---:|---:|
| Dinamis75K | 1/5 dan 4/5 | 6,92% / 4,13% | 473,55 / 287,57 m |
| Dinamis150K | 5/5 dan 5/5 | 5,24% / 3,07% | 302,74 / 304,64 m |
| Horizon50K total75K | 5/5 dan 5/5 | 3,37% / 3,69% | 357,69 / 301,80 m |
| Horizon50K total150K | 5/5 dan 5/5 | 5,58% / 3,16% | 212,43 / 344,99 m |

Mean seluruh lima seed, termasuk gagal. Kegagalan hanya dinamis75: B empat
over_distance, C satu buntu, semua tidak pernah punya closing action. Dibanding
-3, -5 menekan overlap tiga konfigurasi B tetapi menurunkan loop dinamis75.
Jangan menaikkan penalti lagi dulu. Dua epsilon dan perbandingan state masih
berguna; tidak ada konfigurasi unggul semua ukuran. C dinamis150 Q-state sekitar
2,2x B; ini bukan pengukuran rasio RAM/waktu. Semua angka deskriptif lima seed.
Ada lima loop overlap0%; kandidat C horizon75 seed3 4.860,94m/galat139,06m,
node revisit1. Periksa peta/lapangan sebelum katalog. Tidak ada validasi lapangan.
Laporan terbaru: docs/temp/analisis_BC_revisit5_lengkap_20261103/ANALISIS.md.
Tanpa perubahan kode/notebook/hasil mentah, training penelitian atau unduhan.


## Pembaruan parameter -10 dan tiga worker (3 November 2026)

Permintaan terbaru pengguna: penalti revisit -10, MAX_WORKERS=3 di notebook A--C,
grup reward_revisit_10_overlap_count_20261103. Hasil -5/-3 tetap tersimpan dan
bukan hasil parameter baru. Core default max_workers=1 tetap untuk kompatibilitas;
uji titik satu seed tetap satu proses. Seluruh konfigurasi episode/epsilon/seed,
mask, bobot dan komponen reward lain tetap. Perubahan worker hanya eksekusi,
bukan variasi algoritma Q-Learning. Tidak menjalankan training penelitian baru.

Verifikasi pada kernel bersih: 32 cell lulus. Expected contoh revisit -10 dan
total -8,40 ditulis literal. Uji Jupyter lima seed, 1 vs 3 worker, menghasilkan
Q/history/metrik/rute identik serta metadata workers=3/revisit_penalty=-10.
Bukti uji: docs/temp/verifikasi_revisit10_workers3_20261103/.


## Audit lengkap A–C penalti -10 (3 November 2026)

12 konfigurasi/60 training/6.750.000 episode lengkap. Seluruh60 evaluasi Q-table
cocok metrik/path, overlap geometri independen cocok, metadata -10/3worker,
seed/episode/epsilon/artefak diperiksa. 240 berkas sumber tetap. Greedy25/60 valid:
A3/20, B11/20, C11/20. Selesai training berbeda dari keberhasilan evaluasi.

| Konfigurasi | Loop A/B/C | Overlap A/B/C |
|---|---:|---:|
| Dinamis75K | 0/5, 0/5, 2/5 | 5,12%, 5,46%, 4,67% |
| Dinamis150K | 1/5, 4/5, 3/5 | 3,31%, 0,82%, 0,86% |
| Horizon50K total75K | 0/5, 2/5, 3/5 | 4,17%, 0,71%, 0,74% |
| Horizon50K total150K | 2/5, 5/5, 3/5 | 1,43%, 2,42%, 1,13% |

Overlap mean seluruh lima seed termasuk gagal. B/C turun35/40 pada -5 ke22/40
pada -10; menekan overlap dengan biaya keberhasilan. Satu-satunya5/5 adalah B
horizon150K (galat252,25m, overlap2,42%, skor0,9339). Kegagalan32 over_distance,
3 buntu, semuanya tidak pernah punya closing action legal. Sebelas gagal punya
overlap0%, jadi overlap tidak menggantikan syarat loop. Sembilan valid overlap0%.
C horizon75 seed4 kandidat4.913,09m/galat86,91m/overlap0%; B horizon150 seed1
5.092,78m/galat92,78m/overlap3,28%. Belum validasi lapangan atau pilihan final.
Rekomendasi jangan naikkan penalti lagi; simpan -10 untuk sensitivitas. Kode tetap
-10/3worker, tanpa perubahan otomatis. Parameter reward final A–C harus sama.
Laporan: docs/temp/analisis_ABC_revisit10_20261103/ANALISIS.md.
Tanpa perubahan kode/notebook/hasil mentah, training penelitian atau unduhan.

## Audit sinkronisasi uji titik start (3 November 2026)

uji_titik_start.ipynb sudah memakai core bersama: reward -10/mask/Q/epsilon/
overlap count. Default B150K/horizon50K, satu seed acak dicatat dan satu proses;
ini sengaja berbeda dari lima seed/tiga worker A--C. Kode notebook/koordinat tidak
diubah. Hasil uji terakhir yang tersimpan saat audit masih penalti -1, sehingga
perlu training ulang untuk hasil parameter terbaru; bukan kode yang tertinggal.

Uji cell asli dengan graf sintetis/folder sementara lulus: force download/no-cache
arguments, preview Highway/Surface/Access, metadata -10/seed/worker/overlap, display,
retraining tanpa unduh, overwrite training saja, penolakan koordinat lama serta
invalidasi hasil setelah unduh baru. 2.583 berkas penelitian tetap. Tidak ada
unduhan nyata atau training penelitian, hanya enam episode per uji singkat.
Audit: docs/temp/audit_uji_start_sync_20261103/AUDIT.md.


## Koneksi Overpass uji titik (3 November 2026)

Atas permintaan pengguna, pengaturan server alternatif di-revert. Notebook
kembali memanggil core.load_or_download_graph() langsung tanpa OVERPASS_URL,
perubahan ox.settings.overpass_url atau User-Agent khusus. Server mengikuti
bawaan OSMnx (https://overpass-api.de/api pada versi terpasang). Muat ulang
notebook dari disk dan restart kernel sebelum menjalankan ulang dari awal.

Force download/use_cache=False, pembatalan konteks saat gagal, koordinat/radius,
reward dan konfigurasi training tetap. Core, notebook A--C dan hasil penelitian
tidak diubah. Sumber cell koneksi kembali sama dengan sebelum percobaan endpoint
alternatif; sintaks seluruh cell diperiksa. Tidak menguji unduhan jaringan atau
menjalankan training. Probe/kontrol koneksi sebelumnya tetap riwayat pada
docs/temp/audit_overpass_connection_20261103/AUDIT.md; bukan bukti layanan pulih.

## Uji titik: tiga seed acak (3 November 2026)

Atas permintaan pengguna untuk memeriksa rute yang selalu sama, notebook uji titik
kini menjalankan tiga training mandiri per batch. RANDOM_SEEDS=None membuat tiga
seed acak berbeda melalui SystemRandom.sample(range(2**32), 3), dicetak/disimpan.
Tuple tiga integer berbeda boleh diisi untuk mengulang. Default B/150.000 episode
PER SEED/horizon50.000; total450.000 episode. MAX_WORKERS=3 memakai core spawn
bersama, bisa diisi1 untuk berurutan. A--C tetap lima seed0--4 tanpa perubahan.

Graf/titik/reward/mask/state/Q/epsilon tetap sama antar-seed. Training memakai G
memori, tidak mengunduh atau memuat ulang graf. Folder training/ dibersihkan SEKALI
per batch, lalu menampung ketiga Q-table, JSON rute, CSV metrik/grafik gabungan,
dan peta_scenario_{scenario}_seed_{seed}.html. Metadata titik memuat semua seed dan
nama peta. Cell hasil membaca hasil tersimpan, menampilkan SEMUA peta per seed;
peta perwakilan core tetap disimpan tetapi tidak dipakai sebagai satu-satunya
peta uji. perbandingan_rute_seed.csv memberi kelompok_rute berdasarkan urutan
tepat (from_node,next_node,key). Kelompok sama berarti urutan identik; jumlah
unik mencakup rute gagal. Ini bukan metrik persentase kemiripan geografis.

Dua batch sintetis @3seed x6episode diuji memakai cell asli dan3 worker spawn:
metadata/Q/JSON/peta per seed lengkap, hasil tanpa training, grup sama/berbeda,
overwrite training saja, konfigurasi/titik lama ditolak, training ulang tanpa
HTTP. Core dan notebook A--C cocok hash;2.584 file hasil penelitian tetap utuh.
Belum menjalankan training penuh tiga seed atau unduhan jaringan; kelulusan uji
ini bukan hasil variasi rute pada titik pengguna atau bukti konvergensi.
Audit: docs/temp/audit_uji_tiga_seed_20261103/AUDIT.md.

## Diagnosis service dan atribut kosong (3 November 2026)

Pengguna mencoba HIGHWAY_OTHER_SCORE=-2. Metadata uji tiga seed1279940429,
2839352981,2590398777 mencatat -2; ketiganya loop valid tetapi melewati tiga edge
way432851197 sepanjang637,15m. Q-table tersimpan pada keputusan masuk service
seed1279940429: Q(service)=35,1552; residential terbaik25,5148. Ini estimasi hasil
belajar, bukan bukti optimalitas. Replay memakai pemetaan metadata -2 cocok reward
akhir seluruh seed. Kontribusi ruas service -6,3715, arah +2,5214, gabungan -3,8501;
akses/revisit/terminal pada ketiga edge nol. Bonus sukses +100 pada akhir rute.

Detail penting yang perlu dipertahankan dalam pembahasan: add_comfort_scores
memakai np.clip(gabungan,-1,1). Highway -2 dengan surface/width kosong memberi
raw -1,10 tetapi skor akhir -1. Memberi skor -1 juga untuk atribut kosong tidak
menurunkan skor way tersebut lagi; uji counterfactual di memori membuktikannya.
Jangan menyarankan menurunkan skor lebih jauh tanpa mempertimbangkan clipping.
Data legal22.058edge: highway kosong0, surface kosong7.460, width tidak valid/
kosong7.856. Data kosong bukan bukti bahaya jalan; penalti ketidaklengkapan akan
mempengaruhi banyak alternatif. Tidak menerapkan penalti baru atau mengubah kode.

Saat audit, core di disk memiliki HIGHWAY_OTHER_SCORE=-1 dan hash berbeda dari
training -2; jangan menganggap file aktif identik konfigurasi hasil tersimpan.
Seluruh hasil/graf tetap. Tidak menjalankan training/unduhan. Audit rinci:
docs/temp/diagnosis_service_missing_20261103/audit.json.

## Comfort score tanpa pembatasan (3 November 2026)

Permintaan pengguna diterapkan: add_comfort_scores menyimpan float(gabungan)
langsung tanpa np.clip. Formula dan bobot H/S/W tetap0,55/0,30/0,15; parameter
pemetaan termasuk HIGHWAY_OTHER_SCORE tidak diubah oleh agent. Pengguna akan
mencoba nilai highway sendiri. Tidak menerapkan penalti untuk atribut kosong.

Rentang kini mengikuti nilai komponen, tidak dipaksa -1..1. Skor -1,10/-1,55
atau +1,55 diteruskan apa adanya ke action/reward dan mean_comfort. Nama API dan
atribut legacy tetap. Metadata baru reward_scheme=direct_signed_unclipped_20261103,
comfort_score_range=null (tidak ada batas tetap), comfort_score_clipped=false,
comfort_score_policy=weighted_sum_without_clipping. Metadata/hasil lama tetap.

analisa.ipynb memeriksa rumus gabungan alih-alih batas tetap; histogram interval
0,10 mengikuti min/max data termasuk kasus semua skor sama. Peta memakai kategori
ujung terbuka agar skor di luar rentang lama tidak salah label. Deskripsi dan
tooltip notebook A--C/uji/verifikasi disinkronkan. Hanya cell kode skor/distribusi/
peta analisis dan label pratinjau uji berubah; konfigurasi/koordinat/seed/worker/
reward lain/mask/Q/unduhan tetap. Output pada cell kode yang diedit dibersihkan.

Uji terkontrol: nilai di bawah -1 dan di atas +1, propagasi ke reward, metadata,
histogram dan kategori peta lulus. Regresi60episode sintetis A--C/dua seed pada
nilai default menghasilkan Q/history identik sebelum/sesudah. Satu eksperimen
sintetis tiga episode memeriksa metadata; tidak ada training panjang/unduhan.
Graf serta semua hasil tersimpan tetap (lihat audit). Hasil training lama tidak
dihitung ulang otomatis. Untuk uji titik, simpan perubahan core lalu jalankan
cell training/hasil; reload core dan rescore G sudah otomatis, tanpa unduh ulang.
Perubahan source notebook/label perlu muat ulang dari disk. Verifikasi manual
masih memuat expected untuk nilai default; penyesuaian parameter eksperimen
memerlukan peninjauan angka manual, bukan menganggap contoh lama berlaku.
Audit: docs/temp/audit_comfort_unclipped_20261103/AUDIT.md.


## Checkpoint sebelum penalti data kosong (3 November 2026)

Baseline sebelum perubahan missing: gabungan reward ruas tanpa clipping,
metadata direct_signed_unclipped_20261103, uji titik tiga seed acak/tiga worker,
peta/JSON/Q-table per seed dan perbandingan urutan ruas. Core aktif sekarang
HIGHWAY_OTHER_SCORE=-1; missing highway/surface/width masih0. Pengguna menguji
nilai highway sendiri, jangan otomatis menetapkan -2 berdasarkan arsip. Hasil
uji terakhir memakai unclipped/highway-2/missing0 pada seed708740203/773171908/
1087794112; ketiganya loop valid. Hasil tersimpan/naskah TA tidak diubah.

Pengguna meminta commit baseline DAHULU, baru perubahan missing H/S/W ke-0,5.
Pada checkpoint ini penalti data kosong BELUM diterapkan. Tujuannya preferensi
terhadap kelengkapan informasi, bukan menyatakan data kosong berarti jalan
berbahaya. Catatan ini melengkapi riwayat sebelumnya tanpa menggantikannya.


## Penalti data kosong -0,5 setelah checkpoint (3 November 2026)

Baseline telah di-commit sebagai70b1a08 SEBELUM perubahan missing. Sesudahnya,
HIGHWAY_MISSING_SCORE, SURFACE_MISSING_SCORE dan WIDTH_MISSING_SCORE menjadi-0,5.
HIGHWAY_OTHER_SCORE tetap sesuai file sebelum perubahan (saat itu-1); pengguna
mengujinya sendiri. Kategori terisi yang tidak dikenal tetap OTHER; width kosong,
invalid, tidak positif atau gabungan memakai missing-0,5. Tidak ada blacklist
service/TPU atau perubahan access. Ini preferensi kelengkapan informasi, bukan
kesimpulan bahwa tag kosong berarti jalan berbahaya. Tujuannya percobaan;
belum membuktikan penurunan penggunaan service pada hasil training pengguna.

Formula/bobot tetap0,55/0,30/0,15 dan tanpa clipping. Contoh semua atribut kosong
memberi B=-0,5; service default-1 dengan surface/width kosong B=-0,775; highway-2
pada kondisi sama memberi B=-1,325. Reward ruas tetap B*panjang/100. Metadata baru
reward_scheme=direct_signed_unclipped_missing_05_20261103; pemetaan H/S/W merekam
missing-0,5. Reward akses/arah/revisit/terminal, state, mask, Q, episode/epsilon,
seed/worker dan koordinat tidak diubah. Core bersama menerapkan aturan ke semua
notebook. A--C memakai grup baru reward_missing_05_20261103 untuk melindungi arsip;
uji titik tetap menimpa batch training terbaru tanpa mengunduh ulang G.

Notebook verifikasi:32cell kode lulus pada kernel bersih, expected literal untuk
kasus kosong/invalid/gabungan disesuaikan, termasuk empat contoh atribut parsial.
Pemeriksaan tambahan: missing semua memberi reward ruas-0,5 per100m dan Q pertama
-0,075 (alpha0,15, bootstrap0); highway-2 memberi-1,325 tanpa clipping. Semua
parameter modul selain tiga konstanta missing identik sebelum/sesudah.2.599file
hasil/graf tetap utuh. Tidak menjalankan training panjang/unduhan. Output analisis
skor lama dibersihkan agar tidak menjadi bukti aturan baru; jalankan ulang analisis
untuk tampilan terbaru. Notebook verifikasi menyimpan output kernel yang lulus.

Perubahan missing ini BELUM di-commit (terpisah dari baseline sesuai urutan
permintaan). Untuk mencoba, muat ulang notebook dari disk dan jalankan konfigurasi
agar grup baru terbaca. Uji titik dengan G yang sudah dimuat cukup konfigurasi,
training dan hasil. Gunakan tuple tiga seed yang sama untuk membandingkan reward.
Audit: docs/temp/audit_missing_reward_20261103/AUDIT.md.


## Koreksi grup hasil B agar sama dengan A/C (3 November 2026)

Pengguna meminta menyamakan folder lalu akan training ulang. RESULT_GROUP pada
cell muat graf scenario_B.ipynb dikoreksi dari reward_revisit_10_overlap_count_20261103
ke reward_missing_05_20261103, sama dengan A/C. Empat cell training, empat cell
hasil dan ringkasan memakai variabel yang sama. Output/nomor eksekusi B dibersihkan
agar hasil dari folder lama tidak tampak sebagai hasil grup baru. Deskripsi aktif
A/B/C juga diperjelas karena sebelumnya masih menyebut grup -10 di beberapa bagian.
Core/reward/parameter/seed/worker/koordinat tetap; tidak memindah, menghapus atau
menyalin artefak training. Hasil B missing-0,5 yang terlanjur tersimpan di folder
lama tetap di sana. Pengguna akan menjalankan ulang B ke folder baru; agent tidak
melatih ulang. Sebelum training, muat ulang notebook dari disk dan WAJIB jalankan
cell muat graf/config agar variabel RESULT_GROUP pada kernel diperbarui; pastikan
output Grup hasil: reward_missing_05_20261103. A/C tidak perlu training ulang hanya
karena koreksi nama grup B. Penilaian Bab IV menyeluruh dilanjutkan setelah hasil
training yang hendak dipakai pengguna tersedia pada grup yang konsisten.


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


## Bahan revisi naskah Bab I sampai III pada 4 November 2026

Pemeriksaan naskah utama terhadap core aktif dan panduan kampus menghasilkan
docs/temp/revisi_bab_1_3_20261104/REVISI_BAB_1_3_TERBARU.docx; lampiran kode
PlantUML, sumber rumus, dan ZIP disimpan permanen di docs/assets/. Panduan berisi lokasi penggantian, alasan, teks siap
salin, tabel skor/akses/reward/konfigurasi/metrik, dan koreksi alat yang berulang.
Rumusan masalah dan tujuan tetap. Empat konfigurasi 75K/150K dinamis dan horizon
50K tetap menjadi acuan, dengan lima seed per konfigurasi pada A–C.

Dokumen mengikuti implementasi yang telah dilatih: missing -0,5, revisit -10,
skor langsung tanpa clipping, akses whitelist yes/permissive/kosong, arah 0,60,
sukses +100 dan kegagalan -50. Diskusi pelonggaran missing/revisit belum menjadi
keputusan perubahan; panduan memberi catatan untuk ditinjau sebelum disalin.
Bagian verifikasi dan penulisan ulang Bab IV belum disusun dalam paket ini.
Naskah TA utama, core, notebook, graf dan hasil training tidak diubah.


### Lokasi permanen lampiran naskah pada 4 November 2026

Atas permintaan pengguna, sumber diagram PlantUML, rumus, petunjuk dan ZIP
dipindahkan dari folder revisi sementara ke docs/assets/. Salinan hasil
ekstraksi ZIP yang identik digabung setelah pemeriksaan byte. Word panduan revisi
tetap di docs/temp/revisi_bab_1_3_20261104/. Word panduan dan naskah utama tidak
diubah; rujukan Word memakai nama berkas lampiran sehingga tetap sesuai.
Lampiran naskah berikutnya juga harus disimpan di docs/ di luar folder temp.


### Perapian aset bersama pada 4 November 2026

Aset lama di root docs/ dan lampiran terbaru kini disatukan di docs/assets/.
Folder docs/aset_naskah/ tidak digunakan lagi. Seluruh sumber PlantUML, SVG dan
rumus dipertahankan byte-nya; tidak menghapus diagram terdahulu. README folder
assets membedakan aset revisi terkini dan diagram terdahulu. Panduan visual
Bab II/III menunjuk lokasi baru. PDF panduan kampus, dokumen Word, notebook,
core, graf dan hasil eksperimen tetap. ZIP lampiran diperbarui agar petunjuknya
menunjuk folder baru. Word sementara tetap di docs/temp/.


## Bahan penyusunan Bab IV pada 4 November 2026

Atas permintaan pengguna, fokus penulisan beralih ke hasil dan pembahasan,
tanpa menyusun bagian verifikasi atau validasi. Naskah utama dibaca ulang;
struktur dipertahankan sejauh memungkinkan. Judul Rancangan Eksperimen kedua
diusulkan menjadi Hasil Pelatihan dan Evaluasi. Isi lama yang memakai hasil
dan konfigurasi terdahulu diganti melalui bahan Word sementara, bukan diedit
langsung pada TA.

Word: docs/temp/revisi_bab_4_20261104/REVISI_BAB_4_HASIL_DAN_PEMBAHASAN.docx.
Aset permanen: docs/assets/hasil_pembahasan/ (README, PNG/SVG, CSV/JSON,
buat_aset_hasil.py, dan ZIP). Draf memuat karakteristik graf, kelengkapan
atribut, aturan skor, empat konfigurasi, tabel seluruh lima seed A–C,
perbandingan state dan epsilon, pengulangan ruas, alasan berhenti, dua contoh
rute, pemanfaatan hasil, serta batas kesimpulan. Bahasa ditujukan kepada
pembaca laporan, bukan riwayat perubahan implementasi. Seluruh 32 halaman
Word dirender dan ditinjau; 60 baris tabel per seed dicocokkan ke CSV.

Sumber tunggal hasil utama: reward_missing_05_20261103, lengkap 60 training,
6.750.000 episode, dan 60 evaluasi tersimpan. Loop A/B/C: dinamis75K 0/0/1;
dinamis150K 0/3/1; tetap50K-total75K 0/2/5; tetap50K-total150K 2/4/5.
37 evaluasi gagal terdiri dari 29 melebihi jarak dan 8 tanpa pilihan ruas.
Seluruh rute gagal tidak pernah memiliki pilihan penutup loop legal pada
langkah yang dikunjungi; ini tidak berarti graf tidak mempunyai loop valid.
C tetap75K menghasilkan 5/5 loop, galat rata-rata 141,57 m dan pengulangan
1,15%, tetapi tidak dinyatakan optimal secara umum. B dinamis150K 3/5 lebih
tinggi daripada C 1/5. Tidak mengklaim C selalu unggul atau 50K optimal.

Grafik pelatihan merata-ratakan lima seed per episode lalu menggunakan
rata-rata bergerak 50 episode, ditampilkan tiap 500 episode. Tabel 10.000
episode terakhir memakai seluruh baris pada rentang itu. Pengulangan tetap
berbasis jumlah lintasan, mencakup seluruh episode. Sampel rute berhasil:
C tetap75K seed0, panjang 5.052,51 m, pengulangan 0%. Sampel gagal: A dinamis75K
seed1, panjang 4.985,77 m tetapi posisi akhir masih 2.886,66 m dari start.

Dokumen revisi sebelumnya belum tentu seluruhnya diterapkan pengguna;
pemeriksaan konsistensi antarbab ditunda sampai penyalinan selesai. Naskah TA
utama, core, notebook, graf, metadata dan hasil training tidak diubah.
Tidak menjalankan training, mengunduh peta, atau mengubah dependency proyek.
Kode aset dapat dijalankan ulang dengan uv melalui lingkungan proyek;
runtime plot sementara untuk penyusunan berada di /private/tmp saja.


## Notebook percobaan tanpa simplifikasi pada 4 November 2026

Pengguna meminta salinan sementara analisa.ipynb untuk inspeksi graf dengan
koordinat dan wilayah yang sama, tetapi simplify=False. Notebook tersedia di
docs/temp/analisa_tanpa_simplify.ipynb. Graf dan semua HTML/PNG percobaan memakai
docs/temp/analisa_tanpa_simplify_data/, terpisah dari snapshot utama. Core dan
analisa.ipynb tidak diubah. Aturan analisis atribut/skor tetap memakai core.
Notebook dapat mencari root proyek dari cwd kernel di dalam proyek; seluruh
output lama dibersihkan. Peta ringkas menambahkan overlay maks.1.000 node sekitar
start; cell akhir membaca graf utama hanya untuk perbandingan ringkas. Koordinat
input tetap, tetapi node terdekat dapat berbeda karena graf lebih rapat. Cache
HTTP OSM boleh digunakan; jika belum tersedia, OSMnx mengunduh. Data smoothness
dari cache snapshot tetap diberi penanda cakupan. Percobaan bukan eksperimen
training A–C dan tidak mengubah pilihan simplifikasi penelitian utama.

Pemeriksaan notebook percobaan: seluruh 22 cell kode dijalankan dari cache OSM
lokal dengan akses HTTP diblokir dan output diarahkan ke /private/tmp. Hasil
tanpa simplifikasi: 24.150 node, 53.538 edge, EPSG:32749, node start9620836306.
Seluruh peta/tabel/diagram berhasil dibuat. Hash core, analisa.ipynb, dan GraphML
utama cocok sebelum/sesudah. Notebook yang diserahkan tetap tanpa output lama;
pengguna menjalankannya sendiri. Tidak ada training atau unduhan jaringan baru.
