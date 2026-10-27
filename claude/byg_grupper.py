# -*- coding: utf-8 -*-
"""Bygger vejledning/grupper-fredag.pdf — grupperne, naar 6. og 7. klasse
kommer paa besoeg fredag i uge 44.

Renskrift af den haandskrevne seddel "Info til 9. kl". Listen er kilden her
i filen; PDF'en er bygget og ligger ikke i git.

    python3 claude/byg_grupper.py
"""
import html
import os
import subprocess

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UD_HTML = os.path.join(ROD, 'vejledning', 'grupper-fredag.html')
UD_PDF = os.path.join(ROD, 'vejledning', 'grupper-fredag.pdf')

TITEL = 'Når 6. og 7. klasse kommer på besøg'
UNDER = 'Fredag kl. 11–12 · uge 44 · 8. og 9. klasse'

GRUPPER = [
    ['Jonatan', 'Elias'],
    ['Ursula', 'Olivia', 'Linnea', 'Roxie'],
    ['Sofie', 'Sølve', 'Vigga', 'Vilma'],
    ['Lykke', 'Flora', 'Sif', 'Ella Mai', 'Aida'],
    ['Manfred', 'Vera', 'Malik', 'Agnes'],
    ['Lulu', 'Levi', 'Nora', 'Vitus'],
    ['Kathrine', 'Erika', 'Isabella L', 'Isabella T'],
    ['Sophie', 'Astrid', 'Ella', 'Frida'],
    ['Julian', 'Sigurd'],
    ['Valdemar', 'Alvin'],
]

# Ingen maa staa i to grupper, og ingen maa vaere faldet ud mellem sedlen og
# filen. Begge dele er sket for en klasseliste foer.
_alle = [n for g in GRUPPER for n in g]
assert len(_alle) == len(set(_alle)), \
    f'disse navne står to steder: {sorted(n for n in set(_alle) if _alle.count(n) > 1)}'
I_ALT = len(_alle)

kort = ''
for nr, navne in enumerate(GRUPPER, 1):
    kort += (f'<div class="kort"><div class="nr">{nr}</div>'
             f'<div class="navne">'
             + ''.join(f'<span>{html.escape(n)}</span>' for n in navne)
             + f'</div><div class="antal">{len(navne)}</div></div>')

CSS = '''
*{box-sizing:border-box}
body{margin:0;font-family:Helvetica,Arial,sans-serif;color:#1a2233;
font-size:10pt;line-height:1.35}
.topline{color:#586074;font-size:9pt;letter-spacing:.4px;
text-transform:uppercase;margin-bottom:2mm}
h1{font-size:17pt;margin:0 0 1mm}
.under{color:#586074;font-size:11pt;margin:0 0 6mm}
.gitter{display:grid;grid-template-columns:1fr 1fr;gap:4mm}
.kort{display:flex;align-items:center;gap:4mm;border:1px solid #c9d2e0;
border-radius:3mm;padding:4mm;background:#fbfcfe;min-height:26mm}
.nr{flex:0 0 11mm;height:11mm;border-radius:50%;background:#1f6fd6;color:#fff;
font-weight:700;font-size:12pt;display:flex;align-items:center;
justify-content:center}
.navne{flex:1;display:flex;flex-wrap:wrap;gap:1.5mm 3mm}
.navne span{font-size:11pt;font-weight:600}
.navne span:not(:last-child)::after{content:' ·';color:#9aa4b5;font-weight:400}
.antal{flex:0 0 auto;color:#9aa4b5;font-size:9pt;font-weight:700}
footer{margin-top:6mm;border-top:1px solid #c9d2e0;padding-top:2mm;
color:#586074;font-size:8.5pt;display:flex;justify-content:space-between}
@page{size:A4;margin:14mm}
'''

DOK = ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
       '<title>Grupper · fredag uge 44</title><style>' + CSS
       + '</style></head><body>'
       f'<div class="topline">Info til 8. og 9. klasse</div>'
       f'<h1>{html.escape(TITEL)}</h1>'
       f'<p class="under">{html.escape(UNDER)}</p>'
       f'<div class="gitter">{kort}</div>'
       f'<footer><span>{len(GRUPPER)} grupper · {I_ALT} unger</span>'
       f'<span>Tallet til højre er, hvor mange I er i gruppen.</span>'
       '</footer></body></html>')

os.makedirs(os.path.dirname(UD_HTML), exist_ok=True)
open(UD_HTML, 'w', encoding='utf-8').write(DOK)
subprocess.run(['node', os.path.join(ROD, 'claude', 'html_til_pdf.mjs'),
                UD_HTML, UD_PDF], check=True, stdout=subprocess.DEVNULL)
os.remove(UD_HTML)
print(f'skrevet:  {UD_PDF}')
print(f'{len(GRUPPER)} grupper · {I_ALT} unger · '
      f'{min(len(g) for g in GRUPPER)}–{max(len(g) for g in GRUPPER)} pr. gruppe')
