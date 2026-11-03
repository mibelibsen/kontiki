# -*- coding: utf-8 -*-
"""Bygger tekster/hamborg-segmenter.docx og .pdf — svarene fra Hamborg
delt i fem segmenter, ét til hver gruppe.

    python3 claude/byg_hamborg_segmenter.py          # PDF
    python3.13 claude/byg_hamborg_segmenter.py --word

Svarene hentes fra regnearket ved hver koersel. **De ligger ikke i repoet.**
Det er 170 besvarelser fra unge paa en anden skole, og repoet er offentligt;
det samme gaelder de faerdige dokumenter, som er udelukket i .gitignore.
Scriptet er kilden - dataene bliver hentet, naar der er brug for dem.

Segmenterne er valgt, saa de haenger sagligt sammen OG giver nogenlunde
samme arbejdsmaengde. Det blev maalt, ikke gaettet: antallet af
*forskellige* svar at oversaette pr. segment er 352, 299, 208, 211 og 304.
Foerste opdeling gav segment 5 over 400, og spoergsmaalet om rejser blev
derfor flyttet op i segment 1, hvor det ogsaa passer bedre - det handler om
at blive eller tage af sted.
"""
import csv
import io
import html as H
import os
import subprocess
import sys
import urllib.request
from collections import Counter

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARK = ('https://docs.google.com/spreadsheets/d/'
       '1QwwgmHeMVc-lsMEtmXtT4BobkF0HGyjVr9Twi1tCWbY/gviz/tq?tqx=out:csv')
UD_PDF = os.path.join(ROD, 'tekster', 'hamborg-segmenter.pdf')
UD_DOCX = os.path.join(ROD, 'tekster', 'hamborg-segmenter.docx')

# Et svar regnes for aabent, naar der er mere end AABEN forskellige svar.
# Under graensen er det en svarmulighed, man har valgt, og saa skal den
# taelles op i stedet for at blive oversat 170 gange.
AABEN = 12

SEGMENTER = [
 (1, 'Hamborg, hjemmet og at rejse væk', [2, 3, 4, 5, 6, 7, 31],
  'Hvem bor i byen, hvem gør ikke, hvad holder de af — og hvor ville de '
  'tage hen, hvis de kunne vælge frit.'),
 (2, 'Skole, job og drømmejob', [8, 9, 10, 11, 12],
  'Går de i skole, arbejder de ved siden af, og hvad vil de gerne være.'),
 (3, 'Fritid, sport og venner', [13, 14, 15, 16, 17, 18, 19, 20],
  'Hvad laver de, når de har fri, hvor ofte ses de med vennerne, og hvor '
  'mødes unge i Hamborg.'),
 (4, 'Mobil, medier og film', [21, 22, 23, 24, 25, 32],
  'Hvor mange timer på telefonen, hvad bruger de den til, og hvad ser de.'),
 (5, 'Mad, vaner og værdier', [26, 27, 28, 29, 30],
  'Yndlingsret, slik og øl — og de to store: hvad er vigtigt i livet, og '
  'hvad vil de nå at opleve.'),
]

OPGAVER = [
 'Oversæt jeres spørgsmål til dansk. Skriv oversættelsen ind over hvert '
 'spørgsmål.',
 'Oversæt svarene. De står med antal: <b>Hafen (12)</b> betyder, at tolv '
 'har svaret "Hafen". Begynd med dem, der er svaret flest gange.',
 'Find mønstrene. Hvad svarer mange? Hvad svarer kun én? Er der noget, '
 'der overrasker jer?',
 'Skriv en sammenfatning på en halv side: <b>hvad fortæller jeres '
 'segment om at være ung i Hamborg?</b> Brug tal, hvor I kan — "69 ud af '
 '169" siger mere end "mange".',
]


def hent():
    with urllib.request.urlopen(ARK, timeout=60) as r:
        tekst = r.read().decode('utf-8')
    raekker = list(csv.reader(io.StringIO(tekst)))
    hoved, data = raekker[0], raekker[1:]
    assert len(hoved) > 30, f'regnearket har kun {len(hoved)} kolonner'
    assert len(data) > 100, f'kun {len(data)} besvarelser — hentes det rigtige ark?'
    brugt = sorted(k for _, _, kol, _ in SEGMENTER for k in kol)
    assert len(brugt) == len(set(brugt)), 'et spørgsmål står i to segmenter'
    glemt = [i for i in range(2, len(hoved)) if i not in brugt]
    return hoved, data, glemt


def svar(data, i):
    return Counter(r[i].strip() for r in data
                   if i < len(r) and r[i].strip())


CSS = '''
*{box-sizing:border-box}
body{margin:0;font-family:Helvetica,Arial,sans-serif;color:#1a2233;
font-size:10pt;line-height:1.38}
h1{font-size:20pt;margin:0 0 2mm}
h2{font-size:15pt;margin:0 0 1mm}
h3{font-size:11pt;margin:5mm 0 1mm}
.lead{color:#333;max-width:160mm;margin:0 0 4mm}
.boks{border:0.3mm solid #c9d2e0;border-left:1.2mm solid #1f6fd6;
border-radius:2mm;padding:3mm 5mm;margin:4mm 0}
.boks ol{margin:2mm 0 0;padding-left:5mm}
.boks li{margin:1.5mm 0;color:#333}
.advarsel{border-left-color:#b5710a;background:#fdf8ef}
.seg{page-break-before:always}
.seghoved{background:#eef2f8;border-radius:3mm;padding:4mm 6mm;margin:0 0 4mm}
.seghoved .nr{color:#1f6fd6;font-weight:800;font-size:9pt;
letter-spacing:.6px;text-transform:uppercase}
.seghoved p{margin:1mm 0 0;color:#333}
.spm{border:0.3mm solid #c9d2e0;border-radius:2mm;padding:3mm 4mm;
margin:0 0 3mm;page-break-inside:avoid}
.tysk{font-weight:700;font-size:11pt;margin:0}
.dansk{color:#586074;font-size:9pt;margin:1mm 0 0}
.skrivelinje{border-bottom:0.3mm solid #c9d2e0;height:6mm}
table{width:100%;border-collapse:collapse;margin:2mm 0 0;font-size:9.5pt}
td,th{border:0.3mm solid #c9d2e0;padding:1.5mm 2.5mm;text-align:left;
vertical-align:top}
th{background:#f4f6fb;font-size:8pt;text-transform:uppercase;
letter-spacing:.4px;color:#586074}
td.tal{width:14mm;text-align:right;color:#586074}
td.pct{width:16mm;text-align:right;color:#586074}
td.skriv{width:52mm;background:#fbfcfe}
.flow{font-size:9.5pt;color:#333;margin:2mm 0 0;line-height:1.7}
.sammen{border:0.3mm solid #1f6fd6;border-radius:2mm;padding:3mm 4mm;
margin:4mm 0 0;page-break-inside:avoid}
.sammen b{display:block;margin-bottom:1mm}
footer{margin-top:5mm;border-top:0.3mm solid #c9d2e0;padding-top:2mm;
color:#586074;font-size:8.5pt}
@page{size:A4;margin:14mm}
'''


def spm_html(hoved, data, i, nr):
    u = svar(data, i)
    ialt = sum(u.values())
    s = (f'<div class="spm"><p class="tysk">{nr}. {H.escape(hoved[i])}</p>'
         f'<p class="dansk">På dansk:</p><div class="skrivelinje"></div>')
    if len(u) > AABEN:
        s += (f'<p class="dansk">{len(u)} forskellige svar fra {ialt} '
              f'besvarelser. Oversæt dem — begynd øverst.</p>'
              '<table><thead><tr><th>Svar på tysk</th><th>Antal</th>'
              '<th>På dansk</th></tr></thead><tbody>')
        for tekst, n in u.most_common():
            s += (f'<tr><td>{H.escape(tekst)}</td><td class="tal">{n}</td>'
                  f'<td class="skriv"></td></tr>')
        s += '</tbody></table>'
    else:
        s += (f'<p class="dansk">{ialt} har svaret. Oversæt '
              f'svarmulighederne, og se på tallene.</p>'
              '<table><thead><tr><th>Svarmulighed</th><th>Antal</th>'
              '<th>Andel</th><th>På dansk</th></tr></thead><tbody>')
        for tekst, n in u.most_common():
            s += (f'<tr><td>{H.escape(tekst)}</td><td class="tal">{n}</td>'
                  f'<td class="pct">{100 * n / ialt:.0f} %</td>'
                  f'<td class="skriv"></td></tr>')
        s += '</tbody></table>'
    return s + '</div>'


def byg_html(hoved, data, glemt):
    ialt = len(data)
    ikke_hamborg = sum(1 for r in data if r[2].strip() == 'Nein')
    opg = ''.join(f'<li>{t}</li>' for t in OPGAVER)
    krop = (f'<h1>Svarene fra Hamborg</h1>'
            f'<p class="lead">{ialt} unge har svaret på jeres spørgsmål. '
            f'Svarene er delt i fem segmenter — ét til hver gruppe. I skal '
            f'gennemgå jeres eget segment, oversætte det og sammenfatte, '
            f'hvad det fortæller.</p>'
            f'<div class="boks"><b>Sådan arbejder I</b><ol>{opg}</ol></div>'
            f'<div class="boks advarsel"><b>Læg mærke til det her, før I '
            f'går i gang</b><p style="margin:1mm 0 0;color:#333">'
            f'<b>{ikke_hamborg} af de {ialt}</b> svarer <i>nein</i> til '
            f'spørgsmålet, om de bor i Hamborg. Derfor står der <i>keine '
            f'Ahnung, bin nicht von hier</i> i en del af svarene om byen. '
            f'Det er ikke en fejl i jeres skema — det er et resultat, og I '
            f'skal skrive det i jeres sammenfatning. Et svar fra en, der '
            f'ikke bor i byen, fortæller noget andet end et svar fra en, '
            f'der gør.</p></div>'
            f'<h3>De fem segmenter</h3><table><thead><tr><th>Segment</th>'
            f'<th>Handler om</th><th>Spørgsmål</th></tr></thead><tbody>'
            + ''.join(f'<tr><td><b>{n}. {H.escape(navn)}</b></td>'
                      f'<td>{H.escape(om)}</td>'
                      f'<td class="tal">{len(kol)}</td></tr>'
                      for n, navn, kol, om in SEGMENTER)
            + '</tbody></table>')
    if glemt:
        krop += ('<p class="dansk">Spørgsmål uden for segmenterne (alder og '
                 'køn hører til alle fem): '
                 + ', '.join(H.escape(hoved[i]) for i in glemt) + '</p>')

    for n, navn, kol, om in SEGMENTER:
        aabne = sum(1 for i in kol if len(svar(data, i)) > AABEN)
        krop += (f'<div class="seg"></div>'
                 f'<div class="seghoved"><div class="nr">Segment {n}</div>'
                 f'<h2>{H.escape(navn)}</h2><p>{H.escape(om)}</p>'
                 f'<p><b>{len(kol)} spørgsmål</b>, heraf {aabne} med frie '
                 f'svar, I skal oversætte.</p></div>')
        for nr, i in enumerate(kol, 1):
            krop += spm_html(hoved, data, i, nr)
        krop += ('<div class="sammen"><b>Sammenfatning · segment '
                 f'{n}</b><p class="dansk">Hvad fortæller jeres segment om '
                 'at være ung i Hamborg? Skriv mindst tre ting, og brug '
                 'tal.</p>'
                 + '<div class="skrivelinje"></div>' * 8 + '</div>')

    return ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
            '<title>Svarene fra Hamborg</title><style>' + CSS
            + '</style></head><body>' + krop
            + f'<footer>{ialt} besvarelser · {len(SEGMENTER)} segmenter · '
              'Tysk · Ung i Tyskland.</footer></body></html>')


def byg_word(hoved, data, glemt):
    """Word-udgaven. Grupperne skal skrive oversættelserne ind, og det gør
    de i Word — derfor er den vigtigere end PDF'en her."""
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt, RGBColor

    GRAA = RGBColor(0x58, 0x60, 0x74)
    dok = Document()
    for s in dok.sections:
        s.top_margin = s.bottom_margin = Cm(1.6)
        s.left_margin = s.right_margin = Cm(1.8)
    dok.styles['Normal'].font.name = 'Arial'
    dok.styles['Normal'].font.size = Pt(10)

    def p(tekst='', fed=False, str_=10, farve=None, foer=0, efter=2):
        a = dok.add_paragraph()
        a.paragraph_format.space_before = Pt(foer)
        a.paragraph_format.space_after = Pt(efter)
        if tekst:
            k = a.add_run(tekst)
            k.bold = fed
            k.font.size = Pt(str_)
            if farve is not None:
                k.font.color.rgb = farve
        return a

    def fast_bredde(tabel, bredder):
        """Word fordeler selv kolonnerne efter indholdet. Uden fast layout
        bliver antal-kolonnen bredere end svarene."""
        lay = OxmlElement('w:tblLayout')
        lay.set(qn('w:type'), 'fixed')
        tabel._tbl.tblPr.append(lay)
        gitter = tabel._tbl.find(qn('w:tblGrid'))
        for gc, b in zip(gitter.findall(qn('w:gridCol')), bredder):
            gc.set(qn('w:w'), str(int(b.twips)))
        for r in tabel.rows:
            for c, b in zip(r.cells, bredder):
                c.width = b

    ialt = len(data)
    ikke_hamborg = sum(1 for r in data if r[2].strip() == 'Nein')
    p('Svarene fra Hamborg', fed=True, str_=20, efter=4)
    p(f'{ialt} unge har svaret på jeres spørgsmål. Svarene er delt i fem '
      f'segmenter — ét til hver gruppe. I skal gennemgå jeres eget segment, '
      f'oversætte det og sammenfatte, hvad det fortæller.', efter=10)

    p('Sådan arbejder I', fed=True, str_=12, foer=6)
    for i, t in enumerate(OPGAVER, 1):
        a = dok.add_paragraph()
        a.paragraph_format.left_indent = Cm(1.0)
        a.paragraph_format.first_line_indent = Cm(-0.6)
        a.paragraph_format.space_after = Pt(3)
        a.add_run(f'{i}.\t')
        a.add_run(t.replace('<b>', '').replace('</b>', ''))

    p('Læg mærke til det her, før I går i gang', fed=True, str_=12, foer=10)
    p(f'{ikke_hamborg} af de {ialt} svarer nein til spørgsmålet, om de bor '
      f'i Hamborg. Derfor står der "keine Ahnung, bin nicht von hier" i en '
      f'del af svarene om byen. Det er ikke en fejl i jeres skema — det er '
      f'et resultat, og I skal skrive det i jeres sammenfatning.', efter=12)

    for n, navn, kol, om in SEGMENTER:
        dok.add_page_break()
        p(f'SEGMENT {n}', fed=True, str_=9, farve=GRAA, efter=1)
        p(navn, fed=True, str_=16, efter=2)
        p(om, farve=GRAA, efter=10)
        for nr, i in enumerate(kol, 1):
            u = svar(data, i)
            n_svar = sum(u.values())
            aaben = len(u) > AABEN
            p(f'{nr}. {hoved[i]}', fed=True, str_=11, foer=8, efter=1)
            p('På dansk: ______________________________________________'
              '________________________', farve=GRAA, str_=9, efter=3)
            p(f'{len(u)} forskellige svar fra {n_svar} besvarelser.'
              if aaben else f'{n_svar} har svaret.', farve=GRAA, str_=9,
              efter=2)
            kolonner = ['Svar på tysk', 'Antal', 'På dansk'] if aaben else \
                       ['Svarmulighed', 'Antal', 'Andel', 'På dansk']
            t = dok.add_table(rows=1, cols=len(kolonner))
            t.style = 'Table Grid'
            for c, h in zip(t.rows[0].cells, kolonner):
                r = c.paragraphs[0].add_run(h)
                r.bold = True
                r.font.size = Pt(8)
            for tekst, antal in u.most_common():
                c = t.add_row().cells
                c[0].paragraphs[0].add_run(tekst).font.size = Pt(9)
                a = c[1].paragraphs[0]
                a.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                a.add_run(str(antal)).font.size = Pt(9)
                if not aaben:
                    a2 = c[2].paragraphs[0]
                    a2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                    a2.add_run(f'{100 * antal / n_svar:.0f} %').font.size = Pt(9)
            fast_bredde(t, [Cm(7.2), Cm(1.6), Cm(8.0)] if aaben else
                           [Cm(5.8), Cm(1.6), Cm(1.8), Cm(7.6)])

        p(f'Sammenfatning · segment {n}', fed=True, str_=12, foer=12)
        p('Hvad fortæller jeres segment om at være ung i Hamborg? Skriv '
          'mindst tre ting, og brug tal.', farve=GRAA, str_=9, efter=4)
        for _ in range(8):
            p('_' * 92, farve=GRAA, str_=9, efter=4)

    dok.save(UD_DOCX)
    print('skrevet: ', UD_DOCX)


if __name__ == '__main__':
    hoved, data, glemt = hent()
    os.makedirs(os.path.dirname(UD_PDF), exist_ok=True)
    h = UD_PDF.replace('.pdf', '.html')
    open(h, 'w', encoding='utf-8').write(byg_html(hoved, data, glemt))
    subprocess.run(['node', os.path.join(ROD, 'claude', 'html_til_pdf.mjs'),
                    h, UD_PDF], check=True, stdout=subprocess.DEVNULL)
    os.remove(h)
    print('skrevet: ', UD_PDF)
    if '--word' in sys.argv:
        byg_word(hoved, data, glemt)
    for n, navn, kol, om in SEGMENTER:
        a = sum(1 for i in kol if len(svar(data, i)) > AABEN)
        u = sum(len(svar(data, i)) for i in kol if len(svar(data, i)) > AABEN)
        print(f'  segment {n}: {len(kol)} spørgsmål · {a} åbne · '
              f'{u} svar at oversætte · {navn}')
    print(f'{len(data)} besvarelser')
