# -*- coding: utf-8 -*-
"""Bygger boksplot.html - forklaring og 20 spoergsmaal med figur til hvert.

Siden bruger sitets egen quizmotor. Den loeftes ud af `statistik.html`
sammen med CSS'en og rammen omkring (overlay, navnefelt, fremgangslinje,
resultattabel), saa de to sider ikke kan komme til at opfoere sig
forskelligt. Kun STORAGE_KEY og modulnavnene byttes ud - ellers ville de
to sider dele gemte svar.

**Alle tal regnes, ingen skrives af.** Femtalssammendragene kommer ud af
raadataene med den danske skolemetode, og en assert tjekker hvert
spoergsmaal: at det rigtige svar staar blandt mulighederne praecis én
gang, og at de tre muligheder er forskellige.

    python3 claude/byg_boksplot.py
"""
import html
import os
import re
import sys
from fractions import Fraction as F

HER = os.path.dirname(os.path.abspath(__file__))
ROD = os.path.dirname(HER)
sys.path.insert(0, HER)
import figurer as FG

UD = os.path.join(ROD, 'boksplot.html')
SKABELON = os.path.join(ROD, 'statistik.html')


# --------------------------------------------------- de fem tal, regnet ud
def median(xs):
    s = sorted(xs); n = len(s)
    return F(s[n // 2]) if n % 2 else F(s[n // 2 - 1] + s[n // 2], 2)


def kvartiler(xs):
    """Dansk skolemetode, den samme som i claude/byg_quiz.py: medianen
    deler raekken, og kvartilerne er medianerne i hver halvdel. Midterste
    tal regnes IKKE med i halvdelene, naar antallet er ulige."""
    s = sorted(xs); n = len(s); h = n // 2
    return median(s[:h]), median(s), median(s[h + (n % 2):])


def fem(xs):
    q1, med, q3 = kvartiler(xs)
    return (F(min(xs)), q1, med, q3, F(max(xs)))


# Proevet af paa et kendt eksempel, saa metoden ikke kan skride ubemaerket.
assert fem([10, 15, 15, 20, 25, 30, 30, 35, 40, 45, 50, 60, 70, 75, 120]) == \
    (10, 20, 35, 60, 120), 'skolemetoden regner ikke som forventet'
assert fem([1, 2, 3, 4]) == (1, F(3, 2), F(5, 2), F(7, 2), 4)


def dk(x):
    x = F(x)
    return str(int(x)) if x.denominator == 1 else \
        f'{float(x):.2f}'.rstrip('0').rstrip('.').replace('.', ',')


# ----------------------------------------------------------- eksempeldata
LEKTIER = [10, 15, 15, 20, 25, 30, 30, 35, 40, 45, 50, 60, 70, 75, 120]
L5 = fem(LEKTIER)
assert L5 == (10, 20, 35, 60, 120)
KVARTILBREDDE = L5[3] - L5[1]
VARIATION = L5[4] - L5[0]

# Spoergsmaalenes datasaet. n = 11 overalt i foerste quiz: saa har begge
# halvdele et ulige antal, og alle fem tal bliver hele.
SAET = {
 'q1': [3, 5, 6, 8, 9, 11, 12, 14, 16, 18, 21],
 'q2': [12, 14, 15, 17, 19, 20, 22, 25, 27, 30, 36],
 'q3': [1, 2, 4, 4, 6, 7, 9, 10, 12, 15, 19],
 'q4': [20, 24, 26, 28, 30, 33, 35, 38, 40, 44, 50],
 'q5': [2, 3, 3, 5, 6, 8, 10, 11, 13, 16, 20],
 'q6': [45, 50, 52, 55, 58, 60, 63, 66, 70, 74, 80],
 'q7': [5, 7, 8, 10, 12, 13, 15, 17, 19, 22, 26],
 'q8': [100, 110, 115, 120, 128, 135, 140, 150, 160, 175, 200],
 'q9': [4, 6, 7, 9, 10, 12, 13, 15, 17, 19, 23],
 'q10': [30, 33, 35, 38, 41, 44, 47, 50, 54, 58, 65],
 'q14': [8, 9, 9, 10, 10, 11, 14, 17, 20, 24, 30],      # median taet paa Q1
 'q15': [6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 40],       # lang arm til hoejre
 'q17': [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24],
 'q20': [11, 13, 14, 16, 18, 19, 21, 23, 26, 29, 33],
}
for _n, _d in SAET.items():
    assert len(_d) == 11, _n
    assert all(F(v).denominator == 1 for v in fem(_d)), f'{_n} giver halve tal'

# Par til sammenligningsspoergsmaalene
PAR = {
 'q11': ([14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 36],
         [20, 22, 25, 27, 29, 31, 33, 35, 38, 40, 44]),
 'q12': ([10, 12, 14, 18, 22, 26, 30, 34, 38, 42, 46],
         [10, 20, 24, 26, 27, 28, 29, 30, 32, 36, 46]),
 'q13': ([25, 27, 28, 30, 31, 33, 34, 36, 37, 39, 41],
         [10, 15, 20, 26, 31, 36, 41, 46, 50, 55, 60]),
 'q19': ([20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40],
         [4, 10, 16, 22, 27, 30, 33, 38, 44, 50, 56]),
}
P5 = {k: (fem(a), fem(b)) for k, (a, b) in PAR.items()}

# Spoergsmaal 16: kun ÉN af de tre raekker maa passe til figuren.
R16_RIGTIG = [2, 4, 5, 7, 9, 12, 14, 15, 18, 20, 24]
R16_FORKERT = [[2, 3, 4, 5, 9, 12, 14, 15, 18, 20, 24],
               [2, 4, 5, 7, 9, 12, 16, 19, 22, 23, 24]]
F16 = fem(R16_RIGTIG)
for _r in R16_FORKERT:
    assert fem(_r) != F16, 'to af raekkerne i spm. 16 giver samme boksplot'
    assert min(_r) == min(R16_RIGTIG) and max(_r) == max(R16_RIGTIG), \
        'de forkerte raekker skal have samme yderpunkter, ellers er det for let'


def bp(nav, titel='', **kw):
    return FG.boksplot(*fem(SAET[nav]), titel=titel, **kw)


def bpp(nav, navne, titel=''):
    a, b = P5[nav]
    return FG.boksplot_par(a, b, navne, titel)


# ------------------------------------------------------------- spoergsmaal
# (figur, spoergsmaal, niveau, rigtigt svar, to forkerte, forklaring)
def _v(nav, i):
    return dk(fem(SAET[nav])[i])


SPM_A = [
 (bp('q1', 'Point i en test'), 'Hvad er <b>medianen</b>?', 'Let',
  _v('q1', 2), [_v('q1', 1), _v('q1', 3)],
  'Medianen er den røde streg inde i kassen. Den deler tallene i to lige store halvdele.'),
 (bp('q2', 'Antal beskeder på en dag'), 'Hvad er <b>mindsteværdien</b>?', 'Let',
  _v('q2', 0), [_v('q2', 1), _v('q2', 2)],
  'Mindsteværdien er enden af den venstre arm — det mindste tal i hele datasættet.'),
 (bp('q3', 'Antal bøger læst på et år'), 'Hvad er <b>størsteværdien</b>?', 'Let',
  _v('q3', 4), [_v('q3', 3), _v('q3', 2)],
  'Størsteværdien er enden af den højre arm.'),
 (bp('q4', 'Temperatur om eftermiddagen'), 'Hvad er <b>første kvartil (Q1)</b>?',
  'Middel', _v('q4', 1), [_v('q4', 0), _v('q4', 2)],
  'Q1 er kassens venstre kant. En fjerdedel af tallene ligger under den.'),
 (bp('q5', 'Antal mål i en sæson'), 'Hvad er <b>tredje kvartil (Q3)</b>?',
  'Middel', _v('q5', 3), [_v('q5', 2), _v('q5', 4)],
  'Q3 er kassens højre kant. Tre fjerdedele af tallene ligger under den.'),
 (bp('q6', 'Puls efter en gåtur'), 'Hvad er <b>variationsbredden</b>?', 'Middel',
  dk(fem(SAET['q6'])[4] - fem(SAET['q6'])[0]),
  [dk(fem(SAET['q6'])[3] - fem(SAET['q6'])[1]), _v('q6', 4)],
  'Variationsbredden er største minus mindste værdi — hele armspændet fra ende til ende.'),
 (bp('q7', 'Minutter i bad'), 'Hvad er <b>kvartilbredden</b>?', 'Middel',
  dk(fem(SAET['q7'])[3] - fem(SAET['q7'])[1]),
  [dk(fem(SAET['q7'])[4] - fem(SAET['q7'])[0]), _v('q7', 2)],
  'Kvartilbredden er Q3 minus Q1 — altså hvor bred selve kassen er.'),
 (bp('q8', 'Kroner brugt på en uge'),
  'Hvor stor en del af tallene ligger <b>inde i kassen</b>?', 'Middel',
  '50 %', ['25 %', '75 %'],
  'Kassen går fra Q1 til Q3, og det er netop de midterste 50 % af tallene.'),
 (bp('q9', 'Antal timer søvn'),
  'Hvor stor en del af tallene ligger <b>over medianen</b>?', 'Let',
  'Halvdelen', ['En fjerdedel', 'Tre fjerdedele'],
  'Medianen deler tallene midt over. Halvdelen ligger under, halvdelen over.'),
 (bp('q10', 'Antal sider i en opgave'),
  'Hvilket interval rummer de <b>midterste 50 %</b>?', 'Middel',
  f'Fra {_v("q10", 1)} til {_v("q10", 3)}',
  [f'Fra {_v("q10", 0)} til {_v("q10", 4)}',
   f'Fra {_v("q10", 2)} til {_v("q10", 4)}'],
  'De midterste 50 % er netop kassen, altså fra Q1 til Q3.'),
]

_a11, _b11 = P5['q11']
_a12, _b12 = P5['q12']
_a13, _b13 = P5['q13']
_a19, _b19 = P5['q19']
assert _b11[2] > _a11[2]
assert (_b12[3] - _b12[1]) < (_a12[3] - _a12[1])
assert (_b13[4] - _b13[0]) > (_a13[4] - _a13[0])
assert _a19[2] == _b19[2], 'spm. 19 kræver samme median i de to boksplot'
assert (_b19[3] - _b19[1]) > (_a19[3] - _a19[1])
_f14 = fem(SAET['q14'])
assert _f14[2] - _f14[1] < _f14[3] - _f14[2], 'medianen ligger ikke tæt på Q1'
_f15 = fem(SAET['q15'])
assert _f15[4] - _f15[3] > _f15[1] - _f15[0], 'den højre arm er ikke længst'
_f17 = fem(SAET['q17'])
_f17_ny = fem(SAET['q17'][:-1] + [SAET['q17'][-1] * 2])
assert _f17_ny[2] == _f17[2], 'medianen flyttede sig, da den største blev fordoblet'
assert _f17_ny[4] - _f17_ny[0] > _f17[4] - _f17[0]

SPM_B = [
 (bpp('q11', ('8.A', '8.B'), 'Minutter på lektier'),
  'Hvilken klasse har den <b>højeste median</b>?', 'Let',
  '8.B', ['8.A', 'De har samme median'],
  f'Den røde streg ligger længst til højre i 8.B: {dk(_b11[2])} mod {dk(_a11[2])}.'),
 (bpp('q12', ('Hold 1', 'Hold 2'), 'Antal point'),
  'Hvor ligger de midterste 50 % <b>tættest samlet</b>?', 'Middel',
  'Hold 2', ['Hold 1', 'Lige tæt'],
  f'Kassen er smallest hos Hold 2: kvartilbredden er {dk(_b12[3]-_b12[1])} '
  f'mod {dk(_a12[3]-_a12[1])}.'),
 (bpp('q13', ('Mandag', 'Fredag'), 'Antal kunder i timen'),
  'Hvilken dag har den <b>største variationsbredde</b>?', 'Middel',
  'Fredag', ['Mandag', 'Den er ens'],
  f'Fra ende til ende er fredag bredest: {dk(_b13[4]-_b13[0])} mod '
  f'{dk(_a13[4]-_a13[0])}.'),
 (bp('q14', 'Antal træninger om måneden'),
  'Medianen ligger tæt på kassens venstre kant. Hvad betyder det?', 'Svær',
  'De laveste tal ligger tæt sammen',
  ['Der er flest høje tal', 'Halvdelen af tallene er ens'],
  'Når medianen ligger tæt på Q1, er den nederste fjerdedel af kassen smal: '
  'de tal ligger tæt. Den øverste del af kassen er bredere, så dér er der mere spredning.'),
 (bp('q15', 'Minutter i kø'),
  'Den højre arm er meget lang. Hvad fortæller det?', 'Svær',
  'De højeste tal ligger spredt',
  ['Der er mange høje tal', 'Medianen er høj'],
  'En lang arm viser afstand, ikke antal. Her er der mindst én meget høj værdi, '
  'men boksplottet siger ikke hvor mange.'),
 (FG.boksplot(*F16, titel='Hvilken talrække er tegnet her?'),
  'Hvilken af de tre talrækker passer til boksplottet?', 'Svær',
  ', '.join(map(str, R16_RIGTIG)),
  [', '.join(map(str, r)) for r in R16_FORKERT],
  f'Kun den ene række giver min {dk(F16[0])}, Q1 {dk(F16[1])}, median '
  f'{dk(F16[2])}, Q3 {dk(F16[3])} og maks {dk(F16[4])}. De to andre har de '
  f'samme yderpunkter, men kassen falder et andet sted.'),
 (bp('q17', 'Antal opgaver løst'),
  'Den <b>største</b> værdi fordobles. Hvad sker der med <b>medianen</b>?',
  'Svær', 'Den er uændret', ['Den vokser', 'Den bliver dobbelt så stor'],
  'Medianen er det midterste tal. Ét tal i toppen kan blive så stort det vil — '
  'det midterste bliver stående.'),
 (bp('q17', 'Samme data som før'),
  'Og hvad sker der med <b>variationsbredden</b>?', 'Middel',
  'Den vokser', ['Den er uændret', 'Den bliver mindre'],
  f'Variationsbredden er største minus mindste. Den går fra '
  f'{dk(_f17[4]-_f17[0])} til {dk(_f17_ny[4]-_f17_ny[0])}.'),
 (bpp('q19', ('7.A', '7.B'), 'Antal rigtige i en prøve'),
  'De to har samme median. Hvad kan du så sige?', 'Svær',
  'Tallene i 7.B er mere spredt',
  ['Klasserne har klaret sig ens', '7.A har de bedste resultater'],
  'Samme median betyder kun, at midten ligger samme sted. Kassen og armene er '
  'bredere i 7.B, så dér er der længere mellem tallene.'),
 (bp('q20', 'Antal skridt i tusinder'),
  'Hvor stor en del af tallene ligger <b>under Q3</b>?', 'Middel',
  'Tre fjerdedele', ['Halvdelen', 'En fjerdedel'],
  'Q3 er tredje kvartil. Tre fjerdedele af tallene ligger under den, og den '
  'sidste fjerdedel ligger over.'),
]

# Rigtigt svar skal ikke altid staa samme sted. Raekkefoelgen er fast, saa
# to bygninger af siden giver den samme fil.
ORDEN = [0, 2, 1, 1, 0, 2, 1, 0, 2, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2]


def byg_spm(liste, start, orden):
    ud = []
    for k, (fig, tekst, niveau, rigtig, forkerte, forklaring) in enumerate(liste):
        plads = orden[start + k - 1]
        valg = list(forkerte)
        valg.insert(plads, rigtig)
        assert len(set(valg)) == 3, f'spørgsmål {start+k} har ens svarmuligheder'
        assert valg[plads] == rigtig
        assert '"' not in forklaring and '"' not in tekst
        knapper = ' '.join(
            f'<button class="opt"><span class="mk">{"ABC"[j]}</span> '
            f'{html.escape(v, quote=False)}</button>' for j, v in enumerate(valg))
        ud.append(
            f'<div class="q" data-answer="{plads}" data-exp="{forklaring}">'
            f'<div class="qtext"><span class="qn">{start+k}.</span> {tekst} '
            f'<span class="lvl">{niveau}</span></div>'
            f'<div class="qfig">{fig}</div>'
            f'<div class="opts">{knapper}</div><div class="fb"></div></div>')
    return ''.join(ud)


def quiz(nr, tag, titel, undertitel, krop, antal, slut=None):
    besked = ('<span id="finalMsg"></span>' if slut is None
              else f'<span>{slut}</span>')
    return (f'<section class="quiz" data-quiz id="quiz{nr}">'
            f'<div class="qhead"><span class="qtag">{tag}</span>'
            f'<h3>{titel}</h3></div><p class="qsub">{undertitel}</p>{krop}'
            f'<div class="scorebar"><span class="badge" data-score>'
            f'0 / {antal} rigtige</span> {besked}</div>'
            f'</section>')


# ------------------------------------------------------------------- siden
def _raekke_html(xs, mark):
    """Talraekken med de fem tal markeret, saa snittene kan ses.

    Klasserne maa IKKE hedde q eller m: quizmotoren taeller hvert element
    med klassen `q` som et spoergsmaal, og saa talte den markeringerne med."""
    ud = []
    for i, v in enumerate(xs):
        k = mark.get(i, '')
        ud.append(f'<span class="tal{" " + k if k else ""}">{v}</span>')
    return '<p class="talraekke">' + ''.join(ud) + '</p>'


FORKLARING = (
 '<section class="lesson" id="hvad"><h2><span class="num">1</span> '
 'Hvad et boksplot er</h2>'
 '<p class="sub">Et boksplot er <b>fem tal tegnet</b>. Ikke mere end det. '
 'Kan du de fem tal, kan du læse ethvert boksplot — og tegne dit eget.</p>'
 '<div class="box rule"><span class="rlabel">De fem tal</span><br>'
 '<b>Mindsteværdien</b> — enden af den venstre arm.<br>'
 '<b>Q1 (første kvartil)</b> — kassens venstre kant. En fjerdedel af tallene '
 'ligger under.<br>'
 '<b>Medianen</b> — stregen inde i kassen. Halvdelen ligger under, halvdelen over.<br>'
 '<b>Q3 (tredje kvartil)</b> — kassens højre kant. Tre fjerdedele ligger under.<br>'
 '<b>Størsteværdien</b> — enden af den højre arm.</div>'
 f'<div class="figur">{FG.boksplot(*L5, titel="Minutter brugt på lektier · 15 unger")}'
 '<div class="figtekst">Sådan ser de fem tal ud, når de er tegnet. '
 'Læg mærke til, at der ikke står noget om <i>hvor mange</i> der er.</div></div>'

 '<h3>Hvad de enkelte dele betyder</h3>'
 '<div class="box"><b>Kassen er de midterste 50 %.</b> Den går fra Q1 til Q3. '
 'Halvdelen af alle tallene ligger inde i kassen, uanset hvor bred den er.<br>'
 '<b>Hver arm er cirka 25 %.</b> En fjerdedel af tallene ligger ude i den '
 'venstre arm, en fjerdedel i den højre.<br>'
 '<b>En lang arm betyder afstand — ikke antal.</b> Her går den højre arm fra '
 f'{dk(L5[3])} helt op til {dk(L5[4])}, fordi én enkelt ung brugte '
 f'{dk(L5[4])} minutter. Der er ikke <i>flere</i> deroppe; der er '
 '<i>længere</i> imellem dem.</div>'

 '<h3>To mål for spredning</h3>'
 '<div class="box rule"><span class="rlabel">Regneregel</span><br>'
 f'<b>Variationsbredde</b> = største − mindste = {dk(L5[4])} − {dk(L5[0])} = '
 f'<b>{dk(VARIATION)}</b>. Hele armspændet.<br>'
 f'<b>Kvartilbredde</b> = Q3 − Q1 = {dk(L5[3])} − {dk(L5[1])} = '
 f'<b>{dk(KVARTILBREDDE)}</b>. Kun kassen.<br>'
 'Kvartilbredden er den sejeste af de to, fordi den ikke lader sig rive med '
 'af én enkelt yderlig værdi.</div></section>'

 '<section class="lesson" id="find"><h2><span class="num">2</span> '
 'Sådan finder du de fem tal</h2>'
 '<p class="sub">Der er tre skridt, og det første er det, flest glemmer.</p>'
 '<div class="box rule"><span class="rlabel">Fremgangsmåde</span><br>'
 '<b>1.</b> <b>Sortér tallene</b> fra mindst til størst. Uden det passer '
 'ingenting.<br>'
 '<b>2.</b> Find <b>medianen</b>: det midterste tal. Er der et lige antal, '
 'er det gennemsnittet af de to midterste.<br>'
 '<b>3.</b> Find <b>Q1</b> som medianen af den nederste halvdel og <b>Q3</b> '
 'som medianen af den øverste. Er antallet ulige, regnes det midterste tal '
 '<i>ikke</i> med i nogen af halvdelene.</div>'
 '<p>De 15 tal fra før, sorteret. Medianen er det ottende tal, og halvdelene '
 'har syv tal hver:</p>'
 + _raekke_html(LEKTIER, {3: 'kv', 7: 'md', 11: 'kv'}) +
 f'<p>Nederste halvdel er de syv første, og dens midterste tal er '
 f'<b>{dk(L5[1])}</b> — det er Q1. Øverste halvdel er de syv sidste, og dens '
 f'midterste tal er <b>{dk(L5[3])}</b> — det er Q3. Medianen er '
 f'<b>{dk(L5[2])}</b>.</p>'
 '<div class="box"><b>Fælden:</b> husk at sortere, og husk at det midterste '
 'tal ikke tæller med i halvdelene. Begge fejl flytter kassen, og så passer '
 'tegningen ikke med tallene.</div></section>'

 '<section class="lesson" id="sammenlign"><h2><span class="num">3</span> '
 'To boksplot ved siden af hinanden</h2>'
 '<p class="sub">Det er her boksplottet for alvor er værd at bruge: to '
 'grupper, én figur, og forskellen kan ses med det samme.</p>'
 f'<div class="figur">{bpp("q11", ("8.A", "8.B"), "Minutter på lektier")}'
 '<div class="figtekst">Samme akse for begge — ellers kan de ikke '
 'sammenlignes. 8.B har den højeste median, og 8.A har den bredeste kasse.'
 '</div></div>'
 '<div class="box"><b>Kig efter tre ting:</b><br>'
 '<b>1.</b> Hvor ligger den røde streg? Det er midten.<br>'
 '<b>2.</b> Hvor bred er kassen? Det er spredningen i midten.<br>'
 '<b>3.</b> Hvor lange er armene? Det er, hvor langt der er ud til yderne.'
 '</div>'
 '<div class="box"><b>Og husk, hvad et boksplot <i>ikke</i> viser:</b> '
 'antallet af observationer, hvor mange der ligger på hvert enkelt tal, og '
 'om tallene klumper sig sammen inde i kassen. To vidt forskellige datasæt '
 'kan give præcis det samme boksplot.</div></section>')


def byg():
    s = open(SKABELON, encoding='utf-8').read()
    hoved = s[:s.index('<section class="lesson" id="beskriv">')]
    hale = s[s.index('<section class="lesson" id="results">'):]

    hoved = hoved.replace('<title>Statistik og sandsynlighed - 9. klasse</title>',
                          '<title>Boksplot - 9. klasse</title>')
    hoved = hoved.replace('321flyv · <span>Statistik</span>',
                          '321flyv · <span>Boksplot</span>')
    i = hoved.index('<nav class="jump">')
    j = hoved.index('</nav>', i)
    hoved = (hoved[:i] + '<nav class="jump"><a href="#hvad">Hvad det er</a> '
             '<a href="#find">Find de fem tal</a> '
             '<a href="#sammenlign">Sammenlign</a> '
             '<a href="#quiz1">Aflæs</a> <a href="#quiz2">Forstå</a> '
             '<a href="#results">Resultater</a> '
             '<a class="side" href="matematik.html">Matematik</a> '
             '<a class="side" href="index.html">Forside</a>' + hoved[j:])
    i = hoved.index('<section class="hero"')
    j = hoved.index('<button class="printbtn"', i)
    hoved = (hoved[:i] + '<section class="hero" id="intro">'
             '<span class="pill">9. klasse · statistik</span>'
             '<h1>Boksplot</h1><p>Et boksplot er fem tal tegnet. Siden her '
             'gennemgår hvilke fem, hvordan du finder dem, og hvad kassen og '
             'armene betyder — og bagefter er der <b>20 spørgsmål med en '
             'figur til hvert</b>. Svar og forklaring kommer med det samme.</p>'
             + hoved[j:])

    krop = (FORKLARING
            + quiz(1, 'Quiz · aflæsning', 'Aflæs boksplottet',
                   'Ti spørgsmål. Tallene står på figuren — opgaven er at '
                   'vide, hvilket af dem der er svaret.',
                   byg_spm(SPM_A, 1, ORDEN), len(SPM_A),
                   slut='Videre til de sværere: forstå og sammenlign.')
            + quiz(2, 'Quiz · forståelse', 'Forstå og sammenlign',
                   'Ti spørgsmål, hvor tegningen skal tolkes. Her kan du '
                   'ikke bare aflæse et tal.',
                   byg_spm(SPM_B, 11, ORDEN), len(SPM_B)))

    hale = hale.replace("var STORAGE_KEY = 'stat9_state_v1';",
                        "var STORAGE_KEY = 'boks9_state_v1';")
    hale = re.sub(r"var moduleNames = \[.*?\];",
                  "var moduleNames = ['Aflæs boksplottet','Forstå og sammenlign'];",
                  hale, count=1, flags=re.S)
    hale = hale.replace('Undervisningsmateriale til matematik i 9. klasse · '
                        'Statistik og sandsynlighed.',
                        'Undervisningsmateriale til matematik i 9. klasse · Boksplot.')

    ekstra = ('\n.qfig{margin:10px 0 12px}\n'
              '.qfig svg{width:100%;max-width:460px;height:auto;display:block}\n'
              '.talraekke{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0}\n'
              '.talraekke .tal{display:inline-flex;align-items:center;'
              'justify-content:center;min-width:38px;padding:5px 8px;'
              'border:1px solid var(--line);border-radius:8px;'
              'background:var(--panel2);font-variant-numeric:tabular-nums}\n'
              '.talraekke .tal.md{background:#fdeaec;border-color:#c23b4b;'
              'color:#c23b4b;font-weight:700}\n'
              '.talraekke .tal.kv{background:#eaf2fd;border-color:#1f6fd6;'
              'color:#1f6fd6;font-weight:700}\n')
    hoved = hoved.replace('</style></head>', ekstra + '</style></head>', 1)
    return hoved + '<main-placeholder>' + krop + hale


if __name__ == '__main__':
    doc = byg().replace('<main-placeholder>', '')
    open(UD, 'w', encoding='utf-8').write(doc)
    n = doc.count('<div class="q" ')
    figurer = doc.count('<svg')
    quizzer = doc.count('class="quiz"')
    print(f'skrevet:  boksplot.html  ·  {n} spørgsmål, {figurer} figurer, '
          f'{quizzer} quizzer')
