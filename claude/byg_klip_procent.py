# -*- coding: utf-8 -*-
"""Bygger materiale/klip-procenten-fri.pdf og vejledning/…-svar.pdf

Syvende ark i raekken, og det andet uden geometri. Procent er svaert at
huske, fordi det er tre ting paa én gang: en braek, et decimaltal og et
ord. Her bliver de tre ting det samme stykke papir.

  A  Hundredefeltet -> 100 felter klippet i fire stykker: 50, 25, 20 og 5.
                       Hvert stykke har tre navne, og de fire procenter
                       laegger sig til 100.
  B  Strimlerne     -> tre strimler af forskellig laengde foldes paa midten
                       tre gange. Procenten er den samme, stykket er ikke:
                       25 % af 60 er 15, ikke 25.
  C  Ned og op igen -> en strimmel falder 50 % og stiger 50 %. Den bliver
                       ikke 100 igen. Den bliver 75, og de 25 mm, der
                       mangler, kan holdes op mod den urerte strimmel.

**Laengderne er valgt, saa en ottendedel kan maales.** 100, 60 og 80 mm
giver 12,5 · 7,5 · 10 mm — alle paa en halv millimeter. En strimmel paa
fx 70 mm ville give 8,75 mm, og saa er oevelsen et gaet.

**Oevelsen taaler, at printeren skalerer.** Bliver alt 4 % mindre, er
halvdelen stadig halvdelen. Kun mm-tallene flytter sig, og dem maaler
ungen selv.

    python3 claude/byg_klip_procent.py
"""
import importlib.util
import os
import subprocess
from fractions import Fraction as F

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HER = os.path.dirname(os.path.abspath(__file__))

_spec = importlib.util.spec_from_file_location(
    'rumfang', os.path.join(HER, 'byg_klip_rumfang.py'))
RF = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(RF)

svg = RF.svg
INK, LIN, BLA, LYS = RF.INK, RF.LIN, RF.BLA, RF.LYS
KLIP = RF.KLIP
CSS = RF.CSS

# ------------------------------------------------------------------ A · feltet
CELLE = 12                       # mm pr. felt
RAEKKER = KOLONNER = 10
FELT = CELLE * RAEKKER           # 120 mm
assert FELT <= RF.PLADS_B, 'hundredefeltet er bredere end papiret'
assert RAEKKER * KOLONNER == 100, 'det skal vaere hundrede felter'

# De fire stykker, feltet klippes i. De skal kunne klippes langs
# ternlinjerne, og de skal laegge sig til praecis 100.
STYKKER = [
    ('Det store', 50, '5 rækker'),
    ('Det næststørste', 25, '5 × 5 felter'),
    ('Det tredje', 20, '4 rækker à 5'),
    ('Det mindste', 5, '1 række à 5'),
]
assert sum(a for _, a, _ in STYKKER) == 100, 'stykkerne skal give 100 felter'
assert len({a for _, a, _ in STYKKER}) == len(STYKKER), 'to stykker er ens'
# Hvert stykke skal give en braek, der kan forkortes pænt.
BROEK = {a: F(a, 100) for _, a, _ in STYKKER}
for _a, _f in BROEK.items():
    assert _f.denominator <= 20, f'{_a}/100 forkorter ikke pænt'

# ------------------------------------------------------------- B og C · strimler
STRIMMELH = 14                   # mm
B_STRIMLER = [('P', 100), ('Q', 60), ('R', 80)]
C_STRIMLER = [('U', 100), ('V', 100)]
RESERVE = [('', 100), ('', 100), ('', 60), ('', 80)]
FOLDNINGER = [(2, '50 %'), (4, '25 %'), (8, '12,5 %')]

# En ottendedel skal kunne maales paa en almindelig lineal: tallet skal gaa
# op i en halv millimeter. Det er grunden til, at der ikke staar 70 mm.
for _navn, _L in B_STRIMLER:
    for _d, _ in FOLDNINGER:
        assert (F(_L, _d) * 2).denominator == 1, \
            f'{_navn}: {_L}/{_d} kan ikke maales ({F(_L, _d)} mm)'

DEL = {navn: {d: F(L, d) for d, _ in FOLDNINGER} for navn, L in B_STRIMLER}

# C: ned 50 % og op 50 %. Regnes, aldrig gaettes.
C_START = F(C_STRIMLER[1][1])
C_EFTER_FALD = C_START * (1 - F(1, 2))
C_EFTER_STIGNING = C_EFTER_FALD * (1 + F(1, 2))
C_MANGLER = C_START - C_EFTER_STIGNING
assert C_EFTER_STIGNING == 75 and C_MANGLER == 25
# Den omvendte raekkefoelge giver det samme — det er hele pointen.
assert C_START * (1 + F(1, 2)) * (1 - F(1, 2)) == C_EFTER_STIGNING


def _tal(v):
    """Dansk tal: komma, og ingen decimaler naar der ikke er nogen."""
    f = F(v)
    if f.denominator == 1:
        return str(f.numerator)
    s = f'{float(f):.4f}'.rstrip('0').rstrip('.')
    return s.replace('.', ',')


# ------------------------------------------------------------------- figurer
def hundredefelt():
    """Ti gange ti felter. Alle linjer er klippelinjer og vejer det samme —
    ingen af dem roeber, hvor de fire stykker gaar."""
    k = [f'<rect x="0" y="0" width="{FELT}" height="{FELT}" {KLIP} '
         f'stroke-width="0.7"/>']
    for i in range(1, KOLONNER):
        x = i * CELLE
        k.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{FELT}" {KLIP}/>')
    for i in range(1, RAEKKER):
        y = i * CELLE
        k.append(f'<line x1="0" y1="{y}" x2="{FELT}" y2="{y}" {KLIP}/>')
    return svg(''.join(k), [(0, 0), (FELT, FELT)])


def strimler(liste, note=''):
    """Strimlerne ligger under hinanden. Laengden staar ikke paa dem:
    den skal maales, ellers er der ikke noget at finde ud af."""
    GAB = 7
    k, pkt = [], []
    y = 0
    for navn, L in liste:
        k.append(f'<rect x="0" y="{y}" width="{L}" height="{STRIMMELH}" '
                 f'rx="1" {KLIP}/>')
        # Maalene i figuren er millimeter, ogsaa skriftstoerrelsen:
        # 9 her ville give et bogstav paa 9 mm.
        k.append(f'<text x="4" y="{y + STRIMMELH / 2 + 1.5:.1f}" '
                 f'font-size="4.2" font-weight="700" fill="{INK}">'
                 f'{navn}</text>')
        pkt += [(0, y), (L, y + STRIMMELH)]
        y += STRIMMELH + GAB
    if note:
        k.append(f'<text x="0" y="{y + 1:.1f}" font-size="2.8" '
                 f'fill="#586074">{note}</text>')
        pkt.append((0, y + 4))
    return svg(''.join(k), pkt)


# ------------------------------------------------------------------ klippearket
stykke_li = ''.join(
    f'<li><b>{navn.lower()}</b> på <b>{a}</b> felter ({form})</li>'
    for navn, a, form in STYKKER)

KLIPARK = (
 '<h1 class="smal">Klip procenten fri</h1>'
 '<p class="hvad">Procent betyder <b>hundrededele</b>. Det er ikke en '
 'forklaring, man skal tro på — det er noget, der kan klippes ud og '
 'tælles efter.</p>'
 '<h2>A · Hundredefeltet</h2>'
 '<p class="hvad" style="margin-bottom:1mm">Klip feltet ud, og klip '
 'det så i fire stykker:</p>'
 f'<ul class="hvad" style="margin:0 0 2mm;padding-left:5mm">{stykke_li}</ul>'
 '<p class="hvad">Klip kun langs stregerne. Skriv bagpå hvert stykke, '
 'hvor mange felter det har.</p>'
 f'<div class="net">{hundredefelt()}</div>'
 '<div class="ny"></div>'
 '<h2 style="margin-top:0">B · Strimlerne</h2>'
 '<p class="hvad">Klip de tre strimler ud. Mål hver enkelt, før du gør '
 'noget ved den — og skriv længden ned.</p>'
 f'<div class="net">{strimler(B_STRIMLER)}</div>'
 '<h2>C · Ned og op igen</h2>'
 '<p class="hvad">To ens strimler. <b>U skal ikke klippes</b> — den er '
 'det, du måler op imod til sidst.</p>'
 f'<div class="net">{strimler(C_STRIMLER)}</div>'
 '<h2>Reserve</h2>'
 '<p class="hvad">Klipper du forkert, så tag en herfra. De to øverste '
 'er lige så lange som U og V, de to nederste som Q og R.</p>'
 f'<div class="net">{strimler(RESERVE)}</div>'
 '<footer>Strimlerne er trykt i rigtig størrelse. Skalerer printeren, '
 'passer millimetrene ikke — men halvdelen er stadig halvdelen, og '
 'procenterne holder. Mål selv, og brug dine egne tal.</footer>')

# ------------------------------------------------------------------- arbejdsark
TRIN = [
 ('A', 'Hundredefeltet',
  ['Tæl felterne i hvert af de fire stykker.',
   'Skriv for hvert stykke: brøken ud af 100, brøken forkortet, '
   'decimaltallet og procenten.',
   'Læg det næststørste stykke oven på det største.'],
  'Hvor stor en del af det store stykke dækker det næststørste?',
  ['Læg alle fire stykker sammen igen. Hvad giver de fire procenter '
   'tilsammen — og hvorfor kunne du have vidst det på forhånd?'],
  'Procent betyder:'),
 ('B', 'Strimlerne',
  ['Mål P, Q og R. Skriv længderne i skemaet.',
   'Fold hver strimmel på midten. Mål. Det er 50 %.',
   'Fold igen. Mål. Det er 25 %. Fold en tredje gang: 12,5 %.'],
  'De tre strimler er 25 % lange hver for sig — hvorfor er stykkerne '
  'ikke lige store?',
  ['Hvad gjorde du i virkeligheden ved tallet, hver gang du foldede på '
   'midten? Og hvad gør man så ved et tal for at finde 25 % af det?'],
  'For at finde 25 % af et tal skal man:'),
 ('C', 'Ned og op igen',
  ['Fold V på midten og klip. V er nu faldet 50 %. Mål V.',
   'Nu skal V stige 50 %. Fold det afklippede stykke på midten, klip, '
   'og tape den ene halvdel på V.',
   'Hold V op mod U, som du ikke har rørt.'],
  'V er faldet 50 % og bagefter steget 50 %. Hvorfor er V ikke lige så '
  'lang som U igen?',
  ['Hvor mange millimeter mangler der? Og hvor mange procent af U er V '
   'nu?',
   'Prøv det den anden vej i hovedet: først op 50 %, så ned 50 %. '
   'Hvad ender du på?'],
  'Procenten regnes altid af:'),
]

SKEMA = (
 '<table class="regn"><tbody>'
 '<tr><td class="nr">&nbsp;</td><td><b>Hel strimmel</b></td>'
 + ''.join(f'<td><b>{p}</b></td>' for _, p in FOLDNINGER) + '</tr>'
 + ''.join(f'<tr><td class="nr">{navn}</td><td class="plads"></td>'
           + '<td class="plads"></td>' * len(FOLDNINGER) + '</tr>'
           for navn, _ in B_STRIMLER)
 + '</tbody></table>')

NAVNE = (
 '<table class="regn"><tbody>'
 '<tr><td class="nr">&nbsp;</td><td><b>Felter</b></td>'
 '<td><b>Brøk ud af 100</b></td><td><b>Forkortet</b></td>'
 '<td><b>Decimaltal</b></td><td><b>Procent</b></td></tr>'
 + ''.join(f'<tr><td class="nr">{i}</td>'
           + '<td class="plads"></td>' * 5 + '</tr>'
           for i in range(1, len(STYKKER) + 1))
 + '</tbody></table>')

# ------------------------------------------------------------------ regn videre
# Alt regnes med Fraction. Intet af det her er regnet i hovedet.
REGN = [
 ('Hvor mange er 25 % af 60?', F(25, 100) * 60),
 ('Hvor mange procent er 15 af 60?', F(15, 60) * 100),
 ('En trøje koster 400 kr. og sættes ned med 30 %. Hvad koster den nu?',
  400 * (1 - F(30, 100))),
 ('En billet stiger fra 80 kr. til 100 kr. Hvor mange procent er den steget?',
  F(100 - 80, 80) * 100),
 ('Hvor mange er 12,5 % af 240?', F(125, 1000) * 240),
 ('En vare koster 500 kr. Prisen stiger 20 % og falder bagefter 20 %. '
  'Hvad koster varen til sidst?', 500 * (1 + F(20, 100)) * (1 - F(20, 100))),
 ('3/8 af en klasse på 24 unger spiller fodbold. Hvor mange er det, '
  'og hvor mange procent?', F(3, 8) * 24),
 ('Skriv 1/20 som procent.', F(1, 20) * 100),
]
SVAR_REGN = [
 f'{_tal(REGN[0][1])}',
 f'{_tal(REGN[1][1])} %',
 f'{_tal(REGN[2][1])} kr.',
 f'{_tal(REGN[3][1])} %',
 f'{_tal(REGN[4][1])}',
 f'{_tal(REGN[5][1])} kr. — ikke 500',
 f'{_tal(REGN[6][1])} unger · {_tal(F(3, 8) * 100)} %',
 f'{_tal(REGN[7][1])} %',
]
assert len(SVAR_REGN) == len(REGN)
assert REGN[5][1] == 480, 'op og ned med samme procent giver ikke det samme'
assert REGN[6][1] == 9 and F(3, 8) * 100 == F(75, 2)

trin_html = ''.join(
    f'<div class="gr"><div class="bogstav">{b}</div><div>'
    f'<p class="navn">{navn}</p><ol>'
    + ''.join(f'<li>{t}</li>' for t in gor) + '</ol>'
    + (NAVNE if b == 'A' else SKEMA if b == 'B' else '')
    + f'<p class="sp">{spm}</p><div class="linje"></div>'
    + ''.join(f'<p style="margin:2mm 0 0;color:#333">{t}</p>'
              f'<div class="linje"></div>' for t in under)
    + f'<div class="boks"><b>{formel}</b>'
      f'<div class="linje"></div><div class="linje"></div></div>'
    '</div></div>'
    for b, navn, gor, spm, under, formel in TRIN)

regn_html = ''.join(
    f'<tr><td class="nr">{i}</td><td>{t}</td><td class="plads"></td></tr>'
    for i, (t, _) in enumerate(REGN, 1))

ARBEJD = ('<div class="ny"></div><h1>Hvad fandt du ud af?</h1>'
          '<p class="lead">Et hundredefelt, fem strimler og en saks. Der '
          'står ingen regler nogen steder — dem skal du klippe og folde '
          'dig frem til. Udfyld undervejs, og svar med dine egne mål.</p>'
          + trin_html
          + '<div class="ny"></div><h1>Regn videre</h1>'
            '<p class="lead">Nu har du selv fundet ud af, hvad procent er. '
            'Brug det. Skriv hvordan du regner — ikke kun hvad der '
            'kommer ud.</p>'
            f'<table class="regn"><tbody>{regn_html}</tbody></table>'
            '<footer>Husk enheden. 25 er ikke det samme som 25 %, og '
            '25 % af 60 er hverken 25 eller 60.</footer>')

# ------------------------------------------------------------------ svararket
navne_svar = ''.join(
    f'<tr><td class="nr">{i}</td><td>{a}</td><td>{a}/100</td>'
    f'<td>{BROEK[a].numerator}/{BROEK[a].denominator}</td>'
    f'<td>{_tal(F(a, 100))}</td><td>{a} %</td></tr>'
    for i, (_, a, _f) in enumerate(STYKKER, 1))

skema_svar = ''.join(
    f'<tr><td class="nr">{navn}</td><td>{L} mm</td>'
    + ''.join(f'<td>{_tal(DEL[navn][d])} mm</td>' for d, _ in FOLDNINGER)
    + '</tr>' for navn, L in B_STRIMLER)

regn_svar = ''.join(
    f'<tr><td class="nr">{i}</td><td>{t}</td><td class="plads"><b>{s}</b>'
    f'</td></tr>'
    for i, ((t, _), s) in enumerate(zip(REGN, SVAR_REGN), 1))

VEJL = (
 '<h1>Klip procenten fri · forventede svar</h1>'
 '<p class="lead">Til den voksne. Arket uddeles uden denne side.</p>'
 '<div class="boks"><b>Hvad øvelsen gør.</b> Procent læres som en '
 'opskrift — gang med 100, eller del med 100, og hvem kan huske hvilken. '
 'Her er procenten ikke en opskrift: den er et stykke papir. Hundrede '
 'felter klippes i fire, og det samme stykke har tre navne på én gang. '
 'Bagefter viser strimlerne, at procenten er et <b>forhold</b>, ikke et '
 'antal — og til sidst, at den altid regnes af det, der står nu.</div>'
 '<h2>A · Hundredefeltet</h2>'
 '<table class="regn"><tbody>'
 '<tr><td class="nr">&nbsp;</td><td><b>Felter</b></td>'
 '<td><b>Ud af 100</b></td><td><b>Forkortet</b></td>'
 '<td><b>Decimaltal</b></td><td><b>Procent</b></td></tr>'
 + navne_svar + '</tbody></table>'
 '<p class="hvad">Det næststørste stykke (25) dækker præcis <b>halvdelen</b> '
 'af det store (50). En fjerdedel er halvdelen af en halvdel — det kan '
 'ses, ikke kun regnes. De fire procenter giver <b>100 %</b>, fordi de '
 'fire stykker tilsammen <i>er</i> hele feltet. Det er derfor, procent '
 'findes: det hele er altid 100.</p>'
 '<h2>B · Strimlerne</h2>'
 '<table class="regn"><tbody>'
 '<tr><td class="nr">&nbsp;</td><td><b>Hel</b></td>'
 + ''.join(f'<td><b>{p}</b></td>' for _, p in FOLDNINGER) + '</tr>'
 + skema_svar + '</tbody></table>'
 '<p class="hvad">Alle tre stykker er 25 % — og de er forskellige. '
 'Procenten siger, <i>hvor stor en del</i>, ikke <i>hvor meget</i>. '
 'Det, de gjorde hver gang de foldede, var at <b>dele med 2</b>, og '
 'derfor er 25 % det samme som at dele med 4. Den sætning er mere værd '
 'end formlen.</p>'
 '<div class="ny"></div>'
 '<h2 style="margin-top:0">C · Ned og op igen</h2>'
 f'<p class="hvad">U er {_tal(C_START)} mm. V falder 50 % og bliver '
 f'{_tal(C_EFTER_FALD)} mm. V stiger 50 % — men nu er 50 % kun '
 f'{_tal(C_EFTER_FALD / 2)} mm, for procenten regnes af de '
 f'{_tal(C_EFTER_FALD)}, ikke af de {_tal(C_START)}. V ender på '
 f'<b>{_tal(C_EFTER_STIGNING)} mm</b>, og der mangler '
 f'<b>{_tal(C_MANGLER)} mm</b>. V er {_tal(C_EFTER_STIGNING)} % af U.</p>'
 '<p class="hvad">Den anden vej rundt giver det samme: 100 op 50 % er '
 '150, og 150 ned 50 % er 75. Rækkefølgen er lige meget — faldet er '
 'altid størst, fordi det regnes af det største tal.</p>'
 '<div class="boks"><b>Det, der driller.</b> De siger «ned 50 og op 50 '
 'ophæver hinanden», og det lyder rigtigt. Lad dem måle i stedet for at '
 'diskutere: de 25 mm er der eller ikke der. De blander også procent og '
 'antal — «25 % af 60 er 25». Hold de tre 25 %-stykker fra B op ved '
 'siden af hinanden; de er 25, 15 og 20 mm, og så er den diskussion '
 'slut. Til sidst: <b>procentpoint</b> hører ikke til her, men kommer '
 'lige efter — gemmer de spørgsmålet, er det et godt tegn.</div>'
 '<h2>Regn videre</h2>'
 f'<table class="regn"><tbody>{regn_svar}</tbody></table>'
 f'<footer>Hundredefeltet er {FELT} × {FELT} mm, altså {CELLE} mm pr. '
 f'felt. Strimlerne er {", ".join(str(L) for _, L in B_STRIMLER)} og '
 f'2 × {C_STRIMLER[0][1]} mm. Længderne er valgt, så en ottendedel kan '
 f'måles: 12,5 · 7,5 · 10 mm. En strimmel på 70 mm ville give 8,75 mm, '
 f'og så er øvelsen et gæt.</footer>')


def skriv(navn, krop):
    sti = os.path.join(ROD, navn)
    h = sti.replace('.pdf', '.html')
    os.makedirs(os.path.dirname(sti), exist_ok=True)
    open(h, 'w', encoding='utf-8').write(
        '<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
        '<title>Klip procenten fri</title><style>' + CSS
        + '</style></head><body>' + krop + '</body></html>')
    subprocess.run(['node', os.path.join(ROD, 'claude', 'html_til_pdf.mjs'),
                    h, sti], check=True, stdout=subprocess.DEVNULL)
    os.remove(h)
    print('skrevet: ', sti)


if __name__ == '__main__':
    skriv('materiale/klip-procenten-fri.pdf', KLIPARK + ARBEJD)
    skriv('vejledning/klip-procenten-fri-svar.pdf', VEJL)
    print(' · '.join(f'{n}: {_tal(DEL[n][4])} mm er 25 %'
                     for n, _ in B_STRIMLER)
          + f' · V ender på {_tal(C_EFTER_STIGNING)} mm')
