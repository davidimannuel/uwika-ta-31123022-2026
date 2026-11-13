"""Recreate the thesis completeness figure from the adjacent CSV.

Uses ReportLab graphics charts and the bundled Node/Sharp raster converter.
This helper belongs to thesis assets; it does not change the Go notebook.
Run using the bundled document Python runtime, which already contains ReportLab.
"""
from pathlib import Path
import csv,subprocess
from reportlab.graphics.shapes import Drawing,String,Rect
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderSVG
from reportlab.lib import colors
AS=Path(__file__).resolve().parent
rows=list(csv.DictReader((AS/'sumber_attribute_completeness.csv').open(encoding='utf-8-sig')))
assert all(int(r['present_edges'])+int(r['missing_edges'])==59176 for r in rows)
present=[float(r['present_pct']) for r in rows];missing=[float(r['missing_pct']) for r in rows]
drawing=Drawing(560,320)
drawing.add(Rect(0,0,560,320,fillColor=colors.white,strokeColor=None))
chart=VerticalBarChart();chart.x=65;chart.y=42;chart.width=480;chart.height=220
chart.data=[present,missing];chart.categoryAxis.style='stacked'
chart.categoryAxis.categoryNames=[r['attribute'] for r in rows]
chart.categoryAxis.labels.fontName='Times-Roman';chart.categoryAxis.labels.fontSize=16
chart.categoryAxis.labels.dy=-5
chart.valueAxis.valueMin=0;chart.valueAxis.valueMax=110;chart.valueAxis.valueSteps=list(range(0,101,20))
chart.valueAxis.labels.fontName='Times-Roman';chart.valueAxis.labels.fontSize=15
chart.valueAxis.visibleGrid=True;chart.valueAxis.gridStrokeColor=colors.HexColor('#dddddd');chart.valueAxis.gridStrokeWidth=.5
chart.barWidth=45;chart.groupSpacing=40
chart.bars[0].fillColor=colors.HexColor('#35698a');chart.bars[1].fillColor=colors.HexColor('#eeeeee')
chart.bars.strokeColor=colors.black;chart.bars.strokeWidth=.5
chart.barLabelFormat=[lambda v: f'{v:.2f}%'.replace('.',','),None]
chart.barLabels.fontName='Times-Roman';chart.barLabels.fontSize=15;chart.barLabels.nudge=9
drawing.add(chart)
drawing.add(String(65,274,'Persentase edge (%)',fontName='Times-Roman',fontSize=15))
for x,label,color in [(165,'Terisi','#35698a'),(310,'Tidak tercatat','#eeeeee')]:
    drawing.add(Rect(x,293,18,13,fillColor=colors.HexColor(color),strokeColor=colors.black,strokeWidth=.5))
    drawing.add(String(x+26,293,label,fontName='Times-Roman',fontSize=16))
renderSVG.drawToFile(drawing,str(AS/'kelengkapan_atribut.svg'))
node='/Users/david/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
sharp='/Users/david/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp'
js='const sharp=require(process.argv[1]); sharp(process.argv[2],{density:300}).png().toFile(process.argv[3]).catch(e=>{console.error(e);process.exit(1)});'
subprocess.run([node,'-e',js,sharp,str(AS/'kelengkapan_atribut.svg'),str(AS/'kelengkapan_atribut.png')],check=True)
