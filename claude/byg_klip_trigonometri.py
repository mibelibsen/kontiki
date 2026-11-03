# -*- coding: utf-8 -*-
"""Bygger materiale/klip-trigonometri-fri.pdf og vejledning/…-svar.pdf

Femte ark i raekken. De fire foerste klippede en formel frem; her er der
ikke en formel at klippe. Til gengaeld er der en paastand, som saksen kan
afgoere, og som hele trigonometrien hviler paa:

    forholdet mellem siderne afhaenger KUN af vinklen - ikke af, hvor
    stor trekanten er.

  A  Fem trekanter  -> fire har samme vinkel, én har ikke. Klip dem ud,
                       stak dem, maal dem. Fire giver det samme tal, én
                       giver et andet - og tallet afsloerer den, foer
                       oejet goer
  B  De tre forhold -> samme maaling paa tre kendte vinkler, og saa
                       sammenligningen med det, lommeregneren kalder
                       sin, cos og tan. Det er de samme tal
  C  Den hoejde, du -> 35°-trekanten bliver et sigteinstrument. Hoejden
     ikke kan naa      er oejenhoejde + 0,70 · afstand, og 0,70 er det
                       tal, de selv maalte i A

    python3 claude/byg_klip_trigonometri.py

Figurerne staar i millimeter: der skal maales paa dem med lineal, saa
arket SKAL printes i 100 %.
"""
import importlib.util
import math
import os
import subprocess

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HER = os.path.dirname(os.path.abspath(__file__))

_spec = importlib.util.spec_from_file_location(
    'rumfang', os.path.join(HER, 'byg_klip_rumfang.py'))
RF = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(RF)

svg, kom = RF.svg, RF.kom
INK, LIN, BLA, LYS = RF.INK, RF.LIN, RF.BLA, RF.LYS
KLIP = RF.KLIP
PLADS_B = RF.PLADS_B

V = 35                      # vinklen i A og C
FALSK = 42                  # den femte trekant, der ikke hoerer til
GAB = 6                     # luft mellem brikkerne, saa saksen kan komme til

TAN_V = math.tan(math.radians(V))
assert abs(TAN_V - 0.70) < 0.005, 'tan(V) skal ligge taet paa 0,70, ellers ' \
                                  'bliver regnestykket i C ikke paent'


# ---------------------------------------------------------------- én trekant
class Trekant:
    """En retvinklet trekant med vinklen v og den hosliggende katete b.
    Alle punkter - ogsaa buen ved vinklen og vinkelmaerket - regnes i
    lokale koordinater og drejes derefter samlet. Rammen kommer ud af de
    drejede punkter, ikke af et gaet."""

    def __init__(self, b, v, navn, drej=0, spejl=False, vis_vinkel=False):
        self.b, self.v, self.navn = b, v, navn
        self.vis_vinkel = vis_vinkel
        r = math.radians(v)
        self.a = b * math.tan(r)          # siden over for vinklen
        self.h = b / math.cos(r)          # den lange side
        P0, P1, P2 = (0.0, 0.0), (float(b), 0.0), (float(b), -self.a)
        self.kant = [P0, P1, P2]
        rb = min(9.0, b / 3)
        self.bue = [(rb * math.cos(r * i / 12), -rb * math.sin(r * i / 12))
                    for i in range(13)]
        m = min(4.0, b / 6, self.a / 6)
        self.maerke = [(b - m, 0.0), (b - m, -m), (float(b), -m)]
        tp = ((P0[0] + P1[0] + P2[0]) / 3, (P0[1] + P1[1] + P2[1]) / 3)
        self.etiket = tp
        # Vinkeltallet laegges paa vinkelhalveringslinjen, lige uden for
        # buen. Et fast punkt inde i trekanten lagde 60°-tallet oven i buen.
        hv = math.radians(v / 2)
        self.vtekst = (rb * 1.95 * math.cos(hv), -rb * 1.95 * math.sin(hv))

        c, s = math.cos(math.radians(drej)), math.sin(math.radians(drej))

        def tr(p):
            x, y = (-p[0] if spejl else p[0]), p[1]
            return (x * c - y * s, x * s + y * c)

        for felt in ('kant', 'bue', 'maerke'):
            setattr(self, felt, [tr(p) for p in getattr(self, felt)])
        self.etiket, self.vtekst = tr(self.etiket), tr(self.vtekst)
        alle = self.kant + self.bue + self.maerke
        self.x0 = min(x for x, _ in alle)
        self.y0 = min(y for _, y in alle)
        self.bredde = max(x for x, _ in alle) - self.x0
        self.hojde = max(y for _, y in alle) - self.y0

    def tegn(self, dx, dy):
        ox, oy = dx - self.x0, dy - self.y0

        def f(pkt):
            return ' '.join(f'{x+ox:.2f},{y+oy:.2f}' for x, y in pkt)

        d = [f'<polygon points="{f(self.kant)}" fill="#fff" stroke="{INK}" '
             f'stroke-width="0.5"/>',
             f'<polyline points="{f(self.bue)}" fill="none" stroke="{BLA}" '
             f'stroke-width="0.4"/>',
             f'<polyline points="{f(self.maerke)}" fill="none" '
             f'stroke="{INK}" stroke-width="0.35"/>',
             f'<text x="{self.etiket[0]+ox:.1f}" '
             f'y="{self.etiket[1]+oy+2:.1f}" text-anchor="middle" '
             f'font-size="7" font-weight="700" fill="{LIN}">{self.navn}</text>']
        if self.vis_vinkel:
            d.append(f'<text x="{self.vtekst[0]+ox:.1f}" '
                     f'y="{self.vtekst[1]+oy+2:.1f}" text-anchor="middle" '
                     f'font-size="5.5" fill="{BLA}">{self.v}°</text>')
        return ''.join(d), [(ox + self.x0, oy + self.y0),
                            (ox + self.x0 + self.bredde,
                             oy + self.y0 + self.hojde)]


def pak(dele, bredde=PLADS_B - 8, gab=GAB):
    """Hyldepakning. Brikkerne laegges fra venstre, og der skiftes hylde,
    naar den naeste ikke kan vaere der. Hoejden kommer ud af pakningen -
    den bliver ikke gaettet."""
    krop, pkt = '', []
    x, y, hylde = 0.0, 0.0, 0.0
    for t in dele:
        if x and x + t.bredde > bredde:
            x, y, hylde = 0.0, y + hylde + gab, 0.0
        s, p = t.tegn(x, y)
        krop += s
        pkt += p
        x += t.bredde + gab
        hylde = max(hylde, t.hojde)
    return svg(krop, pkt)


# A: fire ens og én falsk. Stoerrelserne er valgt, saa den mindste er
# upraecis nok til, at forskellen paa stor og lille kan maerkes.
A_TREKANTER = [
    Trekant(85, V, 'S', drej=270),
    Trekant(65, V, 'R', drej=180),
    Trekant(58, FALSK, 'T', spejl=True),
    Trekant(50, V, 'Q', drej=90),
    Trekant(35, V, 'P'),
]
B_TREKANTER = [Trekant(60, 25, 'U', vis_vinkel=True),
               Trekant(48, 45, 'V', vis_vinkel=True),
               Trekant(36, 60, 'W', vis_vinkel=True)]
C_TREKANT = Trekant(150, V, '')

for _t in A_TREKANTER:
    assert _t.bredde <= PLADS_B - 8, f'{_t.navn} er for bred'
# Den falske skal kunne skilles fra med en lineal, der maaler i hele mm.
_ok = [t for t in A_TREKANTER if t.v == V]


def _spand(t):
    return ((t.a - .5) / (t.h + .5), (t.a + .5) / (t.h - .5))


_falsk = [t for t in A_TREKANTER if t.v != V][0]
assert max(_spand(t)[1] for t in _ok) < _spand(_falsk)[0], \
    'den falske trekant kan ikke skilles fra med mm-nøjagtighed'
assert all(_spand(t)[0] <= math.sin(math.radians(V)) <= _spand(t)[1]
           for t in _ok), 'det rigtige tal ligger ikke inden for måleusikkerheden'
# Og pointen i A: jo stoerre trekant, jo smallere spand.
_sorteret = sorted(_ok, key=lambda t: t.b)
_bredder = [_spand(t)[1] - _spand(t)[0] for t in _sorteret]
assert _bredder == sorted(_bredder, reverse=True), \
    'usikkerheden falder ikke med størrelsen'


# ------------------------------------------------------------------- teksten
TRIN = [
 ('A', 'Fem trekanter', [
   'Klip alle fem trekanter ud.',
   'Stak dem oven på hinanden med <b>den buede vinkel i samme hjørne</b>. '
   'Du må gerne vende papiret om. Fire passer sammen. Én gør ikke.',
   'Mål på hver trekant: siden <b>over for</b> den buede vinkel, siden '
   '<b>ind til</b> den, og den lange side. Skriv målene i skemaet, og '
   'regn den sidste søjle ud.'],
  'Hvilken trekant hører ikke til — og kan du se det på tallene alene?',
  ['Hvad gælder der om tallet i sidste søjle for de fire andre?',
   'De fire trekanter er vidt forskellige i størrelse. Hvorfor giver de '
   'alligevel det samme tal?',
   'Hvilken af de fire gav det mest nøjagtige tal? Hvorfor mon?',
   'Har I en vinkelmåler: hvor stor er den buede vinkel?'],
  'Så hvad er det, tallet i sidste søjle følger?',
  'A'),

 ('B', 'De tre forhold', [
   'Klip de tre nye trekanter ud. Her står vinklen skrevet.',
   'Mål de tre sider på hver, og regn de tre forhold ud. Skriv dem '
   'øverst i felterne.',
   'Find nu <b>sin</b>, <b>cos</b> og <b>tan</b> på lommeregneren — tast '
   'fx <code>sin(25)</code> — og skriv tallene <b>nederst</b> i de samme '
   'felter.'],
  'Hvad ser du, når du sammenligner de to tal i hvert felt?',
  ['Hvilket af de tre forhold hedder sin? Hvilket hedder cos? Hvilket '
   'hedder tan?',
   'Trekanten med 45° giver det samme tal to gange. Hvorfor?',
   'Hvorfor behøver man ikke måle, når man har en lommeregner — og hvad '
   'er det så, lommeregneren gør?'],
  'Så hvad er sin, cos og tan i virkeligheden?',
  'B'),

 ('C', 'Den højde, du ikke kan nå', [
   'Klip den store trekant ud. Den har <b>samme vinkel</b> som de fire i A.',
   'Hold den op til øjet, så den <b>korte side nederst er vandret</b> — '
   'tjek efter med en vandret kant i rummet. Kig langs den skrå side.',
   'Gå frem og tilbage, til toppen af det, du måler — dørkarmen, vinduet, '
   'loftet — ligger præcis på sigtelinjen. Mål afstanden til væggen, og '
   'mål din øjenhøjde.'],
  'Hvor højt er det, du sigtede på?',
  ['Du kender tallet fra A. Hvad skal afstanden ganges med?',
   'Hvorfor skal din øjenhøjde lægges til til sidst?',
   'Mål det samme fra en anden afstand. Får du det samme svar?'],
  'Så hvordan finder man en højde, man ikke kan nå op til?',
  None),
]

_t35 = math.tan(math.radians(V))
REGN = [
 'En retvinklet trekant har vinklen 30°, og den lange side er 12 cm. Hvor '
 'lang er siden over for vinklen?',
 'En rampe stiger 1 m over en vandret strækning på 5 m. Hvor stor er '
 'vinklen?',
 'En stige på 4 m står op ad en mur og danner 70° med jorden. Hvor højt '
 'op når den?',
 'I en retvinklet trekant er siden over for vinklen 5 cm og siden ind til '
 'den 12 cm. Hvor stor er vinklen?',
 'Du står 20 m fra et træ og sigter til toppen med trekanten fra C. Din '
 'øjenhøjde er 1,6 m. Hvor højt er træet?',
]
_sv2 = math.degrees(math.atan(1 / 5))
_sv3 = 4 * math.sin(math.radians(70))
_sv4 = math.degrees(math.atan(5 / 12))
_sv5 = 1.6 + _t35 * 20
SVAR_REGN = [
 '6 cm — sin(30°) = 0,5, og 0,5 · 12 = 6',
 f'{kom(_sv2)}° — tan v = 1 ÷ 5 = 0,2',
 f'{kom(_sv3, 2)} m — 4 · sin(70°)',
 f'{kom(_sv4)}° — tan v = 5 ÷ 12. (Den lange side er 13 cm)',
 f'{kom(_sv5, 1)} m — 1,6 + {kom(_t35, 2)} · 20',
]

SVAR = [
 ('A', f'<b>T hører ikke til.</b> De fire andre giver {kom(math.sin(math.radians(V)), 3)} '
       f'i sidste søjle; T giver {kom(math.sin(math.radians(FALSK)), 3)}. '
       f'Med en lineal, der måler i hele millimeter, lander de fire mellem '
       f'{kom(min(_spand(t)[0] for t in _ok), 2)} og '
       f'{kom(max(_spand(t)[1] for t in _ok), 2)}, og T mellem '
       f'{kom(_spand(_falsk)[0], 2)} og {kom(_spand(_falsk)[1], 2)} — '
       f'spandene rører ikke hinanden, så tallet afslører den, også hvis '
       f'stakken var i tvivl. Vinklen er {V}°. '
       f'<b>Det er hele pointen:</b> forholdet følger vinklen og intet '
       f'andet. Trekantens størrelse betyder ingenting. '
       f'Og S gav det mest nøjagtige tal, fordi en halv millimeters fejl '
       f'fylder mindre i et stort tal end i et lille.'),
 ('B', 'De to tal i hvert felt er ens. Det, de har målt, <i>er</i> sin, '
       'cos og tan: <b>over for ÷ lang = sin</b>, '
       '<b>ind til ÷ lang = cos</b>, <b>over for ÷ ind til = tan</b>. '
       'Ved 45° er de to kateter lige lange, så sin og cos giver det '
       'samme, og tan bliver 1. Lommeregneren måler ikke — den slår op i '
       'det samme forhold, som de selv har målt sig frem til, bare med '
       'mange flere decimaler.'),
 ('C', f'<b>Højde = øjenhøjde + {kom(_t35, 2)} · afstand.</b> Tallet '
       f'{kom(_t35, 2)} er tan({V}°), og det er dét, de målte som '
       f'«over for ÷ ind til» i A. Øjenhøjden lægges til, fordi trekanten '
       f'kun måler stykket <i>over</i> øjet. Måler de fra to forskellige '
       f'afstande og får det samme, er det ikke tilfældigt — det er '
       f'beviset på, at forholdet er det samme hele vejen.'),
]

_AREAL = open(os.path.join(ROD, 'claude', 'byg_klip_areal.py'),
              encoding='utf-8').read()
_i = _AREAL.index("CSS = '''") + 9
CSS = _AREAL[_i:_AREAL.index("\n'''", _i)] + '''
.net{border:0.3mm dashed #c9d2e0;border-radius:2mm;padding:2mm;
display:inline-block;margin:0 2mm 0 0;vertical-align:top;font-size:10.5pt;
page-break-inside:avoid}
.rad{font-size:0;margin:0 0 1mm}
.ny{page-break-before:always}
.hvad{color:#333;margin:0 0 2mm;max-width:150mm;font-size:9.5pt}
h1.smal{font-size:16pt;margin:0 0 3mm}
h2{margin:3mm 0 1mm}
table.maal{width:100%;border-collapse:collapse;margin:3mm 0;font-size:9pt}
table.maal th{border:0.3mm solid #c9d2e0;padding:2mm;background:#eef2f8;
font-size:8.5pt;text-align:center;font-weight:700}
table.maal td{border:0.3mm solid #c9d2e0;padding:0;height:11mm}
table.maal td.navn{width:16mm;text-align:center;font-weight:700;
background:#fbfcfe}
table.maal td.to{height:15mm;background:#fbfcfe}
table.maal td.to div{height:7.5mm;border-bottom:0.3mm dotted #c9d2e0}
code{background:#eef2f8;padding:0 1mm;border-radius:1mm}
'''


def _tabel_a():
    r = ('<tr><th>Trekant</th><th>Over for vinklen</th>'
         '<th>Ind til vinklen</th><th>Den lange side</th>'
         '<th>Over for ÷ den lange</th></tr>')
    for t in A_TREKANTER:
        r += (f'<tr><td class="navn">{t.navn}</td>'
              + '<td></td>' * 4 + '</tr>')
    return f'<table class="maal"><tbody>{r}</tbody></table>'


def _tabel_b():
    r = ('<tr><th>Trekant</th><th>Over for ÷ den lange</th>'
         '<th>Ind til ÷ den lange</th><th>Over for ÷ ind til</th></tr>')
    for t in B_TREKANTER:
        r += (f'<tr><td class="navn">{t.navn} · {t.v}°</td>'
              + '<td class="to"><div></div></td>' * 3 + '</tr>')
    return ('<table class="maal"><tbody>' + r + '</tbody></table>'
            '<p class="hvad" style="margin-top:1mm">Øverst i feltet: det, '
            'du selv har målt. Nederst: det, lommeregneren siger.</p>')


TABELLER = {'A': _tabel_a, 'B': _tabel_b}

KLIPARK = (
 '<h1 class="smal">Klip trigonometrien fri</h1>'
 '<h2 style="margin-top:0">A · Fem trekanter</h2>'
 '<p class="hvad">Fire af dem har den samme vinkel — den, der er markeret '
 'med en bue. Én har ikke. Klip dem ud, og find ud af hvilken. Vinklerne '
 'står der ikke; du skal måle dig frem.</p>'
 f'<div class="rad"><div class="net">{pak(A_TREKANTER)}</div></div>'
 '<div class="ny"></div>'
 '<h2 style="margin-top:0">B · De tre forhold</h2>'
 '<p class="hvad">Her står vinklen skrevet. Mål de tre sider på hver '
 'trekant.</p>'
 f'<div class="rad"><div class="net">{pak(B_TREKANTER)}</div></div>'
 '<h2>C · Sigtetrekanten</h2>'
 '<p class="hvad">Samme vinkel som de fire i A, bare stor. Den nederste '
 'side skal holdes vandret, og du kigger langs den skrå.</p>'
 f'<div class="rad"><div class="net">{pak([C_TREKANT])}</div></div>'
 '<footer>Trekanterne er trykt i rigtig størrelse. Printes arket '
 'forminsket, passer dine målinger ikke — men forholdene gør. Tænk over '
 'hvorfor.</footer>')


def trin_html():
    ud = ''
    for bogstav, navn, gor, spm, under, formel, tabel in TRIN:
        ud += (f'<div class="gr"><div class="bogstav">{bogstav}</div><div>'
               f'<p class="navn">{navn}</p><ol>'
               + ''.join(f'<li>{t}</li>' for t in gor) + '</ol>'
               + (TABELLER[tabel]() if tabel else '')
               + f'<p class="sp">{spm}</p><div class="linje"></div>'
               + ''.join(f'<p style="margin:2mm 0 0;color:#333">{t}</p>'
                         f'<div class="linje"></div>' for t in under)
               + f'<div class="boks"><b>{formel}</b>'
                 f'<div class="linje"></div><div class="linje"></div></div>'
               '</div></div>')
    return ud


regn_html = ''.join(
    f'<tr><td class="nr">{i}</td><td>{t}</td><td class="plads"></td></tr>'
    for i, t in enumerate(REGN, 1))

ARBEJD = ('<div class="ny"></div><h1>Hvad fandt du ud af?</h1>'
          '<p class="lead">Der er ingen formel at klippe frem her. Der er '
          'en påstand: <b>forholdet mellem siderne afhænger kun af '
          'vinklen</b> — ikke af, hvor stor trekanten er. Den kan en saks '
          'og en lineal afgøre. Mål omhyggeligt; her er en halv millimeter '
          'til forskel.</p>' + trin_html()
          + '<h2>Regn videre</h2>'
            '<p style="color:#333;margin:0 0 2mm">Nu må du bruge '
            'lommeregneren. Tegn en skitse til hver opgave først, og skriv '
            'på den, hvilken side der er hvad.</p>'
            f'<table class="regn"><tbody>{regn_html}</tbody></table>'
            '<footer>Tjek, at lommeregneren står i grader og ikke i radianer: '
            'sin(30) skal give 0,5. Giver den noget andet, er det '
            'indstillingen — ikke dig.</footer>')

svar_html = ''.join(
    f'<div class="gr"><div class="bogstav">{b}</div><div>'
    f'<p style="margin:0">{t}</p></div></div>' for b, t in SVAR)
svar_regn_html = ''.join(
    f'<tr><td class="nr">{i}</td><td>{REGN[i-1]}</td>'
    f'<td class="plads"><b>{s}</b></td></tr>'
    for i, s in enumerate(SVAR_REGN, 1))

maal_html = ''.join(
    f'<tr><td class="nr">{t.navn}</td><td>{t.v}°, og den hosliggende side '
    f'er {t.b} mm</td><td class="plads"><b>over for {kom(t.a)} · ind til '
    f'{t.b} · lang {kom(t.h)} mm</b></td></tr>'
    for t in A_TREKANTER + B_TREKANTER)

VEJL = (f'<h1>Klip trigonometrien fri · forventede svar</h1>'
        f'<p class="lead">Til den voksne. Arket uddeles uden denne side.</p>'
        f'<div class="boks"><b>Hvad øvelsen gør.</b> De fire foregående ark '
        f'klippede en formel frem. Her er der ikke en formel at klippe — '
        f'der er en påstand: <b>forholdet mellem siderne afhænger kun af '
        f'vinklen.</b> Den kan afgøres med saks og lineal, og når den står '
        f'fast, er sin, cos og tan ikke tre nye ting at lære udenad, men '
        f'navne på tre forhold, de selv har målt.</div>'
        f'<h2>Hvad de skal nå frem til</h2>{svar_html}'
        f'<h2>Trekanternes rigtige mål</h2>'
        f'<p class="hvad">Til at tjekke med. De skal måle sig frem, ikke '
        f'have tallene — men en måling, der er mere end 1 mm ved siden af, '
        f'er en målefejl, ikke et resultat.</p>'
        f'<table class="regn"><tbody>{maal_html}</tbody></table>'
        f'<div class="ny"></div><h2 style="margin-top:0">Regn videre</h2>'
        f'<table class="regn"><tbody>{svar_regn_html}</tbody></table>'
        f'<div class="boks"><b>Det, der driller.</b> «Over for» og «ind '
        f'til» byttes om, så sin og cos bliver forvekslet — lad dem skrive '
        f'det på skitsen, hver gang. Lommeregneren står i radianer: '
        f'sin(30) skal give 0,5. Og i C holdes trekanten skævt; så bliver '
        f'højden forkert, uden at noget ser forkert ud. Lad dem måle fra '
        f'to afstande — får de to forskellige svar, var det hånden.</div>'
        f'<footer>Vinklen i A og C er {V}°, og tan({V}°) = '
        f'{kom(_t35, 4)} ≈ {kom(_t35, 2)}. Den falske trekant T har '
        f'{FALSK}°. Måleusikkerheden er regnet efter: med ±0,5 mm på hver '
        f'måling rører de fires spand og T\'s spand ikke hinanden, og '
        f'spandet bliver smallere, jo større trekanten er.</footer>')


def skriv(navn, krop):
    sti = os.path.join(ROD, navn)
    h = sti.replace('.pdf', '.html')
    os.makedirs(os.path.dirname(sti), exist_ok=True)
    open(h, 'w', encoding='utf-8').write(
        '<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
        '<title>Klip trigonometrien fri</title><style>' + CSS
        + '</style></head><body>' + krop + '</body></html>')
    subprocess.run(['node', os.path.join(ROD, 'claude', 'html_til_pdf.mjs'),
                    h, sti], check=True, stdout=subprocess.DEVNULL)
    os.remove(h)
    print('skrevet: ', sti)


if __name__ == '__main__':
    skriv('materiale/klip-trigonometri-fri.pdf', KLIPARK + ARBEJD)
    skriv('vejledning/klip-trigonometri-fri-svar.pdf', VEJL)
    print(f'vinklen {V}° · sin {kom(math.sin(math.radians(V)), 4)} · '
          f'cos {kom(math.cos(math.radians(V)), 4)} · tan {kom(_t35, 4)} · '
          f'den falske {FALSK}°')
