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

# Antal gruppeborde i lokalet, og hvordan de staar: foerste tal er borde i
# den forreste raekke, andet tal i den bageste. 3 + 2 giver fem borde.
BORDE = 5
RAEKKER = (3, 2)
assert sum(RAEKKER) == BORDE, 'raekkerne skal give det samlede antal borde'

# Bindingerne staar i spoergeskema/bindinger.json. Den er i git, saa de ikke
# gaar tabt mellem sessioner - det var netop det, der skete sidst, hvor hvem
# der var tvillinger laa i en samtale og ikke i repoet. Mappen er udelukket i
# .vercelignore, saa filen ikke kommer paa sitet. Den ser saadan ud:
#
#   {"sammen":  [["Emilie", "Anna"]],
#    "adskilt": [["Milius", "William"], ["Johan", "Silke"]]}
#
# sammen  = skal sidde ved siden af hinanden ved samme bord
# adskilt = maa ikke sidde ved samme bord (ogsaa tvillinger)
BINDINGER = os.path.join(ROD, 'spoergeskema', 'bindinger.json')


def bindinger():
    if not os.path.exists(BINDINGER):
        print(f'BEMÆRK: {BINDINGER} findes ikke — bygger uden bindinger')
        return [], []
    import json
    with open(BINDINGER, encoding='utf-8') as f:
        d = json.load(f)
    return ([tuple(p) for p in d.get('sammen', [])],
            [tuple(p) for p in d.get('adskilt', [])])


SAMMEN, ADSKILT = bindinger()

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


STOERRELSER = stoerrelser(len(NAVNE), BORDE)
assert max(STOERRELSER) <= 6, (
    f'{max(STOERRELSER)} unger ved ét bord er for mange — der skal flere borde til')

for par in SAMMEN + ADSKILT:
    for n in par:
        assert n in NAVNE, f'{n} staar ikke i klasselisten'
for a, b in ADSKILT:
    assert not any({a, b} <= set(p) for p in SAMMEN), \
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


def _holder(borde):
    for a, b in ADSKILT:
        if any(a in bo and b in bo for bo in borde):
            return False
    for a, b in SAMMEN:
        if not any(a in bo and b in bo and abs(bo.index(a) - bo.index(b)) == 1
                   for bo in borde):
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


BORD = plads()
assert len(BORD) == BORDE
assert [len(b) for b in BORD] == STOERRELSER
assert sorted(n for b in BORD for n in b) == sorted(NAVNE), 'en unge er blevet væk'
assert _holder(BORD), 'bindingerne holder ikke'


# ---------------------------------------------------------------------------
# Tegningen. Alle maal i mm, og alle koordinater beregnes.
# ---------------------------------------------------------------------------
SIDE_B, SIDE_H = 297, 210          # A4 paa tvaers
MARGEN = 14
TAVLE_H = 9
TOP = MARGEN + TAVLE_H + 15
BUND = SIDE_H - MARGEN - 16        # plads til forklaringen nederst
GANG = 16                          # mellemrum mellem borde i samme raekke
BORD_B = (SIDE_B - 2 * MARGEN - (max(RAEKKER) - 1) * GANG) / max(RAEKKER)
PLADS_H = 9                        # hoejden paa et navneskilt
BORD_H = 17                        # selve bordpladen
BLOK_H = 2 * PLADS_H + BORD_H + 4  # skilt + bord + skilt
# Luften mellem raekkerne fylder resten af pladsen, men kappes ved 26 mm:
# ellers staar de to raekker i hver sin ende af arket med et hul imellem.
_rest = BUND - TOP - len(RAEKKER) * BLOK_H
LUFT = min(_rest / max(len(RAEKKER) - 1, 1), 26)
# det, der bliver tilovers, laegges som luft foroven, saa blokken staar midt paa
TOP += (_rest - LUFT * (len(RAEKKER) - 1)) / 2
assert BORD_B > 60, f'bordene bliver {BORD_B:.0f} mm brede — for smalle'
assert LUFT >= 8, f'kun {LUFT:.1f} mm mellem rækkerne — ret RAEKKER'

INK, BLA, MUT, LIN, GRO = '#1a2233', '#1f6fd6', '#586074', '#c9d2e0', '#1a8f5e'
TRAE = '#f4f6fb'


def sider(navne):
    """Deler pladserne i en oeverste og en nederste side af bordet."""
    o = (len(navne) + 1) // 2
    return navne[:o], navne[o:]


def skilt(s, x, y, b, navn, bundet):
    kant = GRO if bundet else LIN
    s.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{b:.2f}" height="{PLADS_H}" '
             f'rx="2" fill="#fff" stroke="{kant}" '
             f'stroke-width="{0.9 if bundet else 0.4}"/>')
    # skriftstoerrelsen regnes ud af pladsen: fed Helvetica fylder ca. 0,60 em
    # pr. tegn, og der skal vaere 3 mm luft i alt. Et langt navn ved et smalt
    # bord skal krympe, ikke loebe ud over kanten.
    st = min(6.2, (b - 3) / (len(navn) * 0.60))
    assert st >= 3.6, f'{navn} kan ikke staa paa en plads paa {b:.1f} mm'
    s.append(f'<text x="{x + b / 2:.2f}" y="{y + PLADS_H / 2 + st * 0.35:.2f}" '
             f'text-anchor="middle" fill="{INK}" font-size="{st}" '
             f'font-weight="bold">{navn}</text>')


def tegn():
    s = [f'<svg viewBox="0 0 {SIDE_B} {SIDE_H}" width="{SIDE_B}mm" '
         f'height="{SIDE_H}mm" xmlns="http://www.w3.org/2000/svg" '
         f'font-family="Helvetica, Arial, sans-serif">']
    s.append(f'<rect x="{MARGEN}" y="{MARGEN}" width="{SIDE_B - 2 * MARGEN}" '
             f'height="{TAVLE_H}" rx="2" fill="{INK}"/>')
    s.append(f'<text x="{SIDE_B / 2}" y="{MARGEN + TAVLE_H - 2.6}" '
             f'text-anchor="middle" fill="#fff" font-size="5" '
             f'letter-spacing="1.6">TAVLE</text>')

    bundne_par = [set(p) for p in SAMMEN]
    nr = 0
    for r, antal in enumerate(RAEKKER):
        bredde = antal * BORD_B + (antal - 1) * GANG
        x0 = (SIDE_B - bredde) / 2          # raekken centreres
        y0 = TOP + r * (BLOK_H + LUFT)
        for k in range(antal):
            navne = BORD[nr]
            x = x0 + k * (BORD_B + GANG)
            oeverst, nederst = sider(navne)
            # selve bordpladen
            by = y0 + PLADS_H + 2
            s.append(f'<rect x="{x:.2f}" y="{by:.2f}" width="{BORD_B:.2f}" '
                     f'height="{BORD_H}" rx="3" fill="{TRAE}" stroke="{LIN}" '
                     f'stroke-width="0.5"/>')
            s.append(f'<text x="{x + BORD_B / 2:.2f}" y="{by + BORD_H / 2 + 2.6:.2f}" '
                     f'text-anchor="middle" fill="{MUT}" font-size="7" '
                     f'letter-spacing="0.6">BORD {nr + 1}</text>')
            for side, navne_her, sy in ((0, oeverst, y0),
                                        (1, nederst, by + BORD_H + 2)):
                if not navne_her:
                    continue
                sb = (BORD_B - (len(navne_her) - 1) * 2) / len(navne_her)
                for j, n in enumerate(navne_her):
                    nabo = navne[navne.index(n) - 1] if navne.index(n) else None
                    bundet = any({n} & par and len(par & set(navne_her)) == 2
                                 for par in bundne_par)
                    skilt(s, x + j * (sb + 2), sy, sb, n, bundet)
            nr += 1

    fy = SIDE_H - MARGEN - 4
    s.append(f'<rect x="{MARGEN}" y="{fy - 4.6:.2f}" width="4.6" height="4.6" '
             f'rx="1" fill="#fff" stroke="{GRO}" stroke-width="0.9"/>')
    bindinger = ', '.join(f'{a} ved siden af {b}' for a, b in SAMMEN)
    s.append(f'<text x="{MARGEN + 7:.2f}" y="{fy:.2f}" fill="{MUT}" '
             f'font-size="4.4">Grøn kant: {bindinger}</text>')
    s.append(f'<text x="{SIDE_B - MARGEN:.2f}" y="{fy:.2f}" text-anchor="end" '
             f'fill="{MUT}" font-size="4.4">Bordplan · 9. klasse · {DATO} · '
             f'{len(NAVNE)} unger på {BORDE} borde '
             f'({"+".join(str(n) for n in STOERRELSER)})</text>')
    s.append('</svg>')
    return ''.join(s)


# ---------------------------------------------------------------------------
# Bordkortene: ét ark pr. bord, der laegges paa bordet.
#
# Navnene paa den side, der vender vaek fra tavlen, staar paa hovedet. Det er
# med vilje: arket ligger fladt paa bordet, og saa kan hver unge laese sit eget
# navn rigtigt vej fra sin egen plads. Pilen viser, hvilken kant der skal vende
# mod tavlen, saa arket ikke bliver lagt forkert.
# ---------------------------------------------------------------------------
K_B, K_H = 297, 210                 # A4 paa tvaers
K_MARGEN = 16


def bordkort(nr, navne):
    oeverst, nederst = sider(navne)
    s = [f'<svg viewBox="0 0 {K_B} {K_H}" width="{K_B}mm" height="{K_H}mm" '
         f'xmlns="http://www.w3.org/2000/svg" '
         f'font-family="Helvetica, Arial, sans-serif">']

    # pilen mod tavlen
    s.append(f'<text x="{K_B / 2}" y="{K_MARGEN + 4}" text-anchor="middle" '
             f'fill="{MUT}" font-size="5" letter-spacing="1.8">'
             f'&#9650;  MOD TAVLEN  &#9650;</text>')

    raekker = [(oeverst, False), (nederst, True)]
    bh = 46                          # hoejden paa en navnerraekke
    BAAND = 26                       # midterbaandet, hvor bordnummeret staar
    midte = K_H / 2
    # baandet skal kunne rumme bordnummeret uden at skaere ind i navneboksene
    assert BAAND >= 20, 'bordnummeret staar i vejen for navnene'
    assert 2 * bh + BAAND + 2 * K_MARGEN <= K_H, 'arket er ikke hoejt nok'
    for navne_her, paa_hovedet in raekker:
        if not navne_her:
            continue
        # den oeverste raekke ligger over midten, den nederste under
        y = midte - BAAND / 2 - bh if not paa_hovedet else midte + BAAND / 2
        bred = (K_B - 2 * K_MARGEN - (len(navne_her) - 1) * 6) / len(navne_her)
        for j, n in enumerate(navne_her):
            x = K_MARGEN + j * (bred + 6)
            cx, cy = x + bred / 2, y + bh / 2
            # skriften regnes af pladsen, som paa oversigten
            st = min(26, (bred - 8) / (len(n) * 0.60))
            assert st >= 10, f'{n} kan ikke staa paa {bred:.0f} mm'
            drej = f' transform="rotate(180 {cx:.2f} {cy:.2f})"' if paa_hovedet else ''
            s.append(f'<g{drej}>')
            s.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{bred:.2f}" '
                     f'height="{bh}" rx="4" fill="#fff" stroke="{LIN}" '
                     f'stroke-width="0.6"/>')
            s.append(f'<text x="{cx:.2f}" y="{cy + st * 0.35:.2f}" '
                     f'text-anchor="middle" fill="{INK}" font-size="{st:.1f}" '
                     f'font-weight="bold">{n}</text>')
            s.append('</g>')

    # bordnummeret ligger i midterbaandet, saa det kan laeses fra begge sider
    s.append(f'<text x="{K_B / 2}" y="{midte + 5.2}" text-anchor="middle" '
             f'fill="{MUT}" font-size="14" letter-spacing="5" '
             f'font-weight="bold">BORD {nr}</text>')
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
.kol{{column-count:3;column-gap:10mm}}
@page{{size:A4 landscape;margin:0}}
@media print{{.liste{{margin:0}}}}
</style></head><body>
{tegn()}
<div class="liste"><h1>Bordplan · 9. klasse</h1>
<p>{DATO} · {len(NAVNE)} unger · {BORDE} gruppeborde med
{', '.join(str(n) for n in STOERRELSER)} pladser. Bordene er nummereret fra
venstre mod højre, række for række, med tavlen foran.</p>
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
