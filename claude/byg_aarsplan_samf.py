# -*- coding: utf-8 -*-
"""Bygger aarsplan-samfundsfag.html ud fra laererens egen plan.

Indholdet er skrevet af efter PDF'en `Årsplan samf` og er ikke omskrevet.
Ugernes datoer beregnes med ISO-uger, saa de passer med matematikaarsplanen
(uge 33 = 10.08-14.08 2026). Ferier og OPO er hentet fra matematikaarsplanen,
saa de to planer siger det samme.
"""
import sys, os, html
from datetime import date, timedelta
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figurer as FG

UD = 'aarsplan-samfundsfag.html'


def periode(aar, fra, til=None):
    m = date.fromisocalendar(aar, fra, 1)
    f = date.fromisocalendar(aar, til or fra, 5)
    return f'{m.day:02d}.{m.month:02d} - {f.day:02d}.{f.month:02d}'


# (aar, fra-uge, til-uge, forloeb, [punkter])
TEMA1 = [
 (2026, 32, 39, 'Teknologi og global merkantil økonomi',
  ['Statistik som redskab til at forstå og forklare økonomi og sociale fænomener',
   'International politik', 'Politik og teknologi', 'Politiske processer',
   'Tværfaglighed med matematik og projekt']),
 (2026, 40, 41, 'Digital socialisering blandt unge',
  ['Studietur til Hamborg. Uddeling af spørgeskemaer til andre unge om digitale '
   'vaner og fritid', 'Dataindsamling og analyse']),
 (2026, 43, 47, 'Kriminalitet og overvågning',
  ['Kan man bekæmpe kriminalitet med overvågning?',
   'Fokus: Hvordan reagerer samfundet på lovbrud?']),
 (2026, 48, 51, 'Teknologi og velfærdsstaten',
  ['Det danske velfærdssamfund, NPM og robotterne',
   'Fokus: Hvordan påvirkes velfærdsstaten af teknologi?',
   '<b>Samfundsfagsrapport afleveres før ferien:</b> 2 sider med et selvvalgt '
   'emne. Skal indeholde en vinkel på teknologi, og ud fra den vinkel inddrage '
   'politik, økonomi og sociale forhold']),
]
TEMA2 = [
 (2027, 1, 3, 'Økonomi er magt',
  ['Samfundsøkonomi',
   'Finanslovens effekt på politik og almindelige mennesker — konkrete '
   'eksempler og privatøkonomi']),
 (2027, 8, 11, 'Den nye verdens(u)orden',
  ['Krig i Europa, Kinas teknologiske vækst og det nye USA',
   'EU og tidens omvæltningers indvirkning på danskernes hverdag — EU basis: '
   'institutioner og processer',
   'Global migration og de politiske, økonomiske og sociale konsekvenser — '
   'den danske model']),
 (2027, 13, 17, 'Politik er magt',
  ['Borgerforslag og politiske holdningsskift — nye alliancer, nye holdninger '
   'og gammel ideologi',
   'Magtudredningen og magtdefinitionerne',
   '<b>Samfundsfagsrapport om frit emne</b>, med fagets metoder og politik, '
   'økonomi og sociale forhold som pligtstof']),
 (2027, 18, 20, 'Opsamling og muligvis prøveforberedelse', []),
]

# hvor der skal skydes en ferie- eller OPO-raekke ind, og hvad der staar i den
BRUD = {
 (2026, 41): 'Uge 42 — efterårsferie',
 (2026, 51): 'Uge 52 og 53 — juleferie',
 (2027, 3): 'Uge 4, 5 og 6 — OPO, obligatorisk projektopgave. Uge 7 — vinterferie.',
 (2027, 11): 'Uge 12 — påskeferie',
 (2027, 20): 'Uge 20 — lejrskole på Bornholm',
}

FERIER = [('Uge 40', 'Studietur til Hamborg'), ('Uge 42', 'Efterårsferie'),
          ('Uge 52 - 53', 'Juleferie'),
          ('Uge 4 - 6', 'OPO — obligatorisk projektopgave'),
          ('Uge 7', 'Vinterferie'), ('Uge 12', 'Påskeferie'),
          ('Uge 20', 'Lejrskole på Bornholm — der arbejdes samfundsfagligt')]
AFLEVERINGER = [('Uge 51', 'Samfundsfagsrapport · selvvalgt emne med en vinkel '
                 'på teknologi. 2 sider. Afleveres før juleferien.'),
                ('Uge 17', 'Samfundsfagsrapport · frit emne. Fagets metoder samt '
                 'politik, økonomi og sociale forhold er pligtstof.')]


def uger(blok):
    return sum(t - f + 1 for _, f, t, _, _ in blok)


def raekker(blok):
    ud = []
    for aar, fra, til, forloeb, punkter in blok:
        nr = f'{fra}' if fra == til else f'{fra} - {til}'
        li = ''.join(f'<li>{p}</li>' for p in punkter)
        ud.append(f'<tr><td class="uge">{nr}</td>'
                  f'<td class="per">{periode(aar, fra, til)}</td>'
                  f'<td>{html.escape(forloeb)}</td>'
                  f'<td>{"<ul>" + li + "</ul>" if li else ""}</td></tr>')
        if (aar, til) in BRUD:
            ud.append(f'<tr class="break"><td colspan="4">{BRUD[(aar, til)]}</td></tr>')
    return ''.join(ud)


U1, U2 = uger(TEMA1), uger(TEMA2)
assert U1 == 19 and U2 == 15, (U1, U2)
EFTERAAR = list(range(32, 54))
FORAAR = list(range(1, 21))
linje = FG.aarslinje([
    ('Efterår 2026 · tema 1 · teknologi', EFTERAAR,
     [(32, 39, ('Teknologi og global økonomi', 'Teknologi'), 'forloeb'),
      (40, 41, ('Digital socialisering', 'Digital soc.'), 'forloeb'),
      (42, 42, ('Efterårsferie', 'Ferie'), 'ferie'),
      (43, 47, ('Kriminalitet og overvågning', 'Kriminalitet'), 'forloeb'),
      (48, 51, ('Teknologi og velfærdsstaten', 'Velfærdsstaten'), 'forloeb'),
      (52, 53, ('Juleferie', 'Jul'), 'ferie')]),
    ('Forår 2027 · tema 2 · magt', FORAAR,
     [(1, 3, 'Økonomi er magt', 'forloeb'),
      (4, 6, 'OPO', 'opo'),
      (7, 7, ('Vinterferie', 'Ferie'), 'ferie'),
      (8, 11, ('Den nye verdens(u)orden', 'Verdens(u)orden'), 'forloeb'),
      (12, 12, ('Påskeferie', 'Påske'), 'ferie'),
      (13, 17, 'Politik er magt', 'forloeb'),
      (18, 20, 'Opsamling', 'forloeb')])])
fig = FG.mini_soejler([U1, U2])

CSS = open('aarsplan-matematik.html').read()
CSS = CSS[CSS.find('<style>') + 7:CSS.find('</style>')]
CSS += ('\n.tidslinje{background:var(--panel2);border:1px solid var(--line);'
        'border-radius:14px;padding:16px 18px 10px;margin:18px 0;overflow-x:auto}'
        '\n.tidslinje svg{display:block;min-width:620px}'
        '\n@media print{.tidslinje{break-inside:avoid}}')

KROP = f'''<section class="hero"><span class="pill">Samfundsfag · Årsplan 2026/27</span>
<h1>Årsplan · samfundsfag · 9. klasse</h1>
<p>Året har to overordnede temaer. <b>Teknologi</b> fylder efteråret fra uge 32
til uge 51, {U1} uger. <b>Magt</b> fylder foråret fra uge 1 til uge 20, {U2} uger
lagt uden om OPO og ferierne. To samfundsfagsrapporter afleveres undervejs.</p>
<a class="btnlink ghost" href="samfundsfag.html">Tilbage til samfundsfag</a>
<a class="btnlink ghost" href="index.html">Fagoversigt</a></section>
<div class="tidslinje">{linje}</div>
<table class="plan"><thead><tr><th>Uge</th><th>Periode</th><th>Forløb</th>
<th>Indhold</th></tr></thead><tbody>
<tr class="block"><td colspan="4">Tema 1 · Teknologi — uge 32 til 51</td></tr>
{raekker(TEMA1)}
<tr class="block"><td colspan="4">Tema 2 · Magt — uge 1 til 20</td></tr>
{raekker(TEMA2)}
</tbody></table>
<div class="two"><div><h2 class="sec"><span class="num">i</span> Uger pr. tema</h2>
<table class="mini"><thead><tr><th>Tema</th><th>Uger</th><th>Andel</th></tr></thead>
<tbody><tr><td>Teknologi</td><td>{U1}</td><td>{round(U1 / (U1 + U2) * 100)} %</td></tr>
<tr><td>Magt</td><td>{U2}</td><td>{round(U2 / (U1 + U2) * 100)} %</td></tr>
</tbody></table><div class="figur" style="text-align:center;margin-top:10px">{fig}
<div class="mat">Undervisningsuger pr. tema. Ferier og OPO er trukket fra.</div>
</div></div>
<div><h2 class="sec"><span class="num">!</span> Faste afbrydelser</h2>
<table class="mini"><thead><tr><th>Uge</th><th>Afbrydelse</th></tr></thead><tbody>
{''.join(f'<tr><td>{u}</td><td>{t}</td></tr>' for u, t in FERIER)}
</tbody></table></div></div>
<h2 class="sec"><span class="num">A</span> Afleveringer</h2>
<table class="mini"><thead><tr><th>Uge</th><th>Opgave</th></tr></thead><tbody>
{''.join(f'<tr><td>{u}</td><td>{t}</td></tr>' for u, t in AFLEVERINGER)}
</tbody></table>
'''

DOK = ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
       '<meta name="viewport" content="width=device-width,initial-scale=1">'
       '<title>Årsplan · samfundsfag · 9. klasse</title><style>' + CSS +
       '</style></head><body><header class="top"><div class="top-inner">'
       '<a class="brand" href="index.html">Mibelibsen <span>9. klasse</span></a>'
       '<nav class="tabs"><a class="" href="matematik.html">Matematik</a>'
       '<a class="active" href="samfundsfag.html">Samfundsfag</a>'
       '<a class="" href="tysk.html">Tysk</a><span class="soon">Fysik</span>'
       '</nav></div></header><main>' + KROP + '</main><footer>'
       'Undervisningsmateriale · 9. klasse · Mibelibsen. Årsplanen er skrevet af '
       'fra lærerens egen plan.</footer></body></html>')
open(UD, 'w').write(DOK)
print(f'skrevet:  {UD}  ·  {U1} uger teknologi, {U2} uger magt')
