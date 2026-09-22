# -*- coding: utf-8 -*-
"""Bygger regnepyramiden.html — rækkefølgen i regnestykker og de simple regler.

Alle tal på siden er regnet efter med brøkregning, også de forkerte svar, så et
eksempel ikke kommer til at lære ungerne noget forkert.
"""
import sys, os, html
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figurer as FG

UD = 'regnepyramiden.html'

LAG = [('Parenteser', 'Alt inde i en parentes først', FG.BLA),
       ('Potenser og rødder', '3² og √9', FG.GRO),
       ('Gange og dividere', 'Fra venstre mod højre', FG.ORA),
       ('Plus og minus', 'Fra venstre mod højre', FG.ROD)]

# (udtryk, rigtigt, hvorfor, forkert, hvorfor det forkerte sker)
EKSEMPLER = [
 ('2 + 3 · 4', 2 + 3 * 4, 'Gange står højere end plus, så 3 · 4 gøres først.',
  (2 + 3) * 4, 'hvis man bare regner forfra'),
 ('(2 + 3) · 4', (2 + 3) * 4, 'Parentesen er øverst i pyramiden.',
  2 + 3 * 4, 'hvis man overser parentesen'),
 ('12 − 4 + 2', 12 - 4 + 2,
  'Plus og minus står i samme lag — så gælder venstre mod højre.',
  12 - (4 + 2), 'hvis man tager plusset først'),
 ('2 · 3²', 2 * 3 ** 2, 'Potensen står højere end gange: 3² = 9 først.',
  (2 * 3) ** 2, 'hvis man ganger, før man kvadrerer'),
 ('100 : 5 : 2', F(100, 5) / 2,
  'Gange og dividere er samme lag — venstre mod højre.',
  F(100) / F(5, 2), 'hvis man tager den sidste division først'),
 ('20 − 3 · 2²', 20 - 3 * 2 ** 2, 'Først 2² = 4, så 3 · 4 = 12, så 20 − 12.',
  ((20 - 3) * 2) ** 2, 'hvis man regner hele stykket forfra'),
]
for u, r, _, f, _ in EKSEMPLER:
    assert r != f, u                     # et eksempel skal vise en forskel

REGLER = [
 ('Brøkstregen er en parentes',
  '<code>(12 + 6) : 3 = 6</code>, og det er også det, brøkstregen betyder. '
  'Regn tælleren færdig først. <code>12 + 6 : 3 = 14</code> er noget andet.',
  F(12 + 6, 3) == 6 and 12 + F(6, 3) == 14),
 ('Minus foran en parentes vender alle fortegn',
  '<code>−(4 + 3) = −4 − 3 = −7</code>. Minusset gælder <b>hvert</b> led inde '
  'i parentesen, ikke kun det første.',
  -(4 + 3) == -4 - 3 == -7),
 ('Et tal uden for en parentes ganges ind på alle led',
  '<code>2 · (5 + 3) = 2 · 5 + 2 · 3 = 16</code>. Du kan regne parentesen '
  'først eller gange ind — svaret er det samme.',
  2 * (5 + 3) == 2 * 5 + 2 * 3 == 16),
 ('To minusser giver plus',
  '<code>7 − (−3) = 7 + 3 = 10</code> og <code>(−2) · (−5) = 10</code>. '
  'Ét minus alene giver stadig minus: <code>(−2) · 5 = −10</code>.',
  7 - (-3) == 10 and (-2) * (-5) == 10 and (-2) * 5 == -10),
 ('Potens er gange med sig selv',
  '<code>3² = 3 · 3 = 9</code>. Det er <b>ikke</b> 3 · 2 = 6. Det er den '
  'hyppigste fejl med potenser.',
  3 ** 2 == 9 and 3 * 2 == 6),
 ('0 og 1 opfører sig særligt',
  '<code>0 · 9 = 0</code>, <code>9 · 1 = 9</code>, <code>9 : 1 = 9</code>. '
  'Og du må aldrig dividere med 0 — det har intet svar.',
  0 * 9 == 0 and 9 * 1 == 9 and F(9, 1) == 9),
]
for navn, _, ok in REGLER:
    assert ok, navn                       # reglen er regnet efter, ikke skrevet af


def dk(x):
    if isinstance(x, F) and x.denominator == 1:
        x = int(x)
    if isinstance(x, int):
        return f'{x:,}'.replace(',', '.')
    return f'{float(x):.2f}'.rstrip('0').rstrip('.').replace('.', ',')


pyramide = FG.pyramide(LAG)

eks_html = ''.join(
    f'<tr><td class="ud">{u}</td><td class="rigtig">{dk(r)}</td>'
    f'<td>{html.escape(hvorfor)}</td>'
    f'<td class="forkert">{dk(f)} <span>— {html.escape(nar)}</span></td></tr>'
    for u, r, hvorfor, f, nar in EKSEMPLER)

regler_html = ''.join(
    f'<section class="regel"><h3>{html.escape(navn)}</h3><p>{tekst}</p></section>'
    for navn, tekst, _ in REGLER)

BASIS = open('matematik.html').read()
CSS = BASIS[BASIS.find('<style>') + 7:BASIS.find('</style>')]
CSS += '''
.figur{background:var(--panel2);border:1px solid var(--line);border-radius:14px;
padding:18px;margin:18px 0;text-align:center}
.figur svg{max-width:100%;height:auto}
table.eks{width:100%;border-collapse:collapse;margin:14px 0;font-size:.96rem}
table.eks th,table.eks td{border:1px solid var(--line);padding:10px 12px;
text-align:left;vertical-align:top}
table.eks th{background:var(--panel2);white-space:nowrap}
table.eks td.ud{font-family:Consolas,"Courier New",monospace;font-size:1.05rem;
white-space:nowrap;color:#111}
table.eks td.rigtig{font-weight:800;color:var(--good);white-space:nowrap}
table.eks td.forkert{color:var(--muted);white-space:nowrap}
table.eks td.forkert span{color:#9aa6ba;font-size:.85rem;white-space:normal}
.regel{background:var(--panel);border:1px solid var(--line);
border-left:5px solid var(--accent);border-radius:14px;padding:16px 20px;
margin:12px 0;box-shadow:var(--shadow)}
.regel h3{margin:0 0 6px;font-size:1.1rem}
.regel p{margin:0;color:var(--muted);font-size:.97rem;max-width:74ch}
code{font-family:Consolas,"Courier New",monospace;background:var(--panel2);
border:1px solid var(--line);border-radius:6px;padding:2px 7px;color:#111}
.printbtn{background:#fff;border:1px solid var(--line);border-radius:10px;
padding:10px 18px;font-weight:700;font-size:.95rem;cursor:pointer;color:var(--ink);
font-family:inherit;margin:6px 8px 0 0}
.printbtn:hover{border-color:var(--accent);color:var(--accent)}
@media print{header.top,.printbtn,.btnlink{display:none!important}
.regel,.figur{box-shadow:none;break-inside:avoid}body{font-size:11pt}
main{padding:0}@page{size:A4;margin:14mm}}
'''

KROP = f'''<section class="hero"><span class="pill">Matematik · Regneregler</span>
<h1>Regnepyramiden</h1>
<p>Når der står flere regnearter i det samme stykke, er der én rækkefølge, der
er den rigtige. Pyramiden viser den: øverst gøres først. Nederst på siden står
de simple regler, der driller flest.</p>
<button class="printbtn" onclick="window.print()">Print siden</button>
<a class="btnlink ghost" href="matematik.html">Tilbage til matematik</a></section>

<div class="figur">{pyramide}</div>

<div class="note"><b>To ting, pyramiden ikke siger med det samme:</b> står to
regnearter i <b>samme</b> lag — fx gange og dividere — regner du dem fra
<b>venstre mod højre</b>. Og en parentes inden i en parentes regnes indefra og ud.</div>

<h2 class="sec"><span class="num">1</span> Se forskellen</h2>
<p class="mat">Den sidste søjle er det svar, man får, hvis man ikke følger
pyramiden. Læg mærke til hvor stor forskellen bliver.</p>
<table class="eks"><thead><tr><th>Stykke</th><th>Rigtigt</th><th>Hvorfor</th>
<th>Forkert svar</th></tr></thead><tbody>{eks_html}</tbody></table>

<h2 class="sec"><span class="num">2</span> De simple regler</h2>
{regler_html}

<div class="note"><b>Tjek dig selv:</b> regn <code>5 + 2 · (8 − 6)²</code> uden
lommeregner, og brug pyramiden lag for lag. Parentesen giver 2, potensen giver 4,
gange giver 8, og til sidst 5 + 8 = <b>13</b>.</div>
<button class="printbtn" onclick="window.print()">Print siden</button>'''

assert 5 + 2 * (8 - 6) ** 2 == 13        # facit i noten er regnet efter

DOK = ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
       '<meta name="viewport" content="width=device-width,initial-scale=1">'
       '<title>Regnepyramiden · 9. klasse</title><style>' + CSS +
       '</style></head><body><header class="top"><div class="top-inner">'
       '<a class="brand" href="index.html">Mibelibsen <span>9. klasse</span></a>'
       '<nav class="tabs"><a class="active" href="matematik.html">Matematik</a>'
       '<a class="" href="samfundsfag.html">Samfundsfag</a>'
       '<a class="" href="tysk.html">Tysk</a><a class="" href="fysik.html">Fysik</a>'
       '</nav></div></header><main>' + KROP + '</main><footer>'
       'Undervisningsmateriale · 9. klasse · Mibelibsen.</footer></body></html>')
open(UD, 'w').write(DOK)
print(f'skrevet:  {UD}  ·  {len(LAG)} lag, {len(EKSEMPLER)} eksempler, '
      f'{len(REGLER)} regler')
