# -*- coding: utf-8 -*-
"""Bygger vejledning/spejlvend-video.pdf og .docx — hvordan man spejlvender
en video, gratis, uden at uploade den nogen steder.

    python3 claude/byg_spejlvend.py        # PDF
    python3.13 claude/byg_spejlvend.py --word   # ogsaa Word (kraever python-docx)

Teksten staar ét sted (TRIN og HUSK nedenfor), saa de to filer ikke kan komme
til at sige hver sit.
"""
import html
import os
import re
import subprocess
import sys

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UD_HTML = os.path.join(ROD, 'vejledning', 'spejlvend-video.html')
UD_PDF = os.path.join(ROD, 'vejledning', 'spejlvend-video.pdf')
UD_PNG = os.path.join(ROD, 'vejledning', '.spejlvend-figur.png')
UD_DOCX = os.path.join(ROD, 'vejledning', 'spejlvend-video.docx')

TITEL = 'Sådan spejlvender du en video'
UNDER = ('Gratis, og uden at videoen bliver sendt til en fremmed server. '
         'Find afsnittet, der passer til din maskine.')

TRIN = [
    ('iPad eller iPhone', 'Billeder — den app, videoen allerede ligger i. '
     'Du skal ikke hente noget.', [
        'Åbn videoen i <b>Billeder</b>.',
        'Tryk <b>Rediger</b> øverst til højre.',
        'Tryk på <b>beskær-ikonet</b> nederst.',
        'Tryk på <b>vend-ikonet</b> øverst til venstre. Det er den '
        '<b>trekantede</b> — den firkantede ved siden af roterer bare '
        'videoen en kvart omgang.',
        'Tryk <b>Færdig</b>.',
     ],
     'Fortryder du, så tryk Rediger igen og vælg <b>Vend tilbage til '
     'original</b>. Der er intet at miste ved at prøve.'),

    ('Windows', 'Clipchamp. Den følger med Windows 11 — søg efter den i '
     'Start-menuen. Log ind med din skolekonto, den samme som til Teams.', [
        'Åbn Clipchamp og lav et nyt projekt.',
        'Træk videoen ind, og træk den derfra ned på <b>tidslinjen</b> '
        'nederst.',
        'Klik på klippet, så det får en <b>grøn ramme</b>.',
        'I panelet ved siden af forhåndsvisningen vælger du '
        '<b>vend vandret</b>.',
        'Tryk <b>Eksportér</b> og vælg <b>1080p</b>.',
     ],
     'Gratis-udgaven gemmer i 1080p. Det er mere end nok — det er samme '
     'skarphed som en almindelig fjernsynsudsendelse.'),

    ('Mac', 'QuickTime Player, som allerede ligger på maskinen.', [
        'Åbn videoen i <b>QuickTime Player</b>.',
        'Vælg <b>Rediger</b> i menulinjen øverst.',
        'Vælg <b>Vend vandret</b>.',
        'Luk vinduet, og tryk <b>Arkivér</b>.',
     ], ''),
]

HUSK = [
    'Spejlvendingen rammer <b>hele</b> billedet. Stod der skrift i videoen, '
    'som var rigtig, står den spejlvendt bagefter. Se efter, når du er '
    'færdig.',
    'Lad være med at søge efter »flip video online«. De fleste af de sider '
    'vil have dig til at <b>uploade</b> filen til en server, du ikke ved, '
    'hvor står. Alle tre metoder her foregår på din egen maskine.',
]

# Figuren: to lige store rammer med det samme ord, hvor det venstre er
# spejlvendt om sin egen midterakse. Koordinaterne er regnet, ikke sat paa
# oejemaal - rammerne er lige brede, og pilen staar praecis i mellemrummet.
W, H = 520, 120
RAMME_B, GAB = 220, 80
X0 = (W - 2 * RAMME_B - GAB) / 2
X1 = X0 + RAMME_B + GAB
assert abs((X1 + RAMME_B) - (W - X0)) < 0.01, 'rammerne står ikke symmetrisk'
MIDTE_Y = 46
ORD = 'PLASTIK'


def _ramme(x, maerke, spejlet):
    midt = x + RAMME_B / 2
    # scale(-1,1) spejler om x=0, saa teksten skal foerst flyttes derhen og
    # derefter tilbage. 2*midt er netop den tur frem og tilbage.
    t = (f' transform="translate({2 * midt:.1f},0) scale(-1,1)"'
         if spejlet else '')
    return (f'<rect x="{x:.1f}" y="14" width="{RAMME_B}" height="56" rx="4" '
            f'fill="#fff" stroke="#1a2233" stroke-width="1.2"/>'
            f'<text x="{midt:.1f}" y="{MIDTE_Y + 6}" text-anchor="middle" '
            f'font-size="24" font-weight="700" fill="#1a2233"{t}>{ORD}</text>'
            f'<text x="{midt:.1f}" y="90" text-anchor="middle" font-size="12" '
            f'fill="#586074">{maerke}</text>')


FIGUR = (
    f'<svg viewBox="0 0 {W} {H}" width="100%" style="max-width:{W}px" '
    f'xmlns="http://www.w3.org/2000/svg" role="img" '
    f'aria-label="Før: ordet PLASTIK står spejlvendt. Efter: det står '
    f'rigtigt." font-family="Helvetica,Arial,sans-serif">'
    + _ramme(X0, 'Før', True)
    + f'<line x1="{X0 + RAMME_B + 18:.1f}" y1="{MIDTE_Y}" '
      f'x2="{X1 - 18:.1f}" y2="{MIDTE_Y}" stroke="#1a2233" stroke-width="1.5"/>'
      f'<path d="M{X1 - 18:.1f},{MIDTE_Y} l-9,-5 v10 z" fill="#1a2233"/>'
    + _ramme(X1, 'Efter', False)
    + '</svg>')

CSS = '''
body{margin:0;font-family:Georgia,'Times New Roman',serif;color:#000;
font-size:11pt;line-height:1.4}
h1{font-size:18pt;margin:0 0 2mm}
h2{font-size:12.5pt;margin:3.5mm 0 1mm}
.under{margin:0 0 4mm}
.hvad{margin:0 0 2mm;font-size:11pt;color:#333}
.figur{margin:0 0 4mm;text-align:center}
ol{margin:0;padding-left:9mm}
ol li{margin:0 0 1.2mm;padding-left:2mm}
.noteline{margin:1.5mm 0 0;font-size:11pt;color:#333}
h2.husk{margin-top:4mm}
ul{margin:0;padding-left:9mm}
ul li{margin:0 0 1.5mm;padding-left:2mm}
@page{size:A4;margin:14mm}
'''


def _afsnit_html():
    ud = ''
    for navn, hvad, trin, note in TRIN:
        ud += (f'<h2>{html.escape(navn)}</h2>'
               f'<p class="hvad">{hvad}</p><ol>'
               + ''.join(f'<li>{t}</li>' for t in trin) + '</ol>')
        if note:
            ud += f'<p class="noteline">{note}</p>'
    return ud


DOK = ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
       f'<title>{html.escape(TITEL)}</title><style>' + CSS
       + '</style></head><body>'
       f'<h1>{html.escape(TITEL)}</h1>'
       f'<p class="under">{html.escape(UNDER)}</p>'
       f'<div class="figur">{FIGUR}</div>'
       + _afsnit_html()
       + '<h2 class="husk">Husk to ting</h2><ul>'
       + ''.join(f'<li>{t}</li>' for t in HUSK)
       + '</ul></body></html>')


def _skriv(p, s, stoerrelse=None):
    """Skriver teksten i afsnittet og saetter <b>...</b> fed undervejs, saa
    Word-udgaven fremhaever de samme ord som PDF'en - og saa der ikke staar
    raa HTML midt i en saetning."""
    from docx.shared import Pt
    for stump in re.split(r'(<b>.*?</b>)', s):
        if not stump:
            continue
        fed = stump.startswith('<b>')
        k = p.add_run(stump[3:-4] if fed else stump)
        k.bold = fed
        if stoerrelse:
            k.font.size = Pt(stoerrelse)
    return p


def byg_pdf():
    os.makedirs(os.path.dirname(UD_HTML), exist_ok=True)
    open(UD_HTML, 'w', encoding='utf-8').write(DOK)
    subprocess.run(['node', os.path.join(ROD, 'claude', 'html_til_pdf.mjs'),
                    UD_HTML, UD_PDF], check=True, stdout=subprocess.DEVNULL)
    os.remove(UD_HTML)
    print(f'skrevet:  {UD_PDF}')


def byg_figur_png():
    """Figuren som PNG, saa Word-udgaven kan vise den samme tegning."""
    h = ('<!DOCTYPE html><meta charset="UTF-8">'
         '<style>body{margin:0}svg{display:block}</style>' + FIGUR)
    sti = UD_HTML.replace('.html', '-figur.html')
    open(sti, 'w', encoding='utf-8').write(h)
    mjs = os.path.join(ROD, 'claude', 'svg_til_png.mjs')
    open(mjs, 'w', encoding='utf-8').write(f'''// Gengiver en SVG som PNG.
//   node claude/svg_til_png.mjs <kilde.html> <ud.png> <bredde> <hoejde>
import {{ chromium }} from '/opt/node22/lib/node_modules/playwright/index.mjs';
import {{ pathToFileURL }} from 'node:url';
import {{ resolve }} from 'node:path';
const [k, u, b, h] = process.argv.slice(2);
const br = await chromium.launch();
const p = await br.newPage({{ viewportSize: {{ width: +b, height: +h }},
                             deviceScaleFactor: 3 }});
await p.goto(pathToFileURL(resolve(k)).href, {{ waitUntil: 'load' }});
await p.locator('svg').screenshot({{ path: u }});
await br.close();
''')
    subprocess.run(['node', mjs, sti, UD_PNG, str(W), str(H)], check=True)
    os.remove(sti)
    return UD_PNG


def byg_word():
    from docx import Document
    from docx.shared import Cm, Pt

    png = byg_figur_png()
    dok = Document()
    # Words standardmargener er brede nok til at skubbe Mac-afsnittet over
    # paa side to. Samme margener som PDF'en, saa vejledningen er ét ark.
    for s in dok.sections:
        s.top_margin = s.bottom_margin = Cm(1.5)
        s.left_margin = s.right_margin = Cm(1.8)
    dok.styles['Normal'].font.name = 'Times New Roman'
    dok.styles['Normal'].font.size = Pt(11)

    p = dok.add_paragraph()
    k = p.add_run(TITEL)
    k.bold = True
    k.font.size = Pt(18)
    dok.add_paragraph(UNDER).paragraph_format.space_after = Pt(10)
    dok.add_picture(png, width=Cm(9))
    dok.paragraphs[-1].alignment = 1
    dok.paragraphs[-1].paragraph_format.space_after = Pt(8)

    # Numrene skrives som tekst. Words egen List Number deler én taeller
    # mellem alle lister i dokumentet, saa Windows-afsnittet begyndte ved 6
    # og Mac ved 11. Her begynder hver maskine ved 1.
    for navn, hvad, trin, note in TRIN:
        h = dok.add_paragraph()
        r = h.add_run(navn)
        r.bold = True
        r.font.size = Pt(13)
        h.paragraph_format.space_before = Pt(9)
        _skriv(dok.add_paragraph(), hvad)
        for nr, t in enumerate(trin, 1):
            a = dok.add_paragraph()
            a.paragraph_format.left_indent = Cm(1.1)
            a.paragraph_format.first_line_indent = Cm(-0.7)
            a.paragraph_format.space_after = Pt(2)
            a.add_run(f'{nr}.\t')
            _skriv(a, t)
        if note:
            n = dok.add_paragraph()
            n.paragraph_format.space_before = Pt(4)
            _skriv(n, note)

    h = dok.add_paragraph()
    r = h.add_run('Husk to ting')
    r.bold = True
    r.font.size = Pt(13)
    h.paragraph_format.space_before = Pt(8)
    for t in HUSK:
        _skriv(dok.add_paragraph(style='List Bullet'), t)

    dok.save(UD_DOCX)
    os.remove(png)
    print(f'skrevet:  {UD_DOCX}')


if __name__ == '__main__':
    byg_pdf()
    if '--word' in sys.argv:
        byg_word()
    print(f'{len(TRIN)} maskiner · {sum(len(t[2]) for t in TRIN)} trin i alt')
