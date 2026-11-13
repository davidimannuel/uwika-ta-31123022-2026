"""Create an intact readable B composite from a saved SVG.
Usage: python buat_versi_cetak.py SOURCE.svg OUTPUT.svg training|diagnosis
Original plotted path vertices and source axis limits are retained. Typography
changes for 14cm print width. Episode and Q-state labels use thousands.
"""
from pathlib import Path
from copy import deepcopy
import sys,re,hashlib,json
import xml.etree.ElementTree as E
source,destination=map(Path,sys.argv[1:3]);kind=sys.argv[3]
if kind not in ['training','diagnosis']:raise ValueError('Unknown chart kind')
if source.resolve()==destination.resolve():raise ValueError('Output must differ from source')
AS=destination.parent;AS.mkdir(parents=True,exist_ok=True)
NS='http://www.w3.org/2000/svg';N={'s':NS}
E.register_namespace('',NS);E.register_namespace('xlink','http://www.w3.org/1999/xlink')
def tag(t):return '{'+NS+'}'+t
def elem(parent,t,attrs=None,**kw):return E.SubElement(parent,tag(t),{**(attrs or {}),**{k.replace('_','-'):str(v) for k,v in kw.items()}})
def tx(parent,x,y,text,size=8,anchor='middle',**kw):
 e=elem(parent,'text',x=x,y=y,font_size=size,text_anchor=anchor,**kw);e.text=text;return e
def nums(t):return [float(x) for x in re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?',t)]
def label(t):return ''.join(x.text or '' for x in t.iter() if not isinstance(x.tag,str)).strip()
def fmt(t):
 try:
  v=float(t.replace('−','-'))
  if v.is_integer():return f'{int(v):,}'.replace(',','.')
 except ValueError:pass
 return t.replace('.',',')
def hashfile(p):return hashlib.sha256(p.read_bytes()).hexdigest()

audit=[];figures=[];source_hashes={};stats=[];signatures=[]
def print_figure(source,kind,profile):
 root=E.parse(source,parser=E.XMLParser(target=E.TreeBuilder(insert_comments=True))).getroot()
 axes=[g for g in root.findall('.//s:g',N) if re.fullmatch('axes_\\d+',g.get('id',''))]
 assert len(axes)==(6 if kind=='training' else 5)
 dest=E.Element(tag('svg'),{'width':'396pt','height':'372pt','viewBox':'0 0 396 372','version':'1.1'})
 defs=elem(dest,'defs')
 # Original data paths and their original clipping rectangles are retained.
 for d in root.findall('s:defs',N):
  for c in d:defs.append(deepcopy(c))
 style=elem(defs,'style');style.text='text{font-family:"Times New Roman",serif;fill:#111}path{stroke-linejoin:round;stroke-linecap:butt}'
 elem(dest,'rect',x=0,y=0,width=396,height=372,fill='white')
 if kind=='training':
  titles=['Keberhasilan loop','Reward','Jarak perjalanan','Skor karakter ruas','Jumlah state Q-table','Epsilon']
  units=['Proporsi','Reward','Jarak (km)','Skor','State (ribu)','Epsilon']
 else:
  titles=['Jarak akhir ke titik awal','Gerak mendekati titik awal','Ketersediaan penutup loop','Galat pembaruan Q','Jenis akhir episode']
  units=['Meter','Proporsi langkah','Persentase (%)','Rata-rata |TD-error|','Persentase (%)']
 checks=[]
 for i,axis in enumerate(axes):
  r,c=divmod(i,2)
  x,y,w,h=42+c*198,22+r*115.5,144,65
  if kind=='diagnosis' and i==4:x,y,w,h=42,253,342,65
  coords=nums(axis[0].find('s:path',N).get('d'))
  x0,y1,x1,_,_,y0=coords[:6];sx=w/(x1-x0);sy=h/(y1-y0)
  ax,ay=x-sx*x0,y-sy*y0
  title=elem(dest,'g')
  tx(title,x+w/2,y-10,titles[i],9,font_weight='bold')
  tx(title,x-34,y+h/2,units[i],8,transform=f'rotate(-90 {x-34} {y+h/2})')
  ticks=[a for a in axis if a.get('id','').startswith('matplotlib.axis_')]
  assert len(ticks)==2
  for which,tickaxis in enumerate(ticks):
   for tick in tickaxis:
    if 'tick_' not in tick.get('id',''):continue
    path=tick.find('.//s:path',N)
    if path is None:continue
    a=nums(path.get('d',''))
    if len(a)<2:continue
    text=label(tick)
    if which==0:
     xx=sx*a[0]+ax
     if not x-.1<=xx<=x+w+.1:continue
     elem(dest,'line',x1=xx,y1=y,x2=xx,y2=y+h,stroke='#dedede',stroke_width='.4')
     elem(dest,'line',x1=xx,y1=y+h,x2=xx,y2=y+h+3,stroke='#444',stroke_width='.5')
     text=fmt(str(float(text.replace('−','-'))/1000))
     tx(dest,xx,y+h+12,text,8)
    else:
     yy=sy*a[1]+ay
     if not y-.1<=yy<=y+h+.1:continue
     elem(dest,'line',x1=x,y1=yy,x2=x+w,y2=yy,stroke='#dedede',stroke_width='.4')
     elem(dest,'line',x1=x-3,y1=yy,x2=x,y2=yy,stroke='#444',stroke_width='.5')
     display=fmt(str(float(text.replace('−','-'))/1000)) if kind=='training' and i==4 else fmt(text)
     tx(dest,x-5,yy+2.6,display,8,'end')
  tx(dest,x+w/2,y+h+25,'Episode (ribu)',8)
  group=elem(dest,'g',transform=f'matrix({sx} 0 0 {sy} {ax} {ay})')
  paths=[]
  line_index=0
  for child in axis:
   if not child.get('id','').startswith('line2d_'):continue
   co=deepcopy(child)
   for path in co.findall('.//s:path',N):
    # Width is presentation only; d retains every original plotted vertex.
    st=path.get('style','');st=re.sub(r'stroke-width:[^;]+','stroke-width: '+str(.65/min(sx,sy)),st)
    if 'stroke-width:' not in st:st+=';stroke-width:'+str(.65/min(sx,sy))
    path.set('style',st)
    if kind=='diagnosis' and i==4:
     dash=['','4 2','1 2','5 2 1 2'][line_index]
     if dash:path.set('style',path.get('style')+';stroke-dasharray:'+ ' '.join(str(float(v)/min(sx,sy)) for v in dash.split()))
    paths.append(path.get('d'))
   group.append(co)
   line_index+=1
  originals=[p.get('d') for child in axis if child.get('id','').startswith('line2d_') for p in child.findall('.//s:path',N)]
  assert paths==originals and paths
  checks.append({'axis':i+1,'path_count':len(paths),'original_path_d_unchanged':True,'original_path_sha256':hashlib.sha256(json.dumps(paths).encode()).hexdigest(),'matrix':[sx,sy,ax,ay]})
  elem(dest,'rect',x=x,y=y,width=w,height=h,fill='none',stroke='#555',stroke_width='.6')
  if kind=='diagnosis' and i==4:
   labels=['Berhasil loop','Melebihi 6 km','Tidak ada pilihan ruas','Batas langkah']
   colors=['#16a34a','#dc2626','#7c3aed','#475569']
   for j,(text,color) in enumerate(zip(labels,colors)):
    lx=44+(j%2)*177;ly=356+(j//2)*10
    elem(dest,'line',x1=lx,y1=ly-2.5,x2=lx+13,y2=ly-2.5,stroke=color,stroke_width='1.2',stroke_dasharray=['none','4 2','1 2','5 2 1 2'][j])
    tx(dest,lx+17,ly,text,8,'start')
 if kind=='training':
  tx(dest,198,355,'Garis putus-putus: target 5 km; garis titik: batas 4–6 km.',8)
  tx(dest,198,367,'Rata-rata lima seed; kurva dihaluskan 50 episode, kecuali epsilon.',8)
 out=AS/(profile+'_'+kind+'_cetak.svg');E.ElementTree(dest).write(out,encoding='utf-8',xml_declaration=True)
 audit.append({'source':str(source),'output':out.name,'axes':checks,'min_font_pt_at_14cm':8*(14/2.54*72/396),'x_unit':'thousands of episodes; tick positions unchanged','q_state_y_unit':'thousands of states in training axis 5; tick positions and source limits unchanged','layout':'all original panels retained, printed typography and labels adapted, original curve paths and axis limits retained'})
 return out

result=print_figure(source,kind,source.parent.name)
if result!=destination:result.replace(destination)
destination.with_suffix('.audit.json').write_text(json.dumps(audit,indent=2)+'\n')
