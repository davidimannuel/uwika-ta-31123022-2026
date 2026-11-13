"""Buat tabel jumlah berhasil, total pengamatan dan persentase dari CSV sumber.
Jalankan: python buat_tabel_jumlah.py
"""
from pathlib import Path
import csv
R=Path(__file__).resolve().parent
def n(x):return f'{x:,}'.replace(',','.')
rows=[]
for label,ep,suffix in [('Dinamis',150000,'dynamic-150000'),('Dinamis',300000,'dynamic-300000'),('Durasi tetap 100.000 episode',150000,'horizon-100000-total-150000'),('Durasi tetap 100.000 episode',300000,'horizon-100000-total-300000')]:
 row=[label,n(ep),n(5*ep)]
 for c in 'abc':
  f=R/'sumber_terminasi'/f'{c}-{suffix}'/'termination_training.csv'
  counts={x['termination_reason']:int(x['count']) for x in csv.DictReader(f.open())}
  assert sum(counts.values())==5*ep
  percent=f"{100*counts['success']/(5*ep):.2f}".replace('.',',')
  row.append(n(counts['success'])+'\n('+percent+'%)')
 rows.append(row)
with (R/'tabel_keberhasilan_jumlah_dan_persentase.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['Penurunan Epsilon','Episode per Seed','Total Episode Lima Seed','A\nBerhasil (%)','B\nBerhasil (%)','C\nBerhasil (%)']);w.writerows(rows)
