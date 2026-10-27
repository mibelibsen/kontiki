# -*- coding: utf-8 -*-
"""Bygger vejledning/skolehjemsamtale.pdf — en udfyldelig PDF i to dele.

Ét dokument pr. barn, tre sider:

  side 1  Barnets del.   Barnet udfylder den selv, inden samtalen.
  side 2  Lærerens del.  Standpunkt og barnets vurdering i de fire fag.
  side 3  Lærerens del.  De to fokusfag og aftalerne.

Alle felter er rigtige formularfelter: man aabner PDF'en og skriver i den.
Den kan ogsaa printes og udfyldes i haanden - felterne er tegnet som bokse,
ikke som linjer, saa der er lige meget plads begge veje.

    python3 claude/byg_samtaleark.py

Feltmaalene gaettes ikke. Hvert felt faar to usynlige markoerer i hjoernerne,
PDF'en bliver bygget, og `pdftotext -bbox` siger bagefter, hvor de to
markoerer landede. Rektanglet er forskellen mellem dem. Det er ogsaa derfor,
det er sikkert at flytte rundt paa layoutet: maalene foelger med af sig selv.

Arket ligger i vejledning/, som er udelukket fra deploy. Det bliver udfyldt
med vurderinger af et navngivet barn og hoerer ikke paa et offentligt site.
PDF'en er en bygget fil og er ikke i git; scriptet er kilden.
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

BARN_KOL = ['Fag', 'Sådan synes jeg selv, det går',
            'Det vil jeg gerne blive bedre til']
BARN_SPOERGSMAAL = [
    ('Det er jeg glad for i skolen', 'barn_glad'),
    ('Her har jeg brug for hjælp', 'barn_hjaelp'),
    ('Det vil jeg gerne tale om til samtalen', 'barn_tale'),
]

LAERER_KOL = ['Fag', 'Standpunkt', 'Barnets vurdering']

# Stoette i skolen, hjemme og hos barnet selv er det samme spoergsmaal stillet
# tre steder: hvad skal der til. De staar derfor i én raekke med tre kolonner -
# det goer det tydeligt, at de tre ting skal haenge sammen.
DYBDE = [
    ('Standpunkt', 'faglige områder', 'standpunkt', 26, None),
    ('Mål', 'Hvad er det næste skridt', 'maal', 26, None),
    ('Hvad skal der til?', '', 'skal', 36,
     [('I skolen', 'skolen'), ('Hjemme', 'hjemme'), ('Barn', 'barn')]),
]

AFTALER_KOL = ['Aftale', 'Hvem gør det', 'Hvornår']
AFTALER_RAEKKER = 3

# To tomme blokke. De har ingen numre: de to fag vaelges under samtalen, og
# et nummer ved siden af et fag ligner en rangordning.
FOKUS_BLOKKE = 2

# Raekkehoejder, maalt saa hver side fyldes ud. Staar de for lavt, staar der
# en tom tredjedel nederst; for hoejt, og der kommer en side mere.
BARN_RAEKKE = 22
LAERER_RAEKKE = 38
AFTALE_RAEKKE = 15

# Markoererne. To bogstavkombinationer, der ikke staar i et dansk ord, saa
# de ikke kan forveksles med sidens egen tekst, naar den bliver laest ud igen.
MA, MB = 'qQa', 'qQb'

FELTER = []       # [{navn, nr, flerlinje}] - fyldes af felt() nedenfor


def _slug(s):
    s = (s.lower().replace('æ', 'ae').replace('ø', 'oe').replace('å', 'aa')
         .replace('/', '-'))
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def felt(navn, flerlinje=True):
    """Markoererne til ét felt. De skal staa i en kasse med position:relative,
    for det er den kasse, feltet kommer til at fylde."""
    nr = len(FELTER) + 1
    FELTER.append({'navn': navn, 'nr': nr, 'flerlinje': flerlinje})
    return (f'<span class="mA">{MA}{nr:03d}</span>'
            f'<span class="mB">{MB}{nr:03d}</span>')


def boks(navn, hoejde, flerlinje=True):
    return (f'<div class="fb" style="height:{hoejde}mm">'
            f'{felt(navn, flerlinje)}</div>')


def maerket_boks(maerke, navn, hoejde, hint=''):
    h = f' <span class="hint">{html.escape(hint)}</span>' if hint else ''
    return (f'<div class="felt"><span class="mrk">{html.escape(maerke)}</span>'
            f'{h}{boks(navn, hoejde)}</div>')


def skema(kolonner, raekker, hoejde, bredder, praefiks):
    """Et skema, hvor hver celle ud over den foerste kolonne er et felt.

    `raekker` er enten et tal eller en liste af tekster i foerste kolonne.
    `bredder` er procenter - uden dem fordeler browseren kolonnerne efter
    overskrifternes laengde, og saa bliver "Fag" bred uden grund."""
    if isinstance(raekker, int):
        raekker = [''] * raekker
    assert len(bredder) == len(kolonner), 'én bredde pr. kolonne'
    assert abs(sum(bredder) - 100) < 0.5, f'bredderne giver {sum(bredder)} %'
    hoved = ''.join(f'<th>{html.escape(k)}</th>' for k in kolonner)
    krop = ''
    for i, r in enumerate(raekker):
        navn = _slug(r) if r else str(i + 1)
        indre = hoejde - 3          # cellens polstring, 1,5 mm foroven og forneden
        def c(n):
            return (f'<td class="fcelle"><div class="fi" '
                    f'style="height:{indre}mm">{felt(n)}</div></td>')
        celler = ''
        for j, k in enumerate(kolonner):
            if j == 0 and r:
                celler += f'<td class="fagnavn">{html.escape(r)}</td>'
            else:
                celler += c(f'{praefiks}_{navn}_{_slug(k)}')
        krop += f'<tr style="height:{hoejde}mm">{celler}</tr>'
    stil = ''.join(f'<col style="width:{b}%">' for b in bredder)
    return (f'<table class="skema"><colgroup>{stil}</colgroup>'
            f'<thead><tr>{hoved}</tr></thead><tbody>{krop}</tbody></table>')


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
.del{font-weight:700;letter-spacing:.4px;text-transform:uppercase;
font-size:8pt;color:#1f6fd6}
.del.laerer{color:#586074}
.intro{margin:0 0 3mm;font-size:9.5pt;color:#586074}
.felter{display:flex;gap:4mm;margin:0 0 4mm}
.felter > div{flex:1}
.felter .mrk{display:block;font-size:8pt;letter-spacing:.4px;
text-transform:uppercase;color:#586074;margin-bottom:1mm}
.figur{margin:4mm 0 2mm}
.figur svg{display:block;width:100%}
.fb{position:relative;background:#fbfcfe;border:1px solid #c9d2e0;
border-radius:1.2mm}
table.skema{width:100%;border-collapse:collapse;margin:0 0 3mm}
table.skema th,table.skema td{border:1px solid #9aa4b5;padding:1.5mm 2mm;
text-align:left;vertical-align:top}
table.skema th{background:#eef2f8;font-size:8pt;letter-spacing:.4px;
text-transform:uppercase;color:#586074;font-weight:700}
table.skema td.fagnavn{font-weight:700;background:#f6f8fc;font-size:9.5pt}
table.skema td.fcelle{background:#fbfcfe}
.fi{position:relative}
.dybde{border:1px solid #c9d2e0;border-radius:3mm;padding:3mm 5mm 1mm;
margin:0 0 3mm}
.dybde h3 .fb{display:inline-block;width:62%;height:6mm;vertical-align:-1.5mm}
.felt{margin:0 0 2mm}
.felt .mrk{font-size:8pt;letter-spacing:.4px;text-transform:uppercase;
color:#586074;font-weight:700}
.todelt{display:flex;gap:4mm}
.todelt > div{flex:1}
.todelt .und{display:block;margin-bottom:1mm;font-size:9pt}
.ny-side{page-break-before:always}
/* Markoererne. Hvid tekst paa hvid bund: usynlig paa papiret og paa
   skaermen, men `pdftotext -bbox` kan stadig sige, hvor de staar. Det er
   dem, feltets rektangel bliver regnet ud fra. */
.mA,.mB{position:absolute;font-size:3pt;line-height:1;color:#fff}
.mA{left:0;top:0}
.mB{right:0;bottom:0}
@page{size:A4;margin:12mm}
'''

HOVED = ['Navn', 'Klasse', 'Dato']

dybde_html = ''
for i in range(1, FOKUS_BLOKKE + 1):
    felter = ''
    for maerke, hint, noegle, h, to in DYBDE:
        if to:
            felter += (f'<div class="felt"><span class="mrk">'
                       f'{html.escape(maerke)}</span><div class="todelt">'
                       + ''.join(f'<div><span class="und">{html.escape(t)}</span>'
                                 f'{boks(f"fokus{i}_{noegle}_{n}", h)}</div>'
                                 for t, n in to)
                       + '</div></div>')
        else:
            felter += maerket_boks(maerke, f'fokus{i}_{noegle}', h, hint)
    dybde_html += (f'<section class="dybde"><h3>Fag: '
                   f'<span class="fb">{felt(f"fokus{i}_fag", False)}</span>'
                   f'</h3>{felter}</section>')

SIDE1 = f'''
<div class="topline"><span>Skole-hjem-samtale · fagligt fokus</span>
<span class="del">Barnets del</span></div>
<h1>Samtaleark</h1>
<div class="felter">
{''.join(f'<div><span class="mrk">{f}</span>'
         f'{boks("barn_" + _slug(f), 7, flerlinje=False)}</div>'
         for f in HOVED)}
</div>
<p class="intro">Du skriver selv denne side, inden vi mødes.</p>
<div class="figur">{FG.tidsplan(TIDSPLAN, W=700, tal=False)}</div>
<h2>Mine fag</h2>
{skema(BARN_KOL, FAG, BARN_RAEKKE, [16, 42, 42], 'barn')}
<h2>Mere fra mig</h2>
{''.join(maerket_boks(sp, n, 26) for sp, n in BARN_SPOERGSMAAL)}'''

SIDE2 = f'''
<div class="ny-side"></div>
<div class="topline"><span>Skole-hjem-samtale · fagligt fokus</span>
<span class="del laerer">Lærerens del</span></div>
<h2 style="margin-top:0">{OVERSKRIFT}</h2>
{skema(LAERER_KOL, FAG, LAERER_RAEKKE, [16, 46, 38], 'laerer')}
<h2>Aftaler</h2>
{skema(AFTALER_KOL, AFTALER_RAEKKER, AFTALE_RAEKKE, [54, 26, 20], 'aftale')}'''

SIDE3 = f'''
<div class="ny-side"></div>
<div class="topline"><span>Skole-hjem-samtale · fagligt fokus</span>
<span class="del laerer">Lærerens del</span></div>
<h2 style="margin-top:0">Fokusfag</h2>
{dybde_html}'''

DOK = ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
       '<title>Samtaleark · skole-hjem</title><style>' + CSS
       + '</style></head><body>' + SIDE1 + SIDE2 + SIDE3 + '</body></html>')


def _maal(pdf):
    """Hvor landede markoererne? Giver {nr: (side, rect)} i PDF-punkter med
    nulpunkt nederst til venstre."""
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
        t = o.group(5)
        assert t not in fundet, f'markøren {t} står to steder'
        fundet[t] = (side, *(float(o.group(i)) for i in range(1, 5)))

    spec = []
    for f in FELTER:
        a, b = f'{MA}{f["nr"]:03d}', f'{MB}{f["nr"]:03d}'
        assert a in fundet and b in fundet, f'{f["navn"]}: markør væk ({a}/{b})'
        sa, ax0, ay0, _, _ = fundet[a]
        sb, _, _, bx1, by1 = fundet[b]
        assert sa == sb, f'{f["navn"]}: hjørnerne er på hver sin side'
        h = hoejder[sa]
        rect = [ax0, h - by1, bx1, h - ay0]
        assert rect[2] - rect[0] > 20, f'{f["navn"]} er {rect[2]-rect[0]:.0f} pt bredt'
        assert rect[3] - rect[1] > 12, f'{f["navn"]} er {rect[3]-rect[1]:.0f} pt højt'
        spec.append({'navn': f['navn'], 'side': sa, 'rect': rect,
                     'flerlinje': f['flerlinje']})
    return spec


def _python_med_pypdf():
    """pypdf ligger ikke i den samme fortolker i alle containere. Find en,
    der har den, i stedet for at gaette paa `python3` og fejle sent."""
    for p in (sys.executable, 'python3.13', 'python3'):
        if p and shutil.which(p.split('/')[-1]) or p == sys.executable:
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

sider = sorted({f['side'] for f in spec})
print(f'skrevet:  {UD_PDF}')
print(f'{len(FAG)} fag · {MINUTTER} min · barnet selv {_barnet} af {MINUTTER}')
print(f'{len(spec)} udfyldelige felter på siderne '
      f'{", ".join(str(s + 1) for s in sider)}')
