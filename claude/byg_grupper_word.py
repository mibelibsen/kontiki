# -*- coding: utf-8 -*-
"""Bygger vejledning/grupper-fredag.docx — samme liste som PDF'en, i Word.

Navnene hentes fra claude/byg_grupper.py, saa de to filer ikke kan komme til
at sige hver sit. Kraever python-docx, som her kun ligger i python3.13:

    python3.13 claude/byg_grupper_word.py
"""
import os
import sys

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import byg_grupper as G

UD = os.path.join(G.ROD, 'vejledning', 'grupper-fredag.docx')

GRAA = RGBColor(0x58, 0x60, 0x74)
BLAA = RGBColor(0x1f, 0x6f, 0xd6)


def _kort(p, tekst, stoerrelse, fed=False, farve=None):
    k = p.add_run(tekst)
    k.font.size = Pt(stoerrelse)
    k.bold = fed
    if farve is not None:
        k.font.color.rgb = farve
    return k


dok = Document()
stil = dok.styles['Normal']
stil.font.name = 'Arial'
stil.font.size = Pt(11)

p = dok.add_paragraph()
_kort(p, 'INFO TIL 8. OG 9. KLASSE', 9, farve=GRAA)
p = dok.add_paragraph()
_kort(p, G.TITEL, 18, fed=True)
p.paragraph_format.space_after = Pt(2)
p = dok.add_paragraph()
_kort(p, G.UNDER, 12, farve=GRAA)
p.paragraph_format.space_after = Pt(14)

# Word fordeler selv kolonnerne efter indholdet, og saa bliver nummeret
# bredere end navnene. Bredderne saettes derfor paa hver eneste celle -
# det er den eneste maade, Word respekterer dem.
BREDDER = [Cm(1.4), Cm(12.2), Cm(1.8)]

tabel = dok.add_table(rows=0, cols=3)
tabel.style = 'Table Grid'
tabel.alignment = WD_TABLE_ALIGNMENT.LEFT
tabel.autofit = False
for nr, navne in enumerate(G.GRUPPER, 1):
    r = tabel.add_row().cells
    for celle, bredde in zip(r, BREDDER):
        celle.width = bredde
    a = r[0].paragraphs[0]
    a.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _kort(a, str(nr), 13, fed=True, farve=BLAA)
    _kort(r[1].paragraphs[0], ' · '.join(navne), 12, fed=True)
    c = r[2].paragraphs[0]
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _kort(c, str(len(navne)), 10, farve=GRAA)

# Bredder paa cellerne alene er ikke nok: Word og LibreOffice regner stadig
# kolonnerne ud af indholdet, medmindre tabellen er sat til fast layout og
# selve tabelgitteret har maalene. Begge dele skal skrives i XML'en.
_lay = OxmlElement('w:tblLayout')
_lay.set(qn('w:type'), 'fixed')
tabel._tbl.tblPr.append(_lay)
_grid = tabel._tbl.find(qn('w:tblGrid'))
for _gc, _b in zip(_grid.findall(qn('w:gridCol')), BREDDER):
    _gc.set(qn('w:w'), str(int(_b.twips)))

p = dok.add_paragraph()
p.paragraph_format.space_before = Pt(14)
_kort(p, f'{len(G.GRUPPER)} grupper · {G.I_ALT} unger · '
         'tallet til højre er, hvor mange I er i gruppen.', 9, farve=GRAA)

dok.save(UD)
print(f'skrevet:  {UD}')
print(f'{len(G.GRUPPER)} grupper · {G.I_ALT} unger')
