"""Buat ulang gambar laporan dari CSV turunan; tidak menjalankan training."""
from pathlib import Path
import json,math
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
HERE=Path(__file__).resolve().parent
D=json.loads((HERE/'sumber_dan_ringkasan.json').read_text())
R=json.loads((HERE/'rute_evaluasi.json').read_text())
S=pd.read_csv(HERE/'ringkasan_profil.csv');C=pd.read_csv(HERE/'perkembangan_pelatihan.csv');E=pd.read_csv(HERE/'atribut_ruas_dan_skor.csv')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','axes.formatter.useoffset':False,'figure.dpi':150})
colors=['#2463a5','#d87716','#28804b','#8b4c9c'];styles=['-','--','-.',':'];labels=['Dinamis 150k','Dinamis 300k','Horizon 100k total 150k','Horizon 100k total 300k']
def save(fig,name):
 fig.savefig(HERE/f'{name}.png',dpi=220,bbox_inches='tight');fig.savefig(HERE/f'{name}.svg',bbox_inches='tight');plt.close(fig)
# Bentuk jalan berasal dari endpoint trace dan snapshot, tanpa peta daring.
source=Path(D['source_project'])/'workdirs/training/output/osm.json'
nodes={int(e['id']):(e['lon'],e['lat']) for e in json.loads(source.read_text())['elements'] if e['type']=='node'}
segments=[(nodes[int(u)],nodes[int(v)]) for u,v in zip(E['from'],E['to'])]
fig,ax=plt.subplots(figsize=(7,6));ax.add_collection(LineCollection(segments,colors='#a8adb4',linewidths=.3));ax.autoscale()
start=D['common']['start_node'];x,y=nodes[start];ax.scatter([x],[y],s=50,c='#b32624',zorder=5,label='Start penelitian');ax.legend(loc='upper center',bbox_to_anchor=(.5,-.15));ax.xaxis.set_major_locator(plt.MaxNLocator(3));ax.set(xlabel='Longitude',ylabel='Latitude');ax.set_aspect(1/math.cos(math.radians(y)));ax.text(.99,1.01,'Data © OpenStreetMap contributors',ha='right',transform=ax.transAxes,fontsize=11);save(fig,'jaringan_jalan')
fig,ax=plt.subplots(figsize=(7,3.4));ks=['highway','surface','width','access'];vs=[D['graph']['attributes'][k]['percent'] for k in ks]
b=ax.bar(ks,vs,color='#647d98',edgecolor='black',hatch='//');ax.bar_label(b,labels=[f'{v:.2f}%'.replace('.',',') for v in vs],padding=3);ax.set(ylim=(0,113),ylabel='Edge terisi (%)');ax.text(.99,.98,'Width: nilai valid dalam meter\nPenyebut: seluruh 58.020 edge terarah',ha='right',va='top',transform=ax.transAxes,fontsize=11);save(fig,'kelengkapan_atribut')
fig,ax=plt.subplots(figsize=(7,3.3));ax.hist(E['comfort_score'],bins=np.arange(-6,1.11,.2),color='#647d98',edgecolor='white');ax.set(xlabel='Skor karakter ruas',ylabel='Jumlah edge terarah');ax.axvline(0,color='black',ls='--',lw=1);ax.text(.03,.95,'Skor preferensi penelitian\nBukan persentase kenyamanan',va='top',transform=ax.transAxes,fontsize=11);save(fig,'distribusi_skor')
fig,ax=plt.subplots(figsize=(7.4,3.8));xx=np.arange(4);ww=.24
for j,st in enumerate('ABC'):
 rows=S[S.scenario==st];bars=ax.bar(xx+(j-1)*ww,rows.valid,width=ww,label=f'State {st}',color=colors[j],edgecolor='black',hatch=['','//','..'][j]);ax.bar_label(bars,padding=2)
ax.set_xticks(xx,['Dinamis\n150 ribu','Dinamis\n300 ribu','Horizon 100 ribu\nTotal 150 ribu','Horizon 100 ribu\nTotal 300 ribu']);ax.tick_params(axis='x',labelsize=10);ax.set(ylim=(0,6.3),ylabel='Evaluasi loop berhasil dari 5 seed',yticks=np.arange(6));ax.legend(ncol=3,loc='upper left');save(fig,'keberhasilan_evaluasi')
for metric,ylabel,name in [('is_loop','Keberhasilan training (%)','perkembangan_keberhasilan'),('overlap_ratio','Pengulangan segmen (%)','perkembangan_pengulangan')]:
 fig,axes=plt.subplots(3,1,figsize=(7.5,7.2),sharex=True)
 for ax,st in zip(axes,'ABC'):
  for j,pr in enumerate(S[S.scenario==st].profile):
   f=C[C.profile==pr];ax.plot(f.episode_end/1000,100*f[metric],color=colors[j],ls=styles[j],lw=1.2,label=labels[j])
  ax.set(title=f'State {st}');ax.grid(alpha=.2);ax.set_ylim(bottom=0)
 axes[-1].set_xlabel('Episode pelatihan (ribu)');handles,labs=axes[0].get_legend_handles_labels();fig.legend(handles,labs,loc='lower center',ncol=2,fontsize=11);fig.supylabel(ylabel,x=.02,fontsize=12);fig.subplots_adjust(hspace=.5,bottom=.20,left=.14);save(fig,name)
# Contoh rute dari evaluasi aktual, tanpa klaim validasi lapangan.
selected=[('b-horizon-100000-total-300000',1),('c-horizon-100000-total-300000',0)]
validselected=[]
EV=pd.read_csv(HERE/'evaluasi_per_seed.csv')
for profile,seed in selected:
 candidates=EV[(EV.profile==profile)&EV.is_loop]
 if candidates.empty:continue
 e=candidates.sort_values(['absolute_distance_error_m','seed']).iloc[0]
 validselected.append((profile,int(e.seed),e))
fig,axes=plt.subplots(1,len(validselected),figsize=(9,5.8),squeeze=False)
for ax,(pr,se,e) in zip(axes[0],validselected):
 rr=R[f'{pr}/seed-{se}'];seg=[[(float(t['from_lon']),float(t['from_lat'])),(float(t['to_lon']),float(t['to_lat']))] for t in rr if t['action_taken']=='true']
 xs=[p[0] for ss in seg for p in ss];ys=[p[1] for ss in seg for p in ss];ax.add_collection(LineCollection(segments,colors='#d5d8dc',linewidths=.4));ax.add_collection(LineCollection(seg,colors='#2463a5',linewidths=1.5));ax.scatter([x],[y],c='#b32624',s=30,zorder=5);ax.set_xlim(min(xs)-.001,max(xs)+.001);ax.set_ylim(min(ys)-.001,max(ys)+.001);ax.set_aspect(1/math.cos(math.radians(y)));ax.tick_params(labelsize=11)
 ax.set_title(f'State {e.scenario}, seed {se}\n{e.total_distance_m:,.2f} m; overlap {100*e.overlap_ratio:.2f}%'.replace(',','_').replace('.',',').replace('_','.'),fontsize=12)
 ax.set_xlabel('Longitude');ax.set_ylabel('Latitude')
for ax in axes[0]:
 ax.ticklabel_format(axis='both',style='plain',useOffset=False)
 ax.xaxis.set_major_locator(plt.MaxNLocator(2));ax.tick_params(axis='x',labelrotation=25)
fig.text(.5,.01,'Horizon 100 ribu, total 300 ribu episode | Data © OpenStreetMap contributors',ha='center',fontsize=11);fig.tight_layout(rect=(0,.04,1,1));save(fig,'contoh_rute_evaluasi')
print('Gambar PNG dan SVG selesai.')
# Ilustrasi jarak langsung memakai prefix rute aktual, bukan koordinat proyeksi.
pr='b-horizon-100000-total-300000';se=1
prefix=[t for t in R[f'{pr}/seed-{se}'] if t['action_taken']=='true'][:40]
pathseg=[[(float(t['from_lon']),float(t['from_lat'])),(float(t['to_lon']),float(t['to_lat']))] for t in prefix]
end=pathseg[-1][-1];phi1,phi2=map(math.radians,(y,end[1]));dl=math.radians(end[0]-x)
hav=math.sin((phi2-phi1)/2)**2+math.cos(phi1)*math.cos(phi2)*math.sin(dl/2)**2
straight=2*6371009*math.asin(math.sqrt(hav));travel=float(prefix[-1]['total_distance_m'])
fig,ax=plt.subplots(figsize=(6,6));ax.add_collection(LineCollection(segments,colors='#dedede',linewidths=.4));ax.add_collection(LineCollection(pathseg,colors='#2463a5',linewidths=1.8))
ax.plot([x,end[0]],[y,end[1]],color='#a52a2a',ls='--',lw=1.8,label=f'Jarak langsung Haversine {straight:.2f} m')
ax.scatter([x,end[0]],[y,end[1]],color=['#a52a2a','#2463a5'],s=35,zorder=5);ax.annotate('Start',(x,y),xytext=(4,5),textcoords='offset points');ax.annotate('Node langkah 40',end,xytext=(8,-15),textcoords='offset points')
xx=[p[0] for seg in pathseg for p in seg];yy=[p[1] for seg in pathseg for p in seg];ax.set_xlim(min(xx)-.001,max(xx)+.001);ax.set_ylim(min(yy)-.001,max(yy)+.001);ax.set_aspect(1/math.cos(phi1));ax.set(xlabel='Longitude',ylabel='Latitude');fig.text(.5,.96,f'Jarak langsung Haversine: {straight:,.2f} m',ha='center',fontsize=11);fig.text(.5,.01,f'Lintasan sampai langkah 40: {travel:.2f} m | Data © OpenStreetMap contributors',ha='center',fontsize=11);fig.tight_layout(rect=(0,.07,1,.92));ax.ticklabel_format(axis='both',style='plain',useOffset=False);ax.xaxis.set_major_locator(plt.MaxNLocator(2));ax.tick_params(axis='x',labelrotation=25);save(fig,'jarak_langsung_dan_lintasan')
(HERE/'contoh_jarak.json').write_text(json.dumps({'profile':pr,'seed':se,'step':40,'travel_distance_m':travel,'haversine_to_start_m':straight,'source':'evaluation-steps.csv'},indent=2))
