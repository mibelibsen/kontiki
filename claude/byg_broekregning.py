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
    stykke = (f'{frac(1,3)} + {frac(1,4)} = {frac("1 · 4","3 · 4")} + '
              f'{frac("1 · 3","4 · 3")} = {frac(4,12)} + {frac(3,12)} = '
              f'{frac("4 + 3","12")} = {frac(7,12)}')
    return stykke, a + b, fig


def faellesnaevner_eksempel():
    """Forlaengning aendrer ikke maengden. Det er hele begrundelsen for,
    at man overhovedet maa lave om til faellesnaevner, og den skal kunne
    ses — derfor to bjaelker med praecis samme farvede laengde."""
    assert F(1, 3) == F(4, 12) and F(1, 4) == F(3, 12)
    fig = (FG.broekbjaelke(1, 3, tekst='1/3') +
           FG.broekbjaelke(4, 12, farve=FG.GRO,
                           tekst='1/3 forlænget med 4: 4/12 — samme længde'))
    stykke = (f'{frac(1,3)} = {frac("1 · 4","3 · 4")} = {frac(4,12)}')
    return stykke, F(1, 3), fig


# (de to nævnere, fællesnævner, hvad hver ganges med, hvorfor)
FAELLES = [
 (2, 8, 8, (4, 1), 'Den ene går op i den anden: 2 går op i 8. '
  'Så er den største af dem fællesnævneren, og den anden brøk står allerede rigtigt.'),
 (3, 4, 12, (4, 3), 'Ingen af dem går op i den anden. Gang nævnerne: '
  '3 · 4 = 12. Det virker altid.'),
 (6, 4, 12, (2, 3), 'Nævnerne ganget giver 24, og det kan bruges — men 12 '
  'er mindre og går også op i begge. Mindre tal gør resten lettere.'),
]
for a, b, f, (ga, gb), _ in FAELLES:
    assert a * ga == f and b * gb == f, (a, b, f)
    assert f % a == 0 and f % b == 0

FAELLES_TABEL_RAEKKER = ''.join(
    f'<tr><td>{frac(1,a)} + {frac(1,b)}</td><td class="ud"><b>{f}</b></td>'
    f'<td>{a} · {ga} = {f}<br>{b} · {gb} = {f}</td><td>{hvorfor}</td></tr>'
    for a, b, f, (ga, gb), hvorfor in FAELLES)

FAELLES_TABEL = (
    '<p class="naar">Sådan finder du den — tre tilfælde, og de dækker alt:</p>'
    '<table class="om fn"><thead><tr><th>Stykket</th><th>Fællesnævner</th>'
    '<th>Hvad ganges med hvad</th><th>Hvorfor</th></tr></thead>'
    '<tbody>' + FAELLES_TABEL_RAEKKER + '</tbody></table>'
    '<p class="naar"><b>Og så forlænger du:</b> spørg «hvad skal nævneren '
    'ganges med for at blive fællesnævneren?» — og gang tælleren med '
    'præcis det samme tal. Gør du kun det ene, har du ændret brøken.</p>')


def gange_eksempel():
    a, b = F(2, 3), F(3, 4)
    assert a * b == F(1, 2) and F(2 * 3, 3 * 4) == F(1, 2)
    fig = FG.broekgitter(2, 3, 3, 4)
    stykke = (f'{frac(2,3)} · {frac(3,4)} = {frac("2 · 3","3 · 4")} = '
              f'{frac(6,12)} = {frac(1,2)}')
    return stykke, a * b, fig


def divider_eksempel():
    """Division med en broek skal foerst betyde noget, foer reglen giver
    mening. Derfor to eksempler: det lette, hvor svaret kan taelles, og
    det almindelige, hvor det ikke kan."""
    a, b = F(3, 4), F(2, 5)
    assert a / b == F(15, 8) and a * F(5, 2) == F(15, 8)
    assert F(3, 4) / F(1, 4) == 3, 'det lette eksempel skal gaa lige op'
    # at dividere med et tal under 1 goer svaret stoerre — det er pointen
    assert b < 1 and a / b > a
    fig = (FG.gaar_op_i(3, 4, 1, 4) + FG.gaar_op_i(3, 4, 2, 5))
    stykke = (f'{frac(3,4)} : {frac(2,5)} = {frac(3,4)} · {frac(5,2)} = '
              f'{frac("3 · 5","4 · 2")} = {frac(15,8)} = 1{frac(7,8)}')
    return stykke, a / b, fig


def forkort_eksempel():
    assert F(18, 24) == F(3, 4)
    fig = (FG.broekbjaelke(18, 24, tekst='18/24', vis_dele=False) +
           FG.broekbjaelke(3, 4, farve=FG.GRO, tekst='samme mængde: 3/4'))
    stykke = f'{frac(18,24)} = {frac("18 : 6","24 : 6")} = {frac(3,4)}'
    return stykke, F(18, 24), fig


TRIN = [
 ('Forlæng og forkort', 'Gang eller dividér <b>begge</b> tal med det samme. '
  'Brøken ser anderledes ud, men er lige så stor.', *forkort_eksempel()),
 ('Find fællesnævneren',
  '<b>Reglen:</b> du må gange tæller og nævner med det samme tal. Brøken '
  'får nye tal, men er præcis lige så stor. Det er dét, der gør det '
  'lovligt at skrive brøkerne om, før du lægger dem sammen.',
  *faellesnaevner_eksempel(), FAELLES_TABEL),
 ('Plus og minus', 'Når nævnerne er ens, lægger du <b>tællerne</b> sammen. '
  'Nævneren bliver stående — den fortæller kun, hvor store delene er, og '
  'den ændrer sig ikke, fordi du tager flere af dem.',
  *plus_eksempel()),
 ('Gange', 'Tæller gange tæller, nævner gange nævner. Ingen fælles nævner '
  'nødvendig.', *gange_eksempel()),
 ('Dividere',
  '<b>Hvad det betyder:</b> et divisionsstykke spørger, hvor mange gange '
  'det bagerste tal går op i det forreste. {} : {} spørger altså: hvor '
  'mange kvarte er der i tre kvarte? Svaret er 3, og det kan tælles på '
  'den første figur.<br><br>'
  '<b>Reglen:</b> vend den bagerste brøk om, og gang i stedet. Den '
  'omvendte brøk hedder den <b>reciprokke</b> — tæller og nævner bytter '
  'plads, så {} bliver til {}.<br><br>'
  '<b>Hvorfor det virker:</b> at dividere med 2 er det samme som at gange '
  'med {}. At dividere med {} er på samme måde det samme som at gange med '
  '{}. Division og multiplikation er to sider af samme sag, og den '
  'omvendte brøk er broen imellem dem.'.format(
      frac(3, 4), frac(1, 4), frac(2, 5), frac(5, 2),
      frac(1, 2), frac(2, 5), frac(5, 2)),
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
 ('Dividerer du med noget under 1, bliver svaret større',
  f'{frac(3,4)} : {frac(2,5)} = {frac(15,8)}, som er <b>større</b> end '
  f'{frac(3,4)}. Det føles forkert, men er rigtigt: du spørger, hvor '
  f'mange gange noget lille går op i noget større — og det gør det mere '
  'end én gang. Samme sag som 10 : 0,5 = 20.',
  F(3, 4) / F(2, 5) > F(3, 4) and F(10) / F(1, 2) == 20),
 ('En hel er en brøk med samme tal',
  f'{frac(5,5)} = 1 og {frac(12,12)} = 1. Og {frac(8,4)} = 2 — en uægte brøk '
  'er bare et tal større end 1.',
  F(5, 5) == 1 and F(12, 12) == 1 and F(8, 4) == 2),
]
for navn, _, ok in FAELDER:
    assert ok, navn

trin_html = ''
for i, trin in enumerate(TRIN, 1):
    titel, regel, stykke, facit, fig = trin[:5]
    ekstra = trin[5] if len(trin) > 5 else ''      # tabel e.l. under figuren
    figur = f'<div class="figur">{fig}</div>' if fig else ''
    trin_html += (f'<section class="regel"><h3><span class="num">{i}</span>'
                  f'{html.escape(titel)}</h3><p>{regel}</p>'
                  f'<div class="stykke">{stykke}</div>{figur}{ekstra}</section>')

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
table.om.fn{max-width:none;font-size:.95rem}
table.om.fn td:last-child{color:var(--muted);font-size:.9rem}
table.om.fn td{vertical-align:top}
table.om.fn td:first-child{white-space:nowrap;min-width:7.5em}
p.naar{color:var(--muted);max-width:74ch;margin:10px 0}
.regel p.naar{margin:14px 0 6px}
.note{background:var(--panel2);border:1px solid var(--line);
border-left:5px solid var(--accent);border-radius:12px;padding:14px 18px;
margin:14px 0;color:var(--muted);max-width:76ch}
.note b{color:var(--ink)}
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
<p>Først hvad de to tal hedder, så fællesnævneren og reglen bag den, og
derefter de fire regnearter — én ad gangen, med en figur til hver. Nederst
står de fælder, der koster flest point ved prøven.</p>
<button class="printbtn" onclick="window.print()">Print siden</button>
<a class="btnlink ghost" href="regnepyramiden.html">Regnepyramiden</a>
<a class="btnlink ghost" href="matematik.html">Tilbage til matematik</a></section>

<h2 class="sec">Hvad hedder de to tal?</h2>
<p class="naar">Ordene bruges hele året, så de skal sidde fast. De er ikke
tilfældige — begge ord siger, hvad tallet gør.</p>
<div class="figur">{FG.broek_navne(3, 4)}</div>
<div class="note"><b>Tælleren <i>tæller</i></b>, hvor mange dele du har.
<b>Nævneren <i>nævner</i></b>, hvor mange dele det hele er delt i.<br><br>
Derfor bliver en brøk <b>mindre</b>, når nævneren bliver større:
{frac(1,8)} er mindre end {frac(1,3)}, fordi kagen er skåret i flere og
dermed mindre stykker. Og derfor er {frac(5,5)} lig med 1 — du har alle
de dele, der findes.</div>

<h2 class="sec">Regnereglerne, én ad gangen</h2>
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
       '<a class="brand" href="index.html">321flyv · <span>9. klasse</span></a>'
       '<nav class="tabs"><a class="active" href="matematik.html">Matematik</a>'
       '<a class="" href="samfundsfag.html">Samfundsfag</a>'
       '<a class="" href="tysk.html">Tysk</a><a class="" href="fysik.html">Fysik</a>'
       '</nav></div></header><main>' + KROP + '</main><footer>'
       'Undervisningsmateriale · 9. klasse.</footer></body></html>')
open(UD, 'w').write(DOK)
print(f'skrevet:  {UD}  ·  {len(TRIN)} regnearter, {len(FAELDER)} fælder')
