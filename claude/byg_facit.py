# -*- coding: utf-8 -*-
"""Bygger facitlisterne til forloebet Funktioner og ligninger.

Indholdet er kode, figurerne kommer fra figurer.py, og hvert svar regnes
efter med broekregning, foer filen skrives. Skabelonen ligger i facit.py.

    python3 claude/byg_facit.py            bygger alle syv
    python3 claude/byg_facit.py grafer     bygger dem, hvis navn indeholder ordet
"""
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figurer as FG
from facit import byg, dk, dok, forskrift, nulpunkt, proev, skaering


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
# Opgaven er hverdagsstof fra 6. oktober: samme faerdigheder, men tallene
# kommer fra en kvittering, et batteri og to telefoner. b skal kunne lade sig
# goere i virkeligheden - et startgebyr kan ikke vaere negativt, og et batteri
# kan ikke starte uden for 0-100 %.
KAJ_A, KAJ_B = forskrift((2, 200), (5, 350))
assert (KAJ_A, KAJ_B) == (50, 100) and KAJ_B >= 0
assert KAJ_A * 7 + KAJ_B == 450
BAT_A, BAT_B = forskrift((1, 80), (4, 50))
assert (BAT_A, BAT_B) == (-10, 90) and 0 <= BAT_B <= 100
assert nulpunkt(BAT_A, BAT_B) == 9

dok('facit-online-2026-10-05-lineaere-funktioner', 'online', '2026-10-05',
    'Lineære funktioner', 'Funktioner og ligninger, modul 2 · Opgave C', [
    ('h2', 'Opgave C · Find forskriften'),
    ('h3', 'Kajakudlejningen · 2 timer = 200 kr, 5 timer = 350 kr'),
    ('tabel', [
        ('a) Pris pr. time', 'a = 50 kr', '(350 − 200) ÷ (5 − 2) = 150 ÷ 3'),
        ('b) Forskriften', 'y = 50x + 100',
         'Sæt (2, 200) ind: 200 = 50·2 + b → b = 100'),
        ('b) Hvad b betyder', '100 kr i startgebyr',
         'Det du betaler ved 0 timer — redningsvest og udstyr'),
        ('c) Syv timer', '450 kr', '50 · 7 + 100 = 350 + 100'),
        ('d) Tegningen', 'Linjen rammer 450 ved 7 timer',
         'Godkend hvis linjen går gennem begge punkter og skærer y-aksen i 100'),
    ]),
    ('figur', (graf([(KAJ_A, KAJ_B, FG.BLA, 'y = 50x + 100')],
                    [(0, KAJ_B, FG.GRO, '(0, 100)'), (2, 200, FG.ORA, '(2, 200)'),
                     (5, 350, FG.ORA, '(5, 350)'), (7, 450, FG.ROD, '(7, 450)')],
                    xmin=0, xmax=8, ymin=0, ymax=500, ens=False,
                    aksenavne=('timer', 'kr'), titel='Kajakudlejningen'),
               'Den færdige linje. De orange punkter er kvitteringerne, det grønne '
               'er startgebyret, og det røde er de syv timer fra opgave c.')),
    ('h3', 'Telefonens batteri · 1 time = 80 %, 4 timer = 50 %'),
    ('tabel', [
        ('e) Tab pr. time', 'a = −10 %', '(50 − 80) ÷ (4 − 1) = −30 ÷ 3'),
        ('e) Hvorfor negativ', 'Fordi det falder',
         'Et negativt a betyder, at linjen går nedad — batteriet bliver mindre'),
        ('f) Forskriften', 'y = −10x + 90', 'Sæt (1, 80) ind: 80 = −10 + b → b = 90'),
        ('f) Hvad b betyder', '90 % ved start', 'Batteriet, da målingen begyndte'),
        ('g) Nulpunkt', 'x = 9 timer', '−10x + 90 = 0 → 10x = 90 → x = 9'),
    ]),
    ('figur', (graf([(BAT_A, BAT_B, FG.BLA, 'y = −10x + 90')],
                    [(0, BAT_B, FG.GRO, '(0, 90)'), (1, 80, FG.ORA, '(1, 80)'),
                     (4, 50, FG.ORA, '(4, 50)'),
                     (nulpunkt(BAT_A, BAT_B), 0, FG.ROD, '(9, 0)')],
                    xmin=0, xmax=12, ymin=0, ymax=100, ens=False,
                    aksenavne=('timer', '%'), titel='Batteriet'),
               'Det røde punkt er nulpunktet: efter 9 timer er telefonen død. '
               'Her er nulpunktet ikke et tal på en akse, men et klokkeslæt.')),
    ('h3', 'Hvem ændrer sig hurtigst?'),
    ('tabel', [
        ('h) Hurtigst', 'Lisas telefon', '|−18| = 18 er større end |12| = 12'),
        ('h) Hvad fortegnet siger', 'Op eller ned',
         'Lisas falder (negativ a), Omars stiger (positiv a). Talværdien siger, '
         'hvor hurtigt — fortegnet siger hvilken vej'),
    ]),
    ('note', ['Her svarer ungerne ofte "Omars, for 12 er et pænt tal" eller "Lisas, '
              'for −18 er mindre end 12". Begge dele viser samme misforståelse: at '
              'fortegnet og hastigheden er det samme. Lisa taber 18 procentpoint i '
              'timen, Omar vinder 12 — Lisas telefon ændrer sig hurtigst, selvom '
              '−18 står lavere på tallinjen.']),
])

# --- 4. Modul 3, Opgave D - Aflaesning af grafer ---------------------------
A_FAST, A_GB = F(50), F(20)
B_FAST, B_GB = F(150), F(10)
SK = skaering(A_GB, A_FAST, B_GB, B_FAST)
assert SK == (10, 250), SK
assert A_GB * 12 + A_FAST == 290 and B_GB * 12 + B_FAST == 270
assert A_GB * 5 + A_FAST == 150 and B_GB * 5 + B_FAST == 200
AARS = (B_GB * 5 + B_FAST - (A_GB * 5 + A_FAST)) * 12
assert AARS == 600

dok('facit-online-2026-10-05-grafer', 'online', '2026-10-05',
    'Aflæsning af grafer', 'Funktioner og ligninger, modul 3 · Opgave D', [
    ('h2', 'Opgave D · Aflæs og regn efter'),
    ('figur', (graf([(A_GB, A_FAST, FG.BLA, 'A: y = 20x + 50'),
                     (B_GB, B_FAST, FG.GRO, 'B: y = 10x + 150')],
                    [(SK[0], SK[1], FG.ROD, '(10, 250)')],
                    xmin=0, xmax=20, ymin=0, ymax=500, ens=False,
                    aksenavne=('GB', 'kr'), titel='Figuren med svarene på'),
               'Det røde punkt er skæringen. Figuren er den samme som på ungernes '
               'side, med svarene sat på.')),
    ('tabel', [
        ('a) b', '50 kr og 150 kr',
         'Aflæses på y-aksen. Det er abonnementet — prisen ved 0 GB'),
        ('b) a', '20 kr og 10 kr pr. GB',
         'Trappetrin på 5 GB: blå stiger 100 kr, grøn 50 kr. Divider med 5'),
        ('c) Forskrifter', 'A: y = 20x + 50 · B: y = 10x + 150', ''),
        ('d) Skæringspunkt', '(10, 250)',
         'Ved 10 GB koster de præcis det samme, nemlig 250 kr'),
        ('e) Ved regning', 'x = 10, y = 250',
         '20x + 50 = 10x + 150 → 10x = 100 → x = 10, og y = 20·10 + 50 = 250'),
        ('f) 12 GB', 'A: 290 kr · B: 270 kr',
         '20·12 + 50 = 290 og 10·12 + 150 = 270 — B er billigst'),
        ('g) Stejlest', 'A', 'A stiger 20 kr pr. GB mod B’s 10 — dobbelt så hurtigt'),
        ('h) Ved 5 GB', 'A: 150 kr · B: 200 kr',
         'A er billigst. Forskellen er 50 kr om måneden, altså 600 kr om året'),
    ]),
    ('note', ['Pointen med d): skæringspunktet er ikke bare et punkt. Det er '
              'grænsen, hvor det bedste valg skifter. Under 10 GB er A billigst, over '
              '10 GB er B. Et abonnement kan altså ikke være "billigst" i sig selv — '
              'det afhænger af, hvor meget man bruger.',
              'Til g): den stejleste linje er den, hvor prisen stiger hurtigst pr. '
              'GB. Derfor er A kun billig, så længe man holder sig under skæringen.']),
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
    ('h2', 'Opgave C · Med og uden regneprogram'),
    ('tabel', [
        ('a) I hånden', 'x = 8', '7x − 14 = 3x + 18 → 4x = 32'),
        ('b) Med regneprogram', 'x = 8', 'GeoGebra: Løs(7(x−2)=3(x+6))'),
        ('d) Prøve', '42 = 42', '7(8 − 2) = 42 og 3(8 + 6) = 42'),
    ]),
    ('note', ['Til c): det gode svar handler ikke om, at regneprogrammet (CAS) er '
              'hurtigere. Det handler om, at ungen selv skal kunne opstille ligningen '
              'og vurdere, om svaret er rimeligt. Programmet regner — det forstår ikke '
              'opgaven. En tastefejl giver et pænt svar, som er forkert, og kun prøven '
              'fanger det.']),
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
    ('h2', 'Opgave B · Aflæs på grafen'),
    ('figur', (graf([(1, 1, FG.BLA, 'y = x + 1'), (-2, 7, FG.GRO, 'y = −2x + 7')],
                    [(2, 3, FG.ROD, '(2, 3)')],
                    xmin=-2, xmax=8, ymin=-2, ymax=8,
                    titel='Figuren med svarene på'),
               'Det røde punkt er skæringen mellem linjerne. Figuren er den samme som '
               'på lektiearket, med svarene sat på. Arket beder ikke om at løse '
               'ligningen — uge 41 handler om lineære funktioner, ikke om '
               'ligningsløsning.')),
    ('tabel', [
        ('a) b', '1 og 7', 'Aflæses på y-aksen'),
        ('b) a', '1 og −2', 'Blå: 1 til højre, 1 op. Grøn: 1 til højre, 2 ned'),
        ('c) Forskrifter', 'y = x + 1 og y = −2x + 7', ''),
        ('d) Skæringspunkt', '(2, 3)', 'Aflæses'),
        ('e) Nulpunkter', 'x = −1 og x = 3,5',
         'Aflæses hvor hver linje skærer x-aksen'),
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
        ('c) Nulpunkt', 'x = 4',
         'Aflæses hvor grafen skærer x-aksen. Tabellen har y = 0 ved x = 4'),
        ('d) Skæring med y-aksen', '(0, 4)', 'Passer med b = 4 i forskriften'),
    ]),
    ('note', ['Bemærk: hældningen er −1, så linjen går nedad. Går man 1 til højre, går '
              'man 1 ned. Det kan aflæses direkte på tabellen: y falder med 1, hver '
              'gang x vokser med 1.']),
])


# ---------------------------------------------------------------------------
if __name__ == '__main__':
    byg(sys.argv[1] if len(sys.argv) > 1 else '')
