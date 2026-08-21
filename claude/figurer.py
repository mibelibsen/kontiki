# -*- coding: utf-8 -*-
"""SVG-figurer til opgaver og facitlister.

Alle koordinater BEREGNES. Tegn aldrig en figur paa oejemaal - to
linjediagrammer paa manipulation.html paastod at vise de samme seks tal og
afveg 4,8 %, fordi de var tegnet i haanden.

Modulet er et vaerktoej, ikke en del af sitet. Det ligger i claude/, som er
udelukket i .vercelignore. Sitet er fortsat rene HTML-filer uden build.

Brug:
    import sys; sys.path.insert(0, 'claude')
    import figurer as FG
    svg = FG.boksplot(3, 5, 6, 9, 13, 'Talraekken 3, 5, 5, 6, 8, 9, 13')

Funktioner:
    boksplot(min, q1, median, q3, maks, titel)   femtalssammendrag
    cirkeldiagram(dele)                          [(navn, antal)], viser grader
    cirkel_overflow(dele)                        [(navn, procent)] over 100 %
    sumkurve(graenser, hyp, aflaes, xnavn)       -> (svg, aflaesninger)
    terninger(sum_)                              6x6 udfaldsrum
    areal_aerligt(side, ..., forkert_faktor)     arealtricket, ret og vrang
    loen_figur(vals, navne, enhed)               gennemsnit kontra median
    svarprocent(N, n, tekst)                     bortfald som prikgitter
    procentpoint(fra, til)                       procentpoint kontra procent

Farverne foelger sitets palet. Figurerne saettes ind i en <div class="figur">
med en forklarende <div class="figtekst"> under.
"""
from fractions import Fraction as F
import math

INK, MUT, LIN = '#1a2233', '#586074', '#c9d2e0'
BLA, ORA, GRO, ROD = '#1f6fd6', '#b5710a', '#1a8f5e', '#c23b4b'
FONT = 'font-family="Consolas, monospace" font-size="11"'


def _dk(x):
    if isinstance(x, F) and x.denominator == 1:
        x = int(x)
    if isinstance(x, int):
        return str(x)
    s = f'{float(x):.2f}'.rstrip('0').rstrip('.')
    return s.replace('.', ',')


# ---------------------------------------------------------------- boksplot
def boksplot(mini, q1, med, q3, maks, titel=''):
    X0, X1, YB = 46, 494, 92          # akse
    lo, hi = mini, maks
    pad = (hi - lo) * F(1, 10)
    a, b = lo - pad, hi + pad

    def X(v):
        return float(X0 + (F(v) - a) / (b - a) * (X1 - X0))

    xk1, xm, xk3 = X(q1), X(med), X(q3)
    xmin, xmaks = X(mini), X(maks)
    kasse_top, kasse_bund, midt = 34, 74, 54

    s = [f'<svg viewBox="0 0 540 130" role="img" aria-label="Boksplot med '
         f'mindsteværdi {_dk(mini)}, Q1 {_dk(q1)}, median {_dk(med)}, '
         f'Q3 {_dk(q3)} og størsteværdi {_dk(maks)}.">', f'<g {FONT}>']
    if titel:
        s.append(f'<text x="270" y="16" text-anchor="middle" fill="{MUT}" '
                 f'font-size="11">{titel}</text>')
    # whiskers
    s.append(f'<line x1="{xmin:.1f}" y1="{midt}" x2="{xk1:.1f}" y2="{midt}" '
             f'stroke="{INK}" stroke-width="1.5"/>')
    s.append(f'<line x1="{xk3:.1f}" y1="{midt}" x2="{xmaks:.1f}" y2="{midt}" '
             f'stroke="{INK}" stroke-width="1.5"/>')
    for x in (xmin, xmaks):
        s.append(f'<line x1="{x:.1f}" y1="{kasse_top+6}" x2="{x:.1f}" '
                 f'y2="{kasse_bund-6}" stroke="{INK}" stroke-width="1.5"/>')
    # kasse
    s.append(f'<rect x="{xk1:.1f}" y="{kasse_top}" width="{xk3-xk1:.1f}" '
             f'height="{kasse_bund-kasse_top}" fill="#eaf2fd" stroke="{BLA}" '
             f'stroke-width="1.5"/>')
    s.append(f'<line x1="{xm:.1f}" y1="{kasse_top}" x2="{xm:.1f}" '
             f'y2="{kasse_bund}" stroke="{ROD}" stroke-width="2.5"/>')
    # akse
    s.append(f'<line x1="{X0}" y1="{YB}" x2="{X1}" y2="{YB}" stroke="{INK}"/>')
    for v, navn, farve in ((mini, 'min', MUT), (q1, 'Q1', BLA), (med, 'median', ROD),
                           (q3, 'Q3', BLA), (maks, 'max', MUT)):
        x = X(v)
        s.append(f'<line x1="{x:.1f}" y1="{YB-4}" x2="{x:.1f}" y2="{YB+4}" stroke="{INK}"/>')
        s.append(f'<text x="{x:.1f}" y="{YB+18}" text-anchor="middle" fill="{INK}" '
                 f'font-weight="700">{_dk(v)}</text>')
        s.append(f'<text x="{x:.1f}" y="{YB+31}" text-anchor="middle" fill="{farve}" '
                 f'font-size="9.5">{navn}</text>')
    s.append('</g></svg>')
    return ''.join(s)


# ------------------------------------------------------------ cirkeldiagram
def cirkeldiagram(dele, vis_grader=True):
    """dele: [(navn, antal)]. Vinkler beregnes eksakt."""
    N = sum(v for _, v in dele)
    cx = cy, r = 132.0, 108.0
    cx = 140.0
    cy = 140.0
    farver = [BLA, ORA, GRO, ROD, '#7a4fbf']
    vinkel = -90.0
    paths, leg = [], []
    for i, (navn, v) in enumerate(dele):
        pct = F(v, N) * 100
        grad = F(v, N) * 360
        span = float(grad)
        a0 = math.radians(vinkel); a1 = math.radians(vinkel + span)
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        stor = 1 if span > 180 else 0
        paths.append(f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{r},{r} 0 {stor},1 '
                     f'{x1:.1f},{y1:.1f} Z" fill="{farver[i]}" stroke="#fff" stroke-width="1.5"/>')
        g = f' · {_dk(grad)}°' if vis_grader else ''
        leg.append(f'<tspan x="290" dy="{22 if i else 0}">{navn}: '
                   f'{_dk(pct)} %{g}</tspan>')
        vinkel += span
    prikker = ''.join(
        f'<rect x="272" y="{128-len(dele)*11+i*22}" width="10" height="10" '
        f'rx="2" fill="{farver[i]}"/>' for i in range(len(dele)))
    y0leg = 136 - len(dele) * 11 + 9
    return (f'<svg viewBox="0 0 500 290" role="img" aria-label="Cirkeldiagram '
            f'over {N} observationer.">{"".join(paths)}'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#fff" stroke-width="1.5"/>'
            f'{prikker}<text {FONT} fill="{INK}" y="{y0leg}">{"".join(leg)}</text></svg>')


# ---------------------------------------------------------------- sumkurve
def sumkurve(graenser, hyp, aflaes=(25, 50, 75), xnavn=''):
    N = sum(hyp)
    kum, s_ = [], 0
    for v in hyp:
        s_ += v; kum.append(s_)
    frek = [F(k, N) * 100 for k in kum]
    xmin, xmaks = graenser[0][0], graenser[-1][1]
    X0, X1, YT, YB = 54, 452, 26, 214

    def X(v): return float(X0 + (F(v) - xmin) / (xmaks - xmin) * (X1 - X0))
    def Y(p): return float(YB - F(p) / 100 * (YB - YT))

    pts = [(X(xmin), Y(0))] + [(X(g[1]), Y(f)) for g, f in zip(graenser, frek)]
    s = [f'<svg viewBox="0 0 500 265" role="img" aria-label="Sumkurve over {N} '
         f'observationer med aflæsning af kvartiler og median.">', f'<g {FONT}>']
    # gitter
    for p in (0, 25, 50, 75, 100):
        y = Y(p)
        s.append(f'<line x1="{X0}" y1="{y:.1f}" x2="{X1}" y2="{y:.1f}" '
                 f'stroke="{LIN}" stroke-dasharray="2 3"/>')
        s.append(f'<text x="{X0-8}" y="{y+4:.1f}" text-anchor="end" fill="{MUT}">{p} %</text>')
    # aflaesninger
    svar = {}
    for p in aflaes:
        maal = F(p, 100) * N; foer = 0; val = None
        for (lo, hi), v, k in zip(graenser, hyp, kum):
            if k >= maal:
                val = lo + (hi - lo) * F(maal - foer, v); break
            foer = k
        svar[p] = val
        x, y = X(val), Y(p)
        s.append(f'<line x1="{X0}" y1="{y:.1f}" x2="{x:.1f}" y2="{y:.1f}" '
                 f'stroke="{ROD}" stroke-width="1.2" stroke-dasharray="4 3"/>')
        s.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{YB}" '
                 f'stroke="{ROD}" stroke-width="1.2" stroke-dasharray="4 3"/>')
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{ROD}"/>')
        s.append(f'<text x="{x:.1f}" y="{YB+30}" text-anchor="middle" fill="{ROD}" '
                 f'font-weight="700">{_dk(val)}</text>')
    # kurve
    s.append('<polyline points="' + ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts) +
             f'" fill="none" stroke="{BLA}" stroke-width="2.5"/>')
    for x, y in pts:
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{BLA}"/>')
    # akser
    s.append(f'<line x1="{X0}" y1="{YB}" x2="{X1}" y2="{YB}" stroke="{INK}"/>')
    s.append(f'<line x1="{X0}" y1="{YT}" x2="{X0}" y2="{YB}" stroke="{INK}"/>')
    for g in [graenser[0][0]] + [g[1] for g in graenser]:
        x = X(g)
        s.append(f'<line x1="{x:.1f}" y1="{YB}" x2="{x:.1f}" y2="{YB+4}" stroke="{INK}"/>')
        s.append(f'<text x="{x:.1f}" y="{YB+17}" text-anchor="middle" fill="{MUT}">{g}</text>')
    if xnavn:
        s.append(f'<text x="{(X0+X1)/2:.0f}" y="{YB+48}" text-anchor="middle" '
                 f'fill="{MUT}">{xnavn}</text>')
    s.append('</g></svg>')
    return ''.join(s), svar


# ------------------------------------------------------------ terningtabel
def terninger(sum_=7):
    C, X0, Y0 = 30, 60, 40
    s = [f'<svg viewBox="0 0 300 260" role="img" aria-label="Alle 36 udfald med '
         f'to terninger. De {sum(1 for a in range(1,7) for b in range(1,7) if a+b==sum_)} '
         f'gunstige for summen {sum_} er fremhævet.">', f'<g {FONT}>']
    for i in range(6):
        s.append(f'<text x="{X0+i*C+C/2}" y="{Y0-8}" text-anchor="middle" '
                 f'fill="{MUT}">{i+1}</text>')
        s.append(f'<text x="{X0-10}" y="{Y0+i*C+C/2+4}" text-anchor="end" '
                 f'fill="{MUT}">{i+1}</text>')
    for a in range(1, 7):
        for b in range(1, 7):
            x, y = X0 + (b - 1) * C, Y0 + (a - 1) * C
            traef = a + b == sum_
            fill = '#eaf7f0' if traef else '#fff'
            stroke = GRO if traef else LIN
            s.append(f'<rect x="{x}" y="{y}" width="{C}" height="{C}" fill="{fill}" '
                     f'stroke="{stroke}" stroke-width="{1.5 if traef else 1}"/>')
            s.append(f'<text x="{x+C/2}" y="{y+C/2+4}" text-anchor="middle" '
                     f'fill="{GRO if traef else "#aab3c2"}" '
                     f'font-weight="{700 if traef else 400}">{a+b}</text>')
    s.append(f'<text x="150" y="{Y0+6*C+26}" text-anchor="middle" fill="{GRO}" '
             f'font-weight="700">6 gunstige ud af 36</text>')
    s.append('</g></svg>')
    return ''.join(s)


# --------------------------------------------- cirkel der summer over 100 %
def cirkel_overflow(dele):
    """dele: [(navn, procent)] der tilsammen giver mere end 100 %."""
    cx = cy, r = 132.0, 100.0
    cx, cy, r = 130.0, 130.0, 100.0
    farver = [BLA, ORA, GRO, ROD, '#7a4fbf']
    vinkel, paths, leg = -90.0, [], []
    ialt = sum(p for _, p in dele)
    for i, (navn, pct) in enumerate(dele):
        span = pct * 3.6
        a0, a1 = math.radians(vinkel), math.radians(vinkel + span)
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        sidste = i == len(dele) - 1
        op = ' fill-opacity="0.72" stroke="#fff" stroke-width="2"' if sidste else ''
        paths.append(f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{r},{r} 0 '
                     f'{1 if span > 180 else 0},1 {x1:.1f},{y1:.1f} Z" '
                     f'fill="{farver[i]}"{op}/>')
        leg.append((navn, pct, farver[i]))
        vinkel += span
    prikker, tekst = [], []
    for i, (navn, pct, f) in enumerate(leg):
        y = 66 + i * 22
        prikker.append(f'<rect x="262" y="{y-9}" width="10" height="10" rx="2" fill="{f}"/>')
        tekst.append(f'<tspan x="280" y="{y}">{navn}: {_dk(pct)} % · {_dk(pct*F(18,5))}°</tspan>')
    y = 66 + len(leg) * 22 + 6
    tekst.append(f'<tspan x="280" y="{y}" font-weight="700" fill="{ROD}">'
                 f'I alt {_dk(ialt)} % · {_dk(ialt*F(18,5))}°</tspan>')
    tekst.append(f'<tspan x="280" y="{y+20}" fill="{ROD}">'
                 f'{_dk(ialt-100)} procentpoint for meget</tspan>')
    tekst.append(f'<tspan x="280" y="{y+38}" fill="{MUT}">svarer til '
                 f'{_dk((ialt-100)*F(18,5))}° overlap</tspan>')
    return (f'<svg viewBox="0 0 500 265" role="img" aria-label="Cirkeldiagram hvor '
            f'udsnittene tilsammen giver {_dk(ialt)} procent, så det sidste udsnit '
            f'lægger sig oven i det første.">{"".join(paths)}'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#fff" stroke-width="2"/>'
            f'{"".join(prikker)}<text {FONT} fill="{INK}">{"".join(tekst)}</text></svg>')


# ------------------------------------------------- arealtricket, ret og vrang
def areal_aerligt(side=54, tekst_lille='1 mio.', tekst_stor='2 mio.',
                  forkert_faktor=2):
    """Viser hvorfor en fordobling ikke maa tegnes med dobbelt sidelaengde."""
    forkert = side * forkert_faktor
    rigtig = side * math.sqrt(2)
    BUND = 190

    def kvadrat(x, s_, farve, over, sidetxt, arealtxt):
        y = BUND - s_
        return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{s_:.1f}" height="{s_:.1f}" '
                f'fill="{farve}" fill-opacity="0.85"/>'
                f'<text x="{x+s_/2:.1f}" y="{y-8:.1f}" text-anchor="middle" '
                f'fill="{farve}" font-weight="700">{over}</text>'
                f'<text x="{x+s_/2:.1f}" y="{BUND+15:.1f}" text-anchor="middle" '
                f'fill="{MUT}" font-size="9.5">{sidetxt}</text>'
                f'<text x="{x+s_/2:.1f}" y="{BUND+27:.1f}" text-anchor="middle" '
                f'fill="{MUT}" font-size="9.5">{arealtxt}</text>')

    s = [f'<svg viewBox="0 0 560 240" role="img" aria-label="Tre kvadrater: '
         f'udgangspunkt, den forkerte tegning med dobbelt sidelaengde og fire gange '
         f'arealet, og den aerlige med sidelaengde gange kvadratroden af to og '
         f'dobbelt areal.">', f'<g {FONT}>']
    s.append(kvadrat(30, side, BLA, tekst_lille,
                     f'side {side:.0f}', f'areal {side*side:.0f}'))
    s.append(kvadrat(170, forkert, ROD, tekst_stor,
                     f'side {forkert:.0f}', f'areal {forkert*forkert:.0f}'))
    s.append(kvadrat(380, rigtig, GRO, tekst_stor,
                     f'side {rigtig:.0f}', f'areal {rigtig*rigtig:.0f}'))
    s.append(f'<text x="224" y="{BUND+45}" text-anchor="middle" fill="{ROD}" '
             f'font-weight="700">FORKERT · areal {forkert_faktor**2:.0f} gange</text>')
    s.append(f'<text x="418" y="{BUND+45}" text-anchor="middle" fill="{GRO}" '
             f'font-weight="700">RIGTIGT · areal 2 gange</text>')
    s.append(f'<text x="280" y="16" text-anchor="middle" fill="{MUT}">'
             f'Tallet er fordoblet. Hvor stor skal figuren være?</text>')
    s.append(f'<text x="418" y="{BUND-rigtig-22:.0f}" text-anchor="middle" '
             f'fill="{GRO}" font-size="9.5">siden ganges med √2 ≈ 1,41</text>')
    s.append('</g></svg>')
    return ''.join(s)


# ------------------------------------------------ gennemsnit kontra median
def loen_figur(vals, navne=None, enhed='kr'):
    """Vandrette soejler med gennemsnit og median markeret."""
    vals = list(vals)
    N = len(vals)
    gns = F(sum(vals), N)
    m = sorted(vals)[N // 2] if N % 2 else F(sum(sorted(vals)[N//2-1:N//2+1]), 2)
    X0, X1, YT = 96, 396, 34
    VAERDI_X = 492
    H, GAP = 22, 9
    maks = max(vals) * F(11, 10)

    def X(v): return float(X0 + F(v) / maks * (X1 - X0))

    s = [f'<svg viewBox="0 0 500 {YT + N*(H+GAP) + 62}" role="img" '
         f'aria-label="Fem lønninger som søjler. Gennemsnittet ligger højere end '
         f'fire af de fem, medianen midt i feltet.">', f'<g {FONT}>']
    for i, v in enumerate(vals):
        y = YT + i * (H + GAP)
        navn = navne[i] if navne else f'Ansat {i+1}'
        s.append(f'<text x="{X0-10}" y="{y+15}" text-anchor="end" fill="{MUT}">{navn}</text>')
        s.append(f'<rect x="{X0}" y="{y}" width="{X(v)-X0:.1f}" height="{H}" '
                 f'fill="{BLA}" fill-opacity="0.8" rx="2"/>')
        s.append(f'<text x="{VAERDI_X}" y="{y+15}" text-anchor="end" fill="{INK}" '
                 f'font-weight="700">{_dk(v)}</text>')
    ybund = YT + N * (H + GAP)
    for v, navn, farve in ((gns, 'gennemsnit', ROD), (m, 'median', GRO)):
        x = X(v)
        s.append(f'<line x1="{x:.1f}" y1="{YT-8}" x2="{x:.1f}" y2="{ybund+4}" '
                 f'stroke="{farve}" stroke-width="2" stroke-dasharray="5 4"/>')
    s.append(f'<text x="{X(gns):.1f}" y="{ybund+20}" text-anchor="middle" '
             f'fill="{ROD}" font-weight="700">gennemsnit {_dk(gns)}</text>')
    s.append(f'<text x="{X(m):.1f}" y="{ybund+38}" text-anchor="middle" '
             f'fill="{GRO}" font-weight="700">median {_dk(m)}</text>')
    s.append(f'<text x="{X0}" y="{ybund+56}" fill="{MUT}" font-size="9.5">'
             f'{sum(1 for v in vals if v < gns)} af {N} tjener mindre end '
             f'gennemsnittet ({enhed})</text>')
    s.append('</g></svg>')
    return ''.join(s)


# --------------------------------------------------- svarprocent / bortfald
def svarprocent(N, n, tekst=''):
    """Prikgitter der viser hvor faa der svarede."""
    KOL = 40
    R = 4.6
    STEP = 11.4
    raekker = math.ceil(N / KOL)
    W, H = 40 + KOL * STEP, 30 + raekker * STEP + 46
    s = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" role="img" aria-label="{N} prikker '
         f'hvor {n} er fremhævet — det er dem der svarede.">', f'<g {FONT}>']
    for i in range(N):
        r, c = divmod(i, KOL)
        cx, cy = 20 + c * STEP + R, 22 + r * STEP + R
        svarede = i < n
        s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R}" '
                 f'fill="{GRO if svarede else "#dde3ec"}"/>')
    pct = F(n, N) * 100
    y = 22 + raekker * STEP + 20
    s.append(f'<text x="20" y="{y:.0f}" fill="{GRO}" font-weight="700">'
             f'{n} svarede = {_dk(pct)} %</text>')
    s.append(f'<text x="20" y="{y+17:.0f}" fill="{MUT}">'
             f'{N-n} svarede ikke = {_dk(100-pct)} % bortfald</text>')
    if tekst:
        s.append(f'<text x="20" y="{y+34:.0f}" fill="{MUT}" font-size="9.5">{tekst}</text>')
    s.append('</g></svg>')
    return ''.join(s)


# --------------------------------------------- procentpoint kontra procent
def procentpoint(fra, til):
    """To soejler der viser forskellen paa procentpoint og relativ stigning."""
    X0, YB, YT = 70, 176, 30
    BW = 74
    maks = 100

    def Y(v): return YB - F(v) / maks * (YB - YT)

    pp = til - fra
    rel = F(til - fra, fra) * 100
    s = [f'<svg viewBox="0 0 528 250" role="img" aria-label="To soejler: {fra} procent '
         f'og {til} procent. Forskellen er {pp} procentpoint, men {_dk(rel)} procent '
         f'relativ stigning.">', f'<g {FONT}>']
    for p in (0, 25, 50, 75, 100):
        y = float(Y(p))
        s.append(f'<line x1="{X0-6}" y1="{y:.1f}" x2="330" y2="{y:.1f}" '
                 f'stroke="{LIN}" stroke-dasharray="2 3"/>')
        s.append(f'<text x="{X0-12}" y="{y+4:.1f}" text-anchor="end" fill="{MUT}">{p} %</text>')
    for i, (v, farve, mrk) in enumerate(((fra, BLA, 'før'), (til, GRO, 'efter'))):
        x = X0 + 30 + i * 130
        y = float(Y(v))
        s.append(f'<rect x="{x}" y="{y:.1f}" width="{BW}" height="{YB-y:.1f}" '
                 f'fill="{farve}" fill-opacity="0.85" rx="2"/>')
        s.append(f'<text x="{x+BW/2}" y="{y-8:.1f}" text-anchor="middle" '
                 f'fill="{farve}" font-weight="700">{v} %</text>')
        s.append(f'<text x="{x+BW/2}" y="{YB+16}" text-anchor="middle" fill="{MUT}">{mrk}</text>')
    s.append(f'<line x1="{X0-6}" y1="{YB}" x2="330" y2="{YB}" stroke="{INK}"/>')
    s.append(f'<text x="352" y="70" fill="{INK}" font-weight="700">Samme forskel, '
             f'to tal:</text>')
    s.append(f'<text x="352" y="96" fill="{BLA}" font-weight="700">+{pp} procentpoint</text>')
    s.append(f'<text x="352" y="114" fill="{MUT}" font-size="9.5">{til} − {fra} = {pp}</text>')
    s.append(f'<text x="352" y="142" fill="{ROD}" font-weight="700">+{_dk(rel)} %</text>')
    s.append(f'<text x="352" y="160" fill="{MUT}" font-size="9.5">{pp} ÷ {fra} = {_dk(rel)} %</text>')
    s.append('</g></svg>')
    return ''.join(s)


# ============================================================================
# TEGNEPLADSER - tomme figurer til opgaveark, saa ungen kan tegne i dem.
# Roeber ikke facit; giver kun akserne.
# ============================================================================

def tom_talllinje(lo, hi, step, titel='Tegn dit boksplot her'):
    """Tallinje med plads over til et boksplot."""
    X0, X1, YB = 46, 494, 116
    def X(v): return float(X0 + (F(v) - lo) / (hi - lo) * (X1 - X0))
    s = [f'<svg viewBox="0 0 540 150" role="img" aria-label="Tom tallinje fra {lo} '
         f'til {hi} med plads til at tegne et boksplot.">', f'<g {FONT}>']
    s.append(f'<text x="270" y="16" text-anchor="middle" fill="{MUT}">{titel}</text>')
    s.append(f'<rect x="{X0}" y="26" width="{X1-X0}" height="76" fill="#fafbfd" '
             f'stroke="{LIN}" stroke-dasharray="4 4" rx="4"/>')
    v = lo
    while v <= hi:
        x = X(v)
        s.append(f'<line x1="{x:.1f}" y1="{YB-5}" x2="{x:.1f}" y2="{YB+5}" stroke="{INK}"/>')
        s.append(f'<text x="{x:.1f}" y="{YB+20}" text-anchor="middle" fill="{MUT}">{_dk(v)}</text>')
        v += step
    s.append(f'<line x1="{X0}" y1="{YB}" x2="{X1}" y2="{YB}" stroke="{INK}"/>')
    s.append('</g></svg>')
    return ''.join(s)


def tomt_sumkurvegitter(graenser, xnavn='', titel='Tegn din sumkurve her'):
    """Akser med procentgitter, uden kurve."""
    xmin, xmaks = graenser[0][0], graenser[-1][1]
    X0, X1, YT, YB = 54, 452, 30, 218
    def X(v): return float(X0 + (F(v) - xmin) / (xmaks - xmin) * (X1 - X0))
    def Y(p): return float(YB - F(p) / 100 * (YB - YT))
    s = [f'<svg viewBox="0 0 500 268" role="img" aria-label="Tomt koordinatsystem '
         f'til en sumkurve, med procent på y-aksen.">', f'<g {FONT}>']
    s.append(f'<text x="250" y="16" text-anchor="middle" fill="{MUT}">{titel}</text>')
    for p in (0, 10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90, 100):
        y = Y(p)
        tyk = p in (0, 25, 50, 75, 100)
        dash = '' if tyk else ' stroke-dasharray="2 4"'
        s.append(f'<line x1="{X0}" y1="{y:.1f}" x2="{X1}" y2="{y:.1f}" stroke="{LIN}" '
                 f'stroke-width="{1 if tyk else 0.5}"{dash}/>')
        if tyk:
            s.append(f'<text x="{X0-8}" y="{y+4:.1f}" text-anchor="end" fill="{MUT}">{p} %</text>')
    for g in [graenser[0][0]] + [g[1] for g in graenser]:
        x = X(g)
        s.append(f'<line x1="{x:.1f}" y1="{YT}" x2="{x:.1f}" y2="{YB}" stroke="{LIN}" '
                 f'stroke-width="0.5" stroke-dasharray="2 4"/>')
        s.append(f'<line x1="{x:.1f}" y1="{YB}" x2="{x:.1f}" y2="{YB+5}" stroke="{INK}"/>')
        s.append(f'<text x="{x:.1f}" y="{YB+18}" text-anchor="middle" fill="{MUT}">{g}</text>')
    s.append(f'<line x1="{X0}" y1="{YB}" x2="{X1}" y2="{YB}" stroke="{INK}"/>')
    s.append(f'<line x1="{X0}" y1="{YT}" x2="{X0}" y2="{YB}" stroke="{INK}"/>')
    if xnavn:
        s.append(f'<text x="{(X0+X1)/2:.0f}" y="{YB+38}" text-anchor="middle" '
                 f'fill="{MUT}">{xnavn}</text>')
    s.append('</g></svg>')
    return ''.join(s)


def tom_cirkel(titel='Tegn dit cirkeldiagram her'):
    """Cirkel med gradmarkeringer for hver 30 grader."""
    cx, cy, r = 250.0, 148.0, 108.0
    s = [f'<svg viewBox="0 0 500 300" role="img" aria-label="Tom cirkel med '
         f'gradmarkeringer for hver 30 grader.">', f'<g {FONT}>']
    s.append(f'<text x="250" y="18" text-anchor="middle" fill="{MUT}">{titel}</text>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fafbfd" stroke="{INK}" stroke-width="1.5"/>')
    for g in range(0, 360, 30):
        a = math.radians(g - 90)
        x1_, y1_ = cx + (r - 8) * math.cos(a), cy + (r - 8) * math.sin(a)
        x2_, y2_ = cx + r * math.cos(a), cy + r * math.sin(a)
        s.append(f'<line x1="{x1_:.1f}" y1="{y1_:.1f}" x2="{x2_:.1f}" y2="{y2_:.1f}" '
                 f'stroke="{MUT}"/>')
        xt, yt = cx + (r + 16) * math.cos(a), cy + (r + 16) * math.sin(a) + 4
        s.append(f'<text x="{xt:.1f}" y="{yt:.1f}" text-anchor="middle" fill="{MUT}" '
                 f'font-size="9">{g}°</text>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="2.5" fill="{INK}"/>')
    s.append(f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy-r}" stroke="{INK}" '
             f'stroke-dasharray="4 3"/>')
    s.append(f'<text x="250" y="{cy+r+38:.0f}" text-anchor="middle" fill="{MUT}" '
             f'font-size="9.5">Start ved 0° og gå med uret. 1 % = 3,6°</text>')
    s.append('</g></svg>')
    return ''.join(s)


# ============================================================================
# KOORDINATSYSTEM - til lineaere funktioner og grafaflaesning
# ============================================================================

def _koord_ramme(xmin, xmax, ymin, ymax, W=470, H=360, top=30):
    """Returnerer plotgeometri og X/Y-omregnere."""
    X0, X1 = 44, W - 16
    YT, YB = top, H - 34
    def X(v): return float(X0 + (F(v) - xmin) / (xmax - xmin) * (X1 - X0))
    def Y(v): return float(YB - (F(v) - ymin) / (ymax - ymin) * (YB - YT))
    return X0, X1, YT, YB, X, Y


def _skridt(spaend, maks_linjer=22):
    """Vaelger et paent gitterskridt, saa der aldrig tegnes tusindvis af linjer."""
    import math as _m
    raa = spaend / maks_linjer
    if raa <= 1:
        return 1
    tier = 10 ** int(_m.floor(_m.log10(raa)))
    for m in (1, 2, 2.5, 5, 10):
        if tier * m >= raa:
            return int(tier * m) if tier * m >= 1 else 1
    return int(tier * 10)


def _koord_gitter(X0, X1, YT, YB, X, Y, xmin, xmax, ymin, ymax, tal=True):
    s = []
    xs = _skridt(float(xmax - xmin))
    ys = _skridt(float(ymax - ymin))
    for v in range(int(xmin) - int(xmin) % xs, int(xmax) + 1, xs):
        x = X(v)
        akse = v == 0
        s.append(f'<line x1="{x:.1f}" y1="{YT}" x2="{x:.1f}" y2="{YB}" '
                 f'stroke="{INK if akse else LIN}" stroke-width="{1.4 if akse else 0.6}"/>')
        if tal and v != 0:
            s.append(f'<text x="{x:.1f}" y="{Y(0)+15:.1f}" text-anchor="middle" '
                     f'fill="{MUT}" font-size="10">{v}</text>')
    for v in range(int(ymin) - int(ymin) % ys, int(ymax) + 1, ys):
        y = Y(v)
        akse = v == 0
        s.append(f'<line x1="{X0}" y1="{y:.1f}" x2="{X1}" y2="{y:.1f}" '
                 f'stroke="{INK if akse else LIN}" stroke-width="{1.4 if akse else 0.6}"/>')
        if tal and v != 0:
            s.append(f'<text x="{X(0)-7:.1f}" y="{y+4:.1f}" text-anchor="end" '
                     f'fill="{MUT}" font-size="10">{v}</text>')
    s.append(f'<text x="{X1-4}" y="{Y(0)-8:.1f}" text-anchor="end" fill="{INK}" '
             f'font-style="italic">x</text>')
    s.append(f'<text x="{X(0)+8:.1f}" y="{YT+12}" fill="{INK}" font-style="italic">y</text>')
    return s


def koordinatsystem(linjer=(), punkter=(), xmin=-2, xmax=8, ymin=-4, ymax=10,
                    titel='', vis_tal=True):
    """linjer: [(a, b, farve, navn)] for y = ax + b.
       punkter: [(x, y, farve, navn)]."""
    xmin, xmax, ymin, ymax = F(xmin), F(xmax), F(ymin), F(ymax)
    X0, X1, YT, YB, X, Y = _koord_ramme(xmin, xmax, ymin, ymax)
    s = [f'<svg viewBox="0 0 470 360" role="img" aria-label="Koordinatsystem'
         + (f' med {len(linjer)} rette linjer' if linjer else '') + '.">', f'<g {FONT}>']
    if titel:
        s.append(f'<text x="235" y="16" text-anchor="middle" fill="{MUT}">{titel}</text>')
    s.append(f'<rect x="{X0}" y="{YT}" width="{X1-X0}" height="{YB-YT}" fill="#fff"/>')
    s += _koord_gitter(X0, X1, YT, YB, X, Y, xmin, xmax, ymin, ymax, vis_tal)
    signatur = []
    for a, b, farve, navn in linjer:
        a, b = F(a), F(b)
        signatur.append((farve, navn))
        pts = []
        for xv in (xmin, xmax):
            yv = a * xv + b
            if ymin <= yv <= ymax:
                pts.append((xv, yv))
        for yv in (ymin, ymax):
            if a != 0:
                xv = F(yv - b, a)
                if xmin <= xv <= xmax:
                    pts.append((xv, yv))
        pts = sorted(set(pts))[:2]
        if len(pts) == 2:
            (xa, ya), (xb, yb) = pts
            s.append(f'<line x1="{X(xa):.1f}" y1="{Y(ya):.1f}" x2="{X(xb):.1f}" '
                     f'y2="{Y(yb):.1f}" stroke="{farve}" stroke-width="2.6"/>')
    for px, py, farve, navn in punkter:
        s.append(f'<circle cx="{X(px):.1f}" cy="{Y(py):.1f}" r="5" fill="{farve}" '
                 f'stroke="#fff" stroke-width="1.5"/>')
        if navn:
            s.append(f'<text x="{X(px)+11:.1f}" y="{Y(py)-10:.1f}" fill="{farve}" '
                     f'font-weight="700" stroke="#fff" stroke-width="3.5" '
                     f'paint-order="stroke" stroke-linejoin="round">{navn}</text>')
    if signatur:
        bx = X0
        for farve, navn in signatur:
            s.append(f'<line x1="{bx}" y1="{YB+26}" x2="{bx+22}" y2="{YB+26}" '
                     f'stroke="{farve}" stroke-width="3"/>')
            s.append(f'<text x="{bx+28}" y="{YB+30}" fill="{INK}">{navn}</text>')
            bx += 34 + len(navn) * 7
    s.append('</g></svg>')
    return ''.join(s)


def tomt_koordinatsystem(xmin=-2, xmax=8, ymin=-4, ymax=10,
                         titel='Tegn din graf her'):
    return koordinatsystem(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, titel=titel)


# ============================================================================
# LIGNINGER - vaegtmodel og arealmodel
# ============================================================================

def vaegt(a, b, c, xnavn='x'):
    """Vaegtstang i balance for ligningen a*x + b = c.

    Indholdet ligger i EN raekke, og broedstoerrelsen tilpasses antallet, saa
    figuren aldrig loeber ud over skaalen - uanset hvor store tallene er.
    """
    CX, CY, ARM, PAN = 250.0, 86.0, 168.0, 112.0
    s = [f'<svg viewBox="0 0 500 190" role="img" aria-label="En vægt i balance. '
         f'På venstre skål {a} kasser med {xnavn} og {b} lodder, på højre skål '
         f'{c} lodder.">', f'<g {FONT}>']
    s.append(f'<text x="250" y="18" text-anchor="middle" fill="{INK}" '
             f'font-weight="700">{a}{xnavn} + {b} = {c}</text>')

    def skaal(cx, kasser, lodder, farve):
        n = kasser + lodder
        pitch = min(28.0, (PAN - 8) / max(n, 1))
        kb = min(26.0, pitch - 3)
        pr = min(8.0, pitch / 2 - 1.5)
        ud = [f'<line x1="{cx}" y1="{CY}" x2="{cx}" y2="{CY+32}" stroke="{MUT}"/>',
              f'<path d="M{cx-PAN/2},{CY+32} L{cx+PAN/2},{CY+32} '
              f'L{cx+PAN/2-14},{CY+48} L{cx-PAN/2+14},{CY+48} Z" '
              f'fill="#eef1f6" stroke="{MUT}"/>']
        x = cx - n * pitch / 2
        for i in range(n):
            midt = x + pitch / 2
            if i < kasser:
                ud.append(f'<rect x="{midt-kb/2:.1f}" y="{CY+29-kb:.1f}" '
                          f'width="{kb:.1f}" height="{kb:.1f}" rx="3" fill="{farve}"/>')
                ud.append(f'<text x="{midt:.1f}" y="{CY+29-kb/2+4:.1f}" '
                          f'text-anchor="middle" fill="#fff" font-weight="700" '
                          f'font-style="italic" font-size="{min(12, kb*0.6):.0f}">'
                          f'{xnavn}</text>')
            else:
                ud.append(f'<circle cx="{midt:.1f}" cy="{CY+29-pr:.1f}" '
                          f'r="{pr:.1f}" fill="{MUT}"/>')
            x += pitch
        return ''.join(ud)

    s.append(f'<line x1="{CX-ARM}" y1="{CY}" x2="{CX+ARM}" y2="{CY}" '
             f'stroke="{INK}" stroke-width="3"/>')
    s.append(f'<path d="M{CX},{CY} L{CX-20},{CY+56} L{CX+20},{CY+56} Z" fill="{INK}"/>')
    s.append(skaal(CX - ARM, a, b, BLA))
    s.append(skaal(CX + ARM, 0, c, GRO))
    s.append('</g></svg>')
    return ''.join(s)


def arealmodel(k, n, xnavn='x'):
    """Rektangel der viser k(x + n) = kx + kn."""
    X0, Y0, H = 66, 46, 92
    BX, BN = 150, 88
    s = [f'<svg viewBox="0 0 500 170" role="img" aria-label="Rektangel med højden '
         f'{k} delt i to felter: {xnavn} gange {k} og {n} gange {k}.">', f'<g {FONT}>']
    s.append(f'<text x="250" y="20" text-anchor="middle" fill="{MUT}">'
             f'{k}({xnavn} + {n}) = {k}{xnavn} + {k*n}</text>')
    s.append(f'<rect x="{X0}" y="{Y0}" width="{BX}" height="{H}" fill="#eaf2fd" '
             f'stroke="{BLA}" stroke-width="1.5"/>')
    s.append(f'<rect x="{X0+BX}" y="{Y0}" width="{BN}" height="{H}" fill="#eaf7f0" '
             f'stroke="{GRO}" stroke-width="1.5"/>')
    s.append(f'<text x="{X0+BX/2}" y="{Y0+H/2+5}" text-anchor="middle" fill="{BLA}" '
             f'font-weight="700">{k} · {xnavn}</text>')
    s.append(f'<text x="{X0+BX+BN/2}" y="{Y0+H/2+5}" text-anchor="middle" '
             f'fill="{GRO}" font-weight="700">{k} · {n} = {k*n}</text>')
    s.append(f'<text x="{X0+BX/2}" y="{Y0-8}" text-anchor="middle" fill="{MUT}" '
             f'font-style="italic">{xnavn}</text>')
    s.append(f'<text x="{X0+BX+BN/2}" y="{Y0-8}" text-anchor="middle" fill="{MUT}">{n}</text>')
    s.append(f'<line x1="{X0-14}" y1="{Y0}" x2="{X0-14}" y2="{Y0+H}" stroke="{MUT}"/>')
    s.append(f'<text x="{X0-20}" y="{Y0+H/2+4}" text-anchor="end" fill="{MUT}">{k}</text>')
    s.append('</g></svg>')
    return ''.join(s)


# ============================================================================
# SMAA EKSEMPELFIGURER - til forklaringer og oversigtskort paa sitet
# ============================================================================

def mini_cirkel(dele=(4, 3, 2, 1)):
    """Lille cirkeldiagram uden tekst - til et oversigtskort."""
    import math as _m
    cx = cy = 50.0
    r = 40.0
    N = sum(dele)
    farver = [BLA, ORA, GRO, ROD]
    vinkel, ud = -90.0, []
    for i, v in enumerate(dele):
        span = float(F(v, N) * 360)
        a0, a1 = _m.radians(vinkel), _m.radians(vinkel + span)
        x0, y0 = cx + r * _m.cos(a0), cy + r * _m.sin(a0)
        x1, y1 = cx + r * _m.cos(a1), cy + r * _m.sin(a1)
        ud.append(f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{r},{r} 0 '
                  f'{1 if span > 180 else 0},1 {x1:.1f},{y1:.1f} Z" '
                  f'fill="{farver[i % 4]}" stroke="#fff" stroke-width="1.5"/>')
        vinkel += span
    return (f'<svg viewBox="0 0 100 100" role="img" aria-label="Lille '
            f'cirkeldiagram med fire udsnit.">{"".join(ud)}</svg>')


def mini_soejler(vals=(5, 8, 3, 6)):
    """Lille soejlediagram - adskilte soejler, en pr. kategori."""
    W, H, BUND = 100.0, 100.0, 86.0
    maks = max(vals)
    bw = 15.0
    gap = (W - 12 - len(vals) * bw) / max(len(vals) - 1, 1)
    ud, x = [], 6.0
    for v in vals:
        h = v / maks * 62
        ud.append(f'<rect x="{x:.1f}" y="{BUND-h:.1f}" width="{bw}" height="{h:.1f}" '
                  f'rx="1.5" fill="{BLA}"/>')
        x += bw + gap
    ud.append(f'<line x1="4" y1="{BUND}" x2="{W-4}" y2="{BUND}" stroke="{INK}" '
              f'stroke-width="1.5"/>')
    return (f'<svg viewBox="0 0 100 100" role="img" aria-label="Lille '
            f'søjlediagram med fire adskilte søjler.">{"".join(ud)}</svg>')


def mini_histogram(vals=(2, 5, 8, 4, 2)):
    """Lille histogram - soejler uden mellemrum, fordi intervallerne graenser op."""
    W, BUND = 100.0, 86.0
    maks = max(vals)
    bw = (W - 12) / len(vals)
    ud, x = [], 6.0
    for v in vals:
        h = v / maks * 62
        ud.append(f'<rect x="{x:.1f}" y="{BUND-h:.1f}" width="{bw:.1f}" '
                  f'height="{h:.1f}" fill="{GRO}" stroke="#fff" stroke-width="1"/>')
        x += bw
    ud.append(f'<line x1="4" y1="{BUND}" x2="{W-4}" y2="{BUND}" stroke="{INK}" '
              f'stroke-width="1.5"/>')
    return (f'<svg viewBox="0 0 100 100" role="img" aria-label="Lille histogram '
            f'med fem søjler uden mellemrum.">{"".join(ud)}</svg>')


def mini_sumkurve(frek=(10, 35, 70, 90, 100)):
    """Lille sumkurve - stiger altid, ender i 100 %."""
    W, BUND, TOP = 100.0, 86.0, 16.0
    ud = []
    for p in (50,):
        y = BUND - p / 100 * (BUND - TOP)
        ud.append(f'<line x1="8" y1="{y:.1f}" x2="{W-6}" y2="{y:.1f}" '
                  f'stroke="{LIN}" stroke-dasharray="2 2"/>')
    pts = [(8.0, BUND)]
    for i, f in enumerate(frek):
        x = 8 + (i + 1) / len(frek) * (W - 16)
        pts.append((x, BUND - f / 100 * (BUND - TOP)))
    ud.append('<polyline points="' + ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts) +
              f'" fill="none" stroke="{ORA}" stroke-width="2.5"/>')
    ud.append(f'<line x1="8" y1="{BUND}" x2="{W-6}" y2="{BUND}" stroke="{INK}" '
              f'stroke-width="1.5"/>')
    ud.append(f'<line x1="8" y1="{TOP-4}" x2="8" y2="{BUND}" stroke="{INK}" '
              f'stroke-width="1.5"/>')
    return (f'<svg viewBox="0 0 100 100" role="img" aria-label="Lille sumkurve der '
            f'stiger fra nul til hundrede procent.">{"".join(ud)}</svg>')


def afskaaret_akse(v1, v2, afskaering, navne=('A', 'B')):
    """To soejlediagrammer med samme tal: et afskaaret og et fra nul."""
    def panel(x0, ymin, ymax, farve, overskrift, undertekst):
        W, BUND, TOP = 190.0, 176.0, 46.0
        ud = [f'<text x="{x0+W/2:.0f}" y="30" text-anchor="middle" fill="{farve}" '
              f'font-weight="700">{overskrift}</text>']
        for i, v in enumerate((v1, v2)):
            h = (v - ymin) / (ymax - ymin) * (BUND - TOP)
            bx = x0 + 46 + i * 62
            ud.append(f'<rect x="{bx}" y="{BUND-h:.1f}" width="40" height="{h:.1f}" '
                      f'rx="2" fill="{farve}" fill-opacity="0.85"/>')
            ud.append(f'<text x="{bx+20}" y="{BUND-h-7:.1f}" text-anchor="middle" '
                      f'fill="{farve}" font-weight="700">{v}</text>')
            ud.append(f'<text x="{bx+20}" y="{BUND+15}" text-anchor="middle" '
                      f'fill="{MUT}">{navne[i]}</text>')
        ud.append(f'<line x1="{x0+30}" y1="{BUND}" x2="{x0+W-14}" y2="{BUND}" '
                  f'stroke="{INK}"/>')
        ud.append(f'<line x1="{x0+30}" y1="{TOP-6}" x2="{x0+30}" y2="{BUND}" '
                  f'stroke="{INK}"/>')
        ud.append(f'<text x="{x0+25}" y="{BUND+4}" text-anchor="end" fill="{MUT}" '
                  f'font-size="10">{ymin}</text>')
        ud.append(f'<text x="{x0+25}" y="{TOP+4}" text-anchor="end" fill="{MUT}" '
                  f'font-size="10">{ymax}</text>')
        ud.append(f'<text x="{x0+W/2:.0f}" y="{BUND+34}" text-anchor="middle" '
                  f'fill="{MUT}" font-size="9.5">{undertekst}</text>')
        return ''.join(ud)

    reel = F(int(round((v2 - v1) * 100)), int(round(v1 * 100))) * 100
    hoejde = F(int(round((v2 - afskaering) * 100)), int(round((v1 - afskaering) * 100)))
    s = [f'<svg viewBox="0 0 500 230" role="img" aria-label="To søjlediagrammer med '
         f'de samme to tal. I det venstre starter y-aksen ved {afskaering}, så '
         f'forskellen ser meget større ud.">', f'<g {FONT}>']
    s.append(panel(10, afskaering, v2 + (v2 - afskaering) * 0.15, ROD,
                   f'y-aksen starter ved {afskaering}',
                   f'Søjlerne ser {_dk(hoejde)} gange så høje ud'))
    s.append(panel(280, 0, v2 * 1.25, GRO, 'y-aksen starter ved 0',
                   f'Den reelle forskel er {_dk(reel)} %'))
    s.append('</g></svg>')
    return ''.join(s)


# ------------------------------------------------------------ regneark-mock
# Bruges til Excel-vejledninger. Cellernes placering beregnes ud fra
# kolonnebredderne, saa pile og rammer altid rammer den rigtige celle.

GITTER, HOVEDFYLD = '#c9d2e0', '#eef2f8'


def _celleboks(kols, bredder, gutter=30, celleh=21):
    """Returnerer (x_for_kolonne, samlet_bredde)."""
    x, ud = gutter, {}
    for k in kols:
        ud[k] = x
        x += bredder[k]
    return ud, x


def regneark(kols, raekker, data, bredder, hoejre=(), rammer=(), noter=(),
             fyld=(), celleh=21, gutter=30, W=None):
    """Tegner et udsnit af et regneark.

    kols     ['B','C','D']            kolonnebogstaver i raekkefoelge
    raekker  [6,7,8,None,24,25]       raekkenumre; None giver en brudlinje
    data     {'B6':'Aktiekurs'}       celleindhold
    bredder  {'B':62,'C':132}         kolonnebredde i px
    hoejre   ('D',)                   kolonner der staar hoejrestillet (tal)
    rammer   [('D7','D25','#1f6fd6')] markering om et celleomraade
    noter    [('D7','tekst','#b5710a')] pil med tekst til hoejre for arket
    fyld     {'B6':'#1f6fd6'}         cellefarve; tekst bliver hvid
    """
    xk, arkb = _celleboks(kols, bredder, gutter, celleh)
    rk = {r: 18 + i * celleh for i, r in enumerate(raekker)}   # 18 = hovedhoejde
    H = 18 + len(raekker) * celleh + 2
    notb = 250 if noter else 0
    if W is None:
        W = arkb + notb + 12
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" '
         f'style="max-width:{W}px" xmlns="http://www.w3.org/2000/svg" {FONT}>']
    s.append(f'<rect x="0" y="0" width="{arkb}" height="{H}" fill="#fff"/>')
    # kolonnehoveder
    s.append(f'<rect x="0" y="0" width="{arkb}" height="18" fill="{HOVEDFYLD}"/>')
    for k in kols:
        s.append(f'<rect x="{xk[k]}" y="0" width="{bredder[k]}" height="18" '
                 f'fill="{HOVEDFYLD}" stroke="{GITTER}"/>')
        s.append(f'<text x="{xk[k] + bredder[k] / 2:.1f}" y="13" text-anchor="middle" '
                 f'fill="{MUT}" font-weight="bold">{k}</text>')
    # raekkenumre og celler
    for r in raekker:
        y = rk[r]
        if r is None:
            continue
        s.append(f'<rect x="0" y="{y}" width="{gutter}" height="{celleh}" '
                 f'fill="{HOVEDFYLD}" stroke="{GITTER}"/>')
        s.append(f'<text x="{gutter / 2}" y="{y + celleh - 6}" text-anchor="middle" '
                 f'fill="{MUT}">{r}</text>')
        for k in kols:
            ref = f'{k}{r}'
            bg = dict(fyld).get(ref, '#fff')
            s.append(f'<rect x="{xk[k]}" y="{y}" width="{bredder[k]}" '
                     f'height="{celleh}" fill="{bg}" stroke="{GITTER}"/>')
            v = data.get(ref)
            if v is None:
                continue
            farve = '#fff' if bg != '#fff' else INK
            if k in hoejre:
                s.append(f'<text x="{xk[k] + bredder[k] - 5}" y="{y + celleh - 6}" '
                         f'text-anchor="end" fill="{farve}">{v}</text>')
            else:
                s.append(f'<text x="{xk[k] + 5}" y="{y + celleh - 6}" '
                         f'fill="{farve}">{v}</text>')
    # brudlinje hvor raekker springer
    for i, r in enumerate(raekker):
        if r is None:
            y = 18 + i * celleh
            s.append(f'<rect x="0" y="{y}" width="{arkb}" height="{celleh}" fill="#fff"/>')
            s.append(f'<text x="{arkb / 2}" y="{y + celleh - 6}" text-anchor="middle" '
                     f'fill="{MUT}">⋮</text>')

    def _pos(ref):
        k = ''.join(c for c in ref if c.isalpha())
        r = int(''.join(c for c in ref if c.isdigit()))
        return xk[k], rk[r], bredder[k]

    for fra, til, farve in rammer:
        x1, y1, b1 = _pos(fra)
        x2, y2, b2 = _pos(til)
        s.append(f'<rect x="{x1}" y="{y1}" width="{x2 + b2 - x1}" '
                 f'height="{y2 + celleh - y1}" fill="none" stroke="{farve}" '
                 f'stroke-width="2.5"/>')
    for ref, tekst, farve in noter:
        x, y, b = _pos(ref)
        ym = y + celleh / 2
        xs = arkb + 10
        s.append(f'<line x1="{x + b}" y1="{ym}" x2="{xs}" y2="{ym}" '
                 f'stroke="{farve}" stroke-width="1.5"/>')
        s.append(f'<circle cx="{x + b}" cy="{ym}" r="3" fill="{farve}"/>')
        s.append(f'<text x="{xs + 6}" y="{ym + 4}" fill="{farve}">{tekst}</text>')
    s.append('</svg>')
    return ''.join(s)


def soejler_log(vals, kats, log=False, titel='', ynavn='', xnavn='',
                W=620, H=340):
    """Soejlediagram med lineaer eller logaritmisk y-akse.

    Hoejderne beregnes: lineaert v/maks, logaritmisk (log v - log lo)/(log hi - log lo).
    """
    X0, X1, YT, YB = 92, W - 14, 34, H - 46
    ph, pb = YB - YT, X1 - X0
    n = len(vals)
    bb = pb / n * 0.62
    mid = [X0 + pb / n * (i + .5) for i in range(n)]
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" style="max-width:{W}px" '
         f'xmlns="http://www.w3.org/2000/svg" {FONT}>',
         f'<rect x="0" y="0" width="{W}" height="{H}" fill="#fff" stroke="{LIN}"/>']
    if titel:
        s.append(f'<text x="{W / 2}" y="20" text-anchor="middle" fill="{INK}" '
                 f'font-size="13" font-weight="bold">{titel}</text>')

    if log:
        lo, hi = 0, math.ceil(math.log10(max(vals)))
        def yy(v):
            return YB - (math.log10(v) - lo) / (hi - lo) * ph
        for e in range(lo, hi + 1):
            y = yy(10 ** e)
            s.append(f'<line x1="{X0}" y1="{y:.1f}" x2="{X1}" y2="{y:.1f}" '
                     f'stroke="{LIN}" stroke-dasharray="2 3"/>')
            s.append(f'<text x="{X0 - 6}" y="{y + 4:.1f}" text-anchor="end" '
                     f'fill="{MUT}">10<tspan dy="-4" font-size="8">{e}</tspan></text>')
        bund = YB
    else:
        maks = max(vals)
        e = math.floor(math.log10(maks))
        for m in (1, 2, 2.5, 5, 10):                    # pæne akseskridt
            trin = m * 10 ** (e - 1)
            if 4 <= math.ceil(maks / trin) <= 8:
                break
        def yy(v):
            return YB - v / (math.ceil(maks / trin) * trin) * ph
        t = 0
        while t <= math.ceil(maks / trin) * trin + 1:
            y = yy(t)
            s.append(f'<line x1="{X0}" y1="{y:.1f}" x2="{X1}" y2="{y:.1f}" '
                     f'stroke="{LIN}" stroke-dasharray="2 3"/>')
            mrk = '0' if t == 0 else f'{_dk(t / 1e9)} mia.'
            s.append(f'<text x="{X0 - 6}" y="{y + 4:.1f}" text-anchor="end" '
                     f'fill="{MUT}">{mrk}</text>')
            t += trin
        bund = yy(0)

    for i, v in enumerate(vals):
        y = yy(v)
        h = max(bund - y, 0.4)
        s.append(f'<rect x="{mid[i] - bb / 2:.1f}" y="{y:.1f}" width="{bb:.1f}" '
                 f'height="{h:.1f}" fill="{BLA}"/>')
        s.append(f'<text x="{mid[i]:.1f}" y="{YB + 15}" text-anchor="middle" '
                 f'fill="{MUT}" font-size="9" '
                 f'transform="rotate(-55 {mid[i]:.1f} {YB + 15})">{kats[i]}</text>')
    s.append(f'<line x1="{X0}" y1="{bund:.1f}" x2="{X1}" y2="{bund:.1f}" stroke="{INK}"/>')
    s.append(f'<line x1="{X0}" y1="{YT}" x2="{X0}" y2="{YB}" stroke="{INK}"/>')
    if ynavn:
        s.append(f'<text x="14" y="{(YT + YB) / 2}" text-anchor="middle" fill="{MUT}" '
                 f'transform="rotate(-90 14 {(YT + YB) / 2})">{ynavn}</text>')
    if xnavn:
        s.append(f'<text x="{(X0 + X1) / 2}" y="{H - 5}" text-anchor="middle" '
                 f'fill="{MUT}">{xnavn}</text>')
    s.append('</svg>')
    return ''.join(s)


def potenslinje(navne, punkter=(), W=680, H=170):
    """Logaritmisk tallinje fra 10^0 og op, med navne og nedslag.

    navne    [(eksponent, 'Million'), ...]      mærker over linjen
    punkter  [(tal, 'SpaceX 2002'), ...]        nedslag under linjen
    Positionen beregnes af eksponenten, saa afstanden mellem million og
    milliard er praecis lige saa lang som mellem milliard og billion.
    """
    hi = max(e for e, _ in navne)
    X0, X1, Y = 40, W - 40, 74
    def x(e):
        return X0 + (X1 - X0) * e / hi
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" style="max-width:{W}px" '
         f'xmlns="http://www.w3.org/2000/svg" {FONT}>',
         f'<line x1="{X0}" y1="{Y}" x2="{X1}" y2="{Y}" stroke="{INK}" stroke-width="1.5"/>']
    for e in range(0, hi + 1, 3):
        s.append(f'<line x1="{x(e):.1f}" y1="{Y - 5}" x2="{x(e):.1f}" y2="{Y + 5}" '
                 f'stroke="{INK}"/>')
        s.append(f'<text x="{x(e):.1f}" y="{Y + 20}" text-anchor="middle" fill="{MUT}">'
                 f'10<tspan dy="-4" font-size="8">{e}</tspan></text>')
    for e, navn in navne:
        s.append(f'<line x1="{x(e):.1f}" y1="{Y - 5}" x2="{x(e):.1f}" y2="{Y - 26}" '
                 f'stroke="{BLA}"/>')
        s.append(f'<text x="{x(e):.1f}" y="{Y - 31}" text-anchor="middle" fill="{BLA}" '
                 f'font-weight="bold" transform="rotate(-32 {x(e):.1f} {Y - 31})">'
                 f'{navn}</text>')
    for v, navn in punkter:
        e = math.log10(v)
        s.append(f'<circle cx="{x(e):.1f}" cy="{Y}" r="4.5" fill="{ORA}"/>')
        s.append(f'<line x1="{x(e):.1f}" y1="{Y + 26}" x2="{x(e):.1f}" y2="{Y + 46}" '
                 f'stroke="{ORA}" stroke-dasharray="2 2"/>')
        s.append(f'<text x="{x(e):.1f}" y="{Y + 60}" text-anchor="middle" fill="{ORA}">'
                 f'{navn}</text>')
    s.append('</svg>')
    return ''.join(s)
