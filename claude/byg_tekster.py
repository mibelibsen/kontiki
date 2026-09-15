# -*- coding: utf-8 -*-
"""Bygger samfundsfag-tekster.html — oversigt over klassens tekster.

To slags tekster:

  * Vores eget materiale ligger i materiale/ og er aabent for alle. Det vises
    med forside og en knap, der aabner PDF'en direkte paa sitet.
  * Tekster med begraenset rettighed ligger i tekster/, som er udelukket i
    .vercelignore. De vises kun som overskrift med et link til klassens Teams.

En tekst tilfoejes ved at skrive en linje mere i TEKSTER: giv enten `fil`
(vores eget) eller `link` (Teams) — aldrig begge.
"""
import os, html

UD = 'samfundsfag-tekster.html'

# (titel, kilde, dato, sider, forloeb, beskrivelse, link, fil)
# link: adressen i Teams, naar rettighederne er begraensede.
# fil:  vores eget materiale i materiale/, aabent for alle.
TEKSTER = [
 ('Den demokratiske beslutningsproces i Danmark',
  'Lavet til klassen', '', 1, 'Politiske processer · uge 32-39',
  'Vejen fra idé til gældende lov, trin for trin: lovforberedelse i '
  'ministeriet, høring, høringsnotat, fremsættelse med L-nummer, og de tre '
  'behandlinger i Folketinget med udvalgsarbejde imellem. Brug den som '
  'opslag, når et konkret lovforslag skal følges.',
  '', 'lovprocessen-i-danmark'),
 ('Tech-ekspert: Big Tech tjener nu magthaverne før brugerne',
  'Debatindlæg af Aaron Zamost i Politiken', '9. december 2025', 5,
  'Politik og teknologi · uge 32-39',
  'En tidligere YouTube-ansat skriver, at Silicon Valley er gået fra at '
  'kæmpe mod magthaverne til at tjene dem. Teksten er et debatindlæg — den '
  'argumenterer for en holdning. Læs den også som kilde: hvem skriver, '
  'hvorfra, og hvad vil afsenderen have dig til at mene?',
  'https://kontikiskolen.sharepoint.com/:b:/s/HavetsVogtere/'
  'IQBj5R9_wNHRS4gxHnxDoJidAc9ZLuaP3q46v3qTsIaYgxQ?e=8zbFPE', ''),
 ('Kom godt i gang med en alkoholpolitik',
  'Fra guiden "Få en alkoholpolitik" til ledelse og bestyrelse i foreninger',
  '', 1, 'Socialisering',
  'Om hvordan foreningslivet er med til at forme unges normer og vaner, og '
  'hvorfor voksne i en forening er rollemodeller. Konkrete tal om unge og '
  'alkohol. Brugbar til socialisering: hvem opdrager på hvem, og hvordan '
  'normer bliver til.',
  'https://kontikiskolen.sharepoint.com/:b:/s/HavetsVogtere/'
  'IQCKp8JvY_wGQaspX5QXULwTAYUCZqFCsn6sXJI8IYYL6-0?e=iibu2z', ''),
]

kort = []
for titel, kilde, dato, sider, forloeb, tekst, link, fil in TEKSTER:
    assert not (link and fil), f'{titel}: vælg enten link eller fil'
    meta = ' · '.join(x for x in (kilde, dato,
                                  f'{sider} side' + ('r' if sider > 1 else '')) if x)
    forside = ''
    if fil:
        pdf, jpg = f'materiale/{fil}.pdf', f'materiale/{fil}-forside.jpg'
        for sti in (pdf, jpg):
            assert os.path.exists(sti), f'mangler: {sti}'
        knap = (f'<a class="btnlink" href="{pdf}" target="_blank" rel="noopener">'
                f'Åbn teksten</a> <span class="aaben">Åben for alle</span>')
        forside = (f'<a class="forside" href="{pdf}" target="_blank" rel="noopener">'
                   f'<img src="{jpg}" alt="Forsiden af {html.escape(titel)}" '
                   f'loading="lazy"></a>')
    elif link:
        knap = (f'<a class="btnlink" href="{link}" target="_blank" rel="noopener">'
                f'Åbn teksten i Teams</a> <span class="laast">Kun for klassen</span>')
    else:
        knap = '<p class="mangler">Linket til Teams mangler endnu.</p>'
    kort.append(
        f'<article class="tekst{" med-forside" if forside else ""}">{forside}'
        f'<div class="krop"><span class="emne">{html.escape(forloeb)}</span>'
        f'<h2>{html.escape(titel)}</h2>'
        f'<p class="kilde">{html.escape(meta)}</p>'
        f'<p>{html.escape(tekst)}</p>{knap}</div></article>')

BASIS = open('samfundsfag.html').read()
CSS = BASIS[BASIS.find('<style>') + 7:BASIS.find('</style>')]
CSS += '''
.tekst{background:var(--panel);border:1px solid var(--line);border-radius:16px;
padding:22px 24px;box-shadow:var(--shadow);margin:16px 0}
.tekst.med-forside{display:flex;gap:22px;align-items:flex-start}
.tekst .forside{flex:0 0 124px;display:block;border:1px solid var(--line);
border-radius:8px;overflow:hidden;background:#fff}
.tekst .forside img{display:block;width:124px;height:auto}
.tekst .forside:hover{border-color:var(--accent)}
.tekst .krop{flex:1;min-width:0}
.aaben,.laast{display:inline-block;font-size:.78rem;font-weight:700;
border-radius:999px;padding:4px 12px;margin-left:8px;white-space:nowrap}
.aaben{background:#eaf7f0;color:var(--good);border:1px solid #bfe6d2}
.laast{background:var(--panel2);color:var(--muted);border:1px solid var(--line)}
@media(max-width:620px){.tekst.med-forside{flex-direction:column}
.tekst .forside{flex:none;max-width:180px}.tekst .forside img{width:100%}}
.tekst h2{margin:8px 0 4px;font-size:1.35rem;line-height:1.25}
.tekst p{margin:8px 0;color:var(--muted);font-size:.95rem;max-width:74ch}
.tekst p.kilde{color:var(--ink);font-size:.88rem;margin:0}
.tekst p.mangler{color:var(--warn);font-size:.88rem;font-style:italic}
.emne{display:inline-block;font-size:.72rem;letter-spacing:.5px;text-transform:uppercase;
font-weight:700;color:var(--accent);background:var(--accent-soft);
border-radius:999px;padding:3px 10px}
@media print{.tekst{box-shadow:none;break-inside:avoid}}
'''

KROP = ('<section class="hero"><span class="pill">Samfundsfag · Tekster</span>'
        '<h1>Tekster</h1><p>Teksterne til forløbene. Det, klassen selv har lavet, '
        'kan du åbne direkte her. De tekster, vi kun har begrænset ret til at '
        'dele, ligger i klassens Teams, hvor du skal være logget ind.</p>'
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
       'Undervisningsmateriale · 9. klasse · Mibelibsen. Tekster med begrænset '
       'rettighed deles kun med klassen i Teams.'
       '</footer></body></html>')
open(UD, 'w').write(DOK)
print(f'skrevet:  {UD}  ·  {len(TEKSTER)} tekster')
