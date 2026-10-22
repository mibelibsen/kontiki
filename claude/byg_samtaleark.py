# -*- coding: utf-8 -*-
"""Bygger vejledning/skolehjemsamtale.pdf — skabelon til en samtale paa 30 min.

Ét ark pr. barn. Fokus er fagligt: hvor staar hun, hvad er maalet, og hvad
skal der til - i skolen, hjemme og hos barnet selv.

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

# Barnet faar halvdelen af baandet. De tre andre dele deler den anden
# halvdel. Det staar ingen steder paa arket - baandet er en tegning, ikke en
# instruks - men den blaa blok er lige saa bred som de tre andre tilsammen,
# og den ligger forrest. Den, der ser arket, kan se, hvem der skal tale.
#
# Tallene staar ikke paa figuren (tal=False). Et minuttal paa en farve goer
# baandet til et skema, man skal overholde; uden tal er det et forhold.
TIDSPLAN = [
    ('Barnet selv', 15),
    ('Overblik', 4),
    ('Fokusfag', 7),
    ('Aftaler', 4),
]
assert sum(m for _, m in TIDSPLAN) == MINUTTER
_barnet = TIDSPLAN[0][1]
assert _barnet * 2 == MINUTTER, 'barnet skal have praecis halvdelen'
assert sum(m for _, m in TIDSPLAN[1:]) == _barnet, 'de tre deler den anden halvdel'

FAG = ['Dansk', 'Matematik', 'Fysik/kemi', 'Samfundsfag',
       'Historie', 'Engelsk', 'Tysk', 'Idræt']

OVERSIGT_KOL = ['Fag', 'Standpunkt', 'Barnets vurdering']

# Stoette i skolen, hjemme og hos barnet selv er det samme spoergsmaal stillet
# tre steder: hvad skal der til. De staar derfor i én raekke med tre kolonner -
# det goer det tydeligt, at de tre ting skal haenge sammen.
DYBDE = [
    ('Standpunkt', 'faglige områder', 2, None),
    ('Mål', 'Hvad er det næste skridt', 2, None),
    ('Hvad skal der til?', '', 4, ('I skolen', 'Hjemme', 'Barn')),
]

AFTALER_KOL = ['Aftale', 'Hvem gør det', 'Hvornår']
AFTALER_RAEKKER = 3

# To tomme blokke. De har ingen numre: de to fag vaelges under samtalen, og
# et nummer ved siden af et fag ligner en rangordning.
FOKUS_BLOKKE = 2


def linjer(n):
    """n skrivelinjer. De tegnes én ad gangen og ikke som et gentaget
    baggrundsmoenster: et moenster bliver klippet af feltets hoejde, og saa
    staar der tre linjer ét sted og to et andet, alt efter hvor en brudt
    millimeter falder. Her er der praecis n, hver gang."""
    return ('<div class="linjer">'
            + '<div class="linje"></div>' * n
            + '</div>')


def skema(kolonner, raekker, hoejde='14mm', bredder=None):
    """Et tomt skema. `raekker` er enten et tal eller en liste af tekster,
    der staar i foerste kolonne. `bredder` er procenter - uden dem fordeler
    browseren kolonnerne efter overskrifternes laengde, og saa bliver
    "Fag" bred og "Standpunkt" smal uden grund."""
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
for _ in range(FOKUS_BLOKKE):
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
    dybde_html += (f'<section class="dybde"><h3>Fag: '
                   f'<span class="udfyld"></span></h3>{felter}</section>')

CSS = '''
*{box-sizing:border-box}
body{margin:0;font-family:Helvetica,Arial,sans-serif;color:#1a2233;
font-size:10pt;line-height:1.35}
h1{font-size:16pt;margin:0 0 1mm}
h2{font-size:11.5pt;margin:5mm 0 2mm;padding-bottom:1mm;
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
.figur{margin:4mm 0 2mm}
.figur svg{display:block;width:100%}
table.skema{width:100%;border-collapse:collapse;margin:0 0 3mm}
table.skema th,table.skema td{border:1px solid #9aa4b5;padding:1.5mm 2mm;
text-align:left;vertical-align:top}
table.skema th{background:#eef2f8;font-size:8pt;letter-spacing:.4px;
text-transform:uppercase;color:#586074;font-weight:700}
table.skema td.fagnavn{font-weight:700;background:#f6f8fc;font-size:9.5pt}
.dybde{border:1px solid #c9d2e0;border-radius:3mm;padding:3mm 5mm 1mm;
margin:0 0 3mm}
.dybde h3 .udfyld{display:inline-block;width:62%;height:5mm;vertical-align:-1mm}
.felt{margin:0 0 1mm}
.felt .mrk{font-size:8pt;letter-spacing:.4px;text-transform:uppercase;
color:#586074;font-weight:700}
.todelt{display:flex;gap:4mm}
.todelt > div{flex:1}
.linjer{margin-top:1mm}
.linje{height:7mm;border-bottom:0.2mm solid #c9d2e0}
.side2{page-break-before:always}
@page{size:A4;margin:12mm}
'''

FELTER = ['Barn', 'Klasse', 'Dato', 'Kl.', 'Til stede']

KROP = f'''
<div class="topline"><span>Skole-hjem-samtale · fagligt fokus</span>
<span>{MINUTTER} minutter · ét ark pr. barn</span></div>
<h1>Samtaleark</h1>
<div class="felter">
{''.join(f'<div><span class="mrk">{f}</span><span class="udfyld"></span></div>'
         for f in FELTER)}
</div>
<div class="figur">{FG.tidsplan(TIDSPLAN, W=700, tal=False)}</div>
<h2>Alle otte fag</h2>
{skema(OVERSIGT_KOL, FAG, hoejde='24mm', bredder=[17, 45, 38])}
<div class="side2"></div>
<h2>Fokusfag</h2>
{dybde_html}
<h2>Aftaler</h2>
{skema(AFTALER_KOL, AFTALER_RAEKKER, hoejde='15mm', bredder=[54, 26, 20])}'''

DOK = ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
       '<title>Samtaleark · skole-hjem</title><style>' + CSS
       + '</style></head><body>' + KROP + '</body></html>')

os.makedirs(os.path.dirname(UD_HTML), exist_ok=True)
open(UD_HTML, 'w', encoding='utf-8').write(DOK)
subprocess.run(['node', os.path.join(ROD, 'claude', 'html_til_pdf.mjs'),
                UD_HTML, UD_PDF], check=True)
os.remove(UD_HTML)
print(f'skrevet:  {UD_PDF}')
print(f'{len(FAG)} fag · {MINUTTER} min · barnet selv {_barnet} af {MINUTTER}')
