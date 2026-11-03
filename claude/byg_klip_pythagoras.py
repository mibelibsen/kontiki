# -*- coding: utf-8 -*-
"""Bygger materiale/klip-pythagoras-fri.pdf og vejledning/…-svar.pdf

Fjerde ark i raekken efter arealet, rumfanget og overfladen. Samme greb:
formlen staar ikke paa arket. Her er saksen det eneste, der kan afgoere
sagen, for kvadratet paa den lange side ligger skaevt og kan ikke taelles.

  A  Tre kvadrater  -> 9 + 16 = 25, men det skraa kvadrat skal klippes ud
                       og laegges paa ternkvadratet, for det kan ikke taelles
  B  Rammen         -> fire ens trekanter i en (a+b)-ramme, lagt paa to
                       maader. Samme ramme, samme trekanter, altsaa lige
                       store huller: a^2 + b^2 i den ene, c^2 i den anden.
                       Det er beviset, og det bruger ikke 3, 4 og 5
  C  Perigal        -> de to smaa kvadrater bliver *fysisk* til det store:
                       fire stykker af b-kvadratet plus a-kvadratet fylder
                       c-kvadratet praecis

A og C viser det for 3, 4 og 5. B viser hvorfor det gaelder for alle.

    python3 claude/byg_klip_pythagoras.py

Figurerne staar i millimeter, ikke pixels: de skal printes i rigtig
stoerrelse, ellers passer brikkerne ikke i rammen.
"""
import importlib.util
import math
import os
import subprocess

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HER = os.path.dirname(os.path.abspath(__file__))

_spec = importlib.util.spec_from_file_location(
    'rumfang', os.path.join(HER, 'byg_klip_rumfang.py'))
RF = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(RF)

svg, kom = RF.svg, RF.kom
INK, LIN, BLA, LYS, FLAPF = RF.INK, RF.LIN, RF.BLA, RF.LYS, RF.FLAPF
KLIP = RF.KLIP
TERN = RF.TERN                      # 10 mm = 1 cm, samme tern som foer

A, B = 30, 40                       # de to korte sider i mm
C = int(math.hypot(A, B))           # den lange side
RAMME = A + B                       # rammen i B er (a+b) paa hver led

assert A * A + B * B == C * C, 'trekanten skal vaere retvinklet med hele tal'
assert A % TERN == 0 and B % TERN == 0 and C % TERN == 0, 'hele centimeter'
assert A <= B, 'Perigals snit regnes ud fra, at a er den korteste side'

TYND = f'stroke="{LIN}" stroke-width="0.25"'
BLOED = f'fill="{FLAPF}" stroke="{INK}" stroke-width="0.5"'


# ------------------------------------------------------------------ hjaelp
def _poly(punkter, fyld='none', streg=INK, bredde=0.5):
    p = ' '.join(f'{x:.2f},{y:.2f}' for x, y in punkter)
    return (f'<polygon points="{p}" fill="{fyld}" stroke="{streg}" '
            f'stroke-width="{bredde}"/>')


def _tern(x0, y0, w, h):
    """Centimetertern inden i et rektangel, saa det kan taelles."""
    d = []
    for i in range(1, round(w / TERN)):
        d.append(f'<line x1="{x0+i*TERN}" y1="{y0}" x2="{x0+i*TERN}" '
                 f'y2="{y0+h}" {TYND}/>')
    for j in range(1, round(h / TERN)):
        d.append(f'<line x1="{x0}" y1="{y0+j*TERN}" x2="{x0+w}" '
                 f'y2="{y0+j*TERN}" {TYND}/>')
    return ''.join(d)


def _areal(punkter):
    s = 0
    for i, (x1, y1) in enumerate(punkter):
        x2, y2 = punkter[(i + 1) % len(punkter)]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


def _inde(pt, poly):
    x, y = pt
    ind = False
    for i, (x1, y1) in enumerate(poly):
        x2, y2 = poly[(i + 1) % len(poly)]
        if (y1 > y) != (y2 > y):
            if x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
                ind = not ind
    return ind


# --------------------------------------------------------- A: tre kvadrater
# Den rette vinkel ligger i (0,0). Den lange side gaar fra (B,0) til (0,A),
# og kvadratet paa den er drejet - derfor kan det ikke taelles.
HJ = (0, 0)
PA = (B, 0)
PB = (0, A)
# Udadvendt normal paa den lange side, regnet - ikke gaettet.
_dx, _dy = PB[0] - PA[0], PB[1] - PA[1]
_nx, _ny = -_dy / C, _dx / C
if (HJ[0] - PA[0]) * _nx + (HJ[1] - PA[1]) * _ny > 0:
    _nx, _ny = -_nx, -_ny
SKRAAT = [PA, PB, (PB[0] + C * _nx, PB[1] + C * _ny),
          (PA[0] + C * _nx, PA[1] + C * _ny)]
assert abs(_areal(SKRAAT) - C * C) < 1e-9, 'det skrå kvadrat har ikke arealet c²'
for _i in range(4):
    _p, _q = SKRAAT[_i], SKRAAT[(_i + 1) % 4]
    assert abs(math.dist(_p, _q) - C) < 1e-9, 'siderne i det skrå kvadrat'


def tre_kvadrater():
    d = [f'<rect x="0" y="{-B}" width="{B}" height="{B}" {KLIP}/>',
         _tern(0, -B, B, B),
         f'<rect x="{-A}" y="0" width="{A}" height="{A}" {KLIP}/>',
         _tern(-A, 0, A, A),
         _poly(SKRAAT, fyld='#fff', bredde=0.6),
         _poly([HJ, PA, PB], fyld=LYS, bredde=0.4),
         f'<path d="M5,0 L5,5 L0,5" fill="none" stroke="{INK}" '
         f'stroke-width="0.4"/>']
    cx = sum(x for x, _ in SKRAAT) / 4
    cy = sum(y for _, y in SKRAAT) / 4
    d.append(f'<text x="{cx:.1f}" y="{cy:.1f}" text-anchor="middle" '
             f'font-size="5" fill="{LIN}">klip ud</text>')
    return svg(''.join(d), [(-A, -B)] + SKRAAT)


def ternkvadrat():
    """Kvadratet paa den lange side, men liggende lige - saa det kan taelles.
    Det bruges to gange: i A laegges det skraa kvadrat oven paa det, og i C
    skal de fem stykker fylde det ud."""
    return svg(f'<rect x="0" y="0" width="{C}" height="{C}" {KLIP}/>'
               + _tern(0, 0, C, C), [(0, 0), (C, C)])


# ----------------------------------------------------------------- B: rammen
def ramme():
    return svg(f'<rect x="0" y="0" width="{RAMME}" height="{RAMME}" {KLIP}/>'
               f'<text x="{RAMME/2}" y="{RAMME/2+2}" text-anchor="middle" '
               f'font-size="5" fill="{LIN}">rammen</text>',
               [(0, 0), (RAMME, RAMME)])


def fire_trekanter(gab=8):
    """Fire ens retvinklede trekanter, to og to, med skiftende retning saa
    de fylder mindst muligt papir."""
    d, pkt = [], []
    for k in range(4):
        ox = (k % 2) * (B + gab)
        oy = (k // 2) * (A + gab)
        if k % 2:
            t = [(ox + B, oy + A), (ox, oy + A), (ox + B, oy)]
        else:
            t = [(ox, oy), (ox + B, oy), (ox, oy + A)]
        d.append(_poly(t, fyld=LYS))
        pkt += t
    return svg(''.join(d), pkt)


# Opstilling 1: to rektangler, to firkantede huller (a² og b²).
OPST1 = [[(0, 0), (B, 0), (B, A)], [(0, 0), (B, A), (0, A)],
         [(B, A), (RAMME, A), (RAMME, RAMME)],
         [(B, A), (RAMME, RAMME), (B, RAMME)]]
HUL1 = [[(B, 0), (RAMME, 0), (RAMME, A), (B, A)],
        [(0, A), (B, A), (B, RAMME), (0, RAMME)]]
# Opstilling 2: vindmoelle, ét skraat hul (c²).
OPST2 = [[(0, 0), (B, 0), (0, A)], [(B, 0), (RAMME, 0), (RAMME, B)],
         [(RAMME, B), (RAMME, RAMME), (A, RAMME)],
         [(A, RAMME), (0, RAMME), (0, A)]]
HUL2 = [[(B, 0), (RAMME, B), (A, RAMME), (0, A)]]

for _o in (OPST1, OPST2):
    assert all(abs(_areal(t) - A * B / 2) < 1e-9 for t in _o), 'trekanterne'
assert abs(sum(_areal(h) for h in HUL1) - (A * A + B * B)) < 1e-9
assert abs(sum(_areal(h) for h in HUL2) - C * C) < 1e-9
assert abs(sum(_areal(t) for t in OPST1) + sum(_areal(h) for h in HUL1)
           - RAMME ** 2) < 1e-9, 'opstilling 1 fylder ikke rammen'
assert abs(sum(_areal(t) for t in OPST2) + sum(_areal(h) for h in HUL2)
           - RAMME ** 2) < 1e-9, 'opstilling 2 fylder ikke rammen'


def opstilling(trekanter, huller, navne):
    d = [f'<rect x="0" y="0" width="{RAMME}" height="{RAMME}" {KLIP}/>']
    for t in trekanter:
        d.append(_poly(t, fyld=LYS, bredde=0.4))
    for h, navn in zip(huller, navne):
        cx = sum(x for x, _ in h) / len(h)
        cy = sum(y for _, y in h) / len(h)
        d.append(f'<text x="{cx:.1f}" y="{cy+2:.1f}" text-anchor="middle" '
                 f'font-size="6" fill="{BLA}" font-weight="700">{navn}</text>')
    return svg(''.join(d), [(0, 0), (RAMME, RAMME)])


# --------------------------------------------------------------- C: Perigal
# To snit gennem midten af b-kvadratet, det ene parallelt med den lange
# side, det andet vinkelret paa den. Enderne regnes, ikke gaettes:
# midten +/- (c/2)·u giver praecis kvadratets kant.
MIDT = (B / 2, B / 2)
SNIT = [((0, (A + B) / 2), (B, (B - A) / 2)),
        (((B - A) / 2, 0), ((A + B) / 2, B))]
for _p, _q in SNIT:
    assert abs(math.dist(_p, _q) - C) < 1e-9, 'snittet skal have længden c'
    assert abs((_p[0] + _q[0]) / 2 - MIDT[0]) < 1e-9
    assert abs((_p[1] + _q[1]) / 2 - MIDT[1]) < 1e-9
_u = ((SNIT[0][1][0] - SNIT[0][0][0]), (SNIT[0][1][1] - SNIT[0][0][1]))
_v = ((SNIT[1][1][0] - SNIT[1][0][0]), (SNIT[1][1][1] - SNIT[1][0][1]))
assert abs(_u[0] * _v[0] + _u[1] * _v[1]) < 1e-9, 'snittene skal være vinkelrette'
# Det ene snit er parallelt med den lange side i trekanten fra A.
assert abs(_u[0] * (PB[1] - PA[1]) - _u[1] * (PB[0] - PA[0])) < 1e-9

BRIK = [(0, 0), (A / 2, B / 2), (B / 2, B / 2), (B / 2, -A / 2)]
assert abs(_areal(BRIK) - B * B / 4) < 1e-9, 'brikken er en fjerdedel af b²'


def _drej(p, k):
    x, y = p[0] - C / 2, p[1] - C / 2
    for _ in range(k):
        x, y = -y, x
    return (x + C / 2, y + C / 2)


def _lagt():
    """De fire brikker og det lille kvadrat, lagt ind i c-kvadratet. Det
    rette hjoerne i hver brik - kvadratets midte - lander i et hjoerne af
    c-kvadratet, og de to kanter paa c/2 falder langs siderne."""
    r = ((-B / C, A / C), (-A / C, -B / C))
    grund = [(r[0][0] * x + r[0][1] * y + C, r[1][0] * x + r[1][1] * y + C)
             for x, y in BRIK]
    stykker = [[_drej(p, k) for p in grund] for k in range(4)]
    stykker.append([_drej(grund[2], k) for k in range(4)])
    return stykker


LAGT = _lagt()
assert abs(sum(_areal(s) for s in LAGT) - C * C) < 1e-9
assert abs(math.dist(LAGT[4][0], LAGT[4][1]) - A) < 1e-9, 'midterkvadratet'
# Og saa den rigtige proeve: daekker de fem stykker c-kvadratet praecis én
# gang? Et areal, der stemmer, er ikke nok - stykkerne kan overlappe.
_fejl = sum(1 for i in range(120) for j in range(120)
            if sum(_inde(((i + 0.3183) * C / 120, (j + 0.7071) * C / 120), s)
                   for s in LAGT) != 1)
assert _fejl == 0, f'{_fejl} punkter er ikke dækket præcis én gang'


def perigalkvadrat():
    d = [f'<rect x="0" y="0" width="{B}" height="{B}" {KLIP}/>']
    for (x1, y1), (x2, y2) in SNIT:
        d.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" {KLIP}/>')
    return svg(''.join(d), [(0, 0), (B, B)])


def lillekvadrat():
    return svg(f'<rect x="0" y="0" width="{A}" height="{A}" {KLIP}/>',
               [(0, 0), (A, A)])


def samlet():
    """Facit til C: de fem stykker lagt paa plads."""
    fyld = [LYS, FLAPF, LYS, FLAPF, '#dbe6f7']
    d = [f'<rect x="0" y="0" width="{C}" height="{C}" {KLIP}/>']
    for s, f in zip(LAGT, fyld):
        d.append(_poly(s, fyld=f, bredde=0.4))
    return svg(''.join(d), [(0, 0), (C, C)])


# ------------------------------------------------------------------- teksten
TRIN = [
 ('A', 'Tre kvadrater', [
   'Tæl ternene i de to kvadrater, der ligger lige. Skriv tallene ned.',
   'Klip det skrå kvadrat ud. Dets tern kan ikke tælles — det ligger skævt.',
   'Læg det oven på ternkvadratet ved siden af.'],
  'Hvor mange tern dækker det skrå kvadrat?',
  ['Hvor mange tern er der i de to andre kvadrater tilsammen?',
   'Hvilke tre tal er sidelængderne i trekanten?',
   'Hvorfor kunne du ikke bare tælle ternene i det skrå kvadrat?'],
  'Så hvad gælder der om de tre kvadrater?'),

 ('B', 'Rammen', [
   'Klip de fire trekanter ud. De er helt ens.',
   'Læg alle fire ind i rammen, så der bliver <b>to</b> firkantede huller '
   'tilbage. Mål hullerne.',
   'Flyt de samme fire trekanter, så der kun bliver <b>ét</b> hul. Mål det.'],
  'Hvor store er hullerne i de to opstillinger?',
  ['Rammen er den samme, og trekanterne er de samme. Hvad må der så gælde '
   'om hullerne tilsammen?',
   'Sig det med ord: de to huller tilsammen er lige så store som …',
   'Brugte du nogen steder, at siderne lige netop var 3, 4 og 5?'],
  'Så hvorfor må de to små kvadrater give det store?'),

 ('C', 'De to kvadrater bliver til ét', [
   'Klip det store kvadrat ud, og klip det i fire langs de to streger.',
   'Klip det lille kvadrat ud. Nu har du fem stykker.',
   'Læg dem alle fem ind i ternkvadratet fra A, så det er helt fyldt.'],
  'Hvor meget papir var der i de to kvadrater tilsammen?',
  ['Hvor meget papir er der i ternkvadratet?',
   'Blev der mere eller mindre papir, da du klippede?',
   'Hvor endte det lille kvadrat — og hvordan ligger det?'],
  'Så hvad sker der, hvis man lægger de to små kvadrater sammen?'),
]

REGN = [
 'En retvinklet trekant har de to korte sider 6 cm og 8 cm. Hvor lang er '
 'den lange side?',
 'Et rektangel er 12 cm langt og 5 cm bredt. Hvor lang er diagonalen?',
 'En stige er 5 m lang og står 1,5 m fra muren. Hvor højt op når den?',
 'En trekant har siderne 9 cm, 12 cm og 15 cm. Er den retvinklet?',
 'Hvor lang er diagonalen i et kvadrat med siden 10 cm?',
]

_stige = math.sqrt(5 ** 2 - 1.5 ** 2)
_diag = math.sqrt(2 * 10 ** 2)
assert abs(math.hypot(6, 8) - 10) < 1e-9
assert abs(math.hypot(5, 12) - 13) < 1e-9
assert 9 ** 2 + 12 ** 2 == 15 ** 2
SVAR_REGN = [
 '10 cm',
 '13 cm',
 f'{kom(_stige)} m',
 'Ja. 9² + 12² = 81 + 144 = 225, og 15² = 225',
 f'{kom(_diag)} cm',
]

SVAR = [
 ('A', f'<b>{C//TERN*(C//TERN)} tern.</b> De to andre er '
       f'{A//TERN}·{A//TERN} = {A*A//100} og {B//TERN}·{B//TERN} = '
       f'{B*B//100}, og {A*A//100} + {B*B//100} = {C*C//100}. Siderne er '
       f'{A//TERN}, {B//TERN} og {C//TERN} cm. Det skrå kvadrat kan ikke '
       'tælles, fordi ingen af dets sider følger ternene — og dét er netop '
       'grunden til, at der skal en saks til.'),
 ('B', f'I den første opstilling er hullerne {A//TERN}·{A//TERN} og '
       f'{B//TERN}·{B//TERN}, i den anden ét hul på {C//TERN}·{C//TERN}. '
       'Rammen er den samme, og de fire trekanter fylder det samme — så '
       'hullerne må være lige store. '
       '<b>Her står beviset.</b> Argumentet bruger ingen steder, at '
       'siderne er 3, 4 og 5: rammen er (a + b) på hver led, uanset hvad a '
       'og b er. A og C viser, at det passer for netop denne trekant; B '
       'viser hvorfor det gælder for dem alle.'),
 ('C', 'De fem stykker fylder ternkvadratet præcis. Papiret bliver '
       'hverken mere eller mindre, når man klipper, så de to små kvadrater '
       '<i>er</i> det store. Det lille kvadrat ender i midten — drejet, så '
       'dets sider er parallelle med trekantens lange side. Det er ikke '
       'tilfældigt: de to snit er lagt parallelt med og vinkelret på netop '
       'den side.'),
]

_AREAL = open(os.path.join(ROD, 'claude', 'byg_klip_areal.py'),
              encoding='utf-8').read()
_i = _AREAL.index("CSS = '''") + 9
CSS = _AREAL[_i:_AREAL.index("\n'''", _i)] + '''
.net{border:0.3mm dashed #c9d2e0;border-radius:2mm;padding:2mm;
display:inline-block;margin:0 2mm 0 0;vertical-align:top;font-size:10.5pt;
page-break-inside:avoid}
/* Mellemrummet mellem to inline-block'e taeller med i bredden. Uden
   font-size:0 paa raekken skubbede det rammen og trekanterne fra hinanden,
   og de to figurer havnede paa hver sin side. */
.rad{font-size:0;margin:0 0 1mm}
.ny{page-break-before:always}
.hvad{color:#333;margin:0 0 2mm;max-width:150mm;font-size:9.5pt}
h1.smal{font-size:16pt;margin:0 0 3mm}
h2{margin:3mm 0 1mm}
'''

KLIPARK = (
 '<h1 class="smal">Klip Pythagoras fri</h1>'
 '<h2 style="margin-top:0">A · Tre kvadrater</h2>'
 '<p class="hvad">Trekanten har en ret vinkel. De to kvadrater, der ligger '
 'lige, kan du tælle. Det skrå kan du ikke — klip det ud, og læg det oven '
 'på ternkvadratet. Gem ternkvadratet bagefter; det skal bruges igen i C.'
 '</p>'
 f'<div class="rad"><div class="net">{tre_kvadrater()}</div>'
 f'<div class="net">{ternkvadrat()}</div></div>'
 '<h2>B · Rammen</h2>'
 '<p class="hvad">Fire helt ens trekanter og én ramme. Alle fire skal ligge '
 'inde i rammen uden at overlappe — og det kan lade sig gøre på mere end én '
 'måde. Rammen skal ikke klippes ud.</p>'
 f'<div class="rad"><div class="net">{ramme()}</div>'
 f'<div class="net">{fire_trekanter()}</div></div>'
 '<div class="ny"></div>'
 '<h2 style="margin-top:0">C · De to kvadrater bliver til ét</h2>'
 '<p class="hvad">Klip begge kvadrater ud, og klip det store i fire langs '
 'de to streger. De fem stykker skal fylde ternkvadratet fra A helt ud.</p>'
 f'<div class="rad"><div class="net">{perigalkvadrat()}</div>'
 f'<div class="net">{lillekvadrat()}</div></div>'
 '<footer>Figurerne er trykt i rigtig størrelse. Printes arket forminsket, '
 'passer brikkerne ikke i rammen, og øvelsen falder.</footer>')


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
          '<p class="lead">Det her kan ikke afgøres ved at se på det. '
          'Kvadratet på den lange side ligger skævt, og skæve ting kan ikke '
          'tælles — de kan klippes ud og lægges oven på. Mål og tæl, mens '
          'du klipper.</p>' + trin_html()
          + '<h2>Regn videre</h2>'
            '<p style="color:#333;margin:0 0 2mm">Nu har du reglen, du selv '
            'har klippet frem. Tegn en skitse til hver opgave først.</p>'
            f'<table class="regn"><tbody>{regn_html}</tbody></table>'
            '<footer>Husk, at den lange side altid er den, der ligger over '
            'for den rette vinkel — ikke bare den, der ser længst ud.'
            '</footer>')

svar_html = ''.join(
    f'<div class="gr"><div class="bogstav">{b}</div><div>'
    f'<p style="margin:0">{t}</p></div></div>' for b, t in SVAR)
svar_regn_html = ''.join(
    f'<tr><td class="nr">{i}</td><td>{REGN[i-1]}</td>'
    f'<td class="plads"><b>{s}</b></td></tr>'
    for i, s in enumerate(SVAR_REGN, 1))

VEJL = (f'<h1>Klip Pythagoras fri · forventede svar</h1>'
        f'<p class="lead">Til den voksne. Arket uddeles uden denne side.</p>'
        f'<div class="boks"><b>Hvad øvelsen gør.</b> Kvadratet på den lange '
        f'side ligger skævt i forhold til ternene. Det er hele pointen: '
        f'arealet kan ikke tælles, kun klippes ud og lægges oven på. '
        f'<b>A</b> og <b>C</b> viser, at det passer for 3-4-5. <b>B</b> '
        f'viser hvorfor det gælder for alle retvinklede trekanter — og det '
        f'er den eneste af de tre, der er et bevis.</div>'
        f'<h2>Hvad de skal nå frem til</h2>{svar_html}'
        f'<h2>B · de to opstillinger</h2>'
        f'<p class="hvad">Samme ramme, samme fire trekanter. Til venstre to '
        f'huller, til højre ét — og lige meget plads i begge.</p>'
        f'<div class="rad"><div class="net">'
        f'{opstilling(OPST1, HUL1, [f"{A//TERN}×{A//TERN}", f"{B//TERN}×{B//TERN}"])}'
        f'</div><div class="net">'
        f'{opstilling(OPST2, HUL2, [f"{C//TERN}×{C//TERN}"])}</div></div>'
        f'<h2>C · de fem stykker på plads</h2>'
        f'<p class="hvad">Det lille kvadrat ligger i midten, drejet. Prøv '
        f'ikke at hjælpe for tidligt — det er en god opgave at sidde fast '
        f'i.</p>'
        f'<div class="net">{samlet()}</div>'
        f'<h2>Regn videre</h2>'
        f'<table class="regn"><tbody>{svar_regn_html}</tbody></table>'
        f'<div class="boks"><b>Det, der driller.</b> De tror, det skrå '
        f'kvadrat kan tælles, og tæller de hele tern og gætter resten — '
        f'det giver {C*C//100 - 1} eller {C*C//100 + 1}, og så er mønstret '
        f'væk. Lad saksen afgøre det. Dernæst: a² læses som a · 2. Og til '
        f'sidst den lange side: i opgave 3 er stigen den lange side, så '
        f'der skal <i>trækkes fra</i>, ikke lægges til.</div>'
        f'<footer>Trekanten er {A//TERN}-{B//TERN}-{C//TERN} cm. Perigals '
        f'to snit er lagt parallelt med og vinkelret på den lange side; '
        f'ligger de anderledes, passer stykkerne ikke. Opdelingen er '
        f'efterregnet: de fem stykker dækker hvert punkt i kvadratet '
        f'præcis én gang.</footer>')


def skriv(navn, krop):
    sti = os.path.join(ROD, navn)
    h = sti.replace('.pdf', '.html')
    os.makedirs(os.path.dirname(sti), exist_ok=True)
    open(h, 'w', encoding='utf-8').write(
        '<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
        '<title>Klip Pythagoras fri</title><style>' + CSS
        + '</style></head><body>' + krop + '</body></html>')
    subprocess.run(['node', os.path.join(ROD, 'claude', 'html_til_pdf.mjs'),
                    h, sti], check=True, stdout=subprocess.DEVNULL)
    os.remove(h)
    print('skrevet: ', sti)


if __name__ == '__main__':
    skriv('materiale/klip-pythagoras-fri.pdf', KLIPARK + ARBEJD)
    skriv('vejledning/klip-pythagoras-fri-svar.pdf', VEJL)
    print(f'trekanten {A//TERN}-{B//TERN}-{C//TERN} cm · '
          f'{A*A//100} + {B*B//100} = {C*C//100} cm²')
