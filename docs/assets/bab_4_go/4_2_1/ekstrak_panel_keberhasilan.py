"""Extract the success panel from a saved Matplotlib training SVG.

Usage: python ekstrak_panel_keberhasilan.py training.svg panel.svg
The Word introduction/caption supplies the generic title and profile identity.
Original data curves, axes and ticks stay unchanged; only the SVG viewport and
visible panel selection change. Render the resulting vector SVG to PNG with a
standard SVG converter if needed. No Go or training files are written.
"""
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

SVG='http://www.w3.org/2000/svg'
ET.register_namespace('',SVG)
ET.register_namespace('xlink','http://www.w3.org/1999/xlink')
source,destination=map(Path,sys.argv[1:3])
if source.resolve()==destination.resolve():
    raise ValueError('Source and destination must be different files.')
tree=ET.parse(source);root=tree.getroot()
root.set('viewBox','7 32 494 286');root.set('width','494pt');root.set('height','286pt')
figure=next(g for g in root.findall('{'+SVG+'}g') if g.get('id')=='figure_1')
for child in list(figure):
    if child.get('id') not in ['patch_1','axes_1']:
        figure.remove(child)
axis=figure.find(".//*[@id='axes_1']")
axis.remove(list(axis)[-1])
tree.write(destination,encoding='utf-8',xml_declaration=True)
