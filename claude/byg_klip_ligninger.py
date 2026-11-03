# -*- coding: utf-8 -*-
"""Bygger materiale/klip-ligninger-fri.pdf og vejledning/…-svar.pdf

Sjette ark i raekken. En ligning er et lighedstegn, og et lighedstegn er
en paastand om, at de to sider vejer det samme. Det kan forklares, og det
kan **laegges paa bordet**: x-brikker og 1-brikker paa to vaegtskaale.
Saa er reglerne ikke regler laengere - de er det eneste, man kan goere,
uden at vaegten tipper.

  A  Vaegten        -> 3x + 2 = 11. Fjern det samme fra begge sider, og
                       del resten i lige store bunker
  B  x paa begge    -> 5x + 1 = 2x + 7. Man maa ogsaa fjerne x-brikker,
     sider            ikke kun tal
  C  Parentesen     -> 2(x + 3) = 14. To ens bunker giver to x-brikker og
                       SEKS 1-brikker. Tretallet bliver ganget med

**x-brikken er med vilje ikke et helt antal 1-brikker lang** (45 mod 18
gaar ikke op). Ellers kan man maale sig til svaret med en lineal i stedet
for at regne det ud, og saa er hele oevelsen spildt.

    python3 claude/byg_klip_ligninger.py
"""
import importlib.util
import os
import subprocess
from fractions import Fraction as F

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HER = os.path.dirname(os.path.abspath(__file__))

_spec = importlib.util.spec_from_file_location(
    'rumfang', os.path.join(HER, 'byg_klip_rumfang.py'))
RF = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(RF)

svg = RF.svg
INK, LIN, BLA, LYS = RF.INK, RF.LIN, RF.BLA, RF.LYS
KLIP = RF.KLIP
PLADS_B = RF.PLADS_B

X_L, X_H = 45, 18               # x-brikken i mm
EN = 18                         # 1-brikken er et kvadrat
ANTAL_X, ANTAL_1 = 8, 20
GAB = 6

X_FYLD, EN_FYLD = '#dbe6f7', '#f4f6fb'

# Hele oevelsens sikring: laengden af x maa IKKE kunne maales i 1-brikker.
assert X_L % EN != 0, 'x-brikken må ikke være et helt antal 1-brikker lang'

LIGNINGER = [
    ('A', (3, 2), (0, 11)),         # 3x + 2 = 11
    ('B', (5, 1), (2, 7)),          # 5x + 1 = 2x + 7
    ('C', (2, 6), (0, 14)),         # 2(x + 3) = 14, pakket ud
]


def _loes(v, h):
    """x ud af (vx, v1) = (hx, h1). Regnes med Fraction, aldrig i hovedet."""
    assert v[0] != h[0], 'ligningen har ikke én løsning'
    return F(h[1] - v[1], v[0] - h[0])


SVAR_X = {b: _loes(v, h) for b, v, h in LIGNINGER}
assert all(x.denominator == 1 for x in SVAR_X.values()), \
    'alle tre svar skal være hele tal — der er kun hele brikker'
assert len(set(SVAR_X.values())) == 3, 'de tre svar skal være forskellige'
for _b, _v, _h in LIGNINGER:
    assert max(_v[0], _h[0]) + min(_v[0], _h[0]) <= ANTAL_X or _b == 'A', _b
    assert _v[1] + _h[1] <= ANTAL_1, f'{_b} kræver flere 1-brikker end arket har'
assert LIGNINGER[1][1][0] + LIGNINGER[1][2][0] <= ANTAL_X


# ------------------------------------------------------------------- brikker
def _brik(x, y, b, h, tekst, fyld, skala=1.0):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{b:.1f}" height="{h:.1f}" '
            f'rx="{2*skala:.1f}" fill="{fyld}" stroke="{INK}" '
            f'stroke-width="{0.5*skala:.2f}"/>'
            f'<text x="{x + b/2:.1f}" y="{y + h/2 + 2.6*skala:.1f}" '
            f'text-anchor="middle" font-size="{8*skala:.1f}" '
            f'font-style="italic" fill="{INK}">{tekst}</text>')


def klippeark():
    """x-brikker foerst, saa 1-brikker. Pakningen regnes, saa intet stikker
    ud over de 184 mm, der er plads til."""
    d, pkt = [], []
    y = 0.0
    pr_raekke = int((PLADS_B - 8 + GAB) // (X_L + GAB))
    for i in range(ANTAL_X):
        r, k = divmod(i, pr_raekke)
        x = k * (X_L + GAB)
        yy = y + r * (X_H + GAB)
        d.append(_brik(x, yy, X_L, X_H, 'x', X_FYLD))
        pkt += [(x, yy), (x + X_L, yy + X_H)]
    raekker = (ANTAL_X + pr_raekke - 1) // pr_raekke
    y += raekker * (X_H + GAB) + GAB
    pr_raekke1 = int((PLADS_B - 8 + GAB) // (EN + GAB))
    for i in range(ANTAL_1):
        r, k = divmod(i, pr_raekke1)
        x = k * (EN + GAB)
        yy = y + r * (EN + GAB)
        d.append(_brik(x, yy, EN, EN, '1', EN_FYLD))
        pkt += [(x, yy), (x + EN, yy + EN)]
    return svg(''.join(d), pkt)


# --------------------------------------------------------------------- vægten
SKAAL_B, SKAAL_H = 80.0, 170.0
GAB_M = 16.0
M_V = 4.0
M_H = M_V + SKAAL_B + GAB_M
TOP = 46.0
MIDT = (M_V + SKAAL_B + M_H) / 2
assert SKAAL_B >= X_L + 6, 'x-brikken kan ikke ligge i vægtskålen'


def vaegt():
    """Underlaget. Det klippes ikke ud - det ligger paa bordet, og
    brikkerne laegges oven paa. Bjaelken og vippen tegnes, fordi det er
    dét, lighedstegnet ER."""
    bx1, bx2 = M_V + SKAAL_B / 2, M_H + SKAAL_B / 2
    d = [f'<line x1="{M_V}" y1="14" x2="{M_H + SKAAL_B}" y2="14" '
         f'stroke="{INK}" stroke-width="2" stroke-linecap="round"/>',
         f'<polygon points="{MIDT},16 {MIDT-7},38 {MIDT+7},38" '
         f'fill="{LYS}" stroke="{INK}" stroke-width="0.6"/>',
         f'<line x1="{MIDT-11}" y1="38" x2="{MIDT+11}" y2="38" '
         f'stroke="{INK}" stroke-width="1.2" stroke-linecap="round"/>']
    for bx in (bx1, bx2):
        d.append(f'<line x1="{bx}" y1="14" x2="{bx}" y2="{TOP}" '
                 f'stroke="{LIN}" stroke-width="1"/>')
    for x, navn in ((M_V, 'VENSTRE SIDE'), (M_H, 'HØJRE SIDE')):
        d.append(f'<rect x="{x}" y="{TOP}" width="{SKAAL_B}" '
                 f'height="{SKAAL_H}" rx="4" fill="none" stroke="{INK}" '
                 f'stroke-width="0.6"/>')
        d.append(f'<text x="{x + SKAAL_B/2}" y="{TOP + 9}" '
                 f'text-anchor="middle" font-size="5" fill="{LIN}" '
                 f'letter-spacing="0.6">{navn}</text>')
    d.append(f'<text x="{MIDT}" y="{TOP + SKAAL_H/2}" text-anchor="middle" '
             f'font-size="16" fill="{BLA}" font-weight="700">=</text>')
    return svg(''.join(d), [(M_V, 0), (M_H + SKAAL_B, TOP + SKAAL_H)])


def _vaegt_lille(ox, vx, v1, hx, h1, note=''):
    """Én lille vaegt med brikker paa, tegnet fra x = ox.

    Brikkerne er smaa og uden bogstav: farven skiller dem ad, og saa
    slipper figuren for tekst i 2 punkt, som ingen kan laese. Skaalens
    hoejde regnes af det, der faktisk ligger i den - ikke af underlagets
    hoejde, for saa blev tre fjerdedele af figuren tom luft.

    Returnerer (tegning, bredde, hoejde), saa flere kan saettes sammen i
    én figur. Hver i sin egen ramme blev for bredt: tre stillinger ved
    siden af hinanden skal kunne vaere paa de 184 mm."""
    en, xl, xh, luft, pr = 6.0, 15.0, 6.0, 1.5, 3
    b = pr * (en + luft) + luft
    gm = 6.0
    assert xl + 2 * luft <= b, 'x-brikken kan ikke være i den lille skål'

    def hoejde(nx, n1):
        return (luft + nx * (xh + luft)
                + ((n1 + pr - 1) // pr) * (en + luft))

    h = max(hoejde(vx, v1), hoejde(hx, h1)) + luft
    top, bredde = 13.0, 2 * b + gm
    d = [f'<line x1="{ox:.1f}" y1="2" x2="{ox + bredde:.1f}" y2="2" '
         f'stroke="{INK}" stroke-width="1" stroke-linecap="round"/>',
         f'<polygon points="{ox + b + gm/2:.1f},3 {ox + b + gm/2 - 3:.1f},10 '
         f'{ox + b + gm/2 + 3:.1f},10" fill="{LYS}" stroke="{INK}" '
         f'stroke-width="0.4"/>']
    for x0, nx, n1 in ((ox, vx, v1), (ox + b + gm, hx, h1)):
        d.append(f'<rect x="{x0:.1f}" y="{top}" width="{b:.1f}" '
                 f'height="{h:.1f}" rx="2" fill="none" stroke="{INK}" '
                 f'stroke-width="0.4"/>')
        y = top + luft
        for _ in range(nx):
            d.append(f'<rect x="{x0 + luft:.1f}" y="{y:.1f}" '
                     f'width="{xl:.1f}" height="{xh:.1f}" rx="1" '
                     f'fill="{X_FYLD}" stroke="{INK}" stroke-width="0.3"/>')
            y += xh + luft
        for i in range(n1):
            r, k = divmod(i, pr)
            d.append(f'<rect x="{x0 + luft + k * (en + luft):.1f}" '
                     f'y="{y + r * (en + luft):.1f}" width="{en:.1f}" '
                     f'height="{en:.1f}" rx="1" fill="{EN_FYLD}" '
                     f'stroke="{INK}" stroke-width="0.3"/>')
        assert y + ((n1 + pr - 1) // pr) * (en + luft) <= top + h + 0.01, \
            'brikkerne kan ikke være i skålen'
    d.append(f'<text x="{ox + b + gm/2:.1f}" y="{top + h/2 + 2:.1f}" '
             f'text-anchor="middle" font-size="7" fill="{BLA}" '
             f'font-weight="700">=</text>')
    if note:
        d.append(f'<text x="{ox + bredde/2:.1f}" y="{top + h + 7:.1f}" '
                 f'text-anchor="middle" font-size="5" fill="{INK}">'
                 f'{note}</text>')
    return ''.join(d), bredde, top + h + 9


def raekke(stillinger, gab=6.0):
    """Flere stillinger i ÉN figur, med pile imellem. Bredden regnes, og
    svg() har en assert paa, at den kan vaere paa papiret."""
    krop, x, hoejder = '', 0.0, []
    for i, st in enumerate(stillinger):
        d, b, h = _vaegt_lille(x, *st)
        krop += d
        hoejder.append(h)
        if i < len(stillinger) - 1:
            px = x + b + gab / 2
            krop += (f'<path d="M{px - 3:.1f},{h/2:.1f} L{px + 3:.1f},'
                     f'{h/2:.1f}" stroke="{LIN}" stroke-width="1.2" '
                     f'marker-end="url(#pil)"/>')
        x += b + gab
    pil = ('<defs><marker id="pil" viewBox="0 0 10 10" refX="7" refY="5" '
           'markerWidth="5" markerHeight="5" orient="auto">'
           f'<path d="M0,0 L10,5 L0,10 z" fill="{LIN}"/></marker></defs>')
    return svg(pil + krop, [(0, 0), (x - gab, max(hoejder))])


# ------------------------------------------------------------------- teksten
TRIN = [
 ('A', 'Vægten', [
   'Læg <b>3 x-brikker og 2 1-brikker</b> på venstre side. Læg '
   '<b>11 1-brikker</b> på højre side. Nu står der 3x + 2 = 11, og de to '
   'sider vejer det samme.',
   'Tag <b>2 1-brikker væk fra venstre side</b>. Nu tipper vægten. Hvad '
   'skal du gøre ved højre side, for at den kommer i balance igen?',
   'Del det, der er tilbage på begge sider, i <b>lige store bunker</b> — '
   'én bunke for hver x-brik.'],
  'Hvor mange 1-brikker er én x-brik værd?',
  ['Hvorfor må du ikke bare fjerne de 2 fra venstre side og lade højre '
   'side ligge?',
   'Hvor mange 1-brikker ligger der i hver bunke til sidst?',
   'Læg dit svar ind i stedet for hver x-brik. Vejer de to sider det '
   'samme nu?'],
  'Så hvad må man gøre ved en ligning, uden at den går i stykker?'),

 ('B', 'x på begge sider', [
   'Læg <b>5 x-brikker og 1 1-brik</b> på venstre side, og <b>2 x-brikker '
   'og 7 1-brikker</b> på højre side. Der står 5x + 1 = 2x + 7.',
   'Fjern <b>2 x-brikker fra begge sider på én gang</b>. Du ved ikke, hvad '
   'en x-brik vejer — men du ved, at de vejer det samme.',
   'Fjern nu 1 1-brik fra begge sider, og del resten i lige store bunker.'],
  'Hvad er x?',
  ['Du fjernede x-brikker og ikke tal. Måtte du det? Hvorfor?',
   'Hvorfor er det smartest at fjerne de x-brikker, der er færrest af?',
   'Læg dit svar ind i stedet for hver x-brik på begge sider. Passer det?'],
  'Så hvordan får man alle x over på den ene side?'),

 ('C', 'Parentesen', [
   'Læg <b>to ens bunker</b> på venstre side. Hver bunke skal have <b>én '
   'x-brik og tre 1-brikker</b>. Det er 2 · (x + 3).',
   'Læg <b>14 1-brikker</b> på højre side.',
   'Tæl nu, hvad der i alt ligger på venstre side. Skriv det <b>uden '
   'parentes</b>, og løs så ligningen som i A.'],
  'Hvor mange x-brikker og hvor mange 1-brikker er 2 · (x + 3)?',
  ['Hvad skete der med 3-tallet, da der kom to bunker?',
   'Hvad ville 3 · (x + 3) være? Læg brikkerne, hvis du er i tvivl.',
   'Hvad er x?'],
  'Så hvad gør man med tallet uden for en parentes?'),
]

REGN = [
 'Løs 4x + 3 = 19',
 'Løs 7x − 2 = 3x + 10',
 'Løs 3(x + 2) = 18',
 'Løs 2(x + 1) = x + 7',
 'Tre ens bøger og en blok til 20 kr koster 170 kr tilsammen. Skriv det '
 'som en ligning, og find prisen på én bog.',
]
_r = [F(19 - 3, 4), F(10 + 2, 7 - 3), F(18 - 6, 3), F(7 - 2, 2 - 1),
      F(170 - 20, 3)]
assert all(x.denominator == 1 for x in _r)
SVAR_REGN = [
 f'x = {_r[0]}',
 f'x = {_r[1]} — træk 3x fra på begge sider, læg 2 til på begge sider',
 f'x = {_r[2]} — parentesen bliver til 3x + 6',
 f'x = {_r[3]} — venstre side bliver 2x + 2, og så trækkes x fra begge sider',
 f'3x + 20 = 170, så x = {_r[4]} kr',
]

SVAR = [
 ('A', f'<b>x = {SVAR_X["A"]}.</b> De 2 1-brikker skal fjernes fra '
       '<i>begge</i> sider, ellers tipper vægten: tilbage står 3x = 9. '
       'Tre lige store bunker giver 3 i hver. '
       '<b>Det er hele reglen:</b> man må gøre hvad som helst ved en '
       'ligning, så længe man gør præcis det samme ved begge sider. Ikke '
       'fordi det står i en bog — fordi vægten ellers tipper.'),
 ('B', f'<b>x = {SVAR_X["B"]}.</b> Fjern 2 x-brikker fra begge sider: '
       'tilbage står 3x + 1 = 7. Fjern 1 fra begge: 3x = 6, altså x = 2. '
       'Man behøver ikke vide, hvad en x-brik vejer, for at fjerne den fra '
       'begge sider — kun at de vejer det samme. Fjern altid den side, der '
       'har <i>færrest</i> x-brikker; så bliver der ingen minus-brikker, '
       'og dem har vi ikke på arket.'),
 ('C', f'<b>2 x-brikker og 6 1-brikker, altså 2x + 6 — og x = '
       f'{SVAR_X["C"]}.</b> Tretallet blev ganget med, fordi der kom to '
       'bunker, og hver bunke havde tre. Det er dét, en parentes er: en '
       'bunke, man tager flere af. Med tre bunker ville det være 3x + 9.'),
]

_AREAL = open(os.path.join(ROD, 'claude', 'byg_klip_areal.py'),
              encoding='utf-8').read()
_i = _AREAL.index("CSS = '''") + 9
CSS = _AREAL[_i:_AREAL.index("\n'''", _i)] + '''
.net{border:0.3mm dashed #c9d2e0;border-radius:2mm;padding:2mm;
display:inline-block;margin:0 2mm 0 0;vertical-align:top;font-size:10.5pt;
page-break-inside:avoid}
.rad{font-size:0;margin:0 0 1mm}
.ny{page-break-before:always}
.hvad{color:#333;margin:0 0 2mm;max-width:150mm;font-size:9.5pt}
h1.smal{font-size:16pt;margin:0 0 3mm}
h2{margin:3mm 0 1mm}
'''

KLIPARK = (
 '<h1 class="smal">Klip ligningen fri</h1>'
 '<p class="hvad">Her er brikkerne. Den lange hedder <b>x</b>, og ingen '
 'ved, hvor meget den vejer — det er lige netop dét, I skal finde ud af. '
 'Den lille hedder <b>1</b>. Klip dem alle ud, og hold de to slags adskilt.'
 '</p>'
 f'<div class="rad"><div class="net">{klippeark()}</div></div>'
 '<p class="hvad" style="margin-top:3mm">Prøv ikke at måle x-brikken med '
 'en lineal. Den går ikke op i 1-brikker — det er med vilje.</p>'
 '<div class="ny"></div>'
 '<h2 style="margin-top:0">Vægten</h2>'
 '<p class="hvad">Den her skal <b>ikke</b> klippes ud. Læg arket på bordet '
 'og brikkerne oven på. Lighedstegnet betyder, at de to sider vejer det '
 'samme — og det skal de blive ved med, hvad du end gør.</p>'
 f'<div class="rad"><div class="net">{vaegt()}</div></div>'
 '<footer>Brikkerne er trykt i rigtig størrelse, så de to slags kan '
 'kendes fra hinanden. Men mål ikke på dem.</footer>')


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
          '<p class="lead">En ligning er ikke en opgave med et '
          'lighedstegn i. Den er en <b>påstand om, at to ting vejer det '
          'samme</b>. Når du har lagt den på vægten, er reglerne ikke '
          'regler længere — de er det eneste, du kan gøre, uden at vægten '
          'tipper.</p>' + trin_html()
          + '<h2>Regn videre</h2>'
            '<p style="color:#333;margin:0 0 2mm">Nu uden brikker. Skriv '
            'ved hvert skridt, hvad du gør ved <i>begge</i> sider.</p>'
            f'<table class="regn"><tbody>{regn_html}</tbody></table>'
            '<footer>Tjek altid til sidst: sæt dit svar ind i den '
            'oprindelige ligning. Giver de to sider det samme, er du '
            'færdig — og du behøver ikke spørge nogen.</footer>')

svar_html = ''.join(
    f'<div class="gr"><div class="bogstav">{b}</div><div>'
    f'<p style="margin:0">{t}</p></div></div>' for b, t in SVAR)
svar_regn_html = ''.join(
    f'<tr><td class="nr">{i}</td><td>{REGN[i-1]}</td>'
    f'<td class="plads"><b>{s}</b></td></tr>'
    for i, s in enumerate(SVAR_REGN, 1))

TRIN_A = [(3, 2, 0, 11, 'som den starter'),
          (3, 0, 0, 9, 'fjern 2 fra begge'),
          (1, 0, 0, 3, 'del i tre bunker')]
TRIN_B = [(5, 1, 2, 7, 'som den starter'),
          (3, 1, 0, 7, 'fjern 2x fra begge'),
          (3, 0, 0, 6, 'fjern 1, del i tre')]
mini_a = f'<div class="net">{raekke(TRIN_A)}</div>'
mini_b = f'<div class="net">{raekke(TRIN_B)}</div>'
mini_c = f'<div class="net">{raekke([(2, 6, 0, 14, "to bunker: 2x + 6")])}</div>'

VEJL = (f'<h1>Klip ligningen fri · forventede svar</h1>'
        f'<p class="lead">Til den voksne. Arket uddeles uden denne side.</p>'
        f'<div class="boks"><b>Hvad øvelsen gør.</b> Reglerne for at løse '
        f'ligninger er lette at lære udenad og lige så lette at glemme, '
        f'fordi de ikke ligner noget. På en vægt er de ikke regler: de er '
        f'det eneste, man kan gøre. Fjerner du noget fra den ene side '
        f'alene, tipper den — og det kan ses, ikke bare siges.</div>'
        f'<h2>Hvad de skal nå frem til</h2>{svar_html}'
        f'<div class="ny"></div>'
        f'<h2 style="margin-top:0">Sådan ser de tre opgaver ud på vægten</h2>'
        f'<p class="hvad">Blå brikker er <b>x</b>, grå er <b>1</b>.</p>'
        f'<p class="hvad" style="margin:3mm 0 1mm"><b>A · 3x + 2 = 11</b></p>'
        f'<div class="rad">{mini_a}</div>'
        f'<p class="hvad" style="margin:4mm 0 1mm">'
        f'<b>B · 5x + 1 = 2x + 7</b></p>'
        f'<div class="rad">{mini_b}</div>'
        f'<p class="hvad" style="margin:4mm 0 1mm">'
        f'<b>C · 2(x + 3) = 14</b></p>'
        f'<div class="rad">{mini_c}</div>'
        f'<div class="ny"></div><h2 style="margin-top:0">Regn videre</h2>'
        f'<table class="regn"><tbody>{svar_regn_html}</tbody></table>'
        f'<div class="boks"><b>Det, der driller.</b> De fjerner fra den '
        f'ene side og glemmer den anden — lad vægten tippe, og spørg hvad '
        f'der skete. De vil måle x-brikken; den går med vilje ikke op i '
        f'1-brikker. Og de deler kun den ene side i bunker. '
        f'<b>Minus har arket ikke.</b> Der er ingen negative brikker, og '
        f'derfor skal der altid fjernes fra den side, der har færrest '
        f'x-brikker. Den dag minus skal med, er det den samme vægt — bare '
        f'med brikker, der trækker op.</div>'
        f'<footer>x-brikken er {X_L} × {X_H} mm og 1-brikken '
        f'{EN} × {EN} mm. {X_L} går ikke op i {EN}: det er bevidst, så '
        f'svaret ikke kan måles med en lineal. Arket har {ANTAL_X} '
        f'x-brikker og {ANTAL_1} 1-brikker — lige præcis nok til alle tre '
        f'opgaver.</footer>')


def skriv(navn, krop):
    sti = os.path.join(ROD, navn)
    h = sti.replace('.pdf', '.html')
    os.makedirs(os.path.dirname(sti), exist_ok=True)
    open(h, 'w', encoding='utf-8').write(
        '<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
        '<title>Klip ligningen fri</title><style>' + CSS
        + '</style></head><body>' + krop + '</body></html>')
    subprocess.run(['node', os.path.join(ROD, 'claude', 'html_til_pdf.mjs'),
                    h, sti], check=True, stdout=subprocess.DEVNULL)
    os.remove(h)
    print('skrevet: ', sti)


if __name__ == '__main__':
    skriv('materiale/klip-ligninger-fri.pdf', KLIPARK + ARBEJD)
    skriv('vejledning/klip-ligninger-fri-svar.pdf', VEJL)
    print(' · '.join(f'{b}: x = {SVAR_X[b]}' for b, _, _ in LIGNINGER)
          + f' · {ANTAL_X} x-brikker og {ANTAL_1} 1-brikker')
