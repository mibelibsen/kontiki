# -*- coding: utf-8 -*-
"""QR-kode til en adresse — som SVG, PNG og et A4-ark til print.

    python3 claude/byg_qr.py https://www.mibelibsen.space/algoritme materiale/qr-algoritme "Reklame-algoritmen"

skriver materiale/qr-algoritme.svg, .png og .pdf. PNG'en kraever Pillow
(pip install pillow); findes det ikke, springes den over. Koden laeses
tilbage med zxing-cpp, hvis det er installeret.
"""
import html
import os
import subprocess
import sys

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROD)
sys.path.insert(0, 'claude')
import qr  # noqa: E402

adresse, ud, titel = sys.argv[1], sys.argv[2], (sys.argv[3] if len(sys.argv) > 3 else '')
kort = adresse.replace('https://', '').replace('http://', '').rstrip('/')

# SVG
svg = qr.svg(adresse, ec='Q', mm=80)
open(ud + '.svg', 'w', encoding='utf-8').write(svg)
print(f'skrevet:  {ud}.svg')

# PNG, 10 px pr. modul med fire modulers stillezone
m, v, _ = qr.matrix(adresse, 'Q')
try:
    from PIL import Image
    n, px, sz = len(m), 10, 4
    im = Image.new('1', ((n + 2 * sz) * px, (n + 2 * sz) * px), 1)
    for y in range(n):
        for x in range(n):
            if m[y][x]:
                for dy in range(px):
                    for dx in range(px):
                        im.putpixel(((x + sz) * px + dx, (y + sz) * px + dy), 0)
    im.save(ud + '.png')
    print(f'skrevet:  {ud}.png   version {v}, {n}×{n} moduler')
except ImportError:
    print('  (Pillow mangler — ingen PNG; pip install pillow)')

# A4-ark
dok = f'''<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8"><title>{html.escape(titel or kort)}</title><style>
@page{{size:A4;margin:0}}*{{box-sizing:border-box}}
body{{margin:0;font-family:"Liberation Sans",Arial,Helvetica,sans-serif;color:#1a2233}}
.side{{width:210mm;height:297mm;padding:30mm 20mm;display:flex;flex-direction:column;align-items:center;text-align:center}}
h1{{font-size:28pt;margin:0 0 14mm}}
.qr{{border:1.2mm solid #1a2233;border-radius:6mm;padding:6mm;background:#fff}}
.qr svg{{display:block;width:120mm;height:120mm}}
.url{{margin-top:14mm;font-size:18pt;font-family:"Liberation Mono","DejaVu Sans Mono",monospace;border:1px solid #d3dae7;border-radius:3mm;padding:4mm 8mm}}
</style></head><body><div class="side">{f"<h1>{html.escape(titel)}</h1>" if titel else ""}
<div class="qr">{svg}</div><div class="url">{html.escape(kort)}</div></div></body></html>'''
kilde = '/tmp/byg_qr.html'
open(kilde, 'w', encoding='utf-8').write(dok)
subprocess.run(['node', 'claude/html_til_pdf.mjs', kilde, ud + '.pdf'], check=True)

# laes tilbage
try:
    import numpy
    import zxingcpp
    n = len(m)
    a = numpy.full(((n + 8) * 5, (n + 8) * 5), 255, dtype=numpy.uint8)
    for y in range(n):
        for x in range(n):
            if m[y][x]:
                a[(y + 4) * 5:(y + 5) * 5, (x + 4) * 5:(x + 5) * 5] = 0
    r = zxingcpp.read_barcode(a)
    assert r is not None and r.text == adresse, 'koden kunne ikke laeses tilbage'
    print(f'  læst tilbage med zxing-cpp: {r.text}')
except ImportError:
    print('  (zxing-cpp mangler — koden er ikke laest tilbage)')
