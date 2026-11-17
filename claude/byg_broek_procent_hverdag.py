# -*- coding: utf-8 -*-
"""Bygger broek-procent-hverdag.html — uge 47 i matematik.

Aarsplanens maal for ugen: regne med procent i virkelighedsnaere opgaver,
loese opgaver med broeker, og **forklare beregninger og loesninger**. Det
sidste er det, der tit mangler til proeven, saa siden har et helt afsnit
om, hvordan en forklaring skrives.

Alle tal regnes med fractions.Fraction og kontrolleres af asserts. Et
eksempel, der ikke stemmer, stopper bygningen.

    python3 claude/byg_broek_procent_hverdag.py
"""
import html
import os
import sys
from fractions import Fraction as F

HER = os.path.dirname(os.path.abspath(__file__))
ROD = os.path.dirname(HER)
sys.path.insert(0, HER)
import figurer as FG

UD = os.path.join(ROD, 'broek-procent-hverdag.html')


def kr(x):
    """Kroner med dansk komma. Beloeb vises med to decimaler, naar de har
    dem — ellers ser 299,00 kr unoedigt teknisk ud."""
    f = F(x)
    if f.denominator == 1:
        return f'{f.numerator:,}'.replace(',', '.') + ' kr'
    return f'{float(f):,.2f}'.replace(',', '#').replace('.', ',').replace('#', '.') + ' kr'


def pct(f):
    """Procent uden unoedige nuller: 12,5 % men 30 %."""
    v = float(F(f) * 100)
    s = f'{v:.2f}'.rstrip('0').rstrip('.')
    return s.replace('.', ',') + ' %'


def frac(t, n):
    return f'<span class="frac"><span>{t}</span><span>{n}</span></span>'


# ===================================================== de tre spørgsmål
# Hver procentopgave er ét af tre spørgsmål. Kender man dem, kan man
# vælge regnestykke uden at gætte.
DEL, HELE = 420, 1200
assert F(DEL, HELE) == F(7, 20) and F(DEL, HELE) * 100 == 35

PCT_AF, TAL = F(35, 100), 1200
assert PCT_AF * TAL == 420

TILBAGE_DEL, TILBAGE_PCT = 420, F(35, 100)
assert TILBAGE_DEL / TILBAGE_PCT == 1200

TRE = [
 ('Hvor mange procent er delen af det hele?',
  f'{DEL} ud af {HELE}',
  f'{DEL} ÷ {HELE} = {FG._dk(float(F(DEL, HELE)))} → {pct(F(DEL, HELE))}',
  'Del med det hele, og gang med 100. Det er den mest almindelige, og '
  'den der oftest bliver vendt om: husk at dele med <b>det hele</b>, '
  'ikke med delen.',
  FG.svarprocent(HELE, DEL, tekst=f'{DEL} af {HELE} elever')),
 ('Hvad er en bestemt procent af et tal?',
  f'{pct(PCT_AF)} af {TAL}',
  f'{TAL} · {FG._dk(float(PCT_AF))} = {DEL}',
  'Lav procenten om til et decimaltal, og gang. 35 % bliver til 0,35 — '
  'flyt kommaet to pladser til venstre.',
  FG.broekbjaelke(7, 20, tekst='35 % = 7/20 af det hele')),
 ('Hvad var det hele?',
  f'{DEL} er {pct(TILBAGE_PCT)} — hvad er 100 %?',
  f'{DEL} ÷ {FG._dk(float(TILBAGE_PCT))} = {TAL}',
  'Den sværeste, fordi man skal <b>dividere</b>, hvor man plejer at '
  'gange. Spørg dig selv: er svaret større end det, jeg startede med? '
  'Det skal det være, når procenten er under 100.',
  FG.broekbjaelke(7, 20, farve=FG.ORA,
                  tekst='kender 35 % — mangler de sidste 65 %')),
]
assert len(TRE) == 3


# ================================================== eksempler fra hverdagen
def _ex(situation, stykke, svar, forklaring, figur, fif=''):
    return dict(situation=situation, stykke=stykke, svar=svar,
                forklaring=forklaring, figur=figur, fif=fif)


# 1 udsalg
PRIS, RABAT = 399, F(30, 100)
assert PRIS * RABAT == F(11970, 100) and PRIS * (1 - RABAT) == F(27930, 100)
# 2 moms baglaens
MED_MOMS, MOMS = 625, F(25, 100)
assert MED_MOMS / (1 + MOMS) == 500
assert MED_MOMS * (1 - MOMS) != 500, 'den klassiske fælde skal være forkert'
# 3 opskrift
FLOEDE, PERS_FRA, PERS_TIL = F(3, 4), 4, 10
assert FLOEDE * F(PERS_TIL, PERS_FRA) == F(15, 8)
# 4 data
BRUGT, DATA = 14, 20
assert F(BRUGT, DATA) == F(7, 10) and F(DATA - BRUGT, DATA) * 100 == 30
# 5 loen
LOEN, STIGNING = 142, F(45, 1000)
assert LOEN * (1 + STIGNING) == F(14839, 100)

EKSEMPLER = [
 _ex('En trøje koster 399 kr. Der er 30 % rabat på udsalget. '
     'Hvad kommer den til at koste?',
     f'{PRIS} · 0,30 = {kr(PRIS * RABAT)} i rabat<br>'
     f'{PRIS} − {kr(PRIS * RABAT)} = {kr(PRIS * (1 - RABAT))}',
     kr(PRIS * (1 - RABAT)),
     'Rabatten er 30 % <i>af prisen</i>, så den regnes af 399. Bagefter '
     'trækkes den fra. Du kan også gøre det i ét hug: betaler du ikke de '
     '30 %, betaler du de 70 % — og 399 · 0,70 giver samme svar.',
     FG.broekbjaelke(70, 100, tekst='du betaler 70 % af prisen',
                     vis_dele=False),
     'Ét regnestykke i stedet for to: 399 · 0,70.'),

 _ex('En vare koster 625 kr med moms. Momsen er 25 %. '
     'Hvad er prisen uden moms?',
     f'{MED_MOMS} ÷ 1,25 = {kr(MED_MOMS / (1 + MOMS))}',
     kr(MED_MOMS / (1 + MOMS)),
     'Her er 625 kr <b>det hele</b> — altså 125 % af prisen uden moms. '
     'Derfor skal der <b>divideres</b>. Det er spørgsmål 3 fra før: '
     'du kender en del og skal finde helheden.',
     FG.broekbjaelke(4, 5, farve=FG.GRO,
                     tekst='100 af 125 dele = 4 af 5 dele'),
     f'<b>Fælden:</b> 625 · 0,75 = {kr(MED_MOMS * (1 - MOMS))}. '
     'Det er forkert — momsen er lagt oven på de 500, ikke trukket fra '
     'de 625.'),

 _ex(f'En opskrift til {PERS_FRA} personer bruger {frac(3, 4)} dl fløde. '
     f'I skal være {PERS_TIL}. Hvor meget fløde?',
     f'{frac(3, 4)} · {frac(PERS_TIL, PERS_FRA)} = {frac(30, 16)} = '
     f'{frac(15, 8)} = 1{frac(7, 8)} dl',
     f'{frac(15, 8)} dl, altså knap 1,9 dl',
     'Opskriften skal ganges med forholdet mellem de to '
     'personantal. Gang tæller med tæller og nævner med nævner, og '
     'forkort til sidst.',
     FG.broekgitter(3, 4, PERS_TIL, PERS_FRA),
     'Tjek rimeligheden: I er lidt over dobbelt så mange, så svaret '
     'skal være lidt over dobbelt så meget. 1,9 passer.'),

 _ex(f'Du har brugt {BRUGT} GB af dine {DATA} GB data. '
     'Hvor mange procent har du tilbage?',
     f'{DATA} − {BRUGT} = {DATA - BRUGT} GB tilbage<br>'
     f'{frac(DATA - BRUGT, DATA)} = {frac(3, 10)} = 0,30 → 30 %',
     '30 %',
     'Spørgsmålet er, hvor meget der er <b>tilbage</b> — ikke hvor meget '
     'der er brugt. Find resten først, og del så med det hele.',
     FG.svarprocent(DATA, DATA - BRUGT, tekst='6 GB tilbage af 20 GB'),
     'Læs spørgsmålet to gange. Brugt og tilbage er to forskellige tal.'),

 _ex(f'Din timeløn er {LOEN} kr og stiger {pct(STIGNING)}. '
     'Hvad bliver den nye løn?',
     f'{LOEN} · 1,045 = {kr(LOEN * (1 + STIGNING))}',
     kr(LOEN * (1 + STIGNING)),
     'En stigning på 4,5 % betyder, at du får de 100 % du havde, '
     '<b>plus</b> 4,5 % — altså 104,5 % i alt. Gang med 1,045.',
     FG.soejler([LOEN, float(LOEN * (1 + STIGNING))],
                ['før', 'efter'], titel='Timeløn i kr', ynavn='kr',
                W=360, H=240, farve=[FG.MUT, FG.GRO]),
     'Tallet 1,045 hedder en <b>vækstfaktor</b>. Den arbejder I videre '
     'med i næste uge.'),
]
assert len(EKSEMPLER) == 5


# ======================================================== brøker i hverdagen
BROEK_HVERDAG = [
 (frac(3, 4) + ' time', '45 minutter',
  f'{frac(3,4)} af 60 minutter: 60 · 0,75 = 45'),
 (frac(2, 3) + ' af klassen', '18 af 27 elever',
  f'{frac(2,3)} af 27: 27 ÷ 3 = 9, og 9 · 2 = 18'),
 ('Forholdet 2 : 3', frac(2, 5) + ' og ' + frac(3, 5),
  'To dele og tre dele er fem dele i alt — derfor er nævneren 5, ikke 3'),
 (frac(1, 8) + ' af en pizza', '12,5 %',
  f'1 ÷ 8 = 0,125 → 12,5 %'),
]
assert F(3, 4) * 60 == 45 and F(2, 3) * 27 == 18 and F(1, 8) * 100 == F(25, 2)


# =================================================================== fælder
R1, R2 = F(30, 100), F(20, 100)
SAMLET = 1 - (1 - R1) * (1 - R2)
assert SAMLET == F(44, 100) and SAMLET != R1 + R2
NED, OP = F(20, 100), F(20, 100)
assert (1 - NED) * (1 + OP) == F(96, 100)

FAELDER = [
 ('To rabatter lægges ikke sammen',
  f'30 % rabat og derefter 20 % mere er <b>ikke</b> 50 %. Den anden '
  f'rabat regnes af den pris, der allerede er sat ned.<br>'
  f'0,70 · 0,80 = 0,56 — du betaler 56 %, så rabatten er '
  f'<b>{pct(SAMLET)}</b>.',
  FG.broekbjaelke(56, 100, farve=FG.ORA,
                  tekst='du betaler 56 % til sidst', vis_dele=False)),
 ('Ned og op med samme procent rammer ikke samme sted',
  'Falder en pris 20 % og stiger 20 % igen, er den <b>ikke</b> tilbage.'
  '<br>0,80 · 1,20 = 0,96 — den er 4 % lavere end før. '
  'De 20 % ned blev regnet af et større tal end de 20 % op.',
  FG.soejler([100, 80, 96], ['start', 'efter fald', 'efter stigning'],
             titel='Samme procent ned og op', ynavn='indeks',
             W=420, H=240, farve=[FG.MUT, FG.ROD, FG.ORA])),
 ('Procent af hvad?',
  'Et procenttal betyder ingenting, før man ved, hvad det er en '
  'procent <b>af</b>. Stiger noget fra 4 % til 6 %, er det en '
  'stigning på <b>2 procentpoint</b> — men på <b>50 %</b>. '
  'Begge dele er rigtige, og de lyder meget forskelligt.',
  FG.procentpoint(4, 6)),
]


# ========================================== forklar beregningen (årsplanmål)
FORKLAR = [
 ('Skriv hvad du leder efter',
  'Begynd med et ord, ikke et tal: <i>Jeg skal finde prisen efter '
  'rabat.</i> Så ved du selv, hvilket af de tre spørgsmål det er.'),
 ('Skriv regnestykket med enheder',
  'Ikke <i>399 · 0,7</i>, men <i>399 kr · 0,70 = 279,30 kr</i>. '
  'Enhederne afslører halvdelen af fejlene: ender du med kr i et '
  'svar, der skulle være en procent, er der noget galt.'),
 ('Sig hvorfor du ganger eller dividerer',
  'Én sætning er nok: <i>Jeg ganger, fordi jeg skal finde en del af '
  'det hele.</i> Eller: <i>Jeg dividerer, fordi jeg kender delen og '
  'skal finde det hele.</i>'),
 ('Slut med at vurdere svaret',
  'Er det rimeligt? En trøje til 399 kr kan ikke koste 1.330 kr efter '
  'rabat. Det tjek fanger de fleste tastefejl — og det er et af '
  'årets mål, så det tæller.'),
]


# ================================================================== opgaver
# (nr, opgave, facit, forklaring til facitarket, figur)
def _o(nr, opgave, facit, hvordan, figur):
    return (nr, opgave, facit, hvordan, figur)


assert F(2400) * F(85, 100) == 2040
assert F(34, 40) * 100 == 85
assert F(480) / F(80, 100) == 600
assert F(3, 8) * 24 == 9
assert F(5995) / F(125, 100) == 4796
assert F(2, 3) * F(9, 6) == 1
assert F(20) * F(55, 100) == 11
assert F(29 - 25, 25) * 100 == 16

OPGAVER = [
 _o(1, 'En cykel koster 2.400 kr. Der er 15 % rabat. Hvad koster den nu?',
    '2.040 kr', '2400 · 0,85 = 2040. Du betaler de 85 %, du ikke får rabat på.',
    FG.broekbjaelke(15, 100, farve=FG.ROD, vis_dele=False,
                    tekst='15 % rabat af de 2.400 kr')),
 _o(2, 'Du har svaret rigtigt på 34 ud af 40 spørgsmål. Hvor mange procent?',
    '85 %', '34 ÷ 40 = 0,85 → 85 %. Del med det hele, gang med 100.',
    FG.broekbjaelke(34, 40, vis_dele=False, tekst='34 rigtige af 40')),
 _o(3, 'En bluse koster 480 kr <b>efter</b> 20 % rabat. '
       'Hvad kostede den før?',
    '600 kr', '480 ÷ 0,80 = 600. De 480 kr er 80 % af den gamle pris, '
    'så der divideres.',
    FG.broekbjaelke(20, 100, farve=FG.ROD, vis_dele=False,
                     tekst='20 % blev taget af — 480 kr er det, der er tilbage')),
 _o(4, f'{frac(3, 8)} af en klasse på 24 spiller fodbold. Hvor mange er det?',
    '9 elever', '24 ÷ 8 = 3, og 3 · 3 = 9. Del med nævneren, gang med tælleren.',
    FG.broekbjaelke(3, 8, tekst='3/8 af klassen')),
 _o(5, 'En computer koster 5.995 kr med moms. Momsen er 25 %. '
       'Hvad er prisen uden moms?',
    '4.796 kr', '5995 ÷ 1,25 = 4796. Prisen med moms er 125 % af prisen uden.',
    FG.broekbjaelke(25, 125, farve=FG.ORA, vis_dele=False,
                     tekst='momsen er 25 % oven på prisen uden moms')),
 _o(6, f'En opskrift til 6 personer bruger {frac(2, 3)} dl olie. '
       'Hvor meget skal der bruges til 9 personer?',
    '1 dl', '2/3 · 9/6 = 2/3 · 3/2 = 1. Gang med forholdet mellem antallene.',
    FG.broekbjaelke(2, 3, tekst='opskriften: 2/3 dl olie til 6 personer')),
 _o(7, 'Du har 20 GB data og har brugt 45 %. Hvor mange GB har du tilbage?',
    '11 GB', '100 % − 45 % = 55 %, og 20 · 0,55 = 11. Find resten først.',
    FG.broekbjaelke(45, 100, farve=FG.ROD, vis_dele=False,
                    tekst='45 % af de 20 GB er brugt')),
 _o(8, 'En biografbillet stiger fra 25 kr til 29 kr. '
       'Hvor mange procent er stigningen?',
    '16 %', 'Stigningen er 4 kr. 4 ÷ 25 = 0,16 → 16 %. Del med den '
    '<b>gamle</b> pris, ikke den nye.',
    FG.soejler([25, 29], ['før', 'efter'], titel='Pris i kr', ynavn='kr',
               W=330, H=230, farve=[FG.MUT, FG.GRO])),
 _o(9, 'I en butik er der først 30 % rabat, og på udsalgets sidste dag '
       'tages der 20 % mere af den nedsatte pris. Hvor stor er den '
       'samlede rabat?',
    '44 %', '0,70 · 0,80 = 0,56. Du betaler 56 %, så rabatten er 44 % — '
    'ikke 50 %.',
    FG.broekbjaelke(30, 100, farve=FG.ROD, vis_dele=False,
                     tekst='først tages 30 % af prisen')),
 _o(10, 'En vare falder 20 % i pris. Senere stiger den 20 %. '
        'Koster den det samme som før? Forklar.',
     'Nej — den er 4 % billigere end før',
     '0,80 · 1,20 = 0,96. Faldet blev regnet af den høje pris, '
     'stigningen af den lave. Derfor rammer de ikke samme sted.',
     FG.soejler([100, 80], ['start', 'efter 20 % fald'],
                titel='Indeks', ynavn='indeks', W=340, H=230,
                farve=[FG.MUT, FG.ROD])),
]
assert len(OPGAVER) == 10
assert all(fig.startswith('<svg') for *_, fig in OPGAVER)


def _tal(s):
    """Tallene i en tekst. Broeker som 2/3 taeller ikke med, og danske
    tusindtalspunktummer fjernes, saa 2.040 bliver til 2040."""
    import re as _re
    s = _re.sub(r'\d+/\d+', ' ', s)
    s = _re.sub(r'(?<=\d)\.(?=\d{3}\b)', '', s)
    return {int(t) for t in _re.findall(r'\b\d+\b', s)}


for _nr, _opg, _facit, _hvordan, _fig in OPGAVER:
    import re as _re
    _figtekst = ' '.join(_re.findall(r'>([^<>]*)</text>', _fig))
    _laekket = _tal(_facit) & _tal(_figtekst)
    assert not _laekket, (
        f'opgave {_nr}: figuren røber facit — tallet {_laekket} står både i '
        f'svaret «{_facit}» og i figuren «{_figtekst.strip()}»')


# =================================================================== siden
BASIS = open(os.path.join(ROD, 'matematik.html'), encoding='utf-8').read()
CSS = BASIS[BASIS.find('<style>') + 7:BASIS.find('</style>')] + '''
.frac{display:inline-block;vertical-align:middle;text-align:center;
line-height:1.16;font-size:.92em;margin:0 .18em}
.frac>span{display:block;padding:0 .32em;white-space:nowrap}
.frac>span:first-child{border-bottom:1.6px solid currentColor;padding-bottom:.05em}
.frac>span:last-child{padding-top:.05em}
h2.sec{font-size:1.3rem;margin:34px 0 10px;padding-top:12px;
border-top:2px solid var(--ink)}
.mat{max-width:70ch;color:var(--muted)}
.kort3{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));
margin:14px 0}
.sp{border:1px solid var(--line);border-radius:14px;padding:16px 18px;background:#fff}
.sp h3{margin:0 0 4px;font-size:1rem}
.sp .regn{font-family:ui-monospace,Menlo,Consolas,monospace;background:var(--panel2);
border-radius:8px;padding:8px 10px;margin:8px 0;font-size:.92rem}
.sp p{color:var(--muted);font-size:.93rem;margin:6px 0 0}
.sp svg{width:100%;height:auto;margin-top:10px}
.ex{border:1px solid var(--line);border-left:5px solid var(--accent);
border-radius:12px;padding:16px 20px;margin:16px 0;background:#fff}
.ex .sit{font-weight:600;max-width:66ch}
.ex .regn{font-family:ui-monospace,Menlo,Consolas,monospace;
background:var(--panel2);border-radius:8px;padding:10px 12px;margin:10px 0;
display:inline-block}
.ex .svar{font-weight:800;color:var(--ok,#1a8f5e)}
.ex .fork{color:var(--muted);max-width:68ch;margin:8px 0 0}
.ex .fif{background:var(--panel2);border-radius:8px;padding:8px 12px;
margin-top:10px;font-size:.92rem;color:var(--muted);max-width:68ch}
.ex figure{margin:12px 0 0;text-align:center}
.ex svg{max-width:460px;width:100%;height:auto}
table.hv{width:100%;border-collapse:collapse;margin:12px 0;font-size:.96rem}
table.hv th,table.hv td{border:1px solid var(--line);padding:9px 11px;
text-align:left;vertical-align:top}
table.hv th{background:var(--panel2)}
table.hv td:last-child{color:var(--muted);font-size:.92rem}
ol.forklar{max-width:70ch;padding-left:22px}
ol.forklar li{margin:12px 0}
ol.forklar b{display:block}
ol.forklar span{color:var(--muted)}
.faelde{border:1px solid var(--line);border-left:5px solid #c23b4b;
border-radius:12px;padding:16px 20px;margin:14px 0;background:#fff}
.faelde h3{margin:0 0 6px;font-size:1.02rem}
.faelde p{color:var(--muted);max-width:68ch;margin:0}
.faelde svg{max-width:420px;width:100%;height:auto;margin-top:10px}
.opg{border-top:1px solid var(--line);padding:18px 0 6px;max-width:72ch}
.opg .nr{color:var(--accent);font-weight:800;margin-right:8px}
.opg svg{max-width:400px;width:100%;height:auto;margin:10px 0 0}
@media print{header.top,.printbtn{display:none!important}
.ex,.sp,.faelde,.opg{break-inside:avoid}@page{size:A4;margin:14mm}}
'''

tre_html = ''.join(
    f'<div class="sp"><h3>{i}. {html.escape(t)}</h3>'
    f'<div class="regn">{sp}<br>{regn}</div><p>{fork}</p>{fig}</div>'
    for i, (t, sp, regn, fork, fig) in enumerate(TRE, 1))

eks_html = ''.join(
    f'<div class="ex"><p class="sit">{e["situation"]}</p>'
    f'<div class="regn">{e["stykke"]}</div>'
    f'<p>Svar: <span class="svar">{e["svar"]}</span></p>'
    f'<p class="fork">{e["forklaring"]}</p>'
    + (f'<div class="fif">{e["fif"]}</div>' if e['fif'] else '')
    + f'<figure>{e["figur"]}</figure></div>' for e in EKSEMPLER)

hv_html = ''.join(
    f'<tr><td>{a}</td><td><b>{b}</b></td><td>{c}</td></tr>'
    for a, b, c in BROEK_HVERDAG)

forklar_html = ''.join(
    f'<li><b>{html.escape(t)}</b><span>{tekst}</span></li>'
    for t, tekst in FORKLAR)

faelder_html = ''.join(
    f'<div class="faelde"><h3>{html.escape(t)}</h3><p>{tekst}</p>{fig}</div>'
    for t, tekst, fig in FAELDER)

opg_html = ''.join(
    f'<div class="opg"><p><span class="nr">{nr}.</span>{opg}</p>{fig}</div>'
    for nr, opg, _, _, fig in OPGAVER)

KROP = f'''<section class="hero"><span class="pill">9. klasse · matematik ·
uge 47</span><h1>Brøker og procent i hverdagen</h1>
<p class="mat">Procent er tre spørgsmål, ikke tredive regler. Kan du kende
dem fra hinanden, kan du regne opgaverne — og forklare, hvorfor du gjorde
det, du gjorde. Det sidste tæller lige så meget til prøven.</p>
<button class="printbtn" onclick="window.print()">Print siden</button></section>

<h2 class="sec">De tre spørgsmål</h2>
<p class="mat">Al procentregning er ét af disse tre. Find ud af hvilket,
før du regner — så er resten mekanik.</p>
<div class="kort3">{tre_html}</div>

<h2 class="sec">Fem situationer fra hverdagen</h2>
<p class="mat">Samme tre spørgsmål, pakket ind i noget, der ligner noget.
Læg mærke til, hvad der er <i>det hele</i> i hver opgave — det er dér, de
fleste fejl opstår.</p>
{eks_html}

<h2 class="sec">Brøker, du møder uden at tænke over det</h2>
<table class="hv"><thead><tr><th>Det du hører</th><th>Det det er</th>
<th>Sådan regnes det</th></tr></thead><tbody>{hv_html}</tbody></table>

<h2 class="sec">Sådan forklarer du en beregning</h2>
<p class="mat">Et rigtigt svar uden forklaring giver ikke fuldt udbytte til
prøven. Fire linjer er nok:</p>
<ol class="forklar">{forklar_html}</ol>

<h2 class="sec">Tre fælder</h2>
{faelder_html}

<h2 class="sec">Opgaver</h2>
<p class="mat">Ti opgaver. Skriv regnestykket <b>og</b> en sætning om,
hvorfor du regner sådan — det er dét, der øves her. Facit får I af
læreren.</p>
{opg_html}
<button class="printbtn" onclick="window.print()">Print siden</button>'''

DOK = ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
       '<meta name="viewport" content="width=device-width,initial-scale=1">'
       '<title>Brøker og procent i hverdagen · 9. klasse</title><style>'
       + CSS + '</style></head><body><header class="top"><div class="top-inner">'
       '<a class="brand" href="index.html">321flyv · <span>9. klasse</span></a>'
       '<nav class="tabs"><a class="active" href="matematik.html">Matematik</a>'
       '<a class="" href="samfundsfag.html">Samfundsfag</a>'
       '<a class="" href="tysk.html">Tysk</a><a class="" href="fysik.html">Fysik</a>'
       '</nav></div></header><main>' + KROP + '</main><footer>'
       'Undervisningsmateriale · 9. klasse · uge 47.</footer></body></html>')

FACIT_KROP = ''.join(
    f'<tr><td class="nr">{nr}</td><td>{opg}</td>'
    f'<td class="sv">{facit}</td><td class="hv">{hvordan}</td></tr>'
    for nr, opg, facit, hvordan, _ in OPGAVER)

FACIT = ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
         '<title>Facit · Brøker og procent i hverdagen</title><style>'
         'body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",'
         'Arial,sans-serif;color:#1a2233;font-size:11pt;line-height:1.45;'
         'margin:0}h1{font-size:19pt;margin:0 0 4px}'
         'p.intro{color:#586074;margin:0 0 16px;max-width:60em}'
         'table{border-collapse:collapse;width:100%;font-size:10pt}'
         'th,td{border:1px solid #c9d2e0;padding:7px 9px;text-align:left;'
         'vertical-align:top}th{background:#f3f6fb}'
         'td.nr{width:2.6em;text-align:right;color:#586074}'
         'td.sv{width:9em;font-weight:700}td.hv{color:#586074}'
         '.frac{display:inline-block;text-align:center;line-height:1.1;'
         'font-size:.9em;vertical-align:middle}'
         '.frac>span{display:block;padding:0 .3em}'
         '.frac>span:first-child{border-bottom:1.4px solid currentColor}'
         'tr{break-inside:avoid}@page{size:A4;margin:16mm}'
         '</style></head><body>'
         '<h1>Facit · Brøker og procent i hverdagen</h1>'
         '<p class="intro">De ti opgaver fra siden, uge 47. Kolonnen til '
         'højre er ikke bare svaret, men den forklaring, eleverne selv '
         'skal kunne skrive — det er ugens tredje mål.</p>'
         '<table><thead><tr><th>#</th><th>Opgave</th><th>Svar</th>'
         '<th>Sådan regnes det</th></tr></thead><tbody>'
         + FACIT_KROP + '</tbody></table></body></html>')


if __name__ == '__main__':
    open(UD, 'w', encoding='utf-8').write(DOK)
    # facit skrives som midlertidig html og laves til PDF af
    # html_til_pdf.mjs — html-filen bliver ikke liggende i facit/
    import subprocess
    navn = 'facit-online-2026-11-16-broek-procent-hverdag'
    tmp = os.path.join(ROD, 'facit', navn + '.html')
    fsti = os.path.join(ROD, 'facit', navn + '.pdf')
    open(tmp, 'w', encoding='utf-8').write(FACIT)
    subprocess.run(['node', os.path.join(HER, 'html_til_pdf.mjs'), tmp, fsti],
                   check=True, capture_output=True)
    os.remove(tmp)
    print(f'skrevet:  broek-procent-hverdag.html  ·  {len(EKSEMPLER)} eksempler, '
          f'{len(OPGAVER)} opgaver, {DOK.count("<svg")} figurer, {len(DOK)//1024} kB')
    print(f'skrevet:  {os.path.relpath(fsti, ROD)}')
