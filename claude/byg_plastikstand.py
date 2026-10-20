# -*- coding: utf-8 -*-
"""Bygger plastik-stand.html — rammen om ungernes eget forloeb i uge 44.

Grupper paa tre til fem bygger en stand om plastik, som besoegende fra andre
klasser og foraeldre kan komme igennem. Siden er rammen, ikke forloebet: den
siger, hvad der skal vaere med, viser et eksempel paa hver del og giver plads
til at skrive deres eget. Den kan printes, saa hver gruppe har ét ark.

    python3 claude/byg_plastikstand.py
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figurer as FG

UD = 'plastik-stand.html'

# Den besoegendes vej gennem en stand - eksemplet i del 2.
ZONER = [
    ('Velkomst', 'Ét spørgsmål, der fanger', 'Vært'),
    ('Prøv selv', 'Den besøgende gør noget', 'Instruktør'),
    ('Svaret', 'Hvad viste det?', 'Forklarer'),
    ('Tag med', 'Noget at huske det på', 'Vært'),
]

# Maalet: det handler om den besoegende, ikke om jer.
MAAL_TRIN = [
    ('Før', 'Den besøgende ved ikke, at …', 'foer'),
    ('På standen', 'Den besøgende prøver selv at …', 'under'),
    ('Efter', 'Den besøgende kan selv …', 'efter'),
]

UGE = [('Uge 44', ['Man', 'Tir', 'Ons', 'Tor', 'Fre'], [
    ('Man', 'Man', ('Idé og mål', 'Idé'), 'plan'),
    ('Tir', 'Ons', ('Byg standen, skaf materialer', 'Byg'), 'byg'),
    ('Tor', 'Tor', ('Prøvekørsel', 'Prøve'), 'proeve'),
    ('Fre', 'Fre', ('Åbent hele dagen', 'Åbent'), 'aabent'),
])]
UGE_FARVER = {'plan': FG.BLA, 'byg': FG.GRO, 'proeve': FG.ORA,
              'aabent': FG.ROD}

RAMMEN = [
    ('Tre til fem i gruppen', 'Alle skal have en rolle, der er noget værd '
     'hele tiden.'),
    ('Ét bord', 'Alt skal kunne stå på det, og det skal kunne ryddes på fem '
     'minutter.'),
    ('7–10 minutter pr. besøgende', 'Kort nok til, at der kan komme mange '
     'igennem. Langt nok til, at de laver noget selv.'),
    ('Den skal kunne køre hele dagen', 'Alt, hvad I bruger op, skal kunne '
     'fyldes op igen. Tænk det med fra starten.'),
    ('Besøgende er både børn og voksne', 'Samme stand skal virke for en fra '
     '3. klasse og for en forælder. Det er den sværeste del af opgaven.'),
]

# (nr, overskrift, [afsnit], figur, figurtekst, eksempeloverskrift,
#  [eksempellinjer], skrivefelt-overskrift, antal_linjer)
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
  'meget I nåede at fortælle.',
  'Sådan kan et mål se ud',
  ['Efter vores stand kan den besøgende <b>kende forskel på de tre '
   'plasttyper</b> ved at se på mærket i bunden.',
   'Efter vores stand kan den besøgende <b>nævne én ting, plastemballage gør '
   'bedre end papir</b>, og én ting den gør værre.'],
  'Jeres mål', 4),

 ('Standen', [
   'Tegn bordet set oppefra, før I bygger noget. Hvor står den besøgende? '
   'Hvor står I? Hvad er det første, man ser?',
   'En stand, der virker, har som regel en <b>rute</b>: man kommer ind et '
   'sted, laver noget i midten og går derfra med noget. Hvis alt ligger i en '
   'bunke, ved den besøgende ikke, hvor han skal begynde.',
   'Husk det kedelige: strøm, vand, spild, skraldespand. Og husk, at nogen '
   'skal kunne se standen på afstand — hvad er jeres skilt?'],
  FG.standplan(ZONER),
  'Et eksempel på en rute. Zonerne må gerne hedde noget andet, men der skal '
  'være en rækkefølge, og den besøgende skal kunne se den uden at spørge.',
  'Sådan kan standen beskrives',
  ['<b>Venstre ende:</b> skilt med spørgsmålet "Hvilken pose er værst?" og '
   'tre poser lagt frem.',
   '<b>Midten:</b> vægten og tre bægre. Den besøgende vejer selv.',
   '<b>Højre ende:</b> plakaten med svaret, og en skål med små mærkater.'],
  'Jeres stand — tegn den og beskriv den', 6),

 ('Medier og materialer', [
   'Skriv <b>alt</b> ned, også det, I tror, der er i forvejen. Det er altid '
   'det, ingen skrev ned, der mangler fredag morgen.',
   'Del listen i to: <b>medier</b> er det, der viser noget — skilt, plakat, '
   'skærm, QR-kode, lyd. <b>Materialer</b> er det, der bliver brugt — poser, '
   'bægre, vand, tape, mærkater.',
   'Ud for hver ting skal der stå, <b>hvem</b> der skaffer den, og hvornår '
   'den er her. Ikke "nogen". Et navn.'],
  None, None,
  'Skriv listen sådan her',
  ['<b>Medie:</b> Plakat A3 med svaret · 1 stk. · printes på skolen · Asta · '
   'onsdag',
   '<b>Materiale:</b> Plastposer · 6 stk. · hjemmefra · Viktor · tirsdag',
   '<b>Materiale:</b> Køkkenvægt · 1 stk. · lånes i hjemkundskab · Nor · '
   'tirsdag'],
  'Jeres medie- og materialeliste', 10),

 ('Opgaver, så standen bliver færdig', [
   'En opgave er noget, <b>én person</b> kan gøre færdig, og som man kan se '
   'er færdig. "Lave plakaten" er en opgave. "Arbejde med plakaten" er ikke.',
   'Skriv opgaverne op, og sæt et navn og en dag på hver. Det, der ikke har '
   'et navn, bliver ikke gjort.',
   'Læg de ting først, som <b>andre venter på</b>: skal plakaten printes, '
   'skal teksten være færdig i god tid før.'],
  FG.aarslinje(UGE, W=620, farver=UGE_FARVER),
  'Et eksempel på en uge — ikke skemaet; det får I af læreren. Læg mærke '
  'til, at prøvekørslen har sin egen dag. Den skal ikke klemmes ind fredag '
  'morgen.',
  'Sådan kan en opgave se ud',
  ['Skrive teksten til plakaten · Asta · mandag · ✔',
   'Printe plakaten i A3 · Nor · onsdag · ✔',
   'Købe mærkater · Viktor · tirsdag · ikke endnu'],
  'Jeres opgaveliste', 10),

 ('Roller og ansvar', [
   'Giv hinanden roller, der gælder <b>hele dagen</b>. Rollerne byttes ikke '
   'undervejs — det er dér, standene går i stå.',
   'Er I tre, slår I to roller sammen. Er I fem, deler I værtsrollen, så I '
   'kan skiftes til at holde pause. Der kommer besøgende i mange timer.',
   'Alle i gruppen skal kunne svare på det, standen handler om. En besøgende '
   'spørger den, der står nærmest — ikke den, der kan svaret.'],
  None, None,
  'Fire roller, der plejer at virke',
  ['<b>Vært:</b> tager imod, stiller spørgsmålet, siger farvel. Taler mest.',
   '<b>Instruktør:</b> viser, hvad den besøgende selv skal gøre. Rører '
   'tingene.',
   '<b>Forklarer:</b> siger, hvad resultatet betyder. Kender tallene.',
   '<b>Materialemester:</b> fylder op, rydder op, holder styr på spild. '
   'Standen kan køre igen om to minutter.'],
  'Jeres roller — skriv navne på', 6),
]

TJEK = [
 'Vi kan sige vores mål højt i én sætning, der begynder med "Efter vores stand kan den besøgende …".',
 'Standen er prøvet på en, der ikke vidste noget i forvejen.',
 'Vi har taget tid på den — den holder sig under 10 minutter.',
 'Alt på materialelisten er her, og der er nok til hele dagen.',
 'Alle fire roller er besat, og alle kan svare på, hvad standen handler om.',
 'Standen kan ryddes op og gøres klar igen på to minutter.',
 'Der er et skilt, man kan læse på tre meters afstand.',
]

# ------------------------------------------------------------------- opsaetning
dele_html = ''
for i, (o, stykker, figur, figtekst, eks_o, eks, skriv_o, linjer) in enumerate(
        DELE, 1):
    dele_html += (f'<section class="afsnit"><h2><span class="num">{i}</span>'
                  f'{html.escape(o)}</h2>')
    dele_html += ''.join(f'<p>{t}</p>' for t in stykker)
    if figur:
        dele_html += (f'<div class="figur">{figur}'
                      f'<div class="figtekst">{html.escape(figtekst)}</div>'
                      f'</div>')
    dele_html += (f'<div class="eks"><h3>{html.escape(eks_o)}</h3><ul>'
                  + ''.join(f'<li>{t}</li>' for t in eks) + '</ul></div>')
    dele_html += (f'<div class="skriv"><h3>{html.escape(skriv_o)}</h3>'
                  + '<div class="linjer" style="height:'
                  + f'{linjer * 26}px"></div></div>')
    dele_html += '</section>'

rammen_html = ''.join(
    f'<li><b>{html.escape(a)}</b> — {html.escape(b)}</li>' for a, b in RAMMEN)
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
.eks{background:var(--panel2);border:1px solid var(--line);border-radius:12px;
padding:12px 18px;margin:14px 0}
.eks h3{font-size:.82rem;letter-spacing:.5px;text-transform:uppercase;
color:var(--accent);margin:0 0 6px}
.eks ul{margin:0;padding-left:20px}
.eks li{color:var(--muted);font-size:.93rem;margin:5px 0;max-width:72ch}
.eks li b{color:var(--ink)}
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
@media print{header.top,.printbtn,.btnlink{display:none!important}
.afsnit,.figur,.skriv,.eks{box-shadow:none;break-inside:avoid;
page-break-inside:avoid}
body{font-size:11pt}main{padding:0}@page{size:A4;margin:13mm}}
'''

KROP = f'''<section class="hero">
<span class="pill">Feature · uge 44 · plastik</span>
<h1>Byg en stand om plastik</h1>
<p>I skal lave jeres eget lille undervisningsforløb og holde det fra en stand.
De besøgende er elever fra andre klasser og forældre. De kommer, prøver noget,
og går igen — og bagefter kan de noget, de ikke kunne før.</p>
<button class="printbtn" onclick="window.print()">Print rammen</button>
<a class="btnlink ghost" href="feature-plastik-og-foedevarer.html">Værkstedet om plast og fødevarer</a>
<a class="btnlink ghost" href="index.html">Forsiden</a>
</section>
<h2 class="sec">Rammen, I skal holde jer inden for</h2>
<div class="ramme"><ul>{rammen_html}</ul></div>
<h2 class="sec">De fem dele, der skal være med</h2>
<p style="color:var(--muted);max-width:74ch">Hver del har en forklaring, et
eksempel og en plads, I selv skriver i. Printer I siden, har I jeres plan på
ét sted — og så kan den ligge på standen.</p>
{dele_html}
<h2 class="sec">Prøvekørslen</h2>
<div class="ramme"><ul>
<li><b>Prøv standen på en, der ikke ved noget om den.</b> En fra en anden
gruppe, en lærer, en lillebror. Ikke jer selv — I ved allerede svaret, og så
virker alt.</li>
<li><b>Tag tid.</b> Fra "hej" til "farvel". Er det over 10 minutter, skal der
skæres noget væk, ikke tales hurtigere.</li>
<li><b>Sig ingenting undervejs.</b> Lad den besøgende prøve. Hver gang I er
nødt til at forklare noget ekstra, har I fundet et sted, standen ikke er
tydelig nok.</li>
<li><b>Ryd op bagefter, og tag tid på det også.</b> Kan I ikke være klar igen
på to minutter, holder standen ikke en hel dag.</li>
</ul></div>
<h2 class="sec">Tjek før I åbner</h2>
<ul class="tjek">{tjek_html}</ul>
<h2 class="sec">Hvor I kan hente idéer</h2>
<p style="color:var(--muted);max-width:74ch">Værkstedet fra naturfagsugen har
tre forsøg om plast og fødevarer — emballagetesten, bioplasten og
plasttyperne. De er lavet til en lektion, men de kan skæres ned og bygges om
til en stand. I må også gerne finde på noget helt andet.</p>
<a class="btnlink" href="feature-plastik-og-foedevarer.html">Åbn værkstedet</a>
<button class="printbtn" onclick="window.print()">Print rammen</button>'''

DOK = ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
       '<meta name="viewport" content="width=device-width,initial-scale=1">'
       '<title>Byg en stand om plastik · uge 44 · 9. klasse</title><style>'
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
