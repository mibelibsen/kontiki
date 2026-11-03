# -*- coding: utf-8 -*-
"""Bygger tysk-resultater.html — hvad de 170 unge svarede.

Den anden halvdel af spoergeskemaprojektet. Ungerne lavede spoergsmaalene,
stod i Hamborg og spurgte, og svarene kom hjem. Siden her viser, hvad der
kom ud af det.

    python3 claude/byg_tysk_resultater.py

**Kun tal, ingen enkeltsvar.** Sitet er offentligt, og besvarelserne er
fra unge paa andre skoler. Siden viser optaellinger og de hyppigste svar
paa de aabne spoergsmaal - aldrig en enkelt besvarelse for sig. De fulde
svar ligger i tekster/, som ikke udgives, og bruges i timen.

Tallene hentes fra regnearket ved hver koersel, saa siden og dataene ikke
kan komme til at sige hver sit.
"""
import csv
import io
import html as H
import os
import sys
import urllib.request
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figurer as FG

UD = 'tysk-resultater.html'
ARK = ('https://docs.google.com/spreadsheets/d/'
       '1QwwgmHeMVc-lsMEtmXtT4BobkF0HGyjVr9Twi1tCWbY/gviz/tq?tqx=out:csv')
TOP = 6          # saa mange af de hyppigste aabne svar vises

# Svar, der ikke skal staa paa en aaben skoleside, selv om de er givet.
# Herbertstrasse er bordelgaden paa St. Pauli; den er lukket for kvinder og
# for alle under 18, og den laa oeverst paa listen over steder, de unge
# ville anbefale os at se. Den staar stadig i klassens eget dokument, hvor
# en voksen er til stede - men ikke her. Det er en redaktionel beslutning,
# ikke en rettelse af data: tallet for, hvor mange der svarede, er uaendret.
UDE = {'Herbertstraße', 'Herbertstrasse', 'Herbertstr.'}


def hent():
    with urllib.request.urlopen(ARK, timeout=60) as r:
        raekker = list(csv.reader(io.StringIO(r.read().decode('utf-8'))))
    hoved, data = raekker[0], raekker[1:]
    assert len(data) > 100, f'kun {len(data)} besvarelser'
    return hoved, data


def t(data, i):
    return Counter(r[i].strip() for r in data if i < len(r) and r[i].strip())


# (overskrift, [(kolonne, figurtype, kort tekst)]) - figurtype er
# 'soejler', 'cirkel' eller 'top' (hyppigste frie svar)
AFSNIT = [
 ('Hvem svarede?', [
   (33, 'soejler', 'Aldersfordelingen. De fleste er på jeres egen alder '
    'eller lidt ældre.'),
   (34, 'cirkel', 'Kønsfordelingen blandt dem, I fik fat i.'),
   (2, 'cirkel', 'Bor de i Hamborg? Det er vigtigere, end det ser ud: '
    'knap halvdelen gør ikke, og det farver alt det, de svarer om byen.'),
 ]),
 ('Byen', [
   (7, 'soejler', 'Vil de bo i Hamborg senere?'),
   (5, 'top', 'Det, de bedst kan lide ved Hamborg.'),
   (6, 'top', 'De steder, de selv ville anbefale jer at se.'),
 ]),
 ('Skole og job', [
   (8, 'soejler', 'Går de i skole?'),
   (10, 'cirkel', 'Har de et job ved siden af?'),
   (12, 'top', 'Drømmejobbet.'),
 ]),
 ('Fritid og venner', [
   (14, 'cirkel', 'Dyrker de sport?'),
   (18, 'soejler', 'Hvor ofte ses de med vennerne?'),
   (13, 'top', 'Det, de helst laver i fritiden.'),
 ]),
 ('Mobil og medier', [
   (21, 'soejler', 'Timer på telefonen om dagen.'),
   (23, 'soejler', 'Hvor mange sociale medier bruger de?'),
   (22, 'top', 'Det, de helst bruger telefonen til.'),
 ]),
 ('Mad, vaner og værdier', [
   (27, 'soejler', 'Hvor tit køber de slik om ugen?'),
   (28, 'cirkel', 'Kan de lide øl?'),
   (29, 'top', 'Det vigtigste i livet.'),
 ]),
]

# Rækkefølgen paa svarmuligheder, hvor "flest foerst" ville skjule en skala.
ORDEN = {
 33: ['13', '14', '15', '16', '17 oder älter'],
 21: ['Unter 1 Stunde', '1–2 Stunden', '3–4 Stunden', 'Mehr als 4 Stunden'],
 23: ['Keine', '1–2', '3–4', '5 oder mehr'],
 27: ['Nie', '1-mal', '2- bis 3-mal', '4-mal oder öfter'],
 18: ['Jeden Tag', 'Mehrmals pro Woche', 'Einmal pro Woche', 'Seltener'],
}


def figur(hoved, data, i, slags):
    u = t(data, i)
    n = sum(u.values())
    if slags == 'top':
        flest = u.most_common(TOP)
        # Kun svar, mere end én har givet. Et svar, kun én har skrevet, er
        # ikke et resultat - og det er dét, der goer en besvarelse til en
        # enkelt persons udsagn i stedet for en optaelling.
        flest = [(k, v) for k, v in flest
                 if v > 1 and k not in UDE]
        if not flest:
            return '', f'Ingen svar går igen hos mere end én af de {n}.'
        liste = ''.join(
            f'<li><span class="de">{H.escape(k)}</span>'
            f'<span class="antal">{v}</span></li>' for k, v in flest)
        andre = len(u) - len(flest)
        return (f'<ol class="top">{liste}</ol>',
                f'{n} svarede. {len(u)} forskellige svar i alt — her er de '
                f'{len(flest)}, som flere end én gav. De øvrige {andre} '
                f'står i klassens eget dokument.')
    rk = ORDEN.get(i)
    par = ([(k, u[k]) for k in rk if k in u] if rk else u.most_common())
    assert sum(v for _, v in par) == n, f'kolonne {i}: en svarmulighed mangler'
    if slags == 'cirkel':
        return FG.cirkeldiagram(par, vis_grader=False), f'{n} svarede.'
    vals = [v for _, v in par]
    kats = [k.replace(' oder älter', '+').replace(' Stunden', ' t')
             .replace('Unter 1 Stunde', 'Under 1 t')
             .replace(' oder mehr', '+').replace('Nein, ', '')[:22]
            for k, _ in par]
    return (FG.soejler(vals, kats, ynavn='antal svar'), f'{n} svarede.')


def byg(hoved, data):
    n = len(data)
    ikke = sum(1 for r in data if r[2].strip() == 'Nein')
    krop = ''
    for navn, dele in AFSNIT:
        krop += f'<h2 class="sec">{H.escape(navn)}</h2>'
        for i, slags, tekst in dele:
            fig, under = figur(hoved, data, i, slags)
            krop += (f'<section class="res"><h3>{H.escape(hoved[i])}</h3>'
                     f'<p class="da">{H.escape(tekst)}</p>'
                     + (f'<div class="figur">{fig}</div>' if fig else '')
                     + f'<p class="kilde">{H.escape(under)}</p></section>')

    BASIS = open('samfundsfag.html', encoding='utf-8').read()
    css = BASIS[BASIS.find('<style>') + 7:BASIS.find('</style>')] + '''
.sec{font-size:1.45rem;margin:32px 0 6px}
.res{background:var(--panel);border:1px solid var(--line);border-radius:14px;
padding:18px 22px;margin:12px 0;box-shadow:var(--shadow)}
.res h3{font-size:1.05rem;margin:0 0 4px}
.da{color:var(--muted);margin:0;font-size:.97rem;max-width:72ch}
.kilde{color:var(--muted);font-size:.86rem;margin:10px 0 0}
.figur{margin:14px 0 0;text-align:center}
.figur svg{max-width:100%;height:auto}
ol.top{list-style:none;counter-reset:n;padding:0;margin:12px 0 0;
max-width:60ch}
ol.top li{counter-increment:n;display:flex;align-items:center;gap:10px;
background:var(--panel2);border:1px solid var(--line);border-radius:10px;
padding:8px 14px;margin:5px 0}
ol.top li:before{content:counter(n);flex:0 0 22px;height:22px;
border-radius:50%;background:var(--accent);color:#fff;font-weight:800;
font-size:.78rem;display:grid;place-items:center}
ol.top .de{flex:1;font-weight:600;text-align:left}
ol.top .antal{color:var(--muted);font-size:.86rem}
.tal{display:flex;flex-wrap:wrap;gap:12px;margin:14px 0 0}
.tal div{flex:1 1 150px;background:var(--panel2);border:1px solid var(--line);
border-radius:12px;padding:14px 16px}
.tal b{display:block;font-size:1.8rem;line-height:1.1;color:var(--accent)}
.tal span{color:var(--muted);font-size:.9rem}
@media print{header.top,.btnlink{display:none!important}
.res,.figur{box-shadow:none;break-inside:avoid}@page{size:A4;margin:14mm}}
'''
    hero = (f'<section class="hero"><span class="pill">Tysk · Ung i '
            f'Tyskland</span><h1>Det svarede de</h1>'
            f'<p>I lavede spørgsmålene, I stod i Hamborg og spurgte, og '
            f'svarene kom hjem. Her er, hvad {n} unge svarede.</p>'
            f'<div class="tal"><div><b>{n}</b><span>besvarelser</span></div>'
            f'<div><b>{len(hoved) - 2}</b><span>spørgsmål, I selv skrev'
            f'</span></div>'
            f'<div><b>{ikke}</b><span>af dem bor ikke i Hamborg</span></div>'
            f'</div>'
            f'<a class="btnlink ghost" href="tysk.html">Tilbage til tysk</a>'
            f'<a class="btnlink ghost" href="tysk-spoergeskema.html">'
            f'Om projektet</a></section>'
            f'<p class="da" style="margin:18px 0 0">Siden viser '
            f'<b>optællinger</b>, ikke enkeltsvar. De fulde besvarelser '
            f'bruger I i timen — de ligger ikke her, fordi de er skrevet af '
            f'unge på andre skoler.</p>')
    return ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Det svarede de · Ung i Tyskland · 9. klasse</title>'
            '<style>' + css + '</style></head><body>'
            '<header class="top"><div class="top-inner">'
            '<a class="brand" href="index.html">Mibelibsen '
            '<span>9. klasse</span></a><nav class="tabs">'
            '<a class="" href="matematik.html">Matematik</a>'
            '<a class="" href="samfundsfag.html">Samfundsfag</a>'
            '<a class="active" href="tysk.html">Tysk</a>'
            '<a class="" href="fysik.html">Fysik</a></nav></div></header>'
            '<main>' + hero + krop + '</main><footer>'
            'Undervisningsmateriale · 9. klasse · Mibelibsen.'
            '</footer></body></html>')


if __name__ == '__main__':
    hoved, data = hent()
    open(UD, 'w', encoding='utf-8').write(byg(hoved, data))
    print(f'skrevet:  {UD}  ·  {len(data)} besvarelser · '
          f'{sum(len(d) for _, d in AFSNIT)} resultater i '
          f'{len(AFSNIT)} afsnit')
