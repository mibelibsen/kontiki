#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bygger KontikAir: tre papirflyvere med skabeloner og foldevejledning.

    python3 claude/byg_kontikair.py <scratch-mappe>

Skriver kontikair.html samt tre A4-skabeloner og en foldevejledning til print.

Foldene regnes, de tegnes ikke på øjemål. Hver fold er én af tre slags:

    kant_til_linje   fold en kant hen på en anden linje (hængslet er vinklens
                     halveringslinje)
    punkt_til_punkt  fold et hjørne hen på et bestemt punkt (hængslet er
                     midtnormalen)
    parallel         fold langs en linje parallelt med kroppen (vingerne)

Papiret føres gennem folderne som en polygon: folden klipper polygonen i to,
klappen spejles i foldelinjen, og resten er den nye silhuet. Scriptet tjekker
undervejs, at en klap, der skal foldes indad, rent faktisk lander inde på
papiret — ellers passer folden ikke.

Alle folder går **bagud**. Derfor bliver den trykte side ved med at vende
opad, mens man folder, og ender udvendigt på den færdige flyver. Det er også
derfor, hver eneste foldelinje kan trykkes på skabelonen: ingen af dem bliver
dækket af en klap undervejs.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figurer as FG                                         # noqa: E402

SCRATCH = sys.argv[1] if len(sys.argv) > 1 else '.'
ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROD)

A4 = (210.0, 297.0)                      # stående
A4L = (297.0, 210.0)                     # liggende
EPS = 1e-9

# ====================================================== 1 · lidt geometri


def _enhed(v):
    n = math.hypot(*v)
    return (v[0] / n, v[1] / n)


def spejl(p, a, d):
    """Spejler punktet p i linjen gennem a med retningen d."""
    v = (p[0] - a[0], p[1] - a[1])
    t = v[0] * d[0] + v[1] * d[1]
    par = (t * d[0], t * d[1])
    per = (v[0] - par[0], v[1] - par[1])
    return (a[0] + par[0] - per[0], a[1] + par[1] - per[1])


def side(p, a, d):
    """Fortegnet afstand fra linjen (a, d) til p — positiv til venstre."""
    return d[0] * (p[1] - a[1]) - d[1] * (p[0] - a[0])


def klip(poly, a, d, behold_positiv):
    """Sutherland-Hodgman: den del af polygonen, der ligger på den ene side."""
    ud = []
    for i, p in enumerate(poly):
        q = poly[(i + 1) % len(poly)]
        sp, sq = side(p, a, d), side(q, a, d)
        if not behold_positiv:
            sp, sq = -sp, -sq
        if sp >= -1e-7:
            ud.append(p)
        if (sp > 1e-7 and sq < -1e-7) or (sp < -1e-7 and sq > 1e-7):
            t = sp / (sp - sq)
            ud.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return _ryd(ud)


def _ryd(poly):
    ud = []
    for p in poly:
        if not ud or math.hypot(p[0] - ud[-1][0], p[1] - ud[-1][1]) > 1e-6:
            ud.append(p)
    if len(ud) > 1 and math.hypot(ud[0][0] - ud[-1][0], ud[0][1] - ud[-1][1]) < 1e-6:
        ud.pop()
    return ud


def i_polygon(p, poly, slup=0.5):
    """Ligger p inde i polygonen? slup tillader et par tiendedele millimeter."""
    n = len(poly)
    inde = False
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > p[1]) != (y2 > p[1]):
            x = x1 + (p[1] - y1) / (y2 - y1) * (x2 - x1)
            if x > p[0]:
                inde = not inde
    if inde:
        return True
    return min(_afstand_til_kant(p, poly[i], poly[(i + 1) % n])
               for i in range(n)) <= slup


def _afstand_til_kant(p, a, b):
    vx, vy = b[0] - a[0], b[1] - a[1]
    n2 = vx * vx + vy * vy
    t = 0 if n2 < EPS else max(0, min(1, ((p[0] - a[0]) * vx + (p[1] - a[1]) * vy) / n2))
    return math.hypot(p[0] - (a[0] + t * vx), p[1] - (a[1] + t * vy))


def snit(poly, a, d):
    """Foldelinjens synlige stykke: hvor den skærer polygonens kant."""
    punkter = []
    for i, p in enumerate(poly):
        q = poly[(i + 1) % len(poly)]
        sp, sq = side(p, a, d), side(q, a, d)
        if abs(sp) < 1e-7:
            punkter.append(p)
        elif (sp > 0) != (sq > 0):
            t = sp / (sp - sq)
            punkter.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    punkter = _ryd(sorted(punkter, key=lambda p: p[0] * d[0] + p[1] * d[1]))
    assert len(punkter) >= 2, 'foldelinjen rammer ikke papiret'
    return punkter[0], punkter[-1]


# ====================================================== 2 · de tre foldetyper


def kant_til_linje(hjoerne, ud_ad_kanten, ud_ad_maalet):
    """Fold kanten hen på målet. Hængslet er vinklens halveringslinje."""
    a = _enhed((ud_ad_kanten[0] - hjoerne[0], ud_ad_kanten[1] - hjoerne[1]))
    b = _enhed((ud_ad_maalet[0] - hjoerne[0], ud_ad_maalet[1] - hjoerne[1]))
    return hjoerne, _enhed((a[0] + b[0], a[1] + b[1]))


def punkt_til_punkt(fra, til):
    """Fold fra-punktet hen på til-punktet. Hængslet er midtnormalen."""
    midt = ((fra[0] + til[0]) / 2, (fra[1] + til[1]) / 2)
    d = _enhed((til[0] - fra[0], til[1] - fra[1]))
    return midt, (-d[1], d[0])


def lodret(x):
    return (x, 0.0), (0.0, 1.0)


# ====================================================== 3 · foldemotoren

class Trin:
    """Ét trin i vejledningen: papiret før folden, folderne, og papiret efter."""

    def __init__(self, nr, tekst, foer, folder, efter, klapper, slags):
        self.nr, self.tekst = nr, tekst
        self.foer, self.efter = foer, efter
        self.folder = folder            # [(punkt_a, punkt_b)] i fladt koordinat
        self.klapper = klapper          # [(klap-polygon, spejlet polygon)]
        self.slags = slags


def kør(ark, opskrift):
    """Fører papiret gennem folderne og bygger listen af trin."""
    W, H = ark
    poly = [(0.0, 0.0), (W, 0.0), (W, H), (0.0, H)]
    trin, nr = [], 0
    for tekst, slags, linjer, bliv in opskrift:
        nr += 1
        foer = list(poly)
        segmenter, klapper = [], []
        for a, d in linjer:
            segmenter.append(snit(poly, a, d))
            if slags == 'ref':
                continue
            # 'bliv' er et punkt på den del af papiret, der ikke flytter sig
            positiv = side(bliv, a, d) > 0
            klap = klip(poly, a, d, not positiv)
            ny = klip(poly, a, d, positiv)
            if slags == 'indad':
                spejlet = [spejl(p, a, d) for p in klap]
                for p in spejlet:
                    assert i_polygon(p, ny), (
                        f'trin {nr} ({tekst}): klappen lander uden for papiret '
                        f'i {p[0]:.1f}, {p[1]:.1f}')
                klapper.append((klap, spejlet))
                poly = ny
            elif slags == 'halv':
                klapper.append((klap, [spejl(p, a, d) for p in klap]))
                poly = ny
            else:                                  # vingefold: papiret knækker
                klapper.append((klap, None))       # ud af planet
        trin.append(Trin(nr, tekst, foer, segmenter, list(poly), klapper, slags))
    return trin


# ====================================================== 4 · de tre flyvere

def pilen():
    W, H = A4
    spids, ned = (W / 2, H), (W / 2, 0.0)
    hj2 = W / 2                                   # hvor trin 2 rammer sidekanten
    return A4, [
        ('Fold arket på midten på langs, og fold det ud igen. Midterfolden er '
         'den streg, alt andet måles fra.', 'ref', [lodret(W / 2)], None),
        ('Fold de to øverste hjørner bagud ind til midterstregen, så topkanten '
         'lægger sig langs midten.', 'indad',
         [kant_til_linje(spids, (0.0, H), ned),
          kant_til_linje(spids, (W, H), ned)], (W / 2, H - 1)),
        ('Fold de to nye skrå kanter bagud ind til midten igen. Nu er næsen '
         'spids og tung.', 'indad',
         [kant_til_linje(spids, (0.0, H - hj2), ned),
          kant_til_linje(spids, (W, H - hj2), ned)], (W / 2, H - 1)),
        ('Fold flyveren sammen bagud om midterfolden, så den trykte side '
         'bliver udvendig.', 'halv', [lodret(W / 2)], (W, H / 2)),
        ('Fold en vinge ned i hver side. Kanten skal følge kroppen hele vejen '
         'ned.', 'vinge', [lodret(W / 2 + 25)], (W / 2 + 1, H / 2)),
    ]


def svaeveren():
    W, H = A4
    spids, ned = (W / 2, H), (W / 2, 0.0)
    return A4, [
        ('Fold arket på midten på langs, og fold det ud igen.', 'ref',
         [lodret(W / 2)], None),
        ('Fold de to øverste hjørner bagud ind til midterstregen.', 'indad',
         [kant_til_linje(spids, (0.0, H), ned),
          kant_til_linje(spids, (W, H), ned)], (W / 2, H - 1)),
        ('Fold næsespidsen bagud og ned, så den lige rammer dér, hvor de to '
         'klapper slutter. Næsen bliver stump og tung — det er den, der gør '
         'Svæveren rolig.', 'indad',
         [punkt_til_punkt(spids, (W / 2, H - W / 2))], (W / 2, 1.0)),
        ('Fold flyveren sammen bagud om midterfolden.', 'halv',
         [lodret(W / 2)], (W, H / 2)),
        ('Fold en bred vinge ned i hver side. Brede vinger bærer længere.',
         'vinge', [lodret(W / 2 + 40)], (W / 2 + 1, H / 2)),
    ]


def bumleren():
    W, H = A4L
    spids, ned = (W / 2, H), (W / 2, 0.0)
    return A4L, [
        ('Læg arket på tværs. Fold det på midten, og fold det ud igen.',
         'ref', [lodret(W / 2)], None),
        ('Fold de to øverste hjørner bagud ind til midterstregen.', 'indad',
         [kant_til_linje(spids, (0.0, H), ned),
          kant_til_linje(spids, (W, H), ned)], (W / 2, H - 1)),
        ('Fold næsen bagud og ned. Den korte krop og den tunge næse er dét, '
         'der får Bumleren til at vende rundt i luften.', 'indad',
         [punkt_til_punkt(spids, (W / 2, H - 110))], (W / 2, 1.0)),
        ('Fold flyveren sammen bagud om midterfolden.', 'halv',
         [lodret(W / 2)], (W, H / 2)),
        ('Fold en vinge ned i hver side — tæt på kroppen, så vingen bliver '
         'meget bred.', 'vinge', [lodret(W / 2 + 45)], (W / 2 + 1, H / 2)),
        ('Fold yderste 20 mm af hver vinge op som et lille sidestyr.', 'vinge',
         [lodret(W - 20)], (W / 2 + 1, H / 2)),
    ]


FLYVERE = [
    dict(nøgle='pilen', navn='Pilen', bygger=pilen, farve=FG.BLA,
         kort='Smal, spids og tung i næsen. Den, der flyver længst, når du '
              'kaster hårdt og lige ud.',
         kast='Hold om kroppen lige bag næsen. Kast hårdt og vandret, lidt '
              'over hovedhøjde.',
         maal='længde'),
    dict(nøgle='svaeveren', navn='Svæveren', bygger=svaeveren, farve=FG.GRO,
         kort='Stump næse og brede vinger. Flyver langsomt og bliver længst '
              'tid i luften.',
         kast='Hold let om kroppen. Skub den af sted roligt og en anelse '
              'opad — kast aldrig hårdt, så stejler den.',
         maal='tid'),
    dict(nøgle='bumleren', navn='Bumleren', bygger=bumleren, farve=FG.ORA,
         kort='Foldet af et ark på tværs: kort krop, meget brede vinger. Den '
              'laver loops, hvis du knækker bagkanten en smule op.',
         kast='Kast opad i en vinkel på cirka 45 grader. Bøj bagkanten af '
              'vingerne 5 mm op, hvis den dykker.',
         maal='loops'),
]

for f in FLYVERE:
    f['ark'], f['opskrift'] = f['bygger']()
    f['trin'] = kør(f['ark'], f['opskrift'])


# ====================================================== 5 · tegninger

PAPIR, PAPIR2, KANT = '#fbf7ef', '#f0e7d6', '#b9ae9a'


def _midte(poly):
    return (sum(p[0] for p in poly) / len(poly), sum(p[1] for p in poly) / len(poly))


def trin_figur(f, t, tidligere):
    """Ét trin: papiret som det ser ud før folden, med folden markeret."""
    W, H = f['ark']
    luft = 16
    r = FG.Rids(-luft, W + luft, -luft, H + luft, skala=0.46,
                alt=f'Trin {t.nr} i foldningen af {f["navn"]}.',
                margen=(4, 4, 4, 4))
    r.poly(t.foer, PAPIR, KANT)
    for a, b in tidligere:                       # folder, der allerede er lavet
        r.linje(a[0], a[1], b[0], b[1], KANT, 1, True)
    for klap, spejlet in t.klapper:              # klappen og hvor den lander
        if klap:
            r.poly(klap, PAPIR2, KANT, opacitet=0.9)
        if spejlet:
            r.poly(spejlet, f['farve'], KANT, opacitet=0.13, stiplet=True)
    for a, b in t.folder:
        r.linje(a[0], a[1], b[0], b[1], f['farve'], 2.2,
                stiplet=(t.slags == 'ref'))
    for i, (klap, spejlet) in enumerate(t.klapper):   # pilen, der viser vejen
        if not klap:
            continue
        fra = _midte(klap)
        if spejlet:
            til = _midte(spejlet)
        else:                        # vingefolden knækker ud af papirets plan,
            a, b = t.folder[i]       # så pilen peger ind mod foldelinjen
            d = _enhed((b[0] - a[0], b[1] - a[1]))
            n = (-d[1], d[0])
            k = side(fra, a, d) * 0.75
            til = (fra[0] - n[0] * k, fra[1] - n[1] * k)
        r.linje(fra[0], fra[1], til[0], til[1], f['farve'], 1.6)
        r._pil(r.px(til[0]), r.py(til[1]),
               r.px(til[0]) - r.px(fra[0]), r.py(til[1]) - r.py(fra[1]))
    r.maerke(-luft + 8, H + luft - 8, str(t.nr), f['farve'])
    return r.svg()


def faerdig_figur(f):
    """Den færdige flyver set forfra: krop, vinger og vingernes hældning."""
    W, H = f['ark']
    vinge = [t for t in f['trin'] if t.slags == 'vinge'][0]
    krop = vinge.folder[0][0][0] - W / 2                 # kropdybde i mm
    spaend = W / 2 - krop                                # halv vingebredde
    r = FG.Rids(-spaend - 14, spaend + 14, -krop - 10, 26, skala=0.9,
                alt=f'{f["navn"]} set forfra.', margen=(6, 6, 6, 6))
    for side_ in (1, -1):
        r.poly([(0, 0), (side_ * spaend, 12), (side_ * spaend, 15), (0, 3)],
               PAPIR, KANT)
    r.poly([(-1.6, 0), (1.6, 0), (1.6, -krop), (-1.6, -krop)], PAPIR2, KANT)
    r.tekst(0, -krop - 6, f'krop {krop:.0f} mm', FG.MUT, 9.5)
    r.tekst(0, 21, f'vingefang {2 * spaend:.0f} mm', FG.MUT, 9.5)
    return r.svg()


# ---------------------------------------------------------- A4-skabelonen

def skabelon(f):
    """Skabelonen i millimeter, så den kan printes i 1:1 på A4."""
    W, H = f['ark']
    farve = f['farve']
    d = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" '
         f'height="{H}mm" viewBox="0 0 {W} {H}" '
         f'font-family="Helvetica, Arial, sans-serif">',
         f'<rect x="0" y="0" width="{W}" height="{H}" fill="#fff"/>']

    def mm(x, y):                       # svg har y nedad, papiret regnes opad
        return x, H - y

    linjer = []                         # (nr, a, b)
    for t in f['trin']:
        for a, b in t.folder:
            linjer.append((t.nr, a, b))
            if t.slags == 'vinge':      # vingefolden findes i begge sider
                linjer.append((t.nr, (W - a[0], a[1]), (W - b[0], b[1])))
    for nr, a, b in linjer:
        x1, y1 = mm(*a)
        x2, y2 = mm(*b)
        d.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" '
                 f'y2="{y2:.2f}" stroke="{farve}" stroke-width="0.4" '
                 f'stroke-dasharray="4 2.2" opacity="0.85"/>')
        # nummeret sættes et stykke inde på linjen, så det ikke havner i
        # papirets kant — og forskudt efter trinnummer, så to folder på den
        # samme streg (midterfolden er både nr. 1 og nr. 4) ikke dækker
        # hinanden
        t_ = 0.18 + 0.13 * ((nr - 1) % 4)
        nx, ny = x1 + (x2 - x1) * t_, y1 + (y2 - y1) * t_
        d.append(f'<circle cx="{nx:.2f}" cy="{ny:.2f}" r="3.1" fill="#fff" '
                 f'stroke="{farve}" stroke-width="0.4"/>')
        d.append(f'<text x="{nx:.2f}" y="{ny + 1.5:.2f}" text-anchor="middle" '
                 f'fill="{farve}" font-size="4" font-weight="700">{nr}</text>')

    # mærke og navnefelt på begge vinger, så de vender rigtigt i flyvningen
    vinge_x = [t for t in f['trin'] if t.slags == 'vinge'][0].folder[0][0][0]
    for side_ in (1, -1):
        cx = W / 2 + side_ * (vinge_x - W / 2 + (W / 2 - (vinge_x - W / 2)) / 2.6)
        x, y = mm(cx, 42)
        d.append(f'<g transform="translate({x:.2f} {y:.2f})">'
                 f'<text x="0" y="0" text-anchor="middle" fill="{farve}" '
                 f'font-size="7.5" font-weight="700" letter-spacing="1.4">'
                 f'KONTIKAIR</text>'
                 f'<text x="0" y="8" text-anchor="middle" fill="#586074" '
                 f'font-size="5">{f["navn"].upper()}</text>'
                 f'<line x1="-26" y1="19" x2="26" y2="19" stroke="#c9d2e0" '
                 f'stroke-width="0.4"/>'
                 f'<text x="-26" y="17" fill="#8e97a8" font-size="3.4">'
                 f'Navn</text></g>')

    x, y = mm(W / 2, 7)
    d.append(f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="middle" '
             f'fill="#8e97a8" font-size="3.6">Print i 100 % — ikke '
             f'«tilpas til side». Fold i nummerrækkefølge. Alle folder går '
             f'bagud, så denne side bliver udvendig.</text>')
    d.append('</svg>')
    return ''.join(d)


# ====================================================== 6 · siden og arkene
for f in FLYVERE:
    tidligere = []
    f['figurer'] = []
    for t in f['trin']:
        f['figurer'].append(trin_figur(f, t, list(tidligere)))
        tidligere += t.folder
    f['faerdig'] = faerdig_figur(f)
    f['skabelon'] = skabelon(f)
    f['pdf'] = f'materiale/kontikair-{f["nøgle"]}-a4.pdf'
    vinge = [t for t in f['trin'] if t.slags == 'vinge'][0]
    f['krop'] = vinge.folder[0][0][0] - f['ark'][0] / 2
    f['spaend'] = f['ark'][0] - 2 * f['krop']

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
.blok h3{margin:0 0 8px;font-size:1.15rem}
.blok p,.blok li{color:var(--muted);font-size:.97rem}
.blok p{margin:6px 0;max-width:74ch}
.blok ul{margin:6px 0 0;padding-left:20px}.blok li{margin:4px 0}
.fly{border:1px solid var(--line);border-radius:16px;padding:20px 24px;
margin:18px 0;background:var(--panel);box-shadow:var(--shadow)}
.fly h2{margin:0 0 4px;font-size:1.5rem}
.fly .undertitel{color:var(--muted);margin:0 0 12px;font-size:.98rem}
.flytop{display:grid;grid-template-columns:1fr 240px;gap:18px;align-items:center}
@media(max-width:700px){.flytop{grid-template-columns:1fr}}
.trin{display:grid;grid-template-columns:repeat(auto-fit,minmax(152px,1fr));
gap:12px;margin-top:14px}
.tr{border:1px solid var(--line);border-radius:12px;padding:10px;
background:var(--panel2)}
.tr svg{max-width:100%;height:auto}
.tr p{margin:8px 0 0;font-size:.88rem;color:var(--muted);line-height:1.45}
.maerke{display:inline-block;background:var(--accent);color:#fff;font-weight:700;
border-radius:999px;padding:1px 9px;font-size:.8rem;margin-right:6px}
table.t{width:100%;border-collapse:collapse;margin:12px 0;font-size:.95rem}
table.t th,table.t td{border:1px solid var(--line);padding:9px 11px;
text-align:left;vertical-align:top}
table.t th{background:var(--panel2)}
.printbtn{background:#fff;border:1px solid var(--line);border-radius:10px;
padding:10px 18px;font-weight:700;font-size:.95rem;cursor:pointer;color:var(--ink);
font-family:inherit;margin:6px 8px 0 0}
.printbtn:hover{border-color:var(--accent);color:var(--accent)}
@media print{header.top,.printbtn,.btnlink{display:none!important}
.blok,.figur,.fly,.tr{box-shadow:none;break-inside:avoid;page-break-inside:avoid}
.figur{background:none;border:none;padding:2px}
body{font-size:9.8pt}main{padding:0}@page{size:A4;margin:11mm}
h2.sec{page-break-after:avoid}}
'''


def side(titel, krop):
    return ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{titel}</title><style>' + GRUND + EKSTRA +
            '</style></head><body><header class="top"><div class="top-inner">'
            '<a class="brand" href="index.html">Mibelibsen <span>9. klasse</span></a>'
            '<nav class="tabs"><a class="" href="matematik.html">Matematik</a>'
            '<a class="" href="samfundsfag.html">Samfundsfag</a>'
            '<a class="" href="tysk.html">Tysk</a>'
            '<span class="soon">Fysik</span></nav>'
            '</div></header><main>' + krop + '</main><footer>'
            'KontikAir · Mibelibsen · 9. klasse.'
            '</footer></body></html>')


def flyver_blok(f):
    trin = ''.join(
        f'<div class="tr">{fig}<p><span class="maerke">{t.nr}</span>'
        f'{t.tekst}</p></div>'
        for fig, t in zip(f['figurer'], f['trin']))
    return f'''<section class="fly">
<h2>{f['navn']}</h2>
<p class="undertitel">{f['kort']}</p>
<div class="flytop"><div>
<p><b>Sådan kaster du:</b> {f['kast']}</p>
<p><b>Ark:</b> A4 {'på tværs' if f['ark'][0] > f['ark'][1] else 'på højkant'} ·
<b>vingefang:</b> {f['spaend']:.0f} mm · <b>krop:</b> {f['krop']:.0f} mm ·
<b>{len(f['trin'])} folder</b>.</p>
<a class="btnlink" href="{f['pdf']}">Hent skabelonen til {f['navn']} (A4)</a>
</div><div>{f['faerdig']}</div></div>
<div class="trin">{trin}</div>
</section>'''


maalefigur = FG.tomt_soejlegitter(
    [f['navn'] for f in FLYVERE], 10, 'Meter', 'Længste kast — sæt en søjle '
    'for hver flyver', trin=2)

KROP = f'''<section class="hero"><span class="pill">KontikAir</span>
<h1>Tre papirflyvere</h1>
<p>Tre skabeloner til A4 med foldelinjerne trykt på, og en vejledning til hver.
Flyverne er ikke ens for sjov: den ene er bygget til at flyve <b>langt</b>, den
anden til at blive <b>længe</b> i luften, den tredje til at <b>vende rundt</b>.
Fold alle tre, og mål selv forskellen.</p>
<button class="printbtn" onclick="window.print()">Print vejledningen</button></section>

<div class="blok"><h3>Fire regler, der gælder alle tre</h3>
<ul>
<li><b>Print i 100 %.</b> Slå «tilpas til side» fra. Er arket skaleret, passer
foldelinjerne ikke til kanterne.</li>
<li><b>Læg arket med den trykte side opad, og fold altid bagud</b> — væk fra dig
selv. Så bliver linjerne ved med at være synlige, mens du folder, og den trykte
side ender udvendigt på den færdige flyver.</li>
<li><b>Fold i nummerrækkefølge.</b> Numrene på arket er de samme som numrene i
vejledningen.</li>
<li><b>Stryg hver fold skarp</b> med en negl eller kanten af en lineal. En
uskarp fold er en skæv flyver.</li>
</ul></div>

{''.join(flyver_blok(f) for f in FLYVERE)}

<h2 class="sec">Mål, og find ud af hvem der har ret</h2>
<div class="blok"><p>Kast hver flyver <b>fem gange</b> fra det samme sted. Mål
længden hver gang, og brug <b>midtertallet</b> — medianen — ikke det længste
kast. Det længste kast er held; midtertallet er flyveren.</p>
<p>Tag tid på Svæveren i stedet for at måle længde. Den taber i meter og vinder
i sekunder, og det er hele pointen: der findes ikke én bedste flyver, kun den
bedste til dét, man måler.</p></div>
<div class="figur">{maalefigur}</div>

<h2 class="sec">Flyver den skævt?</h2>
<table class="t"><thead><tr><th>Det gør den</th><th>Prøv det her</th></tr></thead>
<tbody>
<tr><td>Stejler og falder ned igen</td><td>Kast mindre hårdt, eller bøj
bagkanten af vingerne 5 mm <b>ned</b>.</td></tr>
<tr><td>Dykker lige i gulvet</td><td>Bøj bagkanten af vingerne 5 mm
<b>op</b>.</td></tr>
<tr><td>Drejer altid til samme side</td><td>Vingerne sidder ikke ens. Ret dem
af, så de danner et fladt V set forfra.</td></tr>
<tr><td>Vender rundt om sig selv</td><td>Næsen er for let. Tjek, at
næsefolderne sidder helt inde ved midten.</td></tr>
<tr><td>Flyver kort, uanset hvad</td><td>Folderne er ikke skarpe nok. Stryg dem
igen med en lineal.</td></tr>
</tbody></table>
'''

open('kontikair.html', 'w').write(side('KontikAir · tre papirflyvere', KROP))

for f in FLYVERE:
    W, H = f['ark']
    ud = os.path.join(SCRATCH, f'skabelon-{f["nøgle"]}.html')
    open(ud, 'w').write(
        '<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
        f'<title>KontikAir {f["navn"]}</title><style>'
        f'@page{{size:{"A4 landscape" if W > H else "A4"};margin:0}}'
        'html,body{margin:0;padding:0}svg{display:block}'
        '</style></head><body>' + f['skabelon'] + '</body></html>')

print(f'skrevet:  kontikair.html')
for f in FLYVERE:
    print(f'skrevet:  {SCRATCH}/skabelon-{f["nøgle"]}.html  '
          f'({f["ark"][0]:.0f}×{f["ark"][1]:.0f} mm, {len(f["trin"])} folder, '
          f'vingefang {f["spaend"]:.0f} mm)')
