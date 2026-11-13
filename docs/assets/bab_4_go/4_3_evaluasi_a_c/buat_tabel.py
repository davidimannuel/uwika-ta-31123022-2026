"""Buat ulang15CSV tabel dari12salinan hasil evaluasi dan metadata.
Jalankan: python buat_tabel.py
Tidak memerlukan paket proyek dan tidak mengubah sumber evaluasi.
"""
from pathlib import Path
import json,csv
R=Path(__file__).resolve().parent
suffixes=['dynamic-150000','dynamic-300000','horizon-100000-total-150000','horizon-100000-total-300000']
def num(v,d=2):return f'{float(v):,.{d}f}'.replace(',','_').replace('.',',').replace('_','.')
def save(name,header,rows):
 with (R/name).open('w',newline='') as f:
  w=csv.writer(f);w.writerow(header);w.writerows(rows)
labels={'over_distance':'Melebihi batas jarak','no_available_action':'Tidak ada pilihan ruas','success':'Berhasil loop','step_limit':'Batas langkah'}
for scenario in 'abc':
 summary=[]
 for suffix in suffixes:
  profile=scenario+'-'+suffix;source=R/'sumber'/profile
  meta=json.loads((source/'metadata.json').read_text());t=meta['config']['training'];rows=list(csv.DictReader((source/'evaluation.csv').open()));rows.sort(key=lambda r:int(r['seed']));assert len(rows)==5
  count=sum(x['is_loop']=='true' for x in rows)
  mean=lambda k:sum(float(x[k]) for x in rows)/5
  summary.append(['Dinamis' if t['epsilon_decay_episodes'] is None else 'Durasi tetap 100.000 episode',f"{t['episodes']:,}".replace(',','.'),str(count)+'/5\n('+str(count*20)+'%)',num(mean('absolute_distance_error_m')),num(mean('mean_comfort'),4),num(100*mean('overlap_ratio'))])
  detail=[[x['seed'],num(x['total_distance_m']),num(x['absolute_distance_error_m']),num(x['mean_comfort'],4),num(100*float(x['overlap_ratio'])),labels[x['termination_reason']]] for x in rows]
  save(profile+'_setiap_seed.csv',['Seed','Panjang Rute (m)','Galat Jarak (m)','Skor Karakter Ruas','Pengulangan Ruas (%)','Akhir Episode'],detail)
 save('ringkasan_evaluasi_skenario_'+scenario+'.csv',['Penurunan Epsilon','Episode per Seed','Berhasil','Rata-rata Galat (m)','Rata-rata Skor Ruas','Rata-rata Pengulangan (%)'],summary)
