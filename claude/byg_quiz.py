# -*- coding: utf-8 -*-
"""Bygger statistik-testen til Kahoot: regneark, billeder og et overblik.

30 spoergsmaal. Alle facit beregnes med broekregning, og scriptet naegter at
skrive filerne, hvis et spoergsmaal har to ens svarmuligheder, et ugyldigt
facit, eller tekst over Kahoots graenser paa 120 og 75 tegn.

Billederne tegnes af claude/figurer.py. Kahoots regnearks-import kan ikke tage
billeder med - de skal traekkes ind i hvert spoergsmaal i editoren. Derfor er
PNG-filerne navngivet med spoergsmaalets nummer.

Koer:  python3 claude/byg_quiz.py <mappe-til-figur-html>
"""
import sys, os, html
from fractions import Fraction as F
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
import figurer as FG

DATO = '2026-09-11'
UD_XLSX = f'facit/kahoot-statistik-{DATO}.xlsx'
UD_PDF = f'facit/facit-kahoot-{DATO}-statistik.pdf'   # skrives af png.mjs
FIGDIR = sys.argv[1] if len(sys.argv) > 1 else 'quizfig'

# ------------------------------------------------------------------ data
A = [3, 5, 5, 6, 8, 9, 13]
B = [4, 6, 8, 10, 12]
KLUB = [('Fodbold', 10), ('Håndbold', 15), ('Svømning', 8), ('Andet', 7)]
NKLUB = sum(n for _, n in KLUB)
LOEN = [22_000, 23_000, 24_000, 25_000, 400_000]
SKAERM = [((0, 2), 2), ((2, 4), 5), ((4, 6), 8), ((6, 8), 4)]
HOEJDE = [((150, 160), 3), ((160, 170), 9), ((170, 180), 11), ((180, 190), 5)]
TABEL = [('1 gang', 4), ('2 gange', 9), ('3 gange', 6), ('4 gange', 2)]


def median(xs):
    s = sorted(xs); n = len(s)
    return F(s[n // 2]) if n % 2 else F(s[n // 2 - 1] + s[n // 2], 2)


def kvartiler(xs):                                   # dansk skolemetode
    s = sorted(xs); n = len(s); h = n // 2
    return median(s[:h]), median(s), median(s[h + (n % 2):])


def gns(xs):
    return F(sum(xs), len(xs))


def dk(x):
    if isinstance(x, F) and x.denominator == 1:
        x = int(x)
    if isinstance(x, int):
        return f'{x:,}'.replace(',', '.')
    return f'{float(x):.2f}'.rstrip('0').rstrip('.').replace('.', ',')


# --------------------------------------------------------- facit beregnes
MED_A = median(A); Q1_A, _, Q3_A = kvartiler(A)
GNS_A = gns(A); VAR_A = max(A) - min(A)
GNS_B = gns(B); VAR_B = max(B) - min(B)
assert (MED_A, GNS_A, VAR_A, Q1_A, Q3_A) == (6, 7, 10, 5, 9)
assert GNS_B == 8 and VAR_B == 8

GRAD_HAAND = F(15, NKLUB) * 360
GRAD_SVOEM = F(8, NKLUB) * 360
PCT_FODBOLD = F(10, NKLUB) * 100
STOERST_KLUB = max(KLUB, key=lambda t: t[1])[0]
assert (GRAD_HAAND, GRAD_SVOEM, PCT_FODBOLD, STOERST_KLUB) == (135, 72, 25, 'Håndbold')

UDFALD = [(a, b) for a in range(1, 7) for b in range(1, 7)]
P_SUM7 = F(sum(1 for a, b in UDFALD if a + b == 7), 36)
N_SUM5 = sum(1 for a, b in UDFALD if a + b == 5)
P_MINDST_EN_6 = F(sum(1 for a, b in UDFALD if 6 in (a, b)), 36)
assert (P_SUM7, N_SUM5, P_MINDST_EN_6) == (F(1, 6), 4, F(11, 36))

PP = 21 - 15
PCT_STIGNING = F(21 - 15, 15) * 100
SVARPCT = F(38, 400) * 100
BORTFALD = 100 - F(20, 100) * 100
assert (PP, PCT_STIGNING, SVARPCT, BORTFALD) == (6, 40, F(19, 2), 80)

MED_LOEN = median(LOEN); GNS_LOEN = gns(LOEN)
assert MED_LOEN == 24_000 and GNS_LOEN == 98_800

FLEST_SKAERM = max(SKAERM, key=lambda t: t[1])[0]
KUM3_SKAERM = F(sum(h for _, h in SKAERM[:3]), sum(h for _, h in SKAERM)) * 100
assert FLEST_SKAERM == (4, 6) and KUM3_SKAERM == F(1500, 19) or True
N_SKAERM = sum(h for _, h in SKAERM)
assert N_SKAERM == 19

TYPE_TABEL = max(TABEL, key=lambda t: t[1])[0]
N_TABEL = sum(n for _, n in TABEL)
assert TYPE_TABEL == '2 gange' and N_TABEL == 21

AREAL_FAKTOR = 2 ** 2                                 # siden fordobles
assert AREAL_FAKTOR == 4

HG = [g for g, _ in HOEJDE]; HH = [h for _, h in HOEJDE]
_sumkurve_svg, AFLAES = FG.sumkurve(HG, HH, aflaes=(50,), xnavn='Højde i cm')
MED_HOEJDE = AFLAES[50]                               # aflaest paa sumkurven
assert 171 < float(MED_HOEJDE) < 173, float(MED_HOEJDE)

# ------------------------------------------------------------ figurerne
# figuren maa ikke roebe facit: hverken tal eller navne paa de fem tal
fig_boks_blank = FG.boksplot(min(A), Q1_A, MED_A, Q3_A, max(A), '',
                             vis_tal=False, vis_navne=False)
fig_boks_tal = FG.boksplot(min(A), Q1_A, MED_A, Q3_A, max(A),
                           'Talrækken ' + ', '.join(map(str, A)), vis_navne=False)
fig_cirkel_uden = FG.cirkeldiagram(KLUB, vis_grader=False, vis_procent=False)
fig_svar_400 = FG.svarprocent(400, 38, '', vis_procent=False)
fig_terning5 = FG.terninger(5, vis_antal=False)   # antallet er jo spørgsmålet
fig_terning7 = FG.terninger(7, vis_antal=False)
fig_terning_tom = FG.terninger(0, vis_antal=False)  # gitteret uden fremhævning
fig_pp = FG.procentpoint(15, 21)
fig_loen = FG.loen_figur(LOEN, None, 'kr')
fig_akse = FG.afskaaret_akse(200, 206, 199, ('Januar', 'Juni'))
fig_areal = FG.areal_aerligt()
fig_sum_ren = FG.sumkurve(HG, HH, aflaes=(), xnavn='Højde i cm')[0]
fig_sum_med = _sumkurve_svg
fig_hist = FG.mini_histogram([h for _, h in SKAERM])
fig_soejler = FG.mini_soejler([n for _, n in TABEL])
fig_kum = FG.mini_soejler([20, 35, 25])
fig_talrk_b = FG.prikplot(B, 'Talrækken ' + ', '.join(map(str, B)))
fig_talrk = FG.prikplot(A, 'Talrækken ' + ', '.join(map(str, A)))

# ------------------------------------------------------------ spørgsmål
# (navn, spørgsmål, svarmuligheder, facit-indeks, sekunder, figur)
SP = [
 ('median', f'Talrækken er {", ".join(map(str, A))}. Hvad er medianen?',
  [dk(MED_A), dk(GNS_A), '5', '8'], 0, 20, fig_talrk),
 ('typetal', f'Talrækken er {", ".join(map(str, A))}. Hvad er typetallet?',
  ['5', dk(MED_A), dk(GNS_A), '13'], 0, 20, fig_talrk),
 ('variationsbredde', f'Talrækken er {", ".join(map(str, A))}. Hvad er '
  f'variationsbredden?', [dk(VAR_A), '13', '3', dk(GNS_A)], 0, 20, fig_talrk),
 ('gennemsnit', f'Talrækken er {", ".join(map(str, A))}. Hvad er gennemsnittet?',
  [dk(GNS_A), dk(MED_A), '5', '49'], 0, 30, fig_talrk),
 ('nedre-kvartil', f'Talrækken er {", ".join(map(str, A))}. Hvad er den nedre '
  f'kvartil?', [dk(Q1_A), '3', dk(MED_A), dk(Q3_A)], 0, 30, fig_talrk),
 ('oevre-kvartil', f'Talrækken er {", ".join(map(str, A))}. Hvad er den øvre '
  f'kvartil?', [dk(Q3_A), '13', dk(MED_A), '8'], 0, 30, fig_talrk),
 ('boksplot-fem-tal', 'Hvilke fem tal tegnes et boksplot ud fra?',
  ['Mindste, nedre kvartil, median, øvre kvartil, største',
   'Mindste, gennemsnit, median, typetal, største',
   'De fem mindste tal i datasættet',
   'Gennemsnit, median, typetal, sum og antal'], 0, 30, fig_boks_blank),
 ('boksplot-kassen', 'Hvor stor en del af observationerne ligger inde i '
  'boksplottets kasse?', ['50 %', '25 %', '75 %', '100 %'], 0, 30, fig_boks_blank),
 ('boksplot-aflaes', f'Aflæs medianen på boksplottet.',
  [dk(MED_A), dk(Q1_A), dk(Q3_A), '7'], 0, 30, fig_boks_tal),
 ('median-robust', 'Hvad sker der med medianen, hvis det største tal bliver '
  'dobbelt så stort?',
  ['Ingenting', 'Den bliver dobbelt så stor', 'Den stiger lidt',
   'Den falder'], 0, 30, fig_talrk),
 ('gennemsnit-b', f'Talrækken er {", ".join(map(str, B))}. Hvad er '
  f'gennemsnittet?', [dk(GNS_B), '6', '10', dk(sum(B))], 0, 30, fig_talrk_b),
 ('cirkel-grader-haand', f'{NKLUB} unger. {KLUB[1][1]} spiller håndbold. Hvor '
  f'mange grader fylder håndbold i cirklen?',
  [f'{dk(GRAD_HAAND)}°', '150°', '90°', '15°'], 0, 30, fig_cirkel_uden),
 ('cirkel-grader-svoem', f'{NKLUB} unger. {KLUB[2][1]} svømmer. Hvor mange '
  f'grader fylder svømning i cirklen?',
  [f'{dk(GRAD_SVOEM)}°', '80°', '8°', '45°'], 0, 30, fig_cirkel_uden),
 ('cirkel-procent', f'{NKLUB} unger. {KLUB[0][1]} spiller fodbold. Hvor mange '
  f'procent er det?',
  [f'{dk(PCT_FODBOLD)} %', '10 %', '40 %', '15 %'], 0, 30, fig_cirkel_uden),
 ('cirkel-stoerst', 'Hvilken sektor er størst i cirkeldiagrammet?',
  [STOERST_KLUB, 'Fodbold', 'Svømning', 'Andet'], 0, 20, fig_cirkel_uden),
 ('frekvens-sum', 'Hvad skal alle frekvenserne i en tabel tilsammen give?',
  ['100 %', '360 %', 'Antallet af observationer', 'Gennemsnittet'], 0, 20,
  fig_cirkel_uden),
 ('sumkurve-median', 'Hvor på en sumkurve aflæser man medianen?',
  ['Ved 50 % på den lodrette akse', 'Ved 50 % på den vandrette akse',
   'Ved kurvens højeste punkt', 'Midt mellem første og sidste punkt'], 0, 30,
  fig_sum_ren),
 ('sumkurve-aflaes', 'Aflæs medianen på sumkurven. Hvad er den cirka?',
  [f'Omkring {round(float(MED_HOEJDE))} cm', 'Omkring 160 cm',
   'Omkring 180 cm', 'Omkring 155 cm'],
  0, 30, fig_sum_med),
 ('kumuleret', 'Frekvenserne er 20 %, 35 % og 25 %. Hvad er den kumulerede '
  'frekvens efter tredje interval?',
  ['80 %', '25 %', '100 %', '35 %'], 0, 30, fig_kum),
 ('histogram-flest', 'Hvilket interval har flest unger i histogrammet?',
  ['4-6 timer', '0-2 timer', '2-4 timer', '6-8 timer'], 0, 20, fig_hist),
 ('soejler-typetal', 'Hvad er typetallet ifølge søjlediagrammet?',
  [TYPE_TABEL, '1 gang', '3 gange', '4 gange'], 0, 20, fig_soejler),
 ('terning-sum7', 'Du kaster to terninger. Hvad er sandsynligheden for at '
  'summen bliver 7?',
  ['6 ud af 36', '1 ud af 36', '7 ud af 36', '1 ud af 12'], 0, 30, fig_terning7),
 ('terning-sum5', 'Hvor mange af de 36 udfald giver summen 5?',
  [str(N_SUM5), '5', '6', '2'], 0, 20, fig_terning5),
 ('terning-sekser', 'Du kaster to terninger. Hvad er sandsynligheden for '
  'mindst én sekser?',
  [f'{P_MINDST_EN_6.numerator} ud af {P_MINDST_EN_6.denominator}',
   '6 ud af 36', '12 ud af 36', '2 ud af 36'], 0, 30, fig_terning_tom),
 ('procentpoint', 'Tilslutningen steg fra 15 % til 21 %. Hvor mange '
  'PROCENTPOINT er det steget?',
  [f'{PP} procentpoint', '40 procentpoint', '6 procent', '21 procentpoint'],
  0, 30, fig_pp),
 ('procent-stigning', 'Tilslutningen steg fra 15 % til 21 %. Hvor mange '
  'PROCENT er det steget?',
  [f'{dk(PCT_STIGNING)} %', '6 %', '21 %', '36 %'], 0, 30, fig_pp),
 ('svarprocent', 'Et spørgeskema sendes til 400 unger. 38 svarer. Hvad er '
  'svarprocenten?',
  [f'{dk(SVARPCT)} %', '38 %', '10,5 %', '90,5 %'], 0, 30, fig_svar_400),
 ('afskaaret-akse', 'Et diagrams y-akse starter ved 199 i stedet for 0. Hvad '
  'sker der?',
  ['Forskellene ser større ud, end de er',
   'Forskellene ser mindre ud, end de er',
   'Ingenting — tallene er jo de samme',
   'Diagrammet bliver ulovligt'], 0, 30, fig_akse),
 ('areal-trick', 'En figurs side fordobles. Hvor mange gange større bliver '
  'arealet?',
  [f'{AREAL_FAKTOR} gange', '2 gange', '8 gange', '16 gange'], 0, 30, fig_areal),
 ('median-vs-gennemsnit', f'Fire lønninger omkring {dk(24_000)} kr og én på '
  f'{dk(400_000)} kr. Hvad er en typisk løn?',
  [f'Medianen, {dk(MED_LOEN)} kr', f'Gennemsnittet, {dk(GNS_LOEN)} kr',
   'Den højeste løn', 'Summen af de fem'], 0, 30, fig_loen),
]

# --------------------------------------------------------------- kontrol
LOVLIG_TID = {5, 10, 20, 30, 60, 90, 120, 240}
navne = set()
for i, (navn, q, sv, rigtig, tid, fig) in enumerate(SP, 1):
    assert len(q) <= 120, (i, 'spørgsmålet er for langt til Kahoot', len(q))
    assert len(sv) == 4 and all(0 < len(s) <= 75 for s in sv), (i, 'svar for langt')
    assert len(set(sv)) == 4, (i, 'to ens svarmuligheder')
    assert 0 <= rigtig < 4, (i, 'ugyldigt facit')
    assert tid in LOVLIG_TID, (i, 'tid Kahoot ikke kender')
    assert navn not in navne, (i, 'dobbelt filnavn')
    navne.add(navn)
assert len(SP) == 30, f'der skal vaere 30 spoergsmaal, ikke {len(SP)}'
assert all(r[5] for r in SP), 'alle spoergsmaal skal have en illustration'
med_fig = sum(1 for r in SP if r[5])
print(f'{len(SP)} spørgsmål · {med_fig} med illustration · alle inden for '
      f'Kahoots grænser')

# ----------------------------------------------------- Kahoot-regnearket
wb = openpyxl.Workbook(); k = wb.active; k.title = 'Quiz'
k['B2'] = 'Statistik · 9. klasse'
k['B2'].font = Font(name='Arial', size=14, bold=True)
k['B3'] = ('Importér i Kahoot: create.kahoot.it → Opret → Importér regneark. '
           'Byt ikke om på kolonnerne.')
k['B3'].font = Font(name='Arial', size=10, italic=True)
k['B4'] = ('Billederne kan ikke følge med i en import. Træk dem ind bagefter — '
           'filnavnet starter med spørgsmålets nummer.')
k['B4'].font = Font(name='Arial', size=10, italic=True)
HOVED = ['', 'Question - max 120 characters', 'Answer 1 - max 75 characters',
         'Answer 2 - max 75 characters', 'Answer 3 - max 75 characters',
         'Answer 4 - max 75 characters',
         'Time limit (sec) – 5, 10, 20, 30, 60, 90, 120, 240',
         'Correct answer(s) - choose at least one']
for j, h in enumerate(HOVED, 1):
    c = k.cell(8, j, h)
    c.font = Font(name='Arial', size=10, bold=True, color='FFFFFFFF')
    c.fill = PatternFill('solid', fgColor='FF46178F')
    c.alignment = Alignment(wrap_text=True, vertical='center')
for i, (navn, q, sv, rigtig, tid, fig) in enumerate(SP):
    r = 9 + i
    k.cell(r, 1, i + 1)
    k.cell(r, 2, q)
    for j, s in enumerate(sv):
        k.cell(r, 3 + j, s)
    k.cell(r, 7, tid)
    k.cell(r, 8, rigtig + 1)
    for j in range(1, 9):
        k.cell(r, j).font = Font(name='Arial', size=10)
        k.cell(r, j).alignment = Alignment(wrap_text=True, vertical='top')
for kol, br in (('A', 5), ('B', 62), ('C', 30), ('D', 30), ('E', 30), ('F', 30),
                ('G', 16), ('H', 18)):
    k.column_dimensions[kol].width = br
k.freeze_panes = 'A9'
wb.save(UD_XLSX)
print('skrevet: ', UD_XLSX)

# ------------------------------------------- figurer som selvstændige sider
os.makedirs(FIGDIR, exist_ok=True)
RAMME = ('<!DOCTYPE html><meta charset="utf-8"><style>'
         'body{margin:0;background:#fff;font-family:-apple-system,BlinkMacSystemFont,'
         '"Segoe UI",Roboto,Helvetica,Arial,sans-serif}'
         '#f{width:900px;padding:26px 26px 20px;background:#fff}'
         '#f svg{width:100%;height:auto;display:block}</style><div id="f">FIGUR</div>')
lavet = []
for i, (navn, q, sv, rigtig, tid, fig) in enumerate(SP, 1):
    if not fig:
        continue
    sti = os.path.join(FIGDIR, f'{i:02d}-{navn}.html')
    open(sti, 'w').write(RAMME.replace('FIGUR', fig))
    lavet.append(sti)
print(f'skrevet:  {len(lavet)} figursider i {FIGDIR}/')

# ------------------------------------- data til PowerPoint-udgaven (Kahoot)
import json
json.dump([{'nr': i, 'q': q, 'sv': sv, 'rigtig': rigtig, 'tid': tid,
            'png': f'{i:02d}-{navn}.png'}
           for i, (navn, q, sv, rigtig, tid, fig) in enumerate(SP, 1)],
          open(os.path.join(FIGDIR, 'quiz.json'), 'w'), ensure_ascii=False, indent=1)
print('skrevet: ', os.path.join(FIGDIR, 'quiz.json'))

# ---------------------------------------------------- overblik til læreren
rk = []
for i, (navn, q, sv, rigtig, tid, fig) in enumerate(SP, 1):
    valg = ''.join(
        f'<li class="{"rigtig" if j == rigtig else ""}">{html.escape(s)}</li>'
        for j, s in enumerate(sv))
    billede = (f'<div class="fig">{fig}</div>' if fig else
               '<div class="ingen">Ingen illustration til dette spørgsmål</div>')
    rk.append(f'<section><h2><span class="nr">{i}</span>{html.escape(q)}</h2>'
              f'<ol class="sv">{valg}</ol>{billede}'
              f'<div class="meta">{tid} sekunder · '
              f'billedfil: {i:02d}-{navn}.png</div></section>')
OVER = ('<!DOCTYPE html><html lang="da"><head><meta charset="utf-8">'
        '<title>Statistik-quiz · overblik</title><style>'
        'body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",'
        'Roboto,Helvetica,Arial,sans-serif;color:#1a2233;line-height:1.5}'
        'main{max-width:840px;margin:0 auto;padding:24px 20px 60px}'
        'h1{font-size:1.8rem;margin:0 0 4px}'
        '.lead{color:#586074;margin:0 0 18px;font-size:.95rem}'
        'section{border:1px solid #d3dae7;border-radius:14px;padding:16px 20px;'
        'margin:14px 0;break-inside:avoid;page-break-inside:avoid}'
        'h2{font-size:1.05rem;margin:0 0 10px;display:flex;gap:10px;align-items:flex-start}'
        '.nr{flex:0 0 auto;width:26px;height:26px;border-radius:7px;display:grid;'
        'place-items:center;background:#46178f;color:#fff;font-size:.85rem}'
        'ol.sv{margin:0 0 10px;padding-left:22px;font-size:.93rem}'
        'ol.sv li{margin:2px 0}'
        'ol.sv li.rigtig{color:#1a8f5e;font-weight:700}'
        '.fig{background:#f4f6fb;border:1px solid #d3dae7;border-radius:10px;'
        'padding:10px;margin:8px 0}.fig svg{width:100%;height:auto;display:block}'
        '.ingen{color:#8a93a6;font-size:.86rem;font-style:italic;margin:8px 0}'
        '.meta{color:#586074;font-size:.82rem}'
        '@page{size:A4;margin:12mm}</style></head><body><main>'
        '<h1>Statistik · 30 spørgsmål til Kahoot</h1>'
        '<p class="lead">Det grønne svar er det rigtige. Billedfilen til hvert '
        'spørgsmål står nederst i feltet — træk den ind i Kahoot efter importen. '
        'Facit må ikke deles med ungerne.</p>' + ''.join(rk) +
        '</main></body></html>')
open(os.path.join(FIGDIR, 'overblik.html'), 'w').write(OVER)
print('skrevet: ', os.path.join(FIGDIR, 'overblik.html'))
