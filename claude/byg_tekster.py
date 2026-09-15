# -*- coding: utf-8 -*-
"""Bygger samfundsfag-tekster.html — oversigt over klassens tekster.

En tekst tilfoejes ved at skrive en linje mere i TEKSTER. Forsidebilledet
laves med:  pdftoppm -jpeg -r 42 -f 1 -l 1 tekster/<fil>.pdf tekster/<navn>
"""
import os, html

UD = 'samfundsfag-tekster.html'

# (fil, titel, kilde, dato, sider, forloeb, beskrivelse)
TEKSTER = [
 ('lovprocessen-i-danmark',
  'Den demokratiske beslutningsproces i Danmark',
  'Oversigt lavet til klassen', '', 1, 'Politiske processer · uge 32-39',
  'Vejen fra idé til gældende lov, trin for trin: lovforberedelse i '
  'ministeriet, høring, høringsnotat, fremsættelse med L-nummer, og de tre '
  'behandlinger i Folketinget med udvalgsarbejde imellem. Brug den som '
  'opslag, når et konkret lovforslag skal følges.'),
 ('big-tech-debatindlaeg-politiken',
  'Tech-ekspert: Big Tech tjener nu magthaverne før brugerne',
  'Debatindlæg af Aaron Zamost i Politiken', '9. december 2025', 5,
  'Politik og teknologi · uge 32-39',
  'En tidligere YouTube-ansat skriver, at Silicon Valley er gået fra at '
  'kæmpe mod magthaverne til at tjene dem. Teksten er et debatindlæg — den '
  'argumenterer for en holdning. Læs den også som kilde: hvem skriver, '
  'hvorfra, og hvad vil afsenderen have dig til at mene?'),
 ('alkoholpolitik-guide',
  'Kom godt i gang med en alkoholpolitik',
  'Fra guiden "Få en alkoholpolitik" til ledelse og bestyrelse i foreninger',
  '', 1, 'Socialisering',
  'Om hvordan foreningslivet er med til at forme unges normer og vaner, og '
  'hvorfor voksne i en forening er rollemodeller. Konkrete tal om unge og '
  'alkohol. Brugbar til socialisering: hvem opdrager på hvem, og hvordan '
  'normer bliver til.'),
]

kort = []
for fil, titel, kilde, dato, sider, forloeb, tekst in TEKSTER:
    pdf, jpg = f'tekster/{fil}.pdf', f'tekster/{fil}-forside.jpg'
    for sti in (pdf, jpg):
        assert os.path.exists(sti), f'mangler: {sti}'
    meta = ' · '.join(x for x in (kilde, dato,
                                  f'{sider} side' + ('r' if sider > 1 else '')) if x)
    kort.append(
        f'<article class="tekst"><a class="forside" href="{pdf}" target="_blank" '
        f'rel="noopener"><img src="{jpg}" alt="Forsiden af {html.escape(titel)}" '
        f'loading="lazy"></a><div class="krop">'
        f'<span class="emne">{html.escape(forloeb)}</span>'
        f'<h3>{html.escape(titel)}</h3>'
        f'<p class="kilde">{html.escape(meta)}</p>'
        f'<p>{html.escape(tekst)}</p>'
        f'<a class="btnlink" href="{pdf}" target="_blank" rel="noopener">'
        f'Åbn teksten</a></div></article>')

BASIS = open('samfundsfag.html').read()
CSS = BASIS[BASIS.find('<style>') + 7:BASIS.find('</style>')]
CSS += '''
.tekst{display:flex;gap:20px;background:var(--panel);border:1px solid var(--line);
border-radius:16px;padding:20px;box-shadow:var(--shadow);margin:16px 0}
.tekst .forside{flex:0 0 132px;display:block;border:1px solid var(--line);
border-radius:8px;overflow:hidden;background:#fff;align-self:flex-start}
.tekst .forside img{display:block;width:132px;height:auto}
.tekst .forside:hover{border-color:var(--accent)}
.tekst .krop{flex:1;min-width:0}
.tekst h3{margin:6px 0 4px;font-size:1.22rem}
.tekst p{margin:8px 0;color:var(--muted);font-size:.95rem}
.tekst p.kilde{color:var(--ink);font-size:.88rem;margin:0}
.emne{display:inline-block;font-size:.72rem;letter-spacing:.5px;text-transform:uppercase;
font-weight:700;color:var(--accent);background:var(--accent-soft);
border-radius:999px;padding:3px 10px}
@media(max-width:620px){.tekst{flex-direction:column}.tekst .forside img{width:100%}
.tekst .forside{flex:none;max-width:200px}}
@media print{.tekst{box-shadow:none;break-inside:avoid}}
'''

KROP = ('<section class="hero"><span class="pill">Samfundsfag · Tekster</span>'
        '<h1>Tekster</h1><p>Teksterne til forløbene. Klik på forsiden eller på '
        'knappen for at åbne teksten som PDF — den kan læses på telefonen og '
        'printes.</p>'
        '<a class="btnlink ghost" href="samfundsfag.html">Tilbage til samfundsfag</a>'
        '<a class="btnlink ghost" href="aarsplan-samfundsfag.html">Årsplanen</a>'
        '</section>' + ''.join(kort))

DOK = ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
       '<meta name="viewport" content="width=device-width,initial-scale=1">'
       '<title>Tekster · samfundsfag · 9. klasse</title><style>' + CSS +
       '</style></head><body><header class="top"><div class="top-inner">'
       '<a class="brand" href="index.html">Mibelibsen <span>9. klasse</span></a>'
       '<nav class="tabs"><a class="" href="matematik.html">Matematik</a>'
       '<a class="active" href="samfundsfag.html">Samfundsfag</a>'
       '<a class="" href="tysk.html">Tysk</a><span class="soon">Fysik</span>'
       '</nav></div></header><main>' + KROP + '</main><footer>'
       'Undervisningsmateriale · 9. klasse · Mibelibsen. Teksterne tilhører '
       'deres ophavsmænd og ligger her til brug i undervisningen.'
       '</footer></body></html>')
open(UD, 'w').write(DOK)
print(f'skrevet:  {UD}  ·  {len(TEKSTER)} tekster')
