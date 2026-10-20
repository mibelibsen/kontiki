# -*- coding: utf-8 -*-
"""Bygger hvad-er-socialisering.html — vores egen fagtekst om socialisering.

Den findes, fordi der ikke er nogen. Det frie danske materiale om
socialisering er enten leksikonkort (lex.dk) eller skrevet til gymnasiet
(samfundsfag.dk); resten ligger bag betaling hos Clio, Gyldendal og Alinea.
Teksten her er skrevet til 9. klasse og til det forloeb, de staar i:
begreberne skal kunne bruges paa deres egne svar i uge 43.

Siden er selvbaerende, har en figur til hver forklaring og kan printes.

    python3 claude/byg_socialisering_tekst.py
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figurer as FG

UD = 'hvad-er-socialisering.html'

# ---------------------------------------------------------------- figurerne
RINGE = [
    ('Primær', FG.GRO, 'familie · hjemmet'),
    ('Sekundær', FG.BLA, 'skole · venner · klub · job'),
    ('Tertiær', FG.ORA, 'feed · influencere · reklamer'),
]

NORM_TRIN = [
    ('Normen', 'Det, de fleste gør — og regner med at du også gør', 'norm'),
    ('Bruddet', 'Nogen gør noget andet', 'brud'),
    ('Sanktionen', 'Reaktionen: et blik, et grin, en kommentar — eller ros',
     'sank'),
    ('Normen står fast', 'Nu ved alle, hvor grænsen går. Den er bekræftet',
     'norm'),
]

PRES = [
    ('Hjemme', 'mobilen væk ved bordet'),
    ('I klassen', 'svar nu, ellers er du udenfor'),
    ('I feedet', 'bliv — der kommer mere'),
]

LOOP = [
    ('Du ser', 'et klip fanger dig'),
    ('Du reagerer', 'ser det færdigt, liker'),
    ('Den lærer', 'det her virker på dig'),
    ('Du får mere', 'af samme slags'),
]

# ------------------------------------------------------------------ teksten
# (overskrift, [afsnit], figur, figurtekst)
AFSNIT = [
 ('Socialisering er det, der sker, mens du ikke tænker over det',
  ['Du siger ikke goddag til din lærer på samme måde, som du siger hej til '
   'din bedste ven. Du sætter dig ikke på et bestemt sted i klassen, fordi '
   'nogen har sagt, du skal. Du ved bare, hvordan man gør — og du lagde '
   'mærke til det den dag, en ny i klassen gjorde det forkert.',
   'Den viden har du lært. Det er <b>socialisering</b>: den måde, et menneske '
   'lærer normer, værdier og færdigheder i den gruppe, det vokser op i. Det '
   'foregår hele livet, og det meste af det foregår, uden at nogen '
   'underviser i det.',
   'Man kan se det som ringe uden om en selv. Inderst er de få, man er tæt '
   'på. Yderst er det, der taler til alle på én gang. Ringene forsvinder '
   'ikke, når man bliver ældre — der kommer flere til.'],
  FG.socialisationsringe(RINGE),
  'De tre arenaer, socialiseringen foregår i. Den inderste ring er den '
  'første, man møder, ikke den vigtigste.'),

 ('Hvorfor de hedder primær, sekundær og tertiær',
  ['Navnene siger noget om <b>rækkefølgen</b>, ikke om hvor meget de betyder. '
   'Den primære kom først — den var der, før du kunne vælge noget som helst.',
   '<b>Primær socialisering</b> er familien og hjemmet. Her lærte du at tale, '
   'at spise med de andre, at sige undskyld. Det blev ikke forklaret; det '
   'blev gjort, og du gjorde det efter. Det er derfor, de ting sidder så '
   'dybt, at man først opdager dem, når man kommer hjem til en anden familie '
   'og ser, at de gør det anderledes.',
   '<b>Sekundær socialisering</b> er skolen, vennerne, klubben, fritidsjobbet. '
   'Her er der både regler, nogen har skrevet ned, og regler, ingen har '
   'skrevet ned. Ordensreglerne hænger på væggen. Reglen om, hvor lang tid '
   'der må gå, før man svarer, hænger ingen steder — og alle kender den.',
   '<b>Tertiær socialisering</b> er medierne: serier, reklamer, musik, '
   'influencere, feedet. Den er ny i historien. Dine oldeforældre blev '
   'socialiseret af familien og landsbyen, og det var stort set det.'],
  None, None),

 ('Normer holdes på plads af sanktioner',
  ['En <b>norm</b> er en uskreven regel for, hvad man gør. En <b>sanktion</b> '
   'er den reaktion, der kommer, når nogen gør noget andet. Sanktioner er '
   'sjældent straf. Det er et blik, en pause, der bliver et sekund for lang, '
   'et grin, nogen ikke er med i.',
   'Sanktioner kan også gå den anden vej. Får man ros, et like, en plads i '
   'gruppen, er det en <b>positiv sanktion</b> — og den virker lige så godt.',
   'Pointen er, at normen ikke er skrevet ned nogen steder. Den bliver '
   'vedligeholdt af reaktionerne. Derfor kan man finde normerne i en gruppe '
   'ved at se efter, hvad der bliver reageret på.'],
  # ingen legende: kasserne hedder allerede det, farverne ville forklare
  FG.procesdiagram(NORM_TRIN, W=620,
                   farver={'norm': FG.BLA, 'brud': FG.ORA, 'sank': FG.ROD}),
  'Et brud på en norm fører til en sanktion — og sanktionen gør normen '
  'tydeligere, end den var før. Derfor er et brud den nemmeste måde at få '
  'øje på en norm.'),

 ('Når arenaerne vil noget forskelligt',
  ['Arenaerne er der samtidig, og de er ikke altid enige. Hjemme må mobilen '
   'ikke være fremme ved bordet. I gruppechatten er et svar efter en time '
   'næsten en besked i sig selv. I feedet er der altid et klip mere.',
   'Når to arenaer kræver noget forskelligt af den samme person på samme tid, '
   'hedder det et <b>krydspres</b>. Man kan ikke gøre begge dele, og uanset '
   'hvad man vælger, bryder man en norm et sted.',
   'Det er værd at vide, fordi det flytter spørgsmålet. "Hvorfor kan du ikke '
   'bare lægge den væk?" lyder som et spørgsmål om viljestyrke. Set som '
   'krydspres er det et spørgsmål om, hvilken gruppe man svigter.'],
  FG.krydspres(PRES),
  'Tre arenaer, der vil noget forskelligt med den samme person samtidig. '
  'Det er ikke uvilje — det er et krydspres.'),

 ('Den tertiære arena har fået en motor',
  ['Et blad eller et tv-program viste det samme til alle. Et feed gør ikke. '
   'Det måler, hvad netop du bliver hængende ved, og giver dig mere af det. '
   'Jo længere du bliver, jo bedre kender det dig.',
   'Det betyder, at den tertiære socialisering ikke længere er den samme for '
   'en hel årgang. To i samme klasse kan have hver sit billede af, hvad der '
   'er normalt — fordi de har set hver sit.',
   'Det er også derfor, det er svært at svare på, hvad "unge synes". Der er '
   'ikke ét sted, de henter det fra.'],
  FG.kredsloeb(LOOP, ('Algoritmen', 'lærer af det, du gør')),
  'Kredsløbet gentager sig, hver gang du åbner appen. Du vælger det første '
  'klip. Derefter vælger den, der har målt dig, de næste.'),
]

# Brugen i uge 43: (spørg om svaret, så leder du efter)
ANALYSE = [
 ('Hvem taler personen om?',
  'Familie, venner, skole eller medier — altså hvilken arena svaret handler '
  'om. Nævnes der slet ingen voksne?'),
 ('Hvad tages for givet?',
  'Det, der ikke bliver forklaret, fordi det er selvfølgeligt. Dér ligger '
  'normen.'),
 ('Hvad bliver der reageret på?',
  'Et "man må jo ikke…", et "det er lidt pinligt, hvis…". Sanktionen '
  'afslører normen.'),
 ('Er der noget, der trækker i to retninger?',
  'Ord som "egentlig", "men", "jeg ville gerne". Det er ofte et krydspres.'),
 ('Hvor kommer billedet af det normale fra?',
  'Siger personen "alle gør det"? Spørg: alle hvor? I klassen eller i '
  'feedet?'),
]

ORD = [
 ('Socialisering', 'Den måde, et menneske lærer normer, værdier og '
  'færdigheder i den gruppe, det vokser op i. Foregår hele livet.'),
 ('Socialisationsarena', 'Et sted, socialiseringen foregår: hjemmet, '
  'klassen, klubben, feedet.'),
 ('Primær socialisering', 'Den første — familien og hjemmet. Læres, før man '
  'kan vælge, og sidder derfor dybt.'),
 ('Sekundær socialisering', 'Skolen, vennerne, fritiden, arbejdet. Både '
  'skrevne og uskrevne regler.'),
 ('Tertiær socialisering', 'Medierne: serier, reklamer, influencere, feedet. '
  'Den nyeste af de tre.'),
 ('Norm', 'En uskreven regel for, hvad man gør i en bestemt gruppe. Står '
  'ingen steder, og alle kender den.'),
 ('Sanktion', 'Reaktionen på, at en norm bliver brudt eller fulgt. Kan være '
  'negativ (et blik) eller positiv (et like).'),
 ('Krydspres', 'Når to arenaer kræver noget forskelligt af den samme person '
  'på samme tid.'),
]

KILDER = [
 ('Socialisering', 'Lex · Danmarks Nationalleksikon', 'Arne Poulsen, '
  'professor emeritus, RUC. Senest ændret 1. oktober 2024.',
  'https://lex.dk/socialisering'),
 ('Socialisation', 'samfundsfag.dk', 'Gennemgår primær, sekundær og tertiær '
  'socialisation samt Mead og Erikson. Skrevet til gymnasiet.',
  'https://samfundsfag.dk/begreber/sociologi/identitet-familie-socialisation'
  '/socialisation/'),
 ('Socialisering og ulighed', 'Levende Grønland', 'Asger Lind Krebs. Primær '
  'og sekundær socialisering med sommerfuglemodellen.',
  'https://www.levendegronland.dk/da/samfundsfag/socialisering-og-ulighed/'),
 ('Tallene om unges medievaner', 'Vores eget dataark', 'Danmarks Statistik, '
  'WHO/HBSC, PISA og Eurostat — hver kilde åbnet og læst.',
  'digital-socialisering.html'),
]


def e(t):
    """Teksterne har <b> i sig med vilje, saa de maa ikke escapes helt."""
    return t


afsnit_html = ''
for i, (o, stykker, figur, figtekst) in enumerate(AFSNIT, 1):
    afsnit_html += (f'<section class="afsnit"><h2><span class="num">{i}</span>'
                    f'{html.escape(o)}</h2>')
    afsnit_html += ''.join(f'<p>{e(t)}</p>' for t in stykker)
    if figur:
        afsnit_html += (f'<div class="figur">{figur}'
                        f'<div class="figtekst">{html.escape(figtekst)}</div>'
                        f'</div>')
    afsnit_html += '</section>'

analyse_html = ''.join(
    f'<tr><th>{html.escape(q)}</th><td>{html.escape(a)}</td></tr>'
    for q, a in ANALYSE)
ord_html = ''.join(
    f'<tr><th>{html.escape(o)}</th><td>{html.escape(t)}</td></tr>'
    for o, t in ORD)
kilder_html = ''.join(
    f'<tr><td><a href="{u}"' +
    ('' if not u.startswith('http') else ' target="_blank" rel="noopener"') +
    f'>{html.escape(t)}</a></td><td>{html.escape(hvor)}</td>'
    f'<td>{html.escape(om)}</td></tr>'
    for t, hvor, om, u in KILDER)

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
table.liste th{background:var(--panel2);width:30%}
table.liste thead th{width:auto}
table.kilder td{border:1px solid var(--line);padding:9px 11px;
font-size:.9rem;vertical-align:top}
table.kilder{width:100%;border-collapse:collapse;margin:12px 0}
.printbtn{background:#fff;border:1px solid var(--line);border-radius:10px;
padding:10px 18px;font-weight:700;font-size:.95rem;cursor:pointer;
color:var(--ink);font-family:inherit;margin:6px 8px 0 0}
.printbtn:hover{border-color:var(--accent);color:var(--accent)}
h2.sec{font-size:1.4rem;margin:30px 0 6px}
@media print{header.top,.printbtn,.btnlink{display:none!important}
.afsnit,.figur{box-shadow:none;break-inside:avoid;page-break-inside:avoid}
body{font-size:11pt}main{padding:0}@page{size:A4;margin:14mm}}
'''

KROP = f'''<section class="hero">
<span class="pill">Samfundsfag · Digital socialisering</span>
<h1>Hvad er socialisering?</h1>
<p>Normer, arenaer og sanktioner — og hvorfor et feed ikke gør det samme ved
alle. Teksten hører til forløbet i uge 40–43 og giver de ord, I skal bruge,
når I læser jeres egne svar.</p>
<button class="printbtn" onclick="window.print()">Print siden</button>
<a class="btnlink ghost" href="samfundsfag-tekster.html">Tilbage til teksterne</a>
<a class="btnlink ghost" href="kvalitativ-analyse.html">Den kvalitative analyse</a>
</section>
{afsnit_html}
<h2 class="sec">Sådan bruger du det på jeres egne svar</h2>
<p style="color:var(--muted);max-width:74ch">I uge 43 læser I svarene fra
Hamborg igennem. Begreberne herover er ikke noget, I skal kunne remse op — de
er fem ting at kigge efter. Stil spørgsmålet til venstre til hvert svar.</p>
<table class="liste"><thead><tr><th>Spørg om svaret</th>
<th>Så leder du efter</th></tr></thead><tbody>{analyse_html}</tbody></table>
<h2 class="sec">Ord du skal kunne</h2>
<table class="liste"><thead><tr><th>Ord</th><th>Betyder</th></tr></thead>
<tbody>{ord_html}</tbody></table>
<h2 class="sec">Hvor det kommer fra</h2>
<p style="color:var(--muted);max-width:74ch">Teksten er skrevet til jer, men
begreberne er ikke opfundet her. Vil du læse videre, er det de her, der er
frit tilgængelige.</p>
<table class="kilder"><tbody>{kilder_html}</tbody></table>
<button class="printbtn" onclick="window.print()">Print siden</button>'''

DOK = ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
       '<meta name="viewport" content="width=device-width,initial-scale=1">'
       '<title>Hvad er socialisering? · 9. klasse</title><style>' + CSS +
       '</style></head><body><header class="top"><div class="top-inner">'
       '<a class="brand" href="index.html">Mibelibsen <span>9. klasse</span></a>'
       '<nav class="tabs"><a class="" href="matematik.html">Matematik</a>'
       '<a class="active" href="samfundsfag.html">Samfundsfag</a>'
       '<a class="" href="tysk.html">Tysk</a><a class="" href="fysik.html">Fysik</a>'
       '</nav></div></header><main>' + KROP + '</main><footer>'
       'Undervisningsmateriale · 9. klasse · Mibelibsen.</footer></body></html>')

open(UD, 'w', encoding='utf-8').write(DOK)
print(f'skrevet:  {UD}')
print(f'{len(AFSNIT)} afsnit · {sum(1 for a in AFSNIT if a[2])} figurer · '
      f'{len(ORD)} ord i ordlisten · {len(KILDER)} kilder')
