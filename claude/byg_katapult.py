#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bygger sløjdopskriften på katapulten.

    python3 claude/byg_katapult.py <scratch-mappe>

Skriver:
    katapult.html                     opskriften på sitet (åben, med printknap)
    <scratch>/ungeark-katapult.html   samme opskrift sat til print -> PDF
    <scratch>/vejledning-katapult.html vejledning til den voksne -> PDF

Hele mekanikken er ét sæt tal i MAAL nedenfor. Tegningerne, styklisten og
teksten regnes ud af de samme tal, og scriptet nægter at skrive filerne, hvis
geometrien ikke hænger sammen — fx hvis stoppinden ikke standser armen ved 45
grader, eller hvis halen rammer udløserstangen, når armen står i hvile.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figurer as FG                                         # noqa: E402

SCRATCH = sys.argv[1] if len(sys.argv) > 1 else '.'
ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROD)

# ============================================================ 1 · målene
# Alt måles i millimeter fra grundpladens BAGKANT og fra dens OVERSIDE.
# x vokser fremad (kasteretningen), y vokser opad.
M = dict(
    # grundplade
    plade_l=270, plade_b=95, plade_t=18,
    # hjul og aksler
    hjul_d=45, hjul_t=12, aksel_d=6, aksel_l=135,
    aksel_bag=45, aksel_frem=220,
    # opstandere
    opst_h=120, opst_l=70, opst_t=18, opst_bag=50, opst_luft=26,
    # kastearm (glat liste 9 x 21)
    arm_l=220, arm_b=21, arm_t=9, arm_hale=24,
    # huller (globale koordinater)
    drej=(70, 32), stop=(96, 70), elast=(70, 102),
    hul_pind=8, hul_arm=8.5, hul_aksel=6.5,
    # elastikkens greb på armen, målt langs armen fra drejetappen
    elast_greb=90,
    # udløser
    stang_l=180, stang_bag=-60, stang_t=9,
    klods_x=44, klods_l=16, klods_h=18,
    styr_x=5, styr_l=25, styr_b=15,
    traek=20,
    # skål
    skaal_d=40, skaal_t=18, skaal_fordyb=25, skaal_dybde=8,
)
DREJ, STOP, ELAST = M['drej'], M['stop'], M['elast']
ARM_FREM = M['arm_l'] - M['arm_hale']


def langs(vinkel, a, t=0.0):
    """Punkt på armen: a mm ud ad armen, t mm vinkelret på den."""
    r = math.radians(vinkel)
    return (DREJ[0] + a * math.cos(r) - t * math.sin(r),
            DREJ[1] + a * math.sin(r) + t * math.cos(r))


def arm_polygon(vinkel):
    return FG.drejet(DREJ[0], DREJ[1],
                     [(-M['arm_hale'], -M['arm_t'] / 2), (ARM_FREM, -M['arm_t'] / 2),
                      (ARM_FREM, M['arm_t'] / 2), (-M['arm_hale'], M['arm_t'] / 2)],
                     vinkel)


# -- hvor standser armen? -------------------------------------------------
# Stoppinden rammer armens OVERSIDE, ikke dens midterlinje. Armen står stille,
# når afstanden fra pindens centrum ned til armens midterlinje er lig
# halvdelen af armens tykkelse plus pindens radius.
def stopvinkel():
    dx, dy = STOP[0] - DREJ[0], STOP[1] - DREJ[1]
    r = math.hypot(dx, dy)
    beroring = M['arm_t'] / 2 + M['hul_pind'] / 2
    return math.degrees(math.atan2(dy, dx) - math.asin(beroring / r))


HVILE = stopvinkel()
assert 44.0 < HVILE < 46.0, f'stoppinden standser armen ved {HVILE:.1f}°, ikke 45°'


def elastiklaengde(vinkel):
    p = langs(vinkel, M['elast_greb'])
    return math.hypot(p[0] - ELAST[0], p[1] - ELAST[1])


E_SPAENDT, E_HVILE = elastiklaengde(0), elastiklaengde(HVILE)
assert E_SPAENDT / E_HVILE > 1.6, 'elastikken strækkes for lidt til at kaste'

# -- elastikken må ikke skure mod stoppinden, når armen er spændt ned ------
_p = langs(0, M['elast_greb'])
_dx, _dy = _p[0] - ELAST[0], _p[1] - ELAST[1]
_n = math.hypot(_dx, _dy)
AFSTAND_STOP = abs((_dx * (STOP[1] - ELAST[1]) - _dy * (STOP[0] - ELAST[0])) / _n)
assert AFSTAND_STOP > M['hul_pind'] / 2 + 1, \
    f'elastikken ligger kun {AFSTAND_STOP:.1f} mm fra stoppinden'

# -- halen må ikke lande på udløserstangen, når armen står i hvile --------
HALE_LAVEST = min(y for x, y in arm_polygon(HVILE) if x < DREJ[0])
assert HALE_LAVEST > M['stang_t'] + 1.5, \
    f'armens hale kommer {HALE_LAVEST:.1f} mm ned og rammer udløserstangen'

# -- klodsen skal bære halen, når armen er spændt ned, og slippe den, når
#    stangen er trukket tilbage ------------------------------------------
HALE_BAG = DREJ[0] - M['arm_hale']
KLODS_TOP = M['stang_t'] + M['klods_h']
assert abs(KLODS_TOP - (DREJ[1] - M['arm_t'] / 2)) < 1, \
    'klodsens overside passer ikke med armens underside'
assert M['klods_x'] < HALE_BAG < M['klods_x'] + M['klods_l'], \
    'klodsen står ikke under armens hale'
assert M['klods_x'] + M['klods_l'] - M['traek'] < HALE_BAG, \
    'stangen trækkes ikke langt nok tilbage til at slippe halen'

# -- hullerne skal ligge inde i træet ------------------------------------
for navn, (hx, hy) in (('drejetap', DREJ), ('stoppind', STOP), ('elastikpind', ELAST)):
    lx, ly = hx - M['opst_bag'], hy
    kant = min(lx, M['opst_l'] - lx, ly, M['opst_h'] - ly)
    assert kant > M['hul_pind'] / 2 + 6, \
        f'{navn}s hul ligger kun {kant:.1f} mm fra opstanderens kant'

# -- armen skal kunne være mellem opstanderne ----------------------------
assert M['opst_luft'] > M['arm_b'] + 3, 'der er ikke luft nok til armen'
assert M['aksel_l'] > M['plade_b'] + 2 * M['hjul_t'] + 10, 'akslen er for kort'

TAL = dict(
    hvile=f'{HVILE:.0f}',
    e_spaendt=f'{E_SPAENDT:.0f}', e_hvile=f'{E_HVILE:.0f}',
    straek=f'{E_SPAENDT / E_HVILE:.2f}'.replace('.', ','),
    frihoejde=f'{M["hjul_d"] / 2 - M["plade_t"] / 2:.1f}'.replace('.0', '').replace('.', ','),
)

# ============================================================ 2 · tegninger
GHOST = '#f7f1e4'


def fig_oversigt():
    """Set fra siden. Den nærmeste opstander tegnes gennemsigtig, så
    mekanikken bag den kan ses — ellers skjuler den både hale og klods."""
    r = FG.Rids(M['stang_bag'] - 22, 288, -52, 196, skala=1.6,
                titel='Katapulten set fra siden',
                alt='Katapulten set fra siden med armen spændt ned og i hvile.',
                margen=(30, 26, 26, 30))
    for ax in (M['aksel_bag'], M['aksel_frem']):                  # hjul og aksler
        r.skive(ax, -M['plade_t'] / 2, M['hjul_d'], FG.TRAE3)
        r.pind(ax, -M['plade_t'] / 2, M['aksel_d'])
    r.rekt(0, -M['plade_t'], M['plade_l'], M['plade_t'], FG.TRAE2)
    r.rekt(M['styr_x'], 0, M['styr_l'], M['stang_t'], '#fff', FG.LIN)
    r.rekt(M['stang_bag'], 0, M['stang_l'], M['stang_t'], FG.TRAE)   # udløserstang
    r.poly(klods_form(0), FG.TRAE2)                                  # udløserklods
    r.poly(arm_polygon(HVILE), GHOST, FG.LIN, stiplet=True)          # hvilestilling
    r.poly(skaal_form(HVILE), GHOST, FG.LIN, stiplet=True)
    r.poly(arm_polygon(0), FG.TRAE)                                  # spændt ned
    r.poly(skaal_form(0), FG.TRAE2)
    for v, farve, br in ((HVILE, '#e8bcc2', 1.6), (0, FG.ROD, 2.6)):  # elastikken
        p = langs(v, M['elast_greb'])
        r.linje(ELAST[0], ELAST[1], p[0], p[1], farve, br)
    r.rekt(M['opst_bag'], 0, M['opst_l'], M['opst_h'], FG.TRAE, FG.KANT,
           opacitet=0.42)                                            # gennemsigtig
    for p in (DREJ, STOP, ELAST):
        r.pind(p[0], p[1], M['hul_pind'])
    r.bue(DREJ[0], DREJ[1], ARM_FREM - 10, 0, HVILE)                 # svingbuen
    r.linje(DREJ[0], DREJ[1], DREJ[0] + 96, DREJ[1], FG.LIN, 1, True)
    r.vinkel(DREJ[0], DREJ[1], 62, 0, HVILE, f'{HVILE:.0f}°')
    r.note(DREJ[0], DREJ[1], 20, 52, 'drejetap')
    r.note(ELAST[0], ELAST[1], 20, 116, 'elastikpind')
    r.note(STOP[0], STOP[1], 152, 92, 'stoppind')
    r.tekst(M['stang_bag'] + 26, -14, 'hiv bagud', FG.ROD, 10.5)
    r._pil(r.px(M['stang_bag'] - 4), r.py(-5), -12, 0)
    r.linje(M['stang_bag'] + 26, -5, M['stang_bag'] - 2, -5, FG.ROD, 2.2)
    for bogstav, (bx, by) in (('A', (238, -9)), ('B', (60, 112)),
                              ('C', (DREJ[0] + 150, DREJ[1])),
                              ('D', (M['stang_bag'] + 22, 4.5)),
                              ('E', (M['klods_x'] + 8, 16)),
                              ('G', (DREJ[0] + ARM_FREM - 20, DREJ[1] + 18)),
                              ('H', (M['aksel_frem'], -30))):
        r.maerke(bx, by, bogstav)
    r.maal_v(0, M['plade_l'], -46, hjaelp_fra=-M['plade_t'])
    r.maal_l(0, M['opst_h'], -52, hjaelp_fra=M['opst_bag'])
    return r.svg()


def klods_form(skub):
    """Udløserklodsen — forreste øverste hjørne er skåret skråt af, så den kan
    smutte ind under armens hale i stedet for at støde imod den."""
    kx = M['klods_x'] + skub
    return [(kx, M['stang_t']), (kx + M['klods_l'], M['stang_t']),
            (kx + M['klods_l'], KLODS_TOP - 5),
            (kx + M['klods_l'] - 5, KLODS_TOP), (kx, KLODS_TOP)]


def skaal_form(vinkel):
    return FG.drejet(DREJ[0], DREJ[1],
                     [(ARM_FREM - M['skaal_d'], M['arm_t'] / 2),
                      (ARM_FREM, M['arm_t'] / 2),
                      (ARM_FREM, M['arm_t'] / 2 + M['skaal_t']),
                      (ARM_FREM - M['skaal_d'], M['arm_t'] / 2 + M['skaal_t'])],
                     vinkel)


def fig_plade():
    b = M['plade_b']
    r = FG.Rids(-16, 292, -b - 62, 34, skala=1.55,
                titel='A · grundplade set oppefra',
                alt='Grundpladen med akselhuller og klodsernes plads.',
                margen=(38, 26, 26, 30))
    r.rekt(0, -b, M['plade_l'], b, FG.TRAE)
    midte = -b / 2
    # udløserstangens spor — kun en stiplet bane, så klodserne kan ses
    for dy in (-M['arm_b'] / 2, M['arm_b'] / 2):
        r.linje(-12, midte + dy, 132, midte + dy, FG.LIN, 1, True)
    r.tekst(148, midte - 1, 'udløserstangen glider her', FG.MUT, 9.5,
            anker='start')
    o = M['opst_luft'] / 2
    for side in (1, -1):
        y0 = midte + side * o
        r.rekt(M['opst_bag'], min(y0, y0 + side * M['opst_t']), M['opst_l'],
               M['opst_t'], FG.TRAE2)
        y1 = midte + side * (M['arm_b'] / 2 + 3)
        r.rekt(M['styr_x'], min(y1, y1 + side * M['styr_b']), M['styr_l'],
               M['styr_b'], FG.TRAE2)
    for ax in (M['aksel_bag'], M['aksel_frem']):
        r.linje(ax, -b, ax, 0, FG.BLA, 1, True)
        for kant in (0, -b):
            r.hul(ax, kant, M['hul_aksel'], kryds=False)
    r.maerke(M['opst_bag'] + M['opst_l'] / 2, midte + o + M['opst_t'] / 2, 'B')
    r.maerke(M['styr_x'] + M['styr_l'] / 2,
             midte + M['arm_b'] / 2 + 3 + M['styr_b'] / 2, 'F')
    r.maal_v(0, M['aksel_bag'], 16, hjaelp_fra=0)
    r.maal_v(M['aksel_bag'], M['aksel_frem'], 16.001, hjaelp_fra=0)
    r.maal_v(0, M['plade_l'], -b - 26, hjaelp_fra=-b)
    r.maal_v(M['opst_bag'], M['opst_bag'] + M['opst_l'], -b - 46,
             hjaelp_fra=-b)
    r.maal_v(0, M['opst_bag'], -b - 46.001, hjaelp_fra=-b)
    r.maal_l(-b, 0, -10, hjaelp_fra=0)
    return r.svg()


def fig_opstander():
    r = FG.Rids(-58, 182, -30, M['opst_h'] + 44, skala=1.85,
                titel='B · opstander — 2 ens, alle huller Ø8',
                alt='Opstanderen med de tre hullers mål.',
                margen=(30, 24, 26, 26))
    r.rekt(0, 0, M['opst_l'], M['opst_h'], FG.TRAE)
    huller = [('drejetap', DREJ, -12), ('stoppind', STOP, -28),
              ('elastikpind', ELAST, -44)]
    for navn, (hx, hy), maalx in huller:
        lx = hx - M['opst_bag']
        r.hul(lx, hy, M['hul_pind'])
        r.note(lx, hy, M['opst_l'] + 26, hy, navn)
        r.maal_l(0, hy, maalx, hjaelp_fra=0)
    r.maal_v(0, DREJ[0] - M['opst_bag'], M['opst_h'] + 10, hjaelp_fra=M['opst_h'])
    r.maal_v(0, STOP[0] - M['opst_bag'], M['opst_h'] + 26, hjaelp_fra=M['opst_h'])
    r.maal_v(0, M['opst_l'], -12, hjaelp_fra=0)
    r.maal_l(0, M['opst_h'], 80, hjaelp_fra=M['opst_l'])
    r.tekst(-52, M['opst_h'] + 34, 'bagkanten', FG.MUT, 10, anker='start')
    r.linje(-2, M['opst_h'] + 6, -2, -6, FG.MUT, 2)
    return r.svg()


def fig_arm():
    hale, t = M['arm_hale'], M['arm_t']
    hak = hale + M['elast_greb']
    r = FG.Rids(-76, 246, -40, 66, skala=1.75,
                titel='C · kastearm med G · skål',
                alt='Kastearmen med drejehul, elastikhak og skål.',
                margen=(26, 26, 26, 26))
    r.rekt(0, 0, M['arm_l'], t, FG.TRAE)
    r.hul(hale, t / 2, M['hul_arm'])
    for dy in (0, t - 2):
        r.rekt(hak - 1.5, dy, 3, 2, FG.ROD, FG.ROD)
    r.rekt(M['arm_l'] - M['skaal_d'], t, M['skaal_d'], M['skaal_t'], FG.TRAE2)
    r.rekt(M['arm_l'] - M['skaal_d'] / 2 - M['skaal_fordyb'] / 2,
           t + M['skaal_t'] - M['skaal_dybde'], M['skaal_fordyb'],
           M['skaal_dybde'], '#fff', FG.LIN)
    r.note(hale, t / 2, hale - 8, 44, f'drejehul Ø{FG._dk(M["hul_arm"])}')
    r.note(hak, t, hak - 26, 64, 'to hak til elastikken')
    r.note(M['arm_l'] - M['skaal_d'] / 2, t + M['skaal_t'],
           M['arm_l'] - 26, 62, 'skål')
    r.maerke(62, t / 2, 'C')
    r.maal_v(0, hale, -10, hjaelp_fra=0)
    r.maal_v(hale, hak, -10.001, hjaelp_fra=0)
    r.maal_v(0, M['arm_l'], -26, hjaelp_fra=0)
    return r.svg()


def fig_udloeser():
    """Udløseren i to stillinger: låst og trukket tilbage."""
    ud = []
    for navn, skub in (('Låst — klodsen bærer armens hale', 0),
                       (f'Hivet {M["traek"]} mm bagud — armen er fri',
                        -M['traek'])):
        r = FG.Rids(M['stang_bag'] - 12, 170, -34, 76, skala=1.7, titel=navn,
                    alt='Udløseren set fra siden.', margen=(26, 26, 26, 26))
        r.rekt(0, -M['plade_t'], 170, M['plade_t'], FG.TRAE2)
        r.rekt(M['styr_x'], 0, M['styr_l'], M['stang_t'], '#fff', FG.LIN)
        r.rekt(M['stang_bag'] + skub, 0, M['stang_l'], M['stang_t'], FG.TRAE)
        r.poly(klods_form(skub), FG.TRAE2)
        r.poly(arm_polygon(0 if skub == 0 else HVILE), FG.TRAE)
        r.pind(DREJ[0], DREJ[1], M['hul_pind'])
        if skub:
            r.linje(M['stang_bag'] + 34, 34, M['stang_bag'] + 4, 34, FG.ROD, 2.4)
            r._pil(r.px(M['stang_bag'] + 4), r.py(34), -12, 0)
            r.tekst(M['stang_bag'] + 40, 34, 'hiv bagud', FG.ROD, 10.5,
                    anker='start')
            r.maal_v(M['klods_x'] + skub, M['klods_x'], KLODS_TOP + 18,
                     hjaelp_fra=KLODS_TOP)
        else:
            r.note(M['klods_x'] + 4, KLODS_TOP, 96, 62, 'klodsen holder halen')
        ud.append(r.svg())
    return ud


def fig_hjul():
    r = FG.Rids(-14, 214, -46, 46, skala=1.7, titel='H · hjul og J · aksel',
                alt='Hjulet med centerhul, og akslen gennem grundpladen.',
                margen=(26, 26, 26, 26))
    r.skive(M['hjul_d'] / 2, 0, M['hjul_d'], FG.TRAE3)
    r.hul(M['hjul_d'] / 2, 0, M['aksel_d'])
    r.maal_l(-M['hjul_d'] / 2, M['hjul_d'] / 2, M['hjul_d'] + 12,
             f'Ø{M["hjul_d"]}')
    r.tekst(M['hjul_d'] / 2, -34, f'centerhul Ø{M["aksel_d"]}', FG.MUT, 10)
    # snit: akslen gennem pladen med et hjul i hver ende
    x0, sb = 108, 92
    r.rekt(x0, -M['plade_t'] / 2, sb, M['plade_t'], FG.TRAE2)
    for hx in (x0 - 7, x0 + sb + 7):
        r.rekt(hx - 6, -M['hjul_d'] / 2, 12, M['hjul_d'], FG.TRAE3)
    r.linje(x0 - 20, 0, x0 + sb + 20, 0, FG.ORA, 3.5)
    r.tekst(x0 + sb / 2, -M['plade_t'] / 2 - 12, 'grundpladen', FG.MUT, 10)
    r.note(x0 + sb / 2, 0, x0 + sb / 2 + 6, 34, 'akslen drejer i pladen')
    r.maal_v(x0 - 26, x0 + sb + 26, -40, f'{M["aksel_l"]}')
    return r.svg()


TRIN = [
    ('Sav delene til', 'Sav alle dele efter styklisten. Mål to gange, sav én '
     'gang. Slib kanterne, før der bores.', 'a'),
    ('Bor opstanderne', 'Spænd de to opstandere sammen og bor de tre Ø8-huller '
     'igennem begge på én gang. Så står de ens.', 'b'),
    ('Bor arm og plade', f'Armens drejehul Ø{FG._dk(M["hul_arm"])} og pladens to '
     f'akselhuller Ø{FG._dk(M["hul_aksel"])}. Læg en klods under, så udgangen '
     'ikke flosser.', 'b'),
    ('Skær hjulene', f'Fire hjul Ø{M["hjul_d"]} med hulsav i {M["hjul_t"]} mm '
     f'krydsfiner. Bor centerhullet op til Ø{M["aksel_d"]}.', 'b'),
    ('Lim og skru opstanderne fast', f'{M["opst_luft"]} mm luft mellem dem — læg '
     'kastearmen imellem som afstandsklods, mens limen tørrer.', 'c'),
    ('Lim styreklodser og udløserklods', 'Styreklodserne skal give '
     'udløserstangen plads til at glide, ikke klemme den.', 'c'),
    ('Saml mekanikken', 'Armen på drejetappen, så stoppind og elastikpind i. '
     'Pindene limes i opstanderne — ikke i armen.', 'c'),
    ('Hjul og skål', 'Akslerne limes i hjulene og skal dreje frit i pladen. '
     'Skålen limes på armens spids.', 'c'),
    ('Elastik og prøveskud', 'Start med én elastik. Skyd kun med papirkugler, '
     'og kun mod den væg, den voksne har vist jer.', 'd'),
]
FARVER = {'a': FG.MUT, 'b': FG.BLA, 'c': FG.GRO, 'd': FG.ORA}

STYKLISTE = [
    ('A', 'Grundplade', '1', f'{M["plade_l"]} × {M["plade_b"]} × {M["plade_t"]}',
     'fyr 18 mm'),
    ('B', 'Opstander', '2', f'{M["opst_h"]} × {M["opst_l"]} × {M["opst_t"]}',
     'fyr 18 mm'),
    ('C', 'Kastearm', '1', f'{M["arm_l"]} × {M["arm_b"]} × {M["arm_t"]}',
     'glat liste 9 × 21'),
    ('D', 'Udløserstang', '1', f'{M["stang_l"]} × {M["arm_b"]} × {M["stang_t"]}',
     'glat liste 9 × 21'),
    ('E', 'Udløserklods', '1', f'{M["klods_l"]} × {M["arm_b"]} × {M["klods_h"]}',
     'fyr 18 mm'),
    ('F', 'Styreklods', '2', f'{M["styr_l"]} × {M["styr_b"]} × {M["stang_t"]}',
     'rest af listen'),
    ('G', 'Skål', '1', f'Ø{M["skaal_d"]} × {M["skaal_t"]}, fordybning '
     f'Ø{M["skaal_fordyb"]} × {M["skaal_dybde"]}', 'fyr 18 mm'),
    ('H', 'Hjul', '4', f'Ø{M["hjul_d"]} × {M["hjul_t"]}', 'krydsfiner 12 mm'),
    ('I', 'Drejetap, stoppind, elastikpind', '3', f'Ø{M["hul_pind"]} × 80',
     'rundstok Ø8'),
    ('J', 'Aksel', '2', f'Ø{M["aksel_d"]} × {M["aksel_l"]}', 'rundstok Ø6'),
    ('K', 'Elastik', '2–3', 'ca. 55 mm flad, bred type', ''),
    ('L', 'Skrue', '4', '4 × 40 mm', 'forbores'),
]

# ============================================================ 3 · figurerne
fig_side = fig_oversigt()
fig_a = fig_plade()
fig_b = fig_opstander()
fig_c = fig_arm()
fig_d1, fig_d2 = fig_udloeser()
fig_h = fig_hjul()
fig_trin = FG.procesdiagram([(t, u, g) for t, u, g in TRIN], W=660, farver=FARVER)
fig_maal = FG.tomt_soejlegitter(
    ['1 elastik', '2 elastikker', '3 elastikker'], 10, 'Kastelængde i meter',
    'Sæt en søjle for hver forsøgsrække — brug midtertallet af jeres fem skud',
    trin=2)

# ============================================================ 4 · sidens CSS
BASIS = open('matematik.html').read()
GRUND = BASIS[BASIS.find('<style>') + 7:BASIS.find('</style>')]
EKSTRA = '''
.figur{background:var(--panel2);border:1px solid var(--line);border-radius:14px;
padding:16px;margin:16px 0;text-align:center}
.figur svg{max-width:100%;height:auto}
.figtekst{color:var(--muted);font-size:.9rem;margin-top:8px}
.blok{background:var(--panel);border:1px solid var(--line);
border-left:5px solid var(--accent);border-radius:14px;padding:18px 22px;
margin:14px 0;box-shadow:var(--shadow)}
.blok.gron{border-left-color:var(--good)}
.blok.advar{border-left-color:var(--bad);background:var(--bad-soft)}
.blok h3{margin:0 0 8px;font-size:1.15rem}
.blok p,.blok li{color:var(--muted);font-size:.97rem}
.blok p{margin:6px 0;max-width:74ch}
.blok ul{margin:6px 0 0;padding-left:20px}
.blok li{margin:4px 0}
table.t{width:100%;border-collapse:collapse;margin:12px 0;font-size:.95rem}
table.t th,table.t td{border:1px solid var(--line);padding:9px 11px;
text-align:left;vertical-align:top}
table.t th{background:var(--panel2)}
table.t td.tal{text-align:right;white-space:nowrap}
.skriv{border-bottom:1px solid var(--line);display:inline-block;min-width:120px}
.to{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:760px){.to{grid-template-columns:1fr}}
.printbtn{background:#fff;border:1px solid var(--line);border-radius:10px;
padding:10px 18px;font-weight:700;font-size:.95rem;cursor:pointer;color:var(--ink);
font-family:inherit;margin:6px 8px 0 0}
.printbtn:hover{border-color:var(--accent);color:var(--accent)}
@media print{header.top,.printbtn,.btnlink{display:none!important}
.blok,.figur{box-shadow:none;break-inside:avoid;page-break-inside:avoid}
.figur{padding:4px;margin:8px 0;background:none;border:none}
.blok{padding:10px 14px;margin:8px 0}
.hero{padding:0 0 6px;margin:0}
body{font-size:9.6pt}main{padding:0}@page{size:A4;margin:11mm}
h2.sec{page-break-after:avoid;margin:12px 0 4px}
table.t{font-size:9pt}table.t th,table.t td{padding:5px 7px}}
'''


def side(titel, krop, fane=True):
    nav = ('<nav class="tabs">'
           '<a class="" href="matematik.html">Matematik</a>'
           '<a class="" href="samfundsfag.html">Samfundsfag</a>'
           '<a class="" href="tysk.html">Tysk</a>'
           '<a class="" href="fysik.html">Fysik</a></nav>') if fane else ''
    return ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{titel}</title><style>' + GRUND + EKSTRA +
            '</style></head><body><header class="top"><div class="top-inner">'
            '<a class="brand" href="index.html">Mibelibsen <span>9. klasse</span></a>'
            + nav + '</div></header><main>' + krop + '</main><footer>'
            'Undervisningsmateriale · Mibelibsen · sløjd.'
            '</footer></body></html>')


def tabel(hoved, raekker, klasser=None):
    klasser = klasser or [''] * len(hoved)
    th = ''.join(f'<th>{h}</th>' for h in hoved)
    tr = ''.join('<tr>' + ''.join(f'<td class="{k}">{c}</td>'
                                  for c, k in zip(r, klasser)) + '</tr>'
                 for r in raekker)
    return (f'<table class="t"><thead><tr>{th}</tr></thead>'
            f'<tbody>{tr}</tbody></table>')


STYK_TABEL = tabel(['', 'Del', 'Antal', 'Mål i mm', 'Materiale'], STYKLISTE,
                   ['', '', 'tal', 'tal', ''])

SIKKERHED = '''<div class="blok advar"><h3>Sikkerhed — læses højt, før den første elastik sættes på</h3>
<ul>
<li>Skyd <b>kun</b> med noget blødt: en papirkugle, et stykke skumgummi, en
vingummi. Aldrig sten, mønter, blyanter eller noget hårdt.</li>
<li>Skyd aldrig mod et menneske eller et dyr — heller ikke for sjov, heller ikke
"lige forbi". Der skydes kun den vej, den voksne har vist.</li>
<li>Briller på, når I prøvefyrer. En elastik, der springer, rammer ansigtet.</li>
<li>Hold fingrene væk fra armen, når elastikken er spændt, og gå aldrig fra en
spændt katapult. Har I spændt op, så skyd eller slæk.</li>
<li>Kig på elastikken hver gang: er den tør, mat eller revnet, skal den skiftes.</li>
<li>Ved boring og hulsav: briller på, og emnet skal være spændt fast. Hold
aldrig et lille emne med hånden under boret.</li>
</ul></div>'''

SAADAN = '''<h2 class="sec">Sådan virker den</h2>
<div class="blok"><p>Elastikken sidder mellem <b>elastikpinden</b> øverst på
opstanderne og et hak på <b>kastearmen</b>. Når armen trykkes ned, bliver
afstanden mellem de to punkter større — elastikken strækkes fra ca.
{e_hvile} mm til ca. {e_spaendt} mm, altså {straek} gange så lang. Den energi,
I lægger i at trække armen ned, sidder gemt i elastikken.</p>
<p><b>Udløserstangen</b> holder armen nede: klodsen på stangen står under
armens korte hale. Hives stangen bagud, forsvinder klodsen væk under halen,
halen falder, og armen slår op.</p>
<p>Armen bliver standset af <b>stoppinden</b>. Det er dét, der kaster:
kuglen fortsætter, når armen pludselig står stille. Pinden sidder, så armen
standser ved {hvile}° — tæt på den vinkel, der giver det længste kast.</p></div>'''

KROP = f'''<section class="hero"><span class="pill">Sløjd · opskrift</span>
<h1>Katapult med udløser</h1>
<p>En katapult på fire hjul med kastearm, elastik og en udløser, der hives
bagud. Alle mål står i millimeter, og alle huller er målt fra den samme kant,
så to unger kan bygge hver sin og få dem til at passe sammen.</p>
<a class="btnlink" href="materiale/ungeark-katapult.pdf">Hent opskriften som PDF</a>
<a class="btnlink ghost" href="index.html">Fagoversigt</a>
<button class="printbtn" onclick="window.print()">Print opskriften</button></section>

<div class="figur">{fig_side}
<div class="figtekst"><b>A</b> grundplade · <b>B</b> opstander · <b>C</b>
kastearm · <b>D</b> udløserstang · <b>E</b> udløserklods · <b>G</b> skål ·
<b>H</b> hjul. Den fuldt optrukne arm er spændt ned og låst; den svage er
hvilestillingen, som armen slår op i. Den nærmeste opstander er tegnet
gennemsigtig, så mekanikken bag den kan ses.</div></div>

{SAADAN.format(**TAL)}

{SIKKERHED}

<h2 class="sec">Stykliste</h2>
<p>Mål i millimeter, skrevet som <b>længde × bredde × tykkelse</b>. Har I andre
tykkelser på lager, så hold fast i de tre hulmål og i de {M['opst_luft']} mm
luft mellem opstanderne — resten må gerne ændre sig.</p>
{STYK_TABEL}

<h2 class="sec">Værktøj</h2>
<div class="blok"><p>Fintandet sav eller båndsav · søjleboremaskine · bor
Ø{FG._dk(M['hul_pind'])}, Ø{FG._dk(M['hul_arm'])}, Ø{FG._dk(M['aksel_d'])} og
Ø{FG._dk(M['hul_aksel'])} · hulsav Ø{M['hjul_d']} · forstnerbor
Ø{M['skaal_fordyb']} · trælim · to skruetvinger · skruetrækker · sandpapir ·
vinkel, målebånd og blyant · sikkerhedsbriller.</p></div>

<h2 class="sec">Arbejdsgang</h2>
<div class="figur">{fig_trin}</div>

<h2 class="sec">Tegninger</h2>
<div class="figur">{fig_a}
<div class="figtekst"><b>B</b> er opstandernes plads, <b>F</b>
styreklodsernes. Akselhullerne bores tværs igennem pladen, midt i de
{M['plade_t']} mm.</div></div>
<div class="figur">{fig_b}
<div class="figtekst">De tre huller er alle Ø{FG._dk(M['hul_pind'])} og måles
fra bagkanten og fra underkanten. Stoppindens hul er dét, der bestemmer, hvor
armen standser — mål det efter en ekstra gang.</div></div>
<div class="figur">{fig_c}
<div class="figtekst">Skålen er en skive Ø{M['skaal_d']} med en fordybning
Ø{M['skaal_fordyb']}, {M['skaal_dybde']} mm dyb, limet på armens spids. En
kapsel fra en sodavandsflaske, skruet på, gør det samme.</div></div>
<div class="figur">{fig_h}
<div class="figtekst">Akslen limes fast i hjulene og skal dreje frit i pladen.
Gør I det omvendt, står hjulene stille.</div></div>

<h2 class="sec">Udløseren</h2>
<div class="to"><div class="figur">{fig_d1}</div><div class="figur">{fig_d2}</div></div>
<div class="blok gron"><h3>Sådan spænder I op</h3>
<p>Træk stangen bagud. Tryk armen ned med den ene hånd, til halen står over
klodsen. Skub stangen frem under halen med den anden. Slip forsigtigt — nu
holder klodsen. Fyr af ved at hive stangen bagud.</p>
<p>Klodsens forreste øverste hjørne er skåret skråt af. Det er derfor, den kan
smutte ind under halen i stedet for at støde imod den.</p></div>

<h2 class="sec">Når den er færdig — mål efter</h2>
<div class="blok"><p>Skyd fem gange med den samme papirkugle og mål, hvor langt
den når. Skriv alle fem tal ned, og brug <b>midtertallet</b> (medianen), ikke
det længste — det længste er held, midtertallet er katapulten.</p>
<p>Gentag med to og tre elastikker. Bliver kastet dobbelt så langt af dobbelt
så mange elastikker? Tegn det, og se selv.</p></div>
<div class="figur">{fig_maal}</div>

<h2 class="sec">Virker den ikke?</h2>
{tabel(['Det sker', 'Det er som regel'],
       [('Armen slår ikke op', 'Elastikken er for slap. Prøv en kortere, eller '
         'flyt hakket længere ud ad armen.'),
        ('Armen sætter sig fast', 'Drejehullet i armen er for stramt. Bor det '
         f'op til Ø{FG._dk(M["hul_arm"])}, og slib tappen let.'),
        ('Udløseren er stram at hive i', 'Klodsen og halen gnider. Slib dem '
         'glatte, og gnid et stearinlys på klodsens overside.'),
        ('Katapulten hopper eller vælter', 'Hold på pladen, eller lad den køre '
         '— den ruller bagud, fordi kastet skubber den anden vej.'),
        ('Kuglen går lige op i luften', 'Stoppinden sidder for højt. Den skal '
         f'standse armen ved {TAL["hvile"]}°, ikke ved lodret.'),
        ('Hjulene sidder fast', 'Akslen skal limes i hjulet og dreje frit i '
         'pladen — ikke omvendt.')])}
'''

open('katapult.html', 'w').write(side('Katapult · sløjd', KROP))

# ------------------------------------------------------- ungearket til print
UNGE = KROP.replace(
    '<a class="btnlink" href="materiale/ungeark-katapult.pdf">Hent opskriften '
    'som PDF</a>\n<a class="btnlink ghost" href="index.html">Fagoversigt</a>\n'
    '<button class="printbtn" onclick="window.print()">Print opskriften</button>',
    '<p><b>Navn:</b> <span class="skriv"></span> &nbsp; <b>Klasse:</b> '
    '<span class="skriv"></span> &nbsp; <b>Dato:</b> '
    '<span class="skriv"></span></p>')
open(os.path.join(SCRATCH, 'ungeark-katapult.html'), 'w').write(
    side('Katapult · sløjd', UNGE, fane=False))

# ============================================================ 5 · vejledning
UNGER = 24                      # én katapult pr. unge — skru op eller ned her
PR_KATAPULT = {                 # løbende meter og stykker pr. katapult
    'fyr 18 × 95 mm': (M['plade_l'] + 2 * M['opst_h'] + 120) / 1000,
    'glat liste 9 × 21 mm': (M['arm_l'] + M['stang_l'] + 2 * M['styr_l']) / 1000,
    'rundstok Ø8': 3 * 80 / 1000,
    'rundstok Ø6': 2 * M['aksel_l'] / 1000,
}
SPILD = 1.15                    # tilskæring koster træ


def opad(x, trin):
    return math.ceil(x / trin) * trin


INDKOEB = [
    ('Fyr 18 × 95 mm', f'{opad(PR_KATAPULT["fyr 18 × 95 mm"] * UNGER * SPILD, 0.5):.1f} m'
     .replace('.', ','), 'grundplade, opstandere, klods og skål'),
    ('Glat liste 9 × 21 mm',
     f'{opad(PR_KATAPULT["glat liste 9 × 21 mm"] * UNGER * SPILD, 0.5):.1f} m'
     .replace('.', ','), 'kastearm, udløserstang, styreklodser'),
    ('Krydsfiner 12 mm', '1 plade 600 × 600 mm',
     f'{4 * UNGER} hjul Ø{M["hjul_d"]} — der er plads til godt 120 i pladen'),
    ('Rundstok Ø8',
     f'{opad(PR_KATAPULT["rundstok Ø8"] * UNGER * SPILD, 1):.0f} m',
     'drejetap, stoppind og elastikpind'),
    ('Rundstok Ø6',
     f'{opad(PR_KATAPULT["rundstok Ø6"] * UNGER * SPILD, 1):.0f} m', 'aksler'),
    ('Skruer 4 × 40 mm', f'{4 * UNGER} stk', 'æske med 100 rækker'),
    ('Elastikker, brede', f'{4 * UNGER} stk',
     'tre pr. katapult plus reserve — de tørrer ud'),
    ('Trælim', '1 flaske', ''),
    ('Sandpapir korn 120 og 180', '', ''),
]

MODULER = [
    ('Modul 1 · tilskæring', 'Styklisten gennemgås, delene saves til og slibes. '
     'De to opstandere spændes sammen og bores på én gang.'),
    ('Modul 2 · boring og limning', 'Arm og plade bores, hjulene skæres med '
     'hulsav. Opstandere, styreklodser og udløserklods limes og skrues fast.'),
    ('Modul 3 · samling og prøveskud', 'Mekanikken samles, skålen limes på, '
     'hjulene monteres. Prøvefyring, og kastelængden måles og tegnes.'),
]

VEJL = f'''<section class="hero"><span class="pill">Vejledning til den voksne</span>
<h1>Katapult med udløser</h1>
<p>Sløjdforløb over tre moduler. Opskriften til ungerne ligger på
<b>katapult.html</b> og som PDF. Denne vejledning er det, der ikke skal stå på
ungernes ark: indkøb, maskinopstilling, og hvad der plejer at gå galt.</p>
<button class="printbtn" onclick="window.print()">Print vejledningen</button></section>

<h2 class="sec">Rammen</h2>
<div class="blok"><p>Regnet til <b>{UNGER} unger med hver sin katapult</b>, tre
moduler à 90 minutter. Bygger de to og to, halveres materialerne, og der bliver
god tid til at måle kastelængder i modul 3.</p>
<p>Katapulten er tegnet, så den kan bygges af almindeligt lagertræ: en 18 mm
fyrretræsplanke, en glat liste 9 × 21 og to tykkelser rundstok. Ingen del
kræver mere end lige skæring og lodret boring.</p></div>

{tabel(['Modul', 'Indhold'], MODULER)}

<div class="figur">{fig_side}
<div class="figtekst">Den færdige katapult. Ungerne får den samme tegning på
deres ark, sammen med målene på hver enkelt del.</div></div>

<h2 class="sec">Indkøb</h2>
{tabel(['Materiale', 'Mængde', 'Bruges til'], INDKOEB, ['', 'tal', ''])}
<p>Mængderne er regnet ud af styklisten og lagt 15 % til spild ved tilskæring.
Ændres antallet af unger, skal tallene regnes om — de står i
<b>claude/byg_katapult.py</b>.</p>

<h2 class="sec">De tre mål, der afgør om den virker</h2>
<div class="blok"><p><b>Stoppindens hul.</b> Det bestemmer, hvor armen standser.
Sidder det for højt, standser armen tæt på lodret, og kuglen går op i luften i
stedet for fremad. Med målene her standser armen ved
{TAL['hvile']}°, fordi pinden rammer armens overside — ikke dens midte. Det er
grunden til, at hullet ikke sidder præcis på 45°-linjen.</p>
<p><b>Luften mellem opstanderne.</b> {M['opst_luft']} mm. Læg kastearmen imellem
som afstandsklods, mens limen tørrer, så den ikke kommer til at klemme.</p>
<p><b>Elastikhakket.</b> {M['elast_greb']} mm ude ad armen. Flyttes det tættere
på drejetappen, strækkes elastikken mindre, og katapulten bliver slap. Flyttes
det længere ud, skurer elastikken mod stoppinden.</p></div>

<div class="to"><div class="figur">{fig_d1}</div><div class="figur">{fig_d2}</div></div>
<div class="figtekst">Udløseren er den del, der volder besvær. Klodsen skal
bære halen uden at klemme, og den skrå kant er det, der gør, at stangen kan
skubbes ind under halen igen.</div>

<h2 class="sec">Maskiner og opstilling</h2>
<div class="blok"><p>Bor alt i søjleboremaskine med emnet spændt fast. Hulsaven
Ø{M['hjul_d']} skal køre langsomt, og krydsfineren skal ligge på en offerplade,
ellers flosser udgangen.</p>
<p>Lav én opstander færdig selv og brug den som boreskabelon. Det tager fem
minutter og fjerner den fejl, der ellers rammer halvdelen af holdet: to
opstandere med huller, der ikke står over for hinanden.</p>
<p>Forbor til skruerne. 18 mm fyr flækker, når man skruer i enden uden at
forbore — Ø4 gennem pladen og Ø2,5 op i opstanderen.</p></div>

<h2 class="sec">Hvad der plejer at gå galt</h2>
{tabel(['Fejl', 'Sådan undgås den'],
       [('Drejetappen limes fast i armen', 'Pindene limes i opstanderne. Armen '
         'skal dreje på tappen, ikke med den.'),
        ('Akslen limes fast i pladen', 'Omvendt: limes i hjulet, drejer i '
         'pladen. Ellers kører den ikke.'),
        ('Hullerne i de to opstandere passer ikke', 'Spænd dem sammen og bor '
         'igennem begge på én gang.'),
        ('Udløseren binder', 'Styreklodserne er limet for tæt på stangen. Der '
         'skal være en halv millimeter luft — læg et stykke papir imellem, '
         'mens limen tørrer.'),
        ('Armen slår ikke helt op', 'Halen skraber mod udløserstangen. Slib '
         'halens underkant let skrå.'),
        ('Elastikken springer', 'Den er gammel. Nye elastikker til hvert hold, '
         'og briller på ved prøvefyring.')])}

<h2 class="sec">Det faglige</h2>
<div class="blok"><p>Katapulten er en anledning til tre ting, som ungerne kan
måle frem for at få at vide:</p>
<ul>
<li><b>Energi.</b> Arbejdet lægges i elastikken, når armen trækkes ned. Her
strækkes den fra {TAL['e_hvile']} til {TAL['e_spaendt']} mm — {TAL['straek']}
gange så lang.</li>
<li><b>Median frem for rekord.</b> Fem skud, og midtertallet bruges. Det er den
samme pointe som i statistik: ét godt skud er held.</li>
<li><b>Proportionalitet, der ikke holder.</b> To elastikker giver ikke dobbelt
kastelængde. Det er en god uenighed at have, før tallene er målt.</li>
</ul></div>

<h2 class="sec">Sikkerhed</h2>
{SIKKERHED.replace('<div class="blok advar"><h3>Sikkerhed — læses højt, før den første elastik sættes på</h3>', '<div class="blok advar"><h3>Læses højt for holdet</h3>')}
<div class="blok"><p>Aftal skuderetningen, før den første katapult er færdig.
En væg eller et gardin, ingen der går bag ved. Prøvefyring foregår ét hold ad
gangen, ikke tolv katapulter på én gang.</p></div>
'''

open(os.path.join(SCRATCH, 'vejledning-katapult.html'), 'w').write(
    side('Vejledning · katapult', VEJL, fane=False))

# ============================================================ 6 · nøgletal
print(f'skrevet:  katapult.html')
print(f'skrevet:  {SCRATCH}/ungeark-katapult.html')
print(f'skrevet:  {SCRATCH}/vejledning-katapult.html')
print(f'stop:     armen standser ved {HVILE:.1f}° '
      f'(stoppind {math.hypot(STOP[0] - DREJ[0], STOP[1] - DREJ[1]):.1f} mm '
      f'fra drejetappen)')
print(f'elastik:  {E_HVILE:.0f} mm i hvile -> {E_SPAENDT:.0f} mm spændt '
      f'= {E_SPAENDT / E_HVILE:.2f} gange')
print(f'frigang:  elastik {AFSTAND_STOP:.1f} mm fra stoppinden · '
      f'hale {HALE_LAVEST:.1f} mm over stangen ({M["stang_t"]} mm tyk)')
print(f'indkøb:   til {UNGER} katapulter')
