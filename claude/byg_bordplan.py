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

# (kolonner af dobbeltborde, raekker) — 3 x 4 giver 12 borde og 24 pladser
OPSTILLING = (3, 4)

# Unger der skal sidde ved siden af hinanden, altsaa ved samme dobbeltbord.
SAMMEN = [('Emilie', 'Anna')]

FROE = 20261006          # fast, saa den samme plan kan bygges igen


def unger():
    with open(LISTE, encoding='utf-8') as f:
        navne = [l.strip() for l in f
                 if l.strip() and not l.lstrip().startswith('#')]
    assert len(navne) == len(set(navne)), 'to unger har samme navn i listen'
    return navne


NAVNE = unger()
KOL, RAEK = OPSTILLING
BORDE = KOL * RAEK
PLADSER = BORDE * 2
assert PLADSER >= len(NAVNE), (
    f'{len(NAVNE)} unger kan ikke sidde paa {PLADSER} pladser — ret OPSTILLING')

for a, b in SAMMEN:
    for n in (a, b):
        assert n in NAVNE, f'{n} staar ikke i klasselisten'


def plads():
    """Fordeler ungerne paa dobbeltborde. Bindingerne laegges foerst."""
    r = random.Random(FROE)
    bundet = [list(par) for par in SAMMEN]
    bundne = {n for par in SAMMEN for n in par}
    resten = [n for n in NAVNE if n not in bundne]
    r.shuffle(resten)
    borde = list(bundet)
    while resten:
        borde.append([resten.pop() for _ in range(min(2, len(resten)))])
    while len(borde) < BORDE:
        borde.append([])
    r.shuffle(borde)
    return borde


BORD = plads()
assert len(BORD) == BORDE
assert sorted(n for b in BORD for n in b) == sorted(NAVNE), 'en unge er blevet væk'
for a, b in SAMMEN:
    assert any(a in bo and b in bo for bo in BORD), f'{a} sidder ikke ved siden af {b}'
LEDIGE = PLADSER - len(NAVNE)


# ---------------------------------------------------------------------------
# Tegningen. Alle maal i mm, og alle koordinater beregnes.
# ---------------------------------------------------------------------------
SIDE_B, SIDE_H = 297, 210          # A4 paa tvaers
MARGEN = 14
TAVLE_H = 9
TOP = MARGEN + TAVLE_H + 13        # foerste bordraekke begynder her
BUND = SIDE_H - MARGEN - 20        # plads til forklaringen nederst
GANG = 12                          # mellemrum mellem kolonnerne
BORD_B = (SIDE_B - 2 * MARGEN - (KOL - 1) * GANG) / KOL
BORD_H = 19
assert BORD_B > 60, f'bordene bliver {BORD_B:.0f} mm brede — for smalle'
LUFT = (BUND - TOP - RAEK * BORD_H) / max(RAEK - 1, 1)
assert LUFT >= 6, f'kun {LUFT:.1f} mm mellem rækkerne — ret OPSTILLING'

INK, BLA, MUT, LIN, GRO = '#1a2233', '#1f6fd6', '#586074', '#c9d2e0', '#1a8f5e'


def tegn():
    s = [f'<svg viewBox="0 0 {SIDE_B} {SIDE_H}" width="{SIDE_B}mm" '
         f'height="{SIDE_H}mm" xmlns="http://www.w3.org/2000/svg" '
         f'font-family="Helvetica, Arial, sans-serif">']
    # tavlen
    s.append(f'<rect x="{MARGEN}" y="{MARGEN}" width="{SIDE_B - 2 * MARGEN}" '
             f'height="{TAVLE_H}" rx="2" fill="{INK}"/>')
    s.append(f'<text x="{SIDE_B / 2}" y="{MARGEN + TAVLE_H - 2.6}" '
             f'text-anchor="middle" fill="#fff" font-size="5" '
             f'letter-spacing="1.6">TAVLE</text>')

    for i, navne in enumerate(BORD):
        r, k = divmod(i, KOL)
        x = MARGEN + k * (BORD_B + GANG)
        y = TOP + r * (BORD_H + LUFT)
        bundet = any(set(p) <= set(navne) for p in SAMMEN)
        kant = GRO if bundet else LIN
        s.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{BORD_B:.2f}" '
                 f'height="{BORD_H}" rx="2.5" fill="#fff" stroke="{kant}" '
                 f'stroke-width="{0.9 if bundet else 0.4}"/>')
        s.append(f'<line x1="{x + BORD_B / 2:.2f}" y1="{y + 2.5:.2f}" '
                 f'x2="{x + BORD_B / 2:.2f}" y2="{y + BORD_H - 2.5:.2f}" '
                 f'stroke="{LIN}" stroke-width="0.3"/>')
        s.append(f'<text x="{x + 2.2:.2f}" y="{y + 4.4:.2f}" fill="{MUT}" '
                 f'font-size="3">{i + 1}</text>')
        for j in range(2):
            cx = x + BORD_B / 4 + j * BORD_B / 2
            cy = y + BORD_H / 2 + 2.4
            if j < len(navne):
                s.append(f'<text x="{cx:.2f}" y="{cy:.2f}" text-anchor="middle" '
                         f'fill="{INK}" font-size="7" font-weight="bold">'
                         f'{navne[j]}</text>')
            else:
                s.append(f'<text x="{cx:.2f}" y="{cy:.2f}" text-anchor="middle" '
                         f'fill="{LIN}" font-size="5.5" font-style="italic">'
                         f'ledig</text>')

    # forklaringen nederst
    fy = SIDE_H - MARGEN - 8
    s.append(f'<rect x="{MARGEN}" y="{fy - 4.6:.2f}" width="4.6" height="4.6" '
             f'rx="1" fill="#fff" stroke="{GRO}" stroke-width="0.9"/>')
    bindinger = ', '.join(f'{a} ved siden af {b}' for a, b in SAMMEN)
    s.append(f'<text x="{MARGEN + 7:.2f}" y="{fy:.2f}" fill="{MUT}" '
             f'font-size="4.4">Grøn kant: {bindinger}</text>')
    s.append(f'<text x="{SIDE_B - MARGEN:.2f}" y="{fy:.2f}" text-anchor="end" '
             f'fill="{MUT}" font-size="4.4">Bordplan · 9. klasse · {DATO} · '
             f'{len(NAVNE)} unger på {BORDE} dobbeltborde</text>')
    s.append('</svg>')
    return ''.join(s)


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
.kol{{column-count:3;column-gap:10mm}}
@page{{size:A4 landscape;margin:0}}
@media print{{.liste{{margin:0}}}}
</style></head><body>
{tegn()}
<div class="liste"><h1>Bordplan · 9. klasse</h1>
<p>{DATO} · {len(NAVNE)} unger · {BORDE} dobbeltborde · {LEDIGE} ledig plads.
Bordene er nummereret fra venstre mod højre, række for række, med tavlen
foran.</p>
<div class="kol"><table><tbody>{rk}</tbody></table></div></div>
</body></html>'''

os.makedirs(os.path.dirname(UD_HTML), exist_ok=True)
with open(UD_HTML, 'w', encoding='utf-8') as f:
    f.write(HTML)
subprocess.run(['node', os.path.join(ROD, 'claude', 'html_til_pdf.mjs'),
                UD_HTML, UD_PDF], check=True, cwd=ROD)
os.remove(UD_HTML)
print(f'{len(NAVNE)} unger · {BORDE} borde · {LEDIGE} ledig plads')
for a, b in SAMMEN:
    print(f'binding holdt: {a} + {b}')
