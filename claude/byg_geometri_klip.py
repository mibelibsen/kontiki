# -*- coding: utf-8 -*-
"""Bygger geometri-klip.html - én flise til alle klippearkene.

Arkene laa som fire kort paa matematik.html og fyldte halvdelen af siden.
De hoerer sammen: samme greb, samme format, samme saks. Derfor ét kort,
der hedder **Geometri klip**, og en side bagved med dem alle fire.

Miniaturerne er **de rigtige figurer** fra byggescripterne, ikke tegninger
lavet til lejligheden. Modulerne importeres, figuren hentes, og mm-maalene
i <svg>-taggen fjernes, saa den kan skalere paa en skaerm. Aendrer et ark
sig, aendrer billedet sig med - de kan ikke komme til at vise hver sit.

    python3 claude/byg_geometri_klip.py
"""
import html
import importlib.util
import os
import re

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HER = os.path.dirname(os.path.abspath(__file__))
UD = os.path.join(ROD, 'geometri-klip.html')


def _hent(navn):
    sti = os.path.join(HER, navn + '.py')
    spec = importlib.util.spec_from_file_location(navn, sti)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


AREAL = _hent('byg_klip_areal')
RUMFANG = _hent('byg_klip_rumfang')
OVERFLADE = _hent('byg_klip_overflade')
PYTHAGORAS = _hent('byg_klip_pythagoras')


def mini(s, h=150):
    """Samme figur, men i skaermstoerrelse. mm-maalene ryger ud, viewBox'en
    bliver staaende - saa er forholdet mellem siderne stadig det rigtige."""
    ny, n = re.subn(r'<svg width="[^"]*" height="[^"]*"',
                    f'<svg preserveAspectRatio="xMidYMid meet" '
                    f'style="width:100%;height:{h}px"', s, count=1)
    assert n == 1, 'figuren havde ikke de mm-mål, der skulle fjernes'
    return ny


# (filnavn, titel, hvad det handler om, [hvad man finder], [hvad der skal
#  bruges], figur)
ARK = [
 ('materiale/klip-arealet-fri.pdf', 'Klip arealet fri',
  'Tre arealformler, klippet frem i stedet for forklaret: parallelogrammet '
  'bliver til et rektangel, to trekanter bliver til et parallelogram, og '
  'cirklen bliver til noget, der næsten er et rektangel.',
  ['Areal af parallelogram', 'Areal af trekant', 'Areal af cirkel'],
  ['Saks', 'Lineal'],
  AREAL.klip_cirkel()),

 ('materiale/klip-rumfanget-fri.pdf', 'Klip rumfanget fri',
  'Kassen bygges og fyldes med lag af sin egen grundflade. Pyramiden har '
  'samme grundflade og samme højde — og fylder præcis en tredjedel. Det '
  'kan ikke gættes, men det kan hældes.',
  ['Rumfang af kasse', 'Rumfang af pyramide', 'Tredjedelen'],
  ['Saks', 'Lim', 'Ris eller sand'],
  RUMFANG.pyramidenet()),

 ('materiale/klip-overfladen-fri.pdf', 'Klip overfladen fri',
  'Overfladen er præcis det, der ligger fladt, når man klipper legemet op. '
  'Cylinderens krumme side viser sig at være et rektangel — og dets bredde '
  'er cirklens omkreds.',
  ['Overflade af kasse', 'Overflade af cylinder', 'Overflade af pyramide'],
  ['Saks', 'Lim', 'Kassen og pyramiden fra forrige ark'],
  OVERFLADE.cylindernet()),

 ('materiale/klip-pythagoras-fri.pdf', 'Klip Pythagoras fri',
  'Kvadratet på den lange side ligger skævt og kan ikke tælles — det skal '
  'klippes ud og lægges oven på. Bagefter lægges fire ens trekanter i den '
  'samme ramme på to måder, og så står beviset der.',
  ['De tre kvadrater', 'Hvorfor det gælder', 'De to bliver til ét'],
  ['Saks'],
  PYTHAGORAS.tre_kvadrater()),
]

for _sti, _t, *_ in ARK:
    assert os.path.exists(os.path.join(ROD, _sti)), f'{_sti} findes ikke'

ark_html = ''
for sti, titel, om, finder, kraever, figur in ARK:
    ark_html += (
        '<article class="ark">'
        f'<div class="figkasse">{mini(figur)}</div>'
        '<div class="arktekst">'
        f'<h3>{html.escape(titel)}</h3>'
        f'<p>{om}</p>'
        '<p class="finder"><b>Det klipper de frem:</b> '
        + ' · '.join(html.escape(f) for f in finder) + '</p>'
        '<p class="kraev">'
        + ''.join(f'<span class="mrk">{html.escape(k)}</span>'
                  for k in kraever) + '</p>'
        f'<a class="btnlink" href="{sti}" download>Hent arket som PDF</a>'
        '</div></article>')

BASIS = open(os.path.join(ROD, 'matematik.html'), encoding='utf-8').read()
CSS = BASIS[BASIS.find('<style>') + 7:BASIS.find('</style>')]
CSS += '''
.ark{display:grid;grid-template-columns:230px 1fr;gap:24px;align-items:start;
background:var(--panel,#fff);border:1px solid var(--line);
border-left:5px solid var(--accent);border-radius:14px;padding:20px 24px;
margin:16px 0}
.figkasse{background:#fff;border:1px solid var(--line);border-radius:10px;
padding:10px;display:flex;align-items:center;justify-content:center}
.arktekst h3{margin:0 0 8px;font-size:1.15rem}
.arktekst p{margin:8px 0;color:var(--muted);font-size:.97rem;max-width:68ch}
.finder b{color:var(--ink)}
.kraev{margin:12px 0 14px!important}
.mrk{display:inline-block;background:var(--panel2);border:1px solid var(--line);
border-radius:999px;padding:4px 11px;margin:0 6px 6px 0;font-size:.82rem;
color:var(--muted)}
.vigtigt{background:var(--panel2);border:1px solid var(--line);
border-left:5px solid #d98324;border-radius:12px;padding:14px 20px;
margin:18px 0}
.vigtigt p{margin:0;color:var(--muted);font-size:.95rem;max-width:72ch}
.vigtigt b{color:var(--ink)}
@media(max-width:700px){.ark{grid-template-columns:1fr;gap:14px}}
'''

KROP = f'''<section class="hero">
<span class="pill">Matematik · klip og fold</span>
<h1>Geometri klip</h1>
<p>Fire ark, hvor formlen ikke står nogen steder. Den bliver klippet,
foldet eller hældt frem, og først bagefter skrevet ned — med ungernes egne
ord. Arkene kan tages hver for sig, men de bygger på hinanden i den
rækkefølge, de står her.</p>
<a class="btnlink ghost" href="matematik.html">Tilbage til matematik</a>
</section>
<div class="vigtigt"><p><b>Print i rigtig størrelse.</b> Vælg 100 % i
printervinduet — ikke «tilpas til side». Figurerne er trykt i de mål, der
skal måles på, og bliver arket forminsket, passer hverken brikker, låg
eller tal.</p></div>
{ark_html}'''

DOK = ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
       '<meta name="viewport" content="width=device-width,initial-scale=1">'
       '<title>Geometri klip · 9. klasse</title><style>' + CSS
       + '</style></head><body><header class="top"><div class="top-inner">'
       '<a class="brand" href="index.html">Mibelibsen <span>9. klasse</span>'
       '</a><nav class="tabs"><a class="active" href="matematik.html">'
       'Matematik</a><a href="samfundsfag.html">Samfundsfag</a>'
       '<a href="tysk.html">Tysk</a><a href="fysik.html">Fysik</a></nav>'
       '</div></header><main>' + KROP + '</main><footer>'
       'Undervisningsmateriale · 9. klasse · Mibelibsen.</footer></body></html>')

open(UD, 'w', encoding='utf-8').write(DOK)
print(f'skrevet:  geometri-klip.html  ·  {len(ARK)} ark, '
      f'{len(ARK)} figurer hentet fra byggescripterne')
