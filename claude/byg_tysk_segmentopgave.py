# -*- coding: utf-8 -*-
"""Bygger tysk-segmenter.html — gruppeopgaven over svarene fra Hamborg.

Siden beskriver opgaven: fem segmenter, fem grupper, hvad hver gruppe skal
gennemgaa, oversaette og sammenfatte. **Selve dokumentet med de 170
besvarelser ligger ikke paa sitet og linkes ikke herfra** - besvarelserne
er skrevet af unge paa andre skoler, og sitet er aabent. Laereren deler
dokumentet. Afgjort 3.11.

Segmenterne hentes fra claude/byg_hamborg_segmenter.py, saa siden og
dokumentet ikke kan komme til at sige hver sit. Tallene for, hvor meget
hver gruppe skal oversaette, regnes ud af de rigtige svar.

    python3 claude/byg_tysk_segmentopgave.py
"""
import html as H
import importlib.util
import os
import sys

import figurer as FG

HER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HER)

_spec = importlib.util.spec_from_file_location(
    'hamborg', os.path.join(HER, 'byg_hamborg_segmenter.py'))
HAM = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(HAM)

UD = 'tysk-segmenter.html'
START = 'tirsdag den 10. november'

AFLEVERING = [
 ('Oversættelsen', 'Alle svar i jeres segment skrevet på dansk. Den skriver '
  'I direkte ind i dokumentet.'),
 ('Sammenfatningen', 'En halv side: hvad fortæller jeres segment om at være '
  'ung i Hamborg? Brug tal — "69 ud af 169" siger mere end "mange".'),
 ('Tre fund', 'De tre ting, I selv synes er mest værd at vide. Dem '
  'fremlægger I for de andre grupper, så alle får hele billedet.'),
]


def byg():
    hoved, data, _ = HAM.hent()
    n = len(data)
    ikke = sum(1 for r in data if r[2].strip() == 'Nein')

    # Figuren viser, hvor meget hver gruppe skal oversaette. Den er her,
    # fordi det foerste spoergsmaal fra en gruppe altid er, om de har faaet
    # mere end de andre. Tallene er talt op i de rigtige svar.
    vals, kats = [], []
    kort = ''
    for nr, navn, kol, om in HAM.SEGMENTER:
        aabne = [i for i in kol if len(HAM.svar(data, i)) > HAM.AABEN]
        antal = sum(len(HAM.svar(data, i)) for i in aabne)
        spm = ''.join(f'<li>{H.escape(hoved[i])}</li>' for i in kol)
        vals.append(antal)
        kats.append(f'{nr} {navn.split()[0].rstrip(",")}')
        kort += (f'<section class="seg"><div class="nr">{nr}</div>'
                 f'<div class="krop"><h3>{H.escape(navn)}</h3>'
                 f'<p>{H.escape(om)}</p>'
                 f'<p class="maal"><b>{len(kol)}</b> spørgsmål · '
                 f'<b>{len(aabne)}</b> med frie svar · '
                 f'<b>{antal}</b> forskellige svar at oversætte</p>'
                 f'<details><summary>Se spørgsmålene</summary>'
                 f'<ul class="spm">{spm}</ul></details></div></section>')

    opg = ''.join(f'<li>{t}</li>' for t in HAM.OPGAVER)
    afl = ''.join(f'<tr><th>{H.escape(a)}</th><td>{H.escape(b)}</td></tr>'
                  for a, b in AFLEVERING)

    BASIS = open('samfundsfag.html', encoding='utf-8').read()
    css = BASIS[BASIS.find('<style>') + 7:BASIS.find('</style>')] + '''
.sec{font-size:1.45rem;margin:32px 0 6px}
.lead{color:var(--muted);max-width:74ch;margin:0 0 4px}
.boks{background:var(--panel);border:1px solid var(--line);
border-left:5px solid var(--accent);border-radius:14px;padding:16px 22px;
margin:16px 0;box-shadow:var(--shadow)}
.boks h3{margin:0 0 6px;font-size:1.05rem}
.boks ol{margin:6px 0 0;padding-left:20px}
.boks li{margin:6px 0;color:var(--muted)}
.boks li b{color:var(--ink)}
.advarsel{border-left-color:#b5710a}
.advarsel p{color:var(--muted);margin:0;max-width:74ch}
.seg{display:flex;gap:16px;background:var(--panel);border:1px solid var(--line);
border-radius:14px;padding:18px 22px;margin:12px 0;box-shadow:var(--shadow)}
.seg .nr{flex:0 0 38px;height:38px;border-radius:11px;background:var(--accent);
color:#fff;font-weight:800;font-size:1.1rem;display:grid;place-items:center}
.seg .krop{flex:1}
.seg h3{margin:0 0 4px;font-size:1.12rem}
.seg p{margin:0;color:var(--muted);font-size:.97rem;max-width:70ch}
.seg .maal{margin:8px 0 0;font-size:.9rem}
.seg .maal b{color:var(--accent)}
.seg details{margin:10px 0 0}
.seg summary{cursor:pointer;color:var(--accent);font-size:.9rem;
font-weight:600}
ul.spm{margin:8px 0 0;padding-left:20px}
ul.spm li{color:var(--muted);font-size:.92rem;margin:3px 0}
table.afl{width:100%;border-collapse:collapse;margin:10px 0;font-size:.95rem}
table.afl th,table.afl td{border:1px solid var(--line);padding:10px 12px;
text-align:left;vertical-align:top}
table.afl th{background:var(--panel2);width:26%}
.figur{background:var(--panel2);border:1px solid var(--line);
border-radius:14px;padding:18px;margin:14px 0;text-align:center}
.figur svg{max-width:100%;height:auto}
.figtekst{color:var(--muted);font-size:.9rem;margin-top:10px;text-align:left;
max-width:68ch;margin-left:auto;margin-right:auto}
@media print{header.top,.btnlink{display:none!important}
.seg,.boks{box-shadow:none;break-inside:avoid}
details{display:block}summary{display:none}@page{size:A4;margin:14mm}}
'''

    krop = (f'<section class="hero"><span class="pill">Tysk · Ung i '
            f'Tyskland</span><h1>Svarene fra Hamborg</h1>'
            f'<p>{n} unge svarede på jeres egne spørgsmål. Svarene er delt '
            f'i fem segmenter — ét til hver gruppe. I skal gennemgå jeres '
            f'eget, oversætte det og sammenfatte, hvad det fortæller. '
            f'Vi går i gang <b>{START}</b>.</p>'
            f'<a class="btnlink ghost" href="tysk.html">Tilbage til tysk</a>'
            f'<a class="btnlink ghost" href="tysk-spoergeskema.html">'
            f'Om projektet</a></section>'

            f'<div class="boks"><h3>Sådan arbejder I</h3><ol>{opg}</ol>'
            f'<p style="color:var(--muted);font-size:.92rem;margin:10px 0 0">'
            f'Dokumentet med alle svarene får I af jeres lærer. Det ligger '
            f'ikke her på siden: besvarelserne er skrevet af unge på andre '
            f'skoler, og siden er åben for alle.</p></div>'

            f'<div class="boks advarsel"><h3>Læg mærke til det her, før I '
            f'går i gang</h3><p><b>{ikke} af de {n}</b> svarer <i>nein</i> '
            f'til spørgsmålet, om de bor i Hamborg. Derfor står der '
            f'<i>keine Ahnung, bin nicht von hier</i> i en del af svarene '
            f'om byen. Det er ikke en fejl i jeres skema — det er et '
            f'resultat, og det hører med i jeres sammenfatning. Et svar fra '
            f'en, der ikke bor i byen, fortæller noget andet end et svar '
            f'fra en, der gør.</p></div>'

            f'<h2 class="sec">De fem segmenter</h2>'
            f'<p class="lead">Én gruppe pr. segment. Tallene viser, hvor '
            f'meget der skal oversættes — de er talt op i de rigtige '
            f'svar.</p>'
            f'<div class="figur">'
            f'{FG.soejler(vals, kats, ynavn="svar at oversætte")}'
            f'<div class="figtekst">Ingen gruppe har fået dobbelt så meget '
            f'som en anden. Første opdeling gav segment 5 over 400 svar, og '
            f'spørgsmålet om rejser flyttede derfor til segment 1, hvor det '
            f'også hører bedre hjemme.</div></div>{kort}'

            f'<h2 class="sec">Det afleverer I</h2>'
            f'<table class="afl"><tbody>{afl}</tbody></table>')

    return ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Svarene fra Hamborg · gruppeopgave · 9. klasse</title>'
            '<style>' + css + '</style></head><body>'
            '<header class="top"><div class="top-inner">'
            '<a class="brand" href="index.html">Mibelibsen '
            '<span>9. klasse</span></a><nav class="tabs">'
            '<a class="" href="matematik.html">Matematik</a>'
            '<a class="" href="samfundsfag.html">Samfundsfag</a>'
            '<a class="active" href="tysk.html">Tysk</a>'
            '<a class="" href="fysik.html">Fysik</a></nav></div></header>'
            '<main>' + krop + '</main><footer>'
            'Undervisningsmateriale · 9. klasse · Mibelibsen.'
            '</footer></body></html>')


if __name__ == '__main__':
    open(UD, 'w', encoding='utf-8').write(byg())
    print(f'skrevet:  {UD}  ·  {len(HAM.SEGMENTER)} segmenter · start {START}')
