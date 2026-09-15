# -*- coding: utf-8 -*-
"""Bygger lovprocessen.html — vores egen tekst om lovgivningsprocessen.

Erstatter PDF'en. Siden er selvbaerende, har et procesdiagram tegnet af
claude/figurer.py og kan printes.
"""
import sys, os, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figurer as FG

UD = 'lovprocessen.html'
MIN, FT, EFTER = 'min', 'ft', 'efter'
FARVER = {MIN: FG.GRO, FT: FG.BLA, EFTER: FG.ORA}

# (overskrift, kort undertekst til diagrammet, gruppe, uddybning)
TRIN = [
 ('Idé og lovforberedelse', 'Ministeriet skriver et udkast til lovforslag', MIN,
  'Idéen kan komme fra regeringen, fra en aftale mellem partier, fra EU-regler '
  'eller fra pres udefra — organisationer, medier og borgere. Embedsmændene i '
  'ministeriet skriver selve lovteksten og bemærkningerne, der forklarer, hvad '
  'loven skal, og hvad den kommer til at koste.'),
 ('Høring', 'Organisationer, kommuner og eksperter afgiver høringssvar', MIN,
  'Udkastet sendes ud til dem, loven kommer til at ramme: fagforeninger, '
  'kommuner, brancheforeninger, forskere og interesseorganisationer. De skriver '
  'høringssvar, hvor de roser, kritiserer eller foreslår ændringer. Svarene er '
  'offentlige — det er her, du kan se, hvem der prøver at påvirke loven.'),
 ('Høringsnotat', 'Ministeren samler svarene og retter forslaget til', MIN,
  'Ministeriet skriver et notat med hvert kritikpunkt og et svar på hvert af '
  'dem: rettes forslaget, eller fastholdes det? Mange forslag bliver lavet om '
  'her, før de overhovedet når til Folketinget.'),
 ('Fremsættelse i Folketinget', 'Forslaget får et L-nummer og bliver offentligt',
  FT,
  'Ministeren fremsætter forslaget i Folketingssalen. Fra det øjeblik har det '
  'et nummer — for eksempel L 42 — og alt om det kan følges på ft.dk: teksten, '
  'bemærkningerne, spørgsmålene og senere afstemningen.'),
 ('1. behandling', 'Debat om forslagets hovedidé — derefter i udvalg', FT,
  'Her diskuteres idéen, ikke detaljerne: er det overhovedet en god lov? Der '
  'stemmes ikke om indholdet ved 1. behandling. Til sidst sendes forslaget '
  'videre til det udvalg, der har emnet.'),
 ('Udvalgsbehandling', 'Spørgsmål til ministeren, ændringsforslag og betænkning',
  FT,
  'Det er her det meste arbejde sker. Udvalget stiller skriftlige spørgsmål til '
  'ministeren, kan holde høringer og kalde eksperter ind, og partierne stiller '
  'ændringsforslag. Til sidst skriver udvalget en betænkning: hvad mener hvert '
  'parti, og hvordan vil de stemme?'),
 ('2. behandling', 'Debat om detaljerne og afstemning om ændringsforslag', FT,
  'Nu handler det om paragrafferne. Der stemmes om ændringsforslagene ét for '
  'ét. Bliver forslaget ændret meget, kan det sendes tilbage i udvalg igen.'),
 ('3. behandling', 'Sidste debat og endelig afstemning om hele forslaget', FT,
  'Den sidste runde. Der stemmes om forslaget som helhed, og et flertal af de '
  'afgivne stemmer afgør det. Falder forslaget her, er det slut.'),
 ('Kongelig stadfæstelse', 'Loven kundgøres i Lovtidende og træder i kraft',
  EFTER,
  'Monarken og en minister skriver under — det hedder stadfæstelse. Derefter '
  'kundgøres loven i Lovtidende, og den træder i kraft på den dato, der står i '
  'loven selv. Først dér gælder den for os alle sammen.'),
]

ORD = [
 ('Høringssvar', 'Det, en organisation eller kommune svarer, når den har læst '
  'udkastet. Offentligt — alle kan læse det.'),
 ('L-nummer', 'Lovforslagets nummer i Folketinget, fx L 42. Nummeret gør det '
  'muligt at følge præcis det ene forslag.'),
 ('Ændringsforslag', 'Et forslag om at rette i lovforslaget undervejs. Der '
  'stemmes om dem ved 2. behandling.'),
 ('Betænkning', 'Udvalgets skriftlige indstilling. Her står, hvad hvert parti '
  'mener, og hvad de vil stemme.'),
 ('Stadfæstelse', 'Underskriften fra monarken og en minister, efter at '
  'Folketinget har vedtaget loven.'),
 ('Lovtidende', 'Det officielle sted, hvor love bliver kundgjort. En lov, der '
  'ikke er kundgjort, gælder ikke.'),
]

diagram = FG.procesdiagram(
    [(o, u, g) for o, u, g, _ in TRIN], W=640, farver=FARVER,
    legende=[('Ministeriet', MIN), ('Folketinget', FT), ('Efter vedtagelsen', EFTER)])

trin_html = ''.join(
    f'<section class="trin {g}"><h2><span class="num">{i}</span>{html.escape(o)}</h2>'
    f'<p class="kort">{html.escape(u)}</p><p>{html.escape(tekst)}</p></section>'
    for i, (o, u, g, tekst) in enumerate(TRIN, 1))

BASIS = open('samfundsfag.html').read()
CSS = BASIS[BASIS.find('<style>') + 7:BASIS.find('</style>')]
CSS += '''
.figur{background:var(--panel2);border:1px solid var(--line);border-radius:14px;
padding:18px;margin:18px 0;text-align:center}
.figur svg{max-width:100%;height:auto}
.trin{background:var(--panel);border:1px solid var(--line);border-left:5px solid var(--accent);
border-radius:14px;padding:18px 22px;margin:14px 0;box-shadow:var(--shadow)}
.trin.min{border-left-color:var(--good)}
.trin.efter{border-left-color:var(--warn)}
.trin h2{font-size:1.2rem;margin:0 0 6px;display:flex;align-items:center;gap:12px}
.trin .num{width:30px;height:30px;border-radius:9px;display:grid;place-items:center;
font-weight:800;font-size:.95rem;background:var(--accent);color:#fff;flex:0 0 auto}
.trin.min .num{background:var(--good)}
.trin.efter .num{background:var(--warn)}
.trin p{margin:6px 0;color:var(--muted);font-size:.97rem;max-width:74ch}
.trin p.kort{color:var(--ink);font-weight:600;font-size:.95rem}
.ordliste{width:100%;border-collapse:collapse;margin:12px 0;font-size:.95rem}
.ordliste th,.ordliste td{border:1px solid var(--line);padding:10px 12px;
text-align:left;vertical-align:top}
.ordliste th{background:var(--panel2);white-space:nowrap}
.printbtn{background:#fff;border:1px solid var(--line);border-radius:10px;
padding:10px 18px;font-weight:700;font-size:.95rem;cursor:pointer;color:var(--ink);
font-family:inherit;margin:6px 8px 0 0}
.printbtn:hover{border-color:var(--accent);color:var(--accent)}
h2.sec{font-size:1.4rem;margin:30px 0 6px}
@media print{header.top,.printbtn,.btnlink{display:none!important}
.trin,.figur{box-shadow:none;break-inside:avoid;page-break-inside:avoid}
body{font-size:11pt}main{padding:0}@page{size:A4;margin:14mm}}
'''

KROP = f'''<section class="hero"><span class="pill">Samfundsfag · Politiske processer</span>
<h1>Den demokratiske beslutningsproces i Danmark</h1>
<p>Fra idé til gældende lov — med høring og tre behandlinger. Ni trin, og hvert
trin er et sted, hvor loven kan blive ændret eller stoppet.</p>
<button class="printbtn" onclick="window.print()">Print siden</button>
<a class="btnlink ghost" href="samfundsfag-tekster.html">Tilbage til teksterne</a>
</section>
<div class="figur">{diagram}</div>
<h2 class="sec">Trin for trin</h2>
{trin_html}
<h2 class="sec">To paragraffer i grundloven</h2>
<div class="box note" style="background:#fff7e9;border:1px solid var(--line);
border-left:4px solid var(--warn);border-radius:12px;padding:16px 20px;margin:14px 0">
<p style="margin:0 0 8px"><b>§ 41:</b> et lovforslag skal behandles <b>tre gange</b>
i Folketinget, før det kan vedtages endeligt. At der skal gå mindst to dage
mellem behandlingerne, står i Folketingets forretningsorden.</p>
<p style="margin:0"><b>§ 42:</b> en <b>tredjedel</b> af Folketingets medlemmer kan
kræve, at en vedtaget lov sendes til folkeafstemning. Nogle love er undtaget —
blandt andet finanslove og skattelove.</p></div>
<h2 class="sec">Ord du skal kunne</h2>
<table class="ordliste"><thead><tr><th>Ord</th><th>Betyder</th></tr></thead><tbody>
{''.join(f'<tr><th>{html.escape(o)}</th><td>{html.escape(t)}</td></tr>' for o, t in ORD)}
</tbody></table>
<button class="printbtn" onclick="window.print()">Print siden</button>'''

DOK = ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
       '<meta name="viewport" content="width=device-width,initial-scale=1">'
       '<title>Lovprocessen i Danmark · 9. klasse</title><style>' + CSS +
       '</style></head><body><header class="top"><div class="top-inner">'
       '<a class="brand" href="index.html">Mibelibsen <span>9. klasse</span></a>'
       '<nav class="tabs"><a class="" href="matematik.html">Matematik</a>'
       '<a class="active" href="samfundsfag.html">Samfundsfag</a>'
       '<a class="" href="tysk.html">Tysk</a><span class="soon">Fysik</span>'
       '</nav></div></header><main>' + KROP + '</main><footer>'
       'Undervisningsmateriale · 9. klasse · Mibelibsen.</footer></body></html>')
open(UD, 'w').write(DOK)
print(f'skrevet:  {UD}  ·  {len(TRIN)} trin, {len(ORD)} ord i ordlisten')
