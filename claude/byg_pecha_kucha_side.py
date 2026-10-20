# -*- coding: utf-8 -*-
"""Bygger pecha-kucha.html — vejledningen til ungerne.

Siden hoerer sammen med materiale/pecha-kucha-skabelon.pptx, som bygges af
claude/byg_pecha_kucha.py. Skabelonen ligger i materiale/, saa den udgives og
kan hentes direkte fra siden her.

Formen er ikke et fag, saa siden ligger i roden og er linket fra forsiden.

    python3 claude/byg_pecha_kucha_side.py
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figurer as FG

UD = 'pecha-kucha.html'
SKABELON = 'materiale/pecha-kucha-skabelon.pptx'
assert os.path.exists(SKABELON), (
    f'{SKABELON} mangler — kør claude/byg_pecha_kucha.py først')

SLIDES, SEK = 20, 20
ORD_PR_SLIDE = round(140 / 60 * SEK)      # ca. 140 ord i minuttet

# Et eksempel paa en fordeling i en gruppe paa tre.
GRUPPE = [('Første taler', 7), ('Anden taler', 7), ('Tredje taler', 6)]

# Oeveloekken. Det er den, der goer forskellen, og den er ikke til at se.
OEVE = [
    ('Skriv', 'hvad du vil sige'),
    ('Læs højt', 'med et ur i hånden'),
    ('Skær væk', 'det, der ikke nåede med'),
    ('Igen', 'til det passer hver gang'),
]

AFSNIT = [
 ('Reglen er hele pointen',
  ['En Pecha Kucha er <b>20 slides, der hver står præcis 20 sekunder</b> og '
   'skifter af sig selv. Det giver 6 minutter og 40 sekunder. Hver gang.',
   'Formen blev opfundet på et arkitektkontor i Tokyo i 2003, fordi de var '
   'trætte af oplæg, der trak ud. Navnet er japansk og betyder noget i '
   'retning af "snakkesnak".',
   'Det, der gør den svær, er også det, der gør den god: du kan ikke tale '
   'over tiden, du kan ikke stoppe op og lede efter noget, og du kan ikke '
   'stå og læse op af dit eget slide. <b>Slidet venter ikke på dig.</b>'],
  FG.slidebaand(SLIDES, SEK),
  'Alle felter er lige brede, fordi alle slides varer lige længe. Du kan '
  'ikke give ét slide mere tid ved at tage fra et andet.'),

 ('Billeder på slidesene, ord i munden',
  ['Der er ingen tekstfelter i skabelonen. Det er med vilje. Et slide i en '
   'Pecha Kucha er <b>ét billede</b> — og så siger du resten.',
   'Grunden er praktisk: hvis der står noget på slidet, læser publikum det i '
   'stedet for at høre på dig. Og du begynder selv at læse op. Så står I to '
   'steder i lokalet og læser den samme tekst.',
   f'Skal der endelig et tal med, så ét stort tal. Ikke en tabel.',
   f'<b>20 sekunder er omkring {ORD_PR_SLIDE} ord.</b> Det er mindre, end '
   'du tror — cirka fire linjer. Skriv dem i noterne under slidet; de står '
   'der allerede i skabelonen, sammen med ordantallet.'],
  None, None),

 ('Sådan deler I den i en gruppe',
  ['<b>Del slidesene, ikke emnerne.</b> Er I tre, tager én slide 1–7, den '
   'næste 8–14 og den sidste 15–20. I taler i rækkefølge, og I skifter kun '
   'taler <b>mellem</b> to slides.',
   'Deler I i stedet efter emne, ender I med at skulle skifte taler midt i '
   'et slide — og det går galt, for slidet skifter alligevel.',
   'Aftal på forhånd, hvem der starter afspilningen, og hvor I står, mens I '
   'venter. Det lyder som en detalje. Det er det ikke, når der er 20 '
   'sekunder til at finde ud af det i.'],
  FG.slidebaand(SLIDES, SEK, GRUPPE),
  'En gruppe på tre. Taleren skifter kun mellem to slides, aldrig midt i et. '
  'Er I fire, bliver det 5 slides hver.'),

 ('Øvning er ikke noget, I gør til sidst',
  ['Første gennemløb går galt. Det gør det for alle. Du er ikke færdig med '
   'at sige det, du ville, når slidet skifter.',
   'Når det sker, er der kun én rigtig løsning: <b>skær ord væk</b>. Ikke '
   'tal hurtigere. En Pecha Kucha, der bliver læst op i hast, er værre end '
   'en almindelig fremlæggelse.',
   'Regn med fire-fem gennemløb med et ur. Det er her, formen lærer jer '
   'noget: I opdager selv, hvad der var overflødigt.'],
  FG.kredsloeb(OEVE, ('Fire-fem gange', 'så sidder den')),
  'Løkken, I skal igennem for hvert slide. Den tredje gang er den, der '
  'rykker — dér begynder I at kunne høre, hvad der kan undværes.'),
]

FAELDER = [
 ('At skrive manuskriptet til sidst',
  'Billedet skal vælges ud fra, hvad du siger — ikke omvendt. Skriv først.'),
 ('At øve uden ur',
  'Uden ur ved du ikke, om du er på 20 eller 35 sekunder. Du tror, du er på 20.'),
 ('At tale hurtigere, når tiden er knap',
  'Det kan publikum høre med det samme. Skær i stedet et par sætninger væk.'),
 ('At lave et slide, der skal forklares',
  'Et kompliceret billede koster tid, du ikke har. Vælg et, der kan fanges '
  'på et sekund.'),
 ('At regne med at kunne klikke sig frem',
  'Det kan du ikke. Tiden løber, uanset hvad du gør.'),
]

TJEK = [
 'Alle 20 slides har et billede.',
 'Der står ingen sætninger på slidesene.',
 'Manuskriptet står i noterne, og det er læst højt med ur.',
 'I ved hver især, hvilke slidenumre der er jeres.',
 'I har kørt hele fremlæggelsen igennem mindst to gange i træk uden at stoppe.',
 'I ved, hvem der trykker start.',
]

afsnit_html = ''
for i, (o, stykker, figur, figtekst) in enumerate(AFSNIT, 1):
    afsnit_html += (f'<section class="afsnit"><h2><span class="num">{i}</span>'
                    f'{html.escape(o)}</h2>')
    afsnit_html += ''.join(f'<p>{t}</p>' for t in stykker)
    if figur:
        afsnit_html += (f'<div class="figur">{figur}'
                        f'<div class="figtekst">{html.escape(figtekst)}</div>'
                        f'</div>')
    afsnit_html += '</section>'

faelder_html = ''.join(
    f'<tr><th>{html.escape(a)}</th><td>{html.escape(b)}</td></tr>'
    for a, b in FAELDER)
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
table.liste th{background:var(--panel2);width:34%}
table.liste thead th{width:auto}
.hent{background:var(--accent-soft);border:1px solid var(--line);
border-left:4px solid var(--accent);border-radius:12px;padding:16px 20px;
margin:18px 0}
.hent p{margin:0 0 10px;color:var(--ink);font-size:.97rem;max-width:74ch}
ul.tjek{list-style:none;padding:0;margin:12px 0;max-width:74ch}
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
.afsnit,.figur{box-shadow:none;break-inside:avoid;page-break-inside:avoid}
body{font-size:11pt}main{padding:0}@page{size:A4;margin:14mm}}
'''

KROP = f'''<section class="hero">
<span class="pill">Fremlæggelse · metode</span>
<h1>Pecha Kucha</h1>
<p>{SLIDES} slides. {SEK} sekunder hver. De skifter af sig selv, og de venter
ikke på dig. Her er, hvad formen går ud på, og hvordan I griber den an som
gruppe.</p>
<button class="printbtn" onclick="window.print()">Print siden</button>
<a class="btnlink ghost" href="index.html">Tilbage til forsiden</a>
</section>
{afsnit_html}
<h2 class="sec">Hent skabelonen</h2>
<div class="hent">
<p><b>{SLIDES} tomme slides med tiden sat.</b> Sæt jeres billeder ind, skriv
manuskriptet i noterne, og lad være med at røre ved tiden. Hvert slide har
allerede et ordantal i noten.</p>
<a class="btnlink" href="{SKABELON}" download>Hent skabelonen (.pptx)</a>
</div>
<p style="color:var(--muted);max-width:74ch;font-size:.93rem">To ting, I skal
vide om filen: klik er slået fra, så et uheldigt tryk ikke spoler frem midt i
en fremlæggelse. Og tjek under <b>Diasshow</b>, at <b>Brug tidsindstillinger</b>
er slået til — ellers kører tiden ikke af sig selv.</p>
<h2 class="sec">Fem fælder</h2>
<table class="liste"><thead><tr><th>Fælden</th><th>Hvorfor den koster</th>
</tr></thead><tbody>{faelder_html}</tbody></table>
<h2 class="sec">Tjek før I går op</h2>
<ul class="tjek">{tjek_html}</ul>
<button class="printbtn" onclick="window.print()">Print siden</button>'''

DOK = ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
       '<meta name="viewport" content="width=device-width,initial-scale=1">'
       '<title>Pecha Kucha · 9. klasse</title><style>' + CSS +
       '</style></head><body><header class="top"><div class="top-inner">'
       '<a class="brand" href="index.html">Mibelibsen <span>9. klasse</span></a>'
       '<nav class="tabs"><a class="" href="matematik.html">Matematik</a>'
       '<a class="" href="samfundsfag.html">Samfundsfag</a>'
       '<a class="" href="tysk.html">Tysk</a><a class="" href="fysik.html">Fysik</a>'
       '</nav></div></header><main>' + KROP + '</main><footer>'
       'Undervisningsmateriale · 9. klasse · Mibelibsen.</footer></body></html>')

open(UD, 'w', encoding='utf-8').write(DOK)
print(f'skrevet:  {UD}  ·  {len(AFSNIT)} afsnit, '
      f'{sum(1 for a in AFSNIT if a[2])} figurer, {len(TJEK)} tjekpunkter')
