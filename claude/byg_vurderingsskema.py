#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bygger vurderingsskemaet til projektopgaven i 9. klasse.

    python3 claude/byg_vurderingsskema.py <scratch-mappe>

Skemaet følger de tre områder, projektopgaven vurderes på: arbejdsprocessen,
produktet og fremlæggelsen. Det skrives som ét sæt kriterier i KRITERIER
nedenfor, og både afkrydsningsskemaet, profilen og niveaubeskrivelserne
bygges af den samme liste — så et kriterium ikke kan stå ét sted og mangle et
andet.

Skemaet er til den voksne og lægges i vejledning/, som er udelukket fra
deploy. Niveaubeskrivelserne på sidste side må gerne deles med ungerne: de
skal vide, hvad de bliver vurderet på, før de går i gang.
"""
import os
import sys

SCRATCH = sys.argv[1] if len(sys.argv) > 1 else '.'
ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROD)

NIVEAUER = ['Frem­ragende', 'God', 'Jævn', 'Mangel­fuld']

# ------------------------------------------------------------- kriterierne
# (område, [(kriterium, hvad man kigger efter)], niveaubeskrivelse)
KRITERIER = [
 ('Arbejdsprocessen',
  'Det meste af dette kan kun vurderes undervejs. Skriv noter i løbet af ugen '
  '— ikke først til fremlæggelsen.',
  [('Problemformulering',
    'Afgrænset og til at undersøge. Lægger op til et svar, der skal findes, '
    'ikke til en opremsning.'),
   ('Planlægning',
    'Har en tidsplan med delmål, og holder sig nogenlunde til den. Kommer i '
    'gang uden at blive sat i gang.'),
   ('Informationssøgning',
    'Bruger flere slags kilder end den første side på nettet. Kan forklare, '
    'hvorfor en kilde er god eller dårlig.'),
   ('Selvstændighed',
    'Træffer egne valg og kan begrunde dem. Bruger vejledningen aktivt — '
    'kommer med spørgsmål frem for at vente.'),
   ('Samarbejde',
    'Fordeler arbejdet, lytter, og får løst uenigheder. Vurderes kun, hvis '
    'der arbejdes i gruppe.'),
   ('Vedholdenhed',
    'Arbejder videre, også når det driller, og retter planen til i stedet for '
    'at droppe den.')],
  [('Fremragende', 'Styrer selv hele forløbet. Problemformuleringen er skarp '
    'og bliver justeret med begrundelse undervejs. Kilderne er valgt og '
    'vurderet bevidst.'),
   ('God', 'Har en klar plan og følger den. Søger bredt og forholder sig til '
    'kilderne. Beder om vejledning på de rigtige tidspunkter.'),
   ('Jævn', 'Kommer igennem opgaven, men planen er løs, og kilderne er dem, '
    'der lå øverst. Går ofte i stå uden hjælp.'),
   ('Mangelfuld', 'Ingen reel plan eller problemformulering. Arbejdet kommer '
    'kun i gang, når en voksen sætter det i gang.')]),

 ('Produktet',
  'Vurder produktet for dét, det er — ikke for hvor pænt det ser ud. Et enkelt '
  'produkt, der rammer problemformuleringen, er bedre end et flot, der ikke '
  'gør.',
  [('Sammenhæng med problemformuleringen',
    'Produktet svarer på dét, der blev spurgt om. Man kan se forbindelsen '
    'uden at få den forklaret.'),
   ('Fagligt indhold',
    'Viden fra mere end ét fag, og dybde frem for bredde. Fagene bruges — de '
    'er ikke bare nævnt.'),
   ('Brug af kilder',
    'Bruger kilderne aktivt i produktet og krediterer dem. Citerer ikke uden '
    'at sige hvorfra.'),
   ('Valg af produktform',
    'Formen er valgt med en begrundelse: den passer til budskabet og til dem, '
    'produktet er lavet til.'),
   ('Udførelse',
    'Færdiggjort og omhyggeligt lavet. Det holder, det virker, det kan læses '
    'eller ses.')],
  [('Fremragende', 'Produktet svarer selvstændigt på problemformuleringen og '
    'bruger flere fag til det. Formen er et bevidst valg, og udførelsen er '
    'gennemført.'),
   ('God', 'Klar sammenhæng mellem problemformulering og produkt. Fagligt '
    'indhold fra flere fag, og kilderne er med.'),
   ('Jævn', 'Produktet berører emnet, men svarer kun delvis på '
    'problemformuleringen. Indholdet er refererende.'),
   ('Mangelfuld', 'Produktet og problemformuleringen hænger ikke sammen, '
    'eller produktet er ikke gjort færdigt.')]),

 ('Fremlæggelsen',
  'Fremlæggelsen er en del af opgaven, ikke en afrunding af den. Afsæt tid til '
  'spørgsmål — det er dér, det faglige som regel viser sig.',
  [('Struktur',
    'Rød tråd med en indledning, en midte og en afslutning. Man kan følge '
    'med uden at kende opgaven i forvejen.'),
   ('Formidling',
    'Taler til dem, der lytter — læser ikke op. Tempo og stemme er til at '
    'følge med i.'),
   ('Brug af produktet',
    'Produktet indgår aktivt i fremlæggelsen og bliver vist frem, ikke bare '
    'nævnt.'),
   ('Fagsprog',
    'Bruger fagenes begreber, og bruger dem rigtigt. Kan forklare dem, hvis '
    'der spørges.'),
   ('Svar på spørgsmål',
    'Svarer fagligt og roligt, og kan selv pege på, hvad der var svært, og '
    'hvad der kunne gøres bedre.')],
  [('Fremragende', 'Fremlæggelsen er selvstændig og velstruktureret. '
    'Produktet bruges som argument, og spørgsmål besvares med overblik over '
    'hele forløbet.'),
   ('God', 'Klar struktur og god kontakt til tilhørerne. Produktet indgår, og '
    'spørgsmål bliver besvaret fagligt.'),
   ('Jævn', 'Fremlæggelsen kommer omkring stoffet, men er bundet til '
    'manuskriptet. Spørgsmål besvares kort.'),
   ('Mangelfuld', 'Fremlæggelsen hænger ikke sammen, eller produktet indgår '
    'ikke. Spørgsmål kan ikke besvares.')]),
]

KARAKTERER = [
    ('12', 'Den fremragende præstation'),
    ('10', 'Den fortrinlige præstation'),
    ('7', 'Den gode præstation'),
    ('4', 'Den jævne præstation'),
    ('02', 'Den tilstrækkelige præstation'),
    ('00', 'Den utilstrækkelige præstation'),
    ('-3', 'Den ringe præstation'),
]

STAMDATA = [
    'Navn', 'Klasse', 'Gruppe (hvis flere)', 'Vejleder',
    'Overordnet emne', 'Delemne', 'Produktets form', 'Uge og dato',
]

FORMULERINGER = [
    'N. har arbejdet med … og har undersøgt …',
    'Problemformuleringen var … Den blev undervejs justeret til …, fordi …',
    'I arbejdsprocessen viste N. særligt …',
    'Produktet er … Det svarer på problemformuleringen ved at …',
    'Til fremlæggelsen …',
    'Det næste skridt for N. er …',
]

# ================================================================= HTML


def tabel(hoved, raekker, bredder, klasser=None):
    klasser = klasser or [''] * len(hoved)
    col = ''.join(f'<col style="width:{b}%">' for b in bredder)
    th = ''.join(f'<th>{h}</th>' for h in hoved)
    tr = ''.join('<tr>' + ''.join(f'<td class="{k}">{c}</td>'
                                  for c, k in zip(r, klasser)) + '</tr>'
                 for r in raekker)
    return (f'<table class="t"><colgroup>{col}</colgroup><thead><tr>{th}</tr>'
            f'</thead><tbody>{tr}</tbody></table>')


def linjer(overskrift, antal, bredde=100):
    """Skrivefelt: en tabel med tomme rækker, så det også kan skrives i Word."""
    return tabel([overskrift], [['']] * antal, [bredde], ['linje'])


dele = []
dele.append('<h1>Vurderingsskema · projektopgaven i 9. klasse</h1>')
dele.append('<p class="und">Projektopgaven vurderes på tre områder: '
            '<b>arbejdsprocessen</b>, <b>produktet</b> og '
            '<b>fremlæggelsen</b>. Skemaet her følger de tre områder. '
            'Sæt ét kryds pr. linje, skriv noter undervejs, og brug siden til '
            'sidst til karakteren og den skriftlige udtalelse.</p>')

dele.append(tabel(['Oplysning', 'Udfyldes'],
                  [[navn, ''] for navn in STAMDATA], [34, 66], ['', 'linje']))

for nr, (omraade, indledning, kriterier, _) in enumerate(KRITERIER, 1):
    dele.append(f'<h2>{nr} · {omraade}</h2>')
    dele.append(f'<p class="und">{indledning}</p>')
    dele.append(tabel(['Kriterium', 'Det kigger jeg efter'] + NIVEAUER,
                      [[f'<b>{k}</b>', hvad, '', '', '', ''] for k, hvad in kriterier],
                      [20, 44, 9, 9, 9, 9],
                      ['', 'lille', 'kryds', 'kryds', 'kryds', 'kryds']))
    dele.append(linjer(f'Noter til {omraade.lower()}', 3))

dele.append('<h2 class="nyside">Samlet vurdering</h2>')
dele.append('<p class="und">Profilen er en hurtig opsummering — den erstatter '
            'ikke krydserne ovenfor, men gør det let at se, hvor styrken '
            'ligger.</p>')
dele.append(tabel(['Område'] + NIVEAUER,
                  [[f'<b>{o}</b>', '', '', '', ''] for o, _, _, _ in KRITERIER],
                  [36, 16, 16, 16, 16],
                  ['', 'kryds', 'kryds', 'kryds', 'kryds']))

dele.append('<h3>Karakter</h3>')
dele.append(tabel(['Karakter', 'Beskrivelse', 'Sæt kryds'],
                  [[f'<b>{k}</b>', t, ''] for k, t in KARAKTERER],
                  [14, 66, 20], ['tal', '', 'kryds']))

dele.append('<h3>Skriftlig udtalelse</h3>')
dele.append('<p class="und">Skriv om alle tre områder, og skriv det, der er '
            'sket — ikke kun hvad der mangler. Sætningerne herunder kan bruges '
            'som start: ' + ' · '.join(f'«{f}»' for f in FORMULERINGER) +
            '</p>')
dele.append(linjer('Udtalelse', 10))
dele.append(linjer('Det næste skridt', 3))

dele.append('<h2 class="nyside">Niveaubeskrivelser</h2>')
dele.append('<p class="und">Til at holde vurderingen ens hen over en hel '
            'klasse — og god at give ungerne, <b>før</b> de går i gang. De '
            'skal vide, hvad de bliver vurderet på.</p>')
for omraade, _, _, niveauer in KRITERIER:
    dele.append(f'<h3>{omraade}</h3>')
    dele.append(tabel(['Niveau', 'Sådan ser det ud'],
                      [[f'<b>{n}</b>', t] for n, t in niveauer], [20, 80]))

dele.append('<h3>Det formelle</h3>')
dele.append('<p class="und">Eleven får både en <b>skriftlig udtalelse</b> og '
            'en <b>karakter</b> for projektopgaven, og eleven bestemmer selv, '
            'om udtalelsen, karakteren eller begge dele skal med på '
            'afgangsbeviset. Skemaet her er et arbejdsredskab, ikke et '
            'officielt dokument — tjek ordlyden af udtalelsen mod skolens '
            'egen praksis, før den sendes videre.</p>')

KROP = '\n'.join(dele)

CSS = '''
:root{--ink:#1a2233;--muted:#586074;--line:#c9d2e0;--panel:#f4f6fb;
--accent:#1f6fd6}
*{box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,
Arial,sans-serif;color:var(--ink);margin:0;padding:22px 26px;font-size:10.2pt;
line-height:1.45}
h1{font-size:19pt;margin:0 0 6px}
h2{font-size:13.5pt;margin:20px 0 4px;padding-bottom:4px;
border-bottom:2px solid var(--accent)}
h3{font-size:11.5pt;margin:14px 0 4px}
p.und{color:var(--muted);margin:4px 0 10px;max-width:74ch}
table.t{width:100%;border-collapse:collapse;margin:6px 0 10px;
font-size:9.6pt;table-layout:fixed}
table.t th,table.t td{border:1px solid var(--line);padding:5px 7px;
text-align:left;vertical-align:top;word-wrap:break-word}
table.t th{background:var(--panel);font-size:8.8pt;color:var(--muted);
text-transform:uppercase;letter-spacing:.03em}
table.t td.lille{color:var(--muted);font-size:9pt}
table.t td.kryds{background:#fff}
table.t td.tal{text-align:center;font-weight:700}
table.t td.linje{height:26px}
tbody tr:nth-child(even) td{background:#fbfcfe}
tbody tr:nth-child(even) td.kryds,tbody tr td.linje{background:#fff}
@page{size:A4;margin:12mm}
@media print{h2.nyside{page-break-before:always}
table.t,h2,h3{page-break-inside:avoid}h2,h3{page-break-after:avoid}}
'''

HTML = ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
        '<title>Vurderingsskema · projektopgaven i 9. klasse</title>'
        f'<style>{CSS}</style></head><body>{KROP}</body></html>')

ud = os.path.join(SCRATCH, 'vurderingsskema-projektopgave.html')
open(ud, 'w', encoding='utf-8').write(HTML)

antal = sum(len(k) for _, _, k, _ in KRITERIER)
print(f'skrevet:  {ud}')
print(f'skema:    {len(KRITERIER)} områder · {antal} kriterier · '
      f'{len(NIVEAUER)} niveauer · {len(KARAKTERER)} karaktertrin')
