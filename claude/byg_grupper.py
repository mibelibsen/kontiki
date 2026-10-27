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

liste = ''.join(f'<li>{html.escape(", ".join(g))}</li>' for g in GRUPPER)

CSS = '''
body{margin:0;font-family:Georgia,'Times New Roman',serif;color:#000;
font-size:12pt;line-height:1.5}
h1{font-size:18pt;margin:0 0 2mm;font-weight:700}
.under{margin:0 0 8mm;font-size:12pt}
ol{margin:0;padding-left:9mm}
li{margin:0 0 3.5mm;padding-left:2mm}
p.slut{margin:10mm 0 0;font-size:11pt}
@page{size:A4;margin:20mm}
'''

DOK = ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
       '<title>Grupper · fredag uge 44</title><style>' + CSS
       + '</style></head><body>'
       f'<h1>{html.escape(TITEL)}</h1>'
       f'<p class="under">{html.escape(UNDER)}</p>'
       f'<ol>{liste}</ol>'
       f'<p class="slut">{len(GRUPPER)} grupper · {I_ALT} unger.</p>'
       '</body></html>')

# Guard, saa claude/byg_grupper_word.py kan hente navnelisten herfra uden
# at bygge PDF'en med. Listen staar ét sted; de to filer kan ikke drive fra
# hinanden.
if __name__ == '__main__':
    os.makedirs(os.path.dirname(UD_HTML), exist_ok=True)
    open(UD_HTML, 'w', encoding='utf-8').write(DOK)
    subprocess.run(['node', os.path.join(ROD, 'claude', 'html_til_pdf.mjs'),
                    UD_HTML, UD_PDF], check=True, stdout=subprocess.DEVNULL)
    os.remove(UD_HTML)
    print(f'skrevet:  {UD_PDF}')
    print(f'{len(GRUPPER)} grupper · {I_ALT} unger · '
          f'{min(len(g) for g in GRUPPER)}–{max(len(g) for g in GRUPPER)} pr. gruppe')
