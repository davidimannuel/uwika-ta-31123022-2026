"""Membaca hasil tersimpan dan membuat tabel/gambar pembahasan, tanpa training."""
from pathlib import Path
import argparse, ast, collections, hashlib, json, re, typing
import xml.etree.ElementTree as ET
import __future__
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D

parser=argparse.ArgumentParser()
parser.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[3])
parser.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parent)
args=parser.parse_args();repo=args.repo_root.resolve();out=args.output_dir.resolve()
out.mkdir(parents=True,exist_ok=True)
group=repo/'hasil_bab_4/training_qlearning_5km/reward_missing_05_20261103'
graph_path=repo/'data_osm_5km/graf_jalan_kaki_5km.graphml'
configs=[('dinamis_75000','Dinamis 75.000',75000,None),
         ('dinamis_150000','Dinamis 150.000',150000,None),
         ('tetap_50000_episode_75000','Tetap 50K · 75.000',75000,50000),
         ('tetap_50000_episode_150000','Tetap 50K · 150.000',150000,50000)]
manifest={}
def record(p):
    stat=p.stat()
    manifest[str(p.relative_to(repo))]={'size':stat.st_size,'mtime_ns':stat.st_mtime_ns}
def save(fig,name):
    fig.savefig(out/(name+'.svg'),bbox_inches='tight')
    fig.savefig(out/(name+'.png'),dpi=300,bbox_inches='tight')
    plt.close(fig)
def number(n,d=2):
    return f'{n:,.{d}f}'.replace(',','X').replace('.',',').replace('X','.')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,
                     'axes.titlesize':11,'axes.labelsize':11,
                     'xtick.labelsize':10,'ytick.labelsize':10,
                     'svg.fonttype':'none','axes.spines.top':False,
                     'axes.spines.right':False})
colors={'A':'#333333','B':'#0072B2','C':'#D55E00'}
styles={'A':'-','B':'--','C':'-.'}

# Gunakan fungsi skor murni dari core agar aturan tidak disalin menjadi versi lain.
core_path=repo/'rute_lari_core.py';record(core_path)
tree=ast.parse(core_path.read_text())
functions={'is_missing','osm_values','parse_width_m','calculate_highway_score',
           'calculate_surface_score','width_score'}
nodes=[]
for node in tree.body:
    if isinstance(node,ast.Assign):
        names=[x.id for x in node.targets if isinstance(x,ast.Name)]
        if any(x.startswith(('HIGHWAY_','SURFACE_','WIDTH_','WEIGHT_')) for x in names):nodes.append(node)
    elif isinstance(node,ast.FunctionDef) and node.name in functions:nodes.append(node)
namespace={'np':np,'pd':pd,'re':re,'ast':ast,'Any':typing.Any}
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(core_path),'exec',
             flags=__future__.annotations.compiler_flag),namespace)
osm_values=namespace['osm_values'];parse_width=namespace['parse_width_m']
highway=namespace['calculate_highway_score'];surface=namespace['calculate_surface_score'];width=namespace['width_score']
assert namespace['HIGHWAY_MISSING_SCORE']==namespace['SURFACE_MISSING_SCORE']==namespace['WIDTH_MISSING_SCORE']==-.5
assert namespace['HIGHWAY_OTHER_SCORE']==-1

# Salinan graf dibaca langsung dari GraphML, tanpa unduhan atau penulisan ulang graf.
record(graph_path);root=ET.parse(graph_path).getroot();ns={'g':'http://graphml.graphdrawing.org/xmlns'}
keys={e.attrib['id']:e.attrib['attr.name'] for e in root.findall('g:key',ns)}
g=root.find('g:graph',ns)
def attrs(el):return {keys[d.attrib['key']]:d.text for d in el.findall('g:data',ns)}
meta_graph=attrs(g);assert meta_graph['crs']=='EPSG:32749'
xy={int(n.attrib['id']):(float(attrs(n)['x']),float(attrs(n)['y'])) for n in g.findall('g:node',ns)}
parent={u:u for u in xy}
def find(u):
    while parent[u]!=u:parent[u]=parent[parent[u]];u=parent[u]
    return u
edges={};rows=[];segments=[]
for e in g.findall('g:edge',ns):
    u,v,k=int(e.attrib['source']),int(e.attrib['target']),int(e.attrib['id'])
    d=attrs(e);edges[(u,v,k)]=d
    a,b=find(u),find(v)
    if a!=b:parent[a]=b
    access={part.strip() for value in osm_values(d.get('access')) for part in value.split(';') if part.strip()}
    legal=not access or access.issubset({'yes','permissive'})
    H,S,W=highway(d.get('highway')),surface(d.get('surface')),width(d.get('width'))
    score=.55*H+.30*S+.15*W
    if d.get('geometry'):
        text=d['geometry'];assert text.startswith('LINESTRING '),text[:50]
        points=[tuple(map(float,p.strip().split())) for p in text[text.index('(')+1:text.rindex(')')].split(',')]
    else:points=[xy[u],xy[v]]
    d['_points']=points;segments.append(points)
    raw_surface=d.get('surface');raw_width=d.get('width')
    surface_present=bool([part.strip() for value in osm_values(raw_surface) for part in value.split(';') if part.strip()])
    rows.append({'u':u,'v':v,'key':k,'highway':d.get('highway',''),
                 'surface':raw_surface or '', 'width_raw':raw_width or '',
                 'access':';'.join(sorted(access)) or 'Tidak tersedia',
                 'length_m':float(d['length']),'width_m':parse_width(raw_width),
                 'H':H,'S':S,'W':W,'score':score,'legal':legal,
                 'surface_present':surface_present,'highway_present':H!=-.5})
road=pd.DataFrame(rows)

all_eval=[];summary=[];curves=[];routes={};last_windows=[]
for ci,(prefix,label,total,decay) in enumerate(configs):
    for scenario in 'ABC':
        folder=group/f'{prefix}_{scenario}'
        mp=folder/f'metadata_eksperimen_{scenario}.json';record(mp)
        md=json.loads(mp.read_text())
        assert md['episodes']==total and md['seeds']==[0,1,2,3,4]
        assert md['epsilon_decay_episodes']==decay
        assert md['reward_scheme']=='direct_signed_unclipped_missing_05_20261103'
        assert md['revisit_penalty']==-10 and md['highway_scoring']['other_score']==-1
        assert all(md[k]['missing_score']==-.5 for k in ['highway_scoring','surface_scoring'])
        assert set(md['highway_scoring']['priority'])==namespace['HIGHWAY_PRIORITY']
        assert set(md['surface_scoring']['priority'])==namespace['SURFACE_PRIORITY']
        assert md['width_scoring']['priority_min_m']==namespace['WIDTH_PRIORITY_MIN_M']==3
        ep=folder/f'evaluation_metrics_{scenario}.csv';record(ep)
        ev=pd.read_csv(ep);assert len(ev)==5 and set(ev.seed)==set(range(5))
        ev['config']=ci;ev['config_label']=label;ev['folder']=folder.name
        ev['q_state_count']=0
        for col in ['service_m','missing_surface_m','missing_invalid_width_m','permissive_m','width_below_3_m']:
            ev[col]=0.0
        for ix,row in ev.iterrows():
            rp=folder/f'rute_evaluasi_scenario_{scenario}_seed_{row.seed}.json';record(rp)
            route=json.loads(rp.read_text());routes[(ci,scenario,int(row.seed))]=route
            assert route['metrics']['is_loop']==bool(row.is_loop)
            assert np.isclose(route['metrics']['total_distance_m'],row.total_distance_m)
            ev.loc[ix,'q_state_count']=route['metrics']['q_state_count']
            for a in route['path_actions']:
                d=edges[(a['from_node'],a['next_node'],a['key'])];length=float(d['length'])
                if 'service' in osm_values(d.get('highway')):ev.loc[ix,'service_m']+=length
                if surface(d.get('surface'))==-.5:ev.loc[ix,'missing_surface_m']+=length
                parsed_width=parse_width(d.get('width'))
                if parsed_width is None:ev.loc[ix,'missing_invalid_width_m']+=length
                elif parsed_width<3:ev.loc[ix,'width_below_3_m']+=length
                access={part.strip() for v in osm_values(d.get('access')) for part in v.split(';') if part.strip()}
                if 'permissive' in access:ev.loc[ix,'permissive_m']+=length
        all_eval.append(ev)
        s={'config':ci,'label':label,'scenario':scenario,'episodes':total,'decay':decay,
           'loops':int(ev.is_loop.sum()),'seed_count':5,'representative_seed':md['representative_seed']}
        for col in ['total_distance_m','absolute_distance_error_m','total_reward','mean_comfort',
                    'overlap_ratio','return_progress_ratio','distance_to_start_at_end_m','q_state_count']:
            s['mean_'+col]=float(ev[col].mean())
            s['sd_'+col]=float(ev[col].std(ddof=1))
        s['closing_count']=int(ev.closing_action_available.sum())
        s['terminations']=dict(collections.Counter(ev.termination_reason))
        # Seluruh episode dibaca untuk grafik; tidak menjalankan pembelajaran ulang.
        hp=folder/f'training_history_{scenario}.csv';record(hp)
        hist=pd.read_csv(hp,usecols=['scenario','seed','episode','epsilon','is_loop',
                                     'total_distance_m','total_reward','mean_comfort',
                                     'overlap_ratio','q_state_count','termination_reason'])
        assert len(hist)==5*total and hist.episode.min()==1 and hist.episode.max()==total
        assert hist.groupby('seed').size().eq(total).all()
        means=hist.groupby('episode',sort=True)[['is_loop','total_distance_m','total_reward','mean_comfort','overlap_ratio']].mean()
        rolling=means.rolling(50,min_periods=1).mean()
        sampled=rolling.loc[sorted({1,total,*range(500,total+1,500)})].reset_index()
        sampled['scenario']=scenario;sampled['config']=ci
        curves.append(sampled)
        tail=hist[hist.episode>total-10000]
        s['last10000_loop_rate']=float(tail.is_loop.mean())
        s['last10000_overlap_ratio']=float(tail.overlap_ratio.mean())
        s['last10000_mean_epsilon']=float(tail.epsilon.mean())
        last_windows.append({'config':ci,'scenario':scenario,'episodes':total,
                             'loop_rate':s['last10000_loop_rate'],'overlap_ratio':s['last10000_overlap_ratio']})
        summary.append(s)
        print(f'Terbaca {folder.name}: {s["loops"]}/5 loop',flush=True)

evaluation=pd.concat(all_eval,ignore_index=True);curve=pd.concat(curves,ignore_index=True)
start=routes[(2,'C',0)]['path_nodes'][0];startxy=np.array(xy[start])
assert all(route['path_nodes'][0]==start for route in routes.values())
graph_stats={'nodes':len(xy),'edges':len(road),'mean_edge_length_m':float(road.length_m.mean()),
             'weak_components':len({find(u) for u in xy}),'start_node':start,
             'start_outgoing_edges':int((road.u==start).sum()),
             'legal_edges':int(road.legal.sum()),'excluded_edges':int((~road.legal).sum()),
             'highway_present':int(road.highway_present.sum()),'surface_present':int(road.surface_present.sum()),
             'width_valid':int(road.width_m.notna().sum()),'access_present':int((road.access!='Tidak tersedia').sum()),
             'access_counts':{str(k):int(v) for k,v in road.access.value_counts().items()},
             'highway_counts':{str(k):int(v) for k,v in road.highway.value_counts().items()},
             'surface_counts':{str(k):int(v) for k,v in road.surface.value_counts().items()},
             'scores_all':{k:float(v) for k,v in road.score.describe().items()},
             'scores_legal':{k:float(v) for k,v in road[road.legal].score.describe().items()},
             'score_negative':int((road.score<0).sum()),'score_zero':int(np.isclose(road.score,0).sum()),
             'score_positive':int((road.score>0).sum())}
samples=[]
for conditions in [(road.H.eq(1)&road.S.eq(1)&road.W.eq(1)),
                   (road.highway.eq('service')&road.S.eq(-.5)&road.W.eq(-.5)),
                   (road.H.eq(1)&road.S.eq(-.5)&road.W.eq(1))]:
    r=road[conditions].iloc[0]
    samples.append({k:(None if pd.isna(r[k]) else r[k].item() if isinstance(r[k],np.generic) else r[k])
                    for k in ['u','v','key','highway','surface','width_raw','H','S','W','score']})
graph_stats['samples']=samples

evaluation.to_csv(out/'hasil_evaluasi_lengkap.csv',index=False)
pd.DataFrame(summary).drop(columns=['terminations']).to_csv(out/'ringkasan_hasil.csv',index=False)
curve.to_csv(out/'data_grafik_pelatihan.csv',index=False)
road[['u','v','key','highway','surface','width_raw','access','length_m','H','S','W','score','legal']].to_csv(out/'data_atribut_dan_skor.csv',index=False)
(out/'statistik_graf.json').write_text(json.dumps(graph_stats,indent=2,ensure_ascii=False))
(out/'ringkasan_terstruktur.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False))

def map_axes(ax,route=None):
    lines=[(np.array(s)-startxy)/1000 for s in segments]
    ax.add_collection(LineCollection(lines,colors='#D0D0D0',linewidths=.35,zorder=1))
    if route:
        lines=[(np.array(edges[(a['from_node'],a['next_node'],a['key'])]['_points'])-startxy)/1000 for a in route['path_actions']]
        ax.add_collection(LineCollection(lines,colors='#0072B2' if route['metrics']['is_loop'] else '#D55E00',linewidths=1.8,zorder=3))
        if not route['metrics']['is_loop']:
            end=(np.array(xy[route['path_nodes'][-1]])-startxy)/1000
            ax.scatter(*end,marker='x',s=65,c='#D55E00',linewidths=2,zorder=5,label='Titik akhir')
    ax.scatter(0,0,s=70,marker='*',c='black',zorder=6,label='Titik awal')
    ax.autoscale();ax.set_aspect('equal');ax.set_xlabel('Jarak ke arah timur dari titik awal (km)');ax.set_ylabel('Jarak ke arah utara (km)')
    if route:
        points=np.concatenate(lines);low=points.min(axis=0);high=points.max(axis=0)
        padding=np.maximum((high-low)*.15,.12)
        ax.set_xlim(low[0]-padding[0],high[0]+padding[0]);ax.set_ylim(low[1]-padding[1],high[1]+padding[1])
    handles,labels=ax.get_legend_handles_labels()
    if route:
        handles.insert(0,Line2D([0],[0],color='#0072B2' if route['metrics']['is_loop'] else '#D55E00',lw=2))
        labels.insert(0,'Rute perjalanan')
    ax.legend(handles,labels,loc='lower center' if route else 'upper right',
              bbox_to_anchor=(.5,1.01) if route else None,ncol=3 if route else 1,
              fontsize=10,framealpha=.9)
    ax.text(.01,.01,'Data jaringan © OpenStreetMap contributors',transform=ax.transAxes,fontsize=9,bbox={'facecolor':'white','alpha':.8,'edgecolor':'none'})

fig,ax=plt.subplots(figsize=(6.2,5.7));map_axes(ax);fig.tight_layout();save(fig,'jaringan_jalan_wilayah_studi')
fig,ax=plt.subplots(figsize=(6.2,3.3))
labels=['highway','surface','width valid','access'];counts=[graph_stats[k] for k in ['highway_present','surface_present','width_valid','access_present']]
ax.barh(labels[::-1],np.array(counts[::-1])/len(road)*100,color='#d8d8d8',edgecolor='black',hatch='//')
for i,c in enumerate(counts[::-1]):ax.text(c/len(road)*100+1,i,f'{number(c,0)} ({number(c/len(road)*100)}%)',va='center',fontsize=10)
ax.set_xlim(0,136);ax.set_xlabel('Edge dengan informasi tersedia (%)');ax.set_xticks([0,25,50,75,100]);fig.tight_layout();save(fig,'kelengkapan_atribut_jalan')
fig,ax=plt.subplots(figsize=(6.2,3.7));ax.hist(road.score,bins=np.arange(-1.05,1.051,.1),color='#d9d9d9',edgecolor='black')
ax.set_xlabel('Skor karakter ruas jalan');ax.set_ylabel('Jumlah edge terarah');ax.axvline(0,color='black',ls='--',lw=1);fig.tight_layout();save(fig,'distribusi_skor_karakter_ruas')

# Grafik pelatihan memakai rata-rata bergerak 50 episode dari seluruh lima seed.
def training_figure(column,ylabel,filename,percent=False,ylim=None):
    fig,axes=plt.subplots(2,2,figsize=(6.2,5.8),sharey=True)
    for ci,ax in enumerate(axes.flat):
        for scenario in 'ABC':
            data=curve[(curve.config==ci)&(curve.scenario==scenario)]
            ax.plot(data.episode/1000,data[column]*(100 if percent else 1),label='State '+scenario,
                    color=colors[scenario],ls=styles[scenario],lw=1.3)
        prefix,label,total,decay=configs[ci]
        ax.set_title(('Dinamis' if decay is None else 'Penurunan tetap 50.000')+'\n'+number(total,0)+' episode',fontsize=10.5)
        ax.set_xlim(0,total/1000);ax.set_xticks([0,total/2000,total/1000]);ax.grid(axis='y',alpha=.2)
        if ylim:ax.set_ylim(*ylim)
    fig.supxlabel('Episode pelatihan (ribu)',fontsize=11);fig.supylabel(ylabel,fontsize=11)
    handles,labels=axes[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='upper center',ncol=3,frameon=False,fontsize=10)
    fig.tight_layout(rect=(.03,.03,1,.94));save(fig,filename)
training_figure('is_loop','Episode yang membentuk loop (%)','perkembangan_keberhasilan_pelatihan',True,(0,100))
training_figure('overlap_ratio','Lintasan ruas yang berulang (%)','perkembangan_pengulangan_ruas',True,(0,None))

fig,ax=plt.subplots(figsize=(6.2,3.5));x=np.arange(4);w=.23
for j,scenario in enumerate('ABC'):
    data=[next(s for s in summary if s['config']==ci and s['scenario']==scenario)['loops'] for ci in range(4)]
    bars=ax.bar(x+(j-1)*w,data,width=w,label='State '+scenario,color=['#eeeeee','#999999','#444444'][j],edgecolor='black',hatch=['','//','xx'][j])
    for bar,val in zip(bars,data):ax.text(bar.get_x()+w/2,val+.06,str(val),ha='center',fontsize=10)
ax.set_xticks(x,['Dinamis\n75.000','Dinamis\n150.000','Tetap 50K\n75.000','Tetap 50K\n150.000']);ax.set_ylim(0,5.7);ax.set_yticks(range(6));ax.set_ylabel('Loop valid dari lima seed');ax.legend(ncol=3,fontsize=9,loc='upper left');fig.tight_layout();save(fig,'perbandingan_keberhasilan_evaluasi')

for scenario in 'ABC':
    fig,axes=plt.subplots(2,1,figsize=(6.2,5.5))
    for ci,(prefix,label,total,decay) in enumerate(configs):
        data=evaluation[(evaluation.config==ci)&(evaluation.scenario==scenario)].sort_values('seed')
        col=['#333333','#999999','#0072B2','#D55E00'][ci]
        for ax,metric in zip(axes,['total_distance_m','overlap_ratio']):
            ax.plot(data.seed,data[metric]*(100 if metric=='overlap_ratio' else 1),marker=['o','s','^','D'][ci],color=col,ls=['-','--','-.',':'][ci],label=label,lw=1.2)
    axes[0].axhspan(4500,5500,color='#eeeeee',zorder=0);axes[0].axhline(5000,color='black',ls=':',lw=.8);axes[0].set_ylabel('Jarak rute (m)')
    axes[1].set_ylabel('Pengulangan ruas (%)');axes[1].set_xlabel('Seed');axes[1].set_ylim(bottom=0)
    for ax in axes:ax.set_xticks(range(5));ax.grid(axis='y',alpha=.2)
    handles,labels=axes[0].get_legend_handles_labels();fig.legend(handles,labels,loc='upper center',ncol=2,fontsize=9,frameon=False)
    fig.tight_layout(rect=(0,0,1,.89));save(fig,'perbandingan_rute_state_'+scenario.lower())

examples=[('rute_loop_contoh',2,'C',0),('rute_gagal_contoh',0,'A',1)]
for name,ci,scenario,seed in examples:
    route=routes[(ci,scenario,seed)]
    fig,ax=plt.subplots(figsize=(6.2,5.5));map_axes(ax,route);fig.tight_layout();save(fig,name)
    (out/(name+'.json')).write_text(json.dumps(route,indent=2))

# Tabel riwayat pengujian dan daftar sumber membantu menelusuri setiap angka.
assert int(evaluation.is_loop.sum())==23
assert evaluation.groupby('scenario').is_loop.sum().to_dict()=={'A':2,'B':9,'C':12}
assert (evaluation.loc[~evaluation.is_loop,'closing_action_available']==False).all()
for relative,info in manifest.items():
    stat=(repo/relative).stat();assert (stat.st_size,stat.st_mtime_ns)==(info['size'],info['mtime_ns']),relative
(out/'sumber_data.json').write_text(json.dumps({'result_group':str(group.relative_to(repo)),
    'graph_sha256':hashlib.sha256(graph_path.read_bytes()).hexdigest(),'sources':manifest,
    'training_smoothing_window':50,'training_display_stride':500,
    'training_total_rows':6750000,'evaluation_total_rows':60},indent=2))
print(json.dumps(graph_stats,indent=2,ensure_ascii=False),flush=True)
