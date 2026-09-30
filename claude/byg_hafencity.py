#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bygger turen i HafenCity: at bygge og bo med risiko for stormflod.

    python3 claude/byg_hafencity.py <scratch-mappe>

Skriver hafencity.html og et gruppeark til print (ét A4 pr. gruppe).

Turen står ét sted nedenfor — STOP og GRUPPER — og både siden og gruppearkene
bygges af de samme lister. Tiderne lægges sammen og tjekkes mod den samlede
længde, så programmet ikke kan komme til at love fire timer og vare fem.

Tal, der er slået efter (kilder står på siden):
  · warften i HafenCity ligger 7,8–8,5 m over NHN, i øst hævet til 8,3
  · promenaderne ligger på de gamle kajers niveau og må gerne oversvømmes
  · stormfloden 1962: 5,70 m ved Pegel St. Pauli, over 300 døde i Hamborg
  · stormfloden 1976: 6,45 m — højere, men digerne holdt
  · Hafen.City.Horizonte, Baakenallee 33: ti-fr 10–16, gratis
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figurer as FG                                         # noqa: E402

SCRATCH = sys.argv[1] if len(sys.argv) > 1 else '.'
ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROD)

# ===================================================== 1 · turen
# (minutter, navn, hvor, hvad man ser, [opgaver paa stedet])
STOP = [
 (20, 'Speicherstadt', 'Kibbelstegbrücke og kanalen bagved',
  'Den gamle måde at gøre det på: pakhusene står uden for diget og bliver '
  'oversvømmet flere gange hver vinter. Derfor er der mursten forneden, varer '
  'blev hejst op på de øverste etager, og portene har riller i siderne, som '
  'skot skydes ned i.',
  ['Find en port med riller til skot i karmen — de sidder lige i øjenhøjde.',
   'Kig efter, hvor højt murstenene er skiftet ud eller repareret.',
   'Stå på broen og se, hvor tæt vandet er på gadeniveauet.']),
 (25, 'Sandtorhafen', 'Magellan-Terrassen',
  'Trappen mellem de to niveauer. Nederst promenaden, der må blive våd, '
  'øverst byen, der ikke må. Terrasserne er selve overgangen — og de '
  'forsvinder i vandet, når det står højt.',
  ['Tæl trinnene fra vandet op til øverste terrasse, og mål et trin. '
   'Hvor stor er højdeforskellen?',
   'Sammenlign med tallene på tværsnittet: passer det?',
   'Stå tre på nederste trin og tre på øverste — samme billede.']),
 (30, 'Dalmannkai og Am Kaiserkai', 'Promenaden langs Sandtorhafen',
  'Warften i brug. Promenaden ligger lavt, gaden ligger otte meter oppe, og '
  'imellem dem er der porte, ramper og trapper. Parkeringskældrene kan lukkes '
  'af med fluttore, når varslet kommer.',
  ['Find en flodport eller en nedkørsel, der kan lukkes. Hvor høj er den?',
   'Find en indgang, hvor døren sidder højere end fortovet.',
   'Følg en flugtvej med øjnene: hvor ville du gå hen, hvis vandet kom nu?']),
 (55, 'Frokost', 'Überseequartier eller Überseeboulevard',
  'Spisesteder på begge niveauer og indendørs, hvis det regner. Grupperne '
  'spiser sammen og sorterer dagens billeder imens.',
  ['Slet de billeder, der ikke skal bruges — mens I husker hvorfor.',
   'Skriv de tre ord, jeres gruppe vil bruge om stedet.']),
 (20, 'Lohsepark og Elbarkaden', 'Magdeburger Hafen',
  'Parken ligger på warftniveau, og arkaderne langs vandet er bygget, så '
  'stueetagen kan tåle at stå i vand. Her er forskellen på de to niveauer '
  'lettest at fotografere på ét billede.',
  ['Tag ét billede, hvor begge niveauer er med — en person på hvert.',
   'Find noget, der ville flyde væk, hvis vandet steg to meter.']),
 (40, 'Baakenhafen', 'Hafen.City.Horizonte, Baakenallee 33',
  'Den nyeste del af HafenCity, bygget højere end den ældste. I udstillingen '
  'står byen som model i 1:500, så hele systemet kan ses fra oven. Gratis, '
  'åbent torsdag 10–16.',
  ['Find jeres egne stop på modellen, og fotografér dem oppefra.',
   'Spørg personalet om én ting, I ikke kunne se ude på gaden.',
   'Tag gruppens sidste billede foran modellen.']),
]

GRUPPER = [
 ('De to niveauer',
  'Warften: byen er hævet op på en kunstig bakke, mens promenaden er blevet '
  'liggende nede ved vandet.',
  ['Et billede fra promenaden med gaden bag jer, oppe i højden.',
   'Et billede fra gadeniveau, hvor promenaden ses nedenfor.',
   'Et billede, hvor en af jer står præcis dér, hvor det ene niveau bliver '
   'til det andet.']),
 ('Porte, skot og døre',
  'Alt det, der lukker vandet ude, når varslet kommer: fluttore, riller til '
  'skot, hævede dørtrin, ramper.',
  ['Et nærbillede af en rille eller en port — med en hånd ved siden af, så '
   'man kan se størrelsen.',
   'Et billede af en nedkørsel til en parkeringskælder.',
   'Et billede af en dør, der sidder højere end fortovet.']),
 ('Flugtvejene',
  'Man flygter ikke ud af HafenCity — man går opad og hen over broerne. '
  'Find vejen, en beboer ville tage.',
  ['Et billede af en bro mellem to warfter.',
   'Et billede af en trappe eller rampe fra promenaden op til gaden.',
   'Et billede taget fra det sted, I ville samles, hvis vandet kom.']),
 ('Den gamle måde',
  'Speicherstadt: i stedet for at holde vandet ude byggede man, så det måtte '
  'komme ind. Hvad kostede det, og hvad virkede?',
  ['Et billede af mursten og port i stueetagen.',
   'Et billede, der viser, hvor varerne blev hejst op.',
   'Et billede, hvor I sammenligner et gammelt og et nyt hus.']),
 ('Det, der må blive vådt',
  'Promenader, terrasser, pontonbroer og trapper, der er bygget til at stå '
  'under vand nogle dage om året.',
  ['Et billede af en flydebro eller ponton, der følger vandstanden.',
   'Et billede af et sted, hvor I kan se, at vandet har været der.',
   'Et billede af en bænk, lampe eller skraldespand, der er skruet fast — '
   'eller som ikke er.']),
]

FOTOREGLER = [
 'Der skal være <b>mindst én fra gruppen</b> med på hvert billede. Uden et '
 'menneske kan man ikke se, hvor stort noget er.',
 'Tag <b>højst fem billeder pr. stop</b>. I skal vælge undervejs, ikke '
 'bagefter.',
 'Hold telefonen <b>vandret</b>. Billederne skal bruges i et oplæg.',
 'Døb filerne <b>gruppe_stop_kort-tekst</b> — fx <i>3_dalmannkai_flodport</i>.',
 'Læg billederne i <b>billedmappen i Teams samme aften</b>, i jeres egen '
 'undermappe. Ikke dagen efter.',
]

SIKKERHED = [
 'Grupperne går selv mellem stoppene, men mødes præcist. Sæt et klokkeslæt, '
 'ikke «om en halv time».',
 'Promenaderne har ingen rækværk mod vandet mange steder. Ingen fotografering '
 'med ryggen til kajkanten.',
 'Cykelstierne i HafenCity er hurtige og ligger ofte i samme farve asfalt som '
 'fortovet.',
 'Der er toiletter ved Überseequartier og i Hafen.City.Horizonte.',
]

I_ALT = sum(m for m, *_ in STOP)
GANG = 45                       # cirka gangtid mellem stoppene i alt
assert 3 * 60 + 30 <= I_ALT + GANG <= 4 * 60 + 15, \
    f'programmet varer {I_ALT + GANG} minutter, ikke cirka fire timer'
assert len(GRUPPER) == 5, 'der er fem projektgrupper'

# ===================================================== 2 · figurer
fig_snit = FG.vandstandssnit(
    promenade=(4.5, 5.5), warft=(7.5, 8.3),
    maerker=[('Stormflod 1962', 5.70), ('Stormflod 1976', 6.45)])
fig_rute = FG.procesdiagram(
    [(f'{navn} · {m} min', hvor, 'frokost' if navn == 'Frokost' else 'stop')
     for m, navn, hvor, _, _ in STOP],
    W=660, farver={'stop': FG.BLA, 'frokost': '#e9edf4'})


# ===================================================== 3 · siden
def esc(t):
    return html.escape(t, quote=False)


BASIS = open('matematik.html').read()
GRUND = BASIS[BASIS.find('<style>') + 7:BASIS.find('</style>')]
EKSTRA = '''
.figur{background:var(--panel2);border:1px solid var(--line);border-radius:14px;
padding:14px;margin:14px 0;text-align:center}
.figur svg{max-width:100%;height:auto}
.figtekst{color:var(--muted);font-size:.9rem;margin-top:8px}
.blok{background:var(--panel);border:1px solid var(--line);
border-left:5px solid var(--accent);border-radius:14px;padding:16px 20px;
margin:12px 0;box-shadow:var(--shadow)}
.blok.advar{border-left-color:var(--bad);background:var(--bad-soft)}
.blok h3{margin:0 0 8px;font-size:1.1rem}
.blok p,.blok li{color:var(--muted);font-size:.97rem}
.blok ul,.blok ol{margin:6px 0 0;padding-left:20px}.blok li{margin:5px 0}
.stop{border:1px solid var(--line);border-radius:14px;padding:16px 20px;
margin:12px 0;background:var(--panel);box-shadow:var(--shadow)}
.stop h3{margin:0 0 2px;font-size:1.15rem;display:flex;align-items:center;
gap:10px;flex-wrap:wrap}
.stop .tid{background:var(--accent);color:#fff;border-radius:999px;
padding:2px 11px;font-size:.82rem;font-weight:700;flex:0 0 auto}
.stop .hvor{color:var(--muted);font-size:.88rem;text-transform:uppercase;
letter-spacing:.04em;margin:0 0 9px}
.stop p{color:var(--muted);font-size:.97rem;margin:6px 0;max-width:74ch}
.stop ol{margin:8px 0 0;padding-left:20px}
.stop li{color:var(--ink);font-size:.95rem;margin:5px 0}
.gruppe{border:1px solid var(--line);border-radius:14px;padding:15px 18px;
background:var(--panel2)}
.gruppe h3{margin:0 0 4px;font-size:1.05rem}
.gruppe .nr{background:var(--good);color:#fff;border-radius:999px;
width:24px;height:24px;display:inline-flex;align-items:center;
justify-content:center;font-size:.82rem;margin-right:8px}
.gruppe p{color:var(--muted);font-size:.93rem;margin:4px 0}
.gruppe ul{margin:8px 0 0;padding-left:18px}
.gruppe li{font-size:.92rem;color:var(--ink);margin:4px 0}
.gitter{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
gap:12px;margin:12px 0}
.printbtn{background:#fff;border:1px solid var(--line);border-radius:10px;
padding:10px 18px;font-weight:700;font-size:.95rem;cursor:pointer;color:var(--ink);
font-family:inherit;margin:6px 8px 0 0}
.kilder{color:var(--muted);font-size:.85rem;margin-top:18px}
.kilder a{color:var(--muted)}
@media print{header.top,.printbtn,.btnlink{display:none!important}
.blok,.figur,.stop,.gruppe{box-shadow:none;break-inside:avoid}
body{font-size:10pt}main{padding:0}@page{size:A4;margin:12mm}}
'''

stop_html = ''.join(
    f'''<article class="stop"><h3><span class="tid">{m} min</span>
{i}. {esc(navn)}</h3><p class="hvor">{esc(hvor)}</p><p>{esc(hvad)}</p>
<ol>{''.join(f'<li>{esc(o)}</li>' for o in opgaver)}</ol></article>'''
    for i, (m, navn, hvor, hvad, opgaver) in enumerate(STOP, 1))

gruppe_html = ''.join(
    f'''<div class="gruppe"><h3><span class="nr">{i}</span>{esc(navn)}</h3>
<p>{esc(t)}</p><ul>{''.join(f'<li>{esc(b)}</li>' for b in billeder)}</ul></div>'''
    for i, (navn, t, billeder) in enumerate(GRUPPER, 1))

KROP = f'''<section class="hero"><span class="pill">Studietur Hamborg</span>
<h1>HafenCity: at bygge og bo, når stormfloden kommer</h1>
<p>Fire timer med frokost. Fem grupper, hver med sit fotoemne. HafenCity
ligger <b>uden for diget</b> — byen er i stedet løftet op på kunstige bakker,
warfter, mens promenaderne er blevet liggende nede ved vandet og må blive
våde. Det kan ses med det blotte øje, og det er dét, I skal fotografere.</p>
<button class="printbtn" onclick="window.print()">Print siden</button></section>

<div class="figur">{fig_snit}
<div class="figtekst">De to niveauer, og to rigtige stormfloder tegnet ind.
1976 stod <b>højere</b> end 1962 — men da holdt digerne.
Begge ville have oversvømmet promenaden. Ingen af dem ville have nået op på
warften.</div></div>

<div class="blok"><h3>Det, turen handler om</h3>
<p>I 1962 nåede vandet 5,70 m ved Pegel St. Pauli. Digerne brød sammen 60
steder, og over 300 mennesker døde i Hamborg. I 1976 stod vandet 6,45 m —
højere end i 1962 — men da holdt digerne.</p>
<p>HafenCity er bygget efter den erfaring, men på en anden måde: ikke bag et
dige, men <b>oven på</b> byen. Gader og huse ligger 7,5–8,5 meter over
havets middel. Promenaderne ligger nede på de gamle kajers niveau og bliver
lukket af, når der varsles. Spørgsmålet, I skal tage stilling til undervejs:
<i>er det klogt at bygge sådan — eller er det at flytte problemet?</i></p></div>

<h2 class="sec">Programmet</h2>
<p>Cirka {I_ALT} minutter på stoppene plus omkring {GANG} minutter gang — i alt
knap fire timer. Ruten går fra vest mod øst, cirka tre kilometer i alt.</p>
<div class="figur">{fig_rute}</div>

{stop_html}

<h2 class="sec">Grupperne og deres fotoemne</h2>
<p>Alle fem grupper går den samme rute og ser de samme steder — men de
fotograferer forskellige ting. Så kan billederne lægges sammen bagefter til
én samlet fortælling i stedet for fem ens.</p>
<div class="gitter">{gruppe_html}</div>

<h2 class="sec">Fotoregler</h2>
<div class="blok"><ul>{''.join(f'<li>{r}</li>' for r in FOTOREGLER)}</ul></div>

<h2 class="sec">Praktisk</h2>
<div class="blok advar"><ul>{''.join(f'<li>{esc(s)}</li>' for s in SIKKERHED)}
</ul></div>

<div class="kilder">Tal og åbningstider er slået efter 30. september 2026:
warfternes højde og promenadernes niveau hos
<a href="https://www.db-bauzeitung.de/schwerpunkt/auf-sand-gebaut/">db
Bauzeitung</a> og
<a href="https://de.wikipedia.org/wiki/Hamburg-HafenCity">Wikipedia</a>,
vandstandene i 1962 og 1976 hos
<a href="https://de.wikipedia.org/wiki/Sturmflut_1962">Wikipedia</a>, og
åbningstiderne hos
<a href="https://www.hafencity.com/forum">HafenCity Hamburg</a>.
Tjek åbningstiden samme morgen — den er det eneste her, der kan nå at ændre
sig.</div>
'''


def side(titel, krop):
    return ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{titel}</title><style>' + GRUND + EKSTRA +
            '</style></head><body><header class="top"><div class="top-inner">'
            '<a class="brand" href="index.html">Mibelibsen <span>9. klasse</span></a>'
            '</div></header><main>' + krop + '</main><footer>'
            'Studietur Hamborg · 9. klasse · Mibelibsen.'
            '</footer></body></html>')


open('hafencity.html', 'w').write(side('HafenCity · stormflod', KROP))

# ===================================================== 4 · gruppeark til print
ARK_CSS = '''
@page{size:A4;margin:13mm}
*{box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,
Arial,sans-serif;color:#1a2233;margin:0;font-size:10.4pt;line-height:1.45}
.ark{page-break-after:always}
.ark:last-child{page-break-after:auto}
h1{font-size:17pt;margin:0 0 2px}
h2{font-size:12pt;margin:14px 0 4px;padding-bottom:3px;
border-bottom:2px solid #1f6fd6}
.emne{background:#eaf7f0;border:1px solid #bfe6d2;border-radius:8px;
padding:10px 14px;margin:8px 0 12px}
.emne b{font-size:11.5pt}
.emne p{margin:4px 0 0;color:#586074}
p{margin:5px 0;max-width:80ch}
ul,ol{margin:5px 0;padding-left:20px}li{margin:3px 0}
table{width:100%;border-collapse:collapse;margin:6px 0;font-size:9.4pt}
th,td{border:1px solid #c9d2e0;padding:5px 7px;text-align:left;
vertical-align:top}
th{background:#f4f6fb;font-size:8.6pt;color:#586074;text-transform:uppercase;
letter-spacing:.03em}
td.tid{white-space:nowrap;font-weight:700;width:16mm}
td.kryds{width:14mm}
.fod{color:#586074;font-size:8.8pt;margin-top:12px;border-top:1px solid #c9d2e0;
padding-top:6px}
'''

ark = []
for i, (navn, t, billeder) in enumerate(GRUPPER, 1):
    raekker = ''.join(
        f'<tr><td class="tid">{m} min</td><td><b>{esc(n)}</b><br>{esc(hvor)}</td>'
        f'<td class="kryds"></td></tr>'
        for m, n, hvor, _, _ in STOP)
    ark.append(f'''<div class="ark">
<h1>Gruppe {i} · {esc(navn)}</h1>
<p style="color:#586074">HafenCity · at bygge og bo med risiko for stormflod</p>
<div class="emne"><b>Jeres fotoemne: {esc(navn)}</b><p>{esc(t)}</p></div>
<h2>De tre billeder, I skal have</h2>
<ol>{''.join(f'<li>{esc(b)}</li>' for b in billeder)}</ol>
<h2>Ruten — sæt kryds, når I har været der</h2>
<table><thead><tr><th>Tid</th><th>Stop</th><th>Sat kryds</th></tr></thead>
<tbody>{raekker}</tbody></table>
<h2>Husk</h2>
<ul>{''.join(f'<li>{r}</li>' for r in FOTOREGLER)}</ul>
<h2>Noter — tre ord om hvert stop</h2>
<table><tbody>{''.join('<tr><td style="height:10mm"></td></tr>'
                       for _ in range(3))}</tbody></table>
<div class="fod">Mødested og klokkeslæt aftales på stedet.
Billederne i Teams samme aften.</div></div>''')

open(os.path.join(SCRATCH, 'hafencity-gruppeark.html'), 'w').write(
    '<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
    '<title>HafenCity · gruppeark</title>'
    f'<style>{ARK_CSS}</style></head><body>' + ''.join(ark) + '</body></html>')

print('skrevet:  hafencity.html')
print(f'skrevet:  {SCRATCH}/hafencity-gruppeark.html')
print(f'turen:    {len(STOP)} stop · {I_ALT} min på stoppene + {GANG} min gang '
      f'= {I_ALT + GANG} min · {len(GRUPPER)} grupper')
