# -*- coding: utf-8 -*-
"""Bygger digital-socialisering.html — dataark til forloebet i uge 40 og 41.

Siden samler tallene om unges brug af mobil og digitale medier, saa ungerne kan
holde deres egne tal fra spoergeskemaet i Hamborg op mod publicerede tal fra
Danmark, Europa og 44 lande.

Hver kilde er aabnet og laest, ikke refereret fra et referat, og hver kilde er
frit tilgaengelig — intet bag betalingsmur. Dato og stikproeve staar ved hvert
tal, fordi det er det foerste, man skal kunne svare paa i kildekritik.

Figurerne tegnes af claude/figurer.py. Alle hoejder beregnes.
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figurer as FG

UD = 'digital-socialisering.html'

# Afsnittet "Jeres egne tal" er slaaet fra 6. oktober 2026: ungerne var ikke
# faerdige med at oversaette spoergeskemaerne, og svarene viste sig ikke at vaere
# sammenlignelige paa tvaers af de to sprog. Besvarelserne bruges kvalitativt i
# stedet. Saet den til True, hvis der senere kommer tal, der kan taelles.
VIS_EGNE_TAL = False

# ---------------------------------------------------------------------------
# Tallene. (vaerdi, forklaring) — hver gruppe hoerer til én kilde.
# ---------------------------------------------------------------------------
SKAERM = [('15–19 år', 27), ('20–29 år', 28), ('Hele befolkningen', 16)]
FOR_MEGET = [('8–12 år', 25), ('13–17 år', 35), ('18–25 år', 40)]
HBSC_AAR = [('2018', 7), ('2022', 11)]
HBSC_KOEN = [('Piger · sociale medier', 13), ('Drenge · sociale medier', 9),
             ('Piger · gaming', 7), ('Drenge · gaming', 16)]
EU = [('Frankrig', 70), ('Italien', 80), ('Tyskland', 84), ('EU-snit', 88),
      ('Grækenland', 98), ('Tjekkiet', 99)]
PROFIL = [('9–11 år', 34), ('12–14 år', 70), ('15–16 år', 89)]
PISA = [('Danmark', 3.8), ('OECD-snit', 2.0)]

for navn, raekke in (('skærm', SKAERM), ('for meget', FOR_MEGET),
                     ('HBSC år', HBSC_AAR), ('HBSC køn', HBSC_KOEN),
                     ('EU', EU), ('profil', PROFIL)):
    for k, v in raekke:
        assert 0 <= v <= 100, f'{navn}: {k} = {v} er ikke en procent'
assert [v for _, v in EU] == sorted(v for _, v in EU), 'EU-søjlerne skal stige'
assert HBSC_AAR[1][1] > HBSC_AAR[0][1], 'kurven skal gå op fra 2018 til 2022'
assert PISA[0][1] / PISA[1][1] == 1.9, 'Danmark skal ligge 1,9 gange over OECD'

KILDER = [
    ('dst', 'Danmarks Statistik · Hver fjerde ung er på skærmen over 6 timer dagligt',
     'https://www.dst.dk/da/Statistik/udgivelser/NytHtml?cid=54628',
     '31. august 2026', 'Hele befolkningen over 15 år, danske tal fra 2026'),
    ('kfst', 'Konkurrence- og Forbrugerstyrelsen · Børn, unge og forældre på sociale medier',
     'https://kfst.dk/publikationer/kfst/2025/20251202-boern-unge-og-foraeldre-paa-sociale-medier-tid-vaner-og-oplevet-forbrug',
     '2. december 2025', 'Knap 2.000 børn og unge i Danmark, 8 til 25 år'),
    ('uvm', 'Børne- og Undervisningsministeriet · PISA 2022',
     'https://www.uvm.dk/aktuelt/nyheder/uvm/2023/dec/231205-ny-pisa-undersoegelse-elever-over-hele-verden-er-gaaet-tilbage-i-laesning-og-matematik',
     '5. december 2023', '15-årige elever i 81 lande og regioner'),
    ('who', 'WHO Europa · Teens, screens and mental health',
     'https://www.who.int/europe/news/item/25-09-2024-teens--screens-and-mental-health',
     '25. september 2024', '280.000 unge på 11, 13 og 15 år i 44 lande, data fra 2022'),
    ('hbsc', 'HBSC Data Browser · problematisk brug af sociale medier',
     'https://data-browser.hbsc.org/measure/problematic-social-media-use/',
     'Samme undersøgelse', 'Her vælger I selv landene og får tallene side om side'),
    ('sdu', 'SDU · Skolebørnsundersøgelsen, Danmarks del af HBSC',
     'https://www.sdu.dk/da/sif/forskning/projekter/skoleboernsundersoegelsen',
     'Kører i 2026', '5.000 elever i 5., 7. og 9. klasse — altså jævnaldrende'),
    ('eurostat', 'Eurostat · 97 % af unge i EU bruger internettet dagligt',
     'https://ec.europa.eu/eurostat/web/products-eurostat-news/w/edn-20250715-1',
     '15. juli 2025', 'Unge på 16 til 29 år i hele EU, data fra 2024'),
    ('euk', 'EU Kids Online 2|2026 · børns eget syn på aldersgrænser',
     'https://www.hf.uio.no/imk/forskning/senter/barn-unge-medier/eu-kids-online/eukov_report_2-2026_european_childrens_views.pdf',
     '2026', '28.465 børn på 10 til 16 år i 19 lande, indsamlet april 2025 til april 2026'),
    ('tv2', 'TV 2 · Ny bred aftale fjerner mobiltelefoner fra folkeskolerne',
     'https://nyheder.tv2.dk/politik/2025-09-30-ny-bred-aftale-fjerner-mobiltelefoner-fra-folkeskolerne',
     '30. september 2025', 'Aftalen bag den mobilfri folkeskole'),
    ('ft', 'Retsinformation · lovforslaget om obligatorisk mobilfri politik',
     'https://www.retsinformation.dk/eli/ft/202512L00130',
     'Februar 2026', 'Selve lovteksten, som den blev fremsat'),
    ('dr', 'DR · Forsker: Mobilforbud i skolen kommer ti år for sent',
     'https://www.dr.dk/nyheder/indland/forsker-mobilforbud-i-skolen-kommer-ti-aar-sent-nu-ligger-problemet-et-andet-sted',
     '30. september 2025', 'Modstemmen: Andreas Lieberoth, Aarhus Universitet'),
    ('aus', 'DR · Tre måneder efter forbud er 8 ud af 10 australske teenagere stadig på sociale medier',
     'https://www.dr.dk/nyheder/udland/tre-maaneder-efter-forbud-er-8-ud-af-10-australske-teenagere-stadig-paa-sociale-medier',
     '2. august 2026', 'Den australske myndighed eSafety har spurgt over 4.000 børn og familier'),
    ('fra', 'DR · Frankrig forbyder adgang til sociale medier for børn under 15 år',
     'https://www.dr.dk/nyheder/udland/frankrig-forbyder-adgang-til-sociale-medier-boern-under-15-aar',
     '21. juli 2026', 'Første EU-land med en aldersgrænse, i kraft fra september 2026'),
]
NOEGLE = {k: (t, u, d, s) for k, t, u, d, s in KILDER}
assert len(NOEGLE) == len(KILDER), 'to kilder har samme nøgle'


def kilde(noegle, tekst=None):
    t, u, d, _ = NOEGLE[noegle]
    return (f'<a class="kilde" href="{u}" target="_blank" rel="noopener">'
            f'{html.escape(tekst or t)} · {d}</a>')


# ---------------------------------------------------------------------------
# Figurer — alle højder beregnes af figurer.py
# ---------------------------------------------------------------------------
fig_skaerm = FG.soejler([v for _, v in SKAERM], [k for k, _ in SKAERM],
                        'Over 6 timers skærm om dagen · Danmark 2026', '%',
                        farve=[FG.BLA, FG.BLA, FG.MUT])
fig_formeget = FG.soejler([v for _, v in FOR_MEGET], [k for k, _ in FOR_MEGET],
                          'Synes selv, de bruger for meget tid · Danmark 2025', '%')
fig_aar = FG.soejler([v for _, v in HBSC_AAR], [k for k, _ in HBSC_AAR],
                     'Problematisk brug af sociale medier · 44 lande', '%')
fig_koen = FG.soejler([v for _, v in HBSC_KOEN], [k for k, _ in HBSC_KOEN],
                      'Piger og drenge · 44 lande, 2022', '%', W=620)
fig_eu = FG.soejler([v for _, v in EU], [k for k, _ in EU],
                    'Unge 16–29 år med profil på sociale netværk · EU 2024', '%', W=620)
fig_profil = FG.soejler([v for _, v in PROFIL], [k for k, _ in PROFIL],
                        'Har en profil på sociale medier · 19 lande', '%')
fig_pisa = FG.soejler([v for _, v in PISA], [k for k, _ in PISA],
                      'Digitale redskaber i skoletiden · timer om dagen', 'timer')
fig_eget = FG.tomt_soejlegitter(['Danmark', 'Tyskland'], 100, '%',
                                'Jeres egne tal — tegn dem her', trin=10)

AUS = [('Før forbuddet', 52), ('Tre måneder efter', 42)]
assert AUS[0][1] > AUS[1][1], 'andelen skal falde'
fig_aus = FG.soejler([v for _, v in AUS], [k for k, _ in AUS],
                     'Australske under-16-årige med egen konto på sociale medier', '%')


# ---------------------------------------------------------------------------
# Resumé — hvad fundene siger, i fem punkter
# ---------------------------------------------------------------------------
RESUME = [
 ('Danske unge sidder længe foran skærmen — men ikke nødvendigvis længst på '
  'sociale medier.',
  'Mere end hver fjerde dansker på 15 til 19 år har over 6 timers skærm om dagen. '
  'Det er langt over gennemsnittet for befolkningen. Men skærmtid og tid på '
  'sociale medier er ikke det samme, og det er værd at holde adskilt, når I '
  'læser tallene.'),
 ('Det, Danmark topper i, er skærm <i>i skoletiden</i>.',
  'Danske 15-årige bruger digitale redskaber 3,8 timer om dagen i skolen — '
  'højest af alle 81 lande i PISA, og næsten dobbelt så meget som '
  'OECD-gennemsnittet på 2 timer. 72 % siger, de bruger dem i hver time eller '
  'næsten hver time. I OECD er det 16 %. Den forskel er langt større end '
  'forskellen på fritidsforbruget.'),
 ('Problematisk brug stiger, og rammer piger og drenge forskelligt.',
  'På tværs af 44 lande steg problematisk brug af sociale medier fra 7 % i 2018 '
  'til 11 % i 2022. Piger ligger højere end drenge på sociale medier, 13 mod '
  '9 %, mens det er omvendt for gaming, hvor drengene ligger på 16 mod pigernes '
  '7 %. Et samlet tal for "unge" skjuler altså to forskellige mønstre.'),
 ('De unge er selv kritiske — og jo ældre, jo mere.',
  '25 % af de 8 til 12-årige synes, de bruger for meget tid på sociale medier. '
  'Blandt de 13 til 17-årige er det 35 %, og blandt de 18 til 25-årige 40 %. '
  'Det er ikke kun voksne, der synes, der er et problem.'),
 ('Politikerne handler nu — men en lov er ikke det samme som en virkning.',
  'Danmark gør folkeskolen mobilfri fra skoleåret 2026/27. Australien forbød '
  '10. december 2025 sociale medier helt for børn under 16, som det første land '
  'i verden, og Frankrig fulgte efter som første EU-land med en grænse på 15 år '
  'fra september 2026. Men tre måneder efter det australske forbud brugte '
  '<b>8 ud af 10</b> australske teenagere under 16 stadig sociale medier. '
  'Andelen med egen konto faldt fra 52 % til 42 % — et fald, men ikke et stop.'),
]

# ---------------------------------------------------------------------------
# Dataarkets afsnit: (overskrift, indledning, figur, tabel, kildenøgle)
# ---------------------------------------------------------------------------
AFSNIT = [
 ('Hvor længe er danske unge på skærmen?',
  'Tallet dækker <b>al</b> skærmtid: mobil, computer, tv og spil, i fritiden og '
  'i skolen. <b>Den grå søjle er ikke en tredje aldersgruppe.</b> Den er alle '
  'danskere fra 15 til 89 år lagt sammen til ét tal — derfor har den sin egen '
  'farve. Læs forklaringen under figuren, før I bruger tallene.', fig_skaerm,
  [('Over 6 timer om dagen', f'{v} %', k) for k, v in SKAERM]
  + [('Under 1 time om dagen', '3 %', 'Hele befolkningen'),
     ('Under 1 time om dagen', '4 %', '60–74 år'),
     ('Under 1 time om dagen', '8 %', '75–89 år')], 'dst'),

 ('Hvad bruger de tiden på — og hvad synes de selv?',
  'TikTok-brugere er på knap <b>2 timer</b> om dagen, Snapchat-brugere knap '
  '<b>1 time</b>. Søjlerne viser, hvor mange der selv mener, det er for meget.',
  fig_formeget,
  [('Synes selv, de bruger for meget tid', f'{v} %', k) for k, v in FOR_MEGET],
  'kfst'),

 ('Danmark mod resten af verden: skærm i skoletiden',
  'Her skiller Danmark sig ud. <b>72 %</b> af de danske elever bruger digitale '
  'redskaber i hver time eller næsten hver time. I OECD er tallet <b>16 %</b>.',
  fig_pisa,
  [('Digitale redskaber i skoletiden', '3,8 timer om dagen',
    'Danmark — højest af alle 81 lande'),
   ('Digitale redskaber i skoletiden', '2 timer om dagen', 'OECD-gennemsnit'),
   ('Bruger dem i hver time', '72 %', 'Danmark'),
   ('Bruger dem i hver time', '16 %', 'OECD-gennemsnit')], 'uvm'),

 ('Problematisk brug i 44 lande',
  'At brugen er <i>problematisk</i> betyder i undersøgelsen, at den unge har '
  'mistet kontrollen over den: kan ikke lade være, forsømmer andet, og får det '
  'dårligt uden. Det er ikke det samme som at bruge lang tid.', fig_aar,
  [('Problematisk brug af sociale medier', f'{v} %', f'I {k}') for k, v in HBSC_AAR]
  + [('I risiko for problematisk gaming', '12 %', 'I 2022'),
     ('Spiller digitale spil dagligt', '34 %', 'I 2022'),
     ('15-årige piger med konstant onlinekontakt til venner', '44 %', 'I 2022')],
  'who'),

 ('Piger og drenge gør ikke det samme',
  'Søjlerne krydser hinanden: pigerne ligger højest på sociale medier, drengene '
  'på gaming. Hvis man kun ser på ét samlet tal, forsvinder begge mønstre.',
  fig_koen,
  [(k, f'{v} %', 'Problematisk brug, 2022') for k, v in HBSC_KOEN], 'who'),

 ('Hvor mange unge i Europa er på sociale medier?',
  'Tallene gælder unge på 16 til 29 år. Danmark er ikke brudt ud i den udgivelse '
  '— men I kan slå landene op selv i HBSC Data Browser, hvor Danmark er med.',
  fig_eu,
  [(k, f'{v} %', 'Frankrigs tal er fra 2023, resten fra 2024') for k, v in EU],
  'eurostat'),

 ('Virker et forbud?',
  'Australien forbød 10. december 2025 sociale medier for børn under 16 — som '
  'det første land i verden. Myndigheden eSafety har spurgt over 4.000 børn og '
  'familier før og efter. <b>Frankrig</b> blev første EU-land med en grænse, 15 år, '
  'fra september 2026, og <b>Danmark</b> gør folkeskolen mobilfri fra skoleåret '
  '2026/27.', fig_aus,
  [('Havde egen konto før forbuddet', '52 %', 'Australske under 16 år'),
   ('Havde egen konto tre måneder efter', '42 %', 'Australske under 16 år'),
   ('Brugte stadig sociale medier', '8 ud af 10', 'Australske under 16 år'),
   ('Var aldrig blevet bedt om at bekræfte sin alder', '50 %', 'Af dem der svarede'),
   ('Havde selv skrevet, at de var over 16', '37 %', 'Af dem der svarede')],
  'aus'),

 ('Hvornår får børn deres første profil?',
  'Tallene er fra 19 lande og er indsamlet så sent som foråret 2026. '
  '<b>87 %</b> af børnene bruger en smartphone til at komme på nettet hver dag.',
  fig_profil,
  [(f'Har en profil, {k}', f'{v} %', 'Gennemsnit af 19 lande') for k, v in PROFIL],
  'euk'),
]


# ---------------------------------------------------------------------------
# Siden
# ---------------------------------------------------------------------------
BASIS = open('samfundsfag.html', encoding='utf-8').read()
CSS = BASIS[BASIS.find('<style>') + 7:BASIS.find('</style>')]
CSS += '''
h2.sec{font-size:1.4rem;margin:34px 0 8px}
h3.afs{font-size:1.12rem;margin:26px 0 6px;color:#243149}
.figur{background:var(--panel2);border:1px solid var(--line);border-radius:14px;
padding:16px;margin:14px 0 8px;text-align:center}
.figur svg{max-width:100%;height:auto}
.dat{width:100%;border-collapse:collapse;margin:8px 0 6px;font-size:.95rem}
.dat th,.dat td{border:1px solid var(--line);padding:7px 10px;text-align:left}
.dat thead th{background:var(--panel2)}
.dat td.tal{font-weight:800;color:var(--accent);white-space:nowrap;width:150px}
a.kilde{display:inline-block;font-size:.86rem;color:var(--muted);
border-bottom:1px dotted var(--muted);text-decoration:none;margin:2px 0 18px}
a.kilde:hover{color:var(--accent);border-bottom-color:var(--accent)}
.punkt a.kilde{margin:8px 14px 0 0}
.punkt{background:var(--panel);border:1px solid var(--line);
border-left:5px solid var(--accent);border-radius:14px;padding:14px 20px;margin:12px 0}
.punkt h3{margin:0 0 4px;font-size:1.05rem}
.punkt p{margin:0;color:#374151}
.boks{border-radius:14px;padding:16px 20px;margin:16px 0;border:1px solid var(--line)}
.boks.pas{background:#fff7e9;border-left:4px solid var(--warn)}
.boks.eget{background:#eaf7f0;border-left:4px solid var(--good)}
.boks h3{margin:0 0 6px;font-size:1.08rem}
.boks p{margin:0 0 8px}.boks p:last-child{margin:0}
ol.trin{margin:6px 0 0;padding-left:22px}ol.trin li{margin:5px 0}
.film{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:12px 0}
@media(max-width:720px){.film{grid-template-columns:1fr}}
.film a{display:block;background:var(--panel);border:1px solid var(--line);
border-radius:14px;padding:16px 20px;text-decoration:none;color:inherit}
.film a:hover{border-color:var(--accent)}
.film h3{margin:0 0 4px;font-size:1.05rem;color:var(--accent)}
.film p{margin:0;color:var(--muted);font-size:.94rem}
table.kilder{width:100%;border-collapse:collapse;font-size:.92rem;margin-top:8px}
table.kilder th,table.kilder td{border:1px solid var(--line);padding:8px 10px;
text-align:left;vertical-align:top}
table.kilder thead th{background:var(--panel2)}
table.kilder td.dato{white-space:nowrap;color:var(--muted);width:150px}
@media print{header.top,.printbtn,.btnlink{display:none!important}
.figur,.punkt,.boks,table.dat,table.kilder{break-inside:avoid;page-break-inside:avoid}
.figur svg{-webkit-print-color-adjust:exact;print-color-adjust:exact}
a.kilde{color:#000;border-bottom:none}
body{font-size:10.5pt}main{padding:0}@page{size:A4;margin:14mm}}
'''

RESUME_KILDER = [('dst',), ('uvm',), ('who',), ('kfst',), ('tv2', 'aus', 'fra')]
assert len(RESUME_KILDER) == len(RESUME)

resume_html = ''.join(
    f'<div class="punkt"><h3>{i}. {o}</h3><p>{t}</p>'
    + ' '.join(kilde(n) for n in noegler) + '</div>'
    for i, ((o, t), noegler) in enumerate(zip(RESUME, RESUME_KILDER), 1))

afsnit_html = ''
for overskrift, indledning, figur, raekker, noegle in AFSNIT:
    rk = ''.join(f'<tr><td>{html.escape(a)}</td><td class="tal">{html.escape(b)}</td>'
                 f'<td>{html.escape(c)}</td></tr>' for a, b, c in raekker)
    afsnit_html += (
        f'<h3 class="afs">{overskrift}</h3><p>{indledning}</p>'
        f'<div class="figur">{figur}</div>'
        f'<table class="dat"><thead><tr><th>Hvad</th><th>Tal</th><th>Hvem</th></tr>'
        f'</thead><tbody>{rk}</tbody></table>'
        f'{kilde(noegle, "Kilde: " + NOEGLE[noegle][0])}')

kilder_html = ''.join(
    f'<tr><th><a href="{u}" target="_blank" rel="noopener">{html.escape(t)}</a></th>'
    f'<td class="dato">{d}</td><td>{html.escape(s)}</td></tr>'
    for _, t, u, d, s in KILDER)

egne_tal = f'''<h2 class="sec">Jeres egne tal</h2>
<div class="boks eget">
<h3>Sæt jeres spørgeskema ved siden af</h3>
<p>I har selv samlet svar ind fra tyske unge på turen til Hamborg. Det er den
samme slags data som ovenfor — bare jeres egen. Tegn jeres tal ind i gitteret
herunder, og hold dem op mod tallene fra Danmark og fra de 44 lande.</p>
<ol class="trin">
<li>Vælg <b>ét</b> spørgsmål fra jeres skema, hvor svaret kan laves om til en procent.</li>
<li>Regn procenten ud for de danske svar og for de tyske svar hver for sig.</li>
<li>Tegn de to søjler. Skriv <b>hvor mange</b> der har svaret over hver søjle.</li>
<li>Find et tal i dataarket ovenfor, der måler noget af det samme. Ligner jeres
resultat det — og hvis ikke, hvad kan forklare forskellen?</li>
<li>Slå jeres eget land op i <a href="{NOEGLE['hbsc'][1]}" target="_blank"
rel="noopener">HBSC Data Browser</a> og vælg to lande mere at sammenligne med.</li>
</ol>
</div>
<div class="figur">{fig_eget}</div>''' if VIS_EGNE_TAL else ''

KROP = f'''<section class="hero"><span class="pill">Samfundsfag · Digital socialisering</span>
<h1>Unges brug af mobil og digitale medier</h1>
<p>Dataark til forløbet i uge 40 og 41. Alle tal herunder er hentet i kilden selv,
ikke i et referat, og hver kilde er gratis at læse. Dato og stikprøve står ved
hvert tal — det er det første, I skal kunne svare på.</p>
<button class="printbtn" onclick="window.print()">Print dataarket</button>
<a class="btnlink ghost" href="samfundsfag.html">Tilbage til samfundsfag</a>
</section>

<h2 class="sec">Hvad tallene siger</h2>
{resume_html}

<h2 class="sec">Dataarket</h2>
{afsnit_html}

<div class="boks pas">
<h3>Hvorfor er "hele befolkningen" lavest?</h3>
<p>Det ser forkert ud: 27 % af de 15–19-årige og 28 % af de 20–29-årige er på
skærmen over 6 timer om dagen — men for hele befolkningen er det kun 16 %.
Burde den søjle ikke være størst, når den indeholder alle de andre?</p>
<p><b>Nej, for den er ikke en sum. Den er et gennemsnit.</b> De 16 % betyder:
tager man alle danskere fra 15 til 89 år under ét, så er 16 ud af 100 på
skærmen over 6 timer. Og den gruppe rummer alle de voksne og ældre, der bruger
skærmen langt mindre end de unge. De trækker gennemsnittet <b>ned</b>, ikke op.</p>
<p>Samme kilde viser det direkte: kun <b>3 %</b> af hele befolkningen bruger
under 1 time om dagen — men <b>4 %</b> af de 60–74-årige og <b>8 %</b> af de
75–89-årige. Jo ældre, jo flere med lavt forbrug.</p>
<p><b>Regel at huske:</b> et gennemsnit for en hel befolkning kan godt ligge
<i>under</i> hver eneste gruppe, man kan se i figuren — hvis de grupper, man
ikke kan se, ligger lavt nok. Spørg derfor altid: er det her et tal for
<i>én gruppe</i>, eller for <i>alle</i>?</p>
</div>

{egne_tal}<div class="boks pas">
<h3>Pas på med tallene</h3>
<p><b>Hvor mange har svaret?</b> Et skema med 25 svar og en undersøgelse med
280.000 svar er ikke det samme slags tal. Et enkelt svar flytter den lille
undersøgelse meget — og den store næsten ingenting. Spørg altid om antallet,
før I ser på procenten.</p>
<p><b>Det samme land kan fortælle to historier.</b> Danske unge har et højt
skærmforbrug sammenlignet med lande, vi ligner. Men de er <i>ikke</i> blandt dem,
der bruger mest tid på internet og sociale medier — til gengæld ligger de i bunden,
når det gælder tid brugt fysisk sammen med jævnaldrende. Begge dele er sande.
Hvilket tal man vælger, afgør historien.</p>
<p><b>Skærmtid er ikke ét tal.</b> 3,8 timer i skolen og 6 timer i alt måler ikke
det samme. Spørg altid: hvad tæller med, og hvem er blevet spurgt?</p>
<p><b>Tallene er fra forskellige år.</b> HBSC-tallene er fra 2022, PISA fra 2022,
Eurostat fra 2024 og Danmarks Statistik fra 2026. Fire år er lang tid på et
område, der flytter sig så hurtigt.</p>
</div>

<h2 class="sec">Film</h2>
<div class="film">
<a href="https://www.dr.dk/drtv/serie/alene-hjemme-paa-nettet_440656" target="_blank" rel="noopener">
<h3>DR · Alene hjemme på nettet</h3>
<p>50 danske børn og unge på 12 til 18 år fortæller om, hvad de møder online.
Tættest på ungernes egen alder.</p></a>
<a href="https://play.tv2.dk/program/det-farlige-liv-paa-mobilen-26c2c226-1e8b-4fba-9dc4-ee2a02ac2650" target="_blank" rel="noopener">
<h3>TV 2 · Det farlige liv på mobilen</h3>
<p>12 minutter om, hvordan sociale medier har sat sig i børn og unges hverdag.
Passer i én lektion.</p></a>
</div>

<h2 class="sec">Kilder</h2>
<p>Alle kilder er frit tilgængelige. Kilder bag betalingsmur er holdt ude, så
ungerne kan åbne hver eneste af dem selv.</p>
<table class="kilder"><thead><tr><th>Kilde</th><th>Udgivet</th>
<th>Hvem er spurgt</th></tr></thead><tbody>{kilder_html}</tbody></table>
<button class="printbtn" onclick="window.print()">Print dataarket</button>'''

DOK = ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
       '<meta name="viewport" content="width=device-width,initial-scale=1">'
       '<title>Unges brug af mobil og digitale medier · 9. klasse</title><style>'
       + CSS + '</style></head><body><header class="top"><div class="top-inner">'
       '<a class="brand" href="index.html">Mibelibsen <span>9. klasse</span></a>'
       '<nav class="tabs"><a class="" href="matematik.html">Matematik</a>'
       '<a class="active" href="samfundsfag.html">Samfundsfag</a>'
       '<a class="" href="tysk.html">Tysk</a><a class="" href="fysik.html">Fysik</a>'
       '</nav></div></header><main>' + KROP + '</main><footer>'
       'Undervisningsmateriale · 9. klasse · Mibelibsen.</footer></body></html>')

open(UD, 'w', encoding='utf-8').write(DOK)
print(f'skrevet:  {UD}  ·  {len(RESUME)} resumépunkter, {len(AFSNIT)} dataafsnit, '
      f'{len(KILDER)} kilder')
