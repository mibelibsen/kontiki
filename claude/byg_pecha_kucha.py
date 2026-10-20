# -*- coding: utf-8 -*-
"""Bygger vejledning/pecha-kucha-skabelon.pptx — en tom Pecha Kucha-skabelon.

Pecha Kucha er 20 slides, der hver staar praecis 20 sekunder og skifter af sig
selv. Det er den regel, der goer formen til noget: man kan ikke tale over tiden,
og man kan ikke staa og laese op af sit slide.

    python3 claude/byg_pecha_kucha.py

Scriptet kalder claude/byg_pecha_kucha.mjs, som laver raadaekket med
pptxgenjs, og retter derefter to ting i OOXML'en, som pptxgenjs ikke kan skrive:

  * <p:transition advTm="20000"/> paa hvert slide - de 20 sekunder.
  * En rigtig billedpladsholder (<p:ph type="pic"/>) i stedet for det
    tekstfelt, pptxgenjs laegger ind. Forskellen er, at PowerPoint saa viser
    "Indsaet billede" med et billedikon, og at et indsat billede lander i
    rammen af sig selv.

Selve .pptx'en er en bygget fil og ligger ikke i git - den bygges her.
"""
import os
import re
import shutil
import subprocess
import sys
import zipfile

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MJS = os.path.join(ROD, 'claude', 'byg_pecha_kucha.mjs')
UD = os.path.join(ROD, 'vejledning', 'pecha-kucha-skabelon.pptx')
# pptxgenjs saetter selv .pptx paa filnavnet, hvis det ikke er der i
# forvejen. Raafilen hedder derfor det samme med -raa foran endelsen.
RAA = UD[:-5] + '-raa.pptx'

SLIDES = 20
SEKUNDER = 20

# Slidet er 10 x 5,625 tommer i EMU (914400 EMU paa en tomme).
BREDDE, HOEJDE = 9144000, 5143500

# Billedpladsholderen i layoutet: fylder hele sliden, saa billedet gaar helt
# ud til kanten. Prompteteksten ses kun, naar man redigerer.
LAYOUT_PH = (
    '<p:sp><p:nvSpPr><p:cNvPr id="2" name="Billede"/>'
    '<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
    '<p:nvPr><p:ph type="pic" idx="2" hasCustomPrompt="1"/></p:nvPr></p:nvSpPr>'
    f'<p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{BREDDE}" cy="{HOEJDE}"/>'
    '</a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>'
    '<p:txBody><a:bodyPr anchor="ctr"/><a:lstStyle><a:lvl1pPr algn="ctr">'
    '<a:buNone/><a:defRPr sz="1400"><a:solidFill><a:srgbClr val="8A93A3"/>'
    '</a:solidFill></a:defRPr></a:lvl1pPr></a:lstStyle>'
    '<a:p><a:r><a:rPr lang="da-DK" dirty="0"/>'
    '<a:t>Indsæt billede</a:t></a:r></a:p></p:txBody></p:sp>')

# Den tomme pladsholder paa selve slidet. Den har ingen maal - den arver dem
# fra layoutet, saa alle 20 slides er ens, og en aendring ét sted slaar igennem.
SLIDE_PH = (
    '<p:sp><p:nvSpPr><p:cNvPr id="2" name="Billede"/>'
    '<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
    '<p:nvPr><p:ph type="pic" idx="2"/></p:nvPr></p:nvSpPr>'
    '<p:spPr/><p:txBody><a:bodyPr/><a:lstStyle/>'
    '<a:p><a:endParaRPr lang="da-DK" dirty="0"/></a:p></p:txBody></p:sp>')

# advTm er i millisekunder. advClick bliver staaende, saa et uheldigt klik ikke
# spoler frem, men tiden koerer af sig selv.
TRANSITION = (f'<p:transition spd="med" advClick="0" '
              f'advTm="{SEKUNDER * 1000}"/>')

SP = re.compile(r'<p:sp>.*?</p:sp>', re.S)


def en(xml, ny, hvad):
    """Erstatter den ene <p:sp>, pptxgenjs har lagt ind. Er der ikke praecis
    én, er daekket ikke det, vi tror, og saa skal der ikke rettes i blinde."""
    fundet = SP.findall(xml)
    assert len(fundet) == 1, f'{hvad}: fandt {len(fundet)} <p:sp>, ventede 1'
    return xml.replace(fundet[0], ny)


def byg():
    os.makedirs(os.path.dirname(UD), exist_ok=True)
    subprocess.run(['node', MJS, RAA], check=True)

    kilde = zipfile.ZipFile(RAA)
    navne = kilde.namelist()
    layout = next(n for n in navne if n.endswith('slideLayout2.xml'))
    slides = sorted(n for n in navne
                    if re.fullmatch(r'ppt/slides/slide\d+\.xml', n))
    assert len(slides) == SLIDES, f'{len(slides)} slides, ventede {SLIDES}'

    with zipfile.ZipFile(UD, 'w', zipfile.ZIP_DEFLATED) as ud:
        for navn in navne:
            data = kilde.read(navn)
            if navn == layout:
                data = en(data.decode(), LAYOUT_PH, 'layout').encode()
            elif navn in slides:
                x = en(data.decode(), SLIDE_PH, navn)
                # raekkefoelgen i <p:sld> er fast: cSld, clrMapOvr, transition.
                assert x.count('</p:clrMapOvr>') == 1, navn
                x = x.replace('</p:clrMapOvr>', '</p:clrMapOvr>' + TRANSITION)
                data = x.encode()
            ud.writestr(navn, data)
    kilde.close()
    os.remove(RAA)
    print(f'skrevet:  {UD}')
    print(f'{SLIDES} slides · {SEKUNDER} sekunder pr. slide · '
          f'{SLIDES * SEKUNDER // 60} min {SLIDES * SEKUNDER % 60} sek i alt')


if __name__ == '__main__':
    if shutil.which('node') is None:
        sys.exit('node mangler — pptxgenjs skal bruge den')
    byg()
