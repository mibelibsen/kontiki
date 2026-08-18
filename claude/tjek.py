#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tjekker sitet for de fejl, der rent faktisk er sket i dette projekt.

Koer den foer hvert push:

    python3 claude/tjek.py

Hver kontrol svarer til en konkret fejl fra projektets historie. Scriptet har
ingen afhaengigheder ud over Pythons standardbibliotek, saa det virker i en
frisk session uden installation.

Afslutter med kode 0 hvis alt er i orden, ellers 1.
"""
import os, re, sys, glob, zipfile, html
from collections import Counter

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROD)

FEJL, ADVARSEL, OK = [], [], []


def fejl(kontrol, besked):
    FEJL.append((kontrol, besked))


def advar(kontrol, besked):
    ADVARSEL.append((kontrol, besked))


def ok(kontrol, besked):
    OK.append((kontrol, besked))


def sider():
    """Alle HTML-sider der udgives (dvs. i roden)."""
    return sorted(glob.glob('*.html'))


def alle_html():
    return sorted(glob.glob('*.html') + glob.glob('kommende/*.html'))


def tekst(fil):
    return open(fil, encoding='utf-8').read()


# ---------------------------------------------------------------------------
# 1. Sitet maa aldrig hente CSS eller JS fra roden
#    (manipulation.html laa ustylet med doed quiz, fordi den gjorde det)
# ---------------------------------------------------------------------------
def tjek_selvbaerende():
    synder = []
    for f in alle_html():
        h = tekst(f)
        for m in re.finditer(r'(?:href|src)="(/[^"]+\.(?:css|js))"', h):
            synder.append(f'{f} henter {m.group(1)}')
        if '<style' not in h:
            synder.append(f'{f} har ingen inline <style>')
    if synder:
        for s in synder:
            fejl('selvbærende sider', s)
    else:
        ok('selvbærende sider', f'{len(alle_html())} sider har inline CSS og henter intet fra roden')


# ---------------------------------------------------------------------------
# 2. Facit maa aldrig kunne udgives
# ---------------------------------------------------------------------------
def tjek_facit_skjult():
    if not os.path.exists('.vercelignore'):
        fejl('facit skjult', '.vercelignore findes ikke — alt i repoet udgives')
        return
    ignoreret = {l.strip().rstrip('/') for l in open('.vercelignore', encoding='utf-8')
                 if l.strip() and not l.startswith('#')}
    for mappe in ('facit', 'kommende', 'lektieark', 'claude'):
        if os.path.isdir(mappe) and mappe not in ignoreret:
            fejl('facit skjult', f'mappen {mappe}/ er IKKE udelukket i .vercelignore')
    # ingen facit-filer i roden
    for f in glob.glob('*facit*') + glob.glob('*Facit*'):
        if os.path.isfile(f):
            fejl('facit skjult', f'{f} ligger i roden og ville blive udgivet')
    if not FEJL:
        ok('facit skjult', 'facit/, kommende/, lektieark/ og claude/ er udelukket fra deploy')


# ---------------------------------------------------------------------------
# 3. Lektier er altid aabne opgaver — aldrig multiple choice
# ---------------------------------------------------------------------------
def tjek_lektier_uden_mc():
    lektier = [f for f in alle_html() if os.path.basename(f).startswith('lektier-')]
    if not lektier:
        advar('lektier uden multiple choice', 'ingen lektieark fundet')
        return
    for f in lektier:
        h = tekst(f)
        h_uden_css = re.sub(r'(?s)<style.*?</style>', '', h)
        traf = re.findall(r'class="[^"]*\b(opt|bx|mk)\b', h_uden_css)
        if traf:
            fejl('lektier uden multiple choice',
                 f'{f} har {len(traf)} multiple choice-elementer')
    if not any(k == 'lektier uden multiple choice' for k, _ in FEJL):
        ok('lektier uden multiple choice', f'{len(lektier)} lektieark, ingen afkrydsning')


# ---------------------------------------------------------------------------
# 4. Besvarelsesformuleringen skal vaere den aftalte
# ---------------------------------------------------------------------------
METODE = 'Lav udregninger i Word med Geogebra eller Excel og vis din metode.'
FORBUDT = ['i dit hæfte', 'på linjerne', 'stykke papir']


def tjek_metodetekst():
    lektier = [f for f in alle_html() if os.path.basename(f).startswith('lektier-')]
    for f in lektier:
        if METODE not in tekst(f):
            fejl('metodetekst', f'{f} mangler den aftalte formulering')
    for f in alle_html():
        h = tekst(f)
        for forbudt in FORBUDT:
            if forbudt in h:
                fejl('metodetekst', f'{f} bruger den gamle formulering "{forbudt}"')
    if not any(k == 'metodetekst' for k, _ in FEJL):
        ok('metodetekst', f'{len(lektier)} lektieark bruger den aftalte formulering')


# ---------------------------------------------------------------------------
# 5. Ingen brudte links
# ---------------------------------------------------------------------------
def tjek_links():
    brudte = 0
    for f in alle_html():
        # filer i kommende/ flyttes op i roden, naar de udgives — deres
        # relative links skal derfor maales fra roden, ikke fra mappen
        mappe = '.' if f.startswith('kommende/') else (os.path.dirname(f) or '.')
        for href in set(re.findall(r'href="([^"#][^"]*)"', tekst(f))):
            if href.startswith(('http', 'mailto:')):
                continue
            maal = href.split('#')[0]
            if not maal:
                continue
            sti = maal.lstrip('/') if maal.startswith('/') else os.path.join(mappe, maal)
            if not os.path.exists(sti):
                fejl('links', f'{f} → {href}')
                brudte += 1
    if not brudte:
        ok('links', 'ingen brudte links')


# ---------------------------------------------------------------------------
# 6. Hver side skal have mindst én figur (reglen om visuelle eksempler)
# ---------------------------------------------------------------------------
UDEN_KRAV = {'index.html', 'matematik.html', 'samfundsfag.html', 'tysk.html',
             'aarsplan-matematik.html'}


def tjek_figurer():
    mangler = [f for f in alle_html()
               if os.path.basename(f) not in UDEN_KRAV and '<svg' not in tekst(f)]
    if mangler:
        for f in mangler:
            fejl('visuelle eksempler', f'{f} har ingen figur')
    else:
        n = sum(tekst(f).count('<svg') for f in alle_html())
        ok('visuelle eksempler', f'{n} figurer fordelt på siderne')


# ---------------------------------------------------------------------------
# 7. Quiz-motorens kontrakt skal vaere opfyldt paa de interaktive sider
# ---------------------------------------------------------------------------
IDER = ['startOverlay', 'nameInput', 'ovTitle', 'ovText', 'startBtn', 'skipBtn',
        'resetBtn', 'switchBtn', 'welcomeBar', 'welcomeHi', 'welcomeLive',
        'progressFill', 'progressLabel', 'resultsBody', 'gradeMsg', 'finalMsg']


def tjek_quizmotor():
    interaktive = [f for f in sider() if 'class="quiz"' in tekst(f)]
    for f in interaktive:
        h = tekst(f)
        savn = [i for i in IDER if f'id="{i}"' not in h]
        if savn:
            fejl('quiz-motor', f'{f} mangler id: {", ".join(savn)}')
        markup = re.sub(r'(?s)<script.*?</script>', '', h)
        quizzer = len(re.findall(r'class="quiz"', markup))
        badges = markup.count('data-score')
        if quizzer != badges:
            fejl('quiz-motor', f'{f} har {quizzer} quizzer men {badges} score-badges')
        moduler = re.search(r'data-modules="([^"]*)"', markup)
        if moduler and len(moduler.group(1).split('|')) != quizzer:
            fejl('quiz-motor',
                 f'{f}: data-modules har {len(moduler.group(1).split("|"))} navne '
                 f'men siden har {quizzer} quizzer')
    if not any(k == 'quiz-motor' for k, _ in FEJL):
        ok('quiz-motor', f'{len(interaktive)} interaktive sider opfylder kontrakten')


# ---------------------------------------------------------------------------
# 8. Aarsplanen findes to steder — de skal sige det samme
#    (tre gange i dag blev kun det ene sted rettet)
# ---------------------------------------------------------------------------
def xlsx_tekster(sti):
    """Alle strenge i et regneark, uden afhaengigheder."""
    ud = []
    with zipfile.ZipFile(sti) as z:
        delte = []
        if 'xl/sharedStrings.xml' in z.namelist():
            s = z.read('xl/sharedStrings.xml').decode('utf-8')
            delte = [html.unescape(re.sub(r'<[^>]+>', '', m))
                     for m in re.findall(r'<si>(.*?)</si>', s, re.S)]
        for navn in z.namelist():
            if not re.match(r'xl/worksheets/sheet\d+\.xml', navn):
                continue
            s = z.read(navn).decode('utf-8')
            for c in re.finditer(r'<c[^>]*?(?: t="(\w+)")?[^>]*>(.*?)</c>', s, re.S):
                typ, krop = c.group(1), c.group(2)
                v = re.search(r'<v>(.*?)</v>', krop, re.S)
                if not v:
                    isx = re.search(r'<is>(.*?)</is>', krop, re.S)
                    if isx:
                        ud.append(html.unescape(re.sub(r'<[^>]+>', '', isx.group(1))))
                    continue
                raa = v.group(1)
                if typ == 's':
                    i = int(raa)
                    if i < len(delte):
                        ud.append(delte[i])
                else:
                    ud.append(html.unescape(raa))
    return ud


def tjek_aarsplan():
    side, ark = 'aarsplan-matematik.html', 'aarsplan-matematik-2026-27.xlsx'
    if not (os.path.exists(side) and os.path.exists(ark)):
        advar('årsplan', 'siden eller regnearket findes ikke — springer over')
        return
    h = tekst(side)
    uger_side = [t.strip() for t in re.findall(r'<td class="uge">([^<]+)</td>', h)]
    forloeb_side = [html.unescape(t) for t in re.findall(
        r'<td class="uge">[^<]+</td><td class="per">[^<]*</td><td>([^<]+)</td>', h)]

    celler = xlsx_tekster(ark)
    # ugenumre i regnearket: rene tal der ogsaa staar paa siden
    uger_ark = [c for c in celler if c.strip().isdigit() and c.strip() in uger_side]

    if uger_side != uger_ark:
        fejl('årsplan side↔regneark',
             f'ugerækkefølgen afviger\n      side: {" ".join(uger_side)}'
             f'\n      ark : {" ".join(uger_ark)}')
    else:
        ok('årsplan side↔regneark', f'{len(uger_side)} uger i samme rækkefølge begge steder')

    mangler = [f for f in forloeb_side if f.strip() and f.strip() not in
               {c.strip() for c in celler}]
    if mangler:
        fejl('årsplan side↔regneark',
             'forløb på siden findes ikke i regnearket: ' + ', '.join(mangler))
    else:
        ok('årsplan side↔regneark', f'alle {len(forloeb_side)} forløb findes begge steder')

    # ferier og afbrydelser skal naevnes ens
    for m in re.finditer(r'<tr class="break"><td colspan="5">([^<]+)</td></tr>', h):
        t = html.unescape(m.group(1))
        uge = re.match(r'(Uge [\d\s\-]+)', t)
        if not uge:
            continue
        nr = uge.group(1).strip()
        if not any(nr in c or nr.replace(' - ', '-') in c for c in celler):
            advar('årsplan side↔regneark',
                  f'"{nr}" står på siden, men ikke tydeligt i regnearket')


# ---------------------------------------------------------------------------
# 9. Facit- og lektiearks-filnavne skal foelge moenstret
# ---------------------------------------------------------------------------
def tjek_filnavne():
    for f in glob.glob('facit/*.pdf'):
        n = os.path.basename(f)
        if not re.match(r'facit-(online|lektier)-\d{4}-\d{2}-\d{2}-[a-z0-9-]+\.pdf$', n):
            advar('filnavne', f'facit/{n} følger ikke facit-<serie>-<ÅÅÅÅ-MM-DD>-<emne>.pdf')
    for f in glob.glob('lektieark/*.pdf'):
        n = os.path.basename(f)
        if 'facit' in n.lower():
            fejl('filnavne', f'lektieark/{n} har ordet "facit" i navnet')
        if not re.match(r'lektier-\d{4}-\d{2}-\d{2}-[a-z0-9-]+\.pdf$', n):
            advar('filnavne', f'lektieark/{n} følger ikke lektier-<ÅÅÅÅ-MM-DD>-<emne>.pdf')
    if not any(k == 'filnavne' for k, _ in FEJL):
        ok('filnavne', f'{len(glob.glob("facit/*.pdf"))} facit og '
                       f'{len(glob.glob("lektieark/*.pdf"))} lektieark navngivet efter mønstret')


# ---------------------------------------------------------------------------
def main():
    for f in (tjek_selvbaerende, tjek_facit_skjult, tjek_lektier_uden_mc,
              tjek_metodetekst, tjek_links, tjek_figurer, tjek_quizmotor,
              tjek_aarsplan, tjek_filnavne):
        try:
            f()
        except Exception as e:
            fejl(f.__name__, f'kontrollen kunne ikke køre: {e!r}')

    print('=' * 72)
    for k, b in OK:
        print(f'  OK       {k:26} {b}')
    for k, b in ADVARSEL:
        print(f'  ADVARSEL {k:26} {b}')
    for k, b in FEJL:
        print(f'  FEJL     {k:26} {b}')
    print('=' * 72)
    print(f'  {len(OK)} i orden · {len(ADVARSEL)} advarsler · {len(FEJL)} fejl')
    if FEJL:
        print('\n  Ret fejlene før du pusher.')
        return 1
    print('\n  Klar til push.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
