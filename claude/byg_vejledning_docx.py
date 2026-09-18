#!/usr/bin/env python3
"""Bygger vejledningen til den voksne som Word-fil.

Kilden er den samme HTML, som PDF'en gengives fra — filen som
`claude/byg_feature_plastik.py` skriver. Ingen tekst skrives af i hånden her:
scriptet læser overskrifter, afsnit, tabeller og figuren ud af HTML'en, så
Word-filen og PDF'en aldrig kan komme til at sige noget forskelligt.

    python3 claude/byg_vejledning_docx.py <mappe-med-vejledning-plastik.html>

Figuren er en SVG i HTML'en. Den gengives som PNG med Chromium (Playwright) og
lægges ind samme sted i dokumentet, som den står på siden.
"""
import os
import re
import subprocess
import sys
from html.parser import HTMLParser

from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Cm, Pt, RGBColor

SCRATCH = sys.argv[1] if len(sys.argv) > 1 else '.'
KILDE = os.path.join(SCRATCH, 'vejledning-plastik.html')
ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UD = os.path.join(ROD, 'vejledning', 'vejledning-plastik-og-foedevarer.docx')

SKRIFT = 'Calibri'
INK = RGBColor(0x1A, 0x22, 0x33)
MUTED = RGBColor(0x58, 0x60, 0x74)
ACCENT = RGBColor(0x1F, 0x6F, 0xD6)
LINJE = 'D3DAE7'
HOVED_FYLD = 'F4F6FB'

# =============================================================== 1 · læs HTML

class Laeser(HTMLParser):
    """Trækker blokke ud af vejledningens HTML.

    Resultatet er en liste af (slags, indhold):
      ('h1'|'h2'|'h3', tekststykker) · ('p', tekststykker) · ('figur', None)
      ('tabel', {'hoved': [...], 'raekker': [[...]], 'tal': [bool]})
    Tekststykker er (tekst, fed, kursiv), så fremhævninger overlever.
    """

    SPRING_OVER = {'header', 'footer', 'button', 'style', 'script', 'nav'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blokke = []
        self.dybde_spring = 0
        self.i_svg = 0
        self.aktiv = None          # slags for det afsnit vi samler på
        self.dele = []
        self.fed = self.kursiv = 0
        self.tabel = None
        self.celle = None
        self.i_hoved = False

    # -- små hjælpere ----------------------------------------------------
    def _luk_afsnit(self):
        if self.aktiv and any(t.strip() for t, _, _ in self.dele):
            self.blokke.append((self.aktiv, self._ryd(self.dele)))
        self.aktiv, self.dele = None, []

    @staticmethod
    def _ryd(dele):
        ud = []
        for tekst, f, k in dele:
            tekst = re.sub(r'\s+', ' ', tekst)
            if not tekst:
                continue
            if not ud and tekst.startswith(' '):
                tekst = tekst.lstrip()
            if ud and ud[-1][1] == f and ud[-1][2] == k:
                ud[-1] = (ud[-1][0] + tekst, f, k)
            else:
                ud.append((tekst, f, k))
        if ud:
            ud[-1] = (ud[-1][0].rstrip(), ud[-1][1], ud[-1][2])
        return [d for d in ud if d[0]]

    # -- parserens tilbagekald -------------------------------------------
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'svg':
            self.i_svg += 1
            if self.i_svg == 1:
                self._luk_afsnit()
                self.blokke.append(('figur', None))
            return
        if self.i_svg:
            return
        if self.dybde_spring or tag in self.SPRING_OVER:
            self.dybde_spring += 1
            return
        if tag in ('h1', 'h2', 'h3', 'p'):
            self._luk_afsnit()
            self.aktiv = tag
        elif tag == 'table':
            self._luk_afsnit()
            self.tabel = {'hoved': [], 'raekker': [], 'tal': []}
        elif tag == 'tr' and self.tabel is not None:
            if not self.i_hoved:
                self.tabel['raekker'].append([])
        elif tag in ('th', 'td') and self.tabel is not None:
            self.celle = []
            if tag == 'td' and len(self.tabel['raekker']) == 1:
                self.tabel['tal'].append('tal' in a.get('class', ''))
        elif tag == 'thead':
            self.i_hoved = True
        elif tag in ('b', 'strong'):
            self.fed += 1
        elif tag in ('i', 'em'):
            self.kursiv += 1
        elif tag == 'br':
            self.dele.append((' ', self.fed > 0, self.kursiv > 0))

    def handle_endtag(self, tag):
        if tag == 'svg':
            self.i_svg = max(0, self.i_svg - 1)
            return
        if self.i_svg:
            return
        if self.dybde_spring:
            self.dybde_spring -= 1
            return
        if tag in ('h1', 'h2', 'h3', 'p'):
            self._luk_afsnit()
        elif tag == 'thead':
            self.i_hoved = False
        elif tag in ('th', 'td') and self.tabel is not None:
            tekst = ' '.join(t for t, _, _ in self._ryd(self.celle or []))
            if tag == 'th':
                self.tabel['hoved'].append(tekst)
            else:
                self.tabel['raekker'][-1].append(tekst)
            self.celle = None
        elif tag == 'table' and self.tabel is not None:
            self.tabel['raekker'] = [r for r in self.tabel['raekker'] if r]
            self.blokke.append(('tabel', self.tabel))
            self.tabel = None
        elif tag in ('b', 'strong'):
            self.fed = max(0, self.fed - 1)
        elif tag in ('i', 'em'):
            self.kursiv = max(0, self.kursiv - 1)

    def handle_data(self, data):
        if self.i_svg or self.dybde_spring:
            return
        stykke = (data, self.fed > 0, self.kursiv > 0)
        if self.celle is not None:
            self.celle.append(stykke)
        elif self.aktiv:
            self.dele.append(stykke)


html = open(KILDE, encoding='utf-8').read()
laeser = Laeser()
laeser.feed(html[html.index('<body'):])
BLOKKE = laeser.blokke

assert BLOKKE and BLOKKE[0][0] == 'h1', 'forventede en h1 først i vejledningen'
assert sum(1 for s, _ in BLOKKE if s == 'tabel') == 7, 'forventede 7 tabeller'
assert sum(1 for s, _ in BLOKKE if s == 'figur') == 1, 'forventede én figur'

# =============================================================== 2 · figuren

FIGUR = os.path.join(SCRATCH, 'vejledning-figur.png')
svg = html[html.index('<svg'):html.index('</svg>') + 6]
bredde_px, hoejde_px = (int(v) for v in
                        re.search(r'viewBox="0 0 (\d+) (\d+)"', svg).groups())
fast_bredde = svg.replace('width="100%"', f'width="{bredde_px}"', 1)
open(os.path.join(SCRATCH, '_figur.html'), 'w', encoding='utf-8').write(
    '<!doctype html><meta charset="utf-8">'
    '<body style="margin:0;background:#fff">' + fast_bredde + '</body>')
subprocess.run(['node', '-e', f'''
import('/opt/node22/lib/node_modules/playwright/index.mjs').then(async (m) => {{
  const b = await m.chromium.launch();
  const p = await (await b.newContext({{deviceScaleFactor: 3}})).newPage();
  await p.setViewportSize({{width: {bredde_px}, height: {hoejde_px}}});
  await p.goto('file://{os.path.abspath(SCRATCH)}/_figur.html');
  await p.waitForTimeout(200);
  await p.screenshot({{path: '{FIGUR}'}});
  await b.close();
}});'''], check=True)
assert os.path.getsize(FIGUR) > 5000, 'figuren blev ikke gengivet'

# =============================================================== 3 · skriv docx

# Rækkefølgen af børn i <w:tcPr> er fastlagt i skemaet: tcW, tcBorders, shd,
# … , vAlign. Word nægter at åbne filen, hvis de står i en anden rækkefølge, så
# hvert element sættes ind foran sine efterfølgere i stedet for bare at hænges
# bagpå.
EFTER_TCBORDERS = ('w:shd', 'w:noWrap', 'w:tcMar', 'w:textDirection',
                   'w:tcFitText', 'w:vAlign', 'w:hideMark')
EFTER_SHD = EFTER_TCBORDERS[1:]


def _saet(celle, element, efterfoelgere):
    pr = celle._tc.get_or_add_tcPr()
    pr.insert_element_before(element, *efterfoelgere)


def kant(celle, farve=LINJE):
    ramme = OxmlElement('w:tcBorders')
    for side in ('top', 'left', 'bottom', 'right'):
        b = OxmlElement(f'w:{side}')
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), '6')
        b.set(qn('w:color'), farve)
        ramme.append(b)
    _saet(celle, ramme, EFTER_TCBORDERS)


def fyld(celle, farve):
    sk = OxmlElement('w:shd')
    sk.set(qn('w:val'), 'clear')
    sk.set(qn('w:fill'), farve)
    _saet(celle, sk, EFTER_SHD)


def skriv(afsnit, dele, storrelse=11, farve=INK, fed_alt=False):
    for tekst, f, k in dele:
        r = afsnit.add_run(tekst)
        r.font.name = SKRIFT
        r.font.size = Pt(storrelse)
        r.font.color.rgb = farve
        r.bold = f or fed_alt
        r.italic = k
    return afsnit


doc = Document()
sek = doc.sections[0]
sek.top_margin = sek.bottom_margin = Cm(2.0)
sek.left_margin = sek.right_margin = Cm(2.2)
BRED = sek.page_width - sek.left_margin - sek.right_margin

normal = doc.styles['Normal']
normal.font.name = SKRIFT
normal.font.size = Pt(11)
normal.font.color.rgb = INK
normal.paragraph_format.space_after = Pt(6)
normal.paragraph_format.line_spacing = 1.15

for slags, indhold in BLOKKE:
    if slags == 'h1':
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        skriv(p, indhold, storrelse=24, fed_alt=True)
        u = doc.add_paragraph()
        u.paragraph_format.space_after = Pt(14)
        skriv(u, [('Vejledning til den voksne', False, False)],
              storrelse=11, farve=ACCENT, fed_alt=True)
    elif slags in ('h2', 'h3'):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16 if slags == 'h2' else 10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        skriv(p, indhold, storrelse=14 if slags == 'h2' else 12, fed_alt=True)
    elif slags == 'p':
        skriv(doc.add_paragraph(), indhold)
    elif slags == 'figur':
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(8)
        p.add_run().add_picture(FIGUR, width=min(BRED, Cm(14)))
    elif slags == 'tabel':
        kolonner = len(indhold['hoved'])
        t = doc.add_table(rows=1, cols=kolonner)
        t.autofit = False
        bredder = [int(BRED / kolonner)] * kolonner
        for i, navn in enumerate(indhold['hoved']):
            c = t.rows[0].cells[i]
            c.width = bredder[i]
            c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            fyld(c, HOVED_FYLD)
            kant(c)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            skriv(p, [(navn, False, False)], storrelse=10, farve=MUTED,
                  fed_alt=True)
        for raekke in indhold['raekker']:
            celler = t.add_row().cells
            for i, tekst in enumerate(raekke[:kolonner]):
                c = celler[i]
                c.width = bredder[i]
                kant(c)
                p = c.paragraphs[0]
                p.paragraph_format.space_after = Pt(2)
                if i < len(indhold['tal']) and indhold['tal'][i]:
                    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                skriv(p, [(tekst, False, False)], storrelse=10)
        doc.add_paragraph().paragraph_format.space_after = Pt(2)

doc.save(UD)

print(f'skrevet:  {os.path.relpath(UD, ROD)}')
print(f'blokke:   {len(BLOKKE)} · '
      f"{sum(1 for s, _ in BLOKKE if s == 'tabel')} tabeller · "
      f"{sum(1 for s, _ in BLOKKE if s.startswith('h'))} overskrifter")
