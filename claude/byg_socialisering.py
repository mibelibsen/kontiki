#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bygger ART-forløbet om vredeshåndtering på /socialisering.

    python3 claude/byg_socialisering.py <scratch-mappe>

Skriver:
    socialisering.html                     siden
    <scratch>/art-materialesaet.html       hele materialet sat til print
    <scratch>/art-rollespilskort.html      fire kort til udklip, A4
    <scratch>/art-arbejdsark.html          vredeslog og observatørskema

Materialet står ét sted nedenfor — LEKTIONSPLAN, TEGN, DAEMPERE, KORT,
LOG og OBSERVATION. Siden, PDF'erne og Word-udgaven bygges alle af de samme
lister, så et rollespilskort ikke kan stå på siden og mangle i udklipsarket.

Kortene trykkes med bagsiden vendt 180 grader under forsiden. Så klippes
kortet ud i ét stykke og foldes på midten — ingen dobbeltsidet print, der
skal passe sammen.
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figurer as FG                                         # noqa: E402

SCRATCH = sys.argv[1] if len(sys.argv) > 1 else '.'
ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROD)

# ===================================================== 1 · selve materialet

KAEDEN = [
    ('Udløseren', 'Det, der sker udefra eller indeni — en bemærkning, en '
     'uretfærdighed, en tanke.', 'foer'),
    ('Kropslige tegn', 'Det kroppen gør, før du når at tænke: puls, varme, '
     'spændt kæbe, knyttede næver.', 'i_dag'),
    ('Dæmpere', 'Det, der sænker arousal med det samme: vejrtrækning, tælle '
     'baglæns, et indre billede.', 'i_dag'),
    ('Påmindelser', 'Sætninger til dig selv, der holder dig på sporet: '
     '«Bevar roen», «Det er ikke værd at slås om».', 'efter'),
    ('Tænk fremad', 'Hvad sker der bagefter, hvis jeg gør det her? Og hvis jeg '
     'lader være?', 'efter'),
    ('Brug en færdighed', 'Sig det i stedet: klag ordentligt, forhandl, gå væk '
     'med besked.', 'efter'),
    ('Vurder dig selv', 'Hvad gik godt? Hvad gør jeg anderledes næste gang?',
     'efter'),
]
KAEDE_FARVER = {'foer': FG.MUT, 'i_dag': FG.GRO, 'efter': '#aeb6c4'}

LEKTIONSPLAN = [
    ('00–05', 'Velkomst og opstart',
     ['Dagsorden på tavlen.',
      'Kort opfølgning på sidste uges udløsere.']),
    ('05–15', 'Kropslige tegn',
     ['Oplæg: krop og hjerne reagerer, før tanken gør.',
      'Brainstorm på tavlen om fysiske advarselssignaler: puls, varme, kæbe, '
      'næver, mave.']),
    ('15–25', 'Dæmpere',
     ['Introduktion til de tre dæmpere.',
      'Fælles afprøvning af vejrtrækningen — alle prøver, også trænerne.']),
    ('25–40', 'Rollespil og træning',
     ['Trænerne modellerer et kort scenarium med højttænkning.',
      'Parvis træning ud fra rollespilskortene.',
      'Feedback fra gruppen og fra observatøren.']),
    ('40–45', 'Evaluering og opgave',
     ['Vredesloggen udleveres.',
      'Hjemmeopgave: registrér én episode med kropsligt tegn og dæmper.']),
]

TEGN = [
    ('Kæben spænder, tænderne bides sammen', 0.11, -1),
    ('Varme i ansigtet, rødme', 0.15, 1),
    ('Hjertet banker hurtigere', 0.30, -1),
    ('Vejrtrækningen bliver kort og høj', 0.36, 1),
    ('Knude i maven', 0.48, -1),
    ('Næverne knytter sig', 0.62, 1),
    ('Skuldrene trækkes op', 0.26, 1),
    ('Uro i benene, trang til at gå', 0.78, -1),
]

DAEMPERE = [
    ('4-4-4-vejrtrækning',
     'Ind gennem næsen i fire sekunder, hold i fire, ud gennem munden i fire. '
     'Tre omgange. Den lange udånding er dét, der virker — den sænker pulsen.'),
    ('Tælle baglæns',
     'Tæl langsomt fra 10 eller 20 ned mod 0 inde i hovedet. Baglæns kræver '
     'opmærksomhed, og opmærksomheden kan ikke være to steder på én gang.'),
    ('Indre billede og selvinstruktion',
     'Se et billede for dig, der betyder stop — et rødt skilt, en bremse — og '
     'sig én sætning til dig selv: «Bevar roen».'),
]

KORT = [
    ('Den uretfærdige anklage',
     'Skole, institution eller arbejdsplads',
     'En opgave eller ting mangler, og lederen eller underviseren antyder, at '
     'det er din skyld.',
     'Sig med en bestemt tone: «Det er altid dig, der glemmer at aflevere '
     'tingene eller rydde op! Hvorfor har du lagt det forkert igen?»',
     ['Registrér varmen i ansigtet eller de knyttede næver.',
      'Tag 1–2 dybe vejrtrækninger med 4-4-4.',
      'Svar med rolig stemme uden at gå i forsvar.']),
    ('Sprunget over i køen',
     'Kantinen, supermarkedet eller busstoppestedet',
     'Du har ventet i kø i flere minutter. En person går direkte ind foran dig '
     'uden at spørge.',
     'Stil dig foran med ryggen til, kig på din telefon, og lad som om der '
     'overhovedet ikke står nogen bag dig.',
     ['Registrér spændingen i kæben eller knuden i maven.',
      'Tæl langsomt baglæns fra 10 til 1 inde i hovedet.',
      'Henvend dig høfligt: «Undskyld, jeg stod i kø her.»']),
    ('Afbrudt i en forklaring',
     'Gruppearbejde, møde eller en samtale i pausen',
     'Du er ved at forklare noget vigtigt, men bliver afbrudt midt i en '
     'sætning.',
     'Tal højlydt hen over hovedpersonen midt i en sætning: «Ej, prøv lige at '
     'høre her i stedet, det her er meget vigtigere…»',
     ['Mærk impulsen til at afbryde igen eller råbe.',
      'Dyb udånding, og forestil dig et rødt STOP-skilt.',
      'Vent på en pause og sig: «Jeg var lige ved at tale færdig, bagefter vil '
      'jeg gerne høre din idé.»']),
    ('Spydig bemærkning',
     'Omklædningsrum, frikvarter eller pauserum',
     'Du træder ind i rummet, og nogen kommenterer dit tøj eller noget, du '
     'lige har gjort.',
     'Grin kort og sig spydigt: «Hvad er det lige, du har taget på i dag? '
     'Prøver du at starte en ny mode, eller hvad?»',
     ['Registrér hjertebanken eller et stik af ubehag.',
      'Brug selvinstruktionen «Det er ikke værd at slås om» sammen med en dyb '
      'vejrtrækning.',
      'Træk på skuldrene, eller giv et kort, afvæbnende svar.']),
]

LOG_KOLONNER = [
    ('1. Hvad var udløseren?', 'Blev afbrudt af en kammerat.'),
    ('2. Hvad mærkede du i kroppen?', 'Spændt kæbe, varm i ansigtet.'),
    ('3. Hvilken dæmper brugte du?', 'Talte baglæns fra 10 og tog en dyb '
     'vejrtrækning.'),
    ('4. Hvordan klarede du det?', 'Godt. Fik roligt sagt, at jeg ville tale '
     'færdig.'),
]

OBSERVATION = [
    ('Opdagede et kropsligt tegn',
     'Stoppede personen op, eller viste tegn på at mærke sin krop?'),
    ('Brugte en dæmper',
     'Tog personen en dyb vejrtrækning, en pause, eller talte baglæns?'),
    ('Reagerede roligt',
     'Blev svaret givet med rolig og kontrolleret stemmeføring?'),
]

TRAENERNOTER = [
    ('Modellér før du beder om det',
     'Trænerne spiller scenariet først og tænker højt undervejs: «nu bliver '
     'jeg varm i ansigtet — jeg trækker vejret». Deltagerne skal se, hvordan '
     'det ser ud, før de selv prøver.'),
    ('Ros det konkrete',
     'Ikke «det var godt», men «du stoppede op, før du svarede». Feedback, '
     'der ikke peger på en handling, kan ikke bruges til noget.'),
    ('Rollespillet må gerne være kort',
     'Halvandet minut er nok. Det, der tager tid, er feedbacken — og det er '
     'dér, læringen ligger.'),
    ('Modspilleren skal ikke overdrive',
     'En modspiller, der går amok, gør øvelsen umulig. Sig det på kortet, og '
     'stop rollespillet, hvis det skrider.'),
    ('Slut altid roligt',
     'Ingen går fra en øvelse i høj arousal. Tag en fælles 4-4-4, før I går '
     'videre.'),
]

# ===================================================== 2 · figurerne
fig_kurve = FG.vredeskurve()
fig_kaede = FG.procesdiagram(KAEDEN, W=660, farver=KAEDE_FARVER,
                             legende=[('Dagens to led', 'i_dag'),
                                      ('Resten af kæden', 'efter')])
fig_krop = FG.kropstegn(TEGN)
fig_aande = FG.aandedraet([('Ind', 4, FG.BLA), ('Hold', 4, FG.MUT),
                           ('Ud', 4, FG.GRO)])

# ===================================================== 3 · byggeklodser


def esc(t):
    return html.escape(t, quote=False)


def tabel(hoved, raekker, bredder=None, klasser=None):
    klasser = klasser or [''] * len(hoved)
    col = ''.join(f'<col style="width:{b}%">' for b in (bredder or []))
    col = f'<colgroup>{col}</colgroup>' if bredder else ''
    th = ''.join(f'<th>{h}</th>' for h in hoved)
    tr = ''.join('<tr>' + ''.join(f'<td class="{k}">{c}</td>'
                                  for c, k in zip(r, klasser)) + '</tr>'
                 for r in raekker)
    return (f'<table class="t">{col}<thead><tr>{th}</tr></thead>'
            f'<tbody>{tr}</tbody></table>')


PLAN_TABEL = tabel(
    ['Tid', 'Fase', 'Indhold'],
    [(f'{t} min', f'<b>{esc(f_)}</b>',
      '<br>'.join('• ' + esc(p) for p in punkter))
     for t, f_, punkter in LEKTIONSPLAN],
    [12, 24, 64])

LOG_TABEL = tabel([k for k, _ in LOG_KOLONNER],
                  [[f'<i>{esc(e)}</i>' for _, e in LOG_KOLONNER]] +
                  [[''] * 4] * 5, [25, 25, 25, 25],
                  ['linje'] * 4)

OBS_TABEL = tabel(['Sæt kryds', 'Hvad jeg kigger efter', 'Noter'],
                  [['', f'<b>{esc(n)}</b><br>{esc(t)}', '']
                   for n, t in OBSERVATION], [10, 55, 35],
                  ['kryds', '', 'linje'])


def kort_html(nr, k):
    navn, kontekst, situation, modspiller, fokus = k
    trin = ''.join(f'<li>{esc(t)}</li>' for t in fokus)
    return f'''<article class="kort">
<h3><span class="nr">{nr}</span>{esc(navn)}</h3>
<p class="kontekst">{esc(kontekst)}</p>
<p><b>Situation:</b> {esc(situation)}</p>
<p class="mod"><b>Til modspilleren:</b> {esc(modspiller)}</p>
<div class="fokus"><b>Træningsfokus for hovedpersonen</b><ol>{trin}</ol></div>
</article>'''


# ===================================================== 4 · sidens CSS
BASIS = open('matematik.html').read()
GRUND = BASIS[BASIS.find('<style>') + 7:BASIS.find('</style>')]
EKSTRA = '''
.figur{background:var(--panel2);border:1px solid var(--line);border-radius:14px;
padding:16px;margin:16px 0;text-align:center}
.figur svg{max-width:100%;height:auto}
.figtekst{color:var(--muted);font-size:.9rem;margin-top:8px}
.blok{background:var(--panel);border:1px solid var(--line);
border-left:5px solid var(--accent);border-radius:14px;padding:18px 22px;
margin:14px 0;box-shadow:var(--shadow)}
.blok.gron{border-left-color:var(--good)}
.blok h3{margin:0 0 8px;font-size:1.12rem}
.blok p,.blok li{color:var(--muted);font-size:.97rem}
.blok p{margin:6px 0;max-width:74ch}
.blok ul,.blok ol{margin:6px 0 0;padding-left:20px}
.blok li{margin:4px 0}
table.t{width:100%;border-collapse:collapse;margin:12px 0;font-size:.95rem}
table.t th,table.t td{border:1px solid var(--line);padding:9px 11px;
text-align:left;vertical-align:top}
table.t th{background:var(--panel2);font-size:.82rem;color:var(--muted);
text-transform:uppercase;letter-spacing:.03em}
table.t td.linje{height:34px}
table.t td.kryds{width:34px}
.kortgitter{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));
gap:14px;margin:14px 0}
.kort{border:1px solid var(--line);border-radius:14px;padding:16px 18px;
background:var(--panel);box-shadow:var(--shadow)}
.kort h3{margin:0 0 6px;font-size:1.08rem;display:flex;align-items:center;
gap:9px}
.kort .nr{background:var(--accent);color:#fff;border-radius:999px;
width:24px;height:24px;display:inline-flex;align-items:center;
justify-content:center;font-size:.85rem;flex:0 0 auto}
.kort p{margin:5px 0;font-size:.93rem;color:var(--muted)}
.kort p.kontekst{font-size:.82rem;text-transform:uppercase;letter-spacing:.04em;
color:var(--muted);margin:0 0 8px}
.kort p.mod{background:var(--panel2);border-radius:9px;padding:8px 11px}
.kort .fokus{margin-top:10px;border-top:1px solid var(--line);padding-top:9px}
.kort .fokus b{font-size:.85rem}
.kort .fokus ol{margin:6px 0 0;padding-left:20px}
.kort .fokus li{font-size:.9rem;color:var(--muted);margin:3px 0}
.daemper{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));
gap:12px;margin:12px 0}
.printbtn{background:#fff;border:1px solid var(--line);border-radius:10px;
padding:10px 18px;font-weight:700;font-size:.95rem;cursor:pointer;color:var(--ink);
font-family:inherit;margin:6px 8px 0 0}
.printbtn:hover{border-color:var(--accent);color:var(--accent)}
@media print{header.top,.printbtn,.btnlink{display:none!important}
.blok,.figur,.kort{box-shadow:none;break-inside:avoid;page-break-inside:avoid}
body{font-size:10pt}main{padding:0}@page{size:A4;margin:12mm}
h2.sec{page-break-after:avoid}}
'''


def side(titel, krop):
    return ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{titel}</title><style>' + GRUND + EKSTRA +
            '</style></head><body><header class="top"><div class="top-inner">'
            '<a class="brand" href="index.html">Mibelibsen <span>9. klasse</span></a>'
            '</div></header><main>' + krop + '</main><footer>'
            'ART · vredeshåndtering · Mibelibsen.'
            '</footer></body></html>')


# ===================================================== 5 · siden
daempere_html = ''.join(
    f'<div class="blok gron"><h3>{i}. {esc(n)}</h3><p>{esc(t)}</p></div>'
    for i, (n, t) in enumerate(DAEMPERE, 1))

noter_html = ''.join(f'<li><b>{esc(n)}</b> {esc(t)}</li>'
                     for n, t in TRAENERNOTER)

KROP = f'''<section class="hero"><span class="pill">ART · vredeshåndtering</span>
<h1>Kropslige tegn og dæmpere</h1>
<p>Et forløb på 45 minutter i Aggression Replacement Training. Deltagerne
lærer at opdage de tidlige fysiske advarselstegn på vrede — og at bruge en
dæmper, mens der stadig er noget at gøre. Til grupper på 4–8 deltagere.</p>
<a class="btnlink" href="materiale/art-materialesaet.pdf">Hent hele materialet (PDF)</a>
<a class="btnlink ghost" href="materiale/art-rollespilskort.pdf">Rollespilskort til udklip</a>
<a class="btnlink ghost" href="materiale/art-arbejdsark.pdf">Vredeslog og observatørskema</a>
<a class="btnlink ghost" href="materiale/art-materialesaet.docx">Materialet som Word</a>
<button class="printbtn" onclick="window.print()">Print siden</button></section>

<div class="figur">{fig_kurve}
<div class="figtekst">Vreden stiger ikke pludseligt — den stiger ad en kurve.
Kroppen melder fra længe før toppen, og det er dét tidsrum, hele lektionen
handler om.</div></div>

<h2 class="sec">Hvor i kæden er vi?</h2>
<p>Vredeskontrol i ART er en kæde af led. I dag træner vi de to, der kommer
først — resten bygger ovenpå senere. Kæden er ikke teori, deltagerne skal lære
udenad; den er rækkefølgen, de øver i.</p>
<div class="figur">{fig_kaede}</div>

<h2 class="sec">Lektionsplan · 45 minutter</h2>
{PLAN_TABEL}

<h2 class="sec">1 · Kropslige tegn</h2>
<div class="blok"><p>Kroppen reagerer, før tanken gør. Adrenalinen er sendt af
sted, inden nogen har nået at beslutte noget — og det er derfor, «tæl til ti»
alene sjældent rækker. Tegnene er forskellige fra person til person, så
brainstormen på tavlen er ikke pynt: hver deltager skal finde <b>sine egne</b>
to-tre tegn og kunne nævne dem.</p>
<p>Spørg: <i>hvor i kroppen mærker du det først?</i> Ikke: <i>hvad gør du, når
du bliver vred?</i> Det første kan besvares, det andet fører til forklaringer.</p></div>
<div class="figur">{fig_krop}
<div class="figtekst">De almindeligste tegn. Lad deltagerne sætte kryds ved
deres egne — og skrive dem på, der mangler.</div></div>

<h2 class="sec">2 · Dæmpere</h2>
<p>En dæmper sænker arousal med det samme. Den løser ikke konflikten — den
køber de sekunder, det tager at komme til at tænke igen.</p>
{daempere_html}
<div class="figur">{fig_aande}</div>

<h2 class="sec">3 · Rollespilskort</h2>
<p>Fire situationer. Hovedpersonen træner de tre trin på bagsiden, modspilleren
holder sig til sin instruks. <a href="materiale/art-rollespilskort.pdf">Hent
kortene som PDF</a> — de klippes ud i ét stykke og foldes på midten, så
bagsiden ender bag forsiden.</p>
<div class="kortgitter">
{''.join(kort_html(i, k) for i, k in enumerate(KORT, 1))}
</div>

<h2 class="sec">4 · Vredeslog</h2>
<p>Ugens hjemmeopgave: registrér mindst én episode. Loggen er det, næste
lektion starter med — uden den bliver opfølgningen til løs snak.</p>
{LOG_TABEL}

<h2 class="sec">5 · Observatørskema</h2>
<p>Hver træning har en observatør. Det gør feedbacken konkret, og det giver
observatøren noget at lave, mens de to andre spiller.</p>
{OBS_TABEL}

<h2 class="sec">Til træneren</h2>
<div class="blok"><ul>{noter_html}</ul></div>
'''

open('socialisering.html', 'w').write(side('Socialisering · ART', KROP))

# ===================================================== 6 · materialet til print
DOK_CSS = '''
:root{--ink:#1a2233;--muted:#586074;--line:#c9d2e0;--panel:#f4f6fb;
--accent:#1f6fd6;--good:#1a8f5e}
*{box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,
Arial,sans-serif;color:var(--ink);margin:0;padding:0;font-size:10.4pt;
line-height:1.5}
h1{font-size:19pt;margin:0 0 4px}
h2{font-size:13.5pt;margin:20px 0 6px;padding-bottom:4px;
border-bottom:2px solid var(--accent)}
h3{font-size:11.5pt;margin:14px 0 4px}
p{margin:6px 0;max-width:78ch}
p.und{color:var(--muted)}
ul,ol{margin:6px 0;padding-left:20px}li{margin:3px 0}
table.t{width:100%;border-collapse:collapse;margin:8px 0 12px;font-size:9.6pt;
table-layout:fixed}
table.t th,table.t td{border:1px solid var(--line);padding:6px 8px;
text-align:left;vertical-align:top;word-wrap:break-word}
table.t th{background:var(--panel);font-size:8.8pt;color:var(--muted);
text-transform:uppercase;letter-spacing:.03em}
table.t td.linje{height:30px}
table.t td.kryds{height:30px}
figure{margin:10px 0;text-align:center}
figure svg{max-width:100%;height:auto}
figcaption{color:var(--muted);font-size:9pt;margin-top:4px}
@page{size:A4;margin:14mm}
@media print{h2,h3,table.t,figure{page-break-inside:avoid}
h2,h3{page-break-after:avoid}}
'''

dok = ['<h1>Aggression Replacement Training</h1>',
       '<p class="und">Vredeshåndtering: kropslige tegn og dæmpere. '
       'Undervisningsmateriale til en lektion på 45 minutter for 4–8 '
       'deltagere.</p>',
       f'<figure>{fig_kurve}</figure>',
       '<p class="und">Vreden stiger ad en kurve. Kroppen melder fra længe '
       'før toppen — og det er dét tidsrum, lektionen handler om.</p>',
       '<h2>Formål</h2>',
       '<p>Deltagerne lærer at opdage tidlige fysiske advarselstegn på vrede '
       'og at bruge en dæmper, der sænker arousal, før vreden eskalerer.</p>',
       '<h2>1 · Lektionsplan</h2>', PLAN_TABEL,
       '<h2>2 · Kropslige tegn</h2>',
       '<p>Kroppen reagerer, før tanken gør. Tegnene er forskellige fra person '
       'til person, så hver deltager skal finde sine egne to-tre og kunne '
       'nævne dem. Spørg <i>hvor i kroppen mærker du det først?</i> — ikke '
       '<i>hvad gør du, når du bliver vred?</i></p>',
       f'<figure>{fig_krop}</figure>',
       '<p class="und">De almindeligste tegn. Lad deltagerne sætte kryds ved '
       'deres egne — og skrive dem på, der mangler.</p>',
       '<h2>3 · Dæmpere</h2>']
for i, (n, t) in enumerate(DAEMPERE, 1):
    dok.append(f'<h3>{i}. {esc(n)}</h3><p>{esc(t)}</p>')
dok.append(f'<figure>{fig_aande}</figure>')

dok.append('<h2>4 · Rollespilskort</h2>')
dok.append('<p class="und">Kortene findes også som selvstændigt udklipsark. '
           'Hovedpersonen træner de tre trin, modspilleren holder sig til sin '
           'instruks.</p>')
for i, (navn, kontekst, situation, modspiller, fokus) in enumerate(KORT, 1):
    dok.append(f'<h3>Kort {i} · {esc(navn)}</h3>')
    dok.append(tabel(['Forside · situationen', 'Bagside · træningsfokus'],
                     [[f'<b>{esc(kontekst)}</b><br>{esc(situation)}'
                       f'<br><br><b>Til modspilleren:</b> {esc(modspiller)}',
                       '<br>'.join(f'{j}. {esc(t)}'
                                   for j, t in enumerate(fokus, 1))]],
                     [50, 50]))

dok.append('<h2>5 · Vredeslog</h2>')
dok.append('<p class="und">Navn: ______________________________ &nbsp; '
           'Uge: ____________</p>')
dok.append('<p>Udfyld skemaet, når du oplever en situation, hvor du mærker '
           'vreden stige. Den første række er et eksempel.</p>')
dok.append(LOG_TABEL)
dok.append('<h2>6 · Observatørskema</h2>')
dok.append('<p class="und">Observatørens navn: __________________ &nbsp; '
           'Deltager, der trænes: __________________</p>')
dok.append(OBS_TABEL)
dok.append('<h2>7 · Til træneren</h2>')
dok.append('<ul>' + noter_html + '</ul>')

DOK = ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
       '<title>ART · vredeshåndtering</title>'
       f'<style>{DOK_CSS}</style></head><body>' + '\n'.join(dok) +
       '</body></html>')
open(os.path.join(SCRATCH, 'art-materialesaet.html'), 'w').write(DOK)

# ===================================================== 7 · kort til udklip
# Bagsiden trykkes vendt 180 grader under forsiden. Kortet klippes ud i ét
# stykke og foldes paa midten — saa passer for- og bagside sammen uden
# dobbeltsidet print.
KORT_CSS = '''
@page{size:A4;margin:0}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,
Helvetica,Arial,sans-serif;color:#1a2233}
.ark{position:relative;width:210mm;height:297mm;page-break-after:always;
overflow:hidden}
.ark:last-child{page-break-after:auto}
.kort{position:absolute;left:15mm;width:180mm;height:128mm;
border:0.4mm dashed #9aa4b5;border-radius:2mm}
.halv{position:absolute;left:0;width:180mm;height:64mm;padding:7mm 8mm}
.forside{top:0}
.bagside{top:64mm;transform:rotate(180deg);display:flex;
flex-direction:column;justify-content:flex-end}
.mrk{font-size:7pt;letter-spacing:.09em;text-transform:uppercase;color:#8e97a8}
h2{font-size:14pt;margin:1mm 0 2mm}
p{margin:1.4mm 0;font-size:9.4pt;line-height:1.42}
.mod{background:#f4f6fb;border-radius:2mm;padding:2.6mm 3.4mm;font-size:9pt}
ol{margin:2mm 0 0;padding-left:5.5mm}
li{font-size:9.4pt;line-height:1.4;margin:1.4mm 0}
.fold{position:absolute;left:0;top:64mm;width:180mm;border-top:0.4mm dashed
#9aa4b5}
.foldtekst{position:absolute;right:2mm;top:64.6mm;font-size:6.5pt;color:#9aa4b5}
'''

ark = []
for i in range(0, len(KORT), 2):
    boks = []
    for j, k in enumerate(KORT[i:i + 2]):
        navn, kontekst, situation, modspiller, fokus = k
        nr = i + j + 1
        top = 12 if j == 0 else 157
        trin = ''.join(f'<li>{esc(t)}</li>' for t in fokus)
        boks.append(f'''<div class="kort" style="top:{top}mm">
<div class="halv forside">
<div class="mrk">ART · vredeshåndtering · kort {nr} af {len(KORT)}</div>
<h2>{esc(navn)}</h2>
<p class="mrk">{esc(kontekst)}</p>
<p>{esc(situation)}</p>
<p class="mod"><b>Til modspilleren:</b> {esc(modspiller)}</p></div>
<div class="fold"></div><div class="foldtekst">fold her</div>
<div class="halv bagside">
<div class="mrk">Træningsfokus for hovedpersonen</div>
<ol>{trin}</ol>
<p class="mrk" style="margin-top:3mm">Klip ud langs den stiplede kant og fold
på midten.</p></div></div>''')
    ark.append('<div class="ark">' + ''.join(boks) + '</div>')

open(os.path.join(SCRATCH, 'art-rollespilskort.html'), 'w').write(
    '<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
    '<title>ART · rollespilskort</title>'
    f'<style>{KORT_CSS}</style></head><body>' + ''.join(ark) + '</body></html>')

# ===================================================== 8 · arbejdsark
ARK_CSS = DOK_CSS.replace('@page{size:A4;margin:14mm}',
                          '@page{size:A4 landscape;margin:13mm}')
ARK_CSS += '''
.navne{display:flex;gap:14mm;margin:4mm 0 6mm;font-size:10pt;color:#586074}
.navne span{flex:1;border-bottom:0.4mm solid #c9d2e0;padding-bottom:1mm}
table.t td.linje{height:13mm}
.nyside{page-break-before:always}
'''
LOG_STOR = tabel([k for k, _ in LOG_KOLONNER],
                 [[f'<i>{esc(e)}</i>' for _, e in LOG_KOLONNER]] +
                 [[''] * 4] * 6, [25, 25, 25, 25], ['linje'] * 4)
OBS_STOR = tabel(['Sæt kryds', 'Hvad jeg kigger efter', 'Noter'],
                 [['', f'<b>{esc(n)}</b><br>{esc(t)}', '']
                  for n, t in OBSERVATION], [8, 42, 50], ['kryds', '', 'linje'])
ARK = f'''<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">
<title>ART · vredeslog og observatørskema</title><style>{ARK_CSS}</style></head>
<body>
<h1>Vredeslog</h1>
<div class="navne"><span>Navn:</span><span>Uge:</span></div>
<p class="und">Udfyld en linje, hver gang du mærker vreden stige. Første række
er et eksempel.</p>
{LOG_STOR}
<h1 class="nyside">Observatørskema til rollespil</h1>
<div class="navne"><span>Observatørens navn:</span>
<span>Deltager, der trænes:</span></div>
<p class="und">Sæt kryds undervejs, og giv kort feedback bagefter.</p>
{OBS_STOR}
{tabel(['Gode ting, jeg lagde mærke til'], [[''], ['']], [100], ['linje'])}
{tabel(['Forslag til næste gang'], [[''], ['']], [100], ['linje'])}
</body></html>'''
open(os.path.join(SCRATCH, 'art-arbejdsark.html'), 'w').write(ARK)

print('skrevet:  socialisering.html')
for navn in ('art-materialesaet', 'art-rollespilskort', 'art-arbejdsark'):
    print(f'skrevet:  {SCRATCH}/{navn}.html')
print(f'materiale: {len(KORT)} rollespilskort · {len(TEGN)} kropslige tegn · '
      f'{len(DAEMPERE)} dæmpere · {len(LEKTIONSPLAN)} faser · '
      f'{len(KAEDEN)} led i kæden')
