# Aset naskah tugas akhir

Folder permanen bersama untuk kode diagram, gambar, dan sumber rumus.
Word panduan revisi tetap di `docs/temp/`; PDF panduan kampus dan dokumen Word
lainnya tetap di `docs/`. Folder ini menggantikan `docs/aset_naskah/`.

## Aset revisi terkini

| Berkas | Penggunaan |
|---|---|
| [alur_penelitian.puml](alur_penelitian.puml) | Alur penelitian dengan empat konfigurasi pelatihan dan lima seed. |
| [alur_langkah_q_learning.puml](alur_langkah_q_learning.puml) | Satu langkah environment dan pembaruan Q, termasuk terminal dan buntu. |
| [penyaringan_aksi.puml](penyaringan_aksi.puml) | Penyaringan akses dan aturan perjalanan, pendamping opsional. |
| [rumus_revisi.tex](rumus_revisi.tex) | Sumber persamaan skor, reward, dan metrik. |
| [PETUNJUK.md](PETUNJUK.md) | Cara menggunakan diagram dan persamaan. |
| [LAMPIRAN_DIAGRAM_DAN_RUMUS.zip](LAMPIRAN_DIAGRAM_DAN_RUMUS.zip) | Paket lima berkas lampiran revisi terkini. |

## Ilustrasi dan diagram terdahulu yang dipertahankan

| Berkas | Penggunaan atau status |
|---|---|
| [rl_interaction.puml](rl_interaction.puml) | Siklus agen dan environment pada teori RL. |
| [qlearning_training_flow.puml](qlearning_training_flow.puml) | Diagram pelatihan Q-Learning umum. |
| [multidigraph_representation.puml](multidigraph_representation.puml) | Ilustrasi edge paralel pada MultiDiGraph. |
| [projected_multidigraph_illustration.puml](projected_multidigraph_illustration.puml) | Ilustrasi graf terproyeksi dan sumbu koordinat. |
| [running_loop_illustration.puml](running_loop_illustration.puml) | Ilustrasi rute loop. |
| [ilustrasi_jarak_lurus_node_awal.svg](ilustrasi_jarak_lurus_node_awal.svg) | Gambar jarak lurus terhadap titik awal. |
| [research_method_flow.puml](research_method_flow.puml) | Versi terdahulu, lihat alur_penelitian.puml untuk revisi terkini. |
| [research_method_overview.puml](research_method_overview.puml) | Ringkasan metode terdahulu, dipertahankan sebagai referensi. |
| [qlearning_environment_flow.puml](qlearning_environment_flow.puml) | Versi terdahulu, lihat alur_langkah_q_learning.puml untuk revisi terkini. |

Panduan penempatan: [Bab II](../ASET_VISUAL_BAB_II.md) dan
[Bab III](../ASET_VISUAL_BAB_III.md). Nomor gambar dan caption ditentukan di Word,
bukan ditulis permanen dalam kode diagram. Simpan hasil render berikutnya di
folder assets ini dengan nama sumber yang sama dan ekstensi SVG atau PNG.

Perapian folder tidak mengubah isi sumber PlantUML, SVG, atau LaTeX. Diagram
terdahulu belum otomatis disesuaikan dengan seluruh aturan eksperimen terbaru.


## Hasil dan pembahasan Bab IV

[Folder hasil_pembahasan](hasil_pembahasan/README.md) menyimpan gambar PNG/SVG,
data tabel, dan kode untuk hasil A–C pada grup reward_missing_05_20261103.
Word sementara berada di docs/temp/revisi_bab_4_20261104/.
[Paket ZIP](hasil_pembahasan/LAMPIRAN_HASIL_DAN_PEMBAHASAN.zip) memuat seluruh
lampiran hasil dan petunjuk penggunaannya. Tidak mencakup penulisan verifikasi
atau validasi.
