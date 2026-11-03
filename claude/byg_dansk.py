# -*- coding: utf-8 -*-
"""Bygger dansk.html — de skriftlige opgaver i dansk.

Siden samler genrerne, klassen skal kunne skrive. Lige nu er der én: essayet.
Teksten er brugerens egen; siden saetter den op og giver den to figurer.

    python3 claude/byg_dansk.py
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figurer as FG

UD = 'dansk.html'

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

# Kurverne er tegnet, ikke maalt: de viser en bevaegelse, ikke data. Pointen
# er forholdet mellem de tre. Stilen bliver nede i det konkrete, kronikken
# bliver oppe i det abstrakte, og essayet gaar op og ned mellem dem.
KURVER = [
    ('Stil', [.15, .20, .14, .22, .18, .15]),
    ('Kronik', [.80, .84, .80, .88, .84, .88]),
    ('Essay', [.22, .74, .30, .86, .34, .80]),
]
AFSNIT = [('Indledning', 1), ('Hoveddel', 3), ('Afslutning', 1)]

# Trin 4 i guiden, stillet op som den loekke den er. De fire spoergsmaal er
# dem, der staar i trinnet.
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

# Opgavesaet 3. Tre emner, ét essay. Hvert emne har tre konkrete indgange,
# fordi det er dét, der er svaert ved genren: at finde et sted at begynde,
# som man selv har staaet i. Det store spoergsmaal staar oeverst, men det er
# ikke en overskrift - det er det, teksten skal naa hen imod.
OPGAVER = [
    ('Sociale medier og forventningspres',
     'Hvem har vi travlt med at være noget for?',
     ['Et billede, du slettede igen',
      'En besked, du ikke svarede på',
      'Et tal, du tjekkede flere gange'],
     'Skriv om presset for at være en bestemt slags person online. Begynd i '
     'noget, du selv har gjort eller set — ikke i en generel betragtning om '
     'unge. Zoom først ud, når det konkrete står klart.'),

    ('Drømme om fremtid og uddannelse',
     'Hvad er forskellen på en drøm og en plan?',
     ['Første gang nogen spurgte, hvad du skulle være',
      'En drøm, du har lagt væk igen',
      'En voksen, du gerne vil ligne lidt'],
     'Skriv om at skulle vælge, før man ved nok. Du må gerne være i tvivl i '
     'teksten — et essay skal ikke ende med et svar, det skal ende et sted, '
     'læseren kan tænke videre fra.'),

    ('Fremtidens arbejdsmarked med AI',
     'Hvad skal mennesker kunne, når maskiner kan resten?',
     ['Første gang du lod en maskine skrive for dig',
      'Et arbejde, nogen i din familie har',
      'Noget, du gerne vil kunne helt selv'],
     'Skriv om arbejde og maskiner. Undgå at ende i en liste over fordele og '
     'ulemper — det er en kronik, ikke et essay. Hold fast i det, du selv har '
     'mærket.'),
]

opgaver_html = ''
for nr, (emne, spm, konkrete, tekst) in enumerate(OPGAVER, 1):
    opgaver_html += (
        f'<section class="opg"><h3><em>Emne {nr}</em> {html.escape(emne)}</h3>'
        f'<p>{html.escape(tekst)}</p>'
        f'<div class="figur">{FG.afsaet(spm, konkrete)}</div></section>')

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

BASIS = open('samfundsfag.html', encoding='utf-8').read()
CSS = BASIS[BASIS.find('<style>') + 7:BASIS.find('</style>')]
CSS += '''
.figur{background:var(--panel2);border:1px solid var(--line);border-radius:14px;
padding:18px;margin:18px 0;text-align:center}
.figur svg{max-width:100%;height:auto}
.figtekst{color:var(--muted);font-size:.9rem;margin-top:10px;text-align:left;
max-width:68ch;margin-left:auto;margin-right:auto}
.afsnit{background:var(--panel);border:1px solid var(--line);
border-left:5px solid var(--accent);border-radius:14px;padding:18px 22px;
margin:14px 0;box-shadow:var(--shadow)}
.afsnit h2{font-size:1.2rem;margin:0 0 10px;display:flex;align-items:center;
gap:12px}
.afsnit .num{width:30px;height:30px;border-radius:9px;display:grid;
place-items:center;font-weight:800;font-size:.95rem;background:var(--accent);
color:#fff;flex:0 0 auto}
.afsnit p{margin:8px 0;color:var(--muted);font-size:.97rem;max-width:74ch}
.afsnit p b{color:var(--ink)}
table.liste{width:100%;border-collapse:collapse;margin:12px 0;font-size:.95rem}
table.liste th,table.liste td{border:1px solid var(--line);padding:10px 12px;
text-align:left;vertical-align:top}
table.liste th{background:var(--panel2);width:28%}
h2.sec{font-size:1.4rem;margin:30px 0 6px}
.opg{background:var(--panel);border:1px solid var(--line);border-radius:14px;
padding:18px 22px;margin:14px 0;box-shadow:var(--shadow)}
.opg h3{font-size:1.1rem;margin:0 0 8px}
.opg h3 em{font-style:normal;color:var(--accent);font-weight:800;
margin-right:8px}
.opg p{margin:0;color:var(--muted);font-size:.97rem;max-width:74ch}
p.sec{color:var(--muted);max-width:74ch;margin:0 0 6px;font-size:.97rem}
.printbtn{background:#fff;border:1px solid var(--line);border-radius:10px;
padding:10px 18px;font-weight:700;font-size:.95rem;cursor:pointer;
color:var(--ink);font-family:inherit;margin:6px 8px 0 0}
.printbtn:hover{border-color:var(--accent);color:var(--accent)}
@media print{header.top,.printbtn,.btnlink{display:none!important}
.afsnit,.figur{box-shadow:none;break-inside:avoid;page-break-inside:avoid}
body{font-size:11pt}main{padding:0}@page{size:A4;margin:14mm}}
'''

KROP = f'''<section class="hero">
<span class="pill">Dansk · Skriftlige opgaver</span>
<h1>Essay</h1>
<p>Et essay er en tankeproces, man kan følge. Her er, hvad genren kræver, og
hvordan du kommer igennem skriveprocessen.</p>
<button class="printbtn" onclick="window.print()">Print siden</button>
<a class="btnlink ghost" href="index.html">Tilbage til forsiden</a>
</section>
<h2 class="sec">Hvad kendetegner et essay?</h2>
<table class="liste"><tbody>{kendetegn_html}</tbody></table>
<h2 class="sec">Trin for trin gennem skriveprocessen</h2>
<p class="sec">Fire trin. Det tredje er det, der afgør, om det bliver et essay
eller noget andet.</p>
{trin_html}
<h2 class="sec">Opgavesæt 3 · Skriv et essay</h2>
<p class="sec"><b>Vælg ét af de tre emner.</b> Du skriver i Word. Alle tre
emner er lagt an på, at du begynder i noget konkret fra dit eget liv og
arbejder dig ud mod det store spørgsmål — se trin 3 ovenfor.</p>
{opgaver_html}
<button class="printbtn" onclick="window.print()">Print siden</button>'''

DOK = ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
       '<meta name="viewport" content="width=device-width,initial-scale=1">'
       '<title>Essay · skriftlige opgaver i dansk · 9. klasse</title><style>'
       + CSS +
       '</style></head><body><header class="top"><div class="top-inner">'
       '<a class="brand" href="index.html">Mibelibsen <span>9. klasse</span></a>'
       '<nav class="tabs"><a class="" href="matematik.html">Matematik</a>'
       '<a class="" href="samfundsfag.html">Samfundsfag</a>'
       '<a class="" href="tysk.html">Tysk</a>'
       '<a class="" href="fysik.html">Fysik</a>'
       '<a class="active" href="dansk.html">Dansk</a>'
       '</nav></div></header><main>' + KROP + '</main><footer>'
       'Undervisningsmateriale · 9. klasse · Mibelibsen.</footer></body></html>')

open(UD, 'w', encoding='utf-8').write(DOK)
print(f'skrevet:  {UD}  ·  {len(TRIN)} trin, {len(OPGAVER)} emner, '
      f'{DOK.count("<svg")} figurer')
