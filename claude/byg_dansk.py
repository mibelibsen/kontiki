# -*- coding: utf-8 -*-
"""Bygger dansk.html — skriftlig fremstilling i 9. klasse.

Siden ligger paa mibelibsen.space/dansk (omskrivningen staar i vercel.json)
og er **ulistet med vilje**: ingen anden side linker til den. Den kan kun
naas af den, der har adressen. Ulistet er ikke det samme som privat.

Tre opgavesaet og en genrevejledning til essayet, hver med sit menupunkt
oeverst paa siden.

    python3 claude/byg_dansk.py
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figurer as FG

UD = 'dansk.html'

# ---------------------------------------------------------------- opgaver
# Hvert saet har tre opgaver i tre genrer. Eleven vaelger én.
#
# Hver opgave har den samme figur: tre konkrete steder at begynde, og det,
# teksten skal naa hen imod. Det er samme problem i alle genrer - at finde
# et sted at starte, man selv har staaet i, i stedet for at begynde med
# "I dagens samfund ...".
#
# (genre, titel, opgavetekst, etiket over figuren, kernen, [tre indgange])
SAET = [
 ('saet1', 'Sæt 1', 'Mennesker og netværk',
  'Tre opgaver om at høre til og at stå udenfor. Vælg én.',
  [
   ('Novelle', 'Beskeden, der ikke blev sendt',
    'Skriv en novelle om et menneske, der skriver noget og fortryder. Lad '
    'os se det, inden vi får det forklaret — en novelle viser, den '
    'forklarer ikke.',
    'DET, LÆSEREN SKAL MÆRKE', 'Hvorfor sendte hun den ikke?',
    ['Fingeren over slet-knappen', 'En samtale, der gik i stå',
     'En, der skriver og skriver og holder op']),

   ('Debatindlæg', 'Skal skoledagen være mobilfri?',
    'Skriv et debatindlæg til skolebladet. Tag stilling, og tag det bedste '
    'modargument alvorligt — et debatindlæg, der kun har ét synspunkt, '
    'overbeviser ingen.',
    'PÅSTANDEN', 'Mobilfri skoledag: for hvis skyld?',
    ['En time, hvor telefonen lå væk', 'Et frikvarter, hvor alle sad ned',
     'En aftale, I selv har lavet i klassen']),

   ('Reportage', 'Et helt almindeligt frikvarter',
    'Skriv en reportage fra ti minutter på skolen. Vær til stede: hvad ser, '
    'hører og lugter du? Lad læseren være med, og hold dig fra at '
    'konkludere.',
    'DET, DU SKAL FÅ FREM', 'Hvad sker der egentlig, når ingen kigger?',
    ['Lyden i gangen klokken 9.45', 'Dem, der står udenfor cirklen',
     'Et sted, ingen voksne kommer']),
  ]),

 ('saet2', 'Sæt 2', 'Noget, der forandrer sig',
  'Tre opgaver om forandring — i et menneske, i et samfund, i en vane. '
  'Vælg én.',
  [
   ('Novelle', 'Sidste gang',
    'Skriv en novelle om en sidste gang, som personen ikke vidste var den '
    'sidste. Du må gerne bruge et spring i tid.',
    'DET, LÆSEREN SKAL MÆRKE', 'Hvornår opdager man, at noget er slut?',
    ['En dør, der lukkes som altid', 'En vane, der bare holdt op',
     'Et billede, der er taget uden grund']),

   ('Debatindlæg', 'Hvem har ansvaret for plastikken?',
    'Skriv et debatindlæg om, hvem der skal rydde op: den enkelte, '
    'virksomhederne eller politikerne. Brug gerne noget, I målte i '
    'naturfagsugen.',
    'PÅSTANDEN', 'Hvem skal betale for det, vi smider ud?',
    ['Indpakningen om én agurk', 'En skraldespand efter en fredag',
     'Et tal fra jeres eget forsøg']),

   ('Tale', 'En tale til sidste skoledag',
    'Skriv den tale, du ville holde for din årgang. En tale skal høres, '
    'ikke læses: korte sætninger, gentagelser, og noget konkret, alle var '
    'med til.',
    'DET, DE SKAL HUSKE', 'Hvad var vi sammen om?',
    ['Den dag, noget gik galt for alle', 'En vits, kun I forstår',
     'Noget, I kunne i 9., som I ikke kunne i 7.']),
  ]),

 ('saet3', 'Sæt 3', 'Dig og fremtiden',
  'Tre opgaver om at skulle vælge, før man ved nok. Vælg én. '
  'Den første er essayet — genren er forklaret under menupunktet Essay.',
  [
   ('Essay', 'Vælg ét af tre emner',
    'Skriv et essay. Vælg <b>ét</b> af de tre emner: <b>sociale medier og '
    'forventningspres</b>, <b>drømme om fremtid og uddannelse</b> eller '
    '<b>tanker om fremtidens arbejdsmarked med AI</b>. Begynd i noget '
    'konkret, du selv har stået i, og zoom ud undervejs.',
    'DET STORE SPØRGSMÅL', 'Hvad er forskellen på en drøm og en plan?',
    ['Et billede, du slettede igen',
     'Første gang nogen spurgte, hvad du skulle være',
     'Første gang du lod en maskine skrive for dig']),

   ('Debatindlæg', 'Må man bruge AI i skolen?',
    'Skriv et debatindlæg om, hvor grænsen går. Vær konkret: hvad er hjælp, '
    'og hvad er snyd? Undgå at ende i en liste over fordele og ulemper.',
    'PÅSTANDEN', 'Hvor går grænsen mellem hjælp og snyd?',
    ['En opgave, du fik hjælp til', 'En lærer, der sagde nej',
     'Noget, du gerne vil kunne helt selv']),

   ('Novelle', 'Mennesket og maskinen',
    'Skriv en novelle, hvor en maskine kan noget, et menneske plejede at '
    'kunne. Vælg synsvinkel med omhu — hvem fortæller, og hvad kan den '
    'person ikke se?',
    'DET, LÆSEREN SKAL MÆRKE', 'Hvad mister man, når noget bliver nemt?',
    ['Et arbejde, nogen i din familie har', 'En hånd, der holder op med noget',
     'En stemme, der ikke er et menneskes']),
  ]),
]

# -------------------------------------------------------------- essayet
KENDETEGN = [
    ('Fri genre',
     'Du blander egne oplevelser, tanker, følelser og observationer med '
     'generelle betragtninger.'),
    ('Undersøgende tone',
     'Du starter ofte et sted i det helt konkrete — en hændelse, en genstand '
     'eller en situation — og "zoomer ud" for at reflektere over det store '
     'spørgsmål.'),
    ('Skrivetænkning',
     'Teksten skal virke som en igangværende tankeproces, hvor du betragter '
     'emnet fra flere forskellige vinkler.'),
    ('Levende sprog',
     'Brug billedsprog — metaforer, sammenligninger — sansninger og et '
     'personligt, men stadig præcist sprog.'),
]

# Kurverne viser en bevaegelse, ikke data. Pointen er forholdet mellem de tre.
KURVER = [
    ('Stil', [.15, .20, .14, .22, .18, .15]),
    ('Kronik', [.80, .84, .80, .88, .84, .88]),
    ('Essay', [.22, .74, .30, .86, .34, .80]),
]
AFSNIT = [('Indledning', 1), ('Hoveddel', 3), ('Afslutning', 1)]

GENNEMLAESNING = [
    ('Gentagelser', 'står det samme to gange?'),
    ('Udsagnsord', 'kan det blive mere præcist?'),
    ('Tillægsord', 'fylder det bare?'),
    ('Stavning', 'og kommaer'),
]

TRIN = [
    ('Læs opgaveformuleringen grundigt',
     ['Hvad er kernen i emnet? Hvilke tekster eller billeder følger med som '
      'afsæt, og hvordan kan du bruge dem som springbrættet til dine egne '
      'tanker?'],
     None, None),

    ('Brainstorm og find dit personlige vink',
     ['Spørg dig selv: Hvad betyder det her emne for mig? Hvornår har jeg '
      'oplevet noget lignende?',
      '<b>Undgå at skrive en kedelig stil eller en belærende kronik.</b>'],
     None, None),

    ('Byg essayet op',
     ['<b>Indledning.</b> Fang læseren med en skarp observation, en lille '
      'historie eller en undren. Undgå "I dette essay vil jeg …".',
      '<b>Hoveddel.</b> Bevæg dig frem og tilbage mellem det konkrete — en '
      'episode fra dit liv eller en detalje — og det abstrakte: tanker, '
      'filosofi, samfundet. Lad tankerne udvikle sig undervejs.',
      '<b>Afslutning.</b> Konkludér ikke med et tungt og kedeligt punktum, '
      'men lad tanken hænge i luften eller perspektivér til noget større.'],
     FG.konkret_abstrakt(KURVER, AFSNIT),
     'Det er bevægelsen, der gør et essay til et essay. Stilen bliver nede i '
     'det konkrete, og kronikken bliver oppe i det abstrakte — essayet går op '
     'og ned mellem dem hele vejen igennem. Læg mærke til, at det ender '
     'oppe: tanken skal hænge i luften, ikke lukkes.'),

    ('Gennemlæs og spil sproget op',
     ['Er der for mange gentagelser? Kan du gøre et udsagnsord eller et '
      'tillægsord mere præcist? Tjek for basale retstavnings- og kommafejl.'],
     FG.kredsloeb(GENNEMLAESNING, ('Læs højt', 'en gang til')),
     'De fire spørgsmål, du stiller til din egen tekst. Læs højt — det er '
     'der, gentagelserne høres.'),
]

# ------------------------------------------------------------------ html
saet_html = ''
for ident, maerke, titel, intro, opgaver in SAET:
    saet_html += (f'<h2 class="sec" id="{ident}">{maerke} · '
                  f'{html.escape(titel)}</h2>'
                  f'<p class="sec">{html.escape(intro)}</p>')
    for nr, (genre, o, tekst, etiket, kerne, indgange) in enumerate(opgaver, 1):
        saet_html += (
            f'<section class="opg"><h3><em>Opgave {nr}</em> '
            f'<span class="genre">{html.escape(genre)}</span> '
            f'{html.escape(o)}</h3><p>{tekst}</p>'
            f'<div class="figur">'
            f'{FG.afsaet(kerne, indgange, overskrift=etiket)}</div></section>')

kendetegn_html = ''.join(
    f'<tr><th>{html.escape(a)}</th><td>{b}</td></tr>' for a, b in KENDETEGN)

trin_html = ''
for i, (o, stykker, figur, figtekst) in enumerate(TRIN, 1):
    trin_html += (f'<section class="afsnit"><h2><span class="num">{i}</span>'
                  f'{html.escape(o)}</h2>')
    trin_html += ''.join(f'<p>{t}</p>' for t in stykker)
    if figur:
        trin_html += (f'<div class="figur">{figur}'
                      f'<div class="figtekst">{figtekst}</div></div>')
    trin_html += '</section>'

# CSS'en kommer fra funktioner-og-ligninger.html: det er den side, der har
# .top-inner og .jump — menupunkterne oeverst — og ikke .tabs.
BASIS = open('funktioner-og-ligninger.html', encoding='utf-8').read()
CSS = BASIS[BASIS.find('<style>') + 7:BASIS.find('</style>')]
CSS += '''
.figur{background:var(--panel2);border:1px solid var(--line);border-radius:14px;
padding:18px;margin:16px 0 0;text-align:center}
.figur svg{max-width:100%;height:auto}
.figtekst{color:var(--muted);font-size:.9rem;margin-top:10px;text-align:left;
max-width:68ch;margin-left:auto;margin-right:auto}
.afsnit{background:var(--panel);border:1px solid var(--line);
border-left:5px solid var(--accent);border-radius:14px;padding:18px 22px;
margin:14px 0;box-shadow:var(--shadow)}
.afsnit h2{font-size:1.2rem;margin:0 0 10px;display:flex;align-items:center;
gap:12px;border:0;padding:0}
.afsnit .num{width:30px;height:30px;border-radius:9px;display:grid;
place-items:center;font-weight:800;font-size:.95rem;background:var(--accent);
color:#fff;flex:0 0 auto}
.afsnit p{margin:8px 0;color:var(--muted);font-size:.97rem;max-width:74ch}
.afsnit p b{color:var(--ink)}
.opg{background:var(--panel);border:1px solid var(--line);border-radius:14px;
padding:18px 22px;margin:12px 0;box-shadow:var(--shadow)}
.opg h3{font-size:1.08rem;margin:0 0 8px}
.opg h3 em{font-style:normal;color:var(--muted);font-weight:700;
margin-right:8px;font-size:.86rem;text-transform:uppercase;
letter-spacing:.4px}
.opg .genre{background:var(--accent-soft);color:var(--accent);font-weight:700;
font-size:.8rem;padding:3px 10px;border-radius:999px;margin-right:8px;
vertical-align:2px}
.opg p{margin:0;color:var(--muted);font-size:.97rem;max-width:74ch}
.opg p b{color:var(--ink)}
table.liste{width:100%;border-collapse:collapse;margin:12px 0;font-size:.95rem}
table.liste th,table.liste td{border:1px solid var(--line);padding:10px 12px;
text-align:left;vertical-align:top}
table.liste th{background:var(--panel2);width:28%}
h2.sec{font-size:1.4rem;margin:34px 0 4px;scroll-margin-top:72px}
p.sec{color:var(--muted);max-width:74ch;margin:0 0 10px;font-size:.97rem}
.printbtn{background:#fff;border:1px solid var(--line);border-radius:10px;
padding:10px 18px;font-weight:700;font-size:.95rem;cursor:pointer;
color:var(--ink);font-family:inherit;margin:6px 8px 0 0}
.printbtn:hover{border-color:var(--accent);color:var(--accent)}
@media print{header.top,.printbtn{display:none!important}
.opg,.afsnit,.figur{box-shadow:none;break-inside:avoid;page-break-inside:avoid}
body{font-size:11pt}main{padding:0}@page{size:A4;margin:14mm}}
'''

KROP = f'''<section class="hero" id="start">
<span class="pill">Skriftlig fremstilling</span>
<h1>Dansk i 9. klasse</h1>
<p>Tre opgavesæt. Du vælger én opgave i det sæt, vi er i gang med. Under
<b>Essay</b> står det, du skal vide om den genre, hvis du vælger den.</p>
<button class="printbtn" onclick="window.print()">Print siden</button>
</section>
{saet_html}
<h2 class="sec" id="essay">Essay · sådan skriver du et</h2>
<p class="sec">Essayet er den frieste af genrerne, og det er derfor, den er
svær. Her er, hvad den kræver, og hvordan du kommer igennem.</p>
<h3 class="und">Hvad kendetegner et essay?</h3>
<table class="liste"><tbody>{kendetegn_html}</tbody></table>
<h3 class="und">Trin for trin gennem skriveprocessen</h3>
{trin_html}
<button class="printbtn" onclick="window.print()">Print siden</button>'''

MENU = ''.join(f'<a href="#{i}">{m}</a>' for i, m, *_ in SAET)

DOK = ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
       '<meta name="viewport" content="width=device-width,initial-scale=1">'
       '<title>Dansk · skriftlig fremstilling · 9. klasse</title><style>'
       + CSS + '\n.und{font-size:1.05rem;margin:22px 0 6px}\n'
       '</style></head><body><header class="top"><div class="top-inner">'
       '<div class="brand">Dansk · <span>9. klasse</span></div>'
       '<nav class="jump">' + MENU + '<a href="#essay">Essay</a></nav>'
       '</div></header><main>' + KROP + '</main><footer>'
       'Undervisningsmateriale · 9. klasse · Mibelibsen.</footer></body></html>')

open(UD, 'w', encoding='utf-8').write(DOK)
print(f'skrevet:  {UD}  ·  {len(SAET)} sæt · '
      f'{sum(len(s[4]) for s in SAET)} opgaver · {DOK.count("<svg")} figurer')
