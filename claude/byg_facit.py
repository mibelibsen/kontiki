# -*- coding: utf-8 -*-
"""Bygger facitlisterne til forloebet Funktioner og ligninger.

Facitlisterne fandtes kun som faerdige PDF'er uden kilde. Da det viste sig,
at koordinatsystemerne havde ulige skala paa akserne, kunne de ikke bygges
om - de maatte skrives her foerst. Nu er indholdet kode, figurerne kommer fra
figurer.py, og hvert svar regnes efter med broekregning, foer filen skrives.

    python3 claude/byg_facit.py            bygger alle
    python3 claude/byg_facit.py grafer     bygger dem, hvis navn indeholder ordet

Facit maa aldrig udgives. Filerne skrives i facit/, som er udelukket i
.vercelignore, og sendes i Code.
"""
import os
import subprocess
import sys
import tempfile
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figurer as FG

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UD = os.path.join(ROD, 'facit')

UGEDAG = ['mandag', 'tirsdag', 'onsdag', 'torsdag', 'fredag', 'lørdag', 'søndag']
MAANED = ['januar', 'februar', 'marts', 'april', 'maj', 'juni', 'juli',
          'august', 'september', 'oktober', 'november', 'december']


def dansk_dato(iso):
    import datetime
    d = datetime.date.fromisoformat(iso)
    return f'{UGEDAG[d.weekday()]} den {d.day}. {MAANED[d.month - 1]} {d.year}'


# ---------------------------------------------------------------------------
# Skabelon - selvbaerende A4-side, al CSS inline
# ---------------------------------------------------------------------------
CSS = '''
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,
  Helvetica,Arial,sans-serif;color:#1a2233;line-height:1.5;background:#fff}
.ark{max-width:820px;margin:0 auto;padding:22px 22px 30px}
h1{font-size:1.3rem;line-height:1.28;margin:0 0 5px}
.meta{color:#586074;font-size:.88rem;margin:0 0 2px}
.hoerer{color:#586074;font-size:.88rem;margin:0 0 18px}
h2{font-size:1.05rem;margin:16px 0 7px;padding-bottom:4px;border-bottom:2px solid #1f6fd6}
h3{font-size:.98rem;margin:16px 0 6px}
p{margin:0 0 9px}
table{width:100%;border-collapse:collapse;margin:0 0 10px}
th,td{border:1px solid #cfd6e4;padding:5px 8px;text-align:left;vertical-align:top;
  font-size:.9rem}
th{background:#f4f6fb;font-weight:700}
td.sv{font-weight:700;color:#12633f;white-space:nowrap}
table.vt{width:auto;margin:0 0 10px}
table.vt th{width:34px;text-align:center}
table.vt td{width:44px;text-align:center;font-weight:700}
code{font-family:"Cambria Math",Georgia,serif;background:#f4f6fb;padding:0 4px;
  border-radius:4px;border:1px solid #e0e5ef}
.figur{margin:10px 0 12px;break-inside:avoid;page-break-inside:avoid}
.figur svg{display:block;width:100%;max-width:340px;margin:0 auto;height:auto;
  background:#fff;border:1px solid #cfd6e4;border-radius:8px}
.figtekst{color:#586074;font-size:.86rem;margin:6px 0 0;text-align:center}
.note{background:#f4f6fb;border:1px solid #d3dae7;border-left:4px solid #1f6fd6;
  border-radius:7px;padding:9px 13px;margin:9px 0 14px;font-size:.9rem;color:#374151}
.note p:last-child{margin:0}
footer{color:#586074;font-size:.78rem;margin-top:24px;border-top:1px solid #e0e5ef;
  padding-top:9px}
@page{size:A4;margin:14mm}
@media print{
  body{font-size:9.8pt}
  .ark{padding:0}
  h2{break-after:avoid}
  .figur svg{max-width:270px;-webkit-print-color-adjust:exact;print-color-adjust:exact}
}
'''


def side(titel, meta, hoerer, blokke):
    krop = []
    for slags, data in blokke:
        if slags == 'h2':
            krop.append(f'<h2>{data}</h2>')
        elif slags == 'h3':
            krop.append(f'<h3>{data}</h3>')
        elif slags == 'p':
            krop.append(f'<p>{data}</p>')
        elif slags == 'note':
            krop.append('<div class="note">'
                        + ''.join(f'<p>{t}</p>' for t in data) + '</div>')
        elif slags == 'figur':
            svg, tekst = data
            krop.append(f'<div class="figur">{svg}'
                        f'<p class="figtekst">{tekst}</p></div>')
        elif slags == 'vaerditabel':
            x_, y_ = data
            krop.append(
                '<table class="vt"><tr><th>x</th>'
                + ''.join(f'<td>{v}</td>' for v in x_) + '</tr><tr><th>y</th>'
                + ''.join(f'<td>{v}</td>' for v in y_) + '</tr></table>')
        elif slags == 'tabel':
            r = ['<table><tr><th>Opgave</th><th>Svar</th><th>Udregning</th></tr>']
            for opg, svar, udr in data:
                r.append(f'<tr><td>{opg}</td><td class="sv">{svar}</td>'
                         f'<td>{udr}</td></tr>')
            krop.append(''.join(r) + '</table>')
        else:
            raise ValueError(slags)
    return (f'<!DOCTYPE html>\n<html lang="da">\n<head>\n<meta charset="UTF-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            f'<title>{titel}</title>\n<style>{CSS}</style>\n</head>\n<body>\n'
            f'<div class="ark">\n<h1>{titel}</h1>\n'
            f'<p class="meta">{meta}</p>\n<p class="hoerer">{hoerer}</p>\n'
            + '\n'.join(krop)
            + '\n<footer>Facitliste · må ikke udgives på sitet · '
              '9. klasse matematik · Mibelibsen</footer>\n</div>\n</body>\n</html>\n')


# ---------------------------------------------------------------------------
# Efterregning - intet svar skrives ned uden at vaere kontrolleret
# ---------------------------------------------------------------------------
def proev(venstre, hoejre, x):
    """Saetter x ind i begge sider og kraever, at de giver det samme."""
    v, h = venstre(F(x)), hoejre(F(x))
    assert v == h, f'x = {x} giver {v} mod {h}'
    return x


def forskrift(p1, p2):
    """Haeldning og skaering gennem to punkter - regnet, ikke aflaest."""
    (x1, y1), (x2, y2) = (F(p1[0]), F(p1[1])), (F(p2[0]), F(p2[1]))
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1
    return a, b


def nulpunkt(a, b):
    assert a != 0
    return -F(b) / F(a)


def skaering(a1, b1, a2, b2):
    x = (F(b2) - F(b1)) / (F(a1) - F(a2))
    return x, F(a1) * x + F(b1)


def dk(x):
    """Dansk talskrivning: komma, og minus som rigtigt minustegn."""
    x = F(x)
    if x.denominator == 1:
        t = str(x.numerator)
    else:
        v = float(x)
        t = f'{v:.4f}'.rstrip('0').rstrip('.').replace('.', ',')
    return t.replace('-', '−')


# ---------------------------------------------------------------------------
# Opgavernes tal - samlet ét sted, saa figur, tabel og tekst ikke kan skride
# ---------------------------------------------------------------------------
# Modul 1, Opgave A - de syv ligninger
M1A = [
    ('x − 9 = 4', 13, 'Læg 9 til på begge sider', lambda x: x - 9, lambda x: 4),
    ('3x + 7 = 22', 5, '3x = 15, divider med 3', lambda x: 3*x + 7, lambda x: 22),
    ('6x − 2x + 5 = 21', 4, 'Reducer: 4x + 5 = 21, så 4x = 16',
     lambda x: 6*x - 2*x + 5, lambda x: 21),
    ('5(x − 2) = 25', 7, 'Divider med 5: x − 2 = 5', lambda x: 5*(x - 2), lambda x: 25),
    ('x/3 − 2 = 4', 18, 'x/3 = 6, gang med 3', lambda x: x/3 - 2, lambda x: 4),
    ('7x + 4 = 3x + 24', 5, 'Træk 3x fra: 4x + 4 = 24, så 4x = 20',
     lambda x: 7*x + 4, lambda x: 3*x + 24),
    ('3(x + 4) = 5(x − 2)', 11, 'Gang ud: 3x + 12 = 5x − 10, så 22 = 2x',
     lambda x: 3*(x + 4), lambda x: 5*(x - 2)),
]

# Uge 38, Opgave A - de seks ligninger
U38A = [
    ('x − 5 = 11', 16, 'Læg 5 til', lambda x: x - 5, lambda x: 11),
    ('4x + 3 = 27', 6, '4x = 24', lambda x: 4*x + 3, lambda x: 27),
    ('5x − 2x + 7 = 28', 7, 'Reducer: 3x + 7 = 28, så 3x = 21',
     lambda x: 5*x - 2*x + 7, lambda x: 28),
    ('2x + 9 = 5x − 6', 5, 'Træk 2x fra: 9 = 3x − 6, så 3x = 15',
     lambda x: 2*x + 9, lambda x: 5*x - 6),
    ('x/5 + 4 = 9', 25, 'x/5 = 5, gang med 5', lambda x: x/5 + 4, lambda x: 9),
    ('6(x − 3) = 30', 8, 'Divider med 6: x − 3 = 5', lambda x: 6*(x - 3), lambda x: 30),
]

# Uge 39 - parenteser, broeker og CAS
U39A = [
    ('3(x − 4) = 2(x + 1)', 14, '3x − 12 = 2x + 2  → x = 14',
     lambda x: 3*(x - 4), lambda x: 2*(x + 1)),
    ('4(x + 2) − 3 = 2x + 15', 5, '4x + 5 = 2x + 15  → 2x = 10',
     lambda x: 4*(x + 2) - 3, lambda x: 2*x + 15),
    ('5(x − 1) − 2(x + 3) = 7', 6, '5x − 5 − 2x − 6 = 7  → 3x = 18',
     lambda x: 5*(x - 1) - 2*(x + 3), lambda x: 7),
]
U39B = [
    ('(x + 4)/3 = 5', 11, 'Gang med 3: x + 4 = 15', lambda x: (x + 4)/3, lambda x: 5),
    ('2x/5 − 1 = 3', 10, '2x/5 = 4, gang med 5: 2x = 20',
     lambda x: 2*x/5 - 1, lambda x: 3),
    ('x/2 + x/3 = 10', 12, 'Gang med 6: 3x + 2x = 60  → 5x = 60',
     lambda x: x/2 + x/3, lambda x: 10),
]

for raekke in (M1A, U38A, U39A, U39B):
    for _, svar, _, v, h in raekke:
        proev(v, h, svar)
proev(lambda x: 7*(x - 2), lambda x: 3*(x + 6), 8)       # uge 39, opgave C


# --- lineaere funktioner: hver haeldning og hvert nulpunkt regnes ----------
M2 = {
    'a1': forskrift((2, 5), (6, 17)),        # y = 3x − 1
    'a2': forskrift((-1, 8), (3, -4)),       # y = −3x + 5
}
assert M2['a1'] == (3, -1) and M2['a2'] == (-3, 5), M2
assert nulpunkt(3, -1) == F(1, 3) and nulpunkt(-3, 5) == F(5, 3)

M3 = {'skaering': skaering(2, -3, -1, 6)}
assert M3['skaering'] == (3, 3), M3
assert nulpunkt(2, -3) == F(3, 2) and nulpunkt(-1, 6) == 6

U41 = {
    'a1': forskrift((1, 4), (5, 16)),        # y = 3x + 1
    'a2': forskrift((-2, 9), (2, 1)),        # y = −2x + 5
    'skaering': skaering(1, 1, -2, 7),       # (2, 3)
}
assert U41['a1'] == (3, 1) and U41['a2'] == (-2, 5), U41
assert nulpunkt(3, 1) == F(-1, 3) and nulpunkt(-2, 5) == F(5, 2)
assert U41['skaering'] == (2, 3)
assert nulpunkt(1, 1) == -1 and nulpunkt(-2, 7) == F(7, 2)
assert nulpunkt(-1, 4) == 4
TABEL_C = [(x, -x + 4) for x in range(-1, 6)]
assert [y for _, y in TABEL_C] == [5, 4, 3, 2, 1, 0, -1], TABEL_C

# --- tekstopgaverne: hver ligning loeses, ikke gaettes ---------------------
assert proev(lambda m: 40 + 12*m, lambda m: 160, 10) == 10          # taxa
assert skaering(3, 60, 1, 120) == (30, 150)                          # abonnement
assert proev(lambda x: x + (x+1) + (x+2), lambda x: 96, 31) == 31    # tre tal
assert proev(lambda b: b + (b+5), lambda b: 23, 9) == 9              # rektangel
assert proev(lambda m: 150 + 85*m, lambda m: 745, 7) == 7            # fitnesskort
assert skaering(45, 1200, 25, 1800) == (30, 2550)                    # cykler
assert proev(lambda x: 4*x + 6, lambda x: 102, 24) == 24             # fire tal
assert proev(lambda x: x + 2*x + (x+6), lambda x: 54, 12) == 12      # trekant
for ant, pris in ((40, 3000), (40, 2800)):
    pass
assert 1200 + 45*40 == 3000 and 1800 + 25*40 == 2800
assert 60 + 3*40 == 180 and 120 + 1*40 == 160


# ---------------------------------------------------------------------------
# De syv facitlister
# ---------------------------------------------------------------------------
def r_ligninger(raekke, bogstaver='abcdefghij'):
    return [(f'{bogstaver[i]}) <code>{opg}</code>', f'x = {dk(svar)}', udr)
            for i, (opg, svar, udr, _, _) in enumerate(raekke)]


def graf(linjer, punkter=(), **kw):
    return FG.koordinatsystem(linjer=linjer, punkter=punkter, **kw)


DOKUMENTER = []


def dok(navn, serie, dato, emne, hoerer, blokke):
    titel = (f'Facitliste{" lektier" if serie == "lektier" else ""} Matematik '
             f'{dansk_dato(dato)} {emne} facitliste')
    if serie == 'lektier':
        meta = f'Lektien er givet {dansk_dato(dato)} · 9. klasse · Mibelibsen'
    else:
        meta = (f'Modulets opgaver · gennemgås {dansk_dato(dato)} · '
                f'9. klasse · Mibelibsen')
    DOKUMENTER.append((navn, side(titel, meta, f'Hører til: {hoerer}', blokke)))


# --- 1. Modul 1, Opgave A - Ligninger -------------------------------------
dok('facit-online-2026-09-14-ligninger', 'online', '2026-09-14', 'Ligninger',
    'Funktioner og ligninger, modul 1 · Opgave A', [
    ('h2', 'Opgave A · Løs ligningerne'),
    ('tabel', r_ligninger(M1A)),
    ('figur', (FG.vaegt(3, 7, 22),
               'Opgave b som vægt. Fjern 7 lodder på begge sider, så står 3 kasser '
               'over for 15 lodder — og hver kasse vejer 5. De fire tilladte træk er '
               'præcis dem, der holder vægten i balance.')),
    ('h3', 'h) Prøve'),
    ('p', 'Prøven er ikke pynt — den fanger fortegnsfejl. Tre eksempler:'),
    ('tabel', [
        ('d) <code>5(x − 2) = 25</code>', '✔', '5(7 − 2) = 5 · 5 = 25'),
        ('f) <code>7x + 4 = 3x + 24</code>', '✔', '7 · 5 + 4 = 39 og 3 · 5 + 24 = 39'),
        ('g) <code>3(x + 4) = 5(x − 2)</code>', '✔', '3(11 + 4) = 45 og 5(11 − 2) = 45'),
    ]),
    ('note', ['Typisk fejl i g): at glemme minusset, når 5 ganges ind i '
              '<code>(x − 2)</code>. Bliver det til <code>5x + 10</code>, får ungen '
              '<code>x = −1</code> — og prøven afslører det med det samme.']),
])

# --- 2. Modul 1, Opgave B - Fra tekst til ligning --------------------------
dok('facit-online-2026-09-21-tekst-til-ligning', 'online', '2026-09-21',
    'Fra tekst til ligning', 'Funktioner og ligninger, modul 1 · Opgave B', [
    ('h2', 'Opgave B · Fra tekst til ligning'),
    ('p', 'Det vigtigste er at skrive, hvad <code>x</code> står for. Uden det er '
          'ligningen ikke til at kontrollere.'),
    ('tabel', [
        ('a) Taxa', '10 km', '<code>x</code> = antal km. 40 + 12x = 160 → 12x = 120'),
        ('b) Abonnement', '30 GB', '60 + 3x = 120 + x → 2x = 60'),
        ('c) Tre tal', '31, 32 og 33', 'x + (x+1) + (x+2) = 96 → 3x + 3 = 96'),
        ('d) Rektangel', '9 cm og 14 cm', 'Halv omkreds: b + (b+5) = 23 → 2b = 18'),
    ]),
    ('figur', (graf([(3, 60, FG.BLA, 'A: 60 + 3x'), (1, 120, FG.GRO, 'B: 120 + x')],
                    [(30, 150, FG.ROD, '(30, 150)')],
                    xmin=0, xmax=60, ymin=0, ymax=260,
                    titel='Abonnement A og B', ens=False),
               'Opgave b tegnet. De to linjer skærer hinanden ved 30 GB, hvor begge '
               'koster 150 kr. Til venstre for skæringen er A billigst, til højre er B. '
               'Ved 40 GB koster A 180 kr og B 160 kr — så B er billigst. '
               'Akserne har hver sin enhed, GB mod kroner, så de kan ikke have '
               'samme skala.')),
    ('note', ['Til d): en hyppig fejl er at sætte <code>b + (b+5) = 46</code> med hele '
              'omkredsen. Omkredsen tæller hver side to gange, så der skal deles med 2 '
              'først. Kontrollen er nem: 2(9 + 14) = 46.']),
    ('h3', 'e) Egen tekstopgave'),
    ('p', 'Ingen facitliste. Godkend opgaven, hvis den kan oversættes til en ligning '
          'med <code>x = 7</code> som løsning, og det fremgår, hvad <code>x</code> '
          'betyder.'),
])

# --- 3. Modul 2, Opgave C - Lineaere funktioner ----------------------------
dok('facit-online-2026-10-05-lineaere-funktioner', 'online', '2026-10-05',
    'Lineære funktioner', 'Funktioner og ligninger, modul 2 · Opgave C', [
    ('h2', 'Opgave C · Find forskriften'),
    ('tabel', [
        ('a) Hældning gennem <code>(2, 5)</code> og <code>(6, 17)</code>', 'a = 3',
         '(17 − 5) ÷ (6 − 2) = 12 ÷ 4'),
        ('b) Hele forskriften', 'y = 3x − 1', 'Sæt (2, 5) ind: 5 = 3·2 + b → b = −1'),
        ('c) Nulpunkt', 'x = 1/3', '3x − 1 = 0 → x = 1/3 ≈ 0,33'),
        ('d) Gennem <code>(−1, 8)</code> og <code>(3, −4)</code>', 'y = −3x + 5',
         'a = (−4 − 8) ÷ (3 + 1) = −3 ; 8 = −3·(−1) + b → b = 5'),
        ('d) Nulpunkt', 'x = 5/3', '−3x + 5 = 0 → x = 5/3 ≈ 1,67'),
        ('e) Stejlest', 'y = −3x + 1',
         'Sammenlign talværdien: |−3| = 3 er større end |2| = 2'),
    ]),
    ('figur', (graf([(3, -1, FG.BLA, 'y = 3x − 1'), (-3, 5, FG.GRO, 'y = −3x + 5')],
                    [(F(1, 3), 0, FG.BLA, ''), (F(5, 3), 0, FG.GRO, '')],
                    xmin=-4, xmax=6, ymin=-4, ymax=6,
                    titel='De to linjer og deres nulpunkter'),
               'Punkt f er den blå linje. Nulpunkterne er de steder, hvor linjerne '
               'skærer x-aksen — den blå ved x = 1/3, den grønne ved x = 5/3. '
               'Ternene er kvadratiske, så hældningen kan måles direkte: begge linjer '
               'flytter sig 3 op eller ned for hvert skridt til højre.')),
    ('note', ['Til e): ungerne svarer ofte "y = 2x + 7, for 2 er større end −3". '
              'Hældningens fortegn siger, om linjen går op eller ned; det er '
              'talværdien, der siger hvor stejl den er.']),
])

# --- 4. Modul 3, Opgave D - Aflaesning af grafer ---------------------------
dok('facit-online-2026-10-05-grafer', 'online', '2026-10-05',
    'Aflæsning af grafer', 'Funktioner og ligninger, modul 3 · Opgave D', [
    ('h2', 'Opgave D · Aflæs og regn efter'),
    ('figur', (graf([(2, -3, FG.BLA, 'y = 2x − 3'), (-1, 6, FG.GRO, 'y = −x + 6')],
                    [(3, 3, FG.ROD, '(3, 3)')],
                    xmin=-5, xmax=7, ymin=-5, ymax=7,
                    titel='Figuren med svarene på'),
               'Det røde punkt er skæringen mellem de to linjer. Figuren er den samme '
               'som på ungernes side, med svarene sat på.')),
    ('tabel', [
        ('a) b', '−3 og 6', 'Aflæses hvor linjerne skærer y-aksen'),
        ('b) a', '2 og −1', 'Blå: 1 til højre, 2 op. Grøn: 1 til højre, 1 ned'),
        ('c) Forskrifter', 'y = 2x − 3 og y = −x + 6', ''),
        ('d) Skæringspunkt', '(3, 3)', 'Aflæses på figuren'),
        ('e) Ved regning', 'x = 3, y = 3',
         '2x − 3 = −x + 6 → 3x = 9 → x = 3, og y = 2·3 − 3 = 3'),
        ('f) Nulpunkter', 'x = 1,5 og x = 6', '2x − 3 = 0 og −x + 6 = 0'),
        ('g) Stejlest', 'den blå', '|2| &gt; |−1|'),
    ]),
    ('note', ['Til g): figuren viser det direkte — den blå linje rejser sig hurtigere. '
              'Går man ét skridt til højre, flytter den blå sig 2, mens den grønne kun '
              'flytter sig 1. Det kan måles på figuren, fordi ternene er kvadratiske: '
              'den grønne ligger præcis på 45° nedad.']),
])


# --- 5. Uge 38 - Ligninger -------------------------------------------------
dok('facit-lektier-2026-09-14-ligninger', 'lektier', '2026-09-14', 'Ligninger',
    'Uge 38 · lektier-uge38-ligninger.html', [
    ('h2', 'Opgave A · Løs ligningerne'),
    ('tabel', r_ligninger(U38A)),
    ('figur', (FG.vaegt(4, 3, 27),
               'Opgave b som vægt. Fjern 3 lodder på hver side, og der står 4 kasser '
               'over for 24 lodder. Hver kasse vejer 6.')),
    ('h3', 'g) Prøve'),
    ('tabel', [
        ('b) <code>4x + 3 = 27</code>', '✔', '4·6 + 3 = 27'),
        ('d) <code>2x + 9 = 5x − 6</code>', '✔', '2·5 + 9 = 19 og 5·5 − 6 = 19'),
        ('f) <code>6(x − 3) = 30</code>', '✔', '6(8 − 3) = 30'),
    ]),
    ('h2', 'Opgave B · Fra tekst til ligning'),
    ('tabel', [
        ('a) Fitnesskort', '7 måneder', '150 + 85m = 745 → 85m = 595'),
        ('b) Cykelforhandler', '30 services', '1200 + 45x = 1800 + 25x → 20x = 600'),
        ('c) Fire tal', '24, 25, 26 og 27', '4x + 6 = 102 → 4x = 96'),
        ('d) Trekant', '12, 24 og 18 cm', 'x + 2x + (x+6) = 54 → 4x = 48'),
    ]),
    ('figur', (graf([(45, 1200, FG.BLA, 'A: 1.200 + 45x'),
                     (25, 1800, FG.GRO, 'B: 1.800 + 25x')],
                    [(30, 2550, FG.ROD, '(30, 2550)')],
                    xmin=0, xmax=60, ymin=0, ymax=3600,
                    titel='Hvornår koster de to forhandlere det samme?', ens=False),
               'Ved 30 services koster begge 2.550 kr. Til venstre for skæringen er A '
               'billigst. Ved 40 services koster A 3.000 kr og B 2.800 kr — så B er '
               'billigst dér. Akserne har hver sin enhed, antal mod kroner, så de kan '
               'ikke have samme skala.')),
    ('note', ['Til b): spørgsmålet om hvem der er billigst ved 40 services kan '
              'besvares direkte på grafen — man behøver ikke regne. Det er pointen med '
              'at tegne to linjer i samme koordinatsystem.']),
    ('h3', 'e) Egen tekstopgave'),
    ('p', 'Ingen facitliste. Godkend opgaven, hvis ligningen har <code>x = 9</code> '
          'som løsning, og det står klart, hvad <code>x</code> betyder.'),
])

# --- 6. Uge 39 - Parenteser og broeker -------------------------------------
dok('facit-lektier-2026-09-21-parenteser-og-broeker', 'lektier', '2026-09-21',
    'Ligninger med parenteser og brøker',
    'Uge 39 · lektier-uge39-ligninger-fortsat.html', [
    ('h2', 'Opgave A · Parenteser og x på begge sider'),
    ('tabel', r_ligninger(U39A)),
    ('figur', (FG.arealmodel(4, 2),
               'Opgave b. Rektanglets areal kan skrives som 4(x + 2) eller som de to '
               'felter lagt sammen, 4x + 8. Derfor skal tallet uden for parentesen '
               'ganges ind på begge led.')),
    ('note', ['d) Et minus foran en parentes vender fortegnet på alle led indeni: '
              '<code>−2(x + 3) = −2x − 6</code>. Det er den fejl, der koster flest '
              'point — i opgave c bliver <code>−6</code> til <code>+6</code>, hvis man '
              'glemmer det, og så får man <code>x = 2</code>.']),
    ('h2', 'Opgave B · Ligninger med brøker'),
    ('tabel', r_ligninger(U39B)),
    ('note', ['d) Der ganges med 6, fordi 6 er det mindste tal, som både 2 og 3 går op '
              'i. Ganger man med 2, forsvinder kun den første brøk. Ganger man med 12, '
              'virker det også — men tallene bliver unødigt store.']),
    ('h2', 'Opgave C · Med og uden CAS'),
    ('tabel', [
        ('a) I hånden', 'x = 8', '7x − 14 = 3x + 18 → 4x = 32'),
        ('b) Med CAS', 'x = 8', 'GeoGebra: Løs(7(x−2)=3(x+6))'),
        ('d) Prøve', '42 = 42', '7(8 − 2) = 42 og 3(8 + 6) = 42'),
    ]),
    ('note', ['Til c): det gode svar handler ikke om, at CAS er hurtigere. Det handler '
              'om, at ungen selv skal kunne opstille ligningen og vurdere, om svaret er '
              'rimeligt. CAS regner — det forstår ikke opgaven. En tastefejl giver et '
              'pænt svar, som er forkert, og kun prøven fanger det.']),
])

# --- 7. Uge 41 - Lineaere funktioner og grafer -----------------------------
dok('facit-lektier-2026-10-05-funktioner-og-grafer', 'lektier', '2026-10-05',
    'Lineære funktioner og grafer',
    'Uge 41 · lektier-uge41-funktioner-grafer.html', [
    ('h2', 'Opgave A · Find forskriften'),
    ('tabel', [
        ('a) Hældning gennem <code>(1, 4)</code> og <code>(5, 16)</code>', 'a = 3',
         '(16 − 4) ÷ (5 − 1) = 12 ÷ 4'),
        ('b) Forskrift', 'y = 3x + 1', 'Sæt (1, 4) ind: 4 = 3 + b'),
        ('c) Nulpunkt', 'x = −1/3', '3x + 1 = 0'),
        ('d) Gennem <code>(−2, 9)</code> og <code>(2, 1)</code>', 'y = −2x + 5',
         'a = (1 − 9) ÷ (2 + 2) = −2 ; 9 = −2·(−2) + b → b = 5'),
        ('d) Nulpunkt', 'x = 2,5', '−2x + 5 = 0'),
        ('e) Går nedad', 'y = −2x + 5', 'Hældningen er negativ'),
    ]),
    ('h2', 'Opgave B · Aflæs og regn efter'),
    ('figur', (graf([(1, 1, FG.BLA, 'y = x + 1'), (-2, 7, FG.GRO, 'y = −2x + 7')],
                    [(2, 3, FG.ROD, '(2, 3)')],
                    xmin=-2, xmax=8, ymin=-2, ymax=8,
                    titel='Figuren med svarene på'),
               'Det røde punkt er skæringen mellem linjerne. Figuren er den samme som '
               'på lektiearket, med svarene sat på.')),
    ('tabel', [
        ('a) b', '1 og 7', 'Aflæses på y-aksen'),
        ('b) a', '1 og −2', 'Blå: 1 til højre, 1 op. Grøn: 1 til højre, 2 ned'),
        ('c) Forskrifter', 'y = x + 1 og y = −2x + 7', ''),
        ('d) Skæringspunkt', '(2, 3)', 'Aflæses'),
        ('e) Ved regning', 'x = 2, y = 3', 'x + 1 = −2x + 7 → 3x = 6'),
        ('f) Nulpunkter', 'x = −1 og x = 3,5', 'x + 1 = 0 og −2x + 7 = 0'),
    ]),
    ('h2', 'Opgave C · Tegn selv'),
    ('p', 'a) Tabel for <code>y = −x + 4</code>, hvor x går fra −1 til 5:'),
    ('vaerditabel', ([dk(x) for x, _ in TABEL_C], [dk(y) for _, y in TABEL_C])),
    ('figur', (graf([(-1, 4, FG.BLA, 'y = −x + 4')],
                    [(4, 0, FG.ORA, '(4, 0)'), (0, 4, FG.GRO, '(0, 4)')],
                    xmin=-2, xmax=8, ymin=-2, ymax=8, titel='Den færdige graf'),
               'Nulpunktet er (4, 0), og grafen skærer y-aksen i (0, 4). Fordi ternene '
               'er kvadratiske, ligger linjen præcis på 45° nedad — det er hældningen '
               'a = −1, man kan se.')),
    ('tabel', [
        ('c) Nulpunkt', 'x = 4', '−x + 4 = 0 → x = 4'),
        ('d) Skæring med y-aksen', '(0, 4)', 'Passer med b = 4 i forskriften'),
    ]),
    ('note', ['Bemærk: hældningen er −1, så linjen går nedad. Går man 1 til højre, går '
              'man 1 ned. Det kan aflæses direkte på tabellen: y falder med 1, hver '
              'gang x vokser med 1.']),
])


# ---------------------------------------------------------------------------
def main(filter_=''):
    byg = [(n, h) for n, h in DOKUMENTER if filter_ in n]
    assert byg, f'intet dokument hedder noget med {filter_!r}'
    with tempfile.TemporaryDirectory() as tmp:
        for navn, html in byg:
            kilde = os.path.join(tmp, navn + '.html')
            with open(kilde, 'w', encoding='utf-8') as f:
                f.write(html)
            maal = os.path.join(UD, navn + '.pdf')
            subprocess.run(['node', os.path.join(ROD, 'claude', 'html_til_pdf.mjs'),
                            kilde, maal], check=True, cwd=ROD)
    print(f'{len(byg)} facitlister bygget i facit/')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '')
