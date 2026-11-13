"""Bentuk tabel ringkasan evaluasi dari CSV hasil 12 konfigurasi tersimpan.

Tidak menjalankan pelatihan atau evaluasi ulang. Semua rata-rata pada sumber
mencakup kelima seed, termasuk hasil yang gagal.
"""
from pathlib import Path
import argparse
import csv

def angka(value, digit=2):
    return f'{float(value):,.{digit}f}'.replace(',', '_').replace('.', ',').replace('_', '.')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    here=Path(__file__).resolve().parent
    p.add_argument('--source',type=Path,default=here/'data_ringkasan_12_konfigurasi.csv')
    p.add_argument('--output',type=Path,default=here/'tabel_ringkasan_evaluasi_a_c.csv')
    args=p.parse_args()
    with args.source.open(encoding='utf-8-sig') as f:
        rows=list(csv.DictReader(f))
    profiles={r['profile']:r for r in rows}
    assert len(rows)==len(profiles)==12
    suffixes=['dynamic-150000','dynamic-300000','horizon-100000-total-150000','horizon-100000-total-300000']
    table=[]
    for suffix in suffixes:
        for scenario in 'ABC':
            r=profiles[scenario.lower()+'-'+suffix]
            n=int(r['loop_count']);denom=int(r['seed_count'])
            assert denom==5 and 0<=n<=denom
            assert abs(float(r['success_rate_greedy'])-n/denom)<1e-10
            table.append(['Dinamis' if r['decay_mode']=='dynamic' else 'Durasi tetap\n100.000 episode',angka(r['episodes'],0),scenario,f'{n}/{denom} ({20*n}%)',angka(r['mean_distance_error_m']),angka(r['mean_comfort'],4),angka(100*float(r['mean_overlap_ratio']))])
    with args.output.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f)
        w.writerow(['Penurunan Epsilon','Episode per Seed','Skenario','Berhasil','Galat Jarak (m)','Skor Ruas','Pengulangan Ruas (%)'])
        w.writerows(table)
    print('Tabel ditulis:',args.output)

if __name__=='__main__':main()
