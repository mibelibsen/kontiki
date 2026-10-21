# -*- coding: utf-8 -*-
"""Bygger GeoGebra-vejledningen til opgave C og D i lineaere funktioner.

Siden ligger i roden og udgives, men **ingen side linker til den**. Den kan
kun naas, hvis man kender adressen. Saadan skal det vaere, indtil den er
proevet af - saa kobles den paa matematik.html og funktioner-og-ligninger.html.
Ulistet er ikke privat: har man adressen, kan man laese den.

**Der staar ingen facit paa siden.** Alle eksempler bruger tal, der ikke
findes i opgave C eller D, saa ungerne kan foelge fremgangsmaaden uden at
faa svaret foraeret. Tallene i eksemplet er valgt, saa hver kommando giver et
paent resultat.

Kommandonavnene er proevet af i GeoGebra Classic paa dansk, ikke husket:
Linje, Haeldning, Rod og Skaering er dem, programmet selv skriver i
algebravinduet. "Nulpunkt" findes ikke - den hedder Rod.

    python3 claude/byg_geogebra.py
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figurer as FG

# Siden ligger i roden og bliver udgivet - men der linkes ikke til den fra
# nogen anden side. Den kan kun findes, hvis man kender adressen:
#     mibelibsen.space/geogebra-lineaere-funktioner.html
# Det er med vilje: den skal kunne aabnes i en browser og proeves af, foer
# den kobles paa matematiksiden. Bemaerk, at ulistet ikke er det samme som
# privat - enhver med adressen kan laese den.
UD = 'geogebra-lineaere-funktioner.html'
GEOGEBRA = 'https://www.geogebra.org/classic?lang=da'

# Eksempeltallene. De maa IKKE vaere opgavernes egne - se docstringen.
# y = 2x + 1 gennem (1, 3) og (4, 9); den anden linje y = -x + 9 skaerer
# den i (8/3, ...) - derfor er den valgt som y = 6 - x, som skaerer i (5/3, ...).
# Vi bruger i stedet y = 2x + 1 og y = x + 4: de skaerer i (3, 7). Pænt.
EKS_A, EKS_B = 2, 1                       # y = 2x + 1
P1, P2 = (1, 3), (4, 9)                   # to punkter paa den
EKS2_A, EKS2_B = 1, 4                     # y = x + 4
SKAER = (3, 7)                            # skaeringspunktet
assert EKS_A * P1[0] + EKS_B == P1[1] and EKS_A * P2[0] + EKS_B == P2[1]
assert EKS_A * SKAER[0] + EKS_B == SKAER[1] == EKS2_A * SKAER[0] + EKS2_B

FIG_LINJE = FG.koordinatsystem(
    linjer=[(EKS_A, EKS_B, FG.BLA, 'f')],
    punkter=[(P1[0], P1[1], FG.ROD, 'A'), (P2[0], P2[1], FG.ROD, 'B')],
    xmin=-1, xmax=6, ymin=-1, ymax=11,
    trappe=(EKS_A, EKS_B, P1[0], P2[0] - P1[0]))

FIG_SKAER = FG.koordinatsystem(
    linjer=[(EKS_A, EKS_B, FG.BLA, 'f'), (EKS2_A, EKS2_B, FG.GRO, 'g')],
    punkter=[(SKAER[0], SKAER[1], FG.ROD, 'S')],
    xmin=-1, xmax=6, ymin=-1, ymax=11)

# (overskrift, [afsnit], [(hvad du skriver, hvad der sker)], figur, figurtekst)
TRIN = [
 ('Åbn GeoGebra',
  ['Gå ind på <b>geogebra.org/classic</b> og vælg <b>Graf</b>. Du skal ikke '
   'logge ind, og du skal ikke hente noget.',
   'Til venstre er <b>algebravinduet</b> med feltet, der hedder '
   '<i>Input…</i> — det er dér, du skriver. Til højre er '
   '<b>grafikvinduet</b>, hvor tingene bliver tegnet.',
   'Alt, hvad du skriver i Input-feltet, afsluttes med <b>Enter</b>.'],
  [], None, None),

 ('Sæt de to punkter ind',
  ['Har du to målinger — to kvitteringer, to aflæsninger — så er de to '
   'punkter. Skriv dem ét ad gangen.',
   'Pas på kommaet: koordinater skrives <code class="inl">(1,3)</code>. '
   'Decimaltal skrives med <b>punktum</b> i GeoGebra, så 2,5 skrives '
   '<code class="inl">2.5</code>.'],
  [('A=(1,3)', 'Punktet A dukker op i grafikvinduet'),
   ('B=(4,9)', 'Punktet B kommer også')],
  None, None),

 ('Tegn linjen gennem dem',
  ['Nu trækker du linjen gennem de to punkter. Den får automatisk navnet '
   '<code class="inl">f</code>.',
   '<b>Her kommer en overraskelse.</b> GeoGebra skriver ikke linjen som '
   '<code class="inl">y = ax + b</code>. Den skriver noget i retning af '
   '<code class="inl">−2x + y = 1</code>. Det er den <i>samme</i> linje — '
   'flyt leddet over på den anden side, så står der '
   '<code class="inl">y = 2x + 1</code>. Bliv ikke forvirret af det.'],
  [('Linje(A,B)', 'Linjen tegnes, og dens ligning står i algebravinduet')],
  None, None),

 ('Få hældningen a',
  ['Det her er den vigtigste kommando på siden. Den giver dig ikke bare '
   'tallet — den <b>tegner trappetrinnet</b> ude på linjen, så du kan se, '
   'hvor tallet kommer fra.',
   'Det er præcis det trappetrin, opgaven beder dig om at aflæse. '
   'GeoGebra tegner ét trin til højre; i opgaven går du fem til højre og '
   'deler med fem bagefter — det er det samme.'],
  [('Hældning(f)', 'Tallet a kommer frem, og trappetrinnet tegnes på linjen')],
  FIG_LINJE,
  'Sådan ser det ud. Trappetrinnet viser, hvor meget linjen stiger, når du '
  'går til højre. Her er der gået 3 til højre og 6 op.'),

 ('Aflæs b, og skriv din egen forskrift',
  ['<code class="inl">b</code> er dér, hvor linjen skærer <b>y-aksen</b>. '
   'Det kan du aflæse direkte i grafikvinduet — kig på, hvor linjen krydser '
   'den lodrette akse.',
   'Nu har du både <code class="inl">a</code> og <code class="inl">b</code>. '
   '<b>Skriv selv forskriften</b>, og giv den et nyt navn, fx '
   '<code class="inl">g</code>. Skriv <code class="inl">g(x)=</code> foran — '
   'så bliver det en funktion, og så virker de næste kommandoer.',
   '<b>Sådan tjekker du dig selv:</b> hvis din forskrift er rigtig, lægger '
   '<code class="inl">g</code> sig præcis oven på <code class="inl">f</code>, '
   'og du kan ikke se to linjer. Kan du det, er der en fejl i a eller b.'],
  [('g(x)=2x+1', 'Din egen forskrift tegnes — den skal dække linjen f')],
  None, None),

 ('Regn en værdi ud',
  ['Skal du vide, hvad noget koster ved et bestemt x — 7 timer, 12 GB — så '
   'skriver du bare tallet i parentesen.',
   'Det svarer til at sætte tallet ind i forskriften i hånden. Gør gerne '
   'begge dele: GeoGebra er god til at fange regnefejl.'],
  [('g(7)', 'Svaret står med det samme i algebravinduet')],
  None, None),

 ('Find nulpunktet',
  ['Nulpunktet er dér, hvor grafen rammer <b>x-aksen</b> — hvor y er nul. '
   'Det er fx dér, hvor telefonen er løbet tør for strøm.',
   'Kommandoen hedder <b>Rod</b>. Ikke "Nulpunkt" — det findes ikke i '
   'GeoGebra, selv om det er det, vi kalder det i timen.',
   '<b>Den virker kun på en funktion.</b> Har du kun linjen '
   '<code class="inl">f</code> fra Linje-kommandoen, får du ingenting. '
   'Brug din egen <code class="inl">g</code> fra trin 5.'],
  [('Rod(g)', 'Punktet, hvor grafen krydser x-aksen')],
  None, None),

 ('To linjer og skæringspunktet',
  ['I opgave D er der to abonnementer. Skriv begge forskrifter som '
   'funktioner, og find så punktet, hvor de krydser hinanden.',
   'Skæringspunktet er det sted, hvor de to koster <b>det samme</b>. Til '
   'venstre for punktet er den ene billigst, til højre den anden. Det er '
   'hele pointen i opgaven.'],
  [('g(x)=2x+1', 'Den første linje'),
   ('h(x)=x+4', 'Den anden linje'),
   ('Skæring(g,h)', 'Punktet, hvor de krydser, med begge koordinater')],
  FIG_SKAER,
  'Skæringspunktet S er dér, hvor de to linjer møder hinanden. '
  'Koordinaterne fortæller både ved hvilket x og til hvilken pris.'),

 ('Få billedet ind i Word',
  ['Opgaven siger, at udregningerne skal laves i Word, og at du skal vise '
   'din metode. Billedet fra GeoGebra <b>er</b> en del af metoden.',
   'Klik på <b>menuen</b> øverst til højre (de tre streger) → <b>Fil</b> → '
   '<b>Eksporter billede</b>. Så kan du hente billedet og sætte det ind i '
   'Word.',
   '<b>Skriv altid under billedet, hvad x og y står for.</b> Et '
   'koordinatsystem uden enheder siger ingenting — er det timer og kroner, '
   'eller GB og kroner?'],
  [], None, None),
]

OPGAVER = [
 ('Opgave C · kajakudlejningen og batteriet',
  ['De to kvitteringer er dine to punkter. Sæt dem ind (trin 2), tegn '
   'linjen (trin 3) og find hældningen (trin 4).',
   'Aflæs b på y-aksen, skriv forskriften, og tjek at den dækker linjen '
   '(trin 5).',
   'Hvad 7 timer koster, finder du med trin 6.',
   'I batteridelen skal du finde nulpunktet — det er trin 7. Læg mærke '
   'til, at a bliver <b>negativ</b> her. Trappetrinnet peger nedad.']),
 ('Opgave D · de to abonnementer',
  ['Her er linjerne tegnet i forvejen. Du skal aflæse a og b og vise ved '
   'regning, at det passer.',
   'Skriv de to forskrifter, du har aflæst, ind som funktioner (trin 8). '
   'Lægger de sig oven i de to tegnede linjer, har du aflæst rigtigt.',
   'Find skæringspunktet med trin 8. Sammenlign med det, du aflæste på '
   'figuren — og med det, du får ved at sætte de to forskrifter lig '
   'hinanden i hånden.',
   'Prisen ved 12 GB hos hver af dem er to gange trin 6.']),
]

FALDER = [
 ('Komma og punktum', 'Koordinater skilles med komma: '
  '<code class="inl">(2,200)</code>. Decimaltal skrives med punktum: '
  '<code class="inl">2.5</code>.'),
 ('Linjen er ikke en funktion', '<code class="inl">Linje(A,B)</code> laver en '
  'linje, ikke en funktion. <code class="inl">Rod</code> og '
  '<code class="inl">g(7)</code> virker kun på noget, du har skrevet som '
  '<code class="inl">g(x)=</code>.'),
 ('Ligningen ser forkert ud', 'GeoGebra skriver gerne '
  '<code class="inl">−2x + y = 1</code> i stedet for '
  '<code class="inl">y = 2x + 1</code>. Det er den samme linje.'),
 ('Du kan ikke se noget', 'Punkterne i opgaverne har store y-værdier — 200, '
  '350. Rul ud med musehjulet, eller brug forstørrelsesglasset nede til '
  'højre, indtil punkterne er inde i billedet.'),
 ('Det hedder Rod', 'Ikke Nulpunkt. Begynd at skrive <b>Rod</b>, så '
  'foreslår GeoGebra resten selv.'),
]

trin_html = ''
for i, (o, stykker, skriv, figur, figtekst) in enumerate(TRIN, 1):
    trin_html += (f'<section class="trin"><h2><span class="num">{i}</span>'
                  f'{html.escape(o)}</h2>')
    trin_html += ''.join(f'<p>{t}</p>' for t in stykker)
    if skriv:
        trin_html += '<table class="skriv"><tbody>' + ''.join(
            f'<tr><td class="kmd"><code>{html.escape(k)}</code></td>'
            f'<td class="sker">{html.escape(v)}</td></tr>' for k, v in skriv
        ) + '</tbody></table>'
    if figur:
        trin_html += (f'<div class="figur">{figur}'
                      f'<div class="figtekst">{html.escape(figtekst)}</div></div>')
    trin_html += '</section>'

opg_html = ''.join(
    f'<div class="opg"><h3>{html.escape(o)}</h3>'
    + ''.join(f'<p>{t}</p>' for t in stykker) + '</div>' for o, stykker in OPGAVER)
falder_html = ''.join(
    f'<tr><th>{html.escape(a)}</th><td>{b}</td></tr>' for a, b in FALDER)

BASIS = open('funktioner-og-ligninger.html', encoding='utf-8').read()
CSS = BASIS[BASIS.find('<style>') + 7:BASIS.find('</style>')]
CSS += '''
.trin{background:var(--panel,#fff);border:1px solid var(--line);
border-left:5px solid var(--accent);border-radius:14px;padding:18px 22px;
margin:16px 0}
.trin h2{font-size:1.18rem;margin:0 0 10px;display:flex;align-items:center;
gap:12px}
.trin .num{width:30px;height:30px;border-radius:9px;display:grid;
place-items:center;font-weight:800;font-size:.95rem;background:var(--accent);
color:#fff;flex:0 0 auto}
.trin p{margin:8px 0;color:var(--muted);font-size:.97rem;max-width:72ch}
.trin p b{color:var(--ink)}
table.skriv{width:100%;border-collapse:collapse;margin:14px 0}
table.skriv td{border:1px solid var(--line);padding:9px 12px;
vertical-align:middle}
table.skriv td.kmd{width:40%;background:#1a2233;border-color:#1a2233}
table.skriv td.kmd code{color:#eaf0ff;font-size:1.02rem;font-weight:700}
table.skriv td.sker{color:var(--muted);font-size:.93rem}
.opg{background:var(--panel2);border:1px solid var(--line);border-radius:12px;
padding:14px 20px;margin:14px 0}
.opg h3{margin:0 0 6px;font-size:1.05rem}
.opg p{margin:6px 0;color:var(--muted);font-size:.95rem;max-width:72ch}
table.falder{width:100%;border-collapse:collapse;margin:12px 0;font-size:.95rem}
table.falder th,table.falder td{border:1px solid var(--line);padding:10px 12px;
text-align:left;vertical-align:top}
table.falder th{background:var(--panel2);width:30%}
.figtekst{color:var(--muted);font-size:.9rem;margin-top:10px;text-align:left;
max-width:66ch;margin-left:auto;margin-right:auto}
h2.sec{font-size:1.4rem;margin:30px 0 6px}
@media print{header.top,.printbtn,.btn{display:none!important}
.trin,.figur,.opg{break-inside:avoid;page-break-inside:avoid}
body{font-size:11pt}main{padding:0}@page{size:A4;margin:14mm}}
'''

KROP = f'''<section class="hero">
<span class="pill">Matematik · lineære funktioner</span>
<h1>GeoGebra på ti minutter</h1>
<p>Ni trin, der dækker præcis det, du skal bruge i <b>opgave C og D</b>.
Alle eksempler bruger andre tal end opgaverne — fremgangsmåden er den samme,
men svarene skal du selv finde.</p>
<button class="printbtn" onclick="window.print()">Print vejledningen</button>
<a class="btn" href="{GEOGEBRA}" target="_blank" rel="noopener">Åbn GeoGebra</a>
</section>
<div id="trin">{trin_html}</div>
<h2 class="sec" id="opgaver">Sådan bruger du trinnene i opgaverne</h2>
{opg_html}
<h2 class="sec" id="falder">Fem ting, der driller</h2>
<table class="falder"><tbody>{falder_html}</tbody></table>
<button class="printbtn" onclick="window.print()">Print vejledningen</button>'''

DOK = ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
       '<meta name="viewport" content="width=device-width,initial-scale=1">'
       '<title>GeoGebra til lineære funktioner · 9. klasse</title><style>'
       # Headeren er den samme som paa funktioner-og-ligninger.html, fordi
       # CSS'en kommer derfra: den har .top-inner og .jump, men ingen .tabs.
       + CSS + '</style></head><body><header class="top"><div class="top-inner">'
       '<div class="brand">Matematik · <span>GeoGebra til opgave C og D</span>'
       '</div><nav class="jump">'
       '<a href="#trin">Trinnene</a><a href="#opgaver">I opgaverne</a>'
       '<a href="#falder">Det der driller</a>'
       '</nav></div></header><main>' + KROP + '</main><footer>'
       'Undervisningsmateriale · 9. klasse · Mibelibsen.</footer></body></html>')

open(UD, 'w', encoding='utf-8').write(DOK)
print(f'skrevet:  {UD}  ·  {len(TRIN)} trin, '
      f'{sum(1 for t in TRIN if t[3])} figurer, {len(FALDER)} faldgruber')
print('UDGIVET, men ULINKET: ingen side peger på den. Adressen er')
print(f'  mibelibsen.space/{UD}')
