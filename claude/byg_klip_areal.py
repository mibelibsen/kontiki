# -*- coding: utf-8 -*-
"""Bygger materiale/klip-arealet-fri.pdf og vejledning/klip-arealet-fri-svar.pdf

Tre arealformler, som ungerne klipper sig frem til i stedet for at faa dem
udleveret: parallelogrammet bliver til et rektangel, to trekanter bliver til
et parallelogram, og cirklen bliver til noget, der naermer sig et rektangel.
Uden saks kan ingen af delene lade sig goere.

    python3 claude/byg_klip_areal.py

Figurerne staar i millimeter og ikke i pixels. De skal printes i rigtig
stoerrelse, for hele oevelsen bygger paa, at ungerne maaler paa papiret
bagefter og regner med deres egne maal. Derfor ligger de her og ikke i
claude/figurer.py, som tegner til skaerm. Koordinaterne er regnet, ikke
sat paa oejemaal - se tallene oeverst.
"""
import math
import os
import subprocess
from fractions import Fraction as F


def kom(x, n=1):
    """Dansk decimalkomma. Facit skrives, som ungerne skal skrive det."""
    return f'{x:.{n}f}'.replace('.', ',')


ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- maalene paa papiret, i mm -------------------------------------------
P_G, P_H, P_S = 80, 50, 25      # parallelogram: grundlinje, hoejde, skaevhed
T_G, T_H, T_S = 70, 40, 20      # trekant
C_R, C_N = 40, 16               # cirkel og antal udsnit

P_AREAL = P_G * P_H                     # 4000 mm²
T_AREAL = F(T_G * T_H, 2)               # 1400 mm²
C_OMKREDS = 2 * math.pi * C_R
C_AREAL = math.pi * C_R ** 2

# Den halve omkreds gange radius SKAL give arealet. Er det ikke tilfaeldet,
# er hele oevelsens pointe forkert.
assert abs(C_OMKREDS / 2 * C_R - C_AREAL) < 1e-9
assert C_N % 2 == 0, 'udsnittene skal kunne deles i to lige store kamme'

INK, LIN, BLA, LYS = '#1a2233', '#9aa4b5', '#1f6fd6', '#eef2f8'


def svg(b, h, krop, luft=2):
    """En figur i rigtig stoerrelse. Papiret er i mm, saa viewBox'en er det
    ogsaa - ét skridt i koordinaterne er én millimeter paa arket."""
    return (f'<svg width="{b + 2 * luft}mm" height="{h + 2 * luft}mm" '
            f'viewBox="0 0 {b + 2 * luft} {h + 2 * luft}" '
            f'xmlns="http://www.w3.org/2000/svg">'
            f'<g transform="translate({luft},{luft})">{krop}</g></svg>')


def klip_parallelogram():
    """Klippelinjen er hoejden. Den venstre trekant har kateterne P_S og
    P_H; flyttes den P_G til hoejre, udfylder den praecis hakket i den anden
    ende, og tilbage staar et rektangel paa P_G x P_H."""
    p = f'0,{P_H} {P_G},{P_H} {P_G + P_S},0 {P_S},0'
    return svg(P_G + P_S, P_H,
               f'<polygon points="{p}" fill="{LYS}" stroke="{INK}" '
               f'stroke-width="0.5"/>'
               f'<line x1="{P_S}" y1="0" x2="{P_S}" y2="{P_H}" '
               f'stroke="{BLA}" stroke-width="0.4" stroke-dasharray="3 2"/>'
               f'<text x="{2 * P_S / 3:.1f}" y="{2 * P_H / 3:.1f}" '
               f'text-anchor="middle" font-size="5" fill="{BLA}">1</text>'
               f'<text x="{P_S + P_G / 2:.1f}" y="{P_H / 2 + 2:.1f}" '
               f'text-anchor="middle" font-size="5" fill="{LIN}">2</text>')


def klip_trekanter():
    """To ens trekanter. Den anden er drejet en halv omgang, saa de to kan
    laegges sammen til et parallelogram med samme grundlinje og hoejde."""
    t1 = f'0,{T_H} {T_G},{T_H} {T_S},0'
    t2 = f'{T_G},0 0,0 {T_G - T_S},{T_H}'
    gab = 10
    return svg(T_G * 2 + gab, T_H,
               f'<polygon points="{t1}" fill="{LYS}" stroke="{INK}" '
               f'stroke-width="0.5"/>'
               f'<g transform="translate({T_G + gab},0)">'
               f'<polygon points="{t2}" fill="#fff" stroke="{INK}" '
               f'stroke-width="0.5"/></g>')


def klip_cirkel():
    """Cirklen deles i C_N lige store udsnit. Hver andet er toent, saa man
    kan se de to kamme, der skal skydes ind i hinanden."""
    cx = cy = C_R
    dele = []
    for i in range(C_N):
        a1 = 2 * math.pi * i / C_N
        a2 = 2 * math.pi * (i + 1) / C_N
        x1, y1 = cx + C_R * math.cos(a1), cy + C_R * math.sin(a1)
        x2, y2 = cx + C_R * math.cos(a2), cy + C_R * math.sin(a2)
        f = LYS if i % 2 else '#fff'
        dele.append(f'<path d="M{cx},{cy} L{x1:.2f},{y1:.2f} '
                    f'A{C_R},{C_R} 0 0 1 {x2:.2f},{y2:.2f} Z" fill="{f}" '
                    f'stroke="{BLA}" stroke-width="0.3" '
                    f'stroke-dasharray="2 1.5"/>')
    return svg(C_R * 2, C_R * 2,
               ''.join(dele)
               + f'<circle cx="{cx}" cy="{cy}" r="{C_R}" fill="none" '
                 f'stroke="{INK}" stroke-width="0.5"/>')


# ------------------------------------------------------------------ teksten
TRIN = [
 ('A', 'Parallelogrammet',
  ['Klip figuren ud langs den sorte kant.',
   'Klip langs den stiplede linje. Nu har du <b>1</b> og <b>2</b>.',
   'Flyt <b>1</b> over i hakket i den anden ende.'],
  'Hvad er figuren blevet til?',
  ['Mål de to sider på den nye figur.', 'Hvad er arealet?',
   'Er der forsvundet noget papir undervejs?'],
  'Så hvordan finder man arealet af et parallelogram?'),

 ('B', 'De to trekanter',
  ['Klip begge trekanter ud.',
   'Vend den ene en halv omgang.',
   'Læg dem sammen, så de danner ét parallelogram.'],
  'Hvor stor en del af parallelogrammet er én trekant?',
  ['Mål grundlinjen og højden på parallelogrammet.',
   'Hvad er parallelogrammets areal?',
   'Hvad er så arealet af én trekant?'],
  'Så hvordan finder man arealet af en trekant?'),

 ('C', 'Cirklen',
  ['Klip cirklen ud.',
   'Klip langs alle de stiplede linjer. Du får 16 stykker.',
   'Læg dem i én række: en lys med spidsen opad, en hvid med spidsen '
   'nedad, hele vejen.'],
  'Hvilken figur begynder det at ligne?',
  ['Mål figurens længde og dens højde.',
   'Højden er cirklens radius. Hvad er den?',
   'Mål en snor rundt om en ny cirkel med samme radius — eller regn '
   'omkredsen ud med 2 · π · r. Sammenlign med figurens længde.'],
  'Hvis længden er den halve omkreds og højden er radius — hvad er cirklens '
  'areal så?'),
]

REGN = [
 'Et parallelogram har grundlinjen 12 cm og højden 7 cm.',
 'En trekant har grundlinjen 9 cm og højden 6 cm.',
 'En cirkel har radius 5 cm.',
 'En trekant har arealet 24 cm² og grundlinjen 8 cm. Hvor høj er den?',
 'En cirkel har omkredsen 31,4 cm. Hvad er dens areal?',
]

SVAR = [
 ('A', f'Et <b>rektangel</b> på {P_G} mm × {P_H} mm. '
       f'Areal {P_AREAL} mm² = {F(P_AREAL,100)} cm². Intet papir er '
       'forsvundet — stykkerne er de samme, de ligger bare anderledes. '
       'Derfor er arealet <b>grundlinje · højde</b>.'),
 ('B', f'Én trekant er <b>halvdelen</b>. Parallelogrammet er '
       f'{T_G} mm × {T_H} mm = {T_G*T_H} mm², så trekanten er '
       f'{T_AREAL} mm² = {F(T_AREAL,100)} cm². Derfor '
       '<b>grundlinje · højde ÷ 2</b>.'),
 ('C', f'Et <b>næsten-rektangel</b>. Længden er den halve omkreds, '
       f'{C_OMKREDS/2:.0f} mm, og højden er radius, {C_R} mm. '
       f'{C_OMKREDS/2:.0f} · {C_R} = {C_AREAL:.0f} mm² = '
       f'{kom(C_AREAL/100)} cm². Den halve omkreds er π · r, så arealet er '
       '<b>π · r · r</b>. Jo flere udsnit, jo mere lige bliver kanten — '
       'det er hele idéen bag formlen.'),
]

SVAR_REGN = ['84 cm²', '27 cm²', f'{kom(math.pi*25)} cm²',
             '6 cm — højden er 2 · areal ÷ grundlinje',
             f'r = 31,4 ÷ (2 · π) = 5 cm, så arealet er {kom(math.pi*25)} cm²']

CSS = '''
*{box-sizing:border-box}
body{margin:0;font-family:Helvetica,Arial,sans-serif;color:#1a2233;
font-size:10.5pt;line-height:1.4}
h1{font-size:19pt;margin:0 0 1.5mm}
h2{font-size:13pt;margin:4mm 0 1.5mm}
.lead{color:#333;margin:0 0 3mm;max-width:150mm}
.gr{display:flex;align-items:flex-start;gap:6mm;margin:0 0 6mm;
page-break-inside:avoid}
.bogstav{flex:0 0 11mm;height:11mm;border-radius:50%;background:#1f6fd6;
color:#fff;font-weight:800;font-size:13pt;display:flex;align-items:center;
justify-content:center}
.gr .navn{font-weight:700;font-size:12pt;margin:0 0 1mm}
.gr ol{margin:0;padding-left:5mm;color:#333}
.gr li{margin:1mm 0}
.fig{border:0.3mm dashed #c9d2e0;border-radius:2mm;padding:2mm;
display:inline-block;margin:0;page-break-inside:avoid}
.sp{font-weight:700;margin:3mm 0 1mm}
.linje{border-bottom:0.3mm solid #c9d2e0;height:7mm}
.boks{border:0.3mm solid #c9d2e0;border-left:1.2mm solid #1f6fd6;
border-radius:2mm;padding:3mm 5mm;margin:3mm 0}
table.regn{width:100%;border-collapse:collapse;margin:2mm 0}
table.regn td{border:0.3mm solid #c9d2e0;padding:2.5mm 3mm;
vertical-align:top}
table.regn td.nr{width:9mm;font-weight:700;text-align:center;
background:#eef2f8}
table.regn td.plads{width:46mm;background:#fbfcfe}
.ny{page-break-before:always}
footer{margin-top:4mm;border-top:0.3mm solid #c9d2e0;padding-top:2mm;
color:#586074;font-size:8.5pt}
@page{size:A4;margin:13mm}
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


KLIP = (f'<h1>Klip arealet fri</h1>'
        f'<p class="lead">Tre figurer, en saks og en lineal. Du skal ikke '
        f'bruge formler — du skal finde dem. Klip langs de <b>sorte</b> '
        f'kanter først, og langs de <b>stiplede</b> linjer bagefter.</p>'
        f'<h2>A · Parallelogrammet</h2>'
        f'<div class="fig">{klip_parallelogram()}</div>'
        f'<h2>B · De to trekanter</h2>'
        f'<div class="fig">{klip_trekanter()}</div>'
        f'<h2>C · Cirklen</h2>'
        f'<div class="fig">{klip_cirkel()}</div>'
        f'<footer>Figurerne er trykt i rigtig størrelse. Printes arket '
        f'forminsket, passer dine målinger ikke.</footer>')

regn_html = ''.join(
    f'<tr><td class="nr">{i}</td><td>{t}<br><span style="color:#586074">'
    f'Hvilken figur er det? Hvilken formel hører til?</span></td>'
    f'<td class="plads"></td></tr>' for i, t in enumerate(REGN, 1))

ARBEJD = (f'<div class="ny"></div><h1>Hvad fandt du ud af?</h1>'
          f'<p class="lead">Udfyld, mens du klipper. Svar med dine egne '
          f'målinger — ikke med noget, du har set før.</p>'
          + trin_html()
          + f'<h2>Regn videre</h2>'
            f'<p style="color:#333;margin:0 0 2mm">Nu har du tre formler, '
            f'du selv har fundet. Brug dem.</p>'
            f'<table class="regn"><tbody>{regn_html}</tbody></table>'
          + '<footer>Regn med π ≈ 3,14. Skriv enheden på — cm² er ikke '
            'det samme som cm.</footer>')


svar_html = ''.join(
    f'<div class="gr"><div class="bogstav">{b}</div><div>'
    f'<p style="margin:0">{t}</p></div></div>' for b, t in SVAR)
svar_regn_html = ''.join(
    f'<tr><td class="nr">{i}</td><td>{REGN[i-1]}</td>'
    f'<td class="plads"><b>{s}</b></td></tr>'
    for i, s in enumerate(SVAR_REGN, 1))

VEJL = (f'<h1>Klip arealet fri · forventede svar</h1>'
        f'<p class="lead">Til den voksne. Arket uddeles uden denne side.</p>'
        f'<div class="boks"><b>Hvad øvelsen gør.</b> De tre formler bliver '
        f'ikke forklaret — de bliver klippet frem. Pointen er, at arealet '
        f'ikke ændrer sig, når stykkerne flyttes: der er lige så meget '
        f'papir før og efter. Det er dét argument, formlerne hviler på.</div>'
        f'<h2>Hvad de skal nå frem til</h2>{svar_html}'
        f'<h2>Regn videre</h2>'
        f'<table class="regn"><tbody>{svar_regn_html}</tbody></table>'
        f'<div class="boks"><b>Det, der driller.</b> Højden i et '
        f'parallelogram og i en trekant er <b>ikke</b> den skrå side — den '
        f'skal stå vinkelret på grundlinjen. Klippelinjen i A viser det '
        f'direkte, og det er værd at pege på. I C bliver kanten aldrig helt '
        f'lige: spørg, hvad der sker, hvis man klipper 32 eller 64 stykker '
        f'i stedet. Det er grænseovergangen, og den kan mærkes med en saks, '
        f'længe før den kan skrives.</div>'
        f'<footer>Mål på papiret: parallelogrammet {P_G}×{P_H} mm '
        f'({F(P_AREAL,100)} cm²) · trekanten {T_G}×{T_H} mm '
        f'({F(T_AREAL,100)} cm²) · cirklen r = {C_R} mm '
        f'({kom(C_AREAL/100)} cm²). Måler de 1-2 mm forkert, er det '
        f'målingen, ikke matematikken.</footer>')


def skriv(navn, krop):
    sti = os.path.join(ROD, navn)
    html_sti = sti.replace('.pdf', '.html')
    os.makedirs(os.path.dirname(sti), exist_ok=True)
    open(html_sti, 'w', encoding='utf-8').write(
        '<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
        '<title>Klip arealet fri</title><style>' + CSS
        + '</style></head><body>' + krop + '</body></html>')
    subprocess.run(['node', os.path.join(ROD, 'claude', 'html_til_pdf.mjs'),
                    html_sti, sti], check=True, stdout=subprocess.DEVNULL)
    os.remove(html_sti)
    print('skrevet: ', sti)


if __name__ == '__main__':
    skriv('materiale/klip-arealet-fri.pdf', KLIP + ARBEJD)
    skriv('vejledning/klip-arealet-fri-svar.pdf', VEJL)
    print(f'parallelogram {P_G}×{P_H} mm · trekant {T_G}×{T_H} mm · '
          f'cirkel r={C_R} mm i {C_N} udsnit')
