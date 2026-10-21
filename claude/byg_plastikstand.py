# -*- coding: utf-8 -*-
"""Bygger plastik-stand.html — rammen om ungernes eget forloeb i uge 44.

Grupper paa tre til fem bygger en stand om plastik, som besoegende fra andre
klasser og foraeldre kan komme igennem. Siden er rammen, ikke forloebet: den
siger, hvad der skal vaere med, og giver plads til at skrive det. Den kan
printes, saa hver gruppe har ét ark.

**Der er ingen eksempler paa siden med vilje.** Ungerne skal opfinde deres
egen undervisning om plastik, og de har deres egne noter fra naturfagsugen at
hente inspiration i. Et eksempel paa et maal eller en stand bliver afskrevet i
stedet for taenkt - saa er opgaven lavet for dem. Felterne staar tomme, og
figurerne viser formen, ikke indholdet.

    python3 claude/byg_plastikstand.py
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figurer as FG

UD = 'plastik-stand.html'

# Den besoegendes vej gennem en stand - eksemplet i del 2.
# Tomme med vilje: figuren viser, at en stand har zoner i en raekkefoelge.
# Hvad zonerne hedder, er det, gruppen skal finde ud af.
ZONER = [('', '', '') for _ in range(4)]

# Maalet: det handler om den besoegende, ikke om jer.
MAAL_TRIN = [
    ('Før', 'Den besøgende ved ikke, at …', 'foer'),
    ('På standen', 'Den besøgende prøver selv at …', 'under'),
    ('Efter', 'Den besøgende kan selv …', 'efter'),
]

# Standen holder aabent baade fredag og loerdag, saa ugen gaar til loerdag.
UGE = [('Uge 44', ['Man', 'Tir', 'Ons', 'Tor', 'Fre', 'Lør'], [
    ('Man', 'Man', ('Idé og mål', 'Idé'), 'plan'),
    ('Tir', 'Ons', ('Byg standen, skaf materialer', 'Byg'), 'byg'),
    ('Tor', 'Tor', ('Prøvekørsel', 'Prøve'), 'proeve'),
    ('Fre', 'Lør', ('Åbent for besøgende', 'Åbent'), 'aabent'),
])]
UGE_FARVER = {'plan': FG.BLA, 'byg': FG.GRO, 'proeve': FG.ORA,
              'aabent': FG.ROD}

# Et punkt uden forklaring staar alene - de er ikke alle lige lange.
RAMMEN = [
    ('Tre til fem i gruppen', 'Alle skal have en rolle, der er noget værd '
     'hele tiden.'),
    ('Ét bord eller et tilsvarende stykke plads pr. gruppe', ''),
    ('Ca. 15 minutter pr. besøgende', ''),
    ('Den skal kunne køre flere gange i løbet af både fredag og lørdag',
     'Alt, hvad I bruger op, skal kunne fyldes op igen. Tænk det med fra '
     'starten.'),
    ('Besøgende er både børn og voksne fredag og lørdag', ''),
]

# (overskrift, [afsnit], figur, figurtekst, skrivefelt)
# skrivefelt: ('linjer', overskrift, antal) eller
#             ('skema', overskrift, [kolonner], antal raekker)
DELE = [
 ('Målet', [
   'Et mål er ikke, hvad <b>I</b> vil lave. Det er, hvad den <b>besøgende</b> '
   'kan bagefter. Prøv at skrive sætningen færdig: <i>"Efter vores stand kan '
   'den besøgende …"</i>',
   'Hvis I ikke kan skrive den sætning, ved I ikke, hvad standen går ud på — '
   'og så kan de besøgende heller ikke finde ud af det.',
   '<b>Højst to mål.</b> Ét er bedre. Syv minutter er ikke lang tid.'],
  FG.procesdiagram(MAAL_TRIN, W=620,
                   farver={'foer': FG.MUT, 'under': FG.BLA, 'efter': FG.GRO}),
  'Målet måles på forskellen mellem første og sidste kasse — ikke på, hvor '
  'meget I nåede at fortælle. Sætningerne skal gøres færdige af jer.',
  ('linjer', 'Jeres mål', 5)),

 ('Standen', [
   'Tegn bordet set oppefra, før I bygger noget. Hvor står den besøgende? '
   'Hvor står I? Hvad er det første, man ser?',
   'En stand, der virker, har som regel en <b>rute</b>: man kommer ind et '
   'sted, laver noget i midten og går derfra med noget. Hvis alt ligger i en '
   'bunke, ved den besøgende ikke, hvor han skal begynde.',
   'Husk det kedelige: strøm, vand, spild, skraldespand. Og husk, at nogen '
   'skal kunne se standen på afstand — hvad er jeres skilt?'],
  FG.standplan(ZONER),
  'Formen på en stand: zoner i en rækkefølge, og én fra gruppen ved hver. '
  'Hvad zonerne hedder, og hvad der sker i dem, bestemmer I selv — print '
  'siden, og udfyld figuren i hånden.',
  ('linjer', 'Jeres stand — beskriv hver zone', 6)),

 ('Medier og materialer', [
   'Skriv <b>alt</b> ned, også det, I tror, der er i forvejen. Det er altid '
   'det, ingen skrev ned, der mangler fredag morgen.',
   'Der er to slags. <b>Medier</b> er det, der viser noget — skilt, plakat, '
   'skærm, lyd, en QR-kode. <b>Materialer</b> er det, der bliver brugt, og '
   'som kan slippe op.',
   'Ud for hver ting skal der stå, <b>hvem</b> der skaffer den, og hvornår '
   'den er her. Ikke "nogen". Et navn.'],
  None, None,
  ('skema', 'Jeres medie- og materialeliste',
   ['Hvad', 'Antal', 'Hvorfra', 'Hvem skaffer det', 'Hvornår'], 11)),

 ('Opgaver, så standen bliver færdig', [
   'En opgave er noget, <b>én person</b> kan gøre færdig, og som man kan se '
   'er færdig. "Lave plakaten" er en opgave. "Arbejde med plakaten" er ikke.',
   'Skriv opgaverne op, og sæt et navn og en dag på hver. Det, der ikke har '
   'et navn, bliver ikke gjort.',
   'Læg de ting først, som <b>andre venter på</b>: skal plakaten printes, '
   'skal teksten være færdig i god tid før.'],
  FG.aarslinje(UGE, W=620, farver=UGE_FARVER),
  'Fredag og lørdag er der åbent — resten er rækkefølgen og ikke skemaet; '
  'det får I af læreren. Læg mærke til, at prøvekørslen har sin egen dag. '
  'Den skal ikke klemmes ind fredag morgen.',
  ('skema', 'Jeres opgaveliste',
   ['Opgave', 'Hvem', 'Hvornår', 'Færdig'], 11)),

 ('Roller og ansvar', [
   'Giv hinanden roller, der gælder <b>hele dagen</b>. Rollerne byttes ikke '
   'undervejs — det er dér, standene går i stå.',
   'Find selv ud af, hvilke roller netop jeres stand har brug for. De '
   'afhænger af, hvad der sker på den: en stand, hvor de besøgende selv laver '
   'noget, har brug for andre roller end en, hvor de ser på.',
   'Er I tre, får nogen to roller. Er I fem, kan to deles om den samme, så I '
   'kan skiftes til at holde pause — der kommer besøgende i mange timer.',
   'Uanset rollerne: <b>alle</b> i gruppen skal kunne svare på det, standen '
   'handler om. En besøgende spørger den, der står nærmest — ikke den, der '
   'kan svaret.'],
  None, None,
  ('skema', 'Jeres roller', ['Rolle', 'Navn', 'Ansvar på dagen'], 6)),
]


def tomt_skema(kolonner, raekker):
    """Et skema med overskrifter og tomme felter. Formen er givet, resten er
    deres. Bredden paa kolonnerne fordeles, saa den foerste faar mest plads -
    det er dér, der skal skrives mest."""
    n = len(kolonner)
    bred = [40 if i == 0 else 60 / (n - 1) for i in range(n)]
    hoved = ''.join(f'<th style="width:{b:.0f}%">{html.escape(k)}</th>'
                    for k, b in zip(kolonner, bred))
    krop = ('<tr>' + '<td></td>' * n + '</tr>') * raekker
    return f'<table class="skema"><thead><tr>{hoved}</tr></thead>' \
           f'<tbody>{krop}</tbody></table>'


TJEK = [
 'Vi kan sige vores mål højt i én sætning, der begynder med "Efter vores stand kan den besøgende …".',
 'Standen er prøvet på en, der ikke vidste noget i forvejen.',
 'Vi har taget tid på den — den holder sig omkring de 15 minutter.',
 'Alt på materialelisten er her, og der er nok til hele dagen.',
 'Alle fire roller er besat, og alle kan svare på, hvad standen handler om.',
 'Standen kan ryddes op og gøres klar igen på to minutter.',
 'Der er et skilt, man kan læse på tre meters afstand.',
]

# ------------------------------------------------------------------- opsaetning
dele_html = ''
for i, (o, stykker, figur, figtekst, felt) in enumerate(DELE, 1):
    dele_html += (f'<section class="afsnit"><h2><span class="num">{i}</span>'
                  f'{html.escape(o)}</h2>')
    dele_html += ''.join(f'<p>{t}</p>' for t in stykker)
    if figur:
        dele_html += (f'<div class="figur">{figur}'
                      f'<div class="figtekst">{html.escape(figtekst)}</div>'
                      f'</div>')
    art, titel = felt[0], felt[1]
    indhold = (f'<div class="linjer" style="height:{felt[2] * 26}px"></div>'
               if art == 'linjer' else tomt_skema(felt[2], felt[3]))
    dele_html += (f'<div class="skriv"><h3>{html.escape(titel)}</h3>'
                  f'{indhold}</div></section>')

rammen_html = ''.join(
    f'<li><b>{html.escape(a)}</b>'
    + (f' — {html.escape(b)}' if b else '') + '</li>' for a, b in RAMMEN)
tjek_html = ''.join(f'<li>{html.escape(t)}</li>' for t in TJEK)

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
margin:16px 0;box-shadow:var(--shadow)}
.afsnit h2{font-size:1.2rem;margin:0 0 10px;display:flex;align-items:center;
gap:12px}
.afsnit .num{width:30px;height:30px;border-radius:9px;display:grid;
place-items:center;font-weight:800;font-size:.95rem;background:var(--accent);
color:#fff;flex:0 0 auto}
.afsnit p{margin:8px 0;color:var(--muted);font-size:.97rem;max-width:74ch}
.afsnit p b{color:var(--ink)}
table.skema{width:100%;border-collapse:collapse;font-size:.92rem;
table-layout:fixed}
table.skema th,table.skema td{border:1px solid var(--line);padding:7px 9px;
text-align:left}
table.skema th{background:var(--panel2);font-size:.82rem;letter-spacing:.4px;
text-transform:uppercase;color:var(--muted)}
table.skema td{height:26px}
.skriv{border:1.5px dashed var(--line);border-radius:12px;padding:12px 18px 16px;
margin:14px 0;background:#fff}
.skriv h3{font-size:.82rem;letter-spacing:.5px;text-transform:uppercase;
color:var(--muted);margin:0 0 8px}
.linjer{background-image:repeating-linear-gradient(to bottom,transparent 0,
transparent 25px,var(--line) 25px,var(--line) 26px)}
.ramme{background:var(--accent-soft);border:1px solid var(--line);
border-left:4px solid var(--accent);border-radius:12px;padding:14px 20px 16px;
margin:18px 0}
.ramme ul{margin:0;padding-left:20px}
.ramme li{color:var(--muted);font-size:.96rem;margin:7px 0;max-width:74ch}
.ramme li b{color:var(--ink)}
ul.tjek{list-style:none;padding:0;margin:12px 0;max-width:76ch}
ul.tjek li{background:var(--panel);border:1px solid var(--line);
border-radius:10px;padding:10px 14px 10px 40px;margin:7px 0;position:relative;
color:var(--muted);font-size:.95rem}
ul.tjek li:before{content:"";position:absolute;left:14px;top:12px;width:13px;
height:13px;border:1.5px solid var(--muted);border-radius:3px}
.printbtn{background:#fff;border:1px solid var(--line);border-radius:10px;
padding:10px 18px;font-weight:700;font-size:.95rem;cursor:pointer;
color:var(--ink);font-family:inherit;margin:6px 8px 0 0}
.printbtn:hover{border-color:var(--accent);color:var(--accent)}
h2.sec{font-size:1.4rem;margin:30px 0 6px}
/* to afsnit i heroen loeb sammen til én klump uden den her */
.hero p+p{margin-top:12px}
@media print{header.top,.printbtn,.btnlink{display:none!important}
.afsnit,.figur,.skriv,.eks{box-shadow:none;break-inside:avoid;
page-break-inside:avoid}
body{font-size:11pt}main{padding:0}@page{size:A4;margin:13mm}}
'''

KROP = f'''<section class="hero">
<span class="pill">Feature · uge 44 · plastik</span>
<h1>Lav undervisning om plastik</h1>
<p>I skal lave jeres eget undervisningsforløb om plastik og afholde det fra
et bord, som om det var en stand på en messe. De besøgende er børn fra andre
klasser og forældre. De kommer, prøver noget, og går igen — og bagefter er de
klogere end da de kom.</p>
<p>Dette er en ramme, hvor I skal beskrive jeres stand, hvem der gør hvad,
hvordan og hvorfor, og hvad I skal bruge af materialer.</p>
<button class="printbtn" onclick="window.print()">Print rammen</button>
</section>
<h2 class="sec">Beskrivelse</h2>
<div class="ramme"><ul>{rammen_html}</ul></div>
<h2 class="sec">De fem dele, der skal være med</h2>
<p style="color:var(--muted);max-width:74ch">Hver del har en forklaring og
en plads, I skriver i. Der er ingen eksempler — de ville blive skrevet af i
stedet for tænkt. Printer I siden, har I jeres plan på ét sted, og så kan den
ligge på standen.</p>
{dele_html}
<h2 class="sec">Prøvekørslen</h2>
<div class="ramme"><ul>
<li><b>Prøv standen på en, der ikke ved noget om den.</b> En fra en anden
gruppe, en lærer, en lillebror. Ikke jer selv — I ved allerede svaret, og så
virker alt.</li>
<li><b>Tag tid.</b> Fra "hej" til "farvel". Tager det meget mere end et kvarter, skal der
skæres noget væk, ikke tales hurtigere.</li>
<li><b>Sig ingenting undervejs.</b> Lad den besøgende prøve. Hver gang I er
nødt til at forklare noget ekstra, har I fundet et sted, standen ikke er
tydelig nok.</li>
<li><b>Ryd op bagefter, og tag tid på det også.</b> Kan I ikke være klar igen
på to minutter, holder standen ikke en hel dag.</li>
</ul></div>
<h2 class="sec">Tjek før I åbner</h2>
<ul class="tjek">{tjek_html}</ul>
<h2 class="sec">Hvor idéen skal komme fra</h2>
<p style="color:var(--muted);max-width:74ch">Fra jer. Standen er jeres eget
lille undervisningsforløb, og der står ikke nogen steder, hvad den skal
handle om — ud over plastik.</p>
<p style="color:var(--muted);max-width:74ch">Hent inspiration i <b>jeres egne
noter fra naturfagsugen</b>. Hvad undrede jer dengang? Hvad var der ikke tid
til at undersøge? Hvad troede I, før I målte, og hvad viste det sig at være?
Det sidste er som regel det bedste sted at begynde: <b>en stand er stærk, når
den besøgende tror ét og opdager noget andet.</b></p>
<button class="printbtn" onclick="window.print()">Print rammen</button>'''

DOK = ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
       '<meta name="viewport" content="width=device-width,initial-scale=1">'
       '<title>Lav undervisning om plastik · uge 44 · 9. klasse</title><style>'
       + CSS + '</style></head><body><header class="top"><div class="top-inner">'
       '<a class="brand" href="index.html">Mibelibsen <span>9. klasse</span></a>'
       '<nav class="tabs"><a class="" href="matematik.html">Matematik</a>'
       '<a class="" href="samfundsfag.html">Samfundsfag</a>'
       '<a class="" href="tysk.html">Tysk</a><a class="" href="fysik.html">Fysik</a>'
       '</nav></div></header><main>' + KROP + '</main><footer>'
       'Undervisningsmateriale · 9. klasse · Mibelibsen.</footer></body></html>')

open(UD, 'w', encoding='utf-8').write(DOK)
print(f'skrevet:  {UD}  ·  {len(DELE)} dele, '
      f'{sum(1 for d in DELE if d[2])} figurer, {len(TJEK)} tjekpunkter')
