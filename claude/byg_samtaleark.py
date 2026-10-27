# -*- coding: utf-8 -*-
"""Bygger vejledning/skolehjemsamtale.pdf — skabelon til en samtale paa 30 min.

Ét ark pr. barn. Fokus er fagligt: hvor staar hun, hvad er maalet, og hvad
skal der til - i skolen, hjemme og hos barnet selv.

Arket ligger i vejledning/, som er udelukket fra deploy. Det bliver udfyldt
med vurderinger af et navngivet barn og hoerer ikke paa et offentligt site.
PDF'en er en bygget fil og er ikke i git; scriptet er kilden.

    python3 claude/byg_samtaleark.py

Alle skrivepladser er rigtige formularfelter: man kan aabne PDF'en og skrive
i den, eller printe den og skrive i haanden. Barnet udfylder selv kolonnen
"Barnets vurdering"; resten er laererens.

Feltmaalene gaettes ikke. Hvert felt faar to usynlige markoerer i hjoernerne,
PDF'en bliver bygget, og `pdftotext -bbox` siger bagefter, hvor markoererne
landede. Rektanglet er forskellen mellem dem. Layoutet er uroert - felterne
ligger oven paa de streger, der var der i forvejen, og foelger med af sig
selv, hvis noget flyttes.
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figurer as FG

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UD_HTML = os.path.join(ROD, 'vejledning', 'skolehjemsamtale.html')
UD_PDF = os.path.join(ROD, 'vejledning', 'skolehjemsamtale.pdf')

MINUTTER = 30

# Barnet faar halvdelen af baandet. De tre andre dele deler den anden
# halvdel. Det staar ingen steder paa arket - baandet er en tegning, ikke en
# instruks - men den blaa blok er lige saa bred som de tre andre tilsammen,
# og den ligger forrest. Den, der ser arket, kan se, hvem der skal tale.
#
# Tallene staar ikke paa figuren (tal=False). Et minuttal paa en farve goer
# baandet til et skema, man skal overholde; uden tal er det et forhold.
TIDSPLAN = [
    ('Barnet selv', 15),
    ('Overblik', 4),
    ('Fokusfag', 7),
    ('Aftaler', 4),
]
assert sum(m for _, m in TIDSPLAN) == MINUTTER
_barnet = TIDSPLAN[0][1]
assert _barnet * 2 == MINUTTER, 'barnet skal have praecis halvdelen'
assert sum(m for _, m in TIDSPLAN[1:]) == _barnet, 'de tre deler den anden halvdel'

FAG = ['Dansk', 'Matematik', 'Samfundsfag', 'Idræt']

# Overskriften over skemaet taeller fagene selv. Stod tallet skrevet i
# overskriften, ville den sige "otte", dagen efter listen blev lavet om.
TAL = {1: 'ét', 2: 'to', 3: 'tre', 4: 'fire', 5: 'fem', 6: 'seks',
       7: 'syv', 8: 'otte', 9: 'ni', 10: 'ti'}
assert len(FAG) in TAL, 'skriv flere talord, hvis der skal være flere fag'
OVERSKRIFT = f'Alle {TAL[len(FAG)]} fag'

OVERSIGT_KOL = ['Fag', 'Standpunkt', 'Barnets vurdering']

# Stoette i skolen, hjemme og hos barnet selv er det samme spoergsmaal stillet
# tre steder: hvad skal der til. De staar derfor i én raekke med tre kolonner -
# det goer det tydeligt, at de tre ting skal haenge sammen.
DYBDE = [
    ('Standpunkt', 'faglige områder', 2, None),
    ('Mål', 'Hvad er det næste skridt', 2, None),
    ('Hvad skal der til?', '', 4, ('I skolen', 'Hjemme', 'Barn')),
]

# Raekkehoejden i oversigten er sat, saa de faa fag fylder side 1 ud.
# 192 mm er den plads, der er tilbage under overskriften paa en A4 med
# 12 mm margen, naar hoved, felter, baand og skemaets hovedraekke er taget.
RAEKKE = f'{192 / len(FAG):.0f}mm'

AFTALER_KOL = ['Aftale', 'Hvem gør det', 'Hvornår']
AFTALER_RAEKKER = 3

# To tomme blokke. De har ingen numre: de to fag vaelges under samtalen, og
# et nummer ved siden af et fag ligner en rangordning.
FOKUS_BLOKKE = 2

# Markoererne. To bogstavkombinationer, der ikke staar i et dansk ord, saa de
# ikke kan forveksles med sidens egen tekst, naar den bliver laest ud igen.
MA, MB = 'qQa', 'qQb'

FORMULAR = []     # [{navn, nr, flerlinje}] - fyldes af felt() nedenfor


def _slug(s):
    s = (s.lower().replace('æ', 'ae').replace('ø', 'oe').replace('å', 'aa')
         .replace('/', '-'))
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def felt(navn, flerlinje=True):
    """Markoererne til ét felt. De skal staa i en kasse med position:relative,
    for det er den kasse, feltet kommer til at fylde."""
    nr = len(FORMULAR) + 1
    FORMULAR.append({'navn': navn, 'nr': nr, 'flerlinje': flerlinje})
    return (f'<span class="mA">{MA}{nr:03d}</span>'
            f'<span class="mB">{MB}{nr:03d}</span>')


def udfyld(navn):
    """Den enkeltlinjede skrivelinje med et felt oven paa."""
    return f'<span class="udfyld">{felt(navn, flerlinje=False)}</span>'


def linjer(n, navn):
    """n skrivelinjer. De tegnes én ad gangen og ikke som et gentaget
    baggrundsmoenster: et moenster bliver klippet af feltets hoejde, og saa
    staar der tre linjer ét sted og to et andet, alt efter hvor en brudt
    millimeter falder. Her er der praecis n, hver gang."""
    return ('<div class="linjer">' + felt(navn)
            + '<div class="linje"></div>' * n
            + '</div>')


def skema(kolonner, raekker, hoejde='14mm', bredder=None, praefiks=''):
    """Et tomt skema. `raekker` er enten et tal eller en liste af tekster,
    der staar i foerste kolonne. `bredder` er procenter - uden dem fordeler
    browseren kolonnerne efter overskrifternes laengde, og saa bliver
    "Fag" bred og "Standpunkt" smal uden grund."""
    if isinstance(raekker, int):
        raekker = [''] * raekker
    bredder = bredder or [100 / len(kolonner)] * len(kolonner)
    assert len(bredder) == len(kolonner), 'én bredde pr. kolonne'
    assert abs(sum(bredder) - 100) < 0.5, f'bredderne giver {sum(bredder)} %'
    hoved = ''.join(f'<th>{html.escape(k)}</th>' for k in kolonner)
    krop = ''
    # Cellens polstring er 1,5 mm foroven og forneden. Feltet er resten.
    indre = float(hoejde.removesuffix('mm')) - 3
    for i, r in enumerate(raekker):
        raekke = _slug(r) if r else str(i + 1)
        celler = ''
        for j, k in enumerate(kolonner):
            if j == 0 and r:
                celler += f'<td class="fagnavn">{html.escape(r)}</td>'
            else:
                celler += (f'<td><div class="fi" style="height:{indre}mm">'
                           f'{felt(f"{praefiks}_{raekke}_{_slug(k)}")}'
                           f'</div></td>')
        krop += f'<tr style="height:{hoejde}">{celler}</tr>'
    stil = ''.join(f'<col style="width:{b}%">' for b in bredder)
    return (f'<table class="skema"><colgroup>{stil}</colgroup>'
            f'<thead><tr>{hoved}</tr></thead><tbody>{krop}</tbody></table>')


dybde_html = ''
for b in range(1, FOKUS_BLOKKE + 1):
    felter = ''
    for navn, hint, n, to in DYBDE:
        nd = f'fokus{b}_{_slug(navn)}'
        if to:
            felter += (f'<div class="felt"><span class="mrk">{html.escape(navn)}'
                       f'</span><div class="todelt">'
                       + ''.join(f'<div><span class="und">{html.escape(t)}</span>'
                                 f'{linjer(n, f"{nd}_{_slug(t)}")}</div>'
                                 for t in to)
                       + '</div></div>')
        else:
            h = f' <span class="hint">{html.escape(hint)}</span>' if hint else ''
            felter += (f'<div class="felt"><span class="mrk">'
                       f'{html.escape(navn)}</span>{h}{linjer(n, nd)}</div>')
    dybde_html += (f'<section class="dybde"><h3>Fag: '
                   f'{udfyld(f"fokus{b}_fag")}</h3>{felter}</section>')

CSS = '''
*{box-sizing:border-box}
body{margin:0;font-family:Helvetica,Arial,sans-serif;color:#1a2233;
font-size:10pt;line-height:1.35}
h1{font-size:16pt;margin:0 0 1mm}
h2{font-size:11.5pt;margin:5mm 0 2mm;padding-bottom:1mm;
border-bottom:1.5px solid #1a2233}
h3{font-size:10.5pt;margin:0 0 2mm}
.und,.hint{color:#586074;font-weight:400}
.hint{font-size:8.5pt;font-style:italic}
.topline{display:flex;justify-content:space-between;align-items:baseline;
color:#586074;font-size:9pt;margin-bottom:3mm}
.felter{display:flex;gap:4mm;margin:0 0 4mm}
.felter > div{flex:1}
.felter .mrk{display:block;font-size:8pt;letter-spacing:.4px;
text-transform:uppercase;color:#586074;margin-bottom:1mm}
.udfyld{display:block;border-bottom:1px solid #1a2233;height:7mm;
position:relative}
.figur{margin:4mm 0 2mm}
.figur svg{display:block;width:100%}
table.skema{width:100%;border-collapse:collapse;margin:0 0 3mm}
table.skema th,table.skema td{border:1px solid #9aa4b5;padding:1.5mm 2mm;
text-align:left;vertical-align:top}
table.skema th{background:#eef2f8;font-size:8pt;letter-spacing:.4px;
text-transform:uppercase;color:#586074;font-weight:700}
table.skema td.fagnavn{font-weight:700;background:#f6f8fc;font-size:9.5pt}
.dybde{border:1px solid #c9d2e0;border-radius:3mm;padding:3mm 5mm 1mm;
margin:0 0 3mm}
.dybde h3 .udfyld{display:inline-block;width:62%;height:5mm;vertical-align:-1mm}
.felt{margin:0 0 1mm}
.felt .mrk{font-size:8pt;letter-spacing:.4px;text-transform:uppercase;
color:#586074;font-weight:700}
.todelt{display:flex;gap:4mm}
.todelt > div{flex:1}
.linjer{margin-top:1mm;position:relative}
.linje{height:7mm;border-bottom:0.2mm solid #c9d2e0}
.side2{page-break-before:always}
.fi{position:relative}
/* Markoererne. Hvid tekst paa hvid bund: usynlige paa papiret og paa
   skaermen, men `pdftotext -bbox` kan stadig sige, hvor de staar. Det er
   dem, feltets rektangel bliver regnet ud fra. position:relative paa en
   <td> faar Chromium til at droppe de kollapsede streger, saa markoererne
   staar i en div inde i cellen i stedet. */
.mA,.mB{position:absolute;font-size:3pt;line-height:1;color:#fff}
.mA{left:0;top:0}
.mB{right:0;bottom:0}
@page{size:A4;margin:12mm}
'''

FELTER = ['Barn', 'Klasse', 'Dato', 'Kl.', 'Til stede']

KROP = f'''
<div class="topline"><span>Skole-hjem-samtale · fagligt fokus</span>
<span>{MINUTTER} minutter · ét ark pr. barn</span></div>
<h1>Samtaleark</h1>
<div class="felter">
{''.join(f'<div><span class="mrk">{f}</span>{udfyld("ark_" + _slug(f))}</div>'
         for f in FELTER)}
</div>
<div class="figur">{FG.tidsplan(TIDSPLAN, W=700, tal=False)}</div>
<h2>{OVERSKRIFT}</h2>
{skema(OVERSIGT_KOL, FAG, hoejde=RAEKKE, bredder=[17, 45, 38],
       praefiks='fag')}
<div class="side2"></div>
<h2>Fokusfag</h2>
{dybde_html}
<h2>Aftaler</h2>
{skema(AFTALER_KOL, AFTALER_RAEKKER, hoejde='15mm', bredder=[54, 26, 20],
       praefiks='aftale')}'''

DOK = ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
       '<title>Samtaleark · skole-hjem</title><style>' + CSS
       + '</style></head><body>' + KROP + '</body></html>')

def _maal(pdf):
    """Hvor landede markoererne? Giver feltspecifikationer i PDF-punkter med
    nulpunkt nederst til venstre, som resten af PDF-verdenen regner i."""
    ud = subprocess.run(['pdftotext', '-bbox', pdf, '-'],
                        capture_output=True, text=True, check=True).stdout
    ORD = re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)" '
                     r'xMax="([\d.]+)" yMax="([\d.]+)">([^<]+)</word>')
    hoejder, fundet, side = [], {}, -1
    for linje in ud.splitlines():
        s = re.search(r'<page width="[\d.]+" height="([\d.]+)"', linje)
        if s:
            side += 1
            hoejder.append(float(s.group(1)))
            continue
        o = ORD.search(linje)
        if not o or not o.group(5).startswith((MA, MB)):
            continue
        assert o.group(5) not in fundet, f'markøren {o.group(5)} står to steder'
        fundet[o.group(5)] = (side, *(float(o.group(i)) for i in range(1, 5)))

    spec = []
    for f in FORMULAR:
        a, b = f'{MA}{f["nr"]:03d}', f'{MB}{f["nr"]:03d}'
        assert a in fundet and b in fundet, f'{f["navn"]}: markør væk ({a}/{b})'
        sa, ax0, ay0, _, _ = fundet[a]
        sb, _, _, bx1, by1 = fundet[b]
        assert sa == sb, f'{f["navn"]}: hjørnerne er på hver sin side'
        h = hoejder[sa]
        rect = [ax0, h - by1, bx1, h - ay0]
        assert rect[2] - rect[0] > 20, f'{f["navn"]}: {rect[2]-rect[0]:.0f} pt bredt'
        assert rect[3] - rect[1] > 10, f'{f["navn"]}: {rect[3]-rect[1]:.0f} pt højt'
        spec.append({'navn': f['navn'], 'side': sa, 'rect': rect,
                     'flerlinje': f['flerlinje']})
    return spec


def _python_med_pypdf():
    """pypdf ligger ikke i den samme fortolker i alle containere. Find en,
    der har den, i stedet for at gaette paa `python3` og fejle sent."""
    for p in (sys.executable, 'python3.13', 'python3'):
        if p and (p == sys.executable or shutil.which(p)):
            if subprocess.run([p, '-c', 'import pypdf'],
                              capture_output=True).returncode == 0:
                return p
    sys.exit('pypdf findes ikke i nogen af fortolkerne — kan ikke lave felter')


os.makedirs(os.path.dirname(UD_HTML), exist_ok=True)
open(UD_HTML, 'w', encoding='utf-8').write(DOK)
subprocess.run(['node', os.path.join(ROD, 'claude', 'html_til_pdf.mjs'),
                UD_HTML, UD_PDF], check=True, stdout=subprocess.DEVNULL)
os.remove(UD_HTML)

spec = _maal(UD_PDF)
with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False,
                                 encoding='utf-8') as fh:
    json.dump(spec, fh)
    spec_sti = fh.name
subprocess.run([_python_med_pypdf(),
                os.path.join(ROD, 'claude', 'pdf_felter.py'),
                UD_PDF, spec_sti], check=True)
os.remove(spec_sti)

print(f'skrevet:  {UD_PDF}')
print(f'{len(FAG)} fag · {MINUTTER} min · barnet selv {_barnet} af {MINUTTER}')
print(f'{len(spec)} udfyldelige felter')
