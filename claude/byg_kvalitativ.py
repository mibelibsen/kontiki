# -*- coding: utf-8 -*-
"""Bygger kvalitativ-analyse.html — oplaeg til ungerne i uge 43.

Spoergeskemaerne fra Hamborg kunne ikke taelles: de to sprogversioner maalte
ikke det samme. Svarene bruges derfor kvalitativt, og siden er oplaegget til,
hvordan man goer det ordentligt — med en metode, et gennemfoert eksempel og
de faelder, der goer en kvalitativ analyse vaerdiloes.

Eksempelsvarene er opdigtede og maerket som det. Ungernes egne svar maa ikke
ligge paa sitet.
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figurer as FG

UD = 'kvalitativ-analyse.html'
UGE = 'Uge 43'

# ---------------------------------------------------------------------------
# Metoden
# ---------------------------------------------------------------------------
LAES, KOD, SAML = 'laes', 'kod', 'saml'
FARVER = {LAES: FG.GRO, KOD: FG.BLA, SAML: FG.ORA}

TRIN = [
 ('Læs det hele igennem', 'Uden at skrive noget', LAES,
  'Læs alle svarene én gang fra ende til anden, før du skriver et eneste ord. '
  'Det lyder som spild af tid, men det er det ikke: begynder du at kode fra '
  'svar nummer et, kommer de første svar til at bestemme, hvad du overhovedet '
  'får øje på i resten.'),
 ('Sæt et ord på hvert svar', 'Det kaldes at kode', KOD,
  'Skriv ét eller to ord i margenen ud for hvert svar — et ord, der fanger, '
  'hvad svaret handler om. Ikke hvad du synes om det. "Kedsomhed", "pres fra '
  'venner", "forældre skælder ud". Det ord er en <b>kode</b>.'),
 ('Saml koderne i kategorier', 'Hvilke koder ligner hinanden?', KOD,
  'Læg koderne i bunker. "Pres fra venner", "bange for at gå glip af noget" og '
  '"alle de andre er der" hører sammen — de kan blive til kategorien '
  '<b>socialt pres</b>. En kategori er en bunke koder, der handler om det samme.'),
 ('Find mønstre — og modsigelser', 'Hvad siger mange? Hvem siger det modsatte?', SAML,
  'Nu kan du se, hvad der går igen. Men kig lige så grundigt efter det, der '
  '<b>ikke</b> passer ind. Ét svar, der siger det modsatte af alle de andre, er '
  'ikke en fejl, der skal væk — det er tit det mest interessante i hele bunken.'),
 ('Vælg citater, der viser kategorien', 'Et citat beviser ikke noget — det viser noget', SAML,
  'Find to-tre svar, der formulerer kategorien tydeligst, og citér dem ordret. '
  'Skriv aldrig et citat om, så det passer bedre. Og husk: citatet er et '
  '<b>eksempel</b> på kategorien, ikke et bevis på, hvor mange der mener det.'),
]

# ---------------------------------------------------------------------------
# Det gennemfoerte eksempel. Svarene er opdigtede.
# ---------------------------------------------------------------------------
EKSEMPEL = [
 ('"Ich schaue abends noch schnell, ob jemand geschrieben hat. Dann ist es '
  'plötzlich halb zwei."',
  'mister tiden om aftenen', 'Søvn og tid'),
 ('"Wenn ich nicht antworte, denken sie, ich bin sauer."',
  'skal svare hurtigt', 'Socialt pres'),
 ('"Meine Mutter nimmt das Handy um neun. Finde ich eigentlich okay."',
  'regler hjemmefra — accepteres', 'Voksne og regler'),
 ('"Ohne Handy wüsste ich gar nicht, wann wir uns treffen."',
  'mobilen holder styr på aftaler', 'Mobilen som værktøj'),
 ('"Ich lösche die App manchmal für eine Woche. Dann lade ich sie wieder runter."',
  'prøver selv at holde pause', 'Egen kontrol'),
]
KATEGORIER = sorted({k for _, _, k in EKSEMPEL})
assert len(KATEGORIER) == 5, KATEGORIER

# ---------------------------------------------------------------------------
# Faelderne
# ---------------------------------------------------------------------------
FAELDER = [
 ('Du plukker det citat, der passer til din pointe',
  'Det hedder at <b>cherry-picke</b>. Hvis du allerede ved, hvad du vil skrive, '
  'kan du altid finde ét svar, der bakker dig op. Modgiften: skriv dine '
  'kategorier færdige, <i>før</i> du vælger citater — og tag altid det svar med, '
  'der passer dårligst.'),
 ('Du skriver "de tyske unge mener…"',
  'I har spurgt nogle få unge på én skole i én by. De er ikke Tyskland. Skriv '
  '"de unge, vi talte med" eller "flere af svarene peger på". Det er ikke '
  'forsigtighed for en sikkerheds skyld — det er det eneste, jeres data kan bære.'),
 ('Du tæller alligevel',
  '"Tre ud af fem sagde…" lyder stærkt, men fem svar kan ikke bære en procent. '
  'Kvalitativ analyse svarer på <b>hvad</b> og <b>hvorfor</b>, ikke på hvor mange. '
  'Vil I vide hvor mange, skal I bruge de store undersøgelser i dataarket.'),
 ('Oversættelsen flytter betydningen',
  'Det var præcis dét, der gjorde tallene ubrugelige. Når I citerer, så skriv '
  'den tyske sætning <b>og</b> jeres oversættelse. Så kan læseren selv se, om '
  'I har ramt rigtigt — og I opdager selv de steder, hvor to ord ikke dækker '
  'hinanden.'),
]

ORD = [
 ('Kvalitativ', 'Undersøger hvad noget betyder, og hvorfor. Få svar, læst grundigt.'),
 ('Kvantitativ', 'Undersøger hvor mange og hvor meget. Mange svar, talt op.'),
 ('Kodning', 'At sætte et ord på, hvad et svar handler om.'),
 ('Kategori', 'En bunke koder, der handler om det samme.'),
 ('Mønster', 'Noget, der går igen på tværs af flere svar.'),
 ('Citat', 'Et svar gengivet ordret. Viser en kategori — beviser ikke en udbredelse.'),
 ('Repræsentativ', 'Når de, man har spurgt, ligner dem, man udtaler sig om. '
  'Jeres svar er ikke repræsentative, og det skal stå i opgaven.'),
 ('Bias', 'Skævhed. Her især: at man finder det, man på forhånd ledte efter.'),
]


# ---------------------------------------------------------------------------
# Figurer
# ---------------------------------------------------------------------------
diagram = FG.procesdiagram(
    [(o, u, g) for o, u, g, _ in TRIN], W=640, farver=FARVER,
    legende=[('Læs', LAES), ('Kod og saml', KOD), ('Konkludér', SAML)])

# de to tilgange sat op mod hinanden - en almindelig tabel, ikke en figur:
# regneark() tegner et Excel-ark og ville love noget andet, end der staar
SAMMENLIGN = [
 ('Spørger om', 'Hvor mange?', 'Hvad og hvorfor?'),
 ('Svarer på', 'Udbredelse', 'Betydning'),
 ('Antal svar', 'Mange — tusinder', 'Få — læst grundigt'),
 ('Resultatet er', 'Et tal med en usikkerhed', 'Kategorier med citater'),
 ('Jeres data fra Hamborg', 'Virker ikke — svarene måler ikke det samme',
  'Den, I skal bruge'),
]

# hvad der sker med ét svar paa vejen gennem analysen
vejen = FG.procesdiagram(
    [('Svaret, som det står', 'Ordret, på tysk', LAES),
     ('Koden', 'To ord om, hvad det handler om', KOD),
     ('Kategorien', 'Bunken af koder, der ligner hinanden', KOD),
     ('Citatet i opgaven', 'Det svar, der viser kategorien bedst', SAML)],
    W=600, farver=FARVER)


# ---------------------------------------------------------------------------
# Siden
# ---------------------------------------------------------------------------
BASIS = open('samfundsfag.html', encoding='utf-8').read()
CSS = BASIS[BASIS.find('<style>') + 7:BASIS.find('</style>')]
CSS += '''
h2.sec{font-size:1.4rem;margin:34px 0 8px}
.figur{background:var(--panel2);border:1px solid var(--line);border-radius:14px;
padding:18px;margin:16px 0;text-align:center}
.figur svg{max-width:100%;height:auto}
.figtekst{color:var(--muted);font-size:.9rem;margin:10px 0 0}
.trin{background:var(--panel);border:1px solid var(--line);
border-left:5px solid var(--accent);border-radius:14px;padding:16px 22px;margin:12px 0}
.trin.laes{border-left-color:#1a8f5e}.trin.saml{border-left-color:#b5710a}
.trin h3{margin:0 0 2px;font-size:1.08rem}
.trin .kort{color:var(--muted);font-size:.92rem;margin:0 0 8px}
.trin p{margin:0;color:#374151}
.trin .num{display:inline-flex;align-items:center;justify-content:center;
width:26px;height:26px;border-radius:50%;background:var(--accent);color:#fff;
font-size:.85rem;font-weight:800;margin-right:9px}
.trin.laes .num{background:#1a8f5e}.trin.saml .num{background:#b5710a}
table.tab{width:100%;border-collapse:collapse;margin:10px 0;font-size:.95rem}
table.tab th,table.tab td{border:1px solid var(--line);padding:8px 11px;
text-align:left;vertical-align:top}
table.tab thead th{background:var(--panel2)}
table.tab td.sv{font-style:italic}
table.tab td.kode{font-weight:700;color:var(--accent);white-space:nowrap}
table.tab td.kat{font-weight:700;color:#1a8f5e;white-space:nowrap}
.boks{border-radius:14px;padding:16px 20px;margin:16px 0;border:1px solid var(--line)}
.boks.hvorfor{background:#eaf2fd;border-left:4px solid var(--accent)}
.boks.opgave{background:#eaf7f0;border-left:4px solid var(--good)}
.boks.faelde{background:#fff7e9;border-left:4px solid var(--warn)}
.boks h3{margin:0 0 6px;font-size:1.08rem}
.boks p{margin:0 0 8px}.boks p:last-child{margin:0}
ol.trinliste{margin:6px 0 0;padding-left:22px}ol.trinliste li{margin:6px 0}
.faelde h4{margin:14px 0 2px;font-size:1rem}
.faelde h4:first-of-type{margin-top:0}
.faelde p{margin:0 0 4px;font-size:.95rem}
@media print{header.top,.printbtn,.btnlink{display:none!important}
.figur,.trin,.boks,table.tab{break-inside:avoid;page-break-inside:avoid}
.figur svg{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-size:10.5pt}main{padding:0}@page{size:A4;margin:14mm}}
'''

trin_html = ''.join(
    f'<section class="trin {g}"><h3><span class="num">{i}</span>{html.escape(o)}</h3>'
    f'<p class="kort">{html.escape(u)}</p><p>{t}</p></section>'
    for i, (o, u, g, t) in enumerate(TRIN, 1))

sam_html = ''.join(
    f'<tr><th>{html.escape(a)}</th><td>{html.escape(b)}</td><td>{html.escape(c)}</td></tr>'
    for a, b, c in SAMMENLIGN)

eks_html = ''.join(
    f'<tr><td class="sv">{html.escape(sv)}</td><td class="kode">{html.escape(k)}</td>'
    f'<td class="kat">{html.escape(kat)}</td></tr>' for sv, k, kat in EKSEMPEL)

faelder_html = ''.join(f'<h4>{html.escape(o)}</h4><p>{t}</p>' for o, t in FAELDER)

ord_html = ''.join(
    f'<tr><th>{html.escape(o)}</th><td>{html.escape(t)}</td></tr>' for o, t in ORD)

KROP = f'''<section class="hero"><span class="pill">Samfundsfag · {UGE}</span>
<h1>Kvalitativ analyse af jeres svar fra Hamborg</h1>
<p>I kan ikke tælle jeres svar. I kan læse dem — og det er en metode med sine
egne regler. Her er de.</p>
<button class="printbtn" onclick="window.print()">Print oplægget</button>
<a class="btnlink ghost" href="digital-socialisering.html">Dataarket med tallene</a>
<a class="btnlink ghost" href="samfundsfag.html">Tilbage til samfundsfag</a>
</section>

<div class="boks hvorfor">
<h3>Hvorfor tæller vi ikke svarene?</h3>
<p>Spørgeskemaet fandtes på dansk og på tysk, og de to versioner viste sig ikke
at spørge om helt det samme. Når to spørgsmål ikke betyder nøjagtig det samme,
kan svarene ikke lægges sammen og blive til én procent.</p>
<p><b>Det er ikke en fejl, I skal skjule. Det er et resultat.</b> At få en
oversættelse til at måle det samme på to sprog er noget af det sværeste ved
internationale undersøgelser — og det er grunden til, at de store undersøgelser
bruger år på at teste deres spørgsmål, før de sender dem ud. Skriv det i jeres
opgave: det viser, at I har forstået, hvad der kan gå galt.</p>
<p>Til gengæld kan I noget, tallene ikke kan: I kan høre, <b>hvordan</b> de unge
selv taler om deres mobil. Det er kvalitativ analyse.</p>
</div>

<h2 class="sec">To måder at undersøge på</h2>
<table class="tab"><thead><tr><th></th><th>Kvantitativ</th><th>Kvalitativ</th>
</tr></thead><tbody>{sam_html}</tbody></table>
<p>Ingen af dem er finere end den anden. De svarer bare på hver sit spørgsmål.
Tallene i <a href="digital-socialisering.html">dataarket</a> siger, hvor udbredt
noget er. Jeres svar siger, hvordan det opleves.</p>

<h2 class="sec">Metoden i fem trin</h2>
<div class="figur">{diagram}
<p class="figtekst">Rækkefølgen er ikke til forhandling. Koder du, før du har
læst det hele, bestemmer de første svar, hvad du får øje på i resten.</p></div>
{trin_html}

<h2 class="sec">Sådan ser det ud i praksis</h2>
<p>Her er fem svar, der kunne have stået i jeres skema. <b>De er opdigtede</b> —
de står her for at vise metoden, ikke for at sige noget om de unge, I mødte.</p>
<table class="tab"><thead><tr><th>Svaret</th><th>Koden</th><th>Kategorien</th>
</tr></thead><tbody>{eks_html}</tbody></table>
<p>Læg mærke til svar nummer tre og fem: de to unge er <b>ikke</b> frustrerede
over deres mobil. De passer ikke ind i en historie om afhængighed — og netop
derfor skal de med. En analyse, hvor alle svar peger samme vej, er som regel en
analyse, hvor nogle svar er blevet sorteret fra.</p>
<div class="figur">{vejen}
<p class="figtekst">Vejen fra ét svar til det, der ender i opgaven. Hvert skridt
fjerner noget — derfor skal det oprindelige svar altid kunne findes frem igen.</p>
</div>

<h2 class="sec">Jeres opgave</h2>
<div class="boks opgave">
<h3>I projektgrupperne</h3>
<ol class="trinliste">
<li>Læs <b>alle</b> gruppens svar igennem én gang. Skriv ingenting undervejs.</li>
<li>Kod hvert svar med ét eller to ord. Gør det <b>hver for sig</b> først —
og sammenlign så jeres koder. Hvor I har kodet forskelligt, har I fundet et
svar, der kan læses på to måder. Det er værd at tale om.</li>
<li>Saml koderne i <b>tre til fem kategorier</b>. Giv hver kategori et navn,
der siger, hvad den handler om.</li>
<li>Find til hver kategori <b>to citater</b>: ét der er typisk, og ét der
trækker i en anden retning. Skriv den tyske sætning og jeres oversættelse.</li>
<li>Skriv et afsnit pr. kategori: hvad handler den om, hvad siger citaterne,
og hvad kan I <b>ikke</b> konkludere ud fra den?</li>
<li>Slut med ét afsnit om oversættelsen: hvor var det svært at få de to sprog
til at betyde det samme — og hvad gjorde I ved det?</li>
</ol>
</div>

<h2 class="sec">Fire fælder</h2>
<div class="boks faelde">{faelder_html}</div>

<h2 class="sec">Ord du skal kunne</h2>
<table class="tab"><thead><tr><th>Ord</th><th>Betyder</th></tr></thead>
<tbody>{ord_html}</tbody></table>
<button class="printbtn" onclick="window.print()">Print oplægget</button>'''

DOK = ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
       '<meta name="viewport" content="width=device-width,initial-scale=1">'
       f'<title>Kvalitativ analyse · {UGE} · 9. klasse</title><style>' + CSS +
       '</style></head><body><header class="top"><div class="top-inner">'
       '<a class="brand" href="index.html">Mibelibsen <span>9. klasse</span></a>'
       '<nav class="tabs"><a class="" href="matematik.html">Matematik</a>'
       '<a class="active" href="samfundsfag.html">Samfundsfag</a>'
       '<a class="" href="tysk.html">Tysk</a><a class="" href="fysik.html">Fysik</a>'
       '</nav></div></header><main>' + KROP + '</main><footer>'
       'Undervisningsmateriale · 9. klasse · Mibelibsen.</footer></body></html>')

open(UD, 'w', encoding='utf-8').write(DOK)
print(f'skrevet:  {UD}  ·  {UGE} · {len(TRIN)} trin, {len(EKSEMPEL)} eksempelsvar, '
      f'{len(FAELDER)} fælder, {len(ORD)} ord')
