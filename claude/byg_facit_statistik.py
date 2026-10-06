# -*- coding: utf-8 -*-
"""Bygger facitlisterne til Statistik, Manipulation og Sandsynlighed.

Elleve facitlister: syv til modulopgaverne paa klassens sider og fire til
lektierne i uge 33 til 36. Indholdet er kode, figurerne kommer fra
figurer.py, og hvert tal regnes efter med broekregning, foer filen skrives.
Skabelonen ligger i facit.py.

    python3 claude/byg_facit_statistik.py             bygger alle elleve
    python3 claude/byg_facit_statistik.py sumkurve    bygger dem med ordet i navnet

Kvartiler regnes efter dansk skolemetode: median af hver halvdel, og ved
ulige antal udelades den midterste observation.
"""
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figurer as FG
from facit import byg, dk, dok


# ---------------------------------------------------------------------------
# Statistik regnet efter - aldrig aflaest
# ---------------------------------------------------------------------------
def femtal(xs):
    """Mindste, Q1, median, Q3, stoerste efter dansk skolemetode."""
    v = sorted(xs)
    n = len(v)

    def med(w):
        m = len(w)
        return F(w[m // 2]) if m % 2 else (F(w[m // 2 - 1]) + F(w[m // 2])) / 2

    halv = n // 2
    lav, hoej = v[:halv], v[halv + (n % 2):]
    return F(v[0]), med(lav), med(v), med(hoej), F(v[-1])


def gennemsnit(xs):
    return F(sum(xs), len(xs))


def typetal(xs):
    t = {}
    for x in xs:
        t[x] = t.get(x, 0) + 1
    flest = max(t.values())
    kandidater = [x for x, n in t.items() if n == flest]
    assert len(kandidater) == 1, f'der er {len(kandidater)} typetal: {kandidater}'
    return kandidater[0]


def frekvenser(dele):
    """[(navn, antal)] -> [(navn, antal, frekvens i %, grader)] med eksakt sum."""
    n = sum(a for _, a in dele)
    ud = [(navn, a, F(a * 100, n), F(a * 360, n)) for navn, a in dele]
    assert sum(r[2] for r in ud) == 100, 'frekvenserne giver ikke 100 %'
    assert sum(r[3] for r in ud) == 360, 'graderne giver ikke 360°'
    return ud, n


def kumuleret(hyp):
    """Hyppigheder -> [(kumuleret hyppighed, kumuleret frekvens i %)]."""
    n, loeb, ud = sum(hyp), 0, []
    for h in hyp:
        loeb += h
        ud.append((loeb, F(loeb * 100, n)))
    assert ud[-1][0] == n and ud[-1][1] == 100
    return ud, n


def intervaller(graenser):
    """[0, 100, 200] -> [(0, 100), (100, 200)] - formatet sumkurve() vil have."""
    return [(graenser[i], graenser[i + 1]) for i in range(len(graenser) - 1)]


def aflaes(graenser, hyp, pct):
    """Lineaer interpolation i sumkurven - samme som ungen gaar paa papiret."""
    kum, n = kumuleret(hyp)
    maal = F(pct)
    foer_x, foer_y = F(graenser[0]), F(0)
    for i, (_, f) in enumerate(kum):
        x = F(graenser[i + 1])
        if f >= maal:
            return foer_x + (maal - foer_y) / (f - foer_y) * (x - foer_x)
        foer_x, foer_y = x, f
    raise AssertionError(f'{pct} % ligger uden for kurven')


def pct(t, n):
    return F(t * 100, n)


def tal(x, decimaler=2):
    """Dansk tal med komma og hoejst to decimaler, uden nuller i halen."""
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator).replace('-', '−')
    s = f'{float(x):.{decimaler}f}'.rstrip('0').rstrip('.')
    return s.replace('.', ',').replace('-', '−')


# ---------------------------------------------------------------------------
# Statistik, modul 1 · Opgave A - Beskriv talraekken
# ---------------------------------------------------------------------------
A_KORT = [3, 5, 5, 6, 8, 9, 13]
A_LANG = [2, 4, 5, 5, 6, 7, 8, 9, 10, 12, 14]
a_mi, a_q1, a_med, a_q3, a_ma = femtal(A_KORT)
l_mi, l_q1, l_med, l_q3, l_ma = femtal(A_LANG)
assert (a_mi, a_q1, a_med, a_q3, a_ma) == (3, 5, 6, 9, 13)
assert (l_mi, l_q1, l_med, l_q3, l_ma) == (2, 5, 7, 10, 14)
assert gennemsnit(A_KORT) == 7 and typetal(A_KORT) == 5

dok('facit-online-2026-08-10-beskriv-data', 'online', '2026-08-10', 'Beskriv data',
    'Statistik, modul 1 · Opgave A på klassens statistikside', [
    ('h2', 'Opgave A · Beskriv talrækken'),
    ('p', 'Talrækken <code>3, 5, 5, 6, 8, 9, 13</code> — antal mål i syv '
          'håndboldkampe.'),
    ('tabel', [
        ('a) Gennemsnit', '7', '49 ÷ 7 = 7'),
        ('b) Median', '6', '4. observation af 7'),
        ('b) Typetal', '5', '5 optræder to gange'),
        ('c) Variationsbredde', '10', '13 − 3 = 10'),
        ('d) Nedre kvartil Q1', '5', 'median af 3, 5, 5'),
        ('d) Øvre kvartil Q3', '9', 'median af 8, 9, 13'),
        ('d) Kvartilbredde', '4', '9 − 5 = 4'),
        ('e) Boksplot', '3 · 5 · 6 · 9 · 13', 'mindste, Q1, median, Q3, største'),
    ]),
    ('figur', (FG.boksplot(a_mi, a_q1, a_med, a_q3, a_ma,
                           'Talrækken 3, 5, 5, 6, 8, 9, 13'),
               'Sådan ser det færdige boksplot ud. Kassen går fra Q1 til Q3, den '
               'røde streg er medianen, og whiskers når ud til mindste og største '
               'værdi.')),
    ('h3', 'f) Den længere talrække'),
    ('p', '<code>2, 4, 5, 5, 6, 7, 8, 9, 10, 12, 14</code> — 11 observationer.'),
    ('tabel', [
        ('Mindste', '2', ''),
        ('Q1', '5', 'median af 2, 4, 5, 5, 6'),
        ('Median', '7', '6. observation af 11'),
        ('Q3', '10', 'median af 8, 9, 10, 12, 14'),
        ('Største', '14', ''),
        ('Kvartilbredde', '5', '10 − 5 = 5'),
    ]),
    ('figur', (FG.boksplot(l_mi, l_q1, l_med, l_q3, l_ma,
                           'Talrækken med 11 observationer'),
               'De fem tal aflæses direkte: 2 · 5 · 7 · 10 · 14.')),
    ('note', ['<b>Vær opmærksom:</b> ved ulige antal observationer udelades '
              'midterste tal, når kvartilerne findes. Regner ungen medianen med i '
              'halvdelene, får hen Q1 = 5 og Q3 = 9 i den lange række — et hyppigt '
              'og forståeligt slip, som er værd at tage fælles.']),
])

# ---------------------------------------------------------------------------
# Uge 33 · lektier - Beskriv data
# ---------------------------------------------------------------------------
U33A = [4, 6, 6, 8, 9, 11, 12]
U33B = [2, 3, 5, 6, 8, 9, 10, 12, 13, 15, 18]
p_mi, p_q1, p_med, p_q3, p_ma = femtal(U33A)
q_mi, q_q1, q_med, q_q3, q_ma = femtal(U33B)
assert (p_mi, p_q1, p_med, p_q3, p_ma) == (4, 6, 8, 11, 12)
assert (q_mi, q_q1, q_med, q_q3, q_ma) == (2, 5, 9, 13, 18)
assert gennemsnit(U33A) == 8 and typetal(U33A) == 6
assert p_q3 - p_q1 == 5 and q_q3 - q_q1 == 8
assert sum(1 for x in U33B if q_q1 <= x <= q_q3) == 7

dok('facit-lektier-2026-08-10-beskriv-data', 'lektier', '2026-08-10', 'Beskriv data',
    'Uge 33 · lektier-uge33-beskriv-data.html', [
    ('h2', 'Opgave A · 4, 6, 6, 8, 9, 11, 12'),
    ('tabel', [
        ('a) Gennemsnit', '8', '56 ÷ 7 = 8'),
        ('b) Median', '8', '4. observation af 7'),
        ('b) Typetal', '6', '6 optræder to gange'),
        ('c) Variationsbredde', '8', '12 − 4 = 8'),
        ('d) Q1', '6', 'median af 4, 6, 6'),
        ('d) Q3', '11', 'median af 9, 11, 12'),
        ('d) Kvartilbredde', '5', '11 − 6 = 5'),
        ('e) Boksplot', '4 · 6 · 8 · 11 · 12', 'mindste, Q1, median, Q3, største'),
    ]),
    ('figur', (FG.boksplot(p_mi, p_q1, p_med, p_q3, p_ma,
                           'Talrækken 4, 6, 6, 8, 9, 11, 12'),
               'Det færdige boksplot.')),
    ('h2', 'Opgave B · 2, 3, 5, 6, 8, 9, 10, 12, 13, 15, 18'),
    ('tabel', [
        ('a) Mindste og største', '2 og 18', ''),
        ('b) Median', '9', '6. observation af 11'),
        ('c) Q1', '5', 'median af 2, 3, 5, 6, 8'),
        ('c) Q3', '13', 'median af 10, 12, 13, 15, 18'),
        ('d) Boksplot', '2 · 5 · 9 · 13 · 18', ''),
        ('e) Kvartilbredde', '8', '13 − 5 = 8'),
        ('f) Andel i kassen', 'ca. 50 %', 'kassen går fra Q1 til Q3'),
    ]),
    ('figur', (FG.boksplot(q_mi, q_q1, q_med, q_q3, q_ma,
                           'Talrækken med 11 observationer'),
               'De fem tal: 2 · 5 · 9 · 13 · 18. Kassen dækker den midterste '
               'halvdel.')),
    ('note', ['Til f): kassen dækker per definition den midterste halvdel. I denne '
              'række ligger 5, 6, 8, 9, 10, 12, 13 — syv af elleve — inde i eller på '
              'kassen. At det ikke bliver præcis 5,5 skyldes, at Q1 og Q3 selv er '
              'observationer i en kort talrække. Pointen er definitionen, ikke den '
              'præcise optælling.',
              '<b>Vær opmærksom:</b> ved ulige antal observationer udelades midterste '
              'tal, når kvartilerne findes. Regnes medianen med, får ungen Q1 = 5,5 '
              'og Q3 = 12,5 — et forståeligt slip, som er værd at tage fælles.']),
])


# ---------------------------------------------------------------------------
# Statistik, modul 2 · Opgave B - Frekvens og sumkurve
# ---------------------------------------------------------------------------
SPORT = [('Fodbold', 8), ('Håndbold', 5), ('Svømning', 4), ('Andet', 3)]
sport, n_sport = frekvenser(SPORT)
assert n_sport == 20 and [r[2] for r in sport] == [40, 25, 20, 15]
assert [r[3] for r in sport] == [144, 90, 72, 54]
assert typetal([k for k, a in SPORT for _ in range(a)]) == 'Fodbold'

LOMME_GR = [0, 100, 200, 300, 400, 500]
LOMME_H = [4, 10, 14, 8, 4]
lomme_kum, n_lomme = kumuleret(LOMME_H)
assert n_lomme == 40
assert [h for h, _ in lomme_kum] == [4, 14, 28, 36, 40]
assert [f for _, f in lomme_kum] == [10, 35, 70, 90, 100]
l_q1 = aflaes(LOMME_GR, LOMME_H, 25)
l_md = aflaes(LOMME_GR, LOMME_H, 50)
l_q3 = aflaes(LOMME_GR, LOMME_H, 75)
assert (l_q1, l_q3) == (160, 325) and tal(l_md) == '242,86'

dok('facit-online-2026-08-17-diagrammer-og-sumkurve', 'online', '2026-08-17',
    'Diagrammer og sumkurve',
    'Statistik, modul 2 · Opgave B på klassens statistikside', [
    ('h2', 'Opgave B · Frekvens og sumkurve'),
    ('h3', 'a-d) Yndlingssport, 20 unger'),
    ('kolonner', (['Sportsgren', 'Hyppighed', 'Frekvens', 'Grader i cirkeldiagram'],
                  [[navn, str(a), f'{tal(f)} %', f'{tal(g)}°'] for navn, a, f, g in sport]
                  + [['I alt', str(n_sport), '100 %', '360°']])),
    ('figur', (FG.cirkeldiagram(SPORT),
               'Det færdige cirkeldiagram. Graderne summer til præcis 360°.')),
    ('note', ['b) Typetallet er <b>Fodbold</b>. d) Kontrollen er, at frekvenserne '
              'giver præcis 100 % og graderne præcis 360°. Gør de ikke det, er der '
              'en regnefejl.',
              'Til d) om sammenligning med en klasse på 25: antal kan ikke '
              'sammenlignes direkte, når grupperne har forskellig størrelse — der '
              'skal sammenlignes frekvenser. Et grupperet søjlediagram med procent '
              'på y-aksen er det bedste valg. To cirkeldiagrammer kan bruges, men '
              'er sværere at sammenligne præcist.']),
    ('h3', 'e-g) Lommepenge, 40 unger'),
    ('kolonner', (['Lommepenge (kr)', 'Hyppighed', 'Kumuleret hyppighed',
                   'Kumuleret frekvens'],
                  [[f'{LOMME_GR[i]}–{LOMME_GR[i+1]}', str(LOMME_H[i]),
                    str(lomme_kum[i][0]), f'{tal(lomme_kum[i][1])} %']
                   for i in range(len(LOMME_H))])),
    ('p', 'f) Aflæsninger på sumkurven:'),
    ('tabel', [
        ('Nedre kvartil, 25 %', f'{tal(l_q1)} kr', 'Ligger i intervallet 100–200'),
        ('Median, 50 %', f'ca. {tal(l_md, 0)} kr', 'Ligger i intervallet 200–300'),
        ('Øvre kvartil, 75 %', f'{tal(l_q3)} kr', 'Ligger i intervallet 300–400'),
    ]),
    ('figur', (FG.sumkurve(intervaller(LOMME_GR), LOMME_H, (25, 50, 75), 'kroner om måneden')[0],
               'Sumkurven med de tre aflæsninger. Man går vandret ind fra 25 %, '
               '50 % og 75 % til kurven og derefter lodret ned.')),
    ('note', ['Præcis median: 242,86 kr. Ungerne aflæser på egen tegning, så alt '
              'mellem ca. 235 og 250 bør godkendes — det samme gælder de to '
              'kvartiler med en snes kroners spillerum.',
              'g) <b>70 %</b> får under 300 kr om måneden. Læses direkte som den '
              'kumulerede frekvens ved 300.']),
])

# ---------------------------------------------------------------------------
# Uge 34 · lektier - Diagrammer og sumkurve
# ---------------------------------------------------------------------------
TRANSPORT = [('Cykel', 10), ('Gang', 6), ('Bus', 7), ('Bil', 2)]
transport, n_tr = frekvenser(TRANSPORT)
assert n_tr == 25 and [r[2] for r in transport] == [40, 24, 28, 8]
assert [tal(r[3]) for r in transport] == ['144', '86,4', '100,8', '28,8']

LEKTIE_GR = [0, 30, 60, 90, 120, 150]
LEKTIE_H = [6, 11, 16, 12, 5]
lektie_kum, n_lek = kumuleret(LEKTIE_H)
assert n_lek == 50
assert [h for h, _ in lektie_kum] == [6, 17, 33, 45, 50]
assert [f for _, f in lektie_kum] == [12, 34, 66, 90, 100]
t_q1 = aflaes(LEKTIE_GR, LEKTIE_H, 25)
t_md = aflaes(LEKTIE_GR, LEKTIE_H, 50)
t_q3 = aflaes(LEKTIE_GR, LEKTIE_H, 75)
assert tal(t_q1) == '47,73' and t_md == 75 and tal(t_q3) == '101,25'

dok('facit-lektier-2026-08-17-diagrammer-og-sumkurve', 'lektier', '2026-08-17',
    'Diagrammer og sumkurve', 'Uge 34 · lektier-uge34-diagrammer.html', [
    ('h2', 'Opgave A · Transport, 25 unger'),
    ('kolonner', (['Transport', 'Antal', 'Frekvens', 'Grader'],
                  [[navn, str(a), f'{tal(f)} %', f'{tal(g)}°']
                   for navn, a, f, g in transport]
                  + [['I alt', str(n_tr), '100 %', '360°']])),
    ('figur', (FG.cirkeldiagram(TRANSPORT),
               'Det færdige cirkeldiagram. Graderne summer til præcis 360°.')),
    ('note', ['b) Typetallet er <b>Cykel</b>. e) Kontrollen er, at frekvenserne '
              'giver præcis 100 % og graderne præcis 360°.',
              'f) Med 30 unger kan antal ikke sammenlignes direkte — der skal '
              'sammenlignes frekvenser. Et grupperet søjlediagram med procent på '
              'y-aksen er det bedste valg. To cirkeldiagrammer kan bruges, men er '
              'sværere at sammenligne præcist.']),
    ('h2', 'Opgave B · Lektietid, 50 unger'),
    ('kolonner', (['Minutter', 'Hyppighed', 'Kumuleret hyppighed',
                   'Kumuleret frekvens'],
                  [[f'{LEKTIE_GR[i]}–{LEKTIE_GR[i+1]}', str(LEKTIE_H[i]),
                    str(lektie_kum[i][0]), f'{tal(lektie_kum[i][1])} %']
                   for i in range(len(LEKTIE_H))])),
    ('p', 'd-e) Aflæsninger på sumkurven:'),
    ('tabel', [
        ('Q1, 25 %', f'ca. {tal(t_q1, 0)} min', 'Ligger i intervallet 30–60'),
        ('Median, 50 %', f'{tal(t_md)} min', 'Ligger i intervallet 60–90'),
        ('Q3, 75 %', f'ca. {tal(t_q3, 0)} min', 'Ligger i intervallet 90–120'),
    ]),
    ('figur', (FG.sumkurve(intervaller(LEKTIE_GR), LEKTIE_H, (25, 50, 75), 'minutter om ugen')[0],
               'Sumkurven med de tre aflæsninger. Ungerne aflæser på egen tegning, '
               'så et par minutters afvigelse er fin.')),
    ('note', ['Præcise værdier: Q1 = 47,73 min og Q3 = 101,25 min. Ungerne aflæser '
              'på egen tegning, så ca. 45–50 og ca. 98–105 bør godkendes.',
              'f) <b>66 %</b> bruger under 90 minutter om ugen — læses direkte som '
              'den kumulerede frekvens ved 90.']),
])


# ---------------------------------------------------------------------------
# Statistik, modul 3 · Opgave C - Kildekritik og manipulation
# ---------------------------------------------------------------------------
# Den afskaarne akse: tallene 102 og 105 set gennem et vindue fra 100.
V1, V2, AFSKAER = 102, 105, 100
REEL = pct(V2 - V1, V1)
SET = F(V2 - AFSKAER, V1 - AFSKAER)
assert tal(REEL) == '2,94' and SET == F(5, 2)

OVER120 = [('Video', 45), ('Spil', 40), ('Musik', 35)]
assert sum(p for _, p in OVER120) == 120
assert F(120 - 100) * F(36, 10) == 72        # procentpoint -> grader

dok('facit-online-2026-08-24-kildekritik', 'online', '2026-08-24',
    'Kildekritik og manipulation',
    'Statistik, modul 3 · Opgave C på klassens statistikside', [
    ('h2', 'Opgave C · Gennemskue fremstillingen'),
    ('p', 'For hvert punkt: hvad er teknisk set rigtigt, og hvad vildleder.'),
    ('h3', 'a) To søjler på 102 og 105, y-aksen starter ved 100'),
    ('p', 'Reel forskel: 105 − 102 = 3, altså 3 ÷ 102 = <b>2,94 %</b> — knap 3 %.'),
    ('figur', (FG.afskaaret_akse(V1, V2, AFSKAER),
               'Til venstre som figuren er tegnet, til højre med aksen fra nul. '
               'Søjlen på 102 bliver 2 enheder høj og søjlen på 105 bliver 5 '
               'enheder høj, og 5 ÷ 2 = 2,5. Øjet ser altså 250 % forskel, hvor '
               'der er 3 %. Tallene er rigtige; det er aksen, der lyver.')),
    ('h3', 'b) Cirkeldiagram med 45 %, 40 % og 35 %'),
    ('p', 'Summen er <b>120 %</b> — altså 20 procentpoint for meget, svarende til '
          '<b>72°</b>. En cirkel kan kun rumme 100 % og 360°. Enten er tallene '
          'forkerte, eller man har kunnet vælge flere svar — og så er '
          'cirkeldiagrammet den forkerte diagramtype.'),
    ('figur', (FG.cirkel_overflow(OVER120),
               'Det sidste udsnit lægger sig oven i det første, fordi der ikke er '
               'plads til 432° på en cirkel med 360°.')),
    ('h3', 'c) 12 af skolens 600 unger, alle fra samme klasse'),
    ('p', 'Der er spurgt <b>2 %</b> af skolen (12 ÷ 600). To grunde til at '
          'stikprøven er skæv:'),
    ('figur', (FG.svarprocent(600, 12, 'Spurgt: 12 af skolens 600 unger'),
               'De grønne er de 12, der blev spurgt. Med 12 svar flytter ét enkelt '
               'svar resultatet med over 8 procentpoint.')),
    ('note', ['<b>1. Den er for lille.</b> Med 12 svar fylder tilfældige udsving '
              'alt for meget — ét enkelt svar flytter resultatet med over 8 '
              'procentpoint.',
              '<b>2. Alle er fra samme klasse.</b> Én klasse er ikke skolen: de har '
              'samme alder, samme lærere og ofte samme holdning. Stikprøven er ikke '
              'repræsentativ, uanset hvor mange man havde spurgt i netop den klasse.']),
    ('h3', 'd) "Antallet af cykeltyverier er fordoblet" — fra 3 til 6'),
    ('p', 'Teknisk rigtigt: 6 er det dobbelte af 3, altså +100 %. Men i absolutte '
          'tal er der kun <b>3 tyverier mere</b>. Overskriften er sand og alligevel '
          'vildledende, fordi procenten lyder alarmerende på et grundlag, der er så '
          'lille, at det kan skyldes tilfældighed.'),
    ('note', ['Det generelle svar: procentvis ændring siger intet uden det absolutte '
              'tal. Spørg altid "hvor mange var det?".']),
    ('h3', 'e) Ungens eget eksempel'),
    ('p', 'Ingen facitliste. Godkend hvis ungen kan udpege hvilket greb der er brugt '
          '— afskåret akse, manglende absolutte tal, skæv stikprøve, forkert '
          'diagramtype — og forklare hvorfor tallet teknisk set kan være rigtigt.'),
])

# ---------------------------------------------------------------------------
# Manipulation, modul 1 · Opgave A - Vurder stikproeven
# ---------------------------------------------------------------------------
assert pct(30, 500) == 6 and pct(470, 500) == 94

dok('facit-online-2026-08-24-stikproeven', 'online', '2026-08-24', 'Stikprøven',
    'Manipulation, modul 1 · Opgave A på klassens manipulationsside', [
    ('h2', 'Opgave A · Vurder stikprøven'),
    ('p', 'For hver undersøgelse: population, stikprøve og hvilken skævhed der er '
          'på spil.'),
    ('kolonner', (['Undersøgelse', 'Population', 'Stikprøve', 'Skævhed'], [
        ['a) Avisens hjemmeside: "Er du utryg i nattelivet?" — 4.200 svar, 78 % ja',
         'byens borgere', 'de læsere der selv valgte at klikke',
         '<b>selvselektion</b>'],
        ['b) Teleselskabet: 6 % svarer, 91 % af dem er tilfredse',
         'alle kunder', 'de 6 % der svarede', '<b>stort bortfald</b>'],
        ['c) Ungerådsformanden spørger sin egen klasse, 22 unger',
         'hele skolen', 'egen klasse', '<b>ikke repræsentativ</b>'],
        ['d) Skema om søvn delt i en gaming-gruppe kl. 2 om natten',
         'unge i almindelighed', 'folk der er vågne kl. 2 og spiller',
         '<b>skæv ramme</b>'],
    ])),
    ('note', ['a) De, der har oplevet noget utrygt, har langt større lyst til at '
              'svare. De 4.200 gør det ikke bedre — en skæv stikprøve bliver ikke '
              'repræsentativ af at være stor.',
              'b) 94 % svarede ikke. Utilfredse kunder er ofte allerede skiftet væk '
              'eller gider ikke svare. Konklusionen gælder kun de 6 %.',
              'c) Én klasse er ikke skolen — samme alder, samme hverdag. Dertil at '
              'spørgeren er kendt af dem, og at ordet "flertal" i konklusionen '
              'handler om skolen, men er målt i klassen.',
              'd) Der spørges netop den gruppe, der er mest atypisk på præcis det, '
              'undersøgelsen handler om. Plus selvselektion, og plus at tidspunktet '
              'i sig selv sorterer.']),
    ('figur', (FG.svarprocent(500, 30, '500 kunder, hvor 6 % svarer'),
               'Konklusionen "91 % er tilfredse" gælder kun de grønne. De grå ved vi '
               'intet om — og utilfredse kunder er ofte allerede skiftet væk.')),
    ('h3', 'e) Hvordan det kunne gøres bedre'),
    ('tabel', [
        ('a)', 'Tilfældigt udvalgte', 'Ring til tilfældigt udvalgte borgere i stedet '
         'for at lade folk selv byde ind.'),
        ('b)', 'Følg op', 'Følg op på dem der ikke svarer, eller tag en tilfældig '
         'delmængde og bliv ved, til svarprocenten er høj.'),
        ('c)', 'Lagdelt udtræk', 'Træk tilfældige unger fra alle klassetrin — gerne '
         'lagdelt, så hvert trin er sikret.'),
        ('d)', 'Bredere ramme', 'Spørg bredt på flere skoler, på et tidspunkt hvor '
         'alle er vågne.'),
    ]),
    ('note', ['Den fælles pointe: <b>deltagerne skal udvælges tilfældigt af '
              'undersøgeren.</b> I det øjeblik folk selv vælger, om de vil være med, '
              'kan man ikke længere slutte noget om populationen.']),
])

# ---------------------------------------------------------------------------
# Uge 35 · lektier - Manipulation
# ---------------------------------------------------------------------------
assert tal(pct(38, 400)) == '9,5' and tal(pct(362, 400)) == '90,5'
assert pct(10 - 4, 4) == 150 and pct(6 - 2, 2) == 200
assert pct(21 - 15, 15) == 40 and 21 - 15 == 6

dok('facit-lektier-2026-08-24-manipulation', 'lektier', '2026-08-24', 'Manipulation',
    'Uge 35 · lektier-uge35-manipulation.html', [
    ('h2', 'Opgave A · Vurder stikprøven'),
    ('kolonner', (['Undersøgelse', 'Population', 'Stikprøve', 'Skævhed'], [
        ['a) Sms-afstemning om cykelhjelm — 12.000 stemmer, 81 % nej',
         'alle borgere, eller alle cyklister', 'de seere der selv valgte at stemme',
         '<b>selvselektion</b>'],
        ['b) Trivselsskema til 400 unger — 38 svarer, 92 % glade',
         'skolens 400 unger', 'de 38 der svarede, svarprocent 9,5 %',
         '<b>stort bortfald</b>'],
        ['c) Træneren spørger sine egne 18 spillere',
         'hele klubben', 'eget hold', '<b>ikke repræsentativ</b>'],
        ['d) Skema om morgenvaner delt i en gruppe for morgenløbere',
         'unge i almindelighed', 'morgenløbere', '<b>skæv ramme</b>'],
    ])),
    ('figur', (FG.svarprocent(400, 38, 'Trivselsskema til 400 unger'),
               'Konklusionen "92 % er glade" gælder kun de 38 grønne. De 362 grå kan '
               'have en helt anden holdning.')),
    ('note', ['a) De med en stærk holdning — her modstandere af påbud — gider bruge '
              'tid og penge på at stemme. De 12.000 gør det ikke bedre; en skæv '
              'stikprøve bliver ikke repræsentativ af at være stor.',
              'b) Bortfald 90,5 %. De 362, der ikke svarede, kan have en helt anden '
              'holdning — og det er ofte netop de utilfredse eller fraværende, der '
              'ikke svarer. Konklusionen gælder kun de 38.',
              'c) Ét hold er ikke klubben. Dertil at spørgeren er deres træner, så de '
              'kan svare det, de tror han vil høre.',
              'd) Der spørges netop den gruppe, der er mest atypisk på præcis det, '
              'undersøgelsen handler om. Plus selvselektion oveni.']),
    ('h3', 'e) Hvordan det kunne gøres bedre'),
    ('tabel', [
        ('a)', 'Tilfældigt udvalgte', 'Tilfældigt udvalgte borgere, kontaktet af '
         'undersøgeren.'),
        ('b)', 'Følg op', 'Følg op på dem der ikke svarer, eller spørg en tilfældig '
         'gruppe ansigt til ansigt, så svarprocenten bliver høj.'),
        ('c)', 'Alle hold', 'Tilfældigt udvalgte fra alle hold, og lad en anden end '
         'træneren spørge.'),
        ('d)', 'Bredere ramme', 'Spørg bredt, fx tilfældige klasser på flere skoler.'),
    ]),
    ('h2', 'Opgave B · Oversæt overskriften'),
    ('kolonner', (['Overskrift', 'Teknisk rigtigt?', 'Hvad vildleder'], [
        ['a) "Steget 150 %" (4 → 10)', 'Ja. 6 ÷ 4 = 150 %',
         'Kun 6 unger mere. Små tal giver store procenter.'],
        ['b) "Risikoen tredobles" (2 → 6 pr. 10.000)', 'Ja, faktor 3',
         'Kun 4 flere pr. 10.000. Fra 0,02 % til 0,06 % — stadig meget lille.'],
        ['c) "Op til 80 % rabat på udvalgte varer"', 'Ja',
         '"Op til" og "udvalgte" gør udsagnet uangribeligt. Én vare med 80 % er nok.'],
        ['d) "Steg fra 15 % til 21 %"', 'Ja',
         '6 procentpoint, men 40 % relativ stigning (6 ÷ 15).'],
    ])),
    ('figur', (FG.procentpoint(15, 21),
               'Samme ændring, to helt forskellige tal. 6 procentpoint lyder '
               'beskedent, 40 % lyder voldsomt.')),
    ('note', ['Til d): procentpoint og procent er ikke det samme. Det er den mest '
              'brugte forveksling i nyheder om meningsmålinger.']),
    ('h3', 'e) Ungens egen overskrift'),
    ('p', 'Ingen facitliste. Tre gode spørgsmål: Hvad er tallet i absolutte tal? '
          'Hvem har lavet undersøgelsen, og hvad tjener de på svaret? Hvad '
          'sammenlignes der med?'),
])


# ---------------------------------------------------------------------------
# Manipulation, modul 2 · Opgave B - Find fejlen i diagrammet
# ---------------------------------------------------------------------------
INDEKS = [F('100.0'), F('100.4'), F('100.2'), F('100.8'), F('101.1'), F('101.3')]
assert INDEKS[-1] - INDEKS[0] == F('1.3')
assert pct(INDEKS[-1] - INDEKS[0], INDEKS[0]) == F('1.3')
assert F(120) ** 2 == 4 * F(60) ** 2            # dobbelt side giver firedobbelt areal
OVER115 = [('Video', 45), ('Spil', 30), ('Sociale medier', 25), ('Musik', 15)]
assert sum(p for _, p in OVER115) == 115
assert F(115 - 100) * F(36, 10) == 54

dok('facit-online-2026-08-31-diagrammet', 'online', '2026-08-31', 'Diagrammet',
    'Manipulation, modul 2 · Opgave B på klassens manipulationsside', [
    ('h2', 'Opgave B · Find fejlen i diagrammet'),
    ('p', 'Tallene bag de to linjediagrammer står nu i en tabel på siden: '
          '<code>100,0 · 100,4 · 100,2 · 100,8 · 101,1 · 101,3</code> for jan til jun.'),
    ('tabel', [
        ('a) Hvor mange procent er tallet steget?', '1,3 %',
         '101,3 − 100,0 = 1,3, og 1,3 ÷ 100,0 = 1,3 % over et halvt år'),
        ('c) Arealtricket', '4 gange',
         'Siden går fra 60 til 120, altså 2 gange. Arealet fra 60² = 3.600 til '
         '120² = 14.400'),
    ]),
    ('h3', 'b) Hvorfor det venstre diagram giver et forkert indtryk'),
    ('p', 'Y-aksen går fra 99,8 til 101,5 — et udsnit på 1,7 enheder omkring en '
          'værdi på godt 100. Kurven fylder derfor hele figurens højde, selvom den '
          'kun stiger 1,3 %. I det højre diagram går aksen fra 0, og så ses '
          'stigningen som det, den er: næsten flad. <b>Alle seks tal er rigtige i '
          'begge. Det er aksen, der lyver.</b>'),
    ('h3', 'd) Hvordan de to millioner skulle have været tegnet'),
    ('p', 'Gør kun <b>én</b> dimension større: to søjler med samme bredde, hvor den '
          'ene er dobbelt så høj. Vil man beholde kvadrater, skal arealet fordobles, '
          'og sidelængden skal da være √2 ≈ 1,41 gange større — ikke 2.'),
    ('figur', (FG.areal_aerligt(54, '1 mio.', '2 mio.', 2),
               'Til venstre udgangspunktet. I midten den forkerte tegning, hvor '
               'begge sider er fordoblet. Til højre den ærlige, hvor arealet er '
               'fordoblet.')),
    ('h3', 'e) Cirkeldiagrammet summer til 115 %'),
    ('p', 'Det er <b>15 procentpoint</b> for meget, svarende til <b>54°</b>. '
          'To forklaringer:'),
    ('figur', (FG.cirkel_overflow(OVER115),
               'De 15 procentpoint for meget bliver til 54° overlap, hvor det sidste '
               'udsnit lægger sig oven i det første.')),
    ('note', ['<b>1. Man måtte vælge flere svar.</b> Hver ung har kunnet sætte mere '
              'end ét kryds, så summen overstiger 100 %. Det er ikke en regnefejl, '
              'men et forkert valg af diagramtype — brug et søjlediagram.',
              '<b>2. Tallene er afrundet op</b>, eller en kategori er talt med to '
              'gange. Ved afrunding kan man komme et par procentpoint over, men 15 '
              'procentpoint er for meget til at være afrunding alene.']),
    ('h3', 'f) Et udsnit der får tallet til at styrtdykke'),
    ('p', 'Kurven over de tolv måneder falder samlet — januar er højest, december '
          'lavest — men indeholder flere stigninger undervejs. Vælger man januar til '
          'marts, ser det ud som et frit fald: det er årets stejleste '
          'tre-måneders-nedgang. Også juni til august og juli til september virker '
          'dramatiske.'),
    ('note', ['Sammenlign med sidens eget eksempel, hvor april til juni blev '
              'fremhævet som "den flotte vækst". Samme kurve, modsat historie — '
              'afhængigt af hvilke tre måneder man klipper ud.',
              '<b>Pointen:</b> spørg altid hvor lang perioden er, og hvorfor netop '
              'den er valgt. Et udsnit kan vise det stik modsatte af helheden.']),
])

# ---------------------------------------------------------------------------
# Manipulation, modul 3 · Opgave C og D - Tallet og teksten
# ---------------------------------------------------------------------------
LOEN = [18000, 19000, 20000, 21000, 92000]
assert gennemsnit(LOEN) == 34000 and femtal(LOEN)[2] == 20000
assert sum(1 for v in LOEN if v < 34000) == 4
assert pct(4 - 2, 2) == 100 and pct(6 - 3, 3) == 100
assert 12 - 8 == 4 and pct(12 - 8, 8) == 50

dok('facit-online-2026-08-31-tallet-og-teksten', 'online', '2026-08-31',
    'Tallet og teksten',
    'Manipulation, modul 3 · Opgave C og D på klassens manipulationsside', [
    ('h2', 'Opgave C · Oversæt overskriften'),
    ('kolonner', (['Overskrift', 'Teknisk rigtigt?', 'Hvad vildleder'], [
        ['a) "Topkarakterer steget 100 %" (2 → 4)', 'Ja. 4 er det dobbelte af 2',
         'Kun 2 unger mere. På så lille et grundlag kan forskellen skyldes '
         'tilfældighed.'],
        ['b) "Gennemsnitsløn 34.000"', 'Ja. 170.000 ÷ 5 = 34.000',
         '4 af 5 tjener 21.000 eller mindre. Én løn på 92.000 trækker gennemsnittet '
         'op. Medianen er 20.000 og beskriver en typisk ansat.'],
        ['c) "Risikoen fordobles" (3 → 6 pr. 10.000)', 'Ja, en fordobling',
         'Kun 3 flere pr. 10.000. Risikoen går fra 0,03 % til 0,06 % — stadig meget '
         'lille.'],
        ['d) "Op til 70 % rabat på hele butikken"', 'Ja',
         '"Op til" gør udsagnet uangribeligt. Én vare med 70 % er nok, mens resten '
         'har 5 %. "Hele butikken" beskriver hvor tilbuddet gælder, ikke hvor mange '
         'varer der er billige.'],
        ['e) "Tilslutningen steg fra 8 % til 12 %"', 'Ja',
         '4 procentpoint, men 50 % relativ stigning (4 ÷ 8). De to tal beskriver det '
         'samme og lyder vildt forskelligt.'],
    ])),
    ('figur', (FG.loen_figur(LOEN),
               'De fem lønninger. Gennemsnittet trækkes op af den ene høje løn og '
               'ligger højere end fire af de fem. Medianen ligger midt i feltet og '
               'beskriver en typisk ansat.')),
    ('figur', (FG.procentpoint(8, 12),
               'Samme ændring, to helt forskellige tal. Vælg selv hvilket der passer '
               'til historien — det er præcis dét, der gør overskriften vildledende.')),
    ('note', ['Til e): procentpoint og procent er ikke det samme. Det er den mest '
              'brugte forveksling i nyheder om meningsmålinger, og den er værd at '
              'øve, indtil ungerne selv fanger den.']),
    ('h3', 'f) Ungens egen overskrift'),
    ('p', 'Ingen facitliste. Tre gode spørgsmål ungen kan nå frem til:'),
    ('tabel', [
        ('1.', 'Absolutte tal', 'Hvad er tallet i absolutte tal? Hvor mange var det?'),
        ('2.', 'Afsender', 'Hvem har lavet undersøgelsen, og hvad tjener de på '
         'svaret?'),
        ('3.', 'Sammenligning', 'Hvad sammenlignes der med, og over hvor lang tid?'),
    ]),
    ('h2', 'Opgave D · Lav din egen manipulation'),
    ('p', 'Gruppearbejde to og to. Ingen facitliste — vurder efter:'),
    ('tabel', [
        ('Er de to formuleringer reelt forskellige?', 'Ja/nej',
         'Den ledende skal indeholde et signal om det ønskede svar: "Synes du '
         'også, at …", "Er du enig i, at …".'),
        ('Blev halvdelen spurgt med hver version?', 'Ja/nej',
         'Ellers kan de to resultater ikke sammenlignes.'),
        ('Er det ene diagram ærligt og det andet manipuleret?', 'Ja/nej',
         'Grebet skal kunne navngives — afskåret y-akse, areal, udsnit af perioden, '
         'forkert diagramtype.'),
        ('Kan de sætte ord på deres eget greb?', 'Ja/nej',
         'Det er den vigtigste del: at kunne gennemskue tricket bagefter, også når '
         'andre bruger det.'),
    ]),
    ('note', ['Forvent at formuleringen gør tydelig forskel selv i en enkelt klasse. '
              'Gør den ikke det, var den ledende version nok ikke ledende nok — og '
              'det er i sig selv en god samtale.']),
])

# ---------------------------------------------------------------------------
# Uge 36 · lektier - Manipulation, diagrammer
# ---------------------------------------------------------------------------
U36 = [200, 203, 204, 204, 205, 206]
assert pct(U36[-1] - U36[0], U36[0]) == 3
aendring = [U36[i + 1] - U36[i] for i in range(5)]
assert aendring == [3, 1, 0, 1, 1]
tre = {i: U36[i + 2] - U36[i] for i in range(4)}
assert min(tre, key=tre.get) == 1 and max(tre, key=tre.get) == 0
assert pct(40 - 20, 20) == 100 and F(3) ** 2 == 9
OVER125 = [('Video', 50), ('Spil', 30), ('Musik', 25), ('Andet', 20)]
assert sum(p for _, p in OVER125) == 125
assert F(125 - 100) * F(36, 10) == 90

dok('facit-lektier-2026-08-31-manipulation-diagrammer', 'lektier', '2026-08-31',
    'Manipulation, diagrammer',
    'Uge 36 · lektier-uge36-manipulation-diagrammer.html', [
    ('p', 'Datasæt i opgave A, jan til jun: <code>200 · 203 · 204 · 204 · 205 · 206</code>. '
          'Ændringer: +3, +1, 0, +1, +1.'),
    ('h2', 'Opgave A · Find fejlen i diagrammet'),
    ('tabel', [
        ('a) Stigning i procent', '3 %', '206 − 200 = 6, og 6 ÷ 200 = 3 %'),
        ('c) Ser flad ud', 'feb, mar, apr', '203 → 204, samlet +1 — mindst af alle '
         'udsnit'),
        ('d) Ser stejlest ud', 'jan, feb, mar', '200 → 204, samlet +4 — mest af alle '
         'udsnit'),
    ]),
    ('figur', (FG.afskaaret_akse(200, 206, 199, ('jan', 'jun')),
               'b) Y-aksen går fra 199 til 207 — et udsnit på 8 enheder omkring en '
               'værdi på 200. Kurven fylder derfor hele figurens højde, selvom den '
               'kun stiger 3 %. Til højre går aksen fra 0, og så ses stigningen som '
               'det, den er: næsten flad. Alle seks tal er rigtige. Det er aksen, '
               'der lyver.')),
    ('note', ['d) Det egentlige svar: samme talrække kan fortælle to modsatte '
              'historier, alt efter hvilket udsnit man viser. Spørg derfor altid, '
              'hvor meget der er skåret væk, og hvorfor perioden er valgt netop '
              'sådan.']),
    ('h2', 'Opgave B · Når figuren lyver om størrelsen'),
    ('tabel', [
        ('a) Prisstigning', '100 %', '20 → 40 kr, fordoblet'),
        ('b) Arealer', '1 cm² og 9 cm², altså 9 gange', '1² = 1 og 3² = 9'),
        ('c) Tallet mod figuren', 'tallet 2 gange, figuren 9 gange', ''),
    ]),
    ('p', 'd) Øjet bedømmer <b>areal</b>, ikke sidelængde. Gøres både bredden og '
          'højden 3 gange større, bliver arealet 3 × 3 = 9 gange større. Derfor '
          'virker forskellen langt voldsommere, end tallet berettiger.'),
    ('p', 'e) Ærligt: gør kun én dimension større — fx en søjle der er dobbelt så høj '
          'og lige så bred. Vil man beholde kvadrater, skal arealet fordobles, og '
          'sidelængden skal da være √2 ≈ 1,41 gange større, ikke 3.'),
    ('figur', (FG.areal_aerligt(40, '20 kr', '40 kr', 3),
               'I midten som opgavens figur er tegnet: tre gange så bred og høj, '
               'altså ni gange arealet. Til højre den ærlige tegning.')),
    ('h2', 'Opgave C · Cirklen der går over 100 %'),
    ('p', 'Delene er 50 + 30 + 25 + 20 = <b>125 %</b>.'),
    ('tabel', [
        ('a) For meget', '25 procentpoint', '125 − 100'),
        ('b) I grader', '90°', '25 % × 3,6°/%'),
    ]),
    ('figur', (FG.cirkel_overflow(OVER125),
               'Overlappet er præcis de 25 procentpoint, der er for meget.')),
    ('note', ['c) To forklaringer: (1) man måtte vælge flere svar, så summen '
              'overstiger 100 % — ikke en regnefejl, men et forkert valg af '
              'diagramtype; (2) tallene er afrundet op, eller en kategori er talt '
              'med to gange, men 25 procentpoint er for meget til at være afrunding '
              'alene.',
              'd) Et <b>søjlediagram</b>, hvor hver kategori har sin egen søjle. Et '
              'cirkeldiagram kan kun bruges, når delene udgør en helhed og giver '
              'præcis 100 %. Må man vælge flere svar, hører delene ikke til samme '
              'helhed. I figuren kan man se problemet: det sidste udsnit lægger sig '
              'oven i det første, fordi der ikke er plads til 450° på en cirkel med '
              '360°.']),
    ('h2', 'Opgave D · Lav din egen manipulation'),
    ('p', 'Ingen facitliste — det er ungens egen undersøgelse. Vurder efter:'),
    ('tabel', [
        ('Er de to formuleringer reelt forskellige?', 'Ja/nej',
         'Den ledende skal indeholde et signal om det ønskede svar.'),
        ('Er der mindst seks svar, delt i to halvdele?', 'Ja/nej', ''),
        ('Viser tabellen begge resultater?', 'Ja/nej', 'Så forskellen kan ses.'),
        ('Er det manipulerede diagram manipuleret med et navngivet greb?', 'Ja/nej',
         'Afskåret y-akse, areal, udsnit af perioden, forkert diagramtype.'),
        ('Kan ungen sætte ord på sit eget greb?', 'Ja/nej',
         'Og på, hvor stor forskel formuleringen gjorde. Det er den vigtigste del.'),
    ]),
])

# ---------------------------------------------------------------------------
# Statistik, modul 4 · Opgave D - Sandsynlighed
# ---------------------------------------------------------------------------
ROED, BLAA, GROEN = 3, 4, 5
KUGLER = ROED + BLAA + GROEN
assert KUGLER == 12
p_roed = F(ROED, KUGLER)
p_blaa_groen = F(BLAA + GROEN, KUGLER)
p_ikke_groen = 1 - F(GROEN, KUGLER)
p_to_med = p_roed * p_roed
p_to_uden = F(ROED, KUGLER) * F(ROED - 1, KUGLER - 1)
assert (p_roed, p_blaa_groen, p_ikke_groen) == (F(1, 4), F(3, 4), F(7, 12))
assert p_to_med == F(1, 16) and p_to_uden == F(1, 22)
sum7 = [(a, b) for a in range(1, 7) for b in range(1, 7) if a + b == 7]
assert len(sum7) == 6 and F(len(sum7), 36) == F(1, 6)
assert F(1, 4) * 40 == 10

dok('facit-online-2026-09-07-sandsynlighed', 'online', '2026-09-07', 'Sandsynlighed',
    'Statistik, modul 4 · Opgave D på klassens statistikside', [
    ('h2', 'Opgave D · Regn med chancen'),
    ('p', 'Posen indeholder 3 røde, 4 blå og 5 grønne kugler, altså 12 i alt. '
          'Alle svar som brøk.'),
    ('tabel', [
        ('a) P(rød)', '3/12 = 1/4', '3 gunstige ud af 12'),
        ('a) P(blå eller grøn)', '9/12 = 3/4', '(4 + 5) ÷ 12'),
        ('a) P(ikke grøn)', '7/12', '1 − 5/12'),
        ('b) To røde med tilbagelægning', '1/16', '3/12 × 3/12 = 9/144'),
        ('c) To røde uden tilbagelægning', '1/22', '3/12 × 2/11 = 6/132'),
        ('d) To terninger, sum 7', '6/36 = 1/6', '6 gunstige af 36'),
    ]),
    ('figur', (FG.terninger(7),
               'Alle 36 udfald med to terninger. De seks grønne felter er dem, hvor '
               'summen bliver 7. Bemærk at (1,6) og (6,1) er to forskellige udfald.')),
    ('note', ['d) De gunstige udfald er (1,6) (2,5) (3,4) (4,3) (5,2) (6,1) — seks '
              'stk. Bemærk at (1,6) og (6,1) er to forskellige udfald; regner ungen '
              'dem som ét, får hen 3/21 og har byttet udfaldsrum.',
              'Forskellen på med og uden tilbagelægning er værd at dvæle ved: 1/16 '
              'mod 1/22. Uden tilbagelægning er der én rød og én kugle mindre i '
              'posen ved andet træk.']),
    ('h3', 'e) Klasseøvelse med to mønter'),
    ('p', 'Teoretisk sandsynlighed for to plat: <b>1/4</b>, altså 25 %. Ved 40 kast '
          'er det forventede antal <b>10</b>. Resultater mellem ca. 6 og 14 er helt '
          'normale — det er selve pointen: den statistiske sandsynlighed svinger om '
          'den teoretiske og nærmer sig den, jo flere kast man laver.'),
    ('h3', 'f) Teoretisk og statistisk sandsynlighed'),
    ('tabel', [
        ('Teoretisk', 'Regnes ud fra modellen',
         'Man tæller gunstige udfald og deler med mulige. Ændrer sig ikke.'),
        ('Statistisk', 'Måles ud fra forsøg',
         'Man tæller hvor ofte det skete, og deler med antal forsøg. Ændrer sig hver '
         'gang man laver forsøget igen.'),
    ]),
])


# ---------------------------------------------------------------------------
if __name__ == '__main__':
    byg(sys.argv[1] if len(sys.argv) > 1 else '')
