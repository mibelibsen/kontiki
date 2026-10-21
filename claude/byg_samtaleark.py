# -*- coding: utf-8 -*-
"""Bygger vejledning/skolehjemsamtale.pdf — skabelon til en samtale paa 30 min.

Ét ark pr. elev. Fokus er fagligt: hvor staar hun, hvad er maalet, hvad er
rykket, og hvad skal der til - i skolen og hjemme.

Arket ligger i vejledning/, som er udelukket fra deploy. Det bliver udfyldt
med vurderinger af et navngivet barn og hoerer ikke paa et offentligt site.
PDF'en er en bygget fil og er ikke i git; scriptet er kilden.

    python3 claude/byg_samtaleark.py
"""
import html
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figurer as FG

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UD_HTML = os.path.join(ROD, 'vejledning', 'skolehjemsamtale.html')
UD_PDF = os.path.join(ROD, 'vejledning', 'skolehjemsamtale.pdf')

MINUTTER = 30

# Halvdelen af tiden gaar til de to-tre fag, der skal rykke noget. Resten af
# fagene naevnes, saa intet bliver sprunget over - men de faar ikke lige tid.
# Otte fag paa en halv time er under fire minutter hver, og saa naar man
# ingenting i nogen af dem.
TIDSPLAN = [
    ('Eleven selv', 4),
    ('Overblik over fagene', 8),
    ('De valgte fag', 12),
    ('Aftaler', 6),
]
assert sum(m for _, m in TIDSPLAN) == MINUTTER

FAG = ['Dansk', 'Matematik', 'Fysik/kemi', 'Samfundsfag',
       'Historie', 'Engelsk', 'Tysk', 'Idræt']

FOER = [
 'Udfyld <b>standpunkt</b> og <b>fremskridt</b> for alle otte fag på forhånd. '
 'Det er det, der ikke er tid til at finde ud af undervejs.',
 'Sæt kryds ved de <b>to-tre fag</b>, I går i dybden med. Vælg dem, hvor der '
 'skal ske noget — ikke dem, der er lettest at tale om.',
 'Start med at spørge <b>eleven</b>. Hvad går godt, hvad er svært? Så ved I, '
 'om I er enige, inden I bruger tiden på at fortælle.',
]

OVERSIGT_KOL = ['Fag', 'Standpunkt', 'Mål', 'Fremskridt', 'Støtte / ændring']

# Stoette i skolen, stoette hjemme og aendret adfaerd er det samme
# spoergsmaal stillet tre steder: hvad skal der til. De staar derfor i én
# raekke med tre kolonner - det sparer en tredjedel af hoejden og goer det
# tydeligt, at de tre ting skal haenge sammen.
DYBDE = [
    ('Standpunkt', 'Hvad kan hun/han nu — konkret', 2, None),
    ('Mål', 'Hvad er det næste skridt', 2, None),
    ('Fremskridt siden sidst', '', 1, None),
    ('Hvad skal der til?', '', 2, ('I skolen', 'Hjemme', 'Ændret adfærd')),
]

AFTALER_KOL = ['Aftale', 'Hvem gør det', 'Hvornår']
AFTALER_RAEKKER = 3


def linjer(n):
    return f'<div class="linjer" style="height:{n * 7}mm"></div>'


def skema(kolonner, raekker, hoejde='14mm', bredder=None):
    """Et tomt skema. `raekker` er enten et tal eller en liste af tekster,
    der staar i foerste kolonne. `bredder` er procenter - uden dem fordeler
    browseren kolonnerne efter overskrifternes laengde, og saa bliver
    "Maal" smal og "Stoette / aendring" bred uden grund."""
    if isinstance(raekker, int):
        raekker = [''] * raekker
    bredder = bredder or [100 / len(kolonner)] * len(kolonner)
    assert len(bredder) == len(kolonner), 'én bredde pr. kolonne'
    assert abs(sum(bredder) - 100) < 0.5, f'bredderne giver {sum(bredder)} %'
    hoved = ''.join(f'<th>{html.escape(k)}</th>' for k in kolonner)
    krop = ''
    for r in raekker:
        celler = (f'<td class="fagnavn">{html.escape(r)}</td>' if r else '<td></td>')
        celler += '<td></td>' * (len(kolonner) - 1)
        krop += f'<tr style="height:{hoejde}">{celler}</tr>'
    stil = ''.join(f'<col style="width:{b}%">' for b in bredder)
    return (f'<table class="skema"><colgroup>{stil}</colgroup>'
            f'<thead><tr>{hoved}</tr></thead><tbody>{krop}</tbody></table>')


dybde_html = ''
for nr in (1, 2):
    felter = ''
    for navn, hint, n, to in DYBDE:
        if to:
            felter += (f'<div class="felt"><span class="mrk">{html.escape(navn)}'
                       f'</span><div class="todelt">'
                       + ''.join(f'<div><span class="und">{html.escape(t)}</span>'
                                 f'{linjer(n)}</div>' for t in to)
                       + '</div></div>')
        else:
            h = f' <span class="hint">{html.escape(hint)}</span>' if hint else ''
            felter += (f'<div class="felt"><span class="mrk">'
                       f'{html.escape(navn)}</span>{h}{linjer(n)}</div>')
    dybde_html += (f'<section class="dybde"><h3>Fag {nr}: '
                   f'<span class="udfyld"></span></h3>{felter}</section>')

CSS = '''
*{box-sizing:border-box}
body{margin:0;font-family:Helvetica,Arial,sans-serif;color:#1a2233;
font-size:10pt;line-height:1.35}
h1{font-size:16pt;margin:0 0 1mm}
h2{font-size:11.5pt;margin:4mm 0 2mm;padding-bottom:1mm;
border-bottom:1.5px solid #1a2233}
h3{font-size:10.5pt;margin:0 0 2mm}
.und,.hint{color:#586074;font-weight:400}
.hint{font-size:8.5pt;font-style:italic}
.topline{display:flex;justify-content:space-between;align-items:baseline;
color:#586074;font-size:9pt;margin-bottom:3mm}
.felter{display:flex;gap:4mm;margin:0 0 4mm}
.felter > div{flex:1}
.felter .mrk{display:block;font-size:8pt;letter-spacing:.4px;
text-transform:uppercase;color:#586074;margin-bottom:1mm}
.udfyld{display:block;border-bottom:1px solid #1a2233;height:7mm}
.figur{margin:3mm 0 4mm}
.figur svg{display:block;width:100%}
.foer{border:1px solid #c9d2e0;border-left:4px solid #1f6fd6;border-radius:3mm;
padding:3mm 5mm;margin:0 0 4mm;background:#f6f8fc}
.foer ol{margin:0;padding-left:5mm}
.foer li{margin:1.5mm 0;font-size:9.5pt}
table.skema{width:100%;border-collapse:collapse;margin:0 0 3mm}
table.skema th,table.skema td{border:1px solid #9aa4b5;padding:1.5mm 2mm;
text-align:left;vertical-align:top}
table.skema th{background:#eef2f8;font-size:8pt;letter-spacing:.4px;
text-transform:uppercase;color:#586074;font-weight:700}
table.skema td.fagnavn{font-weight:700;background:#f6f8fc;font-size:9.5pt}
.pil{color:#9aa4b5;font-size:9pt;white-space:nowrap}
.dybde{border:1px solid #c9d2e0;border-radius:3mm;padding:2mm 5mm 0.5mm;
margin:0 0 2mm}
.dybde h3 .udfyld{display:inline-block;width:62%;height:5mm;vertical-align:-1mm}
.felt{margin:0 0 0.5mm}
.felt .mrk{font-size:8pt;letter-spacing:.4px;text-transform:uppercase;
color:#586074;font-weight:700}
.todelt{display:flex;gap:4mm}
.todelt > div{flex:1}
.linjer{margin-top:1mm;background-image:repeating-linear-gradient(to bottom,
transparent 0,transparent 6.3mm,#c9d2e0 6.3mm,#c9d2e0 6.5mm)}
.side2{page-break-before:always}
footer{margin-top:2mm;border-top:1px solid #c9d2e0;padding-top:1.5mm;
color:#586074;font-size:8pt;display:flex;justify-content:space-between}
@page{size:A4;margin:12mm}
'''

FELTER = ['Elev', 'Klasse', 'Dato', 'Kl.', 'Til stede']

foer_html = ''.join(f'<li>{t}</li>' for t in FOER)

KROP = f'''
<div class="topline"><span>Skole-hjem-samtale · fagligt fokus</span>
<span>{MINUTTER} minutter · ét ark pr. elev</span></div>
<h1>Samtaleark</h1>
<div class="felter">
{''.join(f'<div><span class="mrk">{f}</span><span class="udfyld"></span></div>'
         for f in FELTER)}
</div>
<div class="figur">{FG.tidsplan(TIDSPLAN, W=700)}</div>
<div class="foer"><ol>{foer_html}</ol></div>
<h2>Alle otte fag</h2>
{skema(OVERSIGT_KOL, FAG, hoejde='19mm', bredder=[16, 23, 20, 18, 23])}
<div class="side2"></div>
<h2>De valgte fag · i dybden</h2>
{dybde_html}
<h2>Aftaler</h2>
{skema(AFTALER_KOL, AFTALER_RAEKKER, hoejde='10mm', bredder=[54, 26, 20])}
<div class="felter" style="margin-top:2mm">
<div><span class="mrk">Vi følger op</span><span class="udfyld"></span></div>
<div><span class="mrk">Underskrift · skole</span><span class="udfyld"></span></div>
<div><span class="mrk">Underskrift · hjem</span><span class="udfyld"></span></div>
</div>
<footer><span>9. klasse · Mibelibsen</span>
<span>Udfyldt ark indeholder personoplysninger — opbevares ikke på sitet.</span>
</footer>'''

DOK = ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
       '<title>Samtaleark · skole-hjem</title><style>' + CSS
       + '</style></head><body>' + KROP + '</body></html>')

os.makedirs(os.path.dirname(UD_HTML), exist_ok=True)
open(UD_HTML, 'w', encoding='utf-8').write(DOK)
subprocess.run(['node', os.path.join(ROD, 'claude', 'html_til_pdf.mjs'),
                UD_HTML, UD_PDF], check=True)
os.remove(UD_HTML)
print(f'skrevet:  {UD_PDF}')
print(f'{len(FAG)} fag · {MINUTTER} min · '
      f'{" + ".join(str(m) for _, m in TIDSPLAN)}')
