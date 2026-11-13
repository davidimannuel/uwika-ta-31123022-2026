# Referensi Penulisan TA

Dokumen ini adalah daftar sumber yang telah digunakan atau direncanakan untuk digunakan dalam naskah TA. Setiap kali menambahkan sitasi baru ke BAB I--V, tambahkan pula entri sumbernya di sini agar daftar pustaka akhir dapat disinkronkan.

## Pemakaian sumber pada Bab III — 12 November 2026

Bab III memakai sumber teori dan definisi yang sudah ada pada Bab II: Watkins &
Dayan1992, Sutton & Barto2018, OpenStreetMap contributors n.d., dan OSM Wiki
n.d.-a/b/c/d/f. Alias a–g tetap global, jangan diurutkan ulang per bab. Entri yang
sama ada di docs/assets/bab_3_go/referensi_bab_3.txt; jangan digandakan pada daftar
pustaka. Parameter/bobot/reward dinyatakan keputusan desain penelitian, bukan
angka yang diklaim berasal dari referensi tersebut atau hasil optimasi.

Sumber implementasi dan konfigurasi dicatat pada manifest lampiran Bab III,
termasuk hash source Go/metadata, bukan sebagai jurnal baru. Tidak menambah teori
verifikasi/validasi atau menyatakan nilai konfigurasi paling optimal.

## Aturan pencatatan

- Gunakan satu entri untuk satu sumber; jangan menduplikasi sumber yang sama.
- Cantumkan sitasi dalam teks, format daftar pustaka, tautan sumber, dan bagian naskah yang menggunakan sumber tersebut.
- Format mengikuti contoh APA pada panduan UWIKA. Untuk sumber berbahasa Inggris, sitasi naratif menggunakan kata `and`; kutipan pertama dari karya tiga sampai lima penulis menuliskan seluruh nama, sedangkan kutipan berikutnya memakai `et al.`.
- Tanggal akses hanya dipakai pada sumber daring yang relevan, terutama halaman web atau laporan lembaga yang dapat diperbarui.

## Acuan sitasi Bab II yang disepakati — 11 November 2026

Word khusus Bab II berada di `docs/temp/revisi_bab_2_go_20261111/`.
Daftar sumber/penempatan permanen berada di `docs/assets/bab_2_go/`.
Bab II hanya membahas highway/surface/width/access sebagai tag penelitian;
barrier tidak dibahas dan dikeluarkan dari daftar sumber web aktif. Karena itu,
huruf sumber OpenStreetMap Wiki disusun ulang menjadi a–g pada entri aktif di
bawah. Susunan ini menggantikan a–h pada panduan gabungan terdahulu; sesuaikan
sitasi bab lain saat sumber yang sama dirujuk. Daftar pustaka lama di bagian
riwayat bukan acuan penanda terbaru.

Watkins–Dayan tetap sumber teori 2.2, dihapus hanya dari tabel penelitian
terdahulu. Tabel pada subbab 2.5 memuat Zhang/Loepp–Ziegler/Tegart/Boeing. Boeing tetap
referensi pemodelan; OSMnx Developers dipakai untuk Haversine, bukan klaim
bahwa implementasi Go menggunakan OSMnx. Patterson tetap bahan Bab III,
tidak ditambahkan ke Bab II. Penambahan sumber berikut tidak menyatakan
penulisan verifikasi/validasi sudah dikerjakan.

### Patterson, Neumann, White and White 2024

- **Sitasi pertama:** `(Patterson, Neumann, White, and White, 2024)`; berikutnya `(Patterson et al., 2024)`.
- **Pemakaian:** Bab III, rancangan perbandingan empiris, pencatatan kondisi eksperimen dan pengulangan beberapa seed; bukan dasar mengklaim lima seed menjamin stabilitas.
- **Daftar pustaka:** Patterson, A., Neumann, S., White, M., & White, A. (2024). Empirical design in reinforcement learning. *Journal of Machine Learning Research, 25*(318), 1–63. https://www.jmlr.org/papers/v25/23-0183.html
- **Sumber primer:** [JMLR](https://www.jmlr.org/papers/v25/23-0183.html).

## Referensi yang digunakan pada BAB I 1.1 Latar Belakang

### Garmin Indonesia 2025

- **Sitasi dalam teks:** `(Garmin Indonesia, 2025)`
- **Digunakan untuk:** konteks jumlah aktivitas lari yang dicatat pengguna Garmin di Indonesia pada 2025.
- **Daftar pustaka:** Garmin Indonesia. (2025, December 12). *Garmin Connect Data Report 2025: Masyarakat Indonesia tunjukkan tren positif menuju gaya hidup lebih aktif dan sehat*. Retrieved September 21, 2026, from https://www.garmin.co.id/news/press-release/news-2025-dec-year-review/
- **Tautan:** [Garmin Connect Data Report 2025 Indonesia](https://www.garmin.co.id/news/press-release/news-2025-dec-year-review/)
- **Catatan batasan:** data menggambarkan aktivitas yang direkam oleh pengguna Garmin, bukan seluruh populasi pelari Indonesia.

### Tegart Schuurman and Harden 2025

- **Sitasi pertama dalam teks:** `(Tegart, Schuurman, and Harden, 2025)`
- **Sitasi berikutnya:** `(Tegart et al., 2025)`
- **Digunakan untuk:** konteks runnability dan faktor lingkungan yang berkaitan dengan pengalaman berlari.
- **Daftar pustaka:** Tegart, A. D., Schuurman, N., & Harden, S. R. (2025). Runnability: A scoping review. *International Journal of Environmental Research and Public Health, 22*(1), 71. https://doi.org/10.3390/ijerph22010071
- **Tautan:** [Artikel akses terbuka](https://www.mdpi.com/1660-4601/22/1/71)
- **Catatan batasan:** sumber ini tidak memvalidasi comfort score penelitian dan tidak membahas kondisi Dukuh Kupang secara khusus.

### Loepp and Ziegler 2018

- **Sitasi dalam teks:** `(Loepp and Ziegler, 2018)`
- **Digunakan untuk:** argumen bahwa rekomendasi rute lari perlu dibangkitkan berdasarkan kebutuhan dan tujuan pelari, bukan hanya memilih rute yang sudah ada.
- **Daftar pustaka:** Loepp, B., & Ziegler, J. (2018, October). Recommending running routes: Framework and demonstrator. Paper presented at the 2nd Workshop on Recommendation in Complex Scenarios, Vancouver, Canada. Retrieved September 21, 2026, from https://interactivesystems.info/system/pdfs/858/original/ComplexRec-18-Final.pdf
- **Tautan:** [PDF artikel](https://interactivesystems.info/system/pdfs/858/original/ComplexRec-18-Final.pdf)

### Watkins and Dayan 1992

- **Sitasi dalam teks:** `(Watkins and Dayan, 1992)`
- **Digunakan untuk:** definisi Q-Learning sebagai metode model-free yang memperbarui nilai action berdasarkan reward dan estimasi nilai action berikutnya.
- **Daftar pustaka:** Watkins, C. J. C. H., & Dayan, P. (1992). Q-learning. *Machine Learning, 8*(3-4), 279-292. https://doi.org/10.1007/BF00992698
- **Tautan:** [Halaman artikel dan DOI](https://doi.org/10.1007/BF00992698)

### Zhang Li Peng and Liu 2015

- **Sitasi pertama dalam teks:** `(Zhang, Li, Peng, and Liu, 2015)`
- **Sitasi berikutnya:** `(Zhang et al., 2015)`
- **Digunakan untuk:** bukti bahwa Q-Learning pernah diterapkan pada perencanaan rute asal-tujuan di jaringan jalan perkotaan.
- **Daftar pustaka:** Zhang, X., Li, H., Peng, J., & Liu, W. (2015). A cooperative Q-learning path planning algorithm for origin-destination pairs in urban road networks. *Mathematical Problems in Engineering, 2015*, Article 146070. https://doi.org/10.1155/2015/146070
- **Tautan:** [Artikel akses terbuka](https://doi.org/10.1155/2015/146070)

## Referensi yang relevan untuk BAB II dan BAB III

### Sutton and Barto 2018

- **Sitasi dalam teks:** `(Sutton and Barto, 2018)`
- **Digunakan untuk:** konsep dasar Reinforcement Learning, komponen agent--environment--state--action--reward, kebijakan (*policy*), dan tujuan memaksimalkan *return* terdiskonto.
- **Daftar pustaka:** Sutton, R. S., & Barto, A. G. (2018). *Reinforcement learning: An introduction* (2nd ed.). The MIT Press.
- **Tautan:** [Halaman resmi buku The MIT Press](https://mitpress.mit.edu/9780262039246/reinforcement-learning/)

### Boeing 2017

- **Sitasi dalam teks:** `(Boeing, 2017)`
- **Digunakan untuk:** Bab II 2.4–2.5, referensi pemodelan jaringan jalan sebagai graf. Tidak menyatakan program Go memakai OSMnx, proyeksi, atau simplifikasi.
- **Daftar pustaka:** Boeing, G. (2017). OSMnx: New methods for acquiring, constructing, analyzing, and visualizing complex street networks. *Computers, Environment and Urban Systems, 65*, 126-139. https://doi.org/10.1016/j.compenvurbsys.2017.05.004
- **Tautan:** [Halaman artikel](https://doi.org/10.1016/j.compenvurbsys.2017.05.004)

### OSMnx Developers n.d.

- **Sitasi:** `(OSMnx Developers, n.d.)`.
- **Pemakaian aktif:** Bab II, rujukan Haversine/great_circle atau perbandingan dengan representasi OSMnx; OSMnx tidak dipakai oleh core Go.
- **Daftar pustaka:** OSMnx Developers. (n.d.). *User reference*. OSMnx documentation. Retrieved November 11, 2026, from https://osmnx.readthedocs.io/en/stable/user-reference.html
- **Sumber primer:** [Dokumentasi OSMnx](https://osmnx.readthedocs.io/en/stable/user-reference.html).

### OpenStreetMap contributors n.d.

- **Sitasi:** `(OpenStreetMap contributors, n.d.)`.
- **Digunakan untuk:** Bab II 2.3, data OpenStreetMap, lisensi ODbL dan atribusi.
- **Daftar pustaka:** OpenStreetMap contributors. (n.d.). *Copyright and license*. Retrieved November 11, 2026, from https://www.openstreetmap.org/copyright
- **Sumber primer:** [OpenStreetMap](https://www.openstreetmap.org/copyright).

### OpenStreetMap Wiki contributors n.d. — pasangan sitasi aktif Bab II

- **n.d.-a:** OpenStreetMap Wiki contributors. (n.d.-a). *Key: access*. OpenStreetMap Wiki. Retrieved November 11, 2026, from https://wiki.openstreetmap.org/wiki/Key:access
- **n.d.-b:** OpenStreetMap Wiki contributors. (n.d.-b). *Key: highway*. OpenStreetMap Wiki. Retrieved November 11, 2026, from https://wiki.openstreetmap.org/wiki/Key:highway
- **n.d.-c:** OpenStreetMap Wiki contributors. (n.d.-c). *Key: surface*. OpenStreetMap Wiki. Retrieved November 11, 2026, from https://wiki.openstreetmap.org/wiki/Key:surface
- **n.d.-d:** OpenStreetMap Wiki contributors. (n.d.-d). *Key: width*. OpenStreetMap Wiki. Retrieved November 11, 2026, from https://wiki.openstreetmap.org/wiki/Key:width
- **n.d.-e:** OpenStreetMap Wiki contributors. (n.d.-e). *Node*. OpenStreetMap Wiki. Retrieved November 11, 2026, from https://wiki.openstreetmap.org/wiki/Node
- **n.d.-f:** OpenStreetMap Wiki contributors. (n.d.-f). *Overpass API*. OpenStreetMap Wiki. Retrieved November 11, 2026, from https://wiki.openstreetmap.org/wiki/Overpass_API
- **n.d.-g:** OpenStreetMap Wiki contributors. (n.d.-g). *Way*. OpenStreetMap Wiki. Retrieved November 11, 2026, from https://wiki.openstreetmap.org/wiki/Way

**Pemakaian:** Bab II 2.3–2.4 untuk definisi data/tag/node/way/Overpass; Bab III untuk penerapan yang nanti dibahas. Definisi atribut tidak membuktikan keamanan aktual dan tidak menetapkan angka reward. Gunakan pasangan sitasi/huruf yang sama pada naskah dan daftar pustaka.

## Riwayat daftar pustaka draf BAB I–V — 26 September 2026

Daftar berikut telah disinkronkan dengan draf BAB IV--V pada 26 September 2026 dan dirapikan ke gaya APA. Hanya sumber yang digunakan atau direncanakan untuk disitasi pada naskah revisi yang dicantumkan. Sumber daring tanpa tahun publikasi menggunakan `n.d.`; sitasi di BAB II yang sebelumnya memakai `2026a--c` perlu diseragamkan menjadi `n.d.-a--c` saat dokumen utama direvisi.

- Boeing, G. (2017). OSMnx: New methods for acquiring, constructing, analyzing, and visualizing complex street networks. *Computers, Environment and Urban Systems, 65*, 126–139. https://doi.org/10.1016/j.compenvurbsys.2017.05.004
- Garmin Indonesia. (2025, December 12). *Garmin Connect Data Report 2025: Masyarakat Indonesia tunjukkan tren positif menuju gaya hidup lebih aktif dan sehat*. https://www.garmin.co.id/news/press-release/news-2025-dec-year-review/
- Loepp, B., & Ziegler, J. (2018). Recommending running routes: Framework and demonstrator. In *ComplexRec ’18: Proceedings of the 2nd Workshop on Recommendation in Complex Scenarios* (pp. 26–29). https://interactivesystems.info/system/pdfs/858/original/ComplexRec-18-Final.pdf
- OpenStreetMap contributors. (n.d.). *Copyright and license*. Retrieved September 26, 2026, from https://www.openstreetmap.org/copyright
- OpenStreetMap Wiki contributors. (n.d.-a). *Key: highway*. OpenStreetMap Wiki. Retrieved September 26, 2026, from https://wiki.openstreetmap.org/wiki/Key:highway
- OpenStreetMap Wiki contributors. (n.d.-b). *Key: surface*. OpenStreetMap Wiki. Retrieved September 26, 2026, from https://wiki.openstreetmap.org/wiki/Key:surface
- OpenStreetMap Wiki contributors. (n.d.-c). *Key: width*. OpenStreetMap Wiki. Retrieved September 26, 2026, from https://wiki.openstreetmap.org/wiki/Key:width
- OSMnx Developers. (2026). *OSMnx user reference* (Version 2.1.1). Retrieved September 26, 2026, from https://osmnx.readthedocs.io/en/stable/user-reference.html
- Sutton, R. S., & Barto, A. G. (2018). *Reinforcement learning: An introduction* (2nd ed.). The MIT Press.
- Tegart, A. D., Schuurman, N., & Harden, S. R. (2025). Runnability: A scoping review. *International Journal of Environmental Research and Public Health, 22*(1), Article 71. https://doi.org/10.3390/ijerph22010071
- Watkins, C. J. C. H., & Dayan, P. (1992). Q-learning. *Machine Learning, 8*(3–4), 279–292. https://doi.org/10.1007/BF00992698
- Zhang, X., Li, H., Peng, J., & Liu, W. (2015). A cooperative Q-learning path planning algorithm for origin-destination pairs in urban road networks. *Mathematical Problems in Engineering, 2015*, Article 146070. https://doi.org/10.1155/2015/146070

## Kandidat referensi verifikasi dan evaluasi Q-Learning (2 November 2026)

Sumber berikut dibahas sebagai bahan belajar dan kandidat sitasi, **belum otomatis
menjadi daftar pustaka final atau sudah disalin ke TA**. Periksa kembali rincian
bibliografi dan bagian yang akan dikutip sebelum memasukkannya ke naskah utama.
Tanggal pencatatan diskusi: 2 November 2026. Link yang mengarah ke dokumentasi/kode
adalah rujukan implementasi; tidak semuanya paper akademik.

Kesimpulan pembahasan: manual tracing beberapa Q-update tetap dipakai sebagai
bukti implementasi sendiri, dilengkapi pengujian state/mask/graf/terminasi/reward,
evaluasi greedy beberapa training seed, dan pemeriksaan lapangan. Paper yang
melaporkan performa tidak otomatis melakukan unit test atau manual Bellman.

### Enam bacaan awal yang paling relevan

| Sumber | Yang dapat dipelajari | Batas pemakaian |
|---|---|---|
| Boar (2022), chess endgames | Q-table, logging, eksperimen posisi awal, visualisasi solusi | Modifikasi dua pemain; jangan menyalin update lawan/minimax ke environment rute |
| Gymnasium, Taxi action masking | Mask pada eksplorasi, greedy dan max Q berikutnya | Tutorial kode; grafik training bukan validasi dunia nyata |
| OpenSpiel, tabular Q tests | Pengujian pada environment sederhana dengan hasil yang diketahui | Bukan bukti manual Bellman; contoh Blackjack pada test ditandai skip |
| Shi, Wang, dan Zhang (2023) | Perbandingan Q-learning grid dan kontribusi epsilon/inisialisasi | Kriteria konvergensi operasional paper bukan bukti universal |
| Pubben (2020), Snake | Variasi informasi state, training/evaluasi, pelaporan variasi hasil | Memakai MLP, bukan Q-table murni |
| Pina et al. (2021) | Evaluasi simulasi dan penerapan robot nyata | Tugas/representasi berbeda; keberhasilan transfer tidak membuktikan rute kita layak |

### Katalog sumber yang dibahas

1. **Boar, A.-I. (2022). Solving Chess Endgames Using Q Learning.** Skripsi sarjana,
   University of Groningen. Q-table varian dua pemain; tiga endgame, sejumlah
   posisi awal, win rate/jumlah langkah, artefak CSV/Q-table dan inspeksi GUI.
   [PDF](https://fse.studenttheses.ub.rug.nl/28405/1/Bachelor_s_Project_AI_Boar.pdf).
2. **Shi, Wang, dan Zhang (2023). Improved reinforcement learning path planning
   algorithm integrating prior knowledge.** PLOS ONE 18(5), e0284942. Perbandingan
   Q-learning grid, inisialisasi dan epsilon dinamis; beberapa pengulangan dan
   metrik langkah/panjang/waktu. [Artikel](https://pmc.ncbi.nlm.nih.gov/articles/PMC10159141/).
3. **Pubben, I. (2020). QVA-learning for playing the game of Snake.** Skripsi
   sarjana, University of Groningen. Informasi pengamatan, evaluasi setelah
   training, variasi hasil. MLP, bukan tabular; jumlah pengulangan pada metode
   dan beberapa tabel tidak seragam, sehingga perlu diperiksa saat disitasi.
   [PDF](https://fse.studenttheses.ub.rug.nl/22801/1/AI_BA_2020_IlsePubben.pdf).
4. **Gymnasium. Action Masking in the Taxi Environment.** Contoh resmi Q-table:
   action legal dipakai pada eksplorasi, greedy dan bootstrap. Perbandingan
   training return dengan/tanpa mask, bukan validasi lapangan.
   [Tutorial](https://gymnasium.farama.org/tutorials/training_agents/action_masking_taxi/).
5. **Google DeepMind OpenSpiel. Tabular Q-Learner tests.** Test aktif memakai
   permainan kecil dengan reward yang diketahui dan evaluasi setelah belajar;
   contoh Blackjack pada file di-skip. Jangan menyebutnya uji hitung manual.
   [Kode test](https://github.com/google-deepmind/open_spiel/blob/master/open_spiel/python/algorithms/tabular_qlearner_test.py).
6. **Pina et al. (2021). Overcoming Challenges of Applying Reinforcement Learning
   for Intelligent Vehicle Control.** Sensors 21(23), 7829. Simulasi navigasi,
   pengaruh kondisi/start-goal, dan penerapan Q-table pada robot fisik.
   [Artikel](https://pmc.ncbi.nlm.nih.gov/articles/PMC8659501/).
7. **Wang, Emmerich, dan Plaat (2018). Assessing the Potential of Classical
   Q-learning in General Game Playing.** Tic-Tac-Toe, Connect Four kecil dan Hex;
   strategi epsilon dan performa permainan. Jangan memakai uraian AlphaGo pada
   pengantar sebagai sumber DQN Go tanpa pemeriksaan sumber aslinya.
   [PDF](https://arxiv.org/pdf/1810.06078).
8. **Upadhyay, I. (2021). Analysis of Q-Learning Based Game Playing Agents for
   Abstract Board Games with Increasing State-Space Complexity.** Tesis Miami
   University. Tic-Tac-Toe, Nine Men's Morris, Mancala; teacher dan perbandingan
   kompetisi agen. [Repositori](https://etd.ohiolink.edu/acprod/odb_etd/etd/r/1501/10?p10_accession_num=miami1627681408588176).
9. **Dietterich, T. G. (2000). Hierarchical Reinforcement Learning with the MAXQ
   Value Function Decomposition.** JAIR 13, 227–303. Abstraksi/hierarki state dan
   evaluasi pada beberapa domain termasuk Taxi; metode MAXQ-Q bukan Q-table datar
   yang identik dengan penelitian ini. [PDF](https://www.cs.cmu.edu/afs/cs/project/jair/pub/volume13/dietterich00a.pdf).
10. **Boyan dan Littman. Packet Routing in Dynamically Changing Networks:
    A Reinforcement Learning Approach.** NIPS 6, konferensi 1993; tahun volume
    perlu diperiksa untuk format sitasi. Evaluasi delivery time terhadap routing
    pembanding; Q-routing meminimalkan biaya, bukan update reward maksimal yang
    langsung dapat disalin. [PDF](https://proceedings.neurips.cc/paper_files/paper/1993/file/4ea06fbc83cdd0a06020c35d50e1e89a-Paper.pdf).
11. **Abdulhai, Pringle, dan Karakoulas (2003). Reinforcement Learning for True
    Adaptive Traffic Signal Control.** Journal of Transportation Engineering
    129(3), 278–285. Evaluasi delay pada simulasi lalu lintas; menggunakan
    pendekatan aproksimasi CMAC, jangan diklaim sebagai Q-table murni.
    [PDF institusi](https://www.dcsc.tudelft.nl/~sc4081/2018/assign/pap/Reinforcement_Learning2.pdf).
12. **Mahadevan dan Connell (1991). Automatic Programming of Behavior-Based
    Robots Using Reinforcement Learning.** AAAI. Robot OBELIX/box pushing,
    pembandingan perilaku/modul; generalisasi tambahan digunakan. Versi jurnal
    diperluas tahun 1992 adalah entri berbeda.
    [PDF](https://cdn.aaai.org/AAAI/1991/AAAI91-120.pdf).
13. **Hara et al. (2011). Acquisition of a Gymnast-Like Robotic Giant-Swing Motion
    by Q-Learning and Improvement of the Repeatability.** Journal of Robotics
    and Mechatronics 23(1), 126–136. Simulasi dan robot nyata, reward/repeatability.
    Ringkasan sebelumnya berdasarkan abstrak penerbit; jangan menyimpulkan
    prosedur verifikasi rinci yang belum dibaca.
    [Penerbit](https://www.fujipress.jp/jrm/rb/robot002300010126/).
14. **Timóteo, Barbosa, dan Jesus (2026). Robotic Arm Control Using a Q-Learning
    Reinforcement Algorithm.** Robotics 15(3), 50. Q-table Tic-Tac-Toe, pembanding
    kebijakan dan pengukuran posisi robot; percobaan akhir lengan menunjuk sel,
    bukan bukti pick-and-place lengkap. [Penerbit](https://www.mdpi.com/2218-6581/15/3/50).
15. **Van Hasselt (2010). Double Q-learning.** NeurIPS. Contoh tabular kecil dan
    bias estimasi nilai vs performa tugas; varian update berbeda dari Q-learning
    standar. [PDF](https://proceedings.neurips.cc/paper/2010/file/091d584fced301b442654dd8c23b3fc9-Paper.pdf).
16. **Finnson dan Molnö (2019). Deep Reinforcement Learning for Snake.** KTH.
    Ringkasan berdasarkan abstrak repositori; PDF belum berhasil diakses dalam
    pembahasan sebelumnya. DQN, bukan tabular.
    [Dokumen](https://www.diva-portal.org/smash/get/diva2%3A1342302/FULLTEXT01.pdf).
17. **Sebastianelli et al. (2021). A deep Q-learning based approach applied to the
    snake game.** MED, 348–353. Ringkasan hanya abstrak penulis/repositori;
    detail unit test/verifikasi belum dipastikan.
    [Repositori](https://www.iris.unina.it/handle/11588/910625).
18. **Mnih et al. (2015). Human-level Control through Deep Reinforcement
    Learning.** Nature 518, 529–533. DQN Atari, protokol evaluasi dan pembanding;
    epsilon evaluasi paper tidak harus menjadi epsilon evaluasi TA ini.
    [PDF](https://storage.googleapis.com/deepmind-media/dqn/DQNNaturePaper.pdf).
19. **Van Hasselt, Guez, dan Silver (2016). Deep Reinforcement Learning with
    Double Q-learning.** AAAI. Bias Q dan performa Atari; Double DQN berbeda
    dari Q-table standar. [PDF](https://arxiv.org/pdf/1509.06461).
20. **Pratama dan Hermawan (2026). Implementasi Algoritma Q-Learning pada Game
    Edukasi Bahasa Inggris Lexicon Vault.** JATI 10(4). Abstrak menyebut Q-table
    dan black-box testing; full text belum dibaca, jangan mengklaim manual Bellman.
    [Jurnal](https://www.ejournal.itn.ac.id/jati/article/view/18555).
21. **Gymnasium. Solving FrozenLake with Tabular Q-learning.** Contoh reset
    Q-table, seed, analisis reward/langkah dan visualisasi policy. Rata-rata
    Q-table untuk ilustrasi tutorial bukan otomatis protokol evaluasi penelitian.
    [Tutorial](https://gymnasium.farama.org/v1.3.0/tutorials/training_agents/frozenlake_q_learning/).
22. **Gymnasium. Solving Blackjack with Tabular Q-learning.** State, TD-update
    dan bootstrap terminal. [Tutorial](https://gymnasium.farama.org/v1.3.0/tutorials/training_agents/blackjack_q_learning/).
23. **Hugging Face Deep RL Course, Unit 2 Hands-on.** Training Q-table terpisah
    dari evaluasi greedy, rata-rata/variasi dan seed. Gunakan pola evaluate_agent;
    jangan menyalin seluruh helper video tanpa pemeriksaan kondisi terminasi.
    [Materi](https://huggingface.co/learn/deep-rl-course/en/unit2/hands-on).
24. **Henderson et al. (2018). Deep Reinforcement Learning That Matters.** AAAI.
    Reproduksibilitas dan variasi seed; rujukan metodologi RL, bukan aplikasi
    Q-table yang sama. [Artikel](https://ojs.aaai.org/index.php/AAAI/article/view/11694).
25. **Agarwal et al. (2021). Deep Reinforcement Learning at the Edge of the
    Statistical Precipice.** NeurIPS. Ketidakpastian estimasi dari sedikit run
    dan pelaporan statistik; tidak membuktikan lima seed TA sudah cukup untuk
    semua klaim. [PDF](https://proceedings.neurips.cc/paper_files/paper/2021/file/f514cec81cb148559cf475e7426eed5e-Paper.pdf).
26. **Testing and Reinforcement Learning—A Structured Literature Review (2024).**
    IEEE QRS-C, DOI 10.1109/QRS-C63300.2024.00049. Ringkasan berdasarkan abstrak;
    membedakan pengujian sistem RL dari pemakaian RL untuk menguji perangkat lunak.
    Nama penulis/detail sitasi perlu dilengkapi sebelum dipakai dalam naskah.
    [IEEE](https://ieeexplore.ieee.org/document/10726989/).

### Catatan sumber untuk diskusi atribut OSM dan width

- Definisi [surface](https://wiki.openstreetmap.org/wiki/Key:surface) dan
  [width](https://wiki.openstreetmap.org/wiki/Key:width) diperiksa kembali pada
  2 November 2026. Width pada jalan kendaraan umumnya badan jalan, bukan trotoar.
  Aturan skor kelompok dan ambang 3 m tetap keputusan penelitian, bukan skor OSM.
- [Lampiran PP 16 Tahun 2021](https://peraturan.bpk.go.id/Download/244292/PP%20Nomor%2016%20Tahun%202021-dikompresi.pdf)
  sempat dibahas sebagai pembanding dimensi jalur pedestrian. **Bukan dasar untuk
  menyatakan badan jalan 3 m adalah standar nyaman/aman bagi pelari.** Pengguna
  memilih 3 m untuk mengurangi preferensi gang sempit.
- Definisi [access](https://wiki.openstreetmap.org/wiki/Key:access) digunakan dalam
  diskusi akses; whitelist penelitian (yes/permissive/kosong) tidak menerapkan
  seluruh hierarki izin OSM.
  Permissive tidak sama dengan keberadaan pagar tertutup.


### Penyelarasan sitasi OSM untuk revisi Bab I sampai III pada 4 November 2026

Sumber access https://wiki.openstreetmap.org/wiki/Key:access diperiksa untuk
uraian izin akses: yes diizinkan, permissive berdasarkan izin yang dapat dicabut,
serta perbedaan dengan no/private/destination. Tidak menyimpulkan pagar tertutup
dari permissive atau akses publik dari tag kosong. Whitelist penelitian tetap
aturan desain sederhana, bukan seluruh hierarki izin OSM.

Untuk empat entri penulis OpenStreetMap Wiki contributors tanpa tanggal,
panduan sementara mengusulkan urutan judul: n.d.-a Key access, n.d.-b Key highway,
n.d.-c Key surface, n.d.-d Key width. Sitasi dalam teks harus diperbarui bersama
entri referensi jika pengguna menyalin usulan ini. Entri copyright penulis
OpenStreetMap contributors tetap n.d. tanpa akhiran. Sumber dan format lengkap
ada pada docs/temp/revisi_bab_1_3_20261104/REVISI_BAB_1_3_TERBARU.docx.
Tidak mengubah sitasi atau daftar pustaka pada dokumen TA utama secara langsung.
