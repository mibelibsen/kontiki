# -*- coding: utf-8 -*-
"""Beskaerer og komprimerer skaermbillederne fra GeoGebra.

Koeres EFTER claude/hent_geogebra_billeder.mjs og retter filerne paa
stedet. To ting er laert paa den haarde maade:

  * Vaerktoejslinjen oeverst og knapperne i hoejre side er ens paa hvert
    billede og stjaeler plads. De beskaeres vaek paa alt undtagen
    oversigtsbilledet, hvor de hoerer med.
  * `quantize` med faa farver goer billederne smaa, men MEDIANCUT med 96
    farver gjorde de blaa punkter og den orange trappe GRAA. FASTOCTREE
    med 256 holder paa de faa maettede farver, og filerne bliver
    alligevel en femtedel saa store.

    python3 claude/beskaer_geogebra_billeder.py
"""
import os
from PIL import Image

HER = os.path.dirname(os.path.abspath(__file__))
MAPPE = os.path.join(os.path.dirname(HER), 'billeder', 'geogebra')
MAKS = 1300
UDEN_VAERKTOEJ = (0, 168, 2250, 1400)      # kilden er 2400 x 1400

PLAN = {
 '1-vaelg-graf.png': None,
 '2-vinduet.png': (0, 0, 2400, 1330),
 '3-punkter.png': UDEN_VAERKTOEJ,
 '4-linje.png': UDEN_VAERKTOEJ,
 '4b-ligningen.png': None,
 '5-haeldning.png': UDEN_VAERKTOEJ,
 '6-egen-forskrift.png': UDEN_VAERKTOEJ,
 '7-rod.png': UDEN_VAERKTOEJ,
 '8-skaering.png': UDEN_VAERKTOEJ,
 '10-menu.png': (860, 0, 2400, 1300),
 '11-vaerdi.png': UDEN_VAERKTOEJ,
}

if __name__ == '__main__':
    i_alt = 0
    for navn, ramme in PLAN.items():
        sti = os.path.join(MAPPE, navn)
        im = Image.open(sti).convert('RGB')
        if ramme:
            im = im.crop(ramme)
        if im.width > MAKS:
            im = im.resize((MAKS, round(im.height * MAKS / im.width)),
                           Image.LANCZOS)
        im.quantize(colors=256, method=Image.FASTOCTREE,
                    dither=Image.NONE).save(sti, optimize=True)
        k = os.path.getsize(sti) // 1024
        i_alt += k
        print(f'{navn:24} {im.size[0]}x{im.size[1]}  {k} kB')
    print(f'i alt {i_alt} kB')
