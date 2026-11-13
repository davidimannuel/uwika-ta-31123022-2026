"""Buat ulang tabel persentase dari 12 salinan sumber terminasi.
Jalankan dengan Python3: python buat_tabel.py
Keluaran CSV ditulis di folder skrip ini; data sumber tidak diubah.
"""
from pathlib import Path
import csv
R=Path(__file__).resolve().parent
rows=[]
for label,n,suffix in [('Dinamis',150000,'dynamic-150000'),('Dinamis',300000,'dynamic-300000'),('Durasi tetap 100.000 episode',150000,'horizon-100000-total-150000'),('Durasi tetap 100.000 episode',300000,'horizon-100000-total-300000')]:
 row=[label,f'{n:,}'.replace(',','.')]
 for scenario in 'abc':
  source=R/'sumber_terminasi'/f'{scenario}-{suffix}'/'termination_training.csv'
  counts={r['termination_reason']:int(r['count']) for r in csv.DictReader(source.open())}
  assert sum(counts.values())==n*5
  row.append(f"{100*counts['success']/(n*5):.2f}".replace('.',','))
 rows.append(row)
with (R/'tabel_keberhasilan_seluruh_pelatihan.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['Pengaturan Epsilon','Total Episode per Seed','A (%)','B (%)','C (%)']);w.writerows(rows)
