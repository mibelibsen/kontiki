#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bygger turen i HafenCity: at bygge og bo med risiko for stormflod.

    python3 claude/byg_hafencity.py <scratch-mappe>

Skriver hafencity.html og et gruppeark til print (ét A4 pr. gruppe).

Turen står ét sted nedenfor — STOP og GRUPPER — og både siden og gruppearkene
bygges af de samme lister. Tiderne lægges sammen og tjekkes mod den samlede
længde, så programmet ikke kan komme til at love fire timer og vare fem.

Tal, der er slået efter (kilder står på siden):
  · warften i HafenCity ligger 7,8–8,5 m over NHN, i øst hævet til 8,3
  · promenaderne ligger på de gamle kajers niveau og må gerne oversvømmes
  · stormfloden 1962: 5,70 m ved Pegel St. Pauli, over 300 døde i Hamborg
  · stormfloden 1976: 6,45 m — højere, men digerne holdt
  · Hafen.City.Horizonte, Baakenallee 33: ti-fr 10–16, gratis
"""
import html
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figurer as FG                                         # noqa: E402

SCRATCH = sys.argv[1] if len(sys.argv) > 1 else '.'
ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROD)

# ===================================================== 1 · turen
# Opgaverne står på tysk — ungerne skal oversætte dem for at kunne løse dem.
# Den danske udgave er til den voksne og lægges i vejledning/, som ikke
# udgives. Hver post er (minutter, navn, hvor, hvad man ser, [(tysk, dansk)]).
STOP = [
 (20, 'Speicherstadt', 'Kibbelstegbrücke und der Fleet dahinter',
  'Den gamle måde at gøre det på: pakhusene står uden for diget og bliver '
  'oversvømmet flere gange hver vinter. Derfor er der mursten forneden, varer '
  'blev hejst op på de øverste etager, og portene har riller i siderne, som '
  'skot skydes ned i.',
  [('Findet ein Tor, in dessen Rahmen Rillen für Dammbalken sind. Sie liegen '
    'ungefähr auf Augenhöhe.',
    'Find en port med riller til skot i karmen — de sidder omtrent i '
    'øjenhøjde.'),
   ('Schaut nach, bis zu welcher Höhe die Ziegel ausgetauscht oder '
    'ausgebessert worden sind.',
    'Se efter, hvor højt op murstenene er skiftet ud eller repareret.'),
   ('Stellt euch auf die Brücke: Wie nah liegt das Wasser an der Straße?',
    'Stå på broen: hvor tæt ligger vandet på gaden?')]),
 (20, 'Sandtorhafen', 'Magellan-Terrassen',
  'Trappen mellem de to niveauer. Nederst promenaden, der må blive våd, '
  'øverst byen, der ikke må. Terrasserne er selve overgangen — og de '
  'forsvinder i vandet, når det står højt.',
  [('Zählt die Stufen vom Wasser bis zur obersten Terrasse und messt eine '
    'Stufe. Wie groß ist der Höhenunterschied?',
    'Tæl trinnene fra vandet op til øverste terrasse, og mål et trin. Hvor '
    'stor er højdeforskellen?'),
   ('Vergleicht euer Ergebnis mit den Zahlen im Querschnitt. Stimmt es?',
    'Sammenlign resultatet med tallene på tværsnittet. Passer det?'),
   ('Stellt euch zu dritt auf die unterste Stufe und zu dritt auf die '
    'oberste — ein Foto.',
    'Stå tre på nederste trin og tre på øverste — ét billede.')]),
 (20, 'Dalmannkai und Am Kaiserkai', 'Die Promenade am Sandtorhafen',
  'Warften i brug. Promenaden ligger lavt, gaden ligger otte meter oppe, og '
  'imellem dem er der porte, ramper og trapper. Parkeringskældrene kan lukkes '
  'af med fluttore, når varslet kommer.',
  [('Findet ein Fluttor oder eine Einfahrt, die geschlossen werden kann. Wie '
    'hoch ist sie?',
    'Find en flodport eller en nedkørsel, der kan lukkes. Hvor høj er den?'),
   ('Findet einen Eingang, dessen Tür höher liegt als der Gehweg.',
    'Find en indgang, hvor døren sidder højere end fortovet.'),
   ('Verfolgt einen Fluchtweg mit den Augen: Wohin würdet ihr gehen, wenn das '
    'Wasser jetzt käme?',
    'Følg en flugtvej med øjnene: hvor ville I gå hen, hvis vandet kom nu?')]),
 (15, 'Lohsepark und Elbarkaden', 'Magdeburger Hafen',
  'Parken ligger på warftniveau, og arkaderne langs vandet er bygget, så '
  'stueetagen kan tåle at stå i vand. Her er forskellen på de to niveauer '
  'lettest at fotografere på ét billede.',
  [('Macht ein Foto, auf dem beide Ebenen zu sehen sind — auf jeder steht '
    'eine Person.',
    'Tag ét billede, hvor begge niveauer er med — en person på hvert.'),
   ('Findet etwas, das wegschwimmen würde, wenn das Wasser um zwei Meter '
    'steigt.',
    'Find noget, der ville flyde væk, hvis vandet steg to meter.')]),
 (30, 'Baakenhafen', 'Hafen.City.Horizonte, Baakenallee 33',
  'Den nyeste del af HafenCity, bygget højere end den ældste. I udstillingen '
  'står byen som model i 1:500, så hele systemet kan ses fra oven. Gratis '
  'adgang, åbent torsdag 10–16.',
  [('Findet eure eigenen Stationen auf dem Modell und fotografiert sie von '
    'oben.',
    'Find jeres egne stop på modellen, og fotografér dem oppefra.'),
   ('Fragt die Mitarbeiter nach einer Sache, die ihr draußen auf der Straße '
    'nicht sehen konntet.',
    'Spørg personalet om én ting, I ikke kunne se ude på gaden.'),
   ('Macht das letzte Gruppenfoto vor dem Modell.',
    'Tag gruppens sidste billede foran modellen.')]),
]

# (tysk navn, dansk navn, tysk beskrivelse, dansk beskrivelse, [(tysk, dansk)])
GRUPPER = [
 ('Die zwei Ebenen', 'De to niveauer',
  'Die Warft: Die Stadt liegt auf einem künstlichen Hügel, die Promenade ist '
  'unten am Wasser geblieben.',
  'Warften: byen ligger på en kunstig bakke, mens promenaden er blevet '
  'liggende nede ved vandet.',
  [('Ein Foto von der Promenade, mit der Straße hinter euch, oben in der '
    'Höhe.', 'Et billede fra promenaden med gaden bag jer, oppe i højden.'),
   ('Ein Foto von der Straße aus, auf dem die Promenade unten zu sehen ist.',
    'Et billede fra gadeniveau, hvor promenaden ses nedenfor.'),
   ('Ein Foto, auf dem eine Person von euch genau dort steht, wo die eine '
    'Ebene in die andere übergeht.',
    'Et billede, hvor en af jer står præcis dér, hvor det ene niveau bliver '
    'til det andet.')]),
 ('Tore, Dammbalken und Türen', 'Porte, skot og døre',
  'Alles, was das Wasser draußen hält, wenn die Warnung kommt: Fluttore, '
  'Rillen für Dammbalken, erhöhte Türschwellen, Rampen.',
  'Alt det, der lukker vandet ude, når varslet kommer: fluttore, riller til '
  'skot, hævede dørtrin, ramper.',
  [('Eine Nahaufnahme einer Rille oder eines Tores — mit einer Hand daneben, '
    'damit man die Größe sieht.',
    'Et nærbillede af en rille eller en port — med en hånd ved siden af, så '
    'man kan se størrelsen.'),
   ('Ein Foto einer Einfahrt zu einer Tiefgarage.',
    'Et billede af en nedkørsel til en parkeringskælder.'),
   ('Ein Foto einer Tür, die höher liegt als der Gehweg.',
    'Et billede af en dør, der sidder højere end fortovet.')]),
 ('Die Fluchtwege', 'Flugtvejene',
  'Man flieht nicht aus der HafenCity heraus — man geht nach oben und über '
  'die Brücken. Findet den Weg, den ein Bewohner nehmen würde.',
  'Man flygter ikke ud af HafenCity — man går opad og hen over broerne. Find '
  'vejen, en beboer ville tage.',
  [('Ein Foto einer Brücke zwischen zwei Warften.',
    'Et billede af en bro mellem to warfter.'),
   ('Ein Foto einer Treppe oder Rampe von der Promenade zur Straße.',
    'Et billede af en trappe eller rampe fra promenaden op til gaden.'),
   ('Ein Foto von dem Ort, an dem ihr euch sammeln würdet, wenn das Wasser '
    'käme.', 'Et billede taget fra det sted, I ville samles, hvis vandet kom.')]),
 ('Die alte Art zu bauen', 'Den gamle måde',
  'Speicherstadt: Statt das Wasser draußen zu halten, hat man so gebaut, dass '
  'es hereinkommen darf. Was hat das gekostet, und was hat funktioniert?',
  'Speicherstadt: i stedet for at holde vandet ude byggede man, så det måtte '
  'komme ind. Hvad kostede det, og hvad virkede?',
  [('Ein Foto von Ziegeln und einem Tor im Erdgeschoss.',
    'Et billede af mursten og port i stueetagen.'),
   ('Ein Foto, das zeigt, wie die Waren nach oben gehievt wurden.',
    'Et billede, der viser, hvor varerne blev hejst op.'),
   ('Ein Foto, auf dem ihr ein altes und ein neues Gebäude vergleicht.',
    'Et billede, hvor I sammenligner et gammelt og et nyt hus.')]),
 ('Was nass werden darf', 'Det, der må blive vådt',
  'Promenaden, Terrassen, Pontons und Treppen, die einige Tage im Jahr unter '
  'Wasser stehen.',
  'Promenader, terrasser, pontoner og trapper, der er bygget til at stå under '
  'vand nogle dage om året.',
  [('Ein Foto eines Pontons oder Schwimmstegs, der mit dem Wasserstand steigt '
    'und fällt.',
    'Et billede af en flydebro eller ponton, der følger vandstanden.'),
   ('Ein Foto von einer Stelle, an der man sehen kann, dass das Wasser da '
    'war.', 'Et billede af et sted, hvor I kan se, at vandet har været der.'),
   ('Ein Foto einer Bank, einer Lampe oder eines Mülleimers, der '
    'festgeschraubt ist — oder eben nicht.',
    'Et billede af en bænk, lampe eller skraldespand, der er skruet fast — '
    'eller som ikke er.')]),
]

# De ord, opgaverne ikke kan løses uden. Resten må de selv slå op.
WORTLISTE = [
 ('die Sturmflut', 'stormfloden'), ('der Deich', 'diget'),
 ('die Warft', 'warften, den kunstige bakke'),
 ('das Fluttor', 'flodporten'), ('der Dammbalken', 'skottet, bjælken'),
 ('die Rille', 'rillen, sporet'), ('der Gehweg', 'fortovet'),
 ('die Tiefgarage', 'parkeringskælderen'), ('der Fluchtweg', 'flugtvejen'),
 ('der Ziegel', 'murstenen'), ('der Schwimmsteg', 'flydebroen'),
 ('der Wasserstand', 'vandstanden'),
 ('der Höhenunterschied', 'højdeforskellen'), ('die Ebene', 'niveauet'),
 ('überschwemmen', 'at oversvømme'), ('das Erdgeschoss', 'stueetagen'),
 ('die Stufe', 'trinnet'), ('hieven', 'at hejse'),
]

# ------------------------------------------------------------------- dagen
AFGANG = '10.00'                # fælles afgang fra hotellet
OPSAMLING = '14.30'             # fælles opsamling
MOEDESTED = 'Magellan-Terrassen ved Sandtorhafen'
MOEDE_HVORFOR = ('trapperne kan ikke forveksles med noget andet, der er plads '
                 'til alle at sidde ned, og der er fire minutter til U4 ved '
                 'Überseequartier')
# (gangen fra hotellet regnes nu pr. gruppe af koordinaterne)
FROKOST = 40                    # grupperne spiser selv, men sammen

# Grupperne sendes på tværs: hver gruppe har sit eget startsted og sin egen
# rækkefølge. Så står de ikke i kø ved det samme motiv, og de kommer til
# stederne i forskellig belysning og forskellig rækkefølge — to grupper med
# samme emne ender med forskellige billeder.
# Hver rute SLUTTER ved mødestedet (sted 2, Magellan-Terrassen). Så skal
# ingen gruppe nå tilbage fra en fjern ende klokken 14.30, og hele dagen kan
# gås til fods — ingen ubahn.
# Hver gruppe starter sit eget sted. Rækkefølgen derfra er den korteste vej,
# der når alle fem steder og slutter ved mødestedet — fundet ved at regne alle
# 120 muligheder igennem, ikke ved at kigge på kortet.
MOEDE_STED_NR = 2               # Magellan-Terrassen er også sted nr. 2
RAEKKEFOELGE = {
 1: [1, 3, 4, 5, 2],
 2: [2, 4, 5, 3, 1],
 3: [3, 1, 4, 5, 2],
 4: [4, 5, 3, 1, 2],
 5: [5, 4, 1, 3, 2],
}
assert all(sorted(r) == [1, 2, 3, 4, 5] for r in RAEKKEFOELGE.values()), \
    'hver gruppe skal nå alle fem steder'
assert len({r[0] for r in RAEKKEFOELGE.values()}) == 5, \
    'de fem grupper skal starte fem forskellige steder'
assert len({tuple(r) for r in RAEKKEFOELGE.values()}) == 5, \
    'de fem rækkefølger skal være forskellige'

# Koordinater slået op i OpenStreetMap (Nominatim), så afstandene ikke
# hviler på et gæt. Gangafstanden regnes som fugleflugt gange 1,3 — den
# sædvanlige tommelfingerregel i by — og rundes til nærmeste 50 meter, fordi
# den er et overslag og ikke skal se mere præcis ud, end den er.
HOTEL = 'a&o Hamburg Hauptbahnhof, Amsinckstraße 2–10'
KOORDINAT = {
 0: (53.5474311, 10.0106128),   # hotellet
 1: (53.5433082, 9.9905648),    # Am Sandtorkai 30, midt i Speicherstadt
 2: (53.5424027, 9.9925640),    # Magellan-Terrassen
 3: (53.5414927, 9.9893205),    # Am Kaiserkai
 4: (53.5424854, 10.0052118),   # Lohsepark
 5: (53.5377862, 10.0135270),   # Baakenallee 33
}
OMVEJ = 1.3


def fugleflugt(a, b):
    R = 6371000
    la1, lo1 = map(math.radians, KOORDINAT[a])
    la2, lo2 = map(math.radians, KOORDINAT[b])
    h = (math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2)
         * math.sin((lo2 - lo1) / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(h))


def afstand(a, b):
    return 0 if a == b else round(fugleflugt(a, b) * OMVEJ / 50) * 50


TEMPO = 80                      # meter i minuttet med en flok niendeklasser


# Fire af de fem ruter slutter præcis ved mødestedet; den femte 200 m derfra.
assert max(afstand(r[-1], MOEDE_STED_NR) for r in RAEKKEFOELGE.values()) <= 250, \
    'en rute slutter for langt fra mødestedet til at være tryg klokken 14.30'


def rutens_tal(nr):
    """Gangmeter, gangminutter og vejen tilbage til mødestedet."""
    r = RAEKKEFOELGE[nr]
    meter = sum(afstand(r[i], r[i + 1]) for i in range(len(r) - 1))
    hjem = afstand(r[-1], MOEDE_STED_NR)
    return meter, round(meter / TEMPO), hjem, round(hjem / TEMPO)


FOTOREGLER = [
 'Der skal være <b>mindst én fra gruppen</b> med på hvert billede. Uden et '
 'menneske kan man ikke se, hvor stort noget er.',
 'Tag <b>højst fem billeder pr. stop</b>. I skal vælge undervejs, ikke '
 'bagefter.',
 'Hold telefonen <b>vandret</b>. Billederne skal bruges i et oplæg.',
 'Døb filerne <b>gruppe_stop_kort-tekst</b> — fx <i>3_dalmannkai_flodport</i>.',
 'Læg billederne i <b>billedmappen i Teams løbende</b> — efter hvert stop, '
 'i jeres egen undermappe. Vi følger med undervejs, så vent ikke til I er '
 'hjemme.',
]

SIKKERHED = [
 f'<b>Vær ved mødestedet {OPSAMLING}</b> — ikke {OPSAMLING} plus ti minutter. '
 'Sæt en alarm i telefonen med det samme.',
 'Gruppen holder sammen hele dagen. Ingen går alene, heller ikke «lige '
 'derhen».',
  'Promenaderne har ingen rækværk mod vandet mange steder. Ingen fotografering '
 'med ryggen til kajkanten.',
 'Cykelstierne i HafenCity er hurtige og ligger ofte i samme farve asfalt som '
 'fortovet.',
 'Alle stop er gratis. Der er ingen museer med entré på ruten.',
 'Der er toiletter ved Überseequartier og i Hafen.City.Horizonte.',
]

I_ALT = sum(m for m, *_ in STOP)
RAADIGHED = (14 * 60 + 30) - (10 * 60)          # 10.00 til 14.30

# Hver gruppes dag regnes for sig — ruterne er forskellige, så luften er det
# også. Den strammeste af de fem bestemmer, om dagen kan lade sig gøre.
DAGSREGNSKAB = {}
for _nr in RAEKKEFOELGE:
    _m, _gang, _hm, _hjem = rutens_tal(_nr)
    # grupperne starter fem forskellige steder, så de har ikke lige langt ud
    # til deres eget startsted — det skal med i regnskabet
    _ud_m = afstand(0, RAEKKEFOELGE[_nr][0])      # fra hotellet
    _ud = round(_ud_m / TEMPO)
    _brugt = _ud + I_ALT + _gang + FROKOST + _hjem
    DAGSREGNSKAB[_nr] = dict(meter=_m, gang=_gang, hjem_m=_hm, hjem=_hjem,
                             ud_m=_ud_m, ud=_ud, brugt=_brugt,
                             luft=RAADIGHED - _brugt)
LUFT = min(d['luft'] for d in DAGSREGNSKAB.values())
assert LUFT >= 25, (f'den strammeste gruppe har kun {LUFT} minutters luft — '
                    f'ruterne kan ikke nås inden {OPSAMLING}')
assert len(STOP) == len(GRUPPER) == 5, 'fem steder og fem grupper'
for _, _, _, _, opg in GRUPPER:
    assert len(opg) == 3, 'hver gruppe skal have tre billeder'

# ===================================================== 2 · figurer
KORTNAVN = {nr: STOP[nr - 1][1].split(' und ')[0]
            for nr in KOORDINAT if nr}
KORTNAVN[0] = 'Hotellet'
# hvor navnet skal stå i forhold til prikken — de tre vestlige steder
# ligger så tæt, at de ellers skriver oven i hinanden
ETIKET = {0: 'o', 1: 'o', 2: 'h', 3: 'u', 4: 'v', 5: 'u'}
PUNKTER = {nr: (KORTNAVN[nr], *KOORDINAT[nr], ETIKET[nr]) for nr in KOORDINAT}
fig_kort = FG.rutekort(PUNKTER)   # oversigt uden rute

fig_snit = FG.vandstandssnit(
    promenade=(4.5, 5.5), warft=(7.5, 8.3),
    maerker=[('Stormflod 1962', 5.70), ('Stormflod 1976', 6.45)])
fig_rute = FG.procesdiagram(
    [(f'{navn} · {m} min', hvor, 'frokost' if 'Mittagessen' in navn else 'stop')
     for m, navn, hvor, _, _ in STOP],
    W=660, farver={'stop': FG.BLA, 'frokost': '#e9edf4'})


def esc(t):
    return html.escape(t, quote=False)


# ===================================================== 3 · fælles stumper
PALET = '''
:root{--bg:#fff;--panel:#fff;--panel2:#f4f6fb;--ink:#1a2233;--muted:#586074;
--line:#d3dae7;--accent:#1f6fd6;--good:#1a8f5e;--warn:#b5710a;
--shadow:0 1px 2px rgba(20,30,50,.06)}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-size:16px;
font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,
Arial,sans-serif;line-height:1.5;-webkit-text-size-adjust:100%}
a{color:var(--accent)}
'''

WORT_HTML = ''.join(f'<tr><td><b>{esc(d_)}</b></td><td>{esc(da)}</td></tr>'
                    for d_, da in WORTLISTE)


def wortliste(aaben=False):
    return (f'<details class="ord"{" open" if aaben else ""}>'
            f'<summary>Wortliste — {len(WORTLISTE)} ord, I får forærende</summary>'
            f'<table class="ord">{WORT_HTML}</table></details>')


# ===================================================== 4 · gruppesiderne
GRUPPE_CSS = PALET + '''
.top{position:sticky;top:0;z-index:5;background:var(--accent);color:#fff;
padding:12px 16px}
.top .nr{font-size:.78rem;letter-spacing:.09em;text-transform:uppercase;
opacity:.85}
.top h1{margin:2px 0 0;font-size:1.25rem;line-height:1.25}
main{padding:14px 16px 40px;max-width:640px;margin:0 auto}
h2{font-size:1.02rem;margin:22px 0 8px;color:var(--muted);
text-transform:uppercase;letter-spacing:.05em}
.intro{background:var(--panel2);border:1px solid var(--line);border-radius:12px;
padding:12px 14px;margin:12px 0;font-size:.97rem}
.intro .da{color:var(--muted);font-size:.88rem;margin-top:6px;display:block}
label.p{display:flex;gap:12px;align-items:flex-start;padding:12px 13px;
border:1px solid var(--line);border-radius:12px;margin:8px 0;
background:var(--panel);box-shadow:var(--shadow);cursor:pointer}
label.p input{width:24px;height:24px;margin:1px 0 0;flex:0 0 auto;
accent-color:var(--good)}
label.p span{font-size:.97rem}
label.p input:checked+span{color:var(--muted);text-decoration:line-through}
.stop{border:1px solid var(--line);border-radius:12px;margin:10px 0;
overflow:hidden;background:var(--panel)}
.stop>summary{padding:12px 14px;font-weight:700;cursor:pointer;
display:flex;justify-content:space-between;gap:10px;align-items:baseline}
.stop>summary::-webkit-details-marker{display:none}
.stop .tid{font-size:.8rem;color:var(--muted);font-weight:400;white-space:nowrap}
.stop .krop{padding:0 14px 12px}
.stop .hvor{color:var(--muted);font-size:.85rem;margin:0 0 8px}
details.ord{border:1px solid var(--line);border-radius:12px;margin:14px 0;
background:var(--panel2)}
details.ord>summary{padding:12px 14px;font-weight:700;cursor:pointer;
font-size:.95rem}
table.ord{width:100%;border-collapse:collapse;font-size:.92rem}
table.ord td{border-top:1px solid var(--line);padding:7px 14px}
table.ord td:first-child{width:46%}
ul.regler{padding-left:20px;margin:8px 0}
ul.regler li{margin:7px 0;font-size:.93rem;color:var(--muted)}
.dag{background:#eaf7f0;border:1px solid #bfe6d2;border-radius:12px;
padding:12px 14px;margin:12px 0;font-size:.97rem}
.dag div+div{margin-top:5px}
.dag b{display:inline-block;min-width:52px;color:var(--good)}
p.vink{color:var(--muted);font-size:.93rem;margin:8px 0}
p.gang{color:var(--muted);font-size:.86rem;margin:6px 0 10px;padding-left:4px}
.kort{border:1px solid var(--line);border-radius:12px;padding:8px;
margin:10px 0;background:#f7f9fc}
.kort svg{max-width:100%;height:auto;display:block}
.kort .da{color:var(--muted);font-size:.85rem;margin:8px 4px 2px}
.figurboks{padding:6px 12px 12px}
.figurboks svg{max-width:100%;height:auto}
.figurboks .da{color:var(--muted);font-size:.86rem;margin:6px 0 0}
.retur{display:block;text-align:center;margin:26px 0 0;font-size:.92rem}
.nulstil{background:none;border:0;color:var(--muted);font-size:.85rem;
text-decoration:underline;padding:8px;font-family:inherit;cursor:pointer}
'''

GRUPPE_JS = '''
(function(){
  var n = document.body.dataset.gruppe, k = 'sturmflut-g' + n;
  var gemt = {};
  try { gemt = JSON.parse(localStorage.getItem(k) || '{}'); } catch (e) {}
  var bokse = document.querySelectorAll('input[type=checkbox]');
  bokse.forEach(function(b){
    if (gemt[b.id]) b.checked = true;
    b.addEventListener('change', function(){
      gemt[b.id] = b.checked;
      try { localStorage.setItem(k, JSON.stringify(gemt)); } catch (e) {}
    });
  });
  var knap = document.getElementById('nulstil');
  if (knap) knap.addEventListener('click', function(){
    bokse.forEach(function(b){ b.checked = false; });
    try { localStorage.removeItem(k); } catch (e) {}
  });
})();
'''


def gruppeside(nr, g):
    navn_de, navn_da, tekst_de, tekst_da, opgaver = g
    d = DAGSREGNSKAB[nr]
    orden = RAEKKEFOELGE[nr]
    start_navn = STOP[orden[0] - 1][1]
    slut_navn = STOP[orden[-1] - 1][1]
    fotos = ''.join(
        f'<label class="p"><input type="checkbox" id="f{j}">'
        f'<span>{esc(de)}</span></label>'
        for j, (de, _) in enumerate(opgaver, 1))
    stop = ''
    for plads, sted_nr in enumerate(orden, 1):
        m, snavn, hvor, _, opg = STOP[sted_nr - 1]
        punkter = ''.join(
            f'<label class="p"><input type="checkbox" id="s{sted_nr}o{j}">'
            f'<span>{esc(de)}</span></label>'
            for j, (de, _) in enumerate(opg, 1))
        stop += (f'<details class="stop"><summary>'
                 f'<span>{plads}. {esc(snavn)}</span>'
                 f'<span class="tid">ca. {m} min</span></summary>'
                 f'<div class="krop"><p class="hvor">{esc(hvor)}</p>'
                 f'{punkter}</div></details>')
        if plads < len(orden):
            naeste = STOP[orden[plads] - 1][1]
            meter = afstand(sted_nr, orden[plads])
            stop += (f'<p class="gang">↓ ca. {meter} m til {esc(naeste)} — '
                     f'{round(meter / TEMPO)} min at gå</p>')
    if d['hjem_m']:
        stop += (f'<p class="gang">↓ ca. {d["hjem_m"]} m tilbage til '
                 f'mødestedet — {d["hjem"]} min at gå</p>')
    else:
        stop += '<p class="gang">↓ I slutter præcis dér, hvor vi mødes.</p>'

    return f'''<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Gruppe {nr} · {esc(navn_de)}</title><style>{GRUPPE_CSS}</style></head>
<body data-gruppe="{nr}">
<header class="top"><div class="nr">Gruppe {nr} · Sturmflut in der HafenCity</div>
<h1>{esc(navn_de)}</h1></header>
<main>
<div class="dag"><div><b>{AFGANG}</b> fælles afgang fra hotellet</div>
<div><b>{OPSAMLING}</b> alle mødes ved {MOEDESTED}</div>
<div><b>Start</b> {esc(start_navn)} — jeres eget sted</div></div>
<div class="intro">{esc(tekst_de)}</div>

<details class="ord" id="snit"><summary>Querschnitt — die zwei Ebenen</summary>
<div class="figurboks">{fig_snit}
<p class="da">Promenaden ligger 4,5–5,5 m over havets middel, warften
7,5–8,3 m. De stiplede linjer er stormfloderne i 1962 (5,70 m) og 1976
(6,45 m).</p></div></details>

<h2>Eure drei Fotos</h2>
{fotos}

<h2>Eure Route — fünf Orte</h2>
<div class="kort">{FG.rutekort(PUNKTER, [0] + orden, W=560, H=390)}
<p class="da">Grøn ring: her starter I. Rød ring: her slutter I. Kortet er
skematisk — det viser afstande og retninger, ikke gader. Vandet er ikke
tegnet.</p></div>
<p class="vink">Jeres rute er jeres egen: I starter i <b>{esc(start_navn)}</b>,
og ingen anden gruppe starter samme sted. Regn med cirka
<b>{(d['ud_m'] + d['meter'] + d['hjem_m']) / 1000:.1f} km at gå</b> i løbet af
dagen — det hele på gåben, ingen ubahn. Minuttallene er et gæt, ikke en pligt.
Møder I en anden gruppe, er det helt i orden: I fotograferer alligevel hver
jeres ting.</p>
{stop}

<h2>Frokost</h2>
<p class="vink">I sørger selv for frokost, men <b>gruppen spiser sammen</b> —
regn med cirka {FROKOST} minutter. Der er mad ved Überseequartier og
Überseeboulevard, både ude og inde.</p>

{wortliste()}

<h2>Fotoregler</h2>
<ul class="regler">{''.join(f'<li>{r}</li>' for r in FOTOREGLER)}</ul>

<button class="nulstil" id="nulstil">Nulstil alle flueben</button>
<a class="retur" href="/sturmflut">Hele turen og tværsnittet →</a>
</main><script>{GRUPPE_JS}</script></body></html>'''


for nr, g in enumerate(GRUPPER, 1):
    open(f'sturmflut-gruppe{nr}.html', 'w').write(gruppeside(nr, g))


# ===================================================== 5 · forsiden for turen
BASIS = open('matematik.html').read()
GRUND = BASIS[BASIS.find('<style>') + 7:BASIS.find('</style>')]
EKSTRA = '''
.figur{background:var(--panel2);border:1px solid var(--line);border-radius:14px;
padding:14px;margin:14px 0;text-align:center}
.figur svg{max-width:100%;height:auto}
.figtekst{color:var(--muted);font-size:.9rem;margin-top:8px}
.blok{background:var(--panel);border:1px solid var(--line);
border-left:5px solid var(--accent);border-radius:14px;padding:16px 20px;
margin:12px 0;box-shadow:var(--shadow)}
.blok.advar{border-left-color:var(--bad);background:var(--bad-soft)}
.blok h3{margin:0 0 8px;font-size:1.1rem}
.blok p,.blok li{color:var(--muted);font-size:.97rem}
.blok ul{margin:6px 0 0;padding-left:20px}.blok li{margin:5px 0}
.hold{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));
gap:10px;margin:14px 0}
.hold a{display:block;border:1px solid var(--line);border-radius:14px;
padding:14px 16px;background:var(--panel);text-decoration:none;
box-shadow:var(--shadow)}
.hold a:hover{border-color:var(--accent)}
.hold .nr{background:var(--good);color:#fff;border-radius:999px;padding:2px 10px;
font-size:.78rem;font-weight:700}
.hold b{display:block;margin:8px 0 2px;color:var(--ink);font-size:1.02rem}
.hold span.da{color:var(--muted);font-size:.86rem}
.hold code{display:block;margin-top:8px;color:var(--accent);font-size:.85rem}
.stop{border:1px solid var(--line);border-radius:14px;padding:15px 18px;
margin:10px 0;background:var(--panel);box-shadow:var(--shadow)}
.stop h3{margin:0 0 2px;font-size:1.1rem;display:flex;align-items:center;
gap:10px;flex-wrap:wrap}
.stop .tid{background:var(--accent);color:#fff;border-radius:999px;
padding:2px 11px;font-size:.8rem;font-weight:700}
.stop .hvor{color:var(--muted);font-size:.86rem;text-transform:uppercase;
letter-spacing:.04em;margin:0 0 8px}
.stop p{color:var(--muted);font-size:.96rem;margin:6px 0;max-width:74ch}
.stop ol{margin:8px 0 0;padding-left:20px}
.stop li{font-size:.95rem;margin:5px 0}
details.ord{border:1px solid var(--line);border-radius:14px;margin:14px 0;
background:var(--panel2)}
details.ord>summary{padding:13px 16px;font-weight:700;cursor:pointer}
table.ord{width:100%;border-collapse:collapse;font-size:.93rem}
table.ord td{border-top:1px solid var(--line);padding:7px 16px}
table.ord td:first-child{width:44%}
.kilder{color:var(--muted);font-size:.85rem;margin-top:18px}
.kilder a{color:var(--muted)}
@media print{header.top,.printbtn{display:none!important}
.blok,.figur,.stop{box-shadow:none;break-inside:avoid}
body{font-size:10pt}main{padding:0}@page{size:A4;margin:12mm}}
'''

MEST_LUFT = max(d['luft'] for d in DAGSREGNSKAB.values())
rutetabel = ''.join(
    f'<tr><td><b>{i}</b></td><td>{esc(GRUPPER[i - 1][1])}</td>'
    f'<td>{esc(STOP[RAEKKEFOELGE[i][0] - 1][1])}</td>'
    f'<td>{" → ".join(STOP[n - 1][1].split()[0] for n in RAEKKEFOELGE[i])}</td>'
    f'<td>{DAGSREGNSKAB[i]["ud_m"]} m</td>'
    f'<td>{(DAGSREGNSKAB[i]["ud_m"] + DAGSREGNSKAB[i]["meter"] + DAGSREGNSKAB[i]["hjem_m"]) / 1000:.1f} km'
    f'</td></tr>'
    for i in range(1, 6))

hold_html = ''.join(
    f'<a href="/sturmflut/{i}"><span class="nr">Gruppe {i}</span>'
    f'<b>{esc(de)}</b><span class="da">{esc(da)}</span>'
    f'<code>mibelibsen.space/sturmflut/{i}</code></a>'
    for i, (de, da, *_ ) in enumerate(GRUPPER, 1))

stop_html = ''.join(
    f'''<article class="stop"><h3><span class="tid">{m} min</span>
{i}. {esc(navn)}</h3><p class="hvor">{esc(hvor)}</p><p>{esc(hvad)}</p>
<ol>{''.join(f'<li>{esc(de)}</li>' for de, _ in opg)}</ol></article>'''
    for i, (m, navn, hvor, hvad, opg) in enumerate(STOP, 1))

KROP = f'''<section class="hero"><span class="pill">Studietur Hamborg</span>
<h1>Sturmflut: at bygge og bo uden for diget</h1>
<p>Fire timer i HafenCity med frokost. <b>Opgaverne står på tysk</b> — I skal
oversætte dem for at kunne løse dem. Ordlisten nederst giver jer de ord, man
ikke kan gætte sig til; resten må I selv slå op.</p>
<p>Hver gruppe har sin egen side med sine opgaver og flueben, der bliver
gemt i telefonen:</p>
<div class="hold">{hold_html}</div>
<button class="printbtn" onclick="window.print()">Print siden</button></section>

<div class="figur">{fig_snit}
<div class="figtekst">De to niveauer, og to rigtige stormfloder tegnet ind.
1976 stod <b>højere</b> end 1962 — men da holdt digerne. Begge ville have
oversvømmet promenaden. Ingen af dem ville have nået op på warften.</div></div>

<div class="blok"><h3>Det, turen handler om</h3>
<p>I 1962 nåede vandet 5,70 m ved Pegel St. Pauli. Digerne brød sammen 60
steder, og over 300 mennesker døde i Hamborg. I 1976 stod vandet 6,45 m —
højere end i 1962 — men da holdt digerne.</p>
<p>HafenCity er bygget efter den erfaring, men på en anden måde: ikke bag et
dige, men <b>oven på</b> byen. Gader og huse ligger 7,5–8,5 meter over havets
middel. Promenaderne ligger nede på de gamle kajers niveau og bliver lukket
af, når der varsles. Spørgsmålet, I skal tage stilling til undervejs:
<i>er det klogt at bygge sådan — eller er det at flytte problemet?</i></p></div>

<h2 class="sec">Dagen</h2>
<div class="blok"><h3>{AFGANG} fælles afgang · {OPSAMLING} fælles opsamling</h3>
<p>De fem grupper tager af sted samtidig, men går <b>hver for sig</b>. Hver
gruppe bestemmer selv rækkefølgen af de fem steder og hvor længe den bliver.
To grupper kan sagtens ende foran det samme motiv — de fotograferer alligevel
hver deres emne.</p>
<p><b>Mødested {OPSAMLING}:</b> {MOEDESTED}. Valgt fordi {MOEDE_HVORFOR}.</p>
<p><b>Frokost:</b> grupperne sørger selv for den, men <b>spiser sammen</b>, og
lægger den, hvor det passer i deres egen rute. Regn med cirka {FROKOST}
minutter.</p>
<p><b>Sendt på tværs:</b> de fem grupper starter fem forskellige
steder og går ruten i hver sin rækkefølge. De står derfor ikke i kø ved det
samme motiv, de ser stederne i forskelligt lys og forskellig rækkefølge — og
to grupper med samme emne kommer hjem med forskellige billeder.</p>
<p><b>Alt går til fods.</b> Hver rute slutter ved mødestedet eller lige ved
siden af, så ingen skal nå tværs gennem HafenCity klokken {OPSAMLING}.</p>
</div>

<table class="t"><thead><tr><th>Gruppe</th><th>Emne</th><th>Starter i</th>
<th>Rækkefølge</th><th>Ud dertil</th><th>Til fods i alt</th></tr></thead>
<tbody>
{rutetabel}</tbody></table>

<div class="blok"><h3>Regner det sammen?</h3>
<p><b>Hele dagen foregår til fods</b> — ingen ubahn, ingen bus. Fra
{AFGANG} til {OPSAMLING} er der {RAADIGHED} minutter: gang fra hotellet ud
til gruppens eget startsted (11–25 minutter), de fem steder cirka {I_ALT}
minutter, frokost {FROKOST}, og resten gang mellem stederne.</p>
<p>Grupperne går mellem <b>4,2 og 6,5 km</b> i løbet af dagen. De to,
der starter østligst, slipper billigst, fordi hotellet ligger i den ende.
Hver gruppes rækkefølge er den korteste vej, der når alle fem steder og
slutter ved mødestedet — fundet ved at regne alle 120 muligheder igennem.
Afstandene er fugleflugt mellem koordinater fra OpenStreetMap gange 1,3,
rundet til nærmeste 50 meter.</p>
<p>Den strammeste rute har <b>{LUFT} minutters luft</b>, den rummeligste
{MEST_LUFT}. Alle afstande er regnet fra koordinater — også fra
{HOTEL}.</p></div>

<h2 class="sec">Kortet</h2>
<div class="figur">{fig_kort}
<div class="figtekst">De fem steder i korrekt indbyrdes afstand — tegnet af
koordinater fra OpenStreetMap. Kortet viser afstande og retninger, ikke
gader; vandet er ikke tegnet. Hver gruppe har det samme kort med sin egen
rute på sin egen side.</div></div>

<h2 class="sec">De fem steder</h2>
<p>Rækkefølgen herunder går fra vest mod øst. Alle steder er gratis.</p>
<div class="figur">{fig_rute}
<div class="figtekst">Forslag til rækkefølge — ikke et skema. Minuttallene er
et gæt på, hvor længe man skal bruge, ikke en pligt.</div></div>

{stop_html}

<h2 class="sec">Ordliste</h2>
{wortliste(aaben=True)}

<h2 class="sec">Fotoregler</h2>
<div class="blok"><ul>{''.join(f'<li>{r}</li>' for r in FOTOREGLER)}</ul></div>

<h2 class="sec">Praktisk</h2>
<div class="blok advar"><ul>{''.join(f'<li>{esc(s)}</li>' for s in SIKKERHED)}
</ul></div>

<div class="kilder">Tal og åbningstider er slået efter 30. september 2026:
warfternes højde og promenadernes niveau hos
<a href="https://www.db-bauzeitung.de/schwerpunkt/auf-sand-gebaut/">db
Bauzeitung</a> og
<a href="https://de.wikipedia.org/wiki/Hamburg-HafenCity">Wikipedia</a>,
vandstandene i 1962 og 1976 hos
<a href="https://de.wikipedia.org/wiki/Sturmflut_1962">Wikipedia</a>, og
åbningstider og gratis adgang hos
<a href="https://www.hafencity.com/forum">HafenCity Hamburg</a>.</div>
'''


def side(titel, krop):
    return ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{titel}</title><style>' + GRUND + EKSTRA +
            '</style></head><body><header class="top"><div class="top-inner">'
            '<a class="brand" href="index.html">Mibelibsen <span>9. klasse</span></a>'
            '<nav class="tabs"><a class="" href="tysk.html">Tysk</a></nav>'
            '</div></header><main>' + krop + '</main><footer>'
            'Studietur Hamborg · 9. klasse · Mibelibsen.'
            '</footer></body></html>')


open('sturmflut.html', 'w').write(side('Sturmflut · HafenCity', KROP))

# ===================================================== 6 · dansk udgave
DOK_CSS = '''
:root{--ink:#1a2233;--muted:#586074;--line:#c9d2e0;--panel:#f4f6fb;
--accent:#1f6fd6}
*{box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,
Arial,sans-serif;color:var(--ink);margin:0;font-size:10.2pt;line-height:1.45}
h1{font-size:18pt;margin:0 0 4px}
h2{font-size:12.5pt;margin:16px 0 5px;padding-bottom:3px;
border-bottom:2px solid var(--accent)}
h3{font-size:11pt;margin:12px 0 3px}
p{margin:5px 0;max-width:80ch}p.und{color:var(--muted)}
table{width:100%;border-collapse:collapse;margin:6px 0 10px;font-size:9.4pt;
table-layout:fixed}
th,td{border:1px solid var(--line);padding:5px 7px;text-align:left;
vertical-align:top;word-wrap:break-word}
th{background:var(--panel);font-size:8.6pt;color:var(--muted);
text-transform:uppercase;letter-spacing:.03em}
td.de{background:#fbfcfe}
@page{size:A4;margin:13mm}
@media print{table,h2,h3{page-break-inside:avoid}h2,h3{page-break-after:avoid}}
'''

dok = ['<h1>Sturmflut i HafenCity · dansk udgave</h1>',
       '<p class="und">Opgaverne, ungerne får, står på tysk. Her står de med '
       'dansk oversættelse ved siden af. Siderne: '
       'mibelibsen.space/sturmflut og /sturmflut/1 til /sturmflut/5.</p>',
       f'<p class="und"><b>{AFGANG}</b> fælles afgang fra hotellet · '
       f'<b>{OPSAMLING}</b> alle mødes ved {MOEDESTED}. De fem grupper går '
       'hver for sig og bestemmer selv rækkefølgen. Frokosten sørger de selv '
       'for, men gruppen spiser sammen. Alle steder er gratis.</p>',
       f'<p class="und">Regnestykket: {RAADIGHED} minutter til rådighed. '
       f'Alle afstande er regnet fra koordinater, også fra {HOTEL}. '
       f'De fem steder ca. {I_ALT} min, frokost {FROKOST} min, resten gang. '
       'Grupperne går 4,2–6,5 km i løbet af dagen — de østligste startsteder '
       f'slipper billigst. Strammeste luft {LUFT} min, rummeligste '
       f'{MEST_LUFT} min. Alt til fods — ingen ubahn og ingen bus.</p>',
       '<h2>Hvem starter hvor</h2>',
       '<table><thead><tr><th>Gruppe</th><th>Emne</th><th>Starter i</th>'
       '<th>Rækkefølge</th><th>Gang i alt</th></tr>'
       '</thead><tbody>' + ''.join(
           f'<tr><td>{i}</td><td>{esc(GRUPPER[i - 1][1])}</td>'
           f'<td>{esc(STOP[RAEKKEFOELGE[i][0] - 1][1])}</td>'
           f'<td>{" → ".join(str(x) for x in RAEKKEFOELGE[i])}</td>'
           f'<td>{DAGSREGNSKAB[i]["meter"] + DAGSREGNSKAB[i]["hjem_m"]} m</td>'
           f'</tr>' for i in range(1, 6)) +
       '</tbody></table>',
       '<h2>De fem steder</h2>']
for i, (m, navn, hvor, hvad, opg) in enumerate(STOP, 1):
    dok.append(f'<h3>{i}. {esc(navn)} · {m} min</h3>')
    dok.append(f'<p class="und">{esc(hvor)} — {esc(hvad)}</p>')
    dok.append('<table><thead><tr><th>Opgaven på tysk</th>'
               '<th>På dansk</th></tr></thead><tbody>' +
               ''.join(f'<tr><td class="de">{esc(de)}</td><td>{esc(da)}</td></tr>'
                       for de, da in opg) + '</tbody></table>')
dok.append('<h2>Grupperne</h2>')
for i, (de, da, t_de, t_da, opg) in enumerate(GRUPPER, 1):
    dok.append(f'<h3>Gruppe {i} · {esc(de)} — {esc(da)}</h3>')
    dok.append(f'<p class="und">{esc(t_da)}</p>')
    dok.append('<table><thead><tr><th>Billedet på tysk</th>'
               '<th>På dansk</th></tr></thead><tbody>' +
               ''.join(f'<tr><td class="de">{esc(b_de)}</td><td>{esc(b_da)}</td></tr>'
                       for b_de, b_da in opg) + '</tbody></table>')
dok.append('<h2>Ordliste, ungerne får forærende</h2>')
dok.append('<table><tbody>' + WORT_HTML + '</tbody></table>')
dok.append('<h2>Fotoregler og praktisk</h2>')
dok.append('<ul>' + ''.join(f'<li>{r}</li>' for r in FOTOREGLER) +
           ''.join(f'<li>{esc(x)}</li>' for x in SIKKERHED) + '</ul>')

open(os.path.join(SCRATCH, 'sturmflut-dansk.html'), 'w').write(
    '<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
    '<title>Sturmflut · dansk udgave</title>'
    f'<style>{DOK_CSS}</style></head><body>' + '\n'.join(dok) + '</body></html>')

print('skrevet:  sturmflut.html')
for nr in range(1, len(GRUPPER) + 1):
    print(f'skrevet:  sturmflut-gruppe{nr}.html   → /sturmflut/{nr}')
print(f'skrevet:  {SCRATCH}/sturmflut-dansk.html')
print(f'turen:    {len(STOP)} steder · {I_ALT} min på stederne · '
      f'{len(GRUPPER)} grupper · {len(WORTLISTE)} ord i ordlisten')
for _nr, _d in DAGSREGNSKAB.items():
    _rute = ' → '.join(STOP[n - 1][1].split()[0] for n in RAEKKEFOELGE[_nr])
    print(f'  gruppe {_nr}: {_rute}  '
          f'{(_d["ud_m"] + _d["meter"] + _d["hjem_m"]) / 1000:.1f} km · '
          f'{_d["luft"]} min luft')
