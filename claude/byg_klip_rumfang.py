# -*- coding: utf-8 -*-
"""Bygger materiale/klip-rumfanget-fri.pdf og vejledning/…-svar.pdf

Efterfoelgeren til klip-arealet-fri. Samme greb: formlerne staar ikke paa
arket, de bliver klippet og foldet frem.

  A  Grundfladen og lagene  -> rumfang = grundflade · hoejde
  B  Kassen                 -> bygget, fyldt og talt efter
  C  Pyramiden              -> den fylder praecis en tredjedel af kassen

Den sidste er hele pointen. En tredjedel er ikke til at gaette, og den er
ikke til at regne sig til i 7.-8. klasse - men den kan haeldes.

    python3 claude/byg_klip_rumfang.py

Figurerne staar i millimeter, ikke pixels: udfoldningerne skal printes i
rigtig stoerrelse, ellers passer de to legemer ikke sammen, og hele
oevelsen falder.
"""
import math
import os
import subprocess
from fractions import Fraction as F


def kom(x, n=1):
    """Dansk decimalkomma. Facit skrives, som ungerne skal skrive det."""
    return f'{x:.{n}f}'.replace('.', ',')


ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

L, B, H = 60, 40, 40            # kassen: laengde, bredde, hoejde i mm
TERN = 10                       # ternet i grundfladen
FLAP = 8                        # limflap

G = L * B                       # grundfladen
V_KASSE = G * H
V_PYRAMIDE = F(G * H, 3)
assert L % TERN == 0 and B % TERN == 0, 'grundfladen skal gaa op i hele tern'
assert H % TERN == 0, 'hoejden skal vaere et helt antal lag'
# Hele oevelsen staar og falder med, at forholdet er praecis 3.
assert F(V_KASSE) / V_PYRAMIDE == 3

S_L = math.sqrt(H ** 2 + (B / 2) ** 2)   # sidehoejde mod L-siden
S_B = math.sqrt(H ** 2 + (L / 2) ** 2)   # sidehoejde mod B-siden

INK, LIN, BLA, LYS, FLAPF = '#1a2233', '#9aa4b5', '#1f6fd6', '#eef2f8', '#f4f6fb'
KLIP = f'stroke="{INK}" stroke-width="0.5" fill="none"'
FOLD = f'stroke="{BLA}" stroke-width="0.4" stroke-dasharray="4 2.5"'


# Det, der er plads til paa en A4 med 13 mm margen.
PLADS_B, PLADS_H = 184, 271


def svg(krop, punkter, luft=3):
    """Rammen regnes ud af de punkter, figuren faktisk bruger - ogsaa
    limflappernes hjoerner. Et gaet paa bredden gav et pyramidenet paa 206
    mm, og det er bredere end papiret."""
    xs = [x for x, _ in punkter]
    ys = [y for _, y in punkter]
    x0, y0 = min(xs) - luft, min(ys) - luft
    b, h = max(xs) - min(xs) + 2 * luft, max(ys) - min(ys) + 2 * luft
    assert b <= PLADS_B, f'figuren er {b:.0f} mm bred, der er plads til {PLADS_B}'
    assert h <= PLADS_H, f'figuren er {h:.0f} mm høj, der er plads til {PLADS_H}'
    return (f'<svg width="{b:.1f}mm" height="{h:.1f}mm" '
            f'viewBox="0 0 {b:.1f} {h:.1f}" '
            f'xmlns="http://www.w3.org/2000/svg">'
            f'<g transform="translate({-x0:.2f},{-y0:.2f})">{krop}</g></svg>')


def _flap(p, q, væk):
    """En limflap paa kanten p-q, lagt vaek fra punktet `væk`. Retningen
    regnes ud af trekanten, saa flappen altid vender udad - ogsaa paa en
    skraa kant."""
    (x1, y1), (x2, y2) = p, q
    dx, dy = x2 - x1, y2 - y1
    ln = math.hypot(dx, dy)
    nx, ny = -dy / ln, dx / ln
    if (væk[0] - x1) * nx + (væk[1] - y1) * ny > 0:   # peger mod `væk`
        nx, ny = -nx, -ny
    ux, uy = dx / ln, dy / ln
    s = min(FLAP, ln / 3)
    a = (x1 + nx * FLAP + ux * s, y1 + ny * FLAP + uy * s)
    b = (x2 + nx * FLAP - ux * s, y2 + ny * FLAP - uy * s)
    hj = (p, a, b, q)
    pkt = ' '.join(f'{x:.2f},{y:.2f}' for x, y in hj)
    return (f'<polygon points="{pkt}" fill="{FLAPF}" stroke="{INK}" '
            f'stroke-width="0.4"/>'
            f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
            f'{FOLD}/>', list(hj))


def grundflade():
    """Ét lag: grundfladen tegnet som centimetertern, saa den kan taelles."""
    d = [f'<rect x="0" y="0" width="{L}" height="{B}" {KLIP}/>']
    for i in range(1, L // TERN):
        d.append(f'<line x1="{i*TERN}" y1="0" x2="{i*TERN}" y2="{B}" '
                 f'stroke="{LIN}" stroke-width="0.25"/>')
    for j in range(1, B // TERN):
        d.append(f'<line x1="0" y1="{j*TERN}" x2="{L}" y2="{j*TERN}" '
                 f'stroke="{LIN}" stroke-width="0.25"/>')
    return svg(''.join(d), [(0, 0), (L, B)])


def kassenet():
    """Korsudfoldning. Den lodrette stribe er for- og bagside med bund og
    laag imellem; de to sider haenger paa bunden."""
    W, Hh = H + L + H, 2 * H + 2 * B
    x0, x1 = H, H + L
    y = [0, H, H + B, 2 * H + B, 2 * H + 2 * B]   # A, bund, C, laag
    d = [f'<rect x="{x0}" y="0" width="{L}" height="{Hh}" {KLIP}/>',
         f'<rect x="0" y="{y[1]}" width="{H}" height="{B}" {KLIP}/>',
         f'<rect x="{x1}" y="{y[1]}" width="{H}" height="{B}" {KLIP}/>']
    for yy in y[1:-1]:
        d.append(f'<line x1="{x0}" y1="{yy}" x2="{x1}" y2="{yy}" {FOLD}/>')
    d.append(f'<line x1="{x0}" y1="{y[1]}" x2="{x0}" y2="{y[2]}" {FOLD}/>')
    d.append(f'<line x1="{x1}" y1="{y[1]}" x2="{x1}" y2="{y[2]}" {FOLD}/>')
    # limflapper paa de frie lodrette kanter af A, C og laaget, og paa
    # laagets yderkant
    pkt = [(0, 0), (W, Hh)]
    for a, b in ((y[0], y[1]), (y[2], y[3]), (y[3], y[4])):
        for s, mod in (((x0, a), (x0 + 1, a)), ((x1, a), (x1 - 1, a))):
            g, hj = _flap(s, (s[0], b), mod)
            d.append(g)
            pkt += hj
    g, hj = _flap((x0, y[4]), (x1, y[4]), (x0, y[4] - 1))
    d.append(g)
    pkt += hj
    d.append(f'<text x="{x0 + L/2}" y="{y[1] + B/2 + 2}" '
             f'text-anchor="middle" font-size="5" fill="{LIN}">bund</text>')
    return svg(''.join(d), pkt)


def pyramidenet():
    """Grundfladen i midten med de fire sideflader foldet ud. Hoejden i hver
    trekant er sidehoejden - regnet af kassens hoejde og den halve
    grundflade, ikke maalt paa tegningen."""
    W, Hh = 2 * S_B + L, 2 * S_L + B
    bx, by = S_B, S_L
    hj = [(bx, by), (bx + L, by), (bx + L, by + B), (bx, by + B)]
    top = (bx + L / 2, by - S_L)
    bund = (bx + L / 2, by + B + S_L)
    ven = (bx - S_B, by + B / 2)
    hoj = (bx + L + S_B, by + B / 2)
    grund = f'stroke="{INK}" stroke-width="0.5" fill="{LYS}"'
    d = [f'<rect x="{bx:.2f}" y="{by:.2f}" width="{L}" height="{B}" '
         f'{grund}/>']
    for a, b, spids in ((hj[0], hj[1], top), (hj[3], hj[2], bund),
                        (hj[0], hj[3], ven), (hj[1], hj[2], hoj)):
        pkt = ' '.join(f'{x:.2f},{y:.2f}' for x, y in (a, b, spids))
        d.append(f'<polygon points="{pkt}" {KLIP}/>')
        d.append(f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" '
                 f'x2="{b[0]:.2f}" y2="{b[1]:.2f}" {FOLD}/>')
    # flapper paa de to lodrette trekanters skraa kanter
    pkt = list(hj) + [top, bund, ven, hoj]
    for a, b, spids in ((hj[0], hj[3], ven), (hj[1], hj[2], hoj)):
        for kant, mod in ((a, b), (b, a)):
            g, p2 = _flap(kant, spids, mod)
            d.append(g)
            pkt += p2
    d.append(f'<text x="{bx + L/2:.1f}" y="{by + B/2 + 2:.1f}" '
             f'text-anchor="middle" font-size="5" fill="{LIN}">'
             f'grundflade</text>')
    return svg(''.join(d), pkt)


TRIN = [
 ('A', 'Grundfladen', [
   'Klip tern-rektanglet ud. Det er <b>bunden</b> af kassen, i rigtig '
   'størrelse.',
   'Tæl ternene. Hvert tern er 1 cm × 1 cm.',
   'Læg det til side. Du skal bruge det igen om lidt.'],
  'Hvor mange kvadratcentimeter er grundfladen?',
  ['Hvor mange tern er der på langs, og hvor mange på tværs?',
   'Hvordan kan du regne antallet ud uden at tælle hvert enkelt?'],
  'Så hvad er grundfladen?'),

 ('B', 'Kassen', [
   'Klip udfoldningen ud langs de <b>sorte</b> kanter.',
   'Fold langs alle de <b>blå stiplede</b> linjer. Flapperne skal ind.',
   'Lim den sammen, så du har en kasse uden låg — vent med at lukke låget.'],
  'Hvor mange lag af grundfladen er der plads til i kassen?',
  ['Mål kassens højde. Hvor mange centimeter er den?',
   'Læg ternarket ned i bunden. Hvor mange gange skal det stables oven '
   'på sig selv, før kassen er fuld?',
   'Hvor mange kubikcentimeter er der i kassen så?'],
  'Så hvordan finder man rumfanget af en kasse?'),

 ('C', 'Pyramiden', [
   'Klip udfoldningen ud. Grundfladen i midten er <b>den samme</b> som '
   'kassens bund — tjek efter med ternarket.',
   'Fold langs de stiplede linjer, og lim pyramiden sammen. Lad bunden '
   'være åben.',
   'Fyld pyramiden helt op med ris, sand eller linser, og hæld over i '
   'kassen. Gentag, til kassen er fuld.'],
  'Hvor mange pyramider skal der til at fylde kassen?',
  ['Pyramiden og kassen har samme grundflade og samme højde. Havde du '
   'regnet med det tal?',
   'Hvad er pyramidens rumfang så, når du kender kassens?'],
  'Så hvordan finder man rumfanget af en pyramide?'),
]

REGN = [
 'En kasse er 8 cm lang, 5 cm bred og 4 cm høj.',
 'En pyramide har en grundflade på 30 cm² og er 9 cm høj.',
 'En kasse har rumfanget 90 cm³ og en grundflade på 15 cm². Hvor høj er den?',
 'En pyramide og en kasse har samme grundflade og samme højde. Kassen '
 'rummer 150 cm³. Hvad rummer pyramiden?',
 'En pyramide har rumfanget 24 cm³ og er 6 cm høj. Hvad er grundfladen?',
]

SVAR = [
 ('A', f'<b>{L // TERN} × {B // TERN} = {G // 100} tern</b>, altså '
       f'{F(G, 100)} cm². Man behøver ikke tælle dem: antallet på langs '
       'gange antallet på tværs.'),
 ('B', f'Kassen er {H // TERN} cm høj, så der er plads til '
       f'<b>{H // TERN} lag</b> af grundfladen. '
       f'{G // 100} · {H // TERN} = <b>{V_KASSE // 1000} cm³</b>. '
       'Derfor <b>grundflade · højde</b> — præcis som arealet var '
       'grundlinje · højde, bare et skridt op.'),
 ('C', f'<b>Tre.</b> Pyramiden rummer {V_PYRAMIDE // 1000} cm³, kassen '
       f'{V_KASSE // 1000} cm³. Det er den ene tredjedel, ingen gætter, og '
       'den er ikke til at regne sig til uden integralregning — men den er '
       'til at hælde. Derfor <b>grundflade · højde ÷ 3</b>.'),
]
SVAR_REGN = ['160 cm³', '90 cm³', '6 cm — højden er rumfang ÷ grundflade',
             '50 cm³', '12 cm² — grundfladen er 3 · rumfang ÷ højde']


# CSS'en hentes fra arealarket. De to ark hoerer sammen og skal ligne
# hinanden, og én kopi er én kilde til at rette i.
_AREAL = open(os.path.join(ROD, 'claude', 'byg_klip_areal.py'),
              encoding='utf-8').read()
_i = _AREAL.index("CSS = '''") + 9
CSS = _AREAL[_i:_AREAL.index("\n'''", _i)]
CSS += '''
.net{border:0.3mm dashed #c9d2e0;border-radius:2mm;padding:2mm;
display:inline-block;margin:0;page-break-inside:avoid}
.ny{page-break-before:always}
.hvad{color:#333;margin:0 0 2mm;max-width:150mm;font-size:9.5pt}
h1.smal{font-size:16pt;margin:0 0 3mm}
h2{margin:3mm 0 1mm}
'''


def trin_html():
    ud = ''
    for bogstav, navn, gor, spm, under, formel in TRIN:
        ud += (f'<div class="gr"><div class="bogstav">{bogstav}</div><div>'
               f'<p class="navn">{navn}</p><ol>'
               + ''.join(f'<li>{t}</li>' for t in gor) + '</ol>'
               f'<p class="sp">{spm}</p><div class="linje"></div>'
               + ''.join(f'<p style="margin:2mm 0 0;color:#333">{t}</p>'
                         f'<div class="linje"></div>' for t in under)
               + f'<div class="boks"><b>{formel}</b>'
                 f'<div class="linje"></div><div class="linje"></div></div>'
               '</div></div>')
    return ud


KLIPARK = (
 '<h1 class="smal">Klip rumfanget fri</h1>'
 '<h2>A · Grundfladen</h2>'
 f'<div class="net">{grundflade()}</div>'
 '<h2>B · Kassen</h2>'
 '<p class="hvad">Fold langs de blå linjer, flapperne ind. Lad låget stå '
 'åbent, til du har talt lagene.</p>'
 f'<div class="net">{kassenet()}</div>'
 '<div class="ny"></div>'
 '<h2 style="margin-top:0">C · Pyramiden</h2>'
 '<p class="hvad">Grundfladen i midten er den samme som kassens bund — '
 'tjek efter med ternarket. Bunden bliver åben; det er den, du hælder i.</p>'
 f'<div class="net">{pyramidenet()}</div>'
 '<footer>Udfoldningerne er trykt i rigtig størrelse. Printes arket '
 'forminsket, passer pyramiden ikke til kassen, og øvelsen falder.</footer>')

regn_html = ''.join(
    f'<tr><td class="nr">{i}</td><td>{t}</td><td class="plads"></td></tr>'
    for i, t in enumerate(REGN, 1))

ARBEJD = ('<div class="ny"></div><h1>Hvad fandt du ud af?</h1>'
          '<p class="lead">To legemer, en saks og noget at hælde med — ris, '
          'sand eller linser. Formlerne står ikke nogen steder: dem skal du '
          'folde dig frem til. Udfyld, mens du bygger, og svar med dine '
          'egne målinger.</p>' + trin_html()
          + '<h2>Regn videre</h2>'
            '<p style="color:#333;margin:0 0 2mm">Nu har du to formler, du '
            'selv har fundet. Brug dem.</p>'
            f'<table class="regn"><tbody>{regn_html}</tbody></table>'
            '<footer>Skriv enheden på. cm³ er ikke det samme som cm² — og '
            'slet ikke det samme som cm.</footer>')

svar_html = ''.join(
    f'<div class="gr"><div class="bogstav">{b}</div><div>'
    f'<p style="margin:0">{t}</p></div></div>' for b, t in SVAR)
svar_regn_html = ''.join(
    f'<tr><td class="nr">{i}</td><td>{REGN[i-1]}</td>'
    f'<td class="plads"><b>{s}</b></td></tr>'
    for i, s in enumerate(SVAR_REGN, 1))

VEJL = (f'<h1>Klip rumfanget fri · forventede svar</h1>'
        f'<p class="lead">Til den voksne. Arket uddeles uden denne side.</p>'
        f'<div class="boks"><b>Hvad øvelsen gør.</b> Rumfang af en kasse '
        f'kan forklares. Tredjedelen i pyramiden kan ikke — ikke på dette '
        f'trin. Den kan kun vises, og den vises ved at hælde. Det er derfor, '
        f'der skal være ris på bordet.</div>'
        f'<h2>Hvad de skal nå frem til</h2>{svar_html}'
        f'<h2>Regn videre</h2>'
        f'<table class="regn"><tbody>{svar_regn_html}</tbody></table>'
        f'<div class="boks"><b>Det, der driller.</b> Højden i pyramiden er '
        f'<b>ikke</b> sidekanten og heller ikke sidehøjden — den går lodret '
        f'fra spidsen ned til grundfladen. På denne pyramide er højden '
        f'{H // TERN} cm, sidehøjderne {kom(S_L / 10)} og {kom(S_B / 10)} cm, '
        f'og sidekanten '
        f'{kom(math.sqrt((L/2)**2 + (B/2)**2 + H**2) / 10)} cm. Tre '
        f'forskellige tal, og det er det midterste, de kommer til at måle. '
        f'Spørg, hvilket af dem der står i formlen.</div>'
        f'<footer>Grundflade {L // TERN} × {B // TERN} = {G // 100} cm² · '
        f'kassen {V_KASSE // 1000} cm³ · pyramiden {V_PYRAMIDE // 1000} cm³ '
        f'· forholdet er præcis 3.</footer>')


def skriv(navn, krop):
    sti = os.path.join(ROD, navn)
    h = sti.replace('.pdf', '.html')
    os.makedirs(os.path.dirname(sti), exist_ok=True)
    open(h, 'w', encoding='utf-8').write(
        '<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
        '<title>Klip rumfanget fri</title><style>' + CSS
        + '</style></head><body>' + krop + '</body></html>')
    subprocess.run(['node', os.path.join(ROD, 'claude', 'html_til_pdf.mjs'),
                    h, sti], check=True, stdout=subprocess.DEVNULL)
    os.remove(h)
    print('skrevet: ', sti)


if __name__ == '__main__':
    skriv('materiale/klip-rumfanget-fri.pdf', KLIPARK + ARBEJD)
    skriv('vejledning/klip-rumfanget-fri-svar.pdf', VEJL)
    print(f'kassen {L}×{B}×{H} mm = {V_KASSE // 1000} cm³ · '
          f'pyramiden {V_PYRAMIDE // 1000} cm³ · forholdet 3')
