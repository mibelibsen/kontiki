# -*- coding: utf-8 -*-
"""Bygger broekregning.html — de fire regnearter med broeker.

Alle broeker regnes med fractions.Fraction, og scriptet skriver ikke siden,
hvis et eksempel ikke stemmer.
"""
import sys, os, html
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figurer as FG

UD = 'broekregning.html'


def frac(t, n):
    """Broek som HTML med vandret broekstreg — samme .frac som paa sitet."""
    return f'<span class="frac"><span>{t}</span><span>{n}</span></span>'


def vis(f):
    if f.denominator == 1:
        return str(f.numerator)
    return frac(f.numerator, f.denominator)


# ------------------------------------------------------------- regnearterne
# (nr, titel, regel, regnestykke som html, facit, figur)
def plus_eksempel():
    a, b = F(1, 3), F(1, 4)
    faelles = 12
    assert a + b == F(7, 12) and a == F(4, faelles) and b == F(3, faelles)
    fig = (FG.broekbjaelke(4, 12, tekst='1/3 = 4/12') +
           FG.broekbjaelke(3, 12, farve=FG.ORA, tekst='1/4 = 3/12') +
           FG.broekbjaelke(7, 12, farve=FG.GRO, tekst='lagt sammen: 7/12'))
    stykke = (f'{frac(1,3)} + {frac(1,4)} = {frac(4,12)} + {frac(3,12)} = '
              f'{frac(7,12)}')
    return stykke, a + b, fig


def gange_eksempel():
    a, b = F(2, 3), F(3, 4)
    assert a * b == F(1, 2) and F(2 * 3, 3 * 4) == F(1, 2)
    fig = FG.broekgitter(2, 3, 3, 4)
    stykke = (f'{frac(2,3)} · {frac(3,4)} = {frac("2 · 3","3 · 4")} = '
              f'{frac(6,12)} = {frac(1,2)}')
    return stykke, a * b, fig


def divider_eksempel():
    a, b = F(3, 4), F(2, 5)
    assert a / b == F(15, 8) and a * F(5, 2) == F(15, 8)
    stykke = (f'{frac(3,4)} : {frac(2,5)} = {frac(3,4)} · {frac(5,2)} = '
              f'{frac(15,8)}')
    return stykke, a / b, ''


def forkort_eksempel():
    assert F(18, 24) == F(3, 4)
    fig = (FG.broekbjaelke(18, 24, tekst='18/24', vis_dele=False) +
           FG.broekbjaelke(3, 4, farve=FG.GRO, tekst='samme mængde: 3/4'))
    stykke = f'{frac(18,24)} = {frac("18 : 6","24 : 6")} = {frac(3,4)}'
    return stykke, F(18, 24), fig


TRIN = [
 ('Forlæng og forkort', 'Gang eller dividér <b>begge</b> tal med det samme. '
  'Brøken ser anderledes ud, men er lige så stor.', *forkort_eksempel()),
 ('Plus og minus', 'Lav først om til <b>samme nævner</b>. Læg så tællerne '
  'sammen — nævneren bliver stående.', *plus_eksempel()),
 ('Gange', 'Tæller gange tæller, nævner gange nævner. Ingen fælles nævner '
  'nødvendig.', *gange_eksempel()),
 ('Dividere', 'Vend den bagerste brøk om, og gang i stedet.',
  *divider_eksempel()),
]

# ------------------------------------------------------------------ omregning
OMREGN = [(F(3, 4), '0,75', '75 %'), (F(1, 3), '0,333…', '33,3 %'),
          (F(5, 8), '0,625', '62,5 %'), (F(7, 10), '0,7', '70 %')]
for f, _, _ in OMREGN:
    assert 0 < f < 1

FAELDER = [
 ('Man lægger ikke nævnere sammen',
  f'{frac(1,2)} + {frac(1,3)} er <b>ikke</b> {frac(2,5)}. Det er '
  f'{frac(3,6)} + {frac(2,6)} = {frac(5,6)}. Prøv med tal: en halv pizza plus '
  'en tredjedel er mere end en halv — og {} er mindre.'.format(frac(2, 5)),
  F(1, 2) + F(1, 3) == F(5, 6) and F(2, 5) < F(1, 2)),
 ('Den største nævner er ikke den største brøk',
  f'{frac(1,8)} er mindre end {frac(1,3)}. Jo flere dele kagen deles i, jo '
  'mindre bliver hver del.',
  F(1, 8) < F(1, 3)),
 ('Brøkstregen betyder dividér',
  f'{frac(3,4)} er det samme som 3 : 4 = 0,75. Det er tit den nemmeste vej, '
  'når du skal bruge en decimal.',
  F(3, 4) == F(3) / F(4)),
 ('En hel er en brøk med samme tal',
  f'{frac(5,5)} = 1 og {frac(12,12)} = 1. Og {frac(8,4)} = 2 — en uægte brøk '
  'er bare et tal større end 1.',
  F(5, 5) == 1 and F(12, 12) == 1 and F(8, 4) == 2),
]
for navn, _, ok in FAELDER:
    assert ok, navn

trin_html = ''
for i, (titel, regel, stykke, facit, fig) in enumerate(TRIN, 1):
    figur = f'<div class="figur">{fig}</div>' if fig else ''
    trin_html += (f'<section class="regel"><h3><span class="num">{i}</span>'
                  f'{html.escape(titel)}</h3><p>{regel}</p>'
                  f'<div class="stykke">{stykke}</div>{figur}</section>')

omregn_html = ''.join(
    f'<tr><td class="ud">{vis(f)}</td><td>{d}</td><td>{p}</td></tr>'
    for f, d, p in OMREGN)
faelder_html = ''.join(
    f'<section class="regel faelde"><h3>{html.escape(navn)}</h3><p>{tekst}</p>'
    f'</section>' for navn, tekst, _ in FAELDER)

BASIS = open('matematik.html').read()
CSS = BASIS[BASIS.find('<style>') + 7:BASIS.find('</style>')]
CSS += '''
.frac{display:inline-block;vertical-align:middle;text-align:center;
line-height:1.16;font-size:.92em;margin:0 .18em}
.frac>span{display:block;padding:0 .32em;white-space:nowrap}
.frac>span:first-child{border-bottom:1.6px solid currentColor;padding-bottom:.05em}
.frac>span:last-child{padding-top:.05em}
.figur{background:var(--panel2);border:1px solid var(--line);border-radius:12px;
padding:14px;margin:12px 0;text-align:center}
.figur svg{max-width:100%;height:auto;display:block;margin:6px auto}
.regel{background:var(--panel);border:1px solid var(--line);
border-left:5px solid var(--accent);border-radius:14px;padding:18px 22px;
margin:14px 0;box-shadow:var(--shadow)}
.regel.faelde{border-left-color:var(--warn)}
.regel h3{margin:0 0 8px;font-size:1.15rem;display:flex;align-items:center;gap:11px}
.regel .num{width:28px;height:28px;border-radius:8px;display:grid;place-items:center;
font-weight:800;font-size:.9rem;background:var(--accent);color:#fff;flex:0 0 auto}
.regel p{margin:0;color:var(--muted);font-size:.97rem;max-width:74ch}
.stykke{background:var(--accent-soft);border:1px solid var(--line);
border-radius:10px;padding:14px 18px;margin:12px 0;font-size:1.22rem;
text-align:center;color:#111;overflow-x:auto}
table.om{width:100%;border-collapse:collapse;margin:12px 0;font-size:1rem;max-width:460px}
table.om th,table.om td{border:1px solid var(--line);padding:9px 14px;text-align:left}
table.om th{background:var(--panel2)}
table.om td.ud{font-weight:700}
.printbtn{background:#fff;border:1px solid var(--line);border-radius:10px;
padding:10px 18px;font-weight:700;font-size:.95rem;cursor:pointer;color:var(--ink);
font-family:inherit;margin:6px 8px 0 0}
.printbtn:hover{border-color:var(--accent);color:var(--accent)}
@media print{header.top,.printbtn,.btnlink{display:none!important}
.regel,.figur{box-shadow:none;break-inside:avoid}body{font-size:11pt}
main{padding:0}@page{size:A4;margin:14mm}}
'''

KROP = f'''<section class="hero"><span class="pill">Matematik · Regneregler</span>
<h1>Brøkregning</h1>
<p>De fire regnearter med brøker, én ad gangen, med en figur til hver. Nederst
står de fælder, der koster flest point ved prøven.</p>
<button class="printbtn" onclick="window.print()">Print siden</button>
<a class="btnlink ghost" href="regnepyramiden.html">Regnepyramiden</a>
<a class="btnlink ghost" href="matematik.html">Tilbage til matematik</a></section>

<div class="note"><b>Husk hvad de to tal hedder:</b> tallet over stregen er
<b>tælleren</b> — den tæller, hvor mange dele du har. Tallet under er
<b>nævneren</b> — den nævner, hvor mange dele det hele er delt i.</div>
<div class="figur">{FG.broekbjaelke(3, 4, tekst='3/4 — tre dele ud af fire')}</div>

<h2 class="sec">De fire regnearter</h2>
{trin_html}

<h2 class="sec">Brøk, decimaltal og procent</h2>
<p class="mat">Det er det samme tal skrevet på tre måder. Divider tælleren med
nævneren, så har du decimaltallet — gang med 100, så har du procenten.</p>
<table class="om"><thead><tr><th>Brøk</th><th>Decimaltal</th><th>Procent</th>
</tr></thead><tbody>{omregn_html}</tbody></table>

<h2 class="sec">Fælder</h2>
{faelder_html}

<div class="note"><b>Tjek dig selv:</b> regn {frac(2,5)} + {frac(1,10)}.
Fælles nævner er 10, så {frac(2,5)} = {frac(4,10)}, og {frac(4,10)} +
{frac(1,10)} = {frac(5,10)} = {frac(1,2)}.</div>
<button class="printbtn" onclick="window.print()">Print siden</button>'''

assert F(2, 5) + F(1, 10) == F(1, 2) and F(2, 5) == F(4, 10)

DOK = ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
       '<meta name="viewport" content="width=device-width,initial-scale=1">'
       '<title>Brøkregning · 9. klasse</title><style>' + CSS +
       '</style></head><body><header class="top"><div class="top-inner">'
       '<a class="brand" href="index.html">Mibelibsen <span>9. klasse</span></a>'
       '<nav class="tabs"><a class="active" href="matematik.html">Matematik</a>'
       '<a class="" href="samfundsfag.html">Samfundsfag</a>'
       '<a class="" href="tysk.html">Tysk</a><span class="soon">Fysik</span>'
       '</nav></div></header><main>' + KROP + '</main><footer>'
       'Undervisningsmateriale · 9. klasse · Mibelibsen.</footer></body></html>')
open(UD, 'w').write(DOK)
print(f'skrevet:  {UD}  ·  {len(TRIN)} regnearter, {len(FAELDER)} fælder')
