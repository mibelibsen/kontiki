# -*- coding: utf-8 -*-
"""Bygger den pakke, testen skal bruges af i Microsoft Forms.

Testen maa ikke ligge paa sitet: resultatet skal bruges, og saa kan
spoergsmaal og svar ikke staa frit. Derfor haandteres den som materiale
til laereren i vejledning/ og facit/, som begge er udelukket fra deploy.

Der skrives fire ting:

  vejledning/samfundsfagstest/forms-import.docx   til Forms' Quick Import
  vejledning/samfundsfagstest/figurbilag.pdf      figurerne, nummereret
  vejledning/samfundsfagstest/figurer/*.png       samme figurer enkeltvis
  facit/facit-test-2026-11-17-samfundsfag60.pdf   rettenoegle

**Forms kan ikke importere figurer.** Quick Import tager kun tekst og
svarmuligheder, og Microsofts egen vejledning siger, at figurer og tabeller
skal fjernes foerst. Derfor henviser hvert spoergsmaal til et figurnummer,
og figurerne leveres baade som et samlet bilag og som enkeltbilleder, saa
de kan laegges ind i Forms ét ad gangen, hvis det foretraekkes.

Spoergsmaalene og svarenes raekkefoelge genbruges fra byg_samfundsfagstest,
saa retteno eglen passer til baade Forms-udgaven og sitets udgave.

    python3 claude/byg_forms_pakke.py
"""
import html
import importlib.util
import os
import subprocess
import sys

HER = os.path.dirname(os.path.abspath(__file__))
ROD = os.path.dirname(HER)
sys.path.insert(0, HER)

_spec = importlib.util.spec_from_file_location(
    'testen', os.path.join(HER, 'byg_samfundsfagstest.py'))
T = importlib.util.module_from_spec(_spec)
sys.modules['testen'] = T
_spec.loader.exec_module(T)

UDMAPPE = os.path.join(ROD, 'vejledning', 'samfundsfagstest')
FIGMAPPE = os.path.join(UDMAPPE, 'figurer')
FACIT = os.path.join(ROD, 'facit', 'facit-test-2026-11-17-samfundsfag60.pdf')
os.makedirs(FIGMAPPE, exist_ok=True)

# ------------------------------------------------- figurerne nummereres
# 60 spoergsmaal deler 18 figurer. De nummereres i den raekkefoelge, de
# foerst bruges, saa bilaget kan laeses forfra sammen med testen.
NAVNE = {id(v): n for n, v in vars(T).items() if n.startswith('F_')}
figurnr, figurer = {}, []          # svg -> nr,  [(nr, svg, kodenavn)]
for liste in T.ALLE:
    for fig, *_ in liste:
        if fig and fig not in figurnr:   # nogle spoergsmaal har ingen figur
            figurnr[fig] = len(figurer) + 1
            figurer.append((len(figurer) + 1, fig, NAVNE.get(id(fig), 'figur')))
# antallet falder, efterhaanden som figurer, der roebede svaret,
# bliver taget ud. Kun det skal holde: hver figur bruges af nogen.
assert figurer, 'ingen figurer tilbage'
assert len(figurer) == len({f for liste in T.ALLE for f, *_ in liste if f})

FIGTEKST = {
    'F_LOV_KORT': 'Lovprocessen fra ministeriet til Lovtidende',
    'F_RINGE': 'De tre socialisationsarenaer',
    'F_NORM_KORT': 'Norm, brud og sanktion',
    'F_SKAERM': 'Over 6 timers skærm om dagen · Danmark 2026',
    'F_SKOLE': 'Digitale redskaber i skoletiden · timer om dagen',
    'F_PROBLEM': 'Problematisk brug af sociale medier · 44 lande',
    'F_KOEN': 'Problematisk brug fordelt på køn · 2022',
    'F_FORMEGET': 'Synes selv, de bruger for meget tid · 2025',
    'F_LLM_KORT': 'Sådan gætter en sprogmodel',
    'F_AGENT_KORT': 'Hvad en agent gør anderledes',
    'F_AIBRUG': 'Brugere om måneden · millioner',
    'F_EJERE': 'Ejerandelene i OpenAI',
    'F_CHIP': 'Markedet for AI-chips til datacentre',
    'F_AKSE': 'Partierne på en højre-venstre-akse',
    'F_SAL': 'Folketinget efter valget 24. marts 2026',
    'F_REGERING': 'Regeringens fire partier',
    'F_OEKONOMI': 'Tre tal om dansk økonomi · mia. kr.',
    'F_INFLATION': 'Prisstigning på et år · oktober 2026',
    'F_KLUBBER': 'Hvor mange lande er med i EU og OECD?',
}
assert set(FIGTEKST) >= {k for _, _, k in figurer}, \
    'en figur mangler en billedtekst: ' + str(
        {k for _, _, k in figurer} - set(FIGTEKST))


def spoergsmaalene():
    """[(nr, figurnr, spoergsmaal, [tre svar], rigtig plads, forklaring, del)]

    Svarenes raekkefoelge er den samme som paa sitets udgave — den kommer
    af ORDEN, saa en elev, der har oevet sig paa siden, moeder de samme
    bogstaver. Det er med vilje: testen er ikke en overraskelse.
    """
    ud, nr = [], 0
    for (_, _, delnavn, liste, *_rest) in T.MODULER:
        for fig, tekst, _niveau, rigtig, forkerte, forklaring in liste:
            plads = T.ORDEN[nr]
            nr += 1
            valg = list(forkerte)
            valg.insert(plads, rigtig)
            assert valg[plads] == rigtig and len(set(valg)) == 3
            ud.append((nr, figurnr.get(fig), tekst, valg, plads,
                       forklaring, delnavn))
    assert nr == T.ANTAL
    return ud


SPM = spoergsmaalene()
BOGSTAV = 'ABC'
# svarene fordeler sig jaevnt nok, ogsaa naar antallet ikke gaar op i tre
assert all([s[4] for s in SPM].count(b) >= len(SPM) // 3 - 1
           for b in range(3)), 'svarene er skæve'


# ---------------------------------------------------- 1) Forms-importfilen
def skriv_docx():
    """Word-fil til Forms' Quick Import.

    Formatet foelger det, Microsofts vejledning beskriver: ét spoergsmaal
    pr. afsnit, svarmulighederne paa hver sin linje med a./b./c. foran.
    **Ingen tabeller, ingen billeder, ingen overskrifter** — de bliver
    enten ikke importeret eller laest som et spoergsmaal for sig. Derfor
    staar delenes navne kun i rettenoeglen.

    Det rigtige svar er ikke markeret i filen. Quick Import saetter ikke
    facit, og en markering ville enten blive laest som en fjerde
    svarmulighed eller blive hos eleverne. Facit staar i rettenoeglen.
    """
    from docx import Document
    from docx.shared import Pt

    d = Document()
    st = d.styles['Normal']
    st.font.name = 'Arial'
    st.font.size = Pt(11)
    st.paragraph_format.space_after = Pt(0)

    for nr, fignr, tekst, valg, _plads, _forkl, _del in SPM:
        p = d.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        henvis = f' (figur {fignr})' if fignr else ''
        p.add_run(f'Spørgsmål {nr} · {tekst}{henvis}')
        for i, v in enumerate(valg):
            d.add_paragraph(f'{"abc"[i]}. {v}')

    sti = os.path.join(UDMAPPE, 'forms-import.docx')
    d.save(sti)
    return sti


# --------------------------------------------------------- 2) figurerne
def _fig_html():
    """Alle figurer i én fil — bruges baade til PNG-udtraek og til bilaget."""
    dele = []
    for nr, svg, kode in figurer:
        spm = [str(s[0]) for s in SPM if s[1] == nr]
        liste = ('Spørgsmål ' + (', '.join(spm) if len(spm) < 6
                 else f'{spm[0]}–{spm[-1]}'))
        dele.append(
            f'<figure id="fig{nr}"><figcaption><b>Figur {nr}</b>'
            f'<span class="t">{html.escape(FIGTEKST[kode])}</span>'
            f'<span>{liste}</span>'
            f'</figcaption><div class="tegning">{svg}</div></figure>')
    return ''.join(dele)


BILAG_CSS = '''
*{box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,
sans-serif;color:#1a2233;margin:0;padding:0;font-size:11pt;line-height:1.45}
h1{font-size:19pt;margin:0 0 4px}
.intro{color:#586074;max-width:62em;margin:0 0 18px}
figure{margin:0 0 20px;padding:12px 14px;border:1px solid #c9d2e0;
border-radius:10px;break-inside:avoid}
figcaption{font-size:10.5pt;margin-bottom:8px;display:flex;
justify-content:space-between;gap:12px;align-items:baseline}
figcaption span{color:#586074;font-size:9.5pt;white-space:nowrap}
figcaption span.t{color:#1a2233;font-size:10.5pt;white-space:normal}
.tegning{text-align:center}
.tegning svg{max-width:100%;height:auto;max-height:300px}
table{border-collapse:collapse;width:100%;font-size:10pt;margin:10px 0 18px}
th,td{border:1px solid #c9d2e0;padding:5px 8px;text-align:left;
vertical-align:top}
th{background:#f3f6fb}
td.sv{font-weight:700;text-align:center;width:3.2em}
td.nr{text-align:right;width:3em;color:#586074}
h2{font-size:13pt;margin:18px 0 6px;padding-top:6px;
border-top:2px solid #1a2233;break-after:avoid}
.note{background:#f3f6fb;border-left:4px solid #1f6fd6;padding:10px 14px;
margin:12px 0;color:#586074;max-width:62em}
.note b{color:#1a2233}
@page{size:A4;margin:16mm}
'''


def skriv_bilag():
    doc = (f'<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
           f'<title>Figurbilag</title><style>{BILAG_CSS}</style></head><body>'
           f'<h1>Figurbilag · samfundsfagstest</h1>'
           f'<p class="intro">De {len(figurer)} figurer, testens spørgsmål '
           f'henviser til. Hav bilaget åbent ved siden af testen — '
           f'spørgsmålet siger, hvilken figur det handler om. '
           f'Tallene er slået op {T.OPDATERET}.</p>'
           + _fig_html() + '</body></html>')
    sti = os.path.join(UDMAPPE, 'figurbilag.html')
    open(sti, 'w', encoding='utf-8').write(doc)
    return sti


# --------------------------------------------------------- 3) rettenøglen
def skriv_rettenoegle():
    raekker, nu = '', None
    for nr, fignr, tekst, valg, plads, forkl, delnavn in SPM:
        if delnavn != nu:
            nu = delnavn
            raekker += (f'</tbody></table><h2>{html.escape(delnavn)}</h2>'
                        f'<table><thead><tr><th class="nr">#</th>'
                        f'<th class="sv">Svar</th><th>Spørgsmål og det '
                        f'rigtige svar</th></tr></thead><tbody>')
        raekker += (f'<tr><td class="nr">{nr}</td>'
                    f'<td class="sv">{BOGSTAV[plads]}</td><td>'
                    f'{html.escape(tekst)}<br><b>{html.escape(valg[plads])}'
                    f'</b><br><span style="color:#586074">{html.escape(forkl)}'
                    f'</span></td></tr>')
    raekker = raekker[len('</tbody></table>'):] + '</tbody></table>'

    strimmel = '<table><thead><tr>' + ''.join(
        f'<th class="sv">{s[0]}</th>' for s in SPM[:20]) + '</tr></thead>' \
        '<tbody><tr>' + ''.join(
        f'<td class="sv">{BOGSTAV[s[4]]}</td>' for s in SPM[:20]) + \
        '</tr></tbody></table>'
    for fra in (20, 40):
        strimmel += '<table><thead><tr>' + ''.join(
            f'<th class="sv">{s[0]}</th>' for s in SPM[fra:fra + 20]) + \
            '</tr></thead><tbody><tr>' + ''.join(
            f'<td class="sv">{BOGSTAV[s[4]]}</td>' for s in SPM[fra:fra + 20]) \
            + '</tr></tbody></table>'

    doc = (f'<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
           f'<title>Rettenøgle</title><style>{BILAG_CSS}</style></head><body>'
           f'<h1>Rettenøgle · samfundsfagstest</h1>'
           f'<p class="intro">60 spørgsmål. Svarenes rækkefølge er den '
           f'samme som i Forms-importfilen og på øvelsessiden, så '
           f'bogstaverne passer begge steder. Tallene er slået op '
           f'{T.OPDATERET}.</p>'
           f'<div class="note"><b>Må ikke deles med eleverne.</b> '
           f'Filen ligger i facit/, som er udelukket fra deploy, og den '
           f'kommer aldrig på 321flyv.com.</div>'
           f'<h2>Svarstrimmel</h2>{strimmel}{raekker}</body></html>')
    sti = os.path.join(UDMAPPE, 'rettenoegle.html')
    open(sti, 'w', encoding='utf-8').write(doc)
    return sti


# ------------------------------------------------- 4) retteark til eleverne
# Dette ark er til ungerne, ikke til laereren. Derfor staar svarene med
# alle tre muligheder, saa man kan se, hvad man selv valgte — og hvorfor
# det rigtige er rigtigt. Rettenoeglens svarstrimmel hoerer ikke hjemme
# her; den er lavet til at rette hurtigt, ikke til at laere noget af.
RETTEARK_CSS = BILAG_CSS + '''
.spm{border:1px solid #c9d2e0;border-radius:10px;padding:11px 14px;
margin:0 0 10px;break-inside:avoid}
.spm .hd{font-weight:700;margin-bottom:7px}
.spm .hd .nr{color:#1f6fd6;margin-right:6px}
.sv{display:flex;gap:9px;align-items:flex-start;margin:3px 0;
font-size:10pt;color:#586074}
.sv .mk{flex:0 0 auto;width:19px;height:19px;border-radius:5px;
display:grid;place-items:center;font-weight:800;font-size:8.5pt;
background:#f3f6fb;border:1px solid #c9d2e0}
.sv.rigtig{color:#13593d;font-weight:700}
.sv.rigtig .mk{background:#1a8f5e;color:#fff;border-color:#1a8f5e}
.hvorfor{margin:7px 0 0;padding-left:28px;font-size:9.5pt;color:#586074}
.hvorfor b{color:#1a2233}
.tael{background:#f3f6fb;border-left:4px solid #1f6fd6;padding:11px 15px;
border-radius:8px;margin:14px 0}
'''


def skriv_retteark():
    krop, nu = '', None
    for nr, fignr, tekst, valg, plads, forkl, delnavn in SPM:
        if delnavn != nu:
            nu = delnavn
            krop += f'<h2>{html.escape(delnavn)}</h2>'
        svar = ''.join(
            f'<div class="sv{" rigtig" if i == plads else ""}">'
            f'<span class="mk">{BOGSTAV[i]}</span><span>{html.escape(v)}'
            f'{" &nbsp;&#10003;" if i == plads else ""}</span></div>'
            for i, v in enumerate(valg))
        krop += (f'<div class="spm"><div class="hd"><span class="nr">{nr}.</span>'
                 f'{html.escape(tekst)}' + (f' <span style="color:#586074;'
                 f'font-weight:400;font-size:9.5pt">(figur {fignr})</span>'
                 if fignr else '') + '</div>'
                 f'{svar}<p class="hvorfor"><b>Hvorfor:</b> '
                 f'{html.escape(forkl)}</p></div>')

    doc = (f'<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
           f'<title>Retteark · samfundsfagstest</title>'
           f'<style>{RETTEARK_CSS}</style></head><body>'
           f'<h1>Retteark · samfundsfagstest</h1>'
           f'<p class="intro">Her er de {len(SPM)} spørgsmål med det rigtige '
           f'svar markeret med grønt og et flueben — og en linje om, '
           f'<b>hvorfor</b> det er det rigtige. Find dine egne svar, og '
           f'læs begrundelsen ved dem, du ikke fik. Det er dér, der er '
           f'noget at hente.</p>'
           f'<div class="tael"><b>Tæl dine rigtige.</b> Du har '
           f'{len(SPM)} spørgsmål i alt. Hvert rigtigt svar tæller ét. '
           f'Vil du have det i procent, så del dit antal rigtige med '
           f'{len(SPM)} og gang med 100 — det er præcis den slags '
           f'procentregning, I har haft i matematik i denne uge.</div>'
           f'<div class="note"><b>Figurerne</b> står i figurbilaget. '
           f'Er du i tvivl om et spørgsmål, så kig på figuren igen, før '
           f'du læser begrundelsen.</div>'
           + krop + '</body></html>')
    sti = os.path.join(UDMAPPE, 'retteark.html')
    open(sti, 'w', encoding='utf-8').write(doc)
    return sti


if __name__ == '__main__':
    print('skrevet:', os.path.relpath(skriv_docx(), ROD))
    print('skrevet:', os.path.relpath(skriv_bilag(), ROD))
    print('skrevet:', os.path.relpath(skriv_rettenoegle(), ROD))
    print('skrevet:', os.path.relpath(skriv_retteark(), ROD))
    print(f'  {len(SPM)} spørgsmål · {len(figurer)} figurer')
