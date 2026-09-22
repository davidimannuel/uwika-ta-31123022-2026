# Aset Visual Bab II

Dokumen ini mencatat aset yang relevan untuk hasil revisi BAB II. Render berkas `.puml` secara mandiri sebelum dimasukkan ke dokumen Word.

| Bagian | Aset | Status | Berkas atau isi |
|---|---|---|---|
| 2.1 Reinforcement Learning | Gambar siklus agent--environment | Perlu | `rl_interaction.puml`; gunakan untuk mengganti caption gambar yang saat ini menampilkan *Reference source not found*. Nomor dan caption gambar ditentukan saat penyusunan laporan. Sumber: Diolah dari Sutton and Barto (2018). |
| 2.2 Algoritma Q-Learning | Rumus pembaruan Q-Learning | Pertahankan | Tulis sebagai persamaan Word: `Q(s,a) ← Q(s,a) + α[r + γ max Q(s',a') − Q(s,a)]`. Sumber: Watkins and Dayan (1992). |
| 2.2 Algoritma Q-Learning | Flowchart pelatihan per episode | Perlu bila gambar lama tidak akurat | `qlearning_training_flow.puml`. Nomor dan caption gambar ditentukan saat penyusunan laporan. Sumber: Diolah dari Watkins and Dayan (1992) dan Sutton and Barto (2018). |
| 2.3 OpenStreetMap | Tabel atribut OSM | Perlu | Tabel tiga baris: `highway` = klasifikasi/fungsi ruas; `surface` = material permukaan; `width` = lebar aktual ruas. Kolom tambahan: peran dalam comfort score. Sumber: OpenStreetMap Wiki contributors (2026a, 2026b, 2026c). |
| 2.4 Representasi graf | Gambar edge paralel MultiDiGraph | Perlu | `multidigraph_representation.puml`. Nomor dan caption gambar ditentukan saat penyusunan laporan. Sumber: Diolah dari OSMnx Developers (2026). |
| 2.5 Penelitian terdahulu | Tabel perbandingan penelitian | Perlu | Gunakan tabel empat penelitian yang telah disusun pada revisi Subbab 2.5. |

## Aset yang tidak diperlukan

- Tidak perlu gambar atau rumus baru pada BAB I.
- Tidak perlu gambar simplifikasi graf di BAB II; detail parameter `simplify=True` ditempatkan pada BAB III.
- Tidak perlu rumus Haversine, karena tidak digunakan oleh implementasi.
