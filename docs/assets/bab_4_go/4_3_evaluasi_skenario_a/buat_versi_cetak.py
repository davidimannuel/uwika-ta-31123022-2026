"""Buat versi cetak empat panel evaluasi tanpa mengubah titik/garis sumber.
Jalankan: python buat_versi_cetak.py SOURCE.svg OUTPUT.svg
"""
from pathlib import Path
from copy import deepcopy
import sys,re,json,hashlib
import xml.etree.ElementTree as E
NS='http://www.w3.org/2000/svg';N={'s':NS};E.register_namespace('',NS);E.register_namespace('xlink','http://www.w3.org/1999/xlink')
def tag(t):return '{'+NS+'}'+t
def elem(p,t,attrs=None,**kw):return E.SubElement(p,tag(t),{**(attrs or {}),**{k.replace('_','-'):str(v) for k,v in kw.items()}})
def tx(p,x,y,text,size=8,anchor='middle',**kw):
 e=elem(p,'text',x=x,y=y,font_size=size,text_anchor=anchor,**kw);e.text=text;return e
def nums(s):return [float(x) for x in re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?',s)]
def label(t):return ''.join(x.text or '' for x in t.iter() if not isinstance(x.tag,str)).strip()
def fmt(s):
 v=float(s.replace('−','-'))
 if v.is_integer():return f'{int(v):,}'.replace(',','.')
 return str(v).replace('.',',')
def print_comparison(source,destination):
 root=E.parse(source,parser=E.XMLParser(target=E.TreeBuilder(insert_comments=True))).getroot();axes=[g for g in root.findall('.//s:g',N) if re.fullmatch(r'axes_\d+',g.get('id',''))];assert len(axes)==4
 dest=E.Element(tag('svg'),{'width':'396pt','height':'274pt','viewBox':'0 0 396 274','version':'1.1'})
 defs=elem(dest,'defs')
 for d in root.findall('s:defs',N):
  for child in d:defs.append(deepcopy(child))
 sty=elem(defs,'style');sty.text='text{font-family:"Times New Roman",serif;fill:#111}path{stroke-linejoin:round;stroke-linecap:butt}'
 elem(dest,'rect',x=0,y=0,width=396,height=274,fill='white');checks=[]
 titles=['Keberhasilan loop','Galat jarak','Gerak mendekati titik awal','Ketersediaan penutup loop'];units=['Proporsi seed','Meter','Proporsi langkah','Proporsi seed']
 for i,axis in enumerate(axes):
  row,col=divmod(i,2);x,y,w,h=42+198*col,23+131*row,144,75
  coords=nums(axis[0].find('s:path',N).get('d'));x0,y1,x1,_,_,y0=coords[:6];sx=w/(x1-x0);sy=h/(y1-y0);ax=x-sx*x0;ay=y-sy*y0
  tx(dest,x+w/2,y-10,titles[i],9,font_weight='bold');tx(dest,x-33,y+h/2,units[i],8,transform=f'rotate(-90 {x-33} {y+h/2})')
  tickaxes=[z for z in axis if z.get('id','').startswith('matplotlib.axis_')];assert len(tickaxes)==2
  for which,tickaxis in enumerate(tickaxes):
   for tick in tickaxis:
    if 'tick_' not in tick.get('id',''):continue
    path=tick.find('.//s:path',N)
    if path is None:continue
    a=nums(path.get('d',''));text=label(tick)
    if len(a)<2 or not text:continue
    if which==0:
     xx=sx*a[0]+ax
     if not x-.1<=xx<=x+w+.1:continue
     elem(dest,'line',x1=xx,y1=y,x2=xx,y2=y+h,stroke='#dedede',stroke_width='.4');elem(dest,'line',x1=xx,y1=y+h,x2=xx,y2=y+h+3,stroke='#444',stroke_width='.5')
     tx(dest,xx,y+h+12,fmt(str(float(text.replace('−','-'))/1000)),8)
    else:
     yy=sy*a[1]+ay
     if not y-.1<=yy<=y+h+.1:continue
     elem(dest,'line',x1=x,y1=yy,x2=x+w,y2=yy,stroke='#dedede',stroke_width='.4');elem(dest,'line',x1=x-3,y1=yy,x2=x,y2=yy,stroke='#444',stroke_width='.5');tx(dest,x-5,yy+2.6,fmt(text),8,'end')
  tx(dest,x+w/2,y+h+25,'Episode pelatihan (ribu)',8)
  g=elem(dest,'g',transform=f'matrix({sx} 0 0 {sy} {ax} {ay})');before=[];after=[];uses_before=[];uses_after=[]
  for child in axis:
   if not child.get('id','').startswith('line2d_'):continue
   before.extend(p.get('d') for p in child.findall('.//s:path',N));uses_before.extend(z.attrib for z in child.findall('.//s:use',N))
   co=deepcopy(child)
   for p in co.findall('.//s:path',N):
    st=p.get('style','');st=re.sub(r'stroke-width:[^;]+','stroke-width:'+str(.8/min(sx,sy)),st)
    if 'stroke-width:' not in st:st+=';stroke-width:'+str(.8/min(sx,sy))
    p.set('style',st)
   after.extend(p.get('d') for p in co.findall('.//s:path',N));uses_after.extend(z.attrib for z in co.findall('.//s:use',N));g.append(co)
  assert before==after and uses_before==uses_after and before
  elem(dest,'rect',x=x,y=y,width=w,height=h,fill='none',stroke='#555',stroke_width='.6')
  checks.append({'axis':i+1,'source_data_paths_unchanged':True,'source_marker_coordinates_unchanged':True,'original_path_sha256':hashlib.sha256(json.dumps(before).encode()).hexdigest(),'original_clip_rect':coords[:6],'matrix':[sx,sy,ax,ay]})
 tx(dest,198,271,'Setiap titik merangkum lima evaluasi; tanpa rata-rata bergerak.',8)
 E.ElementTree(dest).write(destination,encoding='utf-8',xml_declaration=True)
 return {'source':str(source),'output':destination.name,'panels':checks,'min_font_pt_at_14cm':8*(14/2.54*72/396),'source_axis_limits_preserved':True,'x_unit':'thousands of training episodes','not_a_training_history_curve':True}
source,destination=map(Path,sys.argv[1:3])
if source.resolve()==destination.resolve():raise ValueError('Output must differ from source')
destination.parent.mkdir(parents=True,exist_ok=True)
audit=print_comparison(source,destination)
destination.with_suffix('.audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
