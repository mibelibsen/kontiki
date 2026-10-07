# -*- coding: utf-8 -*-
"""Bygger en bordplan til 9. klasse som PDF i A4 paa tvaers.

Navnene laeses fra spoergeskema/unger.txt, som er udelukket fra deploy.
PDF'en skrives i vejledning/, som ogsaa er udelukket. **Bordplanen maa ikke
ligge paa sitet** - den indeholder ungernes navne.

Opstillingen er tre kolonner med dobbeltborde og tavlen foran. Skal den laves
om, er det de to tal i OPSTILLING, der skal rettes.

    python3 claude/byg_bordplan.py

Bindinger staar i SAMMEN og BLANDES ikke væk: scriptet naegter at skrive
filen, hvis en binding ikke er overholdt.
"""
import os
import random
import subprocess
import sys
from datetime import date

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LISTE = os.path.join(ROD, 'spoergeskema', 'unger.txt')
DATO = date.today().isoformat()
UD_HTML = os.path.join(ROD, 'vejledning', f'bordplan-{DATO}.html')
UD_PDF = os.path.join(ROD, 'vejledning', f'bordplan-{DATO}.pdf')
UD_KORT = os.path.join(ROD, 'vejledning', f'bordkort-{DATO}.pdf')

# Lokalet, set fra tavlen. Bord 1 er 7-mandsbordet. Det staar midt i lokalet
# paa langs, med kortenden vaek fra tavlen: tre paa hver langside og én for
# enden - den plads, der er laengst fra tavlen.
#
# Planen er tegnet SET FRA TAVLEN. Det vender arket om: staar man ved tavlen
# og ser ind i lokalet, har man hoejre vaeg paa sin hoejre haand - men paa et
# kort med tavlen oeverst ligger den vaeg i arkets VENSTRE side. Alt hvad der
# hedder venstre og hoejre herunder er set fra tavlen, ikke fra arket.
#
#   +-------------------- T A V L E --------------------+
#   |                                                   |
#   |                                            [2]    |
#   | []                  | 1 |                  | |    |
#   | doer    | 4 |       |   |                         |
#   |         |   |       (for enden)                   |
#   | []                                         [3]    |
#   | doer                                       | |    |
#   |                     [  5  ]                       |
#   +---------------------------------------------------+
#
# De fire andre er 4-mandsborde: to op ad venstre vaeg, ét op ad hoejre vaeg
# mellem lokalets to doere, og ét op ad bagvaeggen. De tre ved en sidevaeg
# vender paa langs ad vaeggen, saa der sidder to paa hver side; bordet ved
# bagvaeggen vender paa tvaers. Skal lokalet laves om, er det her.
LANGS, LODRET, TVAERS = 'langs', 'lodret', 'tvaers'
LOKALE = (
    (LANGS,  'midt'),        # bord 1 - 7-mandsbordet
    (LODRET, 'venstre'),     # bord 2 - venstre vaeg, forrest
    (LODRET, 'venstre'),     # bord 3 - venstre vaeg, bagerst
    (LODRET, 'hoejre'),      # bord 4 - hoejre vaeg, mellem doerene
    (TVAERS, 'bag'),         # bord 5 - bagvaeggen
)
BORDE = len(LOKALE)
RETNING = [r for r, _ in LOKALE]

# Bindingerne staar i spoergeskema/bindinger.json. Den er i git, saa de ikke
# gaar tabt mellem sessioner - det var netop det, der skete sidst, hvor hvem
# der var tvillinger laa i en samtale og ikke i repoet. Mappen er udelukket i
# .vercelignore, saa filen ikke kommer paa sitet. Den ser saadan ud:
#
#   {"sammen":     [["Emilie", "Anna"]],
#    "samme_bord": [["Anna", "Oskar"]],
#    "adskilt":    [["Milius", "William"], ["Johan", "Silke"]],
#    "pladser":    [6, 4, 4, 4, 4],
#    "fast":       [["Emilie", "Anna", ...], ...]}
#
# sammen     = skal sidde ved siden af hinanden ved samme bord
# samme_bord = skal sidde ved samme bord, men ikke noedvendigvis som nabo
# adskilt    = maa ikke sidde ved samme bord (ogsaa tvillinger)
# pladser    = stolene ved hvert bord. Bordene er ikke lige store: bord 1 har
#              seks pladser, de fire andre har fire. Staar der flere ved et
#              bord, end der er stole, siger scriptet det - i terminalen og
#              nederst paa oversigten. Det er ikke noget, der skal opdages,
#              naar ungerne staar i lokalet.
# fast       = selve planen. Staar den der, blandes der ikke: planen tegnes som
#              den er, og bindingerne tjekkes. Saa flytter man én unge ved at
#              rette én linje, i stedet for at hele klassen bytter plads.
BINDINGER = os.path.join(ROD, 'spoergeskema', 'bindinger.json')


def bindinger():
    if not os.path.exists(BINDINGER):
        print(f'BEMÆRK: {BINDINGER} findes ikke — bygger uden bindinger')
        return [], [], [], [], []
    import json
    with open(BINDINGER, encoding='utf-8') as f:
        d = json.load(f)
    return ([tuple(p) for p in d.get('sammen', [])],
            [tuple(p) for p in d.get('samme_bord', [])],
            [tuple(p) for p in d.get('adskilt', [])],
            [list(b) for b in d.get('fast', [])],
            list(d.get('pladser', [])))


SAMMEN, SAMME_BORD, ADSKILT, FAST, PLADSER = bindinger()

FROE = 20261006          # fast, saa den samme plan kan bygges igen


def unger():
    with open(LISTE, encoding='utf-8') as f:
        navne = [l.strip() for l in f
                 if l.strip() and not l.lstrip().startswith('#')]
    assert len(navne) == len(set(navne)), 'to unger har samme navn i listen'
    return navne


NAVNE = unger()


def stoerrelser(antal, borde):
    """Fordeler ungerne saa jaevnt som muligt: 23 paa 5 borde bliver 5,5,5,4,4."""
    hel, rest = divmod(antal, borde)
    ud = [hel + 1] * rest + [hel] * (borde - rest)
    assert sum(ud) == antal and max(ud) - min(ud) <= 1, ud
    return ud


# Bordene er ikke lige store: bord 1 er 6-mandsbordet. Naar der er en fast
# plan, er det den, der bestemmer, hvor mange der sidder ved hvert bord.
STOERRELSER = [len(b) for b in FAST] if FAST else stoerrelser(len(NAVNE), PLADSER and len(PLADSER) or BORDE)
# Hvor mange der kan sidde ved ét bord, er noget ved lokalet, ikke noget
# scriptet kan vide. Staar pladserne i bindinger.json, er det dem der gaelder;
# ellers er otte en graense, der fanger en tastefejl i antallet af borde.
assert max(STOERRELSER) <= (max(PLADSER) if PLADSER else 8), (
    f'{max(STOERRELSER)} unger ved ét bord er flere, end der er stole til')

if PLADSER:
    assert len(PLADSER) == BORDE, f'{len(PLADSER)} tal i pladser, {BORDE} borde'
    # 23 unger og 22 stole gaar ikke op. Det skal staa nederst paa oversigten,
    # ikke opdages i lokalet.
    MANGLER = [(i + 1, n - k) for i, (n, k) in enumerate(zip(STOERRELSER, PLADSER))
               if n > k]
    for nr, ekstra in MANGLER:
        print(f'ADVARSEL: bord {nr} har {ekstra} unge mere, end der er stole til')
    if sum(PLADSER) < len(NAVNE):
        print(f'ADVARSEL: {len(NAVNE)} unger, {sum(PLADSER)} pladser '
              f'— der mangler {len(NAVNE) - sum(PLADSER)} stol(e) i lokalet')
else:
    MANGLER = []

for par in SAMMEN + SAMME_BORD + ADSKILT:
    for n in par:
        assert n in NAVNE, f'{n} staar ikke i klasselisten'
for a, b in ADSKILT:
    assert not any({a, b} <= set(p) for p in SAMMEN + SAMME_BORD), \
        f'{a} og {b} staar baade som sammen og som adskilt'


def _fordel(r):
    """Ét forsoeg: bundne par ved samme bord foerst, resten fyldt paa."""
    bundne = {n for par in SAMMEN for n in par}
    resten = [n for n in NAVNE if n not in bundne]
    r.shuffle(resten)
    borde = [[] for _ in STOERRELSER]
    for i, par in enumerate(SAMMEN):
        assert len(par) <= STOERRELSER[i], 'bindingen fylder mere end bordet'
        borde[i].extend(par)
    for i, plads_i_alt in enumerate(STOERRELSER):
        while len(borde[i]) < plads_i_alt:
            borde[i].append(resten.pop())
    assert not resten, 'der blev unger tilovers'
    return borde


def naboer(nr, navne):
    """Parrene, der faktisk sidder ved siden af hinanden ved bord nr.

    Pladserne staar i raekkefoelge i planen. Ved et bord paa tvaers er de
    foerste halvdel den side, der vender mod tavlen, og resten den anden side.
    Ved 7-mandsbordet er 0-2 den venstre langside, 3-5 den hoejre, og 6 er
    pladsen for enden - den roerer den bageste plads paa begge langsider.
    Over for hinanden er ikke ved siden af hinanden.
    """
    ud = set()
    if RETNING[nr] == LANGS:
        v, h, ende = navne[:3], navne[3:6], navne[6:]
        for side in (v, h):
            ud |= {frozenset(par) for par in zip(side, side[1:])}
        if ende:
            ud |= {frozenset((ende[0], side[-1])) for side in (v, h) if side}
    else:
        halv = (len(navne) + 1) // 2
        for side in (navne[:halv], navne[halv:]):
            ud |= {frozenset(par) for par in zip(side, side[1:])}
    return ud


def _holder(borde):
    for a, b in ADSKILT:
        if any(a in bo and b in bo for bo in borde):
            return False
    for a, b in SAMME_BORD:
        if not any(a in bo and b in bo for bo in borde):
            return False
    for a, b in SAMMEN:
        if not any(frozenset((a, b)) in naboer(i, bo)
                   for i, bo in enumerate(borde)):
            return False
    return True


def plads(forsoeg=5000):
    """Blander, til alle bindinger holder. Med faa bindinger gaar det paa faa
    forsoeg; en umulig kombination opdages i stedet for at blive tegnet."""
    for i in range(forsoeg):
        borde = _fordel(random.Random(FROE + i))
        if _holder(borde):
            if i:
                print(f'fordeling fundet efter {i + 1} forsøg')
            return borde
    raise AssertionError(
        f'ingen fordeling opfylder alle bindinger efter {forsoeg} forsøg — '
        f'se efter en binding, der modsiger en anden')


def fast_plan():
    """Tegner planen fra bindinger.json i stedet for at blande en ny. En
    rettelse dér skal fange sig selv her, ikke staa paa et ark i klassen."""
    flad = [n for b in FAST for n in b]
    assert len(flad) == len(set(flad)), 'en unge staar to steder i planen'
    mangler = sorted(set(NAVNE) - set(flad))
    ukendte = sorted(set(flad) - set(NAVNE))
    assert not mangler, f'ingen plads til {", ".join(mangler)}'
    assert not ukendte, f'{", ".join(ukendte)} staar ikke i klasselisten'
    assert len(FAST) == BORDE, f'planen har {len(FAST)} borde, lokalet har {BORDE}'
    return [list(b) for b in FAST]


BORD = fast_plan() if FAST else plads()
assert len(BORD) == BORDE
assert [len(b) for b in BORD] == STOERRELSER
assert sorted(n for b in BORD for n in b) == sorted(NAVNE), 'en unge er blevet væk'
assert _holder(BORD), 'bindingerne holder ikke'


# ---------------------------------------------------------------------------
# Tegningen. Alle maal i mm, og alle koordinater beregnes.
#
# Lokalet er ca. 6 m bredt og 8 m dybt - dybere end bredt. Derfor staar
# oversigten paa HOEJKANT. Paa tvaers ville rummet blive tegnet bredere end
# dybt, og saa ligner planen ikke det lokale, den handler om.
# ---------------------------------------------------------------------------
RUM_BREDDE_M, RUM_DYBDE_M = 6.0, 8.0

SIDE_B, SIDE_H = 210, 297          # A4 paa hoejkant
MARGEN = 10
FOD = 14                           # plads til forklaringen under lokalet

# rummet fylder siden ud i den retning, der er plads til, og beholder sit
# forhold. Maalestokken foelger af det og staar i foden.
_b = SIDE_B - 2 * MARGEN
_h = SIDE_H - 2 * MARGEN - FOD
METER = min(_b / RUM_BREDDE_M, _h / RUM_DYBDE_M)
RUM_B, RUM_H = RUM_BREDDE_M * METER, RUM_DYBDE_M * METER
RUM_X0 = (SIDE_B - RUM_B) / 2
RUM_Y0 = MARGEN
RUM_X1, RUM_Y1 = RUM_X0 + RUM_B, RUM_Y0 + RUM_H

LUFT_VAEG = 3                      # fra vaeg til naermeste bord
LUFT_TAVLE = 20                    # fra tavlevaeggen ned til forreste bord
DOER_STRIBE = LUFT_VAEG            # doerene maerkes uden for vaeggen, saa de
                                   # tager ikke plads fra bordene

PLADS_H = 9                        # hoejden paa et navneskilt
# Skiltene er bredere end en stol, ellers kan navnene ikke staa der. Jo
# bredere de er, jo smallere bliver gangene mellem bordene - og gangene skal
# kunne ses, for ungerne skal kunne komme hen til deres plads.
C = 17                             # navneskilt langs et bord, der staar lodret
B_LODRET = 13                      # bordpladen paa et 4-mandsbord paa langs
B7 = 17                            # bordpladen paa 7-mandsbordet
B_TVAERS = 44                      # bordpladen paa bordet ved bagvaeggen
BORD_H = 17                        # dybden paa bordet ved bagvaeggen
SKILT_LUFT = 5                     # mellem to skilte paa samme side

H_LODRET = 2 * PLADS_H + SKILT_LUFT + 4
H7 = 3 * PLADS_H + 2 * SKILT_LUFT + 4

BLOK = {
    LANGS:  (2 * C + 4 + B7, H7 + 2 + PLADS_H),
    LODRET: (2 * C + 4 + B_LODRET, H_LODRET),
    TVAERS: (B_TVAERS, 2 * PLADS_H + 4 + BORD_H),
}

INK, BLA, MUT, LIN, GRO = '#1a2233', '#1f6fd6', '#586074', '#c9d2e0', '#1a8f5e'
TRAE = '#f4f6fb'
VAEG = '#8b94a6'

# --- hvor bordene staar -----------------------------------------------------
INDE_X0, INDE_X1 = RUM_X0 + LUFT_VAEG, RUM_X1 - DOER_STRIBE
INDE_Y0, INDE_Y1 = RUM_Y0 + LUFT_TAVLE, RUM_Y1 - LUFT_VAEG

# bordet ved bagvaeggen staar midt for, helt nede
_bb, _bh = BLOK[TVAERS]
BAG = ((SIDE_B - _bb) / 2, INDE_Y1 - _bh)

# de tre andre staar i zonen mellem tavlen og bagvaeggens bord
ZONE_Y0, ZONE_Y1 = INDE_Y0, BAG[1] - 10
ZONE_H = ZONE_Y1 - ZONE_Y0

# Tre spalter paa tvaers. 7-mandsbordet staar midt i LOKALET - ikke midt i
# det, der er tilbage, naar doerstriben er trukket fra, for saa ville det
# staa en smule til venstre uden grund. De to andre staar op ad hver sin vaeg.
# Set fra tavlen ligger hoejre vaeg i arkets venstre side, og omvendt.
X_MIDT = (SIDE_B - BLOK[LANGS][0]) / 2
X_HOEJRE = INDE_X0                              # hoejre vaeg set fra tavlen
X_VENSTRE = INDE_X1 - BLOK[LODRET][0]           # venstre vaeg set fra tavlen
GANG = min(X_MIDT - (X_HOEJRE + BLOK[LODRET][0]),
           X_VENSTRE - (X_MIDT + BLOK[LANGS][0]))
assert GANG / METER >= 0.3, (
    f'der er kun {GANG / METER:.2f} m mellem bordene — der skal kunne gås '
    f'imellem dem, så gør skiltene smallere eller bordene færre')

# De to borde ved venstre vaeg staar ved hver sin ende af vaeggen - det ene
# fremme ved tavlen, det andet tilbage mod bagvaeggen. Fordeles de jaevnt,
# klumper de sig midt paa vaeggen med tomt gulv i begge ender.
VENSTRE_Y = [ZONE_Y0, ZONE_Y1 - H_LODRET]

HJOERNE = [
    (X_MIDT, ZONE_Y0 + (ZONE_H - BLOK[LANGS][1]) / 2),      # 1: midt i lokalet
    (X_VENSTRE, VENSTRE_Y[0]),                              # 2: venstre, forrest
    (X_VENSTRE, VENSTRE_Y[1]),                              # 3: venstre, bagerst
    (X_HOEJRE, ZONE_Y0 + (ZONE_H - H_LODRET) / 2),          # 4: hoejre vaeg
    BAG,                                                    # 5: bagvaeggen
]

# intet bord maa staa oven i et andet. Det er ikke til at se paa en tegning,
# der er regnet forkert ud - derfor tjekkes det.
for _i in range(BORDE):
    _x, _y = HJOERNE[_i]
    _w, _hh = BLOK[RETNING[_i]]
    for _j in range(_i + 1, BORDE):
        _x2, _y2 = HJOERNE[_j]
        _w2, _h2 = BLOK[RETNING[_j]]
        assert not (_x < _x2 + _w2 and _x2 < _x + _w
                    and _y < _y2 + _h2 and _y2 < _y + _hh), \
            f'bord {_i + 1} og bord {_j + 1} staar oven i hinanden'


def skriftstoerrelse(navne_og_bredder, loft, gulv, luft):
    """Én stoerrelse til hele arket: den stoerste, hvor det laengste navn
    stadig er inden for sit skilt. Fed Helvetica fylder ca. 0,60 em pr. tegn.
    Regnes navnene hver for sig, bliver Nor dobbelt saa stor som Helene paa
    samme bord; regnes de bord for bord, staar ét bord mindre end naboen,
    fordi ét navn er langt. Begge dele ligner en forskel, der ikke er der."""
    st = min([loft] + [(b - luft) / (len(n) * 0.60) for n, b in navne_og_bredder])
    vaerst = min(navne_og_bredder, key=lambda nb: nb[1] / (len(nb[0]) * 0.60))
    assert st >= gulv, \
        f'{vaerst[0]} kan ikke staa paa en plads paa {vaerst[1]:.1f} mm'
    return st


def skilt(s, x, y, b, navn, bundet, st, h=PLADS_H):
    kant = GRO if bundet else LIN
    s.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{b:.2f}" height="{h}" '
             f'rx="2" fill="#fff" stroke="{kant}" '
             f'stroke-width="{0.9 if bundet else 0.4}"/>')
    s.append(f'<text x="{x + b / 2:.2f}" y="{y + h / 2 + st * 0.35:.2f}" '
             f'text-anchor="middle" fill="{INK}" font-size="{st:.2f}" '
             f'font-weight="bold">{navn}</text>')


def _bordplade(s, x, y, b, h, nr, lodret):
    s.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{b:.2f}" height="{h:.2f}" '
             f'rx="3" fill="{TRAE}" stroke="{LIN}" stroke-width="0.5"/>')
    cx, cy = x + b / 2, y + h / 2
    sz = 6
    drej = f' transform="rotate(-90 {cx:.2f} {cy:.2f})"' if lodret else ''
    s.append(f'<text x="{cx:.2f}" y="{cy + sz * 0.37:.2f}"{drej} '
             f'text-anchor="middle" fill="{MUT}" font-size="{sz}" '
             f'letter-spacing="0.6">BORD {nr}</text>')


def _sider_lodret(navne, antal_pr_side):
    """De to langsider, set fra tavlen. Foerste halvdel af pladserne er den
    hoejre side - den ligger i arkets venstre kant, fordi planen er tegnet
    set fra tavlen."""
    return navne[:antal_pr_side], navne[antal_pr_side:2 * antal_pr_side]


def _pladser_lodret(navne, x, y, plade_b, pr_side, hoejde):
    """Et bord, der staar paa langs ad lokalet: lige mange paa hver langside,
    og skiltene staar ud for hinanden."""
    hoejre, venstre = _sider_lodret(navne, pr_side)
    bx = x + C + 2
    y0 = y + (hoejde - (pr_side * PLADS_H + (pr_side - 1) * SKILT_LUFT)) / 2
    ud = []
    for side, sx in ((hoejre, x), (venstre, bx + plade_b + 2)):
        for j, n in enumerate(side):
            ud.append((n, sx, y0 + j * (PLADS_H + SKILT_LUFT), C))
    return ud, (bx, y, plade_b, hoejde, True)


def _pladser_langs(navne, x, y):
    """7-mandsbordet: tre paa hver langside og én for enden, vaek fra tavlen."""
    ud, plade = _pladser_lodret(navne[:6], x, y, B7, 3, H7)
    for n in navne[6:]:
        ud.append((n, x + (BLOK[LANGS][0] - C) / 2, y + H7 + 2, C))
    return ud, plade


def _pladser_tvaers(navne, x, y):
    """Bordet ved bagvaeggen: halvdelen mod tavlen, resten med ryggen til."""
    halv = (len(navne) + 1) // 2
    ud = []
    for side, sy in ((navne[:halv], y),
                     (navne[halv:], y + PLADS_H + 2 + BORD_H + 2)):
        b = (B_TVAERS - (len(side) - 1) * 2) / len(side)
        for j, n in enumerate(side):
            ud.append((n, x + j * (b + 2), sy, b))
    return ud, (x, y + PLADS_H + 2, B_TVAERS, BORD_H, False)


def _skilte(nr):
    navne, (x, y) = BORD[nr], HJOERNE[nr]
    if RETNING[nr] == LANGS:
        return _pladser_langs(navne, x, y)
    if RETNING[nr] == LODRET:
        return _pladser_lodret(navne, x, y, B_LODRET, 2, H_LODRET)
    return _pladser_tvaers(navne, x, y)


def tegn():
    s = [f'<svg viewBox="0 0 {SIDE_B} {SIDE_H}" width="{SIDE_B}mm" '
         f'height="{SIDE_H}mm" xmlns="http://www.w3.org/2000/svg" '
         f'font-family="Helvetica, Arial, sans-serif">']

    # lokalets vaegge
    s.append(f'<rect x="{RUM_X0:.2f}" y="{RUM_Y0:.2f}" width="{RUM_B:.2f}" '
             f'height="{RUM_H:.2f}" rx="2" fill="none" stroke="{VAEG}" '
             f'stroke-width="1.1"/>')
    # tavlen paa den forreste vaeg
    tb = RUM_B * 0.5
    s.append(f'<rect x="{(SIDE_B - tb) / 2:.2f}" y="{RUM_Y0 - 3}" '
             f'width="{tb:.2f}" height="6" rx="1.5" fill="{INK}"/>')
    s.append(f'<text x="{SIDE_B / 2}" y="{RUM_Y0 + 1.4}" text-anchor="middle" '
             f'fill="#fff" font-size="4" letter-spacing="1.6">TAVLE</text>')
    # maalene paa rummet
    s.append(f'<text x="{RUM_X1 - 2:.2f}" y="{RUM_Y1 - 2.5:.2f}" '
             f'text-anchor="end" fill="{VAEG}" font-size="4">'
             f'{RUM_BREDDE_M:.0f} m × {RUM_DYBDE_M:.0f} m · set fra tavlen</text>')

    # de to doere i hoejre vaeg, med bord 4 midt imellem
    # doerene sidder i hoejre vaeg - paa arket er det den venstre kant
    vaeg = RUM_X0
    midt_4 = HJOERNE[3][1] + BLOK[LODRET][1] / 2
    doer_h, doer_afstand, blad = 24, 45, 2
    for d in (midt_4 - doer_afstand, midt_4 + doer_afstand):
        y = d - doer_h / 2
        assert RUM_Y0 + 4 <= y and y + doer_h <= RUM_Y1 - 4, \
            'døren falder uden for væggen'
        s.append(f'<rect x="{vaeg - 1.4:.2f}" y="{y:.2f}" width="2.8" '
                 f'height="{doer_h}" fill="#fff"/>')
        for kant in (y, y + doer_h):
            s.append(f'<path d="M {vaeg - blad:.2f} {kant:.2f} '
                     f'L {vaeg + blad:.2f} {kant:.2f}" fill="none" '
                     f'stroke="{VAEG}" stroke-width="0.7"/>')
        # maerket staar uden for vaeggen: inde i lokalet ville det tage den
        # plads, bordet ved hoejre vaeg skal bruge
        dx = vaeg - 4.5
        s.append(f'<text x="{dx:.2f}" y="{d + 1.2:.2f}" fill="{VAEG}" '
                 f'font-size="3.6" letter-spacing="0.8" text-anchor="middle" '
                 f'transform="rotate(-90 {dx:.2f} {d:.2f})">DØR</text>')

    bundne = [set(p) for p in SAMMEN]
    alle = [(n, b) for nr in range(BORDE) for n, _, _, b in _skilte(nr)[0]]
    st = skriftstoerrelse(alle, 6.2, 2.9, 2)
    for nr in range(BORDE):
        skilte, plade = _skilte(nr)
        _bordplade(s, *plade[:4], nr + 1, plade[4])
        nb = naboer(nr, BORD[nr])
        for n, sx, sy, b in skilte:
            bundet = any(n in par and frozenset(par) in nb for par in bundne)
            skilt(s, sx, sy, b, n, bundet, st)

    # foden staar i linjer under hinanden. Skrives to ting paa samme linje i
    # hver sin ende, moedes de paa midten, saa snart den ene bliver lang.
    linjer = []
    if MANGLER:
        mgl = ', '.join(f'bord {nr}: {e} for meget' for nr, e in MANGLER)
        linjer.append((f'Flere end der er stole til — {mgl}', '#b03030', True))
    linjer.append((f'Grøn kant: {", ".join(f"{a} ved siden af {b}" for a, b in SAMMEN)}',
                   MUT, False))
    fod = (f'Bordplan · 9. klasse · {DATO} · {len(NAVNE)} unger på '
           f'{BORDE} borde · {sum(PLADSER) if PLADSER else len(NAVNE)} pladser')
    linjer.append((fod, MUT, False))
    linjer.append((f'Lokalet er {RUM_BREDDE_M:.0f} × {RUM_DYBDE_M:.0f} m og tegnet '
                   f'i 1:{1000 / METER:.0f}. Navneskiltene er større end en '
                   f'stol, så de kan læses.', VAEG, False))
    fy = SIDE_H - MARGEN - 3 - 4.8 * (len(linjer) - 1)
    for tekst, farve, fed in linjer:
        x = MARGEN
        if 'Grøn kant' in tekst:
            s.append(f'<rect x="{MARGEN}" y="{fy - 3.6:.2f}" width="4.2" '
                     f'height="4.2" rx="1" fill="#fff" stroke="{GRO}" '
                     f'stroke-width="0.9"/>')
            x = MARGEN + 6.4
        vaegt = ' font-weight="bold"' if fed else ''
        s.append(f'<text x="{x:.2f}" y="{fy:.2f}" fill="{farve}" '
                 f'font-size="{4.2 if farve != VAEG else 3.8}"'
                 f'{vaegt}>{tekst}</text>')
        fy += 4.8
    s.append('</svg>')
    return ''.join(s)


# ---------------------------------------------------------------------------
# Bordkortene: ét ark pr. bord, der laegges paa bordet.
#
# Navnene paa den side, der vender vaek fra tavlen, staar paa hovedet. Det er
# med vilje: arket ligger fladt paa bordet, og saa kan hver unge laese sit eget
# navn rigtigt vej fra sin egen plads. Pilen viser, hvilken kant der skal vende
# mod tavlen, saa arket ikke bliver lagt forkert.
#
# Fire af bordene staar paa langs ad lokalet - 7-mandsbordet i midten og de
# tre ved sidevaeggene. Deres ark ligger med laengden ud ad bordet, og saa
# peger tavlen mod arkets venstre kant og ikke opad. Paa 7-mandsbordet staar
# pladsen for enden ude i hoejre side, drejet en kvart omgang - den vej, den
# unge sidder. Kun bordet ved bagvaeggen staar paa tvaers, og dets ark vender
# som foer, med tavlen opad.
# ---------------------------------------------------------------------------
K_B, K_H = 297, 210                 # A4 paa tvaers
K_MARGEN = 16
K_RAEKKE_H = 46                     # hoejden paa en navneraekke
K_BAAND = 26                        # midterbaandet, hvor bordnummeret staar
K_ENDE_B = 52                       # pladsen for enden, ude i siden
assert K_BAAND >= 20, 'bordnummeret staar i vejen for navnene'
assert 2 * K_RAEKKE_H + K_BAAND + 2 * K_MARGEN <= K_H, 'arket er ikke hoejt nok'


def bordkort(nr, navne):
    retning = RETNING[nr - 1]
    langs = retning in (LANGS, LODRET)
    if langs:
        # arket ligger ud ad bordet. Drejes planen en kvart omgang, kommer
        # hoejre langside (set fra tavlen) op og venstre ned.
        # Arket ligger ud ad bordet med tavlen mod venstre kant. Saadan set
        # kommer den langside, der er VENSTRE set fra tavlen, op foroven.
        pr_side = 3 if retning == LANGS else 2
        hoejre, venstre = _sider_lodret(navne, pr_side)
        oeverst, nederst, ende = venstre, hoejre, navne[2 * pr_side:]
    else:
        halv = (len(navne) + 1) // 2
        oeverst, nederst, ende = navne[:halv], navne[halv:], []

    s = [f'<svg viewBox="0 0 {K_B} {K_H}" width="{K_B}mm" height="{K_H}mm" '
         f'xmlns="http://www.w3.org/2000/svg" '
         f'font-family="Helvetica, Arial, sans-serif">']

    hoejre_kant = K_B - K_MARGEN - (K_ENDE_B + 8 if ende else 0)
    bredde = lambda r: (hoejre_kant - K_MARGEN - (len(r) - 1) * 6) / len(r)
    ende_h = 2 * K_RAEKKE_H + K_BAAND
    maal = [(n, bredde(r)) for r in (oeverst, nederst) if r for n in r]
    maal += [(n, ende_h) for n in ende]
    st = skriftstoerrelse(maal, 26, 10, 8)

    # pilen mod tavlen: opad ved bordene paa tvaers, mod venstre ved 7-mandsbordet
    if langs:
        # teksten drejes med arket, men en pil af tekst ville saa pege op og
        # ned i stedet for mod tavlen. Den tegnes derfor som en trekant.
        px, py = K_MARGEN - 5, K_H / 2
        s.append(f'<text x="{px}" y="{py}" fill="{MUT}" font-size="5" '
                 f'letter-spacing="1.8" text-anchor="middle" '
                 f'transform="rotate(-90 {px} {py})">MOD TAVLEN</text>')
        for dy in (-46, 46):
            s.append(f'<path d="M {px - 2.6:.2f} {py + dy:.2f} '
                     f'l 4.4 -2.6 l 0 5.2 Z" fill="{MUT}"/>')
    else:
        s.append(f'<text x="{K_B / 2}" y="{K_MARGEN + 4}" text-anchor="middle" '
                 f'fill="{MUT}" font-size="5" letter-spacing="1.8">'
                 f'&#9650;  MOD TAVLEN  &#9650;</text>')

    midte = K_H / 2
    for navne_her, paa_hovedet in ((oeverst, False), (nederst, True)):
        if not navne_her:
            continue
        y = (midte - K_BAAND / 2 - K_RAEKKE_H if not paa_hovedet
             else midte + K_BAAND / 2)
        bred = bredde(navne_her)
        for j, n in enumerate(navne_her):
            x = K_MARGEN + j * (bred + 6)
            cx, cy = x + bred / 2, y + K_RAEKKE_H / 2
            drej = f' transform="rotate(180 {cx:.2f} {cy:.2f})"' if paa_hovedet else ''
            s.append(f'<g{drej}>')
            s.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{bred:.2f}" '
                     f'height="{K_RAEKKE_H}" rx="4" fill="#fff" stroke="{LIN}" '
                     f'stroke-width="0.6"/>')
            s.append(f'<text x="{cx:.2f}" y="{cy + st * 0.35:.2f}" '
                     f'text-anchor="middle" fill="{INK}" font-size="{st:.1f}" '
                     f'font-weight="bold">{n}</text>')
            s.append('</g>')

    # pladsen for enden: den unge sidder yderst og ser ind mod tavlen, saa
    # navnet drejes en kvart omgang og staar rigtigt vej fra den plads
    for n in ende:
        x, y = K_B - K_MARGEN - K_ENDE_B, midte - ende_h / 2
        cx, cy = x + K_ENDE_B / 2, midte
        s.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{K_ENDE_B}" '
                 f'height="{ende_h}" rx="4" fill="#fff" stroke="{LIN}" '
                 f'stroke-width="0.6"/>')
        s.append(f'<text x="{cx:.2f}" y="{cy + st * 0.35:.2f}" '
                 f'transform="rotate(-90 {cx:.2f} {cy:.2f})" '
                 f'text-anchor="middle" fill="{INK}" font-size="{st:.1f}" '
                 f'font-weight="bold">{n}</text>')

    s.append(f'<text x="{(K_MARGEN + hoejre_kant) / 2:.2f}" y="{midte + 5.2}" '
             f'text-anchor="middle" fill="{MUT}" font-size="14" '
             f'letter-spacing="5" font-weight="bold">BORD {nr}</text>')
    s.append(f'<text x="{K_B / 2}" y="{K_H - K_MARGEN + 2}" text-anchor="middle" '
             f'fill="{MUT}" font-size="4.2">9. klasse · {DATO} · '
             f'{len(navne)} pladser</text>')
    s.append('</svg>')
    return ''.join(s)


KORT_HTML = (
    '<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
    '<title>Bordkort · 9. klasse</title><style>'
    '*{box-sizing:border-box}body{margin:0}'
    'svg{display:block}'
    '.ark{page-break-after:always}.ark:last-child{page-break-after:auto}'
    '@page{size:A4 landscape;margin:0}'
    '</style></head><body>'
    + ''.join(f'<div class="ark">{bordkort(i, b)}</div>'
              for i, b in enumerate(BORD, 1))
    + '</body></html>')


# alfabetisk opslag, saa en vikar kan finde en unge uden at lede i tegningen
opslag = sorted((n, i + 1) for i, b in enumerate(BORD) for n in b)
rk = ''.join(f'<tr><td>{n}</td><td>{b}</td></tr>' for n, b in opslag)

HTML = f'''<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">
<title>Bordplan · 9. klasse · {DATO}</title><style>
*{{box-sizing:border-box}}
body{{margin:0;font-family:Helvetica,Arial,sans-serif;color:{INK}}}
svg{{display:block}}
.liste{{page-break-before:always;padding:14mm}}
.liste h1{{font-size:15pt;margin:0 0 2mm}}
.liste p{{color:{MUT};font-size:9.5pt;margin:0 0 6mm}}
table{{border-collapse:collapse;font-size:10pt}}
td{{border:1px solid {LIN};padding:2mm 4mm}}
td:last-child{{text-align:center;font-weight:bold;color:{BLA};width:18mm}}
.kol{{column-count:2;column-gap:10mm}}
/* oversigten staar paa hoejkant, fordi lokalet er dybere end bredt */
@page{{size:A4;margin:0}}
@media print{{.liste{{margin:0}}}}
</style></head><body>
{tegn()}
<div class="liste"><h1>Bordplan · 9. klasse</h1>
<p>{DATO} · {len(NAVNE)} unger · {BORDE} gruppeborde med
{', '.join(str(n) for n in STOERRELSER)} pladser. Bord 1 er 7-mandsbordet midt
i lokalet; bord 2 og 3 står ved venstre væg, bord 4 ved højre væg mellem de to
døre, og bord 5 ved bagvæggen. Alt er set fra tavlen.</p>
<div class="kol"><table><tbody>{rk}</tbody></table></div></div>
</body></html>'''

os.makedirs(os.path.dirname(UD_HTML), exist_ok=True)
for html_tekst, maal in ((HTML, UD_PDF), (KORT_HTML, UD_KORT)):
    with open(UD_HTML, 'w', encoding='utf-8') as f:
        f.write(html_tekst)
    subprocess.run(['node', os.path.join(ROD, 'claude', 'html_til_pdf.mjs'),
                    UD_HTML, maal], check=True, cwd=ROD)
os.remove(UD_HTML)
print(f'{len(NAVNE)} unger · {BORDE} borde · {STOERRELSER} pladser')
for a, b in SAMMEN:
    print(f'sammen:  {a} + {b}')
for a, b in ADSKILT:
    bord_a = next(i for i, bo in enumerate(BORD, 1) if a in bo)
    bord_b = next(i for i, bo in enumerate(BORD, 1) if b in bo)
    print(f'adskilt: {a} (bord {bord_a}) og {b} (bord {bord_b})')
