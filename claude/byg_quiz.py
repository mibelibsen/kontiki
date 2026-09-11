# -*- coding: utf-8 -*-
"""Bygger statistik-testen i to formater: Kahoot-regneark og Word til Forms.

Alle facit beregnes med broekregning. Ingen svarmulighed er skrevet af i haanden
uden at vaere regnet efter, og scriptet naegter at skrive filen, hvis et
spoergsmaal har to rigtige svar, ingen rigtige, eller er for langt til Kahoot.
"""
from fractions import Fraction as F
import openpyxl, docx
from openpyxl.styles import Font, Alignment, PatternFill
from docx.shared import Pt, RGBColor

# ------------------------------------------------------------------ data
A = [3, 5, 5, 6, 8, 9, 13]                      # datasaettet fra statistik.html
KLUB = [('fodbold', 10), ('håndbold', 15), ('svømning', 8), ('andet', 7)]
NKLUB = sum(n for _, n in KLUB)
LOEN = [22_000, 23_000, 24_000, 25_000, 400_000]

def median(xs):
    s = sorted(xs); n = len(s)
    return F(s[n // 2]) if n % 2 else F(s[n // 2 - 1] + s[n // 2], 2)

def kvartiler(xs):                               # dansk skolemetode
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

# ------------------------------------------------------ beregnede facit
MED_A = median(A); Q1_A, _, Q3_A = kvartiler(A)
GNS_A = gns(A); VAR_A = max(A) - min(A)
assert MED_A == 6 and GNS_A == 7 and VAR_A == 10 and Q1_A == 5 and Q3_A == 9

GRAD_HAAND = F(15, NKLUB) * 360
GRAD_SVOEM = F(8, NKLUB) * 360
PCT_FODBOLD = F(10, NKLUB) * 100
assert GRAD_HAAND == 135 and GRAD_SVOEM == 72 and PCT_FODBOLD == 25

P_SUM7 = F(6, 36)                  # 6 af 36 udfald giver 7
P_MINDST_EN_6 = 1 - F(5, 6) ** 2   # 11/36
assert P_SUM7 == F(1, 6) and P_MINDST_EN_6 == F(11, 36)

PP = 21 - 15                        # procentpoint
PCT_STIGNING = F(21 - 15, 15) * 100
assert PP == 6 and PCT_STIGNING == 40

SVARPCT = F(38, 400) * 100
assert SVARPCT == F(19, 2)          # 9,5 %

MED_LOEN = median(LOEN); GNS_LOEN = gns(LOEN)
assert MED_LOEN == 24_000 and GNS_LOEN == 98_800

# ------------------------------------------------------------ spørgsmål
# (spørgsmål, [svarmuligheder], indeks for det rigtige, sekunder)
SP = [
 (f'Talrækken er {", ".join(map(str, A))}. Hvad er medianen?',
  [dk(MED_A), dk(GNS_A), '5', '8'], 0, 20),
 (f'Talrækken er {", ".join(map(str, A))}. Hvad er typetallet?',
  ['5', dk(MED_A), dk(GNS_A), '13'], 0, 20),
 (f'Talrækken er {", ".join(map(str, A))}. Hvad er variationsbredden?',
  [dk(VAR_A), '13', '3', dk(GNS_A)], 0, 20),
 (f'Talrækken er {", ".join(map(str, A))}. Hvad er gennemsnittet?',
  [dk(GNS_A), dk(MED_A), '5', '49'], 0, 30),
 (f'Talrækken er {", ".join(map(str, A))}. Hvad er den nedre kvartil?',
  [dk(Q1_A), '3', dk(MED_A), dk(Q3_A)], 0, 30),
 ('Hvilke fem tal tegnes et boksplot ud fra?',
  ['Mindste, nedre kvartil, median, øvre kvartil, største',
   'Mindste, gennemsnit, median, typetal, største',
   'De fem mindste tal i datasættet',
   'Gennemsnit, median, typetal, sum og antal'], 0, 30),
 ('Hvad sker der med medianen, hvis det største tal bliver dobbelt så stort?',
  ['Ingenting', 'Den bliver dobbelt så stor',
   'Den stiger lidt', 'Den falder'], 0, 30),
 (f'{NKLUB} unger. {KLUB[1][1]} spiller håndbold. Hvor mange grader fylder '
  f'håndbold i et cirkeldiagram?',
  [f'{dk(GRAD_HAAND)}°', '150°', '90°', '15°'], 0, 30),
 (f'{NKLUB} unger. {KLUB[2][1]} svømmer. Hvor mange grader fylder svømning '
  f'i et cirkeldiagram?',
  [f'{dk(GRAD_SVOEM)}°', '80°', '8°', '45°'], 0, 30),
 (f'{NKLUB} unger. {KLUB[0][1]} spiller fodbold. Hvor mange procent er det?',
  [f'{dk(PCT_FODBOLD)} %', '10 %', '40 %', '15 %'], 0, 30),
 ('Hvad skal alle frekvenserne i en tabel tilsammen give?',
  ['100 %', '360 %', 'Antallet af observationer', 'Gennemsnittet'], 0, 20),
 ('Hvor på en sumkurve aflæser man medianen?',
  ['Ved 50 % på den lodrette akse', 'Ved 50 % på den vandrette akse',
   'Ved kurvens højeste punkt', 'Midt mellem første og sidste punkt'], 0, 30),
 ('Frekvenserne er 20 %, 35 % og 25 %. Hvad er den kumulerede frekvens efter '
  'tredje interval?',
  ['80 %', '25 %', '100 %', '35 %'], 0, 30),
 ('Du kaster to terninger. Hvad er sandsynligheden for at summen bliver 7?',
  ['6 ud af 36', '1 ud af 36', '7 ud af 36', '1 ud af 12'], 0, 30),
 ('Du kaster to terninger. Hvad er sandsynligheden for mindst én sekser?',
  [f'{P_MINDST_EN_6.numerator} ud af {P_MINDST_EN_6.denominator}',
   '6 ud af 36', '12 ud af 36', '2 ud af 36'], 0, 30),
 ('Tilslutningen steg fra 15 % til 21 %. Hvor mange PROCENTPOINT er det steget?',
  [f'{PP} procentpoint', '40 procentpoint', '6 procent', '21 procentpoint'], 0, 30),
 ('Tilslutningen steg fra 15 % til 21 %. Hvor mange PROCENT er det steget?',
  [f'{dk(PCT_STIGNING)} %', '6 %', '21 %', '36 %'], 0, 30),
 ('Et spørgeskema sendes til 400 unger. 38 svarer. Hvad er svarprocenten?',
  [f'{dk(SVARPCT)} %', '38 %', '10,5 %', '90,5 %'], 0, 30),
 ('Et diagram har en y-akse, der starter ved 199 i stedet for 0. Hvad sker der?',
  ['Forskellene ser større ud, end de er',
   'Forskellene ser mindre ud, end de er',
   'Ingenting — tallene er jo de samme',
   'Diagrammet bliver ulovligt'], 0, 30),
 (f'Fem lønninger: fire omkring {dk(24_000)} kr og én på {dk(400_000)} kr. '
  f'Hvad beskriver bedst en typisk løn?',
  [f'Medianen, {dk(MED_LOEN)} kr', f'Gennemsnittet, {dk(GNS_LOEN)} kr',
   'Den højeste løn', 'Summen af de fem'], 0, 30),
]

# --------------------------------------------------------------- kontrol
LOVLIG_TID = {5, 10, 20, 30, 60, 90, 120, 240}
for i, (q, sv, rigtig, tid) in enumerate(SP, 1):
    assert len(q) <= 120, (i, 'spørgsmål for langt til Kahoot', len(q))
    assert len(sv) == 4 and all(0 < len(s) <= 75 for s in sv), (i, 'svar for langt')
    assert len(set(sv)) == 4, (i, 'to ens svarmuligheder')
    assert 0 <= rigtig < 4 and tid in LOVLIG_TID, (i, 'ugyldigt facit eller tid')
print(f'{len(SP)} spørgsmål · alle inden for Kahoots grænser')

# ----------------------------------------------------- Kahoot-regnearket
wb = openpyxl.Workbook(); k = wb.active; k.title = 'Quiz'
k['B2'] = 'Statistik · 9. klasse'
k['B2'].font = Font(name='Arial', size=14, bold=True)
k['B3'] = ('Importér i Kahoot: create.kahoot.it → Opret → Importér regneark. '
           'Ret ikke i rækkefølgen af kolonner.')
k['B3'].font = Font(name='Arial', size=10, italic=True)
HOVED = ['', 'Question - max 120 characters', 'Answer 1 - max 75 characters',
         'Answer 2 - max 75 characters', 'Answer 3 - max 75 characters',
         'Answer 4 - max 75 characters',
         'Time limit (sec) – 5, 10, 20, 30, 60, 90, 120, 240',
         'Correct answer(s) - choose at least one']
for j, h in enumerate(HOVED, 1):
    c = k.cell(8, j, h)
    c.font = Font(name='Arial', size=10, bold=True, color='FFFFFFFF')
    c.fill = PatternFill('solid', fgColor='FF46178F')      # Kahoots lilla
    c.alignment = Alignment(wrap_text=True, vertical='center')
for i, (q, sv, rigtig, tid) in enumerate(SP):
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
wb.save('/home/user/kontiki/facit/kahoot-statistik-2026-09-11.xlsx')

# ------------------------------------------------- Word til Forms/print
d = docx.Document()
for st, stoerrelse in (('Normal', 11), ('Title', 22)):
    try:
        d.styles[st].font.name = 'Arial'
    except KeyError:
        pass
d.add_heading('Statistik · test til 9. klasse', 0)
p = d.add_paragraph('20 spørgsmål med fire svarmuligheder. Det rigtige svar er '
                    'markeret med en stjerne (*) og står med fed.')
p.runs[0].font.size = Pt(10)
d.add_paragraph('Facit må ikke deles med ungerne. Filen hører til i facit/.'
                ).runs[0].font.size = Pt(10)
for i, (q, sv, rigtig, tid) in enumerate(SP, 1):
    h = d.add_paragraph()
    h.add_run(f'{i}. {q}').bold = True
    for j, s in enumerate(sv):
        linje = d.add_paragraph(style='List Bullet')
        r = linje.add_run(('* ' if j == rigtig else '') + s)
        if j == rigtig:
            r.bold = True
            r.font.color.rgb = RGBColor(0x1A, 0x8F, 0x5E)
d.save('/home/user/kontiki/facit/quiz-statistik-2026-09-11.docx')
print('skrevet:  facit/kahoot-statistik-2026-09-11.xlsx')
print('skrevet:  facit/quiz-statistik-2026-09-11.docx')
