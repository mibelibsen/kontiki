# -*- coding: utf-8 -*-
"""Bygger naturfagsfestivalens forløb: Plastik og fødevarer.

Tre dele:
  * feature-plastik-og-foedevarer.html  — siden til sitet (åben for alle)
  * elevark-plastik-og-foedevarer.html  — elevarkets kilde, bliver PDF
  * laerervejledning-plastik.html       — lærervejledning + indkøbsliste, PDF

Indkøbslisten regnes ud fra HOLD, GRUPPER og forbruget pr. gruppe, så tallene
ikke kan komme til at modsige programmet.
"""
import sys, os, html, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figurer as FG

SCRATCH = sys.argv[1] if len(sys.argv) > 1 else '.'

# ------------------------------------------------------------------ rammer
# To klasser, 44 elever i alt, fordelt paa tre hold der kommer hver sin dag.
ELEVER = 44
HOLD = 3
PR_GRUPPE = 4                # fire roller, altsaa fire i en fuld gruppe
DAGE = [('Onsdag', '23. september'), ('Torsdag', '24. september'),
        ('Fredag', '25. september')]
INDPAK = ['Husholdningsfilm', 'Frysepose med lynlås', 'Papirspose',
          'Alufolie', 'Ingen indpakning']
assert len(DAGE) == HOLD

# holdene gores saa lige store som muligt: 15, 15, 14
HOLDSTOERRELSER = [ELEVER // HOLD + (1 if i < ELEVER % HOLD else 0)
                   for i in range(HOLD)]
assert sum(HOLDSTOERRELSER) == ELEVER
GRUPPER_PR_DAG = [math.ceil(n / PR_GRUPPE) for n in HOLDSTOERRELSER]
TOTAL_GRUPPER = sum(GRUPPER_PR_DAG)
GRUPPER = max(GRUPPER_PR_DAG)            # det største hold sætter udstyrsbehovet

# ------------------------------------------------------------------ program
PROGRAM = [
 ('0:00', '0:15', 'Velkomst og spørgsmålet', 'Dagens spørgsmål stilles, og '
  'grupperne fordeler rollerne mellem sig.', 'faelles'),
 ('0:15', '0:45', 'Forsøg 1 sættes op', 'Madprøverne vejes og pakkes ind på '
  'fem måder. De skal stå urørt i to timer.', 'forsog'),
 ('0:45', '1:30', 'Forsøg 2 · Hvilken plast er det?', 'Flyde-synke-test i vand '
  'og saltvand. Gæt først, mål bagefter, tjek koden til sidst.', 'forsog'),
 ('1:30', '1:45', 'Pause', '', 'pause'),
 ('1:45', '2:45', 'Forsøg 3 · Lav din egen bioplast', 'Kartoffelmel, vand, '
  'glycerin og eddike koges til en film, der sættes til tørring.', 'forsog'),
 ('2:45', '3:10', 'Vejning nummer to', 'Prøverne vejes igen. Vægttabet regnes '
  'om til procent og tegnes som søjlediagram.', 'forsog'),
 ('3:10', '3:25', 'Dilemmaet', 'Hver gruppe tager stilling — med egne tal.',
  'faelles'),
 ('3:25', '3:30', 'Oprydning', 'Bioplasten er tør nok til at tages med hjem.',
  'faelles'),
]
FARVER = {'faelles': FG.BLA, 'forsog': FG.GRO, 'pause': '#e9edf4'}
slut_min = 3 * 60 + 30
assert PROGRAM[-1][1] == '3:30'

ROLLER = [
 ('Vejemester', 'Læser vægten af og siger tallet højt. Det er den eneste, der '
  'rører vægten.'),
 ('Skriver', 'Skriver alle tal ind i skemaet med det samme — ikke bagefter.'),
 ('Materialemester', 'Henter og rydder op, og holder styr på, at prøverne står, '
  'hvor de skal.'),
 ('Tidsholder', 'Holder øje med klokken og siger til fem minutter før hver '
  'deadline.'),
]
assert len(ROLLER) == PR_GRUPPE  # én rolle pr. plads i en fuld gruppe

# ------------------------------------------------- densiteter til forsøg 2
DENSITET = [
 ('PP', 'Polypropylen', '0,90', 'Flyder i vand', 'Bøtter til smør og salat, '
  'sugerør, låg'),
 ('LDPE', 'Polyethylen, blød', '0,92', 'Flyder i vand', 'Husholdningsfilm, '
  'fryseposer'),
 ('HDPE', 'Polyethylen, hård', '0,95', 'Flyder i vand', 'Mælkeflasker, '
  'vaskemiddelflasker'),
 ('PS', 'Polystyren', '1,05', 'Synker i vand, flyder i saltvand',
  'Yoghurtbægre, engangsbestik'),
 ('PET', 'Polyethylenterephthalat', '1,38', 'Synker i begge',
  'Sodavandsflasker, salatbokse'),
]
MAETTET_SALT = 1.20          # g/cm³ for mættet saltvand ved stuetemperatur
for kode, _, d, svar, _ in DENSITET:
    t = float(d.replace(',', '.'))
    flyder_vand = t < 1.00
    flyder_salt = t < MAETTET_SALT
    ventet = ('Flyder i vand' if flyder_vand else
              'Synker i vand, flyder i saltvand' if flyder_salt else
              'Synker i begge')
    assert svar == ventet, (kode, svar, ventet)   # tabellen skal følge tallene

# ------------------------------------------------------------ indkøbsliste
# (vare, mængde pr. gruppe, enhed, pakke, note)
FORBRUG = [
 ('Agurk', 0.4, 'stk', 'Én agurk giver cirka 15 skiver på 1 cm'),
 ('Kartoffelmel', 10, 'g', '1 spsk pr. gruppe'),
 ('Glycerin, 99 %', 5, 'ml', '1 tsk pr. gruppe · købes på apoteket'),
 ('Husholdningseddike', 5, 'ml', '1 tsk pr. gruppe'),
 ('Frysepose med lynlås', 1, 'stk', 'Én pr. gruppe'),
 ('Papirspose eller madpapir', 1, 'stk', 'Én pr. gruppe'),
 ('Gennemsigtige glas eller bægre', 3, 'stk', 'Vand, saltvand og skylning'),
 ('Engangsbæger til bioplast', 2, 'stk', 'Ét til at blande, ét til at støbe'),
]
# (vare, maengde pr. dag, enhed, note) — det der bruges pr. hold, ikke pr. gruppe
DAGSFORBRUG = [
 ('Salt til mættet saltvand', 360, 'g', 'Cirka 360 g pr. liter vand. '
  'Én liter rækker til et hold og kan genbruges dagen efter'),
 ('Vand til saltvandet', 1, 'liter', 'Lunkent, så saltet opløses'),
]
indkoeb = []
for vare, pr_gruppe, enhed, note in FORBRUG:
    ialt = pr_gruppe * TOTAL_GRUPPER
    buffer = math.ceil(ialt * 1.2)
    indkoeb.append((vare, f'{FG._dk(pr_gruppe)} {enhed}',
                    f'{FG._dk(ialt)} {enhed}', f'{buffer} {enhed}', note))

dagsindkoeb = []
for vare, pr_dag, enhed, note in DAGSFORBRUG:
    ialt = pr_dag * HOLD
    dagsindkoeb.append((vare, f'{FG._dk(pr_dag)} {enhed}',
                        f'{FG._dk(ialt)} {enhed}',
                        f'{FG._dk(math.ceil(ialt * 1.2))} {enhed}', note))

FAST = [
 ('Køkkenvægt med to decimaler', '3 stk', 'Grupperne kan dele. To decimaler er '
  'et krav — med hele gram kan vægttabet ikke ses.'),
 ('Kogeplade eller mikroovn', '1-2 stk', 'Bioplasten skal varmes under omrøring.'),
 ('Husholdningsfilm', '1 rulle', ''),
 ('Alufolie', '1 rulle', ''),
 ('Bagepapir', '1 rulle', 'Bioplasten støbes på bagepapir.'),
 ('Køkkenrulle og karklude', '', ''),
 ('Grydeske eller træspatel', '6 stk', ''),
 ('Tuschpen og maskeringstape', '', 'Alle prøver skal mærkes med gruppe og dag.'),
 ('Engangshandsker', '1 pakke', 'Stivelsesmassen er brandvarm.'),
 ('Denatureret sprit', '500 ml', 'Kun hvis I vil prøve den svære sortering. '
  'Må ikke være i nærheden af kogepladen.'),
]

FORVENTET = [
 ('Ingen indpakning', 'Størst vægttab — ofte flere procent på to timer'),
 ('Papirspose', 'Næststørst. Papir lukker luft igennem'),
 ('Alufolie', 'Midt imellem, afhænger meget af, hvor tæt de har pakket'),
 ('Husholdningsfilm', 'Lille vægttab'),
 ('Frysepose med lynlås', 'Mindst vægttab'),
]

# ---------------------------------------------------------------- figurer
program_fig = FG.procesdiagram(
    [(f'{a} – {b} · {t}', u, g) for a, b, t, u, g in PROGRAM],
    W=660, farver=FARVER,
    legende=[('Fælles', 'faelles'), ('Forsøg i grupper', 'forsog')])
graf_fig = FG.tomt_soejlegitter(
    ['Film', 'Lynlås-|pose', 'Papirs-|pose', 'Alu-|folie', 'Ingen|indpakning'],
    10, 'Vægttab i procent', 'Tegn en søjle for hver indpakning')

# ------------------------------------------------------------------- CSS
BASIS = open('matematik.html').read()
GRUND = BASIS[BASIS.find('<style>') + 7:BASIS.find('</style>')]
EKSTRA = '''
.figur{background:var(--panel2);border:1px solid var(--line);border-radius:14px;
padding:16px;margin:16px 0;text-align:center}
.figur svg{max-width:100%;height:auto}
.blok{background:var(--panel);border:1px solid var(--line);
border-left:5px solid var(--accent);border-radius:14px;padding:18px 22px;
margin:14px 0;box-shadow:var(--shadow)}
.blok.gron{border-left-color:var(--good)}
.blok.advar{border-left-color:var(--bad);background:var(--bad-soft)}
.blok h3{margin:0 0 8px;font-size:1.15rem}
.blok p,.blok li{color:var(--muted);font-size:.97rem}
.blok p{margin:6px 0;max-width:74ch}
table.t{width:100%;border-collapse:collapse;margin:12px 0;font-size:.95rem}
table.t th,table.t td{border:1px solid var(--line);padding:9px 11px;
text-align:left;vertical-align:top}
table.t th{background:var(--panel2)}
table.t td.tal{text-align:right;white-space:nowrap}
table.t tr.tom td{height:30px}
.skriv{border-bottom:1px solid var(--line);display:inline-block;min-width:120px}
.printbtn{background:#fff;border:1px solid var(--line);border-radius:10px;
padding:10px 18px;font-weight:700;font-size:.95rem;cursor:pointer;color:var(--ink);
font-family:inherit;margin:6px 8px 0 0}
.printbtn:hover{border-color:var(--accent);color:var(--accent)}
@media print{header.top,.printbtn,.btnlink{display:none!important}
.blok,.figur{box-shadow:none;break-inside:avoid;page-break-inside:avoid}
body{font-size:10.5pt}main{padding:0}@page{size:A4;margin:13mm}
h2.sec{page-break-after:avoid}}
'''

def side(titel, pill, krop, aktiv='matematik', fane=True):
    nav = ('<nav class="tabs">'
           '<a class="" href="matematik.html">Matematik</a>'
           '<a class="" href="samfundsfag.html">Samfundsfag</a>'
           '<a class="" href="tysk.html">Tysk</a>'
           '<span class="soon">Fysik</span></nav>') if fane else ''
    return ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{titel}</title><style>' + GRUND + EKSTRA +
            '</style></head><body><header class="top"><div class="top-inner">'
            '<a class="brand" href="index.html">Mibelibsen <span>9. klasse</span></a>'
            + nav + '</div></header><main>' + krop + '</main><footer>'
            'Undervisningsmateriale · Mibelibsen · Naturfagsfestival 2026.'
            '</footer></body></html>')


def tabel(hoved, raekker, klasser=None):
    klasser = klasser or [''] * len(hoved)
    th = ''.join(f'<th>{h}</th>' for h in hoved)
    tr = ''.join('<tr>' + ''.join(
        f'<td class="{k}">{c}</td>' for c, k in zip(r, klasser)) + '</tr>'
        for r in raekker)
    return f'<table class="t"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


PROGRAMTABEL = tabel(
    ['Tid', 'Modul', 'Hvad der sker'],
    [(f'{a} – {b}', f'<b>{html.escape(t)}</b>', html.escape(u)) for a, b, t, u, _ in PROGRAM])

# =========================================================== 1 · sitets side
KROP_SITE = f'''<section class="hero"><span class="pill">Feature · Naturfagsfestival</span>
<h1>Plastik og fødevarer</h1>
<p>Et forløb på 3½ time om det, der både er problemet og løsningen: plast om
maden. To klasser, {ELEVER} elever i alt, fordelt på tre blandede hold fra 8. og
9. klasse — ét hold om dagen, onsdag, torsdag og fredag. Tre forsøg, egne
måledata, og et dilemma til sidst, som ingen kan svare på uden tallene.</p>
<a class="btnlink" href="materiale/elevark-plastik-og-foedevarer.pdf">Hent elevarket som PDF</a>
<a class="btnlink ghost" href="index.html">Fagoversigt</a></section>

<div class="figur">{program_fig}</div>

<h2 class="sec">Dagens spørgsmål</h2>
<div class="blok"><h3>Hvornår er plast om maden det klogeste valg?</h3>
<p>Plast i naturen er noget skidt. Plast om en agurk kan være det, der gør, at
agurken bliver spist i stedet for smidt ud. Begge ting er sande på samme tid, og
det er derfor spørgsmålet er værd at bruge en dag på. I slutningen af dagen skal
hver gruppe svare — med deres egne måletal i hånden, ikke med en mavefornemmelse.</p></div>

<h2 class="sec">De tre forsøg</h2>
<div class="blok gron"><h3>1 · Emballagetesten</h3>
<p>Fem ens stykker agurk vejes, pakkes ind på fem forskellige måder og vejes igen
to timer senere. Det, der er forsvundet, er vand. Vægttabet regnes om til
procent, så stykker med forskellig startvægt kan sammenlignes, og tegnes som
søjlediagram.</p></div>
<div class="blok gron"><h3>2 · Hvilken plast er det?</h3>
<p>Stumper af madindpakning lægges i vand og i mættet saltvand. Om de flyder
eller synker afhænger af massefylden, og det afgør hvilken plasttype det er.
Først gætter grupperne, så måler de, og til sidst tjekker de mod
genbrugstrekanten på emballagen — passer det?</p></div>
<div class="blok gron"><h3>3 · Lav din egen bioplast</h3>
<p>Kartoffelmel, vand, glycerin og eddike varmes til en klar, sej masse, der
støbes tyndt ud og tørrer til en film. To hold med forskellig mængde glycerin
viser, at plast ikke er ét materiale, men noget man kan skrue på.</p></div>

<h2 class="sec">Programmet</h2>
{PROGRAMTABEL}

<h2 class="sec">Roller i gruppen</h2>
<p class="mat">Fire roller, så alle i gruppen har noget at gøre hele tiden.
Rollerne byttes ikke undervejs. Er gruppen kun tre, tager den ene både
tidsholder og materialemester.</p>
{tabel(['Rolle', 'Opgave'], [(f'<b>{n}</b>', t) for n, t in ROLLER])}

<div class="blok advar"><h3>Sikkerhed</h3>
<p>Stivelsesmassen bliver over 90 grader varm og klistrer til huden — brug
handsker, og rør kun i den med spatel. Sprit må aldrig stå på eller ved
kogepladen. Og <b>ingenting fra forsøgene må spises</b>, heller ikke agurken.</p></div>'''

open('feature-plastik-og-foedevarer.html', 'w').write(
    side('Plastik og fødevarer · Naturfagsfestival', 'Feature', KROP_SITE))

# =============================================================== 2 · elevark
vejeskema = tabel(
    ['Indpakning', 'Vægt før (g)', 'Vægt efter (g)', 'Tab (g)', 'Tab i %'],
    [(i, '', '', '', '') for i in INDPAK] + [('<b>Kontrol: intet må mangle</b>',
                                              '', '', '', '')],
    ['', 'tal', 'tal', 'tal', 'tal'])
plastskema = tabel(
    ['Emballagestump', 'Vand: flyder/synker', 'Saltvand: flyder/synker',
     'Vores gæt på plasttype', 'Koden på emballagen'],
    [('', '', '', '', '') for _ in range(5)])

KROP_ELEV = f'''<section class="hero"><span class="pill">Naturfagsfestival · elevark</span>
<h1>Plastik og fødevarer</h1>
<p><b>Navn:</b> <span class="skriv"></span> &nbsp; <b>Klasse:</b>
<span class="skriv"></span> &nbsp; <b>Gruppe:</b> <span class="skriv"></span>
&nbsp; <b>Dato:</b> <span class="skriv"></span></p>
<p>I dag skal I svare på ét spørgsmål: <b>hvornår er plast om maden det klogeste
valg?</b> Svaret skal bygge på jeres egne måletal. Skriv alt ned med det samme —
et tal, man husker forkert, er værdiløst.</p>
<button class="printbtn" onclick="window.print()">Print arket</button></section>

<h2 class="sec">Roller — skriv navnene på</h2>
{tabel(['Rolle', 'Opgave', 'Navn'],
       [(f'<b>{n}</b>', t, '<span class="skriv"></span>') for n, t in ROLLER])}

<h2 class="sec">Forsøg 1 · Emballagetesten</h2>
<div class="blok"><h3>Sådan gør I</h3>
<p>1. Skær fem stykker agurk, der er så ens som muligt. 2. Vej hvert stykke, og
skriv vægten i skemaet <b>før</b> I pakker det ind. 3. Pak hvert stykke ind på
sin måde. 4. Mærk prøverne med gruppe og indpakning. 5. Stil dem sammen på det
sted, læreren viser — og rør dem ikke i to timer.</p></div>

<div class="blok"><h3>Vores hypotese</h3>
<p>Vi tror, at <span class="skriv"></span> holder maden bedst, fordi
<span class="skriv" style="min-width:320px"></span></p>
<p>Vi tror, at <span class="skriv"></span> er dårligst, fordi
<span class="skriv" style="min-width:320px"></span></p></div>

<div class="blok"><h3>Hvad skal holdes ens?</h3>
<p>Skriv tre ting, der skal være ens for alle fem prøver, for at forsøget er
fair. Det er den vigtigste opgave på hele arket.</p>
<p>1. <span class="skriv" style="min-width:380px"></span></p>
<p>2. <span class="skriv" style="min-width:380px"></span></p>
<p>3. <span class="skriv" style="min-width:380px"></span></p></div>

{vejeskema}
<div class="blok"><h3>Regn vægttabet om til procent</h3>
<p>Tab i procent = tab i gram divideret med vægten før, gange 100.
Eksempel: taber et stykke 0,45 g af 12,50 g, er tabet 0,45 ÷ 12,50 · 100 = 3,6 %.</p>
<p><b>Hvorfor procent og ikke gram?</b>
<span class="skriv" style="min-width:420px"></span></p></div>

<div class="figur">{graf_fig}</div>

<h2 class="sec">Forsøg 2 · Hvilken plast er det?</h2>
<div class="blok"><h3>Sådan gør I</h3>
<p>Klip fem små stumper af forskellig madindpakning. Skriv jeres <b>gæt</b> først.
Læg så hver stump i vand, tryk den ned under overfladen med en pind, så luften
slipper, og se om den flyder op. Gentag i mættet saltvand. Tjek til sidst
genbrugstrekanten på emballagen.</p>
<p>Flyder i vand: massefylden er under 1 g/cm³ — PP, LDPE eller HDPE.<br>
Synker i vand, men flyder i saltvand: mellem 1 og cirka 1,2 — PS.<br>
Synker i begge: over 1,2 — PET.</p></div>
{plastskema}
<div class="blok"><h3>Passede jeres gæt?</h3>
<p>Hvor mange ramte I rigtigt? <span class="skriv"></span> ud af 5.
Hvad overraskede jer? <span class="skriv" style="min-width:380px"></span></p></div>

<h2 class="sec">Forsøg 3 · Lav din egen bioplast</h2>
<div class="blok"><h3>Opskrift pr. hold — I laver to</h3>
<p><b>Hold A:</b> 1 spsk kartoffelmel · 4 spsk vand · <b>1 tsk glycerin</b> ·
1 tsk eddike.<br>
<b>Hold B:</b> det samme, men <b>kun ¼ tsk glycerin</b>.</p>
<p>Rør sammen koldt, til der ikke er klumper. Varm under omrøring, til massen
bliver klar og sej — det tager et par minutter. Hæld den tyndt ud på bagepapir,
og lad den tørre. Mærk begge med gruppe og A eller B.</p></div>
<div class="blok"><h3>Hvad skete der?</h3>
<p>Hold A føles: <span class="skriv" style="min-width:300px"></span></p>
<p>Hold B føles: <span class="skriv" style="min-width:300px"></span></p>
<p>Hvad gør glycerinen? <span class="skriv" style="min-width:380px"></span></p>
<p>Kunne jeres bioplast pakke en agurk ind i en uge? Hvorfor, eller hvorfor ikke?
<span class="skriv" style="min-width:420px"></span></p></div>

<h2 class="sec">Dilemmaet — gruppens svar</h2>
<div class="blok"><h3>Hvornår er plast om maden det klogeste valg?</h3>
<p>Skriv jeres svar i tre sætninger. Mindst én af dem skal indeholde et tal fra
jeres eget forsøg.</p>
<p>1. <span class="skriv" style="min-width:440px"></span></p>
<p>2. <span class="skriv" style="min-width:440px"></span></p>
<p>3. <span class="skriv" style="min-width:440px"></span></p>
<p><b>Og hvornår er det ikke?</b>
<span class="skriv" style="min-width:420px"></span></p></div>

<div class="blok advar"><h3>Husk</h3>
<p>Handsker på ved kogepladen. Ingenting fra forsøgene må spises — heller ikke
agurken.</p></div>'''

open(os.path.join(SCRATCH, 'elevark-plastik.html'), 'w').write(
    side('Elevark · Plastik og fødevarer', 'Elevark', KROP_ELEV, fane=False))

# ====================================================== 3 · lærervejledning
dage_tabel = tabel(
    ['Dag', 'Dato', 'Hold', 'Elever', 'Grupper'],
    [(d, dato, f'Hold {i} · blandet 8. og 9. klasse', f'{n} elever',
      f'{g} grupper')
     for i, ((d, dato), n, g) in enumerate(
         zip(DAGE, HOLDSTOERRELSER, GRUPPER_PR_DAG), 1)],
    ['', '', '', 'tal', 'tal'])
indkoeb_tabel = tabel(
    ['Vare', 'Pr. gruppe', f'I alt til {TOTAL_GRUPPER} grupper', 'Køb', 'Note'],
    indkoeb, ['', 'tal', 'tal', 'tal', ''])
fast_tabel = tabel(['Udstyr', 'Antal', 'Note'],
                   [(v, a, n) for v, a, n in FAST])
densitet_tabel = tabel(
    ['Kode', 'Navn', 'Massefylde (g/cm³)', 'I forsøget', 'Typisk emballage'],
    [(f'<b>{k}</b>', n, d, s, e) for k, n, d, s, e in DENSITET],
    ['', '', 'tal', '', ''])
forventet_tabel = tabel(['Indpakning', 'Forventet resultat'],
                        [(f'<b>{a}</b>', b) for a, b in FORVENTET])

KROP_LAERER = f'''<section class="hero"><span class="pill">Vejledning til læreren</span>
<h1>Plastik og fødevarer</h1>
<p>Forløb på 3½ time til naturfagsfestivalen. To klasser, {ELEVER} elever i alt,
fordelt på {HOLD} blandede hold fra 8. og 9. klasse. Ét hold om dagen, samme
program alle tre dage. Grupperne er på {PR_GRUPPE} — i alt {TOTAL_GRUPPER}
grupper over de tre dage.</p>
<button class="printbtn" onclick="window.print()">Print vejledningen</button></section>

{dage_tabel}

<h2 class="sec">Fagligt sigte</h2>
<div class="blok"><p>Forløbet samler tre fag om det samme spørgsmål.
<b>Fysik og kemi:</b> massefylde som materialeegenskab, og hvordan et polymer
ændrer sig, når man tilsætter en blødgører. <b>Biologi og sundhed:</b> hvorfor
mad taber vand, og hvad emballage gør ved holdbarhed og madspild.
<b>Matematik:</b> relativ ændring i procent frem for absolut i gram, og
søjlediagram som argument.</p>
<p>Den vigtigste øvelse er ikke selve målingen, men spørgsmålet
<i>hvad skal holdes ens?</i> Det er dér, forsøget bliver naturvidenskab i stedet
for en aktivitet. Brug tid på det, også selvom det koster minutter.</p></div>

<h2 class="sec">Programmet minut for minut</h2>
{PROGRAMTABEL}
<div class="figur">{program_fig}</div>

<h2 class="sec">Forberedelse dagen før</h2>
<div class="blok"><p>Bland mættet saltvand: rør salt i lunkent vand, til der
ligger salt på bunden, som ikke vil opløses. Cirka 360 g salt pr. liter. Lad det
stå og køle af — én liter rækker til et hold.</p>
<p>Skær ikke agurk på forhånd. Den skal skæres på dagen, ellers er vægttabet
startet, før forsøget er.</p>
<p>Stil vægtene op på et bord, der ikke vipper, og væk fra vinduet. En vægt i
solen eller i træk giver ustabile tal.</p>
<p>Find det sted, prøverne skal stå i to timer. Samme sted alle tre dage, ellers
kan holdene ikke sammenligne.</p></div>

<h2 class="sec">Indkøb til alle tre dage</h2>
<p class="mat">Mængderne er regnet ud fra de {TOTAL_GRUPPER} grupper, de
{ELEVER} elever fordeler sig på over tre dage
({' + '.join(str(g) for g in GRUPPER_PR_DAG)} grupper). Kolonnen <b>Køb</b> er
lagt 20 % oven i, fordi noget altid spildes.</p>
{indkoeb_tabel}
<h3>Pr. dag — ikke pr. gruppe</h3>
{tabel(['Vare', 'Pr. dag', f'I alt til {HOLD} dage', 'Køb', 'Note'],
       dagsindkoeb, ['', 'tal', 'tal', 'tal', ''])}
<h3>Udstyr, der ikke bruges op</h3>
{fast_tabel}

<h2 class="sec">Forsøg 2 · facit til massefylde</h2>
<p class="mat">Tallene er typiske værdier for ren plast. Mættet saltvand ligger
omkring {FG._dk(MAETTET_SALT)} g/cm³, og det er derfor det kan skille PS fra
PET.</p>
{densitet_tabel}
<div class="blok"><p><b>To ting, der driller.</b> Skum af polystyren flyder,
selvom PS synker — det er luften i skummet, ikke plasten. Og luftbobler på en
stump får den til at flyde falsk; ungerne skal trykke stumpen under vandet med
en pind først. Bed dem også tjekke genbrugstrekanten <i>til sidst</i>. Gætter de
først og måler bagefter, husker de det.</p></div>

<h2 class="sec">Forsøg 1 · hvad de plejer at måle</h2>
{forventet_tabel}
<div class="blok"><p>Rækkefølgen holder næsten altid. Størrelsen af tabet gør
ikke: to timer i et køligt lokale kan give under én procent på det uindpakkede
stykke, og da bliver forskellene små. Er vejret køligt, så skær tynde skiver
— stor overflade i forhold til vægt giver et tydeligere tab — og stil prøverne
et lunt sted.</p>
<p><b>Hvis tabet er for lille til at kunne ses:</b> lad grupperne slå deres tal
sammen til ét klassegennemsnit pr. indpakning. Så bliver mønstret tydeligt, og
de har samtidig lært, hvorfor man gentager en måling.</p></div>

<h2 class="sec">Blandede hold · 8. og 9. klasse</h2>
<div class="blok"><p>Rollerne er den vigtigste differentiering: de fordeler
arbejdet, uden at nogen bliver tilskuer. Sæt gerne en fra hver årgang på
vejemester og skriver, så de to skal tale sammen om hvert tal.</p>
<p><b>8. klasse</b> kan nøjes med at udfylde skemaet i gram og tegne søjlerne
efter gram. <b>9. klasse</b> regner om til procent og skal kunne forklare, hvorfor
procent er det rigtige mål her — det er præcis den type spørgsmål, der kommer
til prøven.</p>
<p><b>Ekstra til dem, der bliver færdige:</b> vej bioplasten, når den er tør, og
regn ud hvor meget af massen der var vand. Eller lav en ekstra prøve med et
stykke agurk i frysepose <i>med</i> et hul i og sammenlign.</p></div>

<h2 class="sec">Sikkerhed</h2>
<div class="blok advar"><p>Stivelsesmassen bliver over 90 grader varm, og den
klistrer — den er værre end kogende vand at få på huden. Handsker på, og kun
spatel i gryden.</p>
<p>Denatureret sprit er brandfarlig. Den skal stå i den anden ende af lokalet
end kogepladen, og kun bruges, hvis I vælger den svære sortering.</p>
<p>Intet fra forsøgene må spises. Sig det ved velkomsten, og sig det igen, når
agurken kommer frem.</p>
<p>Mærk alle prøver med gruppe og dag. Tre hold på tre dage betyder tre sæt
prøver, der kan forveksles.</p></div>

<h2 class="sec">Nulstilling mellem dagene</h2>
<div class="blok"><p>Smid de gamle madprøver ud med det samme — de lugter dagen
efter. Saltvandet kan genbruges; hæld det tilbage i dunken gennem et kaffefilter.
Bioplasten skal blive liggende, til den er tør: lad den ligge natten over, og lad
ungerne hente den næste dag, hvis de har tid.</p>
<p>Skriv dagens klassegennemsnit op på et ark, der hænger fremme. Så kan hold 2
og 3 sammenligne med dem, der var der før — og fredagens hold har tre datasæt at
konkludere på. Det er den bedste gratis gevinst ved at køre samme forløb tre
dage i træk.</p></div>'''

open(os.path.join(SCRATCH, 'vejledning-plastik.html'), 'w').write(
    side('Vejledning · Plastik og fødevarer', 'Vejledning', KROP_LAERER, fane=False))

print(f'skrevet:  feature-plastik-og-foedevarer.html')
print(f'skrevet:  {SCRATCH}/elevark-plastik.html')
print(f'skrevet:  {SCRATCH}/vejledning-plastik.html')
print(f'rammer:   {ELEVER} elever på {HOLD} hold ({HOLDSTOERRELSER}) · '
      f'{GRUPPER_PR_DAG} grupper pr. dag = {TOTAL_GRUPPER} grupper i alt')
