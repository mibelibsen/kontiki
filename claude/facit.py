# -*- coding: utf-8 -*-
"""Faelles skabelon til facitlisterne: A4-side, tabeller, figurer og noter.

Facitlisterne fandtes kun som faerdige PDF'er uden kilde, saa de kunne ikke
rettes - heller ikke da det viste sig, at koordinatsystemerne havde ulige
skala. Her ligger det, som alle facitlister deler, saa der kun er ét sted at
rette layout, og de to byggescripts kun indeholder deres eget indhold.

    claude/byg_facit.py             Funktioner og ligninger
    claude/byg_facit_statistik.py   Statistik, manipulation og sandsynlighed

Facit maa aldrig udgives. Filerne skrives i facit/, som er udelukket i
.vercelignore, og sendes i Code.
"""
import os
import re
import subprocess
import sys
import tempfile
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UD = os.path.join(ROD, 'facit')

UGEDAG = ['mandag', 'tirsdag', 'onsdag', 'torsdag', 'fredag', 'lørdag', 'søndag']
MAANED = ['januar', 'februar', 'marts', 'april', 'maj', 'juni', 'juli',
          'august', 'september', 'oktober', 'november', 'december']


def dansk_dato(iso):
    import datetime
    d = datetime.date.fromisoformat(iso)
    return f'{UGEDAG[d.weekday()]} den {d.day}. {MAANED[d.month - 1]} {d.year}'


# ---------------------------------------------------------------------------
# Skabelon - selvbaerende A4-side, al CSS inline
# ---------------------------------------------------------------------------
CSS = '''
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,
  Helvetica,Arial,sans-serif;color:#1a2233;line-height:1.5;background:#fff}
.ark{max-width:820px;margin:0 auto;padding:22px 22px 30px}
h1{font-size:1.3rem;line-height:1.28;margin:0 0 5px}
.meta{color:#586074;font-size:.88rem;margin:0 0 2px}
.hoerer{color:#586074;font-size:.88rem;margin:0 0 18px}
h2{font-size:1.05rem;margin:16px 0 7px;padding-bottom:4px;border-bottom:2px solid #1f6fd6}
h3{font-size:.98rem;margin:16px 0 6px}
p{margin:0 0 9px}
table{width:100%;border-collapse:collapse;margin:0 0 10px}
th,td{border:1px solid #cfd6e4;padding:5px 8px;text-align:left;vertical-align:top;
  font-size:.9rem}
th{background:#f4f6fb;font-weight:700}
td.sv{font-weight:700;color:#12633f;white-space:nowrap}
table.vt{width:auto;margin:0 0 10px}
table.vt th{width:34px;text-align:center}
table.vt td{width:44px;text-align:center;font-weight:700}
code{font-family:"Cambria Math",Georgia,serif;background:#f4f6fb;padding:0 4px;
  border-radius:4px;border:1px solid #e0e5ef}
.figur{margin:10px 0 12px;break-inside:avoid;page-break-inside:avoid}
.figur.bred svg{max-width:470px}
.figur svg{display:block;width:100%;max-width:340px;margin:0 auto;height:auto;
  background:#fff;border:1px solid #cfd6e4;border-radius:8px}
.figtekst{color:#586074;font-size:.86rem;margin:6px 0 0;text-align:center}
.note{background:#f4f6fb;border:1px solid #d3dae7;border-left:4px solid #1f6fd6;
  border-radius:7px;padding:9px 13px;margin:9px 0 14px;font-size:.9rem;color:#374151}
.note p:last-child{margin:0}
footer{color:#586074;font-size:.78rem;margin-top:24px;border-top:1px solid #e0e5ef;
  padding-top:9px}
@page{size:A4;margin:14mm}
@media print{
  body{font-size:9.8pt}
  .ark{padding:0}
  h2{break-after:avoid}
  .figur.bred svg{max-width:420px}
  .figur svg{max-width:270px;-webkit-print-color-adjust:exact;print-color-adjust:exact}
}
'''


def side(titel, meta, hoerer, blokke):
    krop = []
    for slags, data in blokke:
        if slags == 'h2':
            krop.append(f'<h2>{data}</h2>')
        elif slags == 'h3':
            krop.append(f'<h3>{data}</h3>')
        elif slags == 'p':
            krop.append(f'<p>{data}</p>')
        elif slags == 'note':
            krop.append('<div class="note">'
                        + ''.join(f'<p>{t}</p>' for t in data) + '</div>')
        elif slags == 'figur':
            svg, tekst = data
            # en bred figur skal have lov at fylde mere end et kvadratisk
            # koordinatsystem - ellers bliver sumkurvens tal uhjaelpsomt smaa
            m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
            bred = ' bred' if m and float(m.group(1)) / float(m.group(2)) > 1.3 else ''
            krop.append(f'<div class="figur{bred}">{svg}'
                        f'<p class="figtekst">{tekst}</p></div>')
        elif slags == 'vaerditabel':
            x_, y_ = data
            krop.append(
                '<table class="vt"><tr><th>x</th>'
                + ''.join(f'<td>{v}</td>' for v in x_) + '</tr><tr><th>y</th>'
                + ''.join(f'<td>{v}</td>' for v in y_) + '</tr></table>')
        elif slags == 'kolonner':
            kols, raekker = data
            r = ['<table><tr>' + ''.join(f'<th>{k}</th>' for k in kols) + '</tr>']
            for raekke in raekker:
                r.append('<tr>' + ''.join(f'<td>{c}</td>' for c in raekke) + '</tr>')
            krop.append(''.join(r) + '</table>')
        elif slags == 'tabel':
            r = ['<table><tr><th>Opgave</th><th>Svar</th><th>Udregning</th></tr>']
            for opg, svar, udr in data:
                r.append(f'<tr><td>{opg}</td><td class="sv">{svar}</td>'
                         f'<td>{udr}</td></tr>')
            krop.append(''.join(r) + '</table>')
        else:
            raise ValueError(slags)
    return (f'<!DOCTYPE html>\n<html lang="da">\n<head>\n<meta charset="UTF-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            f'<title>{titel}</title>\n<style>{CSS}</style>\n</head>\n<body>\n'
            f'<div class="ark">\n<h1>{titel}</h1>\n'
            f'<p class="meta">{meta}</p>\n<p class="hoerer">{hoerer}</p>\n'
            + '\n'.join(krop)
            + '\n<footer>Facitliste · må ikke udgives på sitet · '
              '9. klasse matematik · Mibelibsen</footer>\n</div>\n</body>\n</html>\n')



# ---------------------------------------------------------------------------
# Efterregning - intet svar skrives ned uden at vaere kontrolleret
# ---------------------------------------------------------------------------
def proev(venstre, hoejre, x):
    """Saetter x ind i begge sider og kraever, at de giver det samme."""
    v, h = venstre(F(x)), hoejre(F(x))
    assert v == h, f'x = {x} giver {v} mod {h}'
    return x


def forskrift(p1, p2):
    """Haeldning og skaering gennem to punkter - regnet, ikke aflaest."""
    (x1, y1), (x2, y2) = (F(p1[0]), F(p1[1])), (F(p2[0]), F(p2[1]))
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1
    return a, b


def nulpunkt(a, b):
    assert a != 0
    return -F(b) / F(a)


def skaering(a1, b1, a2, b2):
    x = (F(b2) - F(b1)) / (F(a1) - F(a2))
    return x, F(a1) * x + F(b1)


def dk(x):
    """Dansk talskrivning: komma, og minus som rigtigt minustegn."""
    x = F(x)
    if x.denominator == 1:
        t = str(x.numerator)
    else:
        v = float(x)
        t = f'{v:.4f}'.rstrip('0').rstrip('.').replace('.', ',')
    return t.replace('-', '−')

# ---------------------------------------------------------------------------
# Registrering og bygning
# ---------------------------------------------------------------------------
DOKUMENTER = []


def dok(navn, serie, dato, emne, hoerer, blokke):
    """Laegger en facitliste i koeen. serie: 'lektier' eller 'online'."""
    titel = (f'Facitliste{" lektier" if serie == "lektier" else ""} Matematik '
             f'{dansk_dato(dato)} {emne} facitliste')
    if serie == 'lektier':
        meta = f'Lektien er givet {dansk_dato(dato)} · 9. klasse · Mibelibsen'
    else:
        meta = (f'Modulets opgaver · gennemgås {dansk_dato(dato)} · '
                f'9. klasse · Mibelibsen')
    DOKUMENTER.append((navn, side(titel, meta, f'Hører til: {hoerer}', blokke)))


def byg(filter_=''):
    valgte = [(n, h) for n, h in DOKUMENTER if filter_ in n]
    assert valgte, f'intet dokument hedder noget med {filter_!r}'
    with tempfile.TemporaryDirectory() as tmp:
        for navn, html in valgte:
            kilde = os.path.join(tmp, navn + '.html')
            with open(kilde, 'w', encoding='utf-8') as f:
                f.write(html)
            subprocess.run(['node', os.path.join(ROD, 'claude', 'html_til_pdf.mjs'),
                            kilde, os.path.join(UD, navn + '.pdf')],
                           check=True, cwd=ROD)
    print(f'{len(valgte)} facitlister bygget i facit/')
