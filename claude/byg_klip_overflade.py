# -*- coding: utf-8 -*-
"""Bygger materiale/klip-overfladen-fri.pdf og vejledning/…-svar.pdf

Tredje ark i raekken efter arealet og rumfanget. Her er saksen ikke et
hjaelpemiddel - den er hele pointen: **overfladen er praecis det, der ligger
fladt, naar man klipper legemet op.** Et legeme har ikke en overflade, man
kan se; en udfoldning har et areal, man kan maale.

  A  Kassen      -> seks flader, tre par
  B  Cylinderen  -> den krumme side er et rektangel, og dets bredde er
                    omkredsen. Det kan ikke ses uden at klippe.
  C  Pyramiden   -> grundflade og fire trekanter, og faelden med sidehoejden

Kassen og pyramiden er **de samme som paa rumfangsarket**. Har klassen
bygget dem, kan de klippes op igen i stedet for at blive printet forfra.

    python3 claude/byg_klip_overflade.py
"""
import importlib.util
import math
import os
import subprocess
from fractions import Fraction as F

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HER = os.path.dirname(os.path.abspath(__file__))

_spec = importlib.util.spec_from_file_location(
    'rumfang', os.path.join(HER, 'byg_klip_rumfang.py'))
RF = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(RF)

L, B, H = RF.L, RF.B, RF.H          # samme kasse og pyramide som sidst
R, CH = 20, 50                      # cylinderen: radius og hoejde
FLAP = RF.FLAP

OMKREDS = 2 * math.pi * R
O_KASSE = 2 * (L * B + L * H + B * H)
O_CYLINDER = 2 * math.pi * R ** 2 + OMKREDS * CH
S_L = math.sqrt(H ** 2 + (B / 2) ** 2)     # sidehoejde mod L-siden
S_B = math.sqrt(H ** 2 + (L / 2) ** 2)     # sidehoejde mod B-siden
O_PYRAMIDE = L * B + 2 * (L * S_L / 2) + 2 * (B * S_B / 2)

# Sidehoejden mod B-siden er en 3-4-5-trekant og derfor praecis 50 mm.
assert abs(S_B - 50) < 1e-9, 'sidehøjden er ikke længere præcis'
# Rektanglet i cylinderens udfoldning SKAL vaere lige saa bredt som
# cirklens omkreds - det er hele oevelsens pointe.
assert abs(OMKREDS - 2 * math.pi * R) < 1e-9

INK, LIN, BLA, LYS, FLAPF = RF.INK, RF.LIN, RF.BLA, RF.LYS, RF.FLAPF
KLIP, FOLD = RF.KLIP, RF.FOLD


def kom(x, n=1):
    """Dansk decimalkomma. Facit skrives, som ungerne skal skrive det."""
    return f'{x:.{n}f}'.replace('.', ',')



def cylindernet():
    """Den krumme side som rektangel, og de to cirkler ved siden af. Der er
    én limflap paa rektanglets korte kant: nok til at rulle det til et roer
    og proeve, om cirklen passer i aabningen. Det er den proeve, der viser,
    at bredden er omkredsen."""
    gab = 8
    d = [f'<rect x="0" y="0" width="{OMKREDS:.2f}" height="{CH}" {KLIP}/>']
    g, pkt = RF._flap((OMKREDS, 0), (OMKREDS, CH), (OMKREDS - 1, 0))
    d.append(g)
    punkter = [(0, 0), (OMKREDS, CH)] + pkt
    cy = CH + gab + R
    for i, cx in enumerate((R + 2, 3 * R + 12)):
        d.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" {KLIP}/>')
        punkter += [(cx - R, cy - R), (cx + R, cy + R)]
    d.append(f'<text x="{OMKREDS/2:.1f}" y="{CH/2 + 2:.0f}" '
             f'text-anchor="middle" font-size="5" fill="{LIN}">'
             f'den krumme side</text>')
    return RF.svg(''.join(d), punkter)


TRIN = [
 ('A', 'Kassen', [
   'Klip kassen op langs kanterne, så den kan ligge helt fladt.',
   'Mål hvert eneste rektangel, og skriv målene ned.',
   'Læg mærke til, at der ikke blev mere eller mindre papir.'],
  'Hvor stort er arealet af hele udfoldningen?',
  ['Hvor mange flader er der i alt?',
   'Hvor mange af dem er helt ens? Hvor mange par?',
   'Blev papiret større eller mindre, da du klippede den op?'],
  'Så hvad er overfladearealet af en kasse?'),

 ('B', 'Cylinderen', [
   'Klip rektanglet og de to cirkler ud.',
   'Mål rektanglets <b>bredde</b>, og skriv den ned.',
   'Rul rektanglet til et rør, og prøv, om en cirkel passer i åbningen.'],
  'Hvad er rektanglets bredde — og hvad er cirklens omkreds?',
  ['Regn cirklens omkreds ud med 2 · π · r. Passer det med det, du målte?',
   'Hvor stort er rektanglets areal?',
   'Hvor stort er arealet af de to cirkler tilsammen?'],
  'Så hvad er overfladearealet af en cylinder?'),

 ('C', 'Pyramiden', [
   'Klip pyramiden op, så den ligger fladt.',
   'Mål grundfladen og hver af de fire trekanter.',
   'Læg mærke til, at trekanterne ikke er lige store to og to.'],
  'Hvor stort er overfladearealet?',
  ['Hvilken højde bruger du i en trekant — pyramidens højde eller '
   'trekantens egen?',
   'Mål begge dele på din pyramide. Hvor stor er forskellen?',
   'Hvorfor er de to par trekanter ikke lige store?'],
  'Så hvad er overfladearealet af en pyramide?'),
]

REGN = [
 'En kasse er 10 cm lang, 6 cm bred og 4 cm høj.',
 'En terning har kanten 5 cm.',
 'En dåse er 8 cm høj og har radius 3 cm. Hvor meget metal går der til?',
 'En terning har overfladearealet 96 cm². Hvor lang er en kant?',
 'En cylinder har radius 4 cm og højden 10 cm.',
]

SVAR_REGN = ['248 cm²', '150 cm²',
             f'{kom(2*math.pi*9 + 2*math.pi*3*8)} cm²',
             '4 cm — en terning har seks ens flader, så 96 ÷ 6 = 16, og '
             'kanten er kvadratroden af 16',
             f'{kom(2*math.pi*16 + 2*math.pi*4*10)} cm²']

SVAR = [
 ('A', f'<b>{O_KASSE // 100} cm².</b> Seks flader, tre par: bund og låg '
       f'{L//10}·{B//10}, for og bag {L//10}·{H//10}, to sider '
       f'{B//10}·{H//10}. Papiret blev hverken større eller mindre, da det '
       'blev foldet — derfor er overfladen netop udfoldningens areal. '
       '<b>2 · (l·b + l·h + b·h)</b>.'),
 ('B', f'Rektanglet er <b>{OMKREDS:.0f} mm</b> bredt, og cirklens omkreds '
       f'er 2 · π · {R} = {kom(OMKREDS)} mm. Det er det samme tal, og det er '
       'ikke et tilfælde: rektanglet <i>er</i> cirklen rullet ud. Derfor '
       f'<b>2 · π · r² + 2 · π · r · h</b> = {kom(O_CYLINDER/100)} cm².'),
 ('C', f'<b>{kom(O_PYRAMIDE/100)} cm².</b> Grundfladen {L*B//100} cm² og '
       'fire trekanter — to og to ens. De er ikke alle fire ens, fordi '
       'grundfladen ikke er et kvadrat: sidehøjden mod den lange side er '
       f'{kom(S_L)} mm, mod den korte {S_B:.0f} mm. <b>Grundflade + de fire '
       'trekanter</b>.'),
]

_AREAL = open(os.path.join(ROD, 'claude', 'byg_klip_areal.py'),
              encoding='utf-8').read()
_i = _AREAL.index("CSS = '''") + 9
CSS = _AREAL[_i:_AREAL.index("\n'''", _i)] + '''
.net{border:0.3mm dashed #c9d2e0;border-radius:2mm;padding:2mm;
display:inline-block;margin:0;page-break-inside:avoid}
.ny{page-break-before:always}
.hvad{color:#333;margin:0 0 2mm;max-width:150mm;font-size:9.5pt}
h1.smal{font-size:16pt;margin:0 0 3mm}
h2{margin:3mm 0 1mm}
'''

KLIPARK = (
 '<h1 class="smal">Klip overfladen fri</h1>'
 '<div class="boks" style="margin:0 0 4mm"><b>Find kassen og pyramiden '
 'frem.</b><p style="margin:1mm 0 0;color:#333;font-size:9.5pt">Det er de '
 'samme to legemer som på <i>Klip rumfanget fri</i>. Har I bygget dem, '
 'skal I klippe dem op igen — det er netop dét, øvelsen går ud på. Har I '
 'ikke, så print klippearket derfra. Her er kun cylinderen, for den er '
 'ny.</p></div>'
 '<h2 style="margin-top:0">B · Cylinderen</h2>'
 '<p class="hvad">Rektanglet er den krumme side, rullet ud. De to cirkler '
 'er bund og låg.</p>'
 f'<div class="net">{cylindernet()}</div>'
 '<footer>Udfoldningen er trykt i rigtig størrelse. Printes arket '
 'forminsket, passer dine målinger ikke.</footer>')


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


regn_html = ''.join(
    f'<tr><td class="nr">{i}</td><td>{t}</td><td class="plads"></td></tr>'
    for i, t in enumerate(REGN, 1))

ARBEJD = ('<div class="ny"></div><h1>Hvad fandt du ud af?</h1>'
          '<p class="lead">Overfladearealet er ikke noget, man kan se på et '
          'legeme. Det er det, der ligger fladt, når man klipper det op. '
          'Mål, mens du klipper.</p>' + trin_html()
          + '<h2>Regn videre</h2>'
            '<p style="color:#333;margin:0 0 2mm">Nu har du tre formler, du '
            'selv har fundet. Regn med π ≈ 3,14.</p>'
            f'<table class="regn"><tbody>{regn_html}</tbody></table>'
            '<footer>Skriv enheden på. Overfladeareal måles i cm², ikke '
            'cm³ — det er stadig et areal, bare et foldet et.</footer>')

svar_html = ''.join(
    f'<div class="gr"><div class="bogstav">{b}</div><div>'
    f'<p style="margin:0">{t}</p></div></div>' for b, t in SVAR)
svar_regn_html = ''.join(
    f'<tr><td class="nr">{i}</td><td>{REGN[i-1]}</td>'
    f'<td class="plads"><b>{s}</b></td></tr>'
    for i, s in enumerate(SVAR_REGN, 1))

VEJL = (f'<h1>Klip overfladen fri · forventede svar</h1>'
        f'<p class="lead">Til den voksne. Arket uddeles uden denne side.</p>'
        f'<div class="boks"><b>Hvad øvelsen gør.</b> Et legeme har ikke en '
        f'overflade, man kan måle på. En udfoldning har et areal, man kan '
        f'måle. Det er hele broen, og den bliver klippet. Cylinderen er den '
        f'vigtigste: at den krumme side er et rektangel, og at dets bredde '
        f'er omkredsen, kan ikke ses — kun vises.</div>'
        f'<h2>Hvad de skal nå frem til</h2>{svar_html}'
        f'<h2>Regn videre</h2>'
        f'<table class="regn"><tbody>{svar_regn_html}</tbody></table>'
        f'<div class="boks"><b>Det, der driller.</b> I pyramiden bruger de '
        f'pyramidens højde i stedet for trekantens. Her er de '
        f'{H} mm mod {kom(S_L)} og {S_B:.0f} mm — spørg, hvilken højde der '
        f'hører til den trekant, de regner på. Og i cylinderen glemmer de '
        f'den ene cirkel: en dåse har både bund og låg, et rør har '
        f'ingen af delene. Lad dem selv afgøre, hvad opgaven spørger om.'
        f'</div>'
        f'<footer>Kassen {O_KASSE//100} cm² · cylinderen '
        f'{kom(O_CYLINDER/100)} cm² · pyramiden {kom(O_PYRAMIDE/100)} cm². '
        f'Sidehøjden mod den korte side er præcis {S_B:.0f} mm — en '
        f'3-4-5-trekant.</footer>')


def skriv(navn, krop):
    sti = os.path.join(ROD, navn)
    h = sti.replace('.pdf', '.html')
    os.makedirs(os.path.dirname(sti), exist_ok=True)
    open(h, 'w', encoding='utf-8').write(
        '<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
        '<title>Klip overfladen fri</title><style>' + CSS
        + '</style></head><body>' + krop + '</body></html>')
    subprocess.run(['node', os.path.join(ROD, 'claude', 'html_til_pdf.mjs'),
                    h, sti], check=True, stdout=subprocess.DEVNULL)
    os.remove(h)
    print('skrevet: ', sti)


if __name__ == '__main__':
    skriv('materiale/klip-overfladen-fri.pdf', KLIPARK + ARBEJD)
    skriv('vejledning/klip-overfladen-fri-svar.pdf', VEJL)
    print(f'kassen {O_KASSE//100} cm² · cylinderen {kom(O_CYLINDER/100)} cm² '
          f'· pyramiden {kom(O_PYRAMIDE/100)} cm²')
